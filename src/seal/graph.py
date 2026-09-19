from __future__ import annotations
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .hashutil import sha256_obj
from .policy import band, provider_allowed
from .vein import record_success, record_fail
from .coverage import classify_path, ledger as coverage_ledger, meets_policy

ROOT = Path(__file__).resolve().parents[2]
PACKS = ROOT / "packs"

def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

def load_pack(pack_id: str) -> dict[str, Any]:
    pdir = PACKS / pack_id
    pack = json.loads((pdir / "pack.json").read_text(encoding="utf-8"))
    gaps = {}
    for gid in pack["gaps"]:
        gaps[gid] = json.loads((pdir / "gaps" / f"{gid}.json").read_text(encoding="utf-8"))
        gaps[gid]["status"] = "open"
        gaps[gid]["sealed_by"] = None
    effects = json.loads((pdir / "effects.json").read_text(encoding="utf-8"))
    for e in effects.values():
        e["status"] = "locked"
    return pack, gaps, effects

def open_product(product_id: str, idea: str, pack_id: str = "edtech.foundation", lang: str = "ko") -> dict[str, Any]:
    pack, gaps, effects = load_pack(pack_id)
    g = {
        "seal_version": "0.3.0",
        "product": {
            "id": product_id,
            "idea": idea,
            "pack": pack_id,
            "packs": [pack_id],
            "pack_version": pack["version"],
            "lang": lang,
            "created_at": _now(),
        },
        "gaps": gaps,
        "candidates": {},
        "seals": {},
        "effects": effects,
        "evidence": {},
        "journal": [{"op": "open", "pack": pack_id, "at": _now()}],
        "vein": {},
    }
    return g

def attach_pack(graph: dict[str, Any], pack_id: str) -> dict[str, Any]:
    """Compose another Gap Pack onto an open product (real products need multiple packs)."""
    packs = graph["product"].setdefault("packs", [graph["product"]["pack"]])
    if pack_id in packs:
        return {"ok": False, "error": "pack_already_attached", "pack": pack_id}
    pack, gaps, effects = load_pack(pack_id)
    collisions = set(gaps) & set(graph["gaps"])
    if collisions:
        return {"ok": False, "error": "gap_id_collision", "gaps": sorted(collisions)}
    graph["gaps"].update(gaps)
    for eid, eff in effects.items():
        if eid in graph["effects"]:
            return {"ok": False, "error": "effect_id_collision", "effect": eid}
        graph["effects"][eid] = eff
    packs.append(pack_id)
    graph["product"]["packs"] = packs
    graph["journal"].append({"op": "attach_pack", "pack": pack_id, "at": _now()})
    refresh_effects(graph)
    return {"ok": True, "pack": pack_id, "gaps_added": list(gaps.keys())}

def attach_evidence(
    graph: dict[str, Any],
    *,
    kind: str,
    ref: str,
    note: str = "",
    seal_id: str | None = None,
    gap_id: str | None = None,
) -> str:
    """Record real-world evidence (URL, commit, deploy, screenshot path) on the graph."""
    eid = f"evidence.{len(graph.setdefault('evidence', {}))+1:04d}"
    graph["evidence"][eid] = {
        "id": eid,
        "kind": kind,
        "ref": ref,
        "note": note,
        "seal": seal_id,
        "gap": gap_id,
        "at": _now(),
    }
    if seal_id and seal_id in graph.get("seals", {}):
        graph["seals"][seal_id].setdefault("evidence", []).append(eid)
    graph["journal"].append({"op": "evidence", "id": eid, "at": _now()})
    return eid

