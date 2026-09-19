# SEAL — Creative Destruction Framework

**Working title:** SEAL (Seal · Evidence · Atomic Lock)  
**Status:** Manifesto + kernel design v0 · 2026-09-19 KST  
**Parents (to be consumed, not wrapped):** App Factory · UKDL · TypeSafe/Jev  
**Stance:** Not an integration layer. A replacement operating model for “idea → durable product truth.”

---

## 0. Indictment (what we destroy)

Creative destruction starts by naming the idols.

### Kill from App Factory

| Idol | Why it dies |
|------|-------------|
| **67 MECE generative modules as the spine** | Catalog equality pretends every stage needs an LLM essay. Most stages need a *typed hole* and a *seal*, not another prompt. |
| **Envelope-as-truth** | Envelopes are receipts of generation. Truth is what survives a lock, not what validated JSON once. |
| **Ship → then audit** | Quality after generation is theater. The default must be **decide-the-lock-first**. |
| **Harness pack as prompt stuffing** | Slots for coding agents are a *projection*, not the product brain. |
| **Persona panel as quality** | Celebrity cosplay ≠ calibrated acceptance. Keep as optional *commentary*, never as the lock. |
| **Hebbian “what module next” as intelligence** | Path statistics without sealed outcomes confuse habit with truth. |

### Kill from UKDL

| Idol | Why it dies |
|------|-------------|
| **Document-that-executes (L3–L5 action/pipeline)** | Orchestration in a markup language is a category error. Docs hold seals & gaps; runtimes host effects. |
| **Quantum/entanglement as product metaphor without mint** | Probabilistic state without an external calibrated mint is fan fiction. |
| **Ten kinds competing with Markdown/RDF/LangChain** | Ambition diluted the kernel. Fewer primitives, harder guarantees. |
| **`@confidence` on knowledge** | Provenance is not inference. Mixing them taught every consumer the wrong lesson (BlogRich LIVE). |

### Kill from Jev-alone usage

| Idol | Why it dies |
|------|-------------|
| **Stateless “bring your own state every time”** | Forces every app to reinvent memory; seals evaporate. |
| **Ephemeral question JSON** | Unreviewed, unversioned decisions. |
| **Judgment as a side library beside the factory** | Side libraries get skipped under deadline. Locks must be the *only* way to advance. |

### Kill from the “three-layer fusion” draft

| Idol | Why it dies |
|------|-------------|
| **AF makes / UKDL remembers / UJH decides** | Clean ownership diagram = polite federation. Federations preserve legacy waste. |
| **Adapters forever (`ukdl-ingest`, observe hooks)** | Glue code is the tell that no new object exists. |

---

## 1. The new object

**There is one product substrate: the Seal Graph.**

A product is not a `spec.md`, not a module chain, not a `.ukdl` novel.

A product is a growing graph of:

1. **Gaps** — typed absences (what must become true)  
2. **Candidates** — proposed fills (human, import, or generative)  
3. **Strikes** — atomic judgment batches over a projected world-state  
4. **Seals** — accepted fills, locked with provider+policy evidence  
5. **Effects** — optional side effects *after* seal (write file, deploy, publish)

Generation is demoted from protagonist to **Gap Filler**: it may only propose Candidates. It cannot advance the product.

```
        Gap (typed hole)
           │
           ▼
     Candidate(s)     ← human | import | generative fill
           │
           ▼
        Strike         ← Jev-class atomic questions, independent, one state
           │
     ┌─────┴─────┐
     ▼           ▼
  Seal         Reject / Escalate
     │
     ▼
  Effect? (optional, sandboxed)
```

This inverts App Factory: **locks drive the timeline; modules do not.**

---## 2. Name and meaning

**SEAL** = Seal · Evidence · Atomic Lock

| Term | Definition | Boundary |
|------|------------|----------|
| **Gap** | A schema-backed unknown with acceptance criteria already declared | Not a prompt. Not a “module to run.” |
| **Candidate** | A proposed value for a Gap, with provenance | Not truth until sealed |
| **Strike** | One evaluate tick: shared state, N independent questions | Not an agent loop |
| **Seal** | Irreversible (append-only) accept record: value + answers + policy + hashes | Not an envelope |
| **Lock Policy** | Gate bands by risk class | Not a rubric essay |
| **World Projection** | Deterministic view of Seal Graph → Strike `state` | Not “whatever the last LLM wrote” |
| **Effect** | Post-seal side effect | Never runs on Candidate alone |
| **Vein** | Learned edge weights between *sealed* transitions only | Not Hebbian-on-prompts |

UKDL survives only as **serialization grammar for the Seal Graph** (human-readable).  
Jev survives as **the preferred Strike mint** (calibrated).  
App Factory survives as **a library of Gap Type packs + Candidate generators** — scavenged parts, not the OS.

