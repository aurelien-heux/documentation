# Tooling

| Folder | What |
|---|---|
| `canvas/` | Generators of the canvas boards: labs (`*_lab_build.py`), Community prototype (`community_build.py`, `community-prototype-src/`), production vision (`vision_build2.py` and its parts, `vision-prototype-src/`), Architecture board (`architecture-board/`: data, logic, `build_arch.py`, `gen_graphs.py`), ArchiMate notation (`archimate_ds.py`), checks (`markup_check.py`), standalone conversion (`convert.py` + `dc-standalone.js`). |
| `colour-review/` | The colour review of 2026-11-14: `gen.mjs` (option palettes with `@material/material-color-utilities`), `contrast.py`, `build.py` (the `ColourLab` board), `pal.mjs`, `apply_tokens.py` (tokens 5.0), `recolour.py` (board recolour 4.7 → 5.0.1). Paths at the top of each script point at the working folders used then; set them to your checkout before running. |

Python 3.11+, Node 20+. The scripts read the board sources in `canvases/` and the tokens in `design-system/`.
