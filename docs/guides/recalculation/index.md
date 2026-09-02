# Recalculation Guides

Task-oriented steps for the recalculation workflow defined in
[Design 1.25](../../design/synanton-design-1.25.md): changing a rule, inspecting impact, creating a
recalculation, monitoring execution, and prioritizing workloads.

## At a glance

Recalculation always follows the same two-stage model: [Resolutor](../../architecture/resolutor.md)
determines *what* needs to change, and [Equalix](../../architecture/equalix.md) determines *how* that
change is executed safely. This guide walks through that workflow from the point a rule changes to the
point updated knowledge is available.

!!! note "Design status"
    This guide describes the recalculation model as defined in the approved Design 1.25 architecture.
    Recalculation tooling is at an early implementation phase — see
    [Design 1.25 §90](../../design/synanton-design-1.25.md#90-implementation-phases) for phase status
    before assuming a specific command-line or API surface is already available in your deployment.

## Change a rule

Changing an [annotation definition](../annotations/index.md) — publishing a new `producer_version`, a new
detection pattern, a new dependency — never mutates the existing definition. It registers a new version:

```yaml
definition_id: payment-detection
version: 4        # was 3
producer: payment-rule-engine
producer_version: 4.2
```

The old version's annotations remain queryable for comparison (`payment-detection v3` vs. `v4`) unless
governance explicitly requires invalidation.

## Inspect impact

Before executing a recalculation, Resolutor computes the impact set: every downstream object that
declared a dependency on the changed definition, transitively.

```text
payment-detection v3 → v4
        ↓
  Resolutor
        ↓
Affected: payment annotations, billing-issue annotations (dependent),
          escalation-required annotations (dependent),
          reverse index entries, vector entries, graph edges, analytics facts
```

Inspecting the impact set before executing lets an operator confirm the blast radius matches expectation —
a rule change that unexpectedly touches millions of chunks is worth catching before execution, not after.

## Create a recalculation

A recalculation plan targets exactly the objects Resolutor identified — never "recalculate everything, to
be safe." Equalix then schedules the plan's execution as one of several concurrent workload classes:

```text
Incremental ingestion
Interactive processing
User-triggered recalculation
Background recalculation
```

## Monitor execution

A recalculation runs as one or more [processing runs](../../concepts/provenance.md#how-it-works), each
identifying its producer, version, input scope, timing, status, and any errors. Monitor:

- affected-object count vs. the impact set computed during inspection (should match);
- processing duration and failure rate;
- whether dependent recalculations (e.g. `billing-issue` following `payment`) have started.

## Prioritize workloads

> **Background maintenance must not starve incremental and interactive workloads.**

Equalix applies priority, concurrency, resource, and retry policies across workload classes so that a
large historical recalculation cannot delay time-sensitive ingestion or interactive search. Where a
recalculation is not urgent, prefer scheduling it as background work rather than requesting interactive
priority.

## Go deeper

| If you want to know... | Read... |
|---|---|
| What Resolutor and Equalix are responsible for | [Resolutor](../../architecture/resolutor.md) · [Equalix](../../architecture/equalix.md) |
| The full change-impact matrix | [Recalculation](../../architecture/recalculation.md) |
| How annotation dependencies form the graph Resolutor walks | [Annotation Dependencies](../../concepts/annotation-dependencies.md) |
| The normative design and implementation phases | [Design 1.25](../../design/synanton-design-1.25.md) §48–§55, §90 |
