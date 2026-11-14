# AIToolbox · Simplified metamodel v4 — Baseline / Target, delivery, requirements and business rules

Transcription of the diagram shared on 2026-11-09 (`metamodele-baseline-target-delivery-v4.svg`), its mapping onto the
current Meridian model (`arch_data.json`, LikeC4 conventions in `architecture-knowledge-base-notes.md`) and onto the
change & documentation process (DEC-KB-38..42), and the prototype changes it implies. Status: sections 3 and 4.1 are
decided (DEC-KB-43, DEC-KB-44); section 7 lists what is settled, parked and still open; **section 8 says what was
built** (canvas version 230).

Diagram subtitle, kept as the design intent: *the application chain is tightened for code generation — what to do
(Service), under which contract (Interface), on which data (Data Object), where (Component).*

---

## 1. The metamodel, in English

### 1.1 State chain (identical for Baseline and Target)

| Object | Short definition (from the diagram) | Linked to |
|---|---|---|
| Value stream | Value chain and its stages | *relies on* → Capability |
| Capability | Business capability (level 1…n) | *realized by* → Process / Data / Event / Business rule |
| Process | Business process | *automated by* → Application service |
| Data | Business object | *read / written* by the process; *manipulated* by the service through a Data object |
| Event | Business event | *emitted* by the process |
| Business rule | `BR-…`, ≈ Constraint | *influences* the process; *realized by (DR-…)* → Application service |
| Application service | Use case: operation, inputs/outputs, `DR-…`, acceptance criteria | *exposed by* → Application interface; *manipulates* → Data object |
| Application interface | API · events · screen | *offered by* → Application component |
| Data object | Aggregate, invariants | *owned by* → Application component |
| Application component | Module: boundary, allowed dependencies | — |
| Standards (cross-cutting, outside the chain) | `ARL-CODE`, `ARL-UI`… given to the agent as context | not linked; context only |

Reading downwards: why (value stream, capability) → what the business does (process, data, event, rule) → what the
application does (service) → through which contract (interface) → on which data (data object) → where (component).

### 1.2 Delivery line

| Object | Short definition | Relationships |
|---|---|---|
| Requirement | Need, functional or non-functional | *justifies* → Gap; *satisfied by* ← Target element; *realized by* ← Ticket |
| Gap | Addition · modification · removal; one Baseline element and/or one Target element | *state before* ← Baseline element; *state after* ← Target element; *addressed by* ← Work package |
| Work package (epic) | Batch of work, owner, due date | *contains* → Ticket |
| Ticket (deliverable change) | Acceptance criteria | *implements* → Target element; *realizes* → Requirement; *delivered by* ← Commit |
| Commit | Code change (SHA) | *modifies* → Target element; *replaces / retires* → Baseline element; *grouped by* ← Version |
| Version (release) | Delivered tag, reaches a plateau | — |

Reading the line top-down answers "why is this being built"; bottom-up, from a commit, "which requirement does this
code serve". The dashed arrows from Requirement to the Target chain (*creates · modifies · retires (influence)*) say
that a requirement changes the Target state; the model records that change as gaps.

---

## 2. Mapping onto the current model

Legend: ✓ present · ◐ present but not in this shape · ✗ missing.

### 2.1 State chain

| Metamodel | ArchiMate kind in the model | Status | Today in `arch_data.json` / conventions |
|---|---|---|---|
| Value stream | `value-stream` | ✓ | 11 elements |
| Capability | `capability` | ✓ | 31, level 1…n through `children` |
| Process | `business-process` | ✓ | 8 |
| Data | `business-object` | ✓ | 10, `data[].bo` links to the owning data object |
| Event | `business-event` | ◐ | In the notation, no element instanced |
| Business rule | none in ArchiMate 3.2 | ✗ | Diagram says ≈ Constraint (motivation). Not modelled; `BR-…` ids nowhere |
| Application service | `application-service` | ✓ | 4 — the use-case content (operation, inputs/outputs, acceptance criteria) lives in the Markdown requirement rows, not on the service |
| Application interface | `application-interface` | ✓ | 12, `contract` metadata → OpenAPI / AsyncAPI |
| Data object | `data-object` | ✓ | 35, `mode: master \| copy` |
| Application component | `application-component` | ✓ | 31 = modules; "allowed dependencies" = the hexagonal rules of the DD, not a model fact |
| Standards | `technology` lifecycle + `principle` | ◐ | Technology standards (adopt · trial · hold · retire) and principles exist; `ARL-CODE` / `ARL-UI` rule lists do not |

