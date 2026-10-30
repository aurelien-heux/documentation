AIDocs › Architecture › **Process**

Architecture change management

# Architecture Change Process

How a change to the architecture goes from a request to an approved target and a reached plateau, following the TOGAF ADM. The toolbox is where people work; Git is where every version lives. Each change is one work package, one branch and one pull request in the central architecture repository.

0 Trigger1 Decide2 Design3 Review4 Deliver

WP-FAC-02 · PR #88 · arb.facility.2026-14

### Extract facility-service from the Credit origination monolith

iRe-architecting

Portfolio: Corporate creditBaseline → Transition 1 · Dec 2026Owner: Facility architect

1. Decide✓DoneScope and reviewers set
2. Design✓Done0 errors · coverage 13/13
3. Review!Needs attentionSecurity requested changes
4. Deliver–Not started2 conditions to come

12 checks · 4 reviewers · 2 conditions · 3 asks to the board · reviewed at `7c1e9a0`, updated since review

Example change from the Corporate credit worked example, as it appears in Process › Changes.

## The flow

Columns are the steps, mapped to TOGAF phases. Rows are who acts. A request for changes from the board loops back to design; a simplification change skips the board.

PeopleToolbox screenAutomated (agent or CI) BoardGit NextRequest changesSimplification path

On a small screen, scroll the diagram sideways.

## Three classes of change

TOGAF Phase H classifies each change request. In the toolbox the owner picks the class in step 1; it decides who approves and how much of the ASD is needed.

| Class | Examples | Steps | Who approves | ASD |
| --- | --- | --- | --- | --- |
| Simplification | Rename, owner change, a missing relationship, a description | Decide → Design → merge | CODEOWNERS approve the PR once checks are green | None |
| Incremental | A new interface on an existing SBB, a new Module inside an agreed plateau | All steps | Portfolio architect, recorded as a Checkpoint | Short: context, gap, decisions |
| Re-architecting | A new plateau, extracting a service, a new platform or data store | All steps | Architecture Board | Full: the 13 coverage items |

## The steps in the toolbox

Each step says what the TOGAF deliverable is, which toolbox screen does the work, what happens in Git, and when the step is done. Screens refer to the Process area of the architecture space: Changes, Decisions, Reviews, Roadmap.

