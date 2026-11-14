"""Static graph views for the Architecture board: lane layouts drawn with ArchiMate figures (buttons wired to
{{go.<sid>}}) and one SVG of relationship lines per view. Each view is one <sc-if value="{{gOn.<key>}}"> block."""
import re, html, json

NW, NH, LW, LGAP, LPAD, HEAD, PITCH, TOP, BOTTOM = 176, 56, 216, 64, 20, 30, 76, 14, 20
SID = lambda s: re.sub(r'[^A-Za-z0-9_]', '_', s)

DASH = {'flow': '6 4', 'realization': '5 4', 'influence': '5 4', 'access': '2 3', 'assignment': '', 'serving': '', 'triggering': '', 'composition': '', 'aggregation': '', 'association': ''}
END = {'flow': 'arrow', 'realization': 'hollow', 'influence': 'open', 'access': 'open', 'assignment': 'arrow', 'serving': 'open', 'triggering': 'arrow', 'composition': None, 'aggregation': None, 'association': None}
START = {'composition': 'diamond', 'aggregation': 'hdiamond', 'assignment': 'dot'}
REL_LABEL = {'flow': 'Flow', 'realization': 'Realization', 'influence': 'Influence', 'access': 'Access', 'assignment': 'Assignment', 'serving': 'Serving', 'triggering': 'Triggering', 'composition': 'Composition', 'aggregation': 'Aggregation', 'association': 'Association'}

def markers(key):
    p = f'm-{key}-'
    return (f'<defs>'
            f'<marker id="{p}arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M1 1L9 5 1 9z" fill="#48454E"/></marker>'
            f'<marker id="{p}open" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M1 1L9 5 1 9" fill="none" stroke="#48454E" stroke-width="1.4"/></marker>'
            f'<marker id="{p}hollow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M1 1L9 5 1 9z" fill="#FDF8FD" stroke="#48454E" stroke-width="1.2"/></marker>'
            f'<marker id="{p}diamond" viewBox="0 0 12 10" refX="1" refY="5" markerWidth="10" markerHeight="8" orient="auto"><path d="M1 5L6 1 11 5 6 9z" fill="#48454E"/></marker>'
            f'<marker id="{p}hdiamond" viewBox="0 0 12 10" refX="1" refY="5" markerWidth="10" markerHeight="8" orient="auto"><path d="M1 5L6 1 11 5 6 9z" fill="#FDF8FD" stroke="#48454E" stroke-width="1.2"/></marker>'
            f'<marker id="{p}dot" viewBox="0 0 10 10" refX="2" refY="5" markerWidth="6" markerHeight="6" orient="auto"><circle cx="5" cy="5" r="3.5" fill="#48454E"/></marker>'
            f'</defs>')

def node_html(n, x, y, w=NW, h=NH):
    cls = f"ax-box ax-l-{n['layer']} ax-shape-{n['shape']}" + (' ax-chg-' + n['change'] if n.get('change') else '') + (' ax-muted' if n.get('muted') else '')
    return (f'<button type="button" class="{cls}" data-sid="{SID(n["id"])}" style="left: {x}px; top: {y}px; --ax-w: {w}px; --ax-h: {h}px" onClick="{{{{pick.{SID(n["id"])}}}}}" title="{html.escape(n["kname"])} · {html.escape(n["title"])}">'
            f'<span class="ax-in"><span class="ax-name">{html.escape(n["title"])}</span></span><i class="axg axg-{n["kind"]} ax-glyph" aria-hidden="true"></i></button>')

def path_html(key, pts, kind, label=None):
    d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
    dash = f' stroke-dasharray="{DASH.get(kind, "")}"' if DASH.get(kind) else ''
    me = f' marker-end="url(#m-{key}-{END[kind]})"' if END.get(kind) else ''
    ms = f' marker-start="url(#m-{key}-{START[kind]})"' if START.get(kind) else ''
    out = f'<path d="{d}" fill="none" stroke="#48454E" stroke-width="1.3"{dash}{me}{ms}/>'
    if label:
        # label at the middle of the longest segment
        best, bl = None, -1
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            L = abs(x2 - x1) + abs(y2 - y1)
            if L > bl: bl, best = L, ((x1 + x2) / 2, (y1 + y2) / 2, abs(x2 - x1) > abs(y2 - y1))
        mx, my, horiz = best
        if horiz: out += f'<text x="{mx:.1f}" y="{my - 4:.1f}" text-anchor="middle" class="gv-lbl">{html.escape(label)}</text>'
        else: out += f'<text x="{mx + 5:.1f}" y="{my + 3:.1f}" class="gv-lbl">{html.escape(label)}</text>'
    return out

