# Component rules & tokens · Angular Material 21 (M2) and 22 (M3)

Every AIToolbox component with its design rules and the Angular Material tokens that implement them, for the two theming generations the product runs: **Material 2 theming on Angular Material 21** (`angular/theme.m2.scss`) and **Material 3 on Angular Material 22** (`angular/_theme-colors.scss` + `angular/theme.m3.scss`). Both files compile on 21.2 and 22.2 without a warning; the hex values are identical by construction.

## How to read this

- **One token vocabulary.** Since v20 every component exposes its styling as `--mat-<component>-<token>` custom properties, and since v19 each component has a `mat.<component>-overrides((token: value))` mixin that writes them. The names are the same under M2 and M3 — only the *defaults* differ: an M2 theme fills them from the `primary` / `accent` / `warn` palettes, `mat.theme` fills them from the `--mat-sys-*` system variables. The token names below are taken from the 22.1 sources; they are the ones you pass to the overrides mixins (without the component prefix).
- **M2 on v21.** The `mat.m2-*` APIs (`m2-define-palette`, `m2-define-light-theme`, `m2-define-typography-config`) are still shipped in 22.2 and compile without deprecation output, so the M2 file is not on a cliff — but the old `--mdc-*` variable names are gone since v20: anything you wrote against `--mdc-filled-button-container-shape` and friends is dead on 21 and must become `mat.button-overrides(...)`. `theme.m2.scss` does that now.
- **M3 on v22.** `mat.theme` + `mat.theme-overrides` pin the roles to the AIToolbox hex (Angular would otherwise put light roles at tone 40 and the dark surface at tone 6). v21 renamed the `utility-classes` mixin to `system-classes` and the `extra-small` corner to `xs`; v22 added typography mixins. Nothing in 21 or 22 changed the component tokens used here.
- **Values** are written light / dark. Extended colours (`ai`, `success`, `warning`) have no Angular slot in either generation: they are the `--md-sys-color-*` custom properties from `css/tokens.css`, used through the `.dt-*` classes.
- **"DS rule"** lines are the design-system rules the Angular component must respect; the component READMEs are the source.

## Foundations: AIToolbox token → M2 slot → M3 variable

| AIToolbox | Value (light / dark) | M2 · v21 | M3 · v22 |
|---|---|---|---|
| `primary` / `on-primary` | #254487 / #B1C5FF · on: #FFFFFF / #042C70 | `primary` palette hue 700 (light) · 200 (dark); `color="primary"` | `--mat-sys-primary` / `--mat-sys-on-primary` (pinned by `theme-overrides`) |
| `primary-container` / `on-primary-container` | #DAE2FF / #254487 · on: #001847 / #DAE2FF | `primary` palette `lighter` (hue 100) | `--mat-sys-primary-container` / `--mat-sys-on-primary-container` |
| `secondary` (violet) | #4D3D75 / #D0BCFE | `accent` palette 700 / 200; `color="accent"` for the violet text/icon role only | `--mat-sys-secondary` |
| `secondary-container` / `on-secondary-container` (violet tint) | #E9DDFF / #4D3D75 · on: #210F47 / #E9DDFF | `accent` `lighter` (hue 100) | `--mat-sys-secondary-container` / `--mat-sys-on-secondary-container` |
| `tertiary` / `on-tertiary` (copper, Run) | #773200 / #FFB68F · on: #FFFFFF / #542100 | no slot → `.dt-run` scoped theme | `--mat-sys-tertiary` / `--mat-sys-on-tertiary`; `.dt-run` via `mat.button-overrides` |
| `tertiary-container` | #FFDBCA / #773200 | `.dt-run` `lighter` | `--mat-sys-tertiary-container` |
| `error` / `on-error` / `error-container` / `on-error-container` | #BA1A1A / #FFB4AB · on: #FFFFFF / #690005 / #FFDAD6 / #93000A · on: #410002 / #FFDAD6 | `warn` palette 600 / 200; `color="warn"` | `--mat-sys-error`, `--mat-sys-on-error`, `--mat-sys-error-container`, `--mat-sys-on-error-container` |
| `ai` / `on-ai` (light teal, both themes) | #80D5D4 / #80D5D4 · on: #003737 / #003737 | no slot → `.dt-ai` scoped theme (teal hue 200) | `--md-sys-color-ai` / `--md-sys-color-on-ai` + `.dt-ai` overrides |
| `ai-container` / `on-ai-container` | #9CF1F0 / #004F50 · on: #002020 / #9CF1F0 | same | `--md-sys-color-ai-container` / `--md-sys-color-on-ai-container` |
| `success`, `warning` families | #1B5F1F / #91D888 · #6A4E00 / #FCBC00 (+ containers) | no slot → `.dt-chip-*` classes, own banners | same custom properties, same classes |
| `surface` | #FBF8FD / #1F1F23 | `background.background` | `--mat-sys-surface` |
| `surface-container-lowest … highest` | #FFFFFF…#D5D4D8 / #17171B…#424245 | M2 knows four steps only: `card` = lowest (light) / low (dark), `dialog` = high, `app-bar` = container | `--mat-sys-surface-container-lowest` … `-highest` |
| `on-surface` / `on-surface-variant` | #1B1B1F / #E9E7EC · on: #44464F / #C5C6D0 | `foreground.text` / `foreground.secondary-text` | `--mat-sys-on-surface` / `--mat-sys-on-surface-variant` |
| `outline` / `outline-variant` | #696A73 / #9C9DA7 · on: #B7B8C2 / #53545D | — / `foreground.divider` | `--mat-sys-outline` / `--mat-sys-outline-variant` |
| `inverse-surface` / `inverse-on-surface` / `inverse-primary` | #303034 / #E4E2E6 · on: #F2F0F4 / #303034 · action: #B1C5FF / #3F5CA1 | `mat.snack-bar-overrides` (M2 hard-codes a dark snackbar) | `--mat-sys-inverse-surface`, `--mat-sys-inverse-on-surface`, `--mat-sys-inverse-primary` |
| Type: display / headline / title / label (BNPP Type 500) | tokens.json type scale | `m2-define-typography-config` levels `headline-1…6`, `subtitle-1/2`, `button` | `brand-family` of `mat.theme` → `--mat-sys-display-*`, `-headline-*`, `-title-*`, `-label-*` |
| Type: body, code (Open Sans 400 / 600) | body-large 16/24 · medium 14/20 · small 12/16; code 13/20 at 600 | `body-1`, `body-2`, `caption`; code = custom class | `plain-family` → `--mat-sys-body-*`; code = custom class |
| Shape: `radius-xs/sm/md/lg/xl/full` | 4 / 8 / 12 / 16 / 28 / 9999 px | `*-overrides` shape tokens (same as M3) | `--mat-sys-corner-extra-small` (4), `-small` (8), `-medium` (12), `-large` (16), `-extra-large` (28), `-full`; per-component shape tokens pinned |
| Elevation 1–5 | tokens.json shadows | `mat.core()` elevation classes | `--mat-sys-level1` … `--mat-sys-level5` |

