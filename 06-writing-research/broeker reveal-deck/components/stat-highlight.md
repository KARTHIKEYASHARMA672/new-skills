---
name: stat-highlight
category: component
description: Large number or statistic with label and optional context line. Use for data points, metrics, percentages, or any number that needs to land with impact.
---

> **CSS:** All styles for this component are in `themes/electric-dark.css`. Do not add CSS from this file.

## Usage

Use when a single number or metric is the main point of a slide or section.
Works standalone, in pairs (cols-2), or in a row of three (cols-3). The number
should be large enough to read from the back of the room.

## HTML

**Single stat:**
```html
<div class="stat">
  <span class="stat-number">87%</span>
  <span class="stat-label">of teams report faster deploys</span>
</div>
```

**Stat with context line:**
```html
<div class="stat">
  <span class="stat-number">3x</span>
  <span class="stat-label">faster onboarding</span>
  <span class="stat-context">compared to manual documentation</span>
</div>
```

**Multiple stats in a row:**
```html
<div class="cols-3">
  <div class="stat">
    <span class="stat-number">87%</span>
    <span class="stat-label">adoption rate</span>
  </div>
  <div class="stat">
    <span class="stat-number">3x</span>
    <span class="stat-label">faster deploys</span>
  </div>
  <div class="stat">
    <span class="stat-number">42</span>
    <span class="stat-label">skills created</span>
  </div>
</div>
```
