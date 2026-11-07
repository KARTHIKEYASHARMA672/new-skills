---
name: icon-grid
category: component
description: Grid of icon + label + description blocks. Use for feature overviews, capability lists, or category breakdowns.
---

> **CSS:** All styles for this component are in `themes/electric-dark.css`. Do not add CSS from this file.

## Usage

Use when presenting multiple features, capabilities, or categories that are
peers — each gets equal visual weight. More compact and visual than panels.
Works best with 3, 4, or 6 items.

Icons can be emoji, inline SVG, or single characters.

## HTML

```html
<div class="icon-grid">
  <div class="icon-grid-item">
    <span class="icon-grid-icon">&#9889;</span>
    <span class="icon-grid-label">Fast</span>
    <span class="icon-grid-desc">Skip the setup, get to the work.</span>
  </div>
  <div class="icon-grid-item">
    <span class="icon-grid-icon">&#128736;</span>
    <span class="icon-grid-label">Flexible</span>
    <span class="icon-grid-desc">Works with any project or tool.</span>
  </div>
  <div class="icon-grid-item">
    <span class="icon-grid-icon">&#129309;</span>
    <span class="icon-grid-label">Shareable</span>
    <span class="icon-grid-desc">Team-wide skills from day one.</span>
  </div>
</div>
```

**With inline SVG icons:**
```html
<div class="icon-grid-item">
  <span class="icon-grid-icon">
    <svg width="1.2em" height="1.2em" viewBox="0 0 24 24" fill="currentColor">
      <!-- path data -->
    </svg>
  </span>
  <span class="icon-grid-label">Feature</span>
  <span class="icon-grid-desc">Description here.</span>
</div>
```
