---
name: spike-it
description: Answer one technical question with throwaway code — a spike, prototype, or investigation. Writes scrappy code outside the repo, runs it, reports the learning, and drops the code. Use for "can we...", "does X work with Y", "how fast is...", "prototype this", "let's spike it". Not for building the real thing; that's implement-tdd.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# spike-it

The code is a measuring instrument, not a deliverable. It exists to answer one question, then it gets thrown away. The learning is the only output that survives.

## Flow

1. **Name the question.** One sentence, plus one line on what a convincing answer looks like: "Can we stream Postgres changes into the worker under 200ms lag?" not "look into CDC". If there are several questions, pick the one that unblocks the most and say out loud which ones you're leaving.
2. **Cheapest harness that can answer it.** Work in the session scratchpad directory, never in the repo. Real dependency, fake data. One file. No tests, no error handling, no types, no abstractions, no config — hardcode everything. If a `curl` or a one-liner answers it, write no file at all.
3. **Run it and watch.** Print generously. Stop building the moment the answer is visible, even if the code is half-finished and ugly. Label what you observed vs inferred vs assumed.
4. **Report, then drop the code.** Chat report only. The files stay in the scratchpad and are never offered for merge.

## Rules

- Never edit files in the repo. Reading it to understand the question is fine.
- Notice something broken along the way? One line in the report. Don't fix it.
- If the spike starts growing, the question was too big. Cut it, re-ask smaller, say you did.
- If the answer is no, say no. Don't rescue the approach.
- Don't polish, don't refactor, don't generalise. Ugly is correct here.

## Report

```
Q: Can Bun's SQLite driver handle the 40k-row import in under a second?
A: Yes — 380ms for 40k rows with a prepared statement in a transaction. (observed)
Evidence: spike ran 5x, 360-410ms. Without the transaction: 11s.
Surprise: WAL mode made no difference at this size.
For real: needs batch size tuning above ~1M rows, untested.
Thrown away: <scratchpad>/sqlite-import-spike.ts
```

Then one next step: `to-spec` if it becomes a feature, `domain-docs` if the decision deserves an ADR, `to-issues` if it's ready to slice, `implement-tdd` to build it properly.
