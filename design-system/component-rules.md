# Component rules & tokens · Angular Material 21 (M2) and 22 (M3)

Every AIToolbox component with its design rules and the Angular Material tokens that implement them, for the two theming generations the product runs: **Material 2 theming on Angular Material 21** (`angular/theme.m2.scss`) and **Material 3 on Angular Material 22** (`angular/_theme-colors.scss` + `angular/theme.m3.scss`). Both files compile on 21.2 and 22.2 without a warning; the hex values are identical by construction.

## How to read this

- **One token vocabulary.** Since v20 every component exposes its styling as `--mat-<component>-<token>` custom properties, and since v19 each component has a `mat.<component>-overrides((token: value))` mixin that writes them. The names are the same under M2 and M3 — only the *defaults* differ: an M2 theme fills them from the `primary` / `accent` / `warn` palettes, `mat.theme` fills them from the `--mat-sys-*` system variables. The token names below are taken from the 22.1 sources; they are the ones you pass to the overrides mixins (without the component prefix).
- **M2 on v21.** The `mat.m2-*` APIs (`m2-define-palette`, `m2-define-light-theme`, `m2-define-typography-config`) are still shipped in 22.2 and compile without deprecation output, so the M2 file is not on a cliff — but the old `--mdc-*` variable names are gone since v20: anything you wrote against `--mdc-filled-button-container-shape` and friends is dead on 21 and must become `mat.button-overrides(...)`. `theme.m2.scss` does that now.
- **M3 on v22.** `mat.theme` + `mat.theme-overrides` pin the roles to the AIToolbox hex (Angular would otherwise put the light primary at tone 40 and use its own surface steps). v21 renamed the `utility-classes` mixin to `system-classes` and the `extra-small` corner to `xs`; v22 added typography mixins. Nothing in 21 or 22 changed the component tokens used here.
- **Values** are written light / dark. Extended colours (`ai`, `success`, `warning`) have no Angular slot in either generation: they are the `--md-sys-color-*` custom properties from `css/tokens.css`, used through the `.dt-*` classes.
- **"DS rule"** lines are the design-system rules the Angular component must respect; the component READMEs are the source.

## Foundations: AIToolbox token → M2 slot → M3 variable

