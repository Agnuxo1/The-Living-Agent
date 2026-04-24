# Cell [9,6] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.ZK.R1CSBool.matches_cons_head`
**Module**: `HeytingLean.Crypto.ZK.R1CSBool`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: matches_cons_head
**Signature**: `∀ {builder : HeytingLean.Crypto.ZK.R1CSBool.Builder} {b : Bool} {stack : HeytingLean.Crypto.BoolLens.Stack} {v : HeytingLean.Crypto.ZK.Var} {vars : List HeytingLean.Crypto.ZK.Var}, HeytingLean.Crypto.ZK.R1CSBool.Matches builder (List.cons b stack) (List.cons v vars) → Eq (HeytingLean.Crypto.ZK.boolToRat b) (builder.assign v)`

No docstring available; inspect the Lean declaration directly.

## Keywords
heytinglean.crypto.zk.r1csbool.matches_cons_head

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [Stack [dependency]](cell_R0_C12.md)
- ↖️ **NW**: [boolToRat [dependency]](cell_R1_C2.md)
