# Cell [8,9] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.ZK.R1CSBool.compileStep_strong`
**Module**: `HeytingLean.Crypto.ZK.R1CSBool`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: compileStep_strong
**Signature**: `∀ {n : Nat} (ρ : HeytingLean.Crypto.BoolLens.Env n) {instr : HeytingLean.Crypto.Instr n} {before after : HeytingLean.Crypto.BoolLens.Stack} {stackVars : List HeytingLean.Crypto.ZK.Var} {builder : HeytingLean.Crypto.ZK.R1CSBool.Builder}, HeytingLean.Crypto.ZK.R1CSBool.StrongInvariant builder before stackVars → Eq after (HeytingLean.Crypto.BoolLens.step ρ instr before) → HeytingLean.Crypto.ZK.R1CSBool.StrongInvariant (HeytingLean.Crypto.ZK.R1CSBool.compileStep✝ ρ instr before after stackVars builder).fst after (HeytingLean.Crypto.ZK.R1CSBool.compileStep✝¹ ρ instr before after stackVars builder).snd`

No docstring available; inspect the Lean declaration directly.

## Keywords
heytinglean.crypto.zk.r1csbool.compilestep_strong

---
## Navigation (real dependency / similarity edges)
- ⬆️ **N**: [Env [dependency]](cell_R0_C9.md)
- ↗️ **NE**: [Stack [dependency]](cell_R0_C12.md)
- ↖️ **NW**: [Var [dependency]](cell_R0_C1.md)
