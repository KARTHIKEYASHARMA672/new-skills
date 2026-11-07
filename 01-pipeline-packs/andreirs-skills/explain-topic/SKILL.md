---
name: explain-topic
description: Build a rich, self-contained interactive HTML page that teaches a topic, concept, decision, or design worked out in the conversation — background, intuition, the details, diagrams, and a quiz. Use when the user wants to explain or teach back something discussed (an architecture, a decision and its trade-offs, a researched topic, a hard concept), saved as a dated HTML file outside the repo. Sibling of explain-diff, which handles code changes.
---

# explain-topic

Produce one long-form HTML page that teaches a reader a topic worked out in the conversation. The subject is not a code change — it's an idea, a design, a decision, or a concept. The page should make sense to a newcomer while giving someone familiar a fast path to the substance.

Sibling of `explain-diff`: same teaching spine and quiz, but the source of truth is the conversation (plus anything readable) rather than a diff. For a general visual page with no quiz, use `to-html` — the quiz is what makes this skill worth reaching for.

## Workflow

1. **Pick the subject.** The target is usually the thing just worked out — a design, a decision, a researched answer, a concept explained. If the thread covered several things, or the scope is ambiguous, confirm what to explain before building rather than guessing.
2. **Ground and enrich.** Base the page on what was actually said, plus any files, URLs, docs, or tool output you can read. Trace claims to their source. Where the conversation only implies something, mark it as inference; where a detail is missing, write `— not established —` rather than inventing a tidy version that was never decided.
3. **Draft the narrative before writing HTML:** what problem or context motivates the topic, the smallest useful mental model, the concrete details that make it real, and the edge cases, trade-offs, and open questions.
4. **Write one self-contained HTML file** — inline CSS/JS, no external fonts, CDNs, images, or network. Save it outside the repo as `YYYY-MM-DD-explanation-<slug>.html` in a scratch dir — the session scratchpad if there is one, otherwise `mktemp -d`.
5. **Validate before handoff:** confirm the file exists, is a complete document with no external assets, has working quiz interactions, and passes the quiz and code-block checks below. Serve the temp dir over a throwaway local server and screenshot it (the browser blocks `file://`) rather than trusting the markup blind.

## Required page structure

A clear title, a short summary, and a table of contents linking these sections in order:

1. **Background** — only the context needed for the topic. Optional beginner mental model first, then the specific pieces, terms, and prior state involved.
2. **Intuition** — the core idea before the detail, with small concrete examples. Show contrasts (this vs that, before vs after, chosen vs rejected) when they make the idea clearer.
3. **The details** — the concrete substance, in a logical order (cause→effect, step-by-step, or by importance), not the order it came up in chat. Cite sources: `file:line`, a doc, a URL, or "decided in discussion." This is the analog of explain-diff's Code section — make it specific, not hand-wavy.
4. **Quiz** — exactly five medium-difficulty interactive multiple-choice questions. Clicking an option immediately shows whether it's correct and why, tied to the relevant idea.

Plain, precise prose. Explain jargon on first use. Use callouts for definitions, key claims, trade-offs, and open questions. Responsive on phones. One continuous page — no top-level tabs.

## Diagrams

Build diagrams from semantic HTML + CSS, never ASCII. Pick the form that fits the topic: concept maps for how ideas relate, timelines for sequence or history, before/after or chosen/rejected panels for decisions, comparison tables for options and trade-offs, cause→effect chains, labeled cards for parts of a system. Label connections, include concrete example values, and add a caption so the point survives without visual inspection.

## Quiz quality (the anti-gaming rules)

Treat the quiz as part of the explanation. These fixes come from feedback on the original explain-diff — keep them, don't leave them to chance. Inspect all five questions as a set before emitting the page:

- **Deterministic shuffle.** Randomize the option order independently per question using a per-page seed, and balance correct-answer positions across the five as evenly as possible. Never let position, letter, or a repeated pattern reveal the answer.
- **Length-matched options.** Keep options comparable in length, grammar, specificity, and confidence. The correct one must not be conspicuously longer, more qualified, or more precise than the distractors — shorten or enrich distractors until a reader can't pick the answer by size alone.
- Make every distractor plausible and tied to a real misconception about the topic. No joke answers, "all/none of the above," or trivia not inferable from the page.
- Ask about ideas, causality, trade-offs, edge cases, or consequences — not something guessable from one copied phrase.
- Keep answers and explanations in the page's JS/DOM so it works offline; reveal feedback only after selection. Never leak correctness before a click via styling, DOM order, `title` attributes, or accessibility labels.

## HTML and code-block constraints

- Escape derived text for HTML and JS contexts; preserve meaningful whitespace.
- Any code or command blocks use `<pre><code>…</code></pre>`, and the `pre` CSS must include `white-space: pre` or `pre-wrap` — verify every block in the saved source.
- Keep JS small, namespaced, dependency-free. Visible focus states, sufficient contrast, no meaning by color alone.
- Don't claim more certainty than the conversation supports; separate what was established from your interpretation.

## Handoff

Report the absolute path as a clickable local-file link, state what you drew on (conversation, which files/URLs), and note any assumptions or gaps. Nothing lands in the repo unless the user asks.
