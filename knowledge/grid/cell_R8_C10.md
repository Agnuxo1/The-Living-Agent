# Cell [8,10] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.ZK.R1CSBool.compileSteps_strong`
**Module**: `HeytingLean.Crypto.ZK.R1CSBool`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: compileSteps_strong
**Signature**: `∀ {n : Nat} (ρ : HeytingLean.Crypto.BoolLens.Env n) {prog : HeytingLean.Crypto.Program n} {stack : HeytingLean.Crypto.BoolLens.Stack} {stackVars : List HeytingLean.Crypto.ZK.Var} {builder : HeytingLean.Crypto.ZK.R1CSBool.Builder}, HeytingLean.Crypto.ZK.R1CSBool.StrongInvariant builder stack stackVars → HeytingLean.Crypto.ZK.R1CSBool.StrongInvariant (HeytingLean.Crypto.ZK.R1CSBool.compileSteps✝ ρ prog (HeytingLean.Crypto.BoolLens.traceFrom ρ prog stack) stackVars builder).fst (HeytingLean.Crypto.BoolLens.exec ρ prog stack) (HeytingLean.Crypto.ZK.R1CSBool.compileSteps✝¹ ρ prog (HeytingLean.Crypto.BoolLens.traceFrom ρ prog stack) stackVars builder).snd`

No docstring available; inspect the Lean declaration directly.

## Keywords
heytinglean.crypto.zk.r1csbool.compilesteps_strong

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [exec [dependency]](cell_R2_C12.md)
- ↖️ **NW**: [Var [dependency]](cell_R0_C1.md)
