# AIToolbox · Architecture intake and change tracks

Decision of 2026-11-10, taken on the **Change start lab** (canvas, Decision labs page, `StartLab.dc.html`) and built
the same day in the Architecture board and in Docs › Architecture of the production vision (canvas version 235).
Complements `architecture-change-and-documentation-process.md` (documents, gates, DEC-KB-38..42) and
`architecture-metamodel-v4.md` (delivery line, DEC-KB-43/44).

## 1. What was decided (DEC-KB-45)

| Question | Options in the lab | Decision |
|---|---|---|
| How a change starts | A · a form in three questions · B · in the assistant · C · from the signal | **C + B**: intake from signals, plus an explicit request in the assistant, qualified in conversation (chat iteration). No form |
| How the phases in progress are followed | A · board by phase · B · tracks · C · by gate · D · ADM phases | **B · tracks**: one row per change with its own phases and gates |
| Where it lives | — | **Two separate places**: *Intake* (qualification) and *Changes* (ongoing architecture changes) |

## 2. Intake — qualification

Everything that could change the architecture arrives in **Process › Intake** before it is a change.

**Where a change comes from** (the origin, kept on the change afterwards):

| Origin | Example | Suggested entry | Enters at (TOGAF) |
|---|---|---|---|
| Business request | a ticket from a product owner | New need | Vision (A) |
| Request in the assistant | someone describes a need in the pane | New need | Vision (A) |
| Exploration | an architect tries a target | Exploration | Target (B·C·D) |
| Technology standard | the radar moves a technology to Hold or Retire | Evolution | Baseline (B·C·D) |
| Decision | an accepted ADR, a board condition | Decision | Gap analysis (E) or Plateau (F) |
| Code first | a pull request, from Sweep or from a local coding assistant, with no change | Small tweak | Implementation (G) |
| Model finding | a model check, the reconciliation (code differs from the model) | Post-delivery | after G4 (H) |
| Incident | fixed in production first | Post-delivery | after G4 (H) |

**The three outcomes of a qualification:** *Change opened* (at the entry phase, with the first documents to draft),
*Attached* to an existing change (the signal touches a scope a change already owns), *Dismissed* (no architecture
impact, with the reason). The Qualified list keeps all three, with who and when, and links to the change.

**Two ways to qualify:**

- *Qualify in the assistant* (the main one), on a signal or through **New request · ask the assistant**: the global
  assistant pane asks one question, proposes (origin, entry phase and TOGAF letter, what is skipped, kind and class,
  scope, first documents, next gate and who decides, overlaps), and the person iterates in conversation — change the
  class, make it an exploration, narrow or extend the scope — then creates, attaches or records a dismissal. The
  proposal is never applied without the person's confirmation.
- *Open as suggested*, *Attach*, *Dismiss* directly on the row, when the suggestion is obviously right.

Needs the connectors of CTX-INT for the signals: ticketing, Git (pull requests without a change), technology radar,
model checks and reconciliation, ADRs, incidents.

## 3. Changes — tracks

**Process › Changes** lists the ongoing changes by portfolio, one row each:

- title and **where it comes from** (origin and reference);
- the **track**: phases 0–5 and Delivered, each skipped (the change entered later), done or current; the gates G1–G4
  between them, passed, waiting or blocked;
- the current phase with its **TOGAF letter**, what is happening now, documents left to finish, the delivery line
  (tickets, last commit) when there is one;
- the gate chip when the change waits at a gate or is blocked; "New from intake" on a change just opened.

A row opens the change page (documents by phase, delivery, collisions); the page now starts with "Comes from …".
The filters stay: portfolio, missing documents, waiting for a gate.

## 4. Built

| Where | What |
|---|---|
| Architecture board · Process | New first entry **Intake** (To qualify, Qualified); **Changes** as tracks (replaces the cards); origin line on the change page; a change opened from intake is a real change (entry phase, first documents to do, change page) |
| Production vision · assistant pane | **Intake mode** of the global pane: one question, the proposal card, suggested replies and free text for the iteration, Create / Attach / Record; "Open the change" at the end. On the standalone board the same buttons say that the conversation lives in the product's pane |
| Change start lab | Kept as the record of the alternatives, with 19 example changes on every phase and at every gate (waiting, in review, changes requested, rejected, passed, passed with conditions) |

Tooling: `intake_data.py` (origins, signals with their question and replies, qualified history, origin of the existing
changes), `intake_logic.js` (spliced into `arch_logic.js`: `originOf`, `qualOf`, `intakeCreate`, `intakeResolve`,
`intakeVals`, `intakeOpen`, `intakeSay`, `intakeTurns`), templates `INTAKE`, `CHANGES`, `MINITRACK` in `build_arch.py`,
the pane hook in `vision_arch.py` and the proposal card and replies in `vision_parts.py`; lab: `startlab_data.py`,
`build_startlab.py`.

`vision_shrink.py` (new, end of `vision_build2.py`): a board file above about 2 MiB is not shown by the canvas, so the
vision is minified without loss (CSS, script comments and indentation, whitespace between tags, optional spaces in
inline styles), the LikeC4 source of elements is left out of the vision only, and the build fails within 24 KB of the
limit. Today: 2 052 399 bytes of 2 097 152.

## 5. Open

- The conversation script is deterministic in the prototype (one question per signal, keyword-driven iteration); the
  real one is the assistant with the knowledge-base MCP server (DEC-KB-43).
- Who may qualify: the portfolio architect for their portfolio (assumed); requesters see the outcome.
- A dismissed signal that comes back (same ticket reopened): not designed.
- Attached signals are not yet listed on the change page.
