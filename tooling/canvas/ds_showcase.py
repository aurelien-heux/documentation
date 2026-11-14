"""Build one self-contained HTML page that shows the whole AIToolbox design system:
principles, colour roles (light and dark), type scale, shape, elevation, spacing, layout and breakpoints,
brand assets and state marks, and every component with its live preview, specification and rules.
Usage: python3 ds_showcase.py <design-system/project dir> <output.html>"""
import sys, os, re, json, html, base64
import markdown

SRC, DST = sys.argv[1], sys.argv[2]
J = lambda *p: os.path.join(SRC, *p)
tok = json.load(open(J('tokens.json'), encoding='utf-8'))
man = json.load(open(J('manifest.json'), encoding='utf-8'))
readme = open(J('README.md'), encoding='utf-8').read()
rules = open(J('component-rules.md'), encoding='utf-8').read()
font_b64 = base64.b64encode(open(J('fonts', 'BNPPType-Regular.woff2'), 'rb').read()).decode()

md = lambda s: markdown.markdown(s, extensions=['tables', 'fenced_code', 'sane_lists'])
esc = lambda s: html.escape(s, quote=True)

# ---------- token CSS (from tokens.json, the source of truth) ----------
colors = tok['color']['tokens']
def theme_block(t):
    return ''.join(f'--{c["name"]}:{c["value"][t]};' for c in colors)
static = ''.join(f'--{x["name"]}:{x["value"]};' for x in tok['radius']['tokens'] + tok['shadow']['tokens'] + tok['spacing']['tokens'])
fam = tok['type']['families']
static += f"--font-ui:{fam['ui']};--font-body:{fam['body']};--font-plain:{fam['plain']};--font-brand:{fam['ui']};"
for g in tok['type']['groups']:
    for st in g['styles']:
        f = fam[st.get('family', g['family'])]
        static += f"--text-{st['name']}:{st['fontWeight']} {st['fontSize']}/{st['lineHeight']} {f};"
FONT_FACE = f"@font-face{{font-family:'BNPP Type';src:url(data:font/woff2;base64,{font_b64}) format('woff2');font-weight:400 700;font-display:swap}}"
FONT_REL = os.environ.get('DS_FONT_URL', 'design-system/project/fonts/BNPPType-Regular.woff2')
IFRAME_FONT = f"@font-face{{font-family:'BNPP Type';src:url({FONT_REL}) format('woff2');font-weight:400 700;font-display:swap}}"
TOKENS_CSS = (FONT_FACE + f":root,[data-theme=\"light\"]{{{theme_block('light')}color-scheme:light}}"
              f"[data-theme=\"dark\"]{{{theme_block('dark')}color-scheme:dark}}:root{{{static}}}")
IFRAME_CSS = TOKENS_CSS.replace(FONT_FACE, IFRAME_FONT)

# ---------- rules per component (### sections of component-rules.md) ----------
rule_sec = {}
for m in re.finditer(r'^### (.+?)\n(.*?)(?=^### |^## |\Z)', rules, flags=re.S | re.M):
    rule_sec[m.group(1).strip()] = m.group(2).strip()

