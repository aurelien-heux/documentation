---
title: Production vision — global consistency review (content, features, language, data, navigation, accessibility, themes, responsive)
status: review done and fixes applied 2026-11-03 (canvas version 225)
date: 2026-11-03
relates-to: devtoolbox-domain-reference.md, aitoolbox-component-rules.md, aitoolbox-feature-marks.md, architecture-merge-plan.md
---

# Production vision · consistency review

Scope: `ProductionVision.dc.html` as published (canvas version 224), 49 screens and layers crawled (Sweep, Environments,
Docs and its four spaces, Catalog, Community, Administration's 13 sections, the header's four layers), at 360 · 600 ·
840 · 1200 · 1600 px with and without the assistant pane, with axe-core (WCAG 2.2 AA + best practices) on every screen.
Reference for "invented": `devtoolbox-domain-reference.md` (bounded contexts, reserved words, DEC-ENV-01, INV-ENV-08)
and the feature marks (Sweep, Docs, Environments, Chatbot, Notifications, Architecture).

## 1. Verdict in one paragraph

The core features (Sweep, Environments, Docs with the Architecture space, Catalog, the assistant) are coherent and read
well in English. Three things weigh on the prototype: **explanatory sentences on almost every screen** (the UI explains
itself instead of being obvious), a **Community + Administration layer that goes far beyond the domain** (tours,
surveys, NPS, champions, office hours, insights, feedback profiles with sampling and routing, maintenance banner), and
**no dark theme at all** (1,179 hex colours in the CSS, 622 inline, no token layer). Accessibility is decent on names
and roles (every icon button is named, dialogs are `role=dialog aria-modal`) but weak on structure (no `h1`, 27 of 49
screens without any heading, content outside landmarks) and on keyboard (Escape does not close the Sweep dialog, no
focus management). Responsive is right in its shell (bottom bar under 600, rail to 1199, the assistant takes the whole
width under 600 and replaces the page to 1199, docks at 1200) with three content failures: the Environments table and
the architecture tree under 600 px, the Community tabs at 360.

## 2. Findings by criterion

### 2.1 Useless text (remove or cut to a label)

| Where | Text | Fix |
|---|---|---|
| Boot | Snackbar "New in 4.6: approval cards and PR summaries · Take the tour" on every load | Remove; the bell carries what is new. |
| Sweep › Runs | Card "Tip · new in 4.6 · The Reviewer agent writes a review summary… Show me · Got it" | Remove. |
| Sweep › New run | "The agents read the ticket, plan the change, code and review it, then open the pull requests." | Remove; keep the three fields and their helper lines. |
| Sweep › run (succeeded) | "Each pull request has a review summary from the Reviewer agent. Merge stays with your team." | Remove. |
| Environments | Banner "Deploy and Reserve use the same tools as the assistant and Sweep, from the Catalog. They ask before they change anything." | Remove. |
| Docs home | "Knowledge base · 7 sources · updated today 08:41 · every answer cites its source" | Keep "Knowledge base · 7 sources · updated today 08:41 · Sources". |
| Docs › AI wiki › page | "Tip · A design documented from code is flagged as a draft…" | Remove. |
| Catalog › item | "Asks before it does anything that changes something: run pipeline, open pull request." (repeats the description) | Keep one sentence, in the description. |
| Catalog › Publish › Submit | "Who can use it. You can widen it later from Mine." | "Who can use it". |
| Community › Ideas | Header "Vote once per idea; the platform team answers within two weeks" + "Everyone sees every idea and votes once per idea. Votes are frozen once an idea is delivered." | One short line or none. |
| Community › Guides | "Suggested for you · You used the assistant 14 times this week and have not seen the approval card yet — 3 steps, under a minute." | Remove (behavioural nudging). |
| Admin › Users | "Accounts are created and removed automatically from the company directory (SSO), with their team. This page only gives admin rights." | "From the directory · synced 10 min ago". |
| Admin › Groups, Audit log | "This section is not in the lab. It uses the same shell, with its own content." | Placeholder: give them content (a groups table, an audit table) or remove the sections. |
| Admin › Catalog | "Champions and platform admins review skills submitted to everyone, within 2 working days." | Remove. |
| Admin › Connectors | "The outside services Sweep reads from and writes to. Credentials are kept in the vault and never shown again after saving." | Remove. |
| Admin › Tools and skills | "What each agent of a run may use. Actions that change something ask first and stop the run until someone approves." | Remove (the header already says "what each agent of a run may use"). |
| Admin › Releases | "AI draft · Release notes can be drafted from the changelog…" | Remove. |
| Admin › Tours | "How it works · Developers register anchors on screen elements…" (developer documentation inside an admin page) | Remove. |
| Admin › Feedback | "One place for every feature's feedback form. Feature admins with a Feedback · <feature> right see only…" | Remove. |
| Admin › Insights | "To be designed · Usage metrics · OpenSearch · … come in a later design round", "Open questions in discussions … (later wave)" | Remove the "later" blocks; a prototype shows what exists. |
| Admin (Sweep, Community sections) | Chips "Remote module · sweep-admin@1.4 · owned by Platform team · Full module · Open Sweep" | Remove (implementation detail of the micro-frontend). |
| Header › Help | "Show me around this page · Guides · What's new · Ask a champion · Suggest an idea · Ask the assistant · Documentation" | Keep "Documentation", "What's new", "Keyboard shortcuts"; the rest goes with the Community cut. |