def lane_layout(key, lanes, edges, crumbs):
    """lanes: [{'title', 'nodes': [node]}] ; edges: [{'s','t','k','l'}]. Returns the sc-if block."""
    lanes = [l for l in lanes if l['nodes']]
    pos = {}
    maxn = max(len(l['nodes']) for l in lanes) if lanes else 1
    W = 16 + len(lanes) * LW + (len(lanes) - 1) * LGAP + 16
    H = TOP + HEAD + maxn * PITCH + BOTTOM + 24
    parts = []
    for i, l in enumerate(lanes):
        lx = 16 + i * (LW + LGAP)
        parts.append(f'<div class="gv-lane" style="left: {lx}px; top: {TOP}px; width: {LW}px; height: {H - TOP - 16}px"><span class="gv-lt">{html.escape(l["title"])}</span></div>')
        for j, n in enumerate(l['nodes']):
            x, y = lx + LPAD, TOP + HEAD + j * PITCH
            pos[n['id']] = (i, x, y)
    svg = [markers(key)]
    gap_use, side_use, chan_use = {}, {}, 0
    for e in edges:
        if e['s'] not in pos or e['t'] not in pos or e['s'] == e['t']: continue
        li, sx, sy = pos[e['s']]; lj, tx, ty = pos[e['t']]
        syc, tyc = sy + NH / 2, ty + NH / 2
        if li == lj:
            k = side_use.get(li, 0); side_use[li] = k + 1
            x = sx + NW + 10 + k * 7
            pts = [(sx + NW, syc + 6), (x, syc + 6), (x, tyc - 6), (tx + NW, tyc - 6)]
        elif lj == li + 1:
            g = li; k = gap_use.get(g, 0); gap_use[g] = k + 1
            x = sx + NW + 12 + (k % 6) * 7
            pts = [(sx + NW, syc), (x, syc), (x, tyc), (tx, tyc)]
        elif lj == li - 1:
            g = lj; k = gap_use.get(g, 0); gap_use[g] = k + 1
            x = sx - 12 - (k % 6) * 7
            pts = [(sx, syc), (x, syc), (x, tyc), (tx + NW, tyc)]
        else:
            # long span: through a channel under the lanes
            chan_use += 1; yc = H - 12 - (chan_use % 4) * 6
            if lj > li:
                g1, g2 = li, lj - 1; k1 = gap_use.get(g1, 0); gap_use[g1] = k1 + 1; k2 = gap_use.get(g2, 0); gap_use[g2] = k2 + 1
                x1 = sx + NW + 12 + (k1 % 6) * 7; x2 = tx - 12 - (k2 % 6) * 7
                pts = [(sx + NW, syc), (x1, syc), (x1, yc), (x2, yc), (x2, tyc), (tx, tyc)]
            else:
                g1, g2 = li - 1, lj; k1 = gap_use.get(g1, 0); gap_use[g1] = k1 + 1; k2 = gap_use.get(g2, 0); gap_use[g2] = k2 + 1
                x1 = sx - 12 - (k1 % 6) * 7; x2 = tx + NW + 12 + (k2 % 6) * 7
                pts = [(sx, syc), (x1, syc), (x1, yc), (x2, yc), (x2, tyc), (tx + NW, tyc)]
        svg.append(path_html(key, pts, e['k'], e.get('l')))
    nodes_html = ''.join(node_html(n, x, y) for l in lanes for n in l['nodes'] for (_, x, y) in [pos[n['id']]])
    return (f'<sc-if value="{{{{gOn.{key}}}}}" hint-placeholder-val="{{{{false}}}}"><div class="gv-scroll"><div class="gv" style="width: {W}px; height: {H}px">'
            f'<svg class="gv-edges" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true">{"".join(svg)}</svg>{"".join(parts)}{nodes_html}</div></div></sc-if>')

