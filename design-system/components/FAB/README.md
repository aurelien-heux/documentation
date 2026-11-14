# FAB
Floating action button for the screen's single creative action (new workspace, new tool).
- **Small** 40 px radius-md · **Default** 56 px radius-lg · **Large** 96 px radius-lg (16 px, the ceiling) · **Extended** 56 px with a label.
- Fill `primary-container` with `on-primary-container` content; elevation-3. The small run FAB (`tertiary-container` lime fill, `on-tertiary-container` glyph) is only for a "run" entry point.
- One FAB per screen, bottom-right, 16 px from the edges; it lowers to elevation-1 when a dialog opens.
- **Responsive:** Under 600 px the page primary action (New pipeline) becomes an extended FAB 16 px above the NavigationBar, shrinking to its icon on scroll. From 600 px the action stays a button in the page header: no FAB.
- **Angular Material:** `mat-fab`, `mat-mini-fab`, `mat-fab extended`. M2: `color="primary"` gives a `primary` fill — add a class for the `primary-container` fill, or accept the filled look; M3: `mat.fab-overrides((container-shape: 16px))` and the container colour defaults to `primary-container`. Run entry (lime): `class="dt-run"`. Full map and theme files: `angular-material.md`.
