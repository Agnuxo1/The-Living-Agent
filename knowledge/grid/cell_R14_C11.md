# Cell [14,11] — KNOWLEDGE
**FQN**: `HeytingLean.Contracts.Examples.tensorPack.eq_1`
**Module**: `HeytingLean.Tests.Compliance`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 4

## Topic
**Declaration**: eq_1
**Signature**: `∀ (α : Type u) [inst : HeytingLean.LoF.PrimaryAlgebra α] (R : HeytingLean.LoF.Reentry α) (flags : HeytingLean.Contracts.Examples.BridgeFlags), Eq (HeytingLean.Contracts.Examples.tensorPack α R flags) (if h : Eq flags.useTensorIntensity Bool.true then let model := HeytingLean.Contracts.Examples.tensorIntensityModel α R; have hR := ⋯; have hcontr := model.contract; { Carrier := model.Carrier, contract := ⋯.mp hcontr } else { Carrier := (HeytingLean.Contracts.Examples.tensor α R 0).Carrier, contract := (HeytingLean.Contracts.Examples.tensor α R 0).contract })`

States eq 1. Use when your goal matches this shape or to rewrite subterms using this result.

## Keywords
1., eq, goal, heytinglean.contracts.examples.tensorpack.eq_1, states, use, when, your

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [tensorPack [dependency]](cell_R10_C12.md)
- ↖️ **NW**: [tensor [dependency]](cell_R5_C6.md)