def stream_layout(key, streams):
    """streams: [{'title', 'stages': [{'node', 'caps': [node]}]}]."""
    SW, SG, CH, CG = 176, 56, 46, 10
    maxst = max(len(s['stages']) for s in streams)
    W = 16 + maxst * (SW + SG) + 16
    parts, svg = [], [markers(key)]
    y = TOP
    for s in streams:
        maxc = max([len(st['caps']) for st in s['stages']] + [0])
        bh = HEAD + NH + 18 + maxc * (CH + CG) + 16
        parts.append(f'<div class="gv-band" style="left: 16px; top: {y}px; width: {W - 32}px; height: {bh}px"><span class="gv-lt">{html.escape(s["title"])}</span></div>')
        sx0 = 16 + 20
        for i, st in enumerate(s['stages']):
            x, sy = sx0 + i * (SW + SG), y + HEAD
            parts.append(node_html(st['node'], x, sy))
            if i + 1 < len(s['stages']):
                svg.append(path_html(key, [(x + NW, sy + NH / 2), (x + NW + SG, sy + NH / 2)], 'triggering'))
            for j, c in enumerate(st['caps']):
                cy = sy + NH + 18 + j * (CH + CG)
                parts.append(node_html(c, x, cy, NW, CH))
                if j == 0: svg.append(path_html(key, [(x + NW / 2, cy), (x + NW / 2, sy + NH)], 'serving'))
                else: svg.append(path_html(key, [(x + NW / 2 - 60 + j * 14, cy), (x + NW / 2 - 60 + j * 14, sy + NH)], 'serving'))
        y += bh + 24
    H = y + 8
    return (f'<sc-if value="{{{{gOn.{key}}}}}" hint-placeholder-val="{{{{false}}}}"><div class="gv-scroll"><div class="gv" style="width: {W}px; height: {H}px">'
            f'<svg class="gv-edges" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true">{"".join(svg)}</svg>{"".join(parts)}</div></div></sc-if>')

