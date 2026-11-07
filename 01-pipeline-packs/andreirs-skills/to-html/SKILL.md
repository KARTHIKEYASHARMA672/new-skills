---
name: to-html
description: Turn what's been discussed — plus the files, git history, and tool output you can read — into a single self-contained HTML page that makes a concept, comparison, or plan easier to see and explore. Use when the user wants to visualize an idea, render a discussion as a page, build a quick explainer/dashboard/cheat-sheet/annotated diff, or says "make this an HTML page / artifact". Honours plain-English directives (light mode, cards, table, checklist, interactive) and falls back to sensible defaults. On-demand only; not for repo docs (to-spec), architecture reports (improve-architecture), or Figma work.
---

# to-html

HTML conveys more than Markdown can: tables, diagrams, colour, layout, and live controls. When a discussion has reached the point where *seeing* it would help more than scrolling it, render it as one page.

The page is **grounded in available context** — what was discussed, plus the files, git history, MCP data, and tool output you can actually read. The article's whole argument for HTML is this context integration, so use it: an annotated diff pulls the real diff, a data dashboard reads the real numbers. Never fabricate to fill a gap — where the source is missing, mark it (`— not available —`) rather than inventing it.

## When to use

Fires **on demand**: the user wants to look at something rather than read it — an explainer, comparison, plan, dashboard, cheat-sheet, annotated review. Triggers include "make this an HTML page", "visualize this", "turn this into a page/artifact", "show me this as...". When a discussion turns visual or dense you may add a single non-pushy line ("want this as a page?"), but never auto-generate a page unprompted.

Not for: editing project files, writing docs that belong in the repo (use `to-spec`), codebase architecture reports (`improve-architecture` owns that and its own HTML format), or design work in Figma (the `figma-*` skills).

## Pick the shape

Choose the form that fits what's on screen — or take the user's nudge:

- **Explainer** — a hard concept, with an SVG/diagram and numbered steps.
- **Decision matrix** — options weighed, as a scored comparison table.
- **Plan / roadmap** — phases with a checklist and a simple timeline.
- **Dashboard** — figures/metrics as stat cards and small charts.
- **Architecture / flow** — components and data flow as boxes and arrows.
- **Tuner** — sliders/toggles that recompute live (pricing, easing, scenarios).
- **Reference sheet** — terms/commands as a searchable, filterable grid.
- **Annotated diff** — a reviewed change with inline notes and severity colours.

## Read the directives

Don't over-specify or ask for a config. Take plain words from the request and apply defaults otherwise:

| Directive | Effect |
|---|---|
| `light mode` | light palette (default is dark — see Taste) |
| `card layout` | content as a card grid, not prose |
| `table` / `checklist` | include a comparison table / tickable items |
| `interactive` | sliders, toggles, live recompute |
| `printable` | clean print stylesheet with page breaks |
| `one page` | single file (this is always true anyway) |

Always-on, no need to ask: **responsive** (phone → wide screen) and **light interactivity** where it obviously helps — filter boxes, collapsible sections, tab switching. Reserve heavier JS for when the user asks for `interactive`.

## Build it

- **One self-contained file.** Inline the CSS and JS. No build step.
- **CDNs are allowed** (Tailwind, Mermaid, Chart.js) when they earn their place — but be honest about the tradeoff: **the core layout and content must be readable with no network**; charts and diagrams that depend on a CDN simply won't appear offline, so never put load-bearing information *only* inside them. Don't pull a CDN for something a few lines of CSS would do.
- **Write to a scratch dir, then open it.** Use the session scratchpad if there is one, otherwise `mktemp -d`; name the file `to-html-<slug>-<timestamp>.html`. Open with `open` (macOS), `xdg-open` (Linux), or `start` (Windows). Nothing lands in the repo unless the user asks.
- **Verify before claiming done.** A typo in the JS or a layout that collapses on mobile opens as a blank or broken page. Sanity-check the markup, and for anything with non-trivial JS, screenshot it (the `playwright-cli` skill) before reporting success — don't report a page you haven't confirmed renders. The browser blocks `file://` URLs, so serve the temp dir over a throwaway local server first (`python3 -m http.server <port>` in that dir) and point the browser at `http://localhost:<port>/<file>`; stop the server when done. A lone `favicon.ico` 404 in the console is expected and harmless.
- **Report the absolute path** after opening.

## Iterating

Treat the page as a living artifact, not a one-shot. Remember the path you just wrote; when the user says "make it dark", "add a column", "now drop that section", **Edit that same file in place and re-open it** rather than spawning a new timestamped file. Only start a fresh file when the content is genuinely a different page. If the user later wants it kept, copy it where they say — but default to ephemeral (sharing is a browser concern: print-to-PDF or send the file).

## Taste

Make it genuinely nicer to read than the chat: clear hierarchy, generous spacing, a restrained palette, real content density without clutter. The page should look intentional, not like a default template.

**Use the `brand-it` skill for the visual identity** — its colour tokens, typography (Inter / JetBrains Mono), and rules are the default look for these pages. Dark mode first with a light mode alongside, headings in body-text colour, semantic colours for meaning only. Only depart from it when the user asks for a different style or the content has its own palette (e.g. an annotated diff using a project's syntax theme).
