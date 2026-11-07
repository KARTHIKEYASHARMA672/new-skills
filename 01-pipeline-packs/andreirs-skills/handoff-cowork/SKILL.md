---
name: handoff-cowork
description: Summarise the current Cowork conversation into a handoff document so a fresh Cowork chat can continue the work. Use whenever the user says "hand off", "wrap up this session", "write a handoff", "I'll continue this later/tomorrow", "context is getting long", or wants to pass the work to another chat or teammate.
argument-hint: "What will the next session focus on?"
---

Write a handoff document for this Cowork conversation, save it where the next chat can actually reach it, and present it so the user can open it. The point is that a fresh chat, opened with no memory of this one, can pick up exactly where you left off.

## Where to save

The scratchpad/outputs folder dies with the session — a new chat cannot see it. Save the handoff to the user's connected folder instead (the synced folder mounted into this session), so the next chat can open it by path:

1. If a connected folder is available, save to `<connected-folder>/handoffs/<YYYY-MM-DD>-<topic-slug>.md`. Create the `handoffs/` subfolder if needed. Also write `handoffs/HANDOFF-latest.md` containing the same content (or a one-line pointer to the dated file), so the resume prompt stays stable across sessions.
2. After writing, verify the write actually landed (read the file back or list the folder). Connected folders are sometimes mounted read-only; if the write failed, treat it as case 3.
3. If no folder is connected or the write failed, fall back to the scratchpad, present the file via `present_files`, and also paste the full handoff content into the chat as a fenced markdown block, since the file itself won't survive.

## Sections

Use these sections, in this order. Skip a section only if it's genuinely empty, don't merge them.

**Metadata** — date, project/folder, branch and recent commits if git is involved, and a link to the previous handoff in `handoffs/` if one exists (this builds a chain the next chat can walk back).
**Current state** — one paragraph: what the session was about and where things stand.
**Decisions & why** — the key decisions with the reasoning that ruled out the other options. A new agent can follow instructions; what it can't recover is the why.
**Open threads** — what's unfinished, blocked, or waiting on the user, in priority order.
**Next steps** — concrete, actionable first moves for the next chat, not vague goals.
**Critical files** — paths (and URLs: PRs, tickets, pages) with a few words on why each matters.
**Gotchas** — surprises, workarounds, and patterns discovered the hard way.
**Verification state** — what was actually tested and observed vs what is assumed to work. This stops the next chat from trusting unverified work.
**Suggested skills & connectors** — skills the next chat should invoke and connectors (Slack, Jira, Confluence, Bitbucket, StarRocks, filesystem, etc.) it will need.

## Rules

- Reference existing artifacts (files you created, plans, specs, PRs, diffs, Confluence pages, Jira tickets) by path or URL instead of duplicating their content — the new chat can open them, and copies drift out of date.
- Redact API keys, passwords, tokens, and PII. A handoff doc is easy to paste around, so treat it as shareable.
- If the user passed arguments, treat them as the next session's focus and tailor the doc to it — drop sections that don't serve that focus.
- Keep it to what the next chat actually needs to act. This is a runway, not a transcript.

## After saving

Present the handoff file to the user (via `present_files`), then print a short message with:

1. A short prompt they can paste into a new Cowork chat. Put it on its own line inside a fenced code block (```) so it renders as a copy-paste block rather than inline prose — the whole point is that they can copy it in one click. Make it self-bootstrapping: read the handoff, set up what it names, confirm before acting. Reference `HANDOFF-latest.md` so the same prompt works after future handoffs too. For example:

   ```
   Read handoffs/HANDOFF-latest.md, connect the skills and connectors it lists, then tell me your plan before acting — next focus: X
   ```

   If you had to fall back to the scratchpad, the prompt can't reference a path — tell the user (outside the code block) to attach the doc or paste its contents into the new chat instead.
2. If the work naturally continues on a schedule (a daily check, a weekly recap), offer in one line to set up a scheduled task so the handoff runs itself.
