# Recipe: deploy env ready (배포 감사)

Before Vercel READY / promote:

```bash
export SEAL_RUNS_ROOT=/workspace/seal/runs   # or your run root
RUN_ID="deploy-<product>-<YYYYMMDD>"

bash /workspace/seal/scripts/harness/step-env-ready.sh "$RUN_ID" \
  VERCEL_TOKEN \
  # …product-specific required names (checklist below)

bash /workspace/seal/scripts/harness/step-require-done.sh "$RUN_ID" \
  "${SEAL_RUNS_ROOT}/${RUN_ID}/env-ready-done.md"
```

- Exit 0 → `env-ready-done.md`
- Missing/empty → `env-ready-escalate.md` + exit 2 · 「확인 실패」
- Do **not** mark READY from a pane prompt.
- Order: **`step-env-ready.sh` then `step-require-done.sh`** before READY/promote.

## BlogRich checklist (EXAMPLES — names only, not secrets)

Pass these **names** to `step-env-ready.sh` when promoting BlogRich (values must already be set in the deploy env; never paste secrets into plans/prompts):

| Env name | Role |
|----------|------|
| `VERCEL_TOKEN` | Deploy / promote auth |
| `NAVER_API_HUB_KEY_ID` | Naver API Hub Client ID (alias: `NAVER_CLIENT_ID`) |
| `NAVER_API_HUB_KEY` | Naver API Hub Client Secret (alias: `NAVER_CLIENT_SECRET`) |
| `NAVER_DATA_MODE` | `mock` \| `live` \| `auto` |
| `TYPESAFE_API_KEY` | Claim / diagnose gates (env or box-secrets) |
| `BLOGRICH_DATABASE_URL` | Dataplane (if product requires) |

Optional: `NAVER_API_HUB_BASE` (defaults in app).

Example call (checklist — ensure vars are set in shell/Vercel first):

```bash
bash /workspace/seal/scripts/harness/step-env-ready.sh "$RUN_ID" \
  VERCEL_TOKEN \
  NAVER_API_HUB_KEY_ID \
  NAVER_API_HUB_KEY \
  NAVER_DATA_MODE \
  TYPESAFE_API_KEY
bash /workspace/seal/scripts/harness/step-require-done.sh "$RUN_ID" \
  "${SEAL_RUNS_ROOT}/${RUN_ID}/env-ready-done.md"
```
