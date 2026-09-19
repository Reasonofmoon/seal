# SEAL — notes for coding agents

- Invariant: **No seal, no advance.** Do not unlock codegen/deploy Effects without seals.
- Prefer `seal seal-code` when a deterministic check already decides (lint/tests).
- Prefer TypeSafe/Jev mint only on `user_trust` / `irreversible` gaps.
- Never hide escalations — `seal escalate` then human/code seal.
- One-shot: `bash scripts/demo.sh`
- Scaffold: `PYTHONPATH=src python3 src/seal/cli.py init --dir .seal --id app --idea "…"`
