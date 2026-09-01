# Extraction Plane

## What it is

The Extraction Plane is the platform contract (`synanton.extraction.v1`) that turns raw source bytes into
structured [semantic elements](../concepts/semantic-elements.md) — and the boundary that keeps every parser,
OCR engine, or GPU accelerator invisible to everything downstream of it.

## Why it exists

The platform specifies **what** to extract and under what constraints; the plane specifies **how**.
Parsers, OCR sidecars, GPUs, queues, and worker topology must not appear on the contract. This is what lets
the extraction implementation evolve — swap a parser, add OCR for scanned documents, add a new format —
without touching chunking, security, indexing, or ranking logic.

## How it works

```text
Object store (raw bytes)
        │
        ▼
synanton.extraction.v1  (ExtractSync / async)
        │
        ▼
DocumentPayload (elements, headings, tables, page boxes)
        │
        ▼
synflux SemanticChunkStage → persist (page/section) → synquest
```

Feature support is always explicit — `APPLIED`, `NOT_APPLICABLE`, `UNSUPPORTED`, or `FAILED` — never
silently degraded. The contract is mirrored byte-for-byte between the primary platform and whatever
implements it (`content_extractor` today; see [Content Extractor integration](../integrations/content-extractor.md)),
verified by `scripts/verify-contract-mirror.sh`. If the plane is down or declines a given type, `synflux`
falls back to a local, fail-open extraction path (Tika) rather than blocking ingestion.

## Example

A PDF is submitted to `ExtractSync`; the plane returns a `DocumentPayload` with `elements`, `headings`,
`tables`, and `page boxes`. `synflux`'s `SemanticChunkStage` consumes that payload directly — it never
touches the PDF bytes or the parser that produced the payload.

## Inputs

Raw bytes from `synvault`, plus the source's declared or detected media type.

## Outputs

A `DocumentPayload` of structured [semantic elements](../concepts/semantic-elements.md), consumed by
[Semantic Chunking](semantic-chunking.md).

## Transformations

Format-specific parsing, layout analysis, OCR, and transcription — entirely inside the plane, entirely
invisible above the contract boundary.

## Dependencies

Depends on nothing downstream. [Ingestion](ingestion.md), [Semantic Chunking](semantic-chunking.md), and
everything after them depend on it.

## Change and recalculation

A new plane version or a parser change can alter the elements produced from already-ingested sources; per
the [change impact model](recalculation.md#change-impact-model), that ripples into chunking, annotation,
projections, and analytics — but never requires a contract version bump unless the contract shape itself
changes.

## Security

The plane performs no classification — see [Security](security.md). It must not leak raw content through
any channel other than the defined `DocumentPayload`.

## Lineage

Every semantic element in the payload retains enough positional metadata to trace a later chunk back to the
exact source location.

## Related concepts

[Semantic Chunking](semantic-chunking.md) · [Content Model](content-model.md) ·
[Content Extractor integration](../integrations/content-extractor.md) · [Contracts](contracts.md)
