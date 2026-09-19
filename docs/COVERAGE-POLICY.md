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

## CLI

```bash
seal escalate --graph G --gap gap.… --reason "low confidence"
seal coverage --graph G
seal seal-code --graph G --gap gap.… --ok --predicate code:lint_clean
seal attach-pack --graph G --pack blogrich.trust
seal evidence --graph G --kind github_repo --ref https://github.com/…
```
