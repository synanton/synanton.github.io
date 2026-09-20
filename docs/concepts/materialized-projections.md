# Materialized Projections in AI-Native Knowledge Architecture

*For the complete, normative specification of this model, see the [Synanton Platform Architecture 1.0 document](https://github.com/synanton/platform/blob/main/docs/architecture/synanton-platform-architecture-1.0.md).*

## From a FileNET–Lucene consistency checker to a formal model for Enterprise Knowledge

------

## Abstract

Enterprise AI systems often treat knowledge as a collection of documents, chunks, embeddings, or graph nodes. This paper presents an alternative: **knowledge as a versioned set of materialized projections over heterogeneous source repositories, connected by provenance and constrained by security**. The model emerged from a concrete engineering problem—verifying consistency between a FileNET document repository and a Lucene inverted index—and evolved into a repository-agnostic framework for bidirectional consistency checking, derivation tracking, and incremental invalidation. We describe the historical path, the abstraction process, and the resulting architectural model for AI-native knowledge infrastructure.

------

## 1. Introduction

Modern enterprise AI architectures frequently reduce knowledge to a pipeline:

```text
Documents → Chunks → Embeddings → Vector Search → LLM
```

This pipeline treats derived artifacts as independent sources of truth. It ignores a fundamental property: **derived representations are not invertible**. A chunk cannot reconstruct its source document; an embedding cannot recover the original text; an aggregated fact cannot reveal which documents contributed to it.

The Synanton project explores a broader model:

> **Knowledge is derived state.**

Search indexes, embeddings, graph structures, annotations, and analytics are projections of authoritative source data. Changes to sources, models, policies, or ontologies are therefore lifecycle problems: identify affected derived artifacts, invalidate them, recalculate, and produce a new knowledge state.

This paper describes how that model was developed—not from top-down architectural theory, but from a bottom-up engineering journey that began with a simple question:

> *How do we verify that a Lucene index accurately reflects a FileNET document repository?*

------

## 2. The historical origin: FileNET vs Lucene consistency checker

### 2.1 The initial problem

The original task was straightforward: ensure that documents indexed in Lucene matched their counterparts in FileNET. A naive approach would compare documents directly:

```text
FileNET document  vs  Lucene document
```

However, these objects are not identical: a FileNET document contains binary data that must be transformed into text for index storage and this content is subsequently inaccessible directly from the index (using the Lucene configuration `indexed=true`, `stored=false`) while Lucene may also add or transform metadata. Lucene stores indexed fields, term vectors, and internal version numbers. A direct comparison is therefore meaningless

### 2.2 The first abstraction: bidirectional comparison

The solution was a **bidirectional checker** that operates on both repositories through a minimal interface:

```text
Repository<T>
    scanIds(pageToken) -> Page(nextToken,List<ID>)
    fetch(id)          -> Object<T>
```

The checker can then:

1. Scan IDs from both repositories.
2. Identify missing or orphaned objects.
3. For common IDs, fetch and compare.

This introduces a contract: **any two materialized repositories can be compared if they expose a paged ID stream and fetch-by-ID**.

### 2.3 The transformation problem

Objects still differ because they are produced by a transformation:

```text
    I=T(D)
```

where D is a source document and I is an index document. The checker must therefore compare:

But this requires knowing **which version of T** produced the index object and **which version of D** it was derived from.

### 2.4 Signatures as derivation markers

The breakthrough was to store a **signature** (hash) of the derivation state inside each projection object:

```text
    _id              = 123
    _source_version  = 42
    _projection_sig  = 9a73...
```

The signature is computed from:

- source ID
- source version
- transformation version
- selected fields
- transformation configuration

Now the checker asks a different question:

> **“Is this projection a valid derived representation of a specific source version under a known transformation contract?”**

This shifts consistency checking from object comparison to **derivation validation**.

------

## 3. From checker to repository-agnostic framework

The FileNET / Lucene checker was generalized into a framework for **any source repository ↔ projection repository** pair.

### 3.1 Repository contract

```text
Repository<T>
    scanIds(pageToken) -> Page(nextToken,List<ID>)
    fetch(id)          -> Object<T>
    signature(object)  -> Hash
```

### 3.2 Projection contract

```text
ProjectionContract
    sourceRepository
    projectionRepository
    transformationVersion
    ontologyVersion
    sourceVersion(object)
    projectionSignature(object)
    validate(source, projection)
```

### 3.3 Consistency states

The framework detects:

| State                        | Condition                                                   |
| ---------------------------- | ----------------------------------------------------------- |
| Missing projection           | Source exists, projection does not                          |
| Orphan projection            | Projection exists, source does not                          |
| Stale projection             | `source.version != projection.sourceVersion`                |
| Invalid projection           | `signature(source, transformation) != projection.signature` |
| Wrong transformation version | `projection.transformationVersion != expectedVersion`       |
| Security inconsistency       | `security(projection)` violates policy                      |

This is no longer a utility. It is a **lifecycle management mechanism** for derived knowledge.

------

## 4. Materialized projections: the core model

### 4.1 Knowledge as projections

Enterprise knowledge is not the raw documents, nor the embeddings, nor the graph. It is the **ability to operate over multiple projections in the space of an ontology**:

> **Knowledge=Ontology+Projections(RawData)+Provenance+SecurityKnowledge=Ontology+Projections(RawData)+Provenance+Security**

### 4.2 Many-to-many derivation

The relation between source objects and projection objects is not a function. It is a many-to-many derivation relation:

M⊆R×PM⊆R×P

Examples:

```text
    Document A ─────┐
    Document B ─────┼──→ Chunk X
    Document C ─────┘
```

or:

```text
Document A
    │
    ├── Chunk X
    ├── Chunk Y
    ├── Chunk Z
    └── Embedding E
```

### 4.3 Non-invertibility

If two documents produce the same projection:

```text
M(D1) = M(D2) but D1 ≠ D2 
```

then no inverse function exists. Information is lost during projection. This is true for inverted indexes, embeddings, deduplication, summarization, entity extraction, graph aggregation, and LLM-derived facts.

### 4.4 Provenance replaces inverse mapping

Instead of inverting the mapping, we store a **provenance graph**:

```text
Chunk X
  derived_from:
    - Document A:v17
    - Document B:v4

Embedding E1
  derived_from:
    - Chunk X:v2
    - embedding-model:v5
```

The provenance relation is:

```text
Provenance ⊆ P × R
```

This graph compensates for the non-invertibility of projections.

------

## 5. Signatures and derivation metadata

### 5.1 Component and composite signatures

For a projection depending on multiple sources:

```text
    FileNET ─────┐
    DB1 ─────────┼──► Business Object ───► Lucene
    DB2 ─────────┘
```

Store **component signatures** for each dependency and a **composite signature** for fast validation:

```text
projection_signature =
    H(
        transformation_version,
        filenet_signature,
        db1_signature,
        db2_signature
    )
```

### 5.2 Lineage record

```json
  {
    "projection": "lucene",
    "objectId": "business-123",
    "dependencies": [
        { "repository": "filenet", "id": "doc-991", "version": 42, "signature": "A" },
        { "repository": "db1", "id": "customer-123", "version": 781, "signature": "B" },
        { "repository": "db2", "id": "contract-555", "version": 154, "signature": "C" }
    ],
    "transformation": "business-object-v17",
    "signature": "X"
  }
```

### 5.3 Incremental invalidation

If only DB2 changes:

```text
DB2@154 → DB2@155
        ↓
sig(DB2) changes
        ↓
composite signature changes
        ↓
BusinessObject becomes stale
        ↓
Lucene projection becomes stale
```

This is an **incremental build system for knowledge projections**.

------

## 6. Ontology as semantic contract

The ontology defines not just vocabulary, but the **semantic contract** for interpretation and projection:

- which entities and relations exist
- which attributes are essential
- how source data is interpreted
- which projections are generated
- how queries are decomposed

Projection processors implement:

```text
Pi = Ti(S,O,C)
```

where S is source data, O is ontology, and C is configuration. Changing the ontology version invalidates projections.

------

## 7. Security across the lifecycle

### 7.1 Forward propagation

```text
Source security → Derivation → Projection security
```

### 7.2 Backward impact analysis

```text
Projection security changed
        ↓
which source objects affect this?
        ↓
which permissions need checking?
```

This uses the provenance graph to find ancestors.

### 7.3 Security lattices

Model security as a partially ordered set:

```text
S1 ⊑ S2
```

Derivation must satisfy:
```text
Security(P) ⪯ AllowedSecurity(Derivation(P))
```

This connects to information-flow control, taint tracking, and access-control propagation.

### 7.4 Aggregation and inference

An aggregated fact may reveal information about its sources even if it does not contain their text. Security of derived knowledge ≠ security of source documents.

------

## 8. The build system analogy

| Build System        | Knowledge Projection System |
| ------------------- | --------------------------- |
| source.java         | document                    |
| compiler            | extractor                   |
| class               | chunk                       |
| jar                 | embedding                   |
| incremental rebuild | incremental invalidation    |
| dependency graph    | provenance graph            |

Synanton can be viewed as an **incremental build system for enterprise knowledge**.

------

## 9. Retrieval evaluation as projection quality measurement

Retrieval evaluation becomes measurement of **how well a projection preserves retrieval-relevant properties** under cost, latency, and security constraints.

Metrics include:

- Recall@K
- NDCG@K
- MRR
- Precision
- p50/p95/p99 latency
- answer/evidence quality
- security leakage cases
- provenance completeness
- invalidation cost
- rebuild cost

Different projections optimize different metrics. A multi-objective evaluation framework is needed.

------

## 10. Conclusion: Synanton as a Knowledge Projection Engine

The model developed here is not a RAG platform. It is a system that:

```text
ingest → project → version → secure → index → query → derive → validate → invalidate → recalculate
```

The central architectural idea is:

> **Enterprise knowledge is a versioned, provenance-aware, security-constrained set of semantic projections over heterogeneous source repositories, queried through an ontology.**

The historical path—from a FileNET–Lucene consistency checker to a formal model—demonstrates that **provenance and derivation graphs compensate for the non-invertibility of projections**. That is the core insight.

Synanton is a **knowledge projection engine**. Consistency checking, signature validation, incremental invalidation, and security propagation are not auxiliary utilities—they are the mechanisms that make derived knowledge trustworthy over time.

------

## References

- Synanton Project: https://github.com/synanton
- Synanton Platform: https://github.com/synanton/platform
- Synanton Guides: https://synanton.github.io/

------