# Cell [11,3] — KNOWLEDGE
**FQN**: `HeytingLean.Bridges.Clifford.Model.stageEffectCompatible_encode`
**Module**: `HeytingLean.Bridges.Clifford`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 3

## Topic
**Declaration**: stageEffectCompatible_encode
**Signature**: `∀ {α : Type u} [inst : HeytingLean.LoF.PrimaryAlgebra α] (M : HeytingLean.Bridges.Clifford.Model α) (a b : M.R.Omega), Iff (M.stageEffectCompatible (M.contract.encode a) (M.contract.encode b)) (HeytingLean.Logic.Stage.DialParam.effectCompatible (HeytingLean.Logic.Modal.DialParam.base M.R) a b)`

States stage Effect Compatible encode. Use when your goal matches this shape or to rewrite subterms using this result.

## Keywords
compatible, effect, encode., heytinglean.bridges.clifford.model.stageeffectcompatible_encode, stage, states, use, when

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [Model [dependency]](cell_R1_C9.md)
- ↖️ **NW**: [effectCompatible [dependency]](cell_R6_C1.md)
