#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from living_agent_common import (
    DEFAULT_GRID_ROOT,
    DEFAULT_LIVING_AGENT_ROOT,
    REPO_ROOT,
    load_json,
    normalize_whitespace,
    tokenize,
    write_json,
    write_text,
)


DIRECTION_EMOJI = {
    "N": "⬆️",
    "NE": "↗️",
    "E": "➡️",
    "SE": "↘️",
    "S": "⬇️",
    "SW": "↙️",
    "W": "⬅️",
    "NW": "↖️",
}
INTERNAL_PATTERNS = (
    ".casesOn",
    ".recOn",
    ".rec",
    ".brecOn",
    ".below",
    ".noConfusion",
    ".noConfusionType",
    ".ctor",
    ".match_",
    ".proof_",
    ".injEq",
    ".sizeOf",
    ".induct",
)


@dataclass
class Cell:
    cell_id: str
    row: int
    col: int
    fqn: str
    module: str
    kind: str
    signature: str
    docstring: str
    pagerank: float
    decl_file: str
    keywords: list[str] = field(default_factory=list)
    overlay_summary: str = ""
    neighbors: dict[str, dict] = field(default_factory=dict)

    @property
    def title(self) -> str:
        return self.fqn.split(".")[-1]

    @property
    def cell_filename(self) -> str:
        return f"cell_R{self.row}_C{self.col}.md"

    def to_index(self) -> dict:
        return {
            "cell_id": self.cell_id,
            "row": self.row,
            "col": self.col,
            "fqn": self.fqn,
            "module": self.module,
            "kind": self.kind,
            "signature": self.signature,
            "docstring": self.docstring,
            "pagerank": self.pagerank,
            "decl_file": self.decl_file,
            "keywords": self.keywords,
            "overlay_summary": self.overlay_summary,
            "neighbors": self.neighbors,
        }


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def catalog_entries() -> dict[str, dict]:
    catalog = load_json(REPO_ROOT / "lean_index" / "catalog.json")
    pagerank = load_json(REPO_ROOT / "lean_index" / "tags" / "decl_pagerank.json")
    deps = load_json(REPO_ROOT / "lean_index" / "dependencies.json")
    overlay = load_overlay()
    selected: dict[str, dict] = {}
    for row in catalog:
        module = row.get("module", "")
        if not module.startswith("HeytingLean."):
            continue
        dep_key = dependency_key(row, deps["dependencies"])
        if dep_key is None:
            continue
        fqn = dep_key.split("main::", 1)[1]
        if any(pattern in fqn for pattern in INTERNAL_PATTERNS):
            continue
        selected[fqn] = {
            "fqn": fqn,
            "module": module,
            "kind": row.get("kind", ""),
            "signature": normalize_whitespace(row.get("type", "")),
            "docstring": normalize_whitespace(row.get("docstring", "")),
            "pagerank": float(pagerank.get(fqn, 0.0)),
            "decl_file": f"lean/{module.replace('.', '/')}.lean",
            "dependencies": [
                dep.split("main::", 1)[1]
                for dep in deps["dependencies"].get(dep_key, [])
                if dep.startswith("main::HeytingLean.")
            ],
            "overlay": overlay.get(fqn, {}),
        }
    return selected


def dependency_key(row: dict, dep_map: dict[str, list[str]]) -> str | None:
    candidates = [
        f"main::{row.get('name', '')}",
        f"main::{row.get('module', '')}.{row.get('name', '')}",
    ]
    for candidate in candidates:
        if candidate in dep_map:
            return candidate
    return None


def load_overlay() -> dict[str, dict]:
    overlay_root = REPO_ROOT / "semantic_overlay" / "declarations"
    out: dict[str, dict] = {}
    for path in overlay_root.glob("*.json"):
        payload = load_json(path)
        declarations = payload.get("declarations", {})
        if not isinstance(declarations, dict):
            continue
        for name, item in declarations.items():
            if not isinstance(item, dict):
                continue
            semantic = item.get("semantic", {}) or {}
            extracted = item.get("extracted", {}) or {}
            out[name] = {
                "summary": normalize_whitespace(semantic.get("description", "")),
                "keywords": list(semantic.get("keywords", []) or []),
                "signature": normalize_whitespace(extracted.get("signature", "")),
                "docstring": normalize_whitespace(extracted.get("docstring", "")),
            }
    return out


