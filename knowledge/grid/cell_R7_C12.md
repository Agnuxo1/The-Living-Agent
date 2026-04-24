# Cell [7,12] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.ZK.Plonk.satisfiedNative_iff_r1cs_of_copySatisfied`
**Module**: `HeytingLean.Crypto.ZK.PlonkIR`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: satisfiedNative_iff_r1cs_of_copySatisfied
**Signature**: `∀ (sys : HeytingLean.Crypto.ZK.Plonk.System) (a : HeytingLean.Crypto.ZK.Var → Rat), HeytingLean.Crypto.ZK.System.satisfied a (HeytingLean.Crypto.ZK.Plonk.copyConstraintSystem sys.copyPermutation) → Iff (HeytingLean.Crypto.ZK.Plonk.System.satisfiedNative a sys) (HeytingLean.Crypto.ZK.System.satisfied a sys.toR1CS)`

Under copy-satisfaction, native semantics reduces to the converted R1CS semantics.

## Keywords
Under copy-satisfaction, converted R1CS semantics, native semantics

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [System [dependency]](cell_R0_C13.md)
- ↖️ **NW**: [satisfiedNative [dependency]](cell_R3_C9.md)
