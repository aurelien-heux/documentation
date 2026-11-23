# Tooling

| Folder | What |
|---|---|
| `canvas/` | Generators of the canvas boards: labs (`*_lab_build.py`), Community prototype (`community_build.py`, `community-prototype-src/`), production vision (`vision_build2.py` and its parts, `vision-prototype-src/`), Architecture board (`architecture-board/`: data, logic, `build_arch.py`, `gen_graphs.py`), ArchiMate notation (`archimate_ds.py`), Agent run component boards (`agent_run_build.py`), checks (`markup_check.py`), standalone conversion (`convert.py` + `dc-standalone.js`). |
| `colour-review/` | The colour review of 2026-11-14: `gen.mjs` (option palettes with `@material/material-color-utilities`), `contrast.py`, `build.py` (the `ColourLab` board), `pal.mjs`, `apply_tokens.py` (tokens 5.0), `recolour.py` (board recolour 4.7 → 5.0.1). Paths at the top of each script point at the working folders used then; set them to your checkout before running. |
| `archimate/` | ArchiMate notation 2.0: data, PlantUML and Mermaid themes (`export.py` writes `design-system/archimate/`), example renders (`render.py`, needs `plantuml.jar` and `mmdc`), reference page (`page.py`). See its README. |
| `brand/` | `recolour_rasters.py`: recolours PNG and GIF brand exports from one purple to another in place (anti-aliased blends included, GIF frames and timing untouched). Used for #35307E → #39235F on the light logos and feature marks. Needs Pillow. |

Python 3.11+, Node 20+. The scripts read the board sources in `canvases/` and the tokens in `design-system/`.
