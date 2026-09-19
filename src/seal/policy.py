from __future__ import annotations
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
_POLICY = json.loads((ROOT / "schemas" / "lock-policy.json").read_text(encoding="utf-8"))

def band(risk: str) -> dict[str, Any]:
    return dict(_POLICY["bands"][risk])

def provider_allowed(risk: str, provider: str) -> tuple[bool, str]:
    b = band(risk)
    if provider.startswith("heuristic") and not b.get("heuristic_ok", False):
        return False, f"risk={risk} forbids heuristic mint"
    if b.get("typesafe_required") and not provider.startswith("typesafe"):
        return False, f"risk={risk} requires typesafe mint (got {provider})"
    return True, "ok"
