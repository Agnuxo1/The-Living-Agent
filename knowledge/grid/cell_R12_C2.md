# Cell [12,2] — KNOWLEDGE
**FQN**: `HeytingLean.Contracts.Examples.clifford_encode_synthOmega_fst`
**Module**: `HeytingLean.Contracts.Examples`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 3

## Topic
**Declaration**: clifford_encode_synthOmega_fst
**Signature**: `∀ (α : Type u) [inst : HeytingLean.LoF.PrimaryAlgebra α] (R : HeytingLean.LoF.Reentry α) (T A : R.Omega), Eq ((HeytingLean.Contracts.Examples.clifford α R).encode (HeytingLean.Logic.Dialectic.synthOmega R T A)).fst (Nucleus.instFunLike.coe R.nucleus (SemilatticeSup.toMax.max T.val A.val))`

Clifford: each coordinate of the encoded `synthOmega` reduces to the nucleus of the join.

## Keywords
clifford, coordinate, each, encoded, heytinglean.contracts.examples.clifford_encode_synthomega_fst, of, synthomega, the

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [Reentry [dependency]](cell_R1_C8.md)
- ↖️ **NW**: [PrimaryAlgebra [dependency]](cell_R0_C0.md)
