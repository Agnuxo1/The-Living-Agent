# Cell [14,15] — KNOWLEDGE
**FQN**: `HeytingLean.Contracts.stageOccam_encode`
**Module**: `HeytingLean.Contracts.RoundTrip`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 4

## Topic
**Declaration**: stageOccam_encode
**Signature**: `∀ {α : Type u} [inst : HeytingLean.LoF.PrimaryAlgebra α] (R : HeytingLean.LoF.Reentry α) {β : Type v} (C : HeytingLean.Contracts.RoundTrip R β) (a : R.Omega), Eq (HeytingLean.Contracts.stageOccam R C (C.encode a)) (C.encode (HeytingLean.LoF.Reentry.Omega.mk R (HeytingLean.Epistemic.occam R a.val) ⋯))`

No docstring available; inspect the Lean declaration directly.

## Keywords
heytinglean.contracts.stageoccam_encode

---
## Navigation (real dependency / similarity edges)
- ↖️ **NW**: [occam [dependency]](cell_R5_C13.md)
