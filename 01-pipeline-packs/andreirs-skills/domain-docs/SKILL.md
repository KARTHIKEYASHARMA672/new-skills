---
name: domain-docs
description: Maintain a project's domain documentation — the GLOSSARY.md ubiquitous language and docs/adr/ architecture decision records. Use when a term needs a canonical definition, when a hard-to-reverse decision should be recorded, or when another skill (grill-me, to-spec) flags something worth capturing. Works standalone or chained in the same session.
---

# Domain Docs

Maintain two kinds of durable domain documentation, and nothing else:

- **`GLOSSARY.md`** — the project's glossary. What each term canonically means.
- **`docs/adr/`** — architecture decision records. Why a hard-to-reverse choice was made.

This skill owns the *mechanics* of both: where the files live, how they're formatted, when an entry is worth writing, and how decisions get superseded. Other skills (`grill-me`, `to-spec`) lean on it rather than re-describing any of this.

## When to use

- A term is fuzzy, overloaded, or used two different ways, and needs a canonical definition.
- A decision is being made that is hard to reverse, surprising without context, and the result of a real trade-off.
- Another skill flagged a term or decision worth capturing.
- You want to record terms/decisions already settled earlier in this same conversation: they're in context, so capture them, don't re-litigate them.

This skill does **not** write specs (`to-spec`), break work into issues (`to-issues`), or interview the user (`grill-me`). If a term is fuzzy because the *decision* behind it is unresolved, that's a grilling job, not a documentation job.

## File structure

Most repos have a single glossary at the root:

```
/
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-first-decision.md
│       └── 0002-second-decision.md
└── src/
```

A repo with multiple bounded contexts gets one `GLOSSARY.md` per context, next to the code it describes. There is no central index file to keep in sync — the set of `GLOSSARY.md` files *is* the map:

```
/
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── GLOSSARY.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── GLOSSARY.md
│       └── docs/adr/
```

When more than one `GLOSSARY.md` exists, write a term or decision into the **most local** one that owns it; only use the root `docs/adr/` for genuinely system-wide decisions. The same vocabulary can legitimately mean different things in different contexts (`account` in `ordering` need not match `account` in `billing`) — keep each definition in its own context rather than forcing a single global meaning.

> A true *context map* — how bounded contexts integrate (shared kernel, customer/supplier, anti-corruption layer, …) — is a hard-to-reverse, trade-off-laden decision, so it belongs in an ADR, not a glossary.

## Create lazily

Create files only when you have something to write.

- No `GLOSSARY.md` yet? Create it when the first term is resolved.
- No `docs/adr/` yet? Create it when the first ADR is needed.

The format references (`GLOSSARY-FORMAT.md` and `ADR-FORMAT.md`) are bundled with this skill. Read them to format entries — do **not** copy them into the target repo. They're scaffolding for this skill, not product docs; the existing entries serve as the by-example template for anyone editing later.

## The glossary (`GLOSSARY.md`)

`GLOSSARY.md` is a glossary and nothing else — it documents the project's ubiquitous language. It is **totally devoid of implementation details**. Do not treat it as a spec, a scratch pad, or a home for decisions. Those belong in specs and ADRs respectively.

Add or sharpen a term when:

- A word is used to mean two different things (`account` → is that the `Customer` or the `User`?).
- A term is vague or overloaded and a precise canonical name would remove the ambiguity.
- A new domain concept appears that future readers won't share your context on.

When you record a term, follow this skill's bundled `GLOSSARY-FORMAT.md`. Keep definitions short, name relationships to other terms, and call out what a term is explicitly **not**.

If a new term conflicts with an existing definition, surface the conflict instead of silently overwriting: "the glossary defines `Cancellation` as X, but this usage means Y — which is canonical?" Resolve, then update.

## ADRs (`docs/adr/`)

Record an ADR only when **all three** are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful.
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and one was chosen for specific reasons.

If any of the three is missing, skip the ADR. Most decisions don't warrant one; over-recording is its own kind of noise.

When you write one, follow this skill's bundled `ADR-FORMAT.md`. Number sequentially (`0001-`, `0002-`, …).

### Superseding

When a new decision overrides an old ADR, **do not silently rewrite history**. Either:

- flip the old ADR's status to `Superseded by ADR-NNNN`, or
- leave the old ADR intact and reference it from the new one.

The record of *why we changed our minds* is often more valuable than the decision itself.

## When you're done

Briefly list the files you created or changed, and the terms/ADRs added. If something surfaced that belongs in a spec rather than the glossary, say so and point at `to-spec` rather than recording it here.
</content>
</invoke>
