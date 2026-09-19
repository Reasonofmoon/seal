# Recipe: deploy env ready (배포 감사)

Before Vercel READY / promote:

```bash
export SEAL_RUNS_ROOT=/workspace/seal/runs   # or your run root
bash /workspace/seal/scripts/harness/step-env-ready.sh <run_id> \
  VERCEL_TOKEN \
  BLOGRICH_DATABASE_URL \
  # …product-specific required names
```

- Exit 0 → `env-ready-done.md`
- Missing/empty → `env-ready-escalate.md` + exit 2 · 「확인 실패」
- Do **not** mark READY from a pane prompt.
