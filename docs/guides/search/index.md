# Search Guides

Task-oriented steps for querying knowledge: text search, vector search, annotation filtering, security
filtering, hybrid search, and relationship-aware search.

## At a glance

Every search in Synanton compiles down to the same query path described in
[Security-Aware Search](../../concepts/security-aware-search.md): lexical matching, semantic similarity,
annotation filters, relationship constraints, and security authorization, evaluated together rather than
as separate stages bolted on afterward. This guide shows how to reach for each capability individually,
and how to combine them.

## Text search

Text search matches indexed terms in the [reverse index](../../architecture/reverse-index.md) — exact
identifiers, phrases, and lexical relevance ranking.

```text
query: "invoice 4471"
mode: lexical
```

Use text search when the reader knows an exact term — an invoice number, a ticket ID, a product SKU — and
wants precision over recall.

## Vector search

Vector search matches by meaning, using the [vector store](../../architecture/vector-store.md)'s semantic
similarity over chunk embeddings.

```text
query: "customers unhappy about billing"
mode: semantic
```

Use vector search when the reader doesn't know the exact wording but knows the concept — this is what
finds "cancel my subscription" when the underlying chunk actually says "terminate my account."

## Annotation filtering

Annotation filters narrow results to chunks carrying a specific [annotation](../../concepts/annotations.md),
combinable with either search mode:

```text
query: "billing"
mode: hybrid
filters:
  - annotation.topic = billing
  - annotation.tag = escalation
```

Filtering by annotation is exact-match, unlike vector search — it is the right tool when the reader wants
"only chunks the platform has already classified as X," not "chunks that resemble X."

## Security filtering

Security filtering is never something you add to a query — it is compiled in automatically, at the same
point resource-ACL clauses are injected, using the caller's authorization context. See
[Security-Aware Search](../../concepts/security-aware-search.md) for why this happens at compile time
rather than as a result filter, and [Security Guides](../security/index.md#search-masked-content) for how
to verify it.

## Hybrid search

Hybrid search runs lexical and semantic retrieval together and fuses the two ranked sets — typically via
Reciprocal Rank Fusion — so an exact-term hit and a semantically-similar hit are ranked on a comparable
scale rather than in two disconnected result lists.

```text
query: "invoice 4471 payment dispute"
mode: hybrid
```

This is the default mode for most enterprise search scenarios: real queries usually contain both an exact
identifier and a conceptual intent.

## Relationship-aware search

Relationship-aware search expands the candidate set through the [graph projection](../../architecture/graph.md),
using the top lexical/semantic hits as seed nodes and traversing declared relationships from there.

```text
query: "everything ACME Corp raised about Model X"
mode: hybrid
expand: graph        # traverse Customer -> Ticket -> Product relationships
```

Use this when the answer isn't in any single chunk's text but in how several chunks relate — see
[Relationships](../../concepts/relationships.md) for the underlying model.

## What changes search results

A ranking algorithm change, an embedding model change, or a graph connector change can all change which
results a query returns, without any change to canonical knowledge. A [security policy](../../concepts/security-classification.md)
change can change *who* sees a given result, without the result itself ever being rewritten.

## Go deeper

| If you want to know... | Read... |
|---|---|
| What happens end to end when you search | [Search overview](../overviews/search.md) |
| The query compilation and fusion model | [Search Architecture](../../architecture/search-architecture.md) |
| Why security is compiled in, not filtered after | [Security-Aware Search](../../concepts/security-aware-search.md) |
| The search API | [Search API](../../reference/search-api.md) |
