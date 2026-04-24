# Cell [4,14] — KNOWLEDGE
**FQN**: `HeytingLean.Visual.Region.Expr`
**Module**: `HeytingLean.Visual.RegionDiagram`
**Kind**: `inductive`
**Centrality**: 0.000260
**Dependency Depth**: 2

## Topic
**Declaration**: Expr
**Signature**: `{α : Type u} → [inst : HeytingLean.LoF.PrimaryAlgebra α] → HeytingLean.LoF.Reentry α → Type u`

Syntax of region diagrams over the Heyting core `Ω_R`. The constructors mirror the basic Heyting operations on `R.Omega`: * `atom a` is a primitive region corresponding to `a : Ω_R`; * `inf x y` represents intersection; * `sup x y` represents union; * `himp x y` represents implication; * `neg x` is the negation of a region, defined semantically as implication to bottom in `Ω_R`.

## Keywords
diagrams, heyting, heytinglean.visual.region.expr, of, over, region, syntax, the

---
## Navigation (real dependency / similarity edges)
- ↖️ **NW**: [Reentry [dependency]](cell_R1_C8.md)
- ↙️ **SW**: [eval [dependency]](cell_R14_C4.md)
