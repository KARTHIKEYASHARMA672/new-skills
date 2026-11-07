---
name: prove-it
description: Drive the running app like a human to confirm the flows you just changed work. Walks each happy path with agent-browser and reports a pass/fail verdict. Use to confirm a fix works, smoke-test a change, or check a feature end to end in the real app. Confirmation only; to try to break things, use break-it.
allowed-tools: Bash, Read, Glob, Grep
---

# prove-it

Drive the **running app** like a user and confirm the flows you just touched work end to end. You confirm; you don't hunt edge cases (that's `break-it`) and you don't fix what breaks.

## Flow

1. **Scope.** Pick what to prove, in order: an explicit focus arg → the conversation and this session's work → the diff (`git diff main...HEAD` plus uncommitted). Map the changes to the user-facing flows they touch. Name the flows in one line, then go.
2. **Happy path.** For each flow, state the expected end-to-end success ("log in → dashboard shows the new widget"). That's the bar you prove against.
3. **Walk it.** Drive each path with **agent-browser**: `open`, `snapshot -i` for `@eN` refs, act on them, re-snapshot after every change. Screenshot the key steps. Run `agent-browser --help` for the current API and `agent-browser skills get core --full` for the command reference. For a backend or CLI with no UI, exercise it directly (HTTP calls, the binary) instead.
4. **Verdict.** Each flow passes (ran end to end) or fails (where it broke). Console errors and failed network calls during the walk count as failures — they undercut the claim. Don't probe beyond the flow.

## Report

Chat-first. Save a screenshot only when it adds something. Keep it to the verdict:

```
Proved on http://localhost:3000
✓ Checkout — login → cart → pay → confirmation. Clean console, all 2xx.
✗ Profile edit — avatar upload 500s (POST /api/avatar). [screenshot]
1 of 2 flows confirmed.
```

Driving submits forms and writes data, so assume a dev or throwaway environment.
