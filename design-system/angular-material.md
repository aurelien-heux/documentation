# Angular Material · M2 today, M3 next

How the AIToolbox design system maps onto Angular Material, for a codebase that runs the Material 2 theming API on Angular Material 21 today and will move to Material 3 on 22. Everything here is generated from the same palettes and tokens as the rest of the system, so the hex values are identical whichever API you compile with. Files are in `angular/`; the per-component rules with their tokens for both generations are in `component-rules.md`.

## Where Angular Material stands

| Angular Material | Theming | What it means for AIToolbox |
|---|---|---|
| ≤ 16 | Material 2 only: `mat.define-palette`, `mat.define-light-theme`, `mat.define-dark-theme`, `mat.define-typography-config` | `angular/theme.m2.scss` without the `m2-` prefixes (search-replace `mat.m2-` → `mat.`). |
| 17 | Components rebuilt on MDC (token-based, `--mdc-*` / `--mat-*` variables), still M2 theming; 17.2 ships M3 as experimental (`@angular/material-experimental`) | Same file as 16. The MDC rewrite is what makes the `--mdc-*` shape overrides in the file work. |
| 18 | M3 stable (`mat.define-theme`); M2 APIs kept, renamed with an `m2-` prefix (`mat.m2-define-palette`, `mat.m2-define-light-theme`, `mat.$m2-indigo-palette`); `get-color-from-palette` → `get-theme-color` | **`angular/theme.m2.scss` as written** (prefixed). The deprecation warnings are from Angular's own Sass, not from this file. |
| 19 | `mat.theme()` mixin that emits system variables (`--mat-sys-*`), `light-dark()` + `color-scheme` for dark mode, `mat.theme-overrides` and per-component `*-overrides` mixins, `ng generate @angular/material:theme-color` for custom palettes. M2 themes still build; the prebuilt M2 themes are "provided for backwards compatibility and will be removed in a future version". | **`angular/_theme-colors.scss` + `angular/theme.m3.scss`** — the target. The `*-overrides` mixins also work on top of an M2 theme, which is how `theme.m2.scss` sets shapes, the snackbar and the health chips. |
| 20 | Component tokens unified under `--mat-<component>-*` (the `--mdc-*` names are gone) | Anything written against `--mdc-*` variables stops working; use the `*-overrides` mixins — done in `theme.m2.scss`. |
| 21 (Nov 2025) | `utility-classes` mixin renamed `system-classes`, corner `extra-small` renamed `xs`, CDK overlay Sass variables renamed (`$overlay-backdrop-color`); the `mat.m2-*` APIs still ship | **Today's target for `theme.m2.scss`** — compiled here against 21.2.14 with no warning. |
| 22 (Jun 2026) | Typography mixins added; no theming breaking change; `mat.m2-*` still present (22.2) | **Target for `theme.m3.scss`** — compiled here against 22.2.3 with no warning. M2 is not on a cliff, but it is legacy: plan the switch during the 22 line. |

Minimum plan: stay on `theme.m2.scss` through the 21 line, swap the import for `theme.m3.scss` when moving to 22. Both files are compiled as part of this system against the real packages — 21.2.14 and 22.2.3, Sass 1.80 — with no warnings.

## The files