| AIToolbox | Value (light / dark) | M2 · v21 | M3 · v22 |
|---|---|---|---|
| `primary` / `on-primary` | #39235F / #C4C0FF · on: #FFFFFF / #2A2473 | `primary` palette hue 800 (the Sweep purple #39235F, tone 20, light) · 200 (dark); `color="primary"` | `--mat-sys-primary` / `--mat-sys-on-primary` (pinned by `theme-overrides`) |
| `primary-container` / `on-primary-container` | #E3DFFF / #413C8A · on: #14085E / #E3DFFF | `primary` palette `lighter` (hue 100) | `--mat-sys-primary-container` / `--mat-sys-on-primary-container` |
| `secondary` (from the Sweep pale purple) | #484454 / #CAC3D7 | `accent` palette 700 / 200 (`$dt-mauve`); `color="accent"` for the text/icon role only | `--mat-sys-secondary` |
| `secondary-container` / `on-secondary-container` (the Sweep pale purple) | #DED7EB / #484454 · on: #1D1A28 / #E6DFF3 | `accent` `lighter` (hue 100 = #DED7EB) | `--mat-sys-secondary-container` / `--mat-sys-on-secondary-container` |
| `tertiary` / `on-tertiary` (lime palette: running dots, deploy states — never a fill) | #404B23 / #BFCC99 · on: #FFFFFF / #2A340F | `$dt-lime` palette, hue 700 light / A200 dark | `--mat-sys-tertiary` / `--mat-sys-on-tertiary` |
| `tertiary-container` / `on-tertiary-container` (the Run action: the Sweep lime, pinned in both themes) | #DCEAB4 / #DCEAB4 · on: #39235F / #39235F | `.dt-run` (`mat.button-overrides` / `mat.fab-overrides`, hex); `$dt-lime` `lighter` (time picker AM/PM) | `--mat-sys-tertiary-container` / `--mat-sys-on-tertiary-container`; `.dt-run` via `mat.button-overrides` |
| `error` / `on-error` / `error-container` / `on-error-container` | #93000A / #FFB4AB · on: #FFFFFF / #690005 / #FFDAD6 / #93000A · on: #410002 / #FFDAD6 | `warn` palette 700 (tone 30) / 200; `color="warn"` | `--mat-sys-error`, `--mat-sys-on-error`, `--mat-sys-error-container`, `--mat-sys-on-error-container` |
| `ai` / `on-ai` (Material tones: deep teal in light, light teal in dark) | #004F50 / #80D5D4 · on: #FFFFFF / #003737 | no slot → `.dt-ai` scoped theme (teal hue 700 light / 200 dark) | `--md-sys-color-ai` / `--md-sys-color-on-ai` + `.dt-ai` overrides |
| `ai-container` / `on-ai-container` | #9CF1F0 / #004F50 · on: #002020 / #9CF1F0 | same | `--md-sys-color-ai-container` / `--md-sys-color-on-ai-container` |
| `success`, `warning` families | #0B5314 / #91D888 · #5C4300 / #FCBC00 (+ containers) | no slot → `.dt-chip-*` classes, own banners | same custom properties, same classes |
| `logo-box` / `on-logo-box` / `logo-cursor` / `logo-ai` / `on-logo-ai` (brand group, logo family only) | #0D0B14 / #C4C0FF · on: #FFFFFF / #0D0B14 · cursor: #00F29E / #006C44 · AI badge: #80D5D4 / #80D5D4 · on: #003737 | no slot → `--md-sys-color-logo-*` custom properties (inline SVG) | same custom properties; never on a UI surface |
| `surface` | #FDF8FD / #14121E | `background.background` | `--mat-sys-surface` |
| `nav-container` (navigation only) | #EDE4FF / #1D1A27 | no slot → `.dt-nav` class on `mat-sidenav` / bottom `mat-toolbar` | `--md-sys-color-nav-container` via `.dt-nav` |
| `surface-container-lowest … highest` | #FFFFFF…#ECE5F4 / #0F0C19…#363341 | M2 knows four steps only: `card` = lowest (light) / low (dark), `dialog` = high, `app-bar` = container | `--mat-sys-surface-container-lowest` … `-highest` |
| `on-surface` / `on-surface-variant` | #1C1B1E / #ECE5F8 · on: #48454E / #CAC3DC | `foreground.text` / `foreground.secondary-text` | `--mat-sys-on-surface` / `--mat-sys-on-surface-variant` |
| `outline` / `outline-variant` | #79757F / #948DA5 · on: #CAC4CF / #494458 | — / `foreground.divider` | `--mat-sys-outline` / `--mat-sys-outline-variant` |
| `inverse-surface` / `inverse-on-surface` / `inverse-primary` | #313033 / #E6DFF2 · on: #F4EFF4 / #322E3C · action: #C4C0FF / #413C8A | `mat.snack-bar-overrides` (M2 hard-codes a dark snackbar) | `--mat-sys-inverse-surface`, `--mat-sys-inverse-on-surface`, `--mat-sys-inverse-primary` |
| Type: display / headline / title / label (BNPP Type 500) | tokens.json type scale | `m2-define-typography-config` levels `headline-1…6`, `subtitle-1/2`, `button` | `brand-family` of `mat.theme` → `--mat-sys-display-*`, `-headline-*`, `-title-*`, `-label-*` |
| Type: body, code (Open Sans 400 / 600) | body-large 16/24 · medium 14/20 · small 12/16; code 13/20 at 600 | `body-1`, `body-2`, `caption`; code = custom class | `plain-family` → `--mat-sys-body-*`; code = custom class |
| Shape: `radius-xs/sm/md/lg/xl/full` | 4 / 8 / 12 / 16 / 16 / 9999 px — Large (16) is the ceiling; `xl` is pinned to it and `full` is for circles only (icon buttons, avatars, badges, radio, switch) | `*-overrides` shape tokens (same as M3) | `--mat-sys-corner-extra-small` (4), `-small` (8), `-medium` (12), `-large` (16), `-extra-large` (16), `-full` (circles); per-component shape tokens pinned |
| Elevation 1–5 | tokens.json shadows | `mat.core()` elevation classes | `--mat-sys-level1` … `--mat-sys-level5` |
| State layers (hover, focus, pressed, dragged) | **Neutral surfaces: `primary` at 6 % / 0 % / 10 % / 14 %** (light #39235F, dark #C4C0FF) — e.g. white → #F3F2F5, `nav-container` → #E2D8F5; coloured components (filled, tonal, Run, AI, selected chips, active navigation) use their own content colour (`on-primary`, `on-secondary-container`, `on-tertiary`, `on-ai-container`) at the same opacities. Never the grey `on-surface` layer. Focus adds no layer, so nothing stays tinted after a mouse click; keyboard focus shows only the focus ring. | per-component `state-layer-color` / `hover-state-layer-color` overrides + table rows in CSS (set in `theme.m2.scss`) | `--mat-sys-hover-state-layer-opacity: .06`, `--mat-sys-pressed-state-layer-opacity: .1`, `--mat-sys-focus-state-layer-opacity: 0` + the same overrides (set in `theme.m3.scss`) |

| Focus (keyboard) | 2 px `primary` ring with a 2 px gap outside buttons, chips, icon buttons, list and menu items, tabs, navigation items (12.7:1 / 10.9:1). Text fields, selects and text areas take no ring: their outline turns 2 px `primary` (`error` while invalid). Focus adds no state layer, so a mouse click leaves nothing behind; the ring shows on keyboard focus only. | `mat.strong-focus-indicators` (set in `theme.m2.scss`) | `mat.strong-focus-indicators` (set in `theme.m3.scss`) |

Dark mode: M2 file = `html.dark` block (`mat.all-component-colors($dt-dark)`); M3 file = `color-scheme: light dark` with `light-dark()` values, or the `html.light` / `html.dark` classes.

---

## Accessibility rules for every component (WCAG 2.2 AA)

- **Focus visible.** Every interactive element shows the 2 px `primary` ring on `:focus-visible` (Angular: strong focus indicators; own markup: the rule in `css/tokens.css`). Inside clipping containers (tab bars, segmented buttons) the ring is drawn inside (`outline-offset: -3px`). Fields use their 2 px `primary` outline instead.
- **Never colour alone.** Status = glyph + word; deltas = arrow + word; the active navigation item = pill + 3 px `primary` bar.
- **Keyboard.** Everything reachable with Tab; composite widgets (menus, tabs, radio groups, segmented buttons, lists) use arrow keys with one Tab stop; Esc closes the top layer only and focus returns to the control that opened it. Focus never falls to the page after an action.
- **Hidden means unreachable.** Closed snackbars, popovers, panels and menus are `visibility: hidden` (or removed), never transparent but focusable.
- **Names and descriptions.** Icon-only controls have an `aria-label` that starts with the visible tooltip text; tooltips are `aria-describedby` and stay open while hovered; disabled controls keep a hidden description of why; decorative glyphs and icons are `aria-hidden`.
- **Announcements.** Results of an action that the user cannot see (a save in a closed panel, an answer ready, a form error) are announced once through a live region outside the hidden area.
- **Size.** Text ≥ 11 px (uppercase ≥ 12 px); targets ≥ 24 × 24 px; at 320 CSS px nothing is lost and nothing overprints.
- **Motion.** Under `prefers-reduced-motion` spinners, carets, dots and loaders stop on a rest frame; the label carries the state.

---

## Responsive layout (window size classes)

Material 3 window size classes; a breakpoint is the lower bound of a class (a 600 px window is Medium). Mobile-first `min-width` queries on the window width. The shell (navigation, header, assistant, overlays) follows the **window**; the page content follows the **page area** (`.ait-page` size container), because the drawer and the docked assistant take part of the window.

| Class | Window width | Page margin · columns · gutter | Angular query (`AitWindow`) |
|---|---|---|---|
| **Compact** | 0–599 px | 16 px · 4 · 16 px | `AitWindow.Compact` |
| **Medium** | 600–839 px | 24 px · 8 · 24 px | `AitWindow.Medium` |
| **Expanded** | 840–1199 px | 24 px · 12 · 24 px | `AitWindow.Expanded` |
| **Large** | 1200–1599 px | 32 px · 12 · 24 px | `AitWindow.Large` |
| **Extra-large** | ≥ 1600 px | 32 px · 12 · 24 px | `AitWindow.ExtraLarge` |

| Shell | Compact | Medium | Expanded | Large | Extra-large |
|---|---|---|---|---|---|
| Navigation | NavigationBar at the bottom (80 px, 3–5 destinations, Assistant one of them); the rest in a modal drawer from the top-bar menu | NavigationRail (80 px); its menu button opens the drawer over the page (modal, scrim) | NavigationRail (80 px); its menu button opens the drawer over the page (modal, scrim) | NavigationRail (80 px) by default; its menu button opens the standard drawer on demand (300 px, pushes the page) | Same as Large: rail by default, standard drawer on demand |
| Top app bar | 56 px · menu · logo mark · search icon · bell · avatar; help in the user menu | 64 px · logo · search field 240–600 px, Ask chip as an icon · assistant · bell · avatar; help in the user menu | 64 px · logo · search field 320–600 px, Ask chip as an icon · assistant · bell · help · avatar | 64 px · logo · search field 600 px with the labelled Ask chip · assistant · bell · help · user chip with name and role | same as Large |
| Assistant | Full-screen view, the NavigationBar destination | Takes the page area in place, beside the rail; the header button gives the page back | Takes the page area in place, beside the rail; the header button gives the page back | Docked split view, 400 px (320 – min(640 px, 50 %)), beside the rail; an open drawer folds back to the rail when the page would drop under 720 px (windows under about 1480 px) | Docked split view beside the rail; an open drawer stays while the page keeps ≥ 720 px |
| Page actions | The primary action becomes an extended FAB 16 px above the NavigationBar (shrinks to the icon on scroll); the others go to the ⋮ menu; Run stays in the selection bar | Primary button kept; secondary actions as icon buttons with tooltips | All buttons with labels; Filter as an icon button | All buttons with labels | All buttons with labels |
| Dialogs | Forms: full-screen dialog (close · title · Save in a top bar); confirmations stay basic dialogs, 16 px from the edges | Basic dialog 280–560 px | Basic dialog 280–560 px | Basic dialog 280–560 px | Basic dialog 280–560 px |
| Sheets | BottomSheet (a SideSheet becomes one) | Modal SideSheet (over, scrim) | Modal SideSheet (over, scrim) | Standard SideSheet (pushes the page) or modal | Standard SideSheet or modal |
| Snackbar | Full width minus 2 × 16 px, 16 px above the NavigationBar | 344–600 px, bottom of the page area at the page margin | 344–600 px, bottom of the page area at the page margin | 344–600 px, bottom of the page area at the page margin | same as Large |
| Page margin · grid | 16 px · 4 columns · 16 px gutters | 24 px · 8 columns · 24 px gutters | 24 px · 12 columns · 24 px gutters | 32 px · 12 columns · 24 px gutters | 32 px · 12 columns · 24 px gutters |

Page content (container queries on `.ait-page`):

- **KPI cards.** 1 per row under 300 px · 2 per row from 300 px (a 360 px phone) · 4 per row from 720 px of page area.
- **Side column (AI suggestion, alerts, deploy window).** Beside the table, 360 px (400 px from 1440 px), when the page area is ≥ 1040 px; otherwise stacked full width: alerts above the table, the other cards under it.
- **Data tables.** Under 600 px the rows become a two-line list (state mark + name, a meta line, actions in the row menu); 600–799 px only priority-1 and -2 columns + the row menu; from 800 px every column. A table that must keep every column scrolls inside its own frame with the first column sticky — the page itself never scrolls sideways.
- **Forms.** One column, 600 px max; pairs (start / end date) side by side from 600 px of page area; actions at the end, full width under 600 px.
- **Tabs.** Scrollable under 600 px of page area (counts kept), never wrapped.
- **Reading pages (docs, settings, policies).** Text column 840 px max, centred in the page area; dashboards and tables use the full width.

Height under 480 px (phone in landscape): rail instead of the NavigationBar, top app bar scrolls away, forms in dialogs full screen. Targets 48 px under `(pointer: coarse)` at every width.

**Angular:** `angular/breakpoints.ts` — `AitWindow` media queries for `BreakpointObserver` (never the CDK `Breakpoints` constants: 600 / 960 / 1280 / 1920 are not the Material 3 classes) and the `AitWindowClass` service with signals `windowClass`, `navigation` (`bar` | `rail` | `drawer`; `drawer` only after `openDrawer()` from 1200 px — the rail is the default), `drawerOpen` / `openDrawer()` / `closeDrawer()`, `drawerMode` (`over` | `side` for `mat-sidenav`), `assistantMode` (`full-screen` | `in-place` | `docked`), `fullScreenDialogs`. Sass: `@use 'breakpoints' as bp;` → `bp.from(expanded)`, `bp.below(large)`, `bp.only(medium)`, `bp.short`, `bp.page-from(720px)`. CSS: `--ait-page-margin`, `--ait-grid-columns`, `--ait-grid-gutter`, `.ait-page`, `.ait-grid`, `.ait-kpis`, `.ait-split`, `.ait-col-p2` / `-p3`, `.ait-reading`, `.ait-form` in `css/tokens.css`.

**Test** at 320 (WCAG reflow, 1280 px at 400 % zoom), 360, 600, 768, 840, 1024, 1200, 1440, 1600, 1920 px, and 740 × 360 (phone in landscape). At 320 px the page never scrolls sideways (WCAG 1.4.10); only a data table or code block scrolls, inside its own frame.

---

## Components


### Badge

**Angular Material:** `matBadge`

- Small = 6 px dot, no text; large = 16 px high, label-small, min-width 16 px, "999+" past three digits.
- Always `error` on `on-error`: a badge is an alert, never a brand colour. Top-right of the icon; in a navigation item on the icon, not the label.

`mat.badge-overrides((…))` sets these in **both** files; the CSS variable is `--mat-badge-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `background-color` | #93000A / #FFB4AB | `matBadgeColor="warn"` (default `primary` → set warn) | `--mat-sys-error` by default |
| `text-color` | #FFFFFF / #690005 | from the `warn` palette contrast | `--mat-sys-on-error` |
| `small-size-container-size` | 6px | v21 default 6px | same |
| `container-size` | 16px | `matBadgeSize="medium"` (16px) | same |
| `text-size` | 11px (label-small) | typography level `caption` | `--mat-sys-label-small-size` |


### BottomAppBar

**Angular Material:** `mat-toolbar` at the bottom (no dedicated component) + `mat-fab`

- Phone-only, 80 px, on `nav-container` like the drawer (violet tint in light); up to four icon buttons left, a FAB (no shadow here) right.
- Detail screens where the primary action and a few tools belong at the thumb; never together with a NavigationBar.

`mat.toolbar-overrides((…))` sets these in **both** files; the CSS variable is `--mat-toolbar-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-background-color` | #EDE4FF / #1D1A27 (`nav-container`) | `.dt-nav` class on the bottom `mat-toolbar` (set in `theme.m2.scss`) | `.dt-nav` → `var(--md-sys-color-nav-container)` (set in `theme.m3.scss`) |
| `container-text-color` | #1C1B1E / #ECE5F8 | `foreground.text` | `--mat-sys-on-surface` |
| `standard-height` | 80px for this bar (64px for the TopAppBar) | density 0 → 64px; set 80px on the bar | same |

FAB inside the bar: `mat.fab-overrides((container-elevation-shadow: none))` scoped to the bar.

### BottomSheet

**Angular Material:** `MatBottomSheet`

- `surface-container-low`, radius-lg (16 px) top corners, 32×4 px drag handle in `outline`.
- Modal (scrim) for a short list of actions on one item; standard (no scrim) for persistent content. Tablet/desktop → SideSheet or Dialog.
- **Responsive:** Compact only (under 600 px). From 600 px the same content is a SideSheet, a Menu or a Dialog.
- **Keyboard and screen reader:** modal sheets move focus in and back, Esc closes; the drag handle is also a button.

`mat.bottom-sheet-overrides((…))` sets these in **both** files; the CSS variable is `--mat-bottom-sheet-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-background-color` | #FAF4FF / #1D1A27 | `background.dialog` (surface-container-high) → override to low | `--mat-sys-surface-container-low` (Angular default) |
| `container-text-color` | #1C1B1E / #ECE5F8 | `foreground.text` | `--mat-sys-on-surface` |
| `container-shape` | 16px 16px 0 0 | `mat.bottom-sheet-overrides` | `--mat-sys-corner-large` top (override, default 28) |


### Button

**Angular Material:** `mat-button` (text), `mat-flat-button` (filled; tonal with the `tonal` appearance / `mat-tonal-button` in 21+), `mat-stroked-button` (outlined), `mat-raised-button` (elevated = "protected")

- 40 px, radius-lg (16 px — never full-round), label-large; horizontal padding 24 px (16 px with a leading icon). Icon-only buttons stay 40 px circles with an `aria-label`.
- Filled `primary` = the one decision on a screen; tonal `secondary-container` beside it; elevated on tinted grounds (elevation-1); outlined / text = low emphasis, text is the dialog dismiss.
- Run `.dt-run` = the tertiary container (the Sweep lime, `tertiary-container` fill, `on-tertiary-container` label and play icon, no edge): the single action that starts work, leading play icon, at most one per screen, never in a dialog. Row run actions `.dt-run-text`: text button in `primary`, play icon in a 22 px `tertiary-container` disc with an `on-tertiary-container` glyph, never filled.
- Destructive = text button in `error`, never a filled red. Disabled = on-surface 12 % fill / 38 % text.
- **Keyboard and screen reader:** focus ring outside the button (2 px gap); Enter and Space activate; icon + label buttons need no extra name; a disabled button that must explain itself is `aria-disabled` (stays focusable) with a hidden description.

`mat.button-overrides((…))` sets these in **both** files; the CSS variable is `--mat-button-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `filled-container-color` | #39235F / #C4C0FF | `primary` palette default hue | `--mat-sys-primary` |
| `filled-label-text-color` | #FFFFFF / #2A2473 | palette contrast | `--mat-sys-on-primary` |
| `tonal-container-color` | #DED7EB / #484454 | `accent` lighter (M2 tonal = `mat-flat-button color="accent"` on the lighter hue, or the tonal appearance on 21) | `--mat-sys-secondary-container` |
| `tonal-label-text-color` | #1D1A28 / #E6DFF3 | contrast of the lighter hue | `--mat-sys-on-secondary-container` |
| `protected-container-color` | #FFFFFF / #0F0C19 | `background.card` | `--mat-sys-surface` by default → surface-container-lowest |
| `outlined-outline-color` | #79757F / #948DA5 | `foreground.divider` → set `outline` | `--mat-sys-outline` |
| `text-label-text-color` | #39235F / #C4C0FF | `primary` | `--mat-sys-primary` |
| `filled-container-shape` | 16px (`radius-lg`) | `mat.button-overrides` (also outlined / text / protected / tonal shapes) | `mat.button-overrides` (default is `--mat-sys-corner-full`) |
| `filled-container-height` | 40px | density 0 → 40px | 40px |
| `filled-horizontal-padding` | 24px | default 24px (v21: 24px; text buttons 12px) | default 24px |
| `filled-label-text-size` | 14px (label-large) | typography level `button` | `--mat-sys-label-large-size` |

`.dt-run`: `filled-container-color: tertiary-container`, `filled-label-text-color: on-tertiary-container`, `filled-state-layer-color: on-tertiary-container`, icon `on-tertiary-container`, no edge (both files; hex in M2, `--mat-sys-tertiary-container` in M3) · `.dt-run-text`: default `primary` text button, icon in a 22 px `tertiary-container` disc, glyph `on-tertiary-container`. Destructive text button: `text-label-text-color: error` on a `.dt-danger` class in both.

### Card

**Angular Material:** `mat-card` with `appearance="raised"` (elevated), `"filled"`, `"outlined"` (21+: all three appearances exist)

- radius-md (12 px), 16 px padding, title-medium heading.
- Elevated = `surface-container-lowest` + elevation-1 (the default for a service or tool card with actions); filled = `surface-container-high`, no shadow (dense lists, grids); outlined = `surface` + `outline-variant` border.
- Actions in a bottom flex row: text buttons left, one filled right. Status in a card header is a StatusChip, never a coloured title.
- **Responsive:** KPI cards: 4 per row from 720 px of page area, 2 from 300 px (a 360 px phone), 1 below.

`mat.card-overrides((…))` sets these in **both** files; the CSS variable is `--mat-card-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `elevated-container-color` | #FFFFFF / #0F0C19 | `background.card` | `--mat-sys-surface-container-low` by default → override to lowest |
| `filled-container-color` | #F2EBFA / #2B2836 | override (M2 has no filled default) | `--mat-sys-surface-container-highest` by default → override to high |
| `outlined-container-color` | #FDF8FD / #14121E | `background.card` → override to surface | `--mat-sys-surface` |
| `outlined-outline-color` | #CAC4CF / #494458 | `foreground.divider` | `--mat-sys-outline-variant` |
| `elevated-container-shape` | 12px (`radius-md`) | override (also filled / outlined) | `--mat-sys-corner-medium` |
| `elevated-container-elevation` | elevation-1 | level 1 | `--mat-sys-level1` |
| `title-text-size` | 16px (title-medium) | `subtitle-1` | `--mat-sys-title-medium-size` |


### Carousel

**Angular Material:** no Angular Material component — CDK scrolling (`cdk-virtual-scroll` / `cdkScrollable`) with the AIToolbox markup

- Multi-browse layout: one large item, one medium, small items at the edge, 8 px gaps, radius-lg (16 px).
- Items are `*-container` tones or images; title bottom-left in title-medium. For equal items use List or a grid of Cards.

Tokens: none of Angular's; use `--md-sys-color-*-container`, `--md-sys-shape-corner-large` from `css/tokens.css`.

### Checkbox

**Angular Material:** `mat-checkbox`

- 18 px box, radius 2 px, inside a 44–48 px touch target, 12 px gap to the label.
- Unchecked: 2 px `on-surface-variant` border; checked / indeterminate: `primary` fill with an `on-primary` mark; error: `error` fill; disabled: on-surface 38 %.
- Independent options and multi-select lists; a single on/off setting is a Switch.

`mat.checkbox-overrides((…))` sets these in **both** files; the CSS variable is `--mat-checkbox-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `selected-icon-color` | #39235F / #C4C0FF | `color="primary"` (set as default) | `--mat-sys-primary` |
| `selected-checkmark-color` | #FFFFFF / #2A2473 | palette contrast | `--mat-sys-on-primary` |
| `unselected-icon-color` | #48454E / #CAC3DC | `foreground.secondary-text` | `--mat-sys-on-surface-variant` |
| `label-text-color` | #1C1B1E / #ECE5F8 | `foreground.text` | `--mat-sys-on-surface` |
| `touch-target-size` | 48px | default | default |

Error state: `mat-checkbox` has no error appearance — add `.dt-error { @include mat.checkbox-overrides((selected-icon-color: error, unselected-icon-color: error)); }`.

### Chip

**Angular Material:** `mat-chip-set` / `mat-chip-option` (filter), `mat-chip-row` (input), `mat-chip` (assist / suggestion)

- 32 px, radius-sm (8 px), label-large at 500; wrapping row with 8 px gaps.
- Assist / filter unselected: outlined `outline`, text on-surface. Filter selected: `secondary-container` fill with a leading check. Input: outlined with a trailing close, for applied filters and tags like `env:prod`.
- AI chip `.dt-ai`: `ai-container` fill with the sparkle icon — only AI features. Health status is not a chip: see StatusChip.
- **Keyboard and screen reader:** filter chips are toggle buttons (`aria-pressed`); a chip set has one Tab stop with arrow keys; the remove icon is a 24 × 24 px target named "Remove <label>".

`mat.chips-overrides((…))` sets these in **both** files; the CSS variable is `--mat-chip-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-height` | 32px | default 32px | default |
| `container-shape-radius` | 8px (`radius-sm`) | `mat.chips-overrides` | `--mat-sys-corner-small` |
| `outline-color` | #79757F / #948DA5 | `foreground.divider` → set `outline` | `--mat-sys-outline` |
| `label-text-color` | #1C1B1E / #ECE5F8 | `foreground.text` | `--mat-sys-on-surface-variant` by default → override to on-surface |
| `elevated-selected-container-color` | #DED7EB / #484454 | `accent` lighter (selected `mat-chip-option` uses the `accent` palette with `color="accent"`) | `--mat-sys-secondary-container` |
| `selected-label-text-color` | #1D1A28 / #E6DFF3 | contrast | `--mat-sys-on-secondary-container` |
| `with-avatar-avatar-size` | 18px (tile glyph of StateMark C in status chips) | default 24px → 18px | same |
| `label-text-size` | 14px (label-large) | `button` level | `--mat-sys-label-large-size` |

`.dt-ai`: `elevated-container-color: ai-container`, `label-text-color: on-ai-container`. Health chips (StatusChip) use `.dt-chip-success | warning | error | info` with `elevated-container-color` / `label-text-color` on the state containers — the same mixin in both files.

### DatePicker

**Angular Material:** `mat-datepicker` (+ `mat-date-range-picker`)

- Modal picker 328 px, radius-lg (16 px), `surface-container-high`, elevation-3. Header: label-medium supporting text, selected date in headline-large, edit icon to switch to input.
- 40 px day cells; today outlined in `primary`, selection filled `primary`; text buttons Cancel / OK. Ranges: full-screen range picker; dense forms: docked picker. Week starts Monday, ISO dates in the field.

`mat.datepicker-overrides((…))` sets these in **both** files; the CSS variable is `--mat-datepicker-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `calendar-container-background-color` | #F2EBFA / #2B2836 | `background.card` → override | `--mat-sys-surface-container-high` |
| `calendar-container-shape` | 16px (`radius-lg`) | `mat.datepicker-overrides` | `--mat-sys-corner-large` (default; pinned) |
| `calendar-date-selected-state-background-color` | #39235F / #C4C0FF | `primary` | `--mat-sys-primary` |
| `calendar-date-selected-state-text-color` | #FFFFFF / #2A2473 | contrast | `--mat-sys-on-primary` |
| `calendar-date-today-outline-color` | #39235F / #C4C0FF | `primary` | `--mat-sys-primary` |
| `calendar-date-in-range-state-background-color` | #E3DFFF / #413C8A | `primary` lighter | `--mat-sys-primary-container` |
| `toggle-active-state-icon-color` | #39235F / #C4C0FF | `primary` | `--mat-sys-primary` |


### Dialog

**Angular Material:** `MatDialog` (`mat-dialog-title`, `mat-dialog-content`, `mat-dialog-actions`)

- 280–560 px, radius-lg (16 px), `surface-container-high`, elevation-3, 24 px padding, scrim at 32 %.
- Title headline-small; one line of body-medium supporting text on `on-surface-variant`. Fields: TextField with the label background on the dialog colour; 24 px between rows.
- Actions right-aligned: text dismiss + one filled `primary` confirm. Never the Run button, never a filled destructive button (delete = text in `error`). Focus to the first field, Esc = Cancel; more than ~6 fields → full-screen or page.
- State-driven popin: 32 px StateMark A next to the title.
- **Responsive:** Under 600 px a form opens as a full-screen dialog (close · title · Save in a top bar); a confirmation stays a basic dialog 16 px from the edges. From 600 px: basic dialog 280–560 px.
- **Keyboard and screen reader:** focus moves to the first field (or the title when there is none), Tab cycles inside, Esc = Cancel and closes this dialog only, focus returns to the opener; the page behind is inert.

`mat.dialog-overrides((…))` sets these in **both** files; the CSS variable is `--mat-dialog-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-color` | #F2EBFA / #2B2836 | `background.dialog` (injected) | `--mat-sys-surface-container-high` (default) |
| `container-shape` | 16px | `mat.dialog-overrides` | `mat.dialog-overrides` (default is `--mat-sys-corner-extra-large`, 28) |
| `container-max-width` | 560px | default 560px | default |
| `container-min-width` | 280px | default 280px | default |
| `subhead-size` | 24px (headline-small) | `headline-6` | `--mat-sys-headline-small-size` |
| `supporting-text-color` | #48454E / #CAC3DC | `foreground.secondary-text` | `--mat-sys-on-surface-variant` |
| `content-padding` | 24px | default 20px 24px → 24px | default 20px 24px → 24px |

Scrim: `cdk-overlay-dark-backdrop` → `$overlay-backdrop-color` (v21 rename) = `scrim` at 32 %.

### Divider

**Angular Material:** `mat-divider` (`inset`, `vertical`)

- 1 px in `outline-variant`; full-width between sections, inset 16 px between list items with a leading element, vertical between side-by-side controls.
- Prefer spacing or a container change over a divider; use them where items would otherwise merge (dense lists, tables).

`mat.divider-overrides((…))` sets these in **both** files; the CSS variable is `--mat-divider-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `color` | #CAC4CF / #494458 | `foreground.divider` | `--mat-sys-outline-variant` |
| `width` | 1px | default | default |


### FAB

**Angular Material:** `mat-fab`, `mat-mini-fab`, `mat-fab extended`

- Small 40 px radius-md · default 56 px radius-lg · large 96 px radius-lg (16 px, the ceiling) · extended 56 px with a label.
- Fill `primary-container` with `on-primary-container` content, elevation-3; the small run FAB (`tertiary-container` lime fill, `on-tertiary-container` glyph) only as a "run" entry point.
- One per screen, bottom-right, 16 px from the edges; lowers to elevation-1 when a dialog opens.
- **Responsive:** Under 600 px the page primary action (New pipeline) becomes an extended FAB 16 px above the NavigationBar, shrinking to its icon on scroll. From 600 px the action stays a button in the page header: no FAB.

`mat.fab-overrides((…))` sets these in **both** files; the CSS variable is `--mat-fab-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-color` | #E3DFFF / #413C8A | `primary` lighter (M2 default is `primary` → set `color="primary"` + override) | `--mat-sys-primary-container` (default) |
| `foreground-color` | #14085E / #E3DFFF | contrast | `--mat-sys-on-primary-container` |
| `container-shape` | 16px (`radius-lg`) | override | `--mat-sys-corner-large` (default) |
| `small-container-color` | #DCEAB4 (run entry: `tertiary-container`, `on-tertiary-container` glyph) / primary-container otherwise | `.dt-run` via `mat.fab-overrides` | `.dt-run` via `mat.fab-overrides` |
| `small-container-shape` | 12px (`radius-md`) | override | `--mat-sys-corner-medium` (default) |
| `extended-container-height` | 56px | default | default |


### IconButton

**Angular Material:** `mat-icon-button` (standard); filled / tonal / outlined via `.dt-icon-filled | -tonal | -outlined` classes (Angular has one appearance)

- 40 px circle, 24 px icon; standard = no fill `on-surface-variant`, filled = `primary`, tonal = `secondary-container`, outlined = `outline` border.
- Toggle buttons use `aria-pressed`; the selected standard state takes `primary`. Always an `aria-label`; 48 px touch target (4 px margin in a dense row).
- **Keyboard and screen reader:** `aria-label` starting with its tooltip text; 40 px button, never a hit area under 24 × 24 px; toggles use `aria-pressed`.

`mat.icon-button-overrides((…))` sets these in **both** files; the CSS variable is `--mat-icon-button-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `icon-color` | #48454E / #CAC3DC | `foreground.icon` | `--mat-sys-on-surface-variant` |
| `icon-size` | 24px | default | default |
| `state-layer-size` | 40px | default 40px | default |
| `touch-target-size` | 48px | default | default |
| `container-shape` | 9999px | default full | `--mat-sys-corner-full` |

Filled / tonal / outlined variants are plain CSS on the class (`background: var(--md-sys-color-primary)` etc.) — Angular's icon button has no container-color token.

### List

**Angular Material:** `mat-list`, `mat-nav-list`, `mat-selection-list`, `mat-list-item` (`lines="1|2|3"`)

- Rows 56 / 72 / 88 px (one / two / three lines): leading avatar or icon, title-medium headline, body-medium supporting text in `on-surface-variant`, trailing meta or icon.
- Selected row `surface-container` (`secondary-container` in a navigation list). Inset dividers when rows have a leading element; 16 px row padding; the whole row is the hit target.
- **Responsive:** Under 600 px of page area, data tables become two-line lists: state mark + name, a meta line, actions in the row menu.
- **Keyboard and screen reader:** a selectable list has one Tab stop and arrow keys; row actions are reachable from the row; the focus ring is drawn inside the row.

`mat.list-overrides((…))` sets these in **both** files; the CSS variable is `--mat-list-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `list-item-label-text-color` | #1C1B1E / #ECE5F8 | `foreground.text` | `--mat-sys-on-surface` |
| `list-item-supporting-text-color` | #48454E / #CAC3DC | `foreground.secondary-text` | `--mat-sys-on-surface-variant` |
| `list-item-one-line-container-height` | 56px | default 48px → 56px | default 56px |
| `list-item-two-line-container-height` | 72px | default 64px → 72px | default 72px |
| `list-item-three-line-container-height` | 88px | default 88px | default |
| `active-indicator-color` | #DED7EB / #484454 | `accent` lighter (nav list active item via class) | `--mat-sys-secondary-container` |
| `active-indicator-shape` | 16px | `mat.list-overrides` | `mat.list-overrides` (default is `--mat-sys-corner-full`) |
| `list-item-selected-container-color` | #F8F1FF / #23202D | override | no default → surface-container |
| `list-item-leading-avatar-size` | 40px | default | default |


### Loader (brand)

**Angular Material:** no Angular Material component — inline SVG from `loading-states/` (`brand-loader.svg`, `ait-loader` classes) + `css/loading-states.css`

- Constructor: the AI tag is introduced first (tile grows, "A" then "I" rise into it, a sheen crosses it), construction guides appear, the teal pen leaves the tag, draws the toolbox and goes home, the toolbox fills and the tag pulses; 4.8 s loop, `ait-once` for a splash. 96 px splash / workspace boot, 40 px minimum, app-level waits only.
- Colours from the tokens: `logo-box` (night box on light, lavender on dark), `on-logo-box`, `logo-cursor`, `ai`, `on-ai` — the markup is theme-agnostic.
- **Keyboard and screen reader:** the loader is `role="status"` with a visible or hidden label; under reduced motion it shows the finished mark.

Tokens: `--md-sys-color-logo-box`, `-on-logo-box`, `-logo-cursor`, `-ai`, `-on-ai` through `.ait-loader .ait-*` in `loading-states.css` (identical under M2 and M3).

### Menu

**Angular Material:** `mat-menu` / `mat-menu-item`

- 48 px items on `surface-container`, radius-xs, elevation-2, 8 px vertical padding, 112–280 px wide.
- Items: 20 px leading icon, body-medium label, optional trailing shortcut in label-medium `on-surface-variant`; hover = `primary` state layer at 6 %; keyboard focus = focus ring, no layer.
- Destructive items in `error`, last, after a divider. List-level states as non-selectable items with the 20 px tile glyph (StateMark C) + Retry.
- **Keyboard and screen reader:** the trigger has `aria-haspopup="menu"` and `aria-expanded`; opening moves focus to the first item; ↑ ↓ Home End move; Esc and Tab close and return focus to the trigger (`mat-menu` does this).

`mat.menu-overrides((…))` sets these in **both** files; the CSS variable is `--mat-menu-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-color` | #F8F1FF / #23202D | `background.card` → override | `--mat-sys-surface-container` (default) |
| `container-shape` | 4px (`radius-xs`) | `mat.menu-overrides` | `--mat-sys-corner-extra-small` (default) |
| `item-label-text-color` | #1C1B1E / #ECE5F8 | `foreground.text` | `--mat-sys-on-surface` |
| `item-icon-color` | #48454E / #CAC3DC | `foreground.icon` | `--mat-sys-on-surface-variant` |
| `item-icon-size` | 20px | default 24px → 20px | default 24px → 20px |
| `item-hover-state-layer-color` | `primary` at 6 % (pressed 10 %) | `mat.menu-overrides` (set in `theme.m2.scss`) | `mat.menu-overrides` (set in `theme.m3.scss`) |
| `divider-color` | #CAC4CF / #494458 | `foreground.divider` | `--mat-sys-outline-variant` |


### NavigationBar

**Angular Material:** no Angular Material component — `mat-toolbar` + `mat-button`s (or `mat-tab-nav-bar`) with the AIToolbox markup

- Phone bottom navigation, 80 px, 3–5 destinations on `nav-container` (violet tint in light). Active: 64×32 px `secondary-container` pill behind the icon, label `on-surface` at 600; inactive `on-surface-variant`.
- Badges on the icon. On tablet / desktop the destinations move to the NavigationRail.
- **Responsive:** Compact only (under 600 px): 3–5 destinations, the rest in the modal drawer opened from the top-bar menu. From 600 px the destinations move to the NavigationRail; a phone in landscape (height under 480 px) also takes the rail.
- **Keyboard and screen reader:** the active destination has `aria-current="page"` and a 3 px `primary` bar on top of its pill; labels always visible; it replaces the drawer at 320 CSS px and 200 % zoom.

Tokens: `.dt-nav` on the bottom `mat-toolbar` → `toolbar-container-background-color: nav-container`; the pill is plain CSS on `--md-sys-color-secondary-container` / `-on-secondary-container`.

### NavigationDrawer

**Angular Material:** `mat-sidenav` (`mode="over"` on phones, `"side"` on desktop) + `mat-nav-list`

- Opened **on demand** from the NavigationRail menu button: the rail is the default navigation from 600 px and every session starts on it. 360 px (300 shown) on `nav-container` — a violet band (#EDE4FF in light), the deepest light surface, darker than the pale containers; no border on the content side (the colour separates it); a 2 px gap of `surface` separates it from the top app bar; the menu button (close back to the rail) is the first row of the drawer, aligned with the item icons; 12 px inset, 56 px items at radius-lg (16 px) — hover and active indicators share that shape. Active `secondary-container` (the pale purple #DED7EB in light) + `on-secondary-container` and a 3 px `primary` leading bar; others `on-surface-variant`; trailing counts label-medium.
- Destinations: **Sweep · Environments · Docs · Catalog · Community** (Catalog: Browse · Mine · Team · Requests; Community: What's new · Guides · Ideas), each with its feature mark at 24 px (the static `light/` or `dark/` file). No Dashboard for now; no Settings (account menu in the header); no assistant or notifications (header). Section header label-medium `on-surface-variant` ("Workspace").
- Bottom: **Administration** (shield icon) for people with at least one admin right, then **Cookie policy** — cookie icon, trailing open-in-new icon, opens the policy in a new tab — and nothing under it: no Terms, no version. It replaces the former Privacy · Cookies · Terms footer; never in the top app bar.
- **Responsive:** Closed by default at every width. From 1200 px the rail menu button opens it as a standard drawer (`mode="side"`, 300 px, pushes the page) until the user closes it; it folds back to the rail while the docked assistant needs the room (page keeps ≥ 720 px). Under 1200 px it only opens over the page (`mode="over"`, scrim): from the rail menu button (600–1199 px) or the top-bar menu (under 600 px).
- **Keyboard and screen reader:** the opener has `aria-expanded` and `aria-controls`; Esc closes an over drawer and focus returns to the menu button; the active item has `aria-current="page"`, the `secondary-container` pill and a 3 px `primary` leading bar (`dt-nav-active`), because the pill alone is 1.1:1 on the band.

`mat.sidenav-overrides((…))` sets these in **both** files; the CSS variable is `--mat-sidenav-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-background-color` | #EDE4FF / #1D1A27 (`nav-container`) | `.dt-nav` class on `mat-sidenav` (set in `theme.m2.scss`) | `.dt-nav` → `var(--md-sys-color-nav-container)` (set in `theme.m3.scss`) |
| `container-text-color` | #48454E / #CAC3DC | `foreground.secondary-text` | `--mat-sys-on-surface-variant` |
| `container-shape` | 0 16px 16px 0 | override | `--mat-sys-corner-large` on the open side (default) |
| `container-width` | 360px | default 360px | default |
| `scrim-color` | scrim at 32 % | default | default |

Items: `mat.list-overrides((active-indicator-shape: 16px, list-item-one-line-container-height: 56px))`; inside `.dt-nav` the indicator is `secondary-container` (set in both theme files).

### Administration

- **One entry, admins only.** Administration is the last destination above Cookie policy in the drawer and rail, shown to anyone with at least one admin right (platform, workspace or feature) and hidden otherwise — never disabled. A direct link without the right shows an access-denied state naming who to ask.
- **No admin inside features.** Features expose no Manage tab or settings entry. Each feature team ships its administration as a **remote module** (Native Federation) with a manifest: id, label, route, required right, summary for the hub card. The Administration shell loads only the modules the user has rights on.
- **Shell: the admin sidebar** (B in the Administration layout lab, adopted). One page with a 240 px sidebar on the left and the section on the right. The sidebar lists **Core** (General, Users and permissions, Groups, Audit log, Catalog), then one group per feature module, each with its sections — today **Sweep** (Connectors, Tools and skills) and **Community** (Releases, Tours, Feedback, Ideas triage, Insights). A champion with no other right sees Core reduced to "Catalog · Review". Group headers in label-medium uppercase with the feature mark; items 40 px, radius 16, active item on `secondary-container` with a 3 px `primary` inset and weight 700; counts as badges. Rights remove groups and items (a Sweep admin sees Sweep, and only "Feedback · Sweep" under Community); a new feature module adds a group. The landing section is the first one the person has rights on. Feature sections start with a **module line**: Remote module tag, remote id, owner, scope, then the module's actions (New release, New tour…). No hub and no back chip.
- **Header context:** `Administration · Core` / `Administration · Sweep` / `Administration · Community` over the section and its summary ("Users and permissions · 1,284 users from the directory · 46 admins · 1 request").
- **Core · General** (the landing section for platform admins): workspace name, default language, time zone, support contact; retention for the audit log, feedback and surveys, assistant history; Cancel / Save.
- **Core · Users and permissions.** Accounts are provisioned automatically from the company directory (SSO), with their team: there is **no Invite user and no account creation**. A line "Directory sync · 10 min ago" (success StatusChip) says so; the page only gives admin rights. Filter chips All, Admins, Requests; search; the user table (user, admin rights as tags with a pending request as a warning StatusChip, team from the directory, last active; a row is a button); the **Admin rights** panel (340 px beside the table, below it under 1200 px): team read-only, a pending request with Decline / Approve, checkboxes Platform admin, Sweep admin, Community admin, Feedback · Sweep, then Cancel / Save.
- **Sweep · Connectors**: the outside services Sweep reads from and writes to (DevOps platform, Jira, Microsoft Teams, SonarQube, Artifactory); the DevOps MCP server and the Create Jira ticket tool use the same credentials — table of connector (and host), used for, scope, status (Connected / Token expires in n days / Not connected), last sync, and Configure, Renew token or Connect; Add connector. Credentials are kept in the vault and never shown again after saving.
- **Core · Catalog** (platform admins; champions see Catalog review only): **Review** (a table of skills submitted to everyone — skill and one line, author, submitted, Review; open one to read the instructions and tools, tick three points — tried it, no sensitive data, the actions that change something are needed — use the Discussion with the author, then Ask for changes or Publish), **Items** (every tool, skill and MCP server: owner, who can use it, uses; Add tool or MCP server), **Policies** (who can publish: skills for yourself or your team, everyone; skills for everyone, after review; tools and MCP servers, platform team — and the ceiling for actions that change something, for the assistant and for Sweep runs: Ask first / Allowed / Off; reading is allowed everywhere).
- **Sweep · Tools and skills:** what a run may use **per phase** (implement, review, test, release): catalog items with one checkbox per phase; Add from the Catalog. Actions that change something ask first, per the ceiling in Core › Catalog, and stop the run until someone approves, with the same approval card as the assistant.
- **Community · Insights:** collects feedback from **feedback forms, surveys and tours** (and release reads): a Sources line, KPI cards each naming its source (after-action score, NPS, tour completion, read rate), feedback forms by feature (answers and score, themes by the assistant), tours (started, completed, where people leave), surveys, needs attention, open questions in discussions. **Usage metrics from OpenSearch** (active users, adoption, run volumes, errors) have a dashed "To be designed" slot until a later design round.
- **Responsive:** below 1200 px the sidebar becomes a grouped **Section** select above the content and the Admin rights panel goes under the table; tables scroll sideways in their card under 840 px.
- **Keyboard and screen reader:** the sidebar is a `nav` named "Administration", the active item has `aria-current="page"`; the Section select is labelled; table rows that open a panel are `role="button"` with `aria-pressed`.
- **Rights add up and are scoped.** A feature admin sees only their feature modules, plus their feature's feedback through the scoped right **Feedback · <feature>** (separate from Community admin). Platform admin manages access and cross-cutting settings.
- **Feedback (Community module, admin only).** All feedback administration is in Community › Feedback (variant A in the Feedback administration lab): **Profiles** (every feature's profile, edited with the FeedbackProfile editor), **Inbox** (all features; reply, route to Jira or support, propose as idea with the author's consent; discussions without a reply after 2 working days), **Surveys** and **Solicitation policy**. One cap per user for prompts, micro-surveys and NPS together; the Feedback button and AI-answer thumbs never count against it. Bugs go to Jira, never to Ideas. A feature admin with Feedback · Sweep sees their profile, the Sweep inbox and the cap read-only, never surveys, releases, tours or ideas. See FeedbackProfile below.
- Personal preferences stay in the account menu under **Settings**.

### NavigationRail

**Angular Material:** no Angular Material component — vertical `mat-nav-list` in an 80 px aside

- **The default navigation from 600 px** (Medium to Extra-large): 80 px wide on `nav-container` (violet band in light), no border — the colour itself separates it from the content; menu button, then the destinations **Sweep · Envs · Docs · Catalog · Community** with their feature marks at 24 px and label-medium labels under the icon. Active 56×32 px `secondary-container` pill + 3 px `primary` leading bar.
- Bottom: **Admin** (shield icon, admins only) then **Cookies** (cookie icon, opens the cookie policy in a new tab), nothing under it (no version, no Terms). No Settings (account menu in the header), no Privacy destination.
- **Responsive:** Shown by default at every width from 600 px. Its menu button opens the NavigationDrawer on demand: over the page with a scrim (600–1199 px), standard and pushing the page from 1200 px. While the docked assistant needs the room an open drawer folds back to the rail. A phone in landscape (height under 480 px) also takes the rail.
- **Keyboard and screen reader:** same active cue as the drawer (pill + 3 px leading bar, `aria-current="page"`); every icon has a visible label or a tooltip that is also its name.

Tokens: list overrides as for the drawer (`.dt-nav` → `active-indicator-color: secondary-container`); no edge line.

### ProgressIndicator

**Angular Material:** `mat-progress-spinner` (pen orbit) and `mat-progress-bar` (guide line) keep their slots and APIs — the AIToolbox skins are the inline SVGs from `loading-states/` with `loading-states.css`, or a thin wrapper around the Material components bound to `value`

- Pen orbit (circular): violet arc with the teal pen at its head on a `primary-container` track; 48 px content, 24 px inline, 18 px in a button.
- Guide line (linear, 4 px): dashed teal guide as the track, violet bar with the pen on its edge; determinate = violet to the value. Indeterminate at the top of the app bar during navigation.
- Constructor determinate (`brand-progress.svg`, `--p`): long operations with a known value, 64–96 px. Working dots: neon green = a command runs, teal = a model thinks.
- **Keyboard and screen reader:** `role="progressbar"` with a name and, when known, `aria-valuenow`; the AI pen and guide use `ai` (deep teal on light grounds, 8.9:1); under reduced motion the indicator stops and the label ("Deploying…") carries the state.

`mat.progress-bar-overrides((…))` sets these in **both** files; the CSS variable is `--mat-progress-bar-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `active-indicator-color` | #39235F / #C4C0FF | `color="primary"` | `--mat-sys-primary` |
| `track-color` | #E3DFFF / #413C8A (when the Material bar is kept) | `primary` lighter | `--mat-sys-surface-variant` by default → primary-container |
| `track-height` | 4px | default | default |
| `active-indicator-height` | 4px | default | default |

`mat.progress-spinner-overrides((…))` sets these in **both** files; the CSS variable is `--mat-progress-spinner-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `active-indicator-color` | #39235F / #C4C0FF | `color="primary"` | `--mat-sys-primary` |
| `active-indicator-width` | 4px (5px at 24 / 18 px) | `strokeWidth` | `strokeWidth` |
| `size` | 48 / 24 / 18px | `diameter` | `diameter` |

AI tasks: `.dt-ai` → `active-indicator-color: ai`. The dashed guide and the pen head exist only in the SVG skins (`.ait-gl-guide`, `.ait-po-pen` → `--md-sys-color-ai`).

### RadioButton

**Angular Material:** `mat-radio-group` / `mat-radio-button`

- 20 px ring, 10 px dot, 2 px border; selected `primary`, unselected `on-surface-variant`. One selected per group, grouped in a `fieldset` with a `legend`.
- 2–5 short inline options read better as filter chips or a SegmentedButton; radios suit vertical lists with descriptions, 44 px rows.

`mat.radio-overrides((…))` sets these in **both** files; the CSS variable is `--mat-radio-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `selected-icon-color` | #39235F / #C4C0FF | `color="primary"` (set as default; M2 default is `accent`) | `--mat-sys-primary` |
| `unselected-icon-color` | #48454E / #CAC3DC | `foreground.secondary-text` | `--mat-sys-on-surface-variant` |
| `label-text-color` | #1C1B1E / #ECE5F8 | `foreground.text` | `--mat-sys-on-surface` |
| `touch-target-size` | 48px | default | default |


### Search

**Angular Material:** no Angular Material component — `mat-form-field appearance="fill"` styled as the bar + `mat-autocomplete` as the view

- Search bar 56 px, radius-lg (16 px), `surface-container-high`, leading menu/back icon, placeholder `on-surface-variant`, trailing avatar or action.
- Search view below, radius-lg, same container tone; rows are 48 px list items with a type hint in label-medium; results grouped by kind, identifiers in Open Sans 600.
- **Responsive:** Under 600 px the field is an icon button that opens the search view full screen; 600–1199 px the field flexes from 240 px (320 px from 840) to 440 px with the Ask chip as an icon; from 1200 px it is 600 px with the labelled Ask chip.
- **Keyboard and screen reader:** `role="search"`; ⌘K focuses the field; results are a listbox with arrow keys; the result count is announced.

`mat.autocomplete-overrides((…))` sets these in **both** files; the CSS variable is `--mat-autocomplete-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `background-color` | #F2EBFA / #2B2836 | `background.card` → override | `--mat-sys-surface-container` by default → high |
| `container-shape` | 16px | override | `--mat-sys-corner-extra-small` by default → 16px |

Bar: `mat.form-field-overrides((filled-container-color: surface-container-high, filled-container-shape: 16px, filled-active-indicator-height: 0))`.

### SegmentedButton

**Angular Material:** `mat-button-toggle-group` (`appearance="standard"`; `hideSingleSelectionIndicator=false` for the leading check)

- 2–5 options, 40 px, radius-lg (16 px) outer corners, `outline` dividers. Selected `secondary-container` with a leading check; others transparent, `on-surface` text.
- Views of the same data (Day / Week / Month, List / Grid); navigation → Tabs, filters → chips.
- **Keyboard and screen reader:** one Tab stop, arrow keys between segments, `aria-pressed` (multi) or radio semantics (single); focus ring inside the group.

`mat.button-toggle-overrides((…))` sets these in **both** files; the CSS variable is `--mat-button-toggle-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `selected-state-background-color` | #DED7EB / #484454 | `accent` lighter | `--mat-sys-secondary-container` |
| `selected-state-text-color` | #1D1A28 / #E6DFF3 | contrast | `--mat-sys-on-secondary-container` |
| `text-color` | #1C1B1E / #ECE5F8 | `foreground.text` | `--mat-sys-on-surface` |
| `divider-color` | #79757F / #948DA5 | `foreground.divider` → `outline` | `--mat-sys-outline` |
| `shape` | 16px | `mat.button-toggle-overrides` | `mat.button-toggle-overrides` (default is `--mat-sys-corner-full`) |
| `height` | 40px | default 40px | default |


### SideSheet

**Angular Material:** `mat-sidenav position="end"` (`mode="side"` standard, `"over"` modal) or `mat-drawer`

- 256–400 px docked right: `surface` + `outline-variant` divider (standard) or `surface-container-low` + scrim (modal). Header title-large + close icon button; actions pinned to the bottom above a divider.
- Standard pushes content, modal overlays it; on phones it becomes a BottomSheet. The assistant is **not** a side sheet: it is the inline Assistant block (see Assistant).
- **Responsive:** From 1200 px standard (pushes the page) or modal; 600–1199 px modal only (`mode="over"`, scrim); under 600 px it becomes a BottomSheet, or a full-screen dialog for a form.
- **Keyboard and screen reader:** modal sheets move focus in and back, Esc closes; standard sheets keep focus where it is.

`mat.sidenav-overrides((…))` sets these in **both** files; the CSS variable is `--mat-sidenav-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-background-color` | #FDF8FD / #14121E (standard) · #FAF4FF / #1D1A27 (modal) | `background.background` / `card` | `--mat-sys-surface` / `-surface-container-low` |
| `container-divider-color` | #CAC4CF / #494458 | `foreground.divider` | `--mat-sys-outline-variant` |
| `container-shape` | 0 (docked edge) | override | `--mat-sys-corner-large` by default → 0 on the docked edge |


### Slider

**Angular Material:** `mat-slider` (`discrete`, `showTickMarks`; two `matSliderThumb`s for a range)

- 4 px track `primary-container`, active segment `primary`, 4×24 px handle, value label `inverse-surface` while dragging; continuous or discrete, range with two handles.
- Values with a meaningful visual range (CPU limit, replicas 1–20); exact numbers pair it with a text field.

`mat.slider-overrides((…))` sets these in **both** files; the CSS variable is `--mat-slider-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `active-track-color` | #39235F / #C4C0FF | `color="primary"` | `--mat-sys-primary` |
| `inactive-track-color` | #E3DFFF / #413C8A | `primary` lighter | `--mat-sys-primary-container` by default → keep |
| `handle-color` | #39235F / #C4C0FF | `primary` | `--mat-sys-primary` |
| `handle-width` | 4px | default 20px → 4px | default 20px → 4px |
| `handle-height` | 24px | default 20px → 24px | default 20px → 24px |
| `label-container-color` | #313033 / #E6DFF2 | override | `--mat-sys-primary` by default → inverse-surface |
| `active-track-height` | 4px | default 6px → 4px | default 6px → 4px |
| `inactive-track-height` | 4px | default 4px | default |


### Snackbar

**Angular Material:** `MatSnackBar` (custom component for the leading state mark)

- `inverse-surface` ground, `inverse-on-surface` text, one optional action in `inverse-primary`, optional close; 48 px single line, 68 px two lines; radius-xs; elevation-3; 4–10 s.
- Leading 24 px StateMark A (badge in `inverse-primary` on the inverse surface). Never for errors that need a decision (dialog); never stacked.
- **Responsive:** Under 600 px full width minus 2 × 16 px, 16 px above the NavigationBar; from 600 px 344–600 px wide at the bottom of the page area, aligned on the page margin.
- **Keyboard and screen reader:** `role="status"` (polite); its action is reachable by keyboard while shown and leaves the Tab order when it closes (`visibility: hidden` or removed); never the only place an error is reported.

`mat.snack-bar-overrides((…))` sets these in **both** files; the CSS variable is `--mat-snack-bar-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-color` | #313033 / #E6DFF2 | `mat.snack-bar-overrides` (M2 hard-codes a dark container) | `--mat-sys-inverse-surface` (default) |
| `supporting-text-color` | #F4EFF4 / #322E3C | same override | `--mat-sys-inverse-on-surface` |
| `button-color` | #C4C0FF / #413C8A | same override | `--mat-sys-inverse-primary` |
| `container-shape` | 4px | override | `--mat-sys-corner-extra-small` (default) |
| `supporting-text-size` | 14px (body-medium) | `body-2` | `--mat-sys-body-medium-size` |


### StateMark

**Angular Material:** inline SVG from `assets/States` (never `mat-icon`); hosts: `matChipAvatar` (tile, 18 px), the leading element of a snackbar component (badge, 24 px), first element of a table status column (tile, 20 px), empty-state templates (circle, 56–96 px)

- One construction: the toolbox never changes (the night `logo-box` with its `>_`, lavender on dark), the corner badge carries the state role and symbol (✓ success · i info = `primary` · ! warning · ✕ error).
- A · alone 24–40 px (snackbars, popin headers, inline alerts) · B · circle 56–96 px (empty states, table-/panel-/popin-level errors: disc in the state role, dark on light and light on dark, toolbox reversed, badge in the state container) · C · tile glyph 18–20 px (chips, cells, options).
- Loading is not a state: the slot shows the pen-orbit ring around the plain mark and takes the state in place when the request resolves (warning after a timeout, error with Retry). No entrance animation; never below 18 px; never recoloured.

Tokens: `--md-sys-color-success | warning | error | primary` and their `on-*`, `*-container`, `on-*-container` for the badge, disc and tile; `--md-sys-color-logo-box` / `-on-logo-box` / `-logo-cursor` for the toolbox; `-ai` for the pending pen. Identical under M2 and M3.

### StatusChip

**Angular Material:** `mat-chip` with `class="dt-chip-success | dt-chip-warning | dt-chip-error | dt-chip-info"` + the tile glyph in `matChipAvatar`; log levels are plain `span`s

- Label-medium, radius-xs, `*-container` fill with `on-*-container` text, led by the 18 px tinted tile glyph (StateMark C); a 6 px `outline` dot only for unknown on `surface-container-highest`.
- Log levels colour only the level word, Open Sans 600: INFO `success`, WARN `warning`, ERR `error`. Never `primary` / `secondary` / `tertiary` for a status, never a status colour for a button.
- **Keyboard and screen reader:** the glyph tile is `aria-hidden`, the word is the name ("Failed", not "multiplication x Failed"); never colour alone.

`mat.chips-overrides((…))` sets these in **both** files; the CSS variable is `--mat-chip-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `elevated-container-color` | state container: #ACF4A2 / #0B5314 · #FFDEA0 / #5C4300 · #FFDAD6 / #93000A · #E3DFFF / #413C8A | `.dt-chip-*` → `mat.chips-overrides` (same as M3) | `.dt-chip-*` → `mat.chips-overrides` |
| `label-text-color` | on-state-container | same | same |
| `container-shape-radius` | 4px (`radius-xs`) on status chips | class override | class override |
| `with-avatar-avatar-size` | 18px | override | override |


### Switch

**Angular Material:** `mat-slide-toggle`

- 52×32 px track. On: `primary` track, 24 px `on-primary` handle with an optional check icon. Off: `surface-container-highest` track, 2 px `outline` border, 16 px `outline` handle.
- Label left in settings lists (switch trailing) or right in forms; a switch applies immediately — if the change needs confirmation use a checkbox + Save.
- **Keyboard and screen reader:** `role="switch"` with `aria-checked` and a label; Space toggles; the off-state outline is ≥ 3:1.

`mat.slide-toggle-overrides((…))` sets these in **both** files; the CSS variable is `--mat-slide-toggle-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `selected-track-color` | #39235F / #C4C0FF | `color="primary"` | `--mat-sys-primary` |
| `selected-handle-color` | #FFFFFF / #2A2473 | contrast | `--mat-sys-on-primary` |
| `selected-icon-color` | #39235F / #C4C0FF | default | `--mat-sys-on-primary-container` by default → primary |
| `unselected-track-color` | #ECE5F4 / #363341 | override | `--mat-sys-surface-variant` by default → surface-container-highest |
| `unselected-handle-color` | #79757F / #948DA5 | override | `--mat-sys-outline` (default) |
| `track-outline-color` | #79757F / #948DA5 | override | `--mat-sys-outline` (default) |
| `track-width` | 52px | default | default |
| `track-height` | 32px | default | default |
| `selected-handle-size` | 24px | default | default |
| `unselected-handle-size` | 16px | default | default |


### Tabs

**Angular Material:** `mat-tab-group` (primary: `fitInkBarToContent=false`, `stretchTabs`; secondary: `fitInkBarToContent`, scrollable) / `mat-tab-nav-bar`

- Primary: fixed, equal width, 48 px, 3 px rounded `primary` indicator; top-level sections. Secondary: scrollable, content-width, 2 px full-width indicator; sub-sections.
- Active label `primary`, inactive `on-surface-variant`, label-large; max 6 tabs, else a navigation rail. `role="tab"` + `aria-selected`.
- **Responsive:** Scrollable under 600 px of page area, counts kept; never wrapped onto two lines.
- **Keyboard and screen reader:** `role="tablist"` with one Tab stop (roving tabindex), ← → Home End move and select, each tab `aria-controls` its `tabpanel`; focus ring inside the tab so a scrolling bar does not clip it.

`mat.tabs-overrides((…))` sets these in **both** files; the CSS variable is `--mat-tab-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `active-indicator-color` | #39235F / #C4C0FF | `color="primary"` | `--mat-sys-primary` |
| `active-label-text-color` | #39235F / #C4C0FF | `primary` | `--mat-sys-on-surface` by default → primary |
| `inactive-label-text-color` | #48454E / #CAC3DC | `foreground.secondary-text` | `--mat-sys-on-surface` by default → on-surface-variant |
| `active-indicator-height` | 3px (primary) · 2px (secondary) | default 2px → 3px | default 2px → 3px |
| `active-indicator-shape` | 3px 3px 0 0 (primary) | override | `--mat-sys-corner-full` top (default) |
| `container-height` | 48px | default 48px | default |
| `divider-color` | #CAC4CF / #494458 | `foreground.divider` | `--mat-sys-surface-variant` by default → outline-variant |
| `label-text-size` | 14px (label-large) | `button` | `--mat-sys-label-large-size` |


### TextField

**Angular Material:** `mat-form-field appearance="outline"` + `matInput` (`"fill"` in dense tables); `mat-select`, `mat-autocomplete`, `matDatepicker` inside it

- Outlined, 56 px, radius-xs, floating label on the surface colour behind it. Resting 1 px `outline` border + `on-surface-variant` label; focused 2 px `primary`; error 2 px `error` with label and helper in `error`, `aria-invalid` + `aria-describedby`.
- Code, keys, URLs, paths in Open Sans 600; prose values body-large. Helper body-small `on-surface-variant`, 4 px below, 16 px inset. Inside a dialog the label background is the dialog colour. 24 px between fields.
- **Responsive:** Forms are one column, 600 px max; pairs (start / end date) sit side by side from 600 px of page area; under 600 px the form actions are full width.
- **Keyboard and screen reader:** a visible label (never placeholder only); focus = outline 2 px `primary`, no outer ring; errors set `aria-invalid` and `aria-describedby`, are announced (`role="alert"` on submit) and focus moves to the first invalid field; a form title is a heading.

`mat.form-field-overrides((…))` sets these in **both** files; the CSS variable is `--mat-form-field-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-height` | 56px | density 0 → 56px | 56px |
| `outlined-outline-color` | #79757F / #948DA5 | `foreground.divider` → set `outline` | `--mat-sys-outline` |
| `outlined-outline-width` | 1px | default | default |
| `outlined-label-text-color` | #48454E / #CAC3DC | `foreground.secondary-text` | `--mat-sys-on-surface-variant` |
| `outlined-container-shape` | 4px (`radius-xs`) | `mat.form-field-overrides` | `--mat-sys-corner-extra-small` (default) |
| `outlined-input-text-color` | #1C1B1E / #ECE5F8 | `foreground.text` | `--mat-sys-on-surface` |
| `error-text-color` | #93000A / #FFB4AB | `warn` | `--mat-sys-error` |
| `outlined-error-outline-color` | #93000A / #FFB4AB | `warn` | `--mat-sys-error` |
| `filled-container-color` | #ECE5F4 / #363341 (dense tables) | override | `--mat-sys-surface-container-highest` (default) |
| `subscript-text-size` | 12px (body-small) | `caption` | `--mat-sys-body-small-size` |

Focused 2 px `primary` outline: `focus-outline-color` is not a token — it follows `--mat-sys-primary` (M3) / the `primary` palette (M2) automatically. Select panel: `mat.select-overrides((panel-background-color: surface-container))`, selected option `mat.option-overrides((selected-state-layer-color: secondary-container, selected-state-label-text-color: on-secondary-container))`. Options (select, multi-select, autocomplete): hover = `primary` 6 %; the keyboard-active option shows the 2 px focus ring only, no fill; a select opened with the mouse shows no ring until an arrow key is pressed; the selected option keeps `secondary-container` while active (theme files).

### TimePicker

**Angular Material:** `mat-timepicker` (v19+; input mode) — the dial mode is the AIToolbox custom component

- Input mode 328 px: two 96×80 px fields in display-large, the active one in `primary-container`, AM/PM segmented in `tertiary-container` when selected. 24 h, 5-minute steps in ops forms; schedules always show the timezone next to the field.

`mat.timepicker-overrides((…))` sets these in **both** files; the CSS variable is `--mat-timepicker-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-background-color` | #F2EBFA / #2B2836 | override | `--mat-sys-surface-container` by default → high |
| `container-shape` | 16px | `mat.timepicker-overrides` | `--mat-sys-corner-extra-small` by default → 16px |


### Tooltip

**Angular Material:** `matTooltip` (A–E); structured plain tooltips (B–D) and rich ones (F–G) in a `cdkConnectedOverlay` — CSS in `brand/css/tooltips.css`

- Two families: **plain** (inverse surface, short, never interactive) and **rich** (container surface, can hold actions). Formats: A plain (names an icon-only control) · B plain + shortcut · C data (full value of a truncated identifier, copyable) · D status (state tile + cause + time) · E disabled reason (and how to unlock it) · F rich (explains a term, from an info icon) · G AI rich (explains AI content, AI chip + “Ask the assistant”).
- Plain: `inverse-surface` / `inverse-on-surface`, label-medium 12/16, min-height 24, padding 4 × 8, `radius-xs` 4, max-width 240 (data 320, status 280), one line (two max), no caret. Shortcut keys Open Sans 600 11 with a 1 px `inverse-on-surface` 33 % border. Data value Open Sans 600; “Copied” in `primary-container` for 1.5 s; the truncated anchor has a dotted `outline` underline. Status tile 16 px = the status `*-container` with its `on-*-container` symbol.
- Rich: `surface-container-high`, elevation-2, `radius-md` 12, padding 12 × 16, width 280–320; title-small `on-surface`, body-medium `on-surface-variant`, max 2 text actions in `primary`; AI: `ai-container` chip before the title, first action AI tonal.
- Timing: plain after 500 ms hover, at once on keyboard focus, no delay when moving to the next icon within 300 ms, hides 150 ms after leave; rich 500 ms hover or click, stays while hovered / focused, 300 ms grace. Placement 8 px from the anchor, below in the header, above elsewhere, flips on collision, 8 px from the viewport edge. Motion: fade + scale .8 → 1, 150 ms emphasized decelerate; exit fade 75 ms.
- A11y: `role="tooltip"` + `aria-describedby`; Esc closes; hovering the tooltip keeps it open (WCAG 1.4.13); disabled controls with a reason use `aria-disabled` and stay focusable. Touch: long-press 1.5 s for plain, tap the info icon for rich, data → “Copied” snackbar. Never repeat a visible label, never put controls in a plain tooltip, never hide information that exists nowhere else.
- **Keyboard and screen reader:** shows on hover after 500 ms and at once on keyboard focus; stays open while the pointer is on it (WCAG 1.4.13); Esc dismisses it without moving focus; it is the anchor's `aria-describedby`; a disabled reason is also a persistent hidden description.

`mat.tooltip-overrides((…))` sets these in **both** files; the CSS variable is `--mat-tooltip-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-color` | #313033 / #E6DFF2 | override | `--mat-sys-inverse-surface` (default) |
| `supporting-text-color` | #F4EFF4 / #322E3C | override | `--mat-sys-inverse-on-surface` |
| `container-shape` | 4px | override | `--mat-sys-corner-extra-small` (default) |
| `supporting-text-size` | 12px (label-medium) | `caption` | `--mat-sys-body-small-size` by default → label-medium |

`matTooltipShowDelay` = 500, `matTooltipHideDelay` = 150, `matTooltipPosition` = `below` in the header, `above` elsewhere; `matTooltipClass` = `ait-tip-data` / `ait-tip-status`.

### GuidedTour

**Angular Material:** `ait-guided-tour` service + overlay (`cdkConnectedOverlay` for the step card, a scrim layer in the `Overlay` container); no `MatTooltip` — CSS in `brand/css/tour.css`

- One component, two parts: the **spotlight** (a `scrim` layer at 42 % over the page with a cutout on the target, 6 px larger than the element, `radius-md` 12 or `radius-lg` 16 on navigation items, 2 px `primary` ring with the 4 px 18 % glow) and the **step card** (`surface-container-high`, elevation-2, `radius-md` 12, 340 px, padding 12 × 16: tour tag in `primary-container`, "Step n of N" body-small, title-small, body-medium `on-surface-variant`, text actions Skip · Back · Next / Done). Decided in the Tour focus lab against ring, pulse, beacon, blur, glow and spotlight + pulse.
- Targets are `data-anchor` ids registered by the feature team on the element; the tour measures the element at runtime (after fonts, on resize, after every render), scrolls it into view first, and draws the cutout from the measured rectangle. Never from coordinates. A missing anchor skips the step and is reported.
- Placement: card 16 px right of the cutout, 8 px above its top; else 16 px left; else 12 px below, kept 16 px inside the page. Never over the target. Targets wider than 60 % of the page get a 16 % scrim.
- Motion: scrim fade 350 ms and card rise 8 px / 400 ms, emphasized easing, replayed on every step; no loop, no pulse. Reduced motion: no fade, no rise.
- Only the target is clickable; the dimmed page is inert and out of the Tab order. Never teal, even for an AI feature; the feature keeps its own colour inside the cutout.
- **Keyboard and screen reader:** the card is `role="dialog"` "Guided tour", focus moves to it on each step and stays inside; Esc = Skip; the body names the target in words; the spotlight layers are `aria-hidden`.

Tokens: `scrim` for the layer (M2: `$dt-scrim`; M3: `--mat-sys-scrim`), `primary` for the ring (`--mat-sys-primary`), `surface-container-high` for the card (`--mat-sys-surface-container-high`); shape `--mat-sys-corner-medium` / `-large`.

### Catalog

**Angular Material:** `mat-tab-nav-bar` (Browse · Mine), `mat-button-toggle-group` (kind), `mat-card` (CatalogItem), `mat-stepper` horizontal, linear (publication), `mat-form-field` outline, `mat-chip-listbox` multiple (tools), `mat-radio-group` (audience), `mat-table` (Mine, admin), the Discussion component

- **A rail destination** between Docs and Community, with its feature mark. One catalog for the assistant and Sweep: **skills** published by people, **tools** and **MCP servers** published by the platform team. Today: MCP servers **DevOps** (pipelines, builds, deployments, pull requests) and **Knowledge base** (Docs, runbooks, the architecture model, ARB decisions); tools **Deploy environment**, **Reserve environment** (Environments) and **Create Jira ticket**.
- **Minimal.** Tabs **Browse** and **Mine**; a kind switch (All · Skills · Tools · MCP servers) and a search; cards with the kind tile, the name, one line and "author · team", usage on the right. No tags on cards. New skill is the page's one filled action.
- **Mine** lists the viewer's skills: stage (Draft, In review, Published — the only status tile), who can use it, version, and one next action (Continue, Open, New version).
- **Item page** (one column, 760 px): kind tile, name, "kind · author · version", **one action** Add to my assistant (In my assistant once added); the description; one line with a lock when it can change something ("Asks before it…"); Try asking (example requests with a Try it link); Tools it provides / Uses (plain list, "changes something" in the metadata); the Discussion panel; one line of metadata (Reviewed, uses, works with, source) and Report a problem.
- **Publication process** (linear stepper, the same for a new skill and a new version): **1 Write** (name, one line, instructions, the tools it may use, one example request; or import from a Git repository with SKILL.md and skill.json, versions from tags; Save draft), **2 Test** (automatic checks — manifest, no secrets, tools exist, changes something or reads only, worked out from the tools — and one try in the assistant with the skill on, approval card included; both are required), **3 Submit** (who can use it: Just me · My team, live at once · Everyone, reviewed first; a note for the reviewer), **4 Review** (everyone only: a champion or a platform admin tries it, ticks three points, talks with the author in the skill's discussion, publishes or asks for changes; 2 working days), **5 Published** (in the Catalog and the assistant's Tools menu; admins can turn it on for Sweep phases). A new version goes back to Review only if it adds an action that changes something. Retiring a skill names its successor and gives users 30 days.
- **Responsive:** cards three per row from 1200 px, two from 840 px, one below; the Test step's two columns stack below 1200 px; the stepper keeps its numbers only below 840 px.
- **Keyboard and screen reader:** tabs are a `tablist` "Catalog"; the kind switch is a `group` of toggle buttons with `aria-pressed`; a card is a `button` named by the item; the current step has `aria-current="step"`; every field has a visible label; the result of Submit is announced once from a polite live region.

Tokens: `primary-container` (Skill tile), `tertiary-container` (Tool tile), `ai-container` (MCP server tile), `surface` + 1 px `outline-variant` (cards, no shadow), `primary` (current step), `secondary-container` (done steps, selected kind).

### Discussion

**Angular Material:** `mat-expansion-panel` (single, not in a `mat-accordion`; `hideToggle` + own chevron; header 48px collapsed and expanded), `mat-button` styled as a link for Show more and Show earlier replies, text `mat-button` Reply, `mat-form-field` outline + filled `mat-button` Send, `mat-form-field` outline + tonal `mat-button` Post

- One component for What's new releases and Ideas (it replaced the earlier Q&A pattern): **one expansion panel** at the end of the item, collapsed by default. Panel: 1 px `outline-variant`, radius 12, `surface-container-lowest`, no shadow, open or closed. **Header = summary bar**, the only control: ≥ 48 px, no tint (the panel colour, `primary` 6 % hover layer); chevron · "Discussion" · up to 3 participant avatars (24 px) · "7 threads · 18 messages" · neutral "Platform team replied" when the team took part · "Last message …" · Show / Hide (`primary`). Expanded header: chevron up, Hide, 1 px `outline-variant` divider, no tint; body fades in 200 ms / 4 px (none under reduced motion).
- **Threads:** opening message (32 px avatar, author, role chip if any, date, body-medium) and its **replies** indented 14 px with a 2 px `primary-container` rule (24 px avatars), one level only. Role chips: Platform team neutral, Champion `primary-container`, Author neutral; nobody else has one. A thread shows its last two replies; "Show n earlier replies" (link) reveals the rest and moves focus. Under each thread: **Reply** (text button, `aria-expanded`) + "n replies" / "No reply yet"; Reply opens an inline field "Reply to …" + Send; the reply goes at the end of the thread. New-message field last ("New message", tonal Post); new threads first, then latest activity.
- **Show more:** three threads per page; link "Show 3 more threads" + "3 of 7 threads shown"; each press adds three, focus to the first new thread, polite live region; no numbered pages; collapsing resets to three. No votes, no "same question", no accepted answer.
- Ideas (layout E): the detail ends with the panel, the only thread on an idea; list rows and admin read "13 messages", sort Most discussed. What's new: the ReleaseItem ends with the panel.
- A thread with no reply after 2 working days → Administration › Community › Feedback › Inbox (source "Discussion"). Moderation: report, hide, move to Feedback or to an Idea.
- **Responsive:** panel at item width; under 600 px the header wraps (Show / Hide on the first line), opening avatars 24 px, replies indent 10 px.
- **Keyboard and screen reader:** header `button` with `aria-expanded` / `aria-controls`, Enter and Space, focus stays, name "Discussion · 7 threads, 18 messages, platform team replied, last message 1 h ago", ring inside the panel (−3 px); body `region` "Discussion"; messages `tabindex="-1"` for focus after Show more / earlier replies; Reply `aria-expanded` / `aria-controls`; posted message announced once.

Tokens: `outline-variant` (panel border, divider), `surface-container-lowest` (panel and header), `on-surface-variant` (chevron), container pairs for avatars (`ai-container`, `primary-container`, `warning-container`, `success-container`, `secondary-container` + `on-*`), `primary-container` (reply rule, Champion chip), `surface-container-high` (neutral role chips). `mat.expansion-overrides((…))`: `container-shape` 12px, `header-collapsed-state-height` / `header-expanded-state-height` 48px, `container-background-color` `surface-container-lowest`.

### FeedbackProfile

**Angular Material:** `mat-tab-nav-bar` (Profiles · Inbox · Surveys · Solicitation policy), `mat-table` (profiles), `mat-chip-listbox` multiple (entry points, options) and single (sampling), `mat-select` + `mat-form-field` outline (question type, routing), `mat-form-field` outline (question), `mat-icon-button` Remove, filled `mat-button` Save profile. Ships in `community-admin`.

- **One place:** Administration › Community › Feedback, admin only. Platform admins see every profile, the inbox for all features, surveys and the cap; a feature admin (right **Feedback · <feature>**, separate from Community admin) sees the Community group reduced to "Feedback · Sweep": tabs Profile, Inbox (locked to Sweep) and Solicitation policy (read-only), with a note saying so.
- **Profiles:** table (profile + owner, status, entry points, questions, sampling, routing, Edit / Close; open row with a 3 px `primary` inset); the editor opens under it (straight away for a feature admin).
- **Editor card** (24 px padding, radius 12): title "Sweep · feedback profile" + "FeedbackProfile component · one editor for every feature's profile"; Profile on / off chip; Entry points (Page button, After an action, On AI answers, Account menu); **Questions · n of 3** — rows with a 24 px number badge, type select (Thumbs, Scale 1–5, NPS 0–10, Single choice, Multiple choice, Text), the question field, Remove; Add question below three; Sampling 10 / 20 / 50 / 100 % (after-action prompts only); Routing (Team inbox, + Jira project, + Teams channel; "Bugs always go to Jira; never to Ideas"); Options (Allow anonymous, Attach context); Close (platform admins) and **Save profile**. Saved changes apply within 5 minutes (snackbar).
- **Preview:** 380 px column, "Preview · side sheet in Sweep": the side sheet with each question and its type, Attach context, Send.
- **Kept reversible:** the component and the per-feature right let the section move to a dedicated Feedback module (variant B) if a separate team takes the inbox.
- **Responsive:** preview under the editor and the table scrolling in its card below 1200 px; below 600 px card padding 16 px, a question row wraps (field on its own line), the cap tile and the feature-admin note stack.
- **Keyboard and screen reader:** `tablist` "Feedback"; toggle chips use `aria-pressed`; question fields are "Question n", Remove is "Remove question n"; row buttons name the profile ("Edit the Sweep feedback profile"); read-only cap chips have `aria-disabled`.

Tokens: `surface` (card), `outline-variant` (rows, divider), `primary-container` (number badge, cap tile), `secondary-container` (selected chips), `warning-container` (feature-admin note), `surface-container` + elevation 2 (preview sheet).

### ReleaseItem

**Angular Material:** `mat-card` (elevated) + `mat-chip-option` / `mat-button`; the changes table is a CSS grid with ARIA table roles (not `mat-table`)

- What's new entry in layout **D · Changelog** (What's new layout lab): meta row (version, type tag, action-required StatusChip, date · areas, unread dot + "New") · title-large title · body-medium summary (72 ch) · **changes table** in a 1 px `outline-variant` frame (radius 8), one row per change: tag 96 px · what changed 200 px label-large 700 · detail body-small · **action line** under a divider: one tonal primary action, chips for Try it / Watch / Acknowledge, "Ask the assistant about this" on AI topics, then Useful? with two icon thumbs, right-aligned. Reasons after a thumb down open below the line; the item ends with the Discussion expansion panel.
- No bullets for changes, one tonal button per item, the aggregated usefulness only in Administration.
- **Responsive:** feed beside a 320 px side column from 1200 px, above it below; under 840 px a change row stacks the detail under tag + title and the action line wraps as two groups; under 600 px card padding 16.
- **Keyboard and screen reader:** `article` named by its `h2`; changes `role="table"` / `row` / `cell`; thumbs `aria-pressed`, named "Useful: yes" / "Useful: no"; the Discussion panel header follows its own rules.

### Assistant

**Angular Material:** custom inline block `ait-assistant-pane` + `aitSplitResize` directive (no `MatSidenav` / `MatDrawer`); inside: `mat-menu`, `mat-dialog` + `mat-tab-group`, `mat-select`, `mat-slide-toggle`, `MatSnackBar`, `cdk-virtual-scroll-viewport`

- **Pane** — a custom inline block beside the page under the header (a split view, not a drawer or side sheet: no backdrop, no overlay, no focus trap), on `surface-container-low` in both themes (#FAF4FF / #1D1A27), 400 px by default, resizable 320 – min(640 px, 50 %), width remembered per user. Divider = resize handle: 1 px `outline-variant` line with an always-visible 6 × 40 grip in `outline` (70 %), 12 px hit zone, `col-resize` cursor; hover 100 ms / focus → 2 px `primary` line and a 6 × 48 `primary` grip; drag shows the width; past 240 px it closes; double-click resets to 400; `role="separator"` with arrows ±16 (Shift 64), Home / End. The page keeps ≥ 720 px: the drawer folds to the rail while the block needs the room; under 1200 px the block takes the page area in place beside the rail (the header button gives the page back); on phones it is the NavigationBar Assistant destination. Header: Chatbot mark (once motion on open), conversation title, page context, History, New conversation, Settings, Close. Triggers: the header assistant button toggles it (selected = `secondary-container` pill, `aria-expanded`, tooltip Open / Close assistant ⌘J; typing dots while an answer is written with the block closed, `tertiary` dot when one waits); the Ask chip sends the search-field text (empty: opens and focuses the composer; disabled with its reason while not live); ⌘J toggles, Esc closes and returns focus. Motion: open = width 0 → W, 300 ms `cubic-bezier(.05,.7,.1,1)`, content fades in (200 ms from 80 ms) and slides 16 px; close = 200 ms `cubic-bezier(.3,0,.8,.15)`, content fades first; no transition while dragging; reduced motion → 150 ms fade.
- Messages: questions right in `primary-container` bubbles (radius 16, 4 on the tail); answers left with the Chatbot mark 24 (typing loop while writing), no bubble, body-medium; data and code in Open Sans 600; code blocks on `surface-container-highest` with their own Copy; streamed with a `primary` caret.
- Question actions (hover / focus): Edit (new version, Enter / Esc, ↑ edits the last one), Copy, ‹ n / m ›. Answer actions (always under the last answer): Copy, Retry (new version), Good, Bad (reason form → Feedback feature), ‹ n / m ›. While writing, Send becomes Stop; a stopped answer keeps its text with “Stopped · Retry”.
- Tool trace: collapsible “Used n tools” (1 px `outline-variant`, radius 12) with source (AIToolbox tool, skill, MCP server), label and status (spinner, `success`, `warning`); missing tools or servers are named with a link to their setting. Approval card for any tool that changes something (unless Always allow): `surface-container`, 1 px `outline`, lock + question, arguments in Open Sans 600, filled action + “Don’t run”.
- Composer: context chip (`secondary-container`, removable), auto-growing text, Tools button with the count, Send / Stop. Disclaimer always under it: “The assistant can make mistakes. Check important information before you act on it.” body-small, `on-surface-variant`, centred.
- Tools / skills / MCP servers: quick switches in the composer menu, defaults in Assistant settings (dialog: Tools · Skills · MCP servers · History and data); these are views of the **Catalog** with a Browse catalog button, and a skill added from the Catalog shows here at once. Tools Always allow / Ask first / Off (write tools default Ask first); skills Built-in · Organisation · Yours; MCP servers with status pill, URL, auth, tool list (write tools in `warning-container`), organisation lock, add by https URL. Admin sets the ceiling.
- History: slides over the chat (300 / 250 ms); search, Pinned · Today · Yesterday · Previous 7 days · Previous 30 days; Rename, Pin, Delete with Undo; titles from the first question; private, 90 days by default (pinned kept). Spec: `mockups/24-assistant-conversation`.
- **Responsive:** Docked split view from 1200 px, beside the rail (an open drawer folds back to the rail while the page needs the room: page ≥ 720 px). 600–1199 px: the block takes the page area in place beside the rail and the header button gives the page back. Under 600 px: the full-screen NavigationBar destination.
- **Keyboard and screen reader:** ⌘J toggles and Esc closes the top layer only (popover → history → pane), focus returns to the opener; streaming answers are `aria-busy`, then one "Answer ready" from a live region outside the pane; the header button name carries its state ("Assistant, answer ready"); composer and history search outlines are `outline` (4.3:1) and turn 2 px `primary` on focus; the resize grip is `outline` at 100 % at rest; the disclaimer is 12 / 16.


### TopAppBar

**Angular Material:** `mat-toolbar` (never `color="primary"`)

- Small 64 px: logo or title (title-large) on the left, up to three trailing icon buttons; on `nav-container`, the same colour as the drawer, separated from it by a 2 px gap of the page `surface` (no outline); the navigation menu button lives at the top of the rail (or of the open drawer), not in the bar (under 600 px it is in the top bar); the search field on it is `surface-container-lowest` in light, `surface-container-high` in dark. Medium / large 112 / 152 px with the title under the icons in headline-medium / -large, collapsing to small on scroll.
- Icon buttons 40 px in a 48 px slot; titles truncate, never wrap in the small bar. Never `primary`: the strong violet is for actions; the avatar uses `secondary-container`.
- App header anatomy (left to right): logo · **page context** right of the logo behind a 1 px `outline-variant` divider: feature name (label-large 600 `on-surface`, e.g. "Sweep · Runs") over a one-line summary (body-small `on-surface-variant`, truncated with an ellipsis before the search field) · a **search-or-ask field centred on the bar** (440 × 44, radius 16; ⌘K focuses it, Enter searches, the **Ask** chip — `ai-container` with the Chatbot mark — sends the text to the assistant and opens the assistant block) · **assistant** icon button with the Chatbot mark (idle; typing dots while an answer is written in the background; tertiary dot when a reply waits) · **notifications**: the Notifications feature mark (violet bell, teal clapper) without its dot, 24 px, with an `error` count badge (1–9, 9+, 99+; none when all read); it rings once when a notification arrives · help · divider · **user chip** (avatar on `secondary-container`, name in title-small, role in body-small, chevron → user menu: account settings, settings, notification preferences, API tokens, theme, sign out). Under 1200 px the name and role hide, only the avatar remains. No environment chip in the header: the environment is a page filter. The drawer no longer carries the assistant entry or the user block — the header owns them; on phones the assistant is a NavigationBar destination and the top bar keeps logo · bell · avatar.
- **No page title, no breadcrumb.** The context block names the page; pages start with their content and keep the full height for it. Page-level actions sit on the first content row (right-aligned, or at the end of the tab row). Going back to a parent is a **Subheader** (below): the back arrow, the page's title, its context and its actions in one row; never a back button on its own row. The search-or-ask field is the only search field on a page, and the only way to ask the assistant from it: pages add neither a second search bar nor Ask buttons in their content.
- **Responsive:** Under 600 px: 56 px, menu · logo mark · feature name (the summary hides) · search icon · bell · avatar (help in the user menu, assistant in the NavigationBar). 600–1199 px: 64 px, the search field flexes (240 / 320 – 440 px) with the Ask chip as an icon, avatar only, help in the user menu under 840 px; the context keeps the feature name only. From 1200 px: 440 px search with the labelled Ask chip and the user chip with name and role.
- **Keyboard and screen reader:** the user chip's name starts with the visible name ("Aurélien Heux, platform admin, account menu") with `aria-haspopup="menu"`; at 320 CSS px the avatar stays and navigation moves to the bottom NavigationBar.

`mat.toolbar-overrides((…))` sets these in **both** files; the CSS variable is `--mat-toolbar-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-background-color` | #EDE4FF / #1D1A27 (`nav-container`) | `.dt-nav` class on the `mat-toolbar` (set in `theme.m2.scss`) | `.dt-nav` → `var(--md-sys-color-nav-container)` (set in `theme.m3.scss`) |
| `container-text-color` | #1C1B1E / #ECE5F8 | `foreground.text` | `--mat-sys-on-surface` |
| `standard-height` | 64px | default 64px | default |
| `mobile-height` | 64px (56px on phones) | default 56px | default |
| `title-text-size` | 22px (title-large) | `headline-6` at 22px | `--mat-sys-title-large-size` |


### Subheader

**Angular Material:** `mat-icon-button` (`arrow_back`) + `h2` + StatusChip + buttons; no toolbar

- The first row of a page under another one (an item, a step, a document, a sub-section): **back** IconButton 40 px named by where it goes ("Back to the Catalog"), optional **lead** (kind tile, avatar), **title** in title-large as an `h2`, optional **status** (one StatusChip), a 1 px `outline-variant` **divider**, the **context** in body-small `on-surface-variant` (at most three plain facts the title does not say: "MCP server by Platform team · v2.3"), **actions** right-aligned (one primary, two more at most).
- One row, min 48 px, with a 1 px `outline-variant` bottom border 8 px under it that separates it from the content; no background; from 600 px it does not wrap (the context truncates first). The arrow's hit area overhangs the content edge by 8 px so its glyph lines up with the text. Never a back chip or a "Back" link on its own row; no breadcrumb; the parent's name goes in the context, not on the arrow.
- Not on top-level pages reached from the navigation: they start with their content.
- **Responsive:** from 600 px, one row with the context beside the title when it fits; under 600 px the title and context wrap beside the arrow and the actions take their own line.
- **Keyboard and screen reader:** the back button comes first in the page's reading order; the title is the page's `h2`.

### Table, Paginator, Sort header, Expansion panel, Stepper, Tree (not yet specified)

Angular Material components AIToolbox has not designed yet; the tokens exist in both generations and the rules below are the starting point.

`mat.table-overrides((…))` sets these in **both** files; the CSS variable is `--mat-table-<token>`. Wrapper: `surface-container-lowest`, 1 px `outline-variant`, 12 px radius (`radius-md`), rows square; row hover = `primary` state layer at 6 % (pressed 10 %), CSS on `.mat-mdc-row` (set in both theme files). Status column = 20 px tile glyph (StateMark C); row loading = 20 px pen orbit; row failed = error tile + Retry; table-level error = StateMark B circle 56–64 px; pending = the pending ring in the same slot.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `background-color` | #FFFFFF / #0F0C19 | `background.card` | `--mat-sys-surface` by default → lowest |
| `header-headline-color` | #48454E / #CAC3DC | `foreground.secondary-text` | `--mat-sys-on-surface-variant` |
| `header-headline-size` | 12px (label-medium, uppercase) | `caption` | `--mat-sys-title-small-size` by default → label-medium |
| `header-container-height` | 48px | default 56px → 48px | default 56px → 48px |
| `row-item-container-height` | 52px (40px dense) | default 52px | default |
| `row-item-outline-color` | #CAC4CF / #494458 | `foreground.divider` | `--mat-sys-outline` by default → outline-variant |
| `row-item-label-text-color` | #1C1B1E / #ECE5F8 | `foreground.text` | `--mat-sys-on-surface` |

`mat.paginator-overrides((…))` sets these in **both** files; the CSS variable is `--mat-paginator-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-background-color` | #FFFFFF / #0F0C19 | `background.card` | `--mat-sys-surface` |
| `container-text-color` | #48454E / #CAC3DC | `foreground.secondary-text` | `--mat-sys-on-surface-variant` |
| `container-size` | 56px | default | default |

`mat.sort-overrides((…))` sets these in **both** files; the CSS variable is `--mat-sort-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `arrow-color` | #48454E / #CAC3DC | `foreground.secondary-text` | `--mat-sys-on-surface-variant` |

`mat.expansion-overrides((…))` sets these in **both** files; the CSS variable is `--mat-expansion-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-background-color` | #FAF4FF / #1D1A27 | `background.card` | `--mat-sys-surface` by default → low |
| `header-text-color` | #1C1B1E / #ECE5F8 | `foreground.text` | `--mat-sys-on-surface` |
| `header-collapsed-state-height` | 48px | default | default |
| `container-shape` | 12px | override | `--mat-sys-corner-medium` (default) |

`mat.stepper-overrides((…))` sets these in **both** files; the CSS variable is `--mat-stepper-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `header-selected-state-icon-background-color` | #39235F / #C4C0FF | `primary` | `--mat-sys-primary` |
| `header-done-state-icon-background-color` | #39235F / #C4C0FF | `primary` | `--mat-sys-primary` |
| `header-error-state-icon-foreground-color` | #93000A / #FFB4AB | `warn` | `--mat-sys-error` |
| `line-color` | #CAC4CF / #494458 | `foreground.divider` | `--mat-sys-outline` by default → outline-variant |

`mat.tree-overrides((…))` sets these in **both** files; the CSS variable is `--mat-tree-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-background-color` | #FDF8FD / #14121E | `background.card` | `--mat-sys-surface` |
| `node-text-color` | #1C1B1E / #ECE5F8 | `foreground.text` | `--mat-sys-on-surface` |
| `node-min-height` | 40px | default 48px → 40px | default 48px → 40px |


---

## Putting it in a project

**Angular Material 21, M2 (`angular/theme.m2.scss`)** — `mat.m2-define-palette` on the seven generated palettes (800 = the Sweep purple #39235F (tone 20) for the light primary, 700 = tone 30 for the light tertiary and error, 200 = tone 80 dark, A200 = tone 80 the dark tertiary, 100 = containers: #DED7EB for the secondary, #DCEAB4 for the tertiary), `mat.m2-define-light-theme` / `-dark-theme` with the typography config, surfaces injected into `background` / `foreground`, then the per-component `mat.*-overrides` blocks above for everything M2 does not model (snackbar, shapes, health chips), then `mat.strong-focus-indicators` for the focus ring. Dark mode by the `html.dark` class.

**Angular Material 22, M3 (`angular/_theme-colors.scss` + `angular/theme.m3.scss`)** — `mat.theme((color: (primary: dt.$primary-palette, tertiary: dt.$tertiary-palette, theme-type: color-scheme), typography: (brand-family, plain-family), density: 0))`, then `mat.theme-overrides` pinning the roles to the AIToolbox hex, then the same `mat.*-overrides` blocks. Dark mode by `color-scheme: light dark` (or the `html.light` / `html.dark` classes).

Both files are compiled in this system against `@angular/material` 21.2.14 and 22.2.3 (Sass 1.80) with no warnings. The migration checklist is in `angular-material.md`.