def build_all(D):
    E = {e['id']: e for e in D['elements']}; N = D['notation']; R = D['relations']
    APPS = D['applications']; PF = {p['id']: p for p in D['portfolios']}
    C2A = {c: a for a, A in APPS.items() for c in A.get('components', [])}
    def node(i, change=None, muted=False):
        e = E[i]; n = N.get(e['kind'], {'layer': 'other', 'shape': 'square', 'name': e['kind']})
        return {'id': i, 'title': e['title'], 'kind': e['kind'], 'layer': n['layer'], 'shape': n['shape'], 'kname': n['name'], 'change': change, 'muted': muted}
    def comp(a): return APPS[a]['components'][0]
    def inP(i, tag): e = E.get(i); return not e or not e.get('chain') or not e.get('plateaus') or tag in e['plateaus']
    blocks = []
    # --- motivation
    kinds = ['stakeholder', 'driver', 'assessment', 'goal', 'outcome', 'requirement']
    lanes = [{'title': {'stakeholder': 'Stakeholders', 'driver': 'Drivers', 'assessment': 'Assessments', 'goal': 'Goals', 'outcome': 'Outcomes', 'requirement': 'Requirements'}[k], 'nodes': [node(e['id']) for e in D['elements'] if e['kind'] == k]} for k in kinds]
    ids = {n['id'] for l in lanes for n in l['nodes']}
    edges = [r for r in R if r['s'] in ids and r['t'] in ids]
    blocks.append(lane_layout('motivation', lanes, edges, 'Motivation'))
    # --- value streams
    vs = [e for e in D['elements'] if e['kind'] == 'value-stream' and not any(r['t'] == e['id'] and r['k'] == 'composition' for r in R)]
    streams = []
    for v in vs:
        stages = [r['t'] for r in R if r['s'] == v['id'] and r['k'] == 'composition']
        # order by triggering
        nxt = {r['s']: r['t'] for r in R if r['k'] == 'triggering' and r['s'] in stages}
        first = [s for s in stages if s not in nxt.values()]; order = []
        cur = first[0] if first else stages[0]
        while cur and cur not in order: order.append(cur); cur = nxt.get(cur)
        streams.append({'title': v['title'], 'stages': [{'node': node(s), 'caps': [node(r['s']) for r in R if r['t'] == s and r['k'] == 'serving']} for s in order]})
    blocks.append(stream_layout('valuestreams', streams))
    # --- cooperation per portfolio (target plateau), gap per portfolio, chain per portfolio
    flows = D['flows']
    for p in D['portfolios']:
        mine = [a for a in p['applications'] if inP(comp(a), 'target')]
        myc = {comp(a) for a in mine}
        fl = [f for f in flows if (f['source'] in myc or f['target'] in myc) and inP(f['source'], 'target') and inP(f['target'], 'target')]
        others = sorted({C2A[x] for f in fl for x in (f['source'], f['target']) if C2A.get(x) and C2A[x] not in mine})
        half = (len(mine) + 1) // 2 if len(mine) > 6 else len(mine)
        lanes = [{'title': p['title'], 'nodes': [node(comp(a)) for a in mine[:half]]}]
        if half < len(mine): lanes.append({'title': p['title'] + ' (continued)', 'nodes': [node(comp(a)) for a in mine[half:]]})
        for q in D['portfolios']:
            if q['id'] == p['id']: continue
            ns = [node(comp(a), muted=True) for a in others if APPS[a]['portfolio'] == q['id']]
            if ns: lanes.append({'title': q['title'], 'nodes': ns})
        blocks.append(lane_layout('coop_' + SID(p['id']), lanes, [{'s': f['source'], 't': f['target'], 'k': 'flow', 'l': f['title']} for f in fl], ''))
        L = D['landscapes'][p['id']]
        for gi, g in enumerate(L['gaps']):
            items = {it['id']: it['change'] for it in g['items'] if E[it['id']]['kind'] == 'application-component'}
            lanes = [{'title': t, 'nodes': [node(i, change=c) for i, c in items.items() if c == k]} for k, t in [('new', 'New'), ('changed', 'Changed'), ('retired', 'Retired')]]
            fl2 = [f for f in flows if (f['source'] in items or f['target'] in items) and (inP(f['source'], g['to']) or f['source'] in items) and (inP(f['target'], g['to']) or f['target'] in items)]
            neigh = sorted({x for f in fl2 for x in (f['source'], f['target']) if x not in items and x in E})
            lanes.append({'title': 'Unchanged neighbours', 'nodes': [node(x, muted=True) for x in neigh]})
            blocks.append(lane_layout(f'gap_{SID(p["id"])}_{gi}', lanes, [{'s': f['source'], 't': f['target'], 'k': 'flow', 'l': f['title']} for f in fl2], ''))
        reqs = [e['id'] for e in D['elements'] if e['kind'] == 'requirement' and e.get('portfolio') == p['id']]
        abbs = sorted({r['s'] for r in R if r['t'] in reqs and r['k'] == 'realization' and E[r['s']]['level'] == 'abb'})
        sbbs = sorted({r['s'] for r in R if r['t'] in abbs and r['k'] == 'realization' and E[r['s']]['level'] == 'sbb' and inP(r['s'], 'target')})
        lanes = [{'title': 'Requirements', 'nodes': [node(i) for i in reqs]}, {'title': 'Architecture building blocks', 'nodes': [node(i) for i in abbs]}, {'title': 'Solution building blocks · target', 'nodes': [node(i) for i in sbbs]}]
        ids = set(reqs) | set(abbs) | set(sbbs)
        blocks.append(lane_layout('chain_' + SID(p['id']), lanes, [r for r in R if r['k'] == 'realization' and r['s'] in ids and r['t'] in ids], ''))
    # --- inside per application
    for a, A in APPS.items():
        own = [e['id'] for e in D['elements'] if e.get('scopeType') == 'application' and e.get('application') == a]
        c = comp(a)
        srcs = sorted({f['source'] for f in flows if f['target'] == c}); dsts = sorted({f['target'] for f in flows if f['source'] == c})
        tech = sorted({r['s'] for r in R if r['t'] == c and r['k'] == 'serving' and E[r['s']]['level'] == 'sbb' and E[r['s']].get('scopeType') == 'enterprise'})
        order = {'application-component': 0, 'application-interface': 1, 'application-service': 2, 'data-object': 3}
        own.sort(key=lambda i: (order.get(E[i]['kind'], 9), E[i]['title']))
        lanes = [{'title': 'Sends to it', 'nodes': [node(x, muted=True) for x in srcs]},
                 {'title': A['title'], 'nodes': [node(x) for x in own]},
                 {'title': 'Receives from it', 'nodes': [node(x, muted=True) for x in dsts]},
                 {'title': 'Platforms', 'nodes': [node(x, muted=True) for x in tech]}]
        ids = set(own) | set(srcs) | set(dsts) | set(tech)
        edges = [r for r in R if r['s'] in ids and r['t'] in ids and r['k'] in ('flow', 'composition', 'access', 'serving', 'aggregation')]
        edges = [e for e in edges if not (e['k'] == 'serving' and e.get('l') == 'supports')]
        # platform lane is on the right: draw serving from platform to component as lane 3 -> 1 (backward)
        blocks.append(lane_layout('inside_' + SID(a), lanes, [{'s': e['s'], 't': e['t'], 'k': e['k'], 'l': e.get('l', '')} for e in edges], ''))
    return ''.join(blocks)

if __name__ == '__main__':
    import sys
    D = json.load(open(sys.argv[1], encoding='utf-8'))
    h = build_all(D); print(len(h), h.count('<sc-if'))