Dark mode: M2 file = `html.dark` block (`mat.all-component-colors($dt-dark)`); M3 file = `color-scheme: light dark` with `light-dark()` values, or the `html.light` / `html.dark` classes.

---

## Components


### Badge

**Angular Material:** `matBadge`

- Small = 6 px dot, no text; large = 16 px high, label-small, min-width 16 px, "999+" past three digits.
- Always `error` on `on-error`: a badge is an alert, never a brand colour. Top-right of the icon; in a navigation item on the icon, not the label.

`mat.badge-overrides((…))` sets these in **both** files; the CSS variable is `--mat-badge-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `background-color` | #BA1A1A / #FFB4AB | `matBadgeColor="warn"` (default `primary` → set warn) | `--mat-sys-error` by default |
| `text-color` | #FFFFFF / #690005 | from the `warn` palette contrast | `--mat-sys-on-error` |
| `small-size-container-size` | 6px | v21 default 6px | same |
| `container-size` | 16px | `matBadgeSize="medium"` (16px) | same |
| `text-size` | 11px (label-small) | typography level `caption` | `--mat-sys-label-small-size` |


### BottomAppBar

**Angular Material:** `mat-toolbar` at the bottom (no dedicated component) + `mat-fab`

- Phone-only, 80 px, on `surface-container`; up to four icon buttons left, a FAB (no shadow here) right.
- Detail screens where the primary action and a few tools belong at the thumb; never together with a NavigationBar.

`mat.toolbar-overrides((…))` sets these in **both** files; the CSS variable is `--mat-toolbar-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-background-color` | #E9E7EC / #303034 | `background.app-bar` (injected as surface-container) | `--mat-sys-surface-container` via overrides (Angular default is `surface`) |
| `container-text-color` | #1B1B1F / #E9E7EC | `foreground.text` | `--mat-sys-on-surface` |
| `standard-height` | 80px for this bar (64px for the TopAppBar) | density 0 → 64px; set 80px on the bar | same |

FAB inside the bar: `mat.fab-overrides((container-elevation-shadow: none))` scoped to the bar.

### BottomSheet

**Angular Material:** `MatBottomSheet`

- `surface-container-low`, radius-xl (28 px) top corners, 32×4 px drag handle in `outline`.
- Modal (scrim) for a short list of actions on one item; standard (no scrim) for persistent content. Tablet/desktop → SideSheet or Dialog.

`mat.bottom-sheet-overrides((…))` sets these in **both** files; the CSS variable is `--mat-bottom-sheet-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-background-color` | #F5F3F7 / #27282B | `background.dialog` (surface-container-high) → override to low | `--mat-sys-surface-container-low` (Angular default) |
| `container-text-color` | #1B1B1F / #E9E7EC | `foreground.text` | `--mat-sys-on-surface` |
| `container-shape` | 28px 28px 0 0 | override | `--mat-sys-corner-extra-large` top |


### Button

**Angular Material:** `mat-button` (text), `mat-flat-button` (filled; tonal with the `tonal` appearance / `mat-tonal-button` in 21+), `mat-stroked-button` (outlined), `mat-raised-button` (elevated = "protected")

- 40 px, full-round, label-large; horizontal padding 24 px (16 px with a leading icon). Icon-only buttons are 40 px circles with an `aria-label`.
- Filled `primary` = the one decision on a screen; tonal `secondary-container` beside it; elevated on tinted grounds (elevation-1); outlined / text = low emphasis, text is the dialog dismiss.
- Run `.dt-run` (copper `tertiary`): the single action that starts work, leading play icon, at most one per screen, never in a dialog.
- Destructive = text button in `error`, never a filled red. Disabled = on-surface 12 % fill / 38 % text.

`mat.button-overrides((…))` sets these in **both** files; the CSS variable is `--mat-button-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `filled-container-color` | #254487 / #B1C5FF | `primary` palette default hue | `--mat-sys-primary` |
| `filled-label-text-color` | #FFFFFF / #042C70 | palette contrast | `--mat-sys-on-primary` |
| `tonal-container-color` | #E9DDFF / #4D3D75 | `accent` lighter (M2 tonal = `mat-flat-button color="accent"` on the lighter hue, or the tonal appearance on 21) | `--mat-sys-secondary-container` |
| `tonal-label-text-color` | #210F47 / #E9DDFF | contrast of the lighter hue | `--mat-sys-on-secondary-container` |
| `protected-container-color` | #FFFFFF / #17171B | `background.card` | `--mat-sys-surface` by default → surface-container-lowest |
| `outlined-outline-color` | #696A73 / #9C9DA7 | `foreground.divider` → set `outline` | `--mat-sys-outline` |
| `text-label-text-color` | #254487 / #B1C5FF | `primary` | `--mat-sys-primary` |
| `filled-container-shape` | 9999px (`radius-full`) | `mat.button-overrides` (also outlined / text / protected / tonal shapes) | `--mat-sys-corner-full` (default) |
| `filled-container-height` | 40px | density 0 → 40px | 40px |
| `filled-horizontal-padding` | 24px | default 24px (v21: 24px; text buttons 12px) | default 24px |
| `filled-label-text-size` | 14px (label-large) | typography level `button` | `--mat-sys-label-large-size` |

`.dt-run`: `filled-container-color: tertiary`, `filled-label-text-color: on-tertiary`, `filled-state-layer-color: on-tertiary` (M3) · scoped `mat.button-color($dt-run-light)` theme on the copper palette (M2). Destructive text button: `text-label-text-color: error` on a `.dt-danger` class in both.

### Card

**Angular Material:** `mat-card` with `appearance="raised"` (elevated), `"filled"`, `"outlined"` (21+: all three appearances exist)

- radius-md (12 px), 16 px padding, title-medium heading.
- Elevated = `surface-container-lowest` + elevation-1 (the default for a service or tool card with actions); filled = `surface-container-high`, no shadow (dense lists, grids); outlined = `surface` + `outline-variant` border.
- Actions in a bottom flex row: text buttons left, one filled right. Status in a card header is a StatusChip, never a coloured title.

