---
name: show-it
description: "Show an idea in a live browser instead of describing it in text: mockups, comparisons, charts, diagrams, layouts. Opens a local page that auto-refreshes as you write HTML, so the user sees what you mean within a second. Use whenever a picture would land an idea faster than a paragraph. Triggers on \"show it\", \"visualize this\", \"render this\"."
---

# show-it

A browser-based way to *show* an idea instead of describing it. Some things are easier to grasp by looking than by reading: a layout, a chart, two designs side by side, a flow. This skill opens a local web page and lets you push HTML to it; the page auto-refreshes within a second so the user sees the latest version. It is a display tool, not a decision tool. Reach for it from any flow when a picture would land the idea faster, then go back to the terminal for everything else.

## Browser or terminal?

Whoever calls this skill expects to need a lot of visual help, so the browser is the default medium and full HTML is what you push to it. HTML is the richest and most flexible option: real layouts, color, side-by-side comparisons, charts. Do not reach for a weaker middle ground like Mermaid. When something is visual, show it as HTML in the browser.

The only fallback is the terminal. Use a quick ASCII sketch there when the thing is trivial to show (a two-box flow, a rough tree) and spinning up the browser would be overkill. And keep words in the terminal: requirements, scope, pros and cons, any normal explanation or clarifying question.

Decide per thing, not per session. The test: **would a picture land this faster than a sentence?** If yes, push HTML. If it is trivial, an ASCII sketch in the terminal is fine. If it is words, stay in the terminal. Something that is *about* a UI is not automatically visual: "what kind of dashboard do you want?" is words; "here are two dashboard layouts" is HTML.

## Keep it clean

The page exists to make one idea clear, so show one idea per screen. No clutter, no decoration that does not carry meaning. Give the screen a short title (`h2`) so the user knows what they are looking at, and an optional one-line subtitle for context. Everything else on the screen should be the thing itself: the mockup, the chart, the comparison.

When you show more than one thing to compare (two layouts, three price curves), lay them out side by side with a short label on each so you and the user can point at the same one in the terminal. This is for clarity, not for forcing a choice: you are showing, the user looks, and the conversation continues in the terminal.

## Setup

Needs `bun` and an internet connection (the page pulls Tailwind, Chart.js, and fonts from a CDN).

Pick a screen directory — the session scratchpad if there is one, otherwise `mktemp -d` — and start the server **in the background** so it survives across turns:

```bash
SCREEN_DIR=<scratch-dir>/show-it PORT=52777 bun <skill-dir>/scripts/server.ts
```

It prints `show-it: visualization at http://localhost:52777`. Give the user that URL **once**; the tab never changes address after that. Omit `PORT` to let it pick a free port (read the printed line for the number). Stop it when the visual work is done by killing the process (`lsof -ti tcp:52777 | xargs kill`).

The server reads `scripts/frame.html` at startup and serves it at `/`. The frame owns the page shell, the brand styling, and the poll loop. If you edit `frame.html`, restart the server and the user reloads once. You never write the frame during a session, only screen fragments.

## The loop

1. **Start once.** Launch the server (above), give the user the URL.
2. **Write a screen.** Write the fragment to `$SCREEN_DIR/screen.html`: a title, then the thing you want to show. Always the same file. `Write` for a new screen, `Edit` for a tweak to the current one (cheaper, sends only the diff). The page polls and swaps it in within a second, no refresh.
3. **Hand off.** End your turn with a one-line summary of what is on screen ("two dashboard layouts up, take a look") and continue the conversation in the terminal.
4. **Iterate or advance.** If the user wants changes, `Edit` the current screen. To show something new, `Write` the next screen.
5. **Clear on exit.** When you are done with visuals, write a short "continuing in terminal..." screen so the user is not left staring at a stale page.
6. **Stop** the server when done.

## What you can put in a fragment

A fragment is plain HTML, no `<head>` or `<script src>` for libraries. The frame already provides:

- **Title** — an `h2` for the screen title and an optional `.subtitle` line under it.
- **Panels** — `.card` with an optional `.card-title` for charts, mockups, or any grouped content.
- **Tailwind v4 utility classes** — for any layout the base classes do not cover.
- **Chart.js** — drop a `<canvas>` and a `<script>` that calls `new Chart(...)`. The frame re-runs injected scripts, so the chart renders.
- **Brand tokens** as CSS variables (`--info`, `--success`, `--danger`, `--highlight`, `--muted`, `--surface`, `--border`). Read them in chart scripts with `getComputedStyle(document.documentElement).getPropertyValue("--info")` so charts match the theme in both light and dark mode.

Keep fragments small and on-brand: no gradients, no decorative shadows, color only to signal meaning.

**Stay responsive.** The user may be on a phone. For any multi-column layout use `grid-cols-1 sm:grid-cols-2`, never a bare `grid-cols-2`, so columns stack on narrow screens instead of cramping. For charts in a mixed-height grid, set `options.maintainAspectRatio = false` so they fill the card instead of leaving dead space.
