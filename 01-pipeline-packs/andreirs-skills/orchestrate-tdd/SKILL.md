---
name: orchestrate-tdd
description: Drive a list of issues to completion test-first by spawning one agent per slice instead of coding yourself — size each slice, pick the model tier, run implement-tdd on it, then independently verify and review before advancing. Use when issues are ready (from to-issues, a file, or a tracker) and you want them built autonomously, one verified slice at a time. Pairs with to-issues, which produces the work-list.
---

# Orchestrate TDD

You are the **orchestrator**. You do not write the implementation. You ingest a list of issues, and for each one you size it, spawn an agent that builds it test-first, and independently verify the result before moving on. The agents follow red-green-refactor and commit on green; you drive the batch to the end goal.

If there is no issue list at all, stop and point the user at `to-issues` (to slice a plan into issues) or `grill-me` (to resolve a plan first).

## Roles, kept distinct

```
Orchestrator (you)   sizes, spawns, verifies, judges review findings, advances, writes status back
  ├─ Slice agent      runs implement-tdd on ONE slice, commits on green, reports back
  └─ Reviewer agent   (tier-gated) challenges the committed slice; proposes, never decides
```

You own orchestration. The slice agent owns the red-green-refactor cycle. The reviewer only proposes findings — you are the final judge of what gets fixed. Never blur the roles: you do not write tests or implementation, and the agents do not pick their own model or touch other slices.

## 1. Ingest the work-list

Detect the source the way `to-issues` does and normalize everything into one ordered work-list:

- **File** (path passed as arg): a markdown/checklist of issues.
- **Tracker**: GitHub (`gh`), GitLab (`glab`), Linear MCP, Jira, or a local CLI. Read the open, ready issues.
- **Conversation**: issues already discussed in this session.

For each item capture: **title**, **acceptance criteria**, **dependency order** (blocked-by), **attendance** (attended / unattended), and **complexity** if the source carries a label or estimate.

If the project has a domain glossary, `GLOSSARY.md`, or `docs/adr/`, skim the relevant parts so the slices you pass down use the project's vocabulary. If you are on the default branch, create one working branch for the whole batch.

## 2. Order and gate the batch

Sort by dependency order. Then, for each slice, decide who runs it:

- **Unattended** slices: you run autonomously.
- **Attended** slices (need a human decision, design review, or manual verification): **pause and hand to the user.** Do not auto-run them. Run the unattended slices around them and surface the attended ones when their turn comes.

## 3. Size each slice and pick the model

**Default to the most capable model (Opus). Drop to a cheaper, faster model only for slices that are unambiguously trivial.** Getting a real slice right on the first pass is cheaper end-to-end than a cheap miss plus a re-spawn, a failed verification, and a fix-up cycle — so the bar to leave Opus is high, and any doubt resolves toward Opus.

Before spawning, set the model tier:

1. **If the issue carries an explicit complexity label/field, honor it** (`complexity: trivial|simple|complex`, a story-point estimate, or similar) — but map anything above *trivial* to Opus.
2. **Otherwise judge from the issue text plus a quick codebase peek.** Use the cheap tier only when *every* trivial signal holds; if even one points to real work or judgment, use Opus.

| Tier | Model | Use when (ALL must hold) |
|---|---|---|
| Trivial | cheapest/fastest tier | Single file • well-trodden pattern already in the repo • ~one behavior • no design or interface decisions • nothing to figure out, only to type |
| Everything else | most-capable tier (Opus) | Anything not unambiguously trivial — multiple files, a new interface, an algorithm, cross-cutting changes, any design judgment, or simply any uncertainty about scope |

Use whatever model family the harness exposes for these two tiers; the point is "Opus unless trivial", not the specific names. State the tier and a one-line reason before spawning, e.g. `Slice 3 "date-range export filter" → Opus (new interface, touches export + query layers)` or `Slice 5 "add --json flag to existing list command" → cheap tier (single file, mirrors the existing --yaml flag)`.

## 4. Spawn the slice agent

Spawn one agent (via the `Agent`/`Task` tool) at the chosen model with this contract:

- **Scope**: the slice title + its acceptance criteria, and nothing else. It owns this one slice.
- **Discipline**: "Run `implement-tdd` on exactly this slice. One behavior at a time, real RED, minimum green, refactor while green."
- **Commit**: commit once, after refactor, on green — a single commit describing the slice (the `implement-tdd` close-the-slice rule). Do not commit per behavior.
- **Report back**: the commit SHA, the tests it added and that they pass, and which acceptance criteria each addresses.

One slice at a time, on the shared working branch. Do not fan out.

## 5. Verify independently — never trust the self-report

When the agent returns, confirm the slice is actually done before advancing:

