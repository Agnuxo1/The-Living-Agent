# Cell [13,11] — KNOWLEDGE
**FQN**: `HeytingLean.Tests.graph_shadow_mv_add`
**Module**: `HeytingLean.Tests.Compliance`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 3

## Topic
**Declaration**: graph_shadow_mv_add
**Signature**: `∀ {α : Type u} [inst : HeytingLean.LoF.PrimaryAlgebra α] (R : HeytingLean.LoF.Reentry α) (a b : R.Omega), Eq ((HeytingLean.Contracts.Examples.graph α R).logicalShadow ((HeytingLean.Contracts.Examples.graph α R).stageMvAdd ((HeytingLean.Contracts.Examples.graph α R).contract.encode a) ((HeytingLean.Contracts.Examples.graph α R).contract.encode b))) (Nucleus.instFunLike.coe R.nucleus (HeytingLean.Logic.Stage.DialParam.mvAdd (HeytingLean.Logic.Modal.DialParam.base R) a b).val)`

States graph shadow mv add. Use when reasoning about nucleus property or rewriting goals that match this pattern.

## Keywords
add., graph, heytinglean.tests.graph_shadow_mv_add, mv, shadow, states, use, when

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [base [dependency]](cell_R4_C13.md)
- ↖️ **NW**: [graph [dependency]](cell_R5_C2.md)
