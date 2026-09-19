# S5 — Destroy `implement` happy path

## What dies

| App Factory | Fate |
|-------------|------|
| `app-factory implement` after weak/partial audit | **Destroyed as ungated step** |
| `apply-implementation` writing src/ without passport | **Destroyed** |
| CONTEXT.md emitted by `pack` with no quality lock | **Destroyed** (CONTEXT now post-passport) |

## What replaces it

Effect chain on `conquest.audit-spec` v0.2:

```
all rubric Gaps sealed
        |
        v
effect.aplus_implement_unlock  --> APLUS_PASSPORT.md
        |
        v  (after_effects)
effect.emit_context            --> CONTEXT.md
        |
        v  (after_effects)
effect.codegen_vertical_slice  --> .seal_app/ stub (not a generative model)
```

Kernel rule: **`after_effects` must be `done`**, not merely `ready`.

Codegen stub is intentional: SEAL unlocks the *right to implement*; coding agents still write real code. What dies is implement-without-seal.

## Commands

```bash
# after all rubric seals…
seal effect --graph graph.json --id effect.aplus_implement_unlock --out-dir out/
seal effect --graph graph.json --id effect.emit_context --out-dir out/
seal effect --graph graph.json --id effect.codegen_vertical_slice --out-dir out/
# -> out/.seal_app/{README.md,App.tsx,seal.meta.json}
```

## Proof

`examples/s5-implement-unlock/` — synthetic all-sealed graph runs the chain; fresh graph cannot run codegen (locked).
