---
title: Architecture prototype board — TOGAF views as grids, catalogue tree, ARB page, adjusted TOGAF flow, labs
status: draft
date: 2026-11-03
relates-to: architecture-reading-axis-and-views.md, docs-way-in-and-architecture-navigation.md, architecture-knowledge-base-notes.md, architecture-delivery-and-repositories.md
---

# Architecture prototype board (design canvas, Prototypes page)

The Architecture feature as one live board, `Architecture.dc.html`, on the AIToolbox design canvas beside the
production vision. Meridian Bank example (4 portfolios, 31 applications, 227 elements, 8 changes, 4 ARB submissions),
AIToolbox shell (header with page context, rail, bottom bar under 600 px), window-width simulator, "view as" change
owner · reviewer · board chair · reader. Tabs in this order: **Catalogue · Views · Process** (the catalogue opens first;
it is one tree, searched from the header field).

Three decision labs sit on the Decision labs page beside the Docs lab: Catalogue lab, Views lab, Process lab (section
"Labs" below). All three are decided: A · A · A.

## Decisions

| ID | Decision |
|---|---|
| DEC-KB-24 | **No LikeC4 on the Architecture page.** Every view is a CSS grid, a matrix (table) or a timeline built from the design-system ArchiMate components: figure (`ax-box` / `axf`), type tile, change chip, plateau track, status chip, relationship name under a figure. A relationship is read from the position (row × column) and its name; there are no drawn lines. LikeC4 stays the authoring and validation format (DEC-KB-01) and the MCP source for agents; the page does not embed `likec4-view`. Extends DEC-KB-21 to the six views that were still graphs. |
| DEC-KB-25 | **Matrices added** (TOGAF catalogs and matrices, generated from the model): capabilities × value streams (serving), roles × processes (RACI from `assignment`), application interaction (flows row → column, dependency count), processes × applications (`serving` component → process), applications × technologies (lifecycle-coloured dot), in addition to capability coverage and data ownership. Each matrix carries a rule checked on the row or the summary: one A per process, one master per business object, a capability off every stream, a stage without capability, a process with no application, an application on a Retire standard, more than 4 dependencies. |
| DEC-KB-26 | **Former graph views as grids.** Motivation: one row per driver (stakeholder · driver · assessment · goals · outcomes · requirements), principles under it. Value streams: one grid per stream, stages as ordered columns, serving capabilities in the cells. Application cooperation: receives-from · application · sends-to per application, flows table below. Requirement chain: requirement · ABB · SBB (plateau) · detailed design, empty cells flagged (T1, T2, T4, T6). Inside and neighbours: receives-from · component · interfaces and services · data objects · sends-to · platforms, relationship table below. Gap: a new · changed · retired strip of application components above the gap table. |
| DEC-KB-27 | **Catalogue tree.** By portfolio (enterprise shared › portfolio › portfolio building blocks and applications › ArchiMate layer › elements, the layer level skipped when an application has one layer) or by layer (layer › type › elements); each node shows counts, change chip, plateau track and status; an application node links to its fact sheet. Superseded in part by DEC-KB-31: the tree is now the whole catalogue. |
| DEC-KB-28 | **ARB page = the whole solution document.** Header with status, readiness, from → to plateaus, PR, branch, reviewed commit and an "updated since review" banner; five figures (checks on the scope, sections written, coverage x/13, reviewer decisions, open conditions); four tabs: Solution design (the 13 ASD items in order, each marked Written or From the model and Covered · Partly · Thin · Missing, with a table of contents and "Copy ASD as Markdown"), Checks (by group, items with their fixes), Reviewers & conditions (decision per role with note, conditions with owner and due date, asks to the board), Decision (actions by role: owner submits or re-submits, a reviewer records Approve / Approve with conditions / Request changes / Not required, the chair records the board decision only when no blocking check fails, no reviewer is pending and none requested changes; the Git trail and the three outcomes). |
| DEC-KB-29 | **Process area gets "How it works".** The human change process is inside the product: the flow (DEC-KB-30), the lanes (people, toolbox, agents & CI, gates, Git), three classes of change, who does what (can / cannot per role, agents never decide, only the bot writes ARB records), parallel changes (three collision levels, three answers, guard checks), Git conventions. |
| DEC-KB-30 | **The adjusted TOGAF flow replaces the five steps.** Six phases and four gates: 0 Vision (need, scope) › **G1 Scope agreed** › 1 Baseline (current state · ADD) › 2 Target (ABB, SBB · ADD) › **G2 Target approved** › 3 Gap analysis (baseline vs target) › 4 Plateau (roadmap, WP, DD) › **G3 Ready to build** › 5 Implementation (code, PR, DoR · quality gate) › **G4 Delivered** › Delivery; the delivered plateau becomes the new baseline. A new need runs the full cycle; a change to an existing architecture **enters mid-chain** where it applies: Evolution at Baseline (update the ADD), Exploration at Target (start an ASD), Decision at Gap or Plateau (an ADR sends back to G2 or G3), Small tweak at Implementation (Definition of Ready only), Post-delivery after G4 (update the baseline). Side cases: **dual run** (the legacy way alongside until adoption, A3) and **off-plan change** (document or code first; reconciliation is mandatory before the next gate on the same scope). At every gate a human decides (A); agents draft and check (R): an agent proposes, a human approves. Supersedes Trigger · Decide · Design · Review · Deliver of the Architecture Change Process page; the mapping is Decide → Vision + G1, Design → Baseline · Target · Gap · Plateau, Review → G2 (ARB) and G3, Deliver → Implementation + G4. In the board, each change card shows the phase strip with its gates (passed, pending, needs attention, blocked), where it entered and what it waits for now. |
| DEC-KB-31 | **Catalogue = one tree, one field (Catalogue lab A, adopted 2026-11-03).** The catalogue is the tree (DEC-KB-27) with one Group by (portfolio or layer), Expand and Collapse, counts on every node; no Applications table, no All elements table, no level chips, no scope select, no field in the page. The header's search-or-ask field is the only search field (principle 6): typing from anywhere opens the catalogue and flattens the tree into the matching elements with their path (portfolio › application › layer); clearing it restores the tree. An application node carries TIME, owner and hosting and links to its fact sheet; comparing and sorting applications is a job for the views (landscape, fact sheet, matrices). Still to do: lazy, counted branches past a few hundred leaves; open state and current node in the URL. B Explorer is the fallback if sortable columns are demanded in the catalogue. |
| DEC-KB-32 | **Views navigation by steering level (Views lab A, adopted 2026-11-03).** Level picker, then the side list of that level's views tagged with rendering and audience, scope selects under the picker. B (ADM phase), C (gallery) and D (role) are kept for the record; C's cards may later serve as the landing screen of the tab and D's roles as a filter chip, neither as the navigation. |
| DEC-KB-33 | **Process navigation by object (Process lab A, adopted 2026-11-03).** Changes · Reviews · Decisions · Model checks · How it works; the changes carry the phase strip of DEC-KB-30. B (board by phase), C (board sessions, roadmap, due dates) and D (inbox) are kept for the record; C's sessions and due dates are candidates for the Reviews page, D's inbox for the toolbox home. |

