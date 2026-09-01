# Semantic Elements

## What it is

A semantic element is a typed, structurally-aware building block produced by [extraction](extraction.md) —
the smallest unit the platform recognizes as having a specific role in the source's structure.

## Why it exists

Raw text has no notion of "this is a heading" or "these numbers form a table." Semantic elements exist so
that the platform's understanding of a document's *shape* survives past the extraction boundary, instead of
being flattened into an undifferentiated wall of text before anything useful can be done with it.

## How it works

Semantic elements can represent:

```text
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
```

Each element carries its type, its position within the source's outline, and (where applicable) a page or
time range. Elements are media-independent in *type* even though the extraction process that produced them
is entirely media-specific.

## Example

A support call recording produces one `AudioSegment` element per speaker turn, each with a `speaker`
identity and a `[start_time, end_time]` range. A PDF invoice produces a `Table` element for the line-items
table, with `Cell` children, plus `Paragraph` and `Heading` elements for the surrounding text.

## Inputs

The structured payload emitted by [extraction](extraction.md) for a given source.

## Outputs

A tree of typed elements consumed by [semantic chunking](semantic-chunking.md) to produce
[semantic chunks](chunks.md).

## Transformations

None at this layer — semantic elements are extraction's output, not something further transformed until
chunking groups them.

## Dependencies

Depends on [extraction](extraction.md) having successfully parsed the source's media type.

## Change and recalculation

A change to extraction logic for a media type changes the semantic elements produced for affected sources,
which cascades into chunking, annotation and every downstream projection.

## Security

Semantic elements carry no classification — classification is a property of the
[semantic chunk](chunk-security.md) built from them, not of the raw elements themselves.

## Lineage

Every downstream chunk keeps a pointer back to the specific semantic elements it was built from.

## Related concepts

[Extraction](extraction.md) · [Content Model](content-model.md) · [Semantic Chunking](semantic-chunking.md) ·
[Chunks](chunks.md)
