# Annotation Guides

Task-oriented steps for producing structured interpretation over content: creating tags, classifications,
entities, and custom annotations; using dictionaries and LLMs; creating derived annotations; defining
dependencies; and inspecting provenance.

## At a glance

Design 1.25 defines annotations as first-class, versioned knowledge, independent of the mechanism that
produces them — a rule, a dictionary, an ML model, an LLM, or a human reviewer all publish through the same
[annotation definition](../../concepts/annotations.md) contract. This guide walks through defining that
contract for each of the five [annotation types](../../concepts/annotation-types.md).

## Create tags

A tag is the simplest annotation type — a label attached to a chunk with no further structure.

```yaml
definition_id: escalation-tag
version: 1
inputs:
  - chunk_text
producer: rule-engine
producer_version: 1.0
output:
  type: annotation
  annotation_type: Tag
  name: escalation
```

Once published, every chunk matching the rule's condition carries `Tag: escalation`, filterable in
[search](../search/index.md).

## Create classifications

A classification is a categorical annotation with defined values — security classification
(`classification.security = CONFIDENTIAL`) is one instance of this type, but any categorical dimension
(`topic = billing`) uses the same shape. See [Security Guides](../security/index.md) for the
security-specific classification workflow, which additionally interacts with masking and authorization.

```yaml
definition_id: topic-classification
version: 2
inputs:
  - chunk_text
producer: topic-classifier-model
producer_version: 2.1
output:
  type: annotation
  annotation_type: Classification
  name: topic
  allowed_values: [billing, technical, account, other]
```

## Create entities

An entity annotation references a real-world object — a customer, a product, a ticket — that can
participate in [relationships](../../concepts/relationships.md) and the [graph projection](../../architecture/graph.md).
Entity types must come from the platform's governed [ontology](../../concepts/ontology.md); an undeclared
entity type is rejected rather than silently accepted, to keep the graph from fragmenting into incompatible
vocabularies.

```yaml
definition_id: customer-entity-extraction
version: 1
inputs:
  - chunk_text
producer: entity-extraction-model
producer_version: 1.4
output:
  type: annotation
  annotation_type: Entity
  entity_type: Customer   # must exist in the ontology
```

## Create custom annotations

Attribute and Signal annotations cover everything that isn't a tag, a classification, or an entity —
scalar properties (`language = en`) and derived, often continuous measures (`sentiment = negative`,
`anomaly_score = 0.8`). Define them the same way, choosing the annotation type that matches what the value
represents:

```yaml
definition_id: sentiment-signal
version: 1
inputs:
  - chunk_text
producer: sentiment-model
producer_version: 3.0
output:
  type: annotation
  annotation_type: Signal
  name: sentiment
  value_type: categorical    # negative | neutral | positive
```

## Use dictionaries

A dictionary-backed definition matches chunk content against a curated term list rather than a model.
Dictionaries are versioned like any other producer input — a dictionary update is a `producer_version` bump,
not a silent behavior change, so historical annotations remain attributable to the dictionary version that
produced them.

## Use LLMs

An LLM-backed definition names the model and its version as the producer, exactly like any other producer.
Where enrichment uses a two-pass structure — an analysis pass, then a generation pass — each pass's output
should be recorded with its own provenance, so a low-confidence or contested annotation can be traced to
the specific pass and prompt version that produced it, not just "the LLM."

## Create derived annotations

A derived annotation depends on one or more other annotations rather than on raw chunk content directly.
Declare the dependency explicitly in the definition's `inputs`:

```yaml
definition_id: billing-issue
version: 1
inputs:
  - payment          # another annotation type, not raw content
  - duplicate-charge
producer: annotation-engine
producer_version: 4.2
output:
  type: annotation
  annotation_type: Classification
  name: billing-issue
```

## Define dependencies

Dependencies are declared, not inferred — a definition's `inputs` list *is* the dependency declaration.
[Resolutor](../../architecture/resolutor.md) builds the [dependency graph](../../concepts/annotation-dependencies.md)
from these declarations and rejects any declaration that would introduce a cycle
(`A → B → C → A`) at registration time, before it ever reaches production.

## Inspect provenance

Every annotation answers "why does this exist?" through its recorded producer, producer version,
definition, definition version, confidence, and processing run. To inspect it:

1. Retrieve the annotation by its `annotation_id`.
2. Read `processing_run_id` to see the execution context — configuration, input scope, timing — that
   produced it.
3. Follow declared dependencies to their own annotations for a derived annotation, recursively, until
   reaching annotations produced directly from chunk content.

See [Provenance](../../concepts/provenance.md) for the full lineage chain this participates in.

## Go deeper

| If you want to know... | Read... |
|---|---|
| The distinction between extraction and annotation | [Annotations](../../concepts/annotations.md) |
| Taxonomy vs. dependency | [Taxonomy vs Dependency](../../concepts/taxonomy.md) |
| How a definition change triggers recalculation | [Recalculation Guides](../recalculation/index.md) |
| The annotation schema and API | [Annotation Schema](../../reference/annotation-schema.md) · [Annotation API](../../reference/annotation-api.md) |
| The underlying architecture design | [Design 1.25](../../design/synanton-design-1.25.md) §6–§14 |
