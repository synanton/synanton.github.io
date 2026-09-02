# Security: Classification, Masking, and Authorization

**Audience:** Security officers, architects, compliance teams, developers, and product teams who need to understand how Synanton protects sensitive knowledge.

**Level:** Conceptual to intermediate

**Prerequisites:** None. Detector implementation, storage schemas, and policy internals are covered in deeper architecture documentation.

## At a glance

Synanton separates three questions that are often incorrectly treated as one:

1. **Classification:** What kind of information is this?
2. **Masking:** What representation is safe to store and process?
3. **Authorization:** Which representation may this caller access?

This separation allows Synanton to protect sensitive information without making entire documents inaccessible simply because one part contains sensitive data.

```text
                 Knowledge Chunk
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
    Classification   Masking   Resource access
          │            │            │
          └────────────┼────────────┘
                       ▼
                Authorization
                       │
                       ▼
            Representation selection
                       │
                       ▼
                    Caller
```

The security model operates at the level of semantic content and its representations rather than assuming that an entire document has one uniform sensitivity level.

---

# The problem

Enterprise documents commonly contain information with different sensitivity levels in the same source.

For example, one employee record might contain:

- identity information,
- contact information,
- compensation data,
- public policy text.

Different users may have different rights over those parts.

A document-level permission model has only one basic choice:

```text
Allow document
      or
Deny document
```

That is insufficient when access needs to follow meaningful content boundaries.

Synanton therefore uses the **semantic chunk** as an important unit of security processing.

A chunk is a coherent unit of content that can carry its own classification and participate in representation selection.

---

# Three questions that must remain separate

The core security model is easier to reason about when the three decisions remain independent.

| Question | Mechanism | Meaning |
|---|---|---|
| What kind of information is this? | **Classification** | Describes the sensitivity or category of the content |
| What representation is safe to store? | **Masking** | Determines whether sensitive values may exist in searchable representations |
| Who can access which representation? | **Authorization** | Determines what a particular caller may receive |

These decisions have different lifecycles.

Classification describes the content.

Masking affects what representations can safely exist.

Authorization is evaluated against the caller.

They should therefore not be collapsed into one "permission" property.

---

# Classification

Classification attaches a security category to content.

The current model includes categories such as:

```text
PUBLIC
PERSONAL
FINANCIAL
RESTRICTED
```

The classification describes the content.

It does **not**, by itself, mean that a particular user is allowed or forbidden to see it.

For example:

> `FINANCIAL`

means that the chunk contains financial information.

It does not mean:

> "only payroll can see this."

That second decision belongs to authorization policy.

---

# How classification is determined

Classification can be produced during content processing using deterministic, auditable rules.

Examples include detection of:

- known sensitive identifier patterns;
- validated structured values;
- address patterns;
- financial table structures;
- known classification indicators;
- organization-specific rules.

The important architectural property is that classification is **reviewable and versioned**.

A security reviewer should be able to determine:

- which rule produced the classification;
- which input caused the rule to fire;
- which version of the rule was used.

Classification should not be treated as an unexplained confidence score.

Where automated processing cannot establish a sufficiently reliable classification, the processing workflow may require review rather than silently treating uncertainty as safe.

The exact detector set and implementation are defined in the Security Architecture.

---

# Masking

Classification alone does not prevent a sensitive value from being copied into derived representations.

Consider a salary figure.

Without masking, the value might appear in:

```text
Source-derived text
      │
      ├── Search index
      ├── Vector representation
      ├── Graph fact
      └── Other derived state
```

Masking determines which representation may safely be created and retained.

This distinction is critical:

> **Authorization controls access to an existing representation. Masking controls whether that representation is allowed to exist.**

---

# Three representation outcomes

A security policy can result in three broad representation models.

```text
Sensitive content detected
          │
          ▼
     Masking applied
          │
     ┌────┴────┐
     │         │
unchanged   changed
     │         │
     ▼         ▼
   SINGLE    Policy
              │
       ┌──────┴──────┐
       ▼             ▼
      DUAL       MASKED-ONLY
```

## Single

Masking does not change the relevant representation.

There is one representation.

Example:

> A chunk is classified as `FINANCIAL` because it belongs to a financial section, but the specific sentence contains no sensitive value.

The classification remains useful for policy and audit purposes, but the content itself does not require a separate masked representation.

---

## Dual

Masking changes the content and policy permits the original representation to exist for authorized callers.

Two representations are maintained:

```text
Masked representation
        │
        ├── generally searchable
        │
        ▼
Original representation
        │
        └── authorization required
```

This allows an authorized caller to receive the original value while other callers receive the masked representation.

---

## Masked-only

