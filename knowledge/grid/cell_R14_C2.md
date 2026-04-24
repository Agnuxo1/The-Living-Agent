# Cell [14,2] — KNOWLEDGE
**FQN**: `HeytingLean.Visual.Graph.Diagram.comp.inj`
**Module**: `HeytingLean.Visual.GraphDiagram`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 3

## Topic
**Declaration**: inj
**Signature**: `∀ {α : Type u} {inst : HeytingLean.LoF.PrimaryAlgebra α} {M : HeytingLean.Bridges.Graph.Model α} {x y z : M.Carrier} {a : HeytingLean.Visual.Graph.Diagram M x y} {a_1 : HeytingLean.Visual.Graph.Diagram M y z} {y_1 : M.Carrier} {a_2 : HeytingLean.Visual.Graph.Diagram M x y_1} {a_3 : HeytingLean.Visual.Graph.Diagram M y_1 z}, Eq (a.comp a_1) (a_2.comp a_3) → And (Eq y y_1) (And (HEq a a_2) (HEq a_1 a_3))`

No docstring available; inspect the Lean declaration directly.

## Keywords
heytinglean.visual.graph.diagram.comp.inj

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [Model [dependency]](cell_R1_C10.md)
- ↖️ **NW**: [Diagram [dependency]](cell_R5_C1.md)
