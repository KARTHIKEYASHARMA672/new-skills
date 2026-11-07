# Four Quadrants: how to classify your unknowns, and how to pick a pattern

Before you rush into a prompt, spend a minute breaking the task down the four ways below. Which quadrant you're stuck in decides which pre-implementation pattern to reach for.

## The four kinds

- **Known Knowns** — what you know, and can articulate. This is what goes into your prompt.
- **Known Unknowns** — the parts you know you haven't figured out yet. You can write them as a list of "open questions."
- **Unknown Knowns** — things so obvious you'd never write them down, but recognize the moment you see them. Typically taste / feel / "that's not what I meant" judgment calls.
- **Unknown Unknowns** — what you haven't considered at all; knowledge you don't know you're missing; you don't even know how good something can be. **This is the expensive quadrant** — you don't even know what to ask, so you hit these deep in implementation, where rework costs the most.

## Which quadrant maps to which pattern

| Quadrant | Signature | Pre-implementation pattern |
|----------|-----------|----------------------------|
| Known Knowns | Can put it in the prompt | Just write it clearly; don't over-explain |
| Known Unknowns | You know you haven't settled it | **Interview**: have the agent ask one at a time, architecture-changing questions first |
| Unknown Knowns | Recognize-on-sight only | **Brainstorm + prototype**: get several wildly different directions to react to |
| Unknown Unknowns | Don't know what you don't know | **Blind Spot Pass**: have the agent dig them out and explain them |

References and Implementation Plan span multiple cells: **References** fits "can't say it but can point at something" (often paired with Unknown Knowns), and the **Implementation Plan** is the pre-implementation closer that solidifies the unknowns you've surfaced into a reviewable plan.

## The target state

The best agentic coders have relatively few unknowns — they're deeply in sync with the codebase and model behaviors, and it shows in how much detail they prompt with. But they **also assume unknowns exist**; they don't pretend to know everything. Reducing and planning for your unknowns is itself the skill of agentic coding, and it's one you can improve at by working with the agent.

This skill isn't about filling in all four cells or running the full workflow every time; it's a map of "which quadrant am I stuck in right now," so you can pick the right next move.
