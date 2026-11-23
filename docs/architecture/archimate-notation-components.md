# AIToolbox — architecture notation and diagram components (Notation 2.0)

Updated 2026-11-23. Live reference: **ArchiMate Notation** artifact — https://claude.ai/artifact/6DX22osF1Dgk3o9A6Qh5Yx
Notation 2.0 · tokens 5.0.1 · PlantUML 1.2026.8 · Mermaid 11.16.

Replaces Notation 1.x (LikeC4 kinds, Angular `@aitoolbox/architecture` bindings, plateau/gap and ASD components). Diagrams are generated from YAML views (`views/`) as **PlantUML or Mermaid** (DEC-14), with one AIToolbox theme per renderer, in light and dark. Nobody styles a diagram by hand: the generator writes the include line (PlantUML) or appends the class definitions (Mermaid).

In this repository: theme files and examples in `design-system/archimate/`, generator in `tooling/archimate/`, reference page `architecture/pages/archimate-notation.html`.

## How to read this

- **Notation colours are content colours**, like chart colours: in ArchiMate, component and table views they say which layer an element belongs to. Never used for status, selection or actions.
- **The type decides everything**: layer → colour, aspect → shape, type → glyph. Never pick them separately.
- In workflows, sequences and state machines the **performer** decides the look instead (see Colour rules).
- Framework bindings are dropped pending the React + shadcn decision (DEC-04); the theme files and CSS classes are the contract.

## Theme files (`design-system/archimate/theme/`)

- `aitoolbox.puml` — one include: colours of both themes (`!$AX_THEME = "dark"` before the include switches), `!pragma layout smetana` (no Graphviz; works with the in-browser engine under strict CSP), design-system glyphs as sprites (built-in ArchiMate icons are black in dark), one procedure per element type (`AX_BusinessProcess(alias, label)`…), `AX_Agent`, `AX_Junction`, `AX_Group`, `AX_Layer`, `AX_Rel<Type>(from, to, label, dir)`, `AX_Step(label, by, change)`, `AX_Gate`, `AX_Event`, and styles for activity, state, class, sequence, component and entity diagrams.
- `aitoolbox-mermaid.json` — base theme + themeVariables per theme, and the classDefs (layers, human, agent, system, external, gate, event, decision, added, changed, moved, removed, current, grouping, lane, layer, valueobject, root, entity).

## Diagram kinds (8)

| Kind | Answers | Where | Default | PlantUML | Mermaid |
|---|---|---|---|---|---|
| ArchiMate view (layered) | Which elements across the layers take part, and how are they related? | Phases A–C | PlantUML | description diagram with archimate elements | flowchart with layer groups (no ArchiMate markers: lines name the type) |
| Business workflow | Who does which step, in which order, where does a person approve an agent's work? | Phase B processes | PlantUML | activity diagram with swimlanes | flowchart, lane written in the step (no swimlanes) |
| Process change | What does the target change in this process vs what runs today? | Phase B, every change request on a process | PlantUML | activity with change classes | flowchart with change classes |
| State machine | Which states can this object be in, and what moves it? | Phase C data (agent output, model element, change) | Mermaid | state diagram | stateDiagram-v2 |
| Domain model | Which entities, value objects, aggregates, and how do they relate? | Detailed design (refines DOB-…) | Mermaid | class diagram | classDiagram |
| Interaction | Which messages between people, agents, components, in which order? | Detailed design: one scenario | Mermaid | sequence diagram | sequenceDiagram |
| Components and interfaces | Which components, which interfaces offered/used? | Phase C application, detailed design | PlantUML | component diagram (lollipops) | flowchart with interface circles |
| Data model | Which tables, keys, joins? | Phase C data, detailed design (PostgreSQL) | Mermaid | entity diagram (IE) | erDiagram |

**Proposal** (answers the Preliminary open point "PlantUML or Mermaid"): allow both per view, with the default renderer above — PlantUML where the notation needs it (ArchiMate markers, swimlanes, lollipops), Mermaid where it renders natively in Markdown hosts.

