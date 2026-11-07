---
name: explain-diff
description: Build a rich, self-contained interactive HTML page that teaches how a code change works — the background, intuition, implementation walkthrough, diagrams, and a quiz. Use when the user wants to understand or explain a diff, branch, or pull request in depth, saved as a dated HTML file outside the repo. Adapted from Geoffrey Litt's "explain-diff".
---

# explain-diff

Produce one long-form HTML page that teaches a reader how a specific code change works. Investigate the surrounding system first: the page should make sense to a beginner while still giving an experienced engineer a fast path to the changed behavior.

Not a raw diff dump — a narrative that builds understanding. For a general-purpose visual page use `to-html`; this skill is the focused "explain a change deeply, with a quiz" variant.

## Workflow

1. **Scope the change.** Use the current checkout, diff, branch, or PR as the source of truth. If the target is ambiguous, infer the most likely change and state the assumption on the page.
2. **Explore around it.** Read the relevant callers, tests, config, data models, and docs. Trace the old and new paths far enough to explain behavior, not file-by-file edits. Prefer checked-in examples and tests over speculation.
3. **Draft the narrative before writing HTML:** what motivated the change, how the old system behaved, the smallest useful mental model of the new behavior, how the code realizes it, and the edge cases and trade-offs.
4. **Write one self-contained HTML file** — inline CSS/JS, no external fonts, CDNs, images, or network. Save it outside the repo as `YYYY-MM-DD-explanation-<slug>.html` in a scratch dir — the session scratchpad if there is one, otherwise `mktemp -d`.
5. **Validate before handoff:** confirm the file exists, is a complete document with no external assets, has working quiz interactions, and passes the quiz and code-block checks below. Serve the temp dir over a throwaway local server and screenshot it (the browser blocks `file://`) rather than trusting the markup blind.

## Required page structure

A clear title, a short summary, and a table of contents linking these sections in order:

1. **Background** — only the system needed for the change. Optional beginner mental model first, then the exact components, contracts, and prior behavior involved.
2. **Intuition** — the core idea before implementation detail, with small concrete toy inputs/outputs. Show old vs new behavior when it makes the change clearer.
3. **Code** — walk the changes in conceptual groups, ordered by execution or dependency flow, not file order. Precise `file:line` references, but never the whole diff.
4. **Quiz** — exactly five medium-difficulty interactive multiple-choice questions. Clicking an option immediately shows whether it's correct and why, tied to the relevant behavior or code path.

Plain, precise, systems-oriented prose. Explain jargon on first use. Use callouts for definitions, invariants, edge cases, and consequences. Responsive on phones. One continuous page — no top-level tabs.

## Diagrams

Build diagrams from semantic HTML + CSS, never ASCII: flow diagrams for request/data/control flow, before/after panels for changed behavior, labeled component cards for boundaries, compact tables for mappings and toy data. Label arrows, include example values, and add a caption so the point survives without visual inspection.

## Quiz quality (the anti-gaming rules)

Treat the quiz as part of the explanation. The two fixes below come from feedback on the original — bake them in, don't leave them to chance. Inspect all five questions as a set before emitting the page:

- **Deterministic shuffle.** Randomize the option order independently per question using a per-page seed, and balance correct-answer positions across the five as evenly as possible. Never let position, letter, or a repeated pattern reveal the answer — the original's correct answer landed in the second slot far too often.
- **Length-matched options.** Keep options comparable in length, grammar, specificity, and confidence. The correct one must not be conspicuously longer, more qualified, or more precise than the distractors — shorten or enrich distractors until a reader can't pick the answer by size alone.
- Make every distractor plausible and tied to a real misconception about the change. No joke answers, "all/none of the above," or trivia not inferable from the page.
- Ask about behavior, causality, contracts, edge cases, or trade-offs — not something guessable from one copied phrase.
- Keep answers and explanations in the page's JS/DOM so it works offline; reveal feedback only after selection. Never leak correctness before a click via styling, DOM order, `title` attributes, or accessibility labels.

## HTML and code-block constraints

- Escape code-derived text for HTML and JS contexts; preserve meaningful whitespace.
- Code blocks use `<pre><code>…</code></pre>`, and the `pre` CSS must include `white-space: pre` or `pre-wrap` — verify every block in the saved source.
- Keep JS small, namespaced, dependency-free. Visible focus states, sufficient contrast, no meaning by color alone.
- Don't claim behavior the inspected source doesn't support; separate observed fact from interpretation.

## Handoff

Report the absolute path as a clickable local-file link, state what you inspected, and note any assumptions or validation limits. Nothing lands in the repo unless the user asks.