# ---------- components ----------
summaries = {c['name']: (c.get('group'), c.get('summary', '')) for c in man.get('components', [])}
comps = []
for name in sorted(os.listdir(J('components'))):
    d = J('components', name)
    if not os.path.isdir(d):
        continue
    prev = open(os.path.join(d, 'preview.html'), encoding='utf-8').read() if os.path.exists(os.path.join(d, 'preview.html')) else ''
    rd = open(os.path.join(d, 'README.md'), encoding='utf-8').read() if os.path.exists(os.path.join(d, 'README.md')) else ''
    m = re.search(r'@dsCard([^>]*)-->', prev)
    meta = m.group(1) if m else ''
    grp = re.search(r'group="([^"]+)"', meta)
    hgt = re.search(r'height=(\d+)', meta)
    group = (grp.group(1) if grp else None) or summaries.get(name, (None,))[0] or 'Layout'
    if group == 'Containment':
        group = 'Containers'
    # first paragraph of the README as the summary when the manifest has none
    summ = summaries.get(name, (None, ''))[1]
    if not summ and rd:
        body = re.sub(r'^# .*\n', '', rd).strip()
        para = []
        for ln in body.split('\n'):
            if not ln.strip() or re.match(r'\s*([-*]|\d+\.)\s', ln) or ln.startswith('#'):
                if para: break
                continue
            para.append(ln.strip())
        summ = ' '.join(para)
        if not summ:
            mb = re.search(r'^\s*[-*]\s+(.+)$', body, flags=re.M)
            summ = mb.group(1).strip() if mb else ''
        summ = re.sub(r'[*`]', '', summ)
        if len(summ) > 220:
            summ = summ[:217].rsplit(' ', 1)[0] + '…'
    # the preview runs in an iframe with the tokens injected; theme set from the page
    doc = re.sub(r'<!--\s*@dsCard[^>]*-->\s*', '', prev)
    inj = f'<style>{IFRAME_CSS}</style>'
    doc = doc.replace('<head>', '<head>' + inj, 1) if '<head>' in doc else inj + doc
    rd_html = md(re.sub(r'^# .*\n', '', rd)) if rd else ''
    rk = next((k for k in rule_sec if k == name or k.startswith(name + ' ') or k.startswith(name + ',')), None)
    comps.append(dict(name=name, group=group, summary=summ, height=int(hgt.group(1)) if hgt else 320,
                      doc=doc, readme=rd_html, rules=md(rule_sec[rk]) if rk else ''))
GROUP_ORDER = ['Actions', 'Communication', 'Containers', 'Feedback', 'Inputs', 'Selection', 'Navigation', 'Layout']
comps.sort(key=lambda c: (GROUP_ORDER.index(c['group']) if c['group'] in GROUP_ORDER else 99, c['name']))
groups = []
for c in comps:
    if not groups or groups[-1][0] != c['group']:
        groups.append((c['group'], []))
    groups[-1][1].append(c)

# ---------- README sections ----------
sections = re.split(r'^## ', readme, flags=re.M)
intro = md(re.sub(r'^# .*\n', '', sections[0]).strip())
readme_secs = []
for s in sections[1:]:
    title, _, body = s.partition('\n')
    readme_secs.append((title.strip(), md(body.strip())))
principles = next((b for t, b in readme_secs if t.lower().startswith('principles')), '')

# ---------- colour groups ----------
def cgroup(n):
    segs = n.split('-')
    for key, label in [('logo', 'Logo family'), ('nav-', 'Navigation'), ('run', 'Run action'), ('ai', 'AI'), ('success', 'Status'), ('warning', 'Status'), ('error', 'Status'),
                       ('inverse', 'Inverse'), ('outline', 'Outline'), ('surface', 'Surfaces'), ('scrim', 'Surfaces'), ('shadow', 'Surfaces'), ('focus', 'Focus'),
                       ('primary', 'Primary'), ('secondary', 'Secondary'), ('tertiary', 'Tertiary')]:
        k = key.rstrip('-')
        if k in segs:
            return label
    return 'Other'
CORDER = ['Primary', 'Secondary', 'Tertiary', 'Run action', 'AI', 'Status', 'Surfaces', 'Navigation', 'Outline', 'Inverse', 'Focus', 'Logo family', 'Other']
cg = {}
for c in colors:
    cg.setdefault(cgroup(c['name']), []).append(c)

def lum(hexv):
    h = hexv.lstrip('#'); r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def ratio(a, b):
    la, lb = lum(a), lum(b); hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)
cmap = {c['name']: c['value'] for c in colors}

def swatch(c):
    n = c['name']; on = 'on-' + n if ('on-' + n) in cmap else None
    pair = ''
    if on:
        pair = (f'<span class="ratio" title="Contrast of {on} on {n}">{on} · {ratio(cmap[n]["light"], cmap[on]["light"]):.1f}:1 light · '
                f'{ratio(cmap[n]["dark"], cmap[on]["dark"]):.1f}:1 dark</span>')
    txt = f'var(--{on})' if on else ('#FFFFFF' if lum(c['value']['light']) < .3 else '#1C1B1E')
    return (f'<figure class="sw" data-name="{esc(n)}"><div class="chip-c" style="background:var(--{n});color:{txt}"><span>{esc(n)}</span></div>'
            f'<figcaption><code>--{esc(n)}</code><span class="hex"><i style="background:{c["value"]["light"]}"></i>{c["value"]["light"].upper()}'
            f'<i style="background:{c["value"]["dark"]}"></i>{c["value"]["dark"].upper()}</span>{pair}<p>{esc(c.get("usage", ""))}</p></figcaption></figure>')

