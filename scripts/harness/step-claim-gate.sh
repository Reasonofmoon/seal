#!/usr/bin/env bash
# Harness step: claim-gate.mjs — never pane prompt; keys via env only.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "${SCRIPT_DIR}/lib.sh"

run_id="${1:?usage: step-claim-gate.sh <run_id> <html-path>}"
html_path="${2:?html-path}"
GATE="${CLAIM_GATE_JS:-/workspace/typesafe-gates/claim-gate.mjs}"

if [[ ! -f "$html_path" ]]; then
  escalate_fail "$run_id" "claim-seal" "「확인 실패」 html missing: ${html_path}"
fi
if [[ ! -f "$GATE" ]]; then
  escalate_fail "$run_id" "claim-seal" "「확인 실패」 claim-gate.mjs missing: ${GATE}"
fi

set +e
out="$(node "$GATE" "$html_path" 2>&1)"
rc=$?
set -e

if [[ $rc -eq 0 ]]; then
  write_done "$run_id" "claim-seal" "$out"
  exit 0
fi

reason="「확인 실패」 claim-gate exit ${rc}"
if [[ $rc -eq 2 ]]; then
  reason="claim-gate BLOCK (exit 2)"
fi
# still write escalate with stdout for evidence
d="$(ensure_runs_dir "$run_id")"
printf '%s\n' "$out" >"${d}/claim-seal-gate-stdout.json" || true
escalate_fail "$run_id" "claim-seal" "$reason"
