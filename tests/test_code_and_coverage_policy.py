"""code: provider + effect coverage_policy lock_reason."""
from __future__ import annotations
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from seal.graph import (
    open_product, add_candidate, try_seal, project, compile_questions,
    mark_escalated, refresh_effects, status,
)
from seal.mint_heuristic import mint
from seal.policy import provider_allowed

JTBD = "gap.edtech.jtbd.core_job"


class TestCodeHumanProviders(unittest.TestCase):
    def test_code_allowed_on_user_trust(self):
        ok, _ = provider_allowed("user_trust", "code:lint")
        self.assertTrue(ok)
        ok, _ = provider_allowed("user_trust", "human:reviewer")
        self.assertTrue(ok)
        ok, _ = provider_allowed("user_trust", "heuristic:v0")
        self.assertFalse(ok)

    def test_seal_code_path(self):
        g = open_product("code-demo", "x", "edtech.foundation")
        cid = add_candidate(g, JTBD, {"ok": True, "check": "unit"}, by="code")
        r = try_seal(g, JTBD, cid, {}, "code:unit")
        self.assertTrue(r["ok"], r)
        self.assertEqual(r["seal"]["coverage"]["path"], "code")

    def test_effect_locked_while_escalated(self):
        g = open_product("esc-fx", "habit", "edtech.foundation")
        # seal all foundation gaps quickly with heuristic where allowed
        order = [
            (JTBD, "부모가 잔소리 없이 아이가 매일 영어 책을 읽게 되는 일"),
            ("gap.edtech.persona.primary", {"who": "학부모", "context": "저녁", "constraint": "스크린타임"}),
            ("gap.edtech.vision.one_liner", "잔소리 없이 영어 읽기가 하루의 기본이 된다"),
            ("gap.edtech.constraints.non_negotiables", ["아동 개인정보 최소", "한국어 UI", "부모 동의"]),
        ]
        for gid, val in order:
            cid = add_candidate(g, gid, val)
            ans = mint(project(g, gid, cid), compile_questions(g["gaps"][gid]))
            r = try_seal(g, gid, cid, ans, "heuristic:v0")
            self.assertTrue(r["ok"], (gid, r))
        # ethics needs typesafe — leave open and escalate another? escalate an open gap
        # Mark ethics escalated; emit_context still needs ethics sealed so stays locked for gaps
        # Instead: escalate after sealing via marking a fake — use escalate on sealed? only open matters
        # Seal ethics with human provider
        cid = add_candidate(g, "gap.edtech.ethics.dark_pattern_ban",
                            ["출석 벌점 금지", "가짜 마감 금지", "부모 우회 결제 금지", "허위 완료 금지"])
        r = try_seal(g, "gap.edtech.ethics.dark_pattern_ban", cid, {}, "human:editor")
        self.assertTrue(r["ok"], r)
        # Now open a new escalation on a sealed product by escalating a new attached gap — simpler:
        # reopen policy: mark_escalated only works on existing gaps; add escalate before effect by
        # temporarily setting an open escalated flag via a dummy — use mark on ethics after unseal? 
        # Create open escalation: attach isn't needed — mark_escalated requires gap in graph.
        # Add open gap by mutating: open a synthetic gap
        g["gaps"]["gap.tmp.escalation"] = {"id": "gap.tmp.escalation", "status": "open", "ask": "tmp", "risk": "read", "requires": [], "accept": []}
        mark_escalated(g, "gap.tmp.escalation", "review")
        refresh_effects(g)
        eff = g["effects"]["effect.emit_context"]
        self.assertEqual(eff["status"], "locked")
        self.assertTrue(any("escalat" in str(x).lower() or "gap.tmp" in str(x) for x in (eff.get("lock_reason") or [])))
        # clear escalation by sealing the tmp gap with code
        cid = add_candidate(g, "gap.tmp.escalation", {"ok": True})
        try_seal(g, "gap.tmp.escalation", cid, {}, "code:clear")
        refresh_effects(g)
        self.assertEqual(g["effects"]["effect.emit_context"]["status"], "ready")


if __name__ == "__main__":
    unittest.main()
