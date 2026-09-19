# S7 — UKDL subset grammar (SEAL dialect)

## Destruction
UKDL v2.0 **L3–L5** (`action`, `quantum`, `pipeline`) claimed documents execute.
SEAL keeps UKDL only as **human-readable serialization** of the Seal Graph.

| UKDL level | Kind | SEAL |
|------------|------|------|
| L0–L1 surface | meta, entity, rel | **kept** (meta/entity/rel) |
| — | gap, candidate, seal, effect | **SEAL kinds** (not in stock UKDL) |
| L2 | include, context | rejected in subset (CONTEXT is an Effect artifact) |
| L3 | action | **legacy / banned** |
| L4 | quantum | **legacy / banned** — use resealing Gaps |
| L5 | pipeline | **legacy / banned** — Effects + Vein |

## Dialect
- Fence form: `:: kind id=...` … `::`
- File tip: `.seal.ukdl`
- `@ukdl_level: 1` + `@seal_dialect: "seal-ukdl-0.1"` on meta

## CLI
```bash
python3 src/seal/cli.py dump --graph PATH [--out out.seal.ukdl]
python3 src/seal/cli.py load-ukdl --file out.seal.ukdl [--out partial.json]
python3 src/seal/cli.py load-ukdl --file evil.ukdl --validate-only
```

## Module
`src/seal/ukdl_subset.py` — `dump` / `parse` / `validate_text`
