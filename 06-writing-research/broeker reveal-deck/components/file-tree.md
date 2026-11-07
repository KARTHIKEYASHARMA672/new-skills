---
name: file-tree
category: component
description: Monospace directory tree listing with color-coded dirs, files, and comments.
---

> **CSS:** All styles for this component are in `themes/electric-dark.css`. Do not add CSS from this file.

## Usage

Use to display file/directory structures. Color-code directories, files, comments, and symlink arrows.

## HTML

```html
<div class="file-tree">
  <span class="ft-dir">my-project/</span><br>
  &nbsp;&nbsp;<span class="ft-dir">src/</span><br>
  &nbsp;&nbsp;&nbsp;&nbsp;<span class="ft-file">index.js</span> <span class="ft-cmnt"># entry point</span><br>
  &nbsp;&nbsp;<span class="ft-file">package.json</span><br>
  &nbsp;&nbsp;<span class="ft-file">symlink</span> <span class="ft-arr">-></span> <span class="ft-cmnt">target/path</span>
</div>
```