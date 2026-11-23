"""Build out/site/index.html: the ArchiMate notation page of the AIToolbox design system (notation 2.0)."""
import html, json, os, re, shutil
from axdata import (VERSION, LAYERS, ELEMENTS, RELATIONSHIPS, CHANGE, PERFORMERS, ROLES)
from content import KINDS, COMPONENTS, GROUPS, RETIRED
from samples import samples, LAYERED_MODEL
import yaml

E = html.escape
S = samples()
os.makedirs("out/site", exist_ok=True)


def glyph(e, cls=""):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{e["svg"]}</svg>')


def tile(e, lg=False):
    return f'<span class="ax-tile ax-l-{e["layer"]}{" lg" if lg else ""}" aria-hidden="true">{glyph(e)}</span>'


EL = {e["id"]: e for e in ELEMENTS}


def svg_inline(kind, r, th):
    s = open(f"out/svg/{kind}-{r}-{th}.svg").read()
    s = re.sub(r"<\?xml[^>]*>", "", s)
    if r == "plantuml":
        p = f"pu-{kind}-{th}-"
        s = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{p}{m.group(1)}"', s)
        s = re.sub(r'url\(#([^)]+)\)', lambda m: f"url(#{p}{m.group(1)})", s)
        s = re.sub(r'href="#([^"]+)"', lambda m: f'href="#{p}{m.group(1)}"', s)
        s = s.replace('font-family="Open Sans"', "font-family=\"'Open Sans', system-ui, sans-serif\"")
        s = s.replace('font-family="sans-serif"', "font-family=\"'Open Sans', system-ui, sans-serif\"")
        w = re.search(r'width="([\d.]+)px"', s)
        nat = w.group(1) if w else "800"
    else:
        m = re.search(r'max-width:\s*([\d.]+)px', s)
        nat = m.group(1) if m else "800"
    title = next(k["name"] for k in KINDS if k["id"] == kind)
    s = re.sub(r"^<svg ", f'<svg role="img" aria-label="{E(title)}, {"PlantUML" if r == "plantuml" else "Mermaid"} rendering" ', s.strip(), count=1)
    return s, nat


# ---------- text alternatives, read from the sources ---------------------------------------------------------------
def alt_text(kind):
    pu, mm, y = S[kind]
    items = []
    if kind == "layered":
        model = {x["id"]: x for x in yaml.safe_load(LAYERED_MODEL)}
        view = yaml.safe_load(y.split("# views/")[1].split("\n", 1)[1])
        items = [f'{model[i]["name"]} ({i}, {model[i]["type"]}{", agent" if model[i].get("agent") else ""})' for i in view["elements"]]
        items += [f'{model[r["from"]]["name"]} → {r["type"]} → {model[r["to"]]["name"]}' + (f' ({r["label"]})' if r.get("label") else "") for r in view["relations"]]
    elif kind in ("workflow", "process-change"):
        for m in re.finditer(r'(\w+)@\{ shape: (\w[\w-]*), label: "(.*?)" \}', mm):
            lab = re.sub(r"<[^>]+>", " ", m.group(3).replace("<br>", ": ")).strip()
            lab = re.sub(r"\s+", " ", lab)
            if lab and lab != ":":
                items.append(lab if m.group(2) != "diam" else "Decision: " + lab)
    elif kind == "state-machine":
        items = [re.sub(r"\s+", " ", l.strip().replace("-->", "→")) for l in mm.splitlines() if "-->" in l]
    elif kind == "class":
        items = [l.strip() for l in mm.splitlines() if re.search(r'(\*--|-->|\.\.>|o--)', l)]
    elif kind == "sequence":
        items = [re.sub(r"(-{1,2}>>)", "→", l.strip()) for l in mm.splitlines() if ">>" in l]
    elif kind == "component":
        items = [l.strip().replace("-.->", "→").replace("---", "offers").replace("-->", "→") for l in mm.splitlines() if re.search(r"(-\.->|---|-->)", l)]
    elif kind == "er":
        items = [l.strip() for l in mm.splitlines() if "||--" in l]
    return items


