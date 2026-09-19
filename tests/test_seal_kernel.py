import json, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from seal.graph import open_product, add_candidate, try_seal, project, compile_questions, status
from seal.mint_heuristic import mint

class SealKernelTest(unittest.TestCase):
    def test_open_pack_five_gaps(self):
        g = open_product("t", "idea", "edtech.foundation")
        self.assertEqual(len(g["gaps"]), 5)
        self.assertEqual(status(g)["open"], ["gap.edtech.jtbd.core_job"])

    def test_seal_jtbd_outcome(self):
        g = open_product("t", "한국 어린이 영어 독서", "edtech.foundation")
        cid = add_candidate(g, "gap.edtech.jtbd.core_job", "부모 잔소리 없이 매일 영어 독서 습관을 유지하는 일")
        state = project(g, "gap.edtech.jtbd.core_job", cid)
        answers = mint(state, compile_questions(g["gaps"]["gap.edtech.jtbd.core_job"]))
        r = try_seal(g, "gap.edtech.jtbd.core_job", cid, answers, "heuristic:v0")
        self.assertTrue(r["ok"], r)

    def test_reject_solution_framed(self):
        g = open_product("t", "idea", "edtech.foundation")
        cid = add_candidate(g, "gap.edtech.jtbd.core_job", "게이미피케이션 퀴즈 앱을 만들어 스트릭 기능을 넣는다")
        state = project(g, "gap.edtech.jtbd.core_job", cid)
        answers = mint(state, compile_questions(g["gaps"]["gap.edtech.jtbd.core_job"]))
        r = try_seal(g, "gap.edtech.jtbd.core_job", cid, answers, "heuristic:v0")
        self.assertFalse(r["ok"])
        self.assertEqual(r["kind"], "lock")

    def test_user_trust_blocks_heuristic(self):
        g = open_product("t", "idea", "edtech.foundation")
        # manually mark prerequisites sealed for unit focus
        for gid in [
            "gap.edtech.jtbd.core_job",
            "gap.edtech.persona.primary",
            "gap.edtech.vision.one_liner",
            "gap.edtech.constraints.non_negotiables",
        ]:
            g["gaps"][gid]["status"] = "sealed"
            g["gaps"][gid]["sealed_by"] = "seal.fake"
        cid = add_candidate(g, "gap.edtech.ethics.dark_pattern_ban", ["a", "b", "c", "d"])
        r = try_seal(g, "gap.edtech.ethics.dark_pattern_ban", cid, {}, "heuristic:v0")
        self.assertFalse(r["ok"])
        self.assertEqual(r["kind"], "provider_policy")

    def test_requires_blocks_fill(self):
        g = open_product("t", "idea", "edtech.foundation")
        with self.assertRaises(RuntimeError):
            add_candidate(g, "gap.edtech.persona.primary", {"who": "x", "context": "y", "constraint": "z"})

if __name__ == "__main__":
    unittest.main()
