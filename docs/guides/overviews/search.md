# Search: How Hybrid Search Works

**Audience:** Developers, architects, technical evaluators, and product teams who need to understand how Synanton turns a question into an authorized search result.

**Level:** Conceptual to intermediate

**Prerequisites:** None. No query DSL, gRPC, or ranking mathematics is required.

## At a glance

Synanton uses **hybrid search** because enterprise questions are rarely purely textual.

A single question may require:

- exact term matching,
- semantic similarity,
- relationship traversal,
- security-aware filtering,
- and optional result reranking.

Synanton therefore treats search as a coordinated retrieval process rather than as a single search algorithm.

```text
Query
  │
  ├── Lexical retrieval
  │
  ├── Semantic retrieval
  │
  └── Relationship retrieval
          │
          ▼
    Result fusion
          │
          ▼
    Graph expansion
          │
          ▼
      Reranking
          │
          ▼
Authorized representation
          │
          ▼
       Results
```

The exact execution path depends on the query and the capabilities enabled for the deployment.

---

## What search is solving

Enterprise knowledge contains several kinds of information at the same time:

- exact identifiers and terminology,
- concepts expressed in different words,
- relationships between entities,
- structured annotations,
- security classifications,
- and content that may need different representations for different callers.

No single retrieval method handles all of these equally well.

For example:

> **Which suppliers have contracts expiring soon, and what are the termination requirements?**

This question contains several retrieval problems:

1. identify suppliers and their contracts;
2. find contracts approaching their expiration date;
3. locate relevant termination clauses;
4. find clauses that may describe termination without using the exact word;
5. respect the caller's permissions.

Hybrid search allows these operations to work together.

---

## Why Synanton uses multiple search strategies

Each retrieval strategy has a different strength.

| Strategy | Strong at | Limitation |
|---|---|---|
| **Lexical** | Exact terms, names, identifiers, domain terminology | Does not naturally understand paraphrases |
| **Semantic** | Meaning, similarity, paraphrase, synonyms | May underweight rare exact identifiers |
| **Graph** | Relationships, ownership, dependencies, associations | Does not replace textual relevance ranking |

The strategies are complementary rather than interchangeable.

A query such as:

> "rules for ending an agreement"

may need to find a passage containing:

> "either party may terminate this contract"

even though the two expressions have little lexical overlap.

At the same time, a query containing a contract number or supplier identifier benefits from exact lexical matching.

Relationship retrieval adds another dimension:

> Which supplier is associated with this contract?

That is a graph question rather than a textual relevance question.

---

# How hybrid search works

## 1. Query

A caller submits a search request.

The query may contain:

- natural language,
- exact terms,
- identifiers,
- filters,
- relationship constraints,
- or combinations of these.

The search system determines which retrieval capabilities are relevant.

---

## 2. Lexical retrieval

Lexical search matches indexed terms.

The current implementation uses **Synquest** as the lexical search kernel.

Lexical retrieval is particularly effective for:

- names,
- identifiers,
- product codes,
- contract numbers,
- exact terminology,
- uncommon domain terms.

It provides high precision when the caller knows the terminology used in the source content.

Lexical search does not, by itself, understand that:

> "terminate the agreement"

and

> "end the contract"

may express the same concept.

---

## 3. Semantic retrieval

Semantic search compares meaning rather than requiring the same words to appear.

Content is represented as vectors, and queries are represented in the same semantic space. Retrieval then identifies content whose meaning is sufficiently similar to the query.

For example:

> "rules for ending an agreement"

can retrieve:

> "either party may terminate this contract"

even though the vocabulary differs.

Semantic retrieval complements lexical retrieval rather than replacing it.

---

## 4. Relationship retrieval

Relationship retrieval operates on knowledge about entities and their relationships.

The current architecture uses **Relix** for graph-oriented retrieval.

Examples include:

```text
Supplier
   │
   ├── supplies → Product
   │
   ├── has → Contract
   │
   └── governed by → Policy
```

A relationship query can therefore answer questions such as:

- Which contracts belong to this supplier?
- Which policy governs this contract?
- Which customers are affected by this incident?
- Which obligations depend on this agreement?

Graph retrieval answers a different class of question from textual relevance.

---

# Result fusion

Lexical and semantic retrieval produce independently ranked candidate lists.

Their scores are not directly comparable: a lexical relevance score and a vector similarity score represent different quantities.

Synanton therefore combines their **rank positions** rather than treating the raw scores as equivalent.

