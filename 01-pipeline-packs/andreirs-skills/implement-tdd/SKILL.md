---
name: implement-tdd
description: Implement an existing plan test-first, one behavior at a time, following the red-green-refactor loop. Use when the user has a plan, spec, or set of issues ready and wants the agent to build it TDD-style. Pairs with grill-me/to-issues, which produce the plan this skill consumes.
---

# Implement TDD

Build an existing plan test-first. One failing test, the minimum code to pass it, then refactor, repeated behavior by behavior. This skill consumes a plan; it does not write one. If there is no plan at all, stop and point the user at `grill-me`, `poke-holes`, or `to-issues`.

## Vocabulary

Three levels, kept distinct on purpose:

```
Plan        high-level intent: phases / milestones / a spec
  └─ Slice  a vertical, end-to-end unit of work, independently mergeable
      └─ Behavior  one observable thing the system does (one red-green cycle)
```

A **slice** is the `to-issues` notion: it cuts end-to-end through every layer the change touches (schema, API, UI, tests), so one person could pick it up, merge it, and have nothing left to wire up. A **behavior** is a single thing you can observe through the public interface, and it is what one red-green cycle proves.

## Test philosophy

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests should not. A good test reads like a specification ("user can checkout with valid cart") and survives a refactor because it does not care about internal structure.

Prefer integration-style tests that exercise real code paths through public APIs. Be suspicious of tests that mock internal collaborators, reach for private methods, or verify through a side channel (querying the database directly instead of going through the interface). The warning sign: the test breaks when you rename or move something internal, even though behavior is unchanged. That test was pinned to implementation.

## Stay vertical, at both levels

The same discipline applies twice, and going horizontal is the failure mode each time.

**Slicing the plan.** A slice must cut end-to-end through every layer it touches, so it is demoable or verifiable on its own. A horizontal slice ("build the whole data layer", "wire up all the endpoints") cannot be demoed alone and hides whether anything actually works. The test for a good slice: could one person merge it with nothing left to wire up? If no, it is incomplete; if yes but it is weeks of work, split it. Prefer many thin slices over few thick ones, in dependency order.

Example: a feature to let users export their orders as CSV.

```
BAD (horizontal): each "slice" is one layer, nothing works until the last
  1. Add the orders_export DB table and migration
  2. Add the /export API endpoint and serializer
  3. Add the "Export" button and download UI
  -> after slice 1 or 2 there is nothing to demo, and a wrong
     assumption in slice 1 is only caught once slice 3 lands

GOOD (vertical): each slice runs end-to-end and is mergeable on its own
  1. Export a single order as CSV via the public interface
     (the thin path through API + serialization + a download)
  2. Export all of a user's orders, with the column set finalized
  3. Add date-range filtering to the export
  -> slice 1 proves the whole path works and is demoable; each later
     slice adds one observable capability on top
```

Notice the bad slices are named after *layers* and the good ones after *capabilities a user can observe*. That is the tell.

**Looping inside a slice.** Do NOT write all the tests first and then all the code. That bulk approach produces bad tests: they verify *imagined* behavior, pin the *shape* of things (signatures, data structures) instead of what the system does, and go insensitive to real change (green when behavior breaks, red when it is fine). Go one behavior at a time instead, so each cycle responds to what the last one taught you.

```
WRONG (horizontal):
  write test1, test2, test3, test4, test5
  then impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  test1 -> impl1
  test2 -> impl2
  test3 -> impl3
  ...
```

## Workflow

### 1. Take the handoff and establish the slices

Read the plan (conversation, a spec file, or an issue reference) and figure out which shape it is:

- **Already sliced** (issues from `to-issues`, or a plan whose units are clearly vertical and mergeable): trust them. Build in dependency order; do not re-slice.
- **High-level only** (phases, milestones, a prose spec): derive vertical slices yourself using the slice test above. Then show the breakdown (titles, order, and one line on what makes each end-to-end) and get a quick OK before building. This is where horizontal mistakes are cheapest to catch.

Either way, before writing code:

- If the project has a domain glossary, `GLOSSARY.md`, or `docs/adr/`, skim the relevant parts and match your test names and interface vocabulary to that language. Skip silently if none exist.
- If you are on the default branch, create a working branch.

Invoking this skill is the go-ahead to build. The only approval gate is confirming slices you derived yourself.

### 2. List the behaviors for the current slice

For the slice you are about to build, list its observable behaviors. These are things the system does, not implementation steps. The plan sets the slice's scope; this list drives the red-green cycles inside it.

### 3. First behavior: prove the path

Take the first behavior and drive it through a full cycle:

```
RED:   write the test -> run it -> confirm it FAILS, and fails for the reason you expect
GREEN: write the minimum code to pass -> run it -> confirm it passes
```

Confirming the failure reason matters. A test that errors on a typo or a missing import is not a real RED. Make sure it fails because the behavior is absent, not because the test is broken. This first cycle proves the whole path works end to end: the harness, the interface, and the wiring.

### 4. Loop the remaining behaviors

For each remaining behavior in the slice:

```
RED:   write the next test -> run -> fails for the right reason
GREEN: minimum code to pass -> run -> passes
```

Rules:

- One test at a time. Only enough code to pass the current test.
- Do not anticipate future tests or add speculative features.
- Keep each test on one observable behavior through the public interface.

### 5. Refactor

Once the slice's tests are green, clean up with the tests as your safety net:

- Extract duplication.
- Deepen modules: move complexity behind a simple interface.
- Notice what the new code reveals about the old code.
- Run the tests after each refactor step and stay green.

Never refactor while RED. Get to green first.

### 6. Close the slice

When the slice is green and refactored, commit it as a single commit describing the slice, no need to ask first. Then move to the next slice and return to step 2.

If the working directory is not a git repository, skip committing entirely (do not run `git init`); just build the slices and tell the user once that there is no repo to commit to.

## Pause when something surprises you

Run through the slices on your own, but stop and ask the user when:

- The plan is ambiguous or conflicts with what the code actually does.
- A behavior is awkward to test because the interface the plan specified is not testable. Treat hard-to-test as a design smell: propose a better interface, and once the user agrees, build that.
- A test reveals a design problem or a behavior that looks wrong.
- A slice balloons well beyond its expected scope.

## Per-cycle checklist

```
[ ] Test describes behavior, not implementation
[ ] Test uses the public interface only
[ ] Test would survive an internal refactor
[ ] RED was real: it failed for the expected reason
[ ] Code is the minimum for this test
[ ] No speculative features added
```