### 2.2 Invented or over-built features (decisions needed)

Against the domain reference, which models Catalog, Delivery orchestration, Assistant, Docs, Design system, Knowledge
index, Agent runtime, Environments, Integrations, IAM — and lists analytics, notifications and portal navigation as
"not yet modeled":

| Area | What the prototype has | Proposal |
|---|---|---|
| **Community** | What's new (releases with read/useful rates, discussion threads, "Useful?" votes, Watch videos, Try it tours), Guides (tours and videos with progress and "Suggested for you"), Ideas (votes, statuses, following, platform notes), Champions near you, Become a champion, Office hours with Add to calendar, NPS widget, micro-survey after a run, acknowledgement of policies | **Option A (simple):** keep *What's new* as a plain release-notes list (version, date, what changed) and *Ideas* as a plain list (title, votes, status); drop Guides/tours/videos, champions, office hours, NPS, micro-surveys, discussions, read rates. **Option B:** drop Community entirely; release notes move to Docs › Operations. **Option C:** keep as is. |
| **Administration › Community** | Releases (channels, read %, useful %, acked, scheduled banner, maintenance banner), Tours (triggers, started, completed, Play/Edit), Feedback (profiles, entry points, sampling %, routing, solicitation policy, inbox, surveys), Ideas triage (status, public note, AI duplicate detection), Insights (after-action score, NPS, tour completion, read rate, themes "by the assistant", drop-off steps, low adoption nudges) | Follows the Community decision: A keeps *Releases* (publish a note) and *Ideas* (set a status); B and the rest removed. |
| **Administration › Core** | Groups and Audit log are placeholders; General has retention of "Feedback and surveys" | Give Groups and Audit log real rows or drop them; retention lines follow the Community decision. |
| **Environments** | One application (credit-request) and a `prod-eu` row with a "promotion window Mon–Thu 09:00–17:00"; health "Degraded" with no observer or time; a version per environment but no branch, commit, Effective placement (local vs Upstream), Drift or Reservation details | Domain: v1 is **non-production only** (DEC-ENV-01), runtime state always shows its **Observer source and observedAt** (INV-ENV-08), a Placement is a **branch**; promotion windows do not exist. Rebuild the table: Environment · tier · Upstream environment · what runs (module, branch, observed version · source · time) · Reservation (holder, scope, until) · Deploy / Reserve. Drop `prod-eu` and the windows (and the "Promotion window alerts" release note and idea). |
| **Header** | Three ways to open the assistant: "Ask" in the search bar, the "Open assistant" icon, Help › "Ask the assistant" | One: the search bar's Ask. Remove the icon; the bell, help and account stay. |
| **Rail** | "Cookies" item (a consent banner demo) on an SSO-only internal app | Remove from the production vision (the Cookies board stays on the canvas). |
| **Docs › New joiner** | A page addressed to "Léa" while the signed-in user is Aurélien ("Week 1 for you, Léa", buddy, manager, access) | Make it the signed-in user's page, or a generic checklist without a persona. |
| **Docs › Detailed design** | Still the corporate credit example (facility-service hexagon), unreachable from the Meridian Bank space | Known from the merge plan; move under Meridian › Corporate banking › Facility service. |
| **Sweep** | Consistent with the running app (ai-dev-pipeline, OpenHands, Jira planner, Frontend/Backend tracks, integration check). Kept as is. | Labels only (2.3). |
| **Catalog** | Skills · Tools · MCP servers, publish flow in five steps with a Test step and a review by "champion or platform admin" | Keep; "champion" → "platform admin". |