[0 Trigger](#step-0)[1 Decide](#step-1)[2 Design](#step-2)[3 Review](#step-3)[4 Deliver](#step-4)

0

### Trigger

TOGAF Phase H · change request

TOGAF deliverable

Request for Architecture Work, when the change is large

Who

Anyone can propose. The portfolio architect owns the request.

#### In the toolbox

- **Process › Changes**Propose a change: title, why, Applications concerned.
- **Header search**Ask the assistant to draft a change from a conversation; it fills the same form.
- **Checks, drift alerts, ARB conditions**"Open as a change" pre-fills the request with the finding.

#### In Git

- Nothing yet. The request is a draft in the toolbox, not a branch.

✓**Done when** An architect accepts the request and becomes the change owner.

1

### Decide

TOGAF Phase H → A · classify, then scope

TOGAF deliverable

Statement of Architecture Work (scope, plateaus, stakeholders)

Who

Change owner. The portfolio architect confirms the class.

#### In the toolbox

- **Process › Changes › New change**Class: simplification, incremental or re-architecting. It decides the path below.
- **Scope**Portfolio and Applications, from plateau → to plateau, work package (new or existing).
- **Reviewers**Suggested by role from the class and CODEOWNERS; the owner adjusts.
- **Process › Decisions**A draft ADR for each decision the change needs.

#### In Git

- CTX-INT creates change/WP-FAC-02 in the central repository.
- First commit: work package, gap stub, ADR drafts, ARB record draft (incremental and re-architecting).
- Draft PR #88 opens; CI publishes preview pr-88.

✓**Done when** Scope saved, draft PR open, preview available.

2

### Design

TOGAF Phases B, C, D (target) and E, F (gap, roadmap)

TOGAF deliverable

Architecture Definition: target building blocks, requirements, gap, ASD, detailed design

Who

Change owner, Application leads, agents (drafts only: a person accepts every agent change).

#### In the toolbox

- **Catalogue**Add, change or retire elements; each is tagged with its plateau and change chip.
- **Views**Gap view baseline → target, on the preview build, with drill-down to the DD.
- **Agent actions**Draft DD from the contract, propose SBBs from a new endpoint, write an ASD section from the model.
- **Process › Reviews (draft)**Checks with their fixes and the 13 ASD coverage items, updated on each push.

#### In Git

- Every save is a commit on the branch; agent commits carry the agent as author and the person as co-author.
- DD and contract PRs in Application repositories set change: WP-FAC-02 and validate against preview pr-88.
- arch-validate runs on each push; errors block, warnings show in the PR comment.

✓**Done when** 0 blocking errors, coverage complete or explained, reviewers assigned. "Submit to ARB" becomes available.

3

### Review

TOGAF Phase G · Architecture Board, compliance

TOGAF deliverable

Board decision and, when approved, the Architecture Contract (conditions)

Who

Reviewers by role, the board chair. Decisions are Checkpoints (INV-12); agents never decide.

#### In the toolbox

- **Process › Reviews › arb.facility.2026-14**Submit: the readiness gate runs, the ASD is generated and frozen at the commit.
- **Reviewers**Each records Approve, Approve with conditions, Request changes or Not required, with a note.
- **Conditions and asks**Owner, due date and status per condition; the decisions only the board can take.
- **Updated since review**If the branch moves after submission, a banner shows the diff since the pinned commit.

#### In Git

- PR #88 leaves draft; the reviewed sha is pinned; the arb-decision check stays pending.
- When the Checkpoint is decided, the bot commits the ARB record (status, decision, conditions, decidedAt, reviewedSha).
- arb-decision turns green; the owner merges with a merge commit (no squash) so the reviewed sha stays in history.
- The merge commit is tagged arb/facility-2026-14.

#### Outcomes

- ✓Approve, Approve with conditionsmerge; conditions move to Deliver.
- !Request changesback to Design, then re-submit; the ASD is frozen again.
- ✕RejectPR closed; the bot commits only the ARB record to main, so the decision is kept.

✓**Done when** Decision recorded in Git and the change merged (or closed).

4

### Deliver

TOGAF Phases G and H · implementation governance, monitoring

TOGAF deliverable

Conformance with the Architecture Contract; the plateau reached

Who

Application teams and their agents build; the change owner confirms conformance.

#### In the toolbox

- **Process › Roadmap**Work package status, linked Work items (CTX-ORC), conditions with due dates.
- **Conformance**Reconciliation compares extracted code with the target: missing SBBs, endpoints without a model element.
- **Plateau reached**The owner confirms when every work package of the plateau is delivered and conditions are closed.

#### In Git

- Implementation PRs in Application repositories (code, contracts, DD); fragments published; lock bumps on main.
- A "Promote transition-1" PR: elements of the plateau become baseline, retired elements are removed.
- Tag plateau/facility/transition-1. The ARB record and ADRs stay as history.

✓**Done when** Conditions closed, conformance green, plateau promoted. The change closes.

## Versioning in Git

`main` holds the approved architecture: the baseline and every approved plateau. A change lives on its branch until the board decides; the board decides on one pinned commit; the decision itself is a commit.

## Git conventions

| Rule | Convention | Why |
| --- | --- | --- |
| Branch | `change/<work package>` | One branch and one PR per change, in the central repository. |
| PR title | `[WP-FAC-02] Extract facility-service` | The work package id links the PR, the change and the ARB record. |
| Preview | `?ref=pr-88` | Each push publishes a preview build; the toolbox shows the gap on it. |
| Linked repos | `change: WP-FAC-02` | Frontmatter on DD files changed in Application repositories. |
| Required checks | `arch-validate · arb-decision` | Validator errors block; arb-decision is set by the toolbox from the Checkpoint (green for simplification once CODEOWNERS approve). |
| Review pin | `reviewedSha` | The board decides on one commit; later commits flag "updated since review". |
| Bot commits | `atb-arch-bot` | Only the ARB record and lock bumps; credentials stay in CTX-INT (INV-07). |
| Merge | `merge commit` | No squash, so the reviewed commit stays reachable. |
| Tags | `arb/<portfolio>-<year>-<n> · plateau/<portfolio>/<plateau>` | A decision and a reached plateau are both findable in history. |
| Undo | `revert PR` | A revert is itself a change: simplification if it restores an approved state, otherwise a new review. |

Based on the AIToolbox project notes: architecture knowledge base (DEC-KB-01 to 06), delivery and repositories (central model, CI/CD, ARB loop), docs way in and architecture navigation (Process area, ARB coverage). Board decisions are Checkpoints (INV-12); automated Git writes go through CTX-INT (INV-07).