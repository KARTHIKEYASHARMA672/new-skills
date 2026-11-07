---
name: grill-me
description: Interview the user relentlessly about a plan or design until every branch of the decision tree is resolved. Use when the user wants exhaustive depth and a full spec at the end. For lighter passes use interview (high-level) or poke-holes (risk-focused).
---

Interview the user relentlessly about every aspect of the plan until you reach a shared understanding deep enough to write a full spec. Walk down each branch of the design tree, resolving dependencies between decisions one at a time.

## How to ask

- Ask in chat, **one question at a time**. Pick the shape that fits the question: a closed choice, an open question, or a direct challenge to something the user said.
- **Number each question** sequentially across the interview (Q1, Q2, Q3…).
- Say what you would do and why, then ask. Name the real alternatives and the tradeoff between them so the user can just pick or push back.
- Go in dependency order: resolve upstream decisions before the ones that depend on them.
- Keep questions non-obvious. Skip anything trivial or already settled.
- Follow the answer where it goes. If a reply opens a new branch or contradicts an earlier one, chase that instead of returning to your list.

## When to explore instead of ask

If a question can be answered by reading the codebase, **explore the codebase yourself** rather than asking. Only ask the user about things that genuinely require their judgment, taste, or knowledge of intent.

## What to cover

Technical implementation, UI/UX, data model, edge cases, failure modes, scope boundaries, tradeoffs, and dependencies. Push on assumptions, not just open choices.

## When to stop

Stop when every branch of the decision tree is resolved and you could write the spec without further input. Then hand off rather than writing the spec yourself:

- **Always** point the user at `to-spec` to capture the resolved plan into a lean spec under `docs/specs/`. The decisions are already in this conversation, so `to-spec` can structure them directly without re-asking.
- **When fuzzy terms or hard-to-reverse decisions surfaced** during the grilling, also point at `domain-docs` to record them (a canonical glossary entry in `GLOSSARY.md`, or an ADR in `docs/adr/`).

Don't write `GLOSSARY.md`, ADRs, or the spec file inline — those are the jobs of `domain-docs` and `to-spec`. Your job is to resolve the decision tree; offer to invoke them next.
