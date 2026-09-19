# SEAL

### No seal, no advance.

**SEAL** (Seal · Evidence · Atomic Lock) is a workflow kernel for building products with AI: the product may only move forward when claims are **sealed** under explicit locks.

It is **not** another agent pipeline, not an executable knowledge document, and not “Jev with a UI.”  
[Jev](https://typesafe.ai) is a decision mint. SEAL is the **graph that decides what those decisions are allowed to unlock**.

[Why SEAL](docs/WHY-SEAL.md) · [Beyond Jev](docs/BEYOND-JEV.md) · [Public cases](docs/CASES-PUBLIC.md) · [Manifesto](docs/SEAL-FRAMEWORK.md)

---

## The door beyond Jev

Developers praised Jev for typed, calibrated decisions — and warned that **schema-valid ≠ true**, that **accuracy without coverage** is dishonest, and that a mint is not a product brain. SEAL’s answer is the **Coverage Gate** + **advance gate**: see [docs/BEYOND-JEV.md](docs/BEYOND-JEV.md).

Famous public repos scored as workflow classes: [examples/public-repos](examples/public-repos/).

## Differentiation in one screen

| | Agent / module pipelines | Spec factories | UKDL L3–L5 | Jev / System One | **SEAL** |
|--|--------------------------|----------------|------------|------------------|----------|
| Unit of progress | Step ran | Doc written | Node executed | Decision returned | **Seal recorded** |
| Late audit boss fight | Common | Common | N/A | N/A | **Destroyed** (locks on Gaps) |
| Trust-band enforcement | Rare | Rare | N/A | Caller’s job | **Kernel policy** |
| Durable product brain | Weak | Drifts | Living-doc myth | None | **Seal Graph** |
| Learning signal | Token / prompt chains | — | — | — | **Sealed transitions only (Vein)** |
| Human-readable form | Prompts | Markdown | Full UKDL | API JSON | **UKDL subset that cannot execute** |

If generation alone advances your “product,” you do not have SEAL — you have a parade.

---

## Kernel loop

```
Gap → Candidate → Strike → Seal → Effect
```

1. **Gap** — typed hole; accept locks already attached  
2. **Candidate** — proposed fill (human / import / generative)  
3. **Strike** — atomic judgment batch (heuristic or TypeSafe/Jev)  
4. **Seal** — append-only accept  
5. **Effect** — CONTEXT, codegen, deploy… **only after** required seals  

```bash
seal open   --idea "…" --pack edtech.foundation
seal fill   --gap … --text "…"
seal strike --gap … --candidate … --provider heuristic|typesafe
seal status          # open / blocked / sealed / next (Vein)
seal effect --id …   # refused until seals unlock it
seal board  --out board.html
```

---

## Quickstart

```bash
git clone https://github.com/Reasonofmoon/seal.git
cd seal
PYTHONPATH=src python3 -m unittest discover -s tests -v

# Open a pack and inspect the board
PYTHONPATH=src python3 src/seal/cli.py open \
  --id demo --idea "Korean kids English reading habit app" \
  --pack edtech.foundation --out /tmp/demo.json
PYTHONPATH=src python3 src/seal/cli.py board --graph /tmp/demo.json --out /tmp/board.html
```

`user_trust` / `irreversible` gaps **refuse heuristic**. For those strikes:

```bash
cp .env.example .env   # set TYPESAFE_API_KEY
npm install            # optional: @typesafe-ai/sdk
export TYPESAFE_API_KEY=…
# optional: export NODE_PATH="$(pwd)/node_modules"
```

---

## In-repo proofs

| Example | Shows |
|---------|--------|
| [`examples/demo-open`](examples/demo-open) | Vein-ranked next Gap; blocked dependents |
| [`examples/readmaster-habit`](examples/readmaster-habit) | Foundation 5/5 sealed + CONTEXT effect |
| [`examples/audit-conquest`](examples/audit-conquest) | Weak AF spec fails rubric Gaps under locks |
| [`examples/s5-implement-unlock`](examples/s5-implement-unlock) | Codegen locked until passport + context |

---

## Status (S1–S8)

Schema · Gap packs · Strike mint · TypeSafe on trust bands · audit-spec conquest · post-seal Effects · Vein · UKDL subset · Gap Board.  
See [`docs/S0-S8-STATUS.md`](docs/S0-S8-STATUS.md).

---

## Layout

```
schemas/     seal-graph + lock-policy
packs/       edtech.foundation · conquest.audit-spec
src/seal/    kernel · vein · ukdl subset · board · cli
examples/    sealed proofs + Gap Board HTML
docs/        manifesto · why · phase notes
tests/       22 unittest cases
```

Python kernel: **zero runtime dependencies**. Node is optional and only for TypeSafe mint.

---

## License

MIT · Reason of Moon