`mat.card-overrides((…))` sets these in **both** files; the CSS variable is `--mat-card-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `elevated-container-color` | #FFFFFF / #17171B | `background.card` | `--mat-sys-surface-container-low` by default → override to lowest |
| `filled-container-color` | #DEDCE0 / #39393C | override (M2 has no filled default) | `--mat-sys-surface-container-highest` by default → override to high |
| `outlined-container-color` | #FBF8FD / #1F1F23 | `background.card` → override to surface | `--mat-sys-surface` |
| `outlined-outline-color` | #B7B8C2 / #53545D | `foreground.divider` | `--mat-sys-outline-variant` |
| `elevated-container-shape` | 12px (`radius-md`) | override (also filled / outlined) | `--mat-sys-corner-medium` |
| `elevated-container-elevation` | elevation-1 | level 1 | `--mat-sys-level1` |
| `title-text-size` | 16px (title-medium) | `subtitle-1` | `--mat-sys-title-medium-size` |


### Carousel

**Angular Material:** no Angular Material component — CDK scrolling (`cdk-virtual-scroll` / `cdkScrollable`) with the AIToolbox markup

- Multi-browse layout: one large item, one medium, small items at the edge, 8 px gaps, radius-xl.
- Items are `*-container` tones or images; title bottom-left in title-medium. For equal items use List or a grid of Cards.

Tokens: none of Angular's; use `--md-sys-color-*-container`, `--md-sys-shape-corner-extra-large` from `css/tokens.css`.

### Checkbox

**Angular Material:** `mat-checkbox`

- 18 px box, radius 2 px, inside a 44–48 px touch target, 12 px gap to the label.
- Unchecked: 2 px `on-surface-variant` border; checked / indeterminate: `primary` fill with an `on-primary` mark; error: `error` fill; disabled: on-surface 38 %.
- Independent options and multi-select lists; a single on/off setting is a Switch.

`mat.checkbox-overrides((…))` sets these in **both** files; the CSS variable is `--mat-checkbox-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `selected-icon-color` | #254487 / #B1C5FF | `color="primary"` (set as default) | `--mat-sys-primary` |
| `selected-checkmark-color` | #FFFFFF / #042C70 | palette contrast | `--mat-sys-on-primary` |
| `unselected-icon-color` | #44464F / #C5C6D0 | `foreground.secondary-text` | `--mat-sys-on-surface-variant` |
| `label-text-color` | #1B1B1F / #E9E7EC | `foreground.text` | `--mat-sys-on-surface` |
| `touch-target-size` | 48px | default | default |

Error state: `mat-checkbox` has no error appearance — add `.dt-error { @include mat.checkbox-overrides((selected-icon-color: error, unselected-icon-color: error)); }`.

### Chip

**Angular Material:** `mat-chip-set` / `mat-chip-option` (filter), `mat-chip-row` (input), `mat-chip` (assist / suggestion)

- 32 px, radius-sm (8 px), label-large at 500; wrapping row with 8 px gaps.
- Assist / filter unselected: outlined `outline`, text on-surface. Filter selected: `secondary-container` fill with a leading check. Input: outlined with a trailing close, for applied filters and tags like `env:prod`.
- AI chip `.dt-ai`: `ai-container` fill with the sparkle icon — only AI features. Health status is not a chip: see StatusChip.

`mat.chips-overrides((…))` sets these in **both** files; the CSS variable is `--mat-chip-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-height` | 32px | default 32px | default |
| `container-shape-radius` | 8px (`radius-sm`) | `mat.chips-overrides` | `--mat-sys-corner-small` |
| `outline-color` | #696A73 / #9C9DA7 | `foreground.divider` → set `outline` | `--mat-sys-outline` |
| `label-text-color` | #1B1B1F / #E9E7EC | `foreground.text` | `--mat-sys-on-surface-variant` by default → override to on-surface |
| `elevated-selected-container-color` | #E9DDFF / #4D3D75 | `accent` lighter (selected `mat-chip-option` uses the `accent` palette with `color="accent"`) | `--mat-sys-secondary-container` |
| `selected-label-text-color` | #210F47 / #E9DDFF | contrast | `--mat-sys-on-secondary-container` |
| `with-avatar-avatar-size` | 18px (tile glyph of StateMark C in status chips) | default 24px → 18px | same |
| `label-text-size` | 14px (label-large) | `button` level | `--mat-sys-label-large-size` |

`.dt-ai`: `elevated-container-color: ai-container`, `label-text-color: on-ai-container`. Health chips (StatusChip) use `.dt-chip-success | warning | error | info` with `elevated-container-color` / `label-text-color` on the state containers — the same mixin in both files.

### DatePicker

**Angular Material:** `mat-datepicker` (+ `mat-date-range-picker`)

- Modal picker 328 px, radius-xl, `surface-container-high`, elevation-3. Header: label-medium supporting text, selected date in headline-large, edit icon to switch to input.
- 40 px day cells; today outlined in `primary`, selection filled `primary`; text buttons Cancel / OK. Ranges: full-screen range picker; dense forms: docked picker. Week starts Monday, ISO dates in the field.

