#!/usr/bin/env bash
# Harness step: github-qa-score.mjs — API fail → escalate 「확인 실패」
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "${SCRIPT_DIR}/lib.sh"

run_id="${1:?usage: step-github-qa-score.sh <run_id> <json-in>}"
json_in="${2:?json-in}"
GATE="${GITHUB_QA_SCORE_JS:-/workspace/typesafe-gates/github-qa-score.mjs}"

if [[ ! -f "$json_in" ]]; then
  escalate_fail "$run_id" "github-qa-score" "「확인 실패」 json-in missing: ${json_in}"
fi
if [[ ! -f "$GATE" ]]; then
  escalate_fail "$run_id" "github-qa-score" "「확인 실패」 github-qa-score.mjs missing: ${GATE}"
fi

set +e
out="$(node "$GATE" "$json_in" 2>&1)"
rc=$?
set -e

if [[ $rc -ne 0 ]]; then
  d="$(ensure_runs_dir "$run_id")"
  printf '%s\n' "$out" >"${d}/github-qa-score-stderr.txt" || true
  escalate_fail "$run_id" "github-qa-score" "「확인 실패」 github-qa-score API/exit ${rc}"
fi

write_done "$run_id" "github-qa-score" "$out"
exit 0
