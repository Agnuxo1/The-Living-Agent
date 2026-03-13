#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import tempfile
from functools import lru_cache
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from living_agent_common import (
    DEFAULT_ARTIFACT_ROOT,
    DEFAULT_GRID_ROOT,
    REPO_ROOT,
    ensure_module_runtime,
    normalize_whitespace,
    read_text,
    run,
    sha256_text,
    tokenize,
    write_json,
)
from living_agent_sns_embeddings import Encoder, score_text

ensure_module_runtime("sentence_transformers")
SCHEMA_VERSION = "living-agent-verify-v1"
TYPECHECK_TIMEOUT_SECS = int(os.environ.get("HEYTING_TYPECHECK_TIMEOUT_SECS", "30"))


CLAIM_RE = re.compile(
    r"\b(proves?|demonstrates?|shows?|establishes?|argues?|proposes?|introduces?|suggests?|finds?)\b",
    re.I,
)
SECTION_RE = re.compile(
    r"^(?:#+\s*|\*\*)(abstract|methodology|results|discussion|conclusion|introduction|semantic synthesis|novelty discussion)(?:\*\*)?\s*:?",
    re.I | re.M,
)
CELL_RE = re.compile(r"cell_R\d+_C\d+\.md")
CODE_BLOCK_RE = re.compile(r"```(?:lean|lean4|theorem)\s*\n(.*?)```", re.S | re.I)


