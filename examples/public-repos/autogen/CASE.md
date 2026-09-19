# Case: `microsoft/autogen`

**Public subject:** [microsoft/autogen](https://github.com/microsoft/autogen) · ~61,058★ (snapshot at case authoring)

Programming framework for agentic AI — multi-agent conversation advances work.

## SEAL reading

Scored with pack `audit.workflow-class` against [WHY-SEAL](../../../docs/WHY-SEAL.md).

| Criterion | Verdict |
|-----------|---------|
| `gap.audit.advance_gate` | **fail** |
| `gap.audit.lock_locality` | **fail** |
| `gap.audit.risk_band` | **fail** |
| `gap.audit.durable_ssot` | **fail** |
| `gap.audit.learning_honesty` | **fail** |
| `gap.audit.serialization_runtime` | **n/a** |

## What this proves

**Other people’s famous public repos** as subjects. SEAL scores workflow class, it does not wrap their code.

`fail` on `advance_gate` means step/crew/stream success can move work without a Seal.  
TypeSafe/Jev can `pass` judgment-related criteria and still **`fail` durable product SSOT** — mint ≠ sealed product brain.

Sealed **6/6** · Failed **0** · Evidence **7** · Effects `{'effect.audit.emit_scorecard': 'ready'}`
