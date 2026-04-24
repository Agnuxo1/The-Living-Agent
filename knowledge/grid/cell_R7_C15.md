# Cell [7,15] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.ZK.R1CSBool.Matches.eq_1`
**Module**: `HeytingLean.Crypto.ZK.R1CSBool`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: eq_1
**Signature**: `∀ (builder : HeytingLean.Crypto.ZK.R1CSBool.Builder) (stack : HeytingLean.Crypto.BoolLens.Stack) (vars : List HeytingLean.Crypto.ZK.Var), Eq (HeytingLean.Crypto.ZK.R1CSBool.Matches builder stack vars) (List.Forall₂ (fun b v => Eq (HeytingLean.Crypto.ZK.boolToRat b) (builder.assign v)) stack vars)`

No docstring available; inspect the Lean declaration directly.

## Keywords
heytinglean.crypto.zk.r1csbool.matches.eq_1

---
## Navigation (real dependency / similarity edges)
- ↖️ **NW**: [Matches [dependency]](cell_R2_C11.md)
