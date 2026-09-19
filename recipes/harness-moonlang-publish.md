# Recipe: moonlang publish claim gate

Council 2026-09-19 · call-site wiring v0.3.7  
Standing orders: `workflows/moonlang-standing-orders` (agent-data; not in this git).

## Before `status=publish`

1. Write final HTML to a path on disk.
2. Run claim gate as a **harness step** (never pane prompt):

```bash
RUN_ID="moonlang-<pageId>-<YYYYMMDD>"
bash /workspace/seal/scripts/harness/step-claim-gate.sh "$RUN_ID" /path/to/final.html
bash /workspace/seal/scripts/harness/step-require-done.sh "$RUN_ID" \
  "${SEAL_RUNS_ROOT:-/workspace/seal/runs}/${RUN_ID}/claim-seal-done.md"
```

3. Publish **ONLY** if `claim-seal-done.md` exists under that run.
   - On `claim-seal-escalate.md` or missing done → stop, report 「확인 실패」 / BLOCK, **never publish**.
4. After public URL returns HTTP 200, **re-run** claim-gate on live HTML (fetch → tempfile → same step).
   - Draft PASS + live FAIL → escalate · queue only (do not leave as silent fail).
5. Keys: `TYPESAFE_API_KEY` via env / box-secrets only — never in pane prompts.

## Exit codes

| Result | Artifact | Action |
|--------|----------|--------|
| Exit 0 PASS | `claim-seal-done.md` (+ JSON stdout) | May publish |
| Exit 2 BLOCK | `claim-seal-escalate.md` | Stop · 「확인 실패」 |
| API / missing gate | escalate | Stop · never invent pass |

## Run id pattern

`moonlang-<pageId>-<YYYYMMDD>` e.g. `moonlang-318-20260919`.
