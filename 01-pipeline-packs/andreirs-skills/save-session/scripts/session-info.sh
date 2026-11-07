#!/usr/bin/env bash
# Print facts about a Claude Code session as KEY=VALUE lines.
#
# Usage: session-info.sh [session-id]
#   - no arg: the current session (from CLAUDE_CODE_SESSION_ID)
#   - session-id: that specific session (used by the session-recap skill)
#
# Resolves the session id from the argument or environment, locates its
# transcript, derives the start time (UTC -> local) and a resume command, and
# points at today's daily note in the journal vault configured below.
#
# ┌─ CONFIGURE ME ──────────────────────────────────────────────────────────┐
# │ This skill writes to ONE fixed journal vault, hardcoded here. Change     │
# │ these three lines to point at your own vault / daily-note folder / date  │
# │ format. We use a fixed path on purpose: asking the running Obsidian app  │
# │ resolves against whatever vault is *active* and can yank focus to the    │
# │ wrong vault (that was the "forge" bug).                                   │
# └──────────────────────────────────────────────────────────────────────────┘
JOURNAL_VAULT="$HOME/Brain"   # absolute path to the vault holding your journal
JOURNAL_FOLDER="10-journal"   # daily-notes folder inside the vault ("" = root)
JOURNAL_DATE_FMT="%Y-%m-%d"   # strftime format of the note filename (no .md)

set -euo pipefail

# --- session id ---------------------------------------------------------------
# An explicit id as $1 wins (used by session-recap to bookmark a past/other
# session); otherwise fall back to the current session from the environment.
sid="${1:-${CLAUDE_CODE_SESSION_ID:-}}"
if [ -z "$sid" ]; then
  echo "ERROR: no session id given and CLAUDE_CODE_SESSION_ID is not set — pass a session id, or run inside a Claude Code session." >&2
  exit 1
fi

# --- transcript ---------------------------------------------------------------
# Lives under ~/.claude/projects/<encoded-cwd>/<session-id>.jsonl. Glob by id so
# we never have to reproduce the path-encoding scheme.
# `|| true`: a no-match glob makes the pipeline fail under pipefail, which would
# exit before the friendly check below — swallow it so the [ -z ] error fires.
transcript="$(ls -t "$HOME"/.claude/projects/*/"$sid".jsonl 2>/dev/null | head -1 || true)"
if [ -z "$transcript" ]; then
  echo "ERROR: no transcript found for session $sid." >&2
  exit 1
fi

# --- project dir + name -------------------------------------------------------
# Use the cwd recorded in the transcript (robust even if you cd'd around).
# -m1: grep stops after the first match and exits 0, so it isn't killed by
# SIGPIPE when the downstream closes the pipe early (fatal under pipefail).
cwd="$(grep -o -m1 '"cwd":"[^"]*"' "$transcript" | head -1 | sed 's/.*:"//; s/"$//')"
proj="${cwd:-$PWD}"
name="$(basename "$proj")"

# --- start time (UTC -> local), cross-platform --------------------------------
# Timestamps are UTC ISO8601 with milliseconds + trailing Z, e.g.
# 2026-06-30T13:59:36.887Z. Strip to whole seconds, then format in local time.
ts="$(grep -o -m1 '"timestamp":"[^"]*"' "$transcript" | head -1 | sed 's/.*:"//; s/"$//')"
clean="${ts%.*}"
if start_local="$(date -d "${clean}Z" "+%H:%M" 2>/dev/null)"; then
  : # GNU date
elif epoch="$(date -j -u -f "%Y-%m-%dT%H:%M:%S" "$clean" "+%s" 2>/dev/null)"; then
  start_local="$(date -r "$epoch" "+%H:%M")" # BSD/macOS date
else
  start_local="??:??"
fi

# --- resume command (without the --remote-control name) -----------------------
# The remote-control name should describe the *session*, not the folder, so the
# skill appends --remote-control "<short title>" using the title it generates.
resume_base="cd $proj && claude --resume $sid"

# --- daily note (fixed journal vault, see CONFIGURE ME above) -----------------
if [ ! -d "$JOURNAL_VAULT" ]; then
  echo "ERROR: journal vault not found at $JOURNAL_VAULT — edit JOURNAL_VAULT at the top of $0." >&2
  exit 1
fi
daily="$JOURNAL_VAULT${JOURNAL_FOLDER:+/$JOURNAL_FOLDER}/$(date "+$JOURNAL_DATE_FMT").md"

# Create the note if it's missing so the skill can edit it. The daily-notes
# plugin normally makes it (with your template) when Obsidian is open; this
# fallback is a plain file so we never open the app / steal focus.
if [ ! -f "$daily" ]; then
  mkdir -p "$(dirname "$daily")"
  : > "$daily"
fi

cat <<EOF
SESSION_ID=$sid
PROJECT_DIR=$proj
PROJECT_NAME=$name
START_LOCAL=$start_local
DAILY_NOTE=$daily
RESUME_BASE=$resume_base
EOF
