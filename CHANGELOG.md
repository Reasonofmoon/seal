# Changelog

## 0.3.8 — 2026-09-19

### Worked compare-jev log
- Pack `packs/compare.jev/` — three gaps + `effect.compare.ship` (env code / claim escalate / human_form)
- Real run under `examples/compare-jev/` + harness `runs/compare-jev-20260919/`
- COMPARE.md · JEV-ONLY.md · board.html · seal-status.json (effect left **locked**)
- TypeSafe claim-gate executed: bad BLOCK noul=0.99, clean PASS noul=0.04

## 0.3.7 — 2026-09-19

### Operator call-site wiring (templates + runbook)
- Herdr plan template mirrored: `recipes/herdr-plan.template.json`, `recipes/herdr-run-README.md`
- Frontier Gap recipe: `recipes/harness-frontier-gap.md` (human_form / adopt / primary-source)
- Deploy recipe: BlogRich env **name** checklist + `step-env-ready` → `step-require-done` before READY
- moonlang publish recipe expanded (draft + live claim-gate; `claim-seal-done.md` only)
- GitHub QA: `scripts/harness/examples/qa-items.sample.json` + `ghqa-YYYYMMDD` run_id pattern
- Operator runbook: `docs/OPERATOR-RUNBOOK.md` — five owners' mandatory commands
- Note: moonlang standing-orders SKILL + Herdr `runs/_TEMPLATE` / `bin/new-run.sh` live on the box (agent-data / herdr-manager), not this git tree except the recipe mirrors above

## 0.3.6 — 2026-09-19

### Council seal APPLIED (kernel + harness scripts)
- Coverage policy keys: `require_human_form`, `require_adopt_decision`, `require_primary_source`
- `try_seal(..., adopt_decision=)`; `set_adopt` / `stamp_gap_human_form` / `mark_primary_source_missing`
- CLI: `adopt`, `human-form`, `primary-source-missing`
- Pack `packs/fleet.coverage/` + effect `effect.fleet.ops_ready`
- Executable `scripts/harness/*.sh` (claim / github-qa / env / require-done / blocked-queue)
- Recipes `recipes/harness-*.md`; tests `tests/test_coverage_council.py`
- Docs: COUNCIL status → Applied v0.3.6; COVERAGE-POLICY points at scripts/harness

## 0.3.5 — 2026-09-19

### Council seal — fleet Coverage Gate
- Document harness-only `code` gates (Herdr / deploy / QA / moonlang / Gap)
- Fail · 「확인 실패」 · API fail → escalate; unapproved READY/merge/publish/redeploy = 0
- Evidence SSOT `runs/<id>/*-done.md`; Strike ≠ adopt; `human_form_required`

## 0.3.4 — 2026-09-19

### README overwhelm pass
- Hero, kernel loop, Gap Board UI mock, parade & coverage visuals
- Affordance CTAs: Start / Board / Why / Public proof
- Sticky next-action bar on Gap Board HTML

## 0.3.3 — 2026-09-19

### Practical adoption
- `seal init` scaffolds `.seal/graph.json`
- `scripts/demo.sh` one-shot demo
- CI workflow recipe + `recipes/github-seal-check.md`
- `AGENTS.md` for coding agents
- Fleet council channel kickoff (ops/deploy/QA/moonlang/frontier)

## 0.3.2 — 2026-09-19

### README visuals
- `docs/assets/seal-vs-parade.png` — Agent parade vs SEAL kernel
- `docs/assets/seal-coverage-gate.png` — Accuracy-only vs Coverage Ledger
- Public-repo worked example table on README

## 0.3.1 — 2026-09-19

### Concrete Coverage Gate
- Effects honor `coverage_policy` (default: no open escalations); `lock_reason` on locked effects
- Providers `code:` and `human:` allowed on all risk bands; `seal-code` CLI
- CLI: `attach-pack`, `evidence`, `coverage`, `escalate`
- Gap Board renders coverage ledger + open escalations
- CONTEXT emit includes coverage + evidence sections
- Docs: `BEYOND-JEV.md`, `COVERAGE-POLICY.md`, `CASES-PUBLIC.md`

### Public-repo cases
- LangChain, CrewAI, AutoGen, Vercel AI, TypeSafe SDK scorecards under `examples/public-repos/`

## 0.3.0 — 2026-09-19
- Coverage path stamped on seals; public launch of Reasonofmoon/seal