Key rules per kind:
- Workflow: one lane per role or component; every agent output reaches a review gate before it takes effect (PRI-01) — a workflow without one fails review; decisions are diamonds with a question, branches labelled; start and end on a business event.
- Process change: one diagram, the target, with removed steps drawn where they were; marks computed from baseline (commit) vs target (branch); legend always present.
- State machine: states as written in the YAML (In review, not IN_REVIEW); transition = event [guard] / action; ✦ marks an agent transition; current state highlighted only when the view shows one instance.
- Domain model: stereotype in words («aggregate root», «entity», «value object», «enumeration»); multiplicities on both ends; written with the code, refines the model (not generated from it).
- Interaction: participants in the order they first act; calls solid, returns dashed; a review is a message from the person, never a note.
- Components: interfaces named as in the model (Agent API = API-02); lollipops in PlantUML, circles in Mermaid.
- Data model: tables in snake_case, PK/FK marked, crow's-foot on both ends.

## Colour rules

- ArchiMate, component and table views: the **layer** decides colour (layer fill + 1 px layer ink; glyph = type). An agent is an application component with `agent: true`: application colours + "✦ agent" line, never teal there.
- Workflows, sequences, state machines: the **performer** decides — person plain (surface, outline); agent teal (ai-container / ai) with "✦ agent"; system grey with "system"; review gate violet (primary-container) with a 2 px primary border; event in business colours. Current state of an instance: violet, 2 px.
- Change marks: Added + (success), Changed Δ (warning), Moved ↕ (primary), Removed − (error, dashed, struck through). Unchanged steps carry no mark. Glyph always in the label — colour is never the only cue. **Retired** is a model status, not a change mark.

## Foundations: layer tokens (unchanged)

| Layer | Token | Fill (light / dark) | Ink: border, glyph (light / dark) |
|---|---|---|---|
| Strategy | `--ax-strategy-fill` / `--ax-strategy-ink` | #F8E5C4 / #3F2E12 | #6E4A0E / #F0CB8E |
| Business | `--ax-business-fill` / `--ax-business-ink` | #FFF2B3 / #3D3500 | #5E5000 / #F2DC6E |
| Application | `--ax-application-fill` / `--ax-application-ink` | #CFEDFA / #0C3646 | #0A5570 / #90D2EC |
| Technology | `--ax-technology-fill` / `--ax-technology-ink` | #D5EDC7 / #1E3A15 | #2C5A1C / #A8D795 |
| Physical | `--ax-physical-fill` / `--ax-physical-ink` | #CBE7D4 / #163B23 | #1C5631 / #96D2A8 |
| Motivation | `--ax-motivation-fill` / `--ax-motivation-ink` | #ECDDF6 / #3A2150 | #5A2C80 / #D6B4EE |
| Implementation & migration | `--ax-implementation-fill` / `--ax-implementation-ink` | #F6DCEB / #4A1E37 | #7A2457 / #EFB3D4 |
| Other | `--ax-other-fill` / `--ax-other-ink` | #FBE3C8 / #4A2D10 | #7A4000 / #F2BE84 |

Text on a figure: `on-surface`. Measured contrast on every fill: text ≥ 10:1, ink ≥ 6.4:1, in both themes.

## Foundations: shapes (unchanged)

| Figure | Shape | Types |
|---|---|---|
| `rect` | Square corners | Resource, Business actor/role/collaboration/interface, Application component/collaboration/interface, Node, Device, System software, Technology collaboration/interface, Path, Communication network, Equipment, Facility, Distribution network, Material, Plateau, Gap, Location |
| `rounded` | Rounded corners | Capability, Value stream, Course of action, all business/application/technology functions, processes, interactions, events, services, Work package, Implementation event |
| `object` | Header band with divider | Business object, Data object |
| `contract` | Header band + second line | Contract |
| `wave` | Wavy bottom edge | Representation, Deliverable |
| `product` | Tab top-left | Product |
| `artifact` | Folded corner | Artifact |
| `chamfer` | Cut corners | Stakeholder, Driver, Assessment, Goal, Outcome, Principle, Requirement, Constraint, Meaning |
| `ellipse` | Ellipse | Value |
| `group` | Dashed outline | Grouping |
| `junction` | Dot (filled = and, hollow = or) | And junction, Or junction |

