# Cell [14,3] — KNOWLEDGE
**FQN**: `HeytingLean.Visual.Region.Expr.atom.elim`
**Module**: `HeytingLean.Visual.RegionDiagram`
**Kind**: `def`
**Centrality**: 0.000023
**Dependency Depth**: 3

## Topic
**Declaration**: elim
**Signature**: `{α : Type u} → [inst : HeytingLean.LoF.PrimaryAlgebra α] → {R : HeytingLean.LoF.Reentry α} → {motive : HeytingLean.Visual.Region.Expr R → Sort u_1} → (t : HeytingLean.Visual.Region.Expr R) → Eq t.ctorIdx 0 → ((a : R.Omega) → motive (HeytingLean.Visual.Region.Expr.atom a)) → motive t`

Defines/computes elim. Use to construct or compute the corresponding value in proofs or definitions.

## Keywords
computes, construct, defines, elim., heytinglean.visual.region.expr.atom.elim, or, to, use

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [Expr [dependency]](cell_R4_C14.md)
- ↖️ **NW**: [PrimaryAlgebra [dependency]](cell_R0_C0.md)
