# Cell [9,9] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.ZK.Rename.satisfied_system`
**Module**: `HeytingLean.Crypto.ZK.Rename`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: satisfied_system
**Signature**: `∀ (σ : HeytingLean.Crypto.ZK.Var → HeytingLean.Crypto.ZK.Var) (a : HeytingLean.Crypto.ZK.Var → Rat) (sys : HeytingLean.Crypto.ZK.System), Iff (HeytingLean.Crypto.ZK.System.satisfied a (HeytingLean.Crypto.ZK.Rename.system σ sys)) (HeytingLean.Crypto.ZK.System.satisfied (fun v => a (σ v)) sys)`

Proves satisfaction is preserved under renaming: `system sigma sys` is satisfied by `a` iff `sys` is satisfied by `a circ sigma`.

## Keywords
sigma, system

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [system [dependency]](cell_R3_C14.md)
- ↖️ **NW**: [Var [dependency]](cell_R0_C1.md)
