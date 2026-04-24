# Cell [8,3] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.ZK.R1CSBool.applyAnd_invariant`
**Module**: `HeytingLean.Crypto.ZK.R1CSBool`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: applyAnd_invariant
**Signature**: `∀ {builder : HeytingLean.Crypto.ZK.R1CSBool.Builder} {x y : Bool} {before : HeytingLean.Crypto.BoolLens.Stack} {vx vy : HeytingLean.Crypto.ZK.Var} {vars : List HeytingLean.Crypto.ZK.Var}, HeytingLean.Crypto.ZK.R1CSBool.Invariant builder (List.cons x (List.cons y before)) (List.cons vx (List.cons vy vars)) → HeytingLean.Crypto.ZK.R1CSBool.Invariant (HeytingLean.Crypto.ZK.R1CSBool.recordBoolean✝ ((builder.fresh (HeytingLean.Crypto.ZK.boolToRat (y.and x))).fst.addConstraint { A := HeytingLean.Crypto.ZK.LinComb.single vx 1, B := HeytingLean.Crypto.ZK.LinComb.single vy 1, C := HeytingLean.Crypto.ZK.LinComb.single (builder.fresh (HeytingLean.Crypto.ZK.boolToRat (y.and x))).snd 1 }) (builder.fresh (HeytingLean.Crypto.ZK.boolToRat (y.and x))).snd) (List.cons (y.and x) before) (List.cons (builder.fresh (HeytingLean.Crypto.ZK.boolToRat (y.and x))).snd vars)`

No docstring available; inspect the Lean declaration directly.

## Keywords
heytinglean.crypto.zk.r1csbool.applyand_invariant

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [Builder [dependency]](cell_R0_C4.md)
- ↖️ **NW**: [Var [dependency]](cell_R0_C1.md)
