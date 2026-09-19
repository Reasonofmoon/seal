#!/usr/bin/env bash
# Harness step: each env name set and non-empty. Fail → escalate.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "${SCRIPT_DIR}/lib.sh"

run_id="${1:?usage: step-env-ready.sh <run_id> <env-name> [<env-name>…]}"
shift
if [[ $# -lt 1 ]]; then
  echo "usage: step-env-ready.sh <run_id> <env-name> [<env-name>…]" >&2
  exit 2
fi

missing=()
checked=()
for name in "$@"; do
  checked+=("$name")
  # ${!name} indirect expansion
  val="${!name-}"
  if [[ -z "${val}" ]]; then
    missing+=("$name")
  fi
done

if [[ ${#missing[@]} -gt 0 ]]; then
  escalate_fail "$run_id" "env-ready" "「확인 실패」 missing/empty env: ${missing[*]}"
fi

body="$(printf 'ok env: %s\n' "${checked[*]}")"
write_done "$run_id" "env-ready" "$body"
exit 0
