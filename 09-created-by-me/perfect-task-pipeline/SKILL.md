---
name: perfect-task-pipeline
description: Use when the user gives any non-trivial task ("do X", "make X", "research X and produce X") and wants it done perfectly end-to-end - turns one vague request into a gated 7-stage pipeline: INTAKE, CLARIFY, PLAN, SQUAD, EXECUTE, VERIFY, DELIVER - with quality gates between stages and a written receipt at the end.
---

# Perfect Task Pipeline

Goal: deliver the SAME task once, verified, with zero re-work loops. Every stage has a hard exit gate. Do not skip a gate "because it seems obvious". If a gate is blocked, ship the blocker as output - do not silently degrade.

## Stage 0 - INTAKE (2 min)
1. Restate the task in one sentence: "You want [artifact] based on [source], defined by [success criteria]."
2. Write it at the top of a working file `.pipeline/NOW.md` (create the folder). Include: Task / Inputs / Constraints / Output format / Deliverable location.
3. GATE: if three or more words in the request are ambiguous (number, location, format, audience, depth), go to Stage 1. Otherwise skip to Stage 2.

## Stage 1 - CLARIFY (max 5 questions)
1. Batch 3-5 concrete questions to the user. One round only. Never ask a question you can answer by testing, searching, or reading a file.
2. Auto-answer what you can first (try: file system probe, short web search, inspect similar past work like folder names/docs on disk).
3. Record answers into `.pipeline/NOW.md`. If the user says "you decide", YOU decide and say so: "Assumed X because Y."
4. GATE: decision table in NOW.md - every ambiguity resolved or explicitly assumed.

## Stage 2 - PLAN (write it, don't think it)
1. Write `.pipeline/PLAN.md`:
   - Milestones (max 5, each with "done = ..." evidence)
   - Build order (dependencies first)
   - Risk list (top 3 what-can-kill-this)
   - Tool map: which commands / subagents / scripts each milestone needs (Windows PowerShell where relevant)
2. Include a DISCARD plan: what is cut if time/context runs out (mark [must] / [nice]).
3. GATE: every milestone has executable verification ("run X, expect Y"). If a milestone has no test, it is not planned.

## Stage 3 - SQUAD (parallelize with the task tool)
1. Identify independent work units (research, downloads, file ops, verification) - plan a subagent per unit with:
   [ROLE] + [SCOPE: exact files/dirs/sites] + [DO NOT] + [RETURN FORMAT] + [VERIFY: how]
2. Launch in one parallel batch (up to 15-20). Sequential calls only when units depend on each other.
3. GATE: every agent returns evidence (paths, counts, checksums, URLs). Never accept "done" without proof.

## Stage 4 - EXECUTE
1. Do the critical-path work yourself (main agent owns the spine).
2. Subagents own bulk units. Collect results as they land.
3. Write progress ticks into `.pipeline/PROGRESS.md`: `[x] milestone - date - proof-path`.
4. On failure: fix at the root. Rule: 3 failed fixes on one error = stop and rethink the approach (architecture problem, not effort problem).

## Stage 5 - VERIFY (the enemy is silent breakage)
Run actual checks, in this order:
1. Existence: deliverable exists at the promised path (Test-Path / Get-ChildItem counts).
2. Integrity: metrics match claims (counts, sizes, zip opens).
3. Function: open / run it. PDF: check page count and first-page content. App: build + run. Data: row counts + spot-check values.
4. Cleanliness: no temp/junk files, no leaked secrets, names as promised.
5. GATE: all checks green, or the deviation is documented in the receipt with an honest "what's off" section. Never claim done-higher-than-reality.

## Stage 6 - DELIVER (one receipt, everything attached)
1. Send a single receipt to the user, in this template, matching THEIR requested format:
   - One line: what was delivered and where
   - Proof: file counts / test results / verification output (quote the command output)
   - Deviations: what differs from the original plan and why (or say none)
   - Next steps (only if open questions remain)
2. Land the artifacts in one clean folder, and archive: compress to .zip if more than ~10 files.
3. Delete-the-noise rule: clean staging before finishing.

## Anti-patterns (caught repeatedly; do not do)
- Verbose summaries instead of a file: "I did everything" with no artifact path.
- Secrets/keys echoed into output files.
- Parallel agents touching overlapping paths (conflicts) - scope strictly disjoint.
- Re-cloning over and over instead of diagnosing one clone failure.
- Skipping verification because "it's clear it works".