@dataclass
class TierResult:
    score: float
    passed: bool
    details: dict


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def extract_claim_sentences(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", normalize_whitespace(text))
    claims = [sentence.strip() for sentence in sentences if CLAIM_RE.search(sentence)]
    return claims[:8]


def candidate_typecheck_roots() -> list[Path]:
    roots: list[Path] = []
    for raw in (
        os.environ.get("HEYTING_TYPECHECK_ROOT"),
        os.environ.get("HEYTING_ROOT"),
        str(REPO_ROOT),
        "/home/abraxas/Work/heyting",
    ):
        if not raw:
            continue
        root = Path(raw).resolve()
        if root not in roots:
            roots.append(root)
    return roots


def root_has_typecheck_surface(root: Path) -> bool:
    return (root / "scripts" / "typecheck_snippet.sh").exists() and (root / "lean").exists()


@lru_cache(maxsize=1)
def resolve_typecheck_root() -> tuple[Path | None, str | None]:
    for root in candidate_typecheck_roots():
        if not root_has_typecheck_surface(root):
            continue
        try:
            proc = run(
                [str(root / "scripts" / "typecheck_snippet.sh"), "True"],
                cwd=root,
                check=False,
                timeout_secs=min(TYPECHECK_TIMEOUT_SECS, 15),
            )
        except subprocess.TimeoutExpired:
            continue
        if proc.returncode == 0:
            return root, None
    return None, "no healthy Heyting typecheck root found"


def typecheck_block(root: Path, block: str) -> subprocess.CompletedProcess[str]:
    if "\n" not in block and len(block.split()) <= 8:
        return run(
            [str(root / "scripts" / "typecheck_snippet.sh"), block],
            cwd=root,
            check=False,
            timeout_secs=TYPECHECK_TIMEOUT_SECS,
        )
    with tempfile.NamedTemporaryFile("w", suffix=".lean", delete=False) as tmp:
        tmp.write("import HeytingLean\n")
        tmp.write(block)
        tmp.write("\n")
        temp_path = Path(tmp.name)
    try:
        return run(
            [
                "bash",
                "-lc",
                f"cd {shlex.quote(str(root / 'lean'))} && lake env lean {shlex.quote(str(temp_path))}",
            ],
            cwd=root,
            check=False,
            timeout_secs=TYPECHECK_TIMEOUT_SECS,
        )
    finally:
        temp_path.unlink(missing_ok=True)


def structural_result(text: str, living_agent_root: Path) -> TierResult:
    word_count = len(text.split())
    sections = SECTION_RE.findall(text)
    claim_sentences = extract_claim_sentences(text)
    refs = CELL_RE.findall(text)
    valid_refs = 0
    for ref in refs:
        if (living_agent_root / "knowledge" / "grid" / ref).exists():
            valid_refs += 1
    score = 0.0
    score += 0.25 if word_count >= 120 else min(0.25, word_count / 480.0)
    score += 0.25 if len(sections) >= 2 else (0.125 if len(sections) == 1 else 0.0)
    score += 0.25 if len(claim_sentences) >= 1 else 0.0
    if refs:
        score += 0.25 if valid_refs == len(refs) else 0.0
    else:
        score += 0.125
    score = round(score, 4)
    return TierResult(
        score=score,
        passed=score >= 0.5,
        details={
            "word_count": word_count,
            "section_count": len(sections),
            "sections": sections,
            "claim_count": len(claim_sentences),
            "claim_sentences": claim_sentences,
            "references": refs,
            "valid_references": valid_refs,
        },
    )


def load_grid_cells(grid_root: Path) -> list[dict]:
    payload = json.loads(read_text(grid_root / "verified_grid_index.json"))
    return payload["cells"]


def cell_semantic_tokens(cell: dict) -> set[str]:
    return set(
        tokenize(
            " ".join(
                [
                    cell["fqn"],
                    cell.get("signature", ""),
                    cell.get("docstring", ""),
                    cell.get("overlay_summary", ""),
                    " ".join(cell.get("keywords", [])),
                ]
            )
        )
    )


def semantic_result(
    text: str,
    *,
    archive_dir: Path,
    grid_root: Path,
    encoder: Encoder,
) -> TierResult:
    novelty_payload = score_text(
        text,
        archive_dir=archive_dir,
        encoder=encoder,
        append=False,
        exclude_sha256=sha256_text(normalize_whitespace(text)),
    )
    cells = load_grid_cells(grid_root)
    paper_tokens = set(tokenize(text))
    paper_embedding = encoder.encode([normalize_whitespace(text)])[0]
    cell_texts = [
        normalize_whitespace(
            f"{cell['fqn']} {cell.get('docstring','')} {cell.get('overlay_summary','')} {' '.join(cell.get('keywords', []))}"
        )
        for cell in cells
    ]
    cell_embeddings = encoder.encode(cell_texts)
    similarities = cell_embeddings @ paper_embedding
    top_similarity = float(similarities.max()) if len(similarities) else 0.0
    top_idx = int(similarities.argmax()) if len(similarities) else -1
    top_cell = cells[top_idx] if top_idx >= 0 else None
    anchor_overlap = 0.0
    if top_cell is not None:
        cell_tokens = cell_semantic_tokens(top_cell)
        if cell_tokens:
            anchor_overlap = len(paper_tokens & cell_tokens) / len(cell_tokens)
    coverage = max(0.0, min(1.0, max(0.0, top_similarity) * 0.4 + anchor_overlap * 0.6))
    score = round((coverage + float(novelty_payload["sns"])) / 2.0, 4)
    top_cell_fqn = top_cell["fqn"] if top_cell is not None else None
    return TierResult(
        score=score,
        passed=score >= 0.45 and coverage >= 0.25,
        details={
            "novelty": novelty_payload["sns"],
            "max_similarity": novelty_payload["max_similarity"],
            "coverage": round(coverage, 4),
            "anchor_overlap": round(anchor_overlap, 4),
            "top_grid_match": top_cell_fqn,
        },
    )


def formal_result(text: str) -> TierResult:
    blocks = [normalize_whitespace(block) for block in CODE_BLOCK_RE.findall(text)]
    if not blocks:
        return TierResult(score=1.0, passed=True, details={"no_code_blocks": True, "checked": 0})
    typecheck_root, degraded_reason = resolve_typecheck_root()
    if typecheck_root is None:
        return TierResult(
            score=0.0,
            passed=False,
            details={
                "checked": len(blocks),
                "successes": 0,
                "degraded": False,
                "fail_closed": True,
                "reason": degraded_reason,
            },
        )
    successes = 0
    errors = []
    for block in blocks:
        try:
            proc = typecheck_block(typecheck_root, block)
        except subprocess.TimeoutExpired:
            errors.append(f"typecheck timeout after {TYPECHECK_TIMEOUT_SECS}s")
            continue
        if proc.returncode == 0:
            successes += 1
        else:
            errors.append(proc.stderr or proc.stdout)
    score = round(successes / len(blocks), 4)
    return TierResult(
        score=score,
        passed=score >= 0.5,
        details={
            "checked": len(blocks),
            "successes": successes,
            "errors": errors[:3],
            "typecheck_root": str(typecheck_root),
            "degraded": False,
        },
    )


def verify_paper(
    text: str,
    *,
    archive_dir: Path,
    grid_root: Path,
    living_agent_root: Path,
    encoder: Encoder,
) -> dict:
    structural = structural_result(text, living_agent_root)
    semantic = semantic_result(text, archive_dir=archive_dir, grid_root=grid_root, encoder=encoder)
    formal = formal_result(text)
    passed = structural.passed and semantic.passed and formal.passed
    generated_at = utc_now()
    composite_score = round(min(structural.score, semantic.score, formal.score), 4)
    governing_tier = min(
        (
            ("structural", structural.score),
            ("semantic", semantic.score),
            ("formal", formal.score),
        ),
        key=lambda item: item[1],
    )[0]
    report = {
        "paper_sha256": sha256_text(text),
        "generated_at": generated_at,
        "schema_version": SCHEMA_VERSION,
        "structural": asdict(structural),
        "semantic": asdict(semantic),
        "formal": asdict(formal),
        "composite": {
            "score": composite_score,
            "passed": passed,
            "details": {
                "governing_tier": governing_tier,
                "generated_at": generated_at,
                "structural_passed": structural.passed,
                "semantic_passed": semantic.passed,
                "formal_passed": formal.passed,
            },
        },
    }
    return report


def write_report_payload(archive_dir: Path, payload: dict) -> Path:
    report_dir = archive_dir / "verification_reports"
    report_path = report_dir / f"{payload['paper_sha256']}.json"
    write_json(report_path, payload)
    return report_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Verify Living Agent paper output")
    parser.add_argument("--text")
    parser.add_argument("--paper-file")
    parser.add_argument("--tier", choices=["structural", "semantic", "formal", "all"], default="all")
    parser.add_argument("--archive-dir", default=str(DEFAULT_ARTIFACT_ROOT))
    parser.add_argument("--grid-root", default=str(DEFAULT_GRID_ROOT))
    parser.add_argument("--living-agent-root", default="/tmp/the-living-agent")
    parser.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if not args.text and not args.paper_file:
        raise SystemExit("pass --text or --paper-file")
    text = args.text or read_text(Path(args.paper_file))
    archive_dir = Path(args.archive_dir)
    grid_root = Path(args.grid_root)
    living_agent_root = Path(args.living_agent_root)
    if args.tier == "structural":
        payload = asdict(structural_result(text, living_agent_root))
    elif args.tier == "semantic":
        encoder = Encoder(args.model)
        payload = asdict(semantic_result(text, archive_dir=archive_dir, grid_root=grid_root, encoder=encoder))
    elif args.tier == "formal":
        payload = asdict(formal_result(text))
    else:
        encoder = Encoder(args.model)
        payload = verify_paper(
            text,
            archive_dir=archive_dir,
            grid_root=grid_root,
            living_agent_root=living_agent_root,
            encoder=encoder,
        )
        if args.write_report or args.paper_file:
            report_path = write_report_payload(archive_dir, payload)
            payload["report_path"] = str(report_path)
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
