#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from living_agent_common import (
    DEFAULT_ARTIFACT_ROOT,
    DEFAULT_LIVING_AGENT_ROOT,
    DEFAULT_NUCLEUSDB_ROOT,
    ensure_module_runtime,
    read_text,
    run,
    sha256_text,
    write_text,
)
from living_agent_sns_embeddings import DEFAULT_MODEL, Encoder, score_text
from living_agent_verify import verify_paper, write_report_payload

ensure_module_runtime("sentence_transformers")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")


def dedup(log_path: Path, paper_hash: str) -> bool:
    for row in load_jsonl(log_path):
        if row.get("paper_sha256") != paper_hash:
            continue
        status = ((row.get("publish_result") or {}).get("status")) or row.get("status")
        if status != "rejected":
            return True
    return False


def publish_via_agenthalo(
    *,
    nucleusdb_root: Path,
    title: str,
    paper_text: str,
    dry_run: bool,
    agenthalo_mode: str,
) -> dict:
    if agenthalo_mode != "cli":
        raise ValueError(f"unsupported AgentHALO mode: {agenthalo_mode}")
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as tmp:
        tmp.write(paper_text)
        temp_path = Path(tmp.name)
    cmd = [
        "cargo",
        "run",
        "--manifest-path",
        str(nucleusdb_root / "Cargo.toml"),
        "--bin",
        "agenthalo",
        "--",
        "p2pclaw",
        "bridge",
        "publish-paper",
        "--title",
        title,
        "--content-file",
        str(temp_path),
    ]
    if not dry_run:
        cmd.append("--live")
    proc = run(cmd, cwd=nucleusdb_root, check=False)
    temp_path.unlink(missing_ok=True)
    parsed = None
    if proc.stdout.strip():
        try:
            parsed = json.loads(proc.stdout)
        except json.JSONDecodeError:
            parsed = None
    if proc.returncode != 0:
        return {
            "status": "pending_publication",
            "surface": "agenthalo-cli:p2pclaw-bridge-publish-paper",
            "mode": agenthalo_mode,
            "bridge_response": parsed,
            "publish_command": cmd,
            "publish_returncode": proc.returncode,
            "publish_stdout": proc.stdout.strip(),
            "publish_stderr": proc.stderr.strip(),
        }
    bridge_result = ((parsed or {}).get("result")) if isinstance(parsed, dict) else None
    verification = (bridge_result or {}).get("verification") if isinstance(bridge_result, dict) else None
    if verification and not verification.get("verified", False):
        return {
            "status": "rejected",
            "surface": "agenthalo-cli:p2pclaw-bridge-publish-paper",
            "mode": agenthalo_mode,
            "bridge_response": parsed,
        }
    if dry_run:
        return {
            "status": "dry_run",
            "surface": "agenthalo-cli:p2pclaw-bridge-publish-paper",
            "mode": agenthalo_mode,
            "bridge_response": parsed,
        }
    publish_result = (bridge_result or {}).get("publish_result") if isinstance(bridge_result, dict) else None
    return {
        "status": (
            publish_result.get("status")
            if isinstance(publish_result, dict) and publish_result.get("status")
            else ("published" if proc.returncode == 0 else "pending_publication")
        ),
        "surface": "agenthalo-cli:p2pclaw-bridge-publish-paper",
        "mode": agenthalo_mode,
        "bridge_response": parsed,
        "publish_command": cmd,
        "publish_returncode": proc.returncode,
        "publish_stdout": proc.stdout.strip(),
        "publish_stderr": proc.stderr.strip(),
    }


def update_shared_discoveries(
    living_agent_root: Path,
    *,
    cycle: int,
    title: str,
    sns: float,
    trace: str,
    status: str,
) -> None:
    hive_path = living_agent_root / "memories" / "hive" / "shared_discoveries.md"
    header = "# Shared Discoveries\n\n| Cycle | Title | SNS | Status | Trace |\n|---|---|---:|---|---|\n"
    if not hive_path.exists():
        write_text(hive_path, header)
    else:
        text = read_text(hive_path)
        if "| Cycle | Title | SNS | Trace |" in text:
            text = text.replace(
                "| Cycle | Title | SNS | Trace |\n|-------|-------|-----|-------|\n",
                "| Cycle | Title | SNS | Status | Trace |\n|---|---|---:|---|---|\n",
            )
            write_text(hive_path, text)
    with hive_path.open("a", encoding="utf-8") as handle:
        handle.write(f"| {cycle} | {title} | {sns:.3f} | {status} | {trace} |\n")


