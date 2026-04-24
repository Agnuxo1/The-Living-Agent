# Cell [7,4] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.BoolLens.exec_cons`
**Module**: `HeytingLean.Crypto.BoolLens`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: exec_cons
**Signature**: `∀ {n : Nat} (ρ : HeytingLean.Crypto.BoolLens.Env n) (instr : HeytingLean.Crypto.Instr n) (prog : HeytingLean.Crypto.Program n) (stk : HeytingLean.Crypto.BoolLens.Stack), Eq (HeytingLean.Crypto.BoolLens.exec ρ (List.cons instr prog) stk) (HeytingLean.Crypto.BoolLens.exec ρ prog (HeytingLean.Crypto.BoolLens.step ρ instr stk))`

No docstring available; inspect the Lean declaration directly.

## Keywords
heytinglean.crypto.boollens.exec_cons

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [Instr [dependency]](cell_R0_C7.md)
- ↖️ **NW**: [Program [dependency]](cell_R1_C1.md)
