# Cell [2,4] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.ZK.Constraint.satisfied`
**Module**: `HeytingLean.Crypto.ZK.R1CS`
**Kind**: `def`
**Centrality**: 0.000107
**Dependency Depth**: 1

## Topic
**Declaration**: satisfied
**Signature**: `def Constraint.satisfied (assign : Var -> Q) (c : Constraint) : Prop := c.A.eval assign * c.B.eval assign = c.C.eval assign`

Satisfaction of a constraint by an assignment.

## Keywords
assignment, satisfied, valid, witness

---
## Navigation (real dependency / similarity edges)
- ↖️ **NW**: [Constraint [dependency]](cell_R0_C3.md)
- ↘️ **SE**: [satisfied_ext [dependency]](cell_R7_C6.md)
- ↙️ **SW**: [head_satisfied_imp [dependency]](cell_R9_C1.md)
