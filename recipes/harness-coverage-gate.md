# Recipe: harness Coverage Gate (from Herdr plan.json)

Council 2026-09-19 · SEAL v0.3.6

## Invariant

- Every `code` gate = **harness step** (never pane prompt)
- Keys only via env / box-secrets
- FAIL · 「확인 실패」 · API failure → escalate (non-zero + `*-escalate.md`)
- Never auto-click approval UI
- Evidence SSOT: `runs/<id>/*-done.md`

## Scripts

| Step | Command |
|------|---------|
| claim | `bash /workspace/seal/scripts/harness/step-claim-gate.sh <run_id> <html>` |
| github-qa | `bash /workspace/seal/scripts/harness/step-github-qa-score.sh <run_id> <json>` |
| env | `bash /workspace/seal/scripts/harness/step-env-ready.sh <run_id> VAR…` |
| require | `bash /workspace/seal/scripts/harness/step-require-done.sh <run_id> <glob>` |
| blocked | `bash /workspace/seal/scripts/harness/step-herdr-blocked-queue.sh <run_id>` |

`SEAL_RUNS_ROOT` defaults to `/workspace/seal/runs`.

## plan.json sketch

```json
{
  "id": "fleet-cov-001",
  "steps": [
    { "run": "bash /workspace/seal/scripts/harness/step-env-ready.sh fleet-cov-001 PATH HOME" },
    { "run": "bash /workspace/seal/scripts/harness/step-herdr-blocked-queue.sh fleet-cov-001" },
    { "collect": "runs/fleet-cov-001/*-done.md" }
  ]
}
```

Collect success = files exist (not agent scrollback).
