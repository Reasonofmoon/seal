# Recipe: block merge until foundation seals exist

1. Copy `examples/demo-open/graph.json` pattern or run `seal init --dir .seal --id myapp --idea "…"`.
2. In CI, fail if `seal status` shows required gaps still `open` for your release pack.
3. For trust gaps, require `coverage.path` in `auto|human|code` and zero `escalate_open` before deploy job.

Example gate (bash):

```bash
PYTHONPATH=src python3 -c "
import json,sys
from pathlib import Path
sys.path.insert(0,'src')
from seal.graph import load
from seal.coverage import ledger
g=load(Path('.seal/graph.json'))
led=ledger(g)
open_g=[i for i,x in g['gaps'].items() if x['status']=='open']
if open_g: raise SystemExit('open gaps: '+','.join(open_g))
if led['escalate_open']: raise SystemExit('escalations open')
print('SEAL gate OK')
"
```
