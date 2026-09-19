# S8 — Gap Board UI

## Destruction
App Factory Studio “recommended scenario of modules” / `ship --tier` parade.

## What you see
- **Next**: Vein-ranked open unblocked Gaps
- **Gaps**: open / blocked / sealed cards with risk
- **Effects**: locked | ready | done (post-seal only)
- Banner: generation does not advance the product

## CLI
```bash
python3 src/seal/cli.py board --graph PATH --out board.html
python3 src/seal/cli.py board-json --graph PATH
```

## Module
`src/seal/board.py` + `src/seal/static/gap-board.html`

JSON graph remains canonical; the board is a projection.
