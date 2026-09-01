# Getting Started

## Who this is for

This section is the shortest path to understanding what Synanton is and how its pieces fit together, before
going deep into any one of them. If you already know what problem you're solving, you may prefer to jump
straight to [Use Cases](../use-cases/overview.md) or [Guides](../guides/index.md).

## The shortest possible description

> Synanton transforms heterogeneous enterprise content into structured, annotated, connected and measurable
> knowledge.

Read [What is Synanton?](../concepts/synanton.md) for the full definition, or
[How Data Flows Through Synanton](architecture-overview.md) for the end-to-end pipeline with every
transformation explained.

## How to read this documentation

The site is organized into seven layers, and you're free to stop at any layer that answers your question:

```text
Introduction → Concepts → Use Cases → Architecture → Analytics → Guides/Integrations → Reference/Design
```

| If you are... | Start here | Then continue to |
|---|---|---|
| A business or mid-technical reader | [Concepts](../concepts/synanton.md) | [Use Cases](../use-cases/overview.md), [Analytics overview](../analytics/overview.md) |
| An enterprise architect or technical decision maker | [Architecture Overview](../architecture/overview.md) | [Security](../architecture/security.md), [Recalculation](../architecture/recalculation.md), [Analytics](../architecture/analytics-plane.md), [Contracts](../architecture/contracts.md) |
| A developer or integrator | [Guides](../guides/index.md) | [Integrations](../integrations/content-extractor.md), [Reference](../reference/search-api.md) |
| An SRE / support engineer | [Guides → Operations](../guides/operations/index.md) | [Operations](../operations/deployment.md), [Troubleshooting 101](../guides/overviews/troubleshooting.md) |

## Three things worth knowing before anything else

1. **Extraction and interpretation are separate.** What a document contains and what Synanton understands
   about it are two different steps, produced by two different planes. See
   [Content Model](../concepts/content-model.md).
2. **A semantic chunk is a knowledge unit**, not an arbitrary slice of text — it's what gets annotated,
   classified, indexed, embedded, related, searched, recalculated and measured. See
   [Chunks](../concepts/chunks.md).
3. **Classification and authorization are different.** Content carries a security classification;
   whether a specific user can see it depends on policy, evaluated at search time — so a policy change
   never requires rewriting content. See [Security Classification](../concepts/security-classification.md).

## Next

[How Data Flows Through Synanton](architecture-overview.md) walks the entire pipeline — source to search to
analytics — in one page, and is the recommended next stop.
