---
name: pipeline-builder
description: Design and build data pipelines and orchestration — DAGs, scheduling, dependencies, backfills, alerting, using Airflow, Dagster, Prefect, dbt, cron, or GitHub Actions. Use this skill whenever the user wants to schedule data jobs, chain ETL/ELT steps, automate a data workflow, set up orchestration, handle backfills, or make an existing pipeline reliable. Trigger even for "run this script every night."
---

# Pipeline Builder

A pipeline is a **DAG of idempotent tasks with explicit state**. Everything else — tool choice, scheduling — follows from that.

## Choose the right orchestrator (don't over-tool)

| Situation | Reach for |
|---|---|
| 1–3 jobs, single machine | cron + a wrapper script with logging & alerting |
| Repo-centric, already on GitHub | GitHub Actions scheduled workflows |
| SQL-first transformations | dbt (+ dbt Cloud/cron for scheduling) |
| Many jobs, dependencies, backfills, team | Airflow or Dagster |
| Python-native, dynamic flows | Prefect or Dagster |
| Genuinely sub-minute latency, CDC, event streams | Kafka/Flink — see `streaming-data` |

State the trade-off to the user before scaffolding a heavy tool.

## Design rules

1. **ELT over ETL by default:** land raw data first (see `data-ingestion`), transform inside the warehouse. Raw data enables replay; in-flight transformation destroys it.
2. **Tasks are idempotent and atomic.** Re-running any task with the same logical date produces the same result. Use partition overwrite or MERGE, write to temp then swap.
3. **Parameterize by logical date/window,** never `now()`. `run(date)` makes backfills trivial: a backfill is just a loop over dates.
4. **Explicit dependencies, no hidden coupling.** Task B reads only what task A declares it produces. In Airflow/Dagster, model this as assets/datasets where supported.
5. **Fail loudly, resume cheaply.** Retries with backoff at the task level (2–3 attempts); checkpoint state; on final failure, alert with enough context to act (job, window, error, row counts).
6. **Separate compute from schedule.** Business logic lives in importable, unit-testable functions/models; the orchestrator file only wires and schedules them.

## Standard pipeline shape

```
ingest (per source) → validate (data-quality gates) → transform (staging → marts)
→ publish (views/exports/apps) → notify
```
Validation failures should **block downstream tasks**, not just warn — a pipeline that publishes bad data on green is worse than one that stops.

## Backfills

- Make backfill a first-class command: `pipeline backfill --start 2026-01-01 --end 2026-03-31`.
- Rate-limit backfills against production sources; prefer replaying from the raw zone.
- After a logic change, document which historical partitions were rebuilt (feeds `governance-docs` lineage notes).

## Operations & ethics

- Every run logs: logical window, rows in/out per task, duration, and validation results.
- Schedule respectfully: don't hammer third-party APIs at peak; honor robots.txt and API terms.
- Retention is part of the pipeline: add scheduled deletion/expiry tasks for data with retention limits (see `privacy-engineering`) — retention policies that no job enforces are fiction.
- Alerts go to a channel someone actually reads; every alert should be actionable or it trains people to ignore alerts.

## Testing

- Unit-test transformation logic with fixture data.
- Add one end-to-end smoke test on a tiny sample that runs in CI.
- dbt: `dbt build` (tests + models) in CI on every PR against a scratch schema.
