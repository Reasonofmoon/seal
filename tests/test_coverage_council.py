"""Council 2026-09-19 — human_form / adopt_decision / primary_source policies."""
from __future__ import annotations
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from seal.graph import (
    open_product, add_candidate, try_seal, mark_escalated, refresh_effects,
    set_adopt, stamp_gap_human_form, mark_primary_source_missing, attach_pack,
)
from seal.coverage import meets_policy, ledger, stamp_human_form, human_form_pending


JTBD = "gap.edtech.jtbd.core_job"


class TestCoverageCouncil(unittest.TestCase):
    def test_human_form_lock(self):
        g = open_product("hf", "habit", "edtech.foundation")
        g["gaps"][JTBD]["human_form_required"] = True
        cid = add_candidate(g, JTBD, {"ok": True}, by="code")
        r = try_seal(g, JTBD, cid, {}, "code:unit")
        self.assertTrue(r["ok"], r)
        self.assertFalse(r["seal"]["coverage"].get("human_form_submitted"))
        self.assertIn("suggest", r)
        self.assertIn(JTBD, human_form_pending(g))
        ok, fails = meets_policy(g, {"require_human_form": True})
        self.assertFalse(ok)
        self.assertTrue(any("human_form" in f for f in fails))

        # submit form → pending clears on stamp
        stamp_gap_human_form(g, JTBD, True)
        self.assertNotIn(JTBD, human_form_pending(g))
        ok2, _ = meets_policy(g, {"require_human_form": True})
        self.assertTrue(ok2)

    def test_human_form_submitted_via_answers(self):
        g = open_product("hf2", "habit", "edtech.foundation")
        g["gaps"][JTBD]["human_form_required"] = True
        cid = add_candidate(g, JTBD, {"ok": True}, by="code")
        r = try_seal(g, JTBD, cid, {"human_form_submitted": True}, "code:unit")
        self.assertTrue(r["ok"], r)
        self.assertTrue(r["seal"]["coverage"]["human_form_submitted"])
        self.assertEqual(human_form_pending(g), [])

    def test_adopt_decision_policy(self):
        g = open_product("ad", "habit", "edtech.foundation")
        cid = add_candidate(g, JTBD, {"ok": True}, by="code")
        r = try_seal(g, JTBD, cid, {}, "code:unit")
        self.assertTrue(r["ok"], r)
        sid = r["seal"]["id"]
        ok, fails = meets_policy(
            g, {"require_adopt_decision": True}, effect_after=[JTBD]
        )
        self.assertFalse(ok)
        self.assertTrue(any("adopt_decision" in f for f in fails))

        set_adopt(g, sid, "adopt")
        ok2, fails2 = meets_policy(
            g, {"require_adopt_decision": True}, effect_after=[JTBD]
        )
        self.assertTrue(ok2, fails2)
        self.assertEqual(g["seals"][sid]["adopt_decision"], "adopt")

        bad = set_adopt(g, sid, "maybe")
        self.assertFalse(bad.get("ok"))

    def test_primary_source_fail(self):
        g = open_product("ps", "habit", "edtech.foundation")
        cid = add_candidate(g, JTBD, {"ok": True}, by="code")
        r = try_seal(
            g, JTBD, cid, {"PRIMARY_SOURCE_NOT_FOUND": True}, "code:unit"
        )
        self.assertTrue(r["ok"], r)
        self.assertTrue(r["seal"].get("primary_source_missing"))
        ok, fails = meets_policy(g, {"require_primary_source": True})
        self.assertFalse(ok)
        self.assertTrue(any("primary_source" in f for f in fails))

        g2 = open_product("ps2", "habit", "edtech.foundation")
        mark_primary_source_missing(g2, JTBD, "no upstream")
        ok3, fails3 = meets_policy(g2, {"require_primary_source": True})
        self.assertFalse(ok3)
        self.assertTrue(fails3)

    def test_stamp_human_form_helper(self):
        seal = {"coverage": {"path": "code"}}
        stamp_human_form(seal, True)
        self.assertTrue(seal["coverage"]["human_form_submitted"])

    def test_fleet_pack_loads(self):
        g = open_product("fleet", "ops", "fleet.coverage")
        self.assertIn("gap.fleet.harness_code_only", g["gaps"])
        self.assertIn("effect.fleet.ops_ready", g["effects"])
        pol = g["effects"]["effect.fleet.ops_ready"]["coverage_policy"]
        self.assertTrue(pol.get("require_adopt_decision"))
        self.assertTrue(pol.get("require_human_form"))
        self.assertTrue(g["gaps"]["gap.fleet.human_form_required"].get("human_form_required"))


if __name__ == "__main__":
    unittest.main()
