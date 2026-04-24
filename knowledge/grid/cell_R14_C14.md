# Cell [14,14] — KNOWLEDGE
**FQN**: `HeytingLean.Contracts.stageOccam.eq_1`
**Module**: `HeytingLean.Tests.Compliance`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 4

## Topic
**Declaration**: eq_1
**Signature**: `∀ {α : Type u} [inst : HeytingLean.LoF.PrimaryAlgebra α] (R : HeytingLean.LoF.Reentry α) {β : Type v} (C : HeytingLean.Contracts.RoundTrip R β) (b : β), Eq (HeytingLean.Contracts.stageOccam R C b) (C.encode (HeytingLean.LoF.Reentry.Omega.mk R (HeytingLean.Epistemic.occam R (C.decode b).val) ⋯))`

States eq 1. Use when your goal matches this shape or to rewrite subterms using this result.

## Keywords
1., eq, goal, heytinglean.contracts.stageoccam.eq_1, states, use, when, your

---
## Navigation (real dependency / similarity edges)
- ↖️ **NW**: [RoundTrip [dependency]](cell_R4_C12.md)
