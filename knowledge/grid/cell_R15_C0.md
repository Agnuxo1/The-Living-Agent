# Cell [15,0] — SYNTHESIS
**FQN**: `HeytingLean.Contracts.stageOccam_spec`
**Module**: `HeytingLean.Contracts.RoundTrip`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 4

## Topic
**Declaration**: stageOccam_spec
**Signature**: `∀ {α : Type u} [inst : HeytingLean.LoF.PrimaryAlgebra α] (R : HeytingLean.LoF.Reentry α) {β : Type v} (C : HeytingLean.Contracts.RoundTrip R β) (b : β), Eq (HeytingLean.Contracts.interiorized R C (HeytingLean.Contracts.stageOccam R C b)) (HeytingLean.Epistemic.occam R (C.decode b).val)`

No docstring available; inspect the Lean declaration directly.

## Keywords
heytinglean.contracts.stageoccam_spec

---
## Navigation (real dependency / similarity edges)
- ⬆️ **N**: [PrimaryAlgebra [dependency]](cell_R0_C0.md)
- ↗️ **NE**: [interiorized [dependency]](cell_R10_C6.md)