colour_html = ''.join(f'<h3>{g}</h3><div class="swgrid">' + ''.join(swatch(c) for c in cg[g]) + '</div>' for g in CORDER if g in cg)

# ---------- type ----------
type_rows = []
for g in tok['type']['groups']:
    for st in g['styles']:
        f = fam[st.get('family', g['family'])]
        type_rows.append(f'<div class="ty"><div class="ty-meta"><b>{st["name"]}</b><span>{st["fontSize"]} / {st["lineHeight"]} · {st["fontWeight"]} · {st["letterSpacing"]}</span>'
                         f'<span>{esc(f.split(",")[0])}</span><span class="muted">{esc(st.get("usage", ""))}</span></div>'
                         f'<div class="ty-s" style="font:{st["fontWeight"]} {st["fontSize"]}/{st["lineHeight"]} {esc(f)};letter-spacing:{st["letterSpacing"]}">{esc(st["sample"])}</div></div>')
type_html = ''.join(type_rows)

shape_html = ''.join(f'<figure class="shape"><div style="border-radius:{x["value"]}"></div><figcaption><code>--{x["name"]}</code> {x["value"]}<p>{esc(x["usage"])}</p></figcaption></figure>' for x in tok['radius']['tokens'])
elev_html = ''.join(f'<figure class="elev"><div style="box-shadow:{x["value"]}">{x["name"]}</div><figcaption><p>{esc(x["usage"])}</p></figcaption></figure>' for x in tok['shadow']['tokens'])
space_html = ''.join(f'<div class="sp"><code>--{x["name"]}</code><span class="bar" style="width:{x["value"]}"></span><span>{x["value"]}</span><span class="muted">{esc(x["usage"])}</span></div>' for x in tok['spacing']['tokens'])
bp_html = ('<table><thead><tr><th>Token</th><th>Value</th><th>Use</th></tr></thead><tbody>' +
           ''.join(f'<tr><td><code>{x["name"]}</code></td><td>{x["value"]}</td><td>{esc(x["usage"])}</td></tr>' for x in tok['breakpoint']['tokens'] + tok['layout']['tokens']) + '</tbody></table>')

# ---------- assets ----------
def svg(path):
    s = open(path, encoding='utf-8').read()
    s = re.sub(r'<\?xml[^>]*>\s*', '', s)
    # make ids unique per file so inline masks/gradients don't collide
    base = re.sub(r'\W', '', os.path.basename(path).split('.')[0])
    ids = set(re.findall(r'id="([^"]+)"', s))
    for i in ids:
        s = s.replace(f'id="{i}"', f'id="{base}-{i}"').replace(f'url(#{i})', f'url(#{base}-{i})').replace(f'href="#{i}"', f'href="#{base}-{i}"')
    return s
asset_html = ''
for grp in sorted(os.listdir(J('assets'))):
    gd = J('assets', grp)
    if not os.path.isdir(gd):
        continue
    files = sorted(f for f in os.listdir(gd) if f.endswith('-light.svg'))
    note = ''
    if os.path.exists(os.path.join(gd, 'README.md')):
        note = md(re.sub(r'^# .*\n', '', open(os.path.join(gd, 'README.md'), encoding='utf-8').read()))
    tiles = ''
    for f in files:
        stem = f[:-len('-light.svg')]
        dk = os.path.join(gd, stem + '-dark.svg')
        tiles += (f'<figure class="as"><div class="as-pair"><div class="as-l">{svg(os.path.join(gd, f))}</div>'
                  f'<div class="as-d">{svg(dk) if os.path.exists(dk) else ""}</div></div><figcaption><code>{stem}</code></figcaption></figure>')
    asset_html += (f'<section class="sub" id="assets-{grp.lower()}"><h3>{grp}</h3><div class="asgrid">{tiles}</div>'
                   f'<details class="spec"><summary>About {grp.lower()}</summary><div class="md">{note}</div></details></section>')

