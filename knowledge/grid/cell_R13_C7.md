# Cell [13,7] — KNOWLEDGE
**FQN**: `HeytingLean.Tests.clifford_shadow_mv_add`
**Module**: `HeytingLean.Tests.Compliance`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 3

## Topic
**Declaration**: clifford_shadow_mv_add
**Signature**: `∀ {α : Type u} [inst : HeytingLean.LoF.PrimaryAlgebra α] (R : HeytingLean.LoF.Reentry α) (a b : R.Omega), Eq ((HeytingLean.Contracts.Examples.clifford α R).logicalShadow ((HeytingLean.Contracts.Examples.clifford α R).stageMvAdd ((HeytingLean.Contracts.Examples.clifford α R).contract.encode a) ((HeytingLean.Contracts.Examples.clifford α R).contract.encode b))) (Nucleus.instFunLike.coe R.nucleus (HeytingLean.Logic.Stage.DialParam.mvAdd (HeytingLean.Logic.Modal.DialParam.base R) a b).val)`

States clifford shadow mv add. Use when reasoning about nucleus property or rewriting goals that match this pattern.

## Keywords
add., clifford, heytinglean.tests.clifford_shadow_mv_add, mv, shadow, states, use, when

---
## Navigation (real dependency / similarity edges)
- ⬆️ **N**: [clifford [dependency]](cell_R5_C7.md)
- ↗️ **NE**: [Reentry [dependency]](cell_R1_C8.md)
- ↖️ **NW**: [PrimaryAlgebra [dependency]](cell_R0_C0.md)
