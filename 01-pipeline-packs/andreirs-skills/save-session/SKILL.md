---
name: save-session
description: Bookmark the current Claude Code session into the user's Obsidian daily note so they can jump back into it later from any terminal (or their phone). Use whenever the user says "save this session", "bookmark this session", "/save-session", "link this to my journal", or otherwise wants a resume-able pointer to the current conversation. Writes the start time and a copy-paste `claude --resume … --remote-control` command into the section of today's daily note that already covers this work, or into a new topic section if none does. The journal vault is hardcoded in the helper script — see setup below.
argument-hint: "[optional title for the entry]"
---

Bookmark the current session into today's daily note so it can be resumed later. The point is a durable, copy-paste pointer back into *this* conversation: when it started and the exact command to reopen it (remote-control enabled so it's reachable from a phone), placed inside the note section that already talks about this work so it reads as part of the day, not as an appendix.

## Setup (first-time / per-user)

The helper writes to **one fixed journal vault, hardcoded at the top of `scripts/session-info.sh`** in a `CONFIGURE ME` block. Before using this skill, edit those three lines to match your setup:

- `JOURNAL_VAULT` — absolute path to the vault holding your journal (e.g. `$HOME/Brain`)
- `JOURNAL_FOLDER` — the daily-notes folder inside it (`""` for the vault root)
- `JOURNAL_DATE_FMT` — `strftime` format of the note filename, no `.md` (e.g. `%Y-%m-%d`)

A fixed path is deliberate: the old version asked the running Obsidian app where the daily note lived, which resolved against whatever vault was *active* and could yank focus to the wrong vault (the "forge" bug). The daily-notes plugin still creates the note from your template when Obsidian is open; the script only falls back to a plain empty file if the note doesn't exist yet.

## Steps

1. **Gather the facts.** Run the helper. It reads the live session id from the environment, finds the transcript, derives the start time, and points at today's note in the configured vault:

   ```bash
   ~/.claude/skills/save-session/scripts/session-info.sh [session-id]
   ```

   Omit the argument for the current session. Pass a session id to gather facts about a *different* session instead (the `session-recap` skill uses this to bookmark a past session it just summarized).

   It prints `SESSION_ID`, `PROJECT_DIR`, `PROJECT_NAME`, `START_LOCAL` (HH:MM, already converted from UTC to local), `DAILY_NOTE` (absolute path to today's note, created if missing), and `RESUME_BASE` (the resume command *without* the `--remote-control` name — you add that in step 3).

   If it errors that the journal vault wasn't found, the `CONFIGURE ME` block hasn't been set for this machine — surface the message and point the user at the Setup section above.

2. **Write the title yourself.** A short 2-3 word phrase naming what the session is about (e.g. "Otterly Insane mandate", "save-session skill", "N26 import fix"). If the user passed an argument, use it as the title. This same title doubles as the remote-control name, so it shows up on the phone — keep it recognizable.

3. **Read `DAILY_NOTE` and find the section this session belongs to.** The note is organised by topic, one `##` section per thing worked on. Judge from the content which section covers this session's work — same project, same task, same thread of thought. Match on meaning, not on matching words in the heading.

   - **A section fits and already has a resume block** → add one more entry (comment line + command) inside that same code block, in start-time order. Never open a second code block in the same section.
   - **A section fits but has no resume block yet** → append one resume block at the end of that section. No summary line: the section prose already says what happened. If the prose doesn't cover what this session did, extend *that* prose in the section's own voice rather than writing a separate summary.
   - **No section fits** → add a new `## Title` section at the end of the note, with a one-line summary of where things stand (concrete, not "worked on stuff"), then the resume block.
   - **An entry for this same `SESSION_ID` is already in the note** → update it in place (time, command, and any prose that's now stale) instead of adding a second one. Re-saving a session must never duplicate it.

   Use Read + Edit for the write — direct file edits give clean placement inside a section, which the CLI's blind append can't.

4. **The resume block** is one `bash` code block per section. Each session inside it is a comment line with the local start time and the title, then the command, with a blank line between sessions:

   ```markdown
   ```bash
   # 07:33 AB report update
   claude --resume 033fc39d-… --remote-control "AB report update"

   # 10:52 AB report audit
   claude --resume e18d23da-… --remote-control "AB report audit"
   ```
   ```

   No `_Claude session, HH:MM_` label line above the block; the comment carries the time. Build the command from `RESUME_BASE` plus `--remote-control "<Title>"`, reusing the *same* 2-3 word title so the journal entry and the phone session match. If the user explicitly says they don't want remote control, use `RESUME_BASE` alone.

   **Drop the `cd <dir> &&` prefix when `PROJECT_DIR` is the journal vault itself** (the common case); keep it for sessions from other projects so the command still lands in the right repo. Short lines stay on one line in Obsidian, which is the reason for the format.

5. **Confirm.** Tell the user which section it landed in and echo the resume command so they can copy it straight from the chat too.

## Notes

- **Portability**: the journal vault, folder, and date format are hardcoded in the `CONFIGURE ME` block at the top of `scripts/session-info.sh`. Anyone reusing this skill must edit those three lines for their own machine (see Setup).
- The note always lives in the configured journal vault, even when the session runs in a different project — that's deliberate, so sessions across all projects collect in one journal.
- There is no dedicated sessions section. Bookmarks live next to the writing about the same work, so the note stays organised by topic and a resume command never sits detached from its context.
- Two sessions on different topics land in two different sections. Two sessions on the same topic land in the same section, as two entries inside one code block. A stack of labelled single-command blocks reads as noise; one block per section reads as a list.
