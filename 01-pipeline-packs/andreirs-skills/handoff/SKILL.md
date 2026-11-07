---
name: handoff
description: Summarise the current conversation into a handoff document so a fresh agent can continue the work.
argument-hint: "What will the next session focus on?"
---

Write a handoff document for this conversation and save it to `~/.claude/handoffs/YYYY-MM-DD-<slug>.md`.

That exact path, not the session scratchpad and not a temp dir: the whole point is that a **future** session reads this file, and the scratchpad is deleted when this session ends. Nothing lands in the current workspace.

Include:

**Context** — what the session was about and where things stand, with a short log of why a decision was made.
**Suggested skills** — skills the next agent should invoke.

## Rules

- Reference existing artifacts (plans, PRDs, ADRs, commits, diffs) by path or URL instead of duplicating their content.
- Redact API keys, passwords, and PII.
- If the user passed arguments, treat them as the next session's focus and tailor the doc accordingly — omit sections irrelevant to that focus.

## After saving

Print a short message to the user with:
1. The full path to the handoff doc.
2. A one-sentence prompt they can paste into the next session to orient the agent (e.g. "Continue from [path] — next focus: X").
