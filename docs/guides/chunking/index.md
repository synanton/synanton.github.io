# Chunking Guides

Task-oriented steps for turning extracted content into [semantic chunks](../../concepts/chunks.md):
creating chunks, configuring boundaries, inspecting provenance, and assigning security classification.

## At a glance

Chunking is deterministic and structure-driven — the same document produces the same chunks every time,
independent of chunking's downstream consumers. This guide covers the configuration surface a tenant
actually controls: boundary strategy and thresholds. It does not cover classification logic itself; see
[Security Guides](../security/index.md) for that.

## Create semantic chunks

Chunking runs automatically once [extraction](../extraction/index.md) has produced semantic elements — there
is no separate step to trigger. What you configure is the strategy it applies:

```yaml
chunking:
  strategy: semantic      # semantic | fixed-token | sentence
  max_chunk_tokens: 800    # fallback limit, not the primary rule
  table_handling: atomic   # tables are never split mid-row or mid-column
```

The chunker works from the structure identified during extraction — sections, paragraphs, list items,
tables — and only falls back to a token-count split when a section is too large to keep as one piece.

## Configure boundaries

Boundary configuration decides *when* the chunker is allowed to split inside a large section, not whether
it may split a table or sever a heading from its paragraph — those rules are fixed.

| Setting | Effect |
|---|---|
| `max_chunk_tokens` | Upper bound before a section-level split is forced |
| `min_chunk_tokens` | Lower bound below which adjacent short paragraphs are merged |
| `table_handling: atomic` | Tables are never split, regardless of size |
| `heading_carry` | Whether a chunk repeats its section heading for context when embedded |

Changing these settings changes chunk boundaries for content processed afterward. It does not retroactively
rechunk existing content — see [Change and recalculation](#change-and-recalculation) below.

## Inspect provenance

Every chunk retains a pointer to the semantic elements it was built from, plus its page or time range. To
inspect a chunk's provenance:

1. Retrieve the chunk by its stable identifier.
2. Read its `source_elements` field — the exact structural elements (headings, paragraphs, table cells)
   the chunk was assembled from.
3. Read its page range (or timestamp range, for audio/video) — this is what lets a search result cite
   "§3.1 GPU Execution Plane" instead of "page 14."

See [Provenance](../../concepts/provenance.md) for the full lineage model this participates in.

## Assign security classification

Classification is not something you assign to a chunk manually as a chunking step — it runs automatically,
immediately after chunk boundaries are fixed, using the detectors and policy described in
[Security Guides → Configure classifications](../security/index.md#configure-classifications). What
chunking configuration *does* affect is classification granularity: a chunking strategy that groups
unrelated sensitive and non-sensitive content into one chunk forces an overly broad classification onto
all of it. Tightening boundaries around a compensation table, for example, keeps its `FINANCIAL`
classification from spreading to the surrounding prose.

## Change and recalculation

Changing `strategy`, `max_chunk_tokens`, or `table_handling` affects chunk boundaries only for content
processed after the change. Applying a new strategy to already-ingested content requires an explicit
recalculation — see [Recalculation Guides → Change a rule](../recalculation/index.md#change-a-rule) — which
invalidates every annotation, index entry, embedding, and graph edge tied to the old chunk boundaries.

## Go deeper

| If you want to know... | Read... |
|---|---|
| Why fixed-size splits fail and semantic boundaries don't | [Ingestion overview](../overviews/ingestion.md) |
| The chunk data model | [Chunks](../../concepts/chunks.md) |
| The chunker's implementation-level rules | [Semantic Chunking (architecture)](../../architecture/semantic-chunking.md) |
| The chunk schema | [Chunk Schema](../../reference/chunk-schema.md) |
