# SEAL operator runbook — mandatory call sites

v0.3.7 · Council 2026-09-19 · **owners cannot skip these commands**

Evidence SSOT: `SEAL_RUNS_ROOT` (default `/workspace/seal/runs`) → `<run_id>/*-done.md`.  
Keys only via env / box-secrets. Never pane-prompt TypeSafe / claim / env / QA. Never auto-approve.

## Five owners

| Owner | Mandatory before advance | Command |
|-------|--------------------------|---------|
| **Herdr** | Every run start; blocked → queue only | `bash …/step-herdr-blocked-queue.sh <id>` · copy `runs/_TEMPLATE` via `bin/new-run.sh <id>` · never auto-approve |
| **배포 감사** | Before Vercel READY / promote | `step-env-ready.sh <id> <ENV…>` then `step-require-done.sh <id> …/env-ready-done.md` |
| **GitHub QA** | Weekday briefing ranks | `step-github-qa-score.sh ghqa-YYYYMMDD <qa-items.json>` · consume `*-done.md` only |
| **moonlang** | Before `status=publish` (+ live recheck) | `step-claim-gate.sh moonlang-<pageId>-YYYYMMDD <html>` · publish only if `claim-seal-done.md` |
| **Frontier Gap** | Forms / adopt / primary source | `human_form_required` + `seal human-form` · `seal adopt --decision adopt\|reject\|defer` · `seal primary-source-missing` on `PRIMARY_SOURCE_NOT_FOUND` |

## Canonical paths

```text
/workspace/seal/scripts/harness/step-herdr-blocked-queue.sh
/workspace/seal/scripts/harness/step-env-ready.sh
/workspace/seal/scripts/harness/step-github-qa-score.sh
/workspace/seal/scripts/harness/step-claim-gate.sh
/workspace/seal/scripts/harness/step-require-done.sh
```

Herdr wrappers: `/workspace/herdr-manager/orchestration-harness/bin/step-*.sh`  
Herdr template: `orchestration-harness/runs/_TEMPLATE/` · public mirrors: `recipes/herdr-plan.template.json`, `recipes/herdr-run-README.md`

## Recipes

| Topic | File |
|-------|------|
| Coverage gate | [recipes/harness-coverage-gate.md](../recipes/harness-coverage-gate.md) |
| Deploy / BlogRich env | [recipes/harness-deploy-env.md](../recipes/harness-deploy-env.md) |
| moonlang publish | [recipes/harness-moonlang-publish.md](../recipes/harness-moonlang-publish.md) |
| GitHub QA | [recipes/harness-github-qa.md](../recipes/harness-github-qa.md) |
| Frontier Gap | [recipes/harness-frontier-gap.md](../recipes/harness-frontier-gap.md) |

## Fail posture

FAIL · 「확인 실패」 · API failure → write `*-escalate.md`, exit non-zero, **queue** READY / merge / publish / redeploy / adopt. Never invent pass.
