---
title: Architecture change process and documentation upkeep — scope, flow, RACI, parallel changes, knowledge graph, first-wave screens
status: scoped 2026-11-09 · first-wave prototypes published (canvas version 229)
date: 2026-11-09
relates-to: architecture-prototype-board.md (DEC-KB-29, DEC-KB-30), architecture-delivery-and-repositories.md (DEC-KB-07..12), architecture-knowledge-base-notes.md, devtoolbox-domain-reference.md (Checkpoint, Artifact, INV-12, INV-13, INV-16)
---

# Architecture change process and documentation upkeep

Scoped with the product owner on 2026-11-09. One loop: every change to an application enters the adjusted TOGAF flow
(DEC-KB-30) where it applies, each phase produces or updates a named document, documents are drafted with the
assistant, consolidated in a working document on the page, validated by a person, submitted as a pull request and
reviewed at the gate. Agents draft and check; people decide; nothing reaches Git without a pull request (DEC-KB-12).

## 1. Use cases (triggers)

| # | Use case | Enters at | Documents touched | First wave |
|---|---|---|---|---|
| UC1 | New need (ticket, chat brief) | Vision | Need and scope, requirements, ASD, ADR, DD, contracts | yes |
| UC2 | Evolution of an existing application (a Sweep run changes the code) | Baseline | DD and contracts in the same pull request as the code; SBB when needed | yes |
| UC3 | Exploration, a target to propose | Target | ASD → ARB at G2 | yes |
| UC4 | Decision along the way | Gap or Plateau | ADR, back to G2 or G3 | How it works only |
| UC5 | Small tweak | Implementation | Definition of Ready only | How it works only |
| UC6 | Delivery: the delivered plateau becomes the baseline | after G4 | model (plateaus), roadmap | follows UC12 |
| UC7 | Off-plan change detected (code without model, model without code, undeclared contract) | nightly reconciliation | proposal pull request, reconciled before the next gate on the same scope | yes |
| UC8 | Undocumented application: documentation from code | Baseline | DD "from code · draft", validated by the team, accepted by an architect | yes |
| UC9 | Drift and freshness (documentation older than the code, owner gone, stale knowledge-base source) | continuous | flags, owner reminder, due date | documentation health panel |
| UC10 | Cross-application change (central model, back end, front end: three pull requests) | Target | order of the pull requests, lock bump | How it works only |
| UC11 | Dual run | Plateau | two active SBBs, switch date | How it works only |
| UC12 | Gate session (ARB): agenda, decisions, conditions, follow-up | G2 / G3 | ARB record written to Git | yes |

## 2. The document flow

**Chat (drafts) → working document in the page (consolidation) → Validate → pull request → review at the gate →
published in Git.**

- **Drafting in chat.** Each document has its own thread with the assistant: the agent asks its questions, proposes a
  structure, then the text. Several threads and several people can feed one document. A useful answer carries
  **Insert into section** (or **Replace section**): the agent never writes into the document on its own; the person
  injects.
- **Working document.** One per deliverable and per change (the ASD of change X, the DD of layer Y, ADR Z), held by
  the backend like the ARB workflow is today (Postgres), never the model itself: the page still never writes the
  model (DEC-KB-12), Git receives the pull request only. The document starts from its template (the 13 ASD items,
  the DD layers, the ADR template); each section has a state: empty · proposed by the agent · edited · consolidated.
  The page shows a Markdown editor per section, the pending proposals beside it, the diff against the version
  published in Git, and the history of insertions (who, when, from which thread). Several people may edit at once,
  section by section, with the history; no lock (to adjust if needed).