`mat.datepicker-overrides((…))` sets these in **both** files; the CSS variable is `--mat-datepicker-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `calendar-container-background-color` | #DEDCE0 / #39393C | `background.card` → override | `--mat-sys-surface-container-high` |
| `calendar-container-shape` | 28px (`radius-xl`) | override | `--mat-sys-corner-large` by default → 28px |
| `calendar-date-selected-state-background-color` | #254487 / #B1C5FF | `primary` | `--mat-sys-primary` |
| `calendar-date-selected-state-text-color` | #FFFFFF / #042C70 | contrast | `--mat-sys-on-primary` |
| `calendar-date-today-outline-color` | #254487 / #B1C5FF | `primary` | `--mat-sys-primary` |
| `calendar-date-in-range-state-background-color` | #DAE2FF / #254487 | `primary` lighter | `--mat-sys-primary-container` |
| `toggle-active-state-icon-color` | #254487 / #B1C5FF | `primary` | `--mat-sys-primary` |


### Dialog

**Angular Material:** `MatDialog` (`mat-dialog-title`, `mat-dialog-content`, `mat-dialog-actions`)

- 280–560 px, radius-xl (28 px), `surface-container-high`, elevation-3, 24 px padding, scrim at 32 %.
- Title headline-small; one line of body-medium supporting text on `on-surface-variant`. Fields: TextField with the label background on the dialog colour; 24 px between rows.
- Actions right-aligned: text dismiss + one filled `primary` confirm. Never copper, never a filled destructive button (delete = text in `error`). Focus to the first field, Esc = Cancel; more than ~6 fields → full-screen or page.
- State-driven popin: 32 px StateMark A next to the title.

`mat.dialog-overrides((…))` sets these in **both** files; the CSS variable is `--mat-dialog-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-color` | #DEDCE0 / #39393C | `background.dialog` (injected) | `--mat-sys-surface-container-high` (default) |
| `container-shape` | 28px | `mat.dialog-overrides` | `--mat-sys-corner-extra-large` (default) |
| `container-max-width` | 560px | default 560px | default |
| `container-min-width` | 280px | default 280px | default |
| `subhead-size` | 24px (headline-small) | `headline-6` | `--mat-sys-headline-small-size` |
| `supporting-text-color` | #44464F / #C5C6D0 | `foreground.secondary-text` | `--mat-sys-on-surface-variant` |
| `content-padding` | 24px | default 20px 24px → 24px | default 20px 24px → 24px |

Scrim: `cdk-overlay-dark-backdrop` → `$overlay-backdrop-color` (v21 rename) = `scrim` at 32 %.

### Divider

**Angular Material:** `mat-divider` (`inset`, `vertical`)

- 1 px in `outline-variant`; full-width between sections, inset 16 px between list items with a leading element, vertical between side-by-side controls.
- Prefer spacing or a container change over a divider; use them where items would otherwise merge (dense lists, tables).

`mat.divider-overrides((…))` sets these in **both** files; the CSS variable is `--mat-divider-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `color` | #B7B8C2 / #53545D | `foreground.divider` | `--mat-sys-outline-variant` |
| `width` | 1px | default | default |


### FAB

**Angular Material:** `mat-fab`, `mat-mini-fab`, `mat-fab extended`

- Small 40 px radius-md · default 56 px radius-lg · large 96 px radius-xl · extended 56 px with a label.
- Fill `primary-container` with `on-primary-container` content, elevation-3; the small copper FAB (`tertiary-container`) only as a "run" entry point.
- One per screen, bottom-right, 16 px from the edges; lowers to elevation-1 when a dialog opens.

`mat.fab-overrides((…))` sets these in **both** files; the CSS variable is `--mat-fab-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-color` | #DAE2FF / #254487 | `primary` lighter (M2 default is `primary` → set `color="primary"` + override) | `--mat-sys-primary-container` (default) |
| `foreground-color` | #001847 / #DAE2FF | contrast | `--mat-sys-on-primary-container` |
| `container-shape` | 16px (`radius-lg`) | override | `--mat-sys-corner-large` (default) |
| `small-container-color` | #FFDBCA / #773200 (run entry) / primary-container otherwise | `.dt-run` theme on `mat-mini-fab` | `.dt-run` via `mat.fab-overrides` |
| `small-container-shape` | 12px (`radius-md`) | override | `--mat-sys-corner-medium` (default) |
| `extended-container-height` | 56px | default | default |


### IconButton

**Angular Material:** `mat-icon-button` (standard); filled / tonal / outlined via `.dt-icon-filled | -tonal | -outlined` classes (Angular has one appearance)

- 40 px circle, 24 px icon; standard = no fill `on-surface-variant`, filled = `primary`, tonal = `secondary-container`, outlined = `outline` border.
- Toggle buttons use `aria-pressed`; the selected standard state takes `primary`. Always an `aria-label`; 48 px touch target (4 px margin in a dense row).

`mat.icon-button-overrides((…))` sets these in **both** files; the CSS variable is `--mat-icon-button-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `icon-color` | #44464F / #C5C6D0 | `foreground.icon` | `--mat-sys-on-surface-variant` |
| `icon-size` | 24px | default | default |
| `state-layer-size` | 40px | default 40px | default |
| `touch-target-size` | 48px | default | default |
| `container-shape` | 9999px | default full | `--mat-sys-corner-full` |

Filled / tonal / outlined variants are plain CSS on the class (`background: var(--md-sys-color-primary)` etc.) — Angular's icon button has no container-color token.

### List

**Angular Material:** `mat-list`, `mat-nav-list`, `mat-selection-list`, `mat-list-item` (`lines="1|2|3"`)

- Rows 56 / 72 / 88 px (one / two / three lines): leading avatar or icon, title-medium headline, body-medium supporting text in `on-surface-variant`, trailing meta or icon.
- Selected row `surface-container` (`secondary-container` in a navigation list). Inset dividers when rows have a leading element; 16 px row padding; the whole row is the hit target.

`mat.list-overrides((…))` sets these in **both** files; the CSS variable is `--mat-list-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `list-item-label-text-color` | #1B1B1F / #E9E7EC | `foreground.text` | `--mat-sys-on-surface` |
| `list-item-supporting-text-color` | #44464F / #C5C6D0 | `foreground.secondary-text` | `--mat-sys-on-surface-variant` |
| `list-item-one-line-container-height` | 56px | default 48px → 56px | default 56px |
| `list-item-two-line-container-height` | 72px | default 64px → 72px | default 72px |
| `list-item-three-line-container-height` | 88px | default 88px | default |
| `active-indicator-color` | #E9DDFF / #4D3D75 | `accent` lighter (nav list active item via class) | `--mat-sys-secondary-container` |
| `active-indicator-shape` | 9999px | override | `--mat-sys-corner-full` |
| `list-item-selected-container-color` | #E9E7EC / #303034 | override | no default → surface-container |
| `list-item-leading-avatar-size` | 40px | default | default |


### Loader (brand)

**Angular Material:** no Angular Material component — inline SVG from `loading-states/` (`brand-loader.svg`, `ait-loader` classes) + `css/loading-states.css`

- Constructor: the AI badge arrives alone, construction guides appear, the teal pen draws the toolbox and goes home, the toolbox fills; 4.4 s loop, `ait-once` for a splash. 96 px splash / workspace boot, 40 px minimum, app-level waits only.
- Colours from the tokens: `primary`, `on-primary`, `tertiary-container`, `ai`, `on-ai` — the markup is theme-agnostic.

Tokens: `--md-sys-color-primary`, `-on-primary`, `-tertiary-container`, `-ai`, `-on-ai` through `.ait-loader .ait-*` in `loading-states.css` (identical under M2 and M3).

