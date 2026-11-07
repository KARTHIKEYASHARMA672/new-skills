---
name: codeblock
category: component
description: Terminal-style code container with faux macOS dots header. Use for commands, file contents, and code snippets.
---

> **CSS:** All styles for this component are in `themes/electric-dark.css`. Do not add CSS from this file.

## Usage

Use for any terminal commands, code snippets, or file contents. The faux dot header gives it a terminal/IDE feel.

## HTML

```html
<div class="codeblock">
  <div class="codeblock-header">
    <span class="codeblock-dot" style="background:#FF5F56"></span>
    <span class="codeblock-dot" style="background:#FFBD2E"></span>
    <span class="codeblock-dot" style="background:#27C93F"></span>
  </div>
  <pre><code>your code here</code></pre>
</div>
```
