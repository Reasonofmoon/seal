"""S6 Vein — learn only on sealed transitions; rank next gaps."""
from __future__ import annotations
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from seal.graph import open_product, add_candidate, try_seal, project, compile_questions, status
from seal.mint_heuristic import mint
from seal.vein import record_success, record_fail, suggest_next, snapshot

JTBD = "gap.edtech.jtbd.core_job"
PERSONA = "gap.edtech.persona.primary"


class TestVein(unittest.TestCase):
    def test_success_boosts_start_edge(self):
        g = open_product("vein-demo", "demo", "edtech.foundation")
        g["gaps"][JTBD]["status"] = "sealed"
        g["seals"]["seal_fake"] = {"id": "seal_fake", "gap": JTBD}
        record_success(g, JTBD)
        key = f":start=>{JTBD}"
        self.assertIn(key, g["vein"])
        w0 = g["vein"][key]["weight"]
        self.assertGreater(w0, 0.5)
        record_success(g, JTBD)
        self.assertGreater(g["vein"][key]["weight"], w0)

    def test_fail_decays_existing_edge(self):
        g = open_product("vein-fail", "demo", "edtech.foundation")
        key = f":start=>{JTBD}"
        g["vein"] = {key: {"weight": 0.8, "success": 2, "fail": 0}}
        updated = record_fail(g, JTBD)
        self.assertIn(key, updated)
        self.assertLess(g["vein"][key]["weight"], 0.8)

    def test_suggest_prefers_heavier_edge(self):
        g = open_product("vein-rank", "demo", "edtech.foundation")
        g["vein"] = {
            f":start=>{JTBD}": {"weight": 0.9, "success": 3, "fail": 0},
        }
        nxt = suggest_next(g, limit=5)
        self.assertTrue(nxt)
        ready = [x["gap"] for x in nxt]
        self.assertIn(JTBD, ready)
        jtbd = next(x for x in nxt if x["gap"] == JTBD)
        self.assertGreaterEqual(jtbd["score"], 0.8)

    def test_no_learning_without_seal_or_fail(self):
        g = open_product("vein-cold", "demo", "edtech.foundation")
        self.assertEqual(g.get("vein") or {}, {})
        snap = snapshot(g)
        self.assertEqual(snap["count"], 0)
        self.assertIn("hebbian", snap["destroys"])


class TestVeinIntegration(unittest.TestCase):
    def test_heuristic_seal_updates_vein_and_status_next(self):
        g = open_product("vein-int", "habit app", "edtech.foundation")
        cid = add_candidate(g, JTBD, "부모 잔소리 없이 매일 영어 독서 습관을 유지하는 일")
        state = project(g, JTBD, cid)
        answers = mint(state, compile_questions(g["gaps"][JTBD]))
        r = try_seal(g, JTBD, cid, answers, "heuristic:v0")
        self.assertTrue(r.get("ok"), r)
        self.assertTrue(g.get("vein"))
        self.assertIn(f":start=>{JTBD}", g["vein"])
        st = status(g)
        self.assertIn("next", st)
        self.assertIsInstance(st["next"], list)
        self.assertNotIn(JTBD, [x["gap"] for x in st["next"]])
        # persona should become suggestable after jtbd sealed
        next_ids = [x["gap"] for x in st["next"]]
        self.assertIn(PERSONA, next_ids)


if __name__ == "__main__":
    unittest.main()
