# Annotation Types

## What it is

The five categories of [annotation](annotations.md) the platform recognizes as first-class: Tag,
Classification, Entity, Attribute, and Signal.

## Why it exists

Different kinds of interpretation need different handling downstream — a security classification gates
authorization; a tag drives filtering; an entity feeds the graph. Naming the categories explicitly lets the
rest of the platform (search filters, graph projection, analytics) treat each kind consistently instead of
inventing ad hoc conventions per use case.

## How it works

```text
Annotation
├── Tag            e.g. escalation, urgent
├── Classification e.g. security = CONFIDENTIAL, topic = billing
├── Entity          e.g. Customer "ACME Corp", Product "Model X"
├── Attribute       e.g. confidence = 0.94, language = en
└── Signal          e.g. sentiment = negative, anomaly_score = 0.8
```

- **Tag** — a simple, often boolean, label attached to a chunk.
- **Classification** — a categorical label with defined values, including but not limited to security
  classification (see [Security Classification](security-classification.md)).
- **Entity** — a reference to a real-world object (person, organization, product) that can participate in
  [relationships](relationships.md) and the [graph projection](../architecture/graph.md).
- **Attribute** — a scalar or structured property describing the annotation or its target.
- **Signal** — a derived, often continuous, measure (sentiment, anomaly score, risk score).

## Example

A ticket chunk might carry: `Tag: escalation`, `Classification: topic = billing`, `Entity: Customer =
"ACME Corp"`, `Attribute: language = en`, `Signal: sentiment = negative` — five annotations, five types, one
chunk.

## Inputs

A target ([chunk](chunks.md) or another annotation) plus a definition specifying which type is produced.

## Outputs

A typed [annotation](annotations.md) record, filterable and searchable by type.

## Transformations

None — type is a fixed property of an annotation definition, not something derived after the fact.

## Dependencies

Depends on [Annotations](annotations.md) for the shared identity/provenance model each type uses.

## Change and recalculation

Adding a new annotation type does not require changing existing types. Reclassifying an annotation's type
after the fact is a breaking definition change and requires a new definition version.

## Security

Classification-type annotations carry authorization consequences that other types do not — see
[Security Classification](security-classification.md). Entity and Signal annotations derived from
Masked-only or Dual chunks must respect the same representation the chunk exposes.

## Lineage

Every typed annotation carries the same provenance fields as any other annotation — see
[Provenance](provenance.md).

## Related concepts

[Annotations](annotations.md) · [Security Classification](security-classification.md) ·
[Relationships](relationships.md) · [Taxonomy vs Dependency](taxonomy.md)
