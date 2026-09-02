# Security Guides

Task-oriented steps for configuring classification, masking, and authorization: configuring
classifications, configuring group mappings, configuring masking, searching masked and unmasked content,
and testing authorization.

## At a glance

Security in Synanton is a conjunction, not a single control: `resource_acl ∧ class_grants`. This guide
covers the `class_grants` axis — chunk-level [security classification](../../concepts/security-classification.md)
and [masking](../../concepts/masking.md) — which is what makes sub-document sensitivity possible. Resource
ACLs (space/project/folder access) are configured separately and are not covered here.

## Configure classifications

A classification is a normal [Classification annotation](../annotations/index.md#create-classifications)
whose detector runs deterministically over a chunk's structured elements, before the chunk is committed to
any store.

```yaml
security:
  classification:
    enabled: true
    detectors: [ssn, phone, address, table_header]
    policy:
      RESTRICTED:
        action: MASK
        store_original: false     # never persisted, for anyone
      PERSONAL:
        action: MASK
        store_original: true      # authorized callers may retrieve it
      FINANCIAL:
        action: MASK
        store_original: true
    fail_mode: quarantine          # detector error -> quarantine, not silent pass-through
```

Detectors are deterministic and auditable — the same content always produces the same classification
decision, independent of any model configuration elsewhere in the pipeline.

## Configure group mappings

A group mapping (`class_grants`) decides which roles may access which classifications. It is policy state,
evaluated fresh at query time — changing it never requires rewriting content.

```yaml
class_grants:
  - subject: PAYROLL
    subject_type: ROLE
    class: FINANCIAL
    permission: SEARCH
  - subject: HR_GENERALIST
    subject_type: ROLE
    class: PERSONAL
    permission: SEARCH
```

Because [classification is content state and this mapping is policy state](../../concepts/security-classification.md#how-it-works),
revoking `HR_GENERALIST`'s `PERSONAL` grant here takes effect on the next query — no content rewrite, no
chunk rewrite, no index rebuild.

## Configure masking

Masking decides, per class, whether a caller without a grant sees nothing usable, a masked placeholder, or
— for `store_original: false` classes — nothing at all, ever, for anyone. The masking outcome (Single,
Dual, or Masked-only) is computed automatically from the classification policy above; there is no separate
masking step to configure beyond `action` and `store_original` per class.

To change how a class is masked (for example, moving `PERSONAL` from `store_original: true` to `false`),
update the policy and trigger a `ReindexAfterPolicyChangeWorkflow` — this reprocesses affected chunks
through detection and masking again with the new policy. See
[Change and recalculation](../../concepts/masking.md#change-and-recalculation).

## Search masked content

An unauthorized caller's query automatically targets the masked representation — there is nothing extra to
configure to make this happen; it is the default compile-time behavior described in
[Security-Aware Search](../../concepts/security-aware-search.md). To verify it directly:

1. Issue a search as a role with no grant for the classification in question.
2. Confirm the returned snippet renders `[REDACTED:<CLASS>]` in place of the sensitive span, for a
   Dual-representation chunk.
3. Confirm the search still returns the chunk — masking does not exclude it, it only withholds the literal.

## Search unmasked content

An authorized caller's identical query targets the original representation:

1. Issue the same search as a role holding a grant for the relevant class.
2. Confirm the snippet now renders the actual value.
3. For a `Masked-only` class (e.g. `RESTRICTED`/SSN), confirm that **no** role — including one with the
   grant — can retrieve the original, because it was never computed for storage in the first place.

## Test authorization

Authorization testing should assert both directions explicitly, for every representation outcome:

| Outcome | Unauthorized caller | Authorized caller |
|---|---|---|
| Single | Sees full content | Sees full content (identical) |
| Dual | Sees masked content, non-zero hit | Sees original content |
| Masked-only | Sees masked content | Also sees masked content — no exception |

A negative test that only checks "the literal never appears" is not sufficient on its own — also assert
that the masked field still returns a non-zero, non-degenerate hit, so masking is verified as a
representation choice rather than accidental exclusion.

## Go deeper

| If you want to know... | Read... |
|---|---|
| How Synanton protects sensitive data, end to end | [Security overview](../overviews/security.md) |
| Classification vs. authorization | [Security Classification](../../concepts/security-classification.md) |
| The representation model (Single/Dual/Masked-only) | [Masking](../../concepts/masking.md) |
| The security policy schema | [Security Policy Schema](../../reference/security-policy-schema.md) |
| The normative design | [Design 1.23](../../design/synanton-design-1.23.md) |
