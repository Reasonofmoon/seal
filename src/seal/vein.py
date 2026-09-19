"""Vein — learn ONLY from sealed transitions.

Destroys App Factory Hebbian-on-module-prompts:
- No weight updates from generative module chains
- No weight updates from failed strikes alone as "path success"
- Edges are gap_id => gap_id (or :start => first gap)
- Suggest next open gaps by incoming weight from currently sealed set
"""
from __future__ import annotations
from typing import Any

LEARNING_RATE = 0.25
FAIL_DECAY = 0.85
DEFAULT_W = 0.5

def _edge(frm: str, to: str) -> str:
    return f"{frm}=>{to}"

def _ensure(vein: dict[str, Any], key: str) -> dict[str, Any]:
    if key not in vein:
        vein[key] = {"weight": DEFAULT_W, "success": 0, "fail": 0}
    return vein[key]

def record_success(graph: dict[str, Any], sealed_gap: str) -> list[str]:
    """Call after a Gap is sealed. Boost edges from prior sealed gaps / :start."""
    vein = graph.setdefault("vein", {})
    updated = []
    sealed_before = [
        gid for gid, g in graph["gaps"].items()
        if g.get("status") == "sealed" and gid != sealed_gap
    ]
    # Prefer explicit requires as parents; else all previously sealed; else :start
    requires = list(graph["gaps"][sealed_gap].get("requires") or [])
    parents = [r for r in requires if r in sealed_before] or sealed_before
    if not parents:
        parents = [":start"]
    for frm in parents:
        key = _edge(frm, sealed_gap)
        e = _ensure(vein, key)
        e["weight"] = e["weight"] + LEARNING_RATE * (1.0 - e["weight"])
        e["success"] = int(e.get("success", 0)) + 1
        updated.append(key)
    graph.setdefault("journal", []).append({
        "op": "vein_success",
        "gap": sealed_gap,
        "edges": updated,
    })
    return updated

def record_fail(graph: dict[str, Any], failed_gap: str) -> list[str]:
    """Decay edges into a gap that failed a strike (candidate rejected by lock)."""
    vein = graph.setdefault("vein", {})
    updated = []
    sealed = [gid for gid, g in graph["gaps"].items() if g.get("status") == "sealed"]
    parents = list(graph["gaps"][failed_gap].get("requires") or []) or sealed or [":start"]
    for frm in parents:
        key = _edge(frm, failed_gap)
        if key not in vein and frm == ":start":
            _ensure(vein, key)
        if key not in vein:
            continue
        e = vein[key]
        e["weight"] = float(e["weight"]) * FAIL_DECAY
        e["fail"] = int(e.get("fail", 0)) + 1
        updated.append(key)
    if updated:
        graph.setdefault("journal", []).append({
            "op": "vein_fail",
            "gap": failed_gap,
            "edges": updated,
        })
    return updated

def suggest_next(graph: dict[str, Any], limit: int = 5) -> list[dict[str, Any]]:
    """Rank open, unblocked gaps by Vein weight from sealed parents."""
    vein = graph.get("vein") or {}
    sealed = {gid for gid, g in graph["gaps"].items() if g.get("status") == "sealed"}
    open_ids = [gid for gid, g in graph["gaps"].items() if g.get("status") == "open"]
    ranked = []
    for gid in open_ids:
        miss = [r for r in (graph["gaps"][gid].get("requires") or []) if r not in sealed]
        if miss:
            continue  # blocked
        parents = list(graph["gaps"][gid].get("requires") or []) or list(sealed) or [":start"]
        scores = []
        for frm in parents:
            key = _edge(frm, gid)
            if key in vein:
                scores.append(float(vein[key]["weight"]))
            elif frm == ":start":
                scores.append(DEFAULT_W * 0.5)
        score = max(scores) if scores else 0.1
        ranked.append({
            "gap": gid,
            "score": round(score, 4),
            "ask": graph["gaps"][gid].get("ask", ""),
            "risk": graph["gaps"][gid].get("risk"),
        })
    ranked.sort(key=lambda x: (-x["score"], x["gap"]))
    return ranked[:limit]

def snapshot(graph: dict[str, Any]) -> dict[str, Any]:
    vein = graph.get("vein") or {}
    edges = sorted(
        (
            {"edge": k, "weight": round(float(v["weight"]), 4), "success": v.get("success", 0), "fail": v.get("fail", 0)}
            for k, v in vein.items()
        ),
        key=lambda e: -e["weight"],
    )
    return {"edges": edges, "count": len(edges), "destroys": "app-factory hebbian_engine on module prompts"}