# ---------- diagram kinds -------------------------------------------------------------------------------------------------
def kind_section(k):
    pu, mm, y = S[k["id"]]
    pu_l, nat_pu = svg_inline(k["id"], "plantuml", "light")
    pu_d, _ = svg_inline(k["id"], "plantuml", "dark")
    mm_l, nat_mm = svg_inline(k["id"], "mermaid", "light")
    mm_d, _ = svg_inline(k["id"], "mermaid", "dark")
    d = k["default"]
    rules = "".join(f"<li>{E(r)}</li>" for r in k["rules"])
    alt = "".join(f"<li>{E(a)}</li>" for a in alt_text(k["id"]))
    mm_src = mm + "\n  %% + the class definitions of aitoolbox-mermaid.json" if mm.split("\n", 1)[0].startswith(("flowchart", "stateDiagram", "classDiagram")) else mm
    return f'''
<section class="kind" id="kind-{k["id"]}" data-r="{d}" aria-labelledby="h-{k["id"]}">
  <div class="kind-head">
    <h3 id="h-{k["id"]}">{E(k["name"])}</h3>
    <p class="q">{E(k["answers"])}</p>
    <p class="where">{E(k["where"])}</p>
  </div>
  <div class="kind-body">
    <figure class="dg-frame">
      <div class="dg-bar">
        <span class="dg-title"><b>{E(k["short"])}</b><span class="dg-meta">YAML view kind <code>{k["id"]}</code></span></span>
        <div class="seg" role="radiogroup" aria-label="Renderer for {E(k["name"])}">
          <button type="button" role="radio" data-set-r="plantuml" aria-checked="{str(d == "plantuml").lower()}">PlantUML{" · default" if d == "plantuml" else ""}</button>
          <button type="button" role="radio" data-set-r="mermaid" aria-checked="{str(d == "mermaid").lower()}">Mermaid{" · default" if d == "mermaid" else ""}</button>
        </div>
        <button type="button" class="btn-t fit" aria-pressed="true">Fit width</button>
      </div>
      <div class="dg-body fit">
        <div class="r r-plantuml" style="--nat:{nat_pu}px"><div class="th-l">{pu_l}</div><div class="th-d">{pu_d}</div></div>
        <div class="r r-mermaid" style="--nat:{nat_mm}px"><div class="th-l">{mm_l}</div><div class="th-d">{mm_d}</div></div>
      </div>
      <figcaption class="dg-foot">
        <span class="r-plantuml-only">PlantUML: {E(k["pu"])}</span><span class="r-mermaid-only">Mermaid: {E(k["mm"])}</span>
        <details><summary>Text alternative</summary><ul class="alt">{alt}</ul></details>
        <details><summary>YAML view</summary><div class="code"><button type="button" class="copy" data-copy>Copy</button><pre><code>{E(y.strip())}</code></pre></div></details>
        <details class="r-plantuml-only"><summary>PlantUML source</summary><div class="code"><button type="button" class="copy" data-copy>Copy</button><pre><code>{E(pu)}</code></pre></div></details>
        <details class="r-mermaid-only"><summary>Mermaid source</summary><div class="code"><button type="button" class="copy" data-copy>Copy</button><pre><code>{E(mm_src)}</code></pre></div></details>
      </figcaption>
    </figure>
    <div class="rules"><h4>Rules</h4><ul>{rules}</ul></div>
  </div>
</section>'''


def kinds_overview():
    cards = []
    for k in KINDS:
        cards.append(f'<a class="kcard" href="#kind-{k["id"]}"><b>{E(k["name"])}</b><span>{E(k["answers"])}</span>'
                     f'<span class="chip-s">{"PlantUML" if k["default"] == "plantuml" else "Mermaid"} by default</span></a>')
    return "".join(cards)


# ---------- components --------------------------------------------------------------------------------------------------
STATUS = {"new": ("st-info", "+", "New"), "changed": ("st-warning", "Δ", "Changed"), "kept": ("st-neutral", "=", "Kept")}


