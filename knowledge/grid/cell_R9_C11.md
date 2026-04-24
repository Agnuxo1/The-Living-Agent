# Cell [9,11] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.ZK.Spec.Plonk.Rel_iff_r1cs_of_copySatisfied`
**Module**: `HeytingLean.Crypto.ZK.Spec.Plonk`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: Rel_iff_r1cs_of_copySatisfied
**Signature**: `∀ (sys : HeytingLean.Crypto.ZK.Plonk.System) (a : HeytingLean.Crypto.ZK.Var → Rat), HeytingLean.Crypto.ZK.System.satisfied a (HeytingLean.Crypto.ZK.Plonk.copyConstraintSystem sys.copyPermutation) → Iff (HeytingLean.Crypto.ZK.Spec.Plonk.Rel sys a) (HeytingLean.Crypto.ZK.System.satisfied a sys.toR1CS)`

If the copy-constraint system is satisfied, the native relation is equivalent to R1CS satisfaction of the converted system.

## Keywords
copy-constraint, heytinglean.crypto.zk.spec.plonk.rel_iff_r1cs_of_copysatisfied, if, is, satisfied, system, the

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [System [dependency]](cell_R0_C13.md)
- ↖️ **NW**: [copyConstraintSystem [dependency]](cell_R3_C5.md)
