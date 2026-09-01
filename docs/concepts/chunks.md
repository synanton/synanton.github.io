# Chunks

## What it is

A semantic chunk is an independently addressable **knowledge unit** — not an arbitrary slice of text, but
the thing that gets annotated, classified, indexed, embedded, related, searched, recalculated and measured.

## Why it exists

Every downstream capability needs *something* to attach itself to: a classification, a tag, an embedding,
a graph edge, an analytics fact. Rather than each of those attaching to raw text ranges independently, they
all attach to the same chunk, so a chunk is the one stable coordinate system the whole platform shares.

## How it works

A chunk is a small structured record, not just a string:

| Field | What it's for |
|---|---|
| Stable identifier | Lets every downstream store (index, vector store, graph) refer to the same unit consistently |
| Position in the document's outline | Lets a result cite "§3.1 GPU Execution Plane" instead of "page 14" |
| Content | What gets embedded, indexed, and classified |
| Pointer to source elements | Proves exactly where a piece of knowledge originated |
| Page / time range | Supports citation and audit |
| Security classification | A property of the chunk, not the whole document — see [Chunk Security](chunk-security.md) |

## Example

A chunk may participate in annotation (`intent = cancellation`), classification (`security = CONFIDENTIAL`),
indexing (a Lucene document), vectorization (an embedding), graph relationships (an edge to a `Customer`
node), search (a ranked hit), recalculation (a dependency target) and analytics (a fact row) — all keyed by
the same chunk identity.

## Inputs

Grouped [semantic elements](semantic-elements.md) from [semantic chunking](semantic-chunking.md).

## Outputs

A chunk feeds [chunk security](chunk-security.md) classification, [annotation](annotations.md), and the
three [knowledge projections](knowledge-projections.md) — reverse index, vector store, and graph.

## Transformations

None inherent to the chunk itself; chunks are the stable substrate that other transformations (annotation,
embedding, indexing) are applied to.

## Dependencies

Depends on [semantic chunking](semantic-chunking.md) having produced stable boundaries. Everything else in
the knowledge model — annotations, projections, search, analytics — depends on chunks in turn.

## Change and recalculation

If chunk boundaries change (because chunking logic changed), every annotation, index entry, embedding and
graph relationship tied to the old chunk identity becomes stale and must be recalculated. A chunk's own
content changing (because its source or extraction changed) has the same effect.

## Security

Classification is assigned per chunk, so different portions of the same document can carry different
sensitivity — see [Chunk Security](chunk-security.md).

## Lineage

A chunk's provenance fields — its source elements and page/time range — are what let the platform prove
later exactly where a piece of knowledge came from, and let a security decision be traced to precisely the
content it was made about.

## Related concepts

[Semantic Chunking](semantic-chunking.md) · [Chunk Security](chunk-security.md) · [Annotations](annotations.md) ·
[Knowledge Projections](knowledge-projections.md) · [Provenance](provenance.md)
