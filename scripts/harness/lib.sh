#!/usr/bin/env bash
# SEAL harness helpers — evidence SSOT under runs/<id>/
# Never auto-click approval UI. Keys only via env / box-secrets.
set -euo pipefail

SEAL_RUNS_ROOT="${SEAL_RUNS_ROOT:-/workspace/seal/runs}"

runs_dir() {
  local run_id="${1:?run_id}"
  echo "${SEAL_RUNS_ROOT}/${run_id}"
}

ensure_runs_dir() {
  local run_id="${1:?run_id}"
  local d
  d="$(runs_dir "$run_id")"
  mkdir -p "$d"
  echo "$d"
}

# write_done <run_id> <name> <body>
# Creates runs/<id>/<name>-done.md (name may already include -done)
write_done() {
  local run_id="${1:?run_id}"
  local name="${2:?name}"
  local body="${3:-}"
  local d base out
  d="$(ensure_runs_dir "$run_id")"
  base="${name%-done}"
  base="${base%.md}"
  out="${d}/${base}-done.md"
  {
    echo "# ${base} — done"
    echo
    echo "- run_id: \`${run_id}\`"
    echo "- at: $(date -Iseconds)"
    echo "- exit: 0"
    echo
    if [[ -n "$body" ]]; then
      echo '```'
      echo "$body"
      echo '```'
    fi
  } >"$out"
  echo "$out"
}

# escalate_fail <run_id> <name> <reason> — writes *-escalate.md and exits 2
escalate_fail() {
  local run_id="${1:?run_id}"
  local name="${2:?name}"
  local reason="${3:-확인 실패}"
  local d base out
  d="$(ensure_runs_dir "$run_id")"
  base="${name%-escalate}"
  base="${base%-done}"
  base="${base%.md}"
  out="${d}/${base}-escalate.md"
  {
    echo "# ${base} — escalate"
    echo
    echo "- run_id: \`${run_id}\`"
    echo "- at: $(date -Iseconds)"
    echo "- exit: 2"
    echo "- reason: ${reason}"
    echo
    echo "「확인 실패」 — do not invent pass. Queue READY/merge/publish/redeploy/adopt only."
  } >"$out"
  echo "$out" >&2
  exit 2
}