- **Validate and submit** opens the pull request in the right repository (central model or the application's) and
  attaches the document to its change and gate. The document becomes read-only until the gate decides; once merged
  it shows "Published @ sha" and is the starting point of the next change.
- **States of a document**, as shown on the change page: To do · Drafting in chat · Working document · Validated, PR
  open · Reviewed at G2 (or the gate concerned) · Published. A validated document that no gate has reviewed yet stays
  "waiting for the gate" in the chatbot and on the change page, never presented as current.
- **One pull request per document and per change**, so a gate knows exactly what it reviews.

TOGAF check: the Architecture Definition Document is produced per ADM cycle (phases B, C, D), versioned, "version 1.0"
being a formally reviewed architecture; the Architecture Repository is permanent, holds work in progress, and each
iteration populates the Architecture Landscape. Mapping: working document = one iteration's work in progress; the
Git model = the landscape; ARB records = the governance log; a document reviewed at a gate becomes a landscape asset.

## 3. RACI by document

Rule set by the product owner: documents are drafted through the agentic interaction in the chat, injected once the
user validates, and reviewed at the gates. ARB submissions are reviewed by the domain architects and the product
stakeholders. Detailed design is validated by each portfolio's architect with the tech leads.

| Document | Dialogues with the agent | Validates and submits (PR) | Reviewed at | Informed |
|---|---|---|---|---|
| Need and scope, requirements (UC1) | Product owner or tech lead | The requester | **G1** · portfolio architect + product owner | Team |
| Model (ABB, SBB, plateaus, gaps) | Portfolio architect | Portfolio architect | **G2** | Tech leads concerned |
| ASD / ARB submission (UC3) | Change owner | Owner | **G2** · domain architects + product stakeholders; the chair decides | Portfolio |
| ADR (UC4) | Portfolio architect | Portfolio architect | **G2 or G3** by phase | Tech leads, owner |
| DD and contracts (UC2) | Tech lead, in chat or from a Sweep run | **Portfolio architect with the tech leads** | **G3** (Ready to build), then DoR at implementation | Team |
| Roadmap, baseline after delivery (UC6) | Agent, from what was delivered | Portfolio architect | **G4** | Portfolio |
| Reconciliation proposal (UC7) | Agent, nightly | Tech lead for a DD, architect for the model | Next gate on the same scope | Owner |
| DD from code (UC8) | Agent, on the tech lead's request | Tech lead for the content, architect for the model entry | G3 of the next change | — |
| Doc site pages (runbooks, onboarding) | Application owner | Owner | No gate (same chat → PR mechanism) | — |
| Knowledge base | Automatic on every publish | — | — | Owner reminded when a source is older than 90 days |

## 4. Parallel changes

Extends the three collision levels of "How it works" (DEC-KB-29) to working documents.

| Level | Detected | The page shows | Answers |
|---|---|---|---|
| **Same document** (two changes hold a working document for the same DD layer or portfolio ASD) | When the document opens, and at every gate | "Also being worked on in change Y · n sections overlap", the shared sections marked | **Sequence** (Y waits, then rebases), **Merge** (one change, one document), **Split** (scope re-cut) |
| **Same element** (two changes touch the same SBB or contract) | At Validate, on the pull request's preview build | "Conflicts with change Y on sbb.x" among the checks | Same; the gate does not pass until decided |
| **Base moved** (the other change merged while this one was drafted) | On the publication of main | "Base moved to @ sha · n sections changed upstream" | **Rebase by section**: three-way merge section by section, the person chooses where they diverge |

One person decides the answer (the portfolio architect); the decision is noted on both changes; a rebased document
goes back to "Working document" (its previous pull request is closed). The ARB session shows the queue of changes on
the same scope in the chosen order.

## 5. Knowledge graph persistence

Today: nodes with a reference to Git. Kept, with work in progress added and never confused with what is published.

| Node | Key | Provenance | Enters / leaves |
|---|---|---|---|
| Model element (ABB, SBB, requirement, plateau…) | id + `(repo, path, sha)` | `source: architecture`, `version: sha` | On every publish of `main`; the previous version is replaced |
| Published document (DD, ADR, ASD, ARB record) | id + `(repo, path, sha)` | same, by section (chunks) | Same |
| **Working document** | `change id + document id`, no sha | `source: working-document`, `status: drafting / working / validated / reviewed`, `updatedAt`, `pr-<n>` once the PR exists | Enters at creation; edge **`supersedes`** to the published node; leaves at merge, when the published node takes the new sha |
| Change (work item) | id | phase, current gate, entry point | Edges `produces` to its documents, `touches` to the elements |
| Gate decision | id | deciders, conditions, date | Edges to the change and to the Git record once written |

The chatbot answers from what is published first; when a working document supersedes it, it says so ("a change in
progress proposes… · working document, not reviewed") instead of presenting it as current (INV-13, INV-16 applied to
drafts). Chat threads are not indexed; only the sections inserted into a document are.

## 6. Documentation health

One dataset (coverage: SBB without DD, endpoint without contract; freshness: last code commit vs last DD commit;
origin: written or from code; open drifts; owner to confirm), shown in two places: on the application's fact sheet in
Docs › Architecture (the permanent state) and on the change page in Process (what is missing before the next gate).
The portfolio summary stays in Process › Model checks.

## 7. First-wave screens

1. **Change page**: title, entry point, phase strip with gates and what it waits for; under each phase the documents
   expected with their state and action (Draft in chat, Open document, Validate, Review); the parallel-work banner;
   what the next gate reviews.
2. **Working document** with its thread: template sections and their state, the text, the thread column (agent and
   user turns, Insert into section), the base banner and rebase, Validate and submit → PR open, history.
3. **Process › Changes** with the document summary on each card and a "Missing documents" filter.
4. **Agent proposals**: the reconciliation and documentation pull requests waiting for a person (accept, edit, reject
   with a reason).
5. **ARB session**: agenda, ready or not, decision and conditions, written to Git, follow-up of conditions.
6. **How it works** with the phase × document × role matrix of section 3.

Built first in the Architecture board (Process area), which the production vision embeds (Docs › Architecture).

## 7b. Built (2026-11-09, canvas version 227)

In the Architecture board, Process area, and therefore in the production vision (Docs › Architecture):

- **Changes**: each card carries its document summary (published · validated · in progress · to do) and filters All ·
  Missing documents · Waiting for a gate; the title opens the change page.
- **Change page** (`page.kind = change`), kept deliberately light after the first review: phase strip with gates and
  entry point; one line for the next gate (ready, or the documents still missing); one line per collision (Same
  element with Sequence · Merge · Split, Base moved with Rebase by section); the documents grouped by phase, each
  row = title, a short secondary line only while in progress, the state chip and one action (Start · Continue · PR
  #n · @ sha). Who validates and which gate reviews are in How it works, not repeated on every row; the
  documentation health lives on the application's fact sheet only.
- **Working document** (`page.kind = doc`): the sections of the template, each with its text or "Nothing yet" and one
  link — *Draft in the assistant* when empty, *Edit* / *Rework in the assistant* when filled; a one-line status
  (progress, who validates, which gate); the Base moved line with Rebase by section (the sections changed upstream
  are marked); Validate and submit (refused while a section is empty; opens one pull request and the document becomes
  read-only until the gate). **The drafting happens in the global assistant pane, never in the page** (revised
  2026-11-09 on the product owner's remark): *Draft in the assistant* opens the pane in drafting mode — title
  "Drafting · <document>", context the change, the document's thread (user and agent turns, sources, proposals per
  section with Insert into section / Replace section), a composer that asks the assistant for the named or next
  empty section, and an "Open the document · n/m sections" chip. New conversation or Close leaves the drafting mode.
  The standalone Architecture board, which has no global pane, says so in a toast; the production vision carries the
  full flow.
- **Agent proposals** (Process): the reconciliation and documentation pull requests waiting for a person, with Accept /
  Reject with a reason.
- **How it works › Documents and gates**: the six states, the phase × document × role matrix (section 3), the three
  collision levels, the knowledge-base rule.
- **Fact sheet › Documentation**: coverage (components with a DD, interfaces with a contract), freshness (code vs
  design), origin, drift, owner confirmation.

Prototype data: `tooling/architecture-board/change_docs.py` (documents of the eight changes, four drafting threads,
three collisions, six proposals, health of six applications); logic in `arch_logic.js` (`docOf`, `changeVals`,
`docVals`, `proposalVals`, `healthOf`, `insertProposal`, `validateDoc`, `rebaseDoc`, `askThread`,
`decideCollision`, `decideProposal`); templates `CHANGEPAGE`, `DOCPAGE`, `PROPOSALS` in `build_arch.py`. Checked
with axe in light and dark (0 violations) and at 360 px. Not built yet: the ARB session view (agenda, decision written
to Git) beyond the existing ARB page, and the Sweep-side thread that drafts a DD from a run (OPP-ARC-17).

## 8. Decisions

| ID | Decision |
|---|---|
| DEC-KB-38 | Documents are drafted in the assistant, consolidated in a working document on the page, validated by a person, submitted as one pull request per document and per change, and reviewed at the gate. Agents never write a document or merge anything on their own. |
| DEC-KB-39 | A working document lives per deliverable and per change (one ADM iteration), held by the backend, never in Git before its pull request; a validated document is "waiting for the gate" until reviewed. |
| DEC-KB-40 | ARB submissions are reviewed by the domain architects and the product stakeholders; detailed design is validated by the portfolio architect with the tech leads; the RACI of section 3 applies to the other documents. |
| DEC-KB-41 | Parallel changes are detected at three levels (same document, same element, base moved) and answered by Sequence, Merge or Split, decided by the portfolio architect; rebase is by section. |
| DEC-KB-42 | The knowledge graph keeps Git-referenced nodes for what is published and adds working-document nodes with a `supersedes` edge; the chatbot never presents a draft as current. |

## 9. Open points

| ID | Question | Revisit trigger |
|---|---|---|
| OPP-ARC-14 | Gate criteria still inferred from the photo of the adjusted-flow page. | When the page (sections 2–9) is shared. |
| OPP-ARC-16 | Concurrent editing of a working document: section-level, no lock, history. | First real conflict. |
| OPP-ARC-17 | Sweep integration: when a run changes code, its DD draft comes from the run's thread; does the DD pull request ride with the code pull request or stay separate (one PR per document)? | First Sweep run on an application with a DD. |