def demo(c):
    i = c["id"]
    if i == "figure":
        figs = []
        for eid, name, extra in [("business-process", "Change the architecture model", ""), ("application-component", "Architecture agent", "agent"),
                                 ("data-object", "Architecture model", ""), ("requirement", "Reviewed knowledge in one repository", "")]:
            e = EL[eid]
            sub = '<span class="ax-sub">✦ agent</span>' if extra else ""
            figs.append(f'<div class="ax-box ax-shape-{e["shape"]} ax-l-{e["layer"]}" role="img" aria-label="{E(name)}, {E(e["name"].lower())}{", agent" if extra else ""}">'
                        f'<div class="ax-in">{glyph(e, "ax-glyph")}<span class="ax-name">{E(name)}{sub}</span></div></div>')
        return '<div class="demo-row">' + "".join(figs) + "</div>"
    if i == "tile":
        return '<div class="demo-row">' + "".join(f'<span class="tile-row">{tile(EL[x])}{E(EL[x]["name"])}</span>' for x in ["goal", "capability", "business-process", "application-component", "data-object"]) + "</div>"
    if i == "element-id":
        return '<div class="demo-row"><a class="ax-id" href="#elements">GOL-01</a><a class="ax-id" href="#elements">PRC-04</a><a class="ax-id" href="#elements">APC-07</a><span class="ax-id bad">APC-99 <small>(not in the model)</small></span></div>'
    if i == "model-status":
        return ('<div class="demo-row"><span class="status st-neutral"><span class="g" aria-hidden="true">○</span>Draft</span>'
                '<span class="status st-success"><span class="g" aria-hidden="true">✓</span>Validated</span>'
                '<span class="status st-retired"><span class="g" aria-hidden="true">⊘</span><s>Retired</s></span></div>')
    if i in ("change-mark",):
        return '<div class="demo-row">' + "".join(f'<span class="ax-change {x["id"]}"><b aria-hidden="true">{x["glyph"]}</b>{x["label"]}</span>' for x in CHANGE) + "</div>"
    if i in ("step", "gate", "event"):
        ids = {"step": ["human", "agent", "system"], "gate": ["gate"], "event": ["event"]}[i]
        names = {"human": "Describe the change in chat", "agent": "Draft or fix the model update", "system": "Validate schema and references", "gate": "Review the pull request", "event": "Change requested"}
        out = []
        for p in ids:
            P = next(x for x in PERFORMERS if x["id"] == p)
            mark = f'<small>{E(P["mark"])}</small>' if P["mark"] else ""
            out.append(f'<span class="wf wf-{p}">{mark}{E(names[p])}</span>')
        return '<div class="demo-row">' + "".join(out) + "</div>"
    if i == "state":
        return '<div class="demo-row"><span class="wf sm">Drafted</span><span class="wf sm sm-current">In review</span><span class="wf sm">Approved</span></div>'
    if i in ("readiness", "decision-chip"):
        xs = [("st-success", "✓", "Ready for the board"), ("st-warning", "!", "Needs attention"), ("st-error", "✕", "Blocked")] if i == "readiness" else \
             [("st-success", "✓", "Approved"), ("st-warning", "↩", "Changes requested"), ("st-error", "✕", "Rejected"), ("st-info", "…", "Pending")]
        return '<div class="demo-row">' + "".join(f'<span class="status {c_}"><span class="g" aria-hidden="true">{g}</span>{w}</span>' for c_, g, w in xs) + "</div>"
    see = {"lane": "workflow", "decision": "workflow", "transition": "state-machine", "change-legend": "process-change", "class-box": "class",
           "lifeline": "sequence", "interface": "component", "table": "er", "frame": "layered", "source": "layered", "relationship": "layered",
           "junction": None, "check-row": None}.get(i)
    if see:
        k = next(x for x in KINDS if x["id"] == see)
        return f'<p class="see">In use: <a href="#kind-{see}">{E(k["name"])}</a></p>'
    return ""


def comp_card(c):
    sc, sg, sw = STATUS[c["status"]]
    li = lambda xs: "".join(f"<li>{E(x)}</li>" for x in xs)
    code = [f'<dt>Web</dt><dd><code>{E(c["css"])}</code></dd>']
    if c["pu"] != "—":
        code.append(f'<dt>PlantUML</dt><dd><code>{E(c["pu"])}</code></dd>')
    if c["mm"] != "—":
        code.append(f'<dt>Mermaid</dt><dd><code>{E(c["mm"])}</code></dd>')
    return f'''<article class="comp" id="c-{c["id"]}">
  <header><h4>{E(c["name"])}</h4><span class="status sm {sc}"><span class="g" aria-hidden="true">{sg}</span>{sw}</span></header>
  <p>{E(c["purpose"])}</p>
  {demo(c)}
  <div class="comp-cols"><div><h5>Anatomy</h5><ul>{li(c["anatomy"])}</ul></div><div><h5>Rules</h5><ul>{li(c["rules"])}</ul></div></div>
  <p class="meta"><b>States</b> {E(c["states"])}</p>
  <p class="meta"><b>Accessibility</b> {E(c["a11y"])}</p>
  <dl class="codes">{"".join(code)}</dl>
</article>'''


