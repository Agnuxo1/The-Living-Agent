# Cell [12,0] — KNOWLEDGE
**FQN**: `HeytingLean.Bridges.Tensor.Model.logicalShadow_stageMvAdd_encode`
**Module**: `HeytingLean.Bridges.Tensor`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 3

## Topic
**Declaration**: logicalShadow_stageMvAdd_encode
**Signature**: `∀ {α : Type u} [inst : HeytingLean.LoF.PrimaryAlgebra α] (M : HeytingLean.Bridges.Tensor.Model α) (a b : M.R.Omega), Eq (M.logicalShadow (M.stageMvAdd (M.contract.encode a) (M.contract.encode b))) (Nucleus.instFunLike.coe M.R.nucleus (HeytingLean.Logic.Stage.DialParam.mvAdd (HeytingLean.Logic.Modal.DialParam.base M.R) a b).val)`

No docstring available; inspect the Lean declaration directly.

## Keywords
heytinglean.bridges.tensor.model.logicalshadow_stagemvadd_encode

---
## Navigation (real dependency / similarity edges)
- ⬆️ **N**: [PrimaryAlgebra [dependency]](cell_R0_C0.md)
- ↗️ **NE**: [Model [dependency]](cell_R1_C12.md)
