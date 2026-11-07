#!/usr/bin/env python3
"""Mechanical inventory for the weekly-claude-reflection skill.

Prints the facts and easy flags; the model reads full file contents for the
judgment (patterns, promote, deconflict). Never edits anything.

Facts: every ~/.claude/projects/*/memory/*.md (project, name, days-old, bytes,
type, description) plus the global ~/.claude/CLAUDE.md size.

Flags (per memory):
  ORPHANED    - the project's folder no longer exists on disk, so these memories
                can never load again (per-project memories only load in their own
                cwd); the whole memory dir is dead weight and safe to delete
  STALE       - not modified in > STALE_DAYS days
  GLOBAL_DUP  - a body line restates a line already in global CLAUDE.md
  CROSS_PROJECT - the same lesson (by description keywords) appears in 2+ projects
  SUPPRESSED  - user already declined this item (from suppress-log.json); skip it
"""

import glob
import json
import os
import re
import time

HOME = os.path.expanduser("~")
PROJECTS = os.path.join(HOME, ".claude", "projects")
GLOBAL_CLAUDE_MD = os.path.join(HOME, ".claude", "CLAUDE.md")
SUPPRESS_LOG = os.path.join(HOME, ".claude", "reflection", "suppress-log.json")

STALE_DAYS = 90
DUP_MIN_LEN = 25          # ignore short generic lines when matching global dups
CROSS_MIN_PROJECTS = 2    # a lesson must span this many projects to flag

STOP = set("""a an the and or but of to in on for with without your you our we
i it is are be as by from that this these those do not never always only when
where what how use used using into onto over under off per via not don't dont
should must can will if then else than about across also any each every some
""".split())


def days_old(path):
    return int((time.time() - os.path.getmtime(path)) / 86400)