def components():
    out = []
    for g, title, sub in GROUPS:
        cs = [c for c in COMPONENTS if c["group"] == g]
        out.append(f'<div class="cgroup" id="g-{g}"><h3>{E(title)} <span class="sub">{E(sub)} · {len(cs)}</span></h3><div class="comps">' + "".join(comp_card(c) for c in cs) + "</div></div>")
    ret = "".join(f"<li><b>{E(a)}</b> {E(b)}</li>" for a, b in RETIRED)
    out.append(f'<div class="cgroup"><h3>Taken out of the list <span class="sub">{len(RETIRED)}</span></h3><ul class="retired">{ret}</ul></div>')
    return "".join(out)


def comp_index():
    n = {s: sum(1 for c in COMPONENTS if c["status"] == s) for s in STATUS}
    return f'{len(COMPONENTS)} components: {n["new"]} new, {n["changed"]} changed, {n["kept"]} kept · {len(RETIRED)} taken out'


# ---------- element and relationship tables ------------------------------------------------------------------------------
def element_rows():
    rows = []
    for l in LAYERS:
        es = [e for e in ELEMENTS if e["layer"] == l["id"]]
        rows.append(f'<tr class="lay" data-layer="{l["id"]}"><th colspan="5" scope="colgroup"><span class="sw ax-l-{l["id"]}"></span>{E(l["label"])} <span class="n">{len(es)}</span></th></tr>')
        for e in es:
            m = f'<span class="ax-id">{e["prefix"]}</span> <code>{e["yaml"]}</code>' if e["inModel"] else '<span class="muted">notation only</span>'
            rows.append(f'<tr data-layer="{e["layer"]}" data-model="{str(e["inModel"]).lower()}" data-q="{E((e["name"] + " " + e["id"] + " " + e["prefix"] + " " + e["yaml"]).lower())}">'
                        f'<td><span class="tile-row">{tile(e)}<b>{E(e["name"])}</b></span><span class="def">{E(e["definition"])}</span></td>'
                        f'<td>{m}</td><td><code>{e["shape"]}</code></td><td><code>{E(e["pu"])}</code></td><td><code>{E(e["mm"])}</code></td></tr>')
    return "".join(rows)


def rel_svg(r):
    dash = {"dotted": 'stroke-dasharray="2 3"', "dashed": 'stroke-dasharray="6 4"'}.get(r["line"], "")

    def mk(kind, end):
        x, d = (4, 1) if end == "s" else (116, -1)
        if kind == "diamond":
            return f'<path d="M{x} 12 l{6*d} -4 l{6*d} 4 l{-6*d} 4z" fill="currentColor"/>'
        if kind == "odiamond":
            return f'<path d="M{x} 12 l{6*d} -4 l{6*d} 4 l{-6*d} 4z" fill="var(--surface-lowest)" stroke="currentColor"/>'
        if kind == "dot":
            return f'<circle cx="{x + 3*d}" cy="12" r="3" fill="currentColor"/>'
        if kind == "arrow":
            return f'<path d="M{x} 12 l{10*d} -5 v10z" fill="currentColor"/>'
        if kind == "triangle":
            return f'<path d="M{x} 12 l{12*d} -6 v12z" fill="var(--surface-lowest)" stroke="currentColor"/>'
        if kind == "open":
            return f'<path d="M{x + 10*d} 6 L{x} 12 L{x + 10*d} 18" fill="none" stroke="currentColor"/>'
        if kind == "small":
            return f'<path d="M{x + 7*d} 8 L{x} 12 L{x + 7*d} 16" fill="none" stroke="currentColor"/>'
        return ""
    return (f'<svg viewBox="0 0 120 24" width="120" height="24" aria-hidden="true" class="relsvg"><line x1="6" y1="12" x2="114" y2="12" stroke="currentColor" stroke-width="1.4" {dash}/>'
            f'{mk(r["source"], "s")}{mk(r["target"], "e")}</svg>')


def rel_rows():
    return "".join(
        f'<tr><td><b>{E(r["name"])}</b><span class="def">{E(r["definition"])}</span></td><td>{rel_svg(r)}</td>'
        f'<td>{"in the model" if r["inModel"] else "<span class=muted>notation only</span>"}</td>'
        f'<td><code>{E(r["pu"])}</code><br><code class="muted">{E(r["proc"])}(from, to)</code></td><td><code>{E(r["mm"])}</code> <span class="muted">+ type label</span></td></tr>'
        for r in RELATIONSHIPS)


