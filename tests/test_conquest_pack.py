import json, sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from seal.graph import open_product, load_pack, status

class ConquestPackTest(unittest.TestCase):
    def test_pack_has_corpus_and_13_rubrics(self):
        pack, gaps, effects = load_pack("conquest.audit-spec")
        self.assertEqual(pack["id"], "conquest.audit-spec")
        self.assertEqual(len(pack["gaps"]), 14)
        self.assertIn("gap.af.spec.corpus", gaps)
        rubrics = [g for g in gaps if g.startswith("gap.af.rubric.R")]
        self.assertEqual(len(rubrics), 13)
        self.assertIn("effect.aplus_implement_unlock", effects)

    def test_open_blocks_rubrics_until_corpus(self):
        g = open_product("t", "idea", "conquest.audit-spec")
        st = status(g)
        self.assertEqual(st["open"], ["gap.af.spec.corpus"])
        self.assertTrue(any(b["gap"].startswith("gap.af.rubric.") for b in st["blocked"]))
        self.assertEqual(st["effects"]["effect.aplus_implement_unlock"], "locked")

if __name__ == "__main__":
    unittest.main()
