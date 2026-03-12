#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
import re
from dataclasses import dataclass, field
from pathlib import Path

from living_agent_common import read_text, write_text


SECTION_HEADER = "## PRIORITY_MAP (learning-loop maintained)"
DEFAULT_PRIORITY = 0.5


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
    priorities: dict[str, float] = field(default_factory=dict)

    def update(self, cells_visited: list[str], verification_passed: bool) -> None:
        reward = 1.0 if verification_passed else 0.0
        for cell in cells_visited:
            old = self.priorities.get(cell, DEFAULT_PRIORITY)
            new = old * (1.0 - self.alpha) + reward * self.alpha
            self.priorities[cell] = round(min(1.0, max(0.0, new)), 4)

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
        for cell in sorted(self.priorities):
            rows.append(f"{cell}: {self.priorities[cell]:.4f}")
        return "\n".join(rows)

    def save_to_soul(self, soul_text: str) -> str:
        section = self.render_section()
        pattern = re.compile(
            rf"{re.escape(SECTION_HEADER)}.*?(?=\n## |\Z)", re.S
        )
        if pattern.search(soul_text):
            return pattern.sub(section, soul_text).rstrip() + "\n"
        return soul_text.rstrip() + "\n\n" + section + "\n"

    @classmethod
    def load_from_soul(cls, soul_text: str, alpha: float = 0.1) -> "CellPriority":
        priorities: dict[str, float] = {}
        if SECTION_HEADER in soul_text:
            _, tail = soul_text.split(SECTION_HEADER, 1)
            lines = []
            for raw in tail.splitlines():
                if raw.startswith("## "):
                    break
                raw = raw.strip()
                if raw:
                    lines.append(raw)
            for line in lines:
                if ":" not in line:
                    continue
                cell, value = line.split(":", 1)
                try:
                    priorities[cell.strip()] = round(float(value.strip()), 4)
                except ValueError:
                    continue
        return cls(alpha=alpha, priorities=priorities)


def cmd_update(args: argparse.Namespace) -> int:
    soul_path = Path(args.soul)
    soul_text = read_text(soul_path)
    priority = CellPriority.load_from_soul(soul_text, alpha=args.alpha)
    cells = [cell.strip() for cell in args.cells_visited.split(",") if cell.strip()]
    priority.update(cells, parse_bool(args.verification_passed))
    write_text(soul_path, priority.save_to_soul(soul_text))
    payload = {
        "updated_cells": cells,
        "verification_passed": parse_bool(args.verification_passed),
        "alpha": args.alpha,
        "priorities": {cell: priority.query(cell) for cell in cells},
    }
    print(json.dumps(payload, indent=2))
    return 0


def cmd_query(args: argparse.Namespace) -> int:
    soul_text = read_text(Path(args.soul))
    priority = CellPriority.load_from_soul(soul_text, alpha=args.alpha)
    print(json.dumps({"cell": args.cell, "priority": priority.query(args.cell)}))
    return 0


def cmd_prompt_fragment(args: argparse.Namespace) -> int:
    soul_text = read_text(Path(args.soul))
    priority = CellPriority.load_from_soul(soul_text, alpha=args.alpha)
    cells = [cell.strip() for cell in args.available_cells.split(",") if cell.strip()]
    fragment = priority.inject_into_prompt(cells)
    payload = {"available_cells": cells, "fragment": fragment}
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(fragment)
    return 0


def cmd_simulate(args: argparse.Namespace) -> int:
    rng = random.Random(args.seed)
    priority = CellPriority(alpha=args.alpha)
    verified_cells = [f"R0_C{i}" for i in range(min(8, args.grid_size))]
    rejected_cells = [f"R1_C{i}" for i in range(min(8, args.grid_size))]
    neutral_cells = [f"R2_C{i}" for i in range(min(8, args.grid_size))]
    for _ in range(args.cycles):
        for cell in verified_cells:
            if rng.random() < 0.8:
                priority.update([cell], True)
        for cell in rejected_cells:
            if rng.random() < 0.8:
                priority.update([cell], False)
        for cell in neutral_cells:
            priority.update([cell], rng.random() < args.verify_rate)
    mean = lambda cells: round(sum(priority.query(c) for c in cells) / len(cells), 4)
    print(
        json.dumps(
            {
                "verified_mean_priority": mean(verified_cells),
                "rejected_mean_priority": mean(rejected_cells),
                "neutral_mean_priority": mean(neutral_cells),
                "priority_map_size": len(priority.priorities),
            },
            indent=2,
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Living Agent learning loop utilities")
    sub = parser.add_subparsers(dest="command", required=True)

    update = sub.add_parser("update")
    update.add_argument("--soul", required=True)
    update.add_argument("--cells-visited", required=True)
    update.add_argument("--verification-passed", required=True)
    update.add_argument("--alpha", type=float, default=0.1)
    update.set_defaults(func=cmd_update)

    query = sub.add_parser("query")
    query.add_argument("--soul", required=True)
    query.add_argument("--cell", required=True)
    query.add_argument("--alpha", type=float, default=0.1)
    query.set_defaults(func=cmd_query)

    frag = sub.add_parser("prompt-fragment")
    frag.add_argument("--soul", required=True)
    frag.add_argument("--available-cells", required=True)
    frag.add_argument("--alpha", type=float, default=0.1)
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