---

## 3. Kernel primitives (replace AF modules + UKDL kinds)

Five kinds. That’s the whole language surface.

### 3.1 `gap`

```seal
gap.readmaster.jtbd.core_job {
  schema: { type: string, minLength: 12 }
  ask: "What durable job is the learner hiring this app to do?"
  risk: product_foundation
  accept: [
    noul supports_evidence >= 0.8
    noul not_solution_disguised_as_job >= 0.75
    choice form in [outcome_framed] confidence >= 0.7
  ]
  fillers: [human, generative.af.jtbd, import.url]
}
```

A Gap **ships its own Strike template**. No separate “run jtbd module then audit.”

### 3.2 `candidate`

```seal
candidate.c1 of gap.readmaster.jtbd.core_job {
  value: "Help a child keep a daily English reading habit without parental nagging"
  by: generative.af.jtbd@3.2.1
  model: gemini-2.5-flash-lite
  cost_usd: 0.02
}
```

### 3.3 `strike`

Compiled automatically from Gap.accept + World Projection. Authors rarely write raw strikes; they write accept policies on Gaps.

### 3.4 `seal`

```seal
seal.s1 {
  gap: gap.readmaster.jtbd.core_job
  candidate: candidate.c1
  strike_id: strike.t9
  answers: { ... }
  policy: lock.product_foundation
  state_hash: sha256:…
  questions_hash: sha256:…
  provider: typesafe:jev-latest
  at: 2026-09-19T07:40:00+09:00
}
```

Append-only. Supersede via new seal + `deprecated` pointer — never silent edit (Atlas rule, elevated to kernel).

### 3.5 `effect`

```seal
effect.emit_context {
  after: [seal.s1, seal.s2, …]
  run: pack.context_md
  sandbox: workspace_write
}
```

Effects are privileged and rare. Publishing, deploying, mailing = effects with `risk: irreversible`.

---

## 4. World Projection (destroys Jev statelessness + UKDL context theater)

`state` for any Strike is a **pure function**:

```
state = project(seal_graph, gap.projection_spec, phase)
```

Rules:
- Only **sealed** values appear as facts.  
- Candidates under test appear under `proposal.*`, never as facts.  
- Deprecated seals excluded unless `include_history`.  
- Phase (`full|summary|priority|skeleton`) compresses bodies — borrowed from UKDL, stripped of “document executes.”  
- CJK/risk packaging adjusts thresholds, not facts.

So Jev always sees a world that the graph already commits to — creative destruction of “rebuild JSON by hand in every app.”

---

## 5. Lock Policy (destroys post-hoc rubrics)

Risk classes replace AF tier thresholds and UJH ad-hoc gates:

| Risk class | Default band | Examples |
|------------|--------------|----------|
| `read` | low confidence OK | Show next Gap |
| `product_foundation` | strict | JTBD, north star, data model |
| `user_trust` | very strict | LIVE badges, scores, claims |
| `irreversible` | human co-seal required | publish, pay, delete, prod deploy |

F24’s 13 rubrics become **Gap Types in a pack**, each with accept locks — not a late `audit-spec` boss fight.

Persona panel, if used, writes **commentary candidates** on a `gap.*.critique` that can be sealed or ignored; it cannot seal `user_trust` alone.

---

## 6. Candidate Fillers (scavenge App Factory)

App Factory’s module catalog is **melted into Gap Type Packs**:

| Old module | Becomes |
|------------|---------|
| `jtbd` prompt | filler `generative.af.jtbd` + default Gap Type `gap.pack.discovery.jtbd` |
| `prd` | filler + Gap Type with harder locks |
| `ethics` | often **no filler** — pure Strike over projected UX claims |
| `spec-audit` | deleted as a phase; absorbed into each Gap.accept |
| `vibe-code` | Effect `effect.codegen` after enough foundation seals |
| `pack` / CONTEXT.md | Effect `effect.emit_context` |
| Hebbian engine | Vein: weights on `seal_type → next_gap` using sealed success only |

Studio UX changes meaning: not “recommended scenario of modules,” but **“open Gaps ranked by Vein + risk.”**

CLI changes meaning:

```bash
# old
app-factory ship --tier builder-mini --idea "…"

# seal
seal open --idea "한국 어린이 영어 독서 습관 앱" --pack edtech.foundation
seal fill gap.… --with generative.af.jtbd
seal strike gap.…
seal status          # open gaps / seals / blocked locks
seal effect emit_context
```

`ship` as a word dies. **Opening a pack of Gaps** replaces it.

---

## 7. Serialization (scavenge UKDL)

SEAL Graph serializes to a **strict subset** of UKDL-looking syntax (or JSON canonical form).

