"""S7 — SEAL UKDL subset dump/parse; ban L3–L5 executors."""
from __future__ import annotations
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from seal.graph import open_product, add_candidate, try_seal, project, compile_questions, load
from seal.mint_heuristic import mint
from seal.ukdl_subset import dump, parse, validate_text, UkdlSubsetError, ALLOWED, BANNED

JTBD = "gap.edtech.jtbd.core_job"


class TestUkdlSubset(unittest.TestCase):
    def test_allowed_and_banned_sets(self):
        self.assertIn("gap", ALLOWED)
        self.assertIn("action", BANNED)
        self.assertIn("pipeline", BANNED)
        self.assertIn("quantum", BANNED)

    def test_reject_action_pipeline_quantum(self):
        bad = """
:: meta id=meta:x
@product: "x"
::
:: action id=act:evil agent=bot
@tool: "rm"
::
"""
        with self.assertRaises(UkdlSubsetError) as cm:
            parse(bad)
        self.assertIn("action", str(cm.exception))
        v = validate_text(bad)
        self.assertFalse(v["ok"])
        self.assertIn("action", v["banned"])

    def test_reject_quantum(self):
        bad = """
:: quantum id=qst:level
@states: {"a": 1}
::
"""
        self.assertRaises(UkdlSubsetError, parse, bad)

    def test_roundtrip_gaps_and_seal(self):
        g = open_product("s7-rt", "roundtrip", "edtech.foundation")
        cid = add_candidate(g, JTBD, "부모 잔소리 없이 매일 영어 독서 습관을 유지하는 일")
        answers = mint(project(g, JTBD, cid), compile_questions(g["gaps"][JTBD]))
        r = try_seal(g, JTBD, cid, answers, "heuristic:v0")
        self.assertTrue(r.get("ok"), r)
        text = dump(g)
        self.assertIn(":: gap id=", text)
        self.assertIn(":: seal id=", text)
        self.assertIn(":: candidate id=", text)
        self.assertNotIn(":: action ", text)
        partial = parse(text)
        self.assertEqual(partial["product"]["id"], "s7-rt")
        self.assertIn(JTBD, partial["gaps"])
        self.assertEqual(partial["gaps"][JTBD]["status"], "sealed")
        self.assertTrue(partial["seals"])
        self.assertTrue(partial["candidates"])

    def test_dump_example_readmaster(self):
        path = Path(__file__).resolve().parents[1] / "examples/readmaster-habit/graph.json"
        if not path.exists():
            self.skipTest("no example")
        g = load(path)
        text = dump(g)
        v = validate_text(text)
        self.assertTrue(v["ok"], v)
        self.assertGreater(v["node_count"], 5)
        partial = parse(text)
        self.assertEqual(partial["product"]["id"], "readmaster-habit")
        self.assertEqual(len(partial["gaps"]), 5)


if __name__ == "__main__":
    unittest.main()
