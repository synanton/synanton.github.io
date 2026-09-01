# Provenance

## What it is

Provenance is the record that lets every derived piece of knowledge answer the question: **why does this
exist?**

## Why it exists

Derived knowledge — annotations, embeddings, projections, analytics — is only trustworthy if it remains
explainable. Without provenance, an annotation is an opaque assertion; with it, a reviewer, an auditor, or
another engineer can trace exactly which producer, version, and evidence produced it, and reconstruct why.

## How it works

The canonical lineage chain runs:

```text
Source
 → ECM Element
 → Chunk
 → Annotation
 → Processing Run
 → Knowledge Projection
 → Analytical Event
 → Analytical Fact
 → Aggregate
 → Metric
 → Report
```

For a single annotation, provenance means recording:

```text
producer
producer version
definition
definition version
evidence
confidence
source
target
processing run
dependencies
creation time
lifecycle
```

A [processing run](../architecture/annotation-plane.md#processing-runs) groups the execution context —
producer, version, configuration, input scope, timing, status, affected objects, errors, resource
consumption — for every substantial derived-knowledge operation.

## Example

An analyst asks why a ticket carries `billing-issue`. Provenance answers: `billing-issue` v2, produced by
`annotation-engine` v4.2 in processing run `run-2026-00182`, derived from `payment` v4 and
`duplicate-charge` v1, both computed from chunk `18291`, itself extracted from `invoice.pdf` — a complete
chain from report back to source.

## Inputs

Every stage of the pipeline — extraction, chunking, annotation, projection, analytics — that produces a
derived artifact.

## Outputs

A traceable chain attached to that artifact, queryable independently of the artifact's current value.

## Transformations

None — provenance is metadata *about* transformations, recorded alongside them, never itself transformed.

## Dependencies

Depends on every stage in the pipeline recording its own provenance fields honestly; a gap anywhere in the
chain breaks traceability for everything downstream of that gap.

## Change and recalculation

Provenance is what makes [recalculation](../architecture/recalculation.md) targeted rather than blind: knowing
exactly what an artifact depends on is what lets [Resolutor](../architecture/resolutor.md) compute a precise
impact set instead of "recalculate everything, to be safe."

## Security

Provenance records must not themselves leak restricted content — a processing run's metadata about *which*
chunk was classified is not the same as exposing that chunk's unmasked content.

## Lineage

This page describes the mechanism; see [Analytics Lineage](../analytics/lineage.md) for how the chain
extends all the way to reports.

## Related concepts

[Annotations](annotations.md) · [Annotation Dependencies](annotation-dependencies.md) ·
[Processing Runs](../architecture/annotation-plane.md) · [Analytics Lineage](../analytics/lineage.md)
