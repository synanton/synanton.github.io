#!/usr/bin/env python3
"""Generate placeholder stub pages for nav entries outside the current content phase.

Each stub carries: title, one-paragraph description (from the site plan), the plan
section it comes from, and a "Go further" pointer to source material where known.
Re-running this script only creates files that don't already exist -- it never
overwrites a page that has real content.
"""
import os

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")

# (path relative to docs/, title, plan section, description, optional source note)
STUBS = [
    ("getting-started/quickstart.md", "Quickstart", "§82 Phase 5",
     "A hands-on path to ingesting a first document, running a first search, and seeing "
     "classification and masking in action.",
     "See `guides/overviews/ingestion-101.md` and `guides/overviews/search-101.md` for the "
     "concepts this quickstart will exercise."),

    ("concepts/relationships.md", "Relationships", "§26-27",
     "How entities and facts extracted across chunks and documents connect into a graph, "
     "and why relationship retrieval is a distinct capability from lexical or semantic search.",
     "See `architecture/graph.md` and Design 1.22 §8 (GraphRAG)."),
    ("concepts/ontology.md", "Ontology", "§5 (Concepts layer)",
     "How Synanton's ontology organizes the meaning of tags, classifications and entities "
     "across tenants and domains.",
     "See `synanton/platform` `docs/architecture/syntology/ontology-management.md`."),
    ("concepts/analytics.md", "Analytics", "§34, Phase 2",
     "Analytics observes platform activity and knowledge state and produces derived metrics, "
     "statistics and reports -- without becoming authoritative over the underlying knowledge.",
     "See Design 1.25 (`design/synanton-design-1.25.md`) and `architecture/analytics-plane.md`."),
    ("concepts/metrics.md", "Metrics", "§43, Phase 2",
     "Metrics are named, versioned analytical definitions with identity, dimensions, "
     "aggregation, freshness, security policy and lineage.",
     "See Design 1.25 and `architecture/metrics.md`."),
    ("concepts/reporting.md", "Reporting", "§44, Phase 2",
     "Reports are presentation-level compositions of metrics, built from analytical facts and "
     "aggregates -- not direct queries against canonical transactional knowledge.",
     "See Design 1.25 and `architecture/reporting.md`."),

    ("use-cases/overview.md", "Use Cases Overview", "§59, Phase 3",
     "The same architectural primitives -- extraction, chunking, annotation, security, search, "
     "recalculation, analytics -- demonstrated through concrete enterprise scenarios.", None),
    ("use-cases/multimodal-support.md", "Multimodal Support", "§59.1 / §80 (Hero Tutorial), Phase 3",
     "The centerpiece tutorial: one support ticket (email, PDF invoice, screenshot, audio call, "
     "agent notes) ingested, extracted, chunked, classified, annotated, connected, indexed, "
     "searched and measured -- then recalculated when a rule changes.", None),
    ("use-cases/enterprise-document-search.md", "Enterprise Document Search", "§60, Phase 3",
     "PDF/Office/HTML/TIFF documents through extraction, semantic chunking, annotation, hybrid "
     "search, security and analytics.", None),
    ("use-cases/conversation-intelligence.md", "Conversation Intelligence", "§61, Phase 3",
     "Audio through transcription, speaker/channel/time segmentation, semantic chunking and "
     "annotation (intent, sentiment, topic, escalation).", None),
    ("use-cases/customer-support.md", "Customer Support Intelligence", "§62, Phase 3",
     "Combining email, PDF, screenshot, audio, agent notes and logs into one connected, "
     "measurable knowledge model.", None),
    ("use-cases/sre-production-support.md", "SRE / Production Support", "§63, Phase 3",
     "Incidents assembled from alerts, logs, deployments, runbooks, tickets, chat and "
     "postmortems, measured through annotation coverage and recalculation activity.", None),
    ("use-cases/multimodal-knowledge.md", "Multimodal Enterprise Knowledge", "§64, Phase 3",
     "Documents, audio, images, video, tickets and logs as representations of one common "
     "knowledge model.", None),
    ("use-cases/regulated-private-ai.md", "Private / Regulated AI", "§65, Phase 3",
     "Rules, private LLMs and external models as interchangeable annotation providers under "
     "data residency and security constraints.", None),
    ("use-cases/analytics-and-reporting.md", "Analytics & Reporting", "§59 / Phase 4",
     "How the Analytics Plane turns platform activity and knowledge state into metrics and "
     "reports without becoming the source of truth.", None),
    ("use-cases/custom-enterprise-applications.md", "Custom Enterprise Applications", "§66, Phase 3",
     "Building domain-specific knowledge applications (insurance, finance, legal, compliance, "
     "operations) without rebuilding extraction, annotation, search, graph, recalculation or "
     "analytics infrastructure.", None),

    ("architecture/analytics-plane.md", "Analytics Plane", "§34, Phase 2",
     "The Analytics Plane as a distinct architectural plane that observes platform activity "
     "and knowledge state and produces derived metrics, statistics and reports.",
     "See Design 1.25 (`design/synanton-design-1.25.md`)."),
    ("architecture/analytics-events.md", "Analytics Events", "§35, Phase 2",
     "Observable activity or state transitions (e.g. `document_ingested`, `annotation_created`) "
     "carrying event identity, tenant, timestamp, source, provenance and security context.",
     "See Design 1.25."),
    ("architecture/analytical-facts.md", "Analytical Facts", "§36-37, Phase 2",
     "Structured representations suitable for analytical workloads (ContentFact, ChunkFact, "
     "AnnotationFact, ...), preserving lineage back to canonical knowledge.",
     "See Design 1.25."),
    ("architecture/metrics.md", "Metrics", "§43, Phase 2",
     "Named, versioned analytical definitions with identity, dimensions, aggregation, "
     "freshness, security policy and lineage.", "See Design 1.25."),
    ("architecture/reporting.md", "Reporting", "§44-45, Phase 2",
     "Presentation-level compositions of metrics, demonstrated through the reference "
     "'Daily Platform Processing' report.", "See Design 1.25."),
    ("architecture/analytics-security.md", "Analytics Security", "§39-41, Phase 2",
     "Why analytics follows the same security model as knowledge, and how aggregate side-"
     "channel protection prevents aggregates from leaking what individual records can't.",
     "See Design 1.25."),
    ("architecture/analytics-lineage.md", "Analytics Lineage", "§38, Phase 2",
     "The canonical lineage chain from Source through ECM Element, Chunk, Annotation, "
     "Processing Run, Knowledge Projection, Analytical Event, Fact, Aggregate, Metric, Report.",
     "See Design 1.25."),
    ("architecture/analytics-recalculation.md", "Analytics Recalculation", "§48-49, Phase 2",
     "How metric definition changes and annotation rule changes propagate into affected "
     "aggregates and facts without rebuilding unaffected analytics.", "See Design 1.25."),
    ("architecture/analytics-storage.md", "Analytics Storage", "§42, Phase 2",
     "Analytics storage as a replaceable implementation detail behind the Analytics Storage "
     "Contract -- ClickHouse is an implementation choice, not an architectural dependency.",
     "See Design 1.25."),
    ("architecture/mcp.md", "MCP", "§58 / §51, Phase 4",
     "MCP as an integration/access interface exposing knowledge search, annotation inspection, "
     "provenance and analytics capabilities -- never a replacement for internal contracts.", None),
    ("architecture/scaling.md", "Scaling", "§70, Phase 6",
     "How ingestion, annotation, search and analytics workloads scale independently, and how "
     "Equalix prevents background maintenance from starving interactive workloads.", None),

    ("analytics/overview.md", "Analytics Overview", "§34, Phase 2",
     "Analytics observes derived platform state; it does not become the authoritative state "
     "of the knowledge platform.", "See Design 1.25."),
    ("analytics/concepts.md", "Analytics Concepts", "Phase 2", "Core analytics vocabulary: event, fact, aggregate, metric, report.", None),
    ("analytics/events.md", "Events", "§35, Phase 2", "Analytics events in the reader-facing Analytics section.", None),
    ("analytics/facts.md", "Facts", "§36-37, Phase 2", "Analytical facts in the reader-facing Analytics section.", None),
    ("analytics/aggregates.md", "Aggregates", "§40, Phase 2", "How aggregates are computed and protected against side-channel disclosure.", None),
    ("analytics/metrics.md", "Metrics", "§43, Phase 2", "Metrics in the reader-facing Analytics section.", None),
    ("analytics/reports.md", "Reports", "§44-45, Phase 2", "Reports in the reader-facing Analytics section.", None),
    ("analytics/dashboards.md", "Dashboards", "Phase 2", "How reports and metrics surface in operational and business dashboards.", None),
    ("analytics/freshness.md", "Freshness", "§46, Phase 2", "Freshness classes -- real-time, near-real-time, hourly, daily -- as part of the metric contract.", None),
    ("analytics/retention.md", "Retention", "§47, Phase 2", "Retention policy by analytical data tier: raw events, facts, aggregates, business metrics.", None),
    ("analytics/security.md", "Security", "§39-41, Phase 2", "Analytics security in the reader-facing Analytics section.", None),
    ("analytics/lineage.md", "Lineage", "§38, Phase 2", "Analytics lineage in the reader-facing Analytics section.", None),
    ("analytics/recalculation.md", "Recalculation", "§48-49, Phase 2", "Analytics recalculation in the reader-facing Analytics section.", None),
    ("analytics/storage.md", "Storage", "§42, Phase 2", "Analytics storage in the reader-facing Analytics section.", None),
    ("analytics/operations.md", "Operations", "§71, Phase 6", "Operating analytics: consumers, retention, partitioning, backups, rebuilds, monitoring.", None),

    ("guides/ingestion/index.md", "Ingestion Guides", "§68, Phase 5",
     "Task guides: ingest a document, ingest audio, connect a source, associate related content.", None),
    ("guides/extraction/index.md", "Extraction Guides", "§68, Phase 5",
     "Task guides: process PDF, process image, process audio, process video.", None),
    ("guides/chunking/index.md", "Chunking Guides", "§68, Phase 5",
     "Task guides: create semantic chunks, configure boundaries, inspect provenance, assign "
     "security classification.", None),
    ("guides/annotations/index.md", "Annotation Guides", "§68, Phase 5",
     "Task guides: create tags/classifications/entities/custom annotations, use dictionaries "
     "and LLMs, define dependencies, inspect provenance.", None),
    ("guides/security/index.md", "Security Guides", "§68, Phase 5",
     "Task guides: configure classifications, group mappings, masking; search masked/unmasked; "
     "test authorization.", None),
    ("guides/search/index.md", "Search Guides", "§68, Phase 5",
     "Task guides: text search, vector search, annotation filtering, security filtering, "
     "hybrid search, relationship-aware search.", None),
    ("guides/recalculation/index.md", "Recalculation Guides", "§68, Phase 5",
     "Task guides: change a rule, inspect impact, create a recalculation, monitor execution, "
     "prioritize workloads.", None),
    ("guides/analytics/index.md", "Analytics Guides", "§68, Phase 5",
     "Task guides: emit an event, define a fact/aggregate/metric/report, query analytics, "
     "configure freshness/retention, inspect lineage, rebuild historical analytics.", None),
    ("guides/integrations/index.md", "Integration Guides", "§69, Phase 4",
     "How-to guides for connecting the Content Extractor, MCP, LLM providers, object storage, "
     "search engines, vector databases, graph databases and analytics storage.", None),
    ("guides/operations/index.md", "Operations Guides", "§70-71, Phase 6",
     "How-to guides for deployment, scaling, monitoring, workload isolation, recalculation and "
     "analytics operations, failure recovery and backup/restore.", None),

    ("integrations/content-extractor.md", "Content Extractor", "§69 / Phase 4",
     "The contract between Synanton and the Content Extractor: structured content in, semantic "
     "elements out -- implementation (parsers, OCR, GPU acceleration) stays behind the contract.",
     "See `content_extractor` repo, `doc/Synanton_v1.21_Structured_content_extraction_plane.md`, "
     "and Design 1.21 (`design/synanton-design-1.21.md`)."),
    ("integrations/mcp.md", "MCP", "§58 / §69, Phase 4",
     "MCP as an integration/access interface for knowledge search, annotation inspection, "
     "provenance and analytics.", None),
    ("integrations/llm-providers.md", "LLM Providers", "§69, Phase 4",
     "LLMs as pluggable annotation providers -- private, on-premises or external -- never a "
     "mandatory architectural dependency.", None),
    ("integrations/object-storage.md", "Object Storage", "§69, Phase 4",
     "The contract for durable source and artifact storage that ingestion commits to before "
     "announcing anything downstream.", None),
    ("integrations/search-engines.md", "Search Engines", "§69, Phase 4",
     "The reverse index / lexical search integration contract.", None),
    ("integrations/vector-databases.md", "Vector Databases", "§69, Phase 4",
     "The vector store integration contract for semantic similarity search.", None),
    ("integrations/graph-databases.md", "Graph Databases", "§69, Phase 4",
     "The graph database integration contract for relationship-aware retrieval.", None),
    ("integrations/analytics-storage.md", "Analytics Storage", "§42 / §69, Phase 4",
     "The Analytics Storage Contract -- the analytical event stream remains the authoritative "
     "replay source regardless of which columnar store implements it.", None),

    ("operations/deployment.md", "Deployment", "§72, Phase 6",
     "SaaS, private cloud, on-premises and hybrid deployment models.", None),
    ("operations/on-premises.md", "On-Premises", "§72, Phase 6",
     "Deploying Synanton entirely within a customer network, including private LLM options.", None),
    ("operations/private-llm.md", "Private LLM", "§65 / §72, Phase 6",
     "Running annotation and enrichment against a private or on-premises LLM instead of an "
     "external provider.", None),
    ("operations/scaling.md", "Scaling", "§70, Phase 6",
     "Scaling ingestion, annotation, search and analytics independently.", None),
    ("operations/monitoring.md", "Monitoring", "§53 / §70, Phase 6",
     "Operational metrics and alerts: consumer lag, event loss, latency, freshness, storage "
     "utilization.", None),
    ("operations/storage.md", "Storage", "§70, Phase 6",
     "Storage operations across content, knowledge projections and analytics.", None),
    ("operations/analytics.md", "Analytics Operations", "§71, Phase 6",
     "Operating the Analytics Plane: retention, partitioning, backups, rebuilds, late/out-of-"
     "order events, schema migrations, workload isolation.", None),
    ("operations/recalculation.md", "Recalculation Operations", "§70, Phase 6",
     "Operating Resolutor/Equalix-driven recalculation: monitoring, prioritization, failure "
     "recovery.", None),
    ("operations/troubleshooting.md", "Troubleshooting", "§70, Phase 6",
     "Operator-facing troubleshooting -- see also the narrative "
     "[Troubleshooting 101](../guides/overviews/troubleshooting-101.md).", None),

    ("reference/content-schema.md", "Content Schema", "§73, Phase 5", "Reference schema for extracted content.", None),
    ("reference/semantic-element-schema.md", "Semantic Element Schema", "§73, Phase 5", "Reference schema for semantic elements.", None),
    ("reference/chunk-schema.md", "Chunk Schema", "§73, Phase 5", "Reference schema for semantic chunks.", None),
    ("reference/annotation-schema.md", "Annotation Schema", "§73, Phase 5", "Reference schema for annotations.", None),
    ("reference/security-policy-schema.md", "Security Policy Schema", "§73, Phase 5", "Reference schema for security policy.", None),
    ("reference/analytics-event-schema.md", "Analytics Event Schema", "§73, Phase 5", "Reference schema for analytics events.", None),
    ("reference/analytical-fact-schema.md", "Analytical Fact Schema", "§73, Phase 5", "Reference schema for analytical facts.", None),
    ("reference/metric-schema.md", "Metric Schema", "§73, Phase 5", "Reference schema for metric definitions.", None),
    ("reference/report-schema.md", "Report Schema", "§73, Phase 5", "Reference schema for report definitions.", None),
    ("reference/search-api.md", "Search API", "§52 / §73, Phase 5", "Customer-facing and internal search API reference.", None),
    ("reference/annotation-api.md", "Annotation API", "§73, Phase 5", "Annotation API reference.", None),
    ("reference/analytics-api.md", "Analytics API", "§52 / §73, Phase 5", "Analytics API reference -- internal vs. customer-facing.", None),
    ("reference/configuration.md", "Configuration", "§73, Phase 5", "Platform configuration reference.", None),
]

STUB_TEMPLATE = """# {title}

!!! info "Content pending"
    This page is part of the site's full navigation skeleton. Full content is scheduled per
    the documentation plan's **{section}** and will follow the standard architecture page
    template (What it is / Why it exists / How it works / Example / Inputs / Outputs /
    Dependencies / Change and recalculation / Security / Lineage / Related concepts).

{description}
{source}
See the [Synanton Documentation Site Plan](https://github.com/synanton/synanton.github.io/blob/main/doc/Synanton%20Documentation%20Site%20Plan.md)
for the full outline this page will follow.
"""


def main():
    created, skipped = 0, 0
    for rel_path, title, section, description, source in STUBS:
        full_path = os.path.join(ROOT, rel_path)
        if os.path.exists(full_path):
            skipped += 1
            continue
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        source_line = f"\n**Go further:** {source}\n" if source else ""
        content = STUB_TEMPLATE.format(
            title=title, section=section, description=description, source=source_line
        )
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        created += 1
    print(f"created={created} skipped(existing)={skipped}")


if __name__ == "__main__":
    main()