def dependency_depths(selected: dict[str, dict]) -> dict[str, int]:
    memo: dict[str, int] = {}
    visiting: set[str] = set()

    def visit(fqn: str) -> int:
        if fqn in memo:
            return memo[fqn]
        if fqn in visiting:
            return 0
        visiting.add(fqn)
        deps = [dep for dep in selected[fqn]["dependencies"] if dep in selected]
        depth = 0 if not deps else 1 + max(visit(dep) for dep in deps)
        memo[fqn] = depth
        visiting.remove(fqn)
        return depth

    for fqn in selected:
        visit(fqn)
    return memo


def select_cells(selected: dict[str, dict], rows: int, cols: int, top_n: int) -> list[Cell]:
    capacity = min(top_n, rows * cols)
    depths = dependency_depths(selected)
    ranked = sorted(
        selected.values(),
        key=lambda item: (-item["pagerank"], depths.get(item["fqn"], 0), item["fqn"]),
    )[:capacity]
    max_depth = max((depths[item["fqn"]] for item in ranked), default=0)
    buckets: dict[int, list[dict]] = {idx: [] for idx in range(rows)}
    for item in ranked:
        raw_depth = depths[item["fqn"]]
        bucket = 0 if max_depth == 0 else round(raw_depth * (rows - 1) / max_depth)
        buckets[bucket].append(item)
    ordered: list[dict] = []
    for row in range(rows):
        bucket_items = sorted(
            buckets[row],
            key=lambda item: (-item["pagerank"], item["fqn"]),
        )
        ordered.extend(bucket_items)
    cells: list[Cell] = []
    for idx, item in enumerate(ordered):
        row = idx // cols
        col = idx % cols
        overlay = item["overlay"]
        keywords = overlay.get("keywords") or tokenize(
            f"{item['fqn']} {item['docstring']} {overlay.get('summary', '')}"
        )[:8]
        cells.append(
            Cell(
                cell_id=f"HL_{idx + 1:03d}",
                row=row,
                col=col,
                fqn=item["fqn"],
                module=item["module"],
                kind=item["kind"],
                signature=overlay.get("signature") or item["signature"],
                docstring=overlay.get("docstring") or item["docstring"],
                pagerank=item["pagerank"],
                decl_file=item["decl_file"],
                keywords=sorted(set(keywords))[:12],
                overlay_summary=overlay.get("summary", ""),
            )
        )
    return cells


