# Cell [14,1] — KNOWLEDGE
**FQN**: `HeytingLean.Visual.Graph.Diagram.comp.elim`
**Module**: `HeytingLean.Visual.GraphDiagram`
**Kind**: `def`
**Centrality**: 0.000023
**Dependency Depth**: 3

## Topic
**Declaration**: elim
**Signature**: `{α : Type u} → [inst : HeytingLean.LoF.PrimaryAlgebra α] → {M : HeytingLean.Bridges.Graph.Model α} → {motive : (a a_1 : M.Carrier) → HeytingLean.Visual.Graph.Diagram M a a_1 → Sort u_1} → {a a_1 : M.Carrier} → (t : HeytingLean.Visual.Graph.Diagram M a a_1) → Eq t.ctorIdx 2 → ({x y z : M.Carrier} → (a : HeytingLean.Visual.Graph.Diagram M x y) → (a_2 : HeytingLean.Visual.Graph.Diagram M y z) → motive x z (a.comp a_2)) → motive a a_1 t`

No docstring available; inspect the Lean declaration directly.

## Keywords
heytinglean.visual.graph.diagram.comp.elim

---
## Navigation (real dependency / similarity edges)
- ⬆️ **N**: [Diagram [dependency]](cell_R5_C1.md)
- ↗️ **NE**: [Model [dependency]](cell_R1_C10.md)
- ↖️ **NW**: [PrimaryAlgebra [dependency]](cell_R0_C0.md)
