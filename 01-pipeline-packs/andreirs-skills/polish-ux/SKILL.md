---
name: polish-ux
description: "Review-and-fix craft pass over a rendered HTML artifact — verify it actually renders, then enforce the rules that make it read as designed, not assembled: one layout system, clear hierarchy, typographic execution, tasteful motion, complete empty/loading/error states, and accessibility. Use after generating or editing any HTML page (to-html, show-it, explain-diff, explain-topic, or hand-written). Fixes in place; pairs with brand-it, which owns the visual identity."
---

# polish-ux

A craft pass for rendered HTML. `brand-it` decides what a page should *look* like (colors, fonts, semantic meaning); this skill checks that the page is actually *built well* — it renders, the components work, and every value on the screen traces back to a rule instead of a guess. Run it on any HTML output before handing it off.

Fix defects in place, then re-verify. This is quality only — it does not add features or change content.

## Start by proving it renders

Never review from the source alone. A typo in the JS or a stray duplicate `id` can leave a blank or broken page that reads fine in the file. So first:

1. Serve the file over a throwaway local server (the browser blocks `file://`) and open it — e.g. `python3 -m http.server <port>` in its directory.
2. **Screenshot it** and inspect the real render (the `agent-browser` skill: `open` then `screenshot --full`). For anything interactive, drive the key interaction and screenshot the result state, not just the initial view.
3. Sanity-check the console and the DOM: no uncaught JS errors, elements land where the markup implies. Watch for duplicate `id`s, `getElementById` hitting the wrong node, and libraries that failed to load.

If it doesn't render correctly, that's the first fix. Everything below assumes a page that loads.

**If you can't render and screenshot it** (no browser tool, sandboxed, headless failure), stop and say so — a source-only pass is *incomplete*, not a clean review. Alignment, overflow, and contrast defects are invisible in code and only show on screen. Report the checks you couldn't run rather than presenting the review as verified.

## The checklist

Walk these in order. The layout system comes first because it's the highest-leverage pass — it's what separates a page that feels engineered from one that feels assembled. Fix what's broken; leave what's already right.

- **One layout system** — the core rule: remove arbitrary decisions. (1) Every gap, padding, and margin is a multiple of one spacing scale (4/8px: 4, 8, 12, 16, 24, 32, 48) — no `13px` here and `17px` there. Related things sit close, unrelated things get air; proximity signals grouping. (2) Everything aligns to a shared grid; align content by type — text left, numbers right with tabular figures so columns don't jitter. (3) One density (comfortable *or* compact, not both) and one type scale (3–4 sizes, 2 weights). Hierarchy comes from the scale, never one-off font sizes.
- **Hierarchy & focus** — each view has a single clear focal point; the eye knows where to land first. Emphasis is earned through contrast of size/weight/space, not decoration. If everything is bold, nothing is; secondary and tertiary content visibly recede.
- **Typographic execution** — body measure stays readable (~45–75 characters per line, not edge-to-edge). Real punctuation: curly quotes, em/en dashes, true minus, non-breaking spaces in units. Numbers use locale formatting (thousands separators, units, sensible rounding). Headings get the brand's deliberate treatment (weight, tracking), not just a bigger size. The type system itself is `brand-it`'s job — this checks it's applied cleanly.
- **Restraint & depth** — whitespace is generous and confident; empty space is a choice, not a gap to fill. Shadows form one elevation scale (a few defined levels), not random blurs. Borders *or* shadows for separation, rarely both. No gradient, shadow, or emoji noise a design system wouldn't ship.
- **Progressive disclosure** — lead with the summary, keep the depth one interaction away. Don't dump everything on one screen. For a dense page, overview first and detail on demand; one message per chart.
- **State completeness** — for anything interactive or data-driven, design the empty, loading, and error states, not just the full one. Skeletons over spinners for layout stability; helpful empty states ("no results — widen the range"); one broken widget never blanks the page.
- **Interaction states** — every interactive element has visible `hover`, `:focus-visible`, `disabled`, and selected/active styling. Feedback appears only *after* the user acts, never leaked before (styling, DOM order, `title`, or a11y labels).
- **Motion** — transitions are quick (~150–250ms) and eased (never linear); they clarify state changes, not decorate. Entrances are subtle, not showy. `prefers-reduced-motion` is honored — motion drops to a fade or nothing.
- **Conventions & consistency** — follow patterns people already know rather than inventing; keep one border-radius family, one numbering style, one icon set. Semantic color signals meaning only, never decoration. Adornments (section numbers, markers, badges) use the body/heading typeface, not mono, unless they're code or labels.
- **Responsive** — reflows cleanly at the 640px mobile breakpoint; no horizontal page scroll, no overlap, no clipped text; multi-column grids collapse to one. Wide content (tables, diagrams, code, charts) scrolls inside its own container, not the body. Tap targets ~44px.
- **Accessibility** — sufficient contrast, real focus rings, no meaning conveyed by color alone, labels that describe the element (not its correctness), meaningful alt/captions on diagrams and charts. Dark and light modes both checked, not just the default.

## After fixing

Re-serve and re-screenshot to confirm each fix landed and nothing regressed. Report what was broken, what you changed, and show the before/after state of anything visual. Don't claim a fix you haven't seen render.

Defer to `brand-it` for the actual tokens, fonts, and color meanings — this skill enforces that they're applied cleanly, not what they are.
