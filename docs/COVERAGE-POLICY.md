# Coverage policy (concrete)

## Seal.coverage.path

| Path | When |
|------|------|
| `auto` | `heuristic:*` or `typesafe:*` strike cleared locks |
| `code` | `code:*` deterministic predicate sealed the gap |
| `human` | `human:*` or human fill without mint answers |
| `escalate` | Gap was marked escalated before seal (exception queue) |

## Effect.coverage_policy

Merged with `schemas/lock-policy.json` → `coverage.effect_default`.

```json
{
  "require_no_open_escalations": true,
  "min_auto_rate": 0.0,
  "min_seals": 0
}
```

`refresh_effects` sets `effect.lock_reason` when locked for coverage or missing seals.

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
seal attach-pack --graph G --pack blogrich.trust
seal evidence --graph G --kind github_repo --ref https://github.com/…
```
