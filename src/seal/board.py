"""Gap Board — S8 UI model + HTML (destroys App Factory Studio module parade)."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

from .graph import status
from .vein import suggest_next, snapshot
from .ukdl_subset import dump as ukdl_dump
from .coverage import ledger as snapshot_coverage

RISK_ORDER = {"read": 0, "product_foundation": 1, "user_trust": 2, "irreversible": 3}
_TEMPLATE = Path(__file__).resolve().parent / "static" / "gap-board.html"


def board_model(graph: dict[str, Any]) -> dict[str, Any]:
    st = status(graph)
    blocked_map = {b["gap"]: b for b in st.get("blocked") or []}
    next_scores = {n["gap"]: n for n in (st.get("next") or suggest_next(graph))}
    cards = []
    for gid, gap in (graph.get("gaps") or {}).items():
        state = gap.get("status") or "open"
        if state == "open" and gid in blocked_map:
            state = "blocked"
        cards.append({
            "id": gid,
            "ask": gap.get("ask", ""),
            "risk": gap.get("risk", "read"),
            "status": state,
            "requires": gap.get("requires") or [],
            "sealed_by": gap.get("sealed_by"),
            "missing": (blocked_map.get(gid) or {}).get("missing") or [],
            "vein_score": (next_scores.get(gid) or {}).get("score"),
            "recommended": gid in next_scores and state == "open",
        })

    def sort_key(c):
        pri = {"open": 0, "blocked": 1, "sealed": 2}.get(c["status"], 9)
        if c["recommended"]:
            pri = -1
        return (pri, -(c["vein_score"] or 0), RISK_ORDER.get(c["risk"], 9), c["id"])

    cards.sort(key=sort_key)
    effects = []
    for eid, eff in (graph.get("effects") or {}).items():
        effects.append({
            "id": eid,
            "status": eff.get("status", "locked"),
            "run": eff.get("run"),
            "after": eff.get("after"),
            "after_effects": eff.get("after_effects"),
            "risk": eff.get("risk"),
        })
    effects.sort(key=lambda e: ({"ready": 0, "done": 1, "locked": 2}.get(e["status"], 9), e["id"]))
    product = graph.get("product") or {}
    return {
        "title": "SEAL Gap Board",
        "destroys": "app-factory studio module parade / ship tiers",
        "product": {
            "id": product.get("id") or st.get("product"),
            "idea": product.get("idea", ""),
            "pack": product.get("pack", ""),
            "pack_version": product.get("pack_version"),
        },
        "counts": {
            "open": len([c for c in cards if c["status"] == "open"]),
            "blocked": len([c for c in cards if c["status"] == "blocked"]),
            "sealed": len([c for c in cards if c["status"] == "sealed"]),
            "candidates": st.get("candidates", 0),
            "seals": st.get("seals", 0),
        },
        "next": st.get("next") or [],
        "gaps": cards,
        "effects": effects,
        "vein": snapshot(graph),
        "seal_version": graph.get("seal_version", "0.1.0"),
        "coverage": snapshot_coverage(graph),
        "evidence": list((graph.get("evidence") or {}).values())[:20],
    }


def render_html(graph: dict[str, Any], *, embed_ukdl: bool = True) -> str:
    model = board_model(graph)
    tpl = _TEMPLATE.read_text(encoding="utf-8")
    ukdl = ukdl_dump(graph) if embed_ukdl else ""
    return (
        tpl.replace("__BOARD_JSON__", json.dumps(model, ensure_ascii=False))
        .replace("__UKDL_JSON__", json.dumps(ukdl, ensure_ascii=False))
    )


def write_board(graph: dict[str, Any], out: Path, *, embed_ukdl: bool = True) -> Path:
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_html(graph, embed_ukdl=embed_ukdl), encoding="utf-8")
    return out
