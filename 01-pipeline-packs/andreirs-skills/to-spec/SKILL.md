---
name: to-spec
description: "Capture the why and what of a product, feature, or idea into a lean six-section markdown spec under docs/specs/. Use when the user wants to write a spec or PRD, turn a discussed plan into a durable document, or record the problem and proposed solution before slicing into issues. Capture-first: structures what's already been decided, asks only for missing required pieces."
---

# To Spec

Turn a discussed plan into a lean, durable spec file under `docs/specs/`.

This skill is **capture-first**. The thinking has usually already happened (in this conversation, a `grill-me` session, or the user's head). Your job is to *structure what's been decided*, not to re-interview. Pull everything already settled into the six sections, then ask the user only for **required** sections that are still empty.

If almost nothing has been decided yet, don't try to elicit it all here — point the user at `interview` (quick alignment), `poke-holes` (risk probing), or `grill-me` (exhaustive) first, then come back.

## The spec format

Six sections. Four required, two optional. Pure markdown, no front matter, no status field, no changelog — git is the history.

```markdown
# <Title>

## Problem

What's broken, and why it matters. The heart of the spec.

End with a confidence label and (optionally) the sources behind it:

**Confidence:** assumption | anecdotal | data-backed
**Sources:** <optional — what backs the confidence level>

## Solution

The high-level approach. *How* we mean to tackle it, in prose. Not a task
breakdown (that's `to-issues`) and not an enumeration of features (that's Scope).

## Scope

### In scope

Classic user-story bullets — the concrete capabilities this delivers:

- As a <role>, I can <do something> so that <benefit>.

### Out of scope

The explicit non-goals. State plainly what was deliberately decided *not* to do.

## Success Criteria

Observable signals that the Problem is actually solved. How we'll know it worked.

## Constraints *(optional)*

Non-negotiables the solution must respect: must use X, can't touch Y, perf /
security / compliance bars. Reference GLOSSARY.md for domain terms rather than
redefining them.

## Open Questions / Risks *(optional)*

Honest unknowns and risks. Each becomes a decision point downstream.
```

### Section discipline

- **Problem** is the heart — get it right before anything else. Always attach a **confidence label** (`assumption` = we believe it, no proof; `anecdotal` = a few signals; `data-backed` = metrics or a study). One label per Problem; if there are genuinely distinct sub-problems, handle them in prose. Sources are optional but strengthen a weak-looking confidence level. A weak problem isn't forbidden — labelling it honestly is the point.
- **Solution vs Scope** never restate each other. Solution = the *approach* (the strategy, in prose). Scope/in = the *capabilities* (enumerated user stories that feed `to-issues`). Different altitudes.
- **Out of scope** is required, not decorative. An empty out-of-scope usually means the boundary hasn't been thought through, not that nothing is excluded. Actively ask: "what did you deliberately decide *not* to do here?"
- **Constraints / Open Questions** are optional — omit the heading entirely if there's nothing real to put under it. Don't pad.

## Process

### 1. Read the surroundings

- If `docs/specs/product.md` exists and you're writing a *feature* spec, read it for context — inherit its domain framing and don't restate the product-level problem. Do **not** add a link to it (files get renamed and deleted; avoid link rot).
- If `GLOSSARY.md` or `docs/adr/` exist, read them so the spec uses the project's real terms and the Solution doesn't contradict a recorded decision.

### 2. Decide the target file (infer, then confirm)

Infer from context and **confirm the path before writing**:

- No `docs/specs/` yet → propose `docs/specs/product.md` (the product-wide spec).
- A specific feature/change under discussion → propose `docs/specs/<slug>.md`.
- A matching existing spec → propose **updating** it in place (edit, don't duplicate).

Create the `docs/specs/` folder lazily, on first write. No numbering — these files get versioned and deleted freely, so sequence numbers would just leave gaps.

### 3. Draft from what's known

Fill every section you can from the conversation and the files you read. **Adapt the granularity to the scope**: a product spec paints in broad capability themes; a feature or idea spec is tighter and more concrete. Same six sections either way — leaner when the subject is smaller.

### 4. Ask only for the gaps

Ask the user only about **required** sections still empty or thin — most often a missing confidence label or an empty out-of-scope. Don't ask about optional sections; just omit them. Don't re-ask anything already settled in context.

### 5. Flag, don't formalize

While capturing, watch for two things and **flag them without acting**:

- a **fuzzy or overloaded term** → suggest the user run `domain-docs` to give it a canonical definition.
- the Solution resting on a **hard-to-reverse decision** → note it (often as an Open Question) and suggest recording it as an ADR via `domain-docs`.

Never write `GLOSSARY.md` or ADRs yourself — that's `domain-docs`' job. Stay a pure capture tool.

### 6. Write and hand off

Write the file, then tell the user the path and what's next: the spec feeds **`to-issues`**, which slices it (in-scope stories → slices, success criteria → acceptance criteria, open questions → attended decision slices).
