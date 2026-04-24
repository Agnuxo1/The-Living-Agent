# Cell [15,5] — SYNTHESIS
**FQN**: `HeytingLean.Tests.identity_round_verified`
**Module**: `HeytingLean.Tests.Compliance`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 4

## Topic
**Declaration**: identity_round_verified
**Signature**: `∀ {α : Type u} [inst : HeytingLean.LoF.PrimaryAlgebra α] (R : HeytingLean.LoF.Reentry α) (a : R.Omega), Eq ((HeytingLean.Contracts.Examples.identity α R).decode ((HeytingLean.Contracts.Examples.identity α R).encode a)) a`

Encoding and decoding through the identity contract returns every state unchanged.

## Keywords
and, contract, decoding, encoding, heytinglean.tests.identity_round_verified, identity, the, through

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [identity [dependency]](cell_R10_C8.md)
- ↖️ **NW**: [PrimaryAlgebra [dependency]](cell_R0_C0.md)
