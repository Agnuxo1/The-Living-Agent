#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
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

try:
    import numpy as np
except ImportError:  # pragma: no cover - optional dependency
    np = None


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
SIMILARITY_THRESHOLD = 0.7
PARENT_FANOUT_PENALTY = 0.0005


@dataclass
class Neighbor:
    direction: str
    target_cell: str
    target_fqn: str
    edge_type: str
    label: str
    provenance: str
    score: float | None = None

    def to_index(self) -> dict:
        payload = {
            "direction": self.direction,
            "target_cell": self.target_cell,
            "target_fqn": self.target_fqn,
            "edge_type": self.edge_type,
            "label": self.label,
            "provenance": self.provenance,
        }
        if self.score is not None:
            payload["score"] = round(self.score, 4)
        return payload


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
    dependency_depth: int
    dependency_count: int
    reverse_dependency_count: int
    keywords: list[str] = field(default_factory=list)
    overlay_summary: str = ""
    neighbors: list[Neighbor] = field(default_factory=list)

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
            "dependency_depth": self.dependency_depth,
            "dependency_count": self.dependency_count,
            "reverse_dependency_count": self.reverse_dependency_count,
            "keywords": self.keywords,
            "overlay_summary": self.overlay_summary,
            "neighbors": [neighbor.to_index() for neighbor in self.neighbors],
        }