def add_neighbors(cells: list[Cell], selected: dict[str, dict]) -> None:
    by_fqn = {cell.fqn: cell for cell in cells}
    ordered_cells = sorted(cells, key=lambda cell: (cell.row, cell.col))
    order_index = {cell.fqn: idx for idx, cell in enumerate(ordered_cells)}
    reverse: dict[str, set[str]] = {cell.fqn: set() for cell in cells}
    for cell in cells:
        for dep in selected[cell.fqn]["dependencies"]:
            if dep in reverse:
                reverse[dep].add(cell.fqn)
    token_sets = {
        cell.fqn: set(tokenize(f"{cell.fqn} {cell.docstring} {' '.join(cell.keywords)}"))
        for cell in cells
    }
    for cell in cells:
        linked = set()
        for dep in selected[cell.fqn]["dependencies"]:
            if dep in by_fqn:
                linked.add(dep)
        linked |= reverse[cell.fqn]
        if len(linked) < 4:
            scores: list[tuple[float, str]] = []
            base_tokens = token_sets[cell.fqn]
            for other in cells:
                if other.fqn == cell.fqn or other.fqn in linked:
                    continue
                other_tokens = token_sets[other.fqn]
                if not base_tokens or not other_tokens:
                    continue
                score = len(base_tokens & other_tokens) / len(base_tokens | other_tokens)
                if score >= 0.12:
                    scores.append((score, other.fqn))
            for _, other_fqn in sorted(scores, reverse=True)[:4]:
                linked.add(other_fqn)
        best_for_direction: dict[str, tuple[float, Cell, str, float]] = {}
        for target_fqn in linked:
            target = by_fqn[target_fqn]
            direction = direction_from_delta(target.row - cell.row, target.col - cell.col)
            if direction is None:
                continue
            distance = math.hypot(target.row - cell.row, target.col - cell.col)
            edge_type = (
                "dependency"
                if target_fqn in selected[cell.fqn]["dependencies"] or cell.fqn in selected[target_fqn]["dependencies"]
                else "similarity"
            )
            similarity = 0.0
            if edge_type == "similarity":
                base_tokens = token_sets[cell.fqn]
                target_tokens = token_sets[target_fqn]
                similarity = len(base_tokens & target_tokens) / max(1, len(base_tokens | target_tokens))
            existing = best_for_direction.get(direction)
            if existing is None or distance < existing[0]:
                best_for_direction[direction] = (distance, target, edge_type, similarity)
        for direction, (_, target, edge_type, similarity) in best_for_direction.items():
            cell.neighbors[direction] = {
                "target_cell": target.cell_filename,
                "target_fqn": target.fqn,
                "edge_type": edge_type,
                "score": round(similarity, 4),
                "label": target.title,
            }
        # Ensure the exported graph stays connected by chaining adjacent grid cells as
        # low-priority similarity edges when the structural graph is sparse.
        for offset in (-1, 1):
            target_idx = order_index[cell.fqn] + offset
            if not (0 <= target_idx < len(ordered_cells)):
                continue
            target = ordered_cells[target_idx]
            direction = direction_from_delta(target.row - cell.row, target.col - cell.col)
            if direction is None or direction in cell.neighbors:
                direction = next(
                    (candidate for candidate in ["E", "SE", "S", "NE", "W", "SW", "N", "NW"] if candidate not in cell.neighbors),
                    None,
                )
            if direction is None:
                continue
            base_tokens = token_sets[cell.fqn]
            target_tokens = token_sets[target.fqn]
            similarity = len(base_tokens & target_tokens) / max(1, len(base_tokens | target_tokens))
            cell.neighbors[direction] = {
                "target_cell": target.cell_filename,
                "target_fqn": target.fqn,
                "edge_type": "similarity",
                "score": round(similarity, 4),
                "label": target.title,
            }


def direction_from_delta(dr: int, dc: int) -> str | None:
    sr = 0 if dr == 0 else (1 if dr > 0 else -1)
    sc = 0 if dc == 0 else (1 if dc > 0 else -1)
    mapping = {
        (-1, 0): "N",
        (-1, 1): "NE",
        (0, 1): "E",
        (1, 1): "SE",
        (1, 0): "S",
        (1, -1): "SW",
        (0, -1): "W",
        (-1, -1): "NW",
    }
    return mapping.get((sr, sc))


def render_cell(cell: Cell, rows: int) -> str:
    cell_type = "ENTRY" if cell.row == 0 else "SYNTHESIS" if cell.row == rows - 1 else "KNOWLEDGE"
    lines = [
        f"# Cell [{cell.row},{cell.col}] — {cell_type}",
        f"**FQN**: `{cell.fqn}`",
        f"**Module**: `{cell.module}`",
        f"**Kind**: `{cell.kind}`",
        f"**Centrality**: {cell.pagerank:.6f}",
        "",
        "## Topic",
        f"**Declaration**: {cell.title}",
        f"**Signature**: `{cell.signature}`" if cell.signature else "**Signature**: unavailable",
        "",
        cell.docstring or cell.overlay_summary or "No docstring available; inspect the Lean declaration directly.",
        "",
        "## Keywords",
        ", ".join(cell.keywords[:12]) if cell.keywords else "No overlay keywords available.",
        "",
        "---",
        "## Navigation (real dependency / similarity edges)",
    ]
    for direction in ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]:
        neighbor = cell.neighbors.get(direction)
        if neighbor is None:
            continue
        emoji = DIRECTION_EMOJI[direction]
        label = neighbor["label"]
        target = neighbor["target_cell"]
        edge_type = neighbor["edge_type"]
        suffix = f" [{edge_type}]"
        lines.append(f"- {emoji} **{direction}**: [{label}{suffix}]({target})")
    return "\n".join(lines) + "\n"


