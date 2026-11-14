# CatalogItem

One item of the Catalog: a **skill** published by people, or a **tool** or an **MCP server** published by the platform team, for the assistant and for Sweep. It comes in three forms: the **card** (Catalog › Browse), the **row** (Mine, Administration › Core › Catalog) and the **page** (one item). It is minimal by default: a tag, a count or a button appears only where it decides something. It is live in the Catalog lab.

## What is in the Catalog today

| Kind | Tile | Items |
|---|---|---|
| **MCP server** | `MCP` on `ai-container` | **DevOps** (pipelines, builds, deployments, pull requests), **Knowledge base** (Docs, runbooks, the architecture model, ARB decisions) |
| **Tool** | `TL` on `tertiary-container` | **Deploy environment**, **Reserve environment** (from Environments), **Create Jira ticket** |
| **Skill** | `SK` on `primary-container` | Published by people: migrations, runbooks, reviews, release notes |

## Card

- 1 px `outline-variant` border, radius 12, `surface`, 16 px padding, no shadow. The whole card is one button that opens the page.
- **Kind tile** 36 px, radius 10, with the kind's letters, then the **name** in title-small on one line.
- **One line** of description, two lines at most.
- **Footer:** "author · team" (or the owning team for tools and MCP servers) on the left, "n uses" on the right.
- **No tags.** Scope, review and whether the item can change something are on the page.

## Row

The name with one line of usage, one **stage** tile (Draft, In review, Published), who can use it, the version, and one action (Continue, Open, New version).

## Page

- One column, 760 px at most.
- Header: kind tile 48 px, name in title-large, "kind · author · version" in body-small, and **one action**, Add to my assistant (In my assistant once added).
- The description.
- When the item can change something, one line with a lock: "Asks before it does anything that changes something: run pipeline, open pull request."
- **Try asking:** the example requests, each with a Try it link that opens the assistant with the item on for this conversation only.
- **Tools it provides** (MCP server), **Action** (tool) or **Uses** (skill): a plain list. "changes something · source" goes in the metadata.
- The **Discussion** panel, collapsed by default.
- One line of metadata (Reviewed, uses in 30 days, works with, source) and Report a problem, which goes to Community › Feedback.

## Publication process (skills)

1. **Write.** In the app, or import from a Git repository (SKILL.md and skill.json; versions follow tags). A draft is usable by its author only.
2. **Test.** Automatic checks: the manifest, no secrets in the text, every tool exists, and whether the skill changes something, worked out from its tools. Then one try in the assistant with the skill on. Both are required to continue.
3. **Submit.** Pick who can use it: just me, my team (live at once; the team is responsible), or everyone (reviewed first).
4. **Review** (everyone only). A champion or a platform admin tries it, ticks three points, talks with the author in the skill's discussion, then publishes or asks for changes. Target: 2 working days.
5. **Published.** The skill is in the Catalog and the assistant's Tools menu; admins can turn it on for Sweep phases.
   - A new version goes back through Test.
   - It returns to Review only if it adds an action that changes something.
   - Retiring a skill names its successor and gives users 30 days.

## Responsive

- **Cards:** three per row from 1200 px, two from 840 px, one below.
- **Page:** keeps its single column.
- **Below 600 px:** the card padding is 12 px.

## Keyboard and screen reader

- A card is a `button` named by the item.
- Add to my assistant has `aria-pressed`.
- Each Try it link names its example.
- The publication stepper marks the current step with `aria-current="step"`.

## Angular Material

| Element | Angular Material |
|---|---|
| Card | `mat-card` (outlined) as a button with `matRipple` |
| Row | `mat-table` |
| Stage | StatusChip |
| Kind switch | `mat-button-toggle-group` |
| Add to my assistant | filled or tonal `mat-button` |
| Publication | linear `mat-stepper` |

## Don't

- Don't add tags to cards. If a status matters, put it on the page or in Mine.
- Don't give the item page a second primary action.
- Don't let the author choose whether the skill changes something: it follows from the tools.
- Don't put a second comments box on an item: the Discussion panel is the one place.
