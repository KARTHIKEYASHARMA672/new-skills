---
name: panel
category: component
description: Bordered card with optional color accent and label. Use for grouping related content.
---

> **CSS:** All styles for this component are in `themes/electric-dark.css`. Do not add CSS from this file.

## Usage

Use panels to group related content into visual cards. Supports color-coded left borders and an optional label header. Works well in 2-col and 3-col layouts.

## HTML

```html
<div class="panel panel-cyan">
  <div class="panel-label" style="color:var(--cyan)">LABEL TEXT</div>
  <p>Panel content goes here.</p>
</div>
```

**Variants:**
```html
<div class="panel panel-cyan">...</div>   <!-- lime/green left border -->
<div class="panel panel-amber">...</div>  <!-- amber left border -->
<div class="panel panel-red">...</div>    <!-- red left border -->
<div class="panel">...</div>              <!-- no colored border -->
```