def swatches():
    rows = []
    for p in PERFORMERS:
        def c(th):
            R = ROLES[th]
            if p["fill"] == "business":
                L = next(l for l in LAYERS if l["id"] == "business")[th]
                return L["fill"], L["ink"]
            return R[p["fill"]], R[p["ink"]]
        fl, il = c("light"); fd, idk = c("dark")
        rows.append(f'<tr><td><span class="wf wf-{p["id"]}">{("<small>" + E(p["mark"]) + "</small>") if p["mark"] else ""}{E(p["label"])}</span></td>'
                    f'<td>{E(p["rule"])}</td><td><code>{fl} / {il}</code></td><td><code>{fd} / {idk}</code></td></tr>')
    return "".join(rows)


KIND_TABLE = "".join(
    f'<tr><td><a href="#kind-{k["id"]}">{E(k["name"])}</a></td><td><code>{k["id"]}</code></td><td>{E(k["pu"])}</td><td>{E(k["mm"])}</td>'
    f'<td><b>{"PlantUML" if k["default"] == "plantuml" else "Mermaid"}</b></td></tr>' for k in KINDS)

PUML_USAGE = '''@startuml
!$AX_THEME = "dark"          ' optional, light by default
!include aitoolbox.puml
hide stereotype
AX_Goal(GOL01, "Productivity and developer experience")
AX_BusinessProcess(PRC04, "Change the architecture model")
AX_Agent(APC07, "Architecture agent")
AX_RelServing(APC07, PRC04, "drafts the update", "up")
@enduml'''
MM_USAGE = '''// mermaid@11
import theme from "./aitoolbox-mermaid.json";
const mode = dark ? "dark" : "light";
mermaid.initialize({ startOnLoad: false, ...theme[mode].config });
const src = view + "\\n" + theme[mode].classDefs.join("\\n");
const { svg } = await mermaid.render(id, src);'''

LAYER_CSS = "\n".join(f'.ax-l-{l["id"]} {{ --ax-fill: var(--ax-{l["id"]}-fill); --ax-ink: var(--ax-{l["id"]}-ink); }}' for l in LAYERS)
LAYER_LIGHT = " ".join(f'--ax-{l["id"]}-fill:{l["light"]["fill"]}; --ax-{l["id"]}-ink:{l["light"]["ink"]};' for l in LAYERS)
LAYER_DARK = " ".join(f'--ax-{l["id"]}-fill:{l["dark"]["fill"]}; --ax-{l["id"]}-ink:{l["dark"]["ink"]};' for l in LAYERS)
LIGHT = ("--primary:#39235F; --on-primary:#FFFFFF; --primary-container:#E3DFFF; --on-primary-container:#14085E; --secondary-container:#DED7EB; --on-secondary-container:#1D1A28;"
         " --surface:#FDF8FD; --surface-lowest:#FFFFFF; --surface-low:#FAF4FF; --surface-container:#F8F1FF; --surface-high:#F2EBFA; --surface-highest:#ECE5F4; --nav:#EDE4FF;"
         " --on-surface:#1C1B1E; --on-surface-variant:#48454E; --outline:#79757F; --outline-variant:#CAC4CF; --ai:#004F50; --ai-container:#9CF1F0; --on-ai-container:#002020;"
         " --success:#0B5314; --success-container:#ACF4A2; --on-success-container:#002203; --warning:#5C4300; --warning-container:#FFDEA0; --on-warning-container:#261900;"
         " --error:#93000A; --error-container:#FFDAD6; --on-error-container:#410002; --inverse-surface:#313033; --inverse-on-surface:#F4EFF4;")
DARK = ("--primary:#C4C0FF; --on-primary:#2A2473; --primary-container:#413C8A; --on-primary-container:#E3DFFF; --secondary-container:#484454; --on-secondary-container:#E6DFF3;"
        " --surface:#14121E; --surface-lowest:#0F0C19; --surface-low:#1D1A27; --surface-container:#23202D; --surface-high:#2B2836; --surface-highest:#363341; --nav:#1D1A27;"
        " --on-surface:#ECE5F8; --on-surface-variant:#CAC3DC; --outline:#948DA5; --outline-variant:#494458; --ai:#80D5D4; --ai-container:#004F50; --on-ai-container:#9CF1F0;"
        " --success:#91D888; --success-container:#0B5314; --on-success-container:#ACF4A2; --warning:#FCBC00; --warning-container:#5C4300; --on-warning-container:#FFDEA0;"
        " --error:#FFB4AB; --error-container:#93000A; --on-error-container:#FFDAD6; --inverse-surface:#E6DFF2; --inverse-on-surface:#322E3C;")

