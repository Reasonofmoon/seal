# Recipe: GitHub QA score (weekday briefing)

```bash
# json-in: array of { id, title, kind, repo, ageDays?, ciFailed?, security? }
# sample: scripts/harness/examples/qa-items.sample.json
RUN_ID="ghqa-$(date +%Y%m%d)"   # weekday briefing pattern: ghqa-YYYYMMDD
bash /workspace/seal/scripts/harness/step-github-qa-score.sh "$RUN_ID" \
  /workspace/seal/scripts/harness/examples/qa-items.sample.json
```

- Exit 0 → `github-qa-score-done.md` with ranked JSON
- API / exit fail → escalate 「확인 실패」 — do not invent ranks
- Briefing consumes done-file JSON only; pane never calls the SDK
- `run_id` pattern for weekday briefing: **`ghqa-YYYYMMDD`**
