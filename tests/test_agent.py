"""Tests for living_agent.agent using an in-process fake KoboldCPP server."""
from __future__ import annotations

import json
import random
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import pytest

from living_agent.agent import (
    LivingAgent,
    atomic_write,
    calculate_sns,
    parse_soul,
    update_soul,
)
from living_agent.grid import generate_grid
from living_agent.llm_client import KoboldClient


class FakeHandler(BaseHTTPRequestHandler):
    """Records requests and returns a scripted response."""
    responses: list[str] = []
    received: list[dict] = []

    def log_message(self, format, *args):  # silence
        return

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            parsed = json.loads(body)
        except Exception:
            parsed = {}
        type(self).received.append({"path": self.path, "payload": parsed})
        text = type(self).responses.pop(0) if type(self).responses else "CHOSEN_INDEX: [0]"
        resp = json.dumps({"results": [{"text": text}]}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(resp)))
        self.end_headers()
        self.wfile.write(resp)


@pytest.fixture
def fake_server():
    FakeHandler.responses = []
    FakeHandler.received = []
    server = HTTPServer(("127.0.0.1", 0), FakeHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_address[1]
    try:
        yield f"http://127.0.0.1:{port}/api/v1/generate", FakeHandler
    finally:
        server.shutdown()
        server.server_close()


@pytest.fixture
def base_dir(tmp_path: Path) -> Path:
    generate_grid(tmp_path / "knowledge", rows=16, cols=16, seed=1)
    (tmp_path / "soul.md").write_text(
        "# SOUL\n"
        "Acquired Skills: [alpha]\n"
        "Visited Nodes:     []\n"
        "Current Cycle: 3\n"
        "Total Papers Published: 2\n"
        "Highest SNS Score: 0.5\n",
        encoding="utf-8",
    )
    return tmp_path


def test_parse_soul_extracts_fields():
    text = (
        "Current Cycle: 7\n"
        "Total Papers Published: 6\n"
        "Highest SNS Score: 0.875\n"
        "Acquired Skills: [a, b, c]\n"
        "Visited Nodes:     [R0_C0, R0_C1]\n"
    )
    st = parse_soul(text)
    assert st["cycle"] == 7
    assert st["papers"] == 6
    assert st["highest_sns"] == 0.875
    assert st["skills"] == {"a", "b", "c"}
    assert st["visited"] == {"R0_C0", "R0_C1"}


def test_update_soul_roundtrip():
    orig = (
        "Current Cycle: 1\n"
        "Total Papers Published: 0\n"
        "Highest SNS Score: 0.0\n"
        "Acquired Skills: []\n"
        "Visited Nodes:     []\n"
    )
    new = update_soul(orig, cycle=2, papers=1, highest_sns=0.9,
                      skills={"x", "y"}, visited={"R0_C0"})
    st = parse_soul(new)
    assert st["cycle"] == 2
    assert st["papers"] == 1
    assert st["highest_sns"] == 0.9
    assert st["skills"] == {"x", "y"}
    assert "R0_C0" in st["visited"]


def test_calculate_sns_empty_prior_returns_one():
    assert calculate_sns("hello world", []) == 1.0


def test_calculate_sns_identical_returns_zero():
    assert calculate_sns("hello world", ["hello world"]) == 0.0


def test_atomic_write_replaces_existing(tmp_path: Path):
    p = tmp_path / "a.txt"
    p.write_text("old", encoding="utf-8")
    atomic_write(p, "new")
    assert p.read_text(encoding="utf-8") == "new"
    # No leftover tmp files
    leftovers = [x for x in tmp_path.iterdir() if x.name != "a.txt"]
    assert leftovers == []


def test_choose_direction_uses_endpoint(fake_server, base_dir):
    url, handler = fake_server
    handler.responses.append("CHOSEN_INDEX: [2]")
    agent = LivingAgent(base_dir=base_dir, client=KoboldClient(endpoint=url, max_retries=1))
    options = [("a", "cell_R0_C0.md"), ("b", "cell_R0_C1.md"), ("c", "cell_R0_C2.md")]
    idx = agent.choose_direction("node body", options, "soul", [])
    assert idx == 2
    assert handler.received[0]["path"] == "/api/v1/generate"
    assert "CHOSEN_INDEX" in handler.received[0]["payload"]["prompt"]


def test_choose_direction_fallback_on_unparseable(fake_server, base_dir):
    url, handler = fake_server
    handler.responses.append("no index here")
    agent = LivingAgent(
        base_dir=base_dir,
        client=KoboldClient(endpoint=url, max_retries=1),
        rng=random.Random(0),
    )
    options = [("a", "x.md"), ("b", "y.md")]
    idx = agent.choose_direction("c", options, "s", [])
    assert 0 <= idx < 2


def test_run_cycle_updates_soul_atomically(fake_server, base_dir):
    url, handler = fake_server
    # Feed enough reasoning + synthesis responses
    for _ in range(20):
        handler.responses.append("CHOSEN_INDEX: [0]")
    handler.responses.append("# Paper\nAbstract: done.")
    agent = LivingAgent(
        base_dir=base_dir,
        client=KoboldClient(endpoint=url, max_retries=1),
        rng=random.Random(0),
    )
    result = agent.run_cycle()
    assert result["cycle"] == 3
    # Soul was updated with cycle+1
    new_soul = (base_dir / "soul.md").read_text(encoding="utf-8")
    assert "Current Cycle: 4" in new_soul
    # Paper artifact written
    assert (base_dir / "memories" / "semantic" / "paper_3.md").exists()
    # Episodic artifact written
    assert (base_dir / "memories" / "episodic" / "cycle_3.md").exists()
