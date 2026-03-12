# Cell [14,11] — KNOWLEDGE
**FQN**: `HeytingLean.Topos.LocalOperator`
**Module**: `HeytingLean.Topos.LocalOperator`
**Kind**: `inductive`
**Centrality**: 0.000423

## Topic
**Declaration**: LocalOperator
**Signature**: `(C : Type u) → [inst : CategoryTheory.Category C] → [CategoryTheory.Limits.HasPullbacks C] → Type (max u v)`

`LocalOperator C` is a **universal closure operator** on subobjects: it consists of a closure operator on each `Subobject X`, stable under pullback. This is the “subobject-lattice” presentation of a Lawvere–Tierney modality. A full classifier-based presentation (endomorphism `j : Ω ⟶ Ω` plus axioms) lives separately in `HeytingLean.Topos.LTfromNucleus`.

## Keywords
closure, pullback_stable

---
## Navigation (real dependency / similarity edges)
- ➡️ **E**: [ClosedSieve [similarity]](cell_R14_C12.md)
- ⬅️ **W**: [E91Substrate [similarity]](cell_R14_C10.md)
