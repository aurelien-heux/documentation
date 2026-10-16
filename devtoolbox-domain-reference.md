---
document: Devtoolbox Domain Reference
version: 0.3
status: draft
date: 2026-10-16
audience: LLMs and engineers working on Devtoolbox
language: English (canonical)
---

# Devtoolbox Domain Reference

## 0. How to use this document

- This is the canonical source for domain vocabulary, bounded contexts, invariants, and open decisions of Devtoolbox.
- When generating code, docs, prompts, or tickets, use the exact terms from section 5. Do not introduce synonyms.
- Identifiers are stable and citable: `CTX-*` bounded context, `AGG-*` aggregate, `INV-*` invariant, `EVT-*` domain event, `CMD-*` command, `DEC-*` decision, `OPP-*` open product point. Identifiers specific to a bounded context added after v0.1 carry its segment (e.g. `INV-ENV-*`, `DEC-ENV-*`, `OPP-ENV-*`, `INV-DS-*`, `DEC-DS-*`). Design-system rules use `DSR-*` (section 14).
- Anything marked `v1` is decided for the first release. Anything marked `future` is intended but not designed.
- If a request contradicts an `INV-*`, flag the conflict instead of complying silently.

## 1. Platform summary

- **What**: Devtoolbox is an internal web platform for IT development teams.
- **Today**: exposes a design-system Storybook, Zensical documentation of team-built applications, and internal process documentation (onboarding, release, etc.).
- **Ambition**: an AI-augmented, agent-oriented SDLC. An LLM assistant supports teams; agents perform SDLC work (implementation up to PR is already done with OpenHands, triggered manually from a ticket).
- **Positioning**: internal developer portal (Backstage-like) extended with delivery orchestration and agents.
- **Infrastructure context**: internal cloud with Kubernetes clusters; deployments through Helm/Ansible (driven by Jenkins) and ArgoCD; a dedicated Git repository holds Environment descriptors.

## 2. Domain classification

| Domain | Type | Rationale |
|---|---|---|
| Software Catalog | core | Backbone; every other context keys on its identifiers |
| Delivery Orchestration | core | The differentiator: change flowing through the SDLC with agents |
| Team Assistant | core | Conversational front door to knowledge and to the SDLC |
| Documentation (incl. Playbooks) | supporting | Existing asset; source of knowledge and agent policies |
| Design System | supporting | Existing asset; constraint on UI artifacts |
| Knowledge Index | supporting | Retrieval layer shared by Assistant and agents |
| Agent Runtime | supporting | Executes agents; wraps engines such as OpenHands |
| Environment Management | supporting | Existing infrastructure; value lies in visibility, self-service Deployment and Reservations |
| Integrations | generic | Anti-corruption layer to external systems |
| Identity & Access | generic | Cross-cutting authentication and authorization |

## 3. Bounded contexts

### CTX-CAT — Software Catalog
- **Type**: core
- **Purpose**: register applications, their Modules, teams, ownership, repositories, dependencies.
- **Owns**: AGG-APPLICATION (incl. entity Module), AGG-TEAM, entity Repository (referenced), value objects Ownership, Contacts, Links, Product.
- **Publishes**: EVT-APPLICATION-REGISTERED, EVT-OWNERSHIP-TRANSFERRED, EVT-LIFECYCLE-CHANGED, EVT-REPOSITORY-LINKED, EVT-DEPENDENCY-DECLARED, EVT-MODULE-DECLARED.
- **Consumes**: nothing in v1. Future: team sync from Integrations (OPP-01).
- **Exposes as shared kernel**: `applicationSlug`, `applicationSlug/moduleName`, `teamId` only.
- **Note**: Environments are owned by CTX-ENV. `Application.environments[]` is a read projection of Effective placements from CTX-ENV.

### CTX-DOC — Documentation
- **Type**: supporting
- **Purpose**: publish Zensical doc sites for applications and processes; hold Playbooks.
- **Owns**: Doc Site, AGG-PLAYBOOK (Playbook, Step, Step binding).
- **Publishes**: EVT-DOCSITE-PUBLISHED, EVT-PLAYBOOK-PUBLISHED.
- **Rule**: agents never edit Playbooks directly; changes arrive as Artifacts through a Checkpoint (INV-12).

### CTX-DS — Design System
- **Type**: supporting
- **Purpose**: expose the Storybook, UI Components, Variants, Stories, tokens, brand assets and Angular Material themes.
- **Owns**: UI Component, Variant, Story, Token, Brand asset, Theme.
- **Publishes**: EVT-STORYBOOK-BUILT.
- **Role for agents**: source of Quality gates on UI Artifacts; rules in section 14 (`DSR-*`, INV-DS-*).
- **Current release**: Material Design 3, palette M · Night & neon, tokens 4.1.0, Angular Material 21 (M2) and 22 (M3).

### CTX-KI — Knowledge Index
- **Type**: supporting
- **Purpose**: ingest content from Sources and answer retrieval queries with Evidence.
- **Owns**: Source, Chunk, Provenance, Freshness.
- **Consumes**: EVT-DOCSITE-PUBLISHED, EVT-STORYBOOK-BUILT, EVT-APPLICATION-REGISTERED, EVT-PLAYBOOK-PUBLISHED, EVT-MODULE-DECLARED, EVT-ENVIRONMENT-SYNCED, EVT-ROLLOUT-COMPLETED. Future: Run Traces.
- **Contract**: `Query(text, scope) -> Evidence[]`. Shared by CTX-AST and CTX-ART (Context Assembly).
- **Ingestion**: event-driven, no polling in v1.

### CTX-AST — Team Assistant
- **Type**: core
- **Purpose**: grounded conversational help; front door to the SDLC.
- **Owns**: Conversation, Scope, Answer, Intent, Feedback, Grounding policy.
- **Consumes**: CTX-KI Evidence; CTX-ORC events for status questions; CTX-ENV events for Environment and Reservation questions.
- **Acts via**: CMD-DRAFT-BRIEF, CMD-REQUEST-RUN on CTX-ORC only. Never calls an Engine. Future: CTX-ENV commands (OPP-ENV-07).

