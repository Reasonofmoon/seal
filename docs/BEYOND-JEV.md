# Beyond Jev — the door SEAL opens

## What developers actually said about Jev

Synthesized from public reviews and launch discourse (Flavio Copes deep dive, Actionbox review, DEV jaggedness guides, HN thread on System One demos, awesome-jev caveats):

| Praise | Limit |
|--------|--------|
| Fast, cheap typed decisions for **bounded** tasks | Schema-valid ≠ **semantically** correct |
| Parallel Choice / Score / Noul | **Accuracy without coverage** hides the exception queue |
| Confidence for gating | Vendor evals ≠ your ground truth; pin versions |
| Honest “jaggedness” docs | No write/math/dates — keep those in **code** |
| Belongs between `if` and an LLM | A mint does **not** make a durable product brain |

HN and independent writers were sharp: demos can overclaim; confidently wrong valid labels still happen; chaining Nouls into an “LLM of ifs” is a trap; open weights / reproducibility remain open issues for the mint itself.

## The innovative door (not a better Jev wrapper)

**Jev answers questions. SEAL answers whether the world may change — and shows the exception queue.**

1. **Advance gate** — Effects unlock only after Seals (generation cannot advance).  
2. **Coverage Gate** — Every Seal stamps `coverage.path`: `auto` | `escalate` | `human` | `code`.  
   `seal coverage` prints a ledger. Hiding escalations is a product lie; SEAL refuses that lie.  
3. **Deterministic first** — When code already decides, seal with `provider: code:…`. Developers were right: a free correct `if` beats a paid wrong mint.  
4. **Mint is optional machinery** — TypeSafe/Jev is one Strike provider on trust bands, not the product object.  
5. **Public-repo scorecards** — Famous stacks (LangChain, CrewAI, AutoGen, Vercel AI, TypeSafe SDK) are scored as workflow classes, not wrapped.

## Coverage Ledger (API)

```bash
seal strike …          # stamps coverage.path on the seal
seal escalate --gap …  # open exception-queue entry
seal coverage --graph graph.json
```

Effect policies may require `require_no_open_escalations` and optional `min_auto_rate`.

## What we refuse to claim

We do not claim SEAL is faster or cheaper than Jev.  
We do not claim seals are always true.  
We claim: **no silent advance**, **no hidden exception queue**, **mint ≠ product**.
