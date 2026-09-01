# Contracts

## What it is

A contract is the stable interface between two stages of the platform — what one stage promises to produce
and the next stage is guaranteed to be able to consume — independent of which technology implements either
side.

## Why it exists

> **Polyglot by implementation, contract-driven by architecture.**

Synanton's modules are deliberately implemented in whatever language and technology best fits their
workload — a Rust search kernel, a Java ingestion pipeline, a Node.js protocol adapter. That's only safe if
the boundaries between them are stable enough that any side can be reimplemented, or swapped for a
different technology, without breaking the other. Contracts are what make that possible.

## How it works

Key contracts in the platform:

```text
Extractor        → Structured Content
Chunker          → Chunk
Annotation Engine → Annotation
Annotation       → Search
Annotation       → Graph
Knowledge        → Analytics Events
Analytics Events → Facts
Facts            → Metrics
Metrics          → Reports
Search           → Application
```

A contract specifies the shape and guarantees of its output — never the implementation that produces it.
The [extraction contract](../architecture/extraction-plane.md), for example, is versioned
(`synanton.extraction.v1`) and mirrored byte-for-byte between the platform and whatever implements it
today, so either side can evolve independently as long as the mirror holds.

## Example

The platform's [Content Extractor integration](../integrations/content-extractor.md) implements the
extraction contract in a separate service; the platform's [GPU Runtime](../integrations/graph-databases.md)-adjacent
execution plane implements a GPU execution contract the same way. Neither implementation detail is visible
to anything consuming their contract's output.

## Inputs

An explicit specification: message/schema shape, required fields, versioning rule, and failure semantics.

## Outputs

A guarantee that any conforming implementation can be substituted without the consuming stage changing.

## Transformations

None — a contract is a specification, not a transformation itself.

## Dependencies

Every [Knowledge Projection](knowledge-projections.md), [Annotation](annotations.md) producer, and
[Analytics](analytics.md) stage in the platform is defined against a contract rather than against a
specific implementation.

## Change and recalculation

A contract version change is a breaking change by definition and requires an explicit migration path;
implementation changes behind an unchanged contract require no downstream changes at all.

## Security

Security-relevant contracts (classification, representation) are normative — see
[Design 1.23](../design/synanton-design-1.23.md) — and every implementation must honor them exactly, not
approximately.

## Lineage

Contract versions are part of an artifact's provenance: knowing which contract version produced a chunk or
annotation is part of explaining it.

## Related concepts

[Polyglot Architecture](../architecture/polyglot-architecture.md) · [Extraction Plane](../architecture/extraction-plane.md) ·
[Integrations](../integrations/content-extractor.md)