### CTX-ORC — Delivery Orchestration
- **Type**: core
- **Purpose**: move a Work item through SDLC Phases with agents and humans; includes Intake.
- **Owns**: AGG-WORK-ITEM, Brief, Origin, Phase, Agent role, Artifact, Checkpoint, Handoff, Autonomy policy, Quality gate, Policy.
- **Consumes**: CTX-CAT shared kernel; Briefs from CTX-INT (tickets) and CTX-AST (chat); Playbooks from CTX-DOC as Policies. Future: Environments from CTX-ENV as targets of the test and release Phases.
- **Publishes**: EVT-WORK-ITEM-CREATED, EVT-HANDOFF, EVT-CHECKPOINT-REQUESTED, EVT-CHECKPOINT-DECIDED.
- **Drives**: CTX-ART through CMD-REQUEST-RUN.

### CTX-ART — Agent Runtime
- **Type**: supporting
- **Purpose**: execute one Run of one Agent with a Context pack and a set of Capabilities, on an Engine.
- **Owns**: Agent, Engine, Capability, Run, Trace, Context pack (assembled here via CTX-KI).
- **Publishes**: EVT-RUN-STARTED, EVT-APPROVAL-REQUESTED, EVT-APPROVAL-GRANTED, EVT-RUN-COMPLETED, EVT-RUN-FAILED.
- **First Engine**: OpenHands, developer role, implement Phase.

### CTX-ENV — Environment Management
- **Type**: supporting
- **Purpose**: list existing Environments, show what runs on them, and let users place a Module branch on an Environment, protected by Reservations.
- **Owns**: AGG-ENVIRONMENT (Environment, Reservation, Placement), AGG-DEPLOYMENT (Deployment, Rollout), value objects Observed placement, Effective placement, Drift, Upstream lag.
- **Consumes**: CTX-CAT shared kernel (`applicationSlug`, `applicationSlug/moduleName`); EVT-MODULE-DECLARED; Environment descriptors and Observer readings via CTX-INT.
- **Publishes**: EVT-ENVIRONMENT-SYNCED, EVT-ENVIRONMENT-RESERVED, EVT-RESERVATION-EXTENDED, EVT-RESERVATION-RELEASED, EVT-RESERVATION-EXPIRED, EVT-DEPLOYMENT-REQUESTED, EVT-DEPLOYMENT-SUCCEEDED, EVT-DEPLOYMENT-FAILED, EVT-ROLLOUT-COMPLETED, EVT-ROLLOUT-FAILED, EVT-DRIFT-DETECTED, EVT-UNRESERVED-CHANGE-DETECTED.
- **Acts via**: CTX-INT connectors only: Git connector (descriptor PRs), Deployer connectors, Observer connectors (INV-07, INV-ENV-03).
- **Rule**: Devtoolbox never creates or deletes an Environment; it only changes Placements through auto-merge PRs (INV-ENV-01).
- **v1 scope**: non-production Environments only (DEC-ENV-01). Agent-driven Deployments are `future`.

### CTX-INT — Integrations
- **Type**: generic
- **Purpose**: anti-corruption layer to external systems: OpenHands (Engine adapter), Git hosting (incl. the Descriptor repository), CI (Jenkins), Deployers (Helm/Ansible, ArgoCD), Observers (Kubernetes, ArgoCD, Jenkins), ticketing, chat, org referential (future).
- **Owns**: Engine adapter, Connector (incl. Git, Deployer and Observer connectors), CI context mapping (`ciContextId`), credentials.
- **Rule**: the only place holding external credentials (INV-07).

### CTX-IAM — Identity & Access
- **Type**: generic, cross-cutting
- **Purpose**: SSO, users, roles, scope checks. Supplies the current user to every context.
- **Note**: teams are NOT sourced from SSO/IdP (see DEC-01).

## 4. Context map

| Upstream | Downstream | Relationship | Payload |
|---|---|---|---|
| CTX-CAT | all | shared kernel | `applicationSlug`, `applicationSlug/moduleName`, `teamId` |
| CTX-DOC | CTX-KI | published language, conformist downstream | doc content, Playbooks, events |
| CTX-DS | CTX-KI | published language, conformist downstream | component metadata, events |
| CTX-DOC | CTX-ORC | published language | Playbooks as Policies and Step bindings |
| CTX-KI | CTX-AST | customer–supplier | `Query -> Evidence[]` |
| CTX-KI | CTX-ART | customer–supplier | `Query -> Evidence[]` for Context packs |
| CTX-AST | CTX-ORC | customer (commands only) | CMD-DRAFT-BRIEF, CMD-REQUEST-RUN |
| CTX-ORC | CTX-ART | upstream driver | CMD-REQUEST-RUN; Artifacts and Traces return as events |
| CTX-ART | CTX-INT | anti-corruption layer | Engine and Capability calls |
| CTX-INT | CTX-ORC | supplier | ticket Briefs with `origin = ticket` |
| CTX-INT | CTX-CAT | future | org-referential team sync (OPP-01) |
| CTX-CAT | CTX-ENV | shared kernel | `applicationSlug`, `applicationSlug/moduleName`, EVT-MODULE-DECLARED |
| CTX-INT | CTX-ENV | anti-corruption layer | Environment descriptors, Observer readings, Build and Rollout events from CI |
| CTX-ENV | CTX-INT | anti-corruption layer | descriptor PRs (Git connector), Deployer calls |
| CTX-ENV | CTX-KI | published language | Environment list, Effective placements, events |
| CTX-ENV | CTX-AST | published language | Environment and Reservation status for questions |
| CTX-AST | CTX-ENV | future, customer (commands only) | CMD-RESERVE-ENVIRONMENT, CMD-REQUEST-DEPLOYMENT, subject to Autonomy policy |
| CTX-ENV | CTX-ORC | future, supplier | Environments as targets of the test and release Phases |
| CTX-IAM | all | cross-cutting | user, roles, scope; admin role for CMD-FORCE-RELEASE |

## 5. Ubiquitous language

Format: **Term** (context) — definition. Notes in italics.

