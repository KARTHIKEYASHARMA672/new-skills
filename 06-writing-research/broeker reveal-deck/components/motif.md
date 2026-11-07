---
name: motif
category: component
description: Repeating visual icon system with multiple size/opacity treatments. The icon itself is defined by the theme (emoji, SVG, or image). This component defines how to display it.
---

> **CSS:** All styles for this component are in `themes/electric-dark.css`. Do not add CSS from this file.

## Usage

Every theme can define a **motif** — a repeating visual icon that acts as a
brand element across slides. The theme specifies *what* the icon is; this
component defines *how* to display it at different sizes and opacities.

The motif icon is set by the theme. Examples:
- `electric-dark` uses `&#9889;` (lightning bolt)
- A space theme might use `&#128640;` (rocket)
- A corporate theme might use an inline SVG logo

### Treatments

| Class | Purpose | Required? | Typical placement |
|-------|---------|-----------|-------------------|
| `motif-bg` | Huge ghosted icon, nearly invisible, creates depth | **Yes — every content slide** | `position:absolute` in a slide corner or center |
| `motif-sm` | Small inline icon | Optional | Next to h2 titles |
| `motif-md` | Medium standalone accent | Optional | Between content sections |
| `motif-corner` | Medium-opacity icon anchored to a slide corner | Optional | `position:absolute` top-right or bottom-right |

### Rules

**Baseline (mandatory on every content slide):**
- Every content slide gets a `motif-bg` — the huge ghosted background icon.
  This is a structural element like `slide-tag` or `accent-line`, not optional.
- Vary the position across slides: `top:-40px; right:-60px`, `bottom:-60px; left:-80px`,
  `top:50%; right:-60px; transform:translateY(-50%)`, `left:50%; top:50%; transform:translate(-50%,-50%)`, etc.
- Alternate between `color:var(--cyan)` and `color:var(--amber)` so consecutive
  slides don't repeat the same color.

**Layering (additional treatments on top of motif-bg):**
- Add `motif-sm` inline with `<h2>` on ~40-50% of slides for extra branding
- Add `motif-corner` on ~20-30% of slides for variety
- Use `motif-md` sparingly for standalone accent moments
- Never stack more than 2 treatments on the same slide (bg + one other)
- The motif should feel like a brand signature — present everywhere but not overwhelming

## HTML

Replace `ICON` with the theme's motif icon (emoji entity, inline SVG, or `<img>`).

```html
<!-- Huge ambient background motif -->
<span class="motif-bg" style="position:absolute; top:-40px; right:-20px; color:var(--cyan);">ICON</span>

<!-- Small inline motif next to a heading -->
<h2><span class="motif-sm cyan">ICON</span> Slide Title</h2>

<!-- Medium standalone motif -->
<span class="motif-md cyan">ICON</span>

<!-- Corner motif -->
<span class="motif-corner" style="top:10px; right:30px; color:var(--amber);">ICON</span>
```

### Example: lightning bolt (electric-dark)

```html
<span class="motif-bg" style="position:absolute; top:-40px; right:-20px; color:var(--cyan);">&#9889;</span>
<h2><span class="motif-sm cyan">&#9889;</span> Slide Title</h2>
```

### Example: inline SVG logo

```html
<span class="motif-sm cyan">
  <svg width="1em" height="1em" viewBox="0 0 24 24" fill="currentColor">
    <!-- SVG path data -->
  </svg>
</span>
```

## Theme integration

Themes define their motif in a `## Motif` section:

```markdown
## Motif
- **Icon:** `&#9889;` (lightning bolt emoji)
- **Fallback:** none
- **Notes:** Fits the electric/terminal aesthetic. Alternate cyan and amber.
```

During the interview, the user can also override the motif: "use a rocket
instead of the bolt" — just swap the icon entity in the HTML.
