import json, sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from seal.graph import open_product, refresh_effects, status

class S5EffectsTest(unittest.TestCase):
    def _seal_all(self, g):
        for i, gid in enumerate(list(g["gaps"])):
            cid = f"c{i}"
            g["candidates"][cid] = {"id": cid, "gap": gid, "value": "x", "by": "t", "model": None, "meta": {}}
            sid = f"s{i}"
            g["seals"][sid] = {
                "id": sid, "gap": gid, "candidate": cid, "provider": "t",
                "answers": {}, "policy_risk": "read", "state_hash": "h", "questions_hash": "h",
                "at": "t", "deprecated": False, "superseded_by": None,
            }
            g["gaps"][gid]["status"] = "sealed"
            g["gaps"][gid]["sealed_by"] = sid

    def test_codegen_locked_until_passport_and_context(self):
        g = open_product("t", "idea", "conquest.audit-spec")
        self._seal_all(g)
        refresh_effects(g)
        self.assertEqual(g["effects"]["effect.aplus_implement_unlock"]["status"], "ready")
        self.assertEqual(g["effects"]["effect.emit_context"]["status"], "locked")
        self.assertEqual(g["effects"]["effect.codegen_vertical_slice"]["status"], "locked")
        g["effects"]["effect.aplus_implement_unlock"]["status"] = "done"
        refresh_effects(g)
        self.assertEqual(g["effects"]["effect.emit_context"]["status"], "ready")
        self.assertEqual(g["effects"]["effect.codegen_vertical_slice"]["status"], "locked")
        g["effects"]["effect.emit_context"]["status"] = "done"
        refresh_effects(g)
        self.assertEqual(g["effects"]["effect.codegen_vertical_slice"]["status"], "ready")

    def test_codegen_blocked_when_open_gaps(self):
        g = open_product("t", "idea", "conquest.audit-spec")
        refresh_effects(g)
        self.assertEqual(g["effects"]["effect.codegen_vertical_slice"]["status"], "locked")
