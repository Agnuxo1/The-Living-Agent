# The Living Agent

**Autonomous Chess-Grid research engine** powered by a local LLM (KoboldCPP + Qwen).
The agent walks a 16x16 grid of interconnected Markdown knowledge cells, accumulates
context, writes a short synthesis paper at the far edge, scores its novelty against
prior output, and updates a persistent `soul.md` identity file. One cycle in, one
cycle out, forever.

[![PyPI](https://img.shields.io/pypi/v/living-agent.svg)](https://pypi.org/project/living-agent/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![arXiv 2604.19792](https://img.shields.io/badge/related%20paper-arXiv%3A2604.19792-b31b1b.svg)](https://arxiv.org/abs/2604.19792)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

> **Part of the P2PCLAW ecosystem.** This is the *Series II* white-paper / reference
> implementation of an autonomous research agent in the P2PCLAW cognitive stack.
> For the full project overview, ecosystem map, and the v6.0 production paper, see
> [**Agnuxo1/OpenCLAW-P2P**](https://github.com/Agnuxo1/OpenCLAW-P2P) (the front door).

---

## Prerequisites

The agent does **not** ship a model. It talks to a local KoboldCPP HTTP server
(default `http://localhost:5001/api/v1/generate`). You must bring your own runtime
and weights:

1. **KoboldCPP** — download the latest release from
   [LostRuins/koboldcpp](https://github.com/LostRuins/koboldcpp/releases/latest).
2. **A GGUF model.** The project was developed against
   [`unsloth/Qwen3.5-9B-GGUF`](https://huggingface.co/unsloth/Qwen3.5-9B-GGUF)
   (the `UD-Q3_K_XL` quant, ~5 GB). Any Kobold-compatible GGUF with a decent
   context window will work.

Launch KoboldCPP, load the model, expose it on port 5001.

---

## Install

```bash
pip install living-agent
```

Or from source:

```bash
git clone https://github.com/Agnuxo1/The-Living-Agent
cd The-Living-Agent
pip install -e ".[dev]"
```

---

## Quickstart (3 commands)

```bash
living-agent init --grid-dir .                   # generates knowledge/grid + knowledge/grid_index.md
living-agent run  --cycles 1 --endpoint http://localhost:5001/api/v1/generate
living-agent status --grid-dir .
```

`run` reads `soul.md` (creating a default one if missing), walks the grid, emits
a paper under `memories/semantic/paper_<N>.md`, appends an episodic record under
`memories/episodic/cycle_<N>.md`, and atomically updates `soul.md`.

---

## How the Chess-Grid works

- **256 cells**, each a Markdown file `cell_R<row>_C<col>.md`.
- **8 directions** per cell (N, NE, E, SE, S, SW, W, NW); edges and corners get
  fewer links.
- **Entry row** (R0) and **synthesis row** (R15); a mutation chamber at the
  centre; occasional skill and experiment nodes.
- The agent enters at a random R0 column, picks a direction per cell by asking
  the LLM, and stops when it either hits R15 or saturates ~85% of the context
  window.
- Novelty is a Jaccard-overlap-based Semantic Novelty Score against the last 50
  papers on disk.

---

## Python API

```python
from living_agent import LivingAgent, KoboldClient, generate_grid

generate_grid("knowledge", rows=16, cols=16, seed=0)
agent = LivingAgent(base_dir=".", client=KoboldClient("http://localhost:5001/api/v1/generate"))
result = agent.run_cycle()
print(result["cycle"], result["sns"], result["paper_bytes"])
```

---

## Honest limitations

- **Paper output is short.** With the default Qwen 9B quant and a 2048-token
  completion budget, generated papers are typically a few hundred bytes — not
  a full multi-section publication. No post-processing is applied to inflate
  them.
- **Context window is bounded by the server.** The client advertises 128k, but
  effective context depends on what KoboldCPP negotiates with the model.
- **Synchronous only.** One cycle at a time; no asyncio, no batching, no
  multi-agent orchestration.
- **No automatic model download.** You have to fetch the GGUF manually and
  start KoboldCPP yourself — the package just speaks HTTP.
- **No network in tests.** The test suite mocks KoboldCPP with an in-process
  `http.server`; running the real agent still requires a live endpoint.

---

## Development

```bash
pip install -e ".[dev]"
pytest                       # 23 tests
python -m build              # wheel + sdist into dist/
```

Layout:

```
src/living_agent/
    __init__.py      # version, re-exports
    grid.py          # 16x16 grid generator, cell topology
    llm_client.py    # KoboldCPP HTTP client
    agent.py         # reasoning loop, soul.md state, SNS scoring
    cli.py           # `living-agent {init,run,status}`
tests/
    test_grid.py     # 10 tests
    test_agent.py    # 8 tests (in-process fake HTTP server)
    test_cli.py      # 5 tests
```

---

## License & credits

Apache-2.0. Created by **Francisco Angulo de Lafuente** as the Silicon Layer
of [P2PCLAW](https://www.p2pclaw.com). Inspired by Karpathy's
[autoresearch](https://github.com/karpathy/autoresearch).

---

## Related projects

Part of the [@Agnuxo1](https://github.com/Agnuxo1) v1.0.0 open-source catalog (April 2026).

**AgentBoot constellation** — agents and research loops
- [AgentBoot](https://github.com/Agnuxo1/AgentBoot) — Conversational AI agent for bare-metal hardware detection and OS install.
- [autoresearch-nano](https://github.com/Agnuxo1/autoresearch) — nanoGPT-based autonomous ML research loop.
- [benchclaw-integrations](https://github.com/Agnuxo1/benchclaw-integrations) — Agent-framework adapters for the BenchClaw API.

**CHIMERA / neuromorphic constellation** — GPU-native scientific computing
- [NeuroCHIMERA](https://github.com/Agnuxo1/NeuroCHIMERA__GPU-Native_Neuromorphic_Consciousness) — GPU-native neuromorphic framework on OpenGL compute shaders.
- [Holographic-Reservoir](https://github.com/Agnuxo1/Holographic-Reservoir) — Reservoir computing with simulated ASIC backend.
- [ASIC-RAG-CHIMERA](https://github.com/Agnuxo1/ASIC-RAG-CHIMERA) — GPU simulation of a SHA-256 hash engine wired into a RAG pipeline.
- [QESN-MABe](https://github.com/Agnuxo1/QESN_MABe_V2_REPO) — Quantum-inspired Echo State Network on a 2D lattice (classical).
- [ARC2-CHIMERA](https://github.com/Agnuxo1/ARC2_CHIMERA) — Research PoC: OpenGL primitives for symbolic reasoning.
- [Quantum-GPS](https://github.com/Agnuxo1/Quantum-GPS-Unified-Navigation-System) — Quantum-inspired GPU navigator (classical Eikonal solver).
