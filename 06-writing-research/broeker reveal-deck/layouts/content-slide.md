---
name: content-slide
category: layout
description: Standard workhorse slide with slug, accent line, and title. Prefer 2-column layout.
---

> **CSS:** All styles for this layout are in `themes/electric-dark.css`. Do not add CSS from this file.

## Usage

The default slide type for most content. Every content slide gets a `{NNN}` slug, accent line, and h2 title. Prefer 2-column layouts; use single column with a panel or callout to fill visual weight when needed.

**Before using this layout with plain bullet lists, consider whether a richer
component fits the content better:**
- 3-6 items with labels → `icon-grid` (with emoji icons)
- Ordered steps → `step-list` (with circled numbers)
- Key takeaways → `key-item` (with large accent numbers)
- Grouped concepts → `panel` in `cols-2` or `cols-3`
- Process/flow → `flow` diagram

Plain `<ul>` bullets should only appear when content is truly unstructured
or when nested inside another component like a `panel`.

## HTML

```html
<section data-background-color="#060A12">
  <span class="slide-tag">{001}</span>
  <div class="accent-line"></div>
  <h2>Slide Title</h2>

  <!-- 2-column layout (preferred) -->
  <div class="cols-2">
    <div>
      <p>Left column content.</p>
    </div>
    <div>
      <div class="panel panel-cyan">
        <div class="panel-label" style="color:var(--cyan)">KEY POINT</div>
        <p>Right column content in a panel.</p>
      </div>
    </div>
  </div>
</section>
```

**Single column variant:**
```html
<section data-background-color="#060A12">
  <span class="slide-tag">{002}</span>
  <div class="accent-line"></div>
  <h2>Slide Title</h2>
  <p>Content paragraph.</p>
  <div class="callout">Key takeaway here.</div>
</section>
```
