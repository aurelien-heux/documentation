# Architecture knowledge base — design notes

Notes from the working sessions of 2026-10-22 and 2026-10-23 on the Devtoolbox architecture knowledge base:
from intent to code, TOGAF building blocks, detailed design, ARB reviews, the AIToolbox design system and the
agentic, chatbot-driven direction. Decisions are numbered DEC-KB-*; open items are listed at the end.

The working example that implements these notes is `ea-example.zip` (building blocks in LikeC4, DD in Markdown,
validator, generator, Architecture page, ArchiMate notation and the `@aitoolbox/architecture` Angular library).

---

## 1. Tool choice

### Context

The team wanted a web alternative to Sparx Enterprise Architect and Archi: the same data and visualisation, readable
by agents, navigable in a web page, inside the AIToolbox toolbox. Sparx was judged costly, not modern, and a second
tool to work in.

### Candidates reviewed

| Tool | Fit | Verdict |
|---|---|---|
| LikeC4 (MIT) | Architecture as code: a DSL, custom element kinds and nesting, generated views, static site, VS Code, MCP server for agents | Chosen for building blocks and views |
| ArchiPulse (Apache-2.0) | Self-hosted web platform storing ArchiMate Open Exchange in PostgreSQL, Archi-compatible | Option if Archi interoperability became a requirement; young project |
| Arkidor | Free browser ArchiMate editor, exchange-format compatible | Editing only, not embeddable |
| Essential Project | Data-driven EA repository with a TOGAF mapping | Heavier; EA governance rather than developer-facing |
| Sparx EA | Full ArchiMate / UML / BPMN, `.qea` SQLite, Pro Cloud Server | Replaced; may remain an optional export target |

"Compatibility" between Archi, Sparx and ArchiPulse means file exchange through the ArchiMate Model Exchange File Format
(elements, relationships, properties, views survive; tool-specific extras do not), not live synchronisation. The team
does not care about the format: the goal is the same data, a visual navigable page, and agent readability.

### DEC-KB-01 — Architecture as files in Git, no EA tool as source of truth

Building blocks in LikeC4, text in Markdown, validated in CI, projected into pages and indexes. Sparx becomes at most
an export. Rationale: one working surface (repository, portal, Assistant), agent-native, no licence.

---

## 2. Model structure: what lives where

| Content | Format | Location | Why |
|---|---|---|---|
| Motivation (stakeholders, drivers, goals, outcomes, principles) | LikeC4 | `model/bb/*.c4` | Graph facts with ArchiMate types |
| Requirements and constraints (the elements) | LikeC4 | `model/bb/*.c4` | Traced by ABB through `realization` |
| Requirement details: acceptance rows, decision table, operational figures | Markdown + YAML frontmatter | `model/requirement/<id>.md` | Each row becomes a test |
| ABB, SBB | LikeC4 | `model/bb/*.c4` | ArchiMate kinds; realization chain |
| Plateaus, work packages, gaps, implementation events | LikeC4 | `model/bb/*.c4` | Implementation & migration layer |
| Detailed design (DD), one file per hexagonal layer per module, UML in Mermaid | Markdown | `model/dd/*.md` | Text, optionally graph; `realizes` SBB ids |
| Notes on a building block (state machines, sequences) | Markdown | `model/notes/<id>.md` | Narrative that does not fit a description |
| Architecture decisions | Markdown (MADR) | `model/adr/*.md` | Immutable once accepted; `domainRef` to DEC-* |
| ARB submission: reviewers, conditions, ASD narrative | Markdown | `model/arb/*.md` | Review object |
| Contracts | OpenAPI / AsyncAPI | `contracts/` | Referenced by `contract` metadata |

Rules:

- **Every fact once.** A relationship or a status lives in the model; reasoning lives in a Markdown body. Nothing in prose
  duplicates a fact.
- **Ids** `<folder>.<applicationSlug>.<name>` (`mot`, `req`, `abb`, `sbb`, `imp`); folders are ArchiMate Groupings. Ids are
  immutable; titles may change. The id is the join key across LikeC4, Markdown, page anchors, Git paths and the index.
- **Vocabulary** follows the domain reference §5: `application` = applicationSlug, `module` = applicationSlug/moduleName,
  `workItemId` = CTX-ORC Work item; ArchiMate names stay in `kind`, prose says Module and Work item (DEC-07).
- **Status** (`#draft #ready #done #deprecated`) changes only through a Checkpoint decision (INV-12); an agent never changes
  it in a file.
- **Plateaus** are tags on every ABB/SBB (`#baseline #transition-1 #target`); change tags (`#new #changed #retired`) describe
  baseline → target; gaps between any two plateaus are computed from membership, never typed.
