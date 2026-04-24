# Cell [14,12] — KNOWLEDGE
**FQN**: `HeytingLean.Contracts.interiorized.eq_1`
**Module**: `HeytingLean.Bridges.Tensor`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 4

## Topic
**Declaration**: eq_1
**Signature**: `∀ {α : Type u} [inst : HeytingLean.LoF.PrimaryAlgebra α] (R : HeytingLean.LoF.Reentry α) {β : Type v} (C : HeytingLean.Contracts.RoundTrip R β) (b : β), Eq (HeytingLean.Contracts.interiorized R C b) (Nucleus.instFunLike.coe R.nucleus (C.decode b).val)`

No docstring available; inspect the Lean declaration directly.

## Keywords
heytinglean.contracts.interiorized.eq_1

---
## Navigation (real dependency / similarity edges)
- ⬆️ **N**: [RoundTrip [dependency]](cell_R4_C12.md)
- ↖️ **NW**: [interiorized [dependency]](cell_R10_C6.md)
