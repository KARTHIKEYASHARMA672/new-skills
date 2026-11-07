---
name: data-ingestion
description: Build reliable data ingestion — connecting to APIs, databases, files, or streams and landing data safely. Use this skill whenever the user wants to pull, fetch, load, sync, scrape, extract, or import data from any external source (REST APIs, SFTP, S3, Postgres, CSVs, webhooks, etc.), set up incremental loads, or fix a flaky/failing data fetch. Trigger even if the user just says "get the data from X into Y."
---

# Data Ingestion

Build ingestion that is **idempotent, incremental, and observable**. Ad-hoc scripts that "just fetch the data" become production liabilities; apply these patterns from the first draft.

## Workflow

1. **Profile the source first.** Before writing extraction code, inspect: auth method, rate limits, pagination style, schema, update semantics (append-only? mutable rows? deletes?), and volume. Write findings as comments at the top of the ingestion module.
2. **Run the ethics gate.** Before ingesting any dataset that could contain personal data, consult the `data-ethics-review` skill (PII, consent provenance, minimization). Ingest only the fields you need — minimization starts at extraction, not later.
3. **Choose a load strategy:**
   - *Full refresh* — small (<~1M rows), no reliable change tracking. Simple wins.
   - *Incremental by cursor* — source has `updated_at` / auto-increment ID. Persist the high-water mark (in the target DB or a state file), never in memory.
   - *CDC / log-based* — mutable source with deletes, high volume. Point to Debezium/native CDC rather than hand-rolling (see `streaming-data`).
4. **Land raw, then transform.** Write source data as-received into a raw/staging zone (schema `raw_<source>` or `landing/` prefix) before any transformation. Raw data is your replay buffer.
5. **Make it idempotent.** Re-running the same window must not duplicate data: use MERGE/upsert on natural keys, or delete-insert by partition. Test by running the job twice and diffing counts.

## Reliability patterns

- **Retries:** exponential backoff with jitter, cap attempts (e.g. 5), retry only on transient errors (429, 5xx, timeouts). Never retry on 4xx auth/validation errors.
- **Pagination:** always loop until an explicit termination signal (empty page / no next cursor), never assume page counts.
- **Rate limiting:** respect `Retry-After` headers; add a client-side limiter slightly under the documented cap.
- **Checkpointing:** for long backfills, commit state per chunk so a crash resumes rather than restarts.
- **Dead-letter handling:** records that fail parsing go to a quarantine table/file with the raw payload and error — never silently dropped.

## Observability minimums

Every ingestion job logs: rows read, rows written, rows quarantined, watermark before/after, wall-clock duration. Emit a non-zero exit code on partial failure so orchestrators (see `pipeline-builder`) can alert. Emit these as structured telemetry (spans/metrics) where the stack supports it — see `opentelemetry`.

## Secrets & compliance

- Credentials come from environment variables or a secrets manager — never hardcoded, never committed. Add config files with secrets to `.gitignore` immediately.
- Log record *counts*, never record *contents*, when data may contain personal information.
- Record the source, license/terms, and retrieval date of every external dataset (feeds `governance-docs`).

## Example: incremental API pull (Python skeleton)

```python
def sync(source, target, state_store):
    watermark = state_store.get("watermark", DEFAULT_START)
    for page in paginate(source, since=watermark, retry=backoff(max_tries=5)):
        rows, bad = validate(page)          # quarantine bad rows
        target.upsert("raw_source.events", rows, key="event_id")
        quarantine(bad)
        state_store.set("watermark", max_ts(rows))  # checkpoint per page
    log_metrics(read=..., written=..., quarantined=..., watermark=...)
```

When done, suggest adding validation contracts via the `data-quality` skill.
