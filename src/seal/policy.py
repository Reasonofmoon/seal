from __future__ import annotations
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
_POLICY = json.loads((ROOT / "schemas" / "lock-policy.json").read_text(encoding="utf-8"))

def band(risk: str) -> dict[str, Any]:
    return dict(_POLICY["bands"][risk])

def coverage_defaults() -> dict[str, Any]:
    return dict((_POLICY.get("coverage") or {}).get("effect_default") or {})

def provider_allowed(risk: str, provider: str) -> tuple[bool, str]:
    """Mint policy. Deterministic code and human seals are always admissible.

    Developer consensus (Beyond Jev): a correct `if` beats a paid mint;
    trust bands forbid heuristic, not human/code.
    """
    b = band(risk)
    p = provider or ""
    if p.startswith("code:") or p == "code":
        return True, "ok"
    if p.startswith("human:") or p == "human":
        return True, "ok"
    if p.startswith("heuristic") and not b.get("heuristic_ok", False):
        return False, f"risk={risk} forbids heuristic mint"
    if b.get("typesafe_required") and not p.startswith("typesafe"):
        return False, f"risk={risk} requires typesafe mint (got {provider})"
    return True, "ok"