# ---------- components ----------
def card(c):
    did = 'c-' + c['name'].lower()
    spec = f'<details class="spec"><summary>Specification</summary><div class="md">{c["readme"]}</div></details>' if c['readme'] else ''
    rul = f'<details class="spec"><summary>Rules and Angular Material</summary><div class="md">{c["rules"]}</div></details>' if c['rules'] else ''
    return (f'<article class="comp" id="{did}" data-name="{esc(c["name"].lower())}"><header><h3>{esc(c["name"])}</h3><span class="tag">{esc(c["group"])}</span></header>'
            f'<p class="sum">{esc(c["summary"])}</p>'
            f'<iframe title="{esc(c["name"])} preview" loading="lazy" style="height:{c["height"] + 8}px" srcdoc="{esc(c["doc"])}"></iframe>{spec}{rul}</article>')
comp_html = ''.join(f'<section class="sub" id="g-{g.lower()}"><h3 class="gh">{g} <span class="muted">· {len(cs)}</span></h3>' + ''.join(card(c) for c in cs) + '</section>' for g, cs in groups)

nav_comp = ''.join(f'<li class="ng">{g}</li>' + ''.join(f'<li><a href="#c-{c["name"].lower()}" data-n="{esc(c["name"].lower())}">{esc(c["name"])}</a></li>' for c in cs) for g, cs in groups)
guide_html = ''.join(f'<details class="spec g"><summary>{esc(t)}</summary><div class="md">{b}</div></details>' for t, b in readme_secs)

logo_l = svg(J('assets', 'Logos', 'logo-horizontal-light.svg')) if os.path.exists(J('assets', 'Logos', 'logo-horizontal-light.svg')) else 'AIToolbox'
logo_d = svg(J('assets', 'Logos', 'logo-horizontal-dark.svg')) if os.path.exists(J('assets', 'Logos', 'logo-horizontal-dark.svg')) else ''

