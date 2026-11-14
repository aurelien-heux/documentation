# RadioButton
20 px ring with a 10 px dot, 2 px border; selected in `primary`, unselected in `on-surface-variant`.
- Exactly one option in a group is selected; group them in a `<fieldset>` with a `<legend>`.
- For 2–5 short options shown inline, filter chips or a SegmentedButton read better; radios suit vertical lists with descriptions.
- **Angular Material:** `mat-radio-group` + `mat-radio-button color="primary"` (M2) / default (M3). Wrap in a `fieldset` with a `legend`. Full map and theme files: `angular-material.md`.
