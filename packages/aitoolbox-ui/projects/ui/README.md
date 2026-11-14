# @aitoolbox/ui

The AIToolbox design system for Angular: theme files for Angular Material (M2 on 21, M3 on 22), the token set, and the
UI Components the design system specifies, built on Angular Material.

- **Angular / Angular Material:** 21.2 and 22 (compiled with 21.2, so it runs on both).
- **Tokens:** design system 4.5.0, generated from `tokens/tokens.json`.
- **Standalone components, signals, OnPush.** Every colour is a token; light and dark come from `color-scheme`.

## Install

```bash
npm install @aitoolbox/ui @angular/material @angular/cdk
```

The package is internal (`publishConfig.access: restricted`): publish it to your private registry, or install the tarball
(`npm install ./aitoolbox-ui-1.0.0.tgz`).

## 1. Pick a theme file

| Your app | Add to `angular.json` → `styles` |
|---|---|
| Angular Material 22 (or 21) with Material 3 | `node_modules/@aitoolbox/ui/styles/aitoolbox-m3.scss` |
| Angular Material 21 with the M2 theming API (today) | `node_modules/@aitoolbox/ui/styles/aitoolbox-m2.scss` |

Or from your own Sass: `@use '@aitoolbox/ui/styles/aitoolbox-m3';`. Each entry includes the tokens (CSS custom properties
`--md-sys-color-*`, `--ait-type-*`, `--ait-space-*`, …), the BNPP Type font, base rules, layout helpers, the Angular
Material theme with every override of the design system, and the global rules of the components below. Use one file, not both.

