# Prompt Library

Each pattern gives you two things: the **verbatim original** (the exact prompt from Thariq's blog — copy and use as-is) and a **generalized template** (the scenario abstracted into placeholders for your own task). Placeholders are marked `<...>`.

---

## Pre-implementation

### 1 · Blind Spot Pass

Literally use the words "blind spot pass" / "unknown unknowns," and state who you are and how much you know — that works best.

**Verbatim:**

> "I'm working on adding a new auth provider but I know nothing about the auth modules in this codebase. Can you do a blind spot pass to help me figure out my relevant unknown unknowns and help me prompt you better."

> "I don't know what color grading is but I need to grade this video. Can you teach me to understand my unknown unknowns about color grading, so that I can prompt better?"

**Template:**

> I'm working on `<task>` but I know little about `<the unfamiliar area>` in this codebase. Do a blind spot pass: surface my relevant unknown unknowns, teach me what I'd need to know, and help me prompt you better. For context, I `<who you are / what you already know>`.

### 2 · Brainstorm + prototype

For unknown knowns (recognize-on-sight criteria). Ask for **wildly different** directions, not minor variations.

**Verbatim:**

> "I want a dashboard for this data but I have no visual taste and don't know what's possible. Make me an HTML page with 4 wildly different design directions so I can react to them."

> "Before wiring anything up, make a single HTML file mocking the new editor toolbar with fake data. I want to react to the layout before you touch the real app."

> "Here's my rough problem: users churn after onboarding. Search the codebase and brainstorm 10 places we could intervene, from cheapest to most ambitious. I'll tell you which ones resonate."

**Template:**

> Before wiring anything up, make a single throwaway `<HTML mock / prototype>` of `<the thing>` with fake data — give me `<N>` wildly different directions so I can react. Don't touch the real app yet.

> Here's my rough problem: `<problem>`. Search the codebase and brainstorm `<N>` ways we could intervene, cheapest to most ambitious. I'll tell you which resonate.

### 3 · Interview (have the agent question you)

For known unknowns. The key is to **prioritize questions that would change the architecture**.

**Verbatim:**

> "Interview me one question at a time about anything ambiguous, prioritize questions where my answer would change the architecture."

**Template:**

> Interview me one question at a time about anything ambiguous in `<task>`. Prioritize questions where my answer would change the architecture. Stop when the remaining unknowns wouldn't change your approach.

### 4 · References

When you can't describe it, point at a reference — **source code beats a screenshot / docs / a diagram**.

**Verbatim:**

> "This Rust crate in vendor/rate-limiter implements the exact backoff behavior I want. Read it and reimplement the same semantics in our TypeScript API client."

**Template:**

> `<path/to/reference>` implements the exact `<behavior / structure / style>` I want. Read it and reimplement the same semantics in `<our target: language / module>`, even though the language differs.

### 5 · Implementation Plan

The pre-implementation closer. **Lead with what's most likely to change**; bury the mechanical parts.

**Verbatim:**

> "Write an implementation plan in HTML, but lead with the decisions I'm most likely to tweak with: data model changes, new type interfaces, and anything user-facing. Bury the mechanical refactoring at the bottom, I trust you on that part."

**Template:**

> Write an implementation plan for `<task>`. Lead with the decisions I'm most likely to tweak: `<data model / interfaces / anything user-facing>`. Bury the mechanical parts at the bottom — I trust you there. Flag anything you're guessing at.

---

## During implementation

### 6 · Implementation Notes

Once you're happy with the plan, start a **new session**, pass in the artifacts, and have the agent log deviations.

**Verbatim:**

> "Keep an implementation-notes.md file. If you hit an edge case that forces you to deviate from the plan, pick the conservative option, log it under 'Deviations', and keep going."

**Template:**

> Keep an `implementation-notes.md` file. If you hit an edge case that forces a deviation from the plan, pick the conservative option, log it under 'Deviations' with the reason, and keep going. (Template: `assets/implementation-notes.template.md`)

---

## Post-implementation

### 7 · Pitch / Explainer

**Verbatim:**

> "Package the prototype, the spec, and the implementation notes into a single doc I can drop in Slack to get buy-in. Lead with the demo GIF."

**Template:**

> Package the prototype, the spec, and the implementation notes into a single doc I can drop in `<channel>` to get buy-in. Lead with `<the demo / the headline result>`; make it readable by someone starting with the same unknowns I had. (Template: `assets/handoff.template.md`)

### 8 · Quiz (have the agent test you)

**Only merge after you pass it perfectly.**

**Verbatim:**

> "I want to make sure I understand everything that's happened in this change. Give me a HTML report on the changes for me to read and understand with context, intuition, what was done, etc. and a quiz at the bottom on the changes that I must pass."

**Template:**

> I want to make sure I understand everything in this change. Give me a report on the changes — context, intuition, what was done and why — with a quiz at the bottom I must pass. Don't let me merge until I answer all of it correctly.
