# Cell [2,1] — KNOWLEDGE
**FQN**: `HeytingLean.LoF.IntNucleus`
**Module**: `HeytingLean.LoF.IntReentry`
**Kind**: `inductive`
**Centrality**: 0.000216
**Dependency Depth**: 1

## Topic
**Declaration**: IntNucleus
**Signature**: `structure IntNucleus (α : Type u) [PrimaryAlgebra α] where act : α → α; monotone : Monotone act; idempotent : ∀ a, act (act a) = act a; apply_le : ∀ a, act a ≤ a; map_inf : ∀ a b, act (a ⊓ b) = act a ⊓ act b`

Interior-style nucleus on a primary algebra. R as logic-extraction (domain-specific interior): act plays the role of a stabilization operator that extracts the domain's self-consistent core.

## Keywords
deflationary, idempotent, interior, meet-preserving, nucleus, stabilization

---
## Navigation (real dependency / similarity edges)
- ↖️ **NW**: [PrimaryAlgebra [dependency]](cell_R0_C0.md)
- ⬇️ **S**: [nucleus [dependency]](cell_R10_C1.md)
- ↘️ **SE**: [intNucleus [dependency]](cell_R6_C10.md)
