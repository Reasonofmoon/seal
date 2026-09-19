"""S8 Gap Board — model + HTML; no module parade."""
from __future__ import annotations
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from seal.graph import open_product, load
from seal.board import board_model, render_html, write_board

JTBD = "gap.edtech.jtbd.core_job"


class TestGapBoard(unittest.TestCase):
    def test_open_pack_recommends_jtbd(self):
        g = open_product("board-open", "habit", "edtech.foundation")
        m = board_model(g)
        self.assertEqual(m["counts"]["open"], 1)
        self.assertGreater(m["counts"]["blocked"], 0)
        self.assertTrue(any(c["id"] == JTBD and c["recommended"] for c in m["gaps"]))
        self.assertIn("module parade", m["destroys"])

    def test_html_has_no_ship_module_copy(self):
        g = open_product("board-html", "x", "edtech.foundation")
        html = render_html(g, embed_ukdl=False)
        self.assertIn("SEAL Gap Board", html)
        self.assertIn("Not a module studio", html)
        self.assertNotIn("builder-mini", html)
        self.assertNotIn("app-factory ship", html)
        self.assertIn(JTBD, html)

    def test_write_readmaster_example(self):
        path = Path(__file__).resolve().parents[1] / "examples/readmaster-habit/graph.json"
        if not path.exists():
            self.skipTest("no example")
        g = load(path)
        out = Path(__file__).resolve().parents[1] / "examples/readmaster-habit/board.html"
        write_board(g, out)
        self.assertTrue(out.exists())
        m = board_model(g)
        self.assertEqual(m["counts"]["sealed"], 5)
        self.assertEqual(m["counts"]["open"], 0)


if __name__ == "__main__":
    unittest.main()
