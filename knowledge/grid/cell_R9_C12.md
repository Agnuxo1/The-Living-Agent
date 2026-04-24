# Cell [9,12] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.ZK.Spec.Plonk.Rel_iff_r1cs_of_pairs`
**Module**: `HeytingLean.Crypto.ZK.Spec.Plonk`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: Rel_iff_r1cs_of_pairs
**Signature**: `∀ (sys : HeytingLean.Crypto.ZK.Plonk.System) (a : HeytingLean.Crypto.ZK.Var → Rat), (∀ (ij : Prod Nat Nat), List.instMembership.mem (HeytingLean.Crypto.ZK.Plonk.copyPairs sys.copyPermutation) ij → Eq (a ij.fst) (a ij.snd)) → Iff (HeytingLean.Crypto.ZK.Spec.Plonk.Rel sys a) (HeytingLean.Crypto.ZK.System.satisfied a sys.toR1CS)`

Under an explicit pair-respect hypothesis, the native relation is equivalent to R1CS satisfaction of the converted system.

## Keywords
an, explicit, heytinglean.crypto.zk.spec.plonk.rel_iff_r1cs_of_pairs, hypothesis, native, pair-respect, the, under

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [System [dependency]](cell_R0_C13.md)
- ↖️ **NW**: [copyPairs [dependency]](cell_R1_C7.md)