### Menu

**Angular Material:** `mat-menu` / `mat-menu-item`

- 48 px items on `surface-container`, radius-xs, elevation-2, 8 px vertical padding, 112–280 px wide.
- Items: 20 px leading icon, body-medium label, optional trailing shortcut in label-medium `on-surface-variant`; hover / focus `surface-container-highest`.
- Destructive items in `error`, last, after a divider. List-level states as non-selectable items with the 20 px tile glyph (StateMark C) + Retry.

`mat.menu-overrides((…))` sets these in **both** files; the CSS variable is `--mat-menu-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-color` | #E9E7EC / #303034 | `background.card` → override | `--mat-sys-surface-container` (default) |
| `container-shape` | 4px (`radius-xs`) | `mat.menu-overrides` | `--mat-sys-corner-extra-small` (default) |
| `item-label-text-color` | #1B1B1F / #E9E7EC | `foreground.text` | `--mat-sys-on-surface` |
| `item-icon-color` | #44464F / #C5C6D0 | `foreground.icon` | `--mat-sys-on-surface-variant` |
| `item-icon-size` | 20px | default 24px → 20px | default 24px → 20px |
| `item-hover-state-layer-color` | on-surface at 8 % (reads as surface-container-highest) | default | default |
| `divider-color` | #B7B8C2 / #53545D | `foreground.divider` | `--mat-sys-outline-variant` |


### NavigationBar

**Angular Material:** no Angular Material component — `mat-toolbar` + `mat-button`s (or `mat-tab-nav-bar`) with the AIToolbox markup

- Phone bottom navigation, 80 px, 3–5 destinations on `surface-container`. Active: 64×32 px `secondary-container` pill behind the icon, label `on-surface` at 600; inactive `on-surface-variant`.
- Badges on the icon. On tablet / desktop the destinations move to the NavigationRail.

Tokens: `toolbar-container-background-color: surface-container`; the pill is plain CSS on `--md-sys-color-secondary-container` / `-on-secondary-container`.

### NavigationDrawer

**Angular Material:** `mat-sidenav` (`mode="over"` on phones, `"side"` on desktop) + `mat-nav-list`

- 360 px (300 shown) on `surface-container-low`, 12 px inset, 56 px full-round items. Active `secondary-container` + `on-secondary-container`; others `on-surface-variant`; trailing counts label-medium.
- Section headers label-medium `on-surface-variant` after an inset divider.

`mat.sidenav-overrides((…))` sets these in **both** files; the CSS variable is `--mat-sidenav-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-background-color` | #F5F3F7 / #27282B | `background.card` → override | `--mat-sys-surface` by default → override to low |
| `container-text-color` | #44464F / #C5C6D0 | `foreground.secondary-text` | `--mat-sys-on-surface-variant` |
| `container-shape` | 0 16px 16px 0 | override | `--mat-sys-corner-large` on the open side (default) |
| `container-width` | 360px | default 360px | default |
| `scrim-color` | scrim at 32 % | default | default |

Items: `mat.list-overrides((active-indicator-color: secondary-container, active-indicator-shape: 9999px, list-item-one-line-container-height: 56px))`.

### NavigationRail

**Angular Material:** no Angular Material component — vertical `mat-nav-list` in an 80 px aside

- 80 px wide on `surface` with an `outline-variant` edge, never a container tone; menu button, optional FAB, 3–7 destinations. Active 56×32 px `secondary-container` pill, labels label-medium under the icon. Expands into a NavigationDrawer when there is room.

Tokens: list overrides as for the drawer (`active-indicator-color: secondary-container`); edge = `--md-sys-color-outline-variant`.

### ProgressIndicator

**Angular Material:** `mat-progress-spinner` (pen orbit) and `mat-progress-bar` (guide line) keep their slots and APIs — the AIToolbox skins are the inline SVGs from `loading-states/` with `loading-states.css`, or a thin wrapper around the Material components bound to `value`

- Pen orbit (circular): navy arc with the teal pen at its head on a `primary-container` track; 48 px content, 24 px inline, 18 px in a button.
- Guide line (linear, 4 px): dashed teal guide as the track, navy bar with the pen on its edge; determinate = navy to the value. Indeterminate at the top of the app bar during navigation.
- Constructor determinate (`brand-progress.svg`, `--p`): long operations with a known value, 64–96 px. Working dots: copper = a command runs, teal = a model thinks.

`mat.progress-bar-overrides((…))` sets these in **both** files; the CSS variable is `--mat-progress-bar-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `active-indicator-color` | #254487 / #B1C5FF | `color="primary"` | `--mat-sys-primary` |
| `track-color` | #DAE2FF / #254487 (when the Material bar is kept) | `primary` lighter | `--mat-sys-surface-variant` by default → primary-container |
| `track-height` | 4px | default | default |
| `active-indicator-height` | 4px | default | default |

`mat.progress-spinner-overrides((…))` sets these in **both** files; the CSS variable is `--mat-progress-spinner-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `active-indicator-color` | #254487 / #B1C5FF | `color="primary"` | `--mat-sys-primary` |
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
| `selected-icon-color` | #254487 / #B1C5FF | `color="primary"` (set as default; M2 default is `accent`) | `--mat-sys-primary` |
| `unselected-icon-color` | #44464F / #C5C6D0 | `foreground.secondary-text` | `--mat-sys-on-surface-variant` |
| `label-text-color` | #1B1B1F / #E9E7EC | `foreground.text` | `--mat-sys-on-surface` |
| `touch-target-size` | 48px | default | default |


### Search

**Angular Material:** no Angular Material component — `mat-form-field appearance="fill"` styled as the bar + `mat-autocomplete` as the view

- Search bar 56 px, full-round, `surface-container-high`, leading menu/back icon, placeholder `on-surface-variant`, trailing avatar or action.
- Search view below, radius-xl, same container tone; rows are 48 px list items with a type hint in label-medium; results grouped by kind, identifiers in Open Sans 600.