The current design uses **Reciprocal Rank Fusion (RRF)** for this purpose.

Conceptually:

```text
Lexical results       Semantic results
      │                      │
      └──────────┬───────────┘
                 ▼
          Rank-based fusion
                 │
                 ▼
          Unified candidates
```

A candidate that appears highly in several retrieval paths receives stronger combined evidence than a candidate that appears highly in only one path.

---

# Relationship-aware expansion

Graph retrieval can be used after the initial textual candidate set has been established.

For example:

```text
Contract passage
      │
      ▼
Supplier
      │
      ▼
Related amendment
      │
      ▼
Updated penalty terms
```

This allows search to connect information that is distributed across different documents.

The graph therefore acts as a source of **relationship context**, not simply as another text-ranking engine.

---

# Reranking

Some queries benefit from a second ranking stage.

After candidate generation and fusion, an optional reranker can evaluate the most relevant candidates against the complete query.

```text
Initial retrieval
       ↓
Candidate set
       ↓
Fusion / expansion
       ↓
Reranker
       ↓
Final ranking
```

Reranking is more expensive than initial retrieval, so it is normally applied only to a bounded candidate set.

If reranking is unavailable, search can return the fused candidates without reranking. The response should identify the degraded execution state where the API exposes such information.

**Availability and ranking quality are separate concerns:** failure of an optional ranking stage should not automatically make search unavailable.

---

# Security is part of search

Search results must be evaluated in the context of the caller.

Authorization is therefore not simply a final presentation filter.

Conceptually:

```text
Query
  │
  ▼
Authorized candidate space
  │
  ├── lexical retrieval
  ├── semantic retrieval
  └── graph retrieval
          │
          ▼
       Fusion
          │
          ▼
       Reranking
          │
          ▼
Representation appropriate to caller
```

The exact implementation boundary is defined by the Security and Security-Aware Search architecture.

The important property is that unauthorized information must not become an ordinary search candidate merely to be removed later.

This also protects against indirect disclosure through:

- result counts,
- ranking behavior,
- snippets,
- autocomplete,
- highlighted terms,
- or other search metadata.

See **Security: Classification, Masking, and Authorization** for the complete security model.

---

# The same query can produce different representations

Two callers may submit the same query and receive different representations of the same underlying knowledge.

For example:

```text
Caller A
  → authorized for FINANCIAL
  → "Gross income: €180,000"

Caller B
  → not authorized for original FINANCIAL value
  → "Gross income: [REDACTED:FINANCIAL]"
```

This is different from simply hiding the entire result.

The knowledge remains useful while the representation respects the caller's authorization.

---

# Worked example

Suppose the caller asks:

> **What are our obligations if a vendor misses a delivery deadline?**

### Lexical retrieval

Finds passages containing terms such as:

- vendor,
- delivery,
- deadline,
- delay,
- shipment.

It may find:

> "Vendor shall notify buyer within 48 hours of an anticipated delay."

### Semantic retrieval

May find:

> "Should the supplier fail to fulfill the agreed shipment schedule, the following remedies apply."

The passage expresses the same concept without using the word "deadline".

### Relationship retrieval

The vendor relationship may lead to another document:

```text
Vendor
  │
  ├── Contract
  │
  └── Amendment
        │
        └── Updated penalty terms
```

The amendment may contain a later change to the obligations.

### Fusion and reranking

The textual candidates are combined, relationship context is incorporated where relevant, and the top candidates may be reranked against the complete question.

### Security

Only candidates and representations available to the caller enter the effective search result.

The resulting answer can therefore combine:

- exact contractual language,
- semantically related clauses,
- and related contractual facts,

without bypassing authorization.

---

# Search across languages

Enterprise content is often multilingual.

Lexical retrieval and semantic retrieval address multilingual content differently.

For languages where conventional whitespace tokenization is insufficient, the lexical layer can use language-appropriate indexing strategies rather than assuming that every language defines words in the same way.

Semantic retrieval provides another path because the embedding model can represent related meanings across supported languages.

The result is a search model in which multilingual content does not require the user to know exactly how the original text was phrased.

Language-specific implementation details belong in the Search Architecture documentation.

---

# Performance and resource control

Search must remain predictable under shared enterprise workloads.

The architecture therefore uses bounded work at several stages.

Examples include:

- bounded candidate sets,
- optional reranking over only the top candidates,
- resource-aware semantic retrieval,
- result caching where safe,
- and query budgets.

A cache must never cause one caller to receive another caller's authorized representation.

