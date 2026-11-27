# Design canvases

Source of the five AIToolbox Design canvases (Claude artifacts of the Design type). Each folder is one canvas:
`canvas.json` (board positions, titles, notes) and one `.dc.html` file per board. `ds/devtoolbox/tokens.json` is the
canvas's copy of the design-system tokens (5.0.1).

| Canvas | Boards | Live |
|---|---|---|
| `design-system/` | Colour roles (`Main`), typography, components and dialog, switch, tooltip, breakpoints, app shell (light, dark, rail, overlays, mobile), header, feedback, cookies, logo, favicon, chatbot mark, Sweep mark, loader, progress, state marks, assistant panel and chat, agent run (usage, panel, page, output viewer) | https://claude.ai/artifact/99DCh11LTWKebFQ9QJANMV |
| `labs/` | Decision labs: hover states, Run button rounds 2–3, tour focus, What's new, Ideas, Q&A, Administration, Feedback administration, Catalog, Docs, catalogue, views, process, change start, agent follow (`AgentLab`, C decided), Sweep purples trial, colour system review (`ColourLab`) | https://claude.ai/artifact/DTSkQfZZJTHTrpBSQxmZVg |
| `prototypes/` | Production vision, Architecture board, Community, assistant, header, feedback, loader / logo / progress / state marks live, release channels, accessibility plan | https://claude.ai/artifact/7GdjuxqjRdryVMquDeX32J |
| `catalog/` | Catalog screens: skill page (`Main` desktop with the "What's inside" file viewer, `Mobile`, `MobileFile`) and listing (`Catalog` Browse and Mine with the paginator, `CatalogMobile`); open points as notes in `canvas.json` | https://claude.ai/artifact/4ax3vXidC5xqbwxkPVXaXj |
| `ideas-questions/` | Community Questions coupled to Ideas: questions list (`Main`), question page (`Question`), Ask form with similar questions and the assistant's draft (`Ask`), Ideas list + detail with linked questions (`Ideas`), phone question (`QuestionMobile`); open points as a note in `canvas.json` | https://claude.ai/artifact/13tUcpJKcBSisrMJ6eaZEK |

Boards are Design Components: the markup sits in `<x-dc>`, `{{holes}}` come from `renderVals()` in the
`<script type="text/x-dc">` block, and `<script src="./support.js">` is the canvas runtime (served by the artifact).
To open boards outside the canvas, build standalone pages:

```bash
python3 tooling/canvas/convert.py canvases/labs out/labs
```

A board file must stay under 2 MiB (the canvas does not show larger files); `ProductionVision.dc.html` is built by
`tooling/canvas/vision_build2.py`, which minifies it to fit.
