---
name: comparison
category: component
description: Side-by-side good/bad panels and verdict-style comparison grids. Use for before/after, with/without, or pros/cons.
---

> **CSS:** All styles for this component are in `themes/electric-dark.css`. Do not add CSS from this file.

## Usage

Two styles available: **box comparison** (two panels side by side) and **verdict grid** (label + description rows).

### Box comparison

```html
<div class="cols-2">
  <div class="compare bad">
    <span class="label bad">WITHOUT</span>
    <p>Description of the bad state.</p>
  </div>
  <div class="compare good">
    <span class="label good">WITH</span>
    <p>Description of the good state.</p>
  </div>
</div>
```

### Verdict grid

```html
<div class="compare-grid">
  <span class="verdict bad">AVOID</span>
  <span class="compare-text">Description of what to avoid</span>
  <span class="verdict good">PREFER</span>
  <span class="compare-text">Description of what to prefer</span>
</div>
```