CSS = open("page.css").read().replace("/*LIGHT*/", LIGHT + " " + LAYER_LIGHT).replace("/*DARK*/", DARK + " " + LAYER_DARK).replace("/*LAYERS*/", LAYER_CSS)
JS = open("page.js").read()
n_model = sum(1 for e in ELEMENTS if e["inModel"])
layer_chips = "".join(f'<button type="button" class="chip" data-f="{l["id"]}" aria-pressed="false"><span class="sw ax-l-{l["id"]}"></span>{E(l["label"])}</button>' for l in LAYERS)

PAGE = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ArchiMate Notation</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&family=Open+Sans:wght@400;600;700&display=swap">
<style>
{CSS}
</style>
</head>
<body>
<a class="skip" href="#kinds">Skip to the diagram kinds</a>
<header class="top">
  <div class="wrap top-in">
    <div>
      <p class="eyebrow">AIToolbox design system</p>
      <h1>ArchiMate notation</h1>
      <p class="lead">How AI Toolbox draws its architecture: the ArchiMate figures for the model, and the diagram kinds the model needs beyond ArchiMate (business workflows, process changes, life cycles and detailed design), each generated from a YAML view as PlantUML or Mermaid with one theme.</p>
      <p class="ver">{E(VERSION)} · {len(ELEMENTS)} element types, {n_model} in the model · {len(RELATIONSHIPS)} relationships · {len(KINDS)} diagram kinds · {E(comp_index())}</p>
    </div>
    <div class="seg theme" role="radiogroup" aria-label="Theme">
      <button type="button" role="radio" data-theme-set="system" aria-checked="true">System</button>
      <button type="button" role="radio" data-theme-set="light" aria-checked="false">Light</button>
      <button type="button" role="radio" data-theme-set="dark" aria-checked="false">Dark</button>
    </div>
  </div>
  <nav class="wrap tabs" aria-label="Sections"><a href="#kinds">Diagram kinds</a><a href="#components">Components</a><a href="#elements">Elements</a><a href="#relationships">Relationships</a><a href="#renderers">Renderers and themes</a></nav>
</header>
<main class="wrap">
<section id="kinds" class="block" aria-labelledby="h-kinds">
  <h2 id="h-kinds">Diagram kinds</h2>
  <p class="intro">Every diagram is a YAML view in <code>views/</code>: it names the elements, the kind and the renderer, and the generator emits the source with the AIToolbox theme. ArchiMate covers the model; four kinds go beyond it for processes and life cycles, and four for detailed design. Each kind has a default renderer, the one that draws its notation completely; the other is supported.</p>
  <div class="kgrid">{kinds_overview()}</div>
  {"".join(kind_section(k) for k in KINDS)}
</section>
<section id="components" class="block" aria-labelledby="h-comp">
  <h2 id="h-comp">Components</h2>
  <p class="intro">The amended list: {E(comp_index())}. Colours follow one rule. In ArchiMate, component and table views the <b>layer</b> decides the colour; in workflows and sequences the <b>performer</b> decides it (person, agent, system, review gate). Teal always comes with ✦ agent, and status is never told by colour alone.</p>
  {components()}
</section>
<section id="elements" class="block" aria-labelledby="h-el">
  <h2 id="h-el">Elements</h2>
  <p class="intro">All {len(ELEMENTS)} ArchiMate 3.2 types keep a figure; the {n_model} kept by the Preliminary have an ID prefix and a YAML type and are the only ones the schema accepts.</p>
  <div class="toolbar">
    <label class="search"><span class="vh">Search element types</span><input id="q" type="search" placeholder="Search a type, prefix or YAML name" autocomplete="off"></label>
    <div class="chips" role="group" aria-label="Filter element types"><button type="button" class="chip" data-f="all" aria-pressed="true">All</button><button type="button" class="chip" data-f="model" aria-pressed="false">In the model</button>{layer_chips}</div>
  </div>
  <div class="tbl"><table class="els"><caption class="vh">Element types</caption><thead><tr><th scope="col">Type</th><th scope="col">In the model</th><th scope="col">Figure</th><th scope="col">PlantUML</th><th scope="col">Mermaid shape</th></tr></thead><tbody>{element_rows()}</tbody></table></div>
  <p class="empty" id="empty" hidden>No element type matches. Clear the search or pick All.</p>