def save(graph: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def add_candidate(graph: dict[str, Any], gap_id: str, value: Any, by: str = "human", model: str | None = None) -> str:
    if gap_id not in graph["gaps"]:
        raise KeyError(gap_id)
    if graph["gaps"][gap_id]["status"] == "sealed":
        raise RuntimeError(f"{gap_id} already sealed — no candidate on sealed gap without unseal path")
    for req in graph["gaps"][gap_id].get("requires") or []:
        if graph["gaps"][req]["status"] != "sealed":
            raise RuntimeError(f"{gap_id} blocked: requires sealed {req}")
    cid = f"candidate.{len(graph['candidates'])+1:04d}"
    graph["candidates"][cid] = {
        "id": cid,
        "gap": gap_id,
        "value": value,
        "by": by,
        "model": model,
        "meta": {},
    }
    graph["journal"].append({"op": "candidate", "id": cid, "gap": gap_id, "at": _now()})
    return cid

def sealed_facts(graph: dict[str, Any]) -> dict[str, Any]:
    facts: dict[str, Any] = {}
    for seal in graph["seals"].values():
        if seal.get("deprecated"):
            continue
        gap = graph["gaps"][seal["gap"]]
        cand = graph["candidates"][seal["candidate"]]
        short = seal["gap"].split(".")[-1]
        # friendlier keys
        key = {
            "core_job": "jtbd",
            "primary": "persona",
            "one_liner": "vision",
            "non_negotiables": "constraints",
            "dark_pattern_ban": "ethics_bans",
        }.get(short, short)
        facts[key] = cand["value"]
        facts[seal["gap"]] = cand["value"]
    return facts

def project(graph: dict[str, Any], gap_id: str, candidate_id: str) -> dict[str, Any]:
    gap = graph["gaps"][gap_id]
    cand = graph["candidates"][candidate_id]
    if cand["gap"] != gap_id:
        raise ValueError("candidate/gap mismatch")
    facts = sealed_facts(graph)
    # corpus convenience for rubric strikes
    corpus_seal = None
    for s in graph["seals"].values():
        if s.get("deprecated"):
            continue
        if s["gap"] == "gap.af.spec.corpus":
            corpus_seal = s
            break
    if corpus_seal:
        facts["spec_text"] = graph["candidates"][corpus_seal["candidate"]]["value"]
    if graph["product"].get("known_cli_flags"):
        facts["known_cli_flags"] = graph["product"]["known_cli_flags"]
    return {
        "product": {
            "id": graph["product"]["id"],
            "idea": graph["product"]["idea"],
            "lang": graph["product"].get("lang", "ko"),
            "tier": graph["product"].get("tier"),
        },
        "gap": {"id": gap_id, "ask": gap["ask"], "risk": gap["risk"]},
        "facts": facts,
        "proposal": {"id": candidate_id, "value": cand["value"], "by": cand["by"]},
    }

def compile_questions(gap: dict[str, Any]) -> dict[str, Any]:
    qs = {}
    for rule in gap["accept"]:
        q: dict[str, Any] = {
            "type": rule["type"],
            "instructions": rule["instructions"],
        }
        if "criteria" in rule:
            q["criteria"] = rule["criteria"]
        qs[rule["id"]] = q
    return qs

def evaluate_lock(gap: dict[str, Any], answers: dict[str, Any]) -> tuple[bool, list[str]]:
    failures = []
    for rule in gap["accept"]:
        rid = rule["id"]
        ans = answers.get(rid)
        if ans is None:
            failures.append(f"missing answer {rid}")
            continue
        t = rule["type"]
        if t == "noul":
            v = float(ans.get("noul", 0))
            if "noul_gte" in rule and v < rule["noul_gte"]:
                failures.append(f"{rid}: noul {v:.3f} < {rule['noul_gte']}")
            if "noul_lte" in rule and v > rule["noul_lte"]:
                failures.append(f"{rid}: noul {v:.3f} > {rule['noul_lte']}")
        elif t == "choice":
            ch = ans.get("choice")
            conf = float(ans.get("confidence", 0))
            if "choice_in" in rule and ch not in rule["choice_in"]:
                failures.append(f"{rid}: choice {ch!r} not in {rule['choice_in']}")
            floor = rule.get("confidence_gte", band(gap["risk"]).get("default_confidence_floor", 0))
            if conf < floor:
                failures.append(f"{rid}: confidence {conf:.3f} < {floor}")
        elif t == "score":
            sc = float(ans.get("score", 0))
            conf = float(ans.get("confidence", 0))
            if "score_gte" in rule and sc < rule["score_gte"]:
                failures.append(f"{rid}: score {sc:.3f} < {rule['score_gte']}")
            if "confidence_gte" in rule and conf < rule["confidence_gte"]:
                failures.append(f"{rid}: confidence {conf:.3f} < {rule['confidence_gte']}")
    return (len(failures) == 0, failures)

def refresh_effects(graph: dict[str, Any]) -> None:
    """Unlock when gaps/effects prerequisites hold AND coverage_policy passes.

    Effect may set coverage_policy: {require_no_open_escalations, min_auto_rate, min_seals}.
    Defaults merge from schemas/lock-policy.json → coverage.effect_default.
    """
    from .policy import coverage_defaults
    sealed = {gid for gid, g in graph["gaps"].items() if g["status"] == "sealed"}
    done_effects = {eid for eid, e in graph["effects"].items() if e.get("status") == "done"}
    for eff in graph["effects"].values():
        if eff["status"] == "done":
            continue
        need_gaps = set(eff.get("after") or [])
        need_fx = set(eff.get("after_effects") or [])
        prereq = need_gaps <= sealed and need_fx <= done_effects
        policy = {**coverage_defaults(), **(eff.get("coverage_policy") or {})}
        # Only enforce coverage once gap/effect prereqs are met (otherwise stay locked quietly)
        cov_ok, cov_fail = (True, [])
        if prereq and policy:
            cov_ok, cov_fail = meets_policy(graph, policy)
        if prereq and cov_ok:
            eff["status"] = "ready"
            eff.pop("lock_reason", None)
        else:
            eff["status"] = "locked"
            reasons = []
            if not prereq:
                missing_g = sorted(need_gaps - sealed)
                missing_e = sorted(need_fx - done_effects)
                if missing_g:
                    reasons.append(f"unsealed:{missing_g}")
                if missing_e:
                    reasons.append(f"effects:{missing_e}")
            if prereq and not cov_ok:
                reasons.extend(cov_fail)
            eff["lock_reason"] = reasons

def try_seal(
    graph: dict[str, Any],
    gap_id: str,
    candidate_id: str,
    answers: dict[str, Any],
    provider: str,
    strike_id: str | None = None,
) -> dict[str, Any]:
    gap = graph["gaps"][gap_id]
    ok_p, reason = provider_allowed(gap["risk"], provider)
    if not ok_p:
        return {"ok": False, "error": reason, "kind": "provider_policy"}

    state = project(graph, gap_id, candidate_id)
    questions = compile_questions(gap)
    if provider.startswith("code:") or provider == "code":
        # Deterministic seal: candidate.value must be truthy predicate result or {"ok": true}
        val = graph["candidates"][candidate_id].get("value")
        ok_code = val is True or val == 1 or (isinstance(val, dict) and val.get("ok") is True)
        if not ok_code:
            return {
                "ok": False,
                "error": "code_predicate_false",
                "kind": "code",
                "detail": "code: provider requires candidate.value True or {ok: true}",
            }
        ok, failures = True, []
    elif provider.startswith("human:") or provider == "human":
        # Human coseal: skip mint answers; still require non-empty candidate
        if graph["candidates"][candidate_id].get("value") in (None, "", [], {}):
            return {"ok": False, "error": "empty_human_value", "kind": "human"}
        ok, failures = True, []
    else:
        ok, failures = evaluate_lock(gap, answers)
    if not ok:
        graph["journal"].append({
            "op": "strike_fail",
            "gap": gap_id,
            "candidate": candidate_id,
            "failures": failures,
            "provider": provider,
            "at": _now(),
        })
        record_fail(graph, gap_id)
        return {"ok": False, "error": "lock_failed", "failures": failures, "kind": "lock"}

    sid = f"seal.{len(graph['seals'])+1:04d}"
    cand = graph["candidates"][candidate_id]
    path = classify_path(
        provider=provider,
        answers=answers,
        by=cand.get("by"),
        escalated=bool(gap.get("escalated")),
    )
    seal = {
        "id": sid,
        "gap": gap_id,
        "candidate": candidate_id,
        "strike_id": strike_id or f"strike.{sid}",
        "provider": provider,
        "answers": answers,
        "policy_risk": gap["risk"],
        "state_hash": sha256_obj(state),
        "questions_hash": sha256_obj(questions),
        "coverage": {"path": path},
        "at": _now(),
        "deprecated": False,
        "superseded_by": None,
    }
    graph["seals"][sid] = seal
    gap["status"] = "sealed"
    gap["sealed_by"] = sid
    record_success(graph, gap_id)
    refresh_effects(graph)
    graph["journal"].append({"op": "seal", "id": sid, "gap": gap_id, "at": _now()})
    return {"ok": True, "seal": seal}

def status(graph: dict[str, Any]) -> dict[str, Any]:
    open_gaps = [gid for gid, g in graph["gaps"].items() if g["status"] == "open"]
    blocked = []
    for gid in open_gaps:
        miss = [r for r in (graph["gaps"][gid].get("requires") or []) if graph["gaps"][r]["status"] != "sealed"]
        if miss:
            blocked.append({"gap": gid, "waiting_on": miss})
    from .vein import suggest_next
    open_ready = [g for g in open_gaps if g not in {b["gap"] for b in blocked}]
    return {
        "product": graph["product"]["id"],
        "open": open_ready,
        "blocked": blocked,
        "sealed": [gid for gid, g in graph["gaps"].items() if g["status"] == "sealed"],
        "effects": {eid: e["status"] for eid, e in graph["effects"].items()},
        "effect_locks": {
            eid: e.get("lock_reason")
            for eid, e in graph["effects"].items()
            if e.get("lock_reason")
        },
        "candidates": len(graph["candidates"]),
        "seals": len(graph["seals"]),
        "next": suggest_next(graph, limit=5),
        "coverage": coverage_ledger(graph),
    }


def mark_escalated(graph: dict[str, Any], gap_id: str, reason: str = "") -> None:
    """Open exception-queue entry (developer demand: show coverage, not hide it)."""
    if gap_id not in graph["gaps"]:
        raise KeyError(gap_id)
    graph["gaps"][gap_id]["escalated"] = True
    graph["gaps"][gap_id]["escalate_reason"] = reason
    graph.setdefault("journal", []).append({"op": "escalate", "gap": gap_id, "reason": reason, "at": _now()})


def init_workspace(dir_path: Path, product_id: str, idea: str, pack_id: str = "edtech.foundation") -> dict:
    """Scaffold a local SEAL product folder: graph.json + README stub."""
    dir_path = Path(dir_path)
    dir_path.mkdir(parents=True, exist_ok=True)
    g = open_product(product_id, idea, pack_id)
    save(g, dir_path / "graph.json")
    readme = dir_path / "README.md"
    if not readme.exists():
        readme.write_text(
            f"# {product_id}\n\n"
            f"> SEAL product. Idea: {idea}\n\n"
            f"Pack: `{pack_id}`\n\n"
            f"```bash\n"
            f"PYTHONPATH=../src python3 -m seal.cli status --graph graph.json\n"
            f"PYTHONPATH=../src python3 -m seal.cli board --graph graph.json --out board.html\n"
            f"```\n",
            encoding="utf-8",
        )
    return {"ok": True, "dir": str(dir_path), "graph": str(dir_path / "graph.json"), "status": status(g)}
