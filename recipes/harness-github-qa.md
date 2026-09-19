# Recipe: GitHub QA score (weekday briefing)

```bash
# json-in: array of { id, title, kind, repo, ageDays?, ciFailed?, security? }
bash /workspace/seal/scripts/harness/step-github-qa-score.sh <run_id> /tmp/qa-items.json
```

- Exit 0 → `github-qa-score-done.md` with ranked JSON
- API / exit fail → escalate 「확인 실패」 — do not invent ranks
- Briefing consumes done-file JSON only; pane never calls the SDK