| File | For | Notes |
|---|---|---|
| `angular/theme.m2.scss` | Angular Material 21 (M2 API; compiles on 18–22) | Seven palettes in the M2 hue shape (50–900, A100–A700 + `contrast`), generated from the HCT tones: 800 = the Sweep purple #39235F, tone 20 (the light primary), 600 = tone 40 (the light tertiary), 200 = tone 80 (the dark default), A200 = tone 85 (the neon), 100 = tone 90 (containers). Light and dark themes, AIToolbox typography on the M2 levels, surfaces injected into M2's background/foreground maps, scoped themes for roles M2 has no slot for, and the `*-overrides` mixins (same token names as M3) for shapes, the snackbar and the health chips. |
| `angular/_theme-colors.scss` | Angular Material 22 (19+) | Exactly the shape `ng generate @angular/material:theme-color` writes (`$primary-palette`, `$tertiary-palette`, tones 0–100 with the extra neutral tones), but from the AIToolbox palettes — primary deep violet (seed #1E1B4B), secondary on the same hue, tertiary neon green (seed #00F5A0), night neutrals (seed #0D0B14) — instead of a schematic guess. Plus `$extended` (ai, success, warning). |
| `angular/theme.m3.scss` | Angular Material 22 (19+) | `mat.theme` with those palettes and the type families, then `mat.theme-overrides` pinning every colour role to the design-system token values (Angular would otherwise place light roles at tone 40 and the dark surface at tone 6; AIToolbox uses the Sweep purple #39235F (tone 20) for the light primary and keeps the night surface at tone 6 with its own container steps). Scoped overrides for Run (neon green), AI (teal), health chips, and the shape scale. |
| `angular/mat-sys-bridge.css` | Angular Material 22 (19+) without recompiling | Maps `--md-sys-color-*` from `css/tokens.css` to `--mat-sys-*`, plus the type scale, corners and elevation levels. Redundant with `theme.m3.scss`; useful when tokens must change at runtime or when the Sass theme is owned by another team. |

## Colour roles: token → M2 slot → M3 variable

| AIToolbox token | M2 (`theme.m2.scss`) | M3 (`theme.m3.scss`) |
|---|---|---|
| `primary` / `on-primary` | `primary` palette, hue 800 light / 200 dark; `color="primary"` | `--mat-sys-primary` / `--mat-sys-on-primary` |
| `primary-container` / `on-primary-container` | `primary` palette `lighter` (100) — reached with `mat.get-theme-color($theme, primary, lighter)` | `--mat-sys-primary-container` / `--mat-sys-on-primary-container` |
| `secondary` (from the pale purple #DED7EB) | `accent` palette 700 / 200; `color="accent"` — use it only for the violet *text/icon* role | `--mat-sys-secondary` |
| `secondary-container` (the pale purple #DED7EB: chips, tonal buttons, nav pill, env badges) | `accent` `lighter` (100). M2 has no tonal button: use `mat-flat-button` with `.mat-accent` overridden to the lighter hue, or a stroked button | `--mat-sys-secondary-container`; tonal button = `mat-flat-button` with `mat.button-overrides` or the `tonal` appearance where available |
| `tertiary-container` / `on-tertiary-container` (Run/Deploy/Apply: the Sweep lime, both themes) | `.dt-run` → `mat.button-overrides` + `mat.fab-overrides` with the hex (lime #DCEAB4, label #39235F, no edge); row actions `.dt-run-text` (`primary` label, lime disc behind the icon) | `--mat-sys-tertiary-container` / `--mat-sys-on-tertiary-container`; `.dt-run` / `.dt-run-text` via `mat.button-overrides` |
| `tertiary` (lime palette: running dots, deploy states; olive #404B23 in light) | `$dt-lime` palette, hue 700 in light | `--mat-sys-tertiary` |
| Keyboard focus ring (= `primary`) | `mat.strong-focus-indicators((border-width: 2px))` + `--mat-focus-indicator-border-color` | same mixin, colour `var(--mat-sys-primary)` |
| `error` family | `warn` palette 600 / 200; `color="warn"` | `--mat-sys-error`, `--mat-sys-error-container` |
| `ai` family (teal) | no slot → scoped theme `.dt-ai` | `--md-sys-color-ai*` custom properties + `.dt-ai` overrides |
| `success` / `warning` families | no slot → chip classes `.dt-chip-success` / `.dt-chip-warning` (and your own banners) | same custom properties + the same classes |
| `surface`, `surface-container-*` | injected into `background` (`background`, `card`, `dialog`, `app-bar`) — M2 knows only these four steps | `--mat-sys-surface`, `--mat-sys-surface-container-lowest … highest` |
| `on-surface`, `on-surface-variant`, `outline-variant` | injected into `foreground` (`text`, `secondary-text`, `divider`, `icon`) | `--mat-sys-on-surface`, `--mat-sys-on-surface-variant`, `--mat-sys-outline-variant` |
| `inverse-surface` / `inverse-on-surface` (snackbar) | M2 snackbar hard-codes `#333`; override `--mdc-snackbar-container-color` | `--mat-sys-inverse-surface` / `--mat-sys-inverse-on-surface` (snackbar follows automatically) |

Colours that the Angular theme cannot express (AI teal, success, warning) are the same custom properties in both files, so component code can be written once: `var(--md-sys-color-success-container)` works under M2 and M3.

## Typography

| AIToolbox style | M2 level (`theme.m2.scss`) | M3 (`mat.theme` typography) |
|---|---|---|
| display-large / medium / small | `headline-1` / `headline-2` / `headline-3` | `--mat-sys-display-large` … (brand family) |
| headline-large / medium / small | `headline-4` / `headline-5` / `headline-6` | `--mat-sys-headline-*` |
| title-large | — (M2 has no slot; `headline-6` at 22px if needed) | `--mat-sys-title-large` |
| title-medium / small | `subtitle-1` / `subtitle-2` | `--mat-sys-title-medium` / `-small` |
| body-large / medium / small | `body-1` / `body-2` / `caption` | `--mat-sys-body-*` (plain family) |
| label-large (buttons) | `button` | `--mat-sys-label-large` |
| label-medium / small, code | — (apply `font-family: var(--md-ref-typeface-body); font-weight: 600`) | `--mat-sys-label-medium` / `-small`; code stays a custom class |

Families: `brand-family` = BNPP Type (display, headline, title, label), `plain-family` = Open Sans (body). BNPP Type is one weight (500), so `medium-weight: 500` and the UI never asks for bold; `bold-weight: 600` is Open Sans for data and identifiers. Load the font file from `fonts/BNPPType-Regular.woff2` with the `@font-face` in `css/tokens.css`.

## Component map

Every Angular Material component, the AIToolbox component it implements, and what differs between the two theming generations. "DT rule" is the design-system rule the Angular component must respect.

| Angular Material | AIToolbox | M2 (17–18) | M3 (19+) | DT rule |
|---|---|---|---|---|
| Autocomplete | TextField + Menu | `mat-autocomplete` panel is a menu surface: `background.card` | panel on `--mat-sys-surface-container` | Loading options: 20 px pen-orbit item "Loading…"; failed: 20 px error tile glyph (StateMark C) + Retry item. |
| Badge | Badge | `matBadge` `color="warn"` for counts; `primary` for neutral counts | `matBadge` takes `--mat-badge-*`; keep default = `error` for alerts | Dot badge 6 px, number badge 16 px, error for alerts, primary for neutral counts. |
| Bottom sheet | BottomSheet | `background.dialog` → `surface-container-high`; `mat.bottom-sheet-overrides((container-shape: 16px))` (set in `theme.m2.scss`) | `mat.bottom-sheet-overrides((container-shape: 16px))` | Phone-only; drag handle 32×4 on `outline-variant`. |
| Button | Button (filled, tonal, outlined, text, elevated) | `mat-flat-button` = filled; tonal has no M2 equivalent → `mat-flat-button color="accent"` on the lighter hue, or `mat-stroked-button`; `mat-raised-button` = elevated | `mat-flat-button` (filled), `mat-stroked-button`, `mat-button`, `mat-raised-button`; tonal via `.mat-tonal`/overrides | 40 px, 16 px radius (the system ceiling — never full-round), label-large. One filled lime `.dt-run` per screen. Never a filled destructive button (text button in `error`). |
| Button toggle | SegmentedButton | `mat-button-toggle-group` with `appearance="standard"`; selected = `accent` lighter | tokens follow `secondary-container` for the selected state | Max 5 segments, selected = violet tint + check icon. |
| Card | Card (elevated, filled, outlined) | `mat-card` = elevated (`background.card`); outlined via `appearance="outlined"`; filled has no M2 appearance → class on `surface-container-highest` | `appearance="outlined"` / default; filled through `mat.card-overrides` | 12 px radius, 16 px padding; status rows use StatusChip, never a coloured card border. |
| Checkbox | Checkbox | `mat-checkbox color="primary"` | `--mat-sys-primary` by default | Indeterminate for partial selections in tables; label on the right, 44 px hit area. |
| Chips | Chip (assist, filter, input, suggestion) + StatusChip | `mat-chip-option` selected = `accent` lighter; health chips via `.dt-chip-*` classes; AI chips `.dt-ai` | `mat-chip-set` follows `secondary-container` when selected; `.dt-chip-*` through `mat.chips-overrides` | 32 px, 8 px radius; health chips carry the 18 px tinted tile glyph (StateMark C) as the leading avatar. |
| Core · Option / Optgroup | Menu / List items | `background.card`; selected option = `accent` lighter | `--mat-sys-secondary-container` when selected | Option-level state: 20 px tinted tile glyph (StateMark C), trailing caption says why. Keyboard-active option = focus ring only (no fill); none after a mouse open until a key is pressed. |
| Core · Ripple | state layers | `--dt-state-layer` (primary) in menu, list, option, icon-button, button-toggle overrides + `.mat-mdc-row:hover`; `--mat-ripple-color` primary 10 % (set in `theme.m2.scss`) | `--mat-sys-hover-state-layer-opacity: .06`, pressed `.1`, focus `0`, the same overrides on `--mat-sys-primary` (set in `theme.m3.scss`) | Neutral surfaces: `primary` layer at 6 % hover, 10 % pressed, no focus layer (focus-state-layer opacity 0 everywhere, so a mouse click leaves no tint; keyboard focus = focus ring) — never the grey `on-surface` layer. Coloured components keep their own content colour. |
| Datepicker | DatePicker | calendar on `background.card`; selected day `primary` | selected day `--mat-sys-primary`, today outlined | Week starts Monday; 48 px cells; ISO dates in the field. |
| Dialog | Dialog (+ ComponentsDialog) | `mat-dialog` on `background.dialog` (set to `surface-container-high`); `mat.dialog-overrides((container-shape: 16px))` (set in `theme.m2.scss`) | `mat.dialog-overrides((container-shape: 16px))` | 280–560 px, 24 px padding, headline-small title; confirm = filled primary, dismiss = text; delete = text button in `error`; the lime Run never in dialogs. State-driven popin: 32 px state mark (StateMark A) next to the title. |
| Divider | Divider | `mat-divider` takes `foreground.divider` | `--mat-sys-outline-variant` | 1 px, `outline-variant`; inset 16 px in lists. |
| Expansion panel | — (not in the system yet) | `mat-expansion-panel` on `background.card` | `--mat-sys-surface-container-low` | Proposed: 48 px header, title-medium, chevron trailing; nested panels never deeper than two. |
| Form field + Input | TextField (outlined, filled) | `appearance="outline"` (default DT); `fill` for dense tables; focused = `primary`; error = `warn` | `appearance="outline"`; `mat.form-field-overrides((outlined-container-shape: 4px))` | 56 px, 4 px radius, label floats; helper text body-small; keys/paths/IDs in Open Sans 600. |
| Select | TextField (select) + Menu | panel = menu surface; selected option `accent` lighter | panel on `surface-container`; selected on `secondary-container` | Same as Autocomplete for list-level loading / failed states. |
| Grid list | — (use CSS grid) | — | — | Not used; cards sit in a CSS grid on the 4 px grid. |
| Icon | Iconography | `mat-icon` inherits `currentColor`; `color="primary"` only in app bars | same | Outlined Material Symbols, 24 px (18 in buttons/chips, 22 in app bars); state marks (StateMark) are inline SVGs, not icons. |
| List | List (one-, two-, three-line) | `mat-list` / `mat-nav-list`; active nav item `primary` + `accent` lighter via class | `mat-nav-list` active on `--mat-sys-secondary-container`; `mat.list-overrides((active-indicator-shape: 16px))` in both files | 56/72/88 px rows, 16 px inset divider, leading avatar 40 px. |
| Menu | Menu | `mat-menu` on `background.card`; `--mat-menu-container-shape: 4px` | `mat.menu-overrides((container-shape: 4px))` on `surface-container` | 40 px items, 240 px max width; list-level states as non-selectable items (States rules). |
| Paginator | — (table footer; not in the system yet) | `mat-paginator` on `background.card` | `--mat-sys-surface-container` | Proposed: 56 px, range label body-medium, icon buttons 40 px. |
| Progress bar | ProgressIndicator (linear) | `mat-progress-bar color="primary"`; buffer uses `primary` lighter | track = `--mat-sys-primary-container`, indicator = `primary` | 4 px, full radius; skinned as the guide line (dashed teal track, violet bar, pen on the edge); AI tasks use `.dt-ai`. |
| Progress spinner | ProgressIndicator (circular) + Loader | `mat-progress-spinner color="primary"` | `--mat-sys-primary` | Skinned as the pen orbit: 20 px in tables/menus, 24 px in rows; panel-level pending = the StateMark pending ring (56–64 px); brand loader only at app start. |
| Radio button | RadioButton | `mat-radio-button color="primary"` | `--mat-sys-primary` | Vertical groups, 44 px rows; 2–5 options, else a select. |
| Sidenav | NavigationDrawer | `<mat-sidenav class="dt-nav">` → `nav-container` #F8F1FF / #1D1A27 (set in `theme.m2.scss`); shape `0 16px 16px 0` | `.dt-nav` → `var(--md-sys-color-nav-container)` (set in `theme.m3.scss`) | 360 px, opened on demand from the rail (closed by default: `[opened]="layout.drawerOpen()"`), active item = violet tint at 16 px radius (hover shares the shape), section labels label-medium. |
| Slide toggle | Switch | `mat-slide-toggle color="primary"` (MDC: selected track `primary`) | `--mat-sys-primary` track, `on-primary` handle | 52×32, check icon in the handle when on. |
| Slider | Slider | `mat-slider color="primary"`; discrete with `discrete` + `showTickMarks` | `--mat-sys-primary` | Value label label-medium; ticks every step up to 10 steps. |
| Snackbar | Snackbar | container hard-coded → set `--mdc-snackbar-container-color` to `inverse-surface`, `--mdc-snackbar-supporting-text-color` to `inverse-on-surface`; action `inverse-primary` | follows `--mat-sys-inverse-surface` automatically | 48 px, 4 px radius, one action; 24 px state mark (StateMark A) leading. |
| Sort header | — (table; not in the system yet) | `mat-sort-header` arrow in `foreground.secondary-text` | `--mat-sys-on-surface-variant` | Proposed: arrow 18 px, sorted column label `on-surface`. |
| Stepper | — (not in the system yet) | `mat-stepper` icons on `primary` | `--mat-sys-primary` / `--mat-sys-primary-container` | Proposed: horizontal on desktop, labels title-small, error step = `error` icon. |
| Table | — (Table is the biggest gap in the system) | `mat-table` on `background.card`; header row `surface-container` via class; zebra via `surface-container-low` | `--mat-sys-surface-container*` | 40 px dense rows / 52 px default, header label-medium uppercase on `on-surface-variant`, status column = 20 px tile glyph (StateMark C), row loading = 20 px pen orbit, row failed = error tile + Retry, table-level error = 56–64 px state circle (StateMark B), pending = the pending ring in the same slot. |
| Tabs | Tabs (primary, secondary) | `mat-tab-group color="primary"`; indicator `primary` | indicator `--mat-sys-primary`, label `on-surface-variant` → `on-surface` when active | 48 px, label title-small, indicator 3 px; max 6 tabs, else a nav rail. |
| Timepicker (19+) | TimePicker | — (no M2 component; the DT TimePicker is a custom dial) | `mat-timepicker` on `surface-container-high` | 24 h, 5-minute steps in ops forms. |
| Toolbar | TopAppBar | `mat-toolbar class="dt-nav"` → `nav-container`, like the drawer; never `color="primary"` | `--mat-sys-surface-container` | 64 px, title-large, 22 px icons; the brand violet is for actions, not the bar. |
| Tooltip | Tooltip | `--mdc-plain-tooltip-container-color` = `inverse-surface` | `--mat-sys-inverse-surface` | 24 px plain tooltip, body-small; rich tooltips are a Card. |
| Tree | — (not in the system yet) | `mat-tree` rows 40 px; toggle icon `foreground.icon` | `--mat-sys-on-surface-variant` | Proposed: 40 px rows, 24 px indent per level, same row states as Table. |
| Bottom app bar, Navigation bar, Navigation rail, FAB, Search, Side sheet, Carousel, Segmented button, Status chip, Loader (brand) | BottomAppBar, NavigationBar, NavigationRail, FAB, Search, SideSheet, Carousel, SegmentedButton, StatusChip, Loader | no Angular Material component (FAB: `mat-fab` / `mat-mini-fab`, `color="primary"`, Run entry in lime via `.dt-run`; the rest: `mat-toolbar` / `mat-sidenav` / `mat-button-toggle-group` / `mat-chip` as the base) | FAB: `mat.fab-overrides((container-shape: 16px))`; the rest built from the same bases | Follow the AIToolbox component READMEs; the previews there are the reference. |

### Gaps to close in the design system

Angular Material has components AIToolbox has not specified yet: **Table** (with Paginator and Sort header), **Expansion panel**, **Stepper**, **Tree**. Table is the one IT screens need first; the rules above (row heights, header style, state marks) are the starting point and can become a `Table` component with a preview on request.

## Migration checklist (M2 → M3)

1. Upgrade to Angular Material 22 keeping `theme.m2.scss` (the `m2-` APIs still ship). Nothing visual changes.
2. Replace the import with `theme.m3.scss`; keep `theme.m2.scss` until the diff is reviewed.
3. Diff the two compiled outputs on the four screens that matter (table, form in a popin, assistant panel, empty states): the hex values are the same by construction; what changes is Angular's component anatomy (tonal buttons, chip heights, form-field outline).
4. Replace `color="accent"` with `.dt-*` classes or `--mat-sys-*` variables where it carried a meaning (violet tint, neon green, teal); M3 has no `accent`.
5. The shape, snackbar and chip overrides are already `*-overrides` mixins in both files (the `--mdc-*` names died in v20): copy nothing, delete nothing.
6. Dark mode: switch from the `html.dark` class block to `color-scheme` (the M3 file supports both; pick one).
7. Remove `mat.core()`; M3 needs no global include besides `mat.theme`.
8. Extended colours (`--md-sys-color-ai*`, `success*`, `warning*`) and the `.dt-chip-*` classes need no change — they are the same names in both files.

## Accessibility in the theme files

Both theme files include `mat.strong-focus-indicators((border-style: solid, border-width: 2px))` and set `--mat-focus-indicator-border-color` to `primary`: Material then draws a 2 px ring outside buttons, chips, icon buttons, tabs, list and menu items. Form fields keep their own focus outline (2 px `primary`). The nav list marks the active item with `routerLinkActive="dt-nav-active"` (pill + 3 px `primary` leading bar), and both files stop the spinner and progress-bar animations under `prefers-reduced-motion`. Light `error` and `tertiary` are tone 30 (M2 `warn` default hue 700). Keyboard and screen-reader rules per component are in `component-rules.md`.

