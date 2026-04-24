# Cell [9,14] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.ZK.System.satisfied_cons_cons`
**Module**: `HeytingLean.Crypto.ZK.Support`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: satisfied_cons_cons
**Signature**: `∀ {a : HeytingLean.Crypto.ZK.Var → Rat} {c : HeytingLean.Crypto.ZK.Constraint} {sys : HeytingLean.Crypto.ZK.System}, Iff (HeytingLean.Crypto.ZK.System.satisfied a { constraints := List.cons c sys.constraints }) (And (HeytingLean.Crypto.ZK.Constraint.satisfied a c) (HeytingLean.Crypto.ZK.System.satisfied a sys))`

States satisfied cons cons. Use when your goal matches this shape or to rewrite subterms using this result.

## Keywords
cons, cons., heytinglean.crypto.zk.system.satisfied_cons_cons, satisfied, states, use, when, your

---
## Navigation (real dependency / similarity edges)
- ↖️ **NW**: [satisfied [dependency]](cell_R2_C4.md)
