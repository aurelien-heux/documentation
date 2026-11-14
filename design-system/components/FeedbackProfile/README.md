# FeedbackProfile

The editor for one feature's feedback form, with a live preview of the side sheet users see. All feedback administration lives in **Administration › Community › Feedback**, which is for admins only (variant A in the Feedback administration lab). The platform team reads the inbox, so feedback stays next to ideas, releases and discussions: listen, decide, ship and announce in one module. It is live in the Community prototype and in the Administration and Feedback administration labs.

## Who sees what

| Section of Community › Feedback | Platform admin | Feature admin (right **Feedback · Sweep**) |
|---|---|---|
| **Profiles** | Every profile (Sweep, Environments, Docs, Assistant, global); Edit opens the editor below the table | The Sweep profile only, opened straight away (tab "Profile") |
| **Inbox** | Every feature, with a filter per feature | Sweep items only; the filter is locked |
| **Surveys** | Micro-surveys, NPS and checks | Hidden |
| **Solicitation policy** | Sets the shared cap | Read-only |

- **The scoped right.** "Feedback · <feature>" is separate from "Community admin". A feature admin sees the Community group reduced to one item, **Feedback · Sweep**, with no releases, tours, ideas or surveys. A note at the top says so.
- **Kept reversible.** FeedbackProfile stays a component of its own and the right is per feature. If a dedicated team takes the inbox later, or an overview across features is needed, the section can move into its own Feedback module (variant B) without redesigning it.

## Anatomy

- **Section tabs:** Profiles · Inbox (count of new items) · Surveys · Solicitation policy (`tablist` "Feedback"), then the cap tile "Shared cap · 1 prompt per user every 7 days", right-aligned.
- **Profiles table:** profile and owner, status, entry points, questions, sampling, routing, and Edit (Close on the open row). The open row has a 3 px `primary` inset.
- **Editor card** (24 px padding, radius 12, `surface`):
  - the title "Sweep · feedback profile" in title-large, the line "FeedbackProfile component · one editor for every feature's profile", and a **Profile on / off** filter chip on the right;
  - **Entry points**: filter chips for Page button, After an action, On AI answers and Account menu (Account menu is for the global profile);
  - **Questions · n of 3**: one row per question, with a 24 px number badge, a type select (Thumbs, Scale 1–5, NPS 0–10, Single choice, Multiple choice, Text), the question field and a Remove icon button. An **Add question** chip appears while there are fewer than three questions;
  - **Sampling**: 10 %, 20 %, 50 % or 100 %, for after-action prompts only;
  - **Routing**: Team inbox only, Inbox + Jira project, or Inbox + Teams channel, with the hint "Bugs always go to Jira; never to Ideas";
  - **Options**: Allow anonymous, Attach context;
  - an action row under a 1 px `outline-variant` divider: **Close** (text button, platform admins only) and **Save profile** (filled).
- **Preview** (a 380 px column), headed "Preview · side sheet in Sweep": the side sheet as the user sees it, with the title, "Goes to Sweep team", each question with its type, the Attach context chip when that option is on, and Send.

## Behaviour

- Changes apply within 5 minutes of **Save profile**, and a snackbar says so.
- A profile has at most three questions; Add question disappears at three. A profile with no question shows "Add at least one question" in the preview.
- The Feedback page button and the thumbs on AI answers are started by the user and never count against the shared cap. After-action prompts do count. They are sampled, never appear during a running action and can always be dismissed.
- Bugs always go to Jira, never to Ideas. Turning feedback into an idea needs the author's consent, asked from the inbox.
- Discussions with no reply after 2 working days appear in the inbox with the source "Discussion".

## Responsive

Below 1200 px the preview moves under the editor and the table scrolls sideways in its card. Below 600 px:

- the card padding drops to 16 px;
- a question row wraps, with the field on its own line;
- the cap tile takes its own line;
- the feature-admin note stacks.

## Keyboard and screen reader

- **Tabs.** The section tabs are a `tablist` named "Feedback".
- **Chips.** Entry points, Sampling, Options and Profile on / off are toggle chips with `aria-pressed`.
- **Questions.** Each question field is named "Question n", and Remove is named "Remove question n".
- **Routing.** The Routing select has a visible label.
- **Table.** Each row button names its profile, for example "Edit the Sweep feedback profile".
- **Read-only cap.** For a feature admin, the cap chips have `aria-disabled`.

## Angular Material

| Element | Component |
|---|---|
| Section tabs | `mat-tab-nav-bar` |
| Profiles table | `mat-table` |
| Entry points, Options | `mat-chip-listbox` (multiple) |
| Sampling | `mat-chip-listbox` (single) |
| Question type, Routing | `mat-select` in an outline `mat-form-field` |
| Question | outline `mat-form-field` |
| Remove | `mat-icon-button` |
| Save profile | filled `mat-button` |

The component ships in the Community remote module (`community-admin`).

## Don't

- Don't give a feature admin the full Community admin right just for feedback: use the scoped right Feedback · <feature>.
- Don't copy the editor into feature modules; there is one place to edit profiles.
- Don't let a feature admin change the shared cap or the surveys.
- Don't add a fourth question or a free-form "custom HTML" step.
