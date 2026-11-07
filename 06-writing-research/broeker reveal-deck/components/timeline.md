---
name: timeline
category: component
description: Horizontal timeline with milestones, dates, or phases. Use for roadmaps, project history, or chronological progression.
---

> **CSS:** All styles for this component are in `themes/electric-dark.css`. Do not add CSS from this file.

## Usage

Use for anything with a chronological or phased sequence — project roadmaps,
historical context, release timelines, migration plans. Different from `flow`
(which shows a repeatable process); timeline shows progression through time.

## HTML

```html
<div class="timeline">
  <div class="tl-item">
    <span class="tl-date">Q1 2025</span>
    <div class="tl-dot"></div>
    <span class="tl-label">Research &amp; planning</span>
  </div>
  <div class="tl-item active">
    <span class="tl-date">Q2 2025</span>
    <div class="tl-dot"></div>
    <span class="tl-label">Build &amp; test</span>
  </div>
  <div class="tl-item">
    <span class="tl-date">Q3 2025</span>
    <div class="tl-dot"></div>
    <span class="tl-label">Team rollout</span>
  </div>
  <div class="tl-item">
    <span class="tl-date">Q4 2025</span>
    <div class="tl-dot"></div>
    <span class="tl-label">Full adoption</span>
  </div>
</div>
```