- **Traceability** uses ArchiMate relationships: SBB `-[realization]->` ABB `-[realization]->` requirement; a work package
  `-[realization]->` what it delivers and `-[association]-> … 'retires'` what it removes.

### Frontmatter schema (Markdown side)

`ea-schema.json`: JSON Schema per file plus per-level required keys (`levelRequires`), the DD kinds (`domain`,
`domain-events`, `ports`, `application`, `infrastructure`, `api`, `data-model`), statuses, ARB statuses, the ASD sections,
and `kindMapping` — the Design-to-Code table (ArchiMate kind or DD kind → what it becomes in the DD → Java hexagonal
package → test type) as data, so skills and the page read it instead of a prose table.

### DEC-KB-02 — Sparx-era vocabulary is mapped, not adopted

"Application Component" and "work package" remain ArchiMate kinds in the model; prose, prompts and the page use Module
and Work item. The Definition of Ready and the review are Checkpoints; reading an external model is a Capability through
a CTX-INT connector, never a direct file read by an agent (INV-07).

---

## 3. Validation and ARB readiness

`tools/validate.py` reads the building blocks through `likec4 export json`, the Markdown through the schema, and runs
checks in five groups. Blocking checks fail the pull request; warnings go to the board.

| Group | Checks |
|---|---|
| Structure | S1 frontmatter matches the schema · S2 references resolve · S3 DD realizes SBB only |
| Traceability | T1 new/changed ABB realizes a requirement · T2 new/changed application SBB realizes an ABB · T3 technology SBB serves another SBB (warning) · T4 every requirement realized · T5 acceptance + operational figures · T6 new/changed application SBB has a DD (warning) |
| Plateaus & gaps | P1 every ABB/SBB in a plateau · P2 change tags agree with plateau membership · P3 every gap item addressed by a work package (warning) · P4 plateaus chained (warning) |
| Ownership & contracts | O1 owner on new/changed blocks · O2 contract file exists for interfaces and events · O3 Work item on new/changed SBB and ready DD |
| Decisions | D1 referenced ADR exists · D2 new application component covered by an ADR (warning) · D3 accepted ADR names its domainRef |

**ARB readiness** per submission: the scope is the gap between `from` and `to` plateaus plus its DD and requirements;
the checks run on that scope; the written ASD sections are measured (complete / thin / missing); reviewer decisions and
open conditions are counted. Readiness = Blocked (a blocking check fails or a required section is missing), Needs
attention (warnings, a pending reviewer, a change request, an open condition) or Ready for the board.

**ASD** (Architecture Solution Design): 13 sections, 6 written in the submission file (context and scope, business
need, architecture overview, non-functional requirements, security, risks) and 7 assembled from the model (requirements,
baseline, target, gap and transition, detailed design, decisions, open questions). Exportable as Markdown.

**Decisions** are recorded by reviewers (Approve, Approve with conditions, Request changes) as Checkpoint decisions
(CMD-DECIDE-CHECKPOINT); approval is unavailable while blocking checks fail.

---

## 4. Views and the page

- **LikeC4 views** are generated from the model: landscape per plateau, gap per pair of plateaus (unchanged faded,
  changed dotted, retired dashed and faded), roadmap, chain (Requirement → ABB → SBB of the target), motivation, and one
  view per element (chain up plus neighbours).
- **The Architecture page** (AIToolbox shell: top app bar, drawer / rail / navigation bar by window class) has four tabs:
  Landscape (plateaus, gap with its table and the delivering work package, roadmap), Building blocks, Elements (table
  with type tile, plateau track, change, status), Reviews (ARB list, readiness, ASD, checks, decision).
- **Real LikeC4 inside the page**: `likec4 codegen webcomponent` is inlined; the page injects the AIToolbox skin into
  the component's shadow root and keeps its colour scheme in step with the page theme. The standalone LikeC4 site is
  also built (single file, hash routing) with the same skin.
- LikeC4 1.41 limits: no `style … where`, so gap views style explicit element lists; every type is a rectangle with its
  glyph (ArchiMate figure shapes are CSS only); the skin depends on `data-likec4-color` and Mantine variables.

---

## 5. ArchiMate notation and components in the design system

All 62 ArchiMate 3.2 element types offered by Archi and the 11 relationships, as a design-system notation:

- **Layer colours** (light / dark) are content colours, never status. Measured contrast on every fill: text ≥ 10:1,
  ink (border, glyph) ≥ 6.4:1.
- **Shapes by aspect and figure**: active structure square, behaviour rounded, business/data object header band with the
  divider below the glyph, contract two lines, representation and deliverable wavy bottom, artifact folded corner,
  product tab, motivation cut corners, value ellipse, grouping dashed, junctions dots.