`mat.autocomplete-overrides((…))` sets these in **both** files; the CSS variable is `--mat-autocomplete-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `background-color` | #DEDCE0 / #39393C | `background.card` → override | `--mat-sys-surface-container` by default → high |
| `container-shape` | 28px | override | `--mat-sys-corner-extra-small` by default → 28px |

Bar: `mat.form-field-overrides((filled-container-color: surface-container-high, filled-container-shape: 9999px, filled-active-indicator-height: 0))`.

### SegmentedButton

**Angular Material:** `mat-button-toggle-group` (`appearance="standard"`; `hideSingleSelectionIndicator=false` for the leading check)

- 2–5 options, 40 px, full-round outer corners, `outline` dividers. Selected `secondary-container` with a leading check; others transparent, `on-surface` text.
- Views of the same data (Day / Week / Month, List / Grid); navigation → Tabs, filters → chips.

`mat.button-toggle-overrides((…))` sets these in **both** files; the CSS variable is `--mat-button-toggle-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `selected-state-background-color` | #E9DDFF / #4D3D75 | `accent` lighter | `--mat-sys-secondary-container` |
| `selected-state-text-color` | #210F47 / #E9DDFF | contrast | `--mat-sys-on-secondary-container` |
| `text-color` | #1B1B1F / #E9E7EC | `foreground.text` | `--mat-sys-on-surface` |
| `divider-color` | #696A73 / #9C9DA7 | `foreground.divider` → `outline` | `--mat-sys-outline` |
| `shape` | 9999px | override | `--mat-sys-corner-full` (default) |
| `height` | 40px | default 40px | default |


### SideSheet

**Angular Material:** `mat-sidenav position="end"` (`mode="side"` standard, `"over"` modal) or `mat-drawer`

- 256–400 px docked right: `surface` + `outline-variant` divider (standard) or `surface-container-low` + scrim (modal). Header title-large + close icon button; actions pinned to the bottom above a divider.
- Standard pushes content, modal overlays it; on phones it becomes a BottomSheet.

`mat.sidenav-overrides((…))` sets these in **both** files; the CSS variable is `--mat-sidenav-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-background-color` | #FBF8FD / #1F1F23 (standard) · #F5F3F7 / #27282B (modal) | `background.background` / `card` | `--mat-sys-surface` / `-surface-container-low` |
| `container-divider-color` | #B7B8C2 / #53545D | `foreground.divider` | `--mat-sys-outline-variant` |
| `container-shape` | 0 (docked edge) | override | `--mat-sys-corner-large` by default → 0 on the docked edge |


### Slider

**Angular Material:** `mat-slider` (`discrete`, `showTickMarks`; two `matSliderThumb`s for a range)

- 4 px track `primary-container`, active segment `primary`, 4×24 px handle, value label `inverse-surface` while dragging; continuous or discrete, range with two handles.
- Values with a meaningful visual range (CPU limit, replicas 1–20); exact numbers pair it with a text field.

`mat.slider-overrides((…))` sets these in **both** files; the CSS variable is `--mat-slider-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `active-track-color` | #254487 / #B1C5FF | `color="primary"` | `--mat-sys-primary` |
| `inactive-track-color` | #DAE2FF / #254487 | `primary` lighter | `--mat-sys-primary-container` by default → keep |
| `handle-color` | #254487 / #B1C5FF | `primary` | `--mat-sys-primary` |
| `handle-width` | 4px | default 20px → 4px | default 20px → 4px |
| `handle-height` | 24px | default 20px → 24px | default 20px → 24px |
| `label-container-color` | #303034 / #E4E2E6 | override | `--mat-sys-primary` by default → inverse-surface |
| `active-track-height` | 4px | default 6px → 4px | default 6px → 4px |
| `inactive-track-height` | 4px | default 4px | default |


### Snackbar

**Angular Material:** `MatSnackBar` (custom component for the leading state mark)

- `inverse-surface` ground, `inverse-on-surface` text, one optional action in `inverse-primary`, optional close; 48 px single line, 68 px two lines; radius-xs; elevation-3; 4–10 s.
- Leading 24 px StateMark A (badge in `inverse-primary` on the inverse surface). Never for errors that need a decision (dialog); never stacked.

`mat.snack-bar-overrides((…))` sets these in **both** files; the CSS variable is `--mat-snack-bar-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-color` | #303034 / #E4E2E6 | `mat.snack-bar-overrides` (M2 hard-codes a dark container) | `--mat-sys-inverse-surface` (default) |
| `supporting-text-color` | #F2F0F4 / #303034 | same override | `--mat-sys-inverse-on-surface` |
| `button-color` | #B1C5FF / #3F5CA1 | same override | `--mat-sys-inverse-primary` |
| `container-shape` | 4px | override | `--mat-sys-corner-extra-small` (default) |
| `supporting-text-size` | 14px (body-medium) | `body-2` | `--mat-sys-body-medium-size` |


### StateMark

**Angular Material:** inline SVG from `assets/States` (never `mat-icon`); hosts: `matChipAvatar` (tile, 18 px), the leading element of a snackbar component (badge, 24 px), first element of a table status column (tile, 20 px), empty-state templates (circle, 56–96 px)

- One construction: the toolbox never changes (navy with its `>_`), the corner badge carries the state role and symbol (✓ success · i info = `primary` · ! warning · ✕ error).
- A · alone 24–40 px (snackbars, popin headers, inline alerts) · B · circle 56–96 px (empty states, table-/panel-/popin-level errors: disc in the state role, dark on light and light on dark, toolbox reversed, badge in the state container) · C · tile glyph 18–20 px (chips, cells, options).
- Loading is not a state: the slot shows the pen-orbit ring around the plain mark and takes the state in place when the request resolves (warning after a timeout, error with Retry). No entrance animation; never below 18 px; never recoloured.

Tokens: `--md-sys-color-success | warning | error | primary` and their `on-*`, `*-container`, `on-*-container` for the badge, disc and tile; `--md-sys-color-primary` / `-on-primary` / `-tertiary-container` for the toolbox; `-ai` for the pending pen. Identical under M2 and M3.

### StatusChip

**Angular Material:** `mat-chip` with `class="dt-chip-success | dt-chip-warning | dt-chip-error | dt-chip-info"` + the tile glyph in `matChipAvatar`; log levels are plain `span`s

- Label-medium, radius-xs, `*-container` fill with `on-*-container` text, led by the 18 px tinted tile glyph (StateMark C); a 6 px `outline` dot only for unknown on `surface-container-highest`.
- Log levels colour only the level word, Open Sans 600: INFO `success`, WARN `warning`, ERR `error`. Never `primary` / `secondary` / `tertiary` for a status, never a status colour for a button.

`mat.chips-overrides((…))` sets these in **both** files; the CSS variable is `--mat-chip-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `elevated-container-color` | state container: #ACF4A2 / #0B5314 · #FFDEA0 / #5C4300 · #FFDAD6 / #93000A · #DAE2FF / #254487 | `.dt-chip-*` → `mat.chips-overrides` (same as M3) | `.dt-chip-*` → `mat.chips-overrides` |
| `label-text-color` | on-state-container | same | same |
| `container-shape-radius` | 4px (`radius-xs`) on status chips | class override | class override |
| `with-avatar-avatar-size` | 18px | override | override |


