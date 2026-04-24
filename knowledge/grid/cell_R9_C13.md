# Cell [9,13] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.ZK.Spec.Plonk.Rel_iff_renamed_sigma_of_gateBounds`
**Module**: `HeytingLean.Crypto.ZK.Spec.Plonk`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: Rel_iff_renamed_sigma_of_gateBounds
**Signature**: `∀ (sys : HeytingLean.Crypto.ZK.Plonk.System) (a : HeytingLean.Crypto.ZK.Var → Rat), HeytingLean.Crypto.ZK.System.satisfied a (HeytingLean.Crypto.ZK.Plonk.copyConstraintSystem sys.copyPermutation) → (∀ (g : HeytingLean.Crypto.ZK.Plonk.Gate), List.instMembership.mem sys.gates g → HeytingLean.Crypto.ZK.Plonk.gateBound g sys.copyPermutation.length) → Exists fun σ => Iff (HeytingLean.Crypto.ZK.Spec.Plonk.Rel sys a) (HeytingLean.Crypto.ZK.System.satisfied a (HeytingLean.Crypto.ZK.Rename.system σ sys.toR1CS))`

Under copy-satisfaction and suitable gate-bounds, the native relation coincides with the renamed R1CS semantics for some permutation `σ`.

## Keywords
and, copy-satisfaction, gate-bounds, heytinglean.crypto.zk.spec.plonk.rel_iff_renamed_sigma_of_gatebounds, native, suitable, the, under

---
## Navigation (real dependency / similarity edges)
- ⬆️ **N**: [System [dependency]](cell_R0_C13.md)
- ↗️ **NE**: [system [dependency]](cell_R3_C14.md)
- ↖️ **NW**: [Rel [dependency]](cell_R2_C10.md)