Masking changes the content and policy prohibits the original representation from being retained in the search platform.

Only the masked representation exists.

This is stronger than authorization.

If the original value is never persisted in the search plane, no search authorization can retrieve it.

For example, a highly restricted identifier may be represented only as:

> `[REDACTED:RESTRICTED]`

The platform cannot grant access to the original through search because the original representation does not exist there.

---

# Default masking policy

The default policy can be expressed conceptually as:

| Classification | Default representation policy |
|---|---|
| `PUBLIC` | No masking required |
| `PERSONAL` | Dual |
| `FINANCIAL` | Dual |
| `RESTRICTED` | Masked-only |

Deployments may define different policy requirements where appropriate.

The important architectural distinction remains:

> **Some sensitive information requires authorization to access; some sensitive information must not exist in a retrievable form at all.**

---

# Authorization

Authorization answers:

> **Who may receive which representation?**

A caller may be:

- a person,
- a group,
- a role,
- a service identity,
- or another identity recognized by the deployment.

Authorization combines resource-level access with classification-based grants.

Conceptually:

```text
Effective visibility
    =
Resource-level access
    AND
Classification authorization
```

A caller therefore needs both:

1. access to the relevant resource;
2. authorization for the relevant classification/representation.

---

# Authorization is evaluated at request time

Authorization is not permanently embedded into stored search results.

The effective policy is resolved when a caller requests information.

This has an important operational consequence:

```text
Grant added
     ↓
Next request uses new grant

Grant revoked
     ↓
Next request uses revoked state
```

Changing a user's authorization does not require rewriting every stored chunk simply because the caller's permissions changed.

The authorization state is policy state, not knowledge state.

---

# Representation selection

A search result is therefore not necessarily a binary:

```text
visible / invisible
```

It may instead be:

```text
same knowledge
      │
      ├── original representation
      │
      └── masked representation
```

The representation returned depends on the caller's effective authorization.

For example:

### Authorized caller

> Gross income: €180,000

### Caller without access to the original financial value

> Gross income: [REDACTED:FINANCIAL]

Both callers can receive a meaningful result without exposing the protected value.

---

# Security-aware search

Security must remain part of search execution.

A naive implementation would do this:

```text
Search everything
      ↓
Rank everything
      ↓
Remove unauthorized results
```

That model can create indirect disclosure.

For example, an unauthorized caller might infer information from:

- result counts;
- ranking statistics;
- autocomplete suggestions;
- highlighted snippets;
- query timing;
- existence of a highly specific match.

The safer architectural model is:

```text
Caller
  │
  ▼
Effective authorization
  │
  ▼
Authorized search space
  │
  ├── lexical retrieval
  ├── semantic retrieval
  └── graph retrieval
          │
          ▼
       Ranking
          │
          ▼
Representation selection
          │
          ▼
        Result
```

The exact compilation and execution mechanism is defined by **Security-Aware Search Architecture**.

---

# Search results can differ by caller

Consider two users searching for:

> "gross income"

The payroll user may receive:

> **Gross income: €180,000**

A caller without authorization for the original financial value may receive:

> **Gross income: [REDACTED:FINANCIAL]**

The second caller has not been given the original value.

At the same time, the system has not unnecessarily hidden the existence of useful business context.

This is one of the main benefits of separating classification, masking, and authorization.

---

# Fail closed

Security-sensitive processing should fail closed.

If required security classification or policy information is unavailable, the system should not assume that the content is safe.

Conceptually:

```text
Security decision available?
       │
   ┌───┴───┐
  yes      no
   │        │
   ▼        ▼
evaluate   restrict
```

This principle applies particularly to:

- missing classification;
- incomplete policy state;
- unavailable authorization data;
- ambiguous security metadata.

The precise behavior of each failure mode belongs in the Security Architecture and operational documentation.

---

# What changes security state?

Different security changes have different consequences.

| Change | Example | Reprocessing normally required? |
|---|---|---|
| Authorization grant | Audit receives `FINANCIAL` access | No |
| Authorization revocation | Payroll access is removed | No |
| Classification rule | New detector identifies a sensitive pattern | Potentially yes |
| Masking policy | A class changes from dual to masked-only | Yes |
| Resource permission | User loses access to a project | Usually no content reprocessing |

The key distinction is between **policy changes** and **knowledge changes**.

A change to who may see existing content does not necessarily require recalculating the content.

A change to what content is classified as sensitive may require reprocessing existing knowledge.

---

# What remains stable?

The following architectural distinctions should remain stable:

```text
Classification
    ≠
Masking
    ≠
Authorization
```

Likewise:

```text
Knowledge state
    ≠
Policy state
```

And:

```text
Canonical content
    ≠
Derived representation
```

