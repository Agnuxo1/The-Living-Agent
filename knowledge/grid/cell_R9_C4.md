# Cell [9,4] — KNOWLEDGE
**FQN**: `HeytingLean.Crypto.ZK.R1CSBool.linhead_imp_eval`
**Module**: `HeytingLean.Crypto.ZK.R1CSBool`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 2

## Topic
**Declaration**: linhead_imp_eval
**Signature**: `∀ {ρ : HeytingLean.Crypto.ZK.Var → Rat} {vx vy vmul vz : HeytingLean.Crypto.ZK.Var}, Eq (ρ vmul) (instHMul.hMul (ρ vx) (ρ vy)) → Eq (ρ vz) (instHAdd.hAdd (instHSub.hSub 1 (ρ vy)) (instHMul.hMul (ρ vy) (ρ vx))) → Eq ((HeytingLean.Crypto.ZK.R1CSBool.linhead_imp vz vx vy vmul).eval ρ) 0`

No docstring available; inspect the Lean declaration directly.

## Keywords
heytinglean.crypto.zk.r1csbool.linhead_imp_eval

---
## Navigation (real dependency / similarity edges)
- ↖️ **NW**: [linhead_imp [dependency]](cell_R3_C1.md)
