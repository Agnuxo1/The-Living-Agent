# Cell [9,1] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.ZK.R1CSBool.head_satisfied_imp`
**Module**: `HeytingLean.Crypto.ZK.R1CSBool`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: head_satisfied_imp
**Signature**: `∀ (a : HeytingLean.Crypto.ZK.Var → Rat) {vx vy vmul vz : HeytingLean.Crypto.ZK.Var}, Eq (a vmul) (instHMul.hMul (a vx) (a vy)) → Eq (a vz) (instHAdd.hAdd (instHSub.hSub 1 (a vy)) (instHMul.hMul (a vy) (a vx))) → HeytingLean.Crypto.ZK.Constraint.satisfied a (HeytingLean.Crypto.ZK.R1CSBool.eqConstraint (HeytingLean.Crypto.ZK.R1CSBool.linhead_imp vz vx vy vmul) (HeytingLean.Crypto.ZK.LinComb.ofConst 0))`

No docstring available; inspect the Lean declaration directly.

## Keywords
algebra, boolean, head, imp, satisfied

---
## Navigation (real dependency / similarity edges)
- ⬆️ **N**: [Var [dependency]](cell_R0_C1.md)
- ↗️ **NE**: [satisfied [dependency]](cell_R2_C4.md)