Security policy should therefore be able to change without making the knowledge model itself authoritative for access decisions.

---

# Security beyond search

Security-sensitive representations can appear outside the primary result list.

The same security principles must therefore apply to:

### Autocomplete and suggestions

Suggestions must not reveal terms that are known only from unauthorized content.

### Highlighted snippets

Highlights must be generated from the representation actually available to the caller.

A richer internal representation must not leak through presentation logic.

### Query and operational logging

Logs and analytical processing must be treated as potential secondary data surfaces.

Sensitive query content should not automatically become unrestricted operational data.

### Graph representations

Graph facts derived from sensitive content must follow the applicable representation and authorization policy.

### Vector representations

Embeddings and vector indexes are derived representations and must be evaluated as potential information-bearing state rather than assumed to be harmless because they are not human-readable text.

---

# Raw source content

The security model described here governs the Synanton knowledge and search plane.

Raw source documents may have separate storage and access controls.

Therefore:

> **Masked-only in the search plane does not necessarily mean that the original source file has been destroyed.**

It means that the original value is not retained in the retrievable representation governed by this security model.

Organizations that require source-level sanitization must configure and govern that separately.

---

# Security and provenance

Security decisions should remain traceable.

Where applicable, the system should be able to identify:

- the classification;
- the rule or policy that produced it;
- the masking decision;
- the authorization decision;
- the representation selected;
- the relevant policy/version;
- the source or semantic chunk involved.

This allows security behavior to be investigated as a sequence of explicit decisions rather than as an opaque final result.

---

# Example: one document, multiple security outcomes

Consider an employee document:

```text
Employee record
│
├── Identity
│     └── PERSONAL
│
├── Contact information
│     └── PERSONAL
│
├── Compensation
│     └── FINANCIAL
│
└── Public benefits policy
      └── PUBLIC
```

Different callers may therefore receive:

| Content | Employee | HR | Payroll |
|---|---:|---:|---:|
| Public policy | ✓ | ✓ | ✓ |
| Contact information | — | ✓ | according to policy |
| Compensation | — | according to policy | ✓ |
| Restricted identifiers | masked/restricted according to policy | masked/restricted according to policy | masked/restricted according to policy |

The important point is that security follows the **meaningful content units**, not simply the enclosing file.

---

# Frequently asked questions

### Is classification the same as authorization?

No.

Classification describes the content. Authorization determines whether a caller may receive a particular representation.

### Is masking the same as authorization?

No.

Masking determines whether a representation is safe to store or process. Authorization controls access to representations that are permitted to exist.

### Does masked-only mean that the original data is deleted?

Not necessarily.

It means the original is not retained in the search-plane representation governed by this model. Raw source storage is a separate security boundary.

### Does revoking access require reprocessing documents?

Normally no.

Authorization is evaluated against current policy rather than baked into stored knowledge.

### Can one chunk have multiple classifications?

Yes.

A chunk may contain more than one category of sensitive information. The applicable masking and authorization policy must account for all relevant classifications.

### Is this the same as DLP?

No.

There is overlap in purpose, but the architectural role is different. DLP systems commonly detect sensitive information in data flows or stores. Synanton incorporates classification and representation decisions into knowledge processing so that derived searchable state can be created in an appropriate representation from the beginning.

### What happens if security metadata is missing?

The security model should fail closed rather than assume unrestricted access.

The precise operational behavior is defined by the deployment's security contract.

---

# Go deeper

| Question | Read |
|---|---|
| What is security classification conceptually? | **Concepts → Security Classification** |
| How is masking represented? | **Concepts → Masking** |
| How does security-aware search work? | **Concepts → Security-Aware Search** |
| How are security decisions implemented? | **Architecture → Security** |
| How is authorization incorporated into search? | **Architecture → Security-Aware Search** |
| How are classification changes recalculated? | **Architecture → Recalculation** |
| What is the exact security policy contract? | **Reference → Security Policy Schema** |
| What are the current design decisions? | **Design 1.23 / Design 1.24** |
---

## Summary

Synanton's security model is based on a deliberate separation:

> **Classification describes the content.**

> **Masking determines which representations may exist.**

> **Authorization determines which representation a caller may receive.**

This separation allows sensitive knowledge to remain useful without treating an entire document as uniformly sensitive.

It also makes security policy changes independently manageable:

- authorization can change without reprocessing knowledge;
- classification changes can trigger targeted recalculation;
- masking policy changes can change derived representations;
- search can evaluate access as part of retrieval rather than relying solely on post-filtering;
- and security decisions can remain traceable through their policies, classifications, and representations.

The result is a security model aligned with Synanton's broader architecture: **explicit, composable, traceable, and recalculable.**