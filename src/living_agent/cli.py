"""Command-line interface for The Living Agent."""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from living_agent import __version__
from living_agent.agent import LivingAgent
from living_agent.grid import generate_grid
from living_agent.llm_client import KoboldClient


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="living-agent",
        description="The Living Agent - autonomous Chess-Grid research engine.",
    )
    parser.add_argument("--version", action="version", version=f"living-agent {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Generate a fresh 16x16 knowledge grid.")
    p_init.add_argument("--grid-dir", default="knowledge",
                        help="Directory where grid/ and grid_index.md are written.")
    p_init.add_argument("--rows", type=int, default=16)
    p_init.add_argument("--cols", type=int, default=16)
    p_init.add_argument("--seed", type=int, default=None)

    p_run = sub.add_parser("run", help="Run N reasoning cycles.")
    p_run.add_argument("--cycles", type=int, default=1)
    p_run.add_argument("--endpoint", default="http://localhost:5001/api/v1/generate")
    p_run.add_argument("--base-dir", default=".")
    p_run.add_argument("--sleep", type=float, default=5.0,
                       help="Seconds to rest between cycles.")

    p_status = sub.add_parser("status", help="Show current agent state.")
    p_status.add_argument("--grid-dir", default=".")
    p_status.add_argument("--json", action="store_true", help="Emit JSON instead of text.")

    return parser


def cmd_init(args: argparse.Namespace) -> int:
    out = generate_grid(args.grid_dir, rows=args.rows, cols=args.cols, seed=args.seed)
    print(f"Generated {args.rows}x{args.cols} grid at {out}")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    client = KoboldClient(endpoint=args.endpoint)
    agent = LivingAgent(base_dir=args.base_dir, client=client)
    for i in range(args.cycles):
        result = agent.run_cycle()
        print(f"[cycle {result['cycle']}] trace={len(result['trace'])} "
              f"sns={result['sns']} paper_bytes={result['paper_bytes']}")
        if i < args.cycles - 1 and args.sleep > 0:
            time.sleep(args.sleep)
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    agent = LivingAgent(base_dir=args.grid_dir)
    st = agent.status()
    if args.json:
        print(json.dumps(st, indent=2))
    else:
        print(f"Cycle:            {st['cycle']}")
        print(f"Papers published: {st['papers_published']}")
        print(f"Highest SNS:      {st['highest_sns']}")
        print(f"Skills:           {', '.join(st['skills']) or '(none)'}")
        print(f"Visited cells:    {st['visited_count']}")
        print(f"Paper files:      {st['paper_files']}")
        print(f"Episodic files:   {st['episodic_files']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "init":
        return cmd_init(args)
    if args.command == "run":
        return cmd_run(args)
    if args.command == "status":
        return cmd_status(args)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
