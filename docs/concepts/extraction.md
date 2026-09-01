# Extraction

## What it is

Extraction is the boundary that turns raw source bytes into structured [semantic elements](semantic-elements.md) —
headings, paragraphs, tables, images, speaker turns, scenes — without saying anything about how that
structure was recovered.

## Why it exists

> **Extraction describes what content contains. Annotation describes what Synanton understands about it.**

Keeping extraction separate from interpretation means a classification rule, an entity model, or a
dictionary can change without re-parsing a single document — and a parser, an OCR engine, or a GPU
accelerator can be swapped without any search, security, or annotation logic downstream needing to change.

## How it works

```text
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
```

Extraction is a **platform contract**, not a specific processor: the platform specifies what to extract and
under what constraints; a pluggable extraction plane (embedded, sidecar, or clustered) specifies how.
Feature support is always explicit — `APPLIED`, `NOT_APPLICABLE`, `UNSUPPORTED`, or `FAILED` — rather than
silently degraded. See [Extraction Plane](../architecture/extraction-plane.md) for the contract and the
[Content Extractor integration](../integrations/content-extractor.md) for the implementation that provides
it today.

## Example

A 40-page contract PDF is extracted into page elements, section headings, paragraph elements, and one table
element per compensation table — each retaining its page range and its position in the document's outline.
If the extraction plane is temporarily unavailable, ingestion falls back to a simpler local extraction path
rather than blocking — the platform would rather ingest at reduced, visibly-flagged quality than not ingest
at all.

## Inputs

Raw bytes for a source, plus its declared or detected media type.

## Outputs

A structured payload of [semantic elements](semantic-elements.md): typed, position-aware building blocks
ready to be grouped into [semantic chunks](semantic-chunking.md).

## Transformations

Format-specific: PDF/Office layout analysis, OCR for scanned or image content, audio transcription with
speaker diarization, video scene segmentation.

## Dependencies

Extraction depends on nothing downstream — it is the first stage after ingestion. Everything else in the
[content model](content-model.md) depends on it.

## Change and recalculation

Changing extraction logic for a media type (a new parser version, added OCR support, a new supported
format) can change the semantic elements produced from already-ingested sources, which in turn can change
chunking, annotation, projections and analytics — see the
[change impact model](../architecture/recalculation.md#change-impact-model).

## Security

Extraction produces no classification decisions itself; classification happens once semantic elements are
grouped into chunks. See [Chunk Security](chunk-security.md).

## Lineage

Every semantic element retains enough positional metadata (page range, section path) to trace a later
chunk or annotation back to the exact passage it came from. See [Provenance](provenance.md).

## Related concepts

[Content Model](content-model.md) · [Semantic Elements](semantic-elements.md) · [Semantic Chunking](semantic-chunking.md) ·
[Extraction Plane](../architecture/extraction-plane.md)
