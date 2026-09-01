# Masking

## What it is

Masking is the decision about which *representation* of classified content may be exposed — separate from
classification, which only decides how sensitive the content is.

## Why it exists

```text
Classification → how sensitive is this content?
Masking        → how is sensitive content represented?
Authorization  → who may access which representation?
```

Knowing a chunk is `FINANCIAL` doesn't by itself say whether an unauthorized reader sees nothing, a masked
placeholder, or the literal value. Masking is the mechanism that decides — and, critically, decides it once
at ingest time, not per query.

## How it works

Every chunk resolves to exactly one of three representation outcomes:

```text
detector match
      │
      ▼
apply masking policy → masked_content
      │
      ▼
masked_content == original_content ?
      │                    │
     yes                   no
      │                    │
      ▼                    ▼
   SINGLE              store_original for
 representation         the matched class?
(everyone gets it)      │             │
                       true          false
                        │              │
                        ▼              ▼
                     DUAL          MASKED-ONLY
              representation      (no original ever
              (original gated      stored, for anyone)
               by class grants)
```

| Outcome | When | What's stored | Who gets what |
|---|---|---|---|
| **Single** | Masking makes no change | One `content` field | Everyone with resource access |
| **Dual** | Masking changes content, class permits storing the original | `content_masked` (always) + `content_original` (grant-gated) | Authorized callers get original; everyone else gets masked |
| **Masked-only** | Masking changes content, class forbids storing the original (e.g. SSN/`RESTRICTED`) | Only `content_masked` — the original is never computed for storage | Everyone, including class-authorized callers |

Masked-only is a hard guarantee: the sensitive literal is never written to any store, for anyone, at any
tier of access — not briefly, not in an intermediate cache, not ever.

## Example

`"Salary: €180,000"` → `"Salary: [REDACTED:FINANCIAL]"` is a Dual outcome: both forms exist, and
representation selection at query time decides which one a given caller sees. `"SSN: 000-00-0000"` →
`"SSN: [REDACTED:SSN]"` with `store_original: false` is Masked-only: `"000-00-0000"` is never computed for
storage, so there is no "original" for even a fully-authorized caller to retrieve.

## Inputs

A chunk's [classification](security-classification.md) and its per-class masking policy (`action: MASK`,
`store_original: true|false`).

## Outputs

One of Single, Dual, or Masked-only representation, propagated consistently into every
[knowledge projection](knowledge-projections.md) — index, vector store, and graph.

## Transformations

Masking happens once, before any store commit — never recomputed per query, never reconstructed from a
masked value.

## Dependencies

Depends on [security classification](security-classification.md) having run first. Every projection and
every downstream annotation must respect whichever outcome was decided.

## Change and recalculation

Changing a masking policy (e.g. flipping `store_original` for a class) requires reprocessing affected
chunks through a `ReindexAfterPolicyChangeWorkflow` — re-detect, re-mask, re-index — per the
[change impact model](../architecture/recalculation.md#change-impact-model).

## Security

This is the mechanism that makes [Security-Aware Search](security-aware-search.md) trustworthy: because the
representation decision is made once at ingest, there is no query-time code path that can accidentally
compute or expose an original value that was never stored.

## Lineage

Every representation decision — which outcome, which policy version — is recorded as part of the chunk's
[provenance](provenance.md).

## Related concepts

[Security Classification](security-classification.md) · [Security-Aware Search](security-aware-search.md) ·
[Chunk Security](chunk-security.md) · [Knowledge Projections](knowledge-projections.md)
