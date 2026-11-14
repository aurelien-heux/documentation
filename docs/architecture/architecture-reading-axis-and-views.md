---
title: Architecture reading axis — TOGAF and ArchiMate concepts and views per steering level
status: draft
date: 2026-11-03
relates-to: architecture-knowledge-base-notes.md, docs-way-in-and-architecture-navigation.md, architecture-delivery-and-repositories.md
---

# Architecture reading axis — concepts and views per steering level

How the architecture knowledge base is read: one vertical axis (why → what → how → with what → when), one horizontal
axis (baseline → transitions → target), and at each steering level only the views needed for that level's decisions.
Matrix-shaped views are CSS grids generated from the model; graph views stay in LikeC4 only where relationships carry
the information.

## Decisions

| ID | Decision |
|---|---|
| DEC-KB-20 | **Concept profile**: 25 ArchiMate element types and 9 relationships are required for steering; the other 37 types stay available in the notation but no view or check depends on them. |
| DEC-KB-21 | **Grids, not graphs, for matrices**: capability map, capability × portfolio, application landscape per plateau, data ownership, technology lifecycle and roadmap timeline are CSS grids generated from `bb.json`. Graph layouts (LikeC4) are kept for motivation, value stream, application cooperation, inside an application, deployment and the gap of one change. |
| DEC-KB-22 | **Every steering view exists per plateau**: the plateau selector is on every view; the change against the previous plateau is a chip in the same cell. Gaps are computed, never drawn. |
| DEC-KB-23 | **Three levels of drill-down, 10 to 15 nodes each**, for graph views: enterprise → portfolio → application; nest again inside a portfolio past about 10 applications. Full lists belong to catalogue tables. |

Numbering continues after the delivery doc (DEC-KB-13..18 reserved for the renumbering of its DEC-KB-07..12) and the
navigation doc (DEC-KB-09..12, to be renumbered 13..16). See open point OPP-ARC-07.

## 1. The vertical axis

| Layer (ArchiMate) | Question | TOGAF phase | Required concepts |
|---|---|---|---|
| Motivation | Why change? | Preliminary, A | Stakeholder, Driver, Assessment, Goal, Outcome, Principle, Requirement, Constraint |
| Strategy | What must we be able to do? | A, B | Capability, Value stream, Course of action, Resource |
| Business | Who does what, on what? | B | Business actor / role, Business process, Business service, Business object, Business event |
| Application | Which applications, interfaces, data? | C | Application component, Application interface, Application service, Application event, Data object |
| Technology | Running on what? | D | Node, System software, Technology service, Artifact, Communication network |
| Implementation & migration | In which order, by whom? | E, F, G, H | Plateau, Gap, Work package, Deliverable, Implementation event |

Relationships: realization, serving, composition, aggregation, assignment, access, flow, triggering, influence
(association only as a last resort, and `'retires'` on a work package).

Reading downwards answers "how is this goal delivered"; reading upwards answers "why does this component exist". The
validator's traceability checks (T1–T6) follow the same axis.

## 2. The horizontal axis

Plateaus are the time axis: Baseline, one or more Transitions, Target. Membership comes from relationships (the
baseline aggregates what exists; each later plateau adds what its work packages realize and removes what they retire),
so every view can be shown "as of" any plateau, and the change between two plateaus is a computation. The page shows
the plateau selector (B · T1 · T2 · T) on every landscape, map and gap view; the change chip sits in the cell.

## 3. Levels, questions and views

### 3.1 Enterprise — CIO, enterprise architects: capabilities and standards

| View | ArchiMate viewpoint | Rendering | Decision supported | Inputs needed |
|---|---|---|---|---|
| Capability map, heat-mapped by maturity or investment | Capability map | CSS grid (domains × capabilities, colour by metric) | Where to invest | `maturity`, `investment` metadata on capabilities |
| Capability × portfolio coverage: which applications realize what; gaps and overlaps | Capability realization | CSS grid (matrix) | Rationalize, close gaps | Portfolio attribute from CTX-CAT |
| Value streams and the capabilities each stage needs | Value stream | LikeC4 graph, ≤ 12 nodes | Priorities per stream | Value streams modelled |
| Motivation: drivers → goals → outcomes → principles | Motivation | LikeC4 graph, ≤ 15 nodes | Justify a programme | — |
| Technology standards and lifecycle (adopt · trial · hold · retire) | Technology usage | CSS grid (radar by category) | Standards, obsolescence | `lifecycle` metadata on technology |
| Enterprise roadmap: plateaus per portfolio on a timeline | Implementation and migration | CSS grid (portfolios × quarters) | Sequence programmes | Work package dates |

### 3.2 Portfolio — portfolio architect, ARB: transitions

| View | Viewpoint | Rendering | Decision | Inputs |
|---|---|---|---|---|
| Application landscape per plateau: building blocks by capability, layer colour, change chips | Application cooperation (structure only) | CSS grid — **implemented**: Landscape › Capability map | What the portfolio looks like at each plateau | — |
| Gap baseline → target with the delivering work package | Migration | Table + LikeC4 gap view of the changed subset — implemented | ARB review, delivery scope | — |
| Application cooperation: flows between the portfolio's applications and their neighbours | Application cooperation | LikeC4 graph, nested, ≤ 15 nodes | Integration decisions | — |
| Data ownership: which application masters which business object; CRUD | Information structure | CSS grid (matrix) | Data stewardship, duplicates | `access` relationships with `reads` / `writes` labels |
| Roadmap: work packages, plateaus, dependencies, ARB conditions | Implementation and migration | CSS grid timeline — **implemented**: Landscape › Roadmap › Timeline | Order, conflicts between changes | `start`, `end`, `dependsOn` |
| Decisions and compliance: ADRs, checks, waivers with expiry | — | Table | Governance | Waiver records (future) |

