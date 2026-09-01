# Content Model (Architecture)

## What it is

The architectural implementation of the [content model](../concepts/content-model.md): the concrete data
shapes — `DocumentPayload`, semantic elements, and semantic chunks — that flow between `synflux`'s pipeline
stages.

## Why it exists

For the platform's Extraction and Annotation planes to evolve independently, the shape connecting them has
to be concrete and stable, not just conceptually agreed. This page documents that shape at the level module
owners need to implement against.

## How it works

```text
Object store (raw bytes)
  ↓  Extraction Plane (synanton.extraction.v1)
DocumentPayload { elements, headings, tables, page boxes }
  ↓  synflux.Parser cache (ingestion_cache_chunks)
Semantic Elements (typed, position-aware)
  ↓  synflux.Chunker
Semantic Chunks { chunk_id, chunk_text_hash, section_path, page_start/end, source_elements[] }
```

Parsed artifacts are cached with a `schema_version`, keyed by content hash — a re-ingested, unchanged
document short-circuits the entire pipeline via the `ingestion_cache_source_digests` dedup gate before any
of the above runs again.

## Example

`chunk_id=18291` carries `section_path=["3. GPU Execution Plane", "3.1 GPU Gateway"]`, `page_start=3`,
`page_end=3`, and `source_elements=["elem_42","elem_43"]` — enough for a search result to cite "§3.1 GPU
Execution Plane" and for a security audit to know exactly which extracted elements a classification
decision was made about.

## Inputs

`DocumentPayload` from the [Extraction Plane](extraction-plane.md).

## Outputs

Semantic chunks consumed by [Semantic Chunking](semantic-chunking.md)'s chunker stage and, downstream, by
the [Annotation Plane](annotation-plane.md).

## Transformations

Parse (bytes → elements) → cache commit → chunk (elements → chunks) → cache commit, always cache-before-bus:
the write-through commit must succeed before anything is announced to the rest of the system.

## Dependencies

Depends on the [Extraction Plane](extraction-plane.md) contract. `synflux`'s Cassandra write-through cache
(`ingestion-cache`) is the durability boundary.

## Change and recalculation

A `schema_version` bump on cached artifacts requires either replay from source or a documented migration;
see [Semantic Chunking](semantic-chunking.md#change-and-recalculation) for what changes when chunk
boundaries move.

## Security

No classification happens at this layer — see [Security](security.md) for where and how it's applied,
immediately downstream of chunking.

## Lineage

Every chunk's `source_elements` pointer is the mechanism [Provenance](../concepts/provenance.md) relies on.

## Related concepts

[Extraction Plane](extraction-plane.md) · [Semantic Chunking](semantic-chunking.md) ·
[Ingestion](ingestion.md) · [Content Model (concept)](../concepts/content-model.md)