### 2.3 English and labels

| Now | Proposed | Why |
|---|---|---|
| Rail "Envs" | "Environments" | `env` is a reserved abbreviation (domain §6); the bottom bar has room. |
| "Launch a pipeline" (dialog title) · "New run" (button) · "Dispatch" (confirm) | "New run" · "New run" · "Start" | One name for one action; "pipeline" is CI vocabulary (Workflow is the agentic chain) — kept only in the step strip, which mirrors the running app. |
| Catalog tab "Mine" | "My skills" | "Mine" alone is unclear. |
| Architecture tab "Catalogue" vs rail "Catalog" | "Elements" for the architecture tab | Two different things with the same word in two spellings. |
| British / American mix: organisation, artefacts, catalogue vs Catalog, color | American throughout (Catalog is already American) | One spelling. |
| Admin column "Acked" | "Acknowledged" | No abbreviations in headers. |
| Admin "Solicitation policy", "Ideas triage" | "Feedback prompts", "Ideas" | Plain words. |
| Step status "DONE · 3 MIN 43 S" | "Done · 3 min 43 s" | Uppercase through CSS hides units; keep sentence case. |
| "Useful?" + thumbs on each release | drop with the Community cut | — |
| Admin › Users "Feedback · Sweep" as an admin right | "Sweep feedback" | Reads as a label, not a right. |

Every other label is English and plain; no French, no lorem, no TODO in the visible text.

### 2.4 Mock data: inconsistencies to fix

| Item | Problem | Fix |
|---|---|---|
| "Today" | Office hours "Thu 31 Oct" but the notification says "tomorrow at 14:00"; model change "3 November" is "Action required · by 3 Nov"; the Architecture model is "main @ 4a1b9e0 today" | Fix one date for the whole prototype: **Tuesday 3 November 2026, 11:12**. Every relative date (2 min ago, yesterday, 28 Oct…) and every due date is computed from it; past events (office hours 29 Oct) are shown as past. |
| Docs home › Architecture card | "Corporate credit platform · LikeC4 views by TOGAF phase · 133 elements · 7 views · 4 changes"; Recently updated "Corporate credit · ARB arb.facility.2026-14" | Meridian Bank · 4 portfolios · 31 applications · 227 elements · 8 changes · 4 reviews; recently updated: the Meridian ARB submitted today. |
| Knowledge base › Sources | "Architecture model · 3,040 elements" vs 227 in the space | 227 elements · 20 views, main @ 4a1b9e0. |
| Sweep runs | Every run has "3 files · +156 −12" / "4 files · +188 −6", "212 passed", the same commit `3f9a1c2` in every repository, the same LLM timings "6.1 s", "14.8 s" | Vary per run and per repository (different shas, file counts, test counts, durations). |
| Environments | 4.6.0 on three rows; no branch or commit | Per row: module, branch (`develop`, `release/4.6`, `feature/e2ecc-103870`), observed commit, source (Kubernetes · ArgoCD) and time. |
| Catalog | "9 items for the assistant and Sweep" in the header; Browse shows 9 ✓; item "3,100 uses in 30 days" ✓ | Keep. |
| Community › Ideas | "Dark mode for the runs table · The rest of the app has a dark theme" while the app has none | Becomes true once the dark theme exists; otherwise drop the idea. |
| Admin › Users | 1,284 users, 46 admins, policy "1,141 / 1,284" ✓ | Keep. |
| New joiner | Léa vs Aurélien | See 2.2. |

