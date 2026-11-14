# BottomSheet
Phone-width surface anchored to the bottom: `surface-container-low`, radius-lg (16 px) top corners, 32×4 px drag handle in `outline`.
- **Modal** (with scrim) for a short list of actions on one item; **standard** (no scrim) for persistent supplementary content.
- On tablet and desktop the same content becomes a SideSheet or a Dialog.
- **Responsive:** Compact only (under 600 px). From 600 px the same content is a SideSheet, a Menu or a Dialog.
- **Keyboard and screen reader:** modal sheets move focus in and back, Esc closes; the drag handle is also a button.
- **Angular Material:** `MatBottomSheet`. M2 and M3: `mat.bottom-sheet-overrides((container-shape: 16px))` (M2 also `background.dialog`). Full map and theme files: `angular-material.md`.