### Catalog (CTX-CAT)
- **Application** — a deliverable owned by exactly one Team. Fields: `slug`, `name`, `kind` (service | frontend | library | job), `lifecycle`, `ownerTeamId`, `ownershipSince`, `productId?`, `ciContextId?`, `repositories[]`, `modules[]`, `dependencies[]`, `contacts[]`, `links`. *`environments[]` is a read projection from CTX-ENV, not stored here.*
- **Slug** — stable, unique, immutable identifier of an Application. The join key across all contexts.
- **Module** — a deployable unit of an Application (a Helm chart, an ArgoCD application). Fields: `name`, `repository`, `deployer`. Declared in the Manifest (DEC-02). Referenced as `applicationSlug/moduleName`.
- **CI context id** — `Application.ciContextId`, the key of the Application in the CI/CD system. *External alias only: used in CTX-INT mappings, never in UI, docs or prompts.*
- **Team** — an organisational unit owning Applications. `v1`: declared manually in Devtoolbox.
- **Ownership** — dated link between an Application and a Team. `v1`: current owner plus `ownershipSince`; full history is `future`.
- **Contacts** — named people on an Application (tech lead, product owner). Independent of Team; fallback when a Team is stale.
- **Product** — grouping of related Applications. `v1`: value object on Application.
- **Repository** — Git source referenced by `provider/org/name`. May be shared by several Applications (monorepo). Holds the manifest.
- **Manifest** — `devtoolbox.yaml` in a Repository declaring catalog data. See DEC-02.
- **Dependency** — reference from one Application to another by slug.
- **Links** — URLs to doc site, Storybook, runbook, dashboards.
- **Lifecycle** — experimental → active → deprecated → retired.
- **Stale ownership** — `future`; ownership not confirmed within N days or whose Team no longer exists.
- **Team overlay**, **Ownership confirmation**, **Referential drift** — `future`, tied to OPP-01.

### Documentation and Design System (CTX-DOC, CTX-DS)
- **Doc Site** — a published Zensical site tied to an Application or a process.
- **Playbook** — a versioned, human-readable procedure made of ordered Steps. Lives in CTX-DOC.
- **Step** — an ordered unit of a Playbook. May be bound to a Capability via a Step binding.
- **Step binding** — link "Step N of Playbook P is performed by Capability C". Unbound Steps stay manual.
- **UI Component** — a design-system element with Variants and Stories. *Always say "UI Component", never "component" alone.*
- **Variant**, **Story**, **Token** — Storybook concepts, used as-is.
- **Role** — an MD3 colour token name (`primary`, `secondary-container`, `ai`…). UI code references Roles, never hex values.
- **Extended role** — a Role outside the MD3 scheme: `ai`, `success`, `warning`, `logo-box`, `on-logo-box`, `logo-cursor`.
- **Brand asset** — logo, favicon, app icon, brand loader, state mark or chatbot mark file published by CTX-DS.
- **State mark** — the feedback icon: the logo construction with the state (success, info, warning, error) in its corner badge.
- **Theme** — an Angular Material theme file generated from the tokens (`theme.m2.scss`, `theme.m3.scss`).

### Knowledge Index (CTX-KI)
- **Source** — a registered content origin (Doc Site, Storybook, repository files, Playbooks, Catalog, Environments, Traces). Bound to an Application or marked `global`.
- **Chunk** — an indexed fragment with Provenance.
- **Provenance** — `source`, `applicationSlug`, `version`, `url`, `updatedAt`.
- **Freshness** — gap between Source `updatedAt` and `indexedAt`. Always displayed.
- **Query** — `(text, scope)` request to the index.
- **Evidence** — ranked Chunks with Provenance returned by a Query.

### Assistant (CTX-AST)
- **Conversation** — a chat session with a Scope.
- **Scope** — an Application, a Team, or `global`. Narrows retrieval and unlocks Intents.
- **Answer** — an assistant reply; always carries Sources (the Evidence used) or states the gap.
- **Grounding policy** — rule that Answers rely on Evidence only.
- **Intent** — an allowed action: answer, locate doc, report Work item status, report Environment status, draft Brief, request Run.
- **Feedback** — user rating on an Answer, stored with the Evidence used.

### Delivery Orchestration (CTX-ORC)
- **Work item** — a change to make (feature, bug, tech debt), bound to one Application, created from a Brief. In exactly one Phase at a time.
- **Brief** — normalized input for agents: title, goal, constraints, acceptance criteria, target Application, Markdown body.
- **Origin** — where a Brief came from: `ticket` | `chat` | `manual`.
- **Intake** — the process turning any Origin into a Brief and a Work item.
- **Phase** — refine → design → implement → review → test → release → operate. Applications may use a subset.
- **Agent role** — analyst | developer | reviewer | tester | release manager. Defined by Capabilities, Context pack, and Policies.
- **Artifact** — output of a Phase: spec, plan, PR, test report, release notes, doc update. Handoff currency. *Never a CI build output: that is a Package.*
- **Checkpoint** — human decision point between Phases. Generalises Approval at the orchestration level.
- **Handoff** — event moving a Work item to the next Phase, carrying its Artifacts.
- **Autonomy policy** — per (Application, Phase, Agent role): `propose` | `execute-with-checkpoint` | `autonomous`. Platform default, Application override.
- **Quality gate** — automated check on an Artifact (e.g., design-system conformance on UI).
- **Policy** — a rule an agent must follow, sourced from Playbooks.
- **Workflow** — executable projection of a Playbook version for an Application. *Use "Workflow", never "pipeline", for agentic chains.*

### Agent Runtime (CTX-ART)
- **Agent** — LLM-driven executor holding Capabilities, scoped to one Application and one Run.
- **Engine** — the system that actually runs an Agent (first: OpenHands). Wrapped, never exposed.
- **Engine adapter** — CTX-INT component translating a Run into engine input and engine output into Artifact and Trace.
- **Capability** — a single action an Agent may perform (open PR, trigger CI, post to chat). Has a `risk level`. *Use "Capability", never "tool".*
- **Run** — one execution of an Agent for a Work item Phase. Lifecycle in section 9.
- **Approval** — human decision recorded on a Run for a high-risk Capability.
- **Trace** — full log of what the Agent read, decided, and did.
- **Context pack** — Brief + assembled Evidence (catalog entry, docs, design-system rules, Policies, recent Traces) given to an Agent.

