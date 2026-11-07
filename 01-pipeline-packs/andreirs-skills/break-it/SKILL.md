---
name: break-it
description: Try to break a running app and report the bugs a human QA would catch. Drives the app with agent-browser, throwing nasty inputs and edge cases at the flows you changed. Use to QA, stress-test, or "try to break" a feature or change. Never edits code or files issues; to just confirm the happy path works, use prove-it.
allowed-tools: Bash, Read, Glob, Grep, Write
---

# break-it

Drive the **running app** like a user trying to break it, and write up what you find. You hunt bugs; you don't fix them and you don't file issues. The only thing you write is the report and its screenshots.

## Flow

1. **Scope.** Pick the surface, in order: an explicit focus arg → the conversation and this session's work → the diff (`git diff main...HEAD` plus uncommitted). Map changes to the user-facing flows they touch. The scope is bounded, so this terminates — don't wander into unrelated features.
2. **Attack each flow.** Run the happy path once, then throw the obvious nasties: empty, huge, wrong-type, unauthorized, double-submit, back-button mid-flow. Watch for crashes, blank states, and silent failures (looks like it worked, nothing happened). Stop a flow once its edges are covered; don't chase exhaustive cases.
3. **Checklist, every flow.** Console errors · failed or hanging network calls (4xx/5xx) · form validation (required fields, bad input, are errors shown clearly).

Drive with **agent-browser**: `open`, `snapshot -i` for `@eN` refs, act, re-snapshot. Capture `screenshot`, `console`, `errors`, `network`. Run `agent-browser --help` for the current API and `agent-browser skills get dogfood --full` for the exploratory playbook. For a backend or CLI with no UI, hit endpoints or run the binary with adversarial inputs instead.

## Report

Write to `docs/qa/<date>-<branch>.md`, screenshots alongside. Summarize in chat (counts by severity + the worst findings). Severity: **blocker** (unusable, crash, data loss) · **major** (works but wrong) · **minor** (cosmetic).

```markdown
# break-it — <branch> — <date>
**Scope:** <flows tested>  ·  **App:** <url>

## Findings
### [blocker] <title>
- **Repro:** 1. … 2. …
- **Expected / Actual:** … / …
- **Evidence:** <console/network excerpt> · ![](./<slug>.png)

## Checklist
- Console: <clean | list> · Network: <clean | list> · Validation: <clean | list>
```

Nothing found is still a result — write the report with an empty findings list and the checklist.
