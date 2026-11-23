# ArchiMate notation generator (Notation 2.0)

Generates the PlantUML and Mermaid themes, the example diagrams and the reference page of the ArchiMate notation.
Run every script from this folder.

| File | What |
|---|---|
| `axdata.py` | Notation data: version, colour roles (tokens 5.0.1), layers, 62 element types (model prefix, PlantUML procedure and stereotype, Mermaid shape), relationships, change marks, performers. |
| `notation-1x.json` | Notation 1.x data the element list, layers and glyphs come from. |
| `glyph_paths.json` | Type glyphs as SVG paths with explicit closes (PlantUML sprites ignore `rect`, `circle` and `Z`). |
| `pu_stereo.json` | PlantUML `archimate` stereotype per element type. |
| `themes.py` | `puml_theme()` and `mermaid_theme()`. |
| `samples.py` | The YAML view and the PlantUML and Mermaid sources of each diagram kind. |
| `content.py` | Page content: diagram kinds and their rules, components, what was taken out. |
| `export.py` | Writes `design-system/archimate/theme/` and `design-system/archimate/examples/`. |
| `render.py` | Renders every example in both renderers and both themes to `out/svg/`. |
| `page.py`, `page.css`, `page.js` | Builds `out/site/index.html`, the reference page (copy it to `architecture/pages/archimate-notation.html`). |

## Run

```sh
python3 export.py                     # theme files and examples into design-system/archimate/
python3 render.py                     # out/svg/<kind>-<renderer>-<theme>.svg
python3 page.py                       # out/site/index.html
cp out/site/index.html ../../architecture/pages/archimate-notation.html
```

Needs Python 3.11+, Java 17+ with `plantuml.jar` 1.2026.8 in this folder (from the npm package `plantuml-cli`, or
plantuml.com), and Mermaid CLI 11.16 (`npm i -g @mermaid-js/mermaid-cli`, command `mmdc`). `out/` and the jar are not
committed.
