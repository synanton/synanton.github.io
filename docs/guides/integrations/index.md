# Integration Guides

Task-oriented steps for connecting Synanton to the systems around it: the Content Extractor, MCP, LLM
providers, object storage, search engines, vector databases, graph databases, and analytics storage.

## At a glance

Every integration in this guide sits behind an explicit [contract](../../concepts/contracts.md) — the
platform specifies what it needs from the integration; the integration specifies how it provides it.
Connecting an integration means satisfying that contract, not adopting a specific vendor as an
architectural dependency. See each integration's own page under [Integrations](../../integrations/content-extractor.md)
for the contract itself; this guide covers the connection steps.

## Connect the Content Extractor

1. Deploy an implementation of `synanton.extraction.v1` — embedded, sidecar, or as an independently scaled
   cluster; deployment topology does not change the contract.
2. Point the platform's extraction client at the deployment.
3. Confirm feature-state reporting: submit a document of each media type you expect and check that
   supported features report `APPLIED`, unsupported ones report `UNSUPPORTED` explicitly, and nothing
   silently degrades without being flagged.
4. Confirm the fallback path: temporarily point the client at an unreachable endpoint and verify ingestion
   falls back to local extraction rather than blocking.

See [Content Extractor integration](../../integrations/content-extractor.md) for the full contract.

## Connect MCP

1. Register the MCP endpoint the platform should expose tools through.
2. Confirm every exposed tool (`query_metric`, `get_report`, knowledge search, and so on) is reachable only
   through the platform's canonical authorization and query pipeline — MCP is an access interface, not a
   parallel path around it.
3. Verify a tool call from an unauthorized MCP client is rejected the same way an unauthorized REST call
   would be.

See [MCP integration](../../integrations/mcp.md) and [Architecture: MCP](../../architecture/mcp.md).

## Connect an LLM provider

1. Register the provider (private, on-premises, or external) as an annotation producer, not as a platform
   dependency — the architecture treats LLMs as pluggable, interchangeable producers behind the
   [annotation definition](../annotations/index.md) contract.
2. For regulated or data-residency-sensitive deployments, confirm the provider satisfies the applicable
   residency and security boundary before routing any content to it — see
   [Private / Regulated AI](../../use-cases/regulated-private-ai.md).
3. Verify producer/producer-version are recorded on every annotation the provider generates, so a later
   model swap is attributable, not silent.

## Connect object storage

1. Register the object store as a `synvault` content adapter.
2. Confirm the durability ordering: content must commit to the store before anything about it is announced
   downstream — this is what makes ingestion crash-safe.
3. Confirm tiering behavior if configured (hot/warm/cold movement) doesn't change content identity or
   break provenance pointers.

## Connect a search engine

1. Register the reverse-index implementation behind the [Reverse Index](../../architecture/reverse-index.md)
   contract.
2. Confirm classified content indexes both representations correctly for Dual-representation chunks —
   `content_masked` always, `content_original` only when policy permits.
3. Run a representative query and confirm term statistics for a restricted literal are never computed for
   an unauthorized caller.

## Connect a vector database

1. Register the vector store behind the [Vector Store](../../architecture/vector-store.md) contract.
2. Confirm original and masked embeddings for a Dual-representation chunk are stored and retrieved as
   isolated entries — never merged, never derivable from one another.
3. Confirm an embedding model change can trigger selective or full vector recalculation without touching
   source content.

## Connect a graph database

1. Register the graph backend behind the [Graph](../../architecture/graph.md) contract.
2. Confirm entities and edges carry `classification` and `representation` metadata, and that traversal
   selects representation the same way search does.
3. Confirm the backend can be swapped (e.g. one graph technology for another) without any change to the
   entities/relationships model above the contract.

## Connect analytics storage

1. Register the analytical store behind the [Analytics Storage Contract](../../architecture/analytics-storage.md).
   ClickHouse is the initial implementation candidate, not a required dependency.
2. Confirm `analytics_events` remains the durable, replayable boundary — derived facts, aggregates, and
   metrics must be rebuildable from it independent of which store implements the contract.
3. See [Analytics Guides → Rebuild historical analytics](../analytics/index.md#rebuild-historical-analytics)
   to verify replay determinism.

## Go deeper

| If you want to know... | Read... |
|---|---|
| Why contracts matter more than implementation language | [Contracts](../../concepts/contracts.md) |
| The polyglot architecture principle | [Polyglot Architecture](../../architecture/polyglot-architecture.md) |
| Each integration's exact contract | [Integrations](../../integrations/content-extractor.md) |
