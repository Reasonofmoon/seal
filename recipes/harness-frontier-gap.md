# Recipe: Frontier Gap Prospector (coverage ops)

Council 2026-09-19 · SEAL v0.3.7+

## Forms / subscribe gaps

Gaps that collect human input (forms, subscribe, opt-in):

1. Set `human_form_required: true` on the gap.
2. Seal **only** when `coverage.human_form_submitted` is true (CLI below), **or** leave the gap escalated — never treat agent auto-fill as success.
3. Effect policy: set `require_human_form: true` when the effect must wait on forms.

```bash
seal human-form --graph G --gap gap.… --submitted true   # after real human submit
# or leave escalate until human completes the form
```

## Adopt ≠ Strike

Machine `metric_pass` / Strike success is **not** adopt.

```bash
seal adopt --graph G --seal seal.… --decision adopt|reject|defer
```

Effect policy: `require_adopt_decision: true` so every seal in `effect.after` carries `adopt_decision`.

## Primary source

If answers mark `PRIMARY_SOURCE_NOT_FOUND` (or second-hand-only):

```bash
seal primary-source-missing --graph G --gap gap.… --reason "PRIMARY_SOURCE_NOT_FOUND"
# → code fail / coverage path escalate; do not qualify the gap
```

Effect policy: `require_primary_source: true` as needed.

## Effect policy sketch

```json
{
  "require_no_open_escalations": true,
  "require_human_form": true,
  "require_adopt_decision": true,
  "require_primary_source": true
}
```

## Never

- Auto-click approval / adopt UI
- Seal a form gap without `human_form_submitted`
- Unlock effect without `adopt_decision` when policy requires it
- Qualify on second-hand sources alone

See [COVERAGE-POLICY.md](../docs/COVERAGE-POLICY.md) · [OPERATOR-RUNBOOK.md](../docs/OPERATOR-RUNBOOK.md).
