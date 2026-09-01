# Analytics

## What it is

Analytics is the observation of platform activity and knowledge state — producing metrics, statistics, and
reports — without ever becoming the authoritative source of the knowledge it observes.

## Why it exists

> **Analytics is derived state.**

Every platform accumulates operational questions — how much got processed, how confident are the
annotations, how is the security posture trending — that don't belong in the canonical knowledge model
itself. Analytics exists to answer them from a separate, purpose-built plane, so that the canonical model
stays clean and the analytical model can evolve, be rebuilt, and be queried at scale independently.

## How it works

```text
Knowledge / Platform Activity
      │
      ▼
Analytics Events
      │
      ▼
Analytical Facts
      │
      ▼
Aggregates
      │
      ▼
Metrics
      │
      ▼
Reports
```

Events are emitted only **after** the applicable [classification and masking](masking.md) decision — never
from a pre-security path — so analytics can never become a side channel for content a user couldn't
otherwise access. See [Analytics Plane](../architecture/analytics-plane.md) for the full architecture and
the [Analytics section](../analytics/overview.md) for the reader-facing tour.

## Example

Every annotation produced emits an `annotation_created` event; those events roll up into
`annotations_created` and `annotation_confidence_avg` metrics, which feed the
[Daily Platform Processing report](../analytics/reports.md).

## Inputs

Analytics Events, emitted from the protected knowledge boundary — after classification/masking, never
before.

## Outputs

[Analytical Facts](../architecture/analytical-facts.md), aggregates, [metrics](metrics.md), and
[reports](reporting.md) — every layer derived from the one below it.

## Transformations

Events → Facts → Aggregates → Metrics → Reports, each a defined, versioned transformation, never an ad hoc
query against canonical knowledge.

## Dependencies

Depends on the protected knowledge boundary — extraction, chunking, classification, masking, annotation —
having already run. Analytics never bypasses any of it.

## Change and recalculation

Analytics follows knowledge recalculation rather than driving it: when upstream knowledge changes,
[Resolutor](../architecture/resolutor.md) determines the affected analytics, and
[Equalix](../architecture/equalix.md) schedules their recalculation — see
[Analytics Recalculation](../analytics/recalculation.md).

## Security

Analytical facts inherit applicable classification from their sources and respect the same
Single/Dual/Masked-only representation rules as search — see [Analytics Security](../analytics/security.md).

## Lineage

Every metric and report should remain explainable down to the facts and knowledge it was computed from —
see [Analytics Lineage](../analytics/lineage.md).

## Related concepts

[Metrics](metrics.md) · [Reporting](reporting.md) · [Analytics Plane](../architecture/analytics-plane.md) ·
[Security Classification](security-classification.md)
