---
name: resources-slide
category: layout
description: Categorized links slide for references, docs, and further reading.
---

## Usage

Use as a closing or appendix slide to collect external links organized by category. Uses the `resource-list` component. Works well in 2-column or 3-column layout.

## HTML

```html
<section data-background-color="#060A12">
  <span class="slide-tag">{015}</span>
  <div class="accent-line"></div>
  <h2>Resources</h2>

  <div class="cols-2">
    <div>
      <span class="res-cat">Official Documentation</span>
      <ul class="res-list">
        <li><a href="https://example.com">Resource title</a> — description</li>
        <li><a href="https://example.com">Another resource</a></li>
      </ul>

      <span class="res-cat">Community</span>
      <ul class="res-list">
        <li><a href="https://example.com">Community resource</a></li>
      </ul>
    </div>
    <div>
      <span class="res-cat">Articles &amp; Guides</span>
      <ul class="res-list">
        <li><a href="https://example.com">Article title</a> — author</li>
      </ul>
    </div>
  </div>
</section>
```