### Switch

**Angular Material:** `mat-slide-toggle`

- 52×32 px track. On: `primary` track, 24 px `on-primary` handle with an optional check icon. Off: `surface-container-highest` track, 2 px `outline` border, 16 px `outline` handle.
- Label left in settings lists (switch trailing) or right in forms; a switch applies immediately — if the change needs confirmation use a checkbox + Save.

`mat.slide-toggle-overrides((…))` sets these in **both** files; the CSS variable is `--mat-slide-toggle-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `selected-track-color` | #254487 / #B1C5FF | `color="primary"` | `--mat-sys-primary` |
| `selected-handle-color` | #FFFFFF / #042C70 | contrast | `--mat-sys-on-primary` |
| `selected-icon-color` | #254487 / #B1C5FF | default | `--mat-sys-on-primary-container` by default → primary |
| `unselected-track-color` | #D5D4D8 / #424245 | override | `--mat-sys-surface-variant` by default → surface-container-highest |
| `unselected-handle-color` | #696A73 / #9C9DA7 | override | `--mat-sys-outline` (default) |
| `track-outline-color` | #696A73 / #9C9DA7 | override | `--mat-sys-outline` (default) |
| `track-width` | 52px | default | default |
| `track-height` | 32px | default | default |
| `selected-handle-size` | 24px | default | default |
| `unselected-handle-size` | 16px | default | default |


### Tabs

**Angular Material:** `mat-tab-group` (primary: `fitInkBarToContent=false`, `stretchTabs`; secondary: `fitInkBarToContent`, scrollable) / `mat-tab-nav-bar`

- Primary: fixed, equal width, 48 px, 3 px rounded `primary` indicator; top-level sections. Secondary: scrollable, content-width, 2 px full-width indicator; sub-sections.
- Active label `primary`, inactive `on-surface-variant`, label-large; max 6 tabs, else a navigation rail. `role="tab"` + `aria-selected`.

`mat.tabs-overrides((…))` sets these in **both** files; the CSS variable is `--mat-tab-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `active-indicator-color` | #254487 / #B1C5FF | `color="primary"` | `--mat-sys-primary` |
| `active-label-text-color` | #254487 / #B1C5FF | `primary` | `--mat-sys-on-surface` by default → primary |
| `inactive-label-text-color` | #44464F / #C5C6D0 | `foreground.secondary-text` | `--mat-sys-on-surface` by default → on-surface-variant |
| `active-indicator-height` | 3px (primary) · 2px (secondary) | default 2px → 3px | default 2px → 3px |
| `active-indicator-shape` | 3px 3px 0 0 (primary) | override | `--mat-sys-corner-full` top (default) |
| `container-height` | 48px | default 48px | default |
| `divider-color` | #B7B8C2 / #53545D | `foreground.divider` | `--mat-sys-surface-variant` by default → outline-variant |
| `label-text-size` | 14px (label-large) | `button` | `--mat-sys-label-large-size` |


### TextField

**Angular Material:** `mat-form-field appearance="outline"` + `matInput` (`"fill"` in dense tables); `mat-select`, `mat-autocomplete`, `matDatepicker` inside it

- Outlined, 56 px, radius-xs, floating label on the surface colour behind it. Resting 1 px `outline` border + `on-surface-variant` label; focused 2 px `primary`; error 2 px `error` with label and helper in `error`, `aria-invalid` + `aria-describedby`.
- Code, keys, URLs, paths in Open Sans 600; prose values body-large. Helper body-small `on-surface-variant`, 4 px below, 16 px inset. Inside a dialog the label background is the dialog colour. 24 px between fields.

`mat.form-field-overrides((…))` sets these in **both** files; the CSS variable is `--mat-form-field-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-height` | 56px | density 0 → 56px | 56px |
| `outlined-outline-color` | #696A73 / #9C9DA7 | `foreground.divider` → set `outline` | `--mat-sys-outline` |
| `outlined-outline-width` | 1px | default | default |
| `outlined-label-text-color` | #44464F / #C5C6D0 | `foreground.secondary-text` | `--mat-sys-on-surface-variant` |
| `outlined-container-shape` | 4px (`radius-xs`) | `mat.form-field-overrides` | `--mat-sys-corner-extra-small` (default) |
| `outlined-input-text-color` | #1B1B1F / #E9E7EC | `foreground.text` | `--mat-sys-on-surface` |
| `error-text-color` | #BA1A1A / #FFB4AB | `warn` | `--mat-sys-error` |
| `outlined-error-outline-color` | #BA1A1A / #FFB4AB | `warn` | `--mat-sys-error` |
| `filled-container-color` | #D5D4D8 / #424245 (dense tables) | override | `--mat-sys-surface-container-highest` (default) |
| `subscript-text-size` | 12px (body-small) | `caption` | `--mat-sys-body-small-size` |

Focused 2 px `primary` outline: `focus-outline-color` is not a token — it follows `--mat-sys-primary` (M3) / the `primary` palette (M2) automatically. Select panel: `mat.select-overrides((panel-background-color: surface-container))`, selected option `mat.option-overrides((selected-state-layer-color: secondary-container, selected-state-label-text-color: on-secondary-container))`.

### TimePicker

**Angular Material:** `mat-timepicker` (v19+; input mode) — the dial mode is the AIToolbox custom component

- Input mode 328 px: two 96×80 px fields in display-large, the active one in `primary-container`, AM/PM segmented in `tertiary-container` when selected. 24 h, 5-minute steps in ops forms; schedules always show the timezone next to the field.

`mat.timepicker-overrides((…))` sets these in **both** files; the CSS variable is `--mat-timepicker-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-background-color` | #DEDCE0 / #39393C | override | `--mat-sys-surface-container` by default → high |
| `container-shape` | 28px | override | `--mat-sys-corner-extra-small` by default → 28px |


### Tooltip

**Angular Material:** `matTooltip` (plain); rich tooltips are a Card in a `cdkConnectedOverlay`

- Plain: 24 px, label-medium, `inverse-surface`, after 500 ms on hover / focus; labels an icon button, never holds information unavailable elsewhere.
- Rich: title + supporting text, optional action, `surface-container-high` with elevation-2, radius-md; opens on hover or an info icon click, stays while hovered.