### Environment Management (CTX-ENV)
- **Environment** — a long-lived, pre-existing deployment target, declared in an Environment descriptor. Fields: `name`, `tier`, `cluster`, `namespaces[]`, `upstream?`, `trackedBranch?`, `updateMode?`. Shared by several Applications.
- **Upstream environment** — an Environment fully deployed from one Git flow branch (`develop`, `master`, `release/*`). Serves as fallback for every Module not placed locally on the Environments linked to it. *Always write "Upstream environment" in full; bare "upstream" is DDD only.*
- **Tracked branch** — the Git flow branch an Upstream environment follows.
- **Update mode** — how an Upstream environment follows its Tracked branch: `automatic` (each commit) or `team-triggered` (release branches, by a team job).
- **Environment descriptor** — the file in the Descriptor repository that declares an Environment and its Placements. Source of truth.
- **Descriptor repository** — the Git repository holding all Environment descriptors.
- **Placement** — declaration "Module M runs on Environment E from branch B", stored in the Environment descriptor.
- **Local placement** — a Placement on the Environment itself.
- **Effective placement** — what a caller reaches for a Module on an Environment: the Local placement if one exists, otherwise the Upstream environment's placement. *The UI always shows which of the two applies.*
- **Observed placement** — what one Observer reports for a Module on an Environment: `commit`, `packageVersion`, `source`, `observedAt`.
- **Package** — the versioned deployable output of a Build of a Module for one commit (container image, chart version). *Never "artifact": Artifact is CTX-ORC only.*
- **Build** — CI execution producing a Package from a commit.
- **Deployment** — a user request to place a Module branch on an Environment. Opens an auto-merge PR on the Descriptor repository. Happens once per Placement change.
- **Rollout** — one Package going live on an Environment. Triggered by CI on each new commit of the placed branch; no descriptor change.
- **Deployer** — the mechanism applying a Placement: `helm-ansible` or `argocd`. Configured per Module.
- **Observer** — a CTX-INT connector reading one runtime source (Kubernetes, ArgoCD, Jenkins).
- **Drift** — disagreement between a Placement and Observed placements, or between two Observers. Always shown, never hidden.
- **Upstream lag** — gap between an Upstream environment's running commits and the head of its Tracked branch. A kind of Drift.
- **Reservation** — a time-boxed lock. Fields: `scope` (`environment` | `application` | `module`), `target`, `holder`, `reason`, `startsAt`, `expiresAt`.
- **Holder** — who owns a Reservation: a user in v1; a Work item in `future` (agent-driven).
- **Unreserved change** — a descriptor commit made outside Devtoolbox that touches a Module covered by someone else's Reservation. Detected and notified, not prevented.

## 6. Reserved and ambiguous words

| Word | Do not use for | Use instead |
|---|---|---|
| component | UI element vs software module | UI Component; Application, Module or Repository |
| tool | agent action vs Devtoolbox feature | Capability; feature |
| pipeline | agentic chain | Workflow (agentic); pipeline = CI only |
| context | conversation or agent input vs DDD boundary | Conversation; Context pack; bounded context (DDD only) |
| context (CI/CD) | an Application in the CI/CD system | Application; `ciContextId` in CTX-INT mappings only |
| approval | phase gate vs run-level gate | Checkpoint (between Phases); Approval (inside a Run) |
| upstream | an Environment others fall back on | Upstream environment (in full); bare "upstream" = DDD context map only |
| artifact (CI) | a build output | Package; Artifact = CTX-ORC Phase output only |
| deploy / deployment | each CI push going live | Deployment (Placement change, once); Rollout (each Package) |
| lock | a Reservation | Reservation |
| env | Environment | Environment (in docs and prompts) |

## 7. Invariants

| ID | Context | Rule |
|---|---|---|
| INV-01 | CAT | Every Application has exactly one owning Team at all times. |
| INV-02 | CAT | `slug` never changes once published; renaming changes `name` only. |
| INV-03 | CAT | Retired Applications keep their record; hidden from navigation only. |
| INV-04 | CAT | Dependencies reference registered slugs only. |
| INV-05 | ORC | A Work item is in exactly one Phase at a time. |
| INV-06 | ORC | No Handoff without required Artifacts and passing Quality gates. |
| INV-07 | ART/INT | Agents act only through Capabilities; credentials live in CTX-INT only. |
| INV-08 | ART | High-risk Capabilities always require Approval; no agent override. |
| INV-09 | ART | Every Run references an exact Playbook version and Workflow version, and is scoped to one Application. |
| INV-10 | ORC | A Run never starts without a Brief bound to exactly one Application. |
| INV-11 | ART | Every Artifact traces back to a Run and its Trace. |
| INV-12 | DOC | Agents never edit Playbooks directly; proposed changes are Artifacts passing a Checkpoint. |
| INV-13 | AST | Every Answer cites Evidence or explicitly states the gap. |
| INV-14 | AST | The Assistant acts only via CTX-ORC commands; autonomy policies and Checkpoints apply to it. |
| INV-15 | KI/AST | Retrieval scope never exceeds the user's access. |
| INV-16 | KI | Freshness is always shown; stale Evidence is dated, never hidden. |
| INV-ENV-01 | ENV | Devtoolbox never creates or deletes an Environment; it changes Placements only, through auto-merge PRs on the Descriptor repository. |
| INV-ENV-02 | ENV | A Deployment targets exactly one Module, one branch and one Environment. |
| INV-ENV-03 | ENV/INT | Deployments, Observers and descriptor PRs go through CTX-INT connectors only (extends INV-07). |
| INV-ENV-04 | ENV | Deploy is a Capability whose risk level depends on Environment `tier`; agent-driven Deployments fall under INV-08 and OPP-03. |
| INV-ENV-05 | ENV | Reservations on the same Environment never overlap: an `environment` Reservation excludes all others; an `application` Reservation excludes `module` Reservations on its Modules. |
| INV-ENV-06 | ENV | A Deployment of Module M on Environment E is refused if another Holder has an active Reservation covering (E, M). |
| INV-ENV-07 | ENV | Every Reservation has an `expiresAt`; no open-ended Reservation. The Holder may extend it. |
| INV-ENV-08 | ENV | Displayed runtime state always shows its Observer `source` and `observedAt` (same spirit as INV-16). |
| INV-ENV-09 | CAT | A Module belongs to exactly one Application; its name is unique within that Application. |
| INV-ENV-10 | ENV | An Upstream environment has no Upstream environment itself (no chains). |
| INV-ENV-11 | ENV | An Environment links to at most one Upstream environment. |
| INV-ENV-12 | ENV | Upstream environments are never targets of self-service Deployments and are never reservable. |
| INV-ENV-13 | ENV | Every Rollout traces back to its Placement, and every Placement to the Deployment or external commit that created it. |
| INV-ENV-14 | ENV | v1 manages non-production Environments only (DEC-ENV-01). |

*Accepted behaviour (CTX-ENV)*: a Reservation protects which branch is placed, not commits on that branch. A push to a reserved Module's branch triggers a Rollout regardless of the Holder.

## 8. Domain events

