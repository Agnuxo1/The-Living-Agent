"""Chess-Grid generator for The Living Agent.

Generates an N x M grid of interconnected Markdown knowledge cells.
Each cell has up to 8 directional links to its neighbours.
"""
from __future__ import annotations

import os
import random
import re
from pathlib import Path
from typing import Dict, List, Tuple

RESEARCH_DOMAINS: List[str] = [
    "DNA-based logic gates and their computational limits",
    "Protein folding as a search algorithm",
    "Neural organoid computing architectures",
    "Synthetic biology circuits for Boolean operations",
    "Bacterial quorum sensing as distributed consensus",
    "Slime mold optimization and network design",
    "Enzyme cascades as analog signal processors",
    "Epigenetic memory in cellular computing",
    "Topological qubits and fault-tolerant quantum computation",
    "Quantum coherence in biological photosynthesis",
    "Variational quantum eigensolvers for molecular simulation",
    "Quantum error correction via surface codes",
    "Quantum reservoir computing with spin chains",
    "Quantum tunneling in enzyme catalysis",
    "Entanglement-assisted classical communication",
    "Quantum machine learning kernel methods",
    "Proof-of-Discovery consensus mechanisms",
    "Semantic routing in knowledge graphs",
    "Decentralized AI governance frameworks",
    "Peer-to-peer scientific validation protocols",
    "Token-incentivized research contribution models",
    "Federated learning across heterogeneous agents",
    "Knowledge graph embedding and link prediction",
    "Merkle DAG structures for versioned knowledge",
    "Autopoietic systems and self-organization",
    "Cognitive architectures: SOAR vs ACT-R vs S2FSM",
    "Meta-learning and learning-to-learn paradigms",
    "Embodied cognition and situated AI",
    "Compositional generalization in neural networks",
    "Neuro-symbolic integration approaches",
    "Intrinsic motivation and curiosity-driven exploration",
    "Skill acquisition and procedural knowledge formation",
    "Emergence and complexity in physical systems",
    "Information theory and thermodynamics of computation",
    "Self-organized criticality in neural networks",
    "Scale-free networks and preferential attachment",
    "Dissipative structures and non-equilibrium thermodynamics",
    "Holographic principle and information bounds",
    "Cellular automata and computational universality",
    "Renormalization group and multi-scale physics",
    "Bio-inspired optimization: ant colony and swarm intelligence",
    "Morphogenetic computing: Turing patterns as programs",
    "Neuromorphic hardware: memristors and beyond",
    "Evolutionary strategies for neural architecture search",
    "Reservoir computing with physical substrates",
    "DNA data storage and retrieval systems",
    "Molecular communication and nanonetworks",
    "Synthetic ecosystems for emergent intelligence",
]

# 8 directions: name -> (row_offset, col_offset)
DIRECTIONS: Dict[str, Tuple[int, int]] = {
    "N":  (-1,  0), "NE": (-1,  1), "E":  ( 0,  1), "SE": ( 1,  1),
    "S":  ( 1,  0), "SW": ( 1, -1), "W":  ( 0, -1), "NW": (-1, -1),
}

DIRECTION_EMOJI: Dict[str, str] = {
    "N": "N", "NE": "NE", "E": "E", "SE": "SE",
    "S": "S", "SW": "SW", "W": "W", "NW": "NW",
}

CELL_TYPE_ICON = {
    "ENTRY": "[E]",
    "SYNTHESIS": "[S]",
    "MUTATION_CHAMBER": "[M]",
    "SKILL_NODE": "[K]",
    "EXPERIMENT_NODE": "[X]",
    "KNOWLEDGE": "[ ]",
}


def get_cell_topic(row: int, col: int, rows: int, cols: int) -> str:
    idx = (row * cols + col) % len(RESEARCH_DOMAINS)
    return RESEARCH_DOMAINS[idx]


def get_cell_type(row: int, col: int, rows: int, cols: int) -> str:
    if row == 0:
        return "ENTRY"
    if row == rows - 1:
        return "SYNTHESIS"
    if row == rows // 2 and col == cols // 2:
        return "MUTATION_CHAMBER"
    if (row * cols + col) % 17 == 0:
        return "SKILL_NODE"
    if (row * cols + col) % 23 == 0:
        return "EXPERIMENT_NODE"
    return "KNOWLEDGE"


def neighbours(row: int, col: int, rows: int, cols: int) -> List[Tuple[str, int, int]]:
    """Return list of (direction_name, nr, nc) for in-bounds neighbours."""
    out = []
    for name, (dr, dc) in DIRECTIONS.items():
        nr, nc = row + dr, col + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            out.append((name, nr, nc))
    return out


