# Why SEAL is a better workflow framework (falsifiable)

Jev is a **mint**: typed decisions with calibrated confidence.  
SEAL is a **workflow kernel**: what may advance the product, and only after sealed evidence.

This is not a wrapper around Jev. Jev (or any calibrated provider) is optional machinery for Strikes. The product object is the **Seal Graph**.

## One invariant

> **Generation cannot advance the product. No seal, no advance.**

If a framework lets a prompt chain, module run, or document body move “the product” forward without an explicit accept under lock, it fails this invariant.

| Framework class | What advances the product? | Fail mode |
|-----------------|----------------------------|-----------|
| Prompt / agent pipelines | Successful step execution | Fluent garbage compounds |
| Spec / PRD factories | Written artifacts | Spec drifts from reality; late audit theater |
| Executable knowledge docs (UKDL L3–L5) | Document-as-program | Living-doc fantasy; action/pipeline as truth |
| Decision APIs alone (Jev-class) | Nothing durable | Great judgments, no product state |
| **SEAL** | **Seals only** | Candidates may exist; Effects stay locked |

## Objective criteria (score your stack)

Mark each **pass/fail**. SEAL is designed so the default path **passes all**.

1. **Advance gate** — Can codegen / deploy / “implement” run without a recorded accept set?  
   SEAL: Effects require seals (and ordered `after_effects`). Fail without passport.
2. **Lock locality** — Are accept criteria attached to the claim, or a late rubric phase?  
   SEAL: each Gap carries `accept[]`. Conquest pack destroyed late `audit-spec`.
3. **Risk-proportional mint** — Can soft heuristics seal `user_trust` / irreversible claims?  
   SEAL: lock-policy forbids heuristic on those bands; TypeSafe/Jev required.
4. **Durable SSOT** — Is product truth a diffable graph, or chat + drifting markdown?  
   SEAL: Seal Graph JSON (+ optional UKDL *subset* serialization that cannot execute).
5. **Learning honesty** — Do weights update on generative chains or only on sealed success?  
   SEAL: Vein updates on seal success / lock fail only — not on module prompts.
6. **Ordering without fake DAG** — Are dependencies “run module A then B” or “seal A before fill B”?  
   SEAL: `requires` = seal prerequisites, not prompt order.
7. **Serialization ≠ runtime** — Can the human-readable form execute tools/pipelines?  
   SEAL: `action` / `quantum` / `pipeline` rejected in subset. Documents do not run.

## What Jev wins at (and SEAL does not pretend to)

- Latency and cost per typed decision  
- Calibrated confidence native to the model  

SEAL **uses** that where risk demands it. SEAL does **not** claim to be a System One model.

## What SEAL wins at (and Jev alone cannot)

- Stopping unsealed generation from becoming “the product”  
- Making foundation claims (JTBD, persona, ethics…) first-class durable nodes  
- Unlocking CONTEXT/codegen only after seals  
- Ranking next work by sealed-transition learning (Vein), not Hebbian-on-prompts  

## Worked contrast

```
Old: idea → ship 19 modules → envelopes → audit-spec → maybe implement
Jev-only: idea → many calibrated answers → still no product brain
SEAL: idea → open Gap Pack → fill / strike / seal → Effects unlock
```

Proof artifacts in-repo: `examples/readmaster-habit`, `examples/audit-conquest`, `examples/s5-implement-unlock`.

## Success metric

A clone of the Seal Graph reproduces what the product *is allowed to claim*.  
A clone of a chat transcript or a PRD folder does not.
