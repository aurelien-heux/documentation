# Dialog

Material 3 basic dialog carrying a short form.

- Container 280–560 px wide, radius-lg (16 px), `surface-container-high`, elevation-3, space-6 (24 px) padding, over a `scrim` at 32 %.
- Title in headline-small; one line of supporting text in body-medium on `on-surface-variant`.
- Fields are the TextField component with the label background set to the dialog colour; 24 px between rows; short enumerations are filter chips, defaults are switches, options are checkboxes.
- Actions right-aligned: a Text button to dismiss, one Filled `primary` button to confirm. Never the Run button, never a filled destructive button; a delete confirm is a Text button in `error`.
- Focus goes to the first field; Esc = Cancel. More than about six fields becomes a full-screen dialog or a page.
- **Responsive:** Under 600 px a form opens as a full-screen dialog (close · title · Save in a top bar); a confirmation stays a basic dialog 16 px from the edges. From 600 px: basic dialog 280–560 px.
- **Keyboard and screen reader:** focus moves to the first field (or the title when there is none), Tab cycles inside, Esc = Cancel and closes this dialog only, focus returns to the opener; the page behind is inert.
- **Angular Material:** `MatDialog` (`mat-dialog-title`, `mat-dialog-content`, `mat-dialog-actions align="end"`). M2 and M3: `mat.dialog-overrides((container-shape: 16px))` (M2 also `background.dialog` = `surface-container-high`). Confirm `mat-flat-button`, dismiss `mat-button`, delete `mat-button color="warn"`. Full map and theme files: `angular-material.md`.
