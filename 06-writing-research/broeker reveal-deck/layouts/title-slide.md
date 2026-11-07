---
name: title-slide
category: layout
description: Opening title slide with deck name, subtitle, meta info, and auto-calculated slide count and duration.
---

> **CSS:** All styles for this layout are in `themes/electric-dark.css`. Do not add CSS from this file.

## Usage

Every deck starts with a title slide. No `{NNN}` slug on this slide. Title slide displays auto-calculated slide count and estimated duration.

## HTML

```html
<section data-background-color="#060A12">
  <!-- Optional decorative SVG or bolt-bg -->
  <svg class="title-deco" viewBox="0 0 400 400" fill="none">
    <circle cx="200" cy="200" r="190" stroke="var(--cyan)" stroke-width="0.5" opacity="0.3"/>
    <circle cx="200" cy="200" r="140" stroke="var(--cyan)" stroke-width="0.5" opacity="0.2"/>
    <circle cx="200" cy="200" r="90" stroke="var(--amber)" stroke-width="0.5" opacity="0.15"/>
  </svg>

  <div class="title-meta">PRESENTER / TEAM &mdash; DATE</div>
  <h1>Deck Title</h1>
  <h3>Subtitle or tagline</h3>

  <div class="title-stats">
    <span>15 slides</span>
    <span>~18 min</span>
  </div>
</section>
```

## Auto-calculated values

After generating all slides, count content slides and estimate duration:
- Section dividers / title cards: ~30 seconds each
- Standard content slides: ~1 minute each
- Dense slides (code, comparisons, detailed diagrams): ~1.5 minutes each

Update the title slide `title-stats` with these values. Recalculate after every editing pass.
