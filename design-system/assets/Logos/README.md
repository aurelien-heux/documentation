# Logos

The toolbox-prompt mark and its lockups. Each file exists in two colourings: `-light` for light backgrounds (night `logo-box` #0d0b14 mark with a white `>` and the neon #00f29e cursor; ink + violet wordmark) and `-dark` for dark backgrounds (lavender #c4c0ff mark with a night `>` and the emerald #006c44 cursor; light + tone-80 wordmark); the `ai` badge is the same light teal #80d5d4 with #003737 lettering in both. The box, chevron and cursor are the `logo-box`, `on-logo-box` and `logo-cursor` tokens — the logo family is the only place the raw night seed is used. Colours are fixed in each file; pick the one that matches the surface.

- `logo-horizontal-*` — default lockup, clear space baked in (16 px around an 88 px mark).
- `logo-stacked-*` — centered lockup for square slots and splash screens.
- `mark-*` — the toolbox prompt with the **AI badge**: a light-teal `ai` tile (#80d5d4 in both themes; 31×19 on the 64 grid, radius 5) with "AI" in `on-ai`, on the box's top-right corner, cut out of the mark by a transparent 2.5-unit gap so the two never touch. Minimum 24 px.
- `mark-plain-*` — the mark without the badge: the favicon, the app icon, the loader and anything under 24 px.
- `wordmark-*` — "AIToolbox" in Manrope 800, outlined (no font needed): "AI" in `on-surface`, "Toolbox" in `primary`; never retype it.
- `mark-once-*` / `mark-loop-*` — the mark with the Constructor motion: once builds the logo one time and holds it (splash, app start); loop repeats it (brand loader). Also as GIF (256 px on the surface colour) for slides, wikis and email, and the mark and lockups as transparent PNG for tools that don't take SVG.
- `mark-tag-in-once-*` / `mark-tag-in-loop-*` — the AI-tag intro on the static mark: the plain toolbox, then its corner is carved, the teal tile grows in, "A" then "I" rise and a sheen crosses it. Once (1.4 s) ends on the full mark (first load of the header logo, login, about, end slides); loop (4 s) brings the tag in, holds, folds it back to the plain mark. Same viewBox as `mark-*`; also as GIF.
- `favicon-*` — the `>_` glyph on a rounded night tile (lavender in the dark file) for 16–32 px; the tile is the box.
- `app-icon-*` — full mark reversed on the night tile (white box, night `>`, emerald cursor), maskable-safe, for home-screen and PWA icons.

Alignment grid: inside the mark the `>_` sits on one baseline and is centred in the box (chevron x 17.5–25.5, cursor x 33.5–46.5 on the 64 grid, 2.5 units apart). In the horizontal lockup the capitals of "AIToolbox" are as tall as the box (cap height = 36/64 of the mark) and centred vertically on the whole visible mark, badge top to box bottom (y 5.5–58 of the 64 grid); gap = a quarter of the mark; equal clear space on all four sides. In the stacked lockup the mark (visible bounds, badge included) and the wordmark are both centred on the vertical axis. The lockup files carry this already; when composing them yourself, centre on the visible bounds, not on the SVG boxes.

Rules: a quarter of the mark's height of clear space on every side; no rotation, outlines, gradients or recolouring outside these two sets. The cursor is `logo-cursor`: neon tone 85 on the night box, emerald tone 40 on the lavender box.
