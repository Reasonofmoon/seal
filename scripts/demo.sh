#!/usr/bin/env bash
# One-shot SEAL demo — open pack, seal JTBD with code predicate, board + coverage
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
OUT="${TMPDIR:-/tmp}/seal-demo-$$"
mkdir -p "$OUT"
GRAPH="$OUT/graph.json"

python3 "$ROOT/src/seal/cli.py" open \
  --id demo --idea "Korean kids English reading habit app" \
  --pack edtech.foundation --out "$GRAPH" >/dev/null

python3 "$ROOT/src/seal/cli.py" seal-code \
  --graph "$GRAPH" --gap gap.edtech.jtbd.core_job --ok \
  --predicate code:demo_jtbd >/dev/null

python3 "$ROOT/src/seal/cli.py" board --graph "$GRAPH" --out "$OUT/board.html" >/dev/null
python3 "$ROOT/src/seal/cli.py" coverage --graph "$GRAPH"
python3 "$ROOT/src/seal/cli.py" status --graph "$GRAPH" | python3 -c "import sys,json; d=json.load(sys.stdin); print('open',d['open']); print('sealed',d['sealed']); print('next',[x['gap'] for x in d.get('next',[])])"
echo "Board: $OUT/board.html"
echo "Graph: $GRAPH"
