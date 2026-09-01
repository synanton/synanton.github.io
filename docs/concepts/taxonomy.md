# Taxonomy vs Dependency

## What it is

Taxonomy and dependency are two different relationships that are easy to conflate: taxonomy organizes
*meaning*; dependency describes *derivation*.

## Why it exists

> **Taxonomy describes meaning. Dependency describes derivation.**

It's tempting to assume that because `payment` sits under `billing` sits under `support` in a taxonomy, a
change to `payment` should recalculate everything under `support`. That's wrong, and conflating the two
produces either far too much unnecessary recalculation or missed invalidation. The platform keeps them
explicitly separate.

## How it works

```text
Taxonomy                    Dependency
support                     payment
└── billing                    +
    └── payment              duplicate-charge
                                  │
                                  ▼
                              billing-issue
```

A taxonomy hierarchy is a classification structure a human or a report navigates. A dependency graph is a
computational structure [Resolutor](../architecture/resolutor.md) walks to determine impact. **A taxonomy
hierarchy must not automatically become a processing dependency.**

## Example

`payment` being taxonomically "under" `billing` says nothing about whether a `billing` annotation depends on
`payment` being computed first. `billing-issue` genuinely depends on `payment` and `duplicate-charge` —
that dependency is declared explicitly by the `billing-issue` definition, not inferred from where it sits in
any taxonomy.

## Inputs

A taxonomy is authored/curated directly. A dependency is declared by an
[annotation definition](annotations.md#how-it-works) naming its inputs.

## Outputs

Taxonomy: a navigable classification hierarchy, used for browsing, reporting dimensions, and human
understanding. Dependency: an edge in the [dependency graph](annotation-dependencies.md), used for impact
analysis and recalculation.

## Transformations

Neither transforms the other automatically — that's the entire point of this page.

## Dependencies

Both build on [Annotation Types](annotation-types.md) — specifically the Classification type for
taxonomy membership.

## Change and recalculation

Reorganizing a taxonomy (renaming a category, moving a node) has no recalculation consequence by itself.
Changing a dependency declaration does — see [Annotation Dependencies](annotation-dependencies.md).

## Security

Neither taxonomy nor dependency carries security semantics directly, though a taxonomy category can be
used as a dimension in [aggregate reporting](../analytics/aggregates.md) subject to the same protections as
any other dimension.

## Lineage

Dependency edges are part of an annotation's provenance chain; taxonomy membership is not.

## Related concepts

[Annotations](annotations.md) · [Annotation Dependencies](annotation-dependencies.md) ·
[Ontology](ontology.md) · [Resolutor](../architecture/resolutor.md)
