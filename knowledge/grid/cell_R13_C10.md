# Cell [13,10] — KNOWLEDGE
**FQN**: `HeytingLean.Tests.graph_alexandroff_round_verified`
**Module**: `HeytingLean.Tests.Compliance`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 3

## Topic
**Declaration**: graph_alexandroff_round_verified
**Signature**: `∀ {α : Type u} [inst : HeytingLean.LoF.PrimaryAlgebra α] (R : HeytingLean.LoF.Reentry α) (a : R.Omega), let model := HeytingLean.Bridges.Graph.Alexandroff.Model.univ (HeytingLean.Contracts.Examples.graph α R); Eq (model.decode (model.contract.encode a)) a`

The Alexandroff graph model decodes an encoded state back to the original element.

## Keywords
alexandroff, an, decodes, encoded, graph, heytinglean.tests.graph_alexandroff_round_verified, model, the

---
## Navigation (real dependency / similarity edges)
- ↖️ **NW**: [univ [dependency]](cell_R6_C7.md)
