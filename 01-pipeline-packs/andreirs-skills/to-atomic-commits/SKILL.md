---
name: to-atomic-commits
description: Split uncommitted changes into logical atomic commits, one group of related files at a time. Detects commit message conventions and respects them. Use when changes have piled up in the working tree and should be committed as meaningful, independently-revertable units instead of one monolithic commit.
---

# To Atomic Commits

Turn the current working tree's uncommitted changes into a series of small, focused commits — each containing only files that belong together.

## Process

### 1. Check the working tree

Run `git status` and `git diff` (staged + unstaged) to understand what has changed.

If there are no uncommitted changes, tell the user and stop.

### 2. Detect commit message conventions

Look for commit message conventions in this priority order:

1. **CLAUDE.md** — search the project and user CLAUDE.md files for commit message rules.
2. **`.gitmessage`** — if present in the repo root, read it.
3. **commitlint config** — check for `commitlint.config.js`, `.commitlintrc`, `.commitlintrc.json`, `.commitlintrc.yaml`, or a `commitlint` key in `package.json`.
4. **Recent git log** — run `git log --oneline -20` and infer the pattern (conventional commits, ticket-prefixed, imperative mood only, etc.).
5. **Default** — if nothing is found, use short imperative-mood sentences with no period.

Summarise the detected convention in one line before proceeding (e.g. "Detected: Conventional Commits (`feat:`, `fix:`, `chore:`)").

### 3. Group files into atomic commits

Analyse all changed files and group them into the smallest set of logical commits where:

- Each commit contains only files that are **causally related** (same feature, same bug fix, same refactor, same config change, etc.).
- Each commit is **independently revertable** — reverting it should leave the rest of the codebase in a consistent state.
- Files that touch multiple concerns are split **by staging hunks** (`git add -p`) when a clean file-level split is not possible.

Common groupings to look for:
- New feature or behaviour change + its tests
- Dependency or lockfile updates (together)
- Config / tooling changes (separate from product code)
- Docs or README changes (separate unless they explain code in the same commit)
- Refactors that are pure renames or moves (separate from logic changes)
- Build or CI changes (separate from app code)

### 4. Propose the plan

Before touching git, present the proposed commit breakdown as a numbered list:

```
1. <commit message>
   Files: foo.ts, bar.ts, foo.test.ts

2. <commit message>
   Files: package.json, bun.lockb

3. ...
```

Ask the user: "Does this breakdown look right, or should I adjust any groupings?"

Wait for approval. If the user requests changes, revise and re-present until approved.

### 5. Execute commits in order

For each group in the approved plan:

1. Stage only the files in that group (`git add <files>` or `git add -p` for partial files).
2. Verify the staged diff matches the intended group (`git diff --staged --stat`).
3. Commit with a message that follows the detected convention.
4. Confirm the commit was created (`git log -1 --oneline`).

After all commits, run `git log --oneline -<n>` (where n = number of commits made) so the user can see the final result.

## Rules

- Never use `--no-verify` or skip hooks unless the user explicitly asks.
- Never amend existing commits — always create new ones.
- If a commit fails (hook rejection, conflict, etc.), stop, report the error, and wait for the user to decide how to proceed.
- Do not push — stop after all local commits are made.
- If the user's approval message indicates a different grouping than proposed, re-plan and re-present; don't just charge ahead.
