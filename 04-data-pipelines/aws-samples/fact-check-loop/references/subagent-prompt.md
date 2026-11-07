# Subagent Prompt Template

Use this template to construct the prompt for each fact-check subagent.
Replace `{{placeholders}}` with actual values.

---

```
You are a fact-checker performing round {{ROUND_NUMBER}} of an iterative review.

## Task

Fact-check every claim in the document against the original source.
You must read BOTH the document and the FULL source before reporting.

## Document

Path: {{DOCUMENT_PATH}}
Format: {{FORMAT — pptx/docx/pdf/md/etc.}}

Extract text:
- .md/.txt: read the file directly
- .pdf: read with a page range, covering every page
- .pptx/.docx: convert first, e.g. `python3 -m markitdown {{DOCUMENT_PATH}}`

## Source(s)

{{SOURCE_INSTRUCTIONS — one of:}}

For URLs:
  Fetch with whatever web-retrieval tool you have. If the content exceeds
  ~30k characters, read it in sequential chunks until 100% covered.
  Do NOT summarize or skip sections.

For local files:
  Read the file. For large files, read in chunks with offset/limit until
  fully covered.

Source location(s): {{SOURCE_LOCATIONS}}

## Prior Fixes (rounds 1–{{ROUND_NUMBER - 1}})

{{If round 1: "This is the first round. No prior fixes."}}
{{If round 2+: paste the full fixes_log table:}}

| Round | Page/Section | Issue | Fix Applied |
|-------|-------------|-------|-------------|
{{...rows...}}

Verify each prior fix is correctly applied in the current document.
If a fix was applied incorrectly or introduced a new error, report it.

## How to Check

For each page/section of the document:

1. Identify every factual claim (numbers, percentages, names, dates,
   causal relationships, quotes, technical descriptions).
2. Locate the corresponding passage in the source.
3. Compare. Flag discrepancies.

If you cannot locate a claim anywhere in the source, that is itself a
finding — report it as a fabricated claim rather than assuming you missed it.

## Classification

Classify each finding as ONE of:
- **Factual error**: wrong number, inverted label, fabricated claim
- **Misleading omission**: missing context that changes the meaning
- **Imprecise wording**: oversimplified but not strictly wrong
- **Acceptable simplification**: inherent to summarization, not a problem

Only report the first three categories. Skip acceptable simplifications.

## Output Format

If NO issues found:

ALL_PASS

If issues found, output a numbered list:

ISSUES_FOUND

1. [Page/Section] [Category] — Description of issue.
   Source says: "exact quote or paraphrase from source"
   Document says: "exact quote from document"
   Suggested fix: brief description

2. ...

End with a summary line:
Total: X issues (Y factual errors, Z misleading omissions, W imprecise wording)

Also state which extraction path you used for the document and whether you
covered the source in full. A check run against a partial source or a bad
text extraction must be labeled as such, not reported as a pass.
```

---

## Notes for the main agent

- Use the most capable model the runtime offers. This is an accuracy task, not a
  throughput task, and a cheaper model's misses are invisible — they look like passes.
- Keep the subagent description short, e.g. `"Fact-check round N"`.
- Do NOT include instructions about how to fix — the subagent only identifies issues.
- After receiving results, the main agent decides how to fix each finding and whether
  it is valid. Subagents do occasionally flag correct text as wrong; verify against the
  source before editing rather than trusting the report outright.
- If the subagent flags something as "imprecise wording" and the fix would be disruptive,
  the main agent may skip it and note it in the final report.
- If the subagent reports partial source coverage, treat the round as inconclusive rather
  than as a pass, and re-run it.
