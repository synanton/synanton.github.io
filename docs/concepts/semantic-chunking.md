# Semantic Chunking

## What it is

Semantic chunking is the process that groups [semantic elements](semantic-elements.md) into
[semantic chunks](chunks.md) — the units that actually get classified, annotated, indexed, embedded and
searched.

## Why it exists

The naive way to prepare content for search is to slice it into fixed-size windows — every 500 words, say —
regardless of what's inside each window. This is cheap and reliably bad, because **meaning doesn't respect
arbitrary boundaries**: a fixed-size split can sever a table mid-row, separate a heading from the paragraph
it introduces, or cut a conditional clause in half at exactly the point where the condition lives.

Synanton inverts the usual priority:

> **Semantic boundaries first. Token or word-count limits are a fallback, not the primary rule.**

## How it works

```text
Naive: fixed token windows
  "...eligible for the annual bonus program.
   Compensation Table: Name | Salary | Bonus"
        → "John Doe | 180,000 | 15,000
           Jane Roe | 165,00..."   (table severed mid-row)

Synanton: semantic boundaries
  Chunk: "employees are eligible for the annual bonus program"
  Chunk: full Compensation Table, kept intact, atomic
```

The chunker works from the *structure* identified during extraction — sections, paragraphs, list items,
tables — rather than from flattened text. It only splits a section at a paragraph or list boundary when the
section is too large to handle as one piece, and a table is treated as **atomic**: never split mid-row or
mid-column, and given a structured, column-aware representation rather than being flattened into
undifferentiated numbers.

## Example

A 10,000-row table is still one atomic chunk, structurally represented rather than flattened — because a
search or an embedding of a wall of unlabelled digits is useless, no matter how small the pieces are cut.

## Inputs

The tree of [semantic elements](semantic-elements.md) produced by extraction for one source.

## Outputs

A set of [semantic chunks](chunks.md), each with a stable identifier, its position in the outline, and a
pointer back to the structural elements it was built from.

## Transformations

Deterministic and structure-driven — chunking does not use an LLM, specifically so the same document
produces the same chunks every time regardless of which model happens to be configured elsewhere.

## Dependencies

Depends on [extraction](extraction.md) having produced semantic elements. [Chunk security](chunk-security.md),
annotation, indexing, embedding and graph relationships all depend on chunk boundaries being stable.

## Change and recalculation

Changing chunking logic (thresholds, atomicity rules, strategy) changes chunk boundaries for affected
sources, which forces re-annotation, re-indexing, re-embedding and re-analytics for those chunks — see the
[change impact model](../architecture/recalculation.md#change-impact-model). Changed sections benefit from
chunk-level idempotent identity, so reprocessing does not require throwing away chunks that didn't change.

## Security

Chunk boundaries determine the *granularity* of security classification — see
[Chunk Security](chunk-security.md). A chunking strategy that groups unrelated content into one chunk can
force an overly broad classification on it.

## Lineage

Each chunk's pointer to its source elements and page range is what lets a search result cite a precise
location, and lets a security or provenance audit prove exactly what content a decision was made about.

## Related concepts

[Semantic Elements](semantic-elements.md) · [Chunks](chunks.md) · [Chunk Security](chunk-security.md) ·
[Provenance](provenance.md) · [Recalculation](../architecture/recalculation.md)