- **Re-run the slice's tests yourself.** Confirm the suite is green, not just that the agent said so.
- **Review the commit diff** against the acceptance criteria — check each box is genuinely met, not merely claimed.
- **Sanity-check TDD discipline**: tests describe behavior through the public interface, not implementation; the RED was real (failed because the behavior was absent). If the tests look pinned to implementation or the RED looks fake, treat it as a failure.

Only proceed to review when verification passes.

## 6. Review the slice — tier-gated, you judge

A fresh-eyes review catches what the implementer is blind to. The refactor step already cleaned up *within* the slice; this is the team-style review pass on top. Gate it on the tier you already computed, so prototypes made of trivial slices stay cheap:

| Tier | Review |
|---|---|
| Trivial | **Skip** — your verification diff check is enough |
| Everything else | **Full**: spawn a reviewer that checks tests, then runs `code-review` (correctness bugs + complexity challenge) |

**Reviewer and fix-up agents run at Opus, regardless of slice tier.** Review is where the most-capable model pays off most — catching a subtle test or correctness flaw here is what saves the expensive downstream rework. (The only "cheap" path is the trivial-skip above, where there is no reviewer at all.)

Override with `--no-review` (force skip) or `--review-all` (force full review on every slice, including trivial).

**Review the tests first.** In TDD the tests are the spec and the most valuable artifact — a bad test is worse than messy code, because it gives false confidence and survives the refactor it should have caught. Before the code-quality pass, the reviewer challenges: do tests assert behavior through the public interface (not implementation)? Was the RED real? Are edge cases and failure modes covered? Is anything over-mocked? Then it reviews the implementation.

The reviewer **proposes**; you **judge** each finding:

```
trivial nit        → accept as-is, note it
worth fixing       → spawn a fix-up cycle (fresh agent, still TDD, stay green)
out of scope       → file as a new tracker issue, advance
```

A fix-up cycle is a **fresh** slice-agent spawn at Opus (fresh eyes — the original agent created the issue; and a review finding is exactly the kind of judgment call worth the best model), scoped to the findings. It stays test-first and lands changes as a **separate** `refactor(slice): address review` commit on top of the slice commit — the way a developer addresses review comments in a team. For a **correctness bug**, the fix-up first writes a test that reproduces the bug and *fails* (real RED), then makes it green, so the bug can never silently regress.

After the fix-up commit, **re-verify only (step 5) — do not re-review the same slice.** This is a hard stop against review/fix spirals; any issue the fix-up itself introduces is caught by verification or the final batch review. File out-of-scope findings as new issues on the tracker (so nothing is lost and they re-enter the normal flow) rather than fixing them here.

## 7. Handle failure: retry, escalate, then stop

If the agent returns red, or your verification fails:

```
1. If the slice ran on the cheap tier, re-spawn at Opus with the failure
   context (the miss means it wasn't trivial).
   If it already ran on Opus, re-spawn ONCE more at Opus with the failure
   context (what failed, what criterion is unmet, what the suite reported).
2. Still failing → STOP and surface the blocker to the user.
```

A repeated miss on Opus usually means the issue is under-specified or wrong, not that another model would fix it — so escalation tops out at one Opus retry, then a human.

Never loop forever. Never silently skip a slice and move on.

## 8. Write status back and advance

The moment a slice is verified green and committed, update the source of truth **incrementally**: close the GitHub/GitLab issue, move the Linear/Jira card, or check the box in the file. Then move to the next slice and return to step 3.

If the working directory is not a git repository, skip committing and write-back (do not run `git init`); tell the user once that there is no repo to commit to, and just drive the agents through the slices.

## 9. Final batch review

Per-slice review is blind to what accumulates *across* slices — slice 6 re-implementing what slice 2 built, or several slices growing parallel near-copies. Once every unattended slice is green and verified, spawn one **integration reviewer** over the whole branch diff to hunt cross-slice duplication, architectural drift, and inconsistent patterns. Skip this only under `--no-review`.

You judge the findings as in step 6: consolidation worth doing → a fix-up cycle (fresh agent, test-first, stay green, its own commit); out of scope → file as a tracker issue. Re-verify the full suite after any consolidation.

## 10. Close the batch

When the final review is resolved:

- Summarize: slices completed (with SHAs and the model each used), per-slice and batch review fix-ups applied, out-of-scope issues filed (with IDs), slices paused as attended, and any that stopped on failure with the blocker.
- The batch lives on one working branch — point the user at reviewing/opening the PR.

## When to pause and ask

Beyond attended slices and exhausted retries, stop and ask the user when:

- The work-list is ambiguous or an issue conflicts with what the code actually does.
- A slice balloons far beyond its issue's scope (consider asking `to-issues` to re-slice it).
- A verified result reveals a design problem worth resolving before continuing.
