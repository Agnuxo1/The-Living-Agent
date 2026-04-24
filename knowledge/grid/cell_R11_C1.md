# Cell [11,1] — KNOWLEDGE
**FQN**: `HeytingLean.Bridges.Clifford.Model.logicalShadow_stageOrthocomplement_encode`
**Module**: `HeytingLean.Bridges.Clifford`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 3

## Topic
**Declaration**: logicalShadow_stageOrthocomplement_encode
**Signature**: `∀ {α : Type u} [inst : HeytingLean.LoF.PrimaryAlgebra α] (M : HeytingLean.Bridges.Clifford.Model α) (a : M.R.Omega), Eq (M.logicalShadow (M.stageOrthocomplement (M.contract.encode a))) (Nucleus.instFunLike.coe M.R.nucleus (HeytingLean.Logic.Stage.DialParam.orthocomplement (HeytingLean.Logic.Modal.DialParam.base M.R) a).val)`

States logical Shadow stage Orthocomplement encode. Use when reasoning about nucleus property or rewriting goals that match this pattern.

## Keywords
encode., heytinglean.bridges.clifford.model.logicalshadow_stageorthocomplement_encode, logical, orthocomplement, shadow, stage, states, use

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [Model [dependency]](cell_R1_C9.md)
- ↖️ **NW**: [orthocomplement [dependency]](cell_R6_C0.md)
