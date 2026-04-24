# Cell [8,6] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.ZK.R1CSBool.applyOr_strong`
**Module**: `HeytingLean.Crypto.ZK.R1CSBool`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: applyOr_strong
**Signature**: `∀ {builder : HeytingLean.Crypto.ZK.R1CSBool.Builder} {x y : Bool} {before : HeytingLean.Crypto.BoolLens.Stack} {vx vy : HeytingLean.Crypto.ZK.Var} {vars : List HeytingLean.Crypto.ZK.Var}, HeytingLean.Crypto.ZK.R1CSBool.StrongInvariant builder (List.cons x (List.cons y before)) (List.cons vx (List.cons vy vars)) → Or (Eq (builder.assign vx) 0) (Eq (builder.assign vx) 1) → Or (Eq (builder.assign vy) 0) (Eq (builder.assign vy) 1) → have z := y.or x; have mulVal := HeytingLean.Crypto.ZK.boolToRat (y.and x); have fresMul := builder.fresh mulVal; have builder1 := fresMul.fst; have vmul := fresMul.snd; have builder2 := builder1.addConstraint { A := HeytingLean.Crypto.ZK.LinComb.single vy 1, B := HeytingLean.Crypto.ZK.LinComb.single vx 1, C := HeytingLean.Crypto.ZK.LinComb.single vmul 1 }; have builder3 := HeytingLean.Crypto.ZK.R1CSBool.recordBoolean✝ builder2 vmul; have fresZ := builder3.fresh (HeytingLean.Crypto.ZK.boolToRat z); have builder4 := fresZ.fst; have vz := fresZ.snd; have eqOr := HeytingLean.Crypto.ZK.R1CSBool.eqConstraint (HeytingLean.Crypto.ZK.R1CSBool.linhead_or vz vx vy vmul) (HeytingLean.Crypto.ZK.LinComb.ofConst 0); have builder5 := builder4.addConstraint eqOr; have builder6 := HeytingLean.Crypto.ZK.R1CSBool.recordBoolean✝¹ builder5 vz; HeytingLean.Crypto.ZK.R1CSBool.StrongInvariant builder6 (List.cons z before) (List.cons vz vars)`

No docstring available; inspect the Lean declaration directly.

## Keywords
heytinglean.crypto.zk.r1csbool.applyor_strong

---
## Navigation (real dependency / similarity edges)
- ⬆️ **N**: [single [dependency]](cell_R2_C6.md)
- ↗️ **NE**: [Stack [dependency]](cell_R0_C12.md)
- ↖️ **NW**: [linhead_or [dependency]](cell_R3_C2.md)
