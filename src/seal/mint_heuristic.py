"""Uncalibrated mint for product_foundation demos. Tattoo provider=heuristic on seals.
Never use for user_trust / irreversible.
"""
from __future__ import annotations
import re
from typing import Any

SOLUTION_HINTS = re.compile(
    r"(앱|앱을|만들|개발|구현|퀴즈|게이미|스트릭|AI\s*튜터|대시보드|기능)",
    re.I,
)
OUTCOME_HINTS = re.compile(
    r"(습관|유지|도움|고용|해내|할\s*수|없이|매일|독서|학습|성장|독립)",
    re.I,
)

def _text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(map(str, value))
    if isinstance(value, dict):
        return "\n".join(f"{k}: {v}" for k, v in value.items())
    return str(value)

def mint(state: dict[str, Any], questions: dict[str, Any]) -> dict[str, Any]:
    proposal = _text(state.get("proposal", {}).get("value", ""))
    idea = _text(state.get("product", {}).get("idea", ""))
    answers: dict[str, Any] = {}
    for qid, q in questions.items():
        t = q["type"]
        if t == "noul":
            answers[qid] = {"noul": _noul(qid, proposal, idea, q)}
        elif t == "choice":
            answers[qid] = _choice(qid, proposal, q)
        elif t == "score":
            answers[qid] = _score(qid, proposal, q)
    return answers

def _noul(qid: str, proposal: str, idea: str, q: dict[str, Any]) -> float:
    pl = proposal.lower()
    if qid in ("supports_evidence",):
        if SOLUTION_HINTS.search(proposal) and not OUTCOME_HINTS.search(proposal):
            return 0.25
        if OUTCOME_HINTS.search(proposal) and len(proposal) >= 20:
            return 0.82
        return 0.45
    if qid == "persona_concrete":
        need = ("who", "constraint")
        # object serialized in text
        hits = sum(1 for k in ("학부모", "아이", "학생", "교사", "자녀", "부모") if k in proposal)
        return 0.78 if hits >= 1 and len(proposal) > 30 else 0.4
    if qid == "aligned_to_jtbd":
        return 0.8 if len(proposal) >= 16 else 0.3
    if qid == "metric_honesty":
        if re.search(r"\d+\s*%|LIVE|보장|무조건", proposal):
            return 0.2
        return 0.88
    if qid == "constraints_actionable":
        return 0.75 if proposal.count("\n") >= 1 or "," in proposal or len(proposal) > 40 else 0.4
    if qid == "child_safety_present":
        if re.search(r"아동|프라이버시|개인정보|COPPA|보호|안전", proposal):
            return 0.85
        return 0.35
    if qid == "bans_specific":
        lines = [ln for ln in re.split(r"[\n,]", proposal) if ln.strip()]
        return 0.85 if len(lines) >= 3 else 0.4
    if qid == "has_repo":
        if re.search(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", proposal) or "github.com/" in pl:
            return 0.92
        return 0.2
    if qid == "verdict_grounded":
        if re.search(r"\b(pass|fail|n/a)\b", pl) and len(proposal) >= 80:
            return 0.88
        return 0.35
    if qid in ("has_source", "has_three_modes", "honest_fallback", "autorun_or_button",
               "reference_label", "not_official", "no_fake_certainty", "heuristic_fallback",
               "bans_official_rank", "bans_guarantee", "clean_of_forbidden", "checklist_present"):
        return 0.8 if len(proposal) >= 40 else 0.4
    # default soft mid
    return 0.55

def _choice(qid: str, proposal: str, q: dict[str, Any]) -> dict[str, Any]:
    crit = list((q.get("criteria") or {}).keys())
    if qid == "form":
        if SOLUTION_HINTS.search(proposal) and not OUTCOME_HINTS.search(proposal):
            return {"choice": "solution_framed", "confidence": 0.7, "probabilities": {"solution_framed": 0.7, "outcome_framed": 0.2, "vague": 0.1}}
        if OUTCOME_HINTS.search(proposal):
            return {"choice": "outcome_framed", "confidence": 0.72, "probabilities": {"outcome_framed": 0.72, "solution_framed": 0.18, "vague": 0.1}}
        return {"choice": "vague", "confidence": 0.5, "probabilities": {"vague": 0.5, "outcome_framed": 0.3, "solution_framed": 0.2}}
    if qid == "buyer_user_clarity":
        if "부모" in proposal or "학부모" in proposal:
            ch = "parent_buyer"
        elif "교사" in proposal:
            ch = "teacher"
        elif "아이" in proposal or "학생" in proposal or "아동" in proposal:
            ch = "learner"
        else:
            ch = "muddled"
        probs = {k: 0.1 for k in crit}
        probs[ch] = 0.7
        return {"choice": ch, "confidence": 0.65, "probabilities": probs}
    # fallback first criterion
    ch = crit[0] if crit else "other"
    return {"choice": ch, "confidence": 0.4, "probabilities": {ch: 0.4}}

def _score(qid: str, proposal: str, q: dict[str, Any]) -> dict[str, Any]:
    lines = [ln for ln in re.split(r"[\n,;/]", proposal) if ln.strip()]
    if len(lines) >= 3 and re.search(r"강요|속임|우회|가짜|긴급|다크", proposal):
        score, conf = 2.0, 0.7
    elif len(lines) >= 3:
        score, conf = 1.6, 0.6
    else:
        score, conf = 0.8, 0.45
    n = len(q.get("criteria") or [0, 1, 2])
    probs = {str(i): (0.1) for i in range(n)}
    idx = min(int(round(score)), n - 1)
    probs[str(idx)] = conf
    return {"score": score, "confidence": conf, "probabilities": probs, "legend": list(range(n))}
