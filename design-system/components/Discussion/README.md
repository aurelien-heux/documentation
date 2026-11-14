# Discussion

The conversation about one item, a What's new release or an Idea, in **one expansion panel** at the end of the item. People ask questions, share use cases and workarounds, and the platform team, champions and the author reply in the same threads. The component, its anatomy and its rules are the same for releases and ideas. It is live in the Community prototype and in the What's new and Ideas layout labs. It replaces the earlier QandA component.

## Where it appears

- **What's new.** Every ReleaseItem (layout D · Changelog) ends with a Discussion panel.
- **Ideas.** Ideas use layout E (a 320 px stack with the idea beside it), and the idea detail ends with the same Discussion panel. It is the only thread on an idea.
- **Elsewhere.** List rows, the admin triage and notifications show the compact count, "13 messages". The Ideas list can be sorted by Most discussed.
- **Not a support channel.** A broken run goes to Feedback, and a request that needs a decision becomes an Idea. Moderators can move a thread to either.

## The expansion panel

- **Container.** One panel per item: 1 px `outline-variant` border, radius 12, `surface-container-lowest` background (white in light), no shadow. Never several panels, and never an accordion.
- **Header = summary bar.** A full-width button, 48 px minimum, on the panel colour (no tint), with the `primary` 6 % hover layer, and the panel's only control. Participant avatars use container pairs (`ai-container`, `primary-container`, `warning-container`, `success-container`, `secondary-container` with their `on-*` text) so the initials read in both themes. Left to right:
  - chevron;
  - "Discussion" in title-small;
  - up to three participant avatars (24 px);
  - "7 threads · 18 messages" in body-small;
  - a neutral StatusChip "Platform team replied" when the team has taken part;
  - "Last message 1 h ago" (or "No messages yet");
  - **Show** / **Hide**, right-aligned in `primary`.
- **Expanded.** The panel keeps its border and colour; the chevron (`on-surface-variant`) turns up, Hide shows, and a 1 px `outline-variant` divider separates the header from the body. No tint, no shadow: the open state is told by the chevron, the label and the content, not by colour. The body fades in over 200 ms with a 4 px slide (no motion under reduced motion). The same header collapses the panel.
- **Collapsed by default**, everywhere. A link to a message (a notification, a reply to you, the admin inbox) opens the panel with that message in view.

## Threads and messages

- **Thread.** It opens with a message: 32 px avatar, author in label-large, the author's role chip if they have one, date in body-small `on-surface-variant`, then the text in body-medium (72 characters max per line).
- **Replies.** They sit under the opening message, indented 14 px with a 2 px `primary-container` rule on the left. Each reply has a 24 px avatar, its author, role chip, date and text. One level only: a reply to a reply is posted at the end of the same thread.
- **Role chips.** Platform team is neutral, Champion is `primary-container`, Author (of the idea) is neutral. Other people have no chip.
- **Long threads.** A thread shows its **last two replies**. The earlier ones sit behind a text link "Show 1 earlier reply" / "Show 4 earlier replies" above them; opening it moves focus to the first reply that appears.
- **Reply.** Under each thread, a **Reply** text button (`aria-expanded`) and the reply count ("3 replies", "No reply yet"). Reply opens an inline field, "Reply to Nadia Rahal", with a filled **Send** button. The reply is added at the end of the thread and everyone in the thread is notified.
- **New message.** The field is always last in the panel: your avatar, an outlined text field labelled "New message" whose placeholder suggests the use ("Ask a question or share how you use this release…", "Ask the author, add a use case or a workaround…"), and a tonal **Post** button. A new thread appears first.
- **Order.** Your new threads come first, then the threads with the latest activity.
- **Show more, pages of three.** The panel opens on three threads. Under them sits a text link "Show 3 more threads" (`primary`, underlined, a `button` underneath) and "3 of 7 threads shown". Each press adds three threads, moves focus to the first new one, and announces "3 more threads shown, 6 of 7". There are no numbered pages; collapsing the panel goes back to three.
- **Empty panel.** One line: "No messages yet. Start the discussion: champions and the platform team take part."

## Behaviour

- **Who takes part.** Everyone can start a thread or reply. The platform team and feature admins carry the Platform team chip, champions carry Champion on their topics, and the author of an idea carries Author.
- **Service level.** A thread with no reply after 2 working days appears in Administration › Community › Feedback › Inbox, with the source "Discussion" and its item.
- **Moderation.** Report, hide, or move a thread to Feedback or to an Idea.

## Responsive

The panel takes the item width and never sits in a side column of its own. Under 600 px the header wraps onto two lines, with Show / Hide on the first; opening avatars drop to 24 px and replies indent 10 px.

## Keyboard and screen reader

- **Header.** A `button` with `aria-expanded` and `aria-controls` pointing to the body, a `region` named "Discussion". Enter and Space toggle it and focus stays on it.
- **Header's accessible name.** It starts with the visible label: "Discussion · 7 threads, 18 messages, platform team replied, last message 1 h ago". The state is shown by the chevron, the expanded look and `aria-expanded`, never by the label alone.
- **Focus moves.** Threads and replies are focusable (`tabindex="-1"`): Show more and Show earlier replies move focus to the first message that appears, and a polite live region reports what was added.
- **Reply.** The Reply button has `aria-expanded` and `aria-controls` pointing to its field. A posted message is announced once.
- **Focus ring.** The header's ring is drawn inside the panel (offset −3 px).

## Angular Material

`mat-expansion-panel` (alone, not in a `mat-accordion`), `hideToggle` with our own chevron in `mat-expansion-panel-header` (48px collapsed and expanded). Threads are plain markup. A `mat-button` styled as a link serves Show more and Show earlier replies, a text `mat-button` Reply, `mat-form-field` outline with a filled `mat-button` Send for replies, and `mat-form-field` outline with a tonal `mat-button` Post for new messages.

## Don't

- Don't put several Discussion panels, or an accordion, on one item.
- Don't nest replies more than one level, and don't add votes, "same question" counts or an "accepted answer".
- Don't add a second toggle (a chip in the action line, a Hide button in the body): the header is the only one.
- Don't load threads or replies on scroll: Show more and Show earlier replies are explicit, so the new-message field stays reachable.
- Don't use teal for team replies, even when the assistant suggested the text: a person posts it, and their role chip says who they are.
