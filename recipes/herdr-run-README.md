# Herdr run template

## Start a run

```bash
bash /workspace/herdr-manager/orchestration-harness/bin/new-run.sh <id>
# or: copy this folder to runs/<id>/ and replace RUN_ID
```

1. Set `id` in `plan.json` (script does sed `RUN_ID` → `<id>`).
2. Fill `goal` / `workers` / domain-gate examples for this product.
3. Dispatch pane prompts only for worker artifacts — **never** for TypeSafe / claim / env / QA gates.

## Hard rules

- **Always** run `step-herdr-blocked-queue.sh <id>` (first step).
- **Never** auto-approve `agent_blocked` / approval UI.
- **Collect** only `*-done.md` and `*-escalate.md` (under `SEAL_RUNS_ROOT/<id>/` for harness steps; worker files under this folder).
- **Success = `*-done.md` only.** Missing done or any `*-escalate.md` → STOP · 「확인 실패」 · queue to user/감독관.
- Keys (`TYPESAFE_API_KEY`, etc.) via env / box-secrets only — never in pane prompts.

## Domain gates (comments in plan.json)

| Need | Script |
|------|--------|
| Env before READY | `step-env-ready.sh` |
| Claim before publish | `step-claim-gate.sh` |
| GitHub QA briefing | `step-github-qa-score.sh` |
| Assert evidence | `step-require-done.sh` |

Canonical scripts: `/workspace/seal/scripts/harness/`. Wrappers: `orchestration-harness/bin/step-*.sh`.
