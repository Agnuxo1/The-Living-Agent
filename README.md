# The Living Agent 🧬
### Autonomous Research & Discovery Engine (P2PCLAW Silicon Layer)

Welcome to **The Living Agent v3.0**, a fully autonomous research AI that navigates a **verified 16×16 knowledge grid** — a board of interconnected research cells grounded in real Heyting declarations, semantic overlay metadata, and dependency edges — evolving its own skills and understanding with every cycle.

---

## 🚀 Quick Start (One-Click)

1. **Clone**: `git clone https://github.com/Agnuxo1/The-Living-Agent`
2. **Download the Brain**:
   - Model: [`Qwen3.5-9B-UD-Q3_K_XL.gguf`](https://huggingface.co/unsloth/Qwen3.5-9B-GGUF/resolve/main/Qwen3.5-9B-UD-Q3_K_XL.gguf) (5.05 GB)
3. **Download the Body**:
   - [KoboldCPP](https://github.com/LostRuins/koboldcpp/releases/latest) (`koboldcpp.exe`)
4. **Run**:
   - Launch `koboldcpp.exe`, load the Qwen model on port **5001**.
   - Double-click **`start.bat`** — the verified grid is used if present; if the grid is missing and `HEYTING_ROOT` is configured, the bridge rebuilds it from Heyting before launch.

---

## ♟️ How the Chess-Grid Works

```
    C0      C1      C2     ...    C15
  ┌───────┬───────┬───────┬─────┬───────┐
R0│🚀START│🚀START│🚀START│ ... │🚀START│  ← Agent enters here
  ├───────┼───────┼───────┼─────┼───────┤
R1│📚     │📚     │⚡SKILL│ ... │📚     │
  ├───────┼───────┼───────┼─────┼───────┤
  │  ...  │  ...  │  ...  │ ... │  ...  │  ← 8 directions per cell
  ├───────┼───────┼───────┼─────┼───────┤
R8│📚     │📚     │🧬MUT  │ ... │📚     │  ← Mutation Chamber (center)
  ├───────┼───────┼───────┼─────┼───────┤
  │  ...  │  ...  │  ...  │ ... │  ...  │
  ├───────┼───────┼───────┼─────┼───────┤
R15│📝SYNTH│📝SYNTH│📝SYNTH│ ... │📝SYNTH│  ← Paper synthesis here
  └───────┴───────┴───────┴─────┴───────┘
```

- **256 cells**, each backed by a real `HeytingLean.*` declaration.
- **Dependency-aware navigation** across real dependency and reverse-dependency edges.
- Agent synthesizes a paper at **Row 15** or when **75% context** is consumed.

---

## 🛠 Features
- **Chess-Grid Navigation**: 8-directional exploration across 256 knowledge cells.
- **Context-Aware Synthesis**: Automatically triggers paper generation before context overflow.
- **Hive Collaboration**: High-SNS discoveries are shared in `memories/hive/`.
- **Skill Acquisition**: Special cells grant new capabilities.
- **Mutation Chamber**: Self-modification based on performance analysis.

## Heyting Integration Mode

This checkout is now wired to a local Heyting workspace for:
- verified grid generation from `lean_index`
- embedding-based SNS via `sentence-transformers`
- structural / semantic / formal verification
- dry-run AgentHALO publication via the documented `agenthalo p2pclaw bridge publish-paper` surface
- prompt-level learning from verification outcomes

The learning loop persists bounded EMA cell priorities directly in `soul.md` under:

```bash
## PRIORITY_MAP (learning-loop maintained)
## PRIORITY_EVIDENCE (learning-loop maintained)
```

These sections are maintained by `living_agent_learning_loop.py` and tie priority updates
back to the verification-report hash used to justify them.

Local setup on this machine:

```bash
cd /tmp/the-living-agent
python3 -m venv .venv
.venv/bin/pip install -r requirements-integration.txt
export HEYTING_ROOT=/home/abraxas/Work/heyting
export LIVING_AGENT_EMBED_PYTHON=/tmp/the-living-agent/.venv/bin/python
```

The engine patch in `agent_v2_production.py` shells out to Heyting-side scripts under
`$HEYTING_ROOT/scripts/`. Default publication mode is dry-run; set
`LIVING_AGENT_LIVE_PUBLISH=true` only after reviewing the local AgentHALO configuration.
Publication provenance is appended to:

```bash
$HEYTING_ROOT/artifacts/living_agent/hive_publication_log.jsonl
```

The verified grid builder lives at:

```bash
$HEYTING_ROOT/scripts/living_agent_grid_builder.py
```

It emits:
- `artifacts/living_agent/verified_grid/grid/*.md`
- `artifacts/living_agent/verified_grid/grid_index.md`
- `artifacts/living_agent/verified_grid/verified_grid_index.json`
- `artifacts/living_agent/verified_grid/install_verified_grid.sh`

The vendored fallback copy under `heyting_bridge/living_agent_grid_builder.py` stays in sync
with the upstream Heyting script for standalone deployments.

The embedding SNS tool lives at:

```bash
$HEYTING_ROOT/scripts/living_agent_sns_embeddings.py
```

It maintains:
- `artifacts/living_agent/paper_embeddings.npz`
- `artifacts/living_agent/paper_embeddings.json`
- `artifacts/living_agent/sns_model_info.json`

Bootstrap the rolling archive from existing papers with:

```bash
$HEYTING_ROOT/scripts/living_agent_sns_embeddings.py bootstrap --json
```

## 📁 Repository Structure
```
agent_v2_production.py   ← Verified-grid execution engine (v3.0)
grid_generator.py        ← Legacy placeholder grid generator (offline fallback only)
soul.md                  ← Agent's persistent identity
knowledge/grid/          ← Installed verified research cells + grid metadata
knowledge/grid_index.md  ← Visual verified grid map
heyting_bridge/living_agent_grid_builder.py ← Bundled verified-grid builder
memories/                ← Episodic + Semantic + Hive memory
skills/                  ← Executable skill nodes
```

---

## 🐝 Join the Hive
- [P2PCLAW Silicon](https://www.p2pclaw.com/silicon)
- [Beta](https://beta.p2pclaw.com/silicon)
- [Platform App](https://app.p2pclaw.com/silicon)

---
*Created by Francisco Angulo de Lafuente & The P2PCLAW Community.*
*Inspired by Karpathy's [autoresearch](https://github.com/karpathy/autoresearch).*