## Levels and views (as built)

| Level | Views (rendering) |
|---|---|
| Enterprise | Capability map (grid, maturity · investment · applications) · Capability coverage (matrix) · Capabilities × value streams (matrix) · Roles × processes (matrix) · Technology radar (grid + table) · Enterprise roadmap (timeline) · Motivation (grid) · Value streams (grid) |
| Portfolio | Application landscape (grid) · Application cooperation (grid + flows table) · Application interaction (matrix) · Processes × applications (matrix) · Gap (strip + table) · Data ownership (matrix) · Applications × technologies (matrix) · Roadmap (timeline) · Requirement chain (grid) |
| Application | Fact sheet (cards) · Inside and neighbours (grid + relationships table) · Interfaces and data (tables) |

Every view carries For, Decides, a "How to read this view" line and, where it applies, the plateau selector (B · T1 · T);
the side list tags each view Grid · Matrix · Table · Timeline · Cards.

## Labs (Decision labs page) — decided 2026-11-03

| Lab | Alternatives | Decision and criteria |
|---|---|---|
| Catalogue lab | A One tree, one field · B Explorer (containers tree + table) · C Facets (Where and Layer side lists + table) · D Search first | **A adopted (DEC-KB-31)**, with two amendments: no field in the page (the header's search-or-ask field is the only search field, principle 6; typing flattens the tree) and lazy, counted branches with the open state and current node in the URL. Criteria: shows what exists and who owns it; finds a known element; cross-cuts (A has them through Group by layer); scale (thousands of elements: A needs lazy branches, B paginates); Compact width (B's two panes fail); consistency with "minimal by default". B is the fallback if sortable columns are demanded in the catalogue; C and D are not (C loses the hierarchy, D hides the existing and duplicates the chatbot's job). |
| Views lab | A By level · B By ADM phase · C Gallery · D By role | **A adopted (DEC-KB-32)**; the level is the first question of the reading axis and keeps every list short. |
| Process lab | A By object · B Board by phase · C Agenda and roadmap · D Inbox | **A adopted (DEC-KB-33)**; B, C and D kept for the record (C's board sessions and due dates are candidates for Reviews, D's inbox for the toolbox home). |

## Prototype data (to put in the model)

The Meridian Bank model has no business roles and no link from processes to applications, so the board adds, marked
"prototype data": 10 business roles (`business-role`, `model/bb/enterprise-roles.c4`), RACI `assignment` relationships
role → process (label performs · decides · consulted · informed), `serving` relationships application component →
business process (label `supports`), and for the ARB submissions the PR number, branch, reviewed sha and the asks to
the board. The entry point of each change (new need, evolution, exploration, decision) is also prototype data: it
belongs in the work package metadata (`entry`). The notation gains the `business-role` glyph.

## Tooling

`tooling/architecture-board/`: `data_prep.py` (MODEL of the generated page → `arch_data.json` + the extension),
`build_arch.py` (templates, CSS, strict markup check) with `arch_logic.js` (the Component: state, views, matrices,
tree, process, flow, ARB) and `how_data.py` (the adjusted flow, gates, entry points, side cases, classes, roles, Git as
data); `build_catlab.py` and `build_labs.py` build the three labs on the same logic; `convert.py` + `dc-standalone.js`
render a board as a standalone page for checks. Reuses `shell.py` and `navgen.py`.

## Open points

| ID | Question | Revisit trigger |
|---|---|---|
| OPP-ARC-10 | Roles, RACI and process support in the real model: `business-role` elements and `assignment` / `serving` relationships in `model/bb`, with the two checks (one A per process; a process in a plateau has at least one supporting application, else it is declared manual). | Next model change. |
| OPP-ARC-11 | Fold the board back into the production vision (Docs › Architecture) and retire the LikeC4 canvas of the Docs lab, or keep the lab for the record. | Next production-vision update. |
| OPP-ARC-12 | Large matrices (application interaction across the enterprise): sticky first column and headers are done; sorting, grouping by portfolio and a "only rows with a mark" filter are not. | First matrix over ~40 columns. |
| OPP-ARC-13 | Export of the ASD (Markdown is a toast in the prototype) and of a matrix (CSV). | ARB pilot. |
| OPP-ARC-14 | Gate criteria, decisions (section 4), human and agent (section 6), use cases, traceability and glossary of the adjusted-flow page are summarized from its first section only; align the board's gate cards and the Architecture Change Process page on the source once it is shared. | When the adjusted-flow page is in the bundle. |
| OPP-ARC-15 | Closed: the three labs are decided (A · A · A, DEC-KB-31..33) and applied to the board. Remaining from the catalogue amendments: lazy branches at scale, tree state in the URL. | First model over ~1,000 elements. |
