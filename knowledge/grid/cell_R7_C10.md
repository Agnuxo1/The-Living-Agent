# Cell [7,10] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.ZK.Plonk.native_iff_renamed_sigma_of_bounds`
**Module**: `HeytingLean.Crypto.ZK.PlonkIR`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: native_iff_renamed_sigma_of_bounds
**Signature**: `∀ (sys : HeytingLean.Crypto.ZK.Plonk.System) (a : HeytingLean.Crypto.ZK.Var → Rat), HeytingLean.Crypto.ZK.System.satisfied a (HeytingLean.Crypto.ZK.Plonk.copyConstraintSystem sys.copyPermutation) → (∀ (v : HeytingLean.Crypto.ZK.Var), Finset.instMembership.mem sys.toR1CS.support v → instLTNat.lt v sys.copyPermutation.length) → Exists fun σ => Iff (HeytingLean.Crypto.ZK.Plonk.System.satisfiedNative a sys) (HeytingLean.Crypto.ZK.System.satisfied a (HeytingLean.Crypto.ZK.Rename.system σ sys.toR1CS))`

Combine copy-satisfaction and a bound on support to obtain a σ‑renamed view. At this abstraction level we simply choose `σ := id`. Using `satisfiedNative_iff_r1cs_of_copySatisfied` and the renaming lemma specialised to `σ = id`, we obtain the desired equivalence. The `hBound` hypothesis is recorded for future refinements but not used in the proof.

## Keywords
a, and, bound, combine, copy-satisfaction, heytinglean.crypto.zk.plonk.native_iff_renamed_sigma_of_bounds, on, support

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [system [dependency]](cell_R3_C14.md)
- ↖️ **NW**: [satisfiedNative [dependency]](cell_R3_C9.md)
