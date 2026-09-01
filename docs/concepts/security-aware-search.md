# Security-Aware Search

## What it is

Security-aware search is the enforcement of [classification](security-classification.md) and
[masking](masking.md) decisions **inside** the search path itself — compiled into the query before
statistics are computed, not applied as a filter on results afterward.

## Why it exists

A post-filter approach — run the query, then strip out results the caller can't see — leaks information
through term statistics, hit counts, and ranking signals even when it never returns the forbidden content
directly: an unauthorized caller can infer a restricted term exists just by watching how it affects
relevance scores. Security-aware search closes that channel by deciding representation *before* the query
runs.

## How it works

```text
Query
│
├── lexical matching
├── semantic similarity
├── annotation filters
├── relationship constraints
└── security authorization
```

At compile time, the query gets both a resource-ACL clause and a **representation clause**, derived from
the caller's class grants:

```text
Before: Must(org_id=acme, space_id=finance)
After:  Must(org_id=acme, space_id=finance, class IN ('FINANCIAL', 'PUBLIC'))
        → representation = ORIGINAL for FINANCIAL-classified chunks, MASKED otherwise
```

For a Dual-representation chunk: an authorized caller's query targets `content_original` /
`embedding_original`; an unauthorized caller's targets `content_masked` / `embedding_masked` — the chunk is
never *excluded*, its masked field is fully searchable, it simply never contains the sensitive literal. This
reaches lexical term statistics, semantic vector candidates, and the ACL pre-filter alike, and applies to
every tenant tier, not only high-security ones.

## Example

An `hr` role searching "gross income" against a Dual-representation `FINANCIAL` chunk gets a hit whose
snippet reads `[REDACTED:FINANCIAL]`. A `payroll` role's identical search on the same chunk gets the actual
figure. Neither query was filtered after the fact — each was compiled to target a different field from the
start.

## Inputs

A query, the caller's authorization context (resource ACL + class grants), and classified/masked chunks
from [knowledge projections](knowledge-projections.md).

## Outputs

Authorized, ranked results where every hit's representation was correct from the moment candidates were
gathered — never corrected afterward.

## Transformations

Query compilation injects representation-aware clauses; highlight snippets render from the representation
actually selected, never falling back to the unauthorized one.

## Dependencies

Depends on [Security Classification](security-classification.md) and [Masking](masking.md) having already
decided each chunk's representation outcome, and on every [knowledge projection](knowledge-projections.md)
having propagated that outcome consistently.

## Change and recalculation

A grant-mapping change affects authorization at the next query with no content recalculation. A
classification or masking policy change requires reprocessing affected chunks — see
[Masking](masking.md#change-and-recalculation).

## Security

Query-side sanitization extends the same principle to suggest/autocomplete, anomaly logging, and execution
traces: none of them may reveal a restricted term or statistic the caller couldn't otherwise see.

## Lineage

Every result remains traceable to its source chunk; representation selection itself is recorded as part of
query execution, not just chunk state.

## Related concepts

[Security Classification](security-classification.md) · [Masking](masking.md) · [Search](search.md) ·
[Search Architecture](../architecture/search-architecture.md)
