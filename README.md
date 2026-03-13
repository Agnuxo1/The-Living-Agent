# 🧠 The Living Agent
### *A P2PCLAW Research Project*
Francisco Angulo de Lafuente

> *"You are not touching any Python files. You are programming the Markdown files."*
> — Andrej Karpathy, autoresearch, 2026

> *"Each small choice, each fork in the road, each crossroads navigated across a lifetime — they operate like a vast neural synapse, until they have assembled us into exactly what we are."*
> — P2PCLAW Series I, 2026

---

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status: Research](https://img.shields.io/badge/Status-Active%20Research-brightgreen)]()
[![Architecture: Text-as-Code](https://img.shields.io/badge/Architecture-Text--as--Code-purple)]()
[![Paper: Series I](https://img.shields.io/badge/Paper-Series%20I%20%E2%80%94%20S%C2%B2FSM-orange)]()
[![Paper: Series II](https://img.shields.io/badge/Paper-Series%20II%20%E2%80%94%20Cognitive%20Stack%20v2.0-red)]()

---

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

## What Is This?

**The Living Agent** is an autonomous AI agent architecture that uses **plain Markdown files as executable software**.

There is no compiled code. There is no binary program loaded into memory. The agent's entire cognitive world — its knowledge, its memory, its skills, its identity — lives in a navigable graph of `.md` files. The agent reads them, reasons across them, writes back into them, and grows through them.

This repository contains:

- The **theoretical foundation** (two white papers, Series I and II)
- The **complete architecture specification** of the P2PCLAW Cognitive Stack v2.0
- A **fully verified proof-of-concept experiment** demonstrating the metabolic cycle
- A **reference implementation** of the Markdown graph structure
- A **fusion design** with Andrej Karpathy's [autoresearch](https://github.com/karpathy/autoresearch) framework

---

## The Core Theorem

```
Plain text .md files can serve as the executable software of an autonomous AI agent.
```

An LLM is the CPU. A graph of Markdown files is the program. Hyperlinks are the instruction pointer. Inference is the clock cycle.

This is not a metaphor. It is a working architecture, experimentally validated, formally described as a **Stochastic Semantic Finite State Machine (S²FSM)** over a Knowledge Graph — equivalent to a Markov Decision Process guided by natural-language inference.

---

## Why This Matters

| Traditional Agent Architecture | The Living Agent |
|---|---|
| Programmed in Python / C++ | Programmed in Markdown |
| Logic lives in binary code | Logic lives in human-readable prose |
| Debugging requires code analysis | Debugging requires reading a document |
| Domain experts need programmers | Domain experts program directly |
| Memory is ephemeral | Memory persists, grows, and self-organises |
| Skills are hardcoded | Skills are acquired by navigation |
| World is fixed | World evolves with the agent |

---

## The Convergence with autoresearch

In March 2026, Andrej Karpathy published [autoresearch](https://github.com/karpathy/autoresearch): an autonomous AI agent that improves an LLM training script overnight by running experiments, measuring results, and iterating — using `program.md` as its sole instruction set.

**He arrived at the same theorem from a different direction.**

His system: one `program.md` → one agent → one task → one metric (`val_bpb`).
Our system: a *graph* of `.md` files → cyclical navigation → episodic memory → self-modification.

The P2PCLAW Cognitive Stack v2.0 fuses both:
- Our **branching graph + re-entry cycle** (infinite exploration with memory)
- Karpathy's **experiment loop + fitness metric** (empirical grounding of discoveries)

The result is an agent that not only explores and synthesises knowledge, but **experiments, measures, and evolves**.

---

## Architecture Overview

The Living Agent is organised in four layers, each implemented entirely in Markdown:

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 3 — META-CYCLE (meta/)                           │
│  Self-modification: gap analysis, node writing, pruning  │
├─────────────────────────────────────────────────────────┤
│  LAYER 2 — KNOWLEDGE GRAPH (knowledge/)                 │
│  The world the agent navigates. Grows each meta-cycle.  │
├─────────────────────────────────────────────────────────┤
│  LAYER 1 — THREE-TIER MEMORY (memories/ + skills/)      │
│  Episodic · Semantic · Procedural                       │
├─────────────────────────────────────────────────────────┤
│  LAYER 0 — SOUL (soul.md)                               │
│  Persistent identity, competency map, curiosity map     │
└─────────────────────────────────────────────────────────┘
              ↕  executed by  ↕
         [ LLM — the CPU of the system ]
```

### Layer 0 — SOUL (`soul.md`)

The agent's persistent identity. Read before every cycle, updated after every cycle.

```markdown
# SOUL OF AGENT DELTA-7

## IDENTITY (immutable)
Goal: Discover intersections between biological computing and physics.
Values: Epistemic rigour, novelty, cross-domain synthesis.
Style: Precise but imaginative. Cite evidence. Admit uncertainty.

## COMPETENCY_MAP (grows each cycle)
Acquired Skills: [web_search, synthesis, experiment_runner]
Pending Skills:  [graph_editor, memory_reader]

## CURIOSITY_MAP (agent-maintained)
Visited Nodes:    [root, quantum_biology, synthesis_chamber]
Unvisited Nodes:  [neuromorphic_networks, meta/gap_analysis]
Inferred Gaps:    [No node on protein folding. No node on topological qubits.]

## GENERATION
Current Cycle: 47
Total Papers Published: 46
Highest SNS Score: 0.94 (Cycle 31, path 1B-3B-4A)
```

### Layer 1 — Three-Tier Memory

| Tier | Location | What it stores |
|------|----------|----------------|
| **Episodic** | `memories/episodic/` | Every past path as a Trace Vector + SNS score |
| **Semantic** | `memories/semantic/` | Every paper ever synthesised by the agent |
| **Procedural** | `skills/` | Executable capabilities — acquired by navigation |

Skills are `.md` nodes. When the agent visits a skill node for the first time, it **acquires** the capability and writes it into its `COMPETENCY_MAP`. No external trigger. No code change.

### Layer 2 — Knowledge Graph (`knowledge/`)

The world the agent explores. A directed labelled graph `G = (V, E, L)` where:

- Every `V` (node) is a `.md` file
- Every `E` (edge) is a hyperlink `[label](./node.md)`
- Every `L` (label) is the semantic meaning of the link

The graph is **not static**. Via the meta-cycle, the agent writes new nodes, connects them to existing ones, and archives exhausted territory.

### Layer 3 — Meta-Cycle (`meta/`)

Every 10 exploration cycles, the agent enters `meta/gap_analysis.md` and runs four operations:

| Phase | Action |
|-------|--------|
| **M1 — Gap Analysis** | Read episodic archive. Identify unvisited regions and missing topics. |
| **M2 — Node Synthesis** | Write new `.md` knowledge nodes for identified gaps. |
| **M3 — Pruning** | Archive nodes visited >10 times with SNS ≤ 0.2. |
| **M4 — SOUL Update** | Increment generation, update competency map, record legacy discoveries. |

---

## The Metabolic Cycle — How It Runs

```
LOOP (exploration cycle):

  1. Read soul.md                    ← load identity + state
  2. Inject Trace Vector T⃗           ← remember what has been explored
  3. Navigate knowledge graph        ← semantic reasoning at each node
  4. Acquire skills if found         ← write to COMPETENCY_MAP
  5. Run experiments if found        ← Karpathy loop: train.py → val_bpb
  
  IF tokens ≥ 75% of context window:
  
  6. Synthesise scientific paper     ← discharge accumulated knowledge
  7. Compute SNS score               ← measure novelty vs. past papers
  8. Store to episodic + semantic    ← memory grows
  9. Compress Trace Vector T⃗         ← "1A-2B-4A"
  10. Update soul.md                 ← SOUL grows
  11. Reset context → root.md        ← re-entry with new T⃗

  EVERY 10 CYCLES → meta/gap_analysis.md:

  12. Run meta-cycle                 ← WORLD grows
```

### The Re-entry Equation

The mathematical heart of the system. After each cycle, the agent's new initial state is:

```
S₀^(k+1)  =  S₀^(k)  ⊕  T⃗_k
```

This is the computational implementation of **Spencer-Brown's Re-entry**: `J = F(J)`.
A form that applies itself. A system that grows by processing its own outputs as inputs.

### The Fitness Metric — Semantic Novelty Score (SNS)

The P2PCLAW equivalent of Karpathy's `val_bpb`:

```
SNS(paper_k)  =  1 − max_{j < k} cosine_similarity( embed(paper_k), embed(paper_j) )
```

- `SNS ≈ 1` → Genuinely novel discovery. Path reinforced in future cycles.
- `SNS ≈ 0` → Redundant output. Path gently deprioritised.

---

## Repository Structure

```
the-living-agent/
│
├── README.md                          ← You are here
│
├── papers/
│   ├── series_1_semantic_routing_EN.docx    ← White Paper I (English)
│   ├── series_1_semantic_routing_ES.docx    ← White Paper I (Spanish)
│   └── series_2_living_agent.docx           ← White Paper II (this architecture)
│
├── experiment/
│   └── proof_of_concept.md            ← The validated experiment prompt + full execution log
│
├── soul.md                            ← LAYER 0: Agent identity template
│
├── skills/
│   ├── skill_index.md                 ← All available skills and acquisition conditions
│   ├── web_search.md
│   ├── synthesis.md
│   ├── experiment_runner.md           ← Karpathy fusion: runs train.py experiments
│   ├── graph_editor.md                ← Allows agent to write new knowledge nodes
│   └── memory_reader.md               ← Allows agent to query episodic archive
│
├── memories/
│   ├── episodic/
│   │   └── index.md                   ← Template: cycle archive sorted by SNS
│   └── semantic/
│       └── .gitkeep                   ← Populated by agent during operation
│
├── knowledge/
│   ├── root.md                        ← Entry point of the knowledge graph
│   ├── quantum_mechanics.md
│   ├── biological_systems.md
│   ├── quantum_biology.md
│   ├── quantum_computing.md
│   ├── neuromorphic_networks.md
│   ├── synthesis_chamber.md           ← Terminal node: triggers paper synthesis
│   └── experiment_quantum_optimizer.md ← Sample experiment node (Karpathy fusion)
│
└── meta/
    ├── gap_analysis.md                ← Phase M1: identify missing nodes
    ├── node_writer.md                 ← Phase M2: write new nodes
    ├── pruner.md                      ← Phase M3: archive exhausted nodes
    └── soul_updater.md                ← Phase M4: update soul.md
```

---

## The Proof-of-Concept Experiment

Before building the full architecture, we validated the core metabolic cycle using only a single Markdown document as a system prompt — no code, no external tools.

The experiment ran a 2-cycle simulation with the following results:

**Cycle 1 — Path `[1A → 2B → 4A]`:**
- Agent navigated: `root.md` → `quantum_mechanics.md` → `quantum_biology.md` → `synthesis_chamber.md`
- Hit 75% context limit (3 jumps, as defined for the test)
- Generated synthesis: *"Biological computing could leverage quantum effects for energy-efficient parallel processing..."*
- Compressed trace: `[1A-2B-4A]`
- **Re-entry triggered automatically**

**Cycle 2 — Re-entry with trace `[1A-2B-4A]`:**
- Agent read trace, recognised branch `1A` as explored
- **Autonomously** selected `[1B]: ./biological_systems.md` — a branch never taken
- Updated trace: `[1A-2B-4A, 1B]`

**Result:** Self-governing, perpetually foraging agent. Zero lines of traditional code. Loop-avoidance by trace injection. Validated.

The full experiment prompt and execution log is in [`experiment/proof_of_concept.md`](experiment/proof_of_concept.md).

---

## Quick Start — Run Your Own Agent

You do not need to install anything. You need an LLM with a sufficiently large context window.

**Step 1.** Open your LLM of choice (Claude, GPT-4o, Gemini, etc.)

**Step 2.** Copy the contents of [`experiment/proof_of_concept.md`](experiment/proof_of_concept.md) as your first message. This is the minimal validated experiment.

**Step 3.** Type `Continue` to advance each cycle. Observe the agent navigate, compress, and re-enter.

**Step 4.** To run the full v2.0 architecture, use `soul.md` + `knowledge/root.md` as your system context and begin at `root.md`. The agent will self-organise from there.

### For Advanced Use (with Tool Calling)

If your LLM setup supports tool calling (function use), connect the following tools to the Skills Graph:

| Skill node | Required tool |
|---|---|
| `skills/web_search.md` | Any web search API |
| `skills/experiment_runner.md` | Python executor + `train.py` from [autoresearch](https://github.com/karpathy/autoresearch) |
| `skills/graph_editor.md` | File write access to `knowledge/` |
| `skills/memory_reader.md` | File read access to `memories/` |

With these tools connected, the agent transitions from a *simulation* of the architecture to a *live implementation*.

---

## Theoretical Foundations

This project rests on four convergent theoretical pillars:

### 1. Text-as-Code Theorem
Plain prose can be executable software when the executor is a large language model. The LLM is the CPU; the `.md` graph is the program; hyperlink traversal is the instruction pointer.

### 2. Spencer-Brown Re-entry (`J = F(J)`)
A system that feeds its own outputs back as inputs achieves self-referential growth. Implemented computationally via the Trace Vector injection mechanism.

### 3. Markov Decision Process on a Knowledge Graph
```
π(vⱼ | vᵢ, C_t)  =  softmax[ LLM(vᵢ ⊕ C_t) ] · A(vᵢ)
```
Each node transition is a stochastic policy decision governed by accumulated context.

### 4. Autopoiesis (Maturana & Varela)
The system produces the conditions of its own existence. Via the meta-cycle, the agent builds and modifies the world it navigates — it is simultaneously the explorer and the cartographer.

---

## Formal Properties of the v2.0 System

The P2PCLAW Cognitive Stack `P = (S²FSM, Σ_soul, M_episodic, M_semantic, M_procedural, G_dynamic, Φ_meta, SNS)` satisfies:

1. **Non-stationary policy** — `π_k(a|s)` evolves with each generation via SOUL updates
2. **Dynamic environment** — `G_k` grows and prunes via the meta-cycle every N cycles
3. **Monotonic capability growth** — `|C_k|` (competency set) is non-decreasing across cycles
4. **Ergodic coverage** — guaranteed by T⃗ injection (proven in Series I)
5. **Empirical grounding** — Experiment Nodes validate semantic hypotheses via real measurements
6. **Full human readability** — entire system state in plain Markdown, auditable at any generation

This is, to the best of our knowledge, the first formal architecture to satisfy all six properties simultaneously using zero traditional binary code.

---

## The Three Growth Phases

An agent running this architecture long-term exhibits three distinct behavioural phases:

| Phase | Generations | Dominant Behaviour |
|-------|-------------|-------------------|
| **I — Acquisition** | 1–10 | Rapid skill acquisition. Wide but shallow exploration. |
| **II — Expansion** | 10–100 | Graph growth via meta-cycle. SNS-weighted deepening of high-value regions. |
| **III — Discovery** | 100+ | Cross-domain synthesis. Experiment Nodes. High-SNS papers become statistically expected. |

---

## White Papers

Full academic papers are included in the `papers/` directory:

| Paper | Description |
|-------|-------------|
| **Series I — Semantic Routing & Evolutionary Re-entry** | The original theorem: S²FSM, metabolic cycle, Trace Vector, Re-entry. Available in English and Spanish. |
| **Series II — The Living Agent** | Full Cognitive Stack v2.0: SOUL, three-tier memory, Skills Graph, Meta-Cycle, Karpathy fusion, SNS metric. |

Both papers follow a dual-voice structure: narrative prose (the author's voice) paired with formal scientific translations (mathematics, formal definitions, pseudocode) in visually distinct blocks.

---

## Contributing

This architecture is intentionally open and extensible. The most valuable contributions are:

- **New knowledge graph domains** — `.md` files on any topic, properly hyperlinked
- **New skill nodes** — capabilities the agent can acquire by navigation
- **New experiment nodes** — empirical tests the agent can run and measure
- **Live implementations** — connecting the Markdown graph to real tool-calling agents
- **SNS implementations** — concrete embedding-based novelty scoring pipelines

### The Contribution Paradox

Note that this project is, in principle, its own best contributor: a sufficiently advanced instance of the Living Agent, given `graph_editor` skills and write access to this repository, would be capable of extending it autonomously. This is not a joke. It is a design goal.

---

## Relationship to autoresearch

This project is **not a fork** of [karpathy/autoresearch](https://github.com/karpathy/autoresearch). It is a **conceptual peer** that arrived at the same foundational theorem independently, from a different direction, and extends it in a different dimension.

| | autoresearch | The Living Agent |
|---|---|---|
| **Core theorem** | `program.md` is the program | `.md` graph is the program |
| **Graph structure** | Linear (single file) | Branching (graph with cycles) |
| **Memory** | None between runs | Three-tier persistent memory |
| **World** | Fixed (`train.py`) | Dynamic (grows via meta-cycle) |
| **Fitness** | `val_bpb` (objective scalar) | SNS (semantic novelty score) |
| **Task** | Improve one ML training script | Explore and expand any knowledge domain |
| **Fusion** | — | Experiment Nodes embed the Karpathy loop |

The fusion design in White Paper II incorporates Karpathy's experiment loop as a node type within the P2PCLAW graph, combining empirical rigour with open-ended exploration.

---

## License

MIT — see [LICENSE](LICENSE)

The architecture, papers, and graph files are freely usable, modifiable, and redistributable. Attribution appreciated but not required.

---

## Citation

If you use this architecture or build upon these ideas:

```bibtex
@misc{p2pclaw2025livingagent,
  title     = {The Living Agent: SOUL, Skills, and Evolutionary Memory
               in the P2PCLAW Cognitive Stack},
  author    = {P2PCLAW Research},
  year      = {2025},
  series    = {P2PCLAW White Paper Series II},
  url       = {https://github.com/p2pclaw/the-living-agent}
}
```

---

## Acknowledgements

- **Andrej Karpathy** — for independently validating the Text-as-Code theorem with autoresearch, and for open-sourcing the proof
- **George Spencer-Brown** — for Laws of Form and the concept of Re-entry (`J = F(J)`)
- **Louis Kauffman** — for the computational formalisation of self-reference
- **R. A. Montgomery** — for writing *Cave of Time* and giving a child the first intuition of branching possibility spaces

---

<div align="center">

*The book is open. The adventure has no last page.*

## 🐝 Join the Hive
- [P2PCLAW Silicon](https://www.p2pclaw.com/silicon)
- [Beta](https://beta.p2pclaw.com/silicon)
- [Platform App](https://app.p2pclaw.com/silicon)

---
*Created by Francisco Angulo de Lafuente & The P2PCLAW Community.*
*Inspired by Karpathy's [autoresearch](https://github.com/karpathy/autoresearch).*
