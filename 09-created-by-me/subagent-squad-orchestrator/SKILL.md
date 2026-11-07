---
name: subagent-squad-orchestrator
description: Use when a large job needs parallel research/gathering/processing - launches 15-20 subagents in one batch, each briefed with role, exclusive scope, restriction, return format and verification, then consolidates their evidence into one deliverable. Prevents overlapping scopes, fabricated results, and consolidation chaos.
---

# Subagent Squad Orchestrator

Use the task tool with a squad, not serial chains. One batch = one message = N tool calls.

## 1. Dividing principle
Before any launch, draw your boundaries ON PAPER (temp file `.squad\briefs.md`):
- Split by SOURCE dimension (site cluster, repo list, folder, era) never by "half the task".
- Every unit gets: [ROLE] [SCOPE exclusive] [DO NOT] [RETURN FORMAT] [VERIFY].
- If two units could produce the same file at the same path, redraw scopes.

## 2. Brief template (paste in every agent prompt)
You are [ROLE] agent [n of N]. RESEARCH-ONLY unless told otherwise.
SCOPE: exactly these: [URLs / repos / dirs]
DO NOT: touch anything outside scope; no downloads unless instructed; no file writes.
RETURN: [SECTION 1 evidence list] [SECTION 2 findings] with VERIFIED claims only - do not fabricate; every URL must be one you actually fetched.
VERIFY: state for each claim HOW you verified (fetched page, raw URL 200, file exists).

## 3. Batch sizes
- 8 agents = single message batch (fast, easy).
- 15-20 = launch all; they cost tokens but wall-clock time plummets.
- Deep-dive follow-up: resume with task_id instead of new agents.

## 4. Consolidation rules (your job, not theirs)
- Collect all returns; build a plain table: claim | source | verification strength.
- DEDUPE by normalized name; drop everything with weak/no verification.
- Re-verify the DELTA only (the 10-20% that will actually ship) - fetch those yourself before final delivery.
- Single conflict between agents = you fetch it yourself; 3 conflicting claims = mark CONTESTED, print both with sources.

## 5. Failure handling
- Agent aborted/timeout: note the coverage hole, either re-brief ONE replacement agent with a tighter scope or fill the hole yourself with a few direct webfetch calls (cheaper).
- Agent reports claims without evidence: treat as 0% trustworthy.
- Never silently drop scope: report 'original plan vs actual coverage' in the final receipt.

## 6. Anti-patterns
- Launching agents before writing scopes (chaos by design).
- One prompt per agent that says "find the best skills on the internet" with no unit boundary - all agents return the same famous repos at 20x the cost.
- Telling agents to write files: they conflict. Files are the CONSOLIDATOR's job.