### 2.5 Navigation

Works: rail and bottom bar, header context per screen, state kept per screen when switching, Sweep list → run → back,
Catalog browse → item → back, Docs home → space → page → back, Architecture crumbs · Back · drill-down, Admin section
list (a select under 600 px), notifications → the run or the idea.

To fix: **Escape does not close the Sweep "New run" dialog** (nor return focus); the assistant has **three entry
points**; the Help menu is a Community launcher; the Community › Guides and Admin › Tours loop into each other; the
Docs lab's detailed designs are orphaned; no deep links (hash only on the rail) — acceptable for the prototype.

### 2.6 Accessibility (axe + manual)

| Severity | Finding | Fix |
|---|---|---|
| Structure | **No `h1` on any screen; 27 of 49 screens have no heading at all** (titles are `<b class="ui">`). | One `h1` per screen = the header's context title (visually unchanged), `h2` per section, `h3` per card title. |
| Structure | 51 nodes outside landmarks (axe `region`): the assistant pane, the admin section nav, the Docs sub-areas | `<aside aria-label="Assistant">`, `<nav aria-label="Administration">`, `<section aria-labelledby>`. |
| Critical | NPS buttons `role="radio"` with `aria-pressed` (22 nodes) | `radiogroup` + `aria-checked` only — or gone with the NPS. |
| Critical | Catalog `role="tablist"` whose children are not `role="tab"` (also check the 9 tablists vs 11 tabs) | Tabs: `role=tab`, `aria-selected`, `aria-controls`, one Tab stop and arrow keys (DSR-09). |
| Serious | Log line numbers `.no` under 4.5:1 (131 nodes) | `on-surface-variant` #48454E on the log surface. |
| Serious | DD pictures scrollable but not focusable (2) | `tabindex="0"` + `aria-label`. |
| Serious | Escape does not close the Sweep dialog; no focus moved into dialogs and menus, no focus return (one `.focus()` call in the whole page) | A `layer` helper: open → focus first control, Escape → close and return focus, Tab stays inside. |
| Moderate | 10 empty `<th>` (action columns) | Visually hidden "Actions". |
| Moderate | Targets under 24 px: 12 on Docs › Architecture (plateau chips B · T1 · T, tree toggles), 12 on Community (thumbs, NPS) | Minimum 24 × 24 px hit area (DSR-09). |
| Moderate | Text under 11 px: 43 elements on Docs › Architecture (tree meta, chip letters), 6 on Community, 4 on Docs home | 11 px floor (DSR-09). |
| Minor | No skip link; `title` on 549 elements (fine as tooltips, never the only name) ; 4 `prefers-reduced-motion` rules only — the Sweep step animation and the looping feature marks must stop under reduced motion | Add "Skip to content"; audit motion. |
| OK | Every icon button named; `lang="en"`; dialogs `role=dialog aria-modal aria-label`; snackbar `role=status`; `aria-current` on navigation; `aria-invalid`/`aria-describedby` on the Sweep form; `aria-pressed` on chips | — |

### 2.7 Light and dark

