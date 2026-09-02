# Analytics Guides

Task-oriented steps for the Analytics Plane defined in [Design 1.25](../../design/synanton-design-1.25.md):
emitting an analytics event, defining an analytical fact, creating an aggregate, defining a metric,
creating a report, querying analytics, configuring freshness and retention, inspecting lineage, testing
analytics security, and rebuilding historical analytics.

## At a glance

Every analytics capability sits downstream of the same boundary: an event is emitted only after
[classification and masking](../security/index.md) have already decided a chunk's representation. Nothing
in this guide can observe content a caller wasn't already authorized to see — see
[Analytics](../../concepts/analytics.md) for why that boundary is non-negotiable.

!!! note "Design status"
    Design 1.25 is approved architecture; per [Appendix F](../../design/synanton-design-1.25.md#appendix-f--implementation-readiness),
    production adoption of the Analytics Plane is conditional on a ClickHouse proof-of-concept, load
    testing, and security validation. This guide describes the contract the architecture defines, not a
    guaranteed shipped API in every deployment.

## Emit an analytics event

Events are emitted from the protected knowledge boundary, never from a pre-security path:

```text
Extraction → Semantic Content → Classification/Masking → Protected Knowledge → Analytics Event
```

An event such as `annotation_created` preserves event identity, tenant, timestamp, source, processing run,
provenance, security context, and schema version — enough to replay deterministically later.

## Define an analytical fact

A fact is a structured representation of an observed or derived property, registered in the
[Analytics Registry](../../design/synanton-design-1.25.md#71-analytics-registry):

```yaml
fact_type: AnnotationFact
fields:
  - fact_id
  - tenant_id
  - chunk_id
  - definition_id
  - definition_version
  - annotation_type
  - confidence
  - source_classification
  - representation_used
```

`source_classification` and `representation_used` are mandatory — a fact must never be classified less
restrictively merely because aggregation removed the original literal.

## Create an aggregate

An aggregate policy protects against side-channel disclosure through small populations, not just through
hiding individual records:

```yaml
aggregate_policy:
  classification: RESTRICTED
  minimum_group_size: 5
  suppression: true
  rounding: 2
  allowed_dimensions: [tenant, month]
  prohibited_dimensions: [customer_id, employee_id, exact_location]
```

A group smaller than `minimum_group_size` is suppressed entirely, not rounded down to a misleadingly
precise small number.

## Define a metric

A metric is a named, versioned analytical definition — never an ad hoc query:

```yaml
metric_id: processing_latency_p95
version: 1
source_facts: [ProcessingFact]
dimensions: [tenant, media_type]
aggregation: p95
freshness: near-real-time
security_policy: tenant-isolated
```

Published metric definitions are immutable; a changed definition is a new version, following the
[metric lifecycle](../../design/synanton-design-1.25.md#72-metric-lifecycle): Draft → Validated →
Published → Deprecated → Retired.

## Create a report

A report composes explicit metric versions — it does not query canonical knowledge directly:

```yaml
report_id: daily-platform-processing
version: 1
metrics:
  - documents_processed
  - documents_failed
  - annotations_created
  - processing_latency_p95
dimensions: [tenant, media_type, annotation_type]
refresh: daily
security:
  tenant_isolated: true
  classification_aware: true
```

## Query analytics

Every analytics query — API, MCP, or dashboard — passes through the same pipeline:

```text
Request → Authentication → Tenant Resolution → Authorization → Classification Filtering →
Representation Selection → Query Sanitization → Aggregate Protection → Metric/Report Query →
Result Sanitization → Response
```

No external interface may bypass this sequence, including MCP tools such as `get_metric` or
`query_report`.

## Configure freshness

Freshness is part of a metric's contract, not an accidental property of implementation:

```text
Real-time · Near-real-time · Hourly · Daily
```

Declare the freshness a report's audience actually needs — an executive report can be `daily`; an
operational latency metric usually needs `near-real-time`.

## Configure retention

Retention differs by analytical tier:

```text
Raw events      → short, configurable retention
Facts           → medium retention
Aggregates      → long retention
Business metrics → long-term retention
```

Retention is enforced automatically once configured, not something an operator must remember to run.

## Inspect lineage

A report should remain explainable down to the metric version and, where applicable, to the fact and
source lineage that produced it:

```text
Source → ECM Element → Chunk → Annotation → Processing Run → Knowledge Projection →
Analytical Event → Analytical Fact → Aggregate → Metric → Report
```

## Test analytics security

Analytics security testing extends `test:security` with an `analytics-security` tier validating tenant
isolation, classification propagation, masking boundaries, aggregate suppression, cross-tenant
restrictions, cache invalidation, report sanitization, MCP authorization, and platform-scope isolation —
using a representative negative-security corpus (`PUBLIC`, `RESTRICTED`, `MASKED-ONLY`, `SYSTEM-SCOPE`,
and related classes).

## Rebuild historical analytics

Because `analytics_events` is the durable, replayable source boundary, derived state can be rebuilt
without touching canonical knowledge:

```text
analytics_events → replay → new facts → new aggregates → new metrics
```

Replay must be deterministic for the same event stream, schema versions, and metric definitions — this is
what makes a storage migration (e.g. to a different analytical database) safe: it never requires changing
canonical knowledge or external API contracts.

## Go deeper

| If you want to know... | Read... |
|---|---|
| Why analytics is derived state, never authoritative | [Analytics](../../concepts/analytics.md) |
| The full event/fact/aggregate/metric/report architecture | [Analytics Plane](../../architecture/analytics-plane.md) |
| Security and tenant isolation for analytics | [Analytics Security](../../analytics/security.md) |
| The analytics API and event schemas | [Analytics API](../../reference/analytics-api.md) · [Analytics Event Schema](../../reference/analytics-event-schema.md) |
| The normative design | [Design 1.25](../../design/synanton-design-1.25.md) |