The relationship names of the diagram all exist in ArchiMate: *relies on* and *realized by* → `realization`
(serving for value stream → capability is also acceptable), *automated by* / *exposed by* / *offered by* → `serving`
or `assignment`, *read / written / manipulates* → `access`, *emits* → `triggering`, *influences* → `influence`,
*owned by* → `composition`. No new relationship kind is needed.

### 2.2 Delivery line

| Metamodel | Status | Today |
|---|---|---|
| Requirement | ✓ | `requirement` (4) + `model/requirement/<id>.md` (acceptance rows, decision table, figures) |
| Gap | ◐ | **Derived**, never typed (decision of 2026-10-30): the gap between two plateaus is computed from membership; `landscapes[].gaps[].items` carry `change: new \| changed \| retired` and `addressedBy` (work packages). The gap has no identity of its own and no link to a requirement |
| Work package | ✓ | `work-package` (8), `workItemId` (`WI-…` = CTX-ORC work item), `realization` → plateau and → delivered elements, `'retires'` association |
| Ticket | ✗ → built as observed data (§8) | Appeared only as text: `RET-4410` in a Need note, Sweep runs `E2ECC-…` as the author of a DD draft |
| Commit | ◐ → built as observed data (§8) | SHAs were recorded on **documents** (published @ sha) and on repositories, not as objects linked to elements |
| Version | ◐ → built as observed data (§8) | The Environments board knows versions deployed per environment (`VER`, `shaOf`), the plateaus have a date; nothing said "version X reaches plateau T1" |

### 2.3 Where the process documents attach

| Document (DEC-KB-38) | Attaches to | Metamodel reading |
|---|---|---|
| Need, Requirement | Requirement | The delivery line starts here |
| ADD, ASD, Gap table, Roadmap | Work package (one working document per deliverable per change) | The ADD describes the Target chain; the Gap table **is** the set of gaps the work package addresses; the roadmap is the plateau the version will reach |
| ADR | Gap / Target elements | The decision explains why a gap is closed this way |
| Detailed design | Application component (Target) | Written per module; drafted from the Ticket / Commit that touches the module (OPP-ARC-17) |
| Contract | Application interface | Already `contract` metadata |
| Model (`.c4`) | The elements themselves | Published @ sha = the Commit of the model repository |

So the metamodel gives each document an anchor object, and the "published @ sha" state of a document is a Commit
on the architecture repository — the same object as the code commits, just another repository.

---

## 3. Where the code is written: two entry points, one knowledge base, one delivery line

Decisions of 2026-11-09:

- **Sweep is one of the entry points to iterate on the implementation, in parallel with local development done with
  a coding assistant.** Neither is an object of the metamodel; both are ways of producing the same objects.
- **The knowledge base is exposed to agents through one MCP server**, whether the agent runs locally in a harness
  (OpenCode, Claude Code…) or remotely in Sweep. It is the published language of CTX-KI (`Query → Evidence[]`, which
  CTX-ART already uses to assemble Context packs) served over MCP; there is no second path. Recorded as **DEC-KB-43**.