- **Glyphs**: one 24 px icon per type, drawn in currentColor. Drawn for this system; to be reviewed against the standard.
- **Components** (`design-system/archimate/components.md`, project doc `claude/aitoolbox-architecture-components.md`):
  ArchiMate figure (sizes S/M/L; default, clickable, selected, retired), type tile, change chip, plateau track,
  relationship line; readiness chip, check row, ASD section header, reviewer decision.
- **Angular library** `@aitoolbox/architecture` (`angular/architecture`): standalone components on Angular 21/22 with
  the `atb` prefix (`atb-ax-figure`, `atb-check-row`, `AtbDecision`…), `--md-sys-color-*` roles only, theme switch
  `html.light` / `html.dark`, `--ax-*` layer tokens delivered as `tokens.ax.json` (W3C Design Tokens, dark in
  `$extensions`), an M2 Sass bridge for pages without `tokens.css`, `AxIconRegistry` for `mat-icon svgIcon="ax:<type>"`,
  an SVG sprite, 17 Jest specs, Storybook stories. `tokens-bridge.css` exists only for pages that do not load
  `tokens.css`; never in the app.

### DEC-KB-03 — Prefix `atb`

Every selector, class, CSS variable and TypeScript name uses the AIToolbox trigram `atb`.

---

## 6. Delta against a Sparx-based TOGAF practice (light, agentic version)

Already covered: building blocks with ArchiMate types, requirements with acceptance tests, traceability, plateaus and
gaps, work packages, ADRs, ARB readiness and decisions, the ASD, Git review, MCP for agents, design-system components.

| # | Capability | Light, agentic version | Effort |
|---|---|---|---|
| 1 | Portfolio | One `model/bb/<app>.c4` per application, cross-application relationships, enterprise landscape | S |
| 2 | Catalogs and matrices | Generated from `bb.json` (application, interface, technology catalogs; capability map; application × capability; data CRUD) | S |
| 3 | Queries and impact | MCP tools: neighbours, path to requirement, blast radius, filters | M |
| 4 | Lifecycle and roadmap | Lifecycle dates on SBB and technology, radar, time slider, obsolescence alerts from the Catalog | M |
| 5 | Drift between model and reality | Reconciliation agents against CTX-CAT, descriptors, ArgoCD; findings as PRs | M |
| 6 | Agent proposals with evidence | Architect role proposing ABB/SBB/DD from a requirement, with `source` and `evidence` | M |
| 7 | Versioning and baselines | Git history; model diff between tags shown as a gap table | S |
| 8 | Principles and compliance | Principles with machine-checkable rules, shown as checks | M |
| 9 | Risk and cost | Metadata aggregated per application and plateau | S |
| 10 | Governance records | Dispensations and waivers with expiry; decision log | S |
| 11 | Standards and patterns | Pattern catalog as LikeC4 fragments; allowed technology list checked by rule | M |
| 12 | Data architecture | Classification, ownership, data flows | S |
| 13 | Stakeholder viewpoints | A few generated views per audience | S |
| 14 | Collaboration | "Propose a change" through the Assistant, opening the PR | S |
| 15 | Diagram editing | Non-goal: automatic layout, edits through text or the Assistant | — |

Dropped or minimal: manual layout, UML beyond DD files, MDG technologies and code generation from the model, simulation,
document templates beyond the ASD.

### Reviewed for a chatbot-driven knowledge base

Items 2, 3, 7, 9, 12, 13 and 14 become questions the chatbot answers from the knowledge base through tools, not pages.
The page keeps what people must see and decide (landscape, gap, ARB flow, portfolio). New items because it is a chatbot:

| # | Capability | Effort |
|---|---|---|
| A | Retrieval that respects structure: one document per element and per Markdown section, ids as metadata, graph tools for traversal | M |
| B | Evidence in every answer: ids, paths, page links; inference stated as such (INV-13) | S |
| C | Scope and freshness: plateau, commit and date in every answer; stale and draft flagged | S |
| D | Validation as a conversation: readiness, failing checks and fixes, from the existing checks | S |
| E | Write path through proposals: diff → `validate.py` → PR on approval; status never changed | M |
| F | Reconciliation on demand and on schedule | M |
| G | Glossary from the domain reference §5, with synonyms | S |
| H | Conversation memory tied to elements | S |
| I | Evaluation set of questions with expected ids, run on every model change | S |

Suggested order: A, B, C → the impact and traceability tools plus D → I → E and F → portfolio.

---

## 7. Documentation format for a graph / RAG knowledge base

### DEC-KB-04 — Two authoring formats, one generated index

