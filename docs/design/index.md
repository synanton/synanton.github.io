# Design Documents

Historical design proposals remain available here for architectural traceability. They are **not**
required reading — the rest of this site (Concepts, Architecture, Analytics) is written so a reader never
has to open one of these to understand the platform.

## Documentation governance: three kinds of truth

| Layer | What it covers | Changes | Lives in |
|---|---|---|---|
| **Conceptual truth** | Stable concepts: chunk, annotation, classification, relationship, projection, analytics, metric, report | Least frequently | [Concepts](../concepts/synanton.md) |
| **Architectural truth** | Current architecture: extraction, annotation, Resolutor, Equalix, search, graph, analytics | With approved design revisions | [Architecture](../architecture/overview.md) |
| **Implementation truth** | Specific libraries, databases, services, APIs, configuration | Most frequently | Design documents below, and each project's own repository |

Implementation details should not leak into conceptual documentation unless necessary — if a Concepts or
Architecture page names a specific technology, it's calling out a deliberate implementation choice (e.g.
"ClickHouse is an implementation choice, not an architectural dependency" for analytics storage), not a
requirement.

## Design version history

| Version | Status | Covers |
|---|---|---|
| [1.25](synanton-design-1.25.md) | Approved (architecture), consolidates 1.24 | Annotations, derived knowledge, recalculation, analytics & reporting plane |
| [1.23](synanton-design-1.23.md) | Approved | Classification-aware semantic search |
| [1.22](synanton-design-1.22.md) | Current baseline | Semantic content structuring / chunking |
| [1.21](synanton-design-1.21.md) | Folded into 1.22 | Structured Content Extraction Plane (Part IX) |
| [1.20](synanton-design-1.20.md) | Folded into 1.22 | GPU Execution Plane (Part VIII) |
| [1.19](synanton-design-1.19.md) | Superseded baseline | Merged Parts I-VII baseline |

These are mirrored from the [`synanton/platform`](https://github.com/synanton/platform) repository's
`docs/architecture/` tree and are not automatically re-synced — treat that repository as the source of
truth, and refresh the copies here when a new design revision is approved there.

## What links to what

Design 1.25 is the primary source for:

[Annotations](../concepts/annotations.md) · [Annotation Dependencies](../concepts/annotation-dependencies.md) ·
[Security Classification](../concepts/security-classification.md) · [Recalculation](../architecture/recalculation.md) ·
[Analytics](../concepts/analytics.md) · [Metrics](../concepts/metrics.md) · [Reporting](../concepts/reporting.md)

Design 1.22/1.23 are the primary source for:

[Semantic Chunking](../concepts/semantic-chunking.md) · [Search](../concepts/search.md) ·
[Security-Aware Search](../concepts/security-aware-search.md)

Design 1.21/1.20 are the primary source for:

[Extraction](../concepts/extraction.md) · [Extraction Plane](../architecture/extraction-plane.md) — the GPU
execution detail in 1.20 lives entirely behind that contract and doesn't need to be read to understand the
extraction plane conceptually.

## Related repositories

Detailed, implementation-level design documents for specific modules live in their own repositories rather
than being duplicated here:

- [`synanton/platform`](https://github.com/synanton/platform) — `docs/architecture/`, `docs/api/`, `docs/book/`, ADRs
- `content_extractor` — `doc/Synanton_v1.21_Structured_content_extraction_plane.md`
- `gpu-runtime` — `doc/GPU Execution Plane Implementation Plan v1.21.md`
- `equalix` — recalculation/execution control implementation docs
- `commitix`, `lucentrix` — supporting platform service docs