Load Open Sans (body and data) in `index.html`:

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap" />
```

**Dark mode.** M3: follows the system; force it with `<html class="dark">` or `<html class="light">`.
M2: add `class="dark"` on `<html>` (the M2 theme does not follow the system).

**Moving from M2 to M3** is a one-line change in `angular.json`: the tokens, the `dt-*` classes and the components are
the same in both files.

## 2. Providers

```ts
export const appConfig: ApplicationConfig = {
  providers: [provideRouter(routes), provideAitIcons()],
};
```

`provideAitIcons()` registers the outlined icon set in the `ait` namespace (`<mat-icon svgIcon="ait:play" />`). The
components register it themselves; the provider is for your own templates. The router is needed by `AitAppShell` for
`route` items.

## 3. Components

| Component | Selector / API | Built on | Design-system rules it enforces |
|---|---|---|---|
| **App shell** | `<ait-app-shell [items] [bottomItems] [version]>` | `mat-sidenav`, `mat-nav-list` | Drawer 300 px from 1200 px (folds to the rail), rail 600–1199 px with the drawer over the page, bottom NavigationBar under 600 px; `nav-container`, 2 px gap under the header, active pill + 3 px primary bar, `aria-current`, Privacy · Cookies · Terms · version footer. |
| **App header** | `<ait-app-header [user] [notificationCount] [assistant] [assistantOpen]>` | `mat-icon-button`, `mat-menu` | Logo · centred search-or-ask · assistant (Chatbot mark, typing dots, waiting dot) · Notifications bell with error badge (1–9, 9+, 99+) · help · user chip and menu; 56 px under 600 px, avatar only under 1200 px; ⌘J toggles the assistant. |
| **Search or ask** | `<ait-search-ask (search) (ask)>` | — | 44 px, radius 16, Ask chip on `ai-container` with the Chatbot mark, ⌘K / Ctrl+K, `role="search"`. |
| **State mark** | `<ait-state-mark state variant size label>` | inline SVG | Badge (A) 24–40, circle (B) 56–96, tile (C) 18–20, tinted; pending ring; never under 18 px; decorative unless labelled. |
| **Status chip** | `<ait-status-chip state>` | `mat-chip` + `dt-chip-*` | `*-container` fill, 18 px tinted tile, radius 4, label-medium; `unknown` = outline dot. |
| **Log level** | `<ait-log-level level>` | — | Only the word is coloured, Open Sans 600. |
| **Pen orbit** | `<ait-pen-orbit size value label>` | skin of `mat-progress-spinner` | 48 / 24 / 18 px; violet arc, teal pen; determinate with `value`. |
| **Guide line** | `<ait-guide-line value label>` | skin of `mat-progress-bar` | Dashed teal guide, violet bar, pen on the edge. |
| **Working dots** | `<ait-working-dots kind="run \| ai">` | — | Green when a command runs, teal when a model thinks. |
| **Constructor progress** | `<ait-constructor-progress value size>` | — | The pen draws the box; the toolbox fills at 100 %. |
| **Brand loader** | `<ait-brand-loader size once label>` | — | App-level waits only; reduced motion shows the finished logo. |
| **Logo / Chatbot mark** | `<ait-logo variant>`, `<ait-chatbot-mark>` | inline SVG | Night box on light, lavender box on dark, from the logo tokens; wordmark never retyped; Chatbot mark ≥ 24 px. |
| **Run button** | `<button mat-flat-button aitRun>` | `mat-flat-button` + `.dt-run` | Night terminal button with the neon play icon. Development builds warn on a second Run on screen or one inside a dialog. |
| **Button roles** | `aitRunText`, `aitTonal`, `aitDanger`, `aitAi` | Material buttons | Row Re-run (tertiary play icon), tonal on M2 and M3, destructive = text in error, AI teal. |
| **AI chip** | `<ait-ai-chip>` | `mat-chip.dt-ai` | `ai-container` + sparkle; AI content only. |
| **Banner** | `<ait-banner state heading dismissible>` | — | State container strip, 28 px badge mark, `role="alert"` for errors; actions marked `aitBannerAction`. |
| **Empty state** | `<ait-empty-state state title cause>` | — | Circle mark 56–96, title, cause, way out; pending ring in the same slot (`aria-busy`). |
| **Snackbar** | `inject(AitSnackBar).open(msg, { state, action })` | `MatSnackBar` | Inverse surface, 24 px badge mark in the other theme's colours, one action, 6 s (10 s with an action), assertive for errors. |
| **Confirm dialog** | `inject(AitConfirm).open({ title, message, confirmLabel, destructive })` | `MatDialog` | 280–560 px, text dismiss, filled confirm or text-in-error when destructive, 32 px warning mark, `alertdialog`. |
| **Dialog title** | `<h2 mat-dialog-title aitDialogTitle state>` | `mat-dialog-title` | 32 px state mark next to the title of a state-driven popin. |
| **Disabled reason** | `<button disabled disabledInteractive aitDisabledReason="…">` | `MatTooltip` | Tooltip E: stays focusable, 500 ms delay, reason as the accessible description. |
| **Window class** | `inject(AitWindowClass)` | CDK `BreakpointObserver` | Material 3 classes (600 / 840 / 1200 / 1600), `navigation()`, `drawerMode()`, `assistantMode()`, `fullScreenDialogs()`. |

Angular Material components that need no wrapper (buttons, form fields, select, chips, tabs, cards, lists, menus,
checkbox, radio, slide toggle, button toggle, table, paginator, sort, expansion, stepper, tree, tooltip, datepicker,
timepicker, bottom sheet, sidenav) are themed by the theme file: use them as usual. For tables, wrap them in
`<div class="ait-table">` (frame, 48 px uppercase header, 52 px rows; `ait-table-dense` for 40 px) and put a
`<ait-state-mark variant="tile">` first in the status column.

### Classes and helpers

- `dt-run`, `dt-run-text`, `dt-tonal`, `dt-danger`, `dt-ai`, `dt-chip-success | warning | error | info`, `dt-nav`, `dt-nav-active`.
- Layout: `ait-page` (page-area container), `ait-grid`, `ait-kpis` (1 / 2 / 4 per row), `ait-split` + `ait-split-main` / `ait-split-side`, `ait-col-p2` / `ait-col-p3`, `ait-reading`, `ait-form`.
- Type: `ait-display-large` … `ait-label-small`, `ait-code`; `ait-data` for identifiers (Open Sans 600); `ait-muted`; `ait-visually-hidden`.
- Sass: `@use '@aitoolbox/ui/styles/breakpoints' as bp;` → `bp.from(expanded)`, `bp.below(large)`, `bp.page-from(720px)`.
- TypeScript: `AIT_COLORS` (light/dark hex for charts and canvas), `AIT_TOKENS_VERSION`.

### Static files

`assets/logos`, `assets/states`, `assets/chatbot` (the design-system SVGs, light and dark), `fonts/BNPPType-Regular.woff2`,
`tokens/tokens.json`, `styles/tokens.css` (plain CSS for non-Angular pages), `styles/mat-sys-bridge.css`.

BNPP Type is a proprietary typeface: keep this package on the internal registry.

## Not in 1.0

- **Assistant pane** (`ait-assistant-pane` with the resize grip, messages, tool trace, approvals, composer, history).
- **Data, status and rich tooltips** (C, D, F, G); plain and disabled-reason tooltips are covered.
- **Side sheet**, **FAB** placement rules, **Carousel** — use the Material components with the theme until then.
- **Table** as a component: the theme and `ait-table` cover the visual rules; row states are composed by the app.
