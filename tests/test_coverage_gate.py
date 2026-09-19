"""Coverage Gate — beyond Jev accuracy-without-coverage."""
from __future__ import annotations
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from seal.graph import open_product, add_candidate, try_seal, project, compile_questions, status, mark_escalated
from seal.mint_heuristic import mint
from seal.coverage import ledger, meets_policy

JTBD = "gap.edtech.jtbd.core_job"


class TestCoverageGate(unittest.TestCase):
    def test_seal_stamps_auto_path(self):
        g = open_product("cov", "habit", "edtech.foundation")
        cid = add_candidate(g, JTBD, "부모가 잔소리 없이 아이가 매일 영어 책을 읽게 되는 일")
        answers = mint(project(g, JTBD, cid), compile_questions(g["gaps"][JTBD]))
        r = try_seal(g, JTBD, cid, answers, "heuristic:v0")
        self.assertTrue(r["ok"], r)
        self.assertEqual(r["seal"]["coverage"]["path"], "auto")
        led = ledger(g)
        self.assertGreaterEqual(led["auto_or_code"], 1)
        self.assertIn("coverage", status(g))

    def test_escalate_shows_in_ledger(self):
        g = open_product("esc", "habit", "edtech.foundation")
        mark_escalated(g, JTBD, "low confidence mint")
        led = ledger(g)
        self.assertIn(JTBD, led["escalate_open"])
        ok, fails = meets_policy(g, {"require_no_open_escalations": True})
        self.assertFalse(ok)
        self.assertTrue(fails)


if __name__ == "__main__":
    unittest.main()