def store_result_paper(
    living_agent_root: Path,
    *,
    cycle: int,
    paper_text: str,
    accepted: bool,
    report: dict,
    sns: float,
) -> str:
    target_dir = (
        living_agent_root / "memories" / "semantic"
        if accepted
        else living_agent_root / "memories" / "rejected"
    )
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f"paper_{cycle}.md"
    suffix = (
        f"\n\nSNS Score: {sns:.3f}\n"
        f"Verification Passed: {report['composite']['passed']}\n"
        f"Verification Report: {report['paper_sha256']}\n"
    )
    write_text(target_path, paper_text.rstrip() + suffix)
    return str(target_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Publish verified Living Agent papers via AgentHALO")
    parser.add_argument("--paper", "--paper-file", dest="paper_file")
    parser.add_argument("--text")
    parser.add_argument("--cycle", type=int, required=True)
    parser.add_argument("--trace", default="")
    parser.add_argument("--trace-cells", default="")
    parser.add_argument("--archive-dir", default=str(DEFAULT_ARTIFACT_ROOT))
    parser.add_argument("--grid-root")
    parser.add_argument("--living-agent-root", default=str(DEFAULT_LIVING_AGENT_ROOT))
    parser.add_argument("--nucleusdb-root", default=str(DEFAULT_NUCLEUSDB_ROOT))
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--agenthalo-mode", choices=["cli"], default="cli")
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--dry-run", dest="dry_run", action="store_true")
    mode_group.add_argument("--live", dest="dry_run", action="store_false")
    parser.set_defaults(dry_run=True)
    parser.add_argument("--force-republish", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if not args.text and not args.paper_file:
        parser.error("one of --text or --paper/--paper-file is required")
    paper_text = args.text or read_text(Path(args.paper_file))
    title_line = next((line[2:].strip() for line in paper_text.splitlines() if line.startswith("# ")), f"paper_{args.cycle}")
    archive_dir = Path(args.archive_dir)
    grid_root = Path(args.grid_root) if args.grid_root else archive_dir / "verified_grid"
    living_agent_root = Path(args.living_agent_root)
    encoder = Encoder(args.model)
    sns_payload = score_text(
        paper_text,
        archive_dir=archive_dir,
        encoder=encoder,
        append=False,
    )
    report = verify_paper(
        paper_text,
        archive_dir=archive_dir,
        grid_root=grid_root,
        living_agent_root=living_agent_root,
        encoder=encoder,
    )
    report_path = write_report_payload(archive_dir, report)
    report["report_path"] = str(report_path)
    paper_hash = sha256_text(paper_text)
    log_path = archive_dir / "hive_publication_log.jsonl"
    trace_cells = [cell.strip() for cell in args.trace_cells.split(",") if cell.strip()]
    if not args.force_republish and dedup(log_path, paper_hash):
        payload = {
            "status": "duplicate",
            "paper_sha256": paper_hash,
            "verification_report": report,
            "sns_score": sns_payload["sns"],
            "cycle": args.cycle,
            "trace": args.trace,
            "trace_cells": trace_cells,
            "agenthalo_mode": args.agenthalo_mode,
        }
        if args.json:
            print(json.dumps(payload, indent=2))
        else:
            print(payload)
        return 0
    accepted = bool(report["composite"]["passed"])
    if accepted:
        publish = publish_via_agenthalo(
            nucleusdb_root=Path(args.nucleusdb_root),
            title=title_line,
            paper_text=paper_text,
            dry_run=args.dry_run,
            agenthalo_mode=args.agenthalo_mode,
        )
        bridge_rejected = publish.get("status") == "rejected"
        stored_path = store_result_paper(
            living_agent_root,
            cycle=args.cycle,
            paper_text=paper_text,
            accepted=not bridge_rejected,
            report=report,
            sns=sns_payload["sns"],
        )
        if not bridge_rejected:
            score_text(
                paper_text,
                archive_dir=archive_dir,
                encoder=encoder,
                append=True,
                metadata={"paper_file": stored_path, "paper_sha256": paper_hash},
            )
            update_shared_discoveries(
                living_agent_root,
                cycle=args.cycle,
                title=title_line,
                sns=float(sns_payload["sns"]),
                trace=args.trace,
                status=publish["status"],
            )
    else:
        stored_path = store_result_paper(
            living_agent_root,
            cycle=args.cycle,
            paper_text=paper_text,
            accepted=False,
            report=report,
            sns=sns_payload["sns"],
        )
        publish = {"status": "rejected", "surface": None}
    payload = {
        "timestamp": utc_now(),
        "cycle": args.cycle,
        "title": title_line,
        "paper_sha256": paper_hash,
        "paper_path": stored_path,
        "trace": args.trace,
        "trace_cells": trace_cells,
        "sns_score": sns_payload["sns"],
        "report_path": str(report_path),
        "agenthalo_mode": args.agenthalo_mode,
        "verification_report": report,
        "publish_result": publish,
    }
    append_jsonl(log_path, payload)
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
