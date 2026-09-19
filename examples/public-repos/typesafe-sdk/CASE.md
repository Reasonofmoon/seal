# Case: `typesafe-ai/typesafe-sdk-python`

**Public subject:** [typesafe-ai/typesafe-sdk-python](https://github.com/typesafe-ai/typesafe-sdk-python) · ~98★ (snapshot at case authoring)

TypeSafe/Jev mint — calibrated decisions; still no product advance gate alone.

## SEAL reading

Scored with pack `audit.workflow-class` against [WHY-SEAL](../../../docs/WHY-SEAL.md).

| Criterion | Verdict |
|-----------|---------|
| `gap.audit.advance_gate` | **fail** |
| `gap.audit.lock_locality` | **n/a** |
| `gap.audit.risk_band` | **pass** |
| `gap.audit.durable_ssot` | **fail** |
| `gap.audit.learning_honesty` | **n/a** |
| `gap.audit.serialization_runtime` | **pass** |

## What this proves

**Other people’s famous public repos** as subjects. SEAL scores workflow class, it does not wrap their code.

`fail` on `advance_gate` means step/crew/stream success can move work without a Seal.  
TypeSafe/Jev can `pass` judgment-related criteria and still **`fail` durable product SSOT** — mint ≠ sealed product brain.

Sealed **6/6** · Failed **0** · Evidence **7** · Effects `{'effect.audit.emit_scorecard': 'ready'}`
