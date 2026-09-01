# Chunk Security

## What it is

Chunk security is the assignment of a security classification to an individual [chunk](chunks.md), rather
than to the whole document it came from.

## Why it exists

A single PDF can contain identity data (RESTRICTED), personal contact information (PERSONAL), and financial
compensation figures (FINANCIAL) in different sections. A document-level or folder-level classification
can't express that — it forces every reader who can see any of the document to see all of it, or none of
it. Chunk-level classification makes sub-document sensitivity expressible and enforceable.

## How it works

```text
Chunk 18291
│
├── content
├── annotations
├── security = CONFIDENTIAL
└── provenance
```

Classification is a normal annotation (`classification.security = CONFIDENTIAL`), produced by deterministic
detectors running over the chunk's structured elements — pattern/regex detectors, gazetteers, or table-header
rules — before the chunk is committed to any store. See [Security Classification](security-classification.md)
for how classification and authorization relate, and [Masking](masking.md) for what happens to the content
itself once a class is detected.

## Example

A compensation table chunk is detected as `FINANCIAL` because its headers match `Salary`, `Gross income`,
`Federal tax`. A chunk of surrounding prose that only says "employees are eligible for the annual bonus
program" — no literal figures — is not classified, or is classified without any content change, because
nothing in it needed masking.

## Inputs

The chunk's content and structured source elements, evaluated by classification detectors.

## Outputs

A `classification[]` value on the chunk, and — depending on whether masking changed the content — one of
three representation outcomes described in [Masking](masking.md).

## Transformations

Detection is deterministic and auditable, not GPU-dependent — the same input always produces the same
classification decision.

## Dependencies

Depends on [chunks](chunks.md) having stable boundaries; a badly-drawn chunk boundary can force an overly
broad classification onto content that didn't need it.

## Change and recalculation

Classification logic changes (a new detector, a changed pattern) require re-running detection over affected
chunks. Per the [change impact model](../architecture/recalculation.md#change-impact-model), this can affect
indexing, projections and analytics, but — critically — **not** authorization: see
[Classify Once, Authorize Dynamically](security-classification.md#classify-once-authorize-dynamically).

## Security

This page *is* the security mechanism for content — see [Security Classification](security-classification.md),
[Masking](masking.md), and [Security-Aware Search](security-aware-search.md) for how classification is
enforced at query time.

## Lineage

Every classification decision is traceable to the detector, its version, and the exact chunk content it was
evaluated against — never applied retroactively without a record of why.

## Related concepts

[Chunks](chunks.md) · [Security Classification](security-classification.md) · [Masking](masking.md) ·
[Security-Aware Search](security-aware-search.md)
