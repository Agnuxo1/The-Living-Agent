# Cell [9,2] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.ZK.R1CSBool.head_satisfied_or`
**Module**: `HeytingLean.Crypto.ZK.R1CSBool`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: head_satisfied_or
**Signature**: `∀ (a : HeytingLean.Crypto.ZK.Var → Rat) {vx vy vmul vz : HeytingLean.Crypto.ZK.Var}, Eq (a vmul) (instHMul.hMul (a vx) (a vy)) → Eq (a vz) (instHSub.hSub (instHAdd.hAdd (a vx) (a vy)) (instHMul.hMul (a vx) (a vy))) → HeytingLean.Crypto.ZK.Constraint.satisfied a (HeytingLean.Crypto.ZK.R1CSBool.eqConstraint (HeytingLean.Crypto.ZK.R1CSBool.linhead_or vz vx vy vmul) (HeytingLean.Crypto.ZK.LinComb.ofConst 0))`

No docstring available; inspect the Lean declaration directly.

## Keywords
algebra, boolean, expression, function, logic, operation, polynomial, ring, value, variable

---
## Navigation (real dependency / similarity edges)
- ⬆️ **N**: [linhead_or [dependency]](cell_R3_C2.md)
- ↗️ **NE**: [eqConstraint [dependency]](cell_R3_C8.md)
- ↖️ **NW**: [Var [dependency]](cell_R0_C1.md)
