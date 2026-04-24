# Cell [7,13] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.ZK.Plonk.satisfiedNative_iff_r1cs_of_pairs`
**Module**: `HeytingLean.Crypto.ZK.PlonkIR`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: satisfiedNative_iff_r1cs_of_pairs
**Signature**: `∀ (sys : HeytingLean.Crypto.ZK.Plonk.System) (a : HeytingLean.Crypto.ZK.Var → Rat), (∀ (ij : Prod Nat Nat), List.instMembership.mem (HeytingLean.Crypto.ZK.Plonk.copyPairs sys.copyPermutation) ij → Eq (a ij.fst) (a ij.snd)) → Iff (HeytingLean.Crypto.ZK.Plonk.System.satisfiedNative a sys) (HeytingLean.Crypto.ZK.System.satisfied a sys.toR1CS)`

Under an explicit pair-respect hypothesis, native satisfaction reduces to converted R1CS satisfaction.

## Keywords
copyPairs

---
## Navigation (real dependency / similarity edges)
- ⬆️ **N**: [System [dependency]](cell_R0_C13.md)
- ↖️ **NW**: [copyPairs [dependency]](cell_R1_C7.md)
