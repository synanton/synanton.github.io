\# Synanton Documentation Site Plan

**Status:** Proposal
  **Version:** 1.25
  **Documentation stack:** MkDocs + Material
  **Languages:** English (`en`) and Russian (`ru`)
  **Primary audience:** Business and mid-technical readers, enterprise  architects, technical decision makers, platform engineers, developers,  SRE/support teams, data/analytics engineers and system integrators

\---

\# 1. Purpose

The Synanton documentation site explains **why the platform exists, how it works, and how its architectural primitives fit  together**.

The documentation should not begin with source code, APIs, databases or implementation details.

It should progressively answer:

\```text
  What is Synanton?
      ↓
  What problem does it solve?
      ↓
  What happens to enterprise content?
      ↓
  How does content become knowledge?
      ↓
  How is knowledge annotated, connected and secured?
      ↓
  How is knowledge projected and searched?
      ↓
  How are changes propagated and recalculated?
      ↓
  How is platform activity and knowledge state measured?
      ↓
  How can Synanton be integrated and operated?
  \```

The documentation is therefore an **architecture and knowledge guide first**, and a developer reference second.

\---

\# 2. Documentation Positioning

The central positioning should be:

\> **Synanton transforms heterogeneous enterprise content into structured, annotated, connected and measurable knowledge.**

Synanton is not primarily:

\* a chatbot
  \* a vector database
  \* a document parser
  \* a speech analytics system
  \* a search engine
  \* an LLM wrapper
  \* a reporting database

Those are either components, integrations or applications enabled by the platform.

The central architectural promise is:

\> **Extract once. Annotate flexibly. Connect knowledge. Search precisely. Recalculate efficiently. Measure continuously.**

\---

\# 3. Core Documentation Story

The documentation should reinforce one architectural progression:

\```text
            SOURCE CONTENT
               │
      ┌─────────────────┼─────────────────┐
      ▼         ▼         ▼
    Documents      Audio       Images
      │         │         │
      └─────────────────┼─────────────────┘
               ▼
          CONTENT EXTRACTION
               │
               ▼
          SEMANTIC CONTENT MODEL
               │
               ▼
           SEMANTIC CHUNKS
               │
               ▼
            ANNOTATION
               │
         ┌──────────┼──────────┐
         ▼     ▼     ▼
        Tags  Classifications Entities
         │     │     │
         └──────────┼──────────┘
               ▼
           DERIVED KNOWLEDGE
               │
         ┌──────────┼──────────┐
         ▼     ▼     ▼
      Reverse Index Vector Store Graph DB
         │     │     │
         └──────────┼──────────┘
               ▼
              SEARCH
               │
         ┌──────────┴──────────┐
         ▼           ▼
      Query semantics    Security policy
                     │
                 Group → Classification
                     │
                     ▼
                  Authorization
                     │
                     ▼
                   Results
  \```

Analytics extends the lifecycle:

\```text
  Content / Knowledge / Platform Activity
           │
           ▼
        Analytics Plane
           │
      ┌──────────┼──────────┐
      ▼     ▼     ▼
    Events    Facts   Statistics
      │     │     │
      └──────────┼──────────┘
           ▼
          Metrics
           │
           ▼
          Reports
  \```

When knowledge definitions change:

\```text
  Rule / Model / Dictionary changes
         │
         ▼
        Resolutor
         │
         ▼
     Dependency analysis
         │
         ▼
      Recalculation plan
         │
         ▼
        Equalix
         │
         ▼
     Controlled execution
         │
         ▼
      Updated knowledge
         │
         ▼
     Updated analytics
  \```

The documentation should make clear that:

\> **Analytics observes derived platform state; it does not become the authoritative state of the knowledge platform.**

\---

\# 4. Architectural Principles

The documentation should repeatedly explain these principles.

\## 4.1 Extraction and interpretation are separate

\> **Extraction describes what content contains. Annotation describes what Synanton understands about it.**

Changing a classification rule should not require re-extracting the source document.

\---

\## 4.2 Semantic chunks are knowledge units

A chunk is not merely an arbitrary piece of text.

A semantic chunk is an independently addressable unit that can participate in:

\* annotation
  \* security classification
  \* indexing
  \* vectorization
  \* graph relationships
  \* search
  \* recalculation
  \* analytics

\---

\## 4.3 Annotations are first-class knowledge

Annotations include:

\```text
  Tag
  Classification
  Entity
  Attribute
  Signal
  \```

They provide structured meaning on top of extracted content.

\---

\## 4.4 Classification and authorization are different

Content may have:

\```text
  security = confidential
  \```

while access depends on:

\```text
  user/group
    ↓
  security policy
    ↓
  allowed classifications
  \```

The classification belongs to the content.

The authorization mapping belongs to policy.

\---

\## 4.5 Classify once, authorize dynamically

A central security principle:

\> **Security classifications stored with content do not need to be rewritten when user-group mappings change.**

Therefore:

\```text
  Group mapping changes
      ↓
  No content rewrite
  No chunk rewrite
  No annotation recalculation
  No index rebuild
  No graph rebuild
      ↓
  New authorization decision at search time
  \```

\---

\## 4.6 Masking is separate from classification

Classification determines the sensitivity/security level.

Masking determines whether sensitive values are represented in masked form.

\```text
  Classification
     ↓
  How sensitive is this content?

Masking
     ↓
  How is sensitive content represented?

Authorization
     ↓
  Who may access which representation?
  \```

\---

\## 4.7 Knowledge is projected into multiple stores

The same semantic knowledge can be projected into:

\```text
  Reverse Index → lexical/exact/filter search
  Vector Store → semantic similarity
  Graph DB   → relationships/context
  \```

The architecture is intentionally polyglot.

\---

\## 4.8 Contracts are more important than implementation language

\> **Polyglot by implementation, contract-driven by architecture.**

Stable contracts allow implementations to evolve independently.

\---

\## 4.9 Derived knowledge is recalculable

Annotations, embeddings, search projections and analytics are derived state.

The platform must be able to determine what becomes stale when:

\* source content changes
  \* extraction changes
  \* chunking changes
  \* annotation rules change
  \* models change
  \* dictionaries change
  \* dependencies change
  \* security classification changes
  \* analytics definitions change

\---

\## 4.10 Analytics is derived state

This should become a first-class architectural principle.

\> **Analytics is derived state.**

Analytics may observe:

\* content state
  \* chunk state
  \* annotation state
  \* security state
  \* search activity
  \* processing activity
  \* recalculation activity
  \* platform operations

But analytics does not become authoritative over the underlying knowledge.

\```text
  Canonical Knowledge
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
  \```

The canonical knowledge model remains authoritative.

\---

\## 4.11 Analytics preserves lineage

Analytical results should remain traceable to their origins.

Conceptually:

\```text
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
  \```

\---

\## 4.12 Analytics must respect security

Analytics does not bypass the security architecture.

Analytical facts inherit applicable security classification and access scope according to defined policy.

Analytics must not become a side channel for information that a user could not access through the underlying knowledge system.

\---

\# 5. Documentation Layers

The site should have seven logical layers:

\```text

1. Introduction

​      ↓

2. Concepts

​      ↓

3. Use Cases

​      ↓

4. Architecture

​      ↓

5. Analytics

​      ↓

6. Guides / Integrations

​      ↓

7. Reference / Design

  \```

Readers should be able to stop at any layer.

A business reader may need:

\```text
  Introduction
  → Concepts
  → Use Cases
  → Analytics overview
  \```

An architect may continue into:

\```text
  Architecture
  → Security
  → Recalculation
  → Analytics
  → Contracts
  \```

A developer can continue into:

\```text
  Guides
  → Integrations
  → APIs
  → Reference
  \```

\---

\# 6. Recommended Repository Structure

\```text
  docs-site/
  │
  ├── index.md
  │
  ├── getting-started/
  │  ├── overview.md
  │  ├── quickstart.md
  │  └── architecture-overview.md
  │
  ├── concepts/
  │  ├── synanton.md
  │  ├── content-model.md
  │  ├── extraction.md
  │  ├── semantic-elements.md
  │  ├── semantic-chunking.md
  │  ├── chunks.md
  │  ├── chunk-security.md
  │  ├── annotations.md
  │  ├── annotation-types.md
  │  ├── annotation-dependencies.md
  │  ├── taxonomy.md
  │  ├── provenance.md
  │  ├── knowledge-projections.md
  │  ├── search.md
  │  ├── security-classification.md
  │  ├── masking.md
  │  ├── security-aware-search.md
  │  ├── relationships.md
  │  ├── ontology.md
  │  ├── analytics.md
  │  ├── metrics.md
  │  ├── reporting.md
  │  └── contracts.md
  │
  ├── use-cases/
  │  ├── overview.md
  │  ├── multimodal-support.md
  │  ├── enterprise-document-search.md
  │  ├── conversation-intelligence.md
  │  ├── customer-support.md
  │  ├── sre-production-support.md
  │  ├── multimodal-knowledge.md
  │  ├── regulated-private-ai.md
  │  ├── analytics-and-reporting.md
  │  └── custom-enterprise-applications.md
  │
  ├── architecture/
  │  ├── overview.md
  │  ├── ingestion.md
  │  ├── extraction-plane.md
  │  ├── content-model.md
  │  ├── semantic-chunking.md
  │  ├── annotation-plane.md
  │  ├── annotation-dependencies.md
  │  ├── knowledge-projections.md
  │  ├── reverse-index.md
  │  ├── vector-store.md
  │  ├── graph.md
  │  ├── search-architecture.md
  │  ├── security.md
  │  ├── security-aware-search.md
  │  ├── masking.md
  │  ├── recalculation.md
  │  ├── resolutor.md
  │  ├── equalix.md
  │  ├── analytics-plane.md
  │  ├── analytics-events.md
  │  ├── analytical-facts.md
  │  ├── metrics.md
  │  ├── reporting.md
  │  ├── analytics-security.md
  │  ├── analytics-lineage.md
  │  ├── analytics-recalculation.md
  │  ├── analytics-storage.md
  │  ├── polyglot-architecture.md
  │  ├── contracts.md
  │  ├── mcp.md
  │  └── scaling.md
  │
  ├── analytics/
  │  ├── overview.md
  │  ├── concepts.md
  │  ├── events.md
  │  ├── facts.md
  │  ├── aggregates.md
  │  ├── metrics.md
  │  ├── reports.md
  │  ├── dashboards.md
  │  ├── freshness.md
  │  ├── retention.md
  │  ├── security.md
  │  ├── lineage.md
  │  ├── recalculation.md
  │  ├── storage.md
  │  └── operations.md
  │
  ├── guides/
  │  ├── ingestion/
  │  ├── extraction/
  │  ├── chunking/
  │  ├── annotations/
  │  ├── security/
  │  ├── search/
  │  ├── recalculation/
  │  ├── analytics/
  │  ├── integrations/
  │  └── operations/
  │
  ├── integrations/
  │  ├── content-extractor.md
  │  ├── mcp.md
  │  ├── llm-providers.md
  │  ├── object-storage.md
  │  ├── search-engines.md
  │  ├── vector-databases.md
  │  ├── graph-databases.md
  │  └── analytics-storage.md
  │
  ├── operations/
  │  ├── deployment.md
  │  ├── on-premises.md
  │  ├── private-llm.md
  │  ├── scaling.md
  │  ├── monitoring.md
  │  ├── storage.md
  │  ├── analytics.md
  │  ├── recalculation.md
  │  └── troubleshooting.md
  │
  ├── reference/
  │  ├── content-schema.md
  │  ├── semantic-element-schema.md
  │  ├── chunk-schema.md
  │  ├── annotation-schema.md
  │  ├── security-policy-schema.md
  │  ├── analytics-event-schema.md
  │  ├── analytical-fact-schema.md
  │  ├── metric-schema.md
  │  ├── report-schema.md
  │  ├── search-api.md
  │  ├── annotation-api.md
  │  ├── analytics-api.md
  │  └── configuration.md
  │
  └── design/
    ├── synanton-design-1.24.md
    ├── synanton-design-1.25.md
    └── ...
  \```

\---

\# 7. Home Page

The homepage should communicate the platform in less than a few minutes.

\## Hero

\> **Enterprise knowledge infrastructure for heterogeneous content.**

Supporting statement:

\> Synanton transforms documents, images, audio, video  and enterprise records into structured, annotated, connected and  measurable knowledge.

Primary message:

\> **Extract once. Annotate flexibly. Connect knowledge. Search precisely. Recalculate efficiently. Measure continuously.**

\---

\# 8. What Is Synanton?

Explain Synanton without implementation detail.

Recommended definition:

\> Synanton is a programmable enterprise knowledge  platform for transforming heterogeneous information into structured,  annotated and connected knowledge that can be searched, related,  continuously recalculated and measured.

Show:

\```text
  Content
   ↓
  Extraction
   ↓
  Semantic Content
   ↓
  Chunks
   ↓
  Annotations
   ↓
  Knowledge
   ↓
  Search / Applications
   ↓
  Analytics
  \```

\---

\# 9. Content Model

Define the common representation consumed by downstream modules.

\```text
  Source
  ↓
  Extracted representation
  ↓
  Semantic elements
  ↓
  Semantic chunks
  \```

Semantic elements can represent:

\```text
  Document
  Page
  Section
  Paragraph
  Table
  Cell
  Image
  Caption
  Audio segment
  Speaker
  Video scene
  Transcript segment
  \```

The goal is a media-independent semantic foundation.

\---

\# 10. Content Extraction

Explain the Content Extractor as the source-processing boundary.

Examples:

\```text
  PDF
  → pages
  → headings
  → paragraphs
  → tables
  → images

Audio
  → channels
  → speakers
  → transcript
  → timestamps

Image
  → OCR
  → visual elements
  → detected objects

Video
  → scenes
  → clips
  → transcript
  \```

The Synanton platform consumes this structured output.

\---

\# 11. Semantic Chunking

Explain why arbitrary fixed-size chunks are insufficient.

Semantic chunks should preserve meaningful context and become independently addressable knowledge units.

Chunk boundaries affect:

\* search quality
  \* embeddings
  \* annotation scope
  \* security scope
  \* graph relationships
  \* recalculation cost
  \* analytics attribution

\---

\# 12. Chunk Security

Each chunk may carry security classification.

\```text
  Chunk 18291
  │
  ├── content
  ├── annotations
  ├── security = confidential
  └── provenance
  \```

Different portions of a document can therefore have different security characteristics.

\---

\# 13. Annotation Model

\> **Extraction describes what was recovered. Annotation describes what Synanton understands.**

Annotation types:

\```text
  Annotation
  ├── Tag
  ├── Classification
  ├── Entity
  ├── Attribute
  └── Signal
  \```

Annotations may be generated by rules, dictionaries, patterns, ML models, LLMs, external services, custom code or humans.

\---

\# 14. Annotation Types

Document:

\* Tag
  \* Classification
  \* Entity
  \* Attribute
  \* Signal

Each type should have examples and explain its role in the knowledge model.

\---

\# 15. Taxonomy vs Dependency

Make this distinction explicit:

\```text
  Taxonomy
  → semantic organization

Dependency
  → computational derivation
  \```

Therefore:

\> **Taxonomy describes meaning. Dependency describes derivation.**

\---

\# 16. Annotation Dependencies

Annotations may depend on other annotations.

\```text
  payment
  +
  duplicate-charge
    ↓
  billing-issue
    ↓
  escalation-required
  \```

Dependencies form a DAG.

Circular dependencies are rejected.

Dependency information enables incremental recalculation.

\---

\# 17. Annotation Provenance

Every derived annotation should answer:

\> Why does this annotation exist?

Document:

\* producer
  \* producer version
  \* definition
  \* definition version
  \* evidence
  \* confidence
  \* source
  \* target
  \* processing run
  \* dependencies
  \* creation time
  \* lifecycle

\---

\# 18. Security Classification

Security classification is a normal classification annotation.

\```text
  classification.security = confidential
  \```

Architecture:

\```text
  Chunk
   │
   ▼
  Security Classification
   │
   ▼
  Security Policy
   │
   ▼
  User / Group Mapping
   │
   ▼
  Search Authorization
  \```

\---

\# 19. Sensitive Data and Masking

Explain masking separately from classification.

\```text
  Classification
  → sensitivity level

Masking
  → permitted representation

Authorization
  → permitted user access
  \```

\---

\# 20. Masked and Unmasked Search

Authorized users may retrieve permitted unmasked representations.

Restricted users may receive masked representations.

The documentation should explain how search and representation selection interact.

\---

\# 21. Security-Aware Search

Search combines:

\```text
  Query
  │
  ├── lexical matching
  ├── semantic similarity
  ├── annotation filters
  ├── relationship constraints
  └── security authorization
  \```

Security filtering uses the current policy mapping.

\---

\# 22. Stable Classification / Dynamic Authorization

Highlight:

\> **Classification is knowledge state. Authorization mapping is policy state.**

Therefore:

\```text
  Authorization mapping changes
  → search policy changes

No mass knowledge rewrite required.
  \```

\---

\# 23. Knowledge Projections

Introduce:

\```text
  Semantic Chunk
     │
  ┌────┼────┐
  ▼  ▼  ▼
  Index Vector Graph
  \```

Each projection serves a different workload.

\---

\# 24. Reverse Index

Optimized for:

\* exact search
  \* lexical search
  \* annotation filtering
  \* classification filtering
  \* metadata filtering

\---

\# 25. Vector Store

Optimized for semantic similarity.

\```text
  Chunk
  ↓
  Embedding model
  ↓
  Vector
  \```

Vector results remain connected to canonical knowledge and applicable authorization metadata.

\---

\# 26. Graph Database

Optimized for relationships and contextual traversal.

\```text
  Customer
    │
    └── submitted → Ticket
             │
             ├── contains → PDF
             ├── contains → Audio
             └── concerns → Product
  \```

\---

\# 27. Why Three Stores?

\```text
  Reverse Index
  → exact retrieval

Vector Store
  → semantic retrieval

Graph
  → relationship retrieval
  \```

No single storage technology is assumed to be optimal for all workloads.

\---

\# 28. How Data Flows Through Synanton

Dedicated end-to-end page:

\```text
  Source
   ↓
  Ingestion
   ↓
  Extraction
   ↓
  Semantic Elements
   ↓
  Semantic Chunks
   ↓
  Security Classification
   ↓
  Annotations
   ↓
  Derived Annotations
   ↓
  Embeddings / Relationships
   ↓
  Reverse Index
  Vector Store
  Graph DB
   ↓
  Search
   ↓
  Authorization
   ↓
  Application
   ↓
  Analytics
  \```

For every transformation explain:

1. What changes?
2. Why is it needed?
3. What causes it?
4. What remains stable?
5. Can it be recalculated?
6. Is it observable through analytics?

\---

\# 29. Transformation Provenance

Document:

\```text
  Source
  ↓
  Extraction
  ↓
  Chunking
  ↓
  Annotation
  ↓
  Embedding
  ↓
  Index Projection
  ↓
  Graph Projection
  ↓
  Analytics
  \```

Each stage should remain explainable.

\---

\# 30. Recalculation

Recalculation is a first-class capability.

Explain:

\### Source change

\```text
  Source
  ↓
  Extraction
  ↓
  Chunking
  ↓
  Annotations
  ↓
  Projections
  ↓
  Analytics
  \```

\### Annotation rule change

\```text
  Rule
  ↓
  Affected annotations
  ↓
  Dependent annotations
  ↓
  Projections
  ↓
  Analytics
  \```

\### Security mapping change

\```text
  Group mapping
  ↓
  Search policy
  \```

Analytical facts may not need rewriting when only  authorization mapping changes, but authorization-sensitive analytical  caches must be invalidated.

\---

\# 31. Change Matrix

The documentation should include the architecture change-impact matrix.

Analytics should be an explicit output of relevant changes.

| Change             | Extraction |      Chunking |    Annotation |  Reverse Index |      Vector  |      Graph |     Analytics | Search Policy |
  | ------------------------------ | ---------: | ---------------: |  ---------------: | ---------------: | ---------------: |  ---------------: | -----------------: | ------------: |
  | Source content         |     ✓ |        ✓  |        ✓ |        ✓ |        ✓  |        ✓ |         ✓ |       — |
  | Extraction logic        |     ✓ |        ✓  |        ✓ |        ✓ |        ✓  |        ✓ |         ✓ |       — |
  | Chunking logic         |     — |        ✓  |        ✓ |        ✓ |        ✓  |        ✓ |         ✓ |       — |
  | Annotation rule        |     — |        —  |        ✓ |        ✓ |      maybe |       maybe |         ✓ |       — |
  | Annotation dependency     |     — |        —  |        ✓ |        ✓ |      maybe |       maybe |         ✓ |       — |
  | Embedding model        |     — |        —  |        — |        — |        ✓  |        — |         ✓ |       — |
  | Security classification logic |     — |        —  |        ✓ |        ✓ | policy-dependent |  policy-dependent |         ✓ |       — |
  | Group → classification mapping |     — |        —  |        — |        — |        —  |        — | query/cache policy |       ✓ |
  | Masking policy         |     — | policy-dependent |  policy-dependent | policy-dependent | policy-dependent |  policy-dependent |  policy-dependent |       ✓ |
  | Metric definition       |     — |        —  |        — |        — |        —  |        — |         ✓ |       — |
  | Report definition       |     — |        —  |        — |        — |        —  |        — |         ✓ |       — |

\---

\# 32. Resolutor

Resolutor determines **what needs to change**.

Inputs include:

\```text
  Source changes
  Rule changes
  Model changes
  Dictionary changes
  Annotation changes
  Dependency changes
  Classification changes
  Analytics definition changes
  \```

Output:

\```text
  Affected content
  Affected annotations
  Affected dependencies
  Affected projections
  Affected analytics
  \```

\---

\# 33. Equalix

Equalix controls execution.

Workloads include:

\```text
  Incremental ingestion
  Interactive processing
  User-triggered recalculation
  Background recalculation
  Analytics aggregation
  Historical analytics rebuild
  \```

Principle:

\> **Background knowledge and analytics maintenance must not starve incremental and interactive workloads.**

\---

\# 34. Analytics Plane

Introduce the Analytics Plane as a distinct architectural plane.

\> **The Analytics Plane observes platform activity and  knowledge state and produces derived metrics, statistics and reports.**

Conceptually:

\```text
  Knowledge / Platform
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
  \```

The Analytics Plane is not authoritative over source knowledge.

\---

\# 35. Analytics Events

Events represent observable activity or state transitions.

Examples:

\```text
  document_ingested
  document_extracted
  chunk_created
  annotation_created
  annotation_invalidated
  embedding_created
  search_executed
  recalculation_started
  recalculation_completed
  security_classification_changed
  \```

Events should preserve:

\* event identity
  \* tenant
  \* timestamp
  \* source
  \* processing run
  \* provenance
  \* security context
  \* schema version

\---

\# 36. Analytical Facts

Analytical facts are structured representations suitable for analytical workloads.

Examples:

\```text
  ContentFact
  ChunkFact
  AnnotationFact
  ProcessingFact
  SearchFact
  SecurityFact
  CostFact
  \```

Analytical facts should preserve lineage back to canonical knowledge and processing runs.

\---

\# 37. Annotation Analytics

Annotation analytics should support:

\```text
  annotation_type
  namespace
  name
  value
  producer
  producer_version
  definition_id
  definition_version
  target_type
  target_id
  evaluation_run_id
  confidence
  processing_duration
  created_at
  invalidated_at
  \```

This allows analytics to compare versions such as:

\```text
  payment-detection v3
  vs
  payment-detection v4
  \```

without losing provenance.

\---

\# 38. Analytics Lineage

The canonical lineage chain is:

\```text
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
  \```

Analytics should never sever lineage from the underlying knowledge model.

\---

\# 39. Analytics Security

Analytics follows the same fundamental security model as knowledge.

Analytical facts may inherit source classification.

Conceptually:

\```text
  AnalyticalFact
  ├── source_classification
  ├── representation_used
  ├── derived_classification
  └── access_scope
  \```

Rules:

\```text
  Masked-only source
  → analytics must not reconstruct original content

Dual representation
  → analytics follows applicable representation/class-grant policy

Non-PUBLIC source
  → analytical results remain tenant/classification constrained
  \```

\---

\# 40. Aggregate Side-Channel Protection

Aggregates can reveal sensitive information even without exposing individual records.

The documentation should explain:

\* minimum group sizes
  \* suppression
  \* rounding
  \* controlled dimensions
  \* classification-aware aggregation
  \* tenant-aware policies

Policies should be:

\* centrally defined
  \* tenant-configurable within platform limits
  \* classification-aware
  \* enforced at query time or materialization time
  \* auditable

Tenant configuration may strengthen protections but must not weaken platform security policy.

\---

\# 41. Report-Level Security

Reports must pass through the same authorization model as other knowledge access.

For example:

\```text
  Top Search Terms
  \```

must not expose restricted search terms merely because they are aggregated.

Report generation therefore includes:

\```text
  Metric
  ↓
  Classification policy
  ↓
  Tenant scope
  ↓
  Aggregate protection
  ↓
  Authorization
  ↓
  Report
  \```

\---

\# 42. Analytics Storage

Analytics storage is a replaceable implementation detail behind the Analytics Storage Contract.

Initial implementation may use an analytical columnar database such as ClickHouse.

Conceptually:

\```text
  Analytics Contract
      │
      ▼
  ┌─────────────────┐
  │ Analytical Store│
  └─────────────────┘
  \```

The documentation should emphasize:

\> **ClickHouse is an implementation choice, not an architectural dependency.**

The analytical event stream remains the authoritative replay source for derived analytics state.

\---

\# 43. Analytics Metrics

Metrics are named, versioned analytical definitions.

Examples:

\```text
  documents_processed
  documents_failed
  annotations_created
  annotation_confidence_avg
  processing_latency_p95
  search_latency_p95
  search_volume
  classification_distribution
  masking_outcomes
  recalculation_duration
  LLM_cost
  \```

Metrics should have:

\* identity
  \* version
  \* definition
  \* dimensions
  \* aggregation
  \* freshness
  \* security policy
  \* lineage

\---

\# 44. Reporting

Reports are presentation-level compositions of metrics.

Conceptually:

\```text
  Analytical Facts
     ↓
  Aggregates
     ↓
  Metrics
     ↓
  Report
  \```

Reports should not directly query canonical transactional knowledge unless explicitly required.

\---

\# 45. First Analytics Report

The documentation should use one concrete report as the reference implementation.

Example:

\```yaml
  Report: Daily Platform Processing
  Version: 1

Metrics:
   \- documents_processed
   \- documents_failed
   \- annotations_created
   \- processing_latency_p95

Dimensions:
   \- tenant
   \- media_type
   \- annotation_type

Refresh: Daily

Security: Tenant-isolated, classification-aware
  \```

This report demonstrates the complete path:

\```text
  Events
  → Facts
  → Aggregates
  → Metrics
  → Report
  \```

\---

\# 46. Metric Freshness

Define freshness classes:

\```text
  Real-time
  Near-real-time
  Hourly
  Daily
  \```

Each metric should document its expected freshness.

Freshness is part of the metric contract rather than an accidental property of implementation.

\---

\# 47. Analytics Retention

Different analytical data may have different retention policies.

Example:

\```text
  Raw events
  → short / configurable retention

Facts
  → medium retention

Aggregates
  → long retention

Business metrics
  → long-term retention
  \```

Retention should be automatically enforced.

Storage cost and expected analytical value should influence retention decisions.

\---

\# 48. Analytics Recalculation

Analytics must support controlled rebuilding.

Examples:

\```text
  Metric definition changes
      ↓
  Affected aggregates
      ↓
  Recalculation
  \```

or:

\```text
  Annotation rule changes
      ↓
  Knowledge recalculation
      ↓
  Analytical events
      ↓
  Affected facts
      ↓
  Aggregates
      ↓
  Metrics
  \```

The platform should avoid rebuilding unaffected analytics.

\---

\# 49. Security Reclassification and Analytics

Security policy changes require explicit analytics semantics.

The documentation should distinguish:

\```text
  Content classification changes
  → analytical facts may require recalculation/update

Authorization mapping changes
  → analytical facts normally remain unchanged
  → query authorization/cache policy changes
  \```

Authorization-sensitive analytical caches must be invalidated when security mappings change.

Historical facts may use validity periods where required:

\```text
  valid_from
  valid_to
  \```

\---

\# 50. Analytics and Masking

Analytics events must be emitted from the protected knowledge boundary.

Conceptually:

\```text
  Source
  ↓
  Extraction
  ↓
  Classification / Masking
  ↓
  Protected Knowledge
  ↓
  Analytics Event
  \```

Analytics must never capture sensitive original content before the masking/representation decision.

Safe analytics may record:

\```text
  entity_type = SSN
  financial_data_detected = true
  \```

without storing the original value.

\---

\# 51. Analytics and MCP

MCP may expose analytics capabilities:

\```text
  query_metric
  get_report
  inspect_metric
  inspect_lineage
  query_statistics
  \```

All Analytics MCP endpoints must pass through the complete analytics query/security pipeline.

MCP is an access interface, not a replacement for the internal Analytics contracts.

\---

\# 52. Analytics APIs

The documentation should distinguish:

\### Internal APIs

Used by:

\* platform services
  \* analytics processors
  \* operational tooling
  \* recalculation workflows

\### Customer-facing APIs

Used by:

\* enterprise applications
  \* dashboards
  \* reporting systems
  \* customer analytics workflows

Customer-facing APIs require:

\* authentication
  \* authorization
  \* tenant isolation
  \* rate limiting
  \* quotas
  \* aggregate protection

\---

\# 53. Analytics Observability

Initial operational metrics:

\```text
  consumer lag
  event loss rate
  event processing latency
  aggregate freshness
  query latency
  query error rate
  storage utilization
  storage growth
  recalculation duration
  \```

Initial alerts:

\```text
  Consumer lag > threshold
  Event loss > threshold
  Query p95 > SLA
  Storage > 80%
  Aggregate freshness > 2× expected
  Security policy failures
  \```

\---

\# 54. Cost Analytics

Analytics may measure:

\```text
  LLM cost
  Embedding cost
  Extraction cost
  Storage cost
  Processing cost
  \```

Cost data can itself reveal business volume or usage patterns and therefore remains subject to security and tenant isolation.

\---

\# 55. Classification and Masking Metrics

Initial security analytics should include:

\```text
  classification distribution
  counts by classification
  classification trends
  masked vs dual vs single representation
  masking outcomes
  security-policy failures
  \```

These metrics help operators understand platform security posture.

\---

\# 56. Polyglot Architecture

Synanton does not require every component to use the same programming language or storage technology.

\```text
  Stable Contracts
      │
  ┌─────┼─────┐
  ▼   ▼   ▼
  Python JVM/Rust Other
  │   │   │
  └─────┼─────┘
      ▼
    Synanton
  \```

Analytics storage follows the same principle.

\---

\# 57. Contracts

Document stable contracts between:

\```text
  Extractor → Structured Content
  Chunker → Chunk
  Annotation Engine → Annotation
  Annotation → Search
  Annotation → Graph
  Knowledge → Analytics Events
  Analytics Events → Facts
  Facts → Metrics
  Metrics → Reports
  Search → Application
  \```

\---

\# 58. MCP

MCP is an integration/access interface.

\```text
           Synanton
             │
      ┌─────────────┼─────────────┐
      ▼       ▼       ▼
     API      MCP   Internal Contracts
  \```

Potential capabilities:

\* knowledge search
  \* annotation inspection
  \* provenance
  \* analytics
  \* reports
  \* metrics
  \* knowledge retrieval

\---

\# 59. Use Cases

The documentation should demonstrate the same primitives through enterprise scenarios.

\## 59.1 Multimodal Support

\```text
  Ticket #12345
  │
  ├── Email
  ├── PDF invoice
  ├── Screenshot
  ├── Audio call
  └── Agent notes
  \```

Process:

\```text
  Ingest
  ↓
  Extract
  ↓
  Chunk
  ↓
  Classify
  ↓
  Annotate
  ↓
  Connect
  ↓
  Index
  ↓
  Search
  ↓
  Analytics
  \```

\---

\# 60. Enterprise Document Search

Show:

\```text
  PDF / Office / HTML / TIFF
      ↓
  Extraction
      ↓
  Semantic chunks
      ↓
  Annotations
      ↓
  Reverse Index + Vector Store
      ↓
  Search
      ↓
  Security
      ↓
  Analytics
  \```

\---

\# 61. Conversation Intelligence

\```text
  Audio
  ↓
  Transcription
  ↓
  Speakers / Channels / Time
  ↓
  Semantic chunks
  ↓
  Annotations
  ↓
  Analytics
  \```

Example:

\```text
  intent = cancellation
  sentiment = negative
  topic = billing
  customer = ACME
  tag = escalation
  \```

\---

\# 62. Customer Support Intelligence

Combine:

\```text
  Email
  PDF
  Screenshot
  Audio
  Agent notes
  Logs
  \```

Demonstrate how all representations become one connected knowledge model and then become measurable through analytics.

\---

\# 63. SRE / Production Support

\```text
  Incident
  │
  ├── alerts
  ├── logs
  ├── deployment
  ├── runbook
  ├── tickets
  ├── chat
  ├── incident call
  └── postmortem
  \```

Analytics can measure:

\```text
  incident volume
  processing latency
  annotation coverage
  search usage
  recalculation activity
  \```

\---

\# 64. Multimodal Enterprise Knowledge

Different media types are representations of enterprise knowledge.

\```text
  Documents
  Audio
  Images
  Video
  Tickets
  Logs
     ↓
  Synanton
     ↓
  Common knowledge model
     ↓
  Search + Applications + Analytics
  \```

\---

\# 65. Private / Regulated AI

\```text
  Customer environment
      │
      ▼
     Synanton
      │
  ┌──────┼──────┐
  ▼   ▼   ▼
  Rules Private LLM External model
  \```

LLMs remain annotation providers, not mandatory architectural dependencies.

Analytics must follow the same data residency and security boundaries as the protected knowledge environment.

\---

\# 66. Custom Enterprise Applications

Domains include:

\* insurance
  \* finance
  \* legal
  \* industrial maintenance
  \* compliance
  \* customer support
  \* operations
  \* enterprise search

The message:

\> Build domain-specific knowledge applications without  rebuilding extraction, annotation, search, graph, recalculation and  analytics infrastructure.

\---

\# 67. Architecture Navigation

Architecture documentation should follow the data flow:

\```text
  Source
  ↓
  Ingestion
  ↓
  Extraction Plane
  ↓
  Semantic Content
  ↓
  Chunking
  ↓
  Annotation Plane
  ↓
  Knowledge Projections
  ↓
  Search
  ↓
  Security
  ↓
  Recalculation
  ↓
  Analytics Plane
  \```

Supporting architecture:

\```text
  Resolutor
  Equalix
  Contracts
  Polyglot Architecture
  MCP
  Scaling
  \```

\---

\# 68. Developer Guides

Initial guides:

\## Ingestion

\* ingest a document
  \* ingest audio
  \* connect a source
  \* associate related content

\## Extraction

\* process PDF
  \* process image
  \* process audio
  \* process video

\## Chunking

\* create semantic chunks
  \* configure boundaries
  \* inspect provenance
  \* assign security classification

\## Annotation

\* create tags
  \* create classifications
  \* create entities
  \* create custom annotations
  \* use dictionaries
  \* use LLMs
  \* create derived annotations
  \* define dependencies
  \* inspect provenance

\## Security

\* configure classifications
  \* configure group mappings
  \* configure masking
  \* search masked content
  \* search unmasked content
  \* test authorization

\## Search

\* text search
  \* vector search
  \* annotation filtering
  \* security filtering
  \* hybrid search
  \* relationship-aware search

\## Recalculation

\* change a rule
  \* inspect impact
  \* create recalculation
  \* monitor execution
  \* prioritize workloads

\## Analytics

\* emit an analytics event
  \* define an analytical fact
  \* create an aggregate
  \* define a metric
  \* create a report
  \* query analytics
  \* configure freshness
  \* configure retention
  \* inspect lineage
  \* test analytics security
  \* rebuild historical analytics

\---

\# 69. Integrations

Document:

\```text
  Content Extractor
  MCP
  LLM providers
  Object storage
  Search engines
  Vector databases
  Graph databases
  Analytics storage
  \```

The integration documentation explains the contract first and implementation second.

\---

\# 70. Operations

Cover:

\* deployment
  \* private cloud
  \* on-premises
  \* storage
  \* scaling
  \* monitoring
  \* workload isolation
  \* recalculation
  \* analytics operations
  \* failure recovery
  \* backup/recovery

\---

\# 71. Analytics Operations

Dedicated operations documentation should cover:

\```text
  Analytics storage
  Event consumers
  Retention
  Partitioning
  Backups
  Rebuilds
  Late events
  Out-of-order events
  Schema migrations
  Query resource limits
  Workload isolation
  Monitoring
  Alerting
  \```

If ClickHouse is used, implementation documentation should explain:

\* deployment model
  \* partitioning
  \* replication
  \* backups
  \* restore
  \* schema migration
  \* compression
  \* storage estimation
  \* operational runbooks

These remain implementation details behind the Analytics Storage Contract.

\---

\# 72. Deployment Models

\## SaaS

\```text
  Customer
  ↓
  Synanton Cloud
  \```

\## Private Cloud

\```text
  Customer Cloud
  ↓
  Synanton
  \```

\## On-Premises

\```text
  Customer Network
  ↓
  Synanton
  ↓
  Private LLM
  \```

\## Hybrid

\```text
  Sensitive processing → private environment
  Non-sensitive processing → external services
  \```

Analytics deployment must follow the applicable data-residency and tenant-isolation requirements.

\---

\# 73. Reference Documentation

Reference should be implementation-oriented and ideally generated from actual contracts.

Initial reference:

\```text
  Content schema
  Semantic element schema
  Chunk schema
  Annotation schema
  Security policy schema
  Analytics event schema
  Analytical fact schema
  Metric schema
  Report schema
  Search API
  Annotation API
  Analytics API
  Configuration
  \```

\---

\# 74. Design Documents

Historical design proposals remain available for architectural traceability.

\```text
  design/
  ├── synanton-design-1.19.md
  ├── synanton-design-1.20.md
  ├── ...
  ├── synanton-design-1.24.md
  └── synanton-design-1.25.md
  \```

Design 1.24 should be linked from:

\* Annotation concepts
  \* Annotation architecture
  \* Dependency documentation
  \* Security architecture
  \* Recalculation architecture

Design 1.25 should be linked from:

\* Analytics concepts
  \* Analytics architecture
  \* Metrics
  \* Reporting
  \* Analytics security
  \* Analytics lineage
  \* Analytics recalculation
  \* Analytics storage

The main documentation should not require readers to understand historical design documents.

\---

\# 75. Navigation

Recommended MkDocs navigation:

\```yaml
  nav:
   \- Home: index.md

 \- Getting Started:
     \- Overview: getting-started/overview.md
     \- Quickstart: getting-started/quickstart.md
     \- Architecture Overview: getting-started/architecture-overview.md

 \- Concepts:
     \- Synanton: concepts/synanton.md
     \- Content Model: concepts/content-model.md
     \- Extraction: concepts/extraction.md
     \- Semantic Elements: concepts/semantic-elements.md
     \- Semantic Chunking: concepts/semantic-chunking.md
     \- Chunks: concepts/chunks.md
     \- Chunk Security: concepts/chunk-security.md
     \- Annotations: concepts/annotations.md
     \- Annotation Types: concepts/annotation-types.md
     \- Annotation Dependencies: concepts/annotation-dependencies.md
     \- Taxonomy: concepts/taxonomy.md
     \- Provenance: concepts/provenance.md
     \- Knowledge Projections: concepts/knowledge-projections.md
     \- Search: concepts/search.md
     \- Security Classification: concepts/security-classification.md
     \- Masking: concepts/masking.md
     \- Security-Aware Search: concepts/security-aware-search.md
     \- Relationships: concepts/relationships.md
     \- Ontology: concepts/ontology.md
     \- Analytics: concepts/analytics.md
     \- Metrics: concepts/metrics.md
     \- Reporting: concepts/reporting.md
     \- Contracts: concepts/contracts.md

 \- Use Cases:
     \- Overview: use-cases/overview.md
     \- Multimodal Support: use-cases/multimodal-support.md
     \- Enterprise Document Search: use-cases/enterprise-document-search.md
     \- Conversation Intelligence: use-cases/conversation-intelligence.md
     \- Customer Support: use-cases/customer-support.md
     \- SRE & Production Support: use-cases/sre-production-support.md
     \- Multimodal Knowledge: use-cases/multimodal-knowledge.md
     \- Private AI: use-cases/regulated-private-ai.md
     \- Analytics & Reporting: use-cases/analytics-and-reporting.md
     \- Custom Applications: use-cases/custom-enterprise-applications.md

 \- Architecture:
     \- Overview: architecture/overview.md
     \- Ingestion: architecture/ingestion.md
     \- Extraction Plane: architecture/extraction-plane.md
     \- Content Model: architecture/content-model.md
     \- Semantic Chunking: architecture/semantic-chunking.md
     \- Annotation Plane: architecture/annotation-plane.md
     \- Annotation Dependencies: architecture/annotation-dependencies.md
     \- Knowledge Projections: architecture/knowledge-projections.md
     \- Reverse Index: architecture/reverse-index.md
     \- Vector Store: architecture/vector-store.md
     \- Graph: architecture/graph.md
     \- Search Architecture: architecture/search-architecture.md
     \- Security: architecture/security.md
     \- Security-Aware Search: architecture/security-aware-search.md
     \- Masking: architecture/masking.md
     \- Recalculation: architecture/recalculation.md
     \- Resolutor: architecture/resolutor.md
     \- Equalix: architecture/equalix.md
     \- Analytics Plane: architecture/analytics-plane.md
     \- Analytics Events: architecture/analytics-events.md
     \- Analytical Facts: architecture/analytical-facts.md
     \- Metrics: architecture/metrics.md
     \- Reporting: architecture/reporting.md
     \- Analytics Security: architecture/analytics-security.md
     \- Analytics Lineage: architecture/analytics-lineage.md
     \- Analytics Recalculation: architecture/analytics-recalculation.md
     \- Analytics Storage: architecture/analytics-storage.md
     \- Polyglot Architecture: architecture/polyglot-architecture.md
     \- Contracts: architecture/contracts.md
     \- MCP: architecture/mcp.md
     \- Scaling: architecture/scaling.md

 \- Analytics:
     \- Overview: analytics/overview.md
     \- Concepts: analytics/concepts.md
     \- Events: analytics/events.md
     \- Facts: analytics/facts.md
     \- Aggregates: analytics/aggregates.md
     \- Metrics: analytics/metrics.md
     \- Reports: analytics/reports.md
     \- Dashboards: analytics/dashboards.md
     \- Freshness: analytics/freshness.md
     \- Retention: analytics/retention.md
     \- Security: analytics/security.md
     \- Lineage: analytics/lineage.md
     \- Recalculation: analytics/recalculation.md
     \- Storage: analytics/storage.md
     \- Operations: analytics/operations.md

 \- Guides:
     \- Ingestion: guides/ingestion/
     \- Extraction: guides/extraction/
     \- Chunking: guides/chunking/
     \- Annotations: guides/annotations/
     \- Security: guides/security/
     \- Search: guides/search/
     \- Recalculation: guides/recalculation/
     \- Analytics: guides/analytics/
     \- Integrations: guides/integrations/
     \- Operations: guides/operations/

 \- Integrations:
     \- Content Extractor: integrations/content-extractor.md
     \- MCP: integrations/mcp.md
     \- LLM Providers: integrations/llm-providers.md
     \- Storage: integrations/object-storage.md
     \- Search Engines: integrations/search-engines.md
     \- Vector Databases: integrations/vector-databases.md
     \- Graph Databases: integrations/graph-databases.md
     \- Analytics Storage: integrations/analytics-storage.md

 \- Operations:
     \- Deployment: operations/deployment.md
     \- On-Premises: operations/on-premises.md
     \- Private LLM: operations/private-llm.md
     \- Scaling: operations/scaling.md
     \- Monitoring: operations/monitoring.md
     \- Storage: operations/storage.md
     \- Analytics: operations/analytics.md
     \- Recalculation: operations/recalculation.md
     \- Troubleshooting: operations/troubleshooting.md

 \- Reference:
     \- Content Schema: reference/content-schema.md
     \- Semantic Element Schema: reference/semantic-element-schema.md
     \- Chunk Schema: reference/chunk-schema.md
     \- Annotation Schema: reference/annotation-schema.md
     \- Security Policy Schema: reference/security-policy-schema.md
     \- Analytics Event Schema: reference/analytics-event-schema.md
     \- Analytical Fact Schema: reference/analytical-fact-schema.md
     \- Metric Schema: reference/metric-schema.md
     \- Report Schema: reference/report-schema.md
     \- Search API: reference/search-api.md
     \- Annotation API: reference/annotation-api.md
     \- Analytics API: reference/analytics-api.md
     \- Configuration: reference/configuration.md

 \- Design:
     \- Design 1.24: design/synanton-design-1.24.md
     \- Design 1.25: design/synanton-design-1.25.md
  \```

\---

\# 76. Bilingual Documentation

The documentation should support:

\```text
  /en/
  /ru/
  \```

Both versions share the same information architecture.

Analytics terminology should preserve technical names where translation creates ambiguity:

\```text
  Analytics
  Analytical Fact
  Metric
  Aggregate
  Report
  Dashboard
  Event
  Lineage
  Freshness
  Retention
  \```

The English version remains authoritative for technical terminology.

\---

\# 77. Documentation Writing Style

Every architectural page should follow:

\```text
  What is it?
     ↓
  Why does it exist?
     ↓
  How does it work?
     ↓
  Example
     ↓
  How does it interact with other components?
     ↓
  What changes it?
     ↓
  What remains stable?
     ↓
  How is it secured?
     ↓
  How is it recalculated?
  \```

Analytics pages additionally explain:

\```text
  What is measured?
     ↓
  Where does the data come from?
     ↓
  What is authoritative?
     ↓
  How is lineage preserved?
     ↓
  What is the freshness?
     ↓
  How is it secured?
     ↓
  How is it recalculated?
  \```

\---

\# 78. Standard Architecture Page Template

\```text
  \# Component / Concept

\## What it is

Short definition.

\## Why it exists

Business and architectural motivation.

\## How it works

Diagram.

\## Example

Concrete enterprise scenario.

\## Inputs

What enters the component.

\## Outputs

What it produces.

\## Transformations

What changes.

\## Dependencies

What it relies upon.

\## Change and recalculation

What causes it to be recomputed.

\## Security

Authorization/masking implications.

\## Lineage

How the result can be traced.

\## Related concepts

Links to adjacent architecture.
  \```

\---

\# 79. Analytics Page Template

Analytics architecture pages should additionally use:

\```text
  \# Analytics Component

\## What it measures

\## Source of truth

\## Event / fact model

\## Aggregation

\## Metric definition

\## Freshness

\## Retention

\## Security

\## Tenant isolation

\## Aggregate protection

\## Lineage

\## Recalculation

\## Operational considerations

\## Related concepts
  \```

\---

\# 80. Hero Tutorial

The centerpiece tutorial should remain:

\# Build a Multimodal Support Knowledge System

Use:

\```text
  Ticket #12345
  │
  ├── Customer email
  ├── PDF invoice
  ├── Screenshot
  ├── Audio call
  └── Agent notes
  \```

Then:

\```text
  Ingest
  ↓
  Extract
  ↓
  Semantic elements
  ↓
  Semantic chunks
  ↓
  Security classification
  ↓
  Annotations
  ↓
  Derived annotations
  ↓
  Reverse Index
  Vector Store
  Graph
  ↓
  Search
  ↓
  Authorization
  ↓
  Masked / unmasked result
  ↓
  Analytics
  \```

Example analytics:

\```text
  tickets_processed
  documents_processed
  annotations_created
  billing_issue_count
  escalation_count
  processing_latency_p95
  search_latency_p95
  \```

Then change a rule:

\```text
  Rule changed
     ↓
  Resolutor
     ↓
  Affected annotations
     ↓
  Equalix
     ↓
  Controlled recalculation
     ↓
  Updated analytical facts
     ↓
  Updated metrics
  \```

This single tutorial demonstrates almost the entire Synanton architecture.

\---

\# 81. Signature Documentation Concepts

The documentation should intentionally emphasize:

\### 1. Semantic Content

Source material becomes structured semantic content.

\### 2. Semantic Chunks

Chunks are knowledge units.

\### 3. Annotation

Interpretation is separated from extraction.

\### 4. Annotation Dependencies

Knowledge can be derived compositionally.

\### 5. Provenance

Derived knowledge remains explainable.

\### 6. Classify Once, Authorize Dynamically

Security mapping changes do not require mass data rewrites.

\### 7. Masked vs Unmasked Knowledge

Sensitive information can have different permitted representations.

\### 8. Knowledge Projections

One knowledge model can support index, vector and graph technologies.

\### 9. Contract-Driven Polyglot Architecture

The best implementation technology can be selected per problem.

\### 10. Dependency-Aware Recalculation

Changing interpretation does not require rebuilding everything.

\### 11. Analytics is Derived State

Analytics observes knowledge and platform activity without becoming the source of truth.

\### 12. Analytics Preserves Lineage

Every important metric should remain traceable to its underlying facts and knowledge.

\### 13. Analytics Respects Security

Aggregates and reports cannot bypass knowledge security.

\### 14. Measure Without Rebuilding the Knowledge Model

Analytics provides operational and business visibility without turning the analytical store into the canonical knowledge store.

\---

\# 82. V1 Documentation Priority

The site should be built incrementally.

\## Phase 1 — Architecture foundation

1. Home
2. What is Synanton?
3. Architecture overview
4. Content model
5. Extraction
6. Semantic elements
7. Semantic chunking
8. Chunks
9. Chunk security
10. Annotations
11. Annotation types
12. Annotation dependencies
13. Taxonomy
14. Provenance
15. Knowledge projections
16. Search
17. Security classification
18. Masking
19. Security-aware search
20. Recalculation
21. Resolutor
22. Equalix
23. Contracts
24. Polyglot architecture

\---

\## Phase 2 — Analytics foundation

25. Analytics overview
26. Analytics Plane
27. Analytics events
28. Analytical facts
29. Analytics lineage
30. Analytics security
31. Metrics
32. Aggregates
33. Reporting
34. Freshness
35. Retention
36. Analytics recalculation
37. Analytics storage

\---

\## Phase 3 — End-to-end demonstration

38. Multimodal support tutorial
39. Document search
40. Conversation intelligence
41. Customer support
42. SRE knowledge
43. Analytics and reporting use case

\---

\## Phase 4 — Integration

44. Content Extractor
45. MCP
46. LLM providers
47. Vector stores
48. Graph databases
49. Search engines
50. Analytics storage

\---

\## Phase 5 — Developer adoption

51. Quickstart
52. Ingestion
53. Semantic chunking
54. Custom annotations
55. Security configuration
56. Search
57. Recalculation
58. Analytics event
59. Metric
60. Report
61. Analytics API reference

\---

\## Phase 6 — Operations

62. Deployment
63. Private AI
64. Scaling
65. Monitoring
66. Storage
67. Analytics operations
68. Recalculation operations
69. Troubleshooting

\---

\# 83. Documentation Governance

The documentation should distinguish three types of truth.

\## Conceptual truth

Stable concepts:

\```text
  Chunk
  Annotation
  Classification
  Relationship
  Projection
  Analytics
  Metric
  Report
  \```

\## Architectural truth

Current architecture:

\```text
  Extraction
  Annotation
  Resolutor
  Equalix
  Search
  Graph
  Analytics
  \```

\## Implementation truth

Current implementation:

\```text
  specific libraries
  databases
  services
  APIs
  configuration
  \```

The conceptual layer should change least frequently.

Implementation details should not leak into conceptual documentation unless necessary.

\---

\# 84. Relationship to Source Repositories

The Synanton documentation site provides the architectural umbrella.

\```text
  Synanton Documentation
      │
      ├── Platform architecture
      │
      ├── Content Extractor
      │   └── detailed extraction documentation
      │
      ├── Annotation modules
      │
      ├── Search
      │
      ├── Analytics
      │
      └── Integrations
  \```

The central site explains **how the projects fit together**, rather than duplicating every repository's README.

\---

\# 85. Documentation Architecture Diagram

The final architecture story should converge on:

\```text
               SYNANTON
                │
         ┌──────────────┴──────────────┐
         │               │
      Content Plane        Knowledge Plane
         │               │
         ▼               ▼
      Extraction          Annotation
         │               │
         ▼               ▼
     Semantic Content       Derived Knowledge
         │               │
         └──────────────┬──────────────┘
                ▼
             Semantic Chunks
                │
          ┌────────────┼────────────┐
          ▼      ▼      ▼
       Reverse Index Vector Store Graph DB
          │      │      │
          └────────────┼────────────┘
                ▼
               Search
                │
          ┌────────────┴────────────┐
          ▼             ▼
      Query semantics     Security policy
                       │
                   Group → Classification
                       │
                       ▼
                    Authorization
                       │
                       ▼
                     Results
                       │
                       ▼
                   Analytics Plane
                       │
                 ┌──────────┼──────────┐
                 ▼     ▼     ▼
                Events   Facts   Security Facts
                 │     │     │
                 └──────────┼──────────┘
                       ▼
                     Aggregates
                       │
                       ▼
                      Metrics
                       │
                       ▼
                      Reports

​    Rules / Models / Dictionaries / Source Changes
​                │
​                ▼
​               Resolutor
​                │
​                ▼
​             Dependency Analysis
​                │
​                ▼
​               Equalix
​                │
​                ▼
​              Recalculation
​                │
​                ├──────────────► Knowledge
​                │
​                └──────────────► Analytics
  \```

\---

\# 86. Final Documentation Thesis

The documentation should ultimately communicate one architectural idea:

\> **Synanton separates the acquisition of information  from the interpretation, authorization, projection and measurement of  knowledge.**

The resulting model is:

\```text
  Extract
    ↓
  Structure
    ↓
  Chunk
    ↓
  Classify
    ↓
  Annotate
    ↓
  Connect
    ↓
  Project
    ↓
  Search
    ↓
  Authorize
    ↓
  Measure
  \```

And when understanding changes:

\```text
  Change
   ↓
  Resolve impact
   ↓
  Recalculate only what is affected
   ↓
  Refresh derived projections and analytics
  \```

This makes Synanton a platform for **continuously evolving, secure and measurable enterprise knowledge**, rather than a static  document-ingestion, AI-search or reporting system.

The most important architectural distinction remains:

\```text
           CANONICAL KNOWLEDGE
               │
       ┌──────────────┼──────────────┐
       ▼       ▼       ▼
      Search     Graph    Analytics
     projection   projection   projection
       │       │       │
       └──────────────┼──────────────┘
               ▼
           All are derived
            from knowledge
  \```

**Knowledge remains authoritative.**

**Search, graph and analytics are projections.**

**Resolutor determines what becomes stale.**

**Equalix controls how changes are executed.**

**Security remains enforced across every projection and access path.**