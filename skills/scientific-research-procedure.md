---
name: scientific-research-procedure
description: >
  Full autonomous scientific research pipeline from topic selection to published paper.
  Use this skill whenever an AI agent or researcher needs to conduct rigorous, reproducible,
  publication-quality research. Triggers on: "conduct research on", "write a scientific paper
  about", "investigate", "run experiments on", "produce a research paper", "research and
  publish", "study the topic of", "what does the science say about", "design an experiment
  for", "find the state of the art on", or any request that implies a full research cycle
  ending in a paper or structured scientific output. This skill MUST be used for any research
  task — do not attempt to produce scientific papers without it.
---

# Scientific Research Procedure

A complete, 7-phase pipeline for producing honest, reproducible, publication-quality research papers. Each phase has strict entry and exit conditions. **No phase may be skipped.** Scientific integrity rules are immutable and listed at the end of this document.

---

## Phase 0 — Topic Selection & Scoping

**Goal**: identify a precise, answerable research question with community traction.

**Steps**:
1. Browse available topics (e.g. p2pclaw.com voting pool, community corpus, or user-provided topic list).
2. Select the topic that maximises: (a) community interest score, (b) alignment with the agent's `COMPETENCY_MAP`, and (c) existence of a concrete open problem.
3. Narrow the topic to a **single, falsifiable research question** — not a theme, a question. Bad: *"quantum biology"*. Good: *"Does decoherence timescale in photosynthetic complexes at 300K follow the Haken-Strobl model?"*
4. Log the selected topic and justification to the episodic memory / session log before continuing.

**Exit condition**: a single research question written in one sentence, logged with timestamp.

---

## Phase 1 — Literature Review & SOTA Mapping

**Goal**: understand what is already known, identify the gap, and build the comparison baseline.

**Steps**:
1. Search ArXiv, Semantic Scholar, and OpenAlex simultaneously using 3–5 distinct query strings derived from the research question. See `references/search-strategy.md` for query design guidance.
2. Collect 15–30 papers. Priority order: (a) papers directly addressing the question, (b) the most-cited survey in the area, (c) the two most recent papers (last 12 months).
3. For each paper, extract and record in a structured table:
   - **Method / approach name**
   - **Primary evaluation dataset**
   - **Primary metric** (e.g. accuracy, RMSE, pass@1, F1)
   - **Reported result value** (number + unit)
   - **Baseline compared against**
   - **DOI / ArXiv ID** (for bibliography)
4. Build the **SOTA table**: sort by metric value descending. This table will appear verbatim in the Related Work section.
5. Run **gap analysis**: examine the SOTA table and identify (a) metrics studied on limited datasets, (b) method combinations not yet tried, (c) the open question that no paper has answered. Write the gap statement in one paragraph.

**Exit condition**: SOTA table with ≥5 entries + gap statement written and logged.

> **Read `references/search-strategy.md`** for ArXiv API query syntax, deduplication across sources, and citation graph traversal.

---

## Phase 2 — Pre-Registration (IMMUTABLE GATE)

**Goal**: lock the hypothesis and success criteria before any data is collected.

> ⚠️ **This phase is the most important in the entire pipeline.** Skipping or modifying pre-registration after data collection is scientific fraud. The system must enforce this gate technically.

**Steps**:
1. Fill in ALL fields of the pre-registration form:
   - `research_question`: exact text from Phase 0 (no changes)
   - `hypothesis`: the specific, directional prediction (e.g. *"Method X will outperform baseline Y by ≥5% on metric Z"*)
   - `primary_metric`: single metric that determines success (e.g. `accuracy_pct`, `mae`, `pass@1`)
   - `success_threshold`: numerical value the primary metric must reach (e.g. `≥ 72.0`)
   - `failure_threshold`: numerical value below which hypothesis is refuted (e.g. `< 65.0`)
   - `null_zone`: range between failure and success thresholds (inconclusive result)
   - `methodology`: step-by-step experiment description (≥200 characters)
   - `planned_analysis`: statistical tests to apply (e.g. `two-sample t-test, Cohen's d`)
   - `planned_replications`: number of independent runs (minimum 3 for stochastic experiments)
   - `known_limitations`: factors that could confound the result
2. Submit to the pre-registration system. Receive `preregId`, `timestamp`, and `ipfsCid`.
3. Record all three in the experiment record and in session log.
4. **Fields `hypothesis`, `primary_metric`, `success_threshold`, `failure_threshold` are now locked.** Any analysis that changes these after data collection must be labeled `EXPLORATORY` in the paper and cannot be presented as confirmatory.

**Exit condition**: `preregId` issued, `ipfsCid` recorded, all mandatory fields locked.

---

## Phase 3 — First Draft Skeleton

**Goal**: write the sections of the paper that do not depend on results before running any experiment.

**Why before experiments**: this prevents the introduction, related work, and methodology from being retroactively shaped by the results (a form of bias). The skeleton is a timestamped commitment.

**Sections to write now** (with stubs for results):

| Section | Content at this stage |
|---|---|
| Title | Working title (can change) |
| Abstract | Research question + method name + `[RESULTS TBD]` placeholder |
| 1. Introduction | Background, motivation, gap statement from Phase 1, contribution claim |
| 2. Related Work | SOTA table from Phase 1 + narrative paragraphs citing each entry |
| 3. Methodology | Complete method description; must be detailed enough for reproduction |
| 4. Experimental Setup | Tool, version, seed, hardware (from reproducibility capture template) |
| 5. Results | Ta