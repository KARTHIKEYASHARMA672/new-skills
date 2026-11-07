---
name: streaming-data
description: Build streaming and event-driven data systems — Kafka, CDC (Debezium), Flink/Spark streaming, delivery semantics, windowing, watermarks, late data, and schema evolution on topics. Use this skill whenever the user wants real-time or near-real-time data flow, change data capture from a database, Kafka topic/consumer design, stream processing jobs, or is debugging consumer lag, duplicates, or out-of-order events. For batch pipelines see `pipeline-builder`.
---

# Streaming Data

Streaming is batch with the hard parts always on: ordering, duplicates, late data, and state. Take them on only when the latency requirement is real.

## First decision: do you need streaming?

A 5–15 minute micro-batch covers most "real-time" requests at a fraction of the operational cost — ask what decision changes with sub-minute data. Genuine streaming cases: operational reactions (fraud, alerting), event-driven services, and CDC replication of mutable sources. "The dashboard should feel live" is a micro-batch requirement (see `pipeline-builder`).

## CDC (change data capture)

- Use log-based CDC (Debezium, native replication) for mutable sources with deletes — never poll-and-diff at volume (see `data-ingestion` load strategies).
- A CDC feed is snapshot + ordered change log: consumers must handle the initial snapshot, updates, **and delete tombstones** — dropping deletes silently forks reality from the source.
- Ordering is guaranteed per key (usually primary key), not globally; design consumers accordingly.

## Topics, keys, and consumers

- The **message key** decides partition, and partition is the ordering boundary — key by the entity whose events must stay ordered (user, order, device). Keys have the same hot-key risk as NoSQL partition keys (see `nosql-modeling`).
- Partition count caps consumer parallelism; changing it later reshuffles key→partition mapping — decide with headroom.
- **Consumer lag is your freshness SLA.** Monitor it per group with alert thresholds; lag creeping under steady input means you're under-provisioned, not unlucky.
- Poison messages go to a dead-letter topic with the raw payload and error — the streaming version of `data-ingestion` quarantine.

## Delivery semantics

Design for **at-least-once delivery with idempotent consumers** — the same discipline as batch: upsert by key, or deduplicate on event ID within a window. "Exactly-once" holds only inside specific framework boundaries (Kafka transactions, Flink checkpoints); the moment data leaves that boundary, idempotency is again your job. Producers retry too: include a stable event ID at the source.

## Time, windows, and late data

- **Event time, not processing time,** for anything analytical — processing time shifts with lag and backfills.
- Windows need a **watermark** (how long to wait for stragglers) and an explicit **late-data policy**: allowed lateness, then update-downstream or route to a late-events sink. Silently dropped late events are silent undercounts.
- State the trade-off: longer watermarks mean more complete windows and higher latency. Write the chosen lateness bound down where consumers can see it.

## Schemas and reprocessing

- Every topic gets a registered schema (Avro/Protobuf + schema registry) with a compatibility mode — a topic without a schema contract is an outage scheduled for the producer's next deploy (see `data-quality` on contracts).
- Retained topics are the streaming raw zone: size retention so you can **replay** after a consumer bug. Reprocessing is a planned path (reset offsets, idempotent sink), not an emergency invention.
- Stateful jobs checkpoint to durable storage; test recovery by killing the job, not by reading the docs.

## Ethics & retention on streams

- A topic is a log: personal data written to it stays for the full retention period and in every downstream materialization. Minimize at the producer — don't publish fields consumers don't need (see `data-ethics-review`).
- Deletion requests must reach streams too: keep topic retention short where PII flows, and for long-lived compacted topics use key-based deletion (compaction tombstones) or envelope encryption with per-user keys you can destroy (see `privacy-engineering`).
- Add stream sinks to the map of where personal data lands — replay makes copies easy to forget.
