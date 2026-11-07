---
name: flow
category: component
description: Horizontal lifecycle/flow diagram with connected steps. Use for processes, workflows, and sequential stages.
---

> **CSS:** All styles for this component are in `themes/electric-dark.css`. Do not add CSS from this file.

## Usage

Use for any multi-step process or lifecycle. Steps connect with arrows. One step can be highlighted as `.active`.

## HTML

```html
<div class="flow">
  <span class="flow-step">Step 1</span>
  <span class="flow-arrow">-></span>
  <span class="flow-step active">Step 2</span>
  <span class="flow-arrow">-></span>
  <span class="flow-step">Step 3</span>
</div>
```