Similarly, resource limits should be observable rather than silently changing the meaning of a result.

Performance numbers should be interpreted as **targets or measurements under defined workload assumptions**, not as unconditional guarantees.

---

# Degraded operation

Search should distinguish between:

1. successful full-capability execution;
2. successful execution with reduced capability;
3. unavailable execution.

For example, if an optional semantic or reranking service is temporarily unavailable, the platform may continue with the remaining retrieval path.

When a degraded path materially affects search behavior, the execution result should expose the relevant status through the search contract.

A degraded result should not silently appear identical to a fully executed result when that difference matters operationally.

---

# What changes search results?

Search results can change when:

- source content changes;
- semantic chunks change;
- annotations change;
- relationships change;
- search indexes are rebuilt;
- embeddings are recalculated;
- security classifications change;
- authorization changes;
- search configuration changes;
- ranking models change.

Not all changes require the same recalculation.

For example:

```text
Authorization change
      ↓
Query-time visibility changes
      ↓
No content reprocessing required
```

Whereas:

```text
Classification rule change
      ↓
Existing content may be affected
      ↓
Reclassification / recalculation
      ↓
Updated search projections
```

The Recalculation architecture defines the dependency and execution model.

---

# What remains stable?

The following architectural boundaries should remain stable even when implementation technology changes:

- search operates over the canonical knowledge model and its projections;
- lexical, semantic, and graph retrieval remain distinct capabilities;
- retrieval results are combined through an explicit fusion strategy;
- optional expensive stages operate over bounded candidate sets;
- security determines what the caller is allowed to receive;
- derived search state can be rebuilt from authoritative state.

The implementation of an individual search engine or storage technology can evolve without changing these architectural contracts.

---

# Frequently asked questions

### Does semantic search replace lexical search?

No.

Semantic retrieval is strong at meaning and paraphrase. Lexical retrieval remains important for exact identifiers, names, codes, and domain terminology.

### Does graph search replace ordinary search?

No.

Graph search answers relationship questions. It complements textual retrieval.

### Why not compare the lexical and vector scores directly?

Their scores have different meanings and scales. Rank-based fusion avoids treating incomparable scores as if they were the same measurement.

### Does a broader role always receive more search results?

Not necessarily.

A broader role may receive the same hit with a less restricted representation. Additional documents appear only when the caller's effective resource and classification permissions allow them.

### What happens if reranking is unavailable?

The search can return the fused candidate ranking without the optional reranking stage, with degraded execution information exposed according to the search contract.

### Can search results be cached?

Yes, where caching is compatible with authorization and result freshness requirements. Authorization-sensitive results must not cross permission boundaries.

---

# Go deeper

| Question | Read |
|---|---|
| What is search conceptually? | **Concepts → Search** |
| How are lexical, vector, and graph projections implemented? | **Architecture → Search Architecture** |
| How does security-aware search work? | **Architecture → Security-Aware Search** |
| How are chunks and annotations represented? | **Concepts → Chunks / Annotations** |
| How are search dependencies recalculated? | **Architecture → Recalculation** |
| What is the exact API contract? | **Reference → Search API** |
| Why was the current architecture chosen? | **Design 1.22 / Design 1.23** |

---

## Summary

Synanton search is **hybrid because enterprise knowledge is heterogeneous**.

Lexical retrieval handles exact language.

Semantic retrieval handles meaning.

Graph retrieval handles relationships.

Fusion combines evidence from those retrieval paths.

Reranking can improve the ordering of a bounded candidate set.

Security determines which knowledge and representation are available to the caller.

Recalculation keeps derived search state consistent when authoritative knowledge changes.

The result is not simply a faster keyword search. It is a search layer over the **structured, connected, security-aware knowledge model**.

## Go Deeper

| Question | Document |
|---|---|
| What's the exact step-by-step query execution pipeline (compile, plan, execute, fuse, rerank)? | `docs/architecture/synanton-design-1.22.md` §7 (Query Flow) |
| How does GraphRAG combine vector retrieval with graph traversal? | `docs/architecture/synanton-design-1.22.md` §8 |
| How is access control compiled into the query instead of filtered after? | `docs/architecture/synanton-design-1.23.md` §3.3; [Security 101](security.md) |
| What does the reverse index / vector store / graph actually store, mechanically? | `docs/book/Ingestion and security processing guide.md`, Part IV |
| What are the search latency SLOs? | `docs/architecture/synanton-design-1.22.md` §7 ("SLOs") |
