from __future__ import annotations
import tempfile
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from seal.graph import init_workspace, load

class TestInit(unittest.TestCase):
    def test_init_writes_graph(self):
        with tempfile.TemporaryDirectory() as d:
            r = init_workspace(Path(d), "p", "idea", "edtech.foundation")
            self.assertTrue(r["ok"])
            g = load(Path(d) / "graph.json")
            self.assertEqual(g["product"]["id"], "p")
            self.assertTrue((Path(d) / "README.md").exists())

if __name__ == "__main__":
    unittest.main()
