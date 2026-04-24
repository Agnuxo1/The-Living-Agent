"""Tests for living_agent.cli argparse surface."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from living_agent import cli


def test_help_exits_zero(capsys):
    with pytest.raises(SystemExit) as ex:
        cli.main(["--help"])
    assert ex.value.code == 0
    out = capsys.readouterr().out
    assert "living-agent" in out
    assert "init" in out
    assert "run" in out
    assert "status" in out


def test_init_generates_grid(tmp_path: Path):
    rc = cli.main(["init", "--grid-dir", str(tmp_path), "--seed", "0"])
    assert rc == 0
    assert (tmp_path / "grid").is_dir()
    assert (tmp_path / "grid_index.md").is_file()
    assert len(list((tmp_path / "grid").glob("cell_R*_C*.md"))) == 256


def test_status_text_output(tmp_path: Path, capsys):
    # Bare repo with soul.md only
    (tmp_path / "soul.md").write_text(
        "Current Cycle: 5\nTotal Papers Published: 4\n"
        "Highest SNS Score: 0.9\nAcquired Skills: [foo]\nVisited Nodes:     []\n",
        encoding="utf-8",
    )
    rc = cli.main(["status", "--grid-dir", str(tmp_path)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Cycle:" in out
    assert "5" in out
    assert "foo" in out


def test_status_json_output(tmp_path: Path, capsys):
    (tmp_path / "soul.md").write_text(
        "Current Cycle: 9\nTotal Papers Published: 8\n"
        "Highest SNS Score: 0.1\nAcquired Skills: []\nVisited Nodes:     []\n",
        encoding="utf-8",
    )
    rc = cli.main(["status", "--grid-dir", str(tmp_path), "--json"])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["cycle"] == 9
    assert payload["papers_published"] == 8


def test_run_subcommand_surface(capsys):
    # Parsing only — don't actually hit the network
    parser = cli.build_parser()
    args = parser.parse_args(["run", "--cycles", "3", "--endpoint", "http://x/y",
                              "--base-dir", ".", "--sleep", "0"])
    assert args.cycles == 3
    assert args.endpoint == "http://x/y"
    assert args.sleep == 0.0
