---
name: data-quality
description: Define and enforce data quality — validation rules, data contracts, anomaly detection, freshness checks, using dbt tests, Great Expectations, Pandera, or plain SQL assertions. Use this skill whenever the user mentions bad data, duplicates, nulls, broken dashboards, "the numbers look wrong," validating a dataset, testing a pipeline's data, or setting up data contracts and quality monitoring.
---

# Data Quality

Quality checks are **executable expectations placed at trust boundaries**: where data enters, where it transforms, and where it's consumed.

## The six dimensions (check coverage against these)

1. **Completeness** — required fields non-null, expected row volumes present.
2. **Uniqueness** — primary/natural keys have no duplicates.
3. **Validity** — values in range/enum/format (emails parse, amounts ≥ 0, dates plausible).
4. **Consistency** — cross-table integrity (FKs resolve, totals reconcile across systems).
5. **Freshness** — data as recent as the SLA promises (`max(loaded_at)` within threshold).
6. **Accuracy** — matches reality; hardest to automate, so spot-check against a source of truth and reconcile known aggregates.

## Where to put checks

- **Ingestion boundary:** schema + validity checks; bad rows → quarantine with raw payload (see `data-ingestion`).
- **Post-transformation:** uniqueness of keys, referential integrity, business-rule assertions, row-count deltas vs. previous run.
- **Consumption boundary:** freshness + reconciliation checks on marts that dashboards/apps read.

## Severity: block vs. warn

Classify every check. **Blocking** (stop the pipeline): key duplication, schema breakage, failed reconciliation, empty required source. **Warning** (alert, continue): volume drift within tolerance, rising null rates in optional fields. Publishing silently-wrong data damages trust more than a late dashboard.

## Tool selection

- **dbt projects:** built-in tests (`unique`, `not_null`, `relationships`, `accepted_values`) + `dbt_utils`/`dbt_expectations` for the rest. Freshness via `sources: freshness:`.
- **Pandas/Python pipelines:** Pandera schemas (typed, composable) or Great Expectations if the team wants docs/UI.
- **Anything with SQL access:** plain SQL assertions are underrated — a query that returns offending rows, wrapped in a runner that fails on non-empty result.

## Anomaly detection (cheap version first)

Before ML-based monitoring, implement: row count vs. trailing 7-run median (alert beyond ±3 MAD), null-rate per column vs. baseline, and new-category detection on enum columns. This catches most real incidents.

## Data contracts

For interfaces between teams/systems, write the expectation down as a versioned artifact (YAML/JSON schema): columns, types, nullability, keys, freshness SLA, owner, and change policy. Enforce it in CI on the producer side — a contract only the consumer checks is a complaint form.

At organization scale (data mesh), this generalizes: each domain team owns its data as a product — contract, quality checks, freshness SLA, and a named owner published with the dataset. Federate the standards (classification scheme, contract format, `governance-docs` templates), not the ownership.

## Quality is also an ethics issue

Biased or broken data produces harmful decisions. When profiling quality, also check **representation**: missing-data rates and volumes segmented by key population groups where relevant — systematic gaps for one group are a fairness defect, not just a stats footnote. Escalate findings to `data-ethics-review`.

## Deliverable pattern

When adding quality to a project, produce: (1) a check inventory table (check, dimension, location, severity, owner), (2) the implemented tests, (3) alert wiring, and (4) a short runbook: what to do when each blocking check fails.
