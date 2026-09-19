# blocked-queue — done

- run_id: `compare-jev-20260919`
- at: 2026-09-19T08:45:03+00:00
- exit: 0

```
Instruction (queue only — never auto-approve):

  herdr agent wait --until blocked

When an agent is blocked (approval / merge / spend / external send):
1. Enqueue to user · 감독관 approval queue.
2. Do NOT auto-click approval UI.
3. Do NOT answer agent_blocked from harness.
4. READY / merge / publish / redeploy / adopt stay queue-only until sealed.

This step only records the invariant. It never clicks or approves.
```
