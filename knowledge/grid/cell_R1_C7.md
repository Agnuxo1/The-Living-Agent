# Cell [1,7] — KNOWLEDGE
**FQN**: `HeytingLean.LoF.LeanKernel.Expr`
**Module**: `HeytingLean.LoF.LeanKernel.Expression`
**Kind**: `inductive`
**Centrality**: 0.001724

## Topic
**Declaration**: Expr
**Signature**: `Type u → Type u → Type u → Type u → Type u`

Kernel expression AST with a deliberately small 9-way constructor split. We parameterize universe levels separately from expression metavariables: - `Param` / `MetaLevel` appear inside `ULevel` values (Phase 7), - `MetaExpr` is used for expression metavariables. The chosen 9 constructors align with the “core” shapes used by kernels: `bvar`, `mvar`, `sort`, `const`, `app`, `lam`, `forallE`, `letE`, `lit`.

## Keywords
a, ast, deliberately, expression, heytinglean.lof.leankernel.expr, kernel, small, with

---
## Navigation (real dependency / similarity edges)
- ➡️ **E**: [Obj [similarity]](cell_R1_C8.md)
- ⬅️ **W**: [Task [similarity]](cell_R1_C6.md)
