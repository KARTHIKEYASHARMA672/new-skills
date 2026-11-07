# Implementation Notes — <task name>

> Maintained by the agent during implementation. Purpose: record where execution was forced to deviate from the plan, as learning material for the next attempt and raw material for the post-implementation pitch.
> Usage: in a new session, pass the plan / spec / prototype back in as artifacts, then have the agent keep this file updated throughout.

## Plan baseline

- **Plan / spec source**: <link or file path>
- **Key assumptions at the start**: <the key premises carried over from the plan>

## Deviations

> When an edge case forces a deviation from the plan, pick the conservative option and log a row here: **what happened → why you deviated → which option you took → impact**.

| # | Location / trigger | Original plan | What was done (conservative option) | Why | Impact / to confirm |
|---|--------------------|---------------|--------------------------------------|-----|---------------------|
| 1 | <file:line / scenario> | <what the plan said> | <what was actually done> | <the edge case> | <needs a human decision?> |

## New unknowns that surfaced

> Unknown unknowns exposed only during execution. These are what the next pre-implementation pass should tackle first.

- <newly discovered issue that wasn't considered at the start>

## Decisions that need a human

> The conservative option only means "don't break anything for now" — these still need your sign-off.

- [ ] <decision point + which way you lean>
