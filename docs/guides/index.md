# Guides

This section has two layers, for two different jobs.

<div class="grid cards" markdown>

-  **Overviews**

    Long-form, conversational explainers - no code, no protobuf, no gRPC - for readers who want to
    understand *why* Synanton is built the way it is before going deeper.

    [Search](overviews/search.md) · [Ingestion](overviews/ingestion.md) ·
    [Security](overviews/security.md) · [Deployment](overviews/deployment.md) ·
    [Troubleshooting](overviews/troubleshooting.md)

-  **How-to guides**

    Short, task-oriented steps for developers and operators doing a specific job: creating a tag,
    configuring a classification, changing a rule, defining a metric.

    [Ingestion](ingestion/index.md) · [Extraction](extraction/index.md) · [Chunking](chunking/index.md) ·
    [Annotations](annotations/index.md) · [Security](security/index.md) · [Search](search/index.md) ·
    [Recalculation](recalculation/index.md) · [Analytics](analytics/index.md) ·
    [Integrations](integrations/index.md) · [Operations](operations/index.md)

</div>

## Questions the Overviews answer

- **How does Synanton protect sensitive data?** → [Security](overviews/security.md)
- **Why are chunks important, and why not just split on token count?** → [Ingestion](overviews/ingestion.md)
- **What happens when I search?** → [Search](overviews/search.md)
- **How do I deploy this, and what changes between deployment modes?** → [Deployment](overviews/deployment.md)
- **Something looks wrong - where do I even start?** → [Troubleshooting](overviews/troubleshooting.md)

## What you won't find in the Overviews

By design, the Overviews don't cover API/gRPC contracts, SDK usage, or module-level implementation. Each
one ends with a **Go Deeper** table pointing to the normative engineering documents that are the actual
source of truth - those paths (`docs/architecture/...`, `docs/api/...`, `docs/book/...`) refer to the
[`synanton/platform`](https://github.com/synanton/platform) engineering repository, not to this
documentation site. For the underlying architecture explained on this site rather than in that repository,
see [Architecture](../architecture/overview.md) and [Design](../design/index.md).

## Relationship to Concepts and Architecture

The Overviews and How-to guides assume you already care about a specific task or question. If you want the
architectural story from first principles - why chunks exist, what an annotation is, why classification and
authorization are deliberately separate - start at [Concepts](../concepts/synanton.md) instead.
