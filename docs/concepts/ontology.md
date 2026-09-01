# Ontology

## What it is

An ontology is the governed set of entity types, relation types, and taxonomy categories that annotation
and graph extraction are allowed to use — the vocabulary the platform's interpretation of content is
written in.

## Why it exists

Without a governed vocabulary, one annotation producer might tag an entity `Customer` while another tags
the same concept `Client` or `Account` — fragmenting the graph and search filters into incompatible
dialects. An ontology exists so that "what counts as a Customer" is decided once, versioned, and shared
across every producer that emits entities or relationships.

## How it works

The ontology defines entity types (`Customer`, `Product`, `Ticket`), relation types (`submitted`,
`concerns`, `contains`), and taxonomy categories used by [Classification](annotation-types.md) annotations.
It is managed as its own governed artifact — additions are reviewed, and duplicate or conflicting concepts
are merged rather than left to silently diverge (see `syntology` in the platform's module map).

## Example

Before `Product` can be used as an entity type by any annotation producer, it's registered in the ontology
with its expected attributes. Two extraction pipelines that both detect products then agree on the same
type, letting the graph merge references to the same product instead of creating duplicate nodes.

## Inputs

Proposed entity types, relation types, and taxonomy nodes from annotation producers or human curators.

## Outputs

A versioned, governed vocabulary consumed by [Annotations](annotations.md), [Relationships](relationships.md),
and the [graph projection](../architecture/graph.md).

## Transformations

Ontology curation includes duplicate detection and merge review — automated suggestions are surfaced for
human adjudication rather than merged silently.

## Dependencies

[Annotations](annotations.md) and [Relationships](relationships.md) depend on the ontology for valid
entity/relation types; the ontology itself depends on no other concept.

## Change and recalculation

Merging two previously-distinct entity types requires recalculating every annotation and graph edge that
used either type, so they resolve to the single merged type.

## Security

The ontology itself is not classified content, but taxonomy categories it defines may be used as reporting
dimensions subject to [aggregate protection](../analytics/aggregates.md).

## Lineage

Ontology changes (new types, merges) are versioned so that historical annotations can still be interpreted
against the vocabulary that was current when they were produced.

## Related concepts

[Annotations](annotations.md) · [Relationships](relationships.md) · [Taxonomy vs Dependency](taxonomy.md)
