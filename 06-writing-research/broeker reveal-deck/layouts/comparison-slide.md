---
name: comparison-slide
category: layout
description: Side-by-side comparison slide for before/after, with/without, good/bad.
---

## Usage

Use when contrasting two states, approaches, or options. Combines the `comparison` component with `cols-2` layout.

## HTML

```html
<section data-background-color="#060A12">
  <span class="slide-tag">{004}</span>
  <div class="accent-line"></div>
  <h2>Comparison Title</h2>

  <div class="cols-2">
    <div class="compare bad">
      <span class="label bad">WITHOUT</span>
      <ul>
        <li>Pain point one</li>
        <li>Pain point two</li>
      </ul>
    </div>
    <div class="compare good">
      <span class="label good">WITH</span>
      <ul>
        <li>Benefit one</li>
        <li>Benefit two</li>
      </ul>
    </div>
  </div>
</section>
```
