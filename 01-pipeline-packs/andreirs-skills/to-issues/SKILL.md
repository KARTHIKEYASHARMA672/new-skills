---
name: to-issues
description: Break a plan or spec into independently-grabbable issues on the project issue tracker using thin vertical slices. Use when the user wants to convert a plan into issues, create implementation tickets, or break down work into issues.
---

# To Issues

Break a plan into independently-grabbable issues using vertical slices.

## Process

### 1. Gather context

Work from the conversation context. If the user passed an issue reference (number, URL, or path), fetch it and read the full body and comments.

### 2. Explore the codebase (optional)

If you haven't already, skim the codebase so titles and descriptions use the project's domain vocabulary and respect any ADRs in the area you're touching.

### 3. Draft slices

A slice cuts end-to-end through whatever layers the change actually touches, not horizontally across one layer.

**Test for a good slice**: could one person pick it up, merge it, and have nothing left to wire up? If no, it's incomplete. If yes but it would take three weeks, split it.

"Layers" means whatever the change actually involves. For most feature work that's schema + API + UI + tests. For a refactor it's the call sites being migrated. For infra it's config + provisioning + observability + rollback. For a research spike there's no path to complete, so produce one slice per question with a written finding or prototype as the deliverable.

<slice-rules>
- A finished slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
- Slices should be independently grabbable in dependency order
</slice-rules>

#### Attendance

Each slice is **attended** (needs a human at some point: architectural decision, design review, manual verification, spike write-up) or **unattended** (an AFK agent can implement and merge it without human input).

Prefer unattended.

If a slice needs a human only at one specific moment, **split it**: a small attended decision/review slice + an unattended implementation slice that depends on it. This keeps the AFK-readiness signal honest.

### 4. Quiz the user

Present the breakdown as a numbered list. For each slice show:

- **Title**
- **Effort**: XS / S / M / L / XL (see anchors)
- **Attendance**: attended / unattended
- **Depends on**: which other slices, if any
- **User stories covered**: if the source material has them

Effort estimates the tokens/time an agent spends to complete the slice. Uncertainty (vague spec, pending decisions, unknown code) drives this up, so it's folded in rather than a separate field.

<effort-anchors>
- **XS** seconds, one obvious change, no exploration
- **S** minutes, contained, spec is clear
- **M** some files to discover, a few decisions all answerable from context
- **L** lots of context to load, multiple touchpoints, back-and-forth likely
- **XL** so much exploration or so many unknowns it should probably be split
</effort-anchors>

An L/XL slice that's big because of unknowns is the signal to split off an attended decision slice first.

Then ask only about the dimensions you're least confident on (granularity, dependencies, splits/merges, attendance). Don't ask all four every time. Iterate until the user approves.

### 5. Publish

Detect the issue tracker from project context (`gh` CLI, Linear MCP, Jira, etc.). Labels and blocker conventions are project-specific, read them from CLAUDE.md or recent issues rather than assuming.

Publish in dependency order so "Blocked by" can reference real IDs. Apply the project's triage / ready-for-AFK label unless told otherwise. Also apply a `size/XS`..`size/XL` label matching the slice's effort (create the label if the tracker lacks it).

If a publish call fails mid-way, stop and report which issues were created (with IDs) and which weren't, so the user can retry, patch references manually, or roll back.

Use this body template:

<issue-template>
## Parent

Reference to the parent issue (omit if the source wasn't an existing issue).

## Effort

XS / S / M / L / XL — expected tokens/time for an agent to complete.

## What to build

The end-to-end behavior of this slice, not layer-by-layer implementation.

No file paths or code, except a prototype snippet that captures a decision more precisely than prose (schema, state machine, type shape). Trim to the decision-rich parts.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

Reference to the blocking ticket(s), or "None - can start immediately".

</issue-template>

Do NOT close or modify any parent issue.
