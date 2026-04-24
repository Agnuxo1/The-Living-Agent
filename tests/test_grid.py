"""Tests for living_agent.grid."""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from living_agent.grid import (
    DIRECTIONS,
    generate_cell,
    generate_grid,
    get_cell_type,
    load_cell_links,
    neighbours,
    parse_grid_position,
)


def test_directions_has_eight_distinct_entries():
    assert len(DIRECTIONS) == 8
    vectors = set(DIRECTIONS.values())
    assert len(vectors) == 8
    assert (0, 0) not in vectors


def test_neighbours_interior_cell_has_eight():
    n = neighbours(5, 5, 16, 16)
    assert len(n) == 8


def test_neighbours_corner_cell_has_three():
    assert len(neighbours(0, 0, 16, 16)) == 3
    assert len(neighbours(0, 15, 16, 16)) == 3
    assert len(neighbours(15, 0, 16, 16)) == 3
    assert len(neighbours(15, 15, 16, 16)) == 3


def test_neighbours_edge_cell_has_five():
    # Non-corner edge cells
    assert len(neighbours(0, 5, 16, 16)) == 5
    assert len(neighbours(15, 5, 16, 16)) == 5
    assert len(neighbours(5, 0, 16, 16)) == 5
    assert len(neighbours(5, 15, 16, 16)) == 5


def test_generate_grid_creates_256_cells(tmp_path: Path):
    out = generate_grid(tmp_path, rows=16, cols=16, seed=42)
    cells = list(out.glob("cell_R*_C*.md"))
    assert len(cells) == 256


def test_grid_index_lists_all_cells(tmp_path: Path):
    generate_grid(tmp_path, rows=16, cols=16, seed=42)
    index = (tmp_path / "grid_index.md").read_text(encoding="utf-8")
    for r in range(16):
        for c in range(16):
            assert f"cell_R{r}_C{c}.md" in index


def test_cell_types_entry_and_synthesis_rows():
    assert get_cell_type(0, 3, 16, 16) == "ENTRY"
    assert get_cell_type(15, 7, 16, 16) == "SYNTHESIS"
    assert get_cell_type(8, 8, 16, 16) == "MUTATION_CHAMBER"


def test_generated_cell_contains_navigation_links():
    content = generate_cell(5, 5, 16, 16)
    links = load_cell_links(content)
    # 8 neighbours for an interior cell
    assert len(links) == 8
    # All links refer to cell_R*_C*.md
    for _label, href in links:
        assert re.match(r"cell_R\d+_C\d+\.md$", href)


def test_round_trip_read_from_disk(tmp_path: Path):
    out = generate_grid(tmp_path, rows=16, cols=16, seed=7)
    cell = (out / "cell_R0_C0.md").read_text(encoding="utf-8")
    assert "[0,0]" in cell
    assert "ENTRY" in cell
    links = load_cell_links(cell)
    # Corner -> 3 neighbour links
    assert len(links) == 3


def test_parse_grid_position():
    assert parse_grid_position("cell_R3_C7.md") == (3, 7)
    assert parse_grid_position("knowledge/grid/cell_R15_C0.md") == (15, 0)
    assert parse_grid_position("garbage") == (0, 0)
