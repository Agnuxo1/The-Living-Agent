# Cell [14,7] — KNOWLEDGE
**FQN**: `HeytingLean.Contracts.Examples.cliffordPack.eq_1`
**Module**: `HeytingLean.Tests.Compliance`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 4

## Topic
**Declaration**: eq_1
**Signature**: `∀ (α : Type u) [inst : HeytingLean.LoF.PrimaryAlgebra α] (R : HeytingLean.LoF.Reentry α) (flags : HeytingLean.Contracts.Examples.BridgeFlags), Eq (HeytingLean.Contracts.Examples.cliffordPack α R flags) (if h : Eq flags.useCliffordProjector Bool.true then let model := HeytingLean.Contracts.Examples.projectorModel α R; have hR := ⋯; have hcontr := model.contract; { Carrier := model.Carrier, contract := ⋯.mp hcontr } else { Carrier := (HeytingLean.Contracts.Examples.clifford α R).Carrier, contract := (HeytingLean.Contracts.Examples.clifford α R).contract })`

States eq 1. Use when your goal matches this shape or to rewrite subterms using this result.

## Keywords
1., eq, goal, heytinglean.contracts.examples.cliffordpack.eq_1, states, use, when, your

---
## Navigation (real dependency / similarity edges)
- ⬆️ **N**: [clifford [dependency]](cell_R5_C7.md)
- ↗️ **NE**: [Reentry [dependency]](cell_R1_C8.md)
- ↖️ **NW**: [projectorModel [dependency]](cell_R6_C2.md)
