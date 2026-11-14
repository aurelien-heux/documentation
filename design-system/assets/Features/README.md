# Features

Feature marks kept in the design system. Today: **Architecture**; the marks of Sweep, Docs, Environments and Notifications are in the brand package (`brand/feature-marks/`), the Chatbot in `assets/Chatbot`.

## Architecture

Three stacked layers, from intent (top) to code (bottom), linked by dashed traceability lines; the green dot in the bottom layer is running code. It is the mark of the Architecture space (Docs › Architecture) and of the Architecture feature page header.

- `architecture-light.svg` / `-dark.svg` — static mark, 64 × 64 viewBox. Navigation (24 px), headers (32–48 px), space cards and empty states (64 px and up). Light: layers deep violet #39235F, links teal #278383, dot green #00A56B. Dark: lavender #A6A2F8, light teal #80D5D4, neon #00F29E.
- `architecture-once-*.svg` — entrance, 1.6 s, plays one time and holds the static mark: the layers drop in from top to bottom, the links appear, the dot pops. When the Architecture space or a review opens.
- `architecture-loop-*.svg` — working, 2.8 s: the links flow downwards, each layer dims in turn, the dot beats; every cycle starts and ends on the static mark. While the model is being validated or a build is running.
- `architecture-<size>-*.png` — static mark, transparent, 24 to 512 px, for tools that do not take SVG.

Minimum size 24 px: below it the dashed links turn to noise (same rule as the Chatbot). Never recolour; on colour or photos, place it on a `surface` tile. Not yet made: the lockup (mark + "AIToolbox" + "Architecture", outlined text) and the once / loop GIFs.
