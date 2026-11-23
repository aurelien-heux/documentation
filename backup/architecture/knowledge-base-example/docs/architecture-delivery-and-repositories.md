---
title: Architecture knowledge base — delivery, repositories and CI/CD
status: draft
date: 2026-10-26
relates-to: architecture-knowledge-base-notes.md (DEC-KB-01..06)
---

# Architecture knowledge base — delivery, repositories and CI/CD

This document follows `architecture-knowledge-base-notes.md`. It covers how the model reaches people (Angular feature,
Zensical doc sites, chatbot), where each kind of data is stored, how repositories are organised for about 30
Applications in 4 Portfolios, and the CI/CD that ties them together.

## Decisions at a glance

| ID | Decision |
|---|---|
| DEC-KB-07 | The model stays in Git. Each build is published once to object storage, keyed by commit. Postgres holds only the review workflow and the version list. |
| DEC-KB-08 | Interactive work (ARB, checks, views, edits) is an Angular feature. Reading documentation is Zensical. No iframe between them, only deep links. |
| DEC-KB-09 | One central architecture repository holds the model for all levels: enterprise, portfolio and Application. Detailed design, contracts and code structure stay in the Application repositories. |
| DEC-KB-10 | Application repositories publish design fragments. The central build combines them through a lock file that is bumped automatically. |
| DEC-KB-11 | The four groups of Applications are called **Portfolio** (attribute of Application in CTX-CAT), not "domain", which already means a DDD domain. |
| DEC-KB-12 | Every change, from a person, an agent or an ARB decision, reaches the model as a pull request. The web page never writes the model directly. |

---

## 1. Where the data lives (DEC-KB-07)

| Data | Store | Why |
|---|---|---|
| Model: `.c4`, requirements, ADRs, ARB records | **Git**, central architecture repository | Single source of truth (DEC-KB-01). Changes reviewed as pull requests; agents read plain files. |
| Detailed design (tier 1), contracts (tier 2) | **Git**, each Application repository, next to the code | Updated in the same pull request as the code it describes; tier-3 extraction needs the code. |
| Published build: `bb.json`, `model.json`, `validation.json`, LikeC4 bundle, Mermaid SVGs, RAG documents | **Object storage**, one immutable folder per commit, plus aliases (`main`, tags, `pr-<n>`) | Cacheable, reproducible; a pull-request build is a shareable preview of a proposed change. |
| Version list, ARB workflow (submission, reviewers, conditions, comments, decisions in progress) | **Postgres**, Devtoolbox backend | Changes in seconds, tied to users. A reviewer decision is a Checkpoint (INV-12). |
| Search and chatbot content | **CTX-KI** Chunks with Provenance | Ingested on the publish event, like every other Source. |

Two rules keep Git complete:

- **Final ARB decisions are written back to Git.** When the Checkpoint is decided, the backend asks CTX-INT to open an
  auto-merge pull request that updates the ARB record (status, decision, conditions, decidedAt). CTX-INT holds the
  credentials (INV-07); the pattern is the same as Environment descriptors (INV-ENV-01).
