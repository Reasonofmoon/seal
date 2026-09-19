# Recipe: moonlang publish claim gate

Before `status=publish`:

```bash
bash /workspace/seal/scripts/harness/step-claim-gate.sh <run_id> /path/to/final.html
# then require the done file
bash /workspace/seal/scripts/harness/step-require-done.sh <run_id> \
  "${SEAL_RUNS_ROOT:-/workspace/seal/runs}/<run_id>/claim-seal-done.md"
```

- Exit 0 PASS → `claim-seal-done.md` (JSON stdout)
- Exit 2 BLOCK / API fail → escalate · never publish
- `TYPESAFE_API_KEY` from env / box-secrets only — never in pane prompts
