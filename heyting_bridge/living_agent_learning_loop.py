#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
from dataclasses import dataclass, field
from pathlib import Path

from living_agent_common import read_text, write_text


SECTION_HEADER = "## PRIORITY_MAP (learning-loop maintained)"
EVIDENCE_HEADER = "## PRIORITY_EVIDENCE (learning-loop maintained)"
DEFAULT_PRIORITY = 0.5
DEFAULT_MAX_CELLS = 256
CELL_NAME_RE = re.compile(r"^R\d+_C\d+$")


def parse_bool(value: str) -> bool:
    lowered = value.strip().lower()
    if lowered in {"1", "true", "yes", "y"}:
        return True
    if lowered in {"0", "false", "no", "n"}:
        return False
    raise ValueError(f"expected boolean value, got {value!r}")


@dataclass
class CellPriority:
    alpha: float = 0.1
    max_cells: int = DEFAULT_MAX_CELLS
    priorities: dict[str, float] = field(default_factory=dict)
    evidence: dict[str, dict[str, object]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not 0.0 < self.alpha <= 1.0:
            raise ValueError(f"alpha must lie in (0, 1], got {self.alpha!r}")
        if self.max_cells <= 0:
            raise ValueError(f"max_cells must be positive, got {self.max_cells!r}")

    def compact(self) -> None:
        while len(self.priorities) > self.max_cells:
            oldest = next(iter(self.priorities))
            self.priorities.pop(oldest, None)
            self.evidence.pop(oldest, None)

    def update(
        self,
        cells_visited: list[str],
        verification_passed: bool,
        *,
        verification_report_sha256: str | None = None,
        verification_report_path: str | None = None,
    ) -> None:
        reward = 1.0 if verification_passed else 0.0
        for cell in cells_visited:
            if not CELL_NAME_RE.fullmatch(cell):
                continue
            old = self.priorities.get(cell, DEFAULT_PRIORITY)
            new = old * (1.0 - self.alpha) + reward * self.alpha
            if cell in self.priorities:
                self.priorities.pop(cell)
            self.priorities[cell] = round(min(1.0, max(0.0, new)), 4)
            if verification_report_sha256:
                self.evidence[cell] = {
                    "verification_passed": verification_passed,
                    "verification_report_sha256": verification_report_sha256,
                    "verification_report_path": verification_report_path,
                }
        self.compact()

    def query(self, cell: str) -> float:
        return round(self.priorities.get(cell, DEFAULT_PRIORITY), 4)

    def inject_into_prompt(self, available_cells: list[str]) -> str:
        lines = []
        for cell in available_cells:
            value = self.query(cell)
            if value >= 0.6:
                lines.append(
                    f"  {cell}: HIGH PRIORITY (past verified papers used this region)"
                )
            elif value <= 0.4:
                lines.append(
                    f"  {cell}: LOW PRIORITY (past papers from here were rejected)"
                )
            else:
                lines.append(f"  {cell}: NEUTRAL PRIORITY ({value:.2f})")
        return "\n".join(lines)

    def render_section(self) -> str:
        rows = [SECTION_HEADER]
        for cell, value in self.priorities.items():
            rows.append(f"{cell}: {value:.4f}")
        return "\n".join(rows)

    def render_evidence_section(self) -> str:
        rows = [EVIDENCE_HEADER]
        for cell, payload in self.evidence.items():
            rows.append(f"{cell}: {json.dumps(payload, sort_keys=True)}")
        return "\n".join(rows)

    def _replace_section(self, soul_text: str, header: str, section: str) -> str:
        pattern = re.compile(rf"{re.escape(header)}.*?(?=\n## |\Z)", re.S)
        if pattern.search(soul_text):
            return pattern.sub(section, soul_text)
        return soul_text.rstrip() + "\n\n" + section + "\n"

    def save_to_soul(self, soul_text: str) -> str:
        updated = self._replace_section(soul_text, SECTION_HEADER, self.render_section())
        updated = self._replace_section(updated, EVIDENCE_HEADER, self.render_evidence_section())
        return updated.rstrip() + "\n"

    @staticmethod
    def _parse_section_lines(soul_text: str, header: str) -> list[str]:
        if header not in soul_text:
            return []
        _, tail = soul_text.split(header, 1)
        lines = []
        for raw in tail.splitlines():
            if raw.startswith("## "):
                break
            raw = raw.strip()
            if raw:
                lines.append(raw)
        return lines

    @classmethod
    def load_from_soul(
        cls,
        soul_text: str,
        alpha: float = 0.1,
        max_cells: int = DEFAULT_MAX_CELLS,
    ) -> "CellPriority":
        priorities: dict[str, float] = {}
        evidence: dict[str, dict[str, object]] = {}
        for line in cls._parse_section_lines(soul_text, SECTION_HEADER):
            if ":" not in line:
                continue
            cell, value = line.split(":", 1)
            try:
                parsed_value = round(float(value.strip()), 4)
            except ValueError:
                continue
            if CELL_NAME_RE.fullmatch(cell.strip()):
                priorities[cell.strip()] = parsed_value
        for line in cls._parse_section_lines(soul_text, EVIDENCE_HEADER):
            if ":" not in line:
                continue
            cell, payload = line.split(":", 1)
            cell = cell.strip()
            if not CELL_NAME_RE.fullmatch(cell):
                continue
            try:
                parsed = json.loads(payload.strip())
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                evidence[cell] = parsed
        priority = cls(alpha=alpha, max_cells=max_cells, priorities=priorities, evidence=evidence)
        priority.compact()
        return priority


def verification_report_sha256(report_path: Path | None) -> str | None:
    if report_path is None or not report_path.exists():
        return None
    return hashlib.sha256(report_path.read_bytes()).hexdigest()


def simulate_priorities(
    *,
    cycles: int,
    grid_size: int,
    verify_rate: float,
    alpha: float,
    seed: int,
) -> dict[str, float]:
    rng = random.Random(seed)
    priority = CellPriority(alpha=alpha, max_cells=grid_size)
    cols = max(1, min(16, grid_size))
    rows = max(1, (grid_size + cols - 1) // cols)
    verified_cells = [f"R0_C{i}" for i in range(min(8, grid_size))]
    rejected_cells = [f"R1_C{i}" for i in range(min(8, grid_size))]
    neutral_cells = [f"R2_C{i}" for i in range(min(8, grid_size))]
    for _ in range(cycles):
        for cell in verified_cells:
            if rng.random() < 0.8:
                priority.update([cell], True)
        for cell in rejected_cells:
            if rng.random() < 0.8:
                priority.update([cell], False)
        for cell in neutral_cells:
            priority.update([cell], rng.random() < 0.5)
        exploratory_updates = max(1, int(round(grid_size * verify_rate / 32.0)))
        for _ in range(exploratory_updates):
            random_cell = f"R{rng.randrange(rows)}_C{rng.randrange(cols)}"
            priority.update([random_cell], rng.random() < verify_rate)
    mean = lambda cells: round(sum(priority.query(c) for c in cells) / len(cells), 4)
    return {
        "verified_mean_priority": mean(verified_cells),
        "rejected_mean_priority": mean(rejected_cells),
        "neutral_mean_priority": mean(neutral_cells),
        "priority_map_size": len(priority.priorities),
    }


def cmd_update(args: argparse.Namespace) -> int:
    soul_path = Path(args.soul)
    soul_text = read_text(soul_path)
    priority = CellPriority.load_from_soul(soul_text, alpha=args.alpha, max_cells=args.max_cells)
    cells = [
        cell.strip()
        for cell in args.cells_visited.split(",")
        if cell.strip() and CELL_NAME_RE.fullmatch(cell.strip())
    ]
    report_path = Path(args.verification_report) if args.verification_report else None
    report_sha256 = verification_report_sha256(report_path)
    verification_passed = parse_bool(args.verification_passed)
    priority.update(
        cells,
        verification_passed,
        verification_report_sha256=report_sha256,
        verification_report_path=str(report_path) if report_path else None,
    )
    write_text(soul_path, priority.save_to_soul(soul_text))
    payload = {
        "updated_cells": cells,
        "verification_passed": verification_passed,
        "alpha": args.alpha,
        "verification_report_sha256": report_sha256,
        "priorities": {cell: priority.query(cell) for cell in cells},
    }
    print(json.dumps(payload, indent=2))
    return 0


def cmd_query(args: argparse.Namespace) -> int:
    soul_text = read_text(Path(args.soul))
    priority = CellPriority.load_from_soul(soul_text, alpha=args.alpha, max_cells=args.max_cells)
    print(
        json.dumps(
            {
                "cell": args.cell,
                "priority": priority.query(args.cell),
                "evidence": priority.evidence.get(args.cell),
            }
        )
    )
    return 0


def cmd_prompt_fragment(args: argparse.Namespace) -> int:
    soul_text = read_text(Path(args.soul))
    priority = CellPriority.load_from_soul(soul_text, alpha=args.alpha, max_cells=args.max_cells)
    cells = [
        cell.strip()
        for cell in args.available_cells.split(",")
        if cell.strip() and CELL_NAME_RE.fullmatch(cell.strip())
    ]
    fragment = priority.inject_into_prompt(cells)
    payload = {"available_cells": cells, "fragment": fragment}
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(fragment)
    return 0


def cmd_simulate(args: argparse.Namespace) -> int:
    print(json.dumps(simulate_priorities(
        cycles=args.cycles,
        grid_size=args.grid_size,
        verify_rate=args.verify_rate,
        alpha=args.alpha,
        seed=args.seed,
    ), indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Living Agent learning loop utilities")
    sub = parser.add_subparsers(dest="command", required=True)

    update = sub.add_parser("update")
    update.add_argument("--soul", required=True)
    update.add_argument("--cells-visited", required=True)
    update.add_argument("--verification-passed", required=True)
    update.add_argument("--verification-report")
    update.add_argument("--alpha", type=float, default=0.1)
    update.add_argument("--max-cells", type=int, default=DEFAULT_MAX_CELLS)
    update.set_defaults(func=cmd_update)

    query = sub.add_parser("query")
    query.add_argument("--soul", required=True)
    query.add_argument("--cell", required=True)
    query.add_argument("--alpha", type=float, default=0.1)
    query.add_argument("--max-cells", type=int, default=DEFAULT_MAX_CELLS)
    query.set_defaults(func=cmd_query)

    frag = sub.add_parser("prompt-fragment")
    frag.add_argument("--soul", required=True)
    frag.add_argument("--available-cells", required=True)
    frag.add_argument("--alpha", type=float, default=0.1)
    frag.add_argument("--max-cells", type=int, default=DEFAULT_MAX_CELLS)
    frag.add_argument("--json", action="store_true")
    frag.set_defaults(func=cmd_prompt_fragment)

    simulate = sub.add_parser("simulate")
    simulate.add_argument("--cycles", type=int, default=50)
    simulate.add_argument("--grid-size", type=int, default=256)
    simulate.add_argument("--verify-rate", type=float, default=0.3)
    simulate.add_argument("--alpha", type=float, default=0.1)
    simulate.add_argument("--seed", type=int, default=7)
    simulate.add_argument("--json", action="store_true")
    simulate.set_defaults(func=cmd_simulate)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