@dataclass
class EmbeddingIndex:
    vectors: "np.ndarray"
    id_map: dict[str, str]
    path: Path

    def vector_for(self, fqn: str) -> "np.ndarray | None":
        key = self.id_map.get(fqn)
        if key is None:
            return None
        return self.vectors[int(key)]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def iso_mtime(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_optional_json(path: Path) -> dict | list | None:
    if not path.exists():
        return None
    return load_json(path)


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
    if not overlay_root.exists():
        return {}
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


def load_decl_embeddings() -> EmbeddingIndex | None:
    vectors_path = REPO_ROOT / "lean_index" / "embeddings.npy"
    id_map_path = REPO_ROOT / "lean_index" / "id_map.json"
    if np is None or not vectors_path.exists() or not id_map_path.exists():
        return None
    vectors = np.load(vectors_path)
    raw_id_map = load_json(id_map_path)
    if not isinstance(raw_id_map, dict):
        return None
    id_map = {value: key for key, value in raw_id_map.items() if isinstance(value, str)}
    return EmbeddingIndex(vectors=vectors, id_map=id_map, path=vectors_path)


def build_declaration_catalog() -> tuple[dict[str, dict], dict]:
    catalog_path = REPO_ROOT / "lean_index" / "catalog.json"
    dependencies_path = REPO_ROOT / "lean_index" / "dependencies.json"
    pagerank_path = REPO_ROOT / "lean_index" / "tags" / "decl_pagerank.json"
    catalog = load_json(catalog_path)
    deps_payload = load_json(dependencies_path)
    pagerank = load_optional_json(pagerank_path) or {}
    overlay = load_overlay()
    selected: dict[str, dict] = {}
    reverse_map: dict[str, set[str]] = {}
    dep_map = deps_payload["dependencies"]
    for row in catalog:
        module = row.get("module", "")
        if not module.startswith("HeytingLean."):
            continue
        dep_key = dependency_key(row, dep_map)
        if dep_key is None:
            continue
        fqn = dep_key.split("main::", 1)[1]
        if any(pattern in fqn for pattern in INTERNAL_PATTERNS):
            continue
        dependencies = [
            dep.split("main::", 1)[1]
            for dep in dep_map.get(dep_key, [])
            if dep.startswith("main::HeytingLean.")
        ]
        selected[fqn] = {
            "fqn": fqn,
            "module": module,
            "kind": row.get("kind", ""),
            "signature": normalize_whitespace(row.get("type", "")),
            "docstring": normalize_whitespace(row.get("docstring", "")),
            "pagerank": float(pagerank.get(fqn, 0.0)),
            "decl_file": f"lean/{module.replace('.', '/')}.lean",
            "dependencies": dependencies,
            "overlay": overlay.get(fqn, {}),
        }
        reverse_map.setdefault(fqn, set())
    for fqn, item in selected.items():
        for dep in item["dependencies"]:
            if dep in reverse_map:
                reverse_map[dep].add(fqn)
    for fqn, item in selected.items():
        item["reverse_dependencies"] = sorted(reverse_map.get(fqn, set()))
        item["all_neighbors"] = sorted(set(item["dependencies"]) | reverse_map.get(fqn, set()))
    metadata = {
        "catalog": {
            "path": str(catalog_path.relative_to(REPO_ROOT)),
            "sha256": sha256_file(catalog_path),
            "generated_at": iso_mtime(catalog_path),
            "declaration_count": len(catalog),
        },
        "dependencies": {
            "path": str(dependencies_path.relative_to(REPO_ROOT)),
            "sha256": sha256_file(dependencies_path),
            "generated_at": iso_mtime(dependencies_path),
        },
        "pagerank": {
            "available": pagerank_path.exists(),
            "path": str(pagerank_path.relative_to(REPO_ROOT)),
            "sha256": sha256_file(pagerank_path) if pagerank_path.exists() else None,
            "generated_at": iso_mtime(pagerank_path) if pagerank_path.exists() else None,
        },
        "overlay": {
            "available": bool(overlay),
            "path": "semantic_overlay/declarations/",
            "file_count": len(list((REPO_ROOT / "semantic_overlay" / "declarations").glob("*.json")))
            if (REPO_ROOT / "semantic_overlay" / "declarations").exists()
            else 0,
        },
    }
    return selected, metadata


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


def largest_component(selected: dict[str, dict]) -> set[str]:
    best: set[str] = set()
    seen: set[str] = set()
    for start in selected:
        if start in seen:
            continue
        component: set[str] = set()
        queue = deque([start])
        while queue:
            fqn = queue.popleft()
            if fqn in component:
                continue
            component.add(fqn)
            seen.add(fqn)
            queue.extend(neighbor for neighbor in selected[fqn]["all_neighbors"] if neighbor in selected)
        if len(component) > len(best):
            best = component
    return best


def select_connected_fqns(selected: dict[str, dict], capacity: int) -> tuple[list[str], dict[str, str | None]]:
    component = largest_component(selected)
    if not component:
        return [], {}
    ranked_component = sorted(
        component,
        key=lambda fqn: (-selected[fqn]["pagerank"], fqn),
    )
    root = ranked_component[0]
    chosen: list[str] = [root]
    chosen_set = {root}
    parent_map: dict[str, str | None] = {root: None}
    child_count: dict[str, int] = {root: 0}
    while len(chosen) < min(capacity, len(component)):
        frontier: list[tuple[float, float, int, str, str]] = []
        for parent in chosen:
            for neighbor in selected[parent]["all_neighbors"]:
                if neighbor not in component or neighbor in chosen_set:
                    continue
                frontier.append(
                    (
                        selected[neighbor]["pagerank"] - PARENT_FANOUT_PENALTY * child_count.get(parent, 0),
                        selected[neighbor]["pagerank"],
                        len(selected[neighbor]["all_neighbors"]),
                        neighbor,
                        parent,
                    )
                )
        if not frontier:
            break
        frontier.sort(key=lambda item: (-item[0], -item[1], -item[2], item[3], item[4]))
        _, _, _, chosen_fqn, parent = frontier[0]
        chosen.append(chosen_fqn)
        chosen_set.add(chosen_fqn)
        parent_map[chosen_fqn] = parent
        child_count[parent] = child_count.get(parent, 0) + 1
        child_count.setdefault(chosen_fqn, 0)
    return chosen, parent_map


def instantiate_cells(selected: dict[str, dict], chosen_fqns: list[str], rows: int, cols: int) -> list[Cell]:
    chosen_map = {fqn: selected[fqn] for fqn in chosen_fqns}
    depths = dependency_depths(chosen_map)
    max_depth = max((depths[fqn] for fqn in chosen_fqns), default=0)
    buckets: dict[int, list[str]] = {idx: [] for idx in range(rows)}
    for fqn in chosen_fqns:
        raw_depth = depths.get(fqn, 0)
        bucket = 0 if max_depth == 0 else round(raw_depth * (rows - 1) / max_depth)
        buckets[bucket].append(fqn)
    ordered: list[str] = []
    for row in range(rows):
        bucket_fqns = sorted(
            buckets[row],
            key=lambda fqn: (-selected[fqn]["pagerank"], fqn),
        )
        ordered.extend(bucket_fqns)
    cells: list[Cell] = []
    for idx, fqn in enumerate(ordered):
        row = idx // cols
        col = idx % cols
        item = selected[fqn]
        overlay = item["overlay"]
        keywords = overlay.get("keywords") or tokenize(
            f"{fqn} {item['docstring']} {overlay.get('summary', '')}"
        )[:8]
        cells.append(
            Cell(
                cell_id=f"HL_{idx + 1:03d}",
                row=row,
                col=col,
                fqn=fqn,
                module=item["module"],
                kind=item["kind"],
                signature=overlay.get("signature") or item["signature"],
                docstring=overlay.get("docstring") or item["docstring"],
                pagerank=item["pagerank"],
                decl_file=item["decl_file"],
                dependency_depth=depths.get(fqn, 0),
                dependency_count=len([dep for dep in item["dependencies"] if dep in chosen_map]),
                reverse_dependency_count=len([dep for dep in item["reverse_dependencies"] if dep in chosen_map]),
                keywords=sorted(set(keywords))[:12],
                overlay_summary=overlay.get("summary", ""),
            )
        )
    return cells


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


def dependency_edge_type(selected: dict[str, dict], source: str, target: str) -> tuple[str, str]:
    if target in selected[source]["dependencies"]:
        return "dependency", "dependency:imports"
    if target in selected[source]["reverse_dependencies"]:
        return "dependency", "dependency:reverse"
    raise ValueError(f"{source} and {target} do not share a real dependency edge")


def append_edge(
    cell: Cell,
    target: Cell,
    by_fqn: dict[str, Cell],
    *,
    edge_type: str,
    provenance: str,
    score: float | None = None,
    force_direction: bool = False,
) -> bool:
    direction = direction_from_delta(target.row - cell.row, target.col - cell.col) or "E"
    candidate = Neighbor(
        direction=direction,
        target_cell=target.cell_filename,
        target_fqn=target.fqn,
        edge_type=edge_type,
        label=target.title,
        provenance=provenance,
        score=score,
    )
    for idx, existing in enumerate(cell.neighbors):
        if existing.target_fqn == target.fqn:
            cell.neighbors[idx] = candidate
            return True
        if existing.direction != direction:
            continue
        existing_target = by_fqn[existing.target_fqn]
        candidate_priority = (
            1 if edge_type == "dependency" else 0,
            1 if provenance == "dependency:imports" else 0,
            -max(abs(target.row - cell.row), abs(target.col - cell.col)),
            score if score is not None else target.pagerank,
            target.pagerank,
            target.fqn,
        )
        existing_priority = (
            1 if existing.edge_type == "dependency" else 0,
            1 if existing.provenance == "dependency:imports" else 0,
            -max(abs(existing_target.row - cell.row), abs(existing_target.col - cell.col)),
            existing.score if existing.score is not None else existing_target.pagerank,
            existing_target.pagerank,
            existing.target_fqn,
        )
        if force_direction or candidate_priority > existing_priority:
            cell.neighbors[idx] = candidate
            return True
        return False
    cell.neighbors.append(candidate)
    return True


def add_neighbors(
    cells: list[Cell],
    selected: dict[str, dict],
    parent_map: dict[str, str | None],
    embeddings: EmbeddingIndex | None,
) -> None:
    by_fqn = {cell.fqn: cell for cell in cells}

    # Seed a real spanning tree so connectivity never depends on synthetic fallback edges.
    for child, parent in parent_map.items():
        if parent is None or child not in by_fqn or parent not in by_fqn:
            continue
        child_edge_type, child_provenance = dependency_edge_type(selected, child, parent)
        parent_edge_type, parent_provenance = dependency_edge_type(selected, parent, child)
        append_edge(by_fqn[child], by_fqn[parent], by_fqn, edge_type=child_edge_type, provenance=child_provenance)
        append_edge(by_fqn[parent], by_fqn[child], by_fqn, edge_type=parent_edge_type, provenance=parent_provenance)

    for cell in cells:
        real_neighbors = sorted(
            {
                neighbor
                for neighbor in selected[cell.fqn]["all_neighbors"]
                if neighbor in by_fqn and neighbor != cell.fqn
            },
            key=lambda fqn: (-selected[fqn]["pagerank"], fqn),
        )
        best_real_by_direction: dict[str, tuple[float, Cell, str, str]] = {}
        for neighbor_fqn in real_neighbors:
            if any(existing.target_fqn == neighbor_fqn for existing in cell.neighbors):
                continue
            target = by_fqn[neighbor_fqn]
            direction = direction_from_delta(target.row - cell.row, target.col - cell.col) or "E"
            edge_type, provenance = dependency_edge_type(selected, cell.fqn, neighbor_fqn)
            score = selected[neighbor_fqn]["pagerank"]
            existing = best_real_by_direction.get(direction)
            if existing is None or score > existing[0]:
                best_real_by_direction[direction] = (score, target, edge_type, provenance)
        for _, target, edge_type, provenance in best_real_by_direction.values():
            append_edge(cell, target, by_fqn, edge_type=edge_type, provenance=provenance)

        if embeddings is None:
            continue
        base_vector = embeddings.vector_for(cell.fqn)
        if base_vector is None:
            continue
        similarity_candidates: list[tuple[float, str, str]] = []
        for other in cells:
            if other.fqn == cell.fqn or any(existing.target_fqn == other.fqn for existing in cell.neighbors):
                continue
            other_vector = embeddings.vector_for(other.fqn)
            if other_vector is None:
                continue
            score = float(base_vector @ other_vector)
            if score >= SIMILARITY_THRESHOLD:
                direction = direction_from_delta(other.row - cell.row, other.col - cell.col) or "E"
                similarity_candidates.append((score, other.fqn, direction))
        similarity_candidates.sort(key=lambda item: (-item[0], item[1], item[2]))
        used_directions = {neighbor.direction for neighbor in cell.neighbors}
        similarity_edges_added = 0
        for score, target_fqn, direction in similarity_candidates:
            if direction in used_directions:
                continue
            append_edge(
                cell,
                by_fqn[target_fqn],
                by_fqn,
                edge_type="similarity",
                provenance=f"embedding:cosine>={SIMILARITY_THRESHOLD}",
                score=score,
            )
            used_directions.add(direction)
            similarity_edges_added += 1
            if similarity_edges_added >= 2:
                break

    ensure_connected_neighbors(cells, selected, by_fqn)

    for cell in cells:
        cell.neighbors.sort(key=lambda neighbor: (neighbor.direction, neighbor.target_cell))


def connected_components(cells: list[Cell]) -> list[set[str]]:
    graph = {cell.fqn: set() for cell in cells}
    for cell in cells:
        for neighbor in cell.neighbors:
            if neighbor.target_fqn not in graph:
                continue
            graph[cell.fqn].add(neighbor.target_fqn)
            graph[neighbor.target_fqn].add(cell.fqn)
    seen: set[str] = set()
    components: list[set[str]] = []
    for start in graph:
        if start in seen:
            continue
        queue = deque([start])
        component: set[str] = set()
        while queue:
            fqn = queue.popleft()
            if fqn in component:
                continue
            component.add(fqn)
            seen.add(fqn)
            queue.extend(graph[fqn] - component)
        components.append(component)
    return components


def ensure_connected_neighbors(
    cells: list[Cell],
    selected: dict[str, dict],
    by_fqn: dict[str, Cell],
) -> None:
    while True:
        components = connected_components(cells)
        if len(components) <= 1:
            return
        components.sort(key=len, reverse=True)
        main_component = components[0]
        repaired = False
        for component in components[1:]:
            candidates: list[tuple[int, int, float, str, str]] = []
            for source_fqn in component:
                source = by_fqn[source_fqn]
                source_used = {neighbor.direction for neighbor in source.neighbors}
                for target_fqn in selected[source_fqn]["all_neighbors"]:
                    if target_fqn not in main_component or target_fqn not in by_fqn:
                        continue
                    target = by_fqn[target_fqn]
                    direction = direction_from_delta(target.row - source.row, target.col - source.col) or "E"
                    candidates.append(
                        (
                            1 if direction in source_used else 0,
                            max(abs(target.row - source.row), abs(target.col - source.col)),
                            -selected[target_fqn]["pagerank"],
                            source_fqn,
                            target_fqn,
                        )
                    )
            if not candidates:
                continue
            for _, _, _, source_fqn, target_fqn in sorted(candidates):
                edge_type, provenance = dependency_edge_type(selected, source_fqn, target_fqn)
                if append_edge(
                    by_fqn[source_fqn],
                    by_fqn[target_fqn],
                    by_fqn,
                    edge_type=edge_type,
                    provenance=provenance,
                    force_direction=True,
                ):
                    repaired = True
                    break
        if not repaired:
            raise AssertionError("unable to restore connectivity with real dependency edges")


def render_cell(cell: Cell, rows: int) -> str:
    cell_type = "ENTRY" if cell.row == 0 else "SYNTHESIS" if cell.row == rows - 1 else "KNOWLEDGE"
    lines = [
        f"# Cell [{cell.row},{cell.col}] — {cell_type}",
        f"**FQN**: `{cell.fqn}`",
        f"**Module**: `{cell.module}`",
        f"**Kind**: `{cell.kind}`",
        f"**Centrality**: {cell.pagerank:.6f}",
        f"**Dependency Depth**: {cell.dependency_depth}",
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
    for neighbor in cell.neighbors:
        emoji = DIRECTION_EMOJI.get(neighbor.direction, "➡️")
        suffix = f" [{neighbor.edge_type}]"
        if neighbor.score is not None:
            suffix += f" {neighbor.score:.2f}"
        lines.append(f"- {emoji} **{neighbor.direction}**: [{neighbor.label}{suffix}]({neighbor.target_cell})")
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


def build_payload(
    cells: list[Cell],
    rows: int,
    cols: int,
    source_metadata: dict,
    embeddings: EmbeddingIndex | None,
    requested_top_n: int,
) -> dict:
    component_cells = len(cells)
    return {
        "generated_at": now_utc(),
        "rows": rows,
        "cols": cols,
        "requested_top_n": requested_top_n,
        "cell_count": component_cells,
        "sources": {
            **source_metadata,
            "embeddings": {
                "available": embeddings is not None,
                "path": str(embeddings.path.relative_to(REPO_ROOT)) if embeddings is not None else None,
                "sha256": sha256_file(embeddings.path) if embeddings is not None else None,
                "generated_at": iso_mtime(embeddings.path) if embeddings is not None else None,
                "similarity_threshold": SIMILARITY_THRESHOLD if embeddings is not None else None,
            },
        },
        "cells": [cell.to_index() for cell in cells],
    }


def validate_payload(payload: dict, selected: dict[str, dict], embeddings: EmbeddingIndex | None) -> dict:
    cells = payload["cells"]
    if not cells:
        raise AssertionError("grid builder produced zero cells")
    cell_names = {f"cell_R{cell['row']}_C{cell['col']}.md" for cell in cells}
    by_fqn = {cell["fqn"]: cell for cell in cells}
    by_name = {f"cell_R{cell['row']}_C{cell['col']}.md": cell["fqn"] for cell in cells}
    for cell in cells:
        fqn = cell["fqn"]
        if fqn not in selected:
            raise AssertionError(f"missing FQN from lean_index: {fqn}")
        if not cell["decl_file"].startswith("lean/"):
            raise AssertionError(f"unexpected declaration path: {cell['decl_file']}")
        directions = [neighbor["direction"] for neighbor in cell["neighbors"]]
        if len(directions) != len(set(directions)):
            raise AssertionError(f"duplicate compass directions for {fqn}: {directions}")
        for neighbor in cell["neighbors"]:
            target_cell = neighbor["target_cell"]
            target_fqn = neighbor["target_fqn"]
            if target_cell not in cell_names:
                raise AssertionError(f"neighbor target missing: {target_cell}")
            if by_name[target_cell] != target_fqn:
                raise AssertionError(f"neighbor FQN mismatch: {target_cell} != {target_fqn}")
            if target_fqn not in selected:
                raise AssertionError(f"neighbor FQN missing from lean_index: {target_fqn}")
            if neighbor["edge_type"] == "dependency":
                if target_fqn not in selected[fqn]["all_neighbors"]:
                    raise AssertionError(f"fake dependency edge: {fqn} -> {target_fqn}")
            elif neighbor["edge_type"] == "similarity":
                if embeddings is None:
                    raise AssertionError("similarity edge emitted without embeddings")
                base_vector = embeddings.vector_for(fqn)
                target_vector = embeddings.vector_for(target_fqn)
                if base_vector is None or target_vector is None:
                    raise AssertionError(f"similarity edge missing embeddings: {fqn} -> {target_fqn}")
                score = float(base_vector @ target_vector)
                if score < SIMILARITY_THRESHOLD:
                    raise AssertionError(f"similarity score below threshold: {fqn} -> {target_fqn} ({score})")
            else:
                raise AssertionError(f"unknown edge_type: {neighbor['edge_type']}")

    graph = {cell["fqn"]: set() for cell in cells}
    for cell in cells:
        for neighbor in cell["neighbors"]:
            graph[cell["fqn"]].add(neighbor["target_fqn"])
            graph[neighbor["target_fqn"]].add(cell["fqn"])
    seen: set[str] = set()
    queue = deque([cells[0]["fqn"]])
    while queue:
        fqn = queue.popleft()
        if fqn in seen:
            continue
        seen.add(fqn)
        queue.extend(graph[fqn] - seen)
    return {
        "cell_count": len(cells),
        "connected": len(seen) == len(cells),
        "embedding_edges_present": any(
            neighbor["edge_type"] == "similarity"
            for cell in cells
            for neighbor in cell["neighbors"]
        ),
        "pagerank_available": bool(payload["sources"]["pagerank"]["available"]),
        "overlay_available": bool(payload["sources"]["overlay"]["available"]),
    }


def write_install_script(out_root: Path) -> None:
    script = f"""#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${{BASH_SOURCE[0]}}")" && pwd)"
SRC="$SCRIPT_DIR"
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
cp "$SRC/verified_grid_index.json" "$DEST/verified_grid_index.json"
echo "Installed verified grid into {DEFAULT_LIVING_AGENT_ROOT}"
"""
    path = out_root / "install_verified_grid.sh"
    write_text(path, script)
    path.chmod(0o755)


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

    if args.rows <= 0 or args.cols <= 0:
        raise SystemExit("--rows and --cols must be positive")

    selected, source_metadata = build_declaration_catalog()
    embeddings = load_decl_embeddings()
    capacity = min(args.top_n, args.rows * args.cols)
    chosen_fqns, parent_map = select_connected_fqns(selected, capacity)
    cells = instantiate_cells(selected, chosen_fqns, args.rows, args.cols)
    add_neighbors(cells, selected, parent_map, embeddings)
    payload = build_payload(cells, args.rows, args.cols, source_metadata, embeddings, args.top_n)

    if args.dry_run:
        preview = {
            "cell_count": len(cells),
            "rows": args.rows,
            "cols": args.cols,
            "sample_fqns": [cell.fqn for cell in cells[:5]],
            "pagerank_available": payload["sources"]["pagerank"]["available"],
            "embeddings_available": payload["sources"]["embeddings"]["available"],
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
        result = validate_payload(payload, selected, embeddings)
        print(json.dumps(result, indent=2))
        return 0

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"Wrote {len(cells)} cells to {out_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
