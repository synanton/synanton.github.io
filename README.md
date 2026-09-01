# synanton.github.io

Source for the main Synanton documentation site, published at [synanton.github.io](https://synanton.github.io/).

This is the architecture-and-knowledge-guide-first umbrella site described in
[`doc/Synanton Documentation Site Plan.md`](doc/Synanton%20Documentation%20Site%20Plan.md): Introduction →
Concepts → Use Cases → Architecture → Analytics → Guides/Integrations → Reference/Design. It is deliberately
broader than any single repository's README - it explains how the Synanton platform, Content Extractor,
GPU Runtime, Equalix, Commitix and Lucentrix projects fit together, and links out to each repository's own
engineering documentation for implementation depth.

Bilingual: English (`en`, authoritative) and Russian (`ru`), via `mkdocs-static-i18n` suffix files
(`page.md` = English, `page.ru.md` = Russian).

## Local development

```bash
uv venv --python 3.12 --seed
source .venv/bin/activate
uv pip install -r requirements.txt
mkdocs serve            # http://127.0.0.1:8000, live-reloads on edit
```

Validate strictly before pushing (broken internal links/nav fail the build):

```bash
mkdocs build --strict
```

## Structure

```text
docs/
├── index.md                 Home
├── getting-started/         Overview, quickstart, "how data flows through Synanton"
├── concepts/                Architecture-first explainers, no implementation detail
├── use-cases/                Same primitives, told through enterprise scenarios
├── architecture/            Deep architecture pages (What/Why/How/Inputs/Outputs/Security/Recalculation)
├── analytics/               The Analytics Plane as its own reader-facing section
├── guides/
│   ├── overviews/           Long-form "101" explainers (moved from platform/docs-site)
│   ├── ingestion/ extraction/ chunking/ annotations/ security/ search/
│   ├── recalculation/ analytics/ integrations/ operations/   Task-oriented how-tos
├── integrations/            Contract-first integration docs (Content Extractor, MCP, LLM providers, ...)
├── operations/              Deployment, scaling, monitoring, troubleshooting
├── reference/               Schemas and APIs, generated/maintained from contracts
└── design/                  Historical design documents (synanton-design-1.19 … 1.25), for traceability
```

## Content status

Pages fully written follow the plan's Phase 1 priority (architecture foundation: content model, extraction,
chunking, annotations, security, search, recalculation, contracts, polyglot architecture) in both languages.
Pages outside that phase exist as short stubs - a one-paragraph description, the plan section they come
from, and links to the source design documents in [`design/`](docs/design/) or the relevant repository - so
the full navigation and information architecture are in place ahead of the content. See the plan's §82
("V1 Documentation Priority") for the phase order stub pages will be filled in.

## Relationship to other repositories

This site explains *how the projects fit together*; it does not duplicate any repository's own
documentation. Implementation-level detail - protobuf/gRPC contracts, module internals, ADRs - stays in:

- [`synanton/platform`](https://github.com/synanton/platform) - the platform engineering repo (`docs/architecture/`, `docs/api/`, `docs/book/`)
- `content_extractor` - structured content extraction plane implementation
- `gpu-runtime` - GPU execution plane implementation
- `equalix` - recalculation/execution control implementation
- `commitix`, `lucentrix` - supporting platform services

## Design documents

Historical design proposals (`docs/design/synanton-design-1.19.md` … `1.25.md`) are copied here from
`synanton/platform`'s `docs/architecture/` for architectural traceability, per the plan's §74. They are
**not** re-synced automatically - treat `synanton/platform` as the source of truth and refresh the copies
here when a new design revision is approved.
