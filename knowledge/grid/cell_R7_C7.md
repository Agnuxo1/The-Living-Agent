# Cell [7,7] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.ZK.Plonk.copySatisfied_of_pairs`
**Module**: `HeytingLean.Crypto.ZK.PlonkIR`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: copySatisfied_of_pairs
**Signature**: `∀ (a : HeytingLean.Crypto.ZK.Var → Rat) {perm : List Nat}, (∀ {i j : Nat}, List.instMembership.mem (HeytingLean.Crypto.ZK.Plonk.copyPairs perm) { fst := i, snd := j } → Eq (a i) (a j)) → HeytingLean.Crypto.ZK.System.satisfied a (HeytingLean.Crypto.ZK.Plonk.copyConstraintSystem perm)`

Alternative formulation of copy-satisfaction starting from a quantified equality hypothesis.

## Keywords
a, alternative, copy-satisfaction, formulation, from, heytinglean.crypto.zk.plonk.copysatisfied_of_pairs, of, starting

---
## Navigation (real dependency / similarity edges)
- ⬆️ **N**: [copyPairs [dependency]](cell_R1_C7.md)
- ↖️ **NW**: [Var [dependency]](cell_R0_C1.md)
