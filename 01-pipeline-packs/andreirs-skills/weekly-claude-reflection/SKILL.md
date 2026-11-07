---
name: weekly-claude-reflection
description: A weekly ritual to keep the instructions that steer Claude sharp. Scans memories and CLAUDE.md across all projects, finds patterns, and proposes promoting recurring lessons to global, pruning stale ones, deleting duplicates, and flagging conflicts. Use when the user says "weekly reflection", "reflect on how we work", "clean up my memories/CLAUDE.md", "/weekly-claude-reflection", or when it fires on a schedule. Nothing changes without confirmation.
argument-hint: "[autonomous]"
---

# Weekly Claude Reflection

A recurring retro on how you and Claude work together. Treat the steering config, every `CLAUDE.md` and memory file across all projects, as a living system that decays: capture the week's patterns, promote what recurs, prune what's stale, and leave the working agreement a little sharper than last week. Cleaning up is the mechanism, not the point.

**Two golden rules:** never touch `.env` or other secret-bearing files, and change nothing (no edit, no delete) without the user confirming it first.

## When to use

The user asks to "reflect on how we work", "run the weekly Claude reflection", "clean up my memories / CLAUDE.md", "/weekly-claude-reflection", or a scheduled routine invokes it (with the `autonomous` arg).

## Modes

- **Manual** (no arg): the user is in the session. Analyze, propose, and on approval, apply.
- **Autonomous** (`autonomous` arg): headless/scheduled. Analyze and write nothing to memories or CLAUDE.md. End by running `save-session` so a resume command lands in the daily note; the user reopens that session (analysis already in context) and decides what to apply. See step 6.

The deep read wants judgment: **run this on Opus or Fable.** On a weaker model, say so up front, results will be shallow.

## Steps

1. **Run the inventory helper** to get the mechanical facts and easy flags:
   ```bash
   python3 ~/.claude/skills/weekly-claude-reflection/scripts/inventory.py
   ```
   It scans every `~/.claude/projects/*/memory/*.md`, the global `~/.claude/CLAUDE.md`, and prints per-memory facts (project, name, days-old, bytes, type, description) plus flags: `STALE` (>90 days untouched), `GLOBAL_DUP` (a line that restates a global CLAUDE.md rule), and `CROSS_PROJECT` (same lesson appears in 2+ projects). It also prints the global CLAUDE.md size and honors the suppress-log (already-declined items are marked `SUPPRESSED`, don't re-surface them).

2. **Read full contents, don't trust the digest.** The script finds facts; patterns need reading. Read every memory file and every `CLAUDE.md` (global and, where relevant, per-project) in full. The whole picture is where patterns live. Only read session transcripts (`~/.claude/projects/*/*.jsonl`) if the user asked (or an arg requests it) or a candidate pattern needs evidence, they are expensive.

3. **Form the proposals** across four moves:
   - **Promote** — a lesson that **recurs in 2+ projects AND is domain-agnostic** (a working-style or communication habit, not a tech-specific fact). Proposal: add the rule to `~/.claude/CLAUDE.md`, then delete the now-redundant per-project memories and their `MEMORY.md` index lines.
   - **Prune** — a `STALE` memory (>90 days). Age is a prompt to review, not a verdict; evergreen facts (cycling pace, family) stay. Propose delete, never auto-delete.
   - **Dedupe** — a `GLOBAL_DUP` (verbatim restatement of an existing global rule). Propose delete of the copy + its index line.
   - **Deconflict** — a memory that contradicts a global rule, or two memories that disagree. Flag it; propose a resolution but let the user pick.
   Also watch for **project-specific bloat in global CLAUDE.md** (content that only matters in one project) and propose moving it to that project's memory or `CLAUDE.md`.

4. **Present, then apply on approval.** Batch the proposals into one decision prompt (`AskUserQuestion`, grouped by move). Apply only what the user approves: edit `~/.claude/CLAUDE.md`, delete files, and fix the affected `MEMORY.md` index lines. Never apply an unconfirmed change.

5. **Record.** Two artifacts under `~/.claude/reflection/`:
   - **DR** (`dr/NNNN-*.md`, Nygard Context/Decision/Consequences) only for a genuinely significant outcome, e.g. "promoted X to global CLAUDE.md". Not for routine keeps.
   - **Suppress-log** (`suppress-log.json`) for every "keep / declined" decision so the same item does not re-nag next week: `{key, decision, date, reason}`, keyed `project/memory-name`. Update it whenever the user declines or defers a flagged item.

6. **Autonomous handoff (autonomous mode only).** After analysis, apply nothing. Run the `save-session` skill so its resume command is written into today's daily note. Do not touch the suppress-log or DRs (those record user decisions, which haven't happened yet). The user resumes the saved session and continues from step 4.

7. **Offer to schedule (manual mode, if not already scheduled).** Ask whether to set a weekly routine via the `schedule` skill, default **Friday ~16:00**, pinned to Opus, invoking `/weekly-claude-reflection autonomous`. Confirm day/time with the user.

## Notes

- Per-project memories only load in their own project's sessions; the global `CLAUDE.md` loads everywhere. So slimming global CLAUDE.md is the highest-leverage move, weight it accordingly.
- On promote, the payoff is net-negative context: one global rule replaces N project copies. Always delete the copies, don't leave both.
- If the inventory is clean (nothing flagged, no pattern), say so plainly. A quiet week needs no changes and no retro note.
- Keep proposals concrete: name the file, the exact rule text, and which index lines change, so the user is approving something specific.