- **Author** graph facts in LikeC4 and narrative in Markdown with frontmatter: one file per element, one topic per
  heading (headings are the chunk boundary, sections under ~300 words, bullets and tables over paragraphs), section 5
  vocabulary only, no fact carried only by a diagram.
- **Generate** the index (never hand-written):
  1. one document per node in a fixed layout — identity line (id, name, type, layer, level), metadata line, one-sentence
     description, relationships written as sentences with the related element's name, pointers (source path, page
     anchor, commit, date);
  2. one document per Markdown section, prefixed with its element context; tables kept as Markdown, Mermaid kept as source
     with a caption;
  3. the graph itself (`bb.json`) behind MCP tools: find (hybrid vector + keyword), get, neighbours,
     path_to_requirement, impact, diff.
- **Why**: vector search finds the entry node; keyword search catches ids and paths; graph traversal answers
  multi-hop questions exactly; fixed layouts let the model cite id and path; metadata filters narrow by plateau, level,
  application, status, owner.
- Also indexed: views (title, description, included ids) and the glossary (one document per term with synonyms).
- Not needed: a separate ontology or RDF store (the LikeC4 kinds and ArchiMate relationships are the schema) or a graph
  database (hundreds to a few thousand nodes fit in memory, in sync with Git).

### DEC-KB-05 — Detailed design in three tiers

| Tier | Content | Format | Maintained by |
|---|---|---|---|
| 1 Design intent | Boundaries, responsibilities, invariants, main use-case flow, local decisions | Markdown, one file per layer per module, 1–3 pages | Humans and agents, reviewed |
| 2 Contracts and schemas | OpenAPI, AsyncAPI, Liquibase, JSON Schema, state machines | Native formats in the repository | Their own tools |
| 3 Code structure | Packages, classes, ports, adapters, dependencies | Extracted on each build (Spring Modulith, ArchUnit, jdeps) | Generated |

Tier 1 links to tiers 2 and 3 by path (`contracts`, `schemas`, `code` frontmatter keys) and never restates them; no field,
endpoint or column tables in tier 1. Tier 2 is indexed per operation, message or table with the parent SBB id; tier 3
goes into the graph under the SBB, not into the text index. The validator checks the paths; the reconciliation agent
checks that tier 3 agrees with tier 1.

### DEC-KB-06 — Reverse documentation with provenance

Order: extract tier 3 deterministically → index tier 2 → derive SBB candidates deterministically (the Design-to-Code
table backwards: module → application-component, OpenAPI → application-interface, AsyncAPI channel → application-event,
aggregate or schema → data-object, runtime dependency → system-software, external client → technology-service) → agent
writes tier 1 DD with evidence → agent proposes ABB and requirements from ports, tests, tickets and ADRs (lower
confidence) → everything tagged `#baseline`, gaps empty until a target exists.

Provenance metadata on every element and DD file: `origin` (extracted | inferred | authored | reconciled), `evidence`
(paths), `confidence` (for inferred), `extractedAt`. The page shows the origin; the chatbot states it; the validator
refuses `#ready` on an `inferred` element until an architect authors it through a Checkpoint.

Reliability: modules, dependencies, endpoints, messages, tables and runtime are reliable; use cases, domain objects and
events are partly reliable; requirements, goals, capabilities, plateaus, owners and decisions need people.

Tier 3 stays out of the LikeC4 views by default (SBB and above); the chatbot drills into classes on request. After the
first reverse pass, reconciliation keeps the model true: a new endpoint without an SBB or an SBB without code becomes a
proposal.

---

## 8. Pipeline

```
tools/build_notation.py   notation_data.py → design-system/archimate/* , model/bb/_archimate.spec.c4, angular/architecture generated files
likec4 validate model/bb
tools/validate.py         → dist/bb.json, dist/validation.json (checks + ARB readiness)
tools/generate.py         → dist/likec4/ (project + views.generated.c4), dist/model.json, dist/index.html
tools/build_likec4.py     → dist/likec4-site/index.html, <likec4-view> embedded in dist/index.html
likec4 mcp dist/likec4    the same model for agents
```

---

## 9. Open items

- Design review of the 62 glyphs and the layer palette against the ArchiMate standard and the brand.
- Feature mark for Architecture (a proposal exists; the official mark belongs in `feature-marks/`).
- Angular 22 compilation of the library (built on 21; peer range allows 22).
- Storybook packages not installed in the example (stories are CSF 3).
- Second application in the example to show the portfolio and catalogs.
- `export_rag.py` (node and section documents, glossary), the MCP query tools and the evaluation set.
- Reverse pipeline shape: deterministic mapping from Spring Modulith / OpenAPI / Liquibase outputs, `origin` and
  `evidence` metadata with the validator rule, a fixture to run end to end.
- Placeholder reviewer names in the ARB example.
