# TextField

Outlined Material 3 text field, 56 px, radius-xs, floating label on the surface colour behind it.

- **Resting** — 1 px `outline` border, label in `on-surface-variant`.
- **Focused** — 2 px `primary` border, label in `primary`.
- **Error** — 2 px `error` border, label and helper in `error`, `aria-invalid="true"` and the helper linked with `aria-describedby`.
- Values that are code, keys, URLs or paths use the Open Sans at 600; prose values use the brand family at body-large.
- Helper text is body-small in `on-surface-variant`, 4 px below the field, 16 px inset.

Inside a dialog the label's background is the dialog colour (`surface-container-high`). Fields in a form are 24 px apart; two short fields may share a row.
- **Responsive:** Forms are one column, 600 px max; pairs (start / end date) sit side by side from 600 px of page area; under 600 px the form actions are full width.
- **Keyboard and screen reader:** a visible label (never placeholder only); focus = outline 2 px `primary`, no outer ring; errors set `aria-invalid` and `aria-describedby`, are announced (`role="alert"` on submit) and focus moves to the first invalid field; a form title is a heading.
- **Angular Material:** `mat-form-field appearance="outline"` + `matInput` (or `mat-select`, `matDatepicker`). Error: `mat-error` + `aria-invalid` comes from the form control. M2: `--mdc-outlined-text-field-container-shape: 4px`; M3: `mat.form-field-overrides((outlined-container-shape: 4px))`. Keys/paths/IDs: a class setting Open Sans 600 on the input. Full map and theme files: `angular-material.md`.
