# List
Rows of 56 px (one line), 72 px (two lines) or 88 px (three lines): leading avatar/icon, title-medium headline, body-medium supporting text in `on-surface-variant`, trailing meta or icon.
- Selected row: `surface-container` fill (`secondary-container` for a selected item in a navigation list).
- Dividers are inset to the text when rows have a leading element. Row padding is 16 px; the whole row is the hit target.
- **Responsive:** Under 600 px of page area, data tables become two-line lists: state mark + name, a meta line, actions in the row menu.
- **Keyboard and screen reader:** a selectable list has one Tab stop and arrow keys; row actions are reachable from the row; the focus ring is drawn inside the row.
- **Angular Material:** `mat-list`, `mat-nav-list`, `mat-selection-list`, `mat-action-list`; `matListItemAvatar` / `matListItemIcon` for leading elements. Active nav item: `accent` lighter pill (M2 class) / `secondary-container` (M3). Full map and theme files: `angular-material.md`.
