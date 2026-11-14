# AIToolbox

The design system for AIToolbox, an IT platform of utilities for infrastructure and development teams. It is Material Design 3 with a AIToolbox palette, type pairing and a small set of rules that keep the product calm in daily use and unmistakable when something matters.

## Principles

1. **Calm chrome, loud signals.** In light, the page surface and cards are near-neutral, containers (dialogs, menus, pickers, panels) are a pale purple and the navigation frame — top app bar and rail (or drawer) together — is the one deeper violet band; in dark everything sits on night tones with a deep-violet primary used as tints, so the lime Run button, the teal AI badge and the status colours are the strongest signals on screen.
2. **One colour, one meaning.** The Sweep purple decides, the pale purple groups and filters, the lime Run button executes (the Sweep lime with a Sweep purple label; lime means “start”, never a status), teal is AI (the features and the brand’s own tag), green/amber/red are health. A colour is never borrowed for decoration.
3. **Dense but breathable.** Ops screens hold a lot; the 4 px grid, 56 px fields and 40 px buttons keep them scannable without becoming cramped.
4. **Data looks like data.** Keys, paths, IDs, timestamps and log output are set in Open Sans at weight 600 and, where it helps, on a container tone, so the eye can tell data from prose without a monospace face.
5. **Accessible as built (WCAG 2.2 AA).** Every text pair meets 4.5:1 (body text 13.9–17.1:1, coloured text ≥ 7:1 on surface); focus is always visible; status is never told by colour alone; motion stops when the user asks.
6. **Minimal by default.** Show a tag, a count or a button only where it decides something now. A card is a name, one line and who made it; status sits in one line of metadata; a page has one primary action. Add the rest when people ask for it, not before. Going back is a Subheader (arrow, title, context and actions in one row), never a button on its own row; the header's search-or-ask field is the only search field on a page and the only Ask entry in it.

## Colour

Dark is the first-class theme — "night" — and light is its daytime counterpart, not an inversion. Since tokens 5.0 the palettes come from the three **Sweep colours**: the **Sweep purple** #39235F for the primary (hue 303; it is the light primary itself, tone 20), the **pale purple** #DED7EB for the secondary (hue 296, the hue of the neutrals; it is the light `secondary-container`) and the **lime** #DCEAB4 for the tertiary (hue 125; `tertiary-container`, pinned to the lime in both themes, is the Run button). The neutrals come from **night** #0D0B14 (hue 296): chroma 12 in dark, so night surfaces are visibly violet; in light the page surface, the lowest container (cards) and the outlines drop to chroma 4, the four containers are a light purple one step lighter than Material's — tones 97 / 96 / 94 / 92 (#FAF4FF · #F8F1FF · #F2EBFA · #ECE5F4) — and the navigation is the deepest light surface, `nav-container` #EDE4FF. **One tone rule:** light roles at tone 30 (the primary at 20), dark roles at 80, containers 90 / 30, text on containers 10 / 90. Kept from 4.x: the whole dark primary family on the lavender #C4C0FF (hue 288) and the light `primary-container` #E3DFFF. The neon green #00F29E is a brand colour now: it lives in the logo cursor only.

### Roles and what they do

