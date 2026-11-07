# Skills library

A personal collection of reusable skills. Each top-level directory with a `SKILL.md` is one skill.

## Maintaining the size table

The README has a "Size at a glance" table comparing each skill's `SKILL.md` length (lines / words / estimated tokens). It lives between the `<!-- skill-sizes:start -->` and `<!-- skill-sizes:end -->` markers and is generated, not hand-edited.

After adding, removing, or editing any skill, regenerate it:

```bash
bun scripts/skill-sizes.ts --write
```

Keep `SKILL.md` files lean; the table exists to make creeping verbosity visible.
