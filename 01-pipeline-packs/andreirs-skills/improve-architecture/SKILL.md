---
name: improve-architecture
description: "Find deepening opportunities in a codebase — refactors that turn shallow modules into deep ones, for testability and AI-navigability. Surveys the code (a user-named area, or the whole repo) and produces a visual HTML report of the strongest candidates. Read-only: it proposes, it never edits. Use when the user wants to improve architecture, find refactoring opportunities, consolidate tightly-coupled modules, or make a codebase more testable."
---

# Improve Architecture

Surface architectural friction and propose **deepening opportunities** — refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

This skill is **read-only**. It explores, reasons, and writes a report. It does not edit code, and it does not write to the project's domain docs. Design and implementation happen later — hand a chosen candidate to `grill-me` (to design it) or `to-issues` (to slice it).

## Glossary

Use these terms exactly in every suggestion. Consistent language is the point — don't drift into "component," "service," "API," or "boundary."

- **Module** — anything with an interface and an implementation (function, class, package, slice).
- **Interface** — everything a caller must know to use the module: types, invariants, error modes, ordering, config. Not just the type signature.
- **Implementation** — the code inside.
- **Depth** — leverage at the interface: a lot of behaviour behind a small interface. **Deep** = high leverage. **Shallow** = interface nearly as complex as the implementation.
- **Seam** — where an interface lives; a place behaviour can be altered without editing in place. (Use this, not "boundary.")
- **Adapter** — a concrete thing satisfying an interface at a seam.
- **Leverage** — what callers get from depth.
- **Locality** — what maintainers get from depth: change, bugs, and knowledge concentrated in one place.

Three principles do most of the work:

- **Deletion test** — imagine deleting the module. If complexity vanishes, it was a pass-through (shallow). If complexity reappears, spread across N callers, it was earning its keep (deep). A "concentrates complexity" answer is the signal you want.
- **The interface is the test surface.** A module is only as testable as its interface is small and honest.
- **One adapter = a hypothetical seam. Two adapters = a real seam.** Don't invent seams for callers that don't exist.

## Process

### 1. Scope

- If the user named an area, module, or directory, focus there.
- Otherwise, sweep the whole repo and surface the strongest candidates wherever they are.

If `GLOSSARY.md` (a domain glossary) or `docs/adr/` (architecture decision records) exist, read the ones relevant to your scope first. Use that vocabulary for the domain, and respect ADRs — don't re-litigate decisions already recorded. **These are optional**: if they're absent, infer the domain language from the code and carry on. Never create or edit them.

### 2. Explore

Use the Agent tool with `subagent_type=Explore` to walk the code in scope. Don't follow rigid heuristics — explore organically and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow** — interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, while the real bugs hide in how they're wired together (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it? "Concentrates" is the candidate you want.

Aim to end with the **strongest 3-6 candidates** — not every theoretical refactor. Rank them; you'll lead with the best.

### 3. Write the HTML report

Write a self-contained HTML file to a scratch dir so nothing lands in the repo — the session scratchpad if there is one, otherwise `mktemp -d` — named `architecture-review-<timestamp>.html`. Open it — `open <path>` on macOS, `xdg-open <path>` on Linux, `start <path>` on Windows — and tell the user the absolute path.

**Render the report exactly per [HTML-REPORT.md](HTML-REPORT.md)** — it owns the scaffold, the candidate-card spec, the diagram patterns, the styling, and the tone. Don't restate the card fields here; follow that file. In short: Tailwind + Mermaid via CDN, one card per candidate with a before/after diagram doing the heavy lifting, a strength badge (`Strong` / `Worth exploring` / `Speculative`), and a closing **Top recommendation** section.

Two things to carry in from the rest of this skill:

- **Vocabulary** — domain nouns for what the code is about (if `GLOSSARY.md` defines "Order," say "the Order intake module," not "the FooBarHandler" and not "the Order service"), and the **Glossary above** for the architecture.
- **No design** — describe the deepening in plain English; **no interface signatures, no code**. Design is a later step.

If `docs/adr/` exists and a candidate contradicts a recorded ADR, surface it only when the friction warrants reopening the decision, flagged in the card per HTML-REPORT.md. Don't list every refactor an ADR forbids.

### 4. Hand off

After the file is written and opened, stop. Summarise the top recommendation in chat in one or two sentences and point the user at the next step: `grill-me` to design a chosen candidate, or `to-issues` to slice it into work. Do not propose interfaces, edit code, or open a design conversation here.
