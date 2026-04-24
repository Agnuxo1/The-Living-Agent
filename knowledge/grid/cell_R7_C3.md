# Cell [7,3] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.BoolLens.exec_compile_aux`
**Module**: `HeytingLean.Crypto.BoolLens`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: exec_compile_aux
**Signature**: `∀ {n : Nat} (ρ : HeytingLean.Crypto.BoolLens.Env n) (φ : HeytingLean.Crypto.Form n) (stk : HeytingLean.Crypto.BoolLens.Stack), Eq (HeytingLean.Crypto.BoolLens.exec ρ φ.compile stk) (List.cons (HeytingLean.Crypto.BoolLens.eval φ ρ) stk)`

Executing the compiled form pushes its boolean evaluation on the stack.

## Keywords
boolean, compiled, executing, form, heytinglean.crypto.boollens.exec_compile_aux, its, pushes, the

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [eval [dependency]](cell_R2_C9.md)
- ↖️ **NW**: [Form [dependency]](cell_R0_C2.md)