- **The web page never writes the model** (DEC-KB-12). "Edit", "Generate DD" and "Fix finding" open a pull request
  (a human edit, or an agent's Artifact) that goes through a Checkpoint.

Not needed: relational tables as the master copy of elements (they would drift from Git), or a graph database (about
3,000 nodes fit in memory).

The CI output is a **Package** in the domain vocabulary, not an Artifact.

---

## 2. Angular integration

### 2.1 Feature route

```ts
export const ARCHITECTURE_ROUTES: Routes = [{
  path: 'architecture',
  loadComponent: () => import('./architecture-shell.component').then(m => m.ArchitectureShellComponent),
  children: [
    { path: '', loadComponent: () => import('./enterprise.page') },                 // capability map
    { path: 'p/:portfolio', loadComponent: () => import('./portfolio.page') },     // portfolio landscape, roadmap
    { path: 'a/:app', loadComponent: () => import('./application.page') },         // application views
    { path: 'e/:id', loadComponent: () => import('./element.page') },              // any element by id
    { path: 'reviews/:arbId', loadComponent: () => import('./arb.page') },         // ARB / ASD
  ],
}];
```

`?ref=main|<tag>|pr-<n>` selects the build, so any version, including a pull-request preview, is a shareable link.

### 2.2 Data access with signals

```ts
@Injectable({ providedIn: 'root' })
export class ArchitectureStore {
  readonly ref = signal('main');
  private base = computed(() => `/api/architecture/${this.ref()}`);

  readonly model = httpResource<ArchModel>(() => `${this.base()}/model.json`);
  readonly validation = httpResource<ArchValidation>(() => `${this.base()}/validation.json`);
  readonly byId = computed(() => new Map(this.model.value()?.elements.map(e => [e.id, e]) ?? []));
}
```

Gaps, checks and ARB readiness are computed once, in the pipeline (`validate.py`). The client filters and displays.
For the enterprise level the backend also serves slices (`/api/architecture/{ref}/portfolios/{p}/model.json`) so a
page loads only what it shows.

### 2.3 LikeC4 views as a web component

```ts
@Component({
  selector: 'atb-likec4-view',
  standalone: true,
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  template: `<likec4-view [attr.view-id]="viewId()" browser></likec4-view>`,
})
export class AtbLikeC4ViewComponent {
  readonly viewId = input.required<string>();
  readonly bundleUrl = input.required<string>();
  constructor() { effect(() => loadScriptOnce(this.bundleUrl())); } // then inject ATB_LC4_SKIN into the shadow root
}
```

- The bundle comes from `likec4 codegen webcomponent`. It is loaded only on the feature route.
- The AIToolbox skin (`aitoolbox-likec4.css`, `ATB_LC4_SKIN`) is injected into the shadow root and follows
  `html.dark` / `html.light`.
- A custom element name can be registered once per page. To switch versions without a reload, generate each bundle
  with its own element prefix (check the codegen prefix option), or reload when `ref` changes.

### 2.4 Detailed design content

- Markdown is rendered at build time and bound with `[innerHTML]` (Angular's default sanitiser stays on).
- Mermaid diagrams are pre-rendered SVGs shown as `<img>`, light or dark source chosen from a theme signal. No
  `bypassSecurityTrust*`.

### 2.5 Theme and components

Load `archimate.css` and `tokens-bridge.css` once in the feature. The `@aitoolbox/architecture` UI Components
(figure, tile, change chip, plateau track, relationship line, readiness chip, decision chip, check row, ASD section)
already follow the theme classes.

### 2.6 Actions

Each action calls the backend, which opens a pull request or creates a Checkpoint and returns its link. The page shows
"Pending review" until the next published build contains the change.

---

## 3. Angular feature, iframe or Zensical (DEC-KB-08)

Use both Angular and Zensical, each for what it does best. Don't embed one in the other.

| | Angular feature | Zensical doc site |
|---|---|---|
| Best for | ARB/ASD preparation, checks, baseline/target views, reviewer decisions, edit and generate actions, version switching | Reading DD, ADRs, requirements and notes as pages, alongside the Application's other docs |
| Why | Needs users, state, the API and the AIToolbox UI Components | Static, versioned with the Doc Site, already ingested by CTX-KI (EVT-DOCSITE-PUBLISHED); renders Markdown and Mermaid natively |
| Can't do | — | Workflow or user state: a static site cannot record a decision |

Why not an iframe:

- two navigation bars, two searches and two scroll areas;
- the theme switch does not reach the frame without `postMessage` code;
- the back button, deep links and chatbot links break;
- the frame height has to be managed by hand, and it is awkward on phones;
- focus and screen-reader order break at the frame boundary;
- the frame needs extra cookie and CSP setup;
- AIToolbox UI Components can't run inside it, so it fails the design-system Quality gate.

An iframe is acceptable only as a temporary step, for example the current static page until the feature exists.

In practice:

- The same build publishes the JSON and LikeC4 bundle for Angular, and Markdown pages into each Application's
  Zensical site under an "Architecture" section.
- Each Zensical page links to "Open in Architecture" (`/architecture/e/{id}`); each element panel in Angular links to
  "Read the design" on the Doc Site.
- The LikeC4 web component can also be placed on a Zensical page as a read-only diagram.

---

## 4. Repository structure

### 4.1 Three options

| | A · Federated | B · Fully centralized | C · Central model, distributed design |
|---|---|---|---|
| Model (ABB, SBB, requirements, plateaus, ARB) | in each Application repository, plus a landscape repository for higher levels | central repository | **central repository** |
| Detailed design, contracts | Application repositories | central repository | **Application repositories** |
| Cross-Application change | one PR per repository + lock bump | one PR | one PR in the central repository |
| DD updated with the code | yes | no: a second PR in another repository | **yes** |
| Tier-3 extraction | in each build | central build must clone 30 repositories | **in each Application build** |
| Lock files | Application models and DD | none | **DD fragments only, auto-bumped** |
| One place for the ARB, agents and RAG over the model | partly | yes | **yes** |
| Who edits SBBs | Application teams in their repository | architects and teams in the central repository | **architects and teams in the central repository (or through the page)** |
| Closest to the former Sparx repository | no | yes | **yes, for the model** |

**Recommendation: C.** The ARB, portfolio roadmaps and the chatbot all work on the model, and the model is
cross-Application by nature, so it is easiest to govern, validate and query in one place. Detailed design changes with
the code, so it stays next to the code. This also replaces the central Sparx repository without asking 30 teams to
maintain building blocks in their own repositories on day one.

Move towards A later, for a given Application, only if its team wants to own its SBBs in its own repository and the
central pull-request flow becomes a bottleneck. The ids and the published layout are the same in both, so the switch is
a move of files, not a migration.

**Why not B:** detailed design kept away from the code drifts; nothing forces a DD update in the pull request that
changes the code; tier-3 extraction would need every repository cloned centrally; contracts would be copied.

### 4.2 Layout (option C)

```
architecture-repository/                     central · architects and Application leads
├─ enterprise/
│  ├─ motivation/          drivers, goals, principles (mot.*)
│  ├─ capabilities/        one capability map for the organisation (cap.*)
│  ├─ standards/           technology standards, shared platforms (std.*)
│  ├─ adr/                 enterprise ADRs
│  └─ views.c4
├─ portfolios/
│  ├─ delivery-platform/
│  │  ├─ portfolio.c4      value streams, portfolio ABBs, plateaus, work packages (roadmap)
│  │  ├─ requirement/      cross-Application requirements
│  │  ├─ arb/              ARB submissions and records
│  │  ├─ adr/
│  │  └─ views.c4
│  └─ <portfolio-2>/  <portfolio-3>/  <portfolio-4>/
├─ applications/
│  ├─ environments/
│  │  ├─ app.c4            Application ABBs and SBBs (front end and back end included), app-level gaps
│  │  ├─ requirement/
│  │  └─ adr/              Application architecture decisions
│  └─ … 29 more
├─ design.lock.json        applicationSlug → module → published fragment sha
├─ atb-arch.json           { "toolchain": "2.3.0" }
└─ CODEOWNERS

<application repository>/                    × 30 or more (several per Application when Modules are split)
├─ src/ …
├─ contracts/              OpenAPI, AsyncAPI (the provider owns the contract)
└─ architecture/
   ├─ dd/                  tier-1 DD, one file per layer per Module
   ├─ atb-arch.json        { "applicationSlug": "environments", "module": "backend" }
   └─ Makefile             lint · validate · generate (targets from the toolchain)

atb-architecture-toolchain/                  platform team · released with semver
├─ schema/ea-schema.json
├─ notation/               ArchiMate spec, icons, CSS
├─ tools/                  validate, generate, export_rag, reverse/
├─ likec4/                 AIToolbox skin
├─ jenkins/vars/           atbDesign, atbArchitecture
├─ image/                  atb-arch-builder
├─ skills/                 agent skills: write DD, prepare ASD, reverse document
└─ angular/                publishes @aitoolbox/architecture
```

`CODEOWNERS` in the central repository:

```
/enterprise/                         @ea-team
/portfolios/delivery-platform/       @dp-architects
/applications/environments/          @environments-leads @dp-architects
/design.lock.json                    @atb-arch-bot
```

### 4.3 What goes where

| Content | Level | Location | Owner |
|---|---|---|---|
| Drivers, goals, principles, capability map, standards | Enterprise | central `enterprise/` | Enterprise architects |
| Value streams, cross-Application ABBs, roadmap (plateaus, work packages), ARB | Portfolio | central `portfolios/<p>/` | Portfolio architect |
| Application ABBs, SBBs, requirements, architecture ADRs | Application | central `applications/<app>/` | Application leads, portfolio architect reviews |
| Detailed design, local design decisions | Module | Application repository `architecture/dd/` | Application team |
| Contracts | Module (provider) | Application repository `contracts/` | Application team |
| Code structure (tier 3) | Module | extracted by the Application build, never written by hand | — |
| Schema, validator, notation, pipeline, skills, UI Components | Toolchain | toolchain repository | Platform team |

Content lives at the lowest level that owns it; higher levels reference it. A portfolio ABB is realised by Application
SBBs; an Application requirement traces to a portfolio or enterprise goal.

### 4.4 Applications split across several repositories

An Application with a front-end repository and a back-end repository has **one model** (`applications/<app>/app.c4`)
and **one `architecture/dd/` per repository**:

```
environments-back/architecture/dd/     dd.environments.domain, .application, .infrastructure, .api …
environments-back/contracts/           deployments.openapi.yaml, environment-events.asyncapi.yaml …
environments-front/architecture/dd/    dd.environments.frontend-structure, .frontend-state, .frontend-api-client
```

- The front end is one SBB in `app.c4` (`application-component`, `module 'environments/frontend'`).
- The front-end DD names the operations it consumes, for example
  `consumes: environments/backend:deployments.openapi.yaml#createDeployment`, and never copies the contract.
- Each repository publishes its own fragment; the central build combines them by `applicationSlug` and `module`.
- A third Module repository (a worker, say) follows the same pattern: `dd/`, `atb-arch.json`, one more lock entry.

This settles OPP-ENV-08 for architecture purposes.

### 4.5 Identifiers

Ids do not contain the Portfolio, so an Application can move between Portfolios without renaming anything:

| Element | Id pattern |
|---|---|
| Enterprise motivation, capability, standard | `mot.ent.<name>`, `cap.<name>`, `std.<name>` |
| Portfolio ABB, plateau, work package, ARB | `abb.<portfolio>.<name>`, `imp.<portfolio>.<plateau>`, `arb.<portfolio>.<year>-<n>` |
| Application ABB, SBB, requirement | `abb.<applicationSlug>.<name>`, `sbb.<applicationSlug>.<name>`, `req.<applicationSlug>.<name>` |
| Detailed design | `dd.<applicationSlug>.<layer>` |

CTX-CAT maps each Application to its Portfolio; the build reads the Portfolio from there. The validator checks that
every `applicationSlug` exists in the catalog.

### 4.6 Editing the model without leaving the Application

Application teams don't need to clone the central repository for routine changes:

- the Architecture page opens the central pull request for them ("Edit", "Add SBB");
- agent skills (write DD, propose SBB from a new endpoint) open the same pull requests;
- the reconciliation job (§5.8) proposes SBB changes when code and model disagree.

---

## 5. CI/CD (DEC-KB-10)

### 5.1 Overview

```
 Application repository (src/, contracts/, architecture/dd/)        central architecture repository
        │ PR / merge                                                   │ PR / merge
        ▼                                                              ▼
 ┌──── Jenkins: atbDesign() ─────────────────┐            ┌──── Jenkins: atbArchitecture() ──────────────┐
 │ lint → extract code → validate against    │            │ lint → fetch locked fragments → validate all │
 │ central main → render → publish fragment  │            │ → generate → diff → publish → notify         │
 └──────────┬───────────────────────┬────────┘            └─────────┬───────────────┬────────────────────┘
            │                       │                               │               │
            ▼                       ▼                               ▼               ▼
  fragments/{app}/{module}/{sha}/   lock-bump PR ──auto-merge──▶ design.lock.json   PR comment
                                                                    │
                                    central/{sha}/  (+ aliases) ◀───┘
                                          │
                                          ├─ EVT-ARCHITECTURE-PUBLISHED ─▶ CTX-ARC (versions, ARB readiness)
                                          │                               CTX-KI  (ingest node documents)
                                          ├─ Zensical pages ─▶ each Application's Doc Site
                                          └─ Angular /architecture?ref=…  (served by the backend)
```

### 5.2 Triggers

| Event | Build | Publishes | Moves aliases |
|---|---|---|---|
| PR in an Application repository | `atbDesign` | `fragments/{app}/{module}/{sha}/` | `pr-<n>` for that fragment |
| Merge to `main` in an Application repository | `atbDesign` | fragment | fragment `main`; opens the lock-bump PR |
| Lock-bump PR (bot) | `atbArchitecture` | `central/{sha}/` preview | `pr-<n>` |
| Lock-bump PR green | auto-merge | — | — |
| PR in the central repository | `atbArchitecture` | `central/{sha}/` preview | `pr-<n>` |
| Merge to `main` in the central repository (incl. lock bump, ARB decision) | `atbArchitecture` | `central/{sha}/` | `main` |
| Tag `arch-v*` in the central repository | promotion of the `main` build | — | tag alias, `release` |
| Nightly | reconciliation | report and proposal PRs | — |

The lock bump is merged automatically when the central build is green: the DD was already reviewed in its own
repository. A red bump stays open and notifies the Application team and the portfolio architect: their DD now
contradicts the model.

### 5.3 Builder image

`atb-arch-builder:<version>`, pinned by digest, rebuilt monthly: Python 3.12, Node 22, `likec4@1.41.0`,
`@mermaid-js/mermaid-cli` with Chromium, Spectral (OpenAPI lint), the AsyncAPI CLI, Zensical. Lockfiles are inside the
image; builds download nothing.

### 5.4 Application pipeline (`atbDesign`)

| # | Stage | What it does | Fails the build when |
|---|---|---|---|
| 1 | Lint | DD frontmatter against `ea-schema.json`; `spectral lint` and `asyncapi validate` on contracts | schema or contract error |
| 2 | Extract code (tier 3) | Reuses the application build output: Spring Modulith documenter, ArchUnit, jdeps → `code-structure.json` | extraction crashes (findings are only reported) |
| 3 | Validate against the model | Loads `central/main/bb.json` (or `ARCH_BASE_REF`); checks that each `realizes` id exists, consumed operations exist in the provider's published contracts, and every new SBB of this Module has a DD | an error-severity check fails |
| 4 | Render | Markdown → HTML; Mermaid → SVG light and dark (cached by file hash); RAG section documents | renderer error |
| 5 | Publish | `fragments/{app}/{module}/{sha}/` with `manifest.json` written last | upload error |
| 6 | Lock bump (main only) | Bot opens or updates the lock-bump PR in the central repository | never (retried) |

### 5.5 Central pipeline (`atbArchitecture`)

| # | Stage | What it does | Fails the build when |
|---|---|---|---|
| 1 | Lint | Frontmatter against the schema; `likec4 validate` on the whole workspace | schema or DSL error |
| 2 | Fetch fragments | Downloads each fragment in `design.lock.json` (DD, contracts index, code structure) | a locked fragment is missing |
| 3 | Validate | `validate.py` over the full model and fragments: S, T, P, O, D checks plus cross-Application checks X (targets exist, one owner per shared ABB, plateaus aligned across Applications) | an error-severity check fails |
| 4 | Generate (parallel) | `model.json` and slices per enterprise / portfolio / Application; views; `likec4 build` and `codegen webcomponent`; RAG node documents; Zensical pages | generator error |
| 5 | Diff | Against the base `main` build: added, changed, retired elements; new gaps; affected ARBs | never (reports only) |
| 6 | Publish | `central/{sha}/`, manifest last, then aliases | upload error |
| 7 | Notify | `EVT-ARCHITECTURE-PUBLISHED`, PR comment | never (retried) |

Warnings (such as T6) don't block. They appear in the PR comment and count in ARB readiness.

### 5.6 Jenkins shared library

Application repository:

```groovy
@Library('atb-pipeline@v1') _
atbDesign()            // reads architecture/atb-arch.json for applicationSlug and module
```

Central repository:

```groovy
@Library('atb-pipeline@v1') _
atbArchitecture()
```

`vars/atbArchitecture.groovy` (abridged):

```groovy
def call(Map cfg = [:]) {
  pipeline {
    agent { kubernetes { inheritFrom 'atb-arch-builder' } }
    options { timeout(time: 30, unit: 'MINUTES'); disableConcurrentBuilds(abortPrevious: true) }
    environment { LIKEC4 = 'likec4'; DIST = 'dist' }
    stages {
      stage('Lint')      { steps { container('arch') { sh 'make lint' } } }
      stage('Fragments') { steps { container('arch') { sh 'make fetch-fragments LOCK=design.lock.json' } } }
      stage('Validate')  { steps { container('arch') { sh 'make validate' } }
                           post  { always { archiveArtifacts "${DIST}/validation.json" } } }
      stage('Generate')  { parallel {
          stage('Model')  { steps { container('arch') { sh 'make model slices' } } }
          stage('Views')  { steps { container('arch') { sh 'make likec4' } } }
          stage('Pages')  { steps { container('arch') { sh 'make svg zensical' } } }
          stage('RAG')    { steps { container('arch') { sh 'make rag' } } }
      } }
      stage('Diff')      { steps { container('arch') { sh "make diff BASE=${atbBaseSha()}" } } }
      stage('Publish')   { steps { atbArchPublish(scope: 'central', sha: env.GIT_COMMIT, alias: atbAlias()) } }
    }
    post { always { atbArchNotify(scope: 'central', sha: env.GIT_COMMIT) } }
  }
}
```

The Makefile targets come from the toolchain, so `make validate` gives the same result on a laptop and in CI.

### 5.7 Storage layout and manifest

```
architecture-builds/                    bucket · write: CI service account · read: Devtoolbox backend only
├─ central/
│  ├─ 4a1b9e0/                          immutable, one folder per commit
│  │  ├─ manifest.json                  written last = build complete
│  │  ├─ bb.json · model.json · validation.json · diff.json
│  │  ├─ slices/enterprise/ · slices/portfolios/<p>/ · slices/applications/<app>/
│  │  ├─ likec4/index.html · likec4/webcomponent.<hash>.js
│  │  ├─ svg/…{light,dark}.svg
│  │  └─ rag/nodes.jsonl · rag/sections.jsonl
│  └─ _aliases.json                     {"main":"4a1b9e0","arch-v3":"71de0c4","pr-88":"c0ffee1"}
└─ fragments/
   └─ environments/
      ├─ backend/9f3c2ab/               dd/, svg/, contracts index, code-structure.json, manifest.json
      └─ frontend/a41c9d2/
```

```json
{
  "scope": "central",
  "commitSha": "4a1b9e0",
  "ref": "main",
  "builtAt": "2026-10-26T08:41:12Z",
  "toolchain": { "image": "atb-arch-builder:2026.10", "likec4": "1.41.0", "schema": "ea-schema@3" },
  "fragments": { "environments/backend": "9f3c2ab", "environments/frontend": "a41c9d2" },
  "validation": { "passed": 18, "warnings": 1, "errors": 0 },
  "files": { "model.json": "sha256:…", "likec4/webcomponent.3be1.js": "sha256:…" }
}
```

- **Idempotent:** the same commit always writes the same path; the event is deduplicated by `(scope, sha)`.
- **Atomic:** a build is visible only once `manifest.json` exists; aliases move after the manifest.
- **Retention:** `pr-*` 30 days after the PR closes, `main` 90 days, tagged builds forever. Fragments referenced by
  a kept central build are kept with it.

### 5.8 Event, consumers and reconciliation

```json
{
  "type": "EVT-ARCHITECTURE-PUBLISHED",
  "id": "central@4a1b9e0",
  "scope": "central",
  "commitSha": "4a1b9e0",
  "ref": "main",
  "manifestUrl": "s3://architecture-builds/central/4a1b9e0/manifest.json",
  "validation": { "errors": 0, "warnings": 1 },
  "changed": ["sbb.environments.reservation-api", "imp.delivery-platform.target"]
}
```

| Consumer | Does |
|---|---|
| CTX-ARC (Architecture backend) | Records the version (`arch_version`); for each open ARB whose scope intersects `changed`, recomputes readiness and marks it "updated since review". |
| CTX-KI | Ingests `rag/*.jsonl` as Chunks with Provenance (`source=architecture`, `applicationSlug`, `version=sha`, `url`); on `main` replaces the previous version. |
| Angular | Nothing to receive. It reads `/api/architecture/{ref}/…`; the backend resolves aliases and serves from storage with `Cache-Control: immutable`. |

Nightly reconciliation rebuilds every Application's tier 3 with the current extractor, compares it with the model and
the DD, and opens proposal pull requests (a new endpoint without an SBB, an SBB without code). It never changes the
model by itself.

### 5.9 ARB decision loop

```
Architect      Angular /reviews      CTX-ARC          CTX-ORC         CTX-INT Git      Jenkins
   │ submit ARB ──▶│ POST /arb ────────▶│ readiness ok?  │                │               │
   │               │                   │ create Checkpoint ─────▶│        │               │
Reviewers ─ decide ─────────────────────────────────────▶│ decided         │               │
   │               │                   │◀── EVT-CHECKPOINT-DECIDED         │               │
   │               │                   │ decision → arb record ──────────▶│ auto-merge PR │
   │               │                   │                                  │ ─ merge ────▶ │ build
   │               │◀─────────── EVT-ARCHITECTURE-PUBLISHED ─────────────────────────────── │
   │               │ status: Approved with conditions (recorded in Git, sha 4a1b9e0)         │
```

- The decision exists in Postgres as soon as the Checkpoint is decided; Git holds the final record once merged, and
  the page shows "Recorded in Git" with the sha.
- The auto-merge pull request changes only `portfolios/*/arb/*.md` frontmatter (`status`, `decision`, `conditions`,
  `decidedAt`). Branch protection lets the bot merge only when that is the only path changed and CI is green.
- Credentials stay in CTX-INT (INV-07); Jenkins never holds the auto-merge credentials.

### 5.10 Cross-repository changes

A new screen calling a new endpoint touches three places: the central model (new SBB), the back end (contract, DD,
code) and the front end (DD, code). Order:

1. Central PR adds the SBB (and the gap, if it belongs to a plateau). Its preview build is `central pr-<n>`.
2. Back-end PR adds the contract and DD; it validates against `ARCH_BASE_REF=pr-<n>` until step 1 is merged, then
   against `main`.
3. Front-end PR adds its DD with `consumes` pointing to the new operation; it validates against the back-end fragment
   published from its PR or `main`.
4. Merges to `main` publish fragments; lock bumps follow automatically.

### 5.11 Security

- **Write:** only the CI service account writes to the bucket; only CTX-INT writes to Git for automated changes; builds
  of untrusted branches publish `pr-*` only and never move `main`.
- **Read:** browsers never read the bucket. The backend proxies `/api/architecture/…`, checks scope through CTX-IAM,
  and leaves room for team-restricted Sources (OPP-06).
- **Content:** Mermaid runs with `securityLevel: 'strict'`; SVGs pass an SVG sanitiser before upload and are shown as
  `<img>`; Markdown HTML goes through Angular's sanitiser; the LikeC4 bundle is served same-origin with a hashed
  name under `script-src 'self'`.
- **Supply chain:** builder image pinned by digest; no downloads during builds.

### 5.12 Performance (estimates)

| Build | Cold | Cached |
|---|---|---|
| `atbDesign`, one Module (about 7 DD files, 20 diagrams × 2 themes) | 1.5–2 min | under 1 min |
| `atbArchitecture`, about 3,000 elements across 30 Applications | 4–6 min | 2–3 min (Mermaid cache, unchanged slices reused) |

Tier-3 extraction reuses the application's compile output, so it usually adds less than a minute.

### 5.13 Pull-request comment

```
Architecture · central @ c0ffee1                      ! Needs attention
  Checks   212 passed · 3 warnings · 0 errors
           ! T6  sbb.environments.jenkins-descriptor-job has no detailed design
  Changes  + sbb.environments.reservation-api (new, target)
           ~ abb.environments.reservation (changed)
  Gaps     delivery-platform transition-1 → target: 3 new · 1 changed · 1 retired
  ARB      arb.delivery-platform.2026-14 is affected (updated since review)
  Preview  /architecture/a/environments?ref=pr-88
```

---

## 6. Vocabulary additions (DEC-KB-11)

| Term | Context | Definition |
|---|---|---|
| Portfolio | CTX-CAT | A group of Applications governed together, with its own roadmap and ARB. Attribute of Application. |
| Architecture model | CTX-ARC | The building blocks, requirements, plateaus, gaps, work packages, ADRs and ARB records of the organisation, stored in the central architecture repository. |
| Design fragment | CTX-ARC | The published detailed design, contracts index and code structure of one Module at one commit. |
| ARB submission | CTX-ARC | A request for an architecture board decision on a change between two plateaus; decided through a Checkpoint. |

Proposed context: **CTX-ARC — Architecture** (supporting). Owns the architecture model view, design fragments,
ARB submissions; publishes EVT-ARCHITECTURE-PUBLISHED; consumes EVT-CHECKPOINT-DECIDED; reads CTX-CAT for
Applications and Portfolios. The alternative is to fold it into CTX-DOC; a separate context is preferred because the
ARB workflow and its Checkpoints don't belong to documentation.

---

## 7. Open points

| ID | Question | Revisit trigger |
|---|---|---|
| OPP-ARC-01 | Git hosting product: auto-merge and branch protection features differ. | Before building the lock bot. |
| OPP-ARC-02 | Bucket product: MinIO or the internal cloud's S3. | Before the first publish. |
| OPP-ARC-03 | Tier-3 extractor: Spring Modulith in every Module, or jdeps and ArchUnit only. | First Module without Spring Modulith. |
| OPP-ARC-04 | CTX-ARC as its own context, or inside CTX-DOC. | Next domain reference review. |
| OPP-ARC-05 | When an Application moves to federated mode (A): criteria and procedure. | First team asking to own its SBBs in its repository. |
| OPP-ARC-06 | Cross-Portfolio ARB: which Portfolio records it, who is a required reviewer. | First change touching two Portfolios. |
