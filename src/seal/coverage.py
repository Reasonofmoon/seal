"""Coverage Gate — the door beyond Jev.

Developer consensus on Jev (HN, independent reviews, jaggedness docs):
- Schema-valid ≠ semantically correct (confidently wrong is possible)
- Accuracy without coverage hides the exception queue
- Mint alone does not advance a durable product
- Deterministic code should win when it already decides correctly
- Pin versions; jev-latest drifts thresholds

SEAL answer: every Seal records a coverage path. Effects can require a
Coverage Ledger (auto vs escalate rates), not only sealed gap IDs.

Coverage paths
--------------
auto       — mint cleared locks; no human
escalate   — mint low-confidence or policy → human seal required
human      — filled/sealed by human without mint
code       — deterministic predicate sealed the gap (no mint)

Policy keys (effect.coverage_policy / schemas/lock-policy.json effect_default)
-----------------------------------------------------------------------------
require_no_open_escalations  — open gaps with escalated=true block unlock
min_auto_rate / min_seals    — quantitative floors
require_human_form           — fails if human_form_pending nonempty
require_adopt_decision       — every seal for gaps in effect.after must have
                               adopt_decision in {adopt, reject, defer}
require_primary_source       — fails if any seal/gap has primary_source_missing
                               or answers mark PRIMARY_SOURCE_NOT_FOUND
"""
from __future__ import annotations
from typing import Any

# Paths a seal may take
AUTO = "auto"           # mint cleared locks; no human
ESCALATE = "escalate"   # mint low-confidence or policy → human seal required
HUMAN = "human"         # filled/sealed by human without mint
CODE = "code"           # deterministic predicate sealed the gap (no mint)

ADOPT_DECISIONS = frozenset({"adopt", "reject", "defer"})
PRIMARY_SOURCE_NOT_FOUND = "PRIMARY_SOURCE_NOT_FOUND"


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


def stamp_human_form(seal: dict[str, Any], submitted: bool) -> dict[str, Any]:
    """Stamp coverage.human_form_submitted on a seal (mutates and returns seal)."""
    cov = seal.setdefault("coverage", {})
    cov["human_form_submitted"] = bool(submitted)
    return seal


def _answers_primary_missing(answers: dict[str, Any] | None) -> bool:
    if not answers:
        return False
    if answers.get(PRIMARY_SOURCE_NOT_FOUND) is True:
        return True
    if answers.get("primary_source") == PRIMARY_SOURCE_NOT_FOUND:
        return True
    for v in answers.values():
        if v == PRIMARY_SOURCE_NOT_FOUND:
            return True
        if isinstance(v, dict) and (
            v.get("status") == PRIMARY_SOURCE_NOT_FOUND
            or v.get("code") == PRIMARY_SOURCE_NOT_FOUND
            or v.get(PRIMARY_SOURCE_NOT_FOUND) is True
        ):
            return True
    return False


def human_form_pending(graph: dict[str, Any]) -> list[str]:
    """Gaps where human_form_required and not sealed with coverage.human_form_submitted."""
    pending: list[str] = []
    for gid, g in (graph.get("gaps") or {}).items():
        if not g.get("human_form_required"):
            continue
        if g.get("status") != "sealed":
            pending.append(gid)
            continue
        sid = g.get("sealed_by")
        seal = (graph.get("seals") or {}).get(sid or "", {})
        if not (seal.get("coverage") or {}).get("human_form_submitted"):
            pending.append(gid)
    return pending


def primary_source_failures(graph: dict[str, Any]) -> list[str]:
    """IDs (gap or seal) that mark primary source missing."""
    fails: list[str] = []
    for gid, g in (graph.get("gaps") or {}).items():
        if g.get("primary_source_missing"):
            fails.append(gid)
    for sid, seal in (graph.get("seals") or {}).items():
        if seal.get("deprecated"):
            continue
        if seal.get("primary_source_missing"):
            fails.append(sid)
        if (seal.get("coverage") or {}).get("primary_source_missing"):
            fails.append(sid)
        if _answers_primary_missing(seal.get("answers")):
            fails.append(sid)
    return fails


def adopt_decision_missing(
    graph: dict[str, Any],
    gap_ids: list[str] | None = None,
) -> list[str]:
    """Seal ids lacking adopt_decision in {adopt, reject, defer}.

    If gap_ids is provided, only seals for those gaps are checked.
    Otherwise all non-deprecated seals are checked.
    """
    missing: list[str] = []
    want = set(gap_ids) if gap_ids is not None else None
    for sid, seal in (graph.get("seals") or {}).items():
        if seal.get("deprecated"):
            continue
        if want is not None and seal.get("gap") not in want:
            continue
        d = seal.get("adopt_decision")
        if d not in ADOPT_DECISIONS:
            missing.append(sid)
    return missing


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
        seals.append({
            "id": sid,
            "gap": seal.get("gap"),
            "path": path,
            "provider": seal.get("provider"),
            "adopt_decision": seal.get("adopt_decision"),
            "human_form_submitted": (seal.get("coverage") or {}).get("human_form_submitted"),
        })
    total = sum(v for k, v in counts.items() if k != "unknown") + counts["unknown"]
    auto = counts[AUTO] + counts[CODE]  # code counts as covered auto-path
    exception_queue = [
        gid for gid, g in (graph.get("gaps") or {}).items()
        if g.get("status") == "open" and g.get("escalated")
    ]
    hf_pending = human_form_pending(graph)
    ps_fail = primary_source_failures(graph)
    return {
        "counts": counts,
        "total_seals": total,
        "auto_or_code": auto,
        "human": counts[HUMAN],
        "escalate_open": exception_queue,
        "human_form_pending": hf_pending,
        "primary_source_failures": ps_fail,
        "auto_rate": (auto / total) if total else 0.0,
        "destroys": "accuracy-without-coverage dashboards; mint-as-product",
        "seals": seals,
    }


def meets_policy(
    graph: dict[str, Any],
    policy: dict[str, Any] | None,
    *,
    effect_after: list[str] | None = None,
) -> tuple[bool, list[str]]:
    """Effect unlock helper.

    policy keys: min_auto_rate, require_no_open_escalations, min_seals,
    require_human_form, require_adopt_decision, require_primary_source.

    When require_adopt_decision and effect_after is set, only seals for those
    gaps must carry adopt_decision (preferred for effect.after gating).
    """
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
    if policy.get("require_human_form") and led["human_form_pending"]:
        failures.append(f"human_form_pending: {led['human_form_pending']}")
    if policy.get("require_adopt_decision"):
        miss = adopt_decision_missing(graph, gap_ids=effect_after)
        if miss:
            failures.append(f"adopt_decision_missing: {miss}")
    if policy.get("require_primary_source") and led["primary_source_failures"]:
        failures.append(f"primary_source_missing: {led['primary_source_failures']}")
    return (not failures), failures
