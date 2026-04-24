# Cell [11,15] — KNOWLEDGE
**FQN**: `HeytingLean.Bridges.Tensor.Intensity.Model.stageOccam_encode`
**Module**: `HeytingLean.Bridges.Tensor.Intensity`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 3

## Topic
**Declaration**: stageOccam_encode
**Signature**: `∀ {α : Type u} [inst : HeytingLean.LoF.PrimaryAlgebra α] (M : HeytingLean.Bridges.Tensor.Intensity.Model) (bounds : optParam HeytingLean.Bridges.Tensor.Intensity.Bounds M.profile.bounds) (normalised : optParam Prop True) (a : M.core.R.Omega), Eq (M.stageOccam bounds normalised (M.encode bounds normalised a)) (M.encode bounds normalised (HeytingLean.LoF.Reentry.Omega.mk M.core.R (HeytingLean.Epistemic.occam M.core.R a.val) ⋯))`

Occam reduction on the intensity carrier reduces to the core Occam operation on Ω.

## Keywords
carrier, heytinglean.bridges.tensor.intensity.model.stageoccam_encode, intensity, occam, on, reduces, reduction, the

---
## Navigation (real dependency / similarity edges)
- ↖️ **NW**: [Bounds [dependency]](cell_R0_C10.md)
