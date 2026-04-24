# Cell [15,9] — SYNTHESIS
**FQN**: `HeytingLean.Tests.TraceConcurrency.bridgeActWord.eq_2`
**Module**: `HeytingLean.Tests.Compliance`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 5

## Topic
**Declaration**: eq_2
**Signature**: `∀ {α : Type u} [inst : HeytingLean.LoF.PrimaryAlgebra α] (R : HeytingLean.LoF.Reentry α) (suite : HeytingLean.Contracts.Examples.BridgeSuite α R) (x : HeytingLean.Tests.TraceConcurrency.BridgeState R suite) (op : HeytingLean.Tests.TraceConcurrency.BridgeOp) (ops : List HeytingLean.Tests.TraceConcurrency.BridgeOp), Eq (HeytingLean.Tests.TraceConcurrency.bridgeActWord R suite (List.cons op ops) x) (HeytingLean.Tests.TraceConcurrency.bridgeActWord R suite ops (HeytingLean.Tests.TraceConcurrency.bridgeStep R suite op x))`

States eq 2. Use when your goal matches this shape or to rewrite subterms using this result.

## Keywords
2., eq, goal, heytinglean.tests.traceconcurrency.bridgeactword.eq_2, states, use, when, your

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [BridgeOp [dependency]](cell_R0_C14.md)
- ↖️ **NW**: [bridgeStep [dependency]](cell_R14_C6.md)
