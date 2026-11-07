---
name: electric-dark
category: theme
description: Dark electric theme with neon lime accents, dot-grid background, and terminal aesthetic
default: true
---

**The canonical CSS lives in `themes/electric-dark.css`.** This file documents
rationale, design rules, and font assignments. Do not reconstruct CSS from this
file — read `electric-dark.css` and include it verbatim.

## Fonts

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;1,8..60,300&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
```

- **Heading:** Rajdhani (400/500/600/700) — geometric, condensed
- **Body:** Source Serif 4 (300/400/600, italic) — warm serif for paragraph text and list items ONLY
- **Mono:** Fira Code (400/500) — for code, labels, UI chrome, panel-labels, slide-tags

**CRITICAL — font assignment rules:**
- Rajdhani: `h1`, `h2`, `h3`, `h4`, `.stat-number`, `.stat-label`, `.key-num`, `.step-n`, `.icon-grid-label`
- Source Serif 4: `p`, `li`, `.pull-quote-text`, `.key-text`, `.step-body`, `.compare-text` — NEVER on `div` or `span`
- Fira Code: `code`, `pre`, `.panel-label`, `.slide-tag`, `.section-label`, `.filepath`, `.badge`, `.screenshot-url`, `.agenda-num`, `.tl-date`, `.flow-step`
- **Inherit (no font set):** `div`, `span`, `section` — these inherit from their parent. Never set `font-family` on generic elements.

## CSS Variables (reference)

```
--dark:         #060A12
--panel:        #0D1526
--panel2:       #101E35
--accent:       #AAFF00      (primary accent — lime green)
--cyan:         #AAFF00      (alias — same as accent)
--amber:        #FFB020
--red:          #FF4D4D
--text:         #DCE8F5
--muted:        #7A9BBF      (readable on dark backgrounds)
--border:       rgba(170,255,0,0.15)
--border-amber: rgba(255,176,32,0.18)
--glow:         rgba(170,255,0,0.25)
```

**Note:** `--muted` MUST be `#7A9BBF` or lighter. The previous value `#4E6A8A`
is too dark to read on the dark background.

## Content wrapper — vertical centering

Every content slide should wrap its content in a vertically-centered flex container.
Use the `.slide-body` class or an inline style:

```html
<section>
  <div style="display:flex;flex-direction:column;justify-content:center;height:100%;padding:0.5em 2em;">
    <!-- slide content -->
  </div>
</section>
```

The key principle: content should be vertically centered in the viewport, not
pushed to the top. This creates a professional, balanced feel.

## Typography notes

**Bold text:** `strong` should NOT be globally set to `color: var(--cyan)`.
Instead, bold text inherits the parent color. If you want an accent, use
`<strong style="color:var(--accent)">` explicitly. This prevents every bold
word in panels, callouts, and nested components from being lime green.

**Slide tag:** `display: inline-block` with margin, NOT `position: absolute`.

**Accent line:** gradient fade, not solid block. 48px wide, not 80px.

**Cols gap:** `0.7em`, not `2rem`. Tight gaps keep content dense and professional.

## Motif

- **Icon:** `&#9889;` (lightning bolt emoji, renders as lightning bolt)
- **Component:** `motif` (defines the size/opacity treatments)
- **Required:** Yes — the lightning bolt is the signature of this theme. Every
  content slide must include at least a `motif-bg` (huge ghosted bolt in a corner).
  Many slides should also include a `motif-sm` inline with the heading. The bolt
  should feel omnipresent — a watermark-like brand element on every slide, not
  occasional decoration.
- **Colors:** Alternate `var(--accent)` and `var(--amber)` across slides.
- **Positions:** Vary corner placement — top-right, bottom-left, center, mid-right —
  so the bolt feels dynamic, not stamped in the same spot.

## Design principles — MUST FOLLOW

1. **Vertical centering** — all slide content wraps in a flex column with
   `justify-content: center; height: 100%`. Content floats in the middle of
   the viewport, not pushed to the top.
2. **Font discipline** — Source Serif only on `p` and `li`. Never on `div`,
   `span`, or structural elements. Labels, tags, badges use Fira Code.
   Headings use Rajdhani. No exceptions.
3. **Tight spacing** — `0.7em` grid gaps, `0.3em` margins. Dense but
   readable. Avoid `2rem` gaps that waste space.
4. **Gradient accents** — accent lines fade from color to transparent.
   Solid blocks feel heavy; gradients feel polished.
5. **Readable muted text** — `--muted: #7A9BBF`. Must be clearly legible
   on `#060A12` background. Never darker than `#6A8AAF`.
6. **No global strong color** — bold inherits parent color. Use explicit
   `style="color:var(--accent)"` when you want lime emphasis.

## Recommended components

- `motif` — repeating visual icon system (this theme uses the lightning bolt)
- `codeblock` — terminal-style code blocks match the dark theme
- `panel` — bordered cards use accent/border variables
- `callout` — highlighted boxes with accent glow
- `comparison` — good/bad panels with color-coded borders
- `flow` — lifecycle diagrams with glowing active states
- `file-tree` — monospace directory listings
- `badge` — pill labels in amber
- `filepath` — path badges in amber/green
- `key-item` — numbered takeaway lists