Allowed surface kinds: `gap | candidate | seal | effect | meta | entity | rel`  
Banned in kernel: `action`, `pipeline`, `quantum` as executors.

If you need probabilistic product state (learner level), it is a **Gap that reseals on a schedule** (`gap.learner.level` with decay policy), not a physics metaphor node.

Parser/LSP/MCP from ukld-spec are redirected at this subset — creative destruction of L5 fantasies, preservation of tooling investment.

---

## 8. Strike mint (scavenge Jev)

Strike execution = UJH evaluate path, but **mandatory**:

- No seal without strike (except `risk:read` auto-seal for imports with cryptographic checksum only).  
- Heuristic provider allowed only with `provider:heuristic` tattooed on seal; never lights LIVE/trust UI.  
- Independent questions; second strike only when projection truly changes.  
- Audit line ≡ reproducibility (AF hash religion kept, object changed).

Jev is not a plugin. **It is the mint.** Without a mint, the graph may collect Candidates but cannot Seal `user_trust` or `irreversible`.

---

## 9. What the user experiences (new frame, not three apps)

1. Speak an idea.  
2. System opens a **Gap Pack** (edtech / saas / internal…).  
3. You see holes, not a 40-step module parade.  
4. Fillers propose Candidates where allowed.  
5. Each accept is a visible Strike → Seal (or human escalate).  
6. When foundation seals suffice, Effects unlock (CONTEXT, codegen, deploy).  
7. The durable artifact is the Seal Graph — cloneable, diffable, queryable — not a novel `spec.md` that drifts from reality.

Education products (ReadMaster, BlogRich, moonlang) stop maintaining parallel truths: the sealed claims *are* the product brain.

---

## 10. Migration as conquest (not adapters)

| Phase | Act of destruction | Result |
|-------|--------------------|--------|
| **S0** | Freeze AF “three-layer fusion” ADR as rejected | No more glue mythology |
| **S1** | Define Seal Graph schema + JSON canonical | New object exists |
| **S2** | Port 5 Gap Types from AF L0–L1 (jtbd, persona, vision, constraints, ethics-as-lock) | Pack `foundation.v0` |
| **S3** | Wire TypeSafe mint; refuse seal on trust risks without key| Mint is real |
| **S4** | Delete `audit-spec` phase from happy path | Locks live on Gaps |
| **S5** | Effects: emit CONTEXT + optional codegen | Post-seal only |
| **S6** | Vein replaces Hebbian-on-modules | Learning on seals |
| **S7** ✅ | UKDL L3–L5 marked legacy; subset grammar = SEAL | See docs/S7-UKDL-SUBSET.md |
| **S8** ✅ | App Factory Studio relaunches as Gap Board | See docs/S8-GAP-BOARD.md |

Scrap value kept: schemas, golden tests, BYO key UX, publication boundary, glossary discipline, envelope *as candidate receipt* (downgraded).

---

## 11. One worked contrast

**Old (App Factory):**  
idea → ship 19 modules → envelopes → pack harness → audit-spec → maybe fix → implement  

**Old (fusion):**  
same, plus ingest to UKDL plus UJH at pre_pack  

**SEAL:**  
idea → open `edtech.foundation` gaps → fill/strike/seal in any order permitted by dependencies → when seals ⊇ unlock set → effect emit → effect codegen  

Dependencies are **seal prerequisites**, not DAG of prompts.

---

## 12. Success metric (so this isn’t poetry)

A framework earns the name when:

1. Advancing the product **without** a Seal is impossible for `user_trust` and `irreversible`.  
2. A generative module can be deleted without breaking the kernel (only a filler disappears).  
3. Two products can diff Seal Graphs and see *accepted truth drift*, not markdown noise.  
4. BlogRich-class LIVE lies cannot appear without a seal that would fail a Noul.  
5. Cold-start still works: Gap Packs ship default accept policies before any Vein data.

---

## 13. Relation to prior drafts

| Document | Fate |
|----------|------|
| UJH SPEC.md | **Absorbed** as Strike/mint machinery inside SEAL |
| FUSION-app-factory.md | **Superseded** — federation rejected |
| UKDL v2.0 L3–L5 | **Legacy** |
| App Factory module spine | **Scavenged** into Gap Type Packs + fillers |

---

## 14. Closing

App Factory automated *writing*.  
UKDL romanticized *living documents*.  
Jev perfected *atomic judgment*.

SEAL keeps only the hard parts: **typed absence, proposed fill, calibrated lock, append-only truth, effects after.**

Everything else was inventory.

---

*No seal, no advance.*

### S6 Vein
See [S6-VEIN.md](S6-VEIN.md). Learning is sealed-transition only.
