# Extraction Guides

Task-oriented steps for turning raw content into structured [semantic elements](../../concepts/semantic-elements.md):
processing a PDF, an image, audio, and video.

## At a glance

Every media type goes through the same [Extraction Plane](../../architecture/extraction-plane.md) contract
(`synanton.extraction.v1`) and comes out the other side as the same kind of thing: a tree of typed,
position-aware elements. What differs between media types is entirely behind that contract — which parser
or model runs, whether OCR or transcription is involved, whether the work is CPU- or GPU-backed. None of
that is visible from this guide, and it doesn't need to be.

## Process a PDF

1. Submit the PDF through [ingestion](../ingestion/index.md).
2. Extraction returns a payload of elements: pages, headings, paragraphs, and tables, each retaining its
   page range and its position in the document's outline.
3. A table is always returned as one atomic element with a structured, column-aware representation — never
   flattened into an undifferentiated block of numbers.

If the extraction plane is unavailable or declines the PDF, the pipeline falls back to a simpler local
extraction path rather than blocking ingestion. This is reported explicitly, not silently: the platform
would rather ingest at reduced, visibly-flagged quality than not ingest at all.

## Process an image

1. Submit the image through [ingestion](../ingestion/index.md).
2. Extraction runs OCR to recover text, plus visual-element and object detection where configured.
3. The resulting elements — recovered text blocks, detected objects — flow into
   [semantic chunking](../chunking/index.md) exactly like a document's paragraphs would.

An image with no recoverable text still produces elements (detected objects, captions where vision
captioning is enabled) rather than an empty result — extraction reports what it found, including "nothing
textual," rather than failing.

## Process audio

1. Submit the audio through [ingestion](../ingestion/index.md).
2. Extraction returns channel, speaker, and transcript elements, each carrying a timestamp range.
3. Speaker turns become the semantic elements that [chunking](../chunking/index.md) groups — a chunk
   typically corresponds to one coherent speaker turn or a short run of turns, not an arbitrary time
   window.

See [Conversation Intelligence](../../use-cases/conversation-intelligence.md) for how transcript chunks
carry forward into annotation (`intent`, `sentiment`, `topic`).

## Process video

1. Submit the video through [ingestion](../ingestion/index.md).
2. Extraction segments the video into scenes and produces a transcript alongside them, mirroring the audio
   path for the spoken content while adding scene boundaries as their own elements.
3. A scene element and its corresponding transcript segment are chunked together where they describe the
   same span of the video, so a search result can cite both the visual context and what was said.

## Go deeper

| If you want to know... | Read... |
|---|---|
| Why extraction is a contract, not a processor | [Extraction](../../concepts/extraction.md) |
| The extraction plane's feature-state model and fallback behavior | [Extraction Plane](../../architecture/extraction-plane.md) |
| The implementation behind the contract | [Content Extractor integration](../../integrations/content-extractor.md) |
| GPU-accelerated extraction stages | [GPU Runtime integration notes](../../operations/scaling.md) |
