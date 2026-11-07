---
name: session-recap
description: Summarize the Claude Code sessions from a given day across all projects. Defaults to today; accepts "yesterday" or a YYYY-MM-DD date. Use when the user asks to recap, summarize, or review what they worked on with Claude Code today / yesterday / on a date.
argument-hint: "[today|yesterday|YYYY-MM-DD]"
---

# Session Recap

Produce a readable summary of the user's Claude Code sessions for a day, grouped by project, with a short through-line at the end. Then offer to bookmark any session into the Obsidian daily note for easy resume.

## When to use

The user asks things like "summarize today's Claude Code sessions", "what did I work on yesterday", "recap my sessions from 2026-06-28", "/session-recap", "/session-recap yesterday".

## Steps

1. **Resolve the day.** Default is today. If the user passed an argument, pass it straight through: `today`, `yesterday`, or an explicit `YYYY-MM-DD`.

2. **Run the helper script** to get the raw digest:
   ```bash
   python3 ~/.claude/skills/session-recap/scripts/recap.py [today|yesterday|YYYY-MM-DD]
   ```
   It scans every `~/.claude/projects/*/*.jsonl` transcript, keeps only sessions whose content actually lands on the target date (a resumed session bumps the file mtime without adding new-day content, so mtime alone is not trusted), and prints per-session: the full session id, the time span, the message count for that day, and the real user prompts (slash-command echoes, image markers, interrupt markers, and tool results are filtered out). Prompts and the span are scoped to the target day, so a session resumed across days only shows that day's activity.

3. **Write the prose summary** from the digest. Do **not** just dump the script output. For each session that did real work that day:
   - Name the project and what the session was about (infer from the prompts).
   - Summarize what happened in 2-5 bullet points: the goal, key decisions, what shipped, and anything left open.
   - Skip or one-line trivial/automated runs (e.g. a scheduled standup digest).
   - Group by project. Order projects/sessions by time.
   - End with a one-sentence through-line tying the day together and flag any open thread.

4. **Offer to bookmark sessions** (synergy with the `save-session` skill). After the summary, ask whether the user wants to bookmark any of the day's sessions into the Obsidian daily note so they can jump back in later. For each session they pick:
   - You already have a **title** (2-3 words) and a **one-line summary** for it from step 3 — reuse them.
   - Run the save-session helper for that session's id (note the trailing id argument):
     ```bash
     ~/.claude/skills/save-session/scripts/session-info.sh <session-id>
     ```
   - Then **follow the `save-session` skill's write steps** (its step 3 onward) to append the `### HH:MM — Title` entry, using the title and summary you already have. Don't re-derive the markdown shape here; save-session owns it.
   - If the `save-session` skill isn't installed (`~/.claude/skills/save-session` missing), say so and skip this step.

## Notes

- Timestamps in transcripts are UTC; the script labels them as such. "Today" is resolved from the local system date, so a session run late at night may occasionally straddle the UTC date boundary. If a recap looks like it is missing a session, try the adjacent date.
- The current session (the one running this skill) will appear in the digest. It's fine to omit it or mention it as "this session".
- If the digest is empty, say so plainly rather than inventing activity.
- The summary is for the user to read, so favor what they decided and shipped over a mechanical list of tool calls.
- The bookmark in step 4 lands in *today's* daily note (Obsidian resolves the daily note for the current date). For a past-day recap that is still where the resume pointer goes; the entry's time heading reflects the session's real start time.
