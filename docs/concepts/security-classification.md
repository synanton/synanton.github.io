# Security Classification

## What it is

Security classification is a normal [classification annotation](annotation-types.md) — `classification.security
= CONFIDENTIAL` — attached to a chunk, distinct from the separate question of who is currently allowed to
see it.

## Why it exists

Enterprises need to say "this content is sensitive" once, durably, and have who-can-see-it be a policy
question evaluated fresh every time, not baked into the content itself. Conflating the two would mean every
reorganization, every role change, forces content to be rewritten.

## How it works

```text
Chunk
 │
 ▼
Security Classification
 │
 ▼
Security Policy
 │
 ▼
User / Group Mapping
 │
 ▼
Search Authorization
```

The security model is a conjunction, not either control independently:

```text
resource_acl ∧ class_grants
```

A user must satisfy both the ordinary resource ACL (do they have access to this space/project/folder?) and
the classification grant (does their role hold a grant for this content's class?).

### Classify once, authorize dynamically

> **Classification is content state. Authorization mapping is policy state.**

If a chunk is `classification = CONFIDENTIAL` and a group later loses its grant for `CONFIDENTIAL`, the
chunk itself is never rewritten:

```text
Group mapping changes
    ↓
No content rewrite
No chunk rewrite
No annotation recalculation
No index rebuild
No graph rebuild
    ↓
New authorization decision at search time
```

Current authorization is evaluated against current policy, at query time — always.

## Example

A payroll table chunk is classified `FINANCIAL` by a deterministic detector matching "Gross income,"
"Federal tax." The `PAYROLL` role holds a `FINANCIAL` grant; the `HR_GENERALIST` role does not. When
`HR_GENERALIST`'s grants change next quarter, nothing about the chunk changes — only the authorization
decision at the next search.

## Inputs

Chunk content and structure, evaluated by classification detectors; a role/group-to-class grant mapping,
maintained independently as policy.

## Outputs

A `classification[]` value on the chunk (content state) and an authorization decision computed per query
(policy state) — never conflated into one value.

## Transformations

Detection (content → classification) is separate from and does not trigger grant evaluation (policy →
authorization); the two meet only at query time.

## Dependencies

Depends on [chunk security](chunk-security.md) detectors producing a classification, and on a policy store
maintaining grants independently.

## Change and recalculation

A classification **logic** change (a new detector) requires re-running detection over affected chunks. A
**grant mapping** change requires no content recalculation at all — only a fresh authorization evaluation
at the next query, per the [change impact model](../architecture/recalculation.md#change-impact-model).

## Security

This page is the security model. See [Masking](masking.md) for what happens to content once classified,
and [Security-Aware Search](security-aware-search.md) for enforcement at query time.

## Lineage

Every classification decision records the detector, its version, and the exact content evaluated — see
[Provenance](provenance.md).

## Related concepts

[Chunk Security](chunk-security.md) · [Masking](masking.md) · [Security-Aware Search](security-aware-search.md) ·
[Annotation Types](annotation-types.md)
