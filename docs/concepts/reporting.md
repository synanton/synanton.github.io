# Reporting

## What it is

A report is a presentation-level composition of [metrics](metrics.md) — the layer a human or a downstream
system actually reads.

## Why it exists

A metric answers one question; a report answers a role's whole set of questions at once, at a defined
refresh cadence, with defined security scope. Reports exist so that "what does the platform team look at
every morning" is a governed artifact too, not an ad hoc dashboard someone wired together against raw
facts.

## How it works

```text
Analytical Facts
   ↓
Aggregates
   ↓
Metrics
   ↓
Report
```

Reports should not query canonical transactional knowledge directly unless explicitly required — they
compose already-governed metrics. The platform's reference example:

```yaml
Report: Daily Platform Processing
Version: 1

Metrics:
  - documents_processed
  - documents_failed
  - annotations_created
  - processing_latency_p95

Dimensions:
  - tenant
  - media_type
  - annotation_type

Refresh: Daily

Security: Tenant-isolated, classification-aware
```

## Example

A report titled "Top Search Terms" must never expose a restricted search term merely because it's
aggregated — report generation passes through classification policy, tenant scope, aggregate protection,
and authorization before rendering, exactly like any other knowledge access. See
[Report-Level Sanitization](../analytics/security.md#report-level-sanitization).

## Inputs

One or more governed [Metrics](metrics.md), a dimension set, a refresh cadence, and an explicit security
declaration.

## Outputs

A rendered report — dashboard, exported document, or API response — safe to hand to the role it was
designed for.

## Transformations

Composition and presentation only; a report does not define new aggregation logic, it assembles existing
metrics.

## Dependencies

Depends on every [Metric](metrics.md) it composes, and on the [Analytics Security Registry](../analytics/security.md)
having validated its declared policy.

## Change and recalculation

Changing a report definition (adding a metric, changing dimensions) doesn't require recalculating the
underlying metrics — only re-rendering. Changing an underlying metric definition does, per
[Analytics Recalculation](../analytics/recalculation.md).

## Security

Reports pass through the full authorization model: metric → classification policy → tenant scope →
aggregate protection → authorization → report. No report bypasses this by virtue of being "just an
aggregate."

## Lineage

A report should remain explainable down to the metric version — and, where applicable, to the fact and
source lineage — that produced each number in it. See [Analytics Lineage](../analytics/lineage.md).

## Related concepts

[Metrics](metrics.md) · [Analytics](analytics.md) · [Analytics Security](../analytics/security.md) ·
[Dashboards](../analytics/dashboards.md)
