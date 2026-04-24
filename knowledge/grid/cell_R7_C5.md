# Cell [7,5] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.BoolLens.traceFrom_cons`
**Module**: `HeytingLean.Crypto.BoolLens`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: traceFrom_cons
**Signature**: `∀ {n : Nat} (ρ : HeytingLean.Crypto.BoolLens.Env n) (instr : HeytingLean.Crypto.Instr n) (prog : HeytingLean.Crypto.Program n) (stk : HeytingLean.Crypto.BoolLens.Stack), Eq (HeytingLean.Crypto.BoolLens.traceFrom ρ (List.cons instr prog) stk) (List.cons stk (HeytingLean.Crypto.BoolLens.traceFrom ρ prog (HeytingLean.Crypto.BoolLens.step ρ instr stk)))`

No docstring available; inspect the Lean declaration directly.

## Keywords
heytinglean.crypto.boollens.tracefrom_cons

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [Instr [dependency]](cell_R0_C7.md)
- ↖️ **NW**: [Program [dependency]](cell_R1_C1.md)