| | Sweep (platform run) | Local development (coding assistant in a harness on the developer's machine) |
|---|---|---|
| Starts from | A Ticket (its acceptance criteria) | The same Ticket |
| Reads as context | The knowledge-base MCP server, called by CTX-ART when it assembles the Context pack | The same MCP server, declared in the harness (OpenCode, Claude Code…) |
| Produces | Commits on a branch, a pull request | Commits on a branch, a pull request |
| Visible to the knowledge base as | The run (`E2ECC-…`) **and** its commits | Only the commits and the pull request; the local session is not observed |
| Leaves a trace of its reasoning | The run log, kept by the platform | Nothing beyond the commit messages and the PR — by design |

Consequences:

- **The Commit is the convergence point.** Whatever wrote the code, the knowledge base observes the same thing: a
  commit, on a repository mapped to a module, carrying a ticket key. All the edges of section 4.2 (delivers, modifies,
  replaces, grouped by) are derived from commits and PRs, never from Sweep runs. A Sweep run is provenance: an extra
  edge `producedBy` from a commit to a run, present only when the commit came from Sweep.
- **The context pack is the same for both, from the same server.** What the MCP server answers for "context for
  ticket X" or "context for module Y" is the chain Service → Interface → Data object → Component, the contracts, the
  requirement rows (acceptance criteria) and the standards. The "Context for code generation" card on the Application
  service page (section 8) is that answer made visible, so that a developer and an architect see what the agents
  receive, whichever entry point is used. Reads go through the MCP server; writes never do — the agents' only way back
  into the knowledge base is a commit or a PR (INV-07, DEC-KB-38).
- **The DD hook fires on the commit, not on the run.** OPP-ARC-17 ("DD drafted from the Sweep run") becomes "DD drafted
  from the pull request that touches the module": the drafting conversation opens in the global assistant pane when
  the PR is opened, for a Sweep PR and for a local PR alike. The Sweep run only has more material to offer (its log).
- **A Sweep run is an execution of a ticket, not a ticket.** The ticket lives in CTX-ORC before and after the run
  (acceptance, release); several runs and several local sessions can serve one ticket.

### 3.1 The MCP server, minimal surface

Tools, named after the questions the metamodel answers; all read-only (shown as built in How it works › Coding
assistants):

| Tool | Answers | Returns |
|---|---|---|
| `context_for_ticket(key)` | What should I build and against what? | Ticket, acceptance criteria, target elements it implements, the chain down to the component, contracts, standards that apply |
| `context_for_module(application/module)` | What is this module, what may it depend on? | Component, its interfaces, data objects, services, allowed dependencies, DD, standards |
| `chain(element id)` | Why does this exist? | Up: service → process → capability → value stream; requirement rows it realizes |
| `gap(work package or plateau pair)` | What changes between before and after? | State before → after per element, justifying requirement |
| `search(query)` | Free question | `Evidence[]` with element ids and `@ sha` sources, as the assistant pane gets today |

The same tools serve the global assistant pane; the pane is just one more MCP client of the knowledge base.

---

## 4. What the metamodel changes in the conventions

### 4.1 Gap — what TOGAF says, and the resulting rule (settled 2026-11-09)

What the standard says ([Architecture Content, §2 content metamodel](https://pubs.opengroup.org/togaf-standard/architecture-content/chap02.html);
[Pocket guide, ADM and migration-planning techniques](https://pubs.opengroup.org/pocket-guides/togaf-pocket-guide/main/chap05.html)):

- A Gap is a metamodel **entity**: "a statement of difference between two states", with the attributes every entity
  has — ID, name, description, category, source, owner — and no relationship of its own in the relationships table.
  In the metamodel figure it is drawn with the architecture requirements (requirement, constraint, assumption), not
  with the building blocks.
- Gaps are **produced by the gap-analysis technique**, "usually the final step within a phase" (B, C, D): a matrix of
  Baseline building blocks against Target building blocks; what is shared is *Included*, a Baseline block absent from
  the Target is *Eliminated*, a Target block absent from the Baseline is *New* — "anything under Eliminated or New is a
  gap". Every *Eliminated* must be reviewed: either it was removed on purpose, or it is an accidental omission to
  reinstate. Every *New* must be developed or procured.
- In Phases E and F the gaps are **consolidated** in the Consolidated Gaps, Solutions and Dependencies matrix, which
  "can be used as a planning tool when creating work packages".

So TOGAF does both things at once: the gap is *computed* from the comparison, and it is then *recorded* with an
identity, a review (intentional or omission) and a solution. That is the 2026-10-30 decision plus what it lacked.

**Rule (DEC-KB-44):** gaps are derived from plateau membership and never typed in the model, but every derived gap is
an addressable entity of the knowledge base:

- id `gap.<app>.<name>` computed from the pair (baseline element → target element; `∅ →` for *New*, `→ ∅` for
  *Eliminated*), stable across builds;
- category = TOGAF's *New* · *Eliminated* · *Included-changed* (the page says added · changed · retired, as today);
- `addressedBy` = the work packages whose `realization` / `'retires'` cover it; **`justifiedBy`** = the requirements
  reached through the target element's realization chain — no new fact is typed for either;
- the ADD's gap table is the consolidated matrix of the work package: one row per gap, with its category, its
  requirement and its solution;
- the *Eliminated* / *New* review is the existing validation check P3 ("every gap item is addressed by a work
  package"), a warning to the board; it is split in two messages when the time comes ("accidental omission?" for an
  Eliminated block without a retiring work package, "not planned" for a New block without one).

Only a gap with no model difference (a non-functional change on an unchanged block) is declared by hand, in the work
package file, as an ArchiMate `gap` associated with the block — the exception, not the rule.

### 4.2 The rest (proposal)

1. **Business rule = ArchiMate `constraint` with id `br.<app>.<name>`** and `displayId: BR-…`, *influence* → process,
   *realization* ← application service. It is the smallest change that keeps the model pure ArchiMate; a dedicated
   LikeC4 kind `business-rule` (styled as the constraint figure) is the alternative if rules deserve their own tab.
2. **Business event** is simply instanced where processes emit one (`business-event`, *triggering*).
3. **Ticket, Commit, Version are observed, not modelled.** They come from the connectors (CTX-ORC for tickets,
   Git for commits and PRs, CI for versions) and live in the knowledge-base graph as observed nodes, like the
   working-document nodes of DEC-KB-42; the model never contains a ticket. Edges: ticket `partOf` work package (by
   `workItemId`), ticket `implements` target element (from the ticket's element references), commit `delivers` ticket
   (ticket key in the commit or the PR), commit `modifies` component (from the paths of the repository → module
   mapping), commit `producedBy` Sweep run (when applicable), version `groups` commits (tags), version `reaches`
   plateau (declared once on the plateau: `reachedBy: <tag>`). Per INV-07 the agent reads these through connectors,
   never by opening the repositories.
4. **Application service carries the use case.** Operation, inputs/outputs and acceptance criteria move from prose
   into the requirement rows that already exist, each row `realizedBy` the service. (`DR-…` ids: parked, see 7.)
5. **Standards as agent context.** `ARL-CODE`, `ARL-UI`… are rule lists outside the model (Markdown with ids), served
   by the MCP server with the chain Service → Interface → Data object → Component. They are not elements and create
   no relationships.

---

## 5. What the prototypes needed (plan of 2026-11-09, before building)

Kept simple, following the feedback of 2026-11-09 (fewer things per screen, chat only in the global pane). Section 8
says what of this is built; the last three rows are not.

| Screen | Change |
|---|---|
| Change page (Architecture board) | One **delivery line**: Requirement → Gap(s) → Tickets → Commits → Version, each item a link to its object; the tickets under it |
| Element page, Target elements | **Delivered by**: tickets that implement it, last commit that modified it; for a retired baseline element: **Replaced by** |
| Gap table | The justifying requirement, a Delivery column; the TOGAF review stays in the existing check rows |
| Requirement page | The **chain**: requirement → gaps it justifies → tickets that realize it → their state |
| Application service page | **Context for code generation**: the four-step chain plus the standards, with one line saying it is what Sweep runs and coding assistants get |
| Architecture · How tab | **Coding assistants**: the MCP server address, the five tools, the one-line configuration for OpenCode and Claude Code |
| Environments (vision) | Versions deployed become the Version objects: a version chip opens the release (commits, plateau reached) — *not built* |
| Sweep run | Sources panel reads the chain as the agent's context; the run header names the ticket it executes — *not built* |
| Pull request (Sweep PR page and the Docs "Open pull requests" list) | The DD drafting entry point moves here, for Sweep and local PRs alike — *not built* |

---

## 6. TOGAF reading

The delivery line is the Implementation & Migration layer plus the Solution Building Block delivery: Requirement
(Requirements Management, continuous), Gap (gap analysis at the end of Phases B–D, consolidated in E), Work package
(Phase E/F, Implementation and Migration Plan), Ticket / Commit / Version (Phase G, Implementation Governance:
compliance of what is delivered against the Target). The metamodel therefore does not change the gate placement of
DEC-KB-38: the ADD and Gap table are reviewed at the ARB gate, the DD at the portfolio gate; the Version reaching a
plateau is the Phase G check — the only new gate-like event, and it is observed (CI), not reviewed.

---

## 7. Status of the open points (2026-11-09)

| # | Point | Status |
|---|---|---|
| 1 | Gap identity | **Settled** — derived and addressable, per TOGAF (DEC-KB-44, §4.1) |
| 2 | Business rule as `constraint` with `BR-…` | Later |
| 3 | Ticket keys from CTX-ORC; a Sweep run executes a ticket | Settled by the Sweep clarification (§3); keys to confirm later (the prototype uses `CRD-`, `PAY-`, `RET-`) |
| 4 | `DR-…` | **Parked** by decision — not modelled, not shown, until further notice |
| 5 | `ARL-CODE` / `ARL-UI` format and location | Later (shown by name only in the context card) |
| 6 | Version → plateau: declared or inferred | Later (the prototype declares it on the planned version) |
| 7 | Metamodel as enforced LikeC4 schema | Later |
| 8 | Local assistant access | **Settled** — the knowledge-base MCP server (DEC-KB-43). Whether it also serves Sweep run logs: **to rediscuss, not now** |

Still to write when the "later" points are taken: `architecture-knowledge-base-notes.md` and the domain reference
(observed node types, DEC-KB-43/44, OPP-ARC-17 rewritten on the pull request), business rules and events in
`arch_data.json`, the vision's Environments and Sweep pages (section 5, last three rows).

---

## 8. Built (2026-11-09, canvas version 230)

Architecture board and Docs › Architecture in the production vision, light and dark, 360 to 1920 px, 0 axe violations
on the touched screens. Package `aitoolbox-delivery-line-2026-11-09.zip`; data in `delivery_data.py`, logic in
`delivery_logic.js` (spliced into `arch_logic.js`).

| Screen | What is there |
|---|---|
| Change page | A **Delivery** block: Requirement › Gap › Tickets › Commits › Version, each a link where there is something to open; under it the tickets (key, title, what it implements or retires, commits with last sha and date, "Sweep" when a run produced it, state Done · In progress · To do). Shown **first** when the change is in Implementation, after the documents otherwise. Changes without tickets say so in one line ("No ticket before G3 · code written earlier is observed anyway, by its commits") |
| Changes list | One line per card: "3/5 tickets done · 1 in progress · last commit 30 Oct" |
| Element page | **Delivered by** (tickets implementing it, last commit touching it) · **Replaced by** on retired elements (the ticket and the new element) |
| Requirement page | **Delivery · x/y tickets done**: the gaps it justifies, by change; the tickets that realize it |
| Application service page | **Context for code generation**: what to do › under which contract › on which data › where, the requirement and its acceptance rows, the standards (ARL-CODE, ARL-UI); one line says it is what Sweep runs and coding assistants receive |
| Gap view | Summary line gains "justified by <requirement>"; a **Delivery** column per block (tickets done / total; retired blocks count the ticket that retires them) |
| How it works › Coding assistants | The knowledge-base MCP server, its five read-only tools, how Sweep, Claude Code and OpenCode connect |

Mock data: 14 tickets on four changes (CRD-201…205, PAY-310…313, RET-4420…4423, RET-4510 started before G3 from the
Sweep run E2ECC-103870), 11 commits (6 Sweep, 5 local; the shas already used by the documents), 5 versions (2 released,
3 planned, each planned one naming the plateau it reaches). The requirement of a gap row is found through the
realization chain, then through the ticket that implements or retires the block, then through the work package.

Left for later, by decision: `DR-…` (parked), business rules and events in the model, `ARL-CODE` / `ARL-UI` as real
documents, the version → plateau rule, the Sweep run header and the DD entry point on the pull request (vision Sweep
pages), Environments versions as release objects.