| Role | Use for | Never for |
|---|---|---|
| `primary` (Sweep purple #39235F in light, lavender #C4C0FF in dark) | filled buttons, active nav bar, selected tab, focused field, switches on, links, the keyboard focus ring (2 px with a 2 px gap; text fields take no ring, their border turns 2 px `primary`), “Toolbox” in the wordmark | status, decoration |
| `secondary-container` (the Sweep pale purple #DED7EB in light) | tonal buttons, filter chips, the active navigation pill (with a 3 px `primary` bar: the pill is 1.1 : 1 on the band), env badges, avatars | emphasis |
| `tertiary-container` / `on-tertiary-container` (the Sweep lime, both themes) | the one action that starts work: Run, Deploy, Apply, New run — a tonal button, lime #DCEAB4 with a Sweep purple #39235F label and play icon (10.4 : 1), no edge; max one per screen. Row run actions (Re-run) are text buttons in `primary` with the play icon in a small lime disc; “Deploying…” chips | dialogs (confirm with filled `primary`), destructive actions, status (lime is not the `success` green: Passed stays a green chip with its ✓) |
| `tertiary` (olive #404B23 in light, pale lime in dark) | a signal, never a fill: the working dots of a running command, deploy states | button fills, dialogs, status (health green is `success`, hue 145, always with its ✓ tile) |
| `ai` (deep teal #004F50 in light, light teal #80D5D4 in dark) / `ai-container` | AI marks drawn as lines or dots (working dots, pen orbit, guide track, the sparkle icon); suggestion cards and AI chips on `ai-container` — always with the sparkle icon, so a teal tint is never read as a selection | chrome, navigation, non-AI buttons |
| `success` / `warning` / `error` (light at tone 30) | health chips, log levels, badges, validation — always with a glyph and a word: the three share one lightness | brand, decoration, meaning by colour alone |
| `logo-box` / `on-logo-box` / `logo-cursor` / `logo-ai` / `on-logo-ai` (brand group) | the logo family only: mark, favicon, app icon, brand loader, state marks | any UI surface or control |
| `surface-container-*` | tonal layering instead of shadows | — |

Surfaces layer tonally: page `surface` → panels `surface-container-low` → app bar `surface-container` → dialogs and menus `surface-container-high`. Shadows (`elevation-*`) appear only where Material asks for them: elevated buttons and cards, FAB, dialogs, snackbars.

### Contrast

All 260 text/ground pairs in the tokens meet AA (4.5:1). Coloured text on `surface` clears 7:1 in both themes (the light roles are tone 30: 8.9:1 and more; `primary` 12.7:1); the lowest pairs are coloured text on tinted containers (≥ 4.5:1). `on-surface-variant` is the lightest "muted" text allowed on `surface` (8.9:1 light, 10.9:1 dark). `outline` is for borders only, never text. White text sits on the light `primary`, `secondary`, `tertiary`, `ai`, `error`, `success` and `warning`; the lime `tertiary-container` (Run) takes `on-tertiary-container`, the Sweep purple; everything else uses the matching `on-*-container`.

### State layers

Hover and pressed are a translucent layer over the element. On neutral surfaces (page, tables, cards, menus, navigation, header) the layer is the **primary violet at 6 %** for hover and **10 %** for pressed (14 % dragged): white → #F3F2F5, `surface-container` → #EDE5F5, `nav-container` → #E2D8F5; in dark the lavender primary does the same on night tones. It keeps the surfaces in their own hue instead of greying them. Coloured components — filled, tonal, Run (purple layer on lime), AI, selected chips, the active navigation item — use their own content colour (`on-primary`, `on-secondary-container`, `on-tertiary-container`, `on-ai-container`) at the same opacities. The grey `on-surface` layer is not used. **Focus adds no layer (0 %):** Angular Material keeps its focus layer on a button after a mouse click, which read as an extra outline; keyboard focus is shown only by the 2 px focus ring. Tokens: `--md-sys-state-layer-color` and `--md-sys-state-*-opacity` in `css/tokens.css`; Angular overrides in both theme files.

## Typography

- **UI family: BNPP Type** (weight 500) for every display, headline, title and label style: app bars, buttons, chips, navigation, dialog titles.
- **Body family: Open Sans** (400, 600 for emphasis) for body-large/medium/small, and for code, keys, paths, IDs and log output (set at 600 so data reads apart from prose). There is no monospace face in the system.

BNPP Type ships as a font file in `fonts/` and is declared by `tokens.css`. Open Sans loads from Google Fonts: `https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap`. BNPP Type is supplied in one weight, so UI emphasis comes from size and colour, not from bold. The wordmark stays the outlined SVG in `assets/Logos`.

## Shape

The Material shape scale with a **16 px ceiling**: `radius-lg` (16) is the largest corner on any rectangle — buttons, segmented buttons, search bars, navigation items (hover and active), dialogs, bottom and side sheets, pickers, the large FAB; `radius-md` (12) for cards, tables and panels; `radius-sm` (8) for chips; `radius-xs` (4) for text fields, menus, tooltips and snackbars. `radius-xl` is pinned to 16 px and `radius-full` is reserved for circles (avatars, badges, radio, switch, icon-button state layers) — never for a button or a pill. The logo's box corner is 10/64 of its height, which lands on `radius-lg` at 64 px.

## Spacing

A 4 px grid. Inside components: `space-2` between chips and buttons, `space-4` for field and card padding, `space-6` for dialog padding and filled-button horizontal padding. Between things: `space-6` between fields in a form, `space-8` between page sections, Page side margins follow the window class — 16 px Compact, 24 px Medium and Expanded, 32 px Large and up (see Layout and breakpoints); `space-16` (64 px) is the gutter of long-form reading pages.






## Layout and breakpoints

Five **window size classes** from Material 3 decide the layout. A breakpoint is the lower bound of a class: a window of 600 px is Medium. Build mobile-first with `min-width` queries on the **window width** — never on the device or the user agent.

| Class | Window width | Typical | Page margin | Columns | Gutter |
|---|---|---|---|---|---|
| **Compact** | 0–599 px | phones in portrait | 16 px | 4 | 16 px |
| **Medium** | 600–839 px | tablets in portrait, foldables, narrow windows | 24 px | 8 | 24 px |
| **Expanded** | 840–1199 px | tablets in landscape, small laptops, half a desktop screen | 24 px | 12 | 24 px |
| **Large** | 1200–1599 px | laptops and desktops — the reference mockups are 1440 × 900 | 32 px | 12 | 24 px |
| **Extra-large** | ≥ 1600 px | large desktop monitors | 32 px | 12 | 24 px |

**The shell follows the window.** Navigation, header, assistant and overlays change at the class boundaries:

| | Compact | Medium | Expanded | Large | Extra-large |
|---|---|---|---|---|---|
| Navigation | NavigationBar at the bottom (80 px, 3–5 destinations, Assistant one of them); the rest in a modal drawer from the top-bar menu | NavigationRail (80 px); its menu button opens the drawer over the page (modal, scrim) | NavigationRail (80 px); its menu button opens the drawer over the page (modal, scrim) | NavigationRail (80 px) by default; its menu button opens the standard drawer on demand (300 px, pushes the page) | Same as Large: rail by default, standard drawer on demand |
| Top app bar | 56 px · menu · logo mark · search icon · bell · avatar; help in the user menu | 64 px · logo · search field 240–440 px, Ask chip as an icon · assistant · bell · avatar; help in the user menu | 64 px · logo · search field 320–440 px, Ask chip as an icon · assistant · bell · help · avatar | 64 px · logo · search field 440 px with the labelled Ask chip · assistant · bell · help · user chip with name and role | same as Large |
| Assistant | Full-screen view, the NavigationBar destination | Takes the page area in place, beside the rail; the header button gives the page back | Takes the page area in place, beside the rail; the header button gives the page back | Docked split view, 400 px (320 – min(640 px, 50 %)), beside the rail; an open drawer folds back to the rail when the page would drop under 720 px (windows under about 1480 px) | Docked split view beside the rail; an open drawer stays while the page keeps ≥ 720 px |
| Page actions | The primary action becomes an extended FAB 16 px above the NavigationBar (shrinks to the icon on scroll); the others go to the ⋮ menu; Run stays in the selection bar | Primary button kept; secondary actions as icon buttons with tooltips | All buttons with labels; Filter as an icon button | All buttons with labels | All buttons with labels |
| Dialogs | Forms: full-screen dialog (close · title · Save in a top bar); confirmations stay basic dialogs, 16 px from the edges | Basic dialog 280–560 px | Basic dialog 280–560 px | Basic dialog 280–560 px | Basic dialog 280–560 px |
| Sheets | BottomSheet (a SideSheet becomes one) | Modal SideSheet (over, scrim) | Modal SideSheet (over, scrim) | Standard SideSheet (pushes the page) or modal | Standard SideSheet or modal |
| Snackbar | Full width minus 2 × 16 px, 16 px above the NavigationBar | 344–600 px, bottom of the page area at the page margin | 344–600 px, bottom of the page area at the page margin | 344–600 px, bottom of the page area at the page margin | same as Large |
| Page margin · grid | 16 px · 4 columns · 16 px gutters | 24 px · 8 columns · 24 px gutters | 24 px · 12 columns · 24 px gutters | 32 px · 12 columns · 24 px gutters | 32 px · 12 columns · 24 px gutters |

**Page context in the top app bar.** Right of the logo, the feature name (label-large 600) over a one-line summary (body-small) name the page; there is no page title block and no breadcrumb, so the page starts with its content. Going back to a parent is a subheader chip with a back arrow ("← Runs"). See `components/TopAppBar`.

**Navigation.** The rail is the default navigation from 600 px, at every window class: menu button, then Sweep · Environments · Docs · Catalog · Community (feature marks, 24 px; the Catalog is where people publish and use skills, tools and MCP servers for the assistant and Sweep; Community holds the What's new feed, the Guides and the Ideas), then Administration for people with at least one admin right (features have no admin entry of their own: each feature ships its administration as a remote module that the Administration shell loads by right) and Cookies at the bottom (no Terms, no version in the navigation). The drawer opens only on demand from the rail menu button — standard (pushes the page) from 1200 px, over the page with a scrim below — and every session starts on the rail. Settings lives in the account menu of the header, never in the navigation; the assistant and notifications stay in the header. Under 600 px the NavigationBar takes over.

**The page content follows the page area**, not the window: the rail (80 px, or the drawer when opened, 300 px) and the docked assistant (400 px) take part of it, so a 1440 px window with the assistant open gives the page about 900 px. The page area is a size container (`.ait-page`) and content rules are written against its width, measured between the page margins:

- **KPI cards.** 1 per row under 300 px · 2 per row from 300 px (a 360 px phone) · 4 per row from 720 px of page area.
- **Side column (AI suggestion, alerts, deploy window).** Beside the table, 360 px (400 px from 1440 px), when the page area is ≥ 1040 px; otherwise stacked full width: alerts above the table, the other cards under it.
- **Data tables.** Under 600 px the rows become a two-line list (state mark + name, a meta line, actions in the row menu); 600–799 px only priority-1 and -2 columns + the row menu; from 800 px every column. A table that must keep every column scrolls inside its own frame with the first column sticky — the page itself never scrolls sideways.
- **Forms.** One column, 600 px max; pairs (start / end date) side by side from 600 px of page area; actions at the end, full width under 600 px.
- **Tabs.** Scrollable under 600 px of page area (counts kept), never wrapped.
- **Reading pages (docs, settings, policies).** Text column 840 px max, centred in the page area; dashboards and tables use the full width.

**Height.** Under 480 px of height (a phone in landscape) the NavigationBar becomes the rail, the top app bar scrolls away and forms in dialogs open full screen.

**Touch.** Target sizes follow the pointer, not the width: 48 px targets under `(pointer: coarse)` at every size, 40 px controls in a 48 px slot otherwise.

**Tokens and code.** `breakpoint-*` and `layout-*` tokens in `tokens.json`; `--ait-page-margin`, `--ait-grid-columns`, `--ait-grid-gutter` and the `.ait-page`, `.ait-grid`, `.ait-kpis`, `.ait-split`, `.ait-col-p2 / -p3`, `.ait-reading`, `.ait-form` helpers in `css/tokens.css`; Sass mixins `bp.from()`, `bp.below()`, `bp.only()`, `bp.short`, `bp.page-from()` in `angular/_breakpoints.scss`; for Angular, `AitWindow` queries and the `AitWindowClass` service (signals: `windowClass`, `navigation`, `drawerMode`, `assistantMode`, `fullScreenDialogs`) in `angular/breakpoints.ts` — the CDK's own `Breakpoints` constants (600 / 960 / 1280 / 1920) do not match Material 3.

**Test** at 320 (WCAG reflow, 1280 px at 400 % zoom), 360, 600, 768, 840, 1024, 1200, 1440, 1600, 1920 px, and 740 × 360 (phone in landscape). At 320 px nothing is lost and the page never scrolls sideways (WCAG 1.4.10); only a data table or a code block may scroll, inside its own frame.

## Iconography

Outlined icons, 2 px stroke, 24 px grid (18 px inside buttons and chips, 22 px in app bars). Icons take the colour of the text next to them. Never emoji as icons. Icon-only buttons carry an `aria-label`.

## Logo

The mark is the **toolbox prompt**: a toolbox silhouette with a squared handle, holding a terminal `>_` with a neon-green cursor. The box is **night** — `logo-box` #0D0B14, the seed of the palette, with a white `>` (`on-logo-box`) and the full neon cursor (`logo-cursor` #00F29E) on light backgrounds; on dark backgrounds the box is lavender (`primary` #C4C0FF) with a night `>` and an emerald cursor (#006C44). The night box is the one place the raw seed appears; UI surfaces use the tonal `surface-*` roles. The mark carries the **AI badge**: a light-teal `ai` tile (#80D5D4 in both themes) with “AI” in `on-ai` (#003737) on the box's top-right corner, cut out of the silhouette so the two never touch (from 24 px; the favicon and app icon use the plain mark). The wordmark is “AIToolbox” in Manrope 800, “AI” in `on-surface` and “Toolbox” in `primary`. In prose the name is one word, AIToolbox. Alignment: the `>_` is centred in the box on one baseline; in the horizontal lockup the capitals of “AIToolbox” are as tall as the box and centred vertically on the whole mark (badge to box bottom); in the stacked lockup the mark and the wordmark are centred on one vertical axis. Use the horizontal lockup by default, the stacked lockup in square slots, the mark alone from 24 px up. Below 32 px the favicon glyph (the `>_` on a night tile) replaces the mark. Clear space is a quarter of the mark's height on every side. Do not rotate, outline, add gradients, or set the wordmark in another face. All files are in `assets/Logos`; the chatbot avatar is the brace box in `assets/Chatbot` — `{ >_ }` as one continuous outline — never the brand mark.

## Feature marks

Each feature has its own mark, separate from the product logo: Sweep (broom and sparkle), Docs (shelf), Environments (promotion path), Notifications (bell), the Chatbot (brace box, `assets/Chatbot`) and **Architecture** (three stacked layers, `assets/Features`). They identify the features in the navigation (24 px), feature headers (32–48 px), empty states and splash (64 px and up), the docs site and release notes; the AIToolbox logo stays the product brand and the two are never placed side by side as equals. Light files: deep violet `primary` #39235F, teal `ai` 50 #278383, green `tertiary` 60 #00A56B; dark files: lavender #A6A2F8, light teal #80D5D4, neon #00F29E. Colours are fixed per file: pick the file that matches the surface, never recolour. Each mark comes as **static** (default), **once** (an entrance that plays one time and holds the static mark) and **loop** (a working motion, one looping mark per screen at most); under `prefers-reduced-motion` the static mark shows. The marks of Sweep, Docs, Environments and Notifications are in the brand package (`brand/feature-marks/`); Architecture and the Chatbot are also here.

## State marks

Feedback components carry a state mark that is the logo's construction with the state in the badge instead of "AI": the toolbox never changes (the night `logo-box` with its `>_`), the corner badge takes the state role and a symbol — ✓ success, i info, ! warning, ✕ error. Logo, loader and states share one grammar. The same mark is dressed by size: **alone** on a surface at 24–40 px (snackbars, popin headers, inline alerts); **in a circle** at 56–96 px (empty states, table-, panel- or popin-level errors: disc in the state role, dark on light and light on dark, toolbox reversed, badge in the state container); as a **tile glyph** at 18–20 px (chips, table cells, dropdown options: the `>` and the reply on a tile, since the badge does not survive that small). Loading is not a state: the slot shows the pen-orbit ring around the plain mark and, when the request resolves, takes the state in place — warning after a timeout, error with Retry on failure. Info is the one status that uses `primary`. No entrance animation. Full table in `assets/States`.

## Motion

Material emphasized easing `cubic-bezier(0.2, 0, 0, 1)` for state changes; standard durations 150 / 300 / 500 ms. The brand loader is "Constructor" — the AI builds the toolbox: the AI tag is introduced first — its tile grows, "A" then "I" rise into it, a sheen crosses it — then dashed construction guides appear, a teal pen leaves the tag, draws the toolbox in one trip and goes home, and the toolbox becomes solid while the tag pulses once (4.8 s loop with a clean cut, or play once for a splash). Nothing is ever clipped: the badge, guides and pen all sit inside the loader's frame. The in-screen indicators belong to the same family — the circular indicator is a violet arc led by the teal pen (pen orbit), the linear track is a dashed construction guide the bar runs along (guide line), a known-value operation is the pen drawing the box until it fills (Constructor determinate), and the working dots are green when a command runs and teal when a model thinks. Material roles and sizes are unchanged; these are skins for `mat-progress-spinner` and `mat-progress-bar`. Where the static logo is shown instead of the loader, the same AI-tag intro plays on the finished mark (`mark-tag-in`): the plain toolbox, its corner carved, the tile growing in, "A" then "I", the sheen — once (1.4 s) ending on the full mark, or loop (4 s) folding back to the plain mark. Under `prefers-reduced-motion` everything stops on its rest frame — loaders, spinners, the pen orbit, working dots and the streaming caret — and the words beside them carry the state.

## Status and logs

Health chips are `*-container` fills with `on-*-container` text and a solid dot; log levels colour only the level word (`success` INFO, `warning` WARN, `error` ERR), Open Sans 600. The brand colours never appear in a status column.

## Accessibility

Target: WCAG 2.2 AA for every component and screen. The rules that make it hold:

- **Focus.** A 2 px `primary` ring with a 2 px gap on every interactive element (12.7:1 light, 10.9:1 dark; the gap keeps it on the page colour, even around the lime Run button). Text fields, selects and text areas take no ring: their border turns 2 px `primary` (2 px `error` while invalid). Focus adds no state layer, so a mouse click leaves nothing behind; the ring appears on keyboard focus only (`:focus-visible`). Angular: `mat.strong-focus-indicators` in both theme files; your own markup: the `:focus-visible` rule in `css/tokens.css`.
- **Never colour alone.** Status is a glyph and a word (✓ healthy, ! degraded, ✕ down); deltas carry an arrow and a word ("18 s faster"). The active navigation item adds a 3 px `primary` leading bar to its pill (top bar on the bottom NavigationBar).
- **Keyboard.** Menus follow the ARIA menu pattern (arrows, Home/End, Esc back to the trigger); tabs have one Tab stop and arrow keys; popovers and dialogs take focus and give it back; Esc closes the top layer only. Hidden layers (closed snackbar, popover, panel) use `visibility: hidden`, never transparency alone.
- **Screen readers.** Tooltips stay open while hovered and are the anchor's `aria-describedby`; a disabled reason is also a hidden description. Form errors set `aria-invalid`, are announced (`role="alert"`) and move focus to the first error. Streaming answers are `aria-busy`, then one "Answer ready". Accessible names start with the visible text. Status glyphs are `aria-hidden`.
- **Size and reflow.** Nothing below 11 px, uppercase labels 12 px or more; targets at least 24 × 24 px; at 320 CSS px (200 % zoom) navigation stays as a bottom NavigationBar and the avatar stays in the header.
- **Structure.** Headings never skip a level; overlays render inside a landmark.
- **What's new.** Each release is a ReleaseItem in layout D · Changelog: one table row per change, one action line ending with Questions and Useful?. See `components/ReleaseItem/`.
- **Ideas.** Layout E · stack + detail (320 px list, the idea beside it; the idea takes the page below 1200 px). An idea has Questions only, no separate discussion.
- **Discussion.** Releases and Ideas end with the same Discussion expansion panel, collapsed by default. Its header is the summary bar (threads, messages, participants, "Platform team replied", last message, Show / Hide). Open, it shows threads three at a time with Show more; each thread is an opening message and its replies (one level, the last two shown), with role chips for the platform team, champions and authors, and Reply. See `components/Discussion/`.
- **Administration.** One page with a 240 px sidebar (adopted in the Administration layout lab): Core (General first, then Users and permissions, Groups, Audit log), then one group per feature module, today Sweep (Connectors only) and Community, each with its sections. Accounts come from the company directory (SSO): Users and permissions has no invitation and only gives admin rights. Community · Insights brings together feedback forms, surveys and tours; OpenSearch usage metrics will be designed later. Rights remove groups and items; below 1200 px the sidebar becomes a Section select. Feature sections open with the Remote module line and the module's actions. The top app bar search field is 440 px wide.
- **Catalog.** A rail destination where people publish skills and use skills, tools (Deploy environment, Reserve environment, Create Jira ticket) and MCP servers (DevOps, Knowledge base) in the assistant and in Sweep runs. Minimal: tabs Browse and Mine, a kind switch and a search, cards with a name, one line and the author. Skills follow a five-step publication process: Write · Test · Submit · Review (for everyone only) · Published. See `components/CatalogItem/`.
- **Feedback.** All feedback administration is in Community › Feedback, for admins only: Profiles (every feature's form, edited with the FeedbackProfile editor), Inbox, Surveys and the shared solicitation policy. A feature admin gets the scoped right Feedback · <feature> and sees only their profile, their inbox and the cap (read-only). See `components/FeedbackProfile/`.
- **Guided tours.** The spotlight (scrim with a cutout) is the one way a tour points at an element; targets are `data-anchor` ids measured at runtime, the step card is a dialog that names the target in words, Esc skips. See `components/GuidedTour`.

`component-rules.md` lists the keyboard and screen-reader rules per component; the before/after board on the canvas Prototypes page shows each of these rules against the previous behaviour.

## Writing

Short, specific, active. Buttons say what happens ("Create workspace", "Run pipeline"). Errors say what went wrong and how to fix it. Technical identifiers are shown verbatim, Open Sans 600.

## Angular Material

The product is built on Angular Material. `angular-material.md` is the engineering companion: the version timeline (M2 theming on 21 today, `mat.theme` on 22), `angular/theme.m2.scss` and `angular/theme.m3.scss` generated from these tokens, `angular/mat-sys-bridge.css`, the role-to-slot mapping, and every Angular Material component mapped to its AIToolbox component with M2 and M3 notes. `component-rules.md` lists every component's design rules with the Angular Material tokens (same names under M2 and M3) and their AIToolbox values. Each component README ends with its Angular Material line.
