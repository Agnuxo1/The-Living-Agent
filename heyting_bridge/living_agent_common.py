#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


_DEFAULT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(os.environ.get("HEYTING_ROOT", str(_DEFAULT_ROOT))).resolve()
DEFAULT_LIVING_AGENT_ROOT = Path(os.environ.get("LIVING_AGENT_ROOT", "/tmp/the-living-agent"))
DEFAULT_NUCLEUSDB_ROOT = Path(os.environ.get("NUCLEUSDB_ROOT", "/home/abraxas/Work/nucleusdb"))
DEFAULT_ARTIFACT_ROOT = Path(
    os.environ.get("HEYTING_ARTIFACT_DIR", str(REPO_ROOT / "artifacts" / "living_agent"))
).resolve()
DEFAULT_GRID_ROOT = Path(
    os.environ.get("HEYTING_GRID_ROOT", str(DEFAULT_ARTIFACT_ROOT / "verified_grid"))
).resolve()
TOKEN_RE = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_.-]*")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=False)
        handle.write("\n")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_whitespace(text: str) -> str:
    if text is None:
        return ""
    if not isinstance(text, str):
        try:
            text = json.dumps(text, sort_keys=True)
        except TypeError:
            text = str(text)
    return re.sub(r"\s+", " ", text).strip()


def tokenize(text: str) -> list[str]:
    return [tok.lower() for tok in TOKEN_RE.findall(text)]


def python_runtime() -> str:
    env_override = os.environ.get("LIVING_AGENT_EMBED_PYTHON")
    if env_override:
        return env_override
    venv_python = DEFAULT_LIVING_AGENT_ROOT / ".venv" / "bin" / "python"
    if venv_python.exists():
        return str(venv_python)
    return sys.executable


def ensure_module_runtime(module_name: str) -> None:
    if importlib.util.find_spec(module_name) is not None:
        return
    preferred = python_runtime()
    if preferred == sys.executable:
        return
    os.execv(preferred, [preferred] + sys.argv)


def run(
    argv: list[str],
    *,
    cwd: Path | None = None,
    input_text: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    timeout_secs: int | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=str(cwd or REPO_ROOT),
        input=input_text,
        text=True,
        capture_output=True,
        env=env,
        check=check,
        timeout=timeout_secs,
    )


def run_json(
    argv: list[str],
    *,
    cwd: Path | None = None,
    input_text: str | None = None,
) -> Any:
    proc = run(argv, cwd=cwd, input_text=input_text, check=False)
    if proc.returncode != 0:
        raise RuntimeError(
            f"command failed ({proc.returncode}): {' '.join(argv)}\n"
            f"stdout:\n{proc.stdout}\n"
            f"stderr:\n{proc.stderr}"
        )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"command returned non-JSON output: {' '.join(argv)}\n{proc.stdout}"
        ) from exc
