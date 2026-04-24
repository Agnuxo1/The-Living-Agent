# Cell [12,1] — KNOWLEDGE
**FQN**: `HeytingLean.Bridges.Tensor.Model.logicalShadow_stageOrthocomplement_encode`
**Module**: `HeytingLean.Bridges.Tensor`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 3

## Topic
**Declaration**: logicalShadow_stageOrthocomplement_encode
**Signature**: `∀ {α : Type u} [inst : HeytingLean.LoF.PrimaryAlgebra α] (M : HeytingLean.Bridges.Tensor.Model α) (a : M.R.Omega), Eq (M.logicalShadow (M.stageOrthocomplement (M.contract.encode a))) (Nucleus.instFunLike.coe M.R.nucleus (HeytingLean.Logic.Stage.DialParam.orthocomplement (HeytingLean.Logic.Modal.DialParam.base M.R) a).val)`

No docstring available; inspect the Lean declaration directly.

## Keywords
heytinglean.bridges.tensor.model.logicalshadow_stageorthocomplement_encode

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [Model [dependency]](cell_R1_C12.md)
- ↖️ **NW**: [PrimaryAlgebra [dependency]](cell_R0_C0.md)
