# Cell [14,8] — KNOWLEDGE
**FQN**: `HeytingLean.Contracts.Examples.graphPack.eq_1`
**Module**: `HeytingLean.Tests.Compliance`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 4

## Topic
**Declaration**: eq_1
**Signature**: `∀ (α : Type u) [inst : HeytingLean.LoF.PrimaryAlgebra α] (R : HeytingLean.LoF.Reentry α) (flags : HeytingLean.Contracts.Examples.BridgeFlags), Eq (HeytingLean.Contracts.Examples.graphPack α R flags) (if h : Eq flags.useGraphAlexandroff Bool.true then let model := HeytingLean.Bridges.Graph.Alexandroff.Model.univ (HeytingLean.Contracts.Examples.graph α R); have hR := ⋯; have hcontr := model.contract; { Carrier := model.Carrier, contract := ⋯.mp hcontr } else { Carrier := (HeytingLean.Contracts.Examples.graph α R).Carrier, contract := (HeytingLean.Contracts.Examples.graph α R).contract })`

States eq 1. Use when your goal matches this shape or to rewrite subterms using this result.

## Keywords
1., eq, goal, heytinglean.contracts.examples.graphpack.eq_1, states, use, when, your

---
## Navigation (real dependency / similarity edges)
- ⬆️ **N**: [Reentry [dependency]](cell_R1_C8.md)
- ↗️ **NE**: [graphPack [dependency]](cell_R10_C11.md)
- ↖️ **NW**: [univ [dependency]](cell_R6_C7.md)
