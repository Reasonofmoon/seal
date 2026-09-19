#!/usr/bin/env bash
# Success only if file (or glob match) exists.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "${SCRIPT_DIR}/lib.sh"

run_id="${1:?usage: step-require-done.sh <run_id> <glob-or-file>}"
target="${2:?glob-or-file}"

shopt -s nullglob
matches=($target)
shopt -u nullglob

if [[ ${#matches[@]} -eq 0 ]]; then
  # also try as literal path
  if [[ -f "$target" || -e "$target" ]]; then
    matches=("$target")
  fi
fi

if [[ ${#matches[@]} -eq 0 ]]; then
  escalate_fail "$run_id" "require-done" "「확인 실패」 missing evidence: ${target}"
fi

body="$(printf 'found:\n%s\n' "$(printf '%s\n' "${matches[@]}")")"
write_done "$run_id" "require-done" "$body"
exit 0
