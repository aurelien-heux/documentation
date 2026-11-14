"""Catalogue lab: four reductions of the architecture catalogue, same shell, same Meridian Bank data.
usage: ARCH_DATA=arch_data.json python3 build_catlab.py <out .dc.html>"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # shell.py, navgen.py, markup_check.py live one level up in the export bundle
import build_arch as B
from build_arch import sif, sfor, chip, chg, track, tile, I_SEARCH, I_CHEV, S, ROLE_CHIPS, HEADER, RAIL, NAVBAR, SUBHEADER, ELEMENT, TOAST, CSS

OUT = sys.argv[1]

LAB_CSS = CSS + r"""
.labbar{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:8px 12px;border-radius:12px;background:#FFFFFF;border:1px solid #CAC4CF}
.labnote{display:flex;flex-direction:column;gap:4px;padding:12px 16px;border-radius:12px;background:#FFFFFF;border:1px solid #CAC4CF;font-size:13px;line-height:19px;color:#1C1B1E}
.labnote b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif}
.labnote .meta{line-height:17px}
.tbar{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.tn .path{font-size:11px;color:#48454E}
.explorer{display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap}
.xtree{flex:0 0 260px;border:1px solid #CAC4CF;border-radius:12px;background:#fff;overflow:hidden;min-width:0}
.xmain{flex:999 1 480px;min-width:0;display:flex;flex-direction:column;gap:10px}
.xn{display:flex;align-items:center;gap:6px;min-height:40px;border-top:1px solid #F2EBFA;padding-right:8px}
.xn:first-child{border-top:0}
.xn .tnb{flex:1;min-width:0;display:flex;align-items:center;gap:8px;background:none;border:0;padding:6px 0;font:inherit;text-align:left;cursor:pointer;color:inherit;border-radius:8px}
.xn .tnb b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:13px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.xn.xn-on{background:#E3DFFF}
.xn .tog{width:28px;height:28px;border:0;border-radius:8px;background:transparent;color:#48454E;font-size:12px;cursor:pointer;flex:none;display:inline-grid;place-items:center}
.facets{display:flex;flex-direction:column;gap:14px}
.facet{display:flex;flex-direction:column;gap:2px}
.facet button{display:flex;align-items:center;gap:8px;padding:6px 10px;border:0;border-radius:8px;background:none;font:inherit;font-size:13px;color:#1C1B1E;text-align:left;cursor:pointer}
.facet button:hover{background:rgba(53,48,126,.06)}
.facet .f-on{background:#E3DFFF;font-weight:600}
.facet .cnt{margin-left:auto;font-size:11px;color:#48454E}
.crumb{display:flex;align-items:center;gap:6px;font-size:13px;color:#48454E;flex-wrap:wrap}
.crumb b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;color:#1C1B1E;font-size:16px}
.bigsearch{display:flex;align-items:center;gap:12px;height:56px;padding:0 18px;border:1px solid #79757F;border-radius:16px;background:#FFFFFF;max-width:720px}
.bigsearch input{flex:1;min-width:0;border:0;outline:0;background:transparent;font:400 16px 'Open Sans',system-ui,sans-serif;color:#1C1B1E}
.starts{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}
.start{display:flex;flex-direction:column;gap:6px;padding:14px 16px;border:1px solid #CAC4CF;border-radius:12px;background:#fff;font:inherit;text-align:left;cursor:pointer;color:#1C1B1E}
.start:hover{border-color:#35307E}
.start b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:14px;display:flex;align-items:center;gap:8px}
.start span{font-size:12px;color:#48454E}
.start .n{margin-left:auto}
.grp{display:flex;flex-direction:column;gap:6px}
.grp .lbl{display:flex;align-items:center;gap:8px}
.placeholder{display:flex;gap:16px;align-items:center;padding:24px;border:1px solid #CAC4CF;border-radius:12px;background:#FAF4FF;font-size:14px;color:#48454E}
"""

LAB_JS = r"""
  labVals() {
    const s = this.state, self = this, q = s.q.trim().toLowerCase(), V = s.variant || 'A';
    const variants = [['A', 'One tree · adopted'], ['B', 'Explorer'], ['C', 'Facets'], ['D', 'Search first']];
    const NOTES = {
      A: ['A · One tree, one field — adopted (2026-11-03)', 'The tree is the catalogue. One search field, one Group by (portfolio or layer), expand and collapse. An application node carries its TIME, owner and hosting and links to its fact sheet, so the Applications table is not needed; All elements is not needed either, because a search flattens the tree into the matching elements with their path.', 'Removed: the Applications · Tree · All elements segments, the level chips, the scope select. Kept: one field, one toggle.'],
      B: ['B · Explorer: tree on the left, table on the right', 'The left tree holds only containers (the enterprise shared blocks by layer, each portfolio and its applications); selecting one shows its elements in the table on the right, with the search narrowing the table. The tree is the only filter; the columns carry the facts (type, owner, plateaus, change, status).', 'Removed: segments, level chips, scope select, leaf rows in the tree. Kept: one field, one selection.'],
      C: ['C · Facets: two side lists, one table', 'No tree. A side list with two facets, Where (enterprise shared, each portfolio) and Layer, each with counts; one table of elements with the search. Closest to the current All elements, with the filters moved to the side and the Applications table dropped (an application is a row like any other, its facts in the columns).', 'Removed: segments, tree, level chips. Kept: one field, two facets.'],
      D: ['D · Search first', 'One field. Empty, it offers four starting points (applications, changes in progress, requirements, capabilities) that open a table on that kind; typing shows the results grouped by type, eight per group. Fast for people who know what they look for; shows little of what exists, like the Docs way in C that was not adopted.', 'Removed: everything but the field and four cards.'],
    };
    const n = NOTES[V];
    const out = { labVariants: variants.map(v => ({ id: v[0], label: v[0] + ' · ' + v[1], on: V === v[0], cls: V === v[0] ? 'chip-on' : '', pick: self.set({ variant: v[0], q: '' }) })), labTitle: n[0], labText: n[1], labDelta: n[2],
      vA: V === 'A', vB: V === 'B', vC: V === 'C', vD: V === 'D', labArea: self.state.area };
    const match = e => !q || (e.title + ' ' + e.id + ' ' + kindName(e) + ' ' + (e.owner || '')).toLowerCase().indexOf(q) >= 0;
    const nonDd = D.elements.filter(e => e.level !== 'dd' && e.level !== 'adr');
    // ---- A: flat results when searching
    out.aFlat = !!q; out.aRows = q ? nonDd.filter(match).sort(byTitle).slice(0, 80).map(e => self.rowOf(e)) : []; out.aN = q ? nonDd.filter(match).length + ' elements match' : self.state.treeN || '';
    // ---- B: explorer
    const bSel = s.bNode || 'pf:corporate';
    const open = s.open; const isOpen = (id, dflt) => open[id] == null ? !!dflt : !!open[id];
    const tog = id => () => { const o = Object.assign({}, self.state.open); o[id] = !isOpen(id, false); self.setState({ open: o }); };
    const bn = [];
    const node = (id, label, sub, depth, n, kids, dflt, extra) => { const o = isOpen(id, dflt); bn.push(Object.assign({ id, label, sub, n: String(n), depth, pad: 'padding-left: ' + (8 + depth * 18) + 'px', hasKids: !!kids, noKids: !kids, open: o, chev: o ? '▾' : '▸', toggle: tog(id), on: bSel === id, cls: bSel === id ? 'xn-on' : '', pick: self.set({ bNode: id }), hasTile: false, layer: '', kind: '' }, extra || {})); if (o && kids) kids(); };
    const ent = nonDd.filter(e => e.scopeType === 'enterprise' || !e.scopeType);
    node('ent', D.enterprise.title + ' · shared', 'enterprise scope', 0, ent.length, () => LAYER_ORDER.forEach(l => { const xs = ent.filter(e => layerOf(e) === l); if (xs.length) node('ent/' + l, D.layers[l], '', 1, xs.length, null, false); }), true, { hasTile: true, layer: 'strategy', kind: 'capability' });
    D.portfolios.forEach(p => { const pfEls = nonDd.filter(e => e.scopeType === 'portfolio' && e.portfolio === p.id); const total = pfEls.length + p.applications.reduce((k, a) => k + nonDd.filter(e => e.scopeType === 'application' && e.application === a).length, 0);
      node('pf:' + p.id, p.title, p.applications.length + ' applications', 0, total, () => { node('pfel:' + p.id, 'Portfolio building blocks', 'processes, services, requirements, changes, plateaus', 1, pfEls.length, null, false); p.applications.forEach(a => node('app:' + a, APPS[a].title, TIME[APPS[a].time][2] + ' · ' + APPS[a].owner, 1, nonDd.filter(e => e.scopeType === 'application' && e.application === a).length, null, false, { hasTile: true, layer: 'application', kind: 'application-component' })); }, p.id === 'corporate'); });
    out.bNodes = bn;
    let bEls, bTitle, bCrumb = '';
    if (bSel === 'ent') { bEls = ent; bTitle = D.enterprise.title + ' · shared'; }
    else if (bSel.indexOf('ent/') === 0) { const l = bSel.slice(4); bEls = ent.filter(e => layerOf(e) === l); bTitle = D.layers[l]; bCrumb = D.enterprise.title + ' · shared'; }
    else if (bSel.indexOf('pf:') === 0) { const p = bSel.slice(3); bEls = nonDd.filter(e => (e.scopeType === 'portfolio' && e.portfolio === p) || (e.scopeType === 'application' && APPS[e.application] && APPS[e.application].portfolio === p)); bTitle = PF[p].title; }
    else if (bSel.indexOf('pfel:') === 0) { const p = bSel.slice(5); bEls = nonDd.filter(e => e.scopeType === 'portfolio' && e.portfolio === p); bTitle = 'Portfolio building blocks'; bCrumb = PF[p].title; }
    else { const a = bSel.slice(4); bEls = nonDd.filter(e => e.scopeType === 'application' && e.application === a); bTitle = APPS[a].title; bCrumb = PF[APPS[a].portfolio].title; }
    const bm = bEls.filter(match).sort((a, b) => (LAYER_ORDER.indexOf(layerOf(a)) - LAYER_ORDER.indexOf(layerOf(b))) || a.title.localeCompare(b.title));
    out.bTitle = bTitle; out.bCrumb = bCrumb; out.hasBCrumb = !!bCrumb; out.bN = bm.length + ' elements' + (q ? ' match' : ''); out.bRows = bm.slice(0, 120).map(e => self.rowOf(e));
    out.bIsApp = bSel.indexOf('app:') === 0; out.bGoApp = bSel.indexOf('app:') === 0 ? self.openApp(bSel.slice(4)) : null;
    // ---- C: facets
    const where = s.cWhere || 'all', layer = s.cLayer || 'all';
    const inWhere = e => where === 'all' ? true : where === 'ent' ? (e.scopeType === 'enterprise' || !e.scopeType) : (e.portfolio === where || (APPS[e.application] || {}).portfolio === where);
    const inLayer = e => layer === 'all' || layerOf(e) === layer;
    const base = nonDd.filter(match);
    out.cWhere = [['all', 'Everything'], ['ent', D.enterprise.title + ' · shared']].concat(D.portfolios.map(p => [p.id, p.title])).map(w => ({ id: w[0], label: w[1], n: base.filter(e => inLayer(e) && (w[0] === 'all' || (w[0] === 'ent' ? (e.scopeType === 'enterprise' || !e.scopeType) : (e.portfolio === w[0] || (APPS[e.application] || {}).portfolio === w[0])))).length, on: where === w[0], cls: where === w[0] ? 'f-on' : '', pick: self.set({ cWhere: w[0] }) }));
    out.cLayer = [['all', 'All layers']].concat(LAYER_ORDER.filter(l => nonDd.some(e => layerOf(e) === l)).map(l => [l, D.layers[l]])).map(w => ({ id: w[0], label: w[1], n: base.filter(e => inWhere(e) && (w[0] === 'all' || layerOf(e) === w[0])).length, on: layer === w[0], cls: layer === w[0] ? 'f-on' : '', pick: self.set({ cLayer: w[0] }) }));
    const cm = base.filter(e => inWhere(e) && inLayer(e)).sort((a, b) => (LAYER_ORDER.indexOf(layerOf(a)) - LAYER_ORDER.indexOf(layerOf(b))) || a.title.localeCompare(b.title));
    out.cN = cm.length + ' elements'; out.cRows = cm.slice(0, 120).map(e => self.rowOf(e));
    // ---- D: search first
    const dKind = s.dKind || null;
    const starts = [['application-component', 'Applications', 'with TIME, owner, hosting'], ['work-package', 'Changes', 'work packages in progress'], ['requirement', 'Requirements', 'with acceptance rows'], ['capability', 'Capabilities', 'the capability map, as a list']];
    out.dStarts = starts.map(k => ({ id: k[0], label: k[1], sub: k[2], n: nonDd.filter(e => e.kind === k[0]).length, layer: layerOf({ kind: k[0] }), kind: k[0], pick: self.set({ dKind: k[0], q: '' }) }));
    out.dEmpty = !q && !dKind; out.dKindOn = !q && !!dKind; out.dSearching = !!q;
    out.dKindTitle = dKind ? (starts.find(k => k[0] === dKind) || [])[1] || dKind : ''; out.dClearKind = self.set({ dKind: null });
    out.dKindRows = dKind && !q ? nonDd.filter(e => e.kind === dKind).sort(byTitle).map(e => self.rowOf(e)) : [];
    const dm = q ? nonDd.filter(match) : [];
    const kinds = uniq(dm.map(e => e.kind)).sort((a, b) => LAYER_ORDER.indexOf(layerOf({ kind: a })) - LAYER_ORDER.indexOf(layerOf({ kind: b })));
    out.dGroups = kinds.map(k => { const xs = dm.filter(e => e.kind === k).sort(byTitle); const all = !!(s.dMore || {})[k]; return { kind: k, label: (NOTE[k] || {}).name || k, layer: layerOf({ kind: k }), n: xs.length, rows: (all ? xs : xs.slice(0, 8)).map(e => self.rowOf(e)), hasMore: xs.length > 8 && !all, more: () => self.setState({ dMore: Object.assign({}, self.state.dMore || {}, { [k]: true }) }), rest: xs.length - 8 }; });
    out.dN = dm.length + ' results in ' + kinds.length + ' types';
    return out;
  }
"""

logic = B.logic
logic = logic.replace("decisions: {}, note: '', toast: null, pfFilter: 'all',", "decisions: {}, note: '', toast: null, pfFilter: 'all', variant: 'A', bNode: 'pf:corporate', cWhere: 'all', cLayer: 'all', dKind: null, dMore: {},")
logic = logic.replace("  renderVals() {\n    return Object.assign({}, this.simVals(), this.shellVals(), this.viewVals(), this.catVals(), this.pageVals(), this.procVals(), this.arbVals());\n  }",
                      LAB_JS + "  renderVals() {\n    return Object.assign({}, this.simVals(), this.shellVals(), this.viewVals(), this.catVals(), this.pageVals(), this.procVals(), this.arbVals(), this.labVals());\n  }")
assert 'labVals' in logic and 'variant:' in logic

ROW = lambda cols: '<tr class="rowb" onClick="{{e.go}}"><td class="td"><span class="tt">' + tile('e.layer', 'e.k') + '<span class="ttx"><b>{{e.title}}</b><span>{{e.kind}}' + cols + '</span></span></span></td><td class="td mono" style="font-size: 12px">{{e.owner}}</td><td class="td">' + track('e.track') + '</td><td class="td">' + chg('e.change') + '</td><td class="td">' + chip('e.status', 'sm') + '</td></tr>'
TABLE = lambda lst, extra='': '<div class="tb"><table><thead><tr><th class="th">Element</th><th class="th">Owner</th><th class="th">Plateaus</th><th class="th">Change</th><th class="th">Status</th></tr></thead><tbody>' + sfor(lst, 'e', ROW(extra), 8) + '</tbody></table></div>'
SEARCH = ('<div class="srch">' + I_SEARCH + '<label for="lab-q" style="position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0)">Search the catalogue</label><input id="lab-q" type="text" placeholder="Search by name, id, type or owner" value="{{q}}" onChange="{{onQ}}">' + sif('hasQ', '<button type="button" aria-label="Clear" onClick="{{clearQ}}">✕</button>') + '</div>')

TREE_NODES = sfor('tree', 'n',
      sif('n.isLeaf', '<div class="tn" role="treeitem" style="{{n.pad}}"><span class="leafsp"></span><button type="button" class="tnb" onClick="{{n.go}}">' + tile('n.layer', 'n.kind') + '<span class="tnt"><b>{{n.title}}</b><span>{{n.sub}}</span></span></button><span class="tnr">' + chg('n.change') + track('n.track') + chip('n.status', 'sm') + '</span></div>')
      + sif('n.open', '<div class="tn {{n.cls}}" role="treeitem" aria-expanded="true" style="{{n.pad}}"><button type="button" class="tog" aria-label="Collapse" onClick="{{n.toggle}}">▾</button><button type="button" class="tnb" onClick="{{n.toggle}}">' + sif('n.hasTile', tile('n.layer', 'n.kind')) + '<span class="tnt"><b>{{n.title}}</b><span>{{n.sub}}</span></span></button><span class="tnr">' + sif('n.hasGoApp', '<button type="button" class="lnk" style="font-size: 12px" onClick="{{n.goApp}}">fact sheet</button>') + chg('n.change') + track('n.track') + '<span class="cnt">{{n.n}}</span></span></div>')
      + sif('n.isBranchClosed', '<div class="tn {{n.cls}}" role="treeitem" aria-expanded="false" style="{{n.pad}}"><button type="button" class="tog" aria-label="Expand" onClick="{{n.toggle}}">▸</button><button type="button" class="tnb" onClick="{{n.toggle}}">' + sif('n.hasTile', tile('n.layer', 'n.kind')) + '<span class="tnt"><b>{{n.title}}</b><span>{{n.sub}}</span></span></button><span class="tnr">' + sif('n.hasGoApp', '<button type="button" class="lnk" style="font-size: 12px" onClick="{{n.goApp}}">fact sheet</button>') + chg('n.change') + track('n.track') + '<span class="cnt">{{n.n}}</span></span></div>'), 12)

VAR_A = sif('vA', '<div class="tbar">' + SEARCH + '<span class="lbl">Group by</span><div class="seg small" role="group" aria-label="Group by">' + sfor('treeModes', 'm', '<button type="button" class="{{m.cls}}" aria-pressed="{{m.on}}" onClick="{{m.pick}}">{{m.label}}</button>', 2) + '</div><span class="meta">{{aN}}</span><span style="flex: 1"></span><button type="button" class="btn x" onClick="{{expandAll}}">Expand all</button><button type="button" class="btn x" onClick="{{collapseAll}}">Collapse all</button></div>'
  + sif('aFlat', '<div class="tree">' + sfor('aRows', 'e', '<div class="tn" style="padding-left: 12px"><button type="button" class="tnb" onClick="{{e.go}}">' + tile('e.layer', 'e.k') + '<span class="tnt"><b>{{e.title}}</b><span class="path">{{e.kind}} · {{e.path}}</span></span></button><span class="tnr">' + chg('e.change') + track('e.track') + chip('e.status', 'sm') + '</span></div>', 8) + '</div>')
  + sif('aFlatNot', '<div class="tree" role="tree">' + TREE_NODES + '</div>'))
VAR_A = VAR_A.replace('aFlatNot', 'aTree')

VAR_B = sif('vB', '<div class="explorer"><div class="xtree" role="tree">' + sfor('bNodes', 'n', '<div class="xn {{n.cls}}" role="treeitem" style="{{n.pad}}">' + sif('n.hasKids', '<button type="button" class="tog" aria-label="Toggle" onClick="{{n.toggle}}">{{n.chev}}</button>') + sif('n.noKids', '<span class="tog"></span>') + '<button type="button" class="tnb" aria-current="{{n.on}}" onClick="{{n.pick}}">' + sif('n.hasTile', tile('n.layer', 'n.kind')) + '<b>{{n.label}}</b></button><span class="cnt">{{n.n}}</span></div>', 10) + '</div>'
  '<div class="xmain"><div class="tbar"><span class="crumb">' + sif('hasBCrumb', '<span>{{bCrumb}} ›</span>') + '<b>{{bTitle}}</b><span class="meta">{{bN}}</span>' + sif('bIsApp', '<button type="button" class="lnk" onClick="{{bGoApp}}">fact sheet</button>') + '</span><span style="flex: 1"></span>' + SEARCH.replace('lab-q', 'lab-qb') + '</div>' + TABLE('bRows', ' · {{e.scope}}') + '</div></div>')

VAR_C = sif('vC', '<div class="area"><div class="side facets"><div class="facet"><span class="lbl" style="padding: 0 10px 4px">Where</span>' + sfor('cWhere', 'w', '<button type="button" class="{{w.cls}}" aria-pressed="{{w.on}}" onClick="{{w.pick}}">{{w.label}}<span class="cnt">{{w.n}}</span></button>', 6) + '</div><div class="facet"><span class="lbl" style="padding: 0 10px 4px">Layer</span>' + sfor('cLayer', 'w', '<button type="button" class="{{w.cls}}" aria-pressed="{{w.on}}" onClick="{{w.pick}}">{{w.label}}<span class="cnt">{{w.n}}</span></button>', 6) + '</div></div>'
  '<div class="content"><div class="tbar">' + SEARCH.replace('lab-q', 'lab-qc') + '<span class="meta">{{cN}}</span></div>' + TABLE('cRows', ' · {{e.scope}}') + '</div></div>')

VAR_D = sif('vD', '<div class="bigsearch">' + I_SEARCH.replace('width="18" height="18"', 'width="22" height="22"') + '<label for="lab-qd" style="position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0)">Search the architecture model</label><input id="lab-qd" type="text" placeholder="Search the architecture model: an application, a capability, a requirement, a team…" value="{{q}}" onChange="{{onQ}}">' + sif('hasQ', '<button type="button" class="ib" aria-label="Clear" onClick="{{clearQ}}">✕</button>') + '</div>'
  + sif('dEmpty', '<span class="lbl">Start from</span><div class="starts">' + sfor('dStarts', 'k', '<button type="button" class="start" onClick="{{k.pick}}"><b>' + tile('k.layer', 'k.kind') + '{{k.label}}<span class="n">{{k.n}}</span></b><span>{{k.sub}}</span></button>', 4) + '</div>')
  + sif('dKindOn', '<div class="tbar"><span class="crumb"><button type="button" class="lnk" onClick="{{dClearKind}}">Start from</button><span>›</span><b>{{dKindTitle}}</b></span></div>' + TABLE('dKindRows', ' · {{e.scope}}'))
  + sif('dSearching', '<span class="meta">{{dN}}</span>' + sfor('dGroups', 'g', '<div class="grp"><span class="lbl">' + tile('g.layer', 'g.kind') + '{{g.label}} <span class="n">{{g.n}}</span></span>' + TABLE('g.rows', ' · {{e.scope}}') + sif('g.hasMore', '<button type="button" class="btn x" style="align-self: flex-start" onClick="{{g.more}}">Show {{g.rest}} more</button>') + '</div>', 3)))

LAB_BAR = ('<div class="labbar" role="group" aria-label="Catalogue lab"><span class="simlab">CATALOGUE LAB · PICK ONE</span>' + sfor('labVariants', 'v', '<button type="button" class="chip {{v.cls}}" aria-pressed="{{v.on}}" onClick="{{v.pick}}">{{v.label}}</button>', 4) + '</div>'
           '<div class="labnote"><b>{{labTitle}}</b><span>{{labText}}</span><span class="meta">{{labDelta}}</span></div>')
AREA_TABS = B.AREA_TABS
CAT_AREA = sif('isCat', VAR_A + VAR_B + VAR_C + VAR_D)
OTHER = sif('isViews', '<div class="placeholder"><span class="st st-info"><span class="tile">i</span>Not in the lab</span>Views and Process are on the Architecture board; this lab only changes the Catalogue.</div>') + sif('isProc', '<div class="placeholder"><span class="st st-info"><span class="tile">i</span>Not in the lab</span>Views and Process are on the Architecture board; this lab only changes the Catalogue.</div>')

BODY = ('<div style="display: flex; flex-direction: column; gap: 12px; padding: 12px; background: #ECE5F4; min-height: 100vh; box-sizing: border-box; font-family: \'Open Sans\', system-ui, sans-serif">'
        + LAB_BAR + S.sim_bar(ROLE_CHIPS) + S.sim_open('sim-host-arch')
        + '<div class="app" style="min-height: {{simFrameH}}px">' + HEADER + '<div class="bodyrow">' + RAIL + '<main>'
        + sif('noPage', SUBHEADER + AREA_TABS) + CAT_AREA + OTHER + ELEMENT
        + '</main></div>' + NAVBAR + TOAST + '</div>' + S.SIM_CLOSE + '</div>')

# A: the tree shows when not searching
logic = logic.replace("out.aFlat = !!q;", "out.aFlat = !!q; out.aTree = !q;")
assert '</script' not in logic and '</script' not in BODY
page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Catalogue lab · four reductions of the architecture catalogue</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&amp;family=Open+Sans:wght@400;600;700&amp;display=swap">
<style>
{LAB_CSS}
</style>
</helmet>
{BODY}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1440,"height":1400}}}}'>
{logic}
</script>
</body>
</html>
'''
B.emit(page, OUT)
