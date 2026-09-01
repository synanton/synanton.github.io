# Relationships

## What it is

A relationship is a typed connection between knowledge objects — most often between
[entities](annotation-types.md) extracted from content — that lets the platform answer "what is this
connected to?" rather than only "what does this contain?"

## Why it exists

Search alone answers "find content matching X." Many real questions are actually about context: "what else
touches this customer?", "what product does this ticket concern?" Relationships make that context a
first-class, queryable structure instead of something a human has to reconstruct by reading multiple
documents.

## How it works

```text
Customer
  │
  └── submitted → Ticket
           │
           ├── contains → PDF
           ├── contains → Audio
           └── concerns → Product
```

Relationships are derived from annotations — typically Entity annotations plus a relation type — and
projected into the [graph](../architecture/graph.md), where they can be traversed alongside, or instead of,
lexical and semantic search.

## Example

A support ticket's chunks yield entities `Customer("ACME Corp")`, `Product("Model X")`, and relationships
`submitted(Customer → Ticket)`, `concerns(Ticket → Product)`. A later query for "everything ACME Corp has
raised about Model X" traverses these edges rather than re-running full-text search across every document.

## Inputs

Entity and other annotations on [chunks](../concepts/chunks.md), plus the relation types they imply.

## Outputs

Graph nodes and edges in the [graph projection](../architecture/graph.md), each traceable back to the
annotation and chunk that produced it.

## Transformations

Entity resolution (deciding two mentions refer to the same real-world entity) and relation extraction happen
before a relationship becomes a graph edge.

## Dependencies

Depends on [Annotations](annotations.md) — specifically Entity-type annotations — having already been
produced.

## Change and recalculation

A change to entity extraction or relation-detection logic requires recalculating affected relationships and
the graph edges derived from them, per the [change impact model](../architecture/recalculation.md#change-impact-model).

## Security

Relationships derived from Dual or Masked-only chunks carry the same `classification` and `representation`
metadata as their source, and graph traversal must select representation the same way search does — see
[Security-Aware Search](security-aware-search.md).

## Lineage

Every relationship traces back to the annotation and chunk it was extracted from.

## Related concepts

[Annotations](annotations.md) · [Ontology](ontology.md) · [Graph](../architecture/graph.md) ·
[Knowledge Projections](knowledge-projections.md)
