# Synanton

## What it is

Synanton is a programmable enterprise knowledge platform. It transforms heterogeneous information —
documents, images, audio, video, tickets, logs — into structured, annotated and connected knowledge that
can be searched, related, continuously recalculated and measured.

It is deliberately defined by what it *produces* (knowledge with these properties), not by which technology
happens to implement any one stage today.

## Why it exists

Most organizations already have search engines, vector databases, document parsers, and reporting tools.
What they don't have is a single place where:

- extraction (what content contains) is separated from interpretation (what the platform understands about
  it), so re-annotating doesn't mean re-parsing;
- every unit of knowledge can be independently classified, indexed, embedded, related and measured;
- a security classification survives changes to who is allowed to see what, without rewriting content;
- changing a rule or a model triggers *only* the recalculation that's actually affected, not a full rebuild;
- analytics observes all of the above without quietly becoming the authoritative system of record.

Synanton exists to make that architecture available as a platform, rather than something every enterprise
knowledge project re-invents — usually incompletely — on its own.

## How it works

```text
Content
 ↓
Extraction
 ↓
Semantic Content
 ↓
Chunks
 ↓
Annotations
 ↓
Knowledge
 ↓
Search / Applications
 ↓
Analytics
```

Source content becomes **semantic content** (structure-aware, media-independent) through
[extraction](extraction.md), is divided into **[semantic chunks](chunks.md)** — independently addressable
knowledge units — and is layered with **[annotations](annotations.md)**: tags, classifications, entities,
attributes and signals that record what Synanton understands, as distinct from what was merely extracted.

That knowledge is projected into a [reverse index, vector store and graph](knowledge-projections.md) so it
can be [searched](search.md) by keyword, meaning and relationship at once — with
[security classification](security-classification.md) enforced as part of the search itself, not as an
afterthought filter. When a rule, model or dictionary changes, [recalculation](../architecture/recalculation.md)
determines what became stale and updates only that. Everything above is, in turn, observable through
[Analytics](analytics.md) — without analytics becoming the source of truth for the knowledge itself.

## Example

A support ticket arrives with an email, a PDF invoice, a screenshot and a recorded call. Each is extracted
into semantic content, chunked, classified, and annotated (`intent = cancellation`, `topic = billing`).
Annotations on the invoice and the call are connected through the customer and the ticket. A search for
"customers threatening to cancel over billing" returns matching chunks across all four source types, ranked
together, filtered to what the searching user is authorized to see. The whole interaction is measurable
through `tickets_processed`, `billing_issue_count`, and `escalation_count` — see
[Multimodal Support](../use-cases/multimodal-support.md) for the full walkthrough.

## Related concepts

[Content Model](content-model.md) · [Semantic Chunking](semantic-chunking.md) · [Annotations](annotations.md) ·
[Knowledge Projections](knowledge-projections.md) · [Security Classification](security-classification.md) ·
[Contracts](contracts.md)
