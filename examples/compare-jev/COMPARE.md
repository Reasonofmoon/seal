# SEAL vs Jev — worked comparison log

- **Product:** `compare.jev.20260919`
- **Idea:** Can we READY BlogRich-like deploy and publish marketing HTML without hiding exceptions?
- **Timestamp (KST):** 2026-09-19 17:44–17:45 KST (graph seals at `2026-09-19T08:44:48+00:00` / `08:45:03+00:00`)
- **TypeSafe / Jev API key:** **present** (real mint ran)
- **Final effect:** `effect.compare.ship` → **`locked`**
- **lock_reason (from real graph):** `["unsealed:['gap.compare.claim']"]`
- **Also true (coverage ledger):** open escalation on claim; `human_form_pending: [gap.compare.human_approve]`

This log was produced by **executing** SEAL + harness scripts on the box — not invented.

## Step table

| Step | Jev-only | SEAL | Evidence path |
|------|----------|------|---------------|
| 0. Open product / three gaps | No product object | `seal open --pack compare.jev` → durable `graph.json` | `run/graph.json`, `run/seal-status-open.json` |
| 1. Env gate (`PATH`, `HOME`) | N/A (not a mint) | `step-env-ready.sh` → `seal-code` provider `code:env_ready_harness` → seal.0001 path=`code` adopt=`adopt` | `runs/compare-jev-20260919/env-ready-done.md`, seal.0001 in graph |
| 2a. Claim on **bad** HTML (“명문대 합격 보장”) | Mint **BLOCK** noul=0.99 jev-1.13.0 — then **stops** (stdout only) | Same mint via harness → `claim-seal-escalate.md` + `seal escalate` — gap **stays open** in exception queue | `jev-only/claim-gate-stdout-bad.json`, `runs/.../claim-seal-escalate.md`, `run/claim-seal-gate-stdout.json` |
| 2b. Claim on **clean** HTML | Mint **PASS** noul=0.04 | Not used to unlock ship; documented as counterfactual in JEV-ONLY.md | `jev-only/claim-gate-stdout-clean.json` |
| 3. Human / blocked approval | No queue; agent may auto-click | `step-herdr-blocked-queue.sh` (never auto-approve); `human-form --submitted false`; auto `seal-code` → coverage path=`escalate`, adopt=`defer` | `runs/.../blocked-queue-done.md`, seal.0002, `run/human-seal-attempt.json` |
| 4. Ship / READY effect | PASS mint ≠ ship | `effect.compare.ship` locked until env+claim+human + coverage_policy | `run/seal-status.json` → `effect_locks` |
| 5. Board / ledger | Accuracy dashboard only | Gap Board + coverage counts | `run/board.html`, `run/coverage.json` |

## Coverage ledger (real run)

From `run/coverage.json` / `seal coverage`:

| Metric | Value |
|--------|-------|
| total_seals | 2 |
| counts.code | 1 (`gap.compare.env_ready`) |
| counts.escalate | 1 (`gap.compare.human_approve` — form not submitted) |
| counts.auto / human | 0 / 0 |
| auto_rate | 0.5 |
| escalate_open | `["gap.compare.claim"]` |
| human_form_pending | `["gap.compare.human_approve"]` |

## Effect lock (real graph)

```json
"effect.compare.ship": {
  "status": "locked",
  "lock_reason": ["unsealed:['gap.compare.claim']"],
  "coverage_policy": {
    "require_no_open_escalations": true,
    "require_human_form": true,
    "require_adopt_decision": true
  }
}
```

Even if claim were sealed later, ship would still fail `require_human_form` until `human_form_submitted=true`, and would require adopt decisions on all after-gaps (env already `adopt`; human currently `defer`).

## Harness SSOT listing
> **Note:** `runs/` is gitignored; the same files are mirrored at `run/harness/` for the GitHub tree.


```
runs/compare-jev-20260919/blocked-queue-done.md
runs/compare-jev-20260919/claim-escalate.md
runs/compare-jev-20260919/claim-seal-escalate.md
runs/compare-jev-20260919/claim-seal-gate-stdout.json
runs/compare-jev-20260919/env-ready-done.md
```

## Journal ops (excerpt)

`open` → `seal` (env) → `escalate` (claim) → `human_form` → `seal` (human escalate-path) → `adopt` defer — see `run/journal-excerpt.json`.

## Conclusion (falsifiable)

On 2026-09-19 KST, with TypeSafe key present, Jev correctly **BLOCK**ed forbidden marketing copy (noul 0.99) and **PASS**ed clean copy (noul 0.04); SEAL recorded that BLOCK as an **open escalation**, sealed env only via **code** harness evidence, stamped human approval as **escalate/defer** without form submit, and left **`effect.compare.ship` locked**. Anyone can re-open `run/graph.json` and `run/board.html`: if ship were `ready`/`done` while `gap.compare.claim` is still open or `human_form_pending` is nonempty, this comparison would be false. Jev alone never wrote a product SSOT or an effect lock — that is the Coverage Gate difference claimed in `docs/BEYOND-JEV.md`.
