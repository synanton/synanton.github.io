# Knowledge Projections

## What it is

A knowledge projection is a derived, technology-specific representation of canonical semantic knowledge —
built for a particular workload, but never itself the authoritative source.

## Why it exists

No single storage technology is good at everything. Exact/lexical filtering, semantic similarity, and
relationship traversal have genuinely different access patterns and genuinely different optimal data
structures. Rather than force one technology to serve all three badly, Synanton projects the same canonical
chunk into three purpose-built stores.

## How it works

```text
Semantic Chunk
   │
┌────┼────┐
▼   ▼   ▼
Reverse Index   Vector Store   Graph DB
```

- [Reverse Index](../architecture/reverse-index.md) — lexical, exact, and filtered search.
- [Vector Store](../architecture/vector-store.md) — semantic similarity via embeddings.
- [Graph DB](../architecture/graph.md) — relationships and contextual traversal.

Each projection is derived, replaceable and lineage-aware: it can be rebuilt from canonical knowledge at
any time, and every entry in it traces back to the chunk it was projected from.

## Example

A search for "customers threatening to cancel over billing" combines a lexical match on "cancel" (reverse
index), semantic similarity to the concept of cancellation (vector store), and the customer/ticket
relationship that ties the matching chunks together (graph) — see [Search](search.md).

## Inputs

Classified, annotated [semantic chunks](chunks.md).

## Outputs

Index entries, vectors, and graph nodes/edges — each referencing canonical chunks, never replacing them.

## Transformations

Embedding (chunk → vector), indexing (chunk → searchable terms/fields), graph extraction (chunk →
entities/relationships) — each projection-specific, each independently derived from the same source chunk.

## Dependencies

Depends on [chunks](chunks.md) and their [annotations](annotations.md) being stable; classified chunks must
propagate their [security classification and representation](security-classification.md) into every
projection consistently.

## Change and recalculation

Changing an embedding model, a graph extraction rule, or an indexing scheme triggers selective or complete
recalculation of the affected projection only — canonical knowledge itself is untouched. See the
[change impact model](../architecture/recalculation.md#change-impact-model).

## Security

Every projection must preserve the representation contract: a Dual-representation chunk is projected as two
fields/vectors/edges (masked and original), never merged, never cross-contaminated. See
[Security-Aware Search](security-aware-search.md).

## Lineage

Every projected entry — index row, vector, graph edge — retains a reference back to its source chunk, so a
result is always traceable to canonical knowledge.

## Related concepts

[Chunks](chunks.md) · [Search](search.md) · [Security-Aware Search](security-aware-search.md) ·
[Reverse Index](../architecture/reverse-index.md) · [Vector Store](../architecture/vector-store.md) ·
[Graph](../architecture/graph.md)
