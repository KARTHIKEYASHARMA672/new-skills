---
name: resource-list
category: component
description: Categorized link list for resources slides. Groups links under mono-styled category headers.
---

> **CSS:** All styles for this component are in `themes/electric-dark.css`. Do not add CSS from this file.

## Usage

Use on resources/references slides to organize links by category.

## HTML

```html
<span class="res-cat">Official Documentation</span>
<ul class="res-list">
  <li><a href="https://example.com">Resource title</a> — brief description</li>
  <li><a href="https://example.com">Another resource</a></li>
</ul>

<span class="res-cat">Community</span>
<ul class="res-list">
  <li><a href="https://example.com">Community resource</a></li>
</ul>
```