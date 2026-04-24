# Cell [15,1] — SYNTHESIS
**FQN**: `HeytingLean.Crypto.Lens.Form.evalL.eq_4`
**Module**: `HeytingLean.Crypto.Lens.Transport`
**Kind**: `theorem`
**Centrality**: 0.000023
**Dependency Depth**: 4

## Topic
**Declaration**: eq_4
**Signature**: `∀ {α : Type u} [inst : HeytingLean.LoF.PrimaryAlgebra α] {R : HeytingLean.LoF.Reentry α} {n : Nat} (L : HeytingLean.Crypto.Lens R) (x : L.EnvL n) (φ ψ : HeytingLean.Crypto.Form n), Eq (HeytingLean.Crypto.Lens.Form.evalL L (φ.and ψ) x) (L.and (HeytingLean.Crypto.Lens.Form.evalL L φ x) (HeytingLean.Crypto.Lens.Form.evalL L ψ x))`

States eq 4. Use when your goal matches this shape or to rewrite subterms using this result.

## Keywords
4., eq, goal, heytinglean.crypto.lens.form.evall.eq_4, states, use, when, your

---
## Navigation (real dependency / similarity edges)
- ↗️ **NE**: [Lens [dependency]](cell_R4_C10.md)
- ↖️ **NW**: [PrimaryAlgebra [dependency]](cell_R0_C0.md)
