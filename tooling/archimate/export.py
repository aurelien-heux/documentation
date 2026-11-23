"""Write the theme files and the example sources into design-system/archimate/ (run from tooling/archimate)."""
import json, os
from samples import samples
from themes import puml_theme, mermaid_theme

DS = os.path.join("..", "..", "design-system", "archimate")
os.makedirs(os.path.join(DS, "theme"), exist_ok=True); os.makedirs(os.path.join(DS, "examples"), exist_ok=True)
open(os.path.join(DS, "theme", "aitoolbox.puml"), "w").write(puml_theme())
json.dump(mermaid_theme(), open(os.path.join(DS, "theme", "aitoolbox-mermaid.json"), "w"), indent=1, ensure_ascii=False)
for kind, (pu, mm, yml) in samples().items():
    for ext, text in (("yaml", yml), ("puml", pu), ("mmd", mm)):
        open(os.path.join(DS, "examples", f"{kind}.{ext}"), "w").write(text.rstrip() + "\n")
print("written to", os.path.abspath(DS))