| ID | Context | Meaning | Typical subscribers |
|---|---|---|---|
| EVT-APPLICATION-REGISTERED | CAT | new Application in the catalog | KI, ORC |
| EVT-OWNERSHIP-TRANSFERRED | CAT | owning Team changed | AST, KI |
| EVT-LIFECYCLE-CHANGED | CAT | lifecycle transition | KI, portal |
| EVT-REPOSITORY-LINKED | CAT | Repository attached to Application | KI, INT |
| EVT-DEPENDENCY-DECLARED | CAT | dependency added | portal |
| EVT-MODULE-DECLARED | CAT | Module added to an Application via manifest | ENV, KI |
| EVT-DOCSITE-PUBLISHED | DOC | new doc site version | KI |
| EVT-PLAYBOOK-PUBLISHED | DOC | new Playbook version | KI, ORC |
| EVT-STORYBOOK-BUILT | DS | new Storybook build | KI |
| EVT-WORK-ITEM-CREATED | ORC | Brief accepted into a Work item | AST |
| EVT-HANDOFF | ORC | Work item moved to next Phase | AST, ART |
| EVT-CHECKPOINT-REQUESTED | ORC | human decision needed | AST, notifications |
| EVT-CHECKPOINT-DECIDED | ORC | human decided | ORC, AST |
| EVT-RUN-STARTED | ART | Run began | ORC, AST |
| EVT-APPROVAL-REQUESTED | ART | high-risk Capability awaiting Approval | ORC, notifications |
| EVT-APPROVAL-GRANTED | ART | Approval recorded | ART |
| EVT-RUN-COMPLETED | ART | Run succeeded with Artifacts | ORC, KI |
| EVT-RUN-FAILED | ART | Run failed | ORC, AST |
| EVT-ENVIRONMENT-SYNCED | ENV | Environment list or Placements refreshed from the Descriptor repository | KI, AST |
| EVT-ENVIRONMENT-RESERVED | ENV | Reservation created | AST, notifications |
| EVT-RESERVATION-EXTENDED | ENV | `expiresAt` moved later | notifications |
| EVT-RESERVATION-RELEASED | ENV | Reservation ended by Holder or admin | AST, notifications |
| EVT-RESERVATION-EXPIRED | ENV | Reservation reached `expiresAt` | AST, notifications |
| EVT-DEPLOYMENT-REQUESTED | ENV | Deployment accepted, descriptor PR to open | INT, AST |
| EVT-DEPLOYMENT-SUCCEEDED | ENV | PR merged and first Rollout succeeded | AST, KI, notifications |
| EVT-DEPLOYMENT-FAILED | ENV | PR, Build or first Rollout failed | AST, notifications |
| EVT-ROLLOUT-COMPLETED | ENV | a Package went live on an Environment | AST, KI |
| EVT-ROLLOUT-FAILED | ENV | a Package failed to go live | AST, notifications |
| EVT-DRIFT-DETECTED | ENV | Placement and Observed placements disagree, or Observers disagree | AST, notifications |
| EVT-UNRESERVED-CHANGE-DETECTED | ENV | external descriptor commit touched a reserved Module | notifications (Holder) |
| EVT-TEAM-SYNCED-FROM-REFERENTIAL | INT→CAT | `future` (OPP-01) | CAT |

## 9. Lifecycles

- **Application.lifecycle**: `experimental -> active -> deprecated -> retired`
- **Run.status**: `queued -> running -> awaiting_approval -> running -> succeeded | failed | cancelled`
- **Work item.phase**: `refine -> design -> implement -> review -> test -> release -> operate` (subset per Application)
- **v1 slice**: Work item → implement (OpenHands, `autonomous`) → PR Artifact → Handoff → review (human Checkpoint) → done. Other Phases visible but manual.
- **Deployment.status**: `requested -> pr_opened -> merged -> first_rollout -> succeeded | failed`. `requested` checks INV-ENV-06 and INV-ENV-12.
- **Rollout.status**: `building -> rolling_out -> succeeded | failed`. `building` is skipped when a Package already exists for the commit.
- **Reservation.status**: `active -> released | expired`. `active` may be extended any number of times by the Holder.
- **Upstream environment update**: `automatic` = a Rollout on each commit of the Tracked branch; `team-triggered` = a Rollout when the team job runs.
- **CTX-ENV v1 slice**: browse Environments → reserve (optional) → request Deployment of a Module branch → auto-merge PR → Build → first Rollout → subsequent Rollouts on each push → release Reservation.

## 10. Commands

| ID | Context | Input | Effect |
|---|---|---|---|
| CMD-REGISTER-APPLICATION | CAT | manifest or form | creates Application, emits EVT-APPLICATION-REGISTERED |
| CMD-TRANSFER-OWNERSHIP | CAT | slug, teamId | updates Ownership, emits event |
| CMD-DRAFT-BRIEF | ORC | free text, origin, slug | produces a Brief for confirmation |
| CMD-CREATE-WORK-ITEM | ORC | Brief, slug | creates Work item in first Phase |
| CMD-REQUEST-RUN | ORC→ART | workItemId, phase | starts a Run per Autonomy policy |
| CMD-DECIDE-CHECKPOINT | ORC | workItemId, decision | records human decision, may trigger Handoff |
| CMD-GRANT-APPROVAL | ART | runId, capability, decision | unblocks or cancels the Run |
| CMD-SYNC-ENVIRONMENTS | ENV | descriptor commit or schedule | refreshes Environments and Placements, emits EVT-ENVIRONMENT-SYNCED |
| CMD-RESERVE-ENVIRONMENT | ENV | environment, scope, target, reason, expiresAt | creates a Reservation if INV-ENV-05 holds |
| CMD-EXTEND-RESERVATION | ENV | reservationId, expiresAt | moves `expiresAt`, Holder only |
| CMD-RELEASE-RESERVATION | ENV | reservationId | ends the Reservation, Holder only |
| CMD-FORCE-RELEASE | ENV | reservationId, reason | ends the Reservation, admin only, Holder notified |
| CMD-REQUEST-DEPLOYMENT | ENV | environment, applicationSlug/moduleName, branch | checks Reservations, opens auto-merge PR, starts the Deployment |
| CMD-REMOVE-PLACEMENT | ENV | environment, applicationSlug/moduleName | removes the Local placement via PR; the Module falls back to the Upstream environment |

## 11. Decisions (v1)

