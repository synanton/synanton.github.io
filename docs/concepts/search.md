# Search

## What it is

Search is the combination of lexical matching, semantic similarity, annotation filters, relationship
constraints, and security authorization into a single ranked result set.

## Why it exists

A useful enterprise search has to answer "find this exact term," "find things that mean this," and "find
things related to this" — often in the same query — while never returning something the searcher isn't
authorized to see. Treating any one of those as an afterthought (bolting security on as a post-filter, or
skipping relationship context) produces search that's either wrong or unsafe.

## How it works

```text
Query
│
├── lexical matching
├── semantic similarity
├── annotation filters
├── relationship constraints
└── security authorization
```

Lexical and semantic candidates are gathered from the [reverse index and vector store](knowledge-projections.md),
optionally expanded through the [graph](../architecture/graph.md) for relationship context, fused into a
single ranking, and — critically — filtered by security **before** ranking statistics are computed, not
after. See [Security-Aware Search](security-aware-search.md) and
[Search Architecture](../architecture/search-architecture.md) for the query-time mechanics.

## Example

"Customers threatening to cancel over billing" matches lexically on "cancel," semantically on the concept of
cancellation, and pulls in related tickets via the customer→ticket graph edge — all filtered to chunks the
searching user's class grants actually permit.

## Inputs

A query (natural language or structured), the searcher's identity and authorization context, and the three
[knowledge projections](knowledge-projections.md).

## Outputs

A ranked, authorized result set, with each hit traceable back to its source chunk.

## Transformations

Query compilation (natural language → structured query), ranking fusion (lexical + semantic + graph
signals → one score), and representation selection (masked vs. original) all happen before results are
returned.

## Dependencies

Depends on all three [knowledge projections](knowledge-projections.md) being current, and on
[security classification](security-classification.md) being enforced at compile time, not as a post-filter.

## Change and recalculation

A change to ranking logic, an embedding model, or a graph connector affects search results without
requiring any change to canonical knowledge. A change to [security policy](security-classification.md)
changes *who* sees a result without ever rewriting the result itself.

## Security

Security is not a filter applied to search — it's compiled into the query itself, at the same point ACL
clauses are injected, so an unauthorized caller's search never even computes statistics against content
they can't see. See [Security-Aware Search](security-aware-search.md).

## Lineage

Every hit is traceable back to its source chunk and, from there, to the full [provenance](provenance.md)
chain.

## Related concepts

[Knowledge Projections](knowledge-projections.md) · [Security-Aware Search](security-aware-search.md) ·
[Security Classification](security-classification.md) · [Relationships](relationships.md)