def read(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def project_name(encoded_dir):
    """~/.claude/projects/-Users-razvan-surdu-Projects-minuto -> Projects-minuto-ish."""
    base = os.path.basename(encoded_dir)
    for prefix in ("-Users-razvan-surdu-Projects-", "-Users-razvan-surdu-"):
        if base.startswith(prefix):
            return base[len(prefix):] or base
    return base


def resolve_project_path(encoded_dir):
    """Decode a ~/.claude/projects/<encoded> dir back to its real filesystem path.

    The encoding is lossy: '/', '.', and '-' in the original path all become '-',
    so string-replacement can't invert it (e.g. 'innogames-forge' might be
    'innogames/forge' or 'innogames-forge', and 'razvan-surdu' is 'razvan.surdu').
    Walk the real filesystem instead: at each level, match actual directory entries
    (normalizing their own '.'/'-' to tokens) against the remaining tokens.

    Returns the resolved directory path, or None if no such folder exists.
    """
    base = os.path.basename(encoded_dir)
    tokens = [t for t in base.split("-") if t]  # drop the leading empty token

    def rec(path, toks):
        if not toks:
            return path if os.path.isdir(path) else None
        try:
            entries = os.listdir(path)
        except OSError:
            return None
        for entry in entries:
            etoks = [t for t in re.split(r"[-.]", entry) if t]
            k = len(etoks)
            if k and k <= len(toks) and etoks == toks[:k]:
                found = rec(os.path.join(path, entry), toks[k:])
                if found:
                    return found
        return None

    return rec("/", tokens)


def parse_memory(path):
    """Return (type, description, body) from a memory md file with frontmatter."""
    text = read(path)
    mtype, desc = "", ""
    body = text
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if m:
        front, body = m.group(1), m.group(2)
        for line in front.splitlines():
            line = line.strip()
            if line.startswith("description:"):
                desc = line.split(":", 1)[1].strip().strip('"').strip("'")
            elif line.strip().startswith("type:"):
                mtype = line.split(":", 1)[1].strip()
    return mtype, desc, body


def norm_line(line):
    return re.sub(r"[^a-z0-9 ]", "", line.lower()).strip()


def keywords(text):
    return {w for w in re.findall(r"[a-z]{4,}", text.lower()) if w not in STOP}


def load_suppressed():
    data = read(SUPPRESS_LOG)
    if not data:
        return set()
    try:
        parsed = json.loads(data)
    except json.JSONDecodeError:
        return set()
    return {e.get("key") for e in parsed.get("suppressed", []) if e.get("key")}


def main():
    suppressed = load_suppressed()

    # Global CLAUDE.md: size + normalized rule lines for dup detection.
    gtext = read(GLOBAL_CLAUDE_MD)
    glines = gtext.splitlines()
    g_words = len(gtext.split())
    g_norm = {norm_line(l) for l in glines if len(norm_line(l)) >= DUP_MIN_LEN}

    mem_paths = sorted(glob.glob(os.path.join(PROJECTS, "*", "memory", "*.md")))
    orphan_cache = {}  # encoded project dir -> True if folder is gone
    memos = []
    for path in mem_paths:
        if os.path.basename(path) == "MEMORY.md":
            continue
        proj_dir = os.path.dirname(os.path.dirname(path))
        proj = project_name(proj_dir)
        if proj_dir not in orphan_cache:
            orphan_cache[proj_dir] = resolve_project_path(proj_dir) is None
        name = os.path.basename(path)[:-3]
        mtype, desc, body = parse_memory(path)
        key = f"{proj}/{name}"
        flags = []
        if key in suppressed:
            flags.append("SUPPRESSED")
        if orphan_cache[proj_dir]:
            flags.append("ORPHANED")
        if days_old(path) > STALE_DAYS:
            flags.append("STALE")
        if any(norm_line(l) in g_norm for l in body.splitlines()
               if len(norm_line(l)) >= DUP_MIN_LEN):
            flags.append("GLOBAL_DUP")
        memos.append({
            "key": key, "proj": proj, "name": name, "path": path,
            "days": days_old(path), "bytes": os.path.getsize(path),
            "type": mtype or "?", "desc": desc,
            "kw": keywords(desc + " " + name.replace("_", " ").replace("-", " ")),
            "flags": flags,
        })

    # CROSS_PROJECT: cluster memories that share >=3 keywords across >=2 projects.
    for i, a in enumerate(memos):
        peers = set()
        for j, b in enumerate(memos):
            if i == j or a["proj"] == b["proj"]:
                continue
            if len(a["kw"] & b["kw"]) >= 3:
                peers.add(b["proj"])
        if peers and "SUPPRESSED" not in a["flags"]:
            a["flags"].append("CROSS_PROJECT(" + ",".join(sorted(peers)) + ")")

    # Report
    print("=== GLOBAL ~/.claude/CLAUDE.md ===")
    print(f"lines={len(glines)} words={g_words} est_tokens~{len(gtext)//4}")
    print()
    projects = sorted({m["proj"] for m in memos})
    print(f"=== MEMORIES: {len(memos)} files across {len(projects)} projects ===")
    print(f"stale_threshold={STALE_DAYS}d  suppressed_entries={len(suppressed)}")
    print()
    for proj in projects:
        rows = [m for m in memos if m["proj"] == proj]
        print(f"## {proj} ({len(rows)})")
        for m in rows:
            flag = ("  [" + " ".join(m["flags"]) + "]") if m["flags"] else ""
            print(f"  - {m['name']}  ({m['days']}d, {m['bytes']}b, {m['type']}){flag}")
            if m["desc"]:
                print(f"      {m['desc']}")
        print()

    flagged = [m for m in memos if m["flags"] and "SUPPRESSED" not in m["flags"]]
    print(f"=== FLAG SUMMARY: {len(flagged)} memories flagged (excl. suppressed) ===")
    for tag in ("ORPHANED", "STALE", "GLOBAL_DUP", "CROSS_PROJECT"):
        hits = [m["key"] for m in flagged if any(f.startswith(tag) for f in m["flags"])]
        print(f"{tag}: {len(hits)}")
        for k in hits:
            print(f"  - {k}")
    print()
    print("NEXT: read full contents of flagged files + all CLAUDE.md before proposing.")


if __name__ == "__main__":
    main()