### 3.3 Application — application lead, teams: design

| View | Viewpoint | Rendering | Decision |
|---|---|---|---|
| Requirements → ABB → SBB chain | Requirements realization | LikeC4 graph — implemented (chain view) | Traceability, coverage |
| Inside the application: components, interfaces, data, events; the target as a hexagon | Application structure | LikeC4 `view … of <application>` | Boundaries, contracts |
| Interfaces and events with contract status | Application usage | Table | Contract governance |
| Deployment: components on nodes and environments | Technology / deployment | LikeC4 graph, ≤ 12 nodes | Hosting, resilience |
| Business process realization: steps → application services → data | Business process cooperation | LikeC4 graph | Impact of a process change |

### 3.4 Module — developers, agents: implementation

Detailed design in text (domain, events, ports, application, infrastructure, API, data model), Mermaid for the state
machine and the data model, code structure extracted and shown as a tree. No graph view at this level by default; the
chatbot drills into classes on request (DEC-KB-05).

## 4. Why grids

Steering views are sets classified along two axes (capability × maturity, capability × portfolio, application × data,
portfolio × quarter, technology × lifecycle), not graphs. A grid reflows to the window, shows hundreds of cells on one
screen, sorts and filters, and each cell is the ArchiMate figure linking to its element page. A graph layout adds
nothing to a matrix and causes the width problem measured in the Wide Views Demo (a flat landscape of 30 applications
lays out at 9,306 × 496 px and is shown at 12 % in a page frame).

Count per level: about 9 grids, 6 graphs and 4 tables, all generated from `bb.json` and the plateau membership.

## 5. Rules for the graph views that remain

1. Nest: include the parents (portfolio, application) so `dot` has compounds to stack. Flat includes give one row per rank.
2. Drill down: enterprise → portfolio → application, each a `view … of` with 10 to 15 nodes; nest again inside a
   portfolio past about 10 applications.
3. Show less: one kind per overview, `exclude * -> * where kind is flow`, `size xs`, tighter `autoLayout` spacing.
4. Frame: 60 to 80 % of the viewport, `browser` attribute on `<likec4-view>`; `likec4 export png` for documents.

## 6. Implemented (2026-11-03)

The Architecture page now follows the navigation decided on 2026-10-30: three areas, and in Views a level picker.
Every view carries **For** (who), **Decides** (what) and a "How to read this view" line.

| Area | Level | Views | Rendering |
|---|---|---|---|
| Views | Enterprise | Capability map (maturity, investment, applications; per plateau) · Capability coverage (capability × portfolio) · Technology radar (+ applications on Hold or Retire) · Enterprise roadmap · Motivation · Value streams | Grid · grid · grid + table · timeline grid · LikeC4 · LikeC4 |
| Views | Portfolio | Application landscape (capabilities × applications, TIME and change chips) · Application cooperation (+ flows table) · Gap · Data ownership (business object × application, master or copy, one-master check) · Roadmap · Requirement chain | Grid · LikeC4 + table · LikeC4 + table · grid · timeline grid · LikeC4 |
| Views | Application | Fact sheet (catalogue facts, capabilities, platforms, data, changes, decisions, flows) · Inside and neighbours · Interfaces and data | Cards · LikeC4 · tables |
| Catalogue | — | Applications (portfolio, TIME, criticality, owner, hosting, plateaus) · All elements (scope and level filters, search) | Tables |
| Process | — | Changes (Decide · Design · Review · Deliver per work package, overlaps, dependencies, ARB link) · Reviews (ARB, ASD, checks, decision) · Decisions (ADR log) · Model checks | Cards, tables |

Pipeline changes:

- `catalog.yaml` at the model root (CTX-CAT stand-in): portfolios and applications with TIME, criticality, owner,
  sourcing, hosting. Each element gets `scope`, `scopeType` (enterprise, portfolio, application), `portfolio` and
  `chain` (the plateau chain that governs it: its own scope's, or its portfolio's).
- Plateau chains per portfolio; gaps, ARB readiness and the change checks are computed per chain. C3 also checks dates
  across portfolios (a change cannot start before a change it depends on ends).
- O2 now applies to new and changed interfaces only (legacy interfaces may have no contract file).
- Generated LikeC4 views per portfolio (landscape per plateau, gap, cooperation, requirement chain), per application
  (inside and neighbours), and one per changed element, requirement and application component.
- Inputs used by the grids: capability metadata `level` (L1/L2), `parent`, `maturity`, `investment`, `strategic`;
  technology metadata `lifecycle`, `category`; `access` relationships titled `writes` / `reads` from a component to its
  data objects, which realize enterprise business objects; plateau metadata `date`; work package `class`.

Example: `examples/bank/` (Meridian Bank, fictional): 4 portfolios, 31 applications, 29 capabilities, 17 technology
standards, 8 changes, 4 ARB submissions. Its README has the reading guide (who uses which view where).

Not yet implemented: heat maps by cost or risk, the capability × value-stream matrix, deployment views, waivers.

## 7. Open points

| ID | Question | Revisit trigger |
|---|---|---|
| OPP-ARC-07 | Renumber the DEC-KB clash: the delivery doc and the navigation doc both use DEC-KB-09..12. Proposal: navigation keeps 09..12, delivery becomes 13..18, this doc starts at 20. | Next edit of either doc. |
| OPP-ARC-08 | Maturity and investment scales for the capability heat map (who scores, how often). | First enterprise review using the map. |
| OPP-ARC-09 | Technology lifecycle source: metadata in the model, or the CTX-CAT catalog. | First obsolescence alert. |
