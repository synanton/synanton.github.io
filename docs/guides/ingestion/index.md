# Ingestion Guides

Task-oriented steps for getting content into Synanton: ingesting a document, ingesting audio, connecting a
source, and associating related content.

## At a glance

Ingestion is the entry point to the pipeline described in [Content Model](../../concepts/content-model.md):
raw bytes go in, [semantic elements](../../concepts/semantic-elements.md) come out. Everything in this guide
configures *how content arrives*, not what happens to it afterward — for that, see the
[Extraction](../extraction/index.md) and [Chunking](../chunking/index.md) guides.

## Ingest a document

A document is ingested by reference, not by upload-and-forget: the platform pulls the content from a
source through a pluggable content adapter, so the same ingestion path works whether the source is a
filesystem, an object store, or an enterprise content system.

1. Register the source (see [Connect a source](#connect-a-source)) if it isn't already known.
2. Submit a content reference — a URI the adapter can resolve — rather than the raw bytes directly where
   possible. This keeps ingestion resumable: a partial pull restarts from the last consistent point instead
   of starting over.
3. The platform commits the raw content durably before announcing it to any downstream stage. If that
   initial commit fails, nothing downstream ever hears about the document — there is no half-processed
   reference for anything else to trip over.

A re-submitted, byte-identical document short-circuits the entire pipeline: the platform recognizes the
content by a fingerprint of the raw bytes and confirms existing results are still valid rather than
re-parsing, re-chunking, or re-annotating anything. This makes re-running an ingestion job safe to do
liberally.

## Ingest audio

Audio ingestion follows the same content-reference model as a document, with one addition: the source
media type determines which [extraction](../extraction/index.md) path handles it — transcription,
speaker/channel segmentation, and timestamping happen inside the [Extraction Plane](../../architecture/extraction-plane.md),
not in ingestion itself.

1. Submit the audio content reference the same way as a document.
2. Confirm the source's declared or detected media type resolves to an audio extraction path — if it
   doesn't, extraction reports `UNSUPPORTED` explicitly rather than silently producing nothing.
3. Downstream, each speaker turn becomes its own [semantic element](../../concepts/semantic-elements.md),
   which [semantic chunking](../chunking/index.md) groups into chunks the same way it groups paragraphs.

## Connect a source

Connecting a source registers a content adapter — the platform's boundary with wherever content actually
lives (a filesystem, an object store, an enterprise content system, a webhook feed) — so subsequent
ingestion calls can reference it by name rather than by raw connection detail.

A source registration should specify:

| Field | Purpose |
|---|---|
| Adapter type | Which content adapter resolves references from this source |
| Connection scope | What this adapter is allowed to read (a bucket, a folder tree, a mailbox) |
| Tenant | Which tenant's knowledge this source's content belongs to |
| Cursor/resume state | Where a resumable crawl or feed left off |

Adapters are cursor-resumable by design: a source outage or a restart does not require re-crawling content
that was already acquired.

## Associate related content

Related content — an email, its PDF attachment, a screenshot referenced in a support ticket — should be
ingested as separate sources that share a common relationship, not merged into one artifact before
ingestion. Merging would destroy each item's own [provenance](../../concepts/provenance.md) and prevent it
from being classified and searched independently.

1. Ingest each piece of content through its normal path.
2. Record the relationship (e.g. `Ticket contains PDF`) as an [Entity/relationship annotation](../annotations/index.md)
   once both sides have been extracted and chunked.
3. The [graph projection](../../architecture/graph.md) makes the relationship traversable — see
   [Multimodal Support](../../use-cases/multimodal-support.md) for the full worked example of a ticket with
   five related representations.

## Go deeper

| If you want to know... | Read... |
|---|---|
| Why chunking matters and why fixed-size splits fail | [Ingestion overview](../overviews/ingestion.md) |
| What a semantic element is | [Semantic Elements](../../concepts/semantic-elements.md) |
| The ingestion pipeline's failure semantics and SLOs | [Ingestion (architecture)](../../architecture/ingestion.md) |
| How to connect the Content Extractor | [Content Extractor integration](../../integrations/content-extractor.md) |