</section>
<section id="relationships" class="block" aria-labelledby="h-rel">
  <h2 id="h-rel">Relationships</h2>
  <p class="intro">PlantUML draws the ArchiMate markers. Mermaid keeps solid, dotted and thick lines only, so its label always starts with the type.</p>
  <div class="tbl"><table><caption class="vh">Relationships</caption><thead><tr><th scope="col">Relationship</th><th scope="col">Line</th><th scope="col">Model</th><th scope="col">PlantUML</th><th scope="col">Mermaid</th></tr></thead><tbody>{rel_rows()}</tbody></table></div>
</section>
<section id="renderers" class="block" aria-labelledby="h-ren">
  <h2 id="h-ren">Renderers and themes</h2>
  <p class="intro">Both themes are generated from the design-system tokens (5.0.1), in light and dark. The generator writes the include line or appends the class definitions; nobody styles a diagram by hand.</p>
  <div class="two">
    <article class="card">
      <h3>PlantUML</h3>
      <p><code>theme/aitoolbox.puml</code>: one include with the colours of both themes, the {sum(1 for e in ELEMENTS if e["shape"] not in ("group", "junction"))} element procedures with the design-system glyphs, the relationship, step, gate and event procedures, and the styles of the activity, state, class, sequence, component and entity diagrams.</p>
      <ul>
        <li>Layout by Smetana, built into PlantUML: no Graphviz to install in Jenkins.</li>
        <li>Checked with PlantUML 1.2026.8 (jar) and the in-browser engine <code>@plantuml/core</code>, which renders every sample under a strict content security policy. The chat and the web pages can render without a server.</li>
        <li>Dark: <code>!$AX_THEME = "dark"</code> before the include.</li>
      </ul>
      <div class="code"><button type="button" class="copy" data-copy>Copy</button><pre><code>{E(PUML_USAGE)}</code></pre></div>
    </article>
    <article class="card">
      <h3>Mermaid</h3>
      <p><code>theme/aitoolbox-mermaid.json</code>: for each theme, the <code>base</code> theme variables and the class definitions of the layers, performers, change marks, current state and domain-model stereotypes.</p>
      <ul>
        <li>Checked with Mermaid 11.16 (mermaid-cli).</li>
        <li>Rendered natively by GitHub, the bank's Git hosting previews and Markdown in the chat: the default for life cycles, classes, sequences and tables.</li>
        <li>Limits: no ArchiMate markers, no swimlanes, no interface lollipops. Those kinds default to PlantUML.</li>
      </ul>
      <div class="code"><button type="button" class="copy" data-copy>Copy</button><pre><code>{E(MM_USAGE)}</code></pre></div>
    </article>
  </div>
  <h3 class="sub-h">Default renderer per kind</h3>
  <p class="intro">Proposal for the open point of the Preliminary (PlantUML or Mermaid: pick one, or allow both per view): both are allowed; each kind has a default, set in the view with <code>renderer:</code>.</p>
  <div class="tbl"><table><thead><tr><th scope="col">Kind</th><th scope="col">View kind</th><th scope="col">PlantUML</th><th scope="col">Mermaid</th><th scope="col">Default</th></tr></thead><tbody>{KIND_TABLE}</tbody></table></div>
  <h3 class="sub-h">Performer colours</h3>
  <div class="tbl"><table><thead><tr><th scope="col">Performer</th><th scope="col">Rule</th><th scope="col">Light fill / ink</th><th scope="col">Dark fill / ink</th></tr></thead><tbody>{swatches()}</tbody></table></div>
</section>
</main>
<footer class="wrap foot"><p>Source of record: <code>design-system/archimate/</code> in the documentation repository. Generated from the notation data; the PlantUML and Mermaid samples on this page are rendered from the sources shown, with the themes linked above.</p></footer>
<div class="snack" id="snack" role="status" aria-live="polite" hidden></div>
<script>
{JS}
</script>
</body>
</html>
'''
open("out/site/index.html", "w").write(PAGE)
print("page", len(PAGE.encode()))
