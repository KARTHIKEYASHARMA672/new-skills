---
name: wrap-up
description: Close out the session with a short summary in chat. Use on /wrap-up, "wrap up the session", "we're done for today", "summarize what we did". Not for "wrap X in Y" code requests. Writes nothing; for a doc a fresh agent can pick up, use handoff.
---

Print a wrap-up of this session to the chat. Do not write a file.

Cover the whole session under one dominant goal; mention side-quests in a line rather than giving them their own block. Works for code sessions and for discussion, research, or planning sessions.

## Sections

**What got done** — plain bullets.

**Why** — two lines: what triggered the session, then the deeper motivation behind it. If the motivation was never stated, write your best inference and label it as inferred.

**Files** — run `git status --short` and `git log` for this session's commits, and use that as the base. Add files touched outside the repo (Obsidian, `~/.claude`, elsewhere) from memory. Brief overview, not a per-file changelog. Say `none this session` when nothing changed.

**Decisions** — decisions reached and options ruled out. In a discussion session this carries most of the value.

**Open** — unresolved issues, plus anything written but never executed.

**Next** — one concrete step. Name a skill if one fits.

## Rules

- Aim to fit one screen.
- On a thin or mid-task session, drop the six sections and give two or three honest lines instead: what it was about, where it stands, what is next. Say plainly when work is mid-flight rather than finished.
- Do not offer follow-up skills beyond the Next line.
