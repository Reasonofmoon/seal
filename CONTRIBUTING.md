# Contributing to SEAL

## Invariant
**No seal, no advance.** PRs that let generation unlock Effects without seals will be rejected.

## Add a public-repo case
1. Open pack `audit.workflow-class`
2. Seal all six criteria with `subject_repo` + `evidence_url` pointing at a **public** GitHub repo
3. Drop `CASE.md`, `graph.json`, `board.html`, `scorecard.json` under `examples/public-repos/<id>/`
4. Link it from `docs/CASES-PUBLIC.md`

## Add a Gap Pack
See `packs/edtech.foundation/` for shape: `pack.json`, `gaps/*.json`, `effects.json` (optional `coverage_policy`).

## Tests
```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```
