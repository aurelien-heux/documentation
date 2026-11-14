# BottomAppBar
Phone-only 80 px bar on `nav-container` — the same violet tint as the drawer, rail and navigation bar (content stays near-neutral) — with up to four icon buttons on the left and a FAB (no shadow here) on the right.
- Use on detail screens where the primary action and a few tools belong at the thumb; never together with a NavigationBar.
- **Angular Material:** No Angular Material equivalent — a `mat-toolbar class="dt-nav"` fixed to the bottom (the class sets its background to `nav-container` in both theme files) with `mat-icon-button`s and a `mat-fab` (`.dt-run` only for a run entry point). Same under M2 and M3. Full map and theme files: `angular-material.md`.
