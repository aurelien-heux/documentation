# Subheader

The first row of a page that sits under another one: an item, a step, a document, a sub-section. It replaces the back button: going back is **never a button on its own row**. The back arrow, the page's name, its context and its actions share one row, so going back costs no extra line and always says where you are.

## Anatomy (left to right)

1. **Back** — IconButton 40 px (arrow_back, `on-surface`), named by where it goes: "Back to the Catalog", "Back to all ideas". No label next to the arrow.
2. **Lead** (optional) — what identifies the item before its name: the Catalog kind tile, an avatar.
3. **Title** — the page's own name, title-large (22 px; 20 px in the prototypes, 18 px under 600 px), `on-surface`. It is an `h2`: the top app bar holds the page context, not an `h1`.
4. **After the title** (optional) — one status: a StatusChip ("Live", "In review").
5. **Divider and context** — a 1 px `outline-variant` vertical divider (20 px high), then the context in body-small `on-surface-variant`: what the reader needs to place the page ("MCP server by Platform team · v2.3", "Delivery platform portfolio · owned by the Environments team", "Client team · started 26 Oct · buddy: Marta Kowalski").
6. **Actions** (optional, right-aligned) — the page's primary action and at most two more: Add to my assistant, the publication stepper, an application selector, Ask.

## Writing the context

- Plain words a newcomer understands; at most three short facts, separated by ` · `.
- Say what the title does not: who owns it, its state, when it changed, how far along it is. Never repeat the title, the feature name already in the app bar, or the parent's name alone ("Surveys", "Administration").
- No ids, paths or jargon in the context: they belong in the page's metadata line.

## Layout

- One row, at least 48 px, aligned to the start of the content (the arrow's hit area overhangs the content edge by 8 px, so its glyph lines up with the text below).
- The text block takes the free space and wraps: title, then context on the same line when it fits, on the next one when it does not. Actions keep their own line under 600 px.
- A 1 px `outline-variant` bottom border separates it from the page content, 8 px under the row. No background: the subheader is part of the page, not of the app bar.
- From 600 px the row does not wrap: the title truncates last, the context first, both with an ellipsis.

## When to use it

- An item opened from a list (Catalog item, idea on a phone, a run), a step of a flow (Publish a skill), a document opened from a space (detailed design), a sub-section with its own name (Administration group in a hub).
- **Not** on top-level pages reached from the navigation: they start with their content (the top app bar already names them).
- **Not** with a second search field or an Ask button: the top app bar's search-or-ask field is the only way to search or ask from a page. A filter inside a list is a filter, not a search bar.

## Responsive

- From 600 px: one row: arrow · title · status · divider · context · actions.
- Under 600 px: the arrow stays at the top left, the title wraps beside it, the context goes under the title without the divider, and the actions take their own line.

## Keyboard and screen reader

- The back IconButton is first in the reading order of the page, named "Back to …"; Esc does not trigger it.
- The title is the page's `h2`; the context is plain text after it.

## Angular Material

| Element | Angular Material |
|---|---|
| Back | `mat-icon-button` with `arrow_back`, `aria-label="Back to …"`, `routerLink` to the parent |
| Title | `h2` with the title-large type token |
| Status | StatusChip |
| Actions | `mat-flat-button` / `mat-stroked-button`, `mat-select`, `mat-stepper` header |

## Don't

- Don't put a back chip or a "Back" link on its own row.
- Don't repeat the parent's name as the arrow's label: it goes in the context.
- Don't add a breadcrumb: the arrow and the context are enough, and the app bar has the feature.
- Don't add a second search field or an Ask button in the page: the app bar's search-or-ask field does both.
