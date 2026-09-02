# Operations Guides

Task-oriented steps for running Synanton: deployment, private cloud and on-premises, storage, scaling,
monitoring, workload isolation, recalculation operations, and failure recovery/backup.

## At a glance

Operating Synanton means operating several independently scalable planes — ingestion, search, graph,
recalculation, and analytics — each with its own workload characteristics. This guide covers the
operator-facing tasks; see [Operations](../../operations/deployment.md) for the architectural detail each
task assumes.

## Deploy

1. Choose a deployment model — SaaS, private cloud, on-premises, or hybrid — based on data-residency and
   security requirements. See [Deployment](../../operations/deployment.md) for the trade-offs.
2. For a hybrid deployment, route sensitive processing to the private environment and non-sensitive
   processing to external services explicitly — never implicitly by omission.
3. Confirm analytics deployment follows the same data-residency and tenant-isolation requirements as the
   knowledge platform it observes; analytics is not exempt from the deployment model's constraints.

## Operate on-premises / private cloud

1. Confirm every LLM-backed [annotation producer](../annotations/index.md#use-llms) is either a private
   deployment or explicitly approved for external routing.
2. Confirm the [Extraction Plane](../../architecture/extraction-plane.md) and GPU execution boundary are
   deployed inside the customer network where required.
3. See [Private / Regulated AI](../../use-cases/regulated-private-ai.md) for the enterprise scenario this
   supports end to end.

## Operate storage

1. Monitor the content store (`synvault`) and its tiering behavior — hot, warm, cold — separately from
   the analytics store; they have different retention and access patterns.
2. For analytics storage specifically, monitor partitioning, compression, and storage growth against the
   [retention policy](../analytics/index.md#configure-retention) per fact tier.
3. Confirm backup and restore procedures are tested for both the canonical content store and the
   analytics store, independently — a canonical-store restore should never assume analytics state is
   consistent with it, since analytics is [derived, replayable state](../../architecture/analytics-storage.md).

## Scale

1. Scale ingestion, search, graph, and analytics workloads independently — each has a different
   bottleneck (parsing/embedding throughput, query concurrency, traversal cost, event ingestion rate).
2. Use [Equalix](../../architecture/equalix.md)'s workload classes (incremental ingestion, interactive
   processing, user-triggered recalculation, background recalculation, analytics aggregation) to decide
   where added capacity actually helps rather than scaling uniformly.
3. See [Scaling](../../operations/scaling.md) and [Architecture: Scaling](../../architecture/scaling.md)
   for workload-specific guidance.

## Monitor

Baseline operational signals to alert on:

```text
Consumer lag > threshold
Event loss rate > threshold
Query latency p95 > SLA
Storage utilization > 80%
Aggregate freshness > 2x expected
Security policy failures
```

Distinguish platform health, analytics health, and security health as separate signals — a security
policy failure should page differently than a slow dashboard query.

## Isolate workloads

Interactive workloads (search, ingestion) must never be starved by background maintenance (large
historical recalculation, analytics rebuilds). Enforce this through Equalix's priority, concurrency, and
resource controls rather than through manual scheduling — see
[Recalculation Guides → Prioritize workloads](../recalculation/index.md#prioritize-workloads).

## Operate recalculation

1. Monitor recalculation job duration, affected-object counts, and failure rate against the impact set
   [Resolutor](../../architecture/resolutor.md) computed at plan time.
2. Investigate any recalculation whose affected-object count exceeds its computed impact set — that's a
   sign the dependency graph is missing an edge, not that the recalculation is simply "large."
3. See [Operations: Recalculation](../../operations/recalculation.md).

## Recover from failure

1. For a transient failure, confirm retry with exponential backoff resumes correctly — no duplicate
   chunks, no double-processed annotations, thanks to idempotent identity throughout the pipeline.
2. For a permanent processing error, confirm it lands in a dead-letter queue with an alert, rather than
   silently dropping the affected content.
3. For a security policy error, confirm the platform fails closed with no automatic retry — a security
   failure should never resolve itself silently.

## Go deeper

| If you want to know... | Read... |
|---|---|
| Where to even start when something looks wrong | [Troubleshooting overview](../overviews/troubleshooting.md) |
| Deployment models in detail | [Deployment](../../operations/deployment.md) |
| Analytics-specific operations (partitioning, backups, rebuilds) | [Analytics Operations](../../operations/analytics.md) |
| Monitoring and alerting reference | [Monitoring](../../operations/monitoring.md) |
