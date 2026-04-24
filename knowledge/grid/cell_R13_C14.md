# Cell [13,14] — KNOWLEDGE
**FQN**: `HeytingLean.Tests.tensor_shadow_mv_add`
**Module**: `HeytingLean.Tests.Compliance`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 3

## Topic
**Declaration**: tensor_shadow_mv_add
**Signature**: `∀ {α : Type u} [inst : HeytingLean.LoF.PrimaryAlgebra α] (R : HeytingLean.LoF.Reentry α) (n : Nat) (a b : R.Omega), Eq ((HeytingLean.Contracts.Examples.tensor α R n).logicalShadow ((HeytingLean.Contracts.Examples.tensor α R n).stageMvAdd ((HeytingLean.Contracts.Examples.tensor α R n).contract.encode a) ((HeytingLean.Contracts.Examples.tensor α R n).contract.encode b))) (Nucleus.instFunLike.coe R.nucleus (HeytingLean.Logic.Stage.DialParam.mvAdd (HeytingLean.Logic.Modal.DialParam.base R) a b).val)`

States tensor shadow mv add. Use when reasoning about nucleus property or rewriting goals that match this pattern.

## Keywords
add., heytinglean.tests.tensor_shadow_mv_add, mv, shadow, states, tensor, use, when

---
## Navigation (real dependency / similarity edges)
- ↖️ **NW**: [tensor [dependency]](cell_R5_C6.md)
