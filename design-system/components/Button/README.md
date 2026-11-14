# Button

Material 3 buttons at 40 px, radius-lg (16 px — never full-round), label-large. Five emphasis levels plus the lime "run" button.

- **Filled (primary)** — the one decision on a screen: Save, Create, Open.
- **Tonal (secondary-container)** — secondary actions beside a filled one: Filter, Cancel-but-visible.
- **Elevated** — filled-like emphasis on a patterned or tinted ground; elevation-1.
- **Outlined / Text** — low emphasis; Text is the dialog dismiss.
- **Run (`tertiary-container` / `on-tertiary-container`)** — the single action that starts work: Run, Deploy, Apply, New run. A tonal button in the Sweep lime #DCEAB4 (both themes) with a Sweep purple #39235F label and play icon (10.4 : 1), no edge, like every tonal fill. At most one per screen, leading play icon, never inside a dialog. Repeated run actions (rows, cards) are text buttons in `primary` with the play icon in a 22 px lime disc (`tertiary-container` fill, `on-tertiary-container` glyph) (`.dt-run-text`), never filled. Hover: `on-tertiary-container` layer at 6 %. Lime is not a status: Passed stays the green `success` chip with its ✓.
- **Disabled** — on-surface at 12 % fill / 38 % text.

Horizontal padding is space-6 (24 px); with a leading icon the left padding drops to 16 px. Icon-only buttons are 40 px circles and need an `aria-label`. Destructive actions are Text buttons in `error`, never a filled red.
- **Keyboard and screen reader:** focus ring outside the button (2 px gap); Enter and Space activate; icon + label buttons need no extra name; a disabled button that must explain itself is `aria-disabled` (stays focusable) with a hidden description.
- **Angular Material:** `mat-flat-button` = filled, `mat-raised-button` = elevated, `mat-stroked-button` = outlined, `mat-button` = text. Tonal: M2 has none — `mat-flat-button color="accent"` on the `lighter` hue (set in `theme.m2.scss`); M3: `mat.button-overrides` with `secondary-container`. Run: `class="dt-run"` in both. Destructive: `mat-button color="warn"`. Full map and theme files: `angular-material.md`.