def render_grid_index(cells: list[Cell], rows: int, cols: int) -> str:
    lookup = {(cell.row, cell.col): cell for cell in cells}
    lines = ["# Verified Knowledge Grid Index", f"**Dimensions**: {rows}×{cols}", ""]
    lines.append("| | " + " | ".join(f"C{c}" for c in range(cols)) + " |")
    lines.append("|---" * (cols + 1) + "|")
    for row in range(rows):
        row_cells = []
        for col in range(cols):
            cell = lookup.get((row, col))
            if cell is None:
                row_cells.append(" ")
                continue
            icon = "🚀" if row == 0 else "📝" if row == rows - 1 else "📚"
            row_cells.append(f"[{icon}](grid/{cell.cell_filename})")
        lines.append(f"| **R{row}** | " + " | ".join(row_cells) + " |")
    return "\n".join(lines) + "\n"


def write_install_script(out_root: Path) -> None:
    script = f"""#!/usr/bin/env bash
set -euo pipefail
SRC="{out_root}"
DEST="{DEFAULT_LIVING_AGENT_ROOT / 'knowledge' / 'grid'}"
DEST_INDEX="{DEFAULT_LIVING_AGENT_ROOT / 'knowledge' / 'grid_index.md'}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
if [ -d "$DEST" ]; then
  mv "$DEST" "${{DEST}}.bak.$STAMP"
fi
mkdir -p "$(dirname "$DEST")"
mkdir -p "$DEST"
cp -a "$SRC/grid/." "$DEST/"
cp "$SRC/grid_index.md" "$DEST_INDEX"
echo "Installed verified grid into {DEFAULT_LIVING_AGENT_ROOT}"
"""
    path = out_root / "install_verified_grid.sh"
    write_text(path, script)
    path.chmod(0o755)


def validate_output(index_path: Path) -> dict:
    payload = load_json(index_path)
    cells = payload["cells"]
    cell_names = {f"cell_R{cell['row']}_C{cell['col']}.md" for cell in cells}
    for cell in cells:
        assert cell["fqn"].startswith("HeytingLean."), cell["fqn"]
        assert cell["decl_file"].startswith("lean/"), cell["decl_file"]
        for neighbor in cell["neighbors"].values():
            assert neighbor["target_cell"] in cell_names
            assert neighbor["target_fqn"].startswith("HeytingLean.")
    graph = {cell["cell_id"]: [] for cell in cells}
    by_name = {f"cell_R{cell['row']}_C{cell['col']}.md": cell["cell_id"] for cell in cells}
    for cell in cells:
        for neighbor in cell["neighbors"].values():
            graph[cell["cell_id"]].append(by_name[neighbor["target_cell"]])
    seen = set()
    queue = deque([cells[0]["cell_id"]]) if cells else deque()
    while queue:
        node = queue.popleft()
        if node in seen:
            continue
        seen.add(node)
        queue.extend(graph[node])
    return {"cell_count": len(cells), "connected": len(seen) == len(cells)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a verified Living Agent knowledge grid")
    parser.add_argument("--rows", type=int, default=16)
    parser.add_argument("--cols", type=int, default=16)
    parser.add_argument("--top-n", type=int, default=256)
    parser.add_argument("--output-root", default=str(DEFAULT_GRID_ROOT))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    selected = catalog_entries()
    cells = select_cells(selected, args.rows, args.cols, args.top_n)
    add_neighbors(cells, selected)
    payload = {
        "generated_at": now_utc(),
        "rows": args.rows,
        "cols": args.cols,
        "cell_count": len(cells),
        "cells": [cell.to_index() for cell in cells],
    }
    if args.dry_run:
        preview = {
            "cell_count": len(cells),
            "rows": args.rows,
            "cols": args.cols,
            "sample_fqns": [cell.fqn for cell in cells[:5]],
        }
        print(json.dumps(preview, indent=2))
        return 0

    out_root = Path(args.output_root)
    grid_dir = out_root / "grid"
    grid_dir.mkdir(parents=True, exist_ok=True)
    for cell in cells:
        write_text(grid_dir / cell.cell_filename, render_cell(cell, args.rows))
    write_text(out_root / "grid_index.md", render_grid_index(cells, args.rows, args.cols))
    write_json(out_root / "verified_grid_index.json", payload)
    write_install_script(out_root)
    if args.validate:
        result = validate_output(out_root / "verified_grid_index.json")
        print(json.dumps(result, indent=2))
        return 0
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"Wrote {len(cells)} cells to {out_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