| ID | Decision | Rationale |
|---|---|---|
| DEC-01 | Teams are declared manually in Devtoolbox; no sync with org referential or SSO. | Referential lags reality and is not in the IdP; keep Team as a separate entity with a stable id so a sync can be added later. |
| DEC-02 | Catalog source of truth is a `devtoolbox.yaml` manifest per Repository, projected into the catalog, with UI override for ownership and lifecycle. | Manifest is agent-editable and Git-reviewed; ownership and lifecycle change by decision, not by commit. Leaning, confirm before build. |
| DEC-03 | Autonomy is a per-(Application, Phase, Agent role) policy, not a global setting. | Implement Phase is already autonomous up to PR; other Phases are not. |
| DEC-04 | OpenHands is wrapped as an Engine behind an Engine adapter in CTX-INT. | Keep Orchestration engine-agnostic. |
| DEC-05 | All Intake Origins (ticket, chat, manual Markdown) converge on one Brief and one CMD-REQUEST-RUN. | Engine adapter never knows the Origin; Devtoolbox adds the Context pack regardless. |
| DEC-06 | Knowledge Index ingestion is event-driven. | Freshness tied to publication events; avoids polling. |
| DEC-07 | Reserved words per section 6 are enforced in code, docs, and prompts. | Prevents the component / tool / pipeline / context ambiguities. |
| DEC-ENV-01 | v1 covers non-production Environments only. | Only non-production Environments exist in the current list; production will require Approval when added. |
| DEC-ENV-02 | The Descriptor repository is the source of truth for Environments and Placements. | Already used by CI/CD; Git-reviewed; Devtoolbox projects it rather than duplicating it. |
| DEC-ENV-03 | Devtoolbox changes Placements through auto-merge PRs, never direct commits. | Traceability and review hooks at low latency. |
| DEC-ENV-04 | A Placement declares a branch; the running commit and Package are observed, not declared. | CI builds and rolls out each push; no descriptor conflict per commit. |
| DEC-ENV-05 | Deployment (Placement change) and Rollout (Package live) are separate concepts. | One user intent produces many Rollouts over time. |
| DEC-ENV-06 | Reservation is one concept with three scopes: `environment`, `application`, `module`. | Shared Environments need fine locks; full Environment locks stay possible. |
| DEC-ENV-07 | Runtime state is read from several Observers: Kubernetes (what runs), ArgoCD (desired vs synced), Jenkins (Deployment and Rollout history). | No single tool knows everything; disagreement surfaces as Drift. |
| DEC-ENV-08 | The CI/CD "context" maps to Application; no new Devtoolbox term. | Avoids a fourth meaning of "context" (DEC-07). |

## 12. Open product points

| ID | Question | Why deferred | Revisit trigger |
|---|---|---|---|
| OPP-01 | Should Teams sync from the org referential, and how are drift and confirmation handled? | Referential not in SSO, lags changes, access mode unknown. | Referential exposes an API, or stale ownership becomes a visible pain. |
| OPP-02 | Where do Workflow definitions live: in the repo next to the manifest, or in Devtoolbox? | Depends on who edits them (agents vs product) and review needs. | First Workflow beyond implement-to-PR. |
| OPP-03 | Who classifies Capability risk levels, and per Application or globally? | Governance question. | First high-risk Capability (deploy, merge to main). |
| OPP-04 | Does the review Phase get an agent (automated first pass) or stay fully human? | Trust and workload trade-off. | After the v1 slice is stable. |
| OPP-05 | Is a Brief editable after a Run started, or does a change create a new Work item version? | Traceability vs convenience. | First real mid-Run change request. |
| OPP-06 | Is all content visible to everyone, or are some Sources team-restricted? | Decides whether access control enters CTX-KI in v1. | Before indexing anything sensitive. |
| OPP-07 | Which Sources to index first; is Storybook indexed as text or only linked? | Effort vs value. | Knowledge Index v1 scoping. |
| OPP-ENV-01 | Exact Environment descriptor format and field mapping. | No sample reviewed yet. | Before building the descriptor projection. |
| OPP-ENV-02 | Default Reservation duration, maximum, and extension rules. | Needs usage data. | First Reservation conflicts in practice. |
| OPP-ENV-03 | Who is notified on Rollout failure: Holder, branch author, or both? | Notification channel not designed (§13). | Notifications design. |
| OPP-ENV-04 | Should Reservations be enforced in the Descriptor repository CI, not only in Devtoolbox? | Requires a CI check calling Devtoolbox. | Unreserved changes become frequent. |
| OPP-ENV-05 | Observer precedence when sources disagree beyond Drift display. | Depends on reliability of each source. | First recurrent Drift between Observers. |
| OPP-ENV-06 | Production Environments: scope, Approval flow, Capability risk level. | Out of v1 (DEC-ENV-01). | First production Environment in the list. |
| OPP-ENV-07 | Agent-driven Deployments: Holder as Work item, Environments as targets of test and release Phases. | Depends on OPP-03 and OPP-04. | First agent Phase beyond implement. |
| OPP-ENV-08 | Does a Deployment of a branch on an Environment need the branch to exist in all Module repositories, or only the target Module's? | Multi-repository Applications not yet observed. | First multi-Module feature branch. |

## 13. Not yet modeled

- Portal navigation and search façade (assumed thin, over CTX-CAT and CTX-KI).
- Analytics and usage telemetry (generic).
- Multi-tenancy: assumed single organisation.
- Notifications channel (chat, email) — referenced by events, not designed.
- Agent roles beyond developer: analyst, reviewer, tester, release manager are named but not specified.
- Production Environments and agent-driven Deployments (OPP-ENV-06, OPP-ENV-07).

## 14. Design system rules (CTX-DS)

These rules are the published language of CTX-DS and the content of the design-system Quality gate on UI Artifacts (INV-06, INV-DS-*). Identifiers: `DSR-*` rule, `INV-DS-*` invariant, `DEC-DS-*` decision. Brand name on screen: **AIToolbox** (one word); the platform remains Devtoolbox in domain vocabulary.

### 14.1 Sources of truth

| Item | Location | Version |
|---|---|---|
| Tokens (colour, type, shape, elevation, motion) | Design System artifact `tokens.json`; brand package `css/tokens.css`, `css/design-tokens.json` | 4.1.0 |
| Per-UI-Component rules with Angular Material tokens (M2 and M3) | project doc `claude/aitoolbox-component-rules.md`; Design System artifact `component-rules.md`; brand package `angular/COMPONENT-RULES.md` | 4.1.0 |
| Angular Material themes | `angular/theme.m2.scss` (Angular Material 21), `angular/theme.m3.scss` (Angular Material 22), `_theme-colors.scss`, `mat-sys-bridge.css` | compiled on 21.2 and 22.2 |
| Brand assets (logos, favicon, app icon, loaders, state marks, chatbot mark) | Design System artifact asset groups; brand package `aitoolbox-brand-v4.1.zip` | 4.1 |

