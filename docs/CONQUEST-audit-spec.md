# S4 Conquest — Destroy `audit-spec`

## What dies

| App Factory | Fate |
|-------------|------|
| `modules/L9-quality/spec-audit` as terminal boss | **Destroyed as happy path** |
| `app-factory audit-spec` after ship/pack | **Replaced** by SEAL Gap strikes during quality phase |
| Single LLM essay scoring R01–R13 at once | **Replaced** by 13 independent Strikes (Jev Nouls) |
| `overall.aplus_threshold_passed` boolean theater | **Replaced** by `effect.aplus_implement_unlock` passport |

## What is scavenged

- R01–R13 category definitions & detection patterns → Gap `ask` / fail_examples
- Tier thresholds T1/T2/T3 → `noul_gte` defaults on pack (`tier_noul_defaults`)
- `known_cli_flags` → `product.known_cli_flags` in World Projection
- Golden weak spec → `fixtures/af-spec-v4-global-weak.md` regression corpus
- Evidence discipline → every rubric Gap requires `evidence_refs` in candidate schema

## New object

Pack **`conquest.audit-spec`**:

1. `gap.af.spec.corpus` — seal the spec text first  
2. `gap.af.rubric.R01_*` … `R13_*` — each category is a Gap; candidate is `{evidence_refs, assertion}`  
3. `effect.aplus_implement_unlock` — emits `APLUS_PASSPORT.md` only when all sealed  

**No seal on a rubric Gap ⇒ that dimension did not pass.**  
Unsealed rubric Gaps *are* blocking gaps (`has_blocking_spec_gaps`).

## Anti-federation rule

Do not call `audit-spec` and then “also” SEAL.  
Ship/implement unlock reads the passport Effect — not an envelope field from a generative auditor.

## Demo expectation (weak golden spec)

| Gap | Expected |
|-----|----------|
| R01 timeline | fail Strike (Phase 7/8 impossible) |
| R03 team_budget | fail (no team/funding) |
| R05 cli_flag | fail (`--modules` unknown) — requires TypeSafe (`user_trust`) |
| R13 scope | fail (pasted F23) — TypeSafe |

## Commands

```bash
seal open --id shield --idea "…" --pack conquest.audit-spec --out graph.json
# set known CLI flags on product (see examples)
seal fill --gap gap.af.spec.corpus --file fixtures/af-spec-v4-global-weak.md
seal strike --gap gap.af.spec.corpus --candidate candidate.0001 --provider heuristic
# then per rubric…
seal strike --gap gap.af.rubric.R01_timeline_realism --candidate … --provider typesafe
```
