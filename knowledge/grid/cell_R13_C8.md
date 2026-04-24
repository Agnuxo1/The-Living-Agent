# Cell [13,8] — KNOWLEDGE
**FQN**: `HeytingLean.Tests.graph_alexandroff_process_collapse`
**Module**: `HeytingLean.Tests.Compliance`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 3

## Topic
**Declaration**: graph_alexandroff_process_collapse
**Signature**: `∀ {α : Type u} [inst : HeytingLean.LoF.PrimaryAlgebra α] (R : HeytingLean.LoF.Reentry α) (n : Nat) (x : α), (HeytingLean.Bridges.Graph.Alexandroff.Model.processUpper (HeytingLean.Contracts.Examples.graph α R)).memOpen x → (HeytingLean.Bridges.Graph.Alexandroff.Model.processUpper (HeytingLean.Contracts.Examples.graph α R)).memOpen ((HeytingLean.Contracts.Examples.graph α R).stageCollapseAt n x)`

Collapsing a stage in the Alexandroff process keeps the point inside the open process region.

## Keywords
a, alexandroff, collapsing, heytinglean.tests.graph_alexandroff_process_collapse, in, process, stage, the

---
## Navigation (real dependency / similarity edges)
- ⬆️ **N**: [Reentry [dependency]](cell_R1_C8.md)
- ↖️ **NW**: [processUpper [dependency]](cell_R6_C5.md)
