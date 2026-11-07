---
name: data-modeling
description: Design database schemas and analytical data models — tables, keys, normalization, star schemas, dbt-style layered transformations. Use this skill whenever the user wants to design tables, model entities, create a schema, restructure a warehouse, choose between normalized and dimensional designs, or organize dbt models. Trigger even for casual asks like "how should I structure this data?"
---

# Data Modeling

Choose the model for the *workload*, then make the design explicit, documented, and evolvable.

## Step 1: Identify the workload

- **OLTP (apps, transactions):** normalize to 3NF. Optimize for write integrity and row lookups.
- **OLAP (analytics, BI):** dimensional model — star schema with fact and dimension tables. Optimize for scans and joins on surrogate keys.
- **Hybrid/small:** one clean normalized schema plus reporting views is often enough. Don't build a warehouse for 50k rows.
- **Known-query, extreme-scale serving** (high-throughput lookups, cluster-scale writes): query-first NoSQL design — see `nosql-modeling`.
- **Relationship-traversal workloads** (networks, multi-hop paths, pattern matching): see `graph-modeling`.

## Step 2: Model the business, not the source

Name tables and columns after business concepts (`orders`, `customer_id`, `shipped_at`), not source-system jargon. Every entity gets:
- A stable primary key (surrogate keys for dimensions; document natural keys as unique constraints).
- Explicit foreign keys — even in warehouses that don't enforce them, declare them for lineage and docs.
- Timestamps: `created_at`, `updated_at` on mutable tables; state facts get event timestamps in UTC with timezone noted.

## Dimensional modeling rules of thumb

- Facts are **events or measurements** at a declared grain — state the grain in one sentence in the table's doc ("one row per order line per day"). Grain ambiguity is the #1 cause of wrong numbers.
- Dimensions are **context** (who, what, where). Prefer wide, denormalized dimensions over snowflaking.
- Slowly changing dimensions: default to **Type 2** (validity ranges `valid_from`/`valid_to`, `is_current` flag) when history matters; Type 1 (overwrite) when it doesn't. Decide per-column and write the decision down.

## Layered transformation structure (dbt-style)

```
staging/    stg_<source>__<entity>   1:1 with raw, rename/cast/clean only
intermediate/ int_<concept>          joins & business logic, not exposed
marts/      fct_<event>, dim_<entity>  what analysts and apps query
```
Each layer only selects from the layer below. Staging models are the *only* place that reads raw tables.

## Ethics & governance hooks

- Classify each column at design time: `public / internal / confidential / pii`. Put the classification in column descriptions (YAML in dbt, `COMMENT` in SQL). This powers the `privacy-engineering` and `governance-docs` skills later.
- Model consent and provenance as first-class data where relevant (e.g., `consent_status`, `source_system`, `ingested_at`), not tribal knowledge.
- Avoid modeling sensitive attributes (race, health, precise location) unless there's a documented purpose — flag to the user and consult `data-ethics-review`.

## Deliverables checklist

When designing a schema, always produce:
1. An entity-relationship summary (Mermaid `erDiagram` works well).
2. DDL or dbt model files with descriptions on every table and non-obvious column.
3. Grain statements for every fact table.
4. A short "decisions" note: why this shape, SCD choices, known trade-offs.

Suggest `governance-docs` afterward to generate the data dictionary from the schema.
