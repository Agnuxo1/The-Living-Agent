# Cell [8,4] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.ZK.R1CSBool.applyAnd_strong`
**Module**: `HeytingLean.Crypto.ZK.R1CSBool`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: applyAnd_strong
**Signature**: `∀ {builder : HeytingLean.Crypto.ZK.R1CSBool.Builder} {x y : Bool} {before : HeytingLean.Crypto.BoolLens.Stack} {vx vy : HeytingLean.Crypto.ZK.Var} {vars : List HeytingLean.Crypto.ZK.Var}, HeytingLean.Crypto.ZK.R1CSBool.StrongInvariant builder (List.cons x (List.cons y before)) (List.cons vx (List.cons vy vars)) → Or (Eq (builder.assign vx) 0) (Eq (builder.assign vx) 1) → Or (Eq (builder.assign vy) 0) (Eq (builder.assign vy) 1) → have z := y.and x; have fres := builder.fresh (HeytingLean.Crypto.ZK.boolToRat z); have builder1 := fres.fst; have vz := fres.snd; have mulConstraint := { A := HeytingLean.Crypto.ZK.LinComb.single vx 1, B := HeytingLean.Crypto.ZK.LinComb.single vy 1, C := HeytingLean.Crypto.ZK.LinComb.single vz 1 }; have builder2 := builder1.addConstraint mulConstraint; have builder3 := HeytingLean.Crypto.ZK.R1CSBool.recordBoolean✝ builder2 vz; HeytingLean.Crypto.ZK.R1CSBool.StrongInvariant builder3 (List.cons z before) (List.cons vz vars)`

No docstring available; inspect the Lean declaration directly.

## Keywords
heytinglean.crypto.zk.r1csbool.applyand_strong

---
## Navigation (real dependency / similarity edges)
- ⬆️ **N**: [Builder [dependency]](cell_R0_C4.md)
- ↗️ **NE**: [single [dependency]](cell_R2_C6.md)
- ↖️ **NW**: [Var [dependency]](cell_R0_C1.md)
