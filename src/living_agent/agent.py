"""The Living Agent - Chess-Grid reasoning loop."""
from __future__ import annotations

import os
import random
import re
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple

from living_agent.grid import load_cell_links, parse_grid_position
from living_agent.llm_client import KoboldClient

APPROX_TOKENS_PER_CHAR = 0.25
CONTEXT_LIMIT_RATIO = 0.85


def estimate_tokens(text: str) -> int:
    return int(len(text) * APPROX_TOKENS_PER_CHAR)


def atomic_write(path: Path, content: str) -> None:
    """Write a file atomically by using a tempfile and os.replace."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(content)
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def parse_soul(text: str) -> dict:
    """Extract structured state from a soul.md text blob."""
    def _find(pat: str, default: str = "") -> str:
        m = re.search(pat, text)
        return m.group(1) if m else default

    cycle = int(_find(r"Current Cycle:\s*(\d+)", "1"))
    papers = int(_find(r"Total Papers Published:\s*(\d+)", "0"))
    highest = float(_find(r"Highest SNS Score:\s*([\d.]+)", "0.0"))
    skills_raw = _find(r"Acquired Skills:\s*\[(.*?)\]", "")
    visited_raw = _find(r"Visited Nodes:\s*\[(.*?)\]", "")
    skills = {s.strip() for s in skills_raw.split(",") if s.strip()}
    visited = {v.strip() for v in visited_raw.split(",") if v.strip()}
    return {
        "cycle": cycle,
        "papers": papers,
        "highest_sns": highest,
        "skills": skills,
        "visited": visited,
    }


def update_soul(soul_text: str, *, cycle: Optional[int] = None,
                papers: Optional[int] = None,
                highest_sns: Optional[float] = None,
                skills: Optional[set] = None,
                visited: Optional[set] = None) -> str:
    out = soul_text
    if cycle is not None:
        out = re.sub(r"Current Cycle:\s*\d+", f"Current Cycle: {cycle}", out)
    if papers is not None:
        out = re.sub(r"Total Papers Published:\s*\d+",
                     f"Total Papers Published: {papers}", out)
    if highest_sns is not None:
        out = re.sub(r"Highest SNS Score:\s*[\d.]+",
                     f"Highest SNS Score: {highest_sns}", out)
    if skills is not None:
        joined = ", ".join(sorted(skills))
        out = re.sub(r"Acquired Skills:\s*\[.*?\]",
                     f"Acquired Skills: [{joined}]", out)
    if visited is not None:
        joined = ", ".join(sorted(visited)[-100:])
        out = re.sub(r"Visited Nodes:\s*\[.*?\]",
                     f"Visited Nodes:     [{joined}]", out)
    return out


def calculate_sns(new_paper: str, prior_papers: List[str]) -> float:
    """Semantic Novelty Score: 1 - max Jaccard overlap vs prior papers."""
    if not prior_papers:
        return 1.0
    def words(t: str) -> set:
        return set(re.findall(r"\w+", t.lower()))
    new_w = words(new_paper)
    if not new_w:
        return 0.0
    max_overlap = 0.0
    for past in prior_papers:
        pw = words(past)
        if not pw:
            continue
        j = len(new_w & pw) / max(1, len(new_w | pw))
        max_overlap = max(max_overlap, j)
    return round(1.0 - max_overlap, 3)


class LivingAgent:
    """Runs Chess-Grid reasoning cycles against a KoboldCPP endpoint."""

    def __init__(self, base_dir: str | os.PathLike,
                 client: Optional[KoboldClient] = None,
                 rows: int = 16, cols: int = 16,
                 rng: Optional[random.Random] = None):
        self.base_dir = Path(base_dir)
        self.client = client or KoboldClient()
        self.rows = rows
        self.cols = cols
        self.rng = rng or random.Random()
        self.grid_dir = self.base_dir / "knowledge" / "grid"
        self.soul_path = self.base_dir / "soul.md"

    # ---- IO helpers ----
    def load_cell(self, row: int, col: int) -> str:
        return (self.grid_dir / f"cell_R{row}_C{col}.md").read_text(encoding="utf-8")

    def load_soul(self) -> str:
        if self.soul_path.exists():
            return self.soul_path.read_text(encoding="utf-8")
        return ("# SOUL OF AGENT ZERO\n\n"
                "## GENERATION\nCurrent Cycle: 1\n"
                "Total Papers Published: 0\nHighest SNS Score: 0.0\n\n"
                "## COMPETENCY_MAP\nAcquired Skills: []\n\n"
                "## CURIOSITY_MAP\nVisited Nodes:     []\n")

    def save_soul(self, text: str) -> None:
        atomic_write(self.soul_path, text)

    # ---- Reasoning ----
    def choose_direction(self, node_content: str, options: List[Tuple[str, str]],
                         soul: str, trace: List[str]) -> int:
        options_str = "\n".join(
            f"- [{i}] {label} ({url})" for i, (label, url) in enumerate(options)
        )
        prompt = (
            "### SYSTEM: LIVING AGENT CHESS-GRID ENGINE\n"
            "You are navigating a Chess-Grid of knowledge.\n\n"
            f"### AGENT SOUL\n{soul}\n\n"
            f"### CURRENT TRACE\n{trace}\n\n"
            f"### CURRENT CELL CONTENT\n{node_content}\n\n"
            f"### AVAILABLE DIRECTIONS\n{options_str}\n\n"
            "### INSTRUCTION\nOutput EXACTLY one line:\nCHOSEN_INDEX: [N]\n"
        )
        try:
            response = self.client.generate(prompt, max_tokens=64)
        except RuntimeError:
            return self.rng.randrange(len(options))
        m = re.search(r"CHOSEN_INDEX:\s*\[(\d+)\]", response)
        if m:
            idx = int(m.group(1))
            if 0 <= idx < len(options):
                return idx
        return self.rng.randrange(len(options))

    def synthesize(self, trace_content: str, soul: str) -> str:
        prompt = (
            "### SYSTEM: HYPER-SCIENTIFIC GENERATOR\n"
            f"### AGENT SOUL\n{soul}\n\n"
            f"### RESEARCH TRACE\n{trace_content}\n\n"
            "### INSTRUCTION\nProduce a Markdown paper: Abstract, Introduction, "
            "Methodology, Results, Discussion, Conclusion, References.\n"
        )
        try:
            return self.client.generate(prompt, max_tokens=2048)
        except RuntimeError as exc:
            return f"# Synthesis Failed\n\n{exc}\n"

    # ---- Main loop ----
    def run_cycle(self) -> dict:
        soul = self.load_soul()
        state = parse_soul(soul)
        cycle = state["cycle"]
        visited = set(state["visited"])
        skills = set(state["skills"])

        start_col = self.rng.randrange(self.cols)
        row, col = 0, start_col
        trace: List[str] = []
        full_trace = ""
        ctx_tokens = estimate_tokens(soul)
        max_ctx = self.client.max_context

        while True:
            content = self.load_cell(row, col)
            full_trace += f"\n--- CELL [{row},{col}] ---\n{content}\n"
            ctx_tokens += estimate_tokens(content)
            visited.add(f"R{row}_C{col}")
            trace.append(f"[{row},{col}]")

            sm = re.search(r"adds '(.*?)' to COMPETENCY_MAP", content)
            if sm:
                skills.add(sm.group(1))

            if row >= self.rows - 1:
                break
            if ctx_tokens >= max_ctx * CONTEXT_LIMIT_RATIO:
                break

            links = load_cell_links(content)
            if not links:
                break
            idx = self.choose_direction(content, links, soul, trace)
            next_href = links[idx][1]
            row, col = parse_grid_position(next_href)

        paper = self.synthesize(full_trace, soul)
        prior = self._load_prior_papers(limit=50)
        sns = calculate_sns(paper, prior)

        self._save_paper(cycle, paper, sns)
        self._save_episodic(cycle, trace, sns)

        highest = max(state["highest_sns"], sns)
        new_soul = update_soul(
            soul, cycle=cycle + 1, papers=cycle, highest_sns=highest,
            skills=skills, visited=visited,
        )
        self.save_soul(new_soul)

        return {
            "cycle": cycle,
            "trace": trace,
            "sns": sns,
            "paper_bytes": len(paper),
            "skills": sorted(skills),
        }

    # ---- Artifact IO ----
    def _load_prior_papers(self, limit: int = 50) -> List[str]:
        semantic = self.base_dir / "memories" / "semantic"
        if not semantic.exists():
            return []
        files = sorted(
            (p for p in semantic.iterdir() if p.suffix == ".md"),
            key=lambda p: p.stat().st_mtime, reverse=True,
        )[:limit]
        return [p.read_text(encoding="utf-8") for p in files]

    def _save_paper(self, cycle: int, paper: str, sns: float) -> None:
        out = self.base_dir / "memories" / "semantic" / f"paper_{cycle}.md"
        atomic_write(out, f"{paper}\n\nSNS Score: {sns}\n")

    def _save_episodic(self, cycle: int, trace: List[str], sns: float) -> None:
        out = self.base_dir / "memories" / "episodic" / f"cycle_{cycle}.md"
        atomic_write(out, f"Trace: {' -> '.join(trace)}\nSNS: {sns}\n")

    # ---- Status ----
    def status(self) -> dict:
        soul = self.load_soul()
        st = parse_soul(soul)
        semantic = self.base_dir / "memories" / "semantic"
        episodic = self.base_dir / "memories" / "episodic"
        paper_count = len(list(semantic.glob("*.md"))) if semantic.exists() else 0
        episodic_count = len(list(episodic.glob("*.md"))) if episodic.exists() else 0
        return {
            "cycle": st["cycle"],
            "papers_published": st["papers"],
            "highest_sns": st["highest_sns"],
            "skills": sorted(st["skills"]),
            "visited_count": len(st["visited"]),
            "paper_files": paper_count,
            "episodic_files": episodic_count,
        }
