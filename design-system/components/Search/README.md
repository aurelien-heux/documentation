# Search
- **Search bar** — 56 px, radius-lg (16 px), `surface-container-high`, leading menu/back icon, placeholder in `on-surface-variant`, trailing avatar or action.
- **Search view** — the results surface below, radius-lg, same container tone; rows are 48 px list items with a type hint in label-medium.
- Results are grouped by kind (tools, runs, secrets); identifiers show in Open Sans at 600.
- **Responsive:** Under 600 px the field is an icon button that opens the search view full screen; 600–1199 px the field flexes from 240 px (320 px from 840) to 440 px with the Ask chip as an icon; from 1200 px it is 440 px with the labelled Ask chip.
- **Keyboard and screen reader:** `role="search"`; ⌘K focuses the field; results are a listbox with arrow keys; the result count is announced.
- **Angular Material:** `mat-form-field appearance="outline"` with `matInput` + `mat-autocomplete`; the search view is the autocomplete panel (`surface-container-high`, 16 px via overrides). Same in M2 and M3. Full map and theme files: `angular-material.md`.
