# Cell [8,8] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.ZK.R1CSBool.compile.eq_1`
**Module**: `HeytingLean.Crypto.ZK.R1CSBool`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: eq_1
**Signature**: `∀ {n : Nat} (φ : HeytingLean.Crypto.Form n) (ρ : HeytingLean.Crypto.BoolLens.Env n), Eq (HeytingLean.Crypto.ZK.R1CSBool.compile φ ρ) (HeytingLean.Crypto.ZK.R1CSBool.compileSteps.match_1✝ (fun x => HeytingLean.Crypto.ZK.R1CSBool.Compiled) (HeytingLean.Crypto.ZK.R1CSBool.compileSteps✝ ρ φ.compile (HeytingLean.Crypto.BoolLens.traceFrom ρ φ.compile List.nil) List.nil { }) fun builder stackVars => have outputVar := stackVars.headD 0; { system := { constraints := builder.constraints.reverse }, assignment := builder.assign, output := outputVar })`

No docstring available; inspect the Lean declaration directly.

## Keywords
heytinglean.crypto.zk.r1csbool.compile.eq_1

---
## Navigation (real dependency / similarity edges)
- ⬆️ **N**: [traceFrom [dependency]](cell_R2_C8.md)
- ↗️ **NE**: [Env [dependency]](cell_R0_C9.md)
- ↖️ **NW**: [Compiled [dependency]](cell_R1_C6.md)
