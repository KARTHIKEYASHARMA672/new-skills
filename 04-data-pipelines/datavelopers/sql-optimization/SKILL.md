---
name: sql-optimization
description: Write correct analytical SQL and make it fast and cheap — translating business questions into queries, query tuning, EXPLAIN plans, indexing, partitioning, clustering, materialization, and cost-aware patterns for Postgres, MySQL, BigQuery, Snowflake, Redshift, and DuckDB. Use this skill whenever the user asks to write a SQL query or report, or mentions a slow query, timeouts, high warehouse bills, indexes, query plans, or "make this SQL faster/cheaper."
---

# SQL Optimization

Measure, read the plan, fix the biggest cost, re-measure. Never optimize by folklore.

## From business question to correct query (before speed)

- **Pin down the dialect and the schema first** — read the DDL, docs, or dbt models before writing a line; guessed column semantics produce confidently wrong numbers.
- **Restate the question as a grain statement:** "one row per customer per month" decides the joins and GROUP BY before syntax does (see `data-modeling`).
- **Reuse existing metric definitions** from the semantic layer/metrics file rather than re-deriving revenue or active-user logic per query (see `analytics`).
- **Watch join fan-out:** after every join, check row counts against the expected grain — a silently exploding join is the classic source of doubled revenue.
- **Verify before delivering:** reconcile totals against a known-good number, and state filters and time windows in the query header comment.

## Diagnosis workflow

1. **Get the plan:** `EXPLAIN (ANALYZE, BUFFERS)` in Postgres; query profile in Snowflake; execution details in BigQuery. Read from the most expensive node outward.
2. **Find the dominant cost.** Usually one of: full scan of a large table, a mis-ordered/exploding join, a sort/spill to disk, or row-by-row execution (correlated subquery, UDF per row).
3. **Fix that one thing. Re-measure.** Repeat.

## The high-yield fixes (in rough order of frequency)

- **Filter earlier.** Push predicates into subqueries/CTEs before joins; select only needed columns (`SELECT *` defeats column pruning in columnar warehouses — this alone often cuts BigQuery/Snowflake cost dramatically).
- **Sargable predicates.** `WHERE date_col >= '2026-01-01'` uses an index/partition; `WHERE YEAR(date_col) = 2026` doesn't. Never wrap the indexed column in a function — move the function to the constant side.
- **Join keys typed and matched.** Implicit casts (varchar vs int) disable index use and skew join strategies.
- **De-duplicate before joining,** not after — exploding joins then `DISTINCT` is a classic plan killer.
- **Replace correlated subqueries** with joins or window functions.
- **`EXISTS` over `IN (subquery)`** for large semi-joins in OLTP engines.

## Indexing (OLTP: Postgres/MySQL)

- Index FK columns and columns in frequent `WHERE`/`ORDER BY`; composite indexes ordered by (equality cols first, then range col).
- Covering indexes (`INCLUDE`) for hot read paths; partial indexes for common filters (`WHERE status = 'active'`).
- Every index taxes writes and storage — remove unused ones (`pg_stat_user_indexes`).

## Warehouse physical design (OLAP)

- **Partition** big tables by the dominant filter column (almost always date). Confirm queries actually prune (bytes scanned should drop).
- **Cluster/sort** within partitions by the next most common filter/join key.
- **Materialize** expensive shared logic: incremental models (dbt) or materialized views for anything computed repeatedly. Recompute windows incrementally, not full-table.

## Cost hygiene (cloud warehouses)

- Preview with dry-run/bytes-scanned estimates before running exploratory queries on big tables; develop against a sampled dev dataset.
- Right-size and auto-suspend Snowflake warehouses; set per-user/query byte caps in BigQuery.
- Track the top-10 most expensive recurring queries monthly — optimization effort goes where the money is. Cost efficiency is also an environmental footprint issue; treat wasted compute as waste.

## Don't sacrifice correctness

After any rewrite, verify equivalence: row counts and checksums/aggregates match the original on a fixed window. A fast wrong query is a data-quality incident (see `data-quality`).

For advanced query patterns, transactions, schema migrations, and SQL security, see `sql-engineering`.
