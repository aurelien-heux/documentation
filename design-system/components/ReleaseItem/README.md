# ReleaseItem

One entry of the What's new feed: a release, an AI topic, a policy or a fix. Layout **D · Changelog**, chosen in the What's new layout lab (canvas, Prototypes page) against stacked, meta gutter, split and progressive. Live in the Community prototype.

## Anatomy

An elevated Card (`radius-md` 12, padding 20 × 24), top to bottom:

1. **Meta row.** Version (Open Sans 600 on `primary-container`, radius 4), type tag (Feature release `primary-container`, AI topic `ai-container` with the sparkle, Policy and Fix neutral), an action-required StatusChip when there is one ("Action required · by 3 Nov", "Acknowledge by 1 Nov"), then date · areas in body-small `on-surface-variant`. Unread: an 8 px `primary` dot and "New", right-aligned.
2. **Title** in title-large (20 / 28, 700), then the **summary** in body-medium `on-surface-variant`, 72 characters max per line, two sentences at most.
3. **Changes table.** One row per change inside a 1 px `outline-variant` frame (radius 8): tag (New, AI, Improved, Fixed, Changes, Check) · what changed (label-large 700, 200 px) · detail (body-small 13 / 18). Rows are separated by a `surface-container-high` hairline. A release without changes (a policy) has no table.
4. **Action line**, under a 1 px `outline-variant` divider: the tonal primary action (Read the notes · 4 min, Migration guide · 6 min…), then chips for Try it in the app (n steps), Watch (duration), I have read and understood, and for AI topics an "Ask the assistant about this" text button. At the end of the line, right-aligned: **Useful?** with two icon chips (thumb up, thumb down).
5. **Below the line**: the "What was missing?" reason chips after a thumb down, then the **Discussion expansion panel**, which ends every item (collapsed by default; its header is the summary bar).

The aggregated usefulness ("Useful for 87 % · 212 votes") is not shown to readers: it lives in Administration › Community › Releases.

## Responsive

- The item takes the feed width; the feed sits beside a 320 px side column from 1200 px and above it under 1200 px.
- Under 840 px a change row puts the tag and the title on one line and the detail under them. The action line wraps as two groups: the actions, then Useful?.
- Under 600 px the card padding drops to 16 px.

## Keyboard and screen reader

- The item is an `article` named by its title (`h2`). The changes table is `role="table"` with one `row` per change and three `cell`s.
- The Discussion panel header carries `aria-expanded` and the counts in its name. The thumbs are toggle buttons named "Useful: yes" and "Useful: no" with `aria-pressed`.
- Reading order follows the visual order; the unread dot has the word "New" next to it.

## Don't

- Don't use bullets for changes: one row per change, so they line up from one release to the next.
- Don't put more than one tonal button on the action line; the others are chips.
- Don't put the summary or the actions inside the table.
