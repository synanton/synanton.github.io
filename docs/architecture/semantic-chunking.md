# Semantic Chunking (Architecture)

## What it is

The `synflux.Chunker` stage: the deterministic, structure-driven process that turns semantic elements into
stable [semantic chunks](../concepts/chunks.md).

## Why it exists

Chunking has to be deterministic — the same document must produce the same chunks every time, independent
of whichever model happens to be configured for downstream enrichment — because chunk identity is the
coordinate system every later stage (annotation, indexing, embedding, graph, analytics) keys against.

## How it works

The chunker applies the tenant's configured strategy (semantic, fixed-token, or sentence-based), working
from the structure identified during extraction rather than from flattened text:

```text
Section too large for one chunk?
   → split at paragraph/list boundary only
Table?
   → always atomic, never split mid-row/column
```

Each chunk receives a `chunk_text_hash` — a canonical, normalized content hash — used both for stable
identity and for the embedding cache key in [Vector Store](vector-store.md). `manifest.chunk_strategy_version`
records which strategy version produced a given chunk, so a later strategy change can be detected and scoped.

## Example

A 10,000-row compensation table remains one atomic chunk with a structured, column-aware representation.
Two paragraphs either side of it become separate chunks, each retaining the section heading they belong to.

## Inputs

Semantic elements from [Content Model](content-model.md), plus the tenant's chunking strategy
configuration.

## Outputs

Semantic chunks, each with `chunk_id`, `chunk_text_hash`, `section_path`, page range, and
`source_elements[]` — ready for [Security](security.md) classification and the
[Annotation Plane](annotation-plane.md).

## Transformations

Structure-driven grouping only — no LLM call, no non-determinism.

## Dependencies

Depends on [Extraction Plane](extraction-plane.md) output. Every projection and every annotation depends,
in turn, on chunk boundaries being stable.

## Change and recalculation

A chunking strategy or threshold change alters `manifest.chunk_strategy_version` for affected content and
invalidates every downstream artifact keyed to the old chunk boundaries — annotations, index entries,
embeddings, graph edges — per the [change impact model](recalculation.md#change-impact-model). Unchanged
sections keep their existing chunk identity and are not reprocessed.

## Security

Chunk boundaries determine classification granularity — a chunk that groups unrelated sensitive and
non-sensitive content forces an overly broad classification. See [Security](security.md).

## Lineage

Every chunk's `source_elements` pointer and page range are the mechanism that makes citation and audit
possible.

## Related concepts

[Content Model](content-model.md) · [Chunks (concept)](../concepts/chunks.md) ·
[Semantic Chunking (concept)](../concepts/semantic-chunking.md) · [Security](security.md)
