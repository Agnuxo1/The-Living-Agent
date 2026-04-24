# Cell [7,2] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.BoolLens.exec.eq_2`
**Module**: `HeytingLean.Crypto.ZK.R1CSBool`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: eq_2
**Signature**: `∀ {n : Nat} (ρ : HeytingLean.Crypto.BoolLens.Env n) (x : HeytingLean.Crypto.BoolLens.Stack) (instr : HeytingLean.Crypto.Instr n) (prog : List (HeytingLean.Crypto.Instr n)), Eq (HeytingLean.Crypto.BoolLens.exec ρ (List.cons instr prog) x) (HeytingLean.Crypto.BoolLens.exec ρ prog (HeytingLean.Crypto.BoolLens.step ρ instr x))`

No docstring available; inspect the Lean declaration directly.

## Keywords
heytinglean.crypto.boollens.exec.eq_2

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [Instr [dependency]](cell_R0_C7.md)
