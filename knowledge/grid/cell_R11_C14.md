# Cell [11,14] — KNOWLEDGE
**FQN**: `HeytingLean.Bridges.Tensor.Intensity.Model.stageMvAdd_encode`
**Module**: `HeytingLean.Bridges.Tensor.Intensity`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 3

## Topic
**Declaration**: stageMvAdd_encode
**Signature**: `∀ {α : Type u} [inst : HeytingLean.LoF.PrimaryAlgebra α] (M : HeytingLean.Bridges.Tensor.Intensity.Model) (bounds : optParam HeytingLean.Bridges.Tensor.Intensity.Bounds M.profile.bounds) (normalised : optParam Prop True) (a b : M.core.R.Omega), Eq (M.stageMvAdd bounds normalised (M.encode bounds normalised a) (M.encode bounds normalised b)) (M.encode bounds normalised (HeytingLean.Logic.Stage.DialParam.mvAdd (HeytingLean.Logic.Modal.DialParam.base M.core.R) a b))`

Stage-style MV addition on the intensity carrier agrees with the core MV addition on Ω.

## Keywords
Algebraic geometry, Category theory, Computer science, FHE, Intuitionistic logic, Program verification, Proof assistants, Topos theory, Type theory, zkp

---
## Navigation (real dependency / similarity edges)
- ↖️ **NW**: [Bounds [dependency]](cell_R0_C10.md)
