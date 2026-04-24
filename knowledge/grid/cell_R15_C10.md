# Cell [15,10] — SYNTHESIS
**FQN**: `HeytingLean.Tests.TraceConcurrency.bridgeStep.eq_1`
**Module**: `HeytingLean.Tests.Compliance`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 5

## Topic
**Declaration**: eq_1
**Signature**: `∀ {α : Type u} [inst : HeytingLean.LoF.PrimaryAlgebra α] (R : HeytingLean.LoF.Reentry α) (suite : HeytingLean.Contracts.Examples.BridgeSuite α R) (x : HeytingLean.Tests.TraceConcurrency.BridgeState R suite), Eq (HeytingLean.Tests.TraceConcurrency.bridgeStep R suite HeytingLean.Tests.TraceConcurrency.BridgeOp.tensor x) { tensor := HeytingLean.Contracts.stageOccam R suite.tensor.contract x.tensor, graph := x.graph, clifford := x.clifford }`

No docstring available; inspect the Lean declaration directly.

## Keywords
heytinglean.tests.traceconcurrency.bridgestep.eq_1

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [BridgeSuite [dependency]](cell_R4_C11.md)
- ↖️ **NW**: [stageOccam [dependency]](cell_R10_C5.md)
