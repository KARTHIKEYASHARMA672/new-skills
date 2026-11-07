---
name: interview
description: High-level interview to confirm direction and big-picture choices on a plan. Use when the user wants a quick alignment pass before going deeper. For risk-focused probing use poke-holes; for exhaustive depth use grill-me.
---

Run a **short, high-level** interview to confirm the shape of the plan. Goal: shared understanding of scope, intent, and the top-level choices — not implementation detail.

## How to ask

- Use the `AskUserQuestion` tool, **one question at a time**.
- **Number each question** sequentially across the interview (Q1, Q2, Q3…) by putting it at the start of the question text.
- For every question, **provide your recommended answer as the first option**, labeled "(Recommended)", with 1-3 alternatives. Put the tradeoff in each option's description.
- Skip anything already settled in the conversation or trivially answerable from the codebase (explore the code yourself instead).

## What to cover

Stay at the level of:
- Scope and out-of-scope
- Success criterion / what "done" looks like
- The 2-3 most consequential design choices (not every decision)
- Major constraints or non-negotiables

Do **not** drill into edge cases, failure modes, or implementation branches — that's `poke-holes` and `grill-me` territory.

## When to stop

Stop after ~3-6 questions, once you could summarize the plan back to the user and they'd agree. Then write a brief summary of the aligned direction (no full spec).
