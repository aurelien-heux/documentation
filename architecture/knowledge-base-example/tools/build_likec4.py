#!/usr/bin/env python3
"""Build the LikeC4 site from dist/likec4/ and give it the AIToolbox look.

  1. `likec4 build --output-single-file --use-hash-history` → one self-contained HTML file
  2. inject the page fonts (Google Fonts: Manrope, Open Sans; BNPP Type when installed)
  3. inject tools/likec4/aitoolbox-likec4.css (exact tokens, light + dark, Mantine chrome)
  4. add an "Open in AIToolbox" link back to the Architecture page (dist/index.html)
  5. `likec4 codegen webcomponent` → dist/likec4-views.js (<likec4-view view-id=… browser>), then inline it
     with the same CSS into dist/index.html, where the Chain tab and the element pages render real LikeC4 views

Outputs: dist/likec4-site/index.html — next to dist/index.html, so the element links `../index.html#<id>`
open the matching element page · dist/likec4-views.js · dist/index.html (LikeC4 views embedded).
Run after tools/generate.py, which rewrites dist/index.html without the component.

Usage:  python3 tools/build_likec4.py [root]
Env:    LIKEC4=/path/to/likec4   (default: `npx -y likec4@1.41.0`)
"""
from __future__ import annotations
import json, os, shlex, subprocess, sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
PROJECT = ROOT / "dist" / "likec4"
OUT = ROOT / "dist" / "likec4-site"
CSS = ROOT / "tools" / "likec4" / "aitoolbox-likec4.css"
AX_CSS = ROOT / "design-system" / "archimate" / "archimate-likec4.css"   # ArchiMate layer colours, generated
LIKEC4 = shlex.split(os.environ.get("LIKEC4", "npx -y likec4@1.41.0"))

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Open+Sans:wght@400;600&display=swap">')
BACKLINK = '<a class="atb-backlink" href="../index.html">← Open in AIToolbox</a>'


def main() -> int:
    if not (PROJECT / "views.generated.c4").exists():
        print("dist/likec4/ missing: run tools/validate.py and tools/generate.py first")
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    cmd = LIKEC4 + ["build", "--output-single-file", "--use-hash-history",
                    "--title", "AIToolbox Architecture", "-o", str(OUT), str(PROJECT)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-2000:], r.stderr[-2000:])
        return r.returncode
    page = OUT / "index.html"
    html = page.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8") + "\n" + AX_CSS.read_text(encoding="utf-8")
    skin = f'{FONTS}\n<style id="aitoolbox-skin">\n{css}\n</style>\n'
    if 'id="aitoolbox-skin"' not in html:
        # The inlined bundle itself contains "</head>" and "</body>" strings: insert at the LAST occurrence.
        i = html.rfind("</head>"); html = html[:i] + skin + html[i:]      # last in <head>: wins over LikeC4's styles
        j = html.rfind("</body>"); html = html[:j] + BACKLINK + "\n" + html[j:]
    page.write_text(html, encoding="utf-8")
    print(f"built {page.relative_to(ROOT)} ({page.stat().st_size // 1024} KB) with the AIToolbox skin")
    return embed_webcomponent(css)


def embed_webcomponent(css: str) -> int:
    """Generate <likec4-view> and inline it into the Architecture page (dist/index.html)."""
    bundle = ROOT / "dist" / "likec4-views.js"
    r = subprocess.run(LIKEC4 + ["codegen", "webcomponent", "-o", str(bundle), str(PROJECT)], capture_output=True, text=True)
    if r.returncode != 0 or not bundle.exists():
        print(r.stdout[-2000:], r.stderr[-2000:])
        return r.returncode or 1
    page = ROOT / "dist" / "index.html"
    html = page.read_text(encoding="utf-8")
    marker = "<!--LIKEC4-WEBCOMPONENT-->"
    if marker not in html:
        print("dist/index.html has no LikeC4 placeholder (already embedded? run tools/generate.py first)")
        return 1
    js = bundle.read_text(encoding="utf-8").replace("</script", "<\\/script")
    js = js.replace("\ufffd", "\\uFFFD")   # literal U+FFFD inside the bundle's strings → same character, as an escape
    skin = json.dumps(css).replace("</", "<\\/")
    html = html.replace(marker, f"<script>window.ATB_LC4_SKIN = {skin};</script>\n<script>\n{js}\n</script>", 1)
    page.write_text(html, encoding="utf-8")
    print(f"embedded <likec4-view> into dist/index.html ({page.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
