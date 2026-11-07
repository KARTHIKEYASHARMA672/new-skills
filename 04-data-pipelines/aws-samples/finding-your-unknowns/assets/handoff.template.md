# <change name> — Handoff

> Used post-implementation. Purpose: let reviewers start from the same unknowns you had and catch up fast; let experts confirm you've considered the failure points they'd anticipate.
> Usage: have the agent package prototype + spec + implementation-notes into this one doc, leading with the demo.

## At a glance (lead with the demo)

- **Demo**: <demo GIF / screenshot / clickable link>
- **One line**: <what this change does, and for whom it solves what>

## Background: the unknowns going in

> Reviewers most likely start where you did. List what was unclear to you at the outset and how you resolved it, so they don't have to walk it again.

- <what was uncertain at the start → how it was settled>

## What was done

- **Scope**: <modules / files touched>
- **Key decisions**: <the few decisions most likely to be questioned or that need sign-off, one line of "why" each>
- **Deviations from the plan**: <the highlights pulled from the Deviations section of implementation-notes>

## Anticipated failure points & how they're handled

> The "did you consider X?" questions an expert will ask. Answer them proactively.

| Possible concern | Handled? | How / why it's acceptable |
|------------------|----------|---------------------------|
| <edge case / performance / security / compatibility> | Yes / Partial / No | <explanation> |

## Still open

- [ ] <what the reviewer / team needs to decide>
