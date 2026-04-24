# Cell [13,6] — KNOWLEDGE
**FQN**: `HeytingLean.Logic.Stage.DialParam.expandAtOmega_coe`
**Module**: `HeytingLean.Logic.StageSemantics`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 3

## Topic
**Declaration**: expandAtOmega_coe
**Signature**: `∀ {α : Type u} [inst : HeytingLean.LoF.PrimaryAlgebra α] (R : HeytingLean.LoF.Reentry α) (n : Nat) (a : R.Omega), Eq (HeytingLean.Logic.Stage.DialParam.expandAtOmega R n a).val (Nucleus.instFunLike.coe R.nucleus (HeytingLean.Logic.Modal.DialParam.expandAt R n a.val))`

States expand At Omega coe. Use when reasoning about nucleus property or rewriting goals that match this pattern.

## Keywords
at, coe., expand, heytinglean.logic.stage.dialparam.expandatomega_coe, omega, states, use, when

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [expandAtOmega [dependency]](cell_R5_C10.md)
- ↖️ **NW**: [PrimaryAlgebra [dependency]](cell_R0_C0.md)
