# SideSheet
A 256–400 px panel docked to the right edge for filters, details or secondary settings: `surface` with an `outline-variant` divider (standard) or `surface-container-low` with a scrim (modal).
- Header: title-large and a close icon button; actions pinned to the bottom above a divider.
- Standard side sheets push content; modal ones overlay it. On phones the same content becomes a BottomSheet.
- The assistant is **not** a side sheet: it is the inline Assistant block (split view with a resize grip), see `Assistant`.
- **Responsive:** From 1200 px standard (pushes the page) or modal; 600–1199 px modal only (`mode="over"`, scrim); under 600 px it becomes a BottomSheet, or a full-screen dialog for a form.
- **Keyboard and screen reader:** modal sheets move focus in and back, Esc closes; standard sheets keep focus where it is.
- **Angular Material:** `mat-sidenav position="end"` (`mode="side"` standard, `"over"` modal). Width 256–400 px; M2 `background.card` / M3 `surface-container-low`. Full map and theme files: `angular-material.md`.
