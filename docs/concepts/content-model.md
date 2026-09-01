# Content Model

## What it is

The content model is the common representation that every downstream module — chunking, annotation,
search, graph, analytics — consumes, no matter what the source was.

```text
Source
 ↓
Extracted representation
 ↓
Semantic elements
 ↓
Semantic chunks
```

## Why it exists

A PDF, a call recording, a scanned TIFF and a spreadsheet have nothing in common at the byte level. If every
downstream module had to understand every source format, adding a new format would mean touching chunking,
annotation, indexing, and the graph all at once. The content model exists to absorb that variety at one
boundary — [extraction](extraction.md) — so everything after it works against one media-independent shape.

## How it works

Extraction turns raw bytes into **semantic elements**: typed, structurally-aware building blocks such as a
document, a page, a section, a paragraph, a table, a cell, an image, a caption, an audio segment, a speaker
turn, a video scene, or a transcript segment. [Semantic chunking](semantic-chunking.md) then groups
semantic elements into **semantic chunks** — the actual knowledge units that get classified, annotated,
indexed, embedded and searched.

## Example

A PDF invoice becomes: a document element, page elements, a heading element ("Invoice #4471"), paragraph
elements, and a table element for the line items — each retaining its position in the document's outline
and its page range. An audio call becomes: an audio-segment element per speaker turn, each carrying a
timestamp range and a speaker identity. Both flow into the same chunking and annotation pipeline afterward.

## Inputs

Raw source bytes and their declared or detected media type (PDF, DOCX, HTML, image, audio, video, ...).

## Outputs

A tree of semantic elements, media-independent, ready for [semantic chunking](semantic-chunking.md).

## Transformations

Format-specific parsing, OCR, transcription and layout analysis all happen inside
[extraction](extraction.md) and are invisible above this boundary.

## Dependencies

The content model depends only on [extraction](extraction.md) having produced valid semantic elements for
the source's media type. It does not depend on chunking, annotation, or any specific search or storage
technology.

## Change and recalculation

Changing the extraction logic for a media type (a new PDF parser, added OCR support) can change the
semantic elements produced for previously-ingested content. Per the [Change Matrix](../architecture/recalculation.md#change-impact-model),
an extraction change ripples forward into chunking, annotation, projections and analytics.

## Security

Semantic elements carry no classification themselves — classification is assigned at the
[chunk](chunks.md) level once elements are grouped into chunks. See [Chunk Security](chunk-security.md).

## Lineage

Every semantic chunk retains a pointer back to the specific semantic elements it was built from, which is
what lets a search result cite "§3.1 GPU Execution Plane" instead of "page 14 of a 40-page PDF." See
[Provenance](provenance.md).

## Related concepts

[Extraction](extraction.md) · [Semantic Elements](semantic-elements.md) · [Semantic Chunking](semantic-chunking.md) ·
[Chunks](chunks.md) · [Provenance](provenance.md)
