# Metrics

## What it is

A metric is a named, versioned analytical definition — not an ad hoc query, but a governed artifact with an
identity, an owner, and a contract.

## Why it exists

"How many documents were processed yesterday" needs the same answer no matter who asks it or which
dashboard renders it. Treating a metric as a first-class, versioned definition — rather than a query someone
happened to write — is what makes that consistency possible, and what makes a metric's freshness, security
policy, and lineage things that can be relied on rather than re-discovered each time.

## How it works

A metric definition includes:

```text
identity
version
definition
dimensions
aggregation
freshness
security policy
lineage
```

Example metrics: `documents_processed`, `documents_failed`, `annotations_created`,
`annotation_confidence_avg`, `processing_latency_p95`, `search_latency_p95`, `search_volume`,
`classification_distribution`, `masking_outcomes`, `recalculation_duration`, `LLM_cost`.

A metric cannot declare itself `PUBLIC` if the underlying facts it aggregates would violate the applicable
sharing policy — the [Analytics Security Registry](../analytics/security.md#analytics-security-registry)
validates that at registration time.

## Example

`processing_latency_p95`, dimensioned by `tenant` and `media_type`, freshness `near-real-time`, security
`tenant-isolated` — computed from [Processing Facts](../analytics/facts.md), aggregated per tenant per
hour, and surfaced in the [Daily Platform Processing report](reporting.md).

## Inputs

[Analytical Facts](../architecture/analytical-facts.md) and [Aggregates](../analytics/aggregates.md).

## Outputs

A queryable, versioned value (or time series) consumed directly or composed into [Reports](reporting.md).

## Transformations

Aggregation logic defined once per metric — sum, average, percentile, distinct count — applied consistently
regardless of which report or API surface reads it.

## Dependencies

Depends on the [Aggregates](../analytics/aggregates.md) or facts it's defined over, and on the
[Analytics Security Registry](../analytics/security.md) having validated its declared security policy.

## Change and recalculation

Changing a metric's definition (its aggregation, its dimensions) requires recalculating affected aggregates —
see [Analytics Recalculation](../analytics/recalculation.md). Old and new definition versions can coexist for
comparison.

## Security

A metric's security declaration must not exceed what its underlying facts permit; aggregate protection
(minimum group size, suppression, rounding) applies before a metric value is ever returned. See
[Analytics Security](../analytics/security.md).

## Lineage

Every metric is explainable down to the facts, aggregates, and — where applicable — the source knowledge it
was computed from. See [Analytics Lineage](../analytics/lineage.md).

## Related concepts

[Analytics](analytics.md) · [Reporting](reporting.md) · [Aggregates](../analytics/aggregates.md) ·
[Analytics Security](../analytics/security.md)
