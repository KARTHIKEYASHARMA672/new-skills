# HTML Report Format

The architectural review is rendered as a single self-contained HTML file in the OS temp directory. Tailwind and Mermaid both come from CDNs. Mermaid handles graph-shaped diagrams reliably; hand-built divs and inline SVG handle the more editorial visuals (mass diagrams, cross-sections). Mix the two — don't lean on Mermaid for everything, it'll start to look generic.

Architectural vocabulary comes from the **Glossary** in [SKILL.md](SKILL.md) — module, interface, implementation, depth, deep, shallow, seam, adapter, leverage, locality. That is the single source of truth for terms; this file never redefines them.

## Theme

The report is **dark-first**. It supports three modes — **System / Light / Dark** — toggled from a control in the header and persisted in `localStorage` under `arch-theme`. On first open (no stored choice) the mode is **System**: it follows the OS `prefers-color-scheme`, and **falls back to dark** when the OS expresses no preference. Theme is resolved in an inline script in `<head>` *before* paint, so there's no light flash.

Tailwind runs in `darkMode: "class"` — every coloured surface needs a `dark:` variant (see [Dark variants](#dark-variants)). Mermaid re-renders on theme change: `theme: "neutral"` in light, `theme: "dark"` in dark. The scaffold below wires all of this; copy it verbatim and only fill in the content.

## Scaffold

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Architecture review — {{repo name}}</title>

    <!-- Resolve theme before paint (no flash). Default mode = system, dark fallback.
         localStorage is wrapped in try/catch: it throws on file:// (Safari) and in
         private-browsing modes, and an unguarded throw here would kill theming. -->
    <script>
      (function () {
        var mode = "system"; // "light" | "dark" | "system"
        try { mode = localStorage.getItem("arch-theme") || "system"; } catch (e) {}
        var sysDark = matchMedia("(prefers-color-scheme: dark)").matches;
        var sysLight = matchMedia("(prefers-color-scheme: light)").matches;
        var dark =
          mode === "dark" ? true :
          mode === "light" ? false :
          sysDark ? true : sysLight ? false : true; // system: follow OS, else dark
        document.documentElement.classList.toggle("dark", dark);
        window.__archThemeMode = mode;
      })();
    </script>

    <script src="https://cdn.tailwindcss.com"></script>
    <script>
      tailwind.config = { darkMode: "class" };
    </script>

    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      var nodes = [...document.querySelectorAll("pre.mermaid")];
      nodes.forEach((el) => (el.dataset.src = el.textContent)); // stash source for re-render
      function render() {
        nodes.forEach((el) => {
          el.removeAttribute("data-processed");
          el.innerHTML = el.dataset.src;
        });
        mermaid.initialize({
          startOnLoad: false,
          securityLevel: "loose",
          theme: document.documentElement.classList.contains("dark") ? "dark" : "neutral",
        });
        mermaid.run({ nodes });
      }
      render();
      window.__archRenderMermaid = render; // toggle calls this after switching theme
    </script>

    <style>
      /* small custom layer for things Tailwind doesn't cover cleanly:
         dashed seam lines, hand-drawn-feeling arrow heads, etc. */
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      /* "deep module" fill works on both themes — dark slab on light, darker on dark */
      .deep { background: linear-gradient(135deg, #1e293b, #334155); }
      .dark .deep { background: linear-gradient(135deg, #020617, #0f172a); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100 font-sans antialiased transition-colors">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>

    <!-- Theme toggle: cycles System → Light → Dark. -->
    <script>
      (function () {
        var btn = document.getElementById("theme-toggle");
        var mql = matchMedia("(prefers-color-scheme: dark)");
        var order = ["system", "light", "dark"];
        var label = { system: "🖥️ System", light: "☀️ Light", dark: "🌙 Dark" };
        var mode = window.__archThemeMode || "system";
        function apply() {
          var dark =
            mode === "dark" ? true :
            mode === "light" ? false :
            mql.matches ? true : matchMedia("(prefers-color-scheme: light)").matches ? false : true;
          document.documentElement.classList.toggle("dark", dark);
          if (btn) btn.textContent = label[mode];
          if (window.__archRenderMermaid) window.__archRenderMermaid();
        }
        if (btn)
          btn.addEventListener("click", function () {
            mode = order[(order.indexOf(mode) + 1) % order.length];
            try { localStorage.setItem("arch-theme", mode); } catch (e) {}
            apply();
          });
        mql.addEventListener("change", function () { if (mode === "system") apply(); });
        apply();
      })();
    </script>
  </body>
</html>
```

## Header

Repo name, date, and a compact legend: solid box = module, dashed line = seam, red arrow = leakage, thick dark box = deep module. No introduction paragraph — straight into the candidates.

Include the theme toggle here, right-aligned — a single pill button the user clicks to cycle modes:

```html
<button
  id="theme-toggle"
  type="button"
  class="rounded-full border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800
         px-3 py-1.5 text-sm text-slate-700 dark:text-slate-200 hover:bg-slate-100
         dark:hover:bg-slate-700 transition-colors"
>🌙 Dark</button>
```

The button's label is set by the toggle script on load — the literal text above is just a placeholder.

## Candidate card

This is the **authoritative card spec** — SKILL.md defers to it. The diagrams carry the weight. Prose is sparse, plain, and uses the glossary terms without ceremony.

Each candidate is one `<article>`:

- **Title** — short, names the deepening (e.g. "Collapse the Order intake pipeline").
- **Badge** — recommendation strength only: `Strong` = emerald, `Worth exploring` = amber, `Speculative` = slate. Use translucent fills that read on both themes, e.g. `bg-emerald-100 text-emerald-800 dark:bg-emerald-500/15 dark:text-emerald-300`.
- **Files** — monospaced list, `font-mono text-sm`.
- **Before / After diagram** — the centrepiece. Two columns, side by side. See patterns below.
- **Problem** — one sentence. What hurts.
- **Solution** — one sentence. What changes. Describe the deepening in plain English — **no interface signatures, no code**. Design happens later, not here.
- **Wins** — bullets, ≤6 words each. e.g. "Tests hit one interface", "Pricing logic stops leaking", "Delete 4 shallow wrappers".
- **ADR callout** (only if `docs/adr/` exists and a candidate contradicts a recorded ADR) — one line in an amber-tinted box: _"contradicts ADR-0007, but worth revisiting because…"_.

No paragraphs of explanation. If the diagram needs a paragraph to be understood, redraw the diagram.

## Diagram patterns

Pick the pattern that fits the candidate. Mix them. Don't make every diagram look the same — variety is part of the point.

### Mermaid graph (the workhorse for dependencies / call flow)

Use a Mermaid `flowchart` or `graph` when the point is "X calls Y calls Z, and look at the mess." Wrap it in a Tailwind-styled card so it doesn't feel parachuted in. Style with classDef to colour leakage edges red and the deep module dark. Sequence diagrams work well for "before: 6 round-trips; after: 1."

```html
<div class="rounded-lg border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4">
  <pre class="mermaid">
    flowchart LR
      A[OrderHandler] --> B[OrderValidator]
      B --> C[OrderRepo]
      C -.leak.-> D[PricingClient]
      classDef leak stroke:#dc2626,stroke-width:2px;
      class C,D leak
  </pre>
</div>
```

Leakage red (`#dc2626`) and the deep-module slab read on both themes, so `classDef` colours stay as-is — the re-render just swaps Mermaid's base palette. Don't hardcode light fills (white node backgrounds, near-black text) inside the diagram; let the Mermaid theme supply them.

### Hand-built boxes-and-arrows (when Mermaid's layout fights you)

Modules as `<div>`s with borders and labels. Arrows as inline SVG `<line>` or `<path>` elements positioned absolutely over a relative container. Reach for this when you want the "after" diagram to feel like one thick-bordered deep module with greyed-out internals — Mermaid won't render that with the right weight.

### Cross-section (good for layered shallowness)

Stack horizontal bands (`h-12 border-l-4`) to show layers a call passes through. Before: 6 thin layers each doing nothing. After: 1 thick band labelled with the consolidated responsibility.

### Mass diagram (good for "interface as wide as implementation")

Two rectangles per module — one for interface surface area, one for implementation. Before: interface rectangle is nearly as tall as the implementation rectangle (shallow). After: interface rectangle is short, implementation rectangle is tall (deep).

### Call-graph collapse

Before: a tree of function calls rendered as nested boxes. After: the same tree collapsed into one box, with the now-internal calls shown faded inside it.

## Style guidance

- Lean editorial, not corporate-dashboard. Generous whitespace. Serif optional for headings (`font-serif` works well with stone/slate).
- Colour sparingly: one accent (emerald or indigo) plus red for leakage and amber for warnings.
- Keep diagrams ~320px tall so before/after sits comfortably side by side without scrolling.
- Use `text-xs uppercase tracking-wider` for module labels inside diagrams — they should read as schematic, not as UI.
- The only scripts are the theme resolver, the Tailwind CDN + config, the Mermaid ESM import, and the toggle. The report is otherwise static — no app code, no interactivity beyond the theme toggle and Mermaid's own rendering.

### Dark variants

The report is dark-first; the eye should never get flash-burned. **Every coloured surface needs a `dark:` variant** — if you write a `bg-`, `text-`, `border-`, or `ring-` utility, pair it with its dark counterpart. Untag elements inherit the body (`dark:bg-slate-950 dark:text-slate-100`), so a plain element is safe; a *coloured* one is not.

Tune for dark first, then sanity-check light. Reach for the same families both schemes already use:

- **Surfaces** — `bg-white dark:bg-slate-900` for cards; `bg-stone-50 dark:bg-slate-950` for the page.
- **Borders** — `border-slate-200 dark:border-slate-800`.
- **Body / muted text** — `text-slate-900 dark:text-slate-100`; muted `text-slate-500 dark:text-slate-400`.
- **Accents & badges** — solid-on-light, translucent-on-dark: `text-emerald-700 dark:text-emerald-300`, `bg-amber-100 dark:bg-amber-500/15`. The ADR callout's amber tint follows the same pattern.
- **Leakage red** stays `#dc2626` in both — it's a warning, it should bite on either background.

## Top recommendation section

One larger card. Candidate name, one sentence on why, anchor link to its card. That's it.

## Tone

Plain English, concise — but the architectural nouns and verbs come straight from the Glossary in [SKILL.md](SKILL.md). Concision is not an excuse to drift.

**Use exactly:** module, interface, implementation, depth, deep, shallow, seam, adapter, leverage, locality.

**Never substitute:** component, service, unit (for module) · API, signature (for interface) · boundary (for seam) · layer, wrapper (for module, when you mean module).

**Phrasings that fit the style:**

- "Order intake module is shallow — interface nearly matches the implementation."
- "Pricing leaks across the seam."
- "Deepen: one interface, one place to test."
- "Two adapters justify the seam: HTTP in prod, in-memory in tests."

**Wins bullets** name the gain in glossary terms: *"locality: bugs concentrate in one module"*, *"leverage: one interface, N call sites"*, *"interface shrinks; implementation absorbs the wrappers"*. Don't write *"easier to maintain"* or *"cleaner code"* — those terms aren't in the glossary and don't earn their place.

No hedging, no throat-clearing, no "it's worth noting that…". If a sentence could be a bullet, make it a bullet. If a bullet could be cut, cut it. If a term isn't in the glossary, reach for one that is before inventing a new one.