`mat.tooltip-overrides((…))` sets these in **both** files; the CSS variable is `--mat-tooltip-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-color` | #303034 / #E4E2E6 | override | `--mat-sys-inverse-surface` (default) |
| `supporting-text-color` | #F2F0F4 / #303034 | override | `--mat-sys-inverse-on-surface` |
| `container-shape` | 4px | override | `--mat-sys-corner-extra-small` (default) |
| `supporting-text-size` | 12px (label-medium) | `caption` | `--mat-sys-body-small-size` by default → label-medium |

`matTooltipShowDelay` = 500.

### TopAppBar

**Angular Material:** `mat-toolbar` (never `color="primary"`)

- Small 64 px: leading navigation icon, title-large, up to three trailing icon buttons; at rest `surface`, scrolled `surface-container`. Medium / large 112 / 152 px with the title under the icons in headline-medium / -large, collapsing to small on scroll.
- Icon buttons 40 px in a 48 px slot; titles truncate, never wrap in the small bar. Navy is for actions, not the bar.

`mat.toolbar-overrides((…))` sets these in **both** files; the CSS variable is `--mat-toolbar-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-background-color` | #FBF8FD / #1F1F23 at rest · #E9E7EC / #303034 scrolled | `background.app-bar` + a `.scrolled` class | `--mat-sys-surface` / `-surface-container` via a class |
| `container-text-color` | #1B1B1F / #E9E7EC | `foreground.text` | `--mat-sys-on-surface` |
| `standard-height` | 64px | default 64px | default |
| `mobile-height` | 64px (56px on phones) | default 56px | default |
| `title-text-size` | 22px (title-large) | `headline-6` at 22px | `--mat-sys-title-large-size` |


### Table, Paginator, Sort header, Expansion panel, Stepper, Tree (not yet specified)

Angular Material components AIToolbox has not designed yet; the tokens exist in both generations and the rules below are the starting point.

`mat.table-overrides((…))` sets these in **both** files; the CSS variable is `--mat-table-<token>`. Status column = 20 px tile glyph (StateMark C); row loading = 20 px pen orbit; row failed = error tile + Retry; table-level error = StateMark B circle 56–64 px; pending = the pending ring in the same slot.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `background-color` | #FFFFFF / #17171B | `background.card` | `--mat-sys-surface` by default → lowest |
| `header-headline-color` | #44464F / #C5C6D0 | `foreground.secondary-text` | `--mat-sys-on-surface-variant` |
| `header-headline-size` | 12px (label-medium, uppercase) | `caption` | `--mat-sys-title-small-size` by default → label-medium |
| `header-container-height` | 48px | default 56px → 48px | default 56px → 48px |
| `row-item-container-height` | 52px (40px dense) | default 52px | default |
| `row-item-outline-color` | #B7B8C2 / #53545D | `foreground.divider` | `--mat-sys-outline` by default → outline-variant |
| `row-item-label-text-color` | #1B1B1F / #E9E7EC | `foreground.text` | `--mat-sys-on-surface` |

`mat.paginator-overrides((…))` sets these in **both** files; the CSS variable is `--mat-paginator-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-background-color` | #FFFFFF / #17171B | `background.card` | `--mat-sys-surface` |
| `container-text-color` | #44464F / #C5C6D0 | `foreground.secondary-text` | `--mat-sys-on-surface-variant` |
| `container-size` | 56px | default | default |

`mat.sort-overrides((…))` sets these in **both** files; the CSS variable is `--mat-sort-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `arrow-color` | #44464F / #C5C6D0 | `foreground.secondary-text` | `--mat-sys-on-surface-variant` |

`mat.expansion-overrides((…))` sets these in **both** files; the CSS variable is `--mat-expansion-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-background-color` | #F5F3F7 / #27282B | `background.card` | `--mat-sys-surface` by default → low |
| `header-text-color` | #1B1B1F / #E9E7EC | `foreground.text` | `--mat-sys-on-surface` |
| `header-collapsed-state-height` | 48px | default | default |
| `container-shape` | 12px | override | `--mat-sys-corner-medium` (default) |

`mat.stepper-overrides((…))` sets these in **both** files; the CSS variable is `--mat-stepper-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `header-selected-state-icon-background-color` | #254487 / #B1C5FF | `primary` | `--mat-sys-primary` |
| `header-done-state-icon-background-color` | #254487 / #B1C5FF | `primary` | `--mat-sys-primary` |
| `header-error-state-icon-foreground-color` | #BA1A1A / #FFB4AB | `warn` | `--mat-sys-error` |
| `line-color` | #B7B8C2 / #53545D | `foreground.divider` | `--mat-sys-outline` by default → outline-variant |

`mat.tree-overrides((…))` sets these in **both** files; the CSS variable is `--mat-tree-<token>`.

| Token | AIToolbox value (light / dark) | M2 · v21 default | M3 · v22 default |
|---|---|---|---|
| `container-background-color` | #FBF8FD / #1F1F23 | `background.card` | `--mat-sys-surface` |
| `node-text-color` | #1B1B1F / #E9E7EC | `foreground.text` | `--mat-sys-on-surface` |
| `node-min-height` | 40px | default 48px → 40px | default 48px → 40px |


---

## Putting it in a project

**Angular Material 21, M2 (`angular/theme.m2.scss`)** — `mat.m2-define-palette` on the seven generated palettes (700 = tone 30 light, 200 = tone 80 dark, 100 = containers), `mat.m2-define-light-theme` / `-dark-theme` with the typography config, surfaces injected into `background` / `foreground`, then the per-component `mat.*-overrides` blocks above for everything M2 does not model (snackbar, shapes, health chips). Dark mode by the `html.dark` class.

**Angular Material 22, M3 (`angular/_theme-colors.scss` + `angular/theme.m3.scss`)** — `mat.theme((color: (primary: dt.$primary-palette, tertiary: dt.$tertiary-palette, theme-type: color-scheme), typography: (brand-family, plain-family), density: 0))`, then `mat.theme-overrides` pinning the roles to the AIToolbox hex, then the same `mat.*-overrides` blocks. Dark mode by `color-scheme: light dark` (or the `html.light` / `html.dark` classes).

Both files are compiled in this system against `@angular/material` 21.2.14 and 22.2.3 (Sass 1.80) with no warnings. The migration checklist is in `angular-material.md`.
