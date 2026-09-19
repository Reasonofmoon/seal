"""Coverage Gate — the door beyond Jev.

Developer consensus on Jev (HN, independent reviews, jaggedness docs):
- Schema-valid ≠ semantically correct (confidently wrong is possible)
- Accuracy without coverage hides the exception queue
- Mint alone does not advance a durable product
- Deterministic code should win when it already decides correctly
- Pin versions; jev-latest drifts thresholds

SEAL answer: every Seal records a coverage path. Effects can require a
Coverage Ledger (auto vs escalate rates), not only sealed gap IDs.
"""
from __future__ import annotations
from typing import Any

# Paths a seal may take
AUTO = "auto"           # mint cleared locks; no human
ESCALATE = "escalate"   # mint low-confidence or policy → human seal required
HUMAN = "human"         # filled/sealed by human without mint
CODE = "code"           # deterministic predicate sealed the gap (no mint)

def classify_path(
    *,
    provider: str,
    answers: dict[str, Any] | None,
    by: str | None,
    escalated: bool = False,
) -> str:
    if escalated:
        return ESCALATE
    if provider.startswith("code:") or provider == "code":
        return CODE
    if by == "human" and (not answers):
        return HUMAN
    if provider.startswith("heuristic") or provider.startswith("typesafe"):
        return AUTO
    return AUTO

def ledger(graph: dict[str, Any]) -> dict[str, Any]:
    """Aggregate coverage across non-deprecated seals."""
    counts = {AUTO: 0, ESCALATE: 0, HUMAN: 0, CODE: 0, "unknown": 0}
    seals = []
    for sid, seal in (graph.get("seals") or {}).items():
        if seal.get("deprecated"):
            continue
        path = (seal.get("coverage") or {}).get("path") or "unknown"
        if path not in counts:
            path = "unknown"
        counts[path] += 1
        seals.append({"id": sid, "gap": seal.get("gap"), "path": path, "provider": seal.get("provider")})
    total = sum(v for k, v in counts.items() if k != "unknown") + counts["unknown"]
    auto = counts[AUTO] + counts[CODE]  # code counts as covered auto-path
    covered = auto + counts[HUMAN]  # human-complete also "covered" for unlock
    exception_queue = [
        gid for gid, g in (graph.get("gaps") or {}).items()
        if g.get("status") == "open" and g.get("escalated")
    ]
    return {
        "counts": counts,
        "total_seals": total,
        "auto_or_code": auto,
        "human": counts[HUMAN],
        "escalate_open": exception_queue,
        "auto_rate": (auto / total) if total else 0.0,
        "destroys": "accuracy-without-coverage dashboards; mint-as-product",
        "seals": seals,
    }

def meets_policy(graph: dict[str, Any], policy: dict[str, Any] | None) -> tuple[bool, list[str]]:
    """Effect unlock helper. policy keys: min_auto_rate, require_no_open_escalations, min_seals."""
    if not policy:
        return True, []
    led = ledger(graph)
    failures = []
    if "min_seals" in policy and led["total_seals"] < int(policy["min_seals"]):
        failures.append(f"min_seals {led['total_seals']} < {policy['min_seals']}")
    if "min_auto_rate" in policy and led["auto_rate"] + 1e-9 < float(policy["min_auto_rate"]):
        failures.append(f"auto_rate {led['auto_rate']:.3f} < {policy['min_auto_rate']}")
    if policy.get("require_no_open_escalations") and led["escalate_open"]:
        failures.append(f"open escalations: {led['escalate_open']}")
    return (not failures), failures
