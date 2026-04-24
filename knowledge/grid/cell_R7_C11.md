# Cell [7,11] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.ZK.Plonk.native_iff_renamed_sigma_of_gateBounds`
**Module**: `HeytingLean.Crypto.ZK.PlonkIR`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: native_iff_renamed_sigma_of_gateBounds
**Signature**: `∀ (sys : HeytingLean.Crypto.ZK.Plonk.System) (a : HeytingLean.Crypto.ZK.Var → Rat), HeytingLean.Crypto.ZK.System.satisfied a (HeytingLean.Crypto.ZK.Plonk.copyConstraintSystem sys.copyPermutation) → (∀ (g : HeytingLean.Crypto.ZK.Plonk.Gate), List.instMembership.mem sys.gates g → HeytingLean.Crypto.ZK.Plonk.gateBound g sys.copyPermutation.length) → Exists fun σ => Iff (HeytingLean.Crypto.ZK.Plonk.System.satisfiedNative a sys) (HeytingLean.Crypto.ZK.System.satisfied a (HeytingLean.Crypto.ZK.Rename.system σ sys.toR1CS))`

Convenience corollary: under gate-bounds we obtain the same σ-equivalence. In the current model the gate-bound hypothesis is recorded but not used.

## Keywords
convenience, corollary, gate-bounds, heytinglean.crypto.zk.plonk.native_iff_renamed_sigma_of_gatebounds, obtain, the, under, we

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [system [dependency]](cell_R3_C14.md)
- ↖️ **NW**: [copyConstraintSystem [dependency]](cell_R3_C5.md)
