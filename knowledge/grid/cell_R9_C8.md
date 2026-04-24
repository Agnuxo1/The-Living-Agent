# Cell [9,8] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.ZK.R1CSSoundness.compile_output_eval`
**Module**: `HeytingLean.Crypto.ZK.R1CSSoundness`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: compile_output_eval
**Signature**: `∀ {n : Nat} (φ : HeytingLean.Crypto.Form n) (ρ : HeytingLean.Crypto.BoolLens.Env n), Eq (HeytingLean.Crypto.ZK.boolToRat (HeytingLean.Crypto.BoolLens.eval φ ρ)) ((HeytingLean.Crypto.ZK.R1CSBool.compile φ ρ).assignment (HeytingLean.Crypto.ZK.R1CSBool.compile φ ρ).output)`

The compiled output variable encodes the boolean evaluation as a rational.

## Keywords
boolean, compiled, encodes, heytinglean.crypto.zk.r1cssoundness.compile_output_eval, output, the, variable

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [Env [dependency]](cell_R0_C9.md)
- ↖️ **NW**: [compile [dependency]](cell_R3_C4.md)