PAGE_CSS = r"""
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:80px}
body{margin:0;background:var(--surface);color:var(--on-surface);font:400 14px/20px var(--font-body)}
a{color:var(--primary)}
code{font:600 12px/16px var(--font-plain);background:var(--surface-container-high);padding:1px 6px;border-radius:4px}
h1,h2,h3,h4{font-family:var(--font-ui);font-weight:500;margin:0}
.muted{color:var(--on-surface-variant)}
.top{position:sticky;top:0;z-index:10;height:64px;display:flex;align-items:center;gap:16px;padding:0 16px 0 20px;background:var(--nav-container);border-bottom:2px solid var(--surface)}
.top .lg{height:32px;display:flex;align-items:center}.top .lg svg{height:30px;width:auto}
.top .lg .d{display:none}[data-theme="dark"] .top .lg .l{display:none}[data-theme="dark"] .top .lg .d{display:flex}
.top .ctx{display:flex;flex-direction:column;padding-left:16px;border-left:1px solid var(--outline-variant)}
.top .ctx b{font:500 14px/18px var(--font-ui)}.top .ctx span{font-size:12px;line-height:16px;color:var(--on-surface-variant)}
.top .grow{flex:1}
.search{width:min(360px,40vw);height:40px;border-radius:16px;border:0;background:var(--surface-container-lowest);color:var(--on-surface);padding:0 14px;font:400 14px var(--font-body)}
.seg{display:inline-flex;border:1px solid var(--outline);border-radius:16px;overflow:hidden}
.seg button{height:36px;padding:0 14px;border:0;background:transparent;color:var(--on-surface);font:500 13px var(--font-ui);cursor:pointer}
.seg button[aria-pressed="true"]{background:var(--secondary-container);color:var(--on-secondary-container)}
.wrap{display:grid;grid-template-columns:260px minmax(0,1fr)}
nav.side{position:sticky;top:64px;height:calc(100vh - 64px);overflow:auto;padding:16px 12px 32px;background:var(--surface-container-low);border-right:1px solid var(--outline-variant)}
nav.side ul{list-style:none;margin:0;padding:0}
nav.side a{display:block;padding:6px 12px;border-radius:16px;color:var(--on-surface);text-decoration:none;font:500 13px/20px var(--font-ui)}
nav.side a:hover{background:color-mix(in srgb,var(--primary) 6%,transparent)}
nav.side a.on{background:var(--nav-active);color:var(--on-secondary-container)}
nav.side .ng{padding:14px 12px 4px;font:600 11px/16px var(--font-ui);letter-spacing:.5px;text-transform:uppercase;color:var(--on-surface-variant)}
main{padding:32px clamp(16px,4vw,48px) 96px;max-width:1240px}
section.top-s{padding:8px 0 40px;border-bottom:1px solid var(--outline-variant);margin-bottom:32px}
section.top-s>h2{font-size:28px;line-height:36px;margin-bottom:6px}
section.top-s>p.lead{margin:0 0 20px;color:var(--on-surface-variant);max-width:80ch}
h3{font-size:18px;line-height:24px;margin:24px 0 12px}
.hero{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:24px;align-items:start}
.hero .card{padding:20px 24px}
.card{background:var(--surface-container-lowest);border-radius:12px;box-shadow:var(--elevation-1)}
.md{max-width:90ch}.md p,.md li{line-height:20px}.md table{border-collapse:collapse;width:100%;margin:12px 0;font-size:13px}
.md th,.md td,table th,table td{border-top:1px solid var(--outline-variant);padding:8px 10px;text-align:left;vertical-align:top}
.md th,table th{font:600 11px/16px var(--font-ui);letter-spacing:.5px;text-transform:uppercase;color:var(--on-surface-variant);border-top:0}
table{border-collapse:collapse;width:100%;font-size:13px}
.swgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}
.sw{margin:0;border:1px solid var(--outline-variant);border-radius:12px;overflow:hidden;background:var(--surface-container-lowest)}
.chip-c{height:72px;display:flex;align-items:flex-end;padding:8px 12px;font:500 13px var(--font-ui);border-bottom:1px solid var(--outline-variant)}
.sw figcaption{padding:10px 12px;display:flex;flex-direction:column;gap:6px;font-size:12px}
.sw p{margin:0;color:var(--on-surface-variant);line-height:16px}
.hex{display:flex;align-items:center;gap:6px;font:600 11px var(--font-plain)}.hex i{width:12px;height:12px;border-radius:3px;border:1px solid var(--outline-variant);margin-left:4px}
.ratio{font-size:11px;color:var(--on-surface-variant)}
.ty{display:grid;grid-template-columns:260px minmax(0,1fr);gap:24px;align-items:center;padding:14px 0;border-top:1px solid var(--outline-variant)}
.ty-meta{display:flex;flex-direction:column;gap:2px;font-size:12px}.ty-meta b{font:500 14px var(--font-ui)}
.ty-s{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.row3{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:16px}
.shape,.elev{margin:0}.shape div{height:72px;background:var(--primary-container);border:1px solid var(--primary)}
.elev div{height:72px;border-radius:12px;background:var(--surface-container-lowest);display:flex;align-items:center;justify-content:center;font:500 13px var(--font-ui)}
.shape figcaption,.elev figcaption{padding-top:8px;font-size:12px}.shape p,.elev p{margin:4px 0 0;color:var(--on-surface-variant)}
.sp{display:grid;grid-template-columns:110px 70px 50px minmax(0,1fr);gap:12px;align-items:center;padding:6px 0;border-top:1px solid var(--outline-variant);font-size:12px}
.sp .bar{height:12px;background:var(--primary);border-radius:2px;display:block}
.asgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
.as{margin:0;border:1px solid var(--outline-variant);border-radius:12px;overflow:hidden}
.as-pair{display:grid;grid-template-columns:1fr 1fr}
.as-l,.as-d{height:110px;display:flex;align-items:center;justify-content:center;padding:12px}
.as-l{background:#FDF8FD}.as-d{background:#14121E}
.as svg{max-width:100%;max-height:80px;width:auto;height:auto}
.as figcaption{padding:8px 12px;border-top:1px solid var(--outline-variant)}
.comp{margin:0 0 20px;padding:16px 20px 12px;border:1px solid var(--outline-variant);border-radius:12px;background:var(--surface-container-lowest)}
.comp header{display:flex;align-items:center;gap:10px}.comp h3{margin:0;font-size:20px;line-height:28px}
.tag{font:600 11px/16px var(--font-ui);padding:2px 8px;border-radius:4px;background:var(--secondary-container);color:var(--on-secondary-container)}
.comp .sum{margin:6px 0 12px;color:var(--on-surface-variant);max-width:90ch}
.comp iframe{width:100%;border:1px solid var(--outline-variant);border-radius:8px;background:var(--surface)}
.gh{font-size:22px;line-height:28px;margin:32px 0 12px}
details.spec{margin-top:10px;border-top:1px solid var(--outline-variant);padding-top:8px}
details.spec>summary{cursor:pointer;font:500 14px/32px var(--font-ui);color:var(--primary);list-style:none;display:flex;align-items:center;gap:6px}
details.spec>summary::before{content:"";width:8px;height:8px;border-right:2px solid currentColor;border-bottom:2px solid currentColor;transform:rotate(-45deg);transition:transform .2s}
details.spec[open]>summary::before{transform:rotate(45deg)}
details.spec>summary::-webkit-details-marker{display:none}
details.g{background:var(--surface-container-lowest);border:1px solid var(--outline-variant);border-radius:12px;padding:4px 16px;margin:8px 0}
details.g>summary{color:var(--on-surface);font-size:16px}
:focus-visible{outline:2px solid var(--focus-ring);outline-offset:2px}
.hidden{display:none!important}
@media (max-width:900px){.wrap{grid-template-columns:1fr}nav.side{display:none}.hero{grid-template-columns:1fr}.ty{grid-template-columns:1fr}.search{display:none}}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""

JS = r"""
(function(){
  var root=document.documentElement, KEY='ait-ds-theme';
  function sys(){return window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'}
  function apply(mode){
    var t=mode==='system'?sys():mode; root.setAttribute('data-theme',t);
    document.querySelectorAll('.seg button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.mode===mode?'true':'false')});
    document.querySelectorAll('iframe').forEach(function(f){try{f.contentDocument.documentElement.setAttribute('data-theme',t)}catch(e){}});
  }
  var mode='system'; try{mode=localStorage.getItem(KEY)||'system'}catch(e){}
  apply(mode);
  document.querySelectorAll('.seg button').forEach(function(b){b.addEventListener('click',function(){mode=b.dataset.mode;try{localStorage.setItem(KEY,mode)}catch(e){};apply(mode)})});
  if(window.matchMedia) matchMedia('(prefers-color-scheme: dark)').addEventListener('change',function(){if(mode==='system')apply(mode)});
  // previews: theme from the page, height from their content (also when they change size later)
  function fit(f){
    try{var d=f.contentDocument; if(!d||!d.body) return; d.documentElement.setAttribute('data-theme',root.getAttribute('data-theme'));
      var size=function(){var h=Math.max(d.documentElement.scrollHeight,d.body.scrollHeight);if(h>40)f.style.height=(h+4)+'px'};
      size(); if(!f._ro&&f.contentWindow.ResizeObserver){f._ro=new f.contentWindow.ResizeObserver(size);f._ro.observe(d.body)}
    }catch(e){}
  }
  document.querySelectorAll('iframe').forEach(function(f){f.addEventListener('load',function(){fit(f)}); if(f.contentDocument&&f.contentDocument.readyState==='complete')fit(f)});
  // component filter
  var q=document.getElementById('q');
  if(q) q.addEventListener('input',function(){var v=q.value.trim().toLowerCase();
    document.querySelectorAll('.comp').forEach(function(c){c.classList.toggle('hidden',v&&c.dataset.name.indexOf(v)<0)});
    document.querySelectorAll('nav.side a[data-n]').forEach(function(a){a.parentNode.classList.toggle('hidden',v&&a.dataset.n.indexOf(v)<0)});
    if(v){var s=document.getElementById('components');if(s)s.scrollIntoView()}});
  // current section in the nav
  var links=[].slice.call(document.querySelectorAll('nav.side a[href^="#"]'));
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(a){a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id)})}})},{rootMargin:'-80px 0px -70% 0px'});
  document.querySelectorAll('section.top-s,.comp').forEach(function(s){io.observe(s)});
})();
"""

v = tok.get('version', '')
page = f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AIToolbox design system</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&amp;display=swap">
<style>{TOKENS_CSS}{PAGE_CSS}</style>
</head>
<body>
<header class="top">
  <span class="lg" aria-label="AIToolbox"><span class="l">{logo_l}</span><span class="d">{logo_d}</span></span>
  <span class="ctx"><b>Design system</b><span>Material Design 3 · tokens {esc(v)} · {len(comps)} components</span></span>
  <span class="grow"></span>
  <input id="q" class="search" type="search" placeholder="Filter components…" aria-label="Filter components">
  <span class="seg" role="group" aria-label="Theme"><button type="button" data-mode="light">Light</button><button type="button" data-mode="dark">Dark</button><button type="button" data-mode="system">System</button></span>
</header>
<div class="wrap">
<nav class="side" aria-label="Design system">
  <ul>
    <li class="ng">Foundations</li>
    <li><a href="#overview">Overview</a></li><li><a href="#colour">Colour</a></li><li><a href="#type">Typography</a></li><li><a href="#shape">Shape and elevation</a></li>
    <li><a href="#spacing">Spacing and layout</a></li><li><a href="#assets">Brand assets</a></li><li><a href="#guidelines">Guidelines</a></li>
    <li class="ng">Components · {len(comps)}</li><li><a href="#components">All components</a></li>
    {nav_comp}
  </ul>
</nav>
<main>
<section class="top-s" id="overview"><h2>AIToolbox design system</h2><p class="lead">Generated on 28 October 2026 from the design system files (tokens {esc(v)}). Previews are the same HTML as the design-system cards, rendered with the tokens below; switch Light, Dark or System at the top.</p>
  <div class="hero"><div class="card md">{intro}</div><div class="card md"><h3 style="margin-top:0">Principles</h3>{principles}</div></div></section>
<section class="top-s" id="colour"><h2>Colour</h2><p class="lead">Every role with its light and dark value, what it is for, and the contrast of its on-colour. The swatches follow the theme switch.</p>{colour_html}</section>
<section class="top-s" id="type"><h2>Typography</h2><p class="lead">{esc(tok.get('meta', {}).get('fonts', ''))}</p>{type_html}</section>
<section class="top-s" id="shape"><h2>Shape and elevation</h2><p class="lead">{esc(tok['radius'].get('note', ''))} {esc(tok['shadow'].get('note', ''))}</p><h3>Shape</h3><div class="row3">{shape_html}</div><h3>Elevation</h3><div class="row3">{elev_html}</div></section>
<section class="top-s" id="spacing"><h2>Spacing and layout</h2><p class="lead">{esc(tok['spacing'].get('note', ''))} {esc(tok['breakpoint'].get('note', ''))}</p><h3>Spacing</h3>{space_html}<h3>Breakpoints and layout</h3>{bp_html}</section>
<section class="top-s" id="assets"><h2>Brand assets</h2><p class="lead">Each asset on light (left) and on dark (right).</p>{asset_html}</section>
<section class="top-s" id="guidelines"><h2>Guidelines</h2><p class="lead">The design system README, section by section.</p>{guide_html}</section>
<section class="top-s" id="components" style="border-bottom:0"><h2>Components</h2><p class="lead">Live preview, specification, and the component rules with their Angular Material mapping.</p>{comp_html}</section>
</main>
</div>
<script>{JS}</script>
</body>
</html>"""
open(DST, 'w', encoding='utf-8').write(page)
print(DST, len(page), 'components:', len(comps), 'with rules:', sum(1 for c in comps if c['rules']))
