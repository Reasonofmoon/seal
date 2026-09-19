# SEAL roadmap status

| Phase | Status | Notes |
|-------|--------|-------|
| S0–S3b | done | kernel + edtech.foundation + TypeSafe mint |
| **S4 audit-spec conquest** | **done (design+pack+proof)** | `packs/conquest.audit-spec` · weak golden spec fails R01/R03/R05 |
| S5 More effects | next | codegen unlock after passport |
| S6 Vein | pending | |
| S7 UKDL subset | pending | |
| S8 Gap Board UI | pending | |

## S4 proof

Fixture: `fixtures/af-spec-v4-global-weak.md` (AF golden weaknesses).

| Strike | passes_category noul | Result |
|--------|----------------------|--------|
| R01 timeline | 0.10 | lock_failed |
| R03 team_budget | 0.03 | lock_failed |
| R05 cli_flag | 0.04 | lock_failed |

`effect.aplus_implement_unlock` remains **locked** — no fake A+.
