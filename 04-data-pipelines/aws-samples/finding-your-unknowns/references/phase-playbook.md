# Phase Playbook: per-pattern rationale and when to use each

SKILL.md gives the skeleton; this fills in the "why, when, and what trips people up" for each pattern. Copy-paste prompts are in [prompt-library.md](prompt-library.md).

---

## Pre-implementation · surface the unknowns

This is the thickest phase, because clarifying unknowns is cheapest before you start. You don't need all five patterns — pick by which quadrant you're stuck in (see [four-quadrants.md](four-quadrants.md)).

### Blind Spot Pass

- **When:** entering an unfamiliar part of the codebase, or doing unfamiliar work like design iteration. You have a pile of unknown unknowns: you don't know what to ask, what "good" looks like, or what historical baggage and potholes are there.
- **How:** have the agent dig the unknown unknowns out and explain them to you. Literally use the words "blind spot pass" and "unknown unknowns." Give it context on who you are and how much you know so it knows where to start.
- **Trap:** asking without stating your experience level — the agent can only pitch to an average reader, landing too shallow or too deep.

### Brainstorm + prototype

- **When:** the area is full of unknown knowns — you only know whether you want it once you see it (visual design is the classic: hard to articulate, but obvious on sight).
- **Why early:** unknown knowns are more expensive to discover during implementation — a small change in spec can cause a drastically different implementation, and reverting the agent's prior changes is harder.
- **How:** ask for 3–4 **wildly different** directions, or a throwaway HTML mock (just the layout, no backend, no state). Open almost every session with an exploration / brainstorm to set scope — the agent often finds high-value paths you'd miss, and sometimes misses the forest for the trees; brainstorming keeps scope from being too narrow or too wide.
- **Trap:** asking for "a few minor variations" instead of "wildly different directions" — that's not really brainstorming.

### Interview

- **When:** ambiguity remains after enough brainstorming (known unknowns).
- **How:** have the agent ask one question at a time, **prioritizing the ones whose answer would change the architecture**. Give it task context to guide the questions.
- **Trap:** letting it dump ten questions at once, so you answer them carelessly. One at a time, sorted by architectural impact, has the highest information density.

### References

- **When:** you can't describe what you want in detail — you don't have the language, or it's complex enough that explaining takes a while.
- **How:** point at a reference, and **the best reference is source code**. If a library implements the behavior you want, or there's a component you like, point the agent at that folder and tell it what to look for, even in another language. Source gives the agent far richer markup / structure detail than a screenshot.
- **Trap:** giving only a screenshot / description and making the agent guess the implementation, when there's existing source you could point at.

### Implementation Plan

- **When:** you think you're ready to build — the last pre-implementation step.
- **How:** have the agent produce a plan for you to review, and **lead with the parts most likely to change** (data model / type interfaces / UX flows), burying the mechanical work — so on review you hit the real decisions first.
- **Trap:** letting the plan run in "execution order," so you have to read halfway down to reach the key decisions. Ordering by "what you're most likely to change" is easier to review.

---

## During implementation · log deviations

### New session + Implementation Notes

- **Why a new session:** the planning session's context is already full. A new session gives the agent a clean context window, but you pass the planning artifacts (spec / prototype / plan) back in — information kept, noise cleared.
- **Why the notes:** no matter how much you plan, unknown unknowns lurk. The agent may be forced to change tack mid-work because of an edge case in the code. Have it maintain `implementation-notes.md`: on a deviation, pick the conservative option, log it under `Deviations`, keep going. Those notes are the learning material for the next attempt and the raw material for the post-implementation pitch.
- **Trap:** keeping no notes, so afterward you can only reverse-engineer from the diff why the agent did what it did.

---

## Post-implementation · verify through unknowns

### Pitch / Explainer

- **Why:** delivery and getting approvals are among the most important parts of shipping. Pitch / explainer artifacts let reviewers start from the same unknowns you had and catch up fast, and let experts confirm you've considered the failure points they'd anticipate — both accelerate.
- **How:** package prototype + spec + implementation notes into one doc, and lead with the demo.

### Quiz

- **Why:** after a long session the agent may have accomplished more than you realized. Reading the diff gives only a light understanding, because much of the behavior depends on existing code paths.
- **How:** have the agent produce a context-rich report plus a quiz at the bottom, and **only merge after you pass it perfectly**. This is the last gate against "the agent finished, and you merged it without really understanding it."
- **Trap:** treating the quiz as a formality and merging even when you get it wrong — then it's pointless.

---

## One-line close

The better models get, the more you can achieve with the right approach. A long task that comes back wrong usually means unknowns weren't defined enough, or you were missing a plan that lets you adapt mid-course. Every explainer / brainstorm / interview / prototype / reference is a cheap way to find out what you didn't know while it's still cheap.
