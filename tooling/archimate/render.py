"""Render every sample with PlantUML (jar) and Mermaid (mermaid-cli), light and dark, into out/svg/."""
import json, os, re, subprocess, sys
from samples import samples
from themes import puml_theme, mermaid_theme

os.makedirs("out/src", exist_ok=True); os.makedirs("out/svg", exist_ok=True)
open("out/src/aitoolbox.puml", "w").write(puml_theme())
MT = mermaid_theme()
for th in ("light", "dark"):
    json.dump(MT[th]["config"], open(f"out/src/mermaid-{th}.json", "w"))
only = sys.argv[1:]
S = samples()
pu_jobs = []
for kind, (pu, mm, _) in S.items():
    if only and kind not in only:
        continue
    for th in ("light", "dark"):
        src = pu if th == "light" else pu.replace("!include aitoolbox.puml", '!$AX_THEME = "dark"\n!include aitoolbox.puml')
        p = f"out/src/{kind}-{th}.puml"; open(p, "w").write(src); pu_jobs.append(p)
        mp = f"out/src/{kind}-{th}.mmd"
        body = mm + "\n" + "\n".join("  " + c for c in MT[th]["classDefs"]) if mm.split("\n", 1)[0].startswith(("flowchart", "stateDiagram", "classDiagram")) else mm
        open(mp, "w").write(body)
        r = subprocess.run(["mmdc", "-i", mp, "-o", f"out/svg/{kind}-mermaid-{th}.svg", "-c", f"out/src/mermaid-{th}.json",
                            "-b", "transparent", "--svgId", f"mm-{kind}-{th}", "-q"], capture_output=True, text=True)
        if r.returncode:
            print("MERMAID FAIL", kind, th, r.stderr[-600:])
r = subprocess.run(["java", "-jar", "plantuml.jar", "-tsvg", "-o", os.path.abspath("out/svg")] + pu_jobs, capture_output=True, text=True)
err = "\n".join(l for l in r.stderr.splitlines() if "JAVA_TOOL" not in l)
if err.strip():
    print("PLANTUML:", err[-1500:])
for p in pu_jobs:
    b = os.path.basename(p)[:-5]
    kind, th = b.rsplit("-", 1)
    src = f"out/svg/{b}.svg"
    if os.path.exists(src):
        os.replace(src, f"out/svg/{kind}-plantuml-{th}.svg")
print("rendered", len(pu_jobs), "PlantUML and", len(pu_jobs), "Mermaid")