There is **no dark theme**: 1,179 hex colours in the page CSS, 622 in inline styles, hex fills in the SVG diagrams,
no `prefers-color-scheme`, no theme control. The design system defines dark as a first-class theme (DSR-02; pairs in
`aitoolbox-component-rules.md`: surface #FDF8FD / #14121E, on-surface #1C1B1E / #ECE5F8, on-surface-variant #48454E /
#CAC3DC, primary #35307E / #C4C0FF, nav-container #EDE4FF / #1D1A27, nav-active #D4D0F9 / #454364, containers
#FAF4FF…#ECE5F4 / #1D1A27…#363341, outline-variant #CAC4CF / #494458, error #93000A / #FFB4AB, success #1B5F1F /
#91D888, warning #6A4E00 / #FCBC00, ai-container #9CF1F0 / #004F50, logo box night / lavender).

Plan: a **token pass at build time** — every light hex (CSS and inline) becomes `var(--c-<role>)`, one `:root` block
with the light values, one `[data-theme=dark]` block (and `@media (prefers-color-scheme: dark)` for "System") with the
dark values from the component rules; the ArchiMate layer fills keep their own `--ax-*` tokens with a dark set; the
feature marks switch to their `dark/` colours. Control: **Theme · System · Light · Dark** in the prototype bar, and
"Appearance" in the account menu. Light stays byte-identical. Legibility check in both: every text pair ≥ 4.5:1, chips
and status glyphs ≥ 3:1 (automated on every screen, as done for this review).

### 2.8 Responsive

| Width | Finding | Fix |
|---|---|---|
| 360, 600 | **Environments table overflows** (Health and Reserved columns cut, no scroll) | Rows as cards under 600 px; horizontal scroll inside the table frame 600–839 (INV-DS-09). |
| 360 | **Architecture tree rows collide**: labels wrap over the chips, the plateau track and the change chip; tabs 4 px over | Compact row: name on one line, the chips on a second line; hide the plateau track under 600 px (it stays on the element page). |
| 360 | Community tabs overflow 17 px; chip rows wrap on three lines | Scrollable tab strip; fewer chips (goes with the cut). |
| 360 | Boot snackbar sits on the bottom bar | Goes with the snackbar removal. |
| all | Assistant pane: full screen under 600 ✓, in place of the page 600–1199 ✓, docked 400 px from 1200 ✓; bottom bar under 600 ✓, rail 600–1199 ✓ | Keep; add `aria-expanded` on the Ask button and move focus into the pane when it opens. |
| 1200 + pane | Page area 719 px: Sweep list and matrices fit; the admin two-column forms fit | Keep. |

## 3. What was done (2026-11-03, canvas version 225)

Decisions taken with the product owner: **Community stays as it is** (text cuts only); **Environments is rebuilt on
the domain** (non-production only, placements by branch, observed state with source and time, reservations).

| Criterion | Done |
|---|---|
| Useless text | Every line of 2.1 removed or cut: boot snackbar, Sweep tip and dialog intro, result sentence, Environments banner, wiki tip, catalog repeats, ideas notices, "Suggested for you", admin explanations (users, catalog, connectors, tools, AI draft, tours "How it works", feedback footer, insights "To be designed" and "later wave"), micro-frontend module lines; Help menu keeps one entry to the assistant (the search bar). |
| Features | Environments: six non-production environments (dev and int as Upstream environments with their tracked branch and update mode; dev-1, dev-2, staging-1, staging-2 falling back on them), an application selector, per module the branch and whether it is a local placement or comes from the Upstream environment, the observed version and commit with its source (Kubernetes, ArgoCD) and time, a Drift mark, reservations with holder, scope and expiry, Deploy / Reserve (through the assistant's approval card: module, branch, environment; descriptor pull request then first rollout) and Extend / Release on one's own reservation. prod-eu and promotion windows are gone, and the release note, guide, idea and notification that mentioned them now speak of reservations. Header: the duplicate assistant icon is gone; the rail has no Cookies item. Groups and Audit log have real tables. New joiner is a generic checklist (no persona). Docs home, Recently updated, the knowledge-base sources and the assistant's architecture answers are Meridian Bank; a source opens the right view, element or ARB of the board (`arTarget`). |
| English and labels | Environments (not Envs), New run / Start (not Launch a pipeline / Dispatch), My skills, Elements (the architecture tab; Catalog stays the skills catalog), Acknowledged, Feedback prompts, Ideas, "a platform admin reviews it" (no champions in the flow), American spelling throughout (organization, artifacts, color, center, behavior, summarize), step status in sentence case. |
| Mock data | One date for the whole prototype, Tuesday 3 November 2026 11:12: office hours Thu 5 Nov, model change 10 Nov, policy 16 Nov, audit log and reservations consistent. Sweep figures vary per run and repository (commit shas, file counts, line counts, test counts and additions, agent latencies, suggestions), and the PR summaries reuse the same numbers. Environments data is consistent with the Sweep runs (feature/e2ecc-103870 on dev-1, feature/e2ecc-103894 on dev-2). |
| Navigation | Escape closes the top layer (dialogs, menus, the notifications panel, the assistant's tools menu, the modal drawer) and returns focus to the opener; focus moves into a dialog or menu when it opens; arrow keys, Home and End move inside tablists, segmented buttons and radio groups; one entry point to the assistant. |
| Accessibility | One `h1` per screen (the header context), section titles as `h2`/`h3`, skip link, named action columns, focusable diagrams, radios without `aria-pressed`, valid tablists, menu items for the appearance control, 11 px text floor, 24 px targets, log line numbers and future steps at AA contrast, reduced motion honoured. **axe (WCAG 2.2 AA + best practices): 0 violations on the 49 screens, in light and in dark.** |
| Light and dark | Token pass at build time (`vision_theme.py`): the 87 colour literals of the page become `--c-<hex>` custom properties with the light values and the dark values of the design system (surface #14121E, on-surface #ECE5F8, primary #C4C0FF, nav-container #1D1A27, containers, outline, error / success / warning / ai families, run and logo roles); property-aware for white (background → surface-container-lowest, text → on-primary); the console and source blocks keep their colours; `color-scheme` follows. Control: THEME · System · Light · Dark in the prototype bar and Appearance in the account menu; System follows `prefers-color-scheme`. Light renders pixel-identical to before. |
| Responsive | Environments as cards under 840 px; compact architecture tree rows (chips on their own line, plateau track hidden); tab strips scroll; no text under 11 px at any width; the assistant takes the whole frame under 600 px, replaces the page to 1199 px and docks at 1200 px, unchanged. |

Left as is: Community's scope (decision C); "Cancelled" spelling (Sweep status, matches the running app); the Docs lab's
detailed-design pages still describe facility-service's hexagon (now realizing Meridian's `sbb.facility-service`);
the standalone Architecture board and the three labs stay light-only (the theme pass is the vision's).

## 3b. Order of the fixes (as planned)

1. **Cuts and text** (2.1, 2.2 after the decision, 2.3): one pass over `vision-prototype-src`, `vision_parts.py`,
   `vision_sweep.py`, `vision_docs.py`, `admin_lab_build.py`, `catalog_lab_build.py`, `docs_lab_data.py`.
2. **Data** (2.4): one `NOW` for the whole prototype and the Meridian Bank figures everywhere; varied Sweep figures;
   Environments rebuilt on the domain fields.
3. **Accessibility and navigation** (2.5, 2.6): headings, landmarks, tabs, dialog layer helper (Escape, focus), log
   contrast, targets and text floor, skip link, reduced motion.
4. **Responsive** (2.8): Environments cards, tree compact rows, tab strips.
5. **Dark theme** (2.7): token pass + theme control, then the contrast run on every screen in both themes.
6. Re-crawl (axe + widths + both themes), publish, zip, update this doc with the result.