def generate_cell(row: int, col: int, rows: int, cols: int,
                  rng: random.Random | None = None) -> str:
    """Generate the Markdown content for a single grid cell."""
    if rng is None:
        rng = random.Random()
    topic = get_cell_topic(row, col, rows, cols)
    cell_type = get_cell_type(row, col, rows, cols)

    lines = [f"# Cell [{row},{col}] - {cell_type}"]
    lines.append(f"**Grid Position**: Row {row}, Column {col}")
    lines.append(f"**Type**: {cell_type}")
    lines.append("")

    if cell_type == "ENTRY":
        lines.append("## Entry Point")
        lines.append(f"Welcome, Agent. You have entered the Chess-Grid at column {col}.")
        lines.append(f"Your mission: traverse the board toward Row {rows-1}.")
        lines.append(f"**Research Focus**: {topic}")
    elif cell_type == "SYNTHESIS":
        lines.append("## Synthesis Terminal")
        lines.append("You have reached the far edge of the Chess-Grid.")
        lines.append("**ACTION REQUIRED**: Synthesize accumulated knowledge.")
        lines.append(f"**Final Topic Integration**: {topic}")
    elif cell_type == "MUTATION_CHAMBER":
        lines.append("## Mutation Chamber")
        lines.append("Analyze your recent performance.")
        lines.append(f"**Mutation Topic**: {topic}")
        lines.append("")
        lines.append("[ACQUIRED: agent reads this node -> adds 'self_mutation' to COMPETENCY_MAP]")
    elif cell_type == "SKILL_NODE":
        skill_name = rng.choice([
            "deep_analysis", "cross_reference", "hypothesis_generator",
            "evidence_evaluator", "pattern_recognition",
        ])
        lines.append(f"## Skill Node: `{skill_name}`")
        lines.append(f"**Research Context**: {topic}")
        lines.append("")
        lines.append(f"[ACQUIRED: agent reads this node -> adds '{skill_name}' to COMPETENCY_MAP]")
    elif cell_type == "EXPERIMENT_NODE":
        lines.append("## Experiment Node")
        lines.append(f"**Hypothesis**: {topic}")
        lines.append("Design a mental experiment to test this hypothesis.")
    else:
        lines.append("## Research Node")
        lines.append(f"**Topic**: {topic}")
        lines.append("Study this topic carefully.")

    lines.append("")
    lines.append("---")
    lines.append("## Navigation (Choose Your Direction)")
    lines.append("")
    for name, nr, nc in neighbours(row, col, rows, cols):
        target = get_cell_topic(nr, nc, rows, cols)
        short = (target[:50] + "...") if len(target) > 50 else target
        lines.append(f"- **{name}**: [{short}](cell_R{nr}_C{nc}.md)")
    lines.append("")
    return "\n".join(lines)


def generate_grid(output_dir: str | os.PathLike, rows: int = 16, cols: int = 16,
                  seed: int | None = None) -> Path:
    """Generate the full grid on disk. Returns the output directory Path."""
    rng = random.Random(seed)
    out = Path(output_dir)
    grid_dir = out / "grid" if out.name != "grid" else out
    grid_dir.mkdir(parents=True, exist_ok=True)

    for r in range(rows):
        for c in range(cols):
            content = generate_cell(r, c, rows, cols, rng=rng)
            (grid_dir / f"cell_R{r}_C{c}.md").write_text(content, encoding="utf-8")

    # Grid index
    idx_lines = [
        "# Chess-Grid Index",
        f"**Dimensions**: {rows}x{cols} = {rows*cols} cells",
        "",
    ]
    idx_lines.append("| | " + " | ".join(f"C{c}" for c in range(cols)) + " |")
    idx_lines.append("|---" * (cols + 1) + "|")
    for r in range(rows):
        cells = []
        for c in range(cols):
            ct = get_cell_type(r, c, rows, cols)
            cells.append(f"[{CELL_TYPE_ICON[ct]}](grid/cell_R{r}_C{c}.md)")
        idx_lines.append(f"| **R{r}** | " + " | ".join(cells) + " |")

    index_path = grid_dir.parent / "grid_index.md"
    index_path.write_text("\n".join(idx_lines), encoding="utf-8")
    return grid_dir


def parse_grid_position(filename: str) -> Tuple[int, int]:
    """Extract (row, col) from a cell filename like cell_R3_C7.md."""
    m = re.search(r"cell_R(\d+)_C(\d+)", filename)
    if m:
        return int(m.group(1)), int(m.group(2))
    return 0, 0


def load_cell_links(cell_text: str) -> List[Tuple[str, str]]:
    """Return list of (label, href) markdown links in a cell body."""
    return re.findall(r"\[([^\]]+)\]\(([^)]+\.md)\)", cell_text)
