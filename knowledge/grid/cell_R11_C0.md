# Cell [11,0] — KNOWLEDGE
**FQN**: `HeytingLean.Bridges.Clifford.Model.logicalShadow_stageMvAdd_encode`
**Module**: `HeytingLean.Bridges.Clifford`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 3

## Topic
**Declaration**: logicalShadow_stageMvAdd_encode
**Signature**: `∀ {α : Type u} [inst : HeytingLean.LoF.PrimaryAlgebra α] (M : HeytingLean.Bridges.Clifford.Model α) (a b : M.R.Omega), Eq (M.logicalShadow (M.stageMvAdd (M.contract.encode a) (M.contract.encode b))) (Nucleus.instFunLike.coe M.R.nucleus (HeytingLean.Logic.Stage.DialParam.mvAdd (HeytingLean.Logic.Modal.DialParam.base M.R) a b).val)`

States logical Shadow stage Mv Add encode. Use when reasoning about nucleus property or rewriting goals that match this pattern.

## Keywords
add, encode., heytinglean.bridges.clifford.model.logicalshadow_stagemvadd_encode, logical, mv, shadow, stage, states

---
## Navigation (real dependency / similarity edges)
- ⬆️ **N**: [PrimaryAlgebra [dependency]](cell_R0_C0.md)
- ↗️ **NE**: [Model [dependency]](cell_R1_C9.md)
