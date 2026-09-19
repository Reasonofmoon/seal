# Coverage policy (concrete)

## Seal.coverage.path

| Path | When |
|------|------|
| `auto` | `heuristic:*` or `typesafe:*` strike cleared locks |
| `code` | `code:*` deterministic predicate sealed the gap |
| `human` | `human:*` or human fill without mint answers |
| `escalate` | Gap was marked escalated before seal (exception queue) |

## Effect.coverage_policy

Merged with `schemas/lock-policy.json` → `coverage.effect_default` (v0.3.6).

```json
{
  "require_no_open_escalations": true,
  "require_human_form": false,
  "require_adopt_decision": false,
  "require_primary_source": false,
  "min_auto_rate": 0.0,
  "min_seals": 0
}
```

| Key | Behavior |
|-----|----------|
| `require_human_form` | Fails if `human_form_pending` nonempty (gaps with `human_form_required` not sealed with `coverage.human_form_submitted`) |
| `require_adopt_decision` | Every seal for gaps in `effect.after` must have `adopt_decision` ∈ {adopt, reject, defer} |
| `require_primary_source` | Fails if any gap/seal has `primary_source_missing` or answers mark `PRIMARY_SOURCE_NOT_FOUND` |

`refresh_effects` sets `effect.lock_reason` when locked for coverage or missing seals.

## Executable harness scripts

Canonical location: **`scripts/harness/`**

| Script | Role |
|--------|------|
| `lib.sh` | `write_done` / `escalate_fail` (exit 2 + `*-escalate.md`) |
| `step-claim-gate.sh` | `claim-gate.mjs` → `claim-seal-done.md` |
| `step-github-qa-score.sh` | QA score; API fail → 「확인 실패」 |
| `step-env-ready.sh` | env names set+nonempty |
| `step-require-done.sh` | success iff file/glob exists |
| `step-herdr-blocked-queue.sh` | documents queue-only; **never auto-approves** |

Evidence SSOT: `SEAL_RUNS_ROOT/<run_id>/*-done.md` (default `/workspace/seal/runs`).

Recipes: `recipes/harness-coverage-gate.md`, `harness-deploy-env.md`, `harness-moonlang-publish.md`, `harness-github-qa.md`.

## Fleet harness (council 2026-09-19)

Sealed with Herdr · 배포 감사 · GitHub QA · moonlang · Frontier Gap Prospector.

| Rule | Detail |
|------|--------|
| Where gates run | **Harness step only** — never pane prompt |
| Keys | env / box-secrets only |
| FAIL / API fail / unverifiable | `escalate` + 「확인 실패」 — no silent pass |
| Approval UI | Never auto-click |
| READY / merge / publish / redeploy / adopt | Queue only until human or sealed `code` |
| Evidence SSOT | `runs/<id>/*-done.md` + artifacts |
| Strike vs Seal | Machine metric_pass ≠ adopt (`adopt_decision` required for Effect) |
| Forms / subscribe | `human_form_required` — agent auto ≠ success |
| Primary source | `PRIMARY_SOURCE_NOT_FOUND` → `code` fail |

Canonical council record: [COUNCIL-2026-09-19.md](COUNCIL-2026-09-19.md)

## CLI

```bash
seal escalate --graph G --gap gap.… --reason "low confidence"
seal coverage --graph G
seal seal-code --graph G --gap gap.… --ok --predicate code:lint_clean
seal adopt --graph G --seal seal.0001 --decision adopt|reject|defer
seal human-form --graph G --gap gap.… --submitted true|false
seal primary-source-missing --graph G --gap gap.… --reason "…"
seal attach-pack --graph G --pack fleet.coverage
seal evidence --graph G --kind github_repo --ref https://github.com/…
```
