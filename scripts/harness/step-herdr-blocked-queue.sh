#!/usr/bin/env bash
# Documents / wraps: herdr agent wait --until blocked must enqueue to user/감독관.
# NEVER auto-approve — this script does not click anything.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "${SCRIPT_DIR}/lib.sh"

run_id="${1:?usage: step-herdr-blocked-queue.sh <run_id>}"

body=$(cat <<'BODY'
Instruction (queue only — never auto-approve):

  herdr agent wait --until blocked

When an agent is blocked (approval / merge / spend / external send):
1. Enqueue to user · 감독관 approval queue.
2. Do NOT auto-click approval UI.
3. Do NOT answer agent_blocked from harness.
4. READY / merge / publish / redeploy / adopt stay queue-only until sealed.

This step only records the invariant. It never clicks or approves.
BODY
)

write_done "$run_id" "blocked-queue" "$body"
echo "blocked-queue-done.md written for run_id=${run_id} (no auto-approve)"
exit 0
