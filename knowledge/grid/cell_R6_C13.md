# Cell [6,13] — KNOWLEDGE
**FQN**: `HeytingLean.Bridges.Tensor.Intensity.Model.Carrier.mk.inj`
**Module**: `HeytingLean.Bridges.Tensor.Intensity`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: inj
**Signature**: `∀ {α : Type u} {inst : HeytingLean.LoF.PrimaryAlgebra α} {M : HeytingLean.Bridges.Tensor.Intensity.Model} {profile : HeytingLean.Bridges.Tensor.Intensity.Profile α} {dim_ok : Eq profile.dim M.core.dim} {coords_fixed : ∀ (i : Fin profile.dim.succ), Eq (Nucleus.instFunLike.coe M.core.R.nucleus (profile.coords i)) (profile.coords i)} {profile_1 : HeytingLean.Bridges.Tensor.Intensity.Profile α} {dim_ok_1 : Eq profile_1.dim M.core.dim} {coords_fixed_1 : ∀ (i : Fin profile_1.dim.succ), Eq (Nucleus.instFunLike.coe M.core.R.nucleus (profile_1.coords i)) (profile_1.coords i)}, Eq { profile := profile, dim_ok := dim_ok, coords_fixed := coords_fixed } { profile := profile_1, dim_ok := dim_ok_1, coords_fixed := coords_fixed_1 } → Eq profile profile_1`

No docstring available; inspect the Lean declaration directly.

## Keywords
heytinglean.bridges.tensor.intensity.model.carrier.mk.inj

---
## Navigation (real dependency / similarity edges)
- ↖️ **NW**: [PrimaryAlgebra [dependency]](cell_R0_C0.md)
