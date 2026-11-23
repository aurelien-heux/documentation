# AgentRun

Decided 2026-11-23 (Agent follow lab, option C: both views on one run). For following AI agents that work on an object (a change, a request). Boards on the design-system canvas, section "Components · agent run" (`canvases/design-system/AgentRun.dc.html` usage, `AgentRunPanel.dc.html`, `AgentRunPage.dc.html`, `AgentOutput.dc.html`; built by `tooling/canvas/agent_run_build.py`). The lab is `canvases/labs/AgentLab.dc.html`. Example data: the four TOGAF agents of change CHG-14 (analysis, draft, review, implementation).

## One run, two views

- A **run** = one agent on one object, through its steps, to an output and, when the output must take effect, a **review gate** (PRI-01: nothing is applied before a person approves).
- **Assistant panel** = for the person in the conversation: milestones of the runs this conversation started or that wait for them; answer the gate in place.
- **Object page** = the record for everyone: an **Agents** tab with every run in process order, all steps, activity, output, history of runs.
- **Header indicator** = from anywhere: what runs, waits for you, or failed.
- **Output viewer** = the full output of one run, with its own address, opened from either view.
- Same state, steps, output and gate in both views; only the depth differs.

## When to use which

- **Panel**: the person started the agents from the conversation or asked about them there; the next thing needed is a decision or a short answer. One row per milestone (started, finished, waiting, failed), never one per step.
- **Page**: several people follow or review; you need every step, the activity, earlier runs or the full output; runs started by a signal, a schedule or another agent.

## Run status chip (8 states)

| State | Glyph | Colours |
|---|---|---|
| Queued | · | `surface-container-highest`, `on-surface-variant` tile |
| Running | ✦ + working dots | `ai-container` #9CF1F0, `ai` #004F50 tile — the only teal state |
| Waiting for you | ! | `primary-container` #E3DFFF + 2 px `primary` border (the review gate) |
| Waiting for <name> | ! | `primary-container`, no border, no buttons |
| Changes requested | ↩ | `warning-container` + `warning` tile |
| Done | ✓ | `success-container` + `success` tile |
| Failed | ✕ | `error-container` + `error` tile; Retry and View log |
| Cancelled (incl. superseded) | – | transparent, 1 px `outline` |

Order of attention when several runs are summed up (header, strip): Waiting for you → Failed → Changes requested → Running → Queued → Done.

## Parts

- **Header indicator**: right of the search, before the assistant button; the most urgent state and its count over the runs you started or must approve; one run → its object's Agents tab, several → a menu; hidden when nothing runs, waits or failed in the last 24 h.
- **Run strip** (panel): pinned under the panel header; chip, agent, n / m steps, trail of the steps (✓ ✦ !), Open in change. Steps tick here only. Disappears when every run is done.
- **Milestone row** (panel): started (n / m while running) · finished (output title, one-line summary, View output, Open in change) · waiting (2 px border, gate: question, primary action, Request changes when allowed, View output; after answering: "Approved by you · time") · failed (what failed, Retry, View log).
- **Stage track** (page): one card per agent in process order, never sorted by state: step number and name, agent, phase, chip, n / m steps, progress bar, next or output line. Waiting card 2 px border, selected card 1 px `primary` ring. Tab "✦ Agents n/m".
- **Run detail** (page): steps checklist (✓ done, ✦ current with the teal ring, number to do), gate (read-only "Waiting for <name>" for others), output summary (≤ 6 rows, View output), activity newest first with run numbers. Earlier runs are listed, never merged.
- **Review gate**: the question is an action on the object ("Confirm the scope", "Approve the change"); only the named approver sees buttons.
- **Output viewer**: header (output title, chip, agent, run, object, start, duration, started by, approved by; actions: the object the output lives in — pull request, page —, Copy link, Download); tabs by kind with counts, Summary first, Log last, only tabs with content; the gate at the bottom while it waits for you. Opens as a 640 px side sheet from the panel (full screen under 840 px), in place of the run detail on the page (back arrow), or from a link (the object page with the viewer open). Earlier runs: same viewer, chip "Cancelled · superseded by run n", no gate.

| Agent | Viewer tabs |
|---|---|
| Analysis | Summary (impacted elements with change marks) · Log |
| Drafting | Summary · Changes (YAML diff per file) · Views (rendered, in the notation's diagram frame) · Files · Log |
| Review | Summary · Checks (one row per rule, failing elements linked) · Log |
| Implementation | Summary · Files (merged commit, published pages, tickets) · Log |

Log = the execution trace: time, glyph, step or tool call, result, duration; never prompts or chain of thought. Diffs: + / − lead each line, added lines on `success-container`, removed on `error-container` struck through.

## Do / Don't

- **Do**: one row per milestone; name outputs by what they are (Impact analysis, Draft pull request #48, Review report); link every milestone to the page and every output to the viewer.
- **Don't**: stream steps or tool calls into the conversation; show Approve to a non-approver or approve on someone's behalf; keep teal once a run stops; move focus or open the viewer by itself when a run finishes; make Download the only way to read an output.

## Sizes, keyboard and screen reader

- Panel 360–480 px (default 400); strip and row cards `surface-container-lowest`, 1 px `outline-variant`, radius 12; glyph tile 20 × 20, radius 3; buttons 32 px high (filled for the gate action, outlined for Request changes, text for links).
- Milestone rows sit in the conversation's `aria-live="polite"` region; step ticks are not announced; the strip is `role="status"`; the gate is a group named by its question; working dots are `aria-hidden` and stop under `prefers-reduced-motion` (the word Running stays); stage cards are buttons with `aria-pressed`; the viewer's tabs are a tablist.
- **Angular / React:** not built yet; bindings follow the React + shadcn decision (DEC-04).
