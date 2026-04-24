# Cell [15,12] — SYNTHESIS
**FQN**: `HeytingLean.Tests.TraceConcurrency.bridge_tensor_clifford_commute`
**Module**: `HeytingLean.Tests.Compliance`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 5

## Topic
**Declaration**: bridge_tensor_clifford_commute
**Signature**: `∀ {α : Type u} [inst : HeytingLean.LoF.PrimaryAlgebra α] (R : HeytingLean.LoF.Reentry α) (flags : optParam HeytingLean.Contracts.Examples.BridgeFlags HeytingLean.Contracts.Examples.BridgeFlags.default) (suite : optParam (HeytingLean.Contracts.Examples.BridgeSuite α R) (HeytingLean.Contracts.Examples.selectSuite α R flags)) (st : HeytingLean.Tests.TraceConcurrency.BridgeState R suite), Eq (HeytingLean.Tests.TraceConcurrency.bridgeStep R suite HeytingLean.Tests.TraceConcurrency.BridgeOp.tensor (HeytingLean.Tests.TraceConcurrency.bridgeStep R suite HeytingLean.Tests.TraceConcurrency.BridgeOp.clifford st)) (HeytingLean.Tests.TraceConcurrency.bridgeStep R suite HeytingLean.Tests.TraceConcurrency.BridgeOp.clifford (HeytingLean.Tests.TraceConcurrency.bridgeStep R suite HeytingLean.Tests.TraceConcurrency.BridgeOp.tensor st))`

Tensor and Clifford bridge steps commute when acting on any state.

## Keywords
Clifford, Tensor, commute, state

---
## Navigation (real dependency / similarity edges)
- ↖️ **NW**: [selectSuite [dependency]](cell_R10_C9.md)