*Agents read these files through the Context pack; they never restate a hex value from memory.*

### 14.2 Foundations

- **DSR-01 Base** — Material Design 3. Every colour is an MD3 role or a declared extended role, referenced by token (`--md-sys-color-*`, `--mat-sys-*`), never by hex in UI code.
- **DSR-02 Palette M · Night & neon** — seeds: primary deep violet #1E1B4B, neutrals night #0D0B14, tertiary neon green #00F5A0. Light: primary tone 25 (#35307E), tertiary tone 40 (#006C44), containers tone 90. Dark (first-class theme): night surfaces tones 4–22 (surface #14121E), primary tone 80 (#C4C0FF), tertiary tone 85 (#00F29E). Surfaces are violet-tinted, never neutral grey.
- **DSR-03 Role usage**

| Role | Use for | Never for |
|---|---|---|
| `primary` | filled buttons, active navigation, selected tab, focused field, switches on, links, "Toolbox" in the wordmark | status, decoration |
| `secondary` / `secondary-container` | tonal buttons, filter chips, active nav item, segmented selection, environment badges, avatars | emphasis |
| `tertiary` (neon green) | the one action that starts work (labels Run, Deploy, Apply); max one filled per screen | dialogs, destructive actions, health status |
| `ai` (light teal #80D5D4, same in both themes) / `ai-container` (#9CF1F0 light, #004F50 dark) | AI-powered features only: suggestion cards, Explain/Generate actions, AI chips, always with the sparkle icon | chrome, navigation, non-AI buttons |
| `success` / `warning` / `error` | health chips, log levels, validation, state marks | brand, decoration |
| `logo-box` / `on-logo-box` / `logo-cursor` | the logo family only (§14.5) | any UI surface |

- **DSR-04 Info status** uses `primary`; it is the only status mapped to a brand role.
- **DSR-05 Typography** — BNPP Type 500 (font file in the design system) for display, headline, title and label; Open Sans 400 for body; Open Sans 600 for code, paths, identifiers and label-small metadata. No monospace face. MD3 sizes, line heights and tracking.
- **DSR-06 Shape, 16 px ceiling** — scale 0 / 4 / 8 / 12 / 16. `radius-lg` (16) is the largest corner on any rectangle: buttons, segmented buttons, search bars, navigation items (hover and active), dialogs, bottom and side sheets, date and time pickers, large FAB. `radius-md` (12): cards, tables, panels. `radius-sm` (8): chips. `radius-xs` (4): text fields, menus, tooltips, snackbars. `radius-xl` is pinned to 16. `radius-full` only on circles: avatars, badges, radio, switch, icon buttons.
- **DSR-07 Elevation** — tonal surface containers first; shadows only where the UI Component spec asks (levels 1–3).
- **DSR-08 Contrast** — every text pair clears 7:1 in the token set; a UI Artifact must not lower it (no opacity on text roles, no custom greys).

### 14.3 Chrome and layout

- **DSR-10** Top app bar on `surface-container`, never `primary`; 64 px, title-large.
- **DSR-11** Navigation drawer on `surface-container-low`, 56 px items at 16 px radius; active item `secondary-container` + `on-secondary-container`.
- **DSR-12** Teal (`ai`) never colours chrome: header, drawer, tabs, app bar.
- **DSR-13** Dialogs: 280–560 px, `surface-container-high`, 16 px radius, confirm = filled `primary`, dismiss = text; a destructive confirm is a text button in `error`; the tertiary Run action never appears in a dialog.

### 14.4 Feedback: state marks and loaders

- **DSR-20 State mark** — the logo construction with the state in the corner badge instead of "AI": ✓ success, i info (`primary`), ! warning, ✕ error. Three containers chosen by size only:
  - alone on a surface, 24–40 px (snackbars, popin headers, inline alerts);
  - in a circle, 56–96 px (empty states, table- or panel-level errors): disc in the state role (dark on light, light on dark), toolbox reversed, badge in the state container;
  - tile glyph, 18–20 px (chips, table cells, menu items): `>` and the symbol on a rounded tile.
- **DSR-21** Loading is not a state: the slot shows the pen-orbit ring around the plain mark, then resolves in place to success, warning (timeout) or error (with Retry). No layout shift, no entrance animation.
- **DSR-22 Loaders** — brand loader "Constructor" for app-level waits only (boot, workspace switch); in-screen waits use the Constructor family skins of Material indicators: pen orbit (circular, `mat-progress-spinner`), guide line (linear, `mat-progress-bar`), Constructor determinate (long operations with a known value), working dots (green = a command runs, teal = a model is working).
- **DSR-23** All motion honours `prefers-reduced-motion` (loaders show the finished logo or stop).

### 14.5 Logo family

- **DSR-30** The mark is the toolbox prompt (box, squared handle, `>_`) with the light-teal AI badge cut out of its top-right corner; the badge appears from 24 px; below 32 px the favicon glyph replaces the mark.
- **DSR-31 Night box** — on light backgrounds the box is `logo-box` night #0D0B14 with a white `>` (`on-logo-box`) and the neon cursor #00F29E (`logo-cursor`); on dark backgrounds the box is lavender #C4C0FF with a night `>` and an emerald cursor #006C44. The favicon tile and app-icon tile use the same box colour. The night seed appears raw only here.
- **DSR-32** Wordmark "AIToolbox" in Manrope 800, outlined: "AI" in `on-surface`, "Toolbox" in `primary`. Never retyped, rotated, outlined, recoloured or set in another face. Clear space: a quarter of the mark height.
- **DSR-33** The chatbot avatar is the brace box `{ >_ }`, never the brand mark.

### 14.6 Angular Material

- **DSR-40** Angular Material 21 uses `theme.m2.scss` (M2 API, `mat.m2-*`); Angular Material 22 uses `theme.m3.scss` (`mat.theme` + `mat.theme-overrides`). Both pin every role to the token values, so hex values are identical whichever API compiles.
- **DSR-41** Per-UI-Component styling goes through `mat.<name>-overrides` mixins; `--mdc-*` variables are dead since v20 and must not appear.
- **DSR-42** Extended roles (`ai`, `success`, `warning`, `logo-*`) have no Angular slot: use `--md-sys-color-*` custom properties and the scoped classes `.dt-ai`, `.dt-run`, `.dt-chip-*`. M3 has no `accent`.
- **DSR-43** State marks and loaders are inline SVG from the brand package, not `mat-icon`.

### 14.7 UI Component rules

The full per-UI-Component reference (rules, values light / dark, M2 slot on Angular Material 21, M3 variable on Angular Material 22) is the project doc `claude/aitoolbox-component-rules.md`. It covers 35 UI Components plus Table, Paginator, Sort header, Expansion panel, Stepper and Tree (not yet designed). Summary of the rules a Quality gate checks first:

| UI Component | Key rules |
|---|---|
| Button | 40 px, 16 px radius, label-large; filled `primary` to confirm, tonal `secondary-container`, outlined, text, elevated; one filled `.dt-run` (tertiary) per screen; destructive = text button in `error`. |
| Icon button | 40 px circle, `aria-label` required; standard / filled / tonal / outlined via classes. |
| FAB | small 40 px r12 · default 56 px r16 · large 96 px r16 · extended 56 px; `primary-container`; `.dt-run` only for a run entry point. |
| Segmented button | 2–5 options, 40 px, 16 px outer radius, `outline` dividers; selected `secondary-container` with a leading check. |
| Chip | 32 px, 8 px radius; filter selected `secondary-container`; AI chips `.dt-ai`; status chips use StatusChip. |
| StatusChip | `*-container` + `on-*-container`, led by the 18 px tinted tile glyph; never colour alone. |
| Card | 12 px radius, 16 px padding; elevated (level 1), filled (`surface-container-highest`), outlined (`outline-variant`). |
| Text field | outlined by default, 56 px, 4 px radius; focus `primary`; error `error` + `mat-error`; helper body-small. |
| Search | bar 56 px, 16 px radius, `surface-container-high`; results view same tone, 48 px rows. |
| Menu, Tooltip, Snackbar | 4 px radius; snackbar on `inverse-surface`, one action in `inverse-primary`, 24 px state mark. |
| Dialog | 280–560 px, 16 px radius, `surface-container-high`, level 3, 24 px padding; confirm filled `primary`, dismiss text; no `.dt-run`. |
| Bottom / side sheet | `surface-container-low`; bottom sheet 16 px top corners, 32×4 drag handle. |
| Date / time picker | 328 px, 16 px radius, `surface-container-high`, level 3. |
| Top app bar | 64 px on `surface-container`, never `primary`; title-large. |
| Navigation drawer | 300–360 px on `surface-container-low`, 56 px items at 16 px radius; active `secondary-container`; section labels label-medium. |
| Navigation rail / bar | 80 px rail; active indicator `secondary-container`; icons + labels. |
| Tabs | primary indicator 3 px `primary`; secondary 2 px. |
| List | 56 / 72 / 88 px rows, 40 px leading avatar, 16 px inset divider. |
| Checkbox, Radio, Switch, Slider | `primary` when on; switch 52×32 with check icon. |
| Badge | `error` role, label-small; never `primary` for an alert count. |
| ProgressIndicator | pen orbit (`mat-progress-spinner` 48 / 24 / 18 px) and guide line (`mat-progress-bar` 4 px) skins; AI tasks `.dt-ai`. |
| Loader (brand) | Constructor, app-level waits only, 96 px splash, 40 px minimum; `logo-*` tokens. |
| StateMark | badge 24–40 px · circle 56–96 px · tile 18–20 px; pending ring resolves in place; never below 18 px. |
| Table | wrapper `surface-container-lowest`, `outline-variant`, 12 px radius, rows square; 48 px header in label-medium, 52 px rows (40 dense); status column = 20 px tile glyph. |

### 14.8 Invariants and decisions (CTX-DS)

| ID | Rule |
|---|---|
| INV-DS-01 | A UI Artifact references colours, type, shape and elevation by token only; a raw hex, a non-token radius or a non-system font fails the Quality gate. |
| INV-DS-02 | At most one filled `tertiary` action per screen, and none inside a dialog. |
| INV-DS-03 | `ai` roles appear only on AI-powered features, always paired with the sparkle icon. |
| INV-DS-04 | No rectangle has a corner larger than 16 px; `radius-full` is used on circles only. |
| INV-DS-05 | Status is never conveyed by colour alone: every state shows its symbol (state mark or chip glyph) and a text label. |
| INV-DS-06 | The logo family uses `logo-*` tokens only; UI surfaces never use them. |
| INV-DS-07 | Agents propose design-system changes as Artifacts through a Checkpoint; they never edit tokens or brand assets directly (same spirit as INV-12). |

| ID | Decision | Rationale |
|---|---|---|
| DEC-DS-01 | Material Design 3 on Angular Material, with an M2 theme for v21 and an M3 theme for v22 sharing one token set. | Teams migrate at their own pace without visual drift. |
| DEC-DS-02 | Palette M · Night & neon (deep violet, night, neon green; light-teal AI kept separate from the brand green). | Generative-AI modernity, high legibility on dark; AI features stay distinguishable from actions. |
| DEC-DS-03 | Logo family on a night box via dedicated `logo-*` tokens. | Strongest brand contrast on light surfaces without darkening the UI `primary`. |
| DEC-DS-04 | Shape ceiling at 16 px; full radius reserved for circles. | Tighter, more technical look consistent across buttons, navigation and containers. |
| DEC-DS-05 | One state-mark construction (logo + badge) for all feedback; no entrance animation. | Recognisable system grammar; calm interface. |

## 15. Changelog

| Version | Date | Change |
|---|---|---|
| 0.3 | 2026-10-16 | Added section 14, design system rules (DSR, INV-DS, DEC-DS) and the UI Component rules summary (14.7, full reference in `claude/aitoolbox-component-rules.md`): palette M · Night & neon, Role usage, typography, 16 px shape ceiling, state marks, loaders, logo family on the night box, Angular Material 21/22. Extended CTX-DS and its vocabulary. |
| 0.2 | 2026-10-02 | Added CTX-ENV Environment Management; Module and CI context id in CTX-CAT; Environment value object moved out of CTX-CAT; new reserved words; INV-ENV, EVT, CMD, DEC-ENV and OPP-ENV entries. |
| 0.1 | 2026-09-12 | Initial draft. |
