# Annotation Dependencies

## What it is

An annotation dependency is an explicit record that one annotation's derivation relies on another —
allowing knowledge to be built compositionally, and allowing the platform to know exactly what becomes
stale when an input changes.

## Why it exists

Some interpretations are cheap to detect directly (a payment reference matches a pattern). Others are only
meaningful as a *combination* of simpler ones (a "billing issue" is a payment annotation plus a
duplicate-charge signal). Without explicit dependency tracking, the platform would have no way to know that
changing the payment detector should also invalidate every `billing-issue` annotation derived from it.

## How it works

```text
payment
  +
duplicate-charge
    ↓
billing-issue
    ↓
escalation-required
```

Dependencies form a **directed acyclic graph**: `A → B → C` is valid, `A → B → C → A` is rejected outright.
Each [annotation definition](annotations.md#how-it-works) declares its inputs, so the platform can build the
full [dependency graph](../architecture/annotation-dependencies.md) and answer "what depends on this?" for
any node.

## Example

Changing the `payment-detection` rule from v3 to v4 marks every `payment` annotation it produced as
affected. Because `billing-issue` declared a dependency on `payment`, [Resolutor](../architecture/resolutor.md)
also marks every `billing-issue` (and, transitively, every `escalation-required`) derived from an affected
`payment` annotation — without touching annotations that never depended on it.

## Inputs

Annotation definitions that declare which other annotation types or definitions they consume as input.

## Outputs

A dependency edge in the platform's [dependency graph](../architecture/annotation-dependencies.md), used by
[Resolutor](../architecture/resolutor.md) for impact analysis.

## Transformations

None — a dependency is a declared relationship, not something that gets computed independently of the
definitions that declare it.

## Dependencies

Depends on [annotation definitions](annotations.md) naming their inputs explicitly. Circular declarations
are rejected at registration time, not discovered later during recalculation.

## Change and recalculation

This is the mechanism that makes [dependency-aware recalculation](../architecture/recalculation.md) possible
at all: a change to one definition only recalculates the definitions that declared a dependency on it,
never the whole knowledge base.

## Security

Dependency tracking has no security implications of its own, but a derived annotation must never expose
information from an input it wasn't authorized to see — see [Security-Aware Search](security-aware-search.md).

## Lineage

Every derived annotation's dependency edges are part of its [provenance](provenance.md) — "why does this
annotation exist" includes "which other annotations it was derived from."

## Related concepts

[Annotations](annotations.md) · [Taxonomy vs Dependency](taxonomy.md) · [Provenance](provenance.md) ·
[Resolutor](../architecture/resolutor.md) · [Recalculation](../architecture/recalculation.md)
