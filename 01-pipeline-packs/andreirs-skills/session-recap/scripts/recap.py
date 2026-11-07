#!/usr/bin/env python3
"""Digest Claude Code session transcripts for a given day, across all projects.

Usage:
  python3 recap.py            # today (local date)
  python3 recap.py today
  python3 recap.py yesterday
  python3 recap.py 2026-06-28 # explicit YYYY-MM-DD

Output: human-readable digest grouped by project. Each session shows its time
span, how many messages landed on the target date, and the real user prompts
(commands, caveats and tool results are filtered out). Sessions whose content
does not touch the target date are skipped, even if the file was recently
modified (a resumed session bumps mtime without adding new-day content).
Prompts and the time span are scoped to the target day, so a session resumed
across several days only contributes that day's activity.
"""
import json
import os
import sys
import glob
from datetime import date, timedelta

PROJECTS = os.path.expanduser("~/.claude/projects")


def target_date(arg):
    if not arg or arg.lower() == "today":
        return date.today().isoformat()
    if arg.lower() == "yesterday":
        return (date.today() - timedelta(days=1)).isoformat()
    # explicit date — validate
    try:
        y, m, d = map(int, arg.split("-"))
        return date(y, m, d).isoformat()
    except Exception:
        sys.exit(f"Bad date arg: {arg!r}. Use today | yesterday | YYYY-MM-DD")


def user_text(msg):
    c = msg.get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return " ".join(
            b.get("text", "")
            for b in c
            if isinstance(b, dict) and b.get("type") == "text"
        )
    return ""


def is_real_prompt(msg):
    """A genuine user message, not a slash-command echo or tool result."""
    c = msg.get("content")
    if isinstance(c, list) and any(
        isinstance(b, dict) and b.get("type") == "tool_result" for b in c
    ):
        return False
    t = user_text(msg)
    if not t.strip():
        return False
    junk = (
        "<local-command",
        "<command-",
        "[tool",
        "Caveat",
        "[Image:",
        "[Request interrupted",
        "Base directory for this skill:",
    )
    return not any(j in t for j in junk)


def digest_file(path, day):
    try:
        rows = [json.loads(l) for l in open(path) if l.strip()]
    except Exception:
        return None
    ts = [r.get("timestamp") for r in rows if r.get("timestamp")]
    if not ts:
        return None
    today_ts = [t for t in ts if t.startswith(day)]
    if not today_ts:
        return None  # no content on the target day
    prompts = []
    for r in rows:
        if r.get("type") != "user":
            continue
        stamp = r.get("timestamp") or ""
        if not stamp.startswith(day):
            continue  # only this day's prompts
        m = r.get("message", {})
        if is_real_prompt(m):
            txt = user_text(m).strip().replace("\n", " ")
            prompts.append((stamp[:19], txt[:240]))
    return {
        "project": os.path.basename(os.path.dirname(path)),
        "sid": os.path.basename(path)[: -len(".jsonl")],
        "span": (today_ts[0][:19], today_ts[-1][:19]),
        "today_count": len(today_ts),
        "rows": len(rows),
        "prompts": prompts,
    }


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    day = target_date(arg)
    files = glob.glob(os.path.join(PROJECTS, "*", "*.jsonl"))
    sessions = [d for d in (digest_file(f, day) for f in files) if d]
    # sort by start of span
    sessions.sort(key=lambda d: d["span"][0])

    print(f"# Claude Code session recap for {day}")
    print(f"(timestamps are UTC; {len(sessions)} session(s) with content this day)\n")
    if not sessions:
        print("No sessions found with content on this date.")
        return
    # group by project
    by_proj = {}
    for s in sessions:
        by_proj.setdefault(s["project"], []).append(s)
    for proj, sess in by_proj.items():
        # tidy the project folder name -> path-ish
        label = proj.replace("-Users-razvan-surdu-", "~/").replace("-", "/")
        print(f"## {label}")
        for s in sess:
            print(
                f"- session {s['sid']} | {s['span'][0]} -> {s['span'][1]} "
                f"| {s['today_count']} msgs today | {len(s['prompts'])} prompts"
            )
            for stamp, p in s["prompts"]:
                print(f"    [{stamp[11:16]}] {p}")
        print()


if __name__ == "__main__":
    main()
