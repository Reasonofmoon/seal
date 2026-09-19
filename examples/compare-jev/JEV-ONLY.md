# Jev-only column (honest)

What this run actually did with TypeSafe System One / Jev, and what Jev **cannot** do alone.

## What Jev provides

- Typed mint answers: **Noul / Score / Choice** — schema-valid judgments for bounded questions.
- Here: `node /workspace/typesafe-gates/claim-gate.mjs` over marketing HTML.
- Key source: `TYPESAFE_API_KEY` via env / `box-secrets.json` (`load-key.mjs`). **Key was present** for this run.

## What this run minted

| Fixture | Exit | Decision | Noul | Model | Evidence |
|---------|------|----------|------|-------|----------|
| `fixtures/bad-claim.html` (“명문대 합격 보장”) | 2 | **BLOCK** | 0.99 | jev-1.13.0 | `jev-only/claim-gate-stdout-bad.json` |
| `fixtures/clean-claim.html` (honest copy) | 0 | **PASS** | 0.04 | jev-1.13.0 | `jev-only/claim-gate-stdout-clean.json` |

Canonical bad stdout also copied to `jev-only/claim-gate-stdout.json`.

## What Jev does **NOT** provide

Themes from [docs/BEYOND-JEV.md](../../docs/BEYOND-JEV.md) (no invented HN quotes):

| Missing in Jev-only world | Why it matters for BlogRich-like ship |
|---------------------------|----------------------------------------|
| Advance gate | A PASS mint does not unlock READY / publish / redeploy |
| Durable Seal Graph SSOT | No `graph.json` product brain; stdout is ephemeral |
| Coverage ledger | Accuracy-only; no `auto` / `escalate` / `human` / `code` paths |
| Effect lock + `lock_reason` | Nothing records *why* ship must stay closed |
| Harness `*-done.md` / `*-escalate.md` SSOT | No `runs/<id>/` evidence contract |
| Blocked → queue without auto-approve | Mint cannot enqueue 감독관 / refuse UI; agents may still click |
| `human_form_required` + `adopt_decision` | Strike ≠ adopt; form pending is invisible to Jev |

## Counterfactual

Even if only the **clean** fixture existed and Jev returned **PASS** (noul 0.04), Jev-only would still:

1. Not seal `gap.compare.env_ready` (needs harness `code:`).
2. Not clear `gap.compare.human_approve` (`human_form_submitted` / adopt).
3. Not unlock `effect.compare.ship` under SEAL `coverage_policy`.

A green mint is a judgment — not a product advance.

## TypeSafe key

- **Present:** yes (loaded by `claim-gate.mjs`).
- Had it been missing, this folder would contain `UNAVAILABLE.md` instead of stdout JSON, and SEAL would still escalate claim with 「확인 실패」 rather than invent PASS.
