# Docs way in and architecture navigation — decisions of 2026-10-30

Follows `architecture-knowledge-base-notes.md` (DEC-KB-01 to DEC-KB-06). Implemented in the Docs lab and the
production vision on the AIToolbox design system canvas.

## DEC-KB-09 — Docs way in: A · Spaces

Docs opens on four spaces, each with its own picture: Architecture, AI wiki, Operations, New joiner. Questions are
asked from the header's search bar on every page, and answers cite their sources and version.

- **Adopted**: A · Spaces. One entry for everyone; architecture is one click away.
- **Not adopted, kept in the lab for the record**:
  - B · Application lens: good for architects and leads, weaker for the AI wiki and onboarding, which belong to no
    application.
  - C · Ask first: fast for people who know what they want, but hides what exists from people who do not. Asking stays in
    the header for everyone.

## DEC-KB-10 — The architecture space in three areas: Catalogue, Views, Process

Supersedes the four tabs of section 4 of the design notes (Landscape, Building blocks, Elements, Reviews). Each area
works the same way: an area tab, then a side list (buttons above the content on small windows). Sub-pages (element,
change, decision, review, ASD) go back with the subheader to the page they were opened from.

| Area | Side list | Main content |
|---|---|---|
| Catalogue | All elements, the ArchiMate layers, shortcuts (with detailed design, from the code, retired in the target) | Table with type tile, type, owner, plateau track, change chip, design, origin; element page with properties, relationships, views, detailed design, decisions, review and LikeC4 source |
| Views | LikeC4 views grouped by TOGAF ADM phase: Enterprise, A, B, C, D, E–F; drill-down views indented under their parent | The view on a plateau or as a gap between two plateaus; select an element to see its relationships in the view and open it in the catalogue; legend of what the view uses; view source |
| Process | Changes, Decisions, Reviews, Roadmap | Each change (one per work package) through Decide · Design · Review · Deliver with a status per step; ADR log; ARB with checks, fixes, ASD and decision; plateaus, work packages and gap table |

## DEC-KB-11 — Drill-down between views, down to the detailed design

Views link to each other the way LikeC4 navigates (`navigateTo`). A figure that has a sub-view or a detailed design
carries a drill-down button; its element card offers "Open the view" or "Open the detailed design".

- **Business**: value stream › stage of the value stream (Decide, Set up the facility) › business process (Committee
  decision: steps, roles, the application services behind each step, the data written).
- **Application**: application cooperation › inside a component. In the baseline, inside the Credit origination
  monolith (its modules, the shared Oracle schema, batch and file interfaces). In the target, inside a hexagonal
  service (facility-service, credit-request-service): inbound adapters, use cases, outbound ports, domain.
- **Detailed design**: an element inside a hexagonal view opens its DD file. A DD is split into seven files, one per
  hexagonal layer: domain, domain events, ports, application, infrastructure, API, data model. Pictures: state machine
  of the aggregate, data model (entities and relationships), the hexagon (adapters › ports › use cases › domain), API
  operations (method, path, operation, response) and tables (events, ports, adapters).
- **Way back**: the canvas panel shows the crumbs from the top view and a back button; the subheader returns from a DD
  to the view it was opened from. Migration plateaus open the landscape on that plateau.

## DEC-KB-12 — ARB in progress: what the ASD must cover

An ARB page shows, before the decision is recorded:

- the checks (structure, traceability, plateaus, ownership, decisions) with the fixes they ask for;
- **coverage**: 13 items the ASD must cover (context, need, requirements realized, overview, baseline and target views,
  gap, detailed design and contracts, NFRs, security, decisions, risks, open questions), each covered, partly covered or
  missing, computed from the ASD sections, the checks, the reviewers and the ADR status;
- reviewers per role with their decision and note (Approve, Approve with conditions, Request changes, Not required,
  Pending) — a "Request changes" puts the review in "Needs attention";
- conditions with owner, due date and status; what is asked of the board (decisions only the board can take).

The ASD mixes written sections (context, need with measures, overview, NFRs, security threats and controls, risks) and
sections generated from the model (requirements and their realizers, baseline/target/gap views, the DD table with
contract status, decisions and asks, open questions).

## Notation in pictures

Views are drawn with the AIToolbox ArchiMate notation (`aitoolbox-architecture-components.md`): `.ax-box`
figures where the type decides colour, shape and glyph; an ArchiMate relationship type with its markers on every line;
change chips, plateau track, type tiles; readiness chip, check row, ASD section header and reviewer decision in the
review pages. In the canvas prototypes, the LikeC4 web component cannot run, so the LikeC4 view chrome (panel with view
id, crumbs, back, zoom, element details) is reproduced around design-system markup. The product keeps the real
`<likec4-view>` with the AIToolbox skin (section 4 of the design notes).

## Worked example

The Corporate credit platform: microservices for the Request, Client and Facility teams; 133 elements on a rich
baseline (monolith modules, Oracle schema, IBM MQ, Control-M, SFTP, pricing workbook, BusinessObjects), 13 views, 3
plateaus (Baseline, Transition 1 · Dec 2026, Target · Jun 2027), 4 changes, 6 ADRs, 4 requirements, 3 ARB submissions:
`arb.facility.2026-14` in review (12 checks, 4 reviewers, 2 conditions, 3 asks), `arb.request.2026-09` approved with
conditions, `arb.client.2026-11` draft.
