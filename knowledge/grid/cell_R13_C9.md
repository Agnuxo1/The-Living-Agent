# Cell [13,9] — KNOWLEDGE
**FQN**: `HeytingLean.Tests.graph_alexandroff_process_expand`
**Module**: `HeytingLean.Tests.Compliance`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 3

## Topic
**Declaration**: graph_alexandroff_process_expand
**Signature**: `∀ {α : Type u} [inst : HeytingLean.LoF.PrimaryAlgebra α] (R : HeytingLean.LoF.Reentry α) (n : Nat) (x : α), (HeytingLean.Bridges.Graph.Alexandroff.Model.processUpper (HeytingLean.Contracts.Examples.graph α R)).memOpen x → (HeytingLean.Bridges.Graph.Alexandroff.Model.processUpper (HeytingLean.Contracts.Examples.graph α R)).memOpen ((HeytingLean.Contracts.Examples.graph α R).stageExpandAt n x)`

Every expansion step of the Alexandroff process preserves membership in the open region.

## Keywords
alexandroff, every, expansion, heytinglean.tests.graph_alexandroff_process_expand, of, process, step, the

---
## Navigation (real dependency / similarity edges)
- ↖️ **NW**: [processUpper [dependency]](cell_R6_C5.md)