62 element types in the notation; 21 kept in the AI Toolbox model with prefixes STK, DRV, ASM, GOL, OUT, PRI, REQ, CON, CAP, VST, ACT, ROL, PRC, FUN, EVT, BSV, BOB, APC, APS, API, DOB. IDs `^[A-Z]{3}-[0-9]{2,3}$`; status draft | validated | retired. Each type's PlantUML procedure is `AX_<CamelType>`.

## Relationships

| Relationship | PlantUML procedure | PlantUML arrow | Mermaid | In model |
|---|---|---|---|---|
| Composition | `AX_RelComposition` | `*--` | `-->` + label | yes |
| Aggregation | `AX_RelAggregation` | `o--` | `-->` + label | yes |
| Assignment | `AX_RelAssignment` | `@-->` | `-->` + label | yes |
| Realization | `AX_RelRealization` | `..\|>` | `-.->` + label | yes |
| Serving | `AX_RelServing` | `-->` | `-->` + label | yes |
| Access | `AX_RelAccess` | `-[dotted]->` | `-.->` + label | yes |
| Influence | `AX_RelInfluence` | `-[dashed]->` | `-.->` + label | yes |
| Triggering | `AX_RelTriggering` | `-->>` | `==>` | yes |
| Flow | `AX_RelFlow` | `-[dashed]->>` | `-.->` + label | yes |
| Specialization | `AX_RelSpecialization` | `--\|>` | `-->` + label | no |
| Association | `AX_RelAssociation` | `--` | `---` | yes |

Mermaid has no ArchiMate end markers: its lines name the type. Use PlantUML for review.

## Components (24 — 16 new, 3 changed, 5 kept)

| Group | Component | Status | Purpose |
|---|---|---|---|
| Notation | ArchiMate figure | kept | One element: layer fill, layer ink, type glyph, name |
| Notation | Type tile | kept | Type mark before an element name in lists, tables, search, chips |
| Notation | Element ID | new | Model ID (GOL-01, PRC-04, APC-07): join key between docs, YAML, diagrams, pages |
| Notation | Model status | new | draft / validated / retired (YAML `status`) |
| Notation | Relationship line | kept | ArchiMate relationship with line style and end markers |
| Notation | Junction and grouping | kept | And/or junctions; grouping without own relationship |
| Workflow | Lane | new | Column per role or component |
| Workflow | Step | new | Unit of work, drawn by its performer |
| Workflow | Review gate | new | Named person approves an agent output (PRI-01) |
| Workflow | Event | new | Starts or ends a workflow (EVT-…) |
| Workflow | Decision | new | Branch on a question; outgoing lines carry the answer |
| State machine | State | new | One status of an object |
| State machine | Transition | new | event [guard] / action; ✦ when an agent makes it |
| Change | Change mark | changed | Replaces the New / Changed / Retired chip |
| Change | Change legend | new | Says what the marks mean on every change view |
| Detailed design | Class | new | Entity, aggregate root (2 px), value object, enumeration (grey); stereotype in words |
| Detailed design | Lifeline and message | new | Participant and messages (calls solid, returns dashed) |
| Detailed design | Interface | new | API-… offered by a component, used by others |
| Detailed design | Table and cardinality | new | Table with PK/FK, crow's-foot joins |
| Diagram frame | Diagram frame | new | One frame for every kind and both renderers: title, kind, renderer switch, fit width, text alternative, sources |
| Diagram frame | Source block | new | PlantUML / Mermaid / YAML source to copy into docs or a pull request |
| Review | Readiness chip | changed | Can the change go to the architecture board (DEC-15) |
| Review | Check row | changed | One pipeline rule (JSON Schema, references, relations, views) with failing elements |
| Review | Reviewer decision | kept | Decision on a pull request or board submission |

## Taken out

- LikeC4 kinds and views — diagrams are PlantUML or Mermaid from YAML views (DEC-14).
- Plateau track — phases E–H not run (DEC-02).
- Gap overlay — replaced by the process-change view and change marks.
- ASD section header — board submission format not defined in the new framing yet.
- New / Retired chip — now Added / Removed change marks; Retired is a model status.
- Angular bindings (`atb-ax-*`) — pending the React + shadcn decision (DEC-04).

Notation 1.x stays in `architecture/knowledge-base-example/` (LikeC4 model, `design-system/archimate/archimate.css`, Angular library) and `tooling/canvas/archimate_ds.py` as history.
