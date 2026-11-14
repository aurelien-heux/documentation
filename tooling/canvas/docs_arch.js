    // ---- architecture: the Corporate credit platform · Catalogue, Views, Process (markup in docs_arch.py)
    var A0 = Object.assign({ area: 'views', cat: 'all', psub: 'changes', view: 'landscape', mode: 'base', gpair: 'gap-base-target', el: null, ep: null, change: null, adr: null, arb: null, asd: false,
      trail: [], vhist: [], zoom: 1, src: false, pair: 'tr1-target', fix: {}, wrote: {}, decided: {} }, s.arch || {});
    var aset = function (o) { return set(function (e) { var p = typeof o === 'function' ? o(e) : o; return { arch: Object.assign({}, A0, p), snack: null }; }); };
    var V = {};
    var VW = DG.views, PLN = DG.plName, GAPS = DG.gaps;
    var CAT = {}; DG.cat.forEach(function (e) { CAT[e.id] = e; });
    var PAGES = { ep: null, change: null, adr: null, arb: null, asd: false };
    var snap = function () { return { area: A0.area, cat: A0.cat, psub: A0.psub, view: A0.view, mode: A0.mode, el: A0.el, ep: A0.ep, change: A0.change, adr: A0.adr, arb: A0.arb, asd: A0.asd }; };
    // open a page on top of the current one (the subheader goes back to it)
    var openP = function (o) { return aset(function () { return Object.assign({ trail: A0.trail.concat([snap()]) }, PAGES, o); }); };
    var goMain = function (o) { return aset(Object.assign({ trail: [] }, PAGES, o)); };
    var adrById = function (id) { return DG.adrs.filter(function (a) { return a.id === id; })[0]; };
    var arbById = function (id) { return DG.arbs.filter(function (a) { return a.id === id; })[0]; };
    var ST = function (st, g, w) { return { st: st, g: g, w: w }; };
    var TRK = function (pl) { return [['base', 'B'], ['tr1', 'T1'], ['target', 'T']].map(function (p) { var on = pl.indexOf(p[0]) >= 0; return { ab: p[1], name: PLN[p[0]], cls: on ? 'on' : '' }; }); };
    var trkAria = function (pl) { return 'In ' + pl.map(function (p) { return PLN[p]; }).join(', '); };
    var CHG = { new: ['+', 'New'], changed: ['Δ', 'Changed'], retired: ['−', 'Retired'], unchanged: ['=', 'Unchanged'] };
    var chgOf = function (pl, a, b, chg) { var ia = pl.indexOf(a) >= 0, ib = pl.indexOf(b) >= 0; if (!ia && !ib) return null; if (ia && ib) return chg && chg.indexOf('gap-' + a + '-' + b) >= 0 ? 'changed' : 'unchanged'; return ib ? 'new' : 'retired'; };
    var ORIGIN = { authored: 'Authored', extracted: 'Extracted from code', inferred: 'Inferred from code · draft' };
    var VERB = { serving: ['serves', 'served by'], flow: ['flows to', 'flow from'], triggering: ['triggers', 'triggered by'], realization: ['realizes', 'realized by'], assignment: ['assigned to', 'assigned from'],
      influence: ['influences', 'influenced by'], association: ['associated with', 'associated with'], access: ['accesses', 'accessed by'], composition: ['composed of', 'part of'], aggregation: ['aggregates', 'aggregated in'], specialization: ['specializes', 'specialized by'] };

    // ---- views (LikeC4 canvas)
    var vKey = VW[A0.view] ? A0.view : 'landscape', vw = VW[vKey];
    var mode = vw.modes.indexOf(A0.mode) >= 0 ? A0.mode : (A0.mode === 'gap' && vw.modes.indexOf(A0.gpair) >= 0 ? A0.gpair : (vw.modes.indexOf('base') >= 0 ? 'base' : vw.modes[0]));
    var isGap = !!GAPS[mode];
    var visN = function (n, m) { m = m || mode; if (GAPS[m]) return n.pl.indexOf(GAPS[m][0]) >= 0 || n.pl.indexOf(GAPS[m][1]) >= 0; return n.pl.indexOf(m) >= 0; };
    DG.order.forEach(function (k) { VW[k].modes.forEach(function (m) { V['lcv_' + k + '_' + m.replace(/-/g, '_')] = k === vKey && m === mode; }); });
    var elK = A0.el && vw.nodes[A0.el] && visN(vw.nodes[A0.el]) ? A0.el : null;
    var allKeys = {}; DG.order.forEach(function (k) { Object.keys(VW[k].nodes).forEach(function (n) { allKeys[n] = true; }); });
    Object.keys(allKeys).forEach(function (k) { V['lcOn_' + k] = k === elK; V['lcPick_' + k] = aset({ el: k === elK ? null : k }); });
    var SW = sim.simW || 1374, navW = SW < 600 ? 0 : 80, side = SW >= 1200 && !s.asOpen ? 256 : 0, paneW = s.asOpen && SW >= 1200 ? 420 : 0;
    var avail = Math.max(280, SW - navW - (SW < 600 ? 32 : 64) - side - paneW - 24);
    var fit = Math.max(.42, Math.min(1, avail / vw.w)), zoom = Math.round(fit * A0.zoom * 100) / 100;
    var baseModes = vw.base.filter(function (m) { return m !== 'gap'; });
    var lcModes = baseModes.concat(vw.base.indexOf('gap') >= 0 ? ['gap'] : []).map(function (m) { var on = m === 'gap' ? isGap : m === mode; return { label: m === 'gap' ? 'Gap' : PLN[m], on: on, pick: aset({ mode: m === 'gap' ? (vw.modes.indexOf(A0.gpair) >= 0 ? A0.gpair : vw.modes.filter(function (x) { return GAPS[x]; }).slice(-1)[0]) : m, el: null }) }; });
    var SHORT = { base: 'B', tr1: 'T1', target: 'T' }, narrow = (sim.simW || 1374) < 600;
    var lcPairs = vw.modes.filter(function (m) { return GAPS[m]; }).map(function (m) { return { label: narrow ? SHORT[GAPS[m][0]] + ' → ' + SHORT[GAPS[m][1]] : PLN[GAPS[m][0]] + ' → ' + PLN[GAPS[m][1]], on: m === mode, pick: aset({ mode: m, gpair: m, el: null }) }; });
    var PH = {}; DG.phases.forEach(function (p) { PH[p[0]] = p; });
    var note = vw.modes.length === 1 ? 'One view of the target, generated from the model.' : isGap ? 'New and changed elements carry a chip; retired ones are struck through; unchanged ones are faded.' : mode === 'base' ? 'As it runs today.' : mode === 'tr1' ? 'Transition 1 · December 2026.' : 'Target · June 2027.';
    V.lc = { title: vw.title, sub: vw.sub, phase: PH[vw.phase][1], viewId: vw.ids[mode], zoom: zoom, h: Math.min(Math.round(vw.h * zoom) + 2, 660), hasModes: vw.modes.length > 1, isGap: isGap, note: note,
      src: vw.src[mode], srcOn: !!A0.src, srcLabel: A0.src ? 'Hide the view source' : 'Show the view source' };
    V.lcModes = lcModes; V.lcPairs = lcPairs; V.lcSel = elK || 'none';
    V.lcZin = aset({ zoom: Math.min(1.6, Math.round((A0.zoom + .2) * 10) / 10) }); V.lcZout = aset({ zoom: Math.max(.6, Math.round((A0.zoom - .2) * 10) / 10) }); V.lcFit = aset({ zoom: 1 });
    V.lcSrc = aset({ src: !A0.src }); V.lcClose = aset({ el: null });
    var openEl = function (id) { return openP({ ep: id }); };
    var ddOpen = function (id) { return set({ view: 'dd', dd: id }); };
    var lcEl = { hasNav: false, navLabel: '', nav: set({}), name: '', kind: '', layer: 'other', type: 'grouping', desc: '', hasDesc: false, owner: '', origin: '', track: [], trackAria: '', rels: [], hasRels: false, hasChg: false, chg: '', chgG: '', chgW: '', hasDd: false, open: set({}), dd: set({}) };
    if (elK) {
      var nd = vw.nodes[elK], ce = CAT[nd.id] || {}, st = isGap ? chgOf(nd.pl, GAPS[mode][0], GAPS[mode][1], nd.chg) : null;
      var rels = vw.edges.filter(function (e) { return (e[0] === elK || e[1] === elK) && visN({ pl: e[4] }) && visN(vw.nodes[e[0]]) && visN(vw.nodes[e[1]]); }).map(function (e) {
        var out = e[0] === elK, o = vw.nodes[out ? e[1] : e[0]], ok = out ? e[1] : e[0];
        return { verb: VERB[e[2]][out ? 0 : 1], name: o.name, layer: o.layer, type: o.type, label: e[3], hasLabel: !!e[3], pick: aset({ el: ok }) }; });
      lcEl = { name: nd.name, kind: nd.kind, layer: nd.layer, type: nd.type, desc: ce.desc || (nd.ext ? 'Belongs to another application; shown because the platform depends on it.' : ''), owner: ce.owner || '—', origin: ORIGIN[ce.origin] || 'Authored',
        track: TRK(nd.pl), trackAria: trkAria(nd.pl), rels: rels, hasRels: rels.length > 0, hasChg: !!st && st !== 'unchanged', chg: st || '', chgG: st ? CHG[st][0] : '', chgW: st ? CHG[st][1] : '',
        hasDd: !!(ce.dd && ce.dd.length), open: openEl(nd.id), dd: ce.dd && ce.dd.length ? ddOpen(ce.dd[0]) : set({}) };
      lcEl.hasDesc = !!lcEl.desc;
    }
    // LikeC4 navigation: open a child view (or a detailed design) from an element, breadcrumbs, back
    var vh = A0.vhist || [], here = { view: vKey, mode: mode, el: elK };
    var modeIn = function (t, pref) { return t.modes.indexOf(pref) >= 0 ? pref : (t.modes.indexOf(mode) >= 0 ? mode : (t.modes.indexOf('target') >= 0 ? 'target' : t.modes[0])); };
    DG.order.forEach(function (k) { Object.keys(VW[k].nodes).forEach(function (nk) { var n = VW[k].nodes[nk]; if (!n.nav && !n.dd) return;
      V['lcNav_' + k + '_' + nk] = n.nav ? aset(function () { return { view: n.nav, mode: modeIn(VW[n.nav], n.navMode), el: null, vhist: vh.concat([{ view: k, mode: mode, el: nk }]) }; }) : set({ view: 'dd', dd: n.dd }); }); });
    var chain = []; for (var c = vKey; c; c = VW[c].parent) chain.unshift(c);
    V.lcCrumbs = chain.map(function (k, i) { return { label: VW[k].title, cur: i === chain.length - 1, more: i < chain.length - 1, pick: i === chain.length - 1 ? set({}) : aset({ view: k, mode: modeIn(VW[k], mode), el: null, vhist: vh.concat([here]) }) }; });
    V.lcCanBack = vh.length > 0; V.lcBack = aset(function () { var l = vh[vh.length - 1]; return { view: l.view, mode: l.mode, el: l.el, vhist: vh.slice(0, -1) }; });
    if (elK) { var nn = vw.nodes[elK]; lcEl.hasNav = !!(nn.nav || nn.dd); lcEl.navLabel = nn.nav ? 'Open the view ' + VW[nn.nav].title : nn.dd ? 'Open the detailed design · ' + DG.dds[nn.dd].layer : ''; lcEl.nav = V['lcNav_' + vKey + '_' + elK] || set({}); }
    V.lcEl = lcEl; V.lcHasEl = !!elK;

    // ---- catalogue
    var LORDER = ['motivation', 'strategy', 'business', 'application', 'technology', 'implementation'];
    var catF = A0.cat, catList = DG.cat.filter(function (e) {
      if (catF === 'all') return true; if (catF === 'dd') return e.dd.length > 0; if (catF === 'inferred') return e.origin !== 'authored'; if (catF === 'retiring') return e.pl.indexOf('target') < 0;
      if (catF === 'data') return e.type === 'data-object'; if (catF === 'application') return e.layer === 'application' && e.type !== 'data-object'; return e.layer === catF; });
    V.catRows = catList.map(function (e) {
      var c = e.pl.length < 3 ? chgOf(e.pl, 'base', 'target', []) : null;
      return { id: e.id, name: e.name, kind: e.kind, layer: e.layer, type: e.type, owner: e.owner, track: TRK(e.pl), trackAria: trkAria(e.pl), hasChg: !!c && c !== 'unchanged', noChg: !c || c === 'unchanged',
        chg: c || '', chgG: c ? CHG[c][0] : '', chgW: c ? CHG[c][1] : '', design: e.dd.length ? e.dd.length + ' file' + (e.dd.length > 1 ? 's' : '') : (/^sbb\./.test(e.id) && e.type === 'application-component' ? 'Not written' : '—'),
        origin: ORIGIN[e.origin], open: openEl(e.id) }; });
    var CATN = { all: ['All elements', 'Building blocks of the corporate credit platform, from the model'], motivation: ['Motivation', 'Stakeholders, drivers, goals, principles and requirements'], strategy: ['Strategy', 'The value stream'],
      business: ['Business', 'Roles that work in the value stream'], application: ['Application', 'Components, interfaces, services, processes and events'], data: ['Data', 'Data objects and the service that owns each'],
      technology: ['Technology', 'Nodes, system software and technology services'], implementation: ['Implementation & migration', 'Plateaus, gaps and work packages'],
      dd: ['With detailed design', 'Services whose design intent is written in their repository'], inferred: ['From the code', 'Elements extracted or inferred from code: drafts until an architect authors them'], retiring: ['Retired in the target', 'What disappears by June 2027'] };
    V.catTitle = CATN[catF][0]; V.catSub = CATN[catF][1]; V.catCount = catList.length + ' of ' + DG.cat.length + ' elements';
    var countL = function (f) { return DG.cat.filter(function (e) { return f(e); }).length; };

    // ---- reviews: checks, ASD sections, readiness, decisions
    var checksOf = function (a) { return a.checks.map(function (c, i) { var key = a.id + ':' + i, fixed = !!A0.fix[key], st = fixed ? 'pass' : c[2];
      return { g: c[0], label: c[1], st: st, sc: st === 'pass' ? 'success' : st === 'warn' ? 'warning' : 'error', word: st === 'pass' ? 'Passed' : st === 'warn' ? 'Warning' : 'Failed · blocking', mark: st === 'pass' ? '✓' : st === 'warn' ? '!' : '✕',
        note: fixed ? 'Fixed in a pull request, merged · the next build re-ran the check' : c[3], hasNote: !!(fixed || c[3]),
        canFix: st !== 'pass' && (c[2] === 'fail' || /^T6/.test(c[1])), blocking: st === 'fail', fix: aset(function () { var f = Object.assign({}, A0.fix); f[key] = true; return { fix: f }; }) }; }); };
    var asdOf = function (a, key) { var v = a.asd ? a.asd[key] : ''; if (!v && key === 'nfr' && A0.wrote[a.id + ':nfr']) v = a.nfrRich || { p: 'Written.' }; return v || null; };
    var secsOf = function (a) { if (!a.asd) return []; return DG.asd.map(function (x, i) { var w = x[1] === 'w', v = w ? asdOf(a, x[2]) : null;
      var state = w ? (v ? 'Written' : 'Missing') : 'From the model'; return { n: i + 1, name: x[0], key: x[2], src: w ? 'Written' : 'From the model', state: state, badge: state === 'Missing' ? 'err' : state === 'Written' ? 'ok' : 'model', v: v, text: v && v.p ? v.p : '', missing: w && !v,
        write: aset(function () { var o = Object.assign({}, A0.wrote); o[a.id + ':' + x[2]] = true; return { wrote: o }; }) }; }); };
    var fixedOf = function (a, re) { return a.checks.some(function (c, i) { return re.test(c[1]) && (c[2] === 'pass' || A0.fix[a.id + ':' + i]); }); };
    // what the ASD must cover, and whether it does (from the sections, the checks and the reviewers)
    var coverOf = function (a) { if (!a.asd) return [];
      var ss = secsOf(a), wr = function (k) { return ss.filter(function (x) { return x.key === k; })[0]; }, adrP = (a.adrs || []).some(function (id) { return adrById(id).status === 'Proposed'; });
      var secRev = (reviewersOf(a).filter(function (r) { return r.role === 'Security'; })[0] || {}).dec;
      var C = function (t, sec, st, note) { var x = { covered: ['success', '✓', 'Covered'], partial: ['warning', '!', 'Partly'], missing: ['error', '✕', 'Missing'] }[st]; return { t: t, sec: sec, note: note, st: x[0], g: x[1], w: x[2], ok: st === 'covered' }; };
      return [ C('Scope and boundaries', '1 · Context and scope', 'covered', 'in and out of scope listed'), C('Business need with measures', '2 · Business need', 'covered', '4 measures, today and target'),
        C('Architecture overview and style', '3 · Architecture overview', 'covered', 'hexagonal services, events, MQ booking'),
        C('Requirements traced to the target', '4 · Requirements', 'covered', (a.reqs || []).length + ' of ' + (a.reqs || []).length + ' realized · T4'),
        C('Baseline and target views', '5–6 · Baseline, Target', 'covered', 'generated from the model'), C('Gap closed by work packages', '7 · Gap and transition', 'covered', 'P3 passed'),
        fixedOf(a, /^T6/) ? C('Detailed design of every new component', '8 · Detailed design', 'covered', '5 of 5 services') : C('Detailed design of every new component', '8 · Detailed design', 'partial', 'collateral-service missing · T6'),
        fixedOf(a, /^O2/) ? C('Contracts for every interface and event', '8 · Detailed design', 'covered', 'OpenAPI and AsyncAPI complete') : C('Contracts for every interface and event', '8 · Detailed design', 'missing', 'cc.limits channel · O2'),
        wr('nfr') && !wr('nfr').missing ? C('Non-functional requirements with evidence', '9 · NFR', 'covered', '5 targets with their evidence') : C('Non-functional requirements with evidence', '9 · NFR', 'missing', 'section not written'),
        secRev === 'Request changes' ? C('Threats and controls', '10 · Security', 'partial', 'Security asks for the MQ authentication · C2') : C('Threats and controls', '10 · Security', 'covered', '4 threats, their controls'),
        adrP ? C('Decisions recorded', '11 · Decisions', 'partial', 'ADR-CC-05 still proposed · D2') : C('Decisions recorded', '11 · Decisions', 'covered', 'all accepted'),
        C('Risks with owners', '12 · Risks', 'covered', '4 risks, each with an owner'), C('Open questions', '13 · Open questions', 'covered', '2 open, owners named') ]; };
    var DEC = { Approved: ['success', '✓'], 'Approve with conditions': ['success', '✓'], 'Request changes': ['warning', '!'], Pending: ['info', '…'], 'Not required': ['neutral', '–'] };
    var reviewersOf = function (a) { var d = A0.decided[a.id]; return a.reviewers.map(function (r) { var dec = (r[0] === 'Enterprise architecture' && d) ? d : r[2], x = DEC[dec] || ['neutral', '–'];
      return { role: r[0], who: r[1], dec: dec, st: x[0], g: x[1], note: r[3] || '', hasNote: !!r[3], w: dec === 'Approve with conditions' ? 'Approved with conditions' : dec === 'Request changes' ? 'Changes requested' : dec }; }); };
    var readinessOf = function (a) { if (a.decided || A0.decided[a.id] === 'Approved' || A0.decided[a.id] === 'Approve with conditions') return ['Decided', 'ok'];
      if (a.status === 'Draft') return ['Draft', 'dr'];
      var cs = checksOf(a), ss = secsOf(a), blk = cs.some(function (c) { return c.blocking; }) || ss.some(function (x) { return x.missing; });
      var att = cs.some(function (c) { return c.st === 'warn'; }) || reviewersOf(a).some(function (r) { return r.dec === 'Pending' || r.dec === 'Request changes'; });
      return blk ? ['Blocked', 'bl'] : att ? ['Needs attention', 'wn'] : ['Ready for the board', 'ok']; };
    var RDS = { ok: ['success', '✓'], wn: ['warning', '!'], bl: ['error', '✕'], dr: ['info', '…'] };
    var rdSt = function (a) { var r = readinessOf(a), x = RDS[r[1]]; return ST(x[0], x[1], r[0]); };
    var gapOf = function (from, to, wp) { var out = []; Object.keys(VW.application.nodes).forEach(function (k) { var n = VW.application.nodes[k];
      if (wp && n.wp !== wp) return; var c = chgOf(n.pl, from, to, n.chg); if (!c || c === 'unchanged') return;
      var w = DG.wps[n.wp], arbId = { wp1: 'arb.request.2026-09', wp2: 'arb.facility.2026-14', wp3: 'arb.facility.2026-14', wp4: 'arb.facility.2026-14' }[n.wp];
      out.push({ k: k, id: n.id, name: n.name, kind: n.kind, layer: n.layer, type: n.type, chg: c, chgG: CHG[c][0], chgW: CHG[c][1], track: TRK(n.pl), trackAria: trkAria(n.pl), wp: w ? w.name : '—', arb: arbId || '—',
        open: openEl(n.id), openArb: arbId ? openP({ arb: arbId }) : set({}) }); }); return out; };
    var countOf = function (rows) { var c = { new: 0, changed: 0, retired: 0 }; rows.forEach(function (r) { c[r.chg]++; }); return c.new + ' new · ' + c.changed + ' changed · ' + c.retired + ' retired'; };
    var openGap = function (from, to) { return goMain({ area: 'views', view: 'application', mode: 'gap-' + from + '-' + to, gpair: 'gap-' + from + '-' + to, el: null }); };

    // ---- process: changes (one per work package), decisions, reviews, roadmap
    var stepsOf = function (c) {
      var w = DG.wps[c.k], adrs = c.adrs.map(adrById).filter(function (a) { return a.status !== 'Superseded'; }), arbs = c.arbs.map(arbById);
      var s1 = adrs.some(function (a) { return a.status === 'Proposed'; }) ? ST('warning', '!', adrs.filter(function (a) { return a.status === 'Proposed'; }).length + ' proposed') : ST('success', '✓', adrs.length + ' accepted');
      var a0 = arbs[0], s2, s3;
      if (!a0) { s2 = ST('neutral', '–', 'Not started'); s3 = ST('neutral', '–', 'Not submitted'); }
      else {
        var rd = readinessOf(a0), ss = secsOf(a0), miss = ss.filter(function (x) { return x.missing; }).length;
        s2 = rd[0] === 'Decided' ? ST('success', '✓', 'Approved') : !a0.asd ? ST('info', '…', 'Draft') : miss ? ST('error', '✕', (13 - miss) + ' of 13') : ST('success', '✓', '13 of 13');
        s3 = rdSt(a0);
      }
      var s4 = w.state === 'In progress' ? ST('info', '›', 'In progress') : w.state === 'Done' ? ST('success', '✓', 'Delivered') : ST('neutral', '–', 'Planned');
      return [s1, s2, s3, s4];
    };
    V.chRows = DG.changes.map(function (c) { var w = DG.wps[c.k], ss = stepsOf(c), o = { name: w.name, scope: PLN[w.from] + ' → ' + PLN[w.to] + ' · ' + w.team + ' · ' + w.when, open: openP({ change: c.k }) };
      ss.forEach(function (x, i) { o['s' + (i + 1) + 'st'] = x.st; o['s' + (i + 1) + 'g'] = x.g; o['s' + (i + 1) + 'w'] = x.w; }); return o; });
    var TILE_ADR = { Accepted: ST('success', '✓', 'Accepted'), Proposed: ST('warning', '!', 'Proposed'), Superseded: ST('neutral', '–', 'Superseded') };
    V.adrRows = DG.adrs.map(function (a) { return Object.assign({ id: a.id, t: a.t, by: a.by, plateau: a.plateau, date: a.date, open: openP({ adr: a.id }) }, TILE_ADR[a.status]); });
    V.arbRows = DG.arbs.map(function (a) { return Object.assign({ id: a.id, t: a.t, by: a.by, scope: PLN[a.from] + ' → ' + PLN[a.to], board: a.board, open: openP({ arb: a.id }) }, rdSt(a)); });
    var PLS = { Live: ST('success', '✓', 'Live'), 'In progress': ST('info', '›', 'In progress'), Planned: ST('neutral', '–', 'Planned') };
    V.plats = DG.plateaus.map(function (p) { var wps = Object.keys(DG.wps).filter(function (k) { return DG.wps[k].to === p.k; }).map(function (k) { return Object.assign({}, DG.wps[k], { open: openP({ change: k }) }); });
      return Object.assign({}, p, PLS[p.state], { hasWps: wps.length > 0, wps: wps }); });
    var pair = A0.pair.split('-');
    V.gapRowsV = gapOf(pair[0], pair[1]);
    V.pairChips = [['base-tr1', 'Baseline → Transition 1', 'B → T1'], ['tr1-target', 'Transition 1 → Target', 'T1 → T'], ['base-target', 'Baseline → Target', 'B → T']].map(function (p) { return { label: narrow ? p[2] : p[1], on: A0.pair === p[0], pick: aset({ pair: p[0] }) }; });
    V.gapSummary = countOf(V.gapRowsV) + ' · application cooperation view';
    V.gapOnView = openGap(pair[0], pair[1]);
    V.adrNew = set({ snack: 'Opens a pull request with an ADR template in model/adr. It is accepted through the review, never edited after.' });
    V.adrEdit = set({ snack: 'An accepted decision is not edited: propose a new decision that supersedes it.' });

    // ---- area navigation
    var area = A0.area;
    var openChanges = DG.changes.filter(function (c) { return DG.wps[c.k].state !== 'Done'; }).length;
    V.areaTabs = [['catalogue', 'Catalogue', DG.cat.length], ['views', 'Views', DG.order.length], ['process', 'Process', openChanges + ' open']].map(function (t) { var on = area === t[0];
      return { label: t[1], n: t[2], on: on, cls: on ? 'tab-on' : '', pick: goMain({ area: t[0] }) }; });
    var item = function (label, cur, pick, o) { return Object.assign({ lv: '', label: label, cur: cur ? 'page' : 'false', pick: pick, hasTile: false, hasSwatch: false, hasSub: false, sub: '', hasN: false, n: '', layer: 'other', type: '' }, o || {}); };
    if (area === 'catalogue') {
      V.anavLabel = 'Catalogue';
      V.anav = [ { label: 'By layer', items: [item('All elements', catF === 'all', aset({ cat: 'all' }), { hasN: true, n: DG.cat.length })].concat(
        [['motivation', 'Motivation'], ['strategy', 'Strategy'], ['business', 'Business'], ['application', 'Application'], ['data', 'Data'], ['technology', 'Technology'], ['implementation', 'Implementation & migration']].map(function (l) {
          var f = l[0] === 'data' ? function (e) { return e.type === 'data-object'; } : l[0] === 'application' ? function (e) { return e.layer === 'application' && e.type !== 'data-object'; } : function (e) { return e.layer === l[0]; };
          return item(l[1], catF === l[0], aset({ cat: l[0] }), { hasSwatch: true, layer: l[0] === 'data' ? 'application' : l[0], hasN: true, n: countL(f) }); })) },
        { label: 'Shortcuts', items: [ item('With detailed design', catF === 'dd', aset({ cat: 'dd' }), { hasN: true, n: countL(function (e) { return e.dd.length > 0; }) }),
          item('From the code', catF === 'inferred', aset({ cat: 'inferred' }), { hasN: true, n: countL(function (e) { return e.origin !== 'authored'; }) }),
          item('Retired in the target', catF === 'retiring', aset({ cat: 'retiring' }), { hasN: true, n: countL(function (e) { return e.pl.indexOf('target') < 0; }) }) ] } ];
    } else if (area === 'process') {
      V.anavLabel = 'Process';
      V.anav = [ { label: 'Architecture process', items: [ item('Changes', A0.psub === 'changes', aset({ psub: 'changes' }), { hasSub: true, sub: 'One per work package', hasN: true, n: DG.changes.length }),
        item('Decisions', A0.psub === 'decisions', aset({ psub: 'decisions' }), { hasSub: true, sub: 'ADR · MADR', hasN: true, n: DG.adrs.length }),
        item('Reviews', A0.psub === 'reviews', aset({ psub: 'reviews' }), { hasSub: true, sub: 'ARB and ASD', hasN: true, n: DG.arbs.length }),
        item('Roadmap', A0.psub === 'roadmap', aset({ psub: 'roadmap' }), { hasSub: true, sub: 'Plateaus and gaps' }) ] } ];
    } else {
      V.anavLabel = 'Views';
      var SUBV = { stage_decide: 'Stage · business processes', process_committee: 'Business process', stage_setup: 'Stage · business processes', base_mono: 'Baseline · inside the monolith', cmp_facility: 'Hexagonal · component', cmp_request: 'Hexagonal · component' };
      var MAIN_T = { stage_decide: 'Business process', process_committee: 'Business process', stage_setup: 'Business process', base_mono: 'Application component', cmp_facility: 'Application interface', cmp_request: 'Application interface', landscape: 'Application component', motivation: 'Goal', business: 'Value stream', application: 'Application component', data: 'Data object', technology: 'Node', migration: 'Plateau' };
      var TY = {}; DG.order.forEach(function (k) { Object.keys(VW[k].nodes).forEach(function (n) { var x = VW[k].nodes[n]; TY[x.kind] = [x.layer, x.type]; }); });
      V.anav = DG.phases.map(function (p) { return { label: p[1], items: DG.order.filter(function (k) { return VW[k].phase === p[0]; }).map(function (k) { var t = TY[MAIN_T[k]] || ['implementation', 'plateau'];
        var d = 0; for (var q = VW[k].parent; q; q = VW[q].parent) d++; return item(VW[k].title, k === vKey, aset({ view: k, mode: modeIn(VW[k], mode), el: null, vhist: vh.concat([here]) }), { lv: d ? 'a-l' + Math.min(d, 2) : '', hasTile: true, layer: t[0], type: t[1], hasSub: true, sub: VW[k].modes.length > 1 ? VW[k].modes.filter(function (m) { return !GAPS[m]; }).length + ' plateaus and gaps' : (SUBV[k] || p[2]) }); }) }; });
    }
    V.arCat = area === 'catalogue'; V.arViews = area === 'views';
    V.prChanges = area === 'process' && A0.psub === 'changes'; V.prDecisions = area === 'process' && A0.psub === 'decisions'; V.prReviews = area === 'process' && A0.psub === 'reviews'; V.prRoadmap = area === 'process' && A0.psub === 'roadmap';
    V.archCounts = DG.cat.length + ' elements · ' + DG.order.length + ' views · 3 plateaus';

    // ---- pages: element, change, decision, review, ASD
    var epRaw = A0.ep ? CAT[A0.ep] : null, chRaw = A0.change ? DG.changes.filter(function (c) { return c.k === A0.change; })[0] : null, adrRaw = adrById(A0.adr), arbRaw = arbById(A0.arb);
    var last = A0.trail[A0.trail.length - 1];
    var backLabel = (function () { if (!last) return 'Back'; if (last.asd) return 'Back to the ASD'; if (last.arb) return 'Back to the review'; if (last.adr) return 'Back to the decision'; if (last.change) return 'Back to the change'; if (last.ep) return 'Back to the element';
      return { catalogue: 'Back to the catalogue', views: 'Back to the view', process: 'Back to ' + ({ changes: 'the changes', decisions: 'the decisions', reviews: 'the reviews', roadmap: 'the roadmap' }[last.psub] || 'the process') }[last.area]; })();
    V.pBack = aset(function () { var t = A0.trail.slice(0, -1), l = A0.trail[A0.trail.length - 1] || { area: A0.area }; return Object.assign({}, PAGES, l, { trail: t }); });
    V.pBackLabel = backLabel;
    var page = arbRaw && A0.asd ? 'asd' : arbRaw ? 'arb' : adrRaw ? 'adr' : chRaw ? 'change' : epRaw ? 'ep' : 'main';
    V.archMain = page === 'main'; V.epOpen = page === 'ep'; V.chOpen = page === 'change'; V.adrOpen = page === 'adr'; V.arbOpen = page === 'arb'; V.asdOpen = page === 'asd';
    var ep = { name: '', kind: '', id: '', layer: 'other', type: 'grouping', track: [], trackAria: '', rels: [], views: [], dds: [], adrs: [], src: '', path: '' };
    if (epRaw) {
      var seen = {}, rr = [];
      epRaw.rels.forEach(function (r) { var key = r.dir + r.rel + r.other; if (seen[key]) return; seen[key] = true; var o = CAT[r.other] || {};
        rr.push({ verb: VERB[r.rel][r.dir === 'out' ? 0 : 1], name: r.otherName, layer: o.layer || 'other', type: o.type || 'grouping', label: r.label || '—', pl: r.pl.length === 3 ? 'All plateaus' : r.pl.map(function (p) { return PLN[p]; }).join(', '), open: openEl(r.other) }); });
      var arbE = epRaw.arb ? arbById(epRaw.arb) : null;
      ep = { name: epRaw.name, kind: epRaw.kind, id: epRaw.id, layer: epRaw.layer, type: epRaw.type, layerName: DG.layers[epRaw.layer], desc: epRaw.desc, hasDesc: !!epRaw.desc, owner: epRaw.owner, origin: ORIGIN[epRaw.origin], inferred: epRaw.origin === 'inferred',
        realizes: epRaw.realizes, hasRealizes: !!epRaw.realizes && epRaw.realizes !== '—', contract: epRaw.contract, hasContract: !!epRaw.contract,
        track: TRK(epRaw.pl), trackAria: trkAria(epRaw.pl), plText: epRaw.pl.indexOf('target') < 0 ? 'retired in the target' : epRaw.pl.indexOf('base') < 0 ? 'new' : 'in every plateau',
        rels: rr, views: epRaw.views.map(function (v) { return { label: VW[v[0]].title + (VW[v[0]].modes.length > 1 ? ' · ' + PLN[v[1]] : ''), open: goMain({ area: 'views', view: v[0], mode: v[1], el: v[2] }) }; }),
        dds: epRaw.dd.map(function (id) { return { label: DG.dds[id].title, open: ddOpen(id) }; }), hasDd: epRaw.dd.length > 0, noDd: !epRaw.dd.length,
        ddNote: /^sbb\./.test(epRaw.id) && epRaw.type === 'application-component' ? 'Not written yet. The ARB check T6 flags it before the board.' : epRaw.ext ? 'Owned by another application.' : 'Not needed for this type of element.',
        adrs: epRaw.adrs.map(function (id) { var a = adrById(id); return Object.assign({ t: id + ' · ' + a.t, open: openP({ adr: id }) }, TILE_ADR[a.status]); }), hasAdrs: epRaw.adrs.length > 0,
        arb: epRaw.arb, hasArb: !!arbE, openArb: arbE ? openP({ arb: epRaw.arb }) : set({}), src: epRaw.src, path: 'model/corporate-credit/' + (epRaw.layer === 'motivation' ? 'motivation' : epRaw.layer === 'implementation' ? 'migration' : epRaw.layer) + '.c4' };
      V.epArbSt = arbE ? rdSt(arbE) : ST('neutral', '–', '');
    } else V.epArbSt = ST('neutral', '–', '');
    V.ep = ep; V.epEdit = set({ snack: 'Opens a pull request on the model with this element. The model is validated before review.' });
    var ch = { name: '', ctx: '', why: '', steps: [], gap: [], openGap: set({}) };
    if (chRaw) {
      var w = DG.wps[chRaw.k], ss = stepsOf(chRaw), sts = ss.map(function (x) { return x.st; }), cur = sts.indexOf('error') >= 0 ? sts.indexOf('error') : (function () { for (var i = 0; i < sts.length; i++) if (sts[i] === 'neutral' || sts[i] === 'info') return i; return sts.indexOf('warning'); })(), warns = sts.filter(function (x) { return x === 'warning'; }).length;
      var L = function (ab, t, sub, open, c) { return { ab: ab, t: t, sub: sub, open: open, bg: c[0], fg: c[1] }; }, CA = ['#CFEDFA', '#0A5570'], CR = ['#ECE5F4', '#48454E'], CS = ['#E3DFFF', '#14085E'], CI = ['#F6DCEB', '#7A2457'];
      var arbs = chRaw.arbs.map(arbById), a0 = arbs[0];
      var steps = [
        { name: 'Decide', lines: chRaw.adrs.map(function (id) { var a = adrById(id); return L('ADR', id + ' · ' + a.t, a.status + ' · ' + a.date, openP({ adr: id }), CA); }), note: '' },
        { name: 'Design', lines: a0 && a0.asd ? [L('ASD', 'Architecture Solution Design', secsOf(a0).filter(function (x) { return !x.missing; }).length + ' of 13 sections ready', openP({ arb: a0.id, asd: true }), CS)] : [], note: a0 ? (a0.asd ? '' : 'The ASD is written with the submission.') : 'Starts after the decisions.' },
        { name: 'Review', lines: arbs.map(function (a) { return L('ARB', a.t, readinessOf(a)[0] + ' · board ' + a.board, openP({ arb: a.id }), CR); }), note: arbs.length ? '' : 'No submission yet.' },
        { name: 'Deliver', lines: [L('WP', w.name, w.team + ' · ' + w.when, openGap(w.from, w.to), CI)], note: 'Reaches ' + PLN[w.to] + ' (' + DG.plateaus.filter(function (p) { return p.k === w.to; })[0].when + ').' } ];
      ch = { name: w.name, ctx: 'Change · ' + PLN[w.from] + ' → ' + PLN[w.to] + ' · ' + w.team + ' · ' + w.when, why: chRaw.why,
        steps: steps.map(function (x, i) { return Object.assign({ n: i + 1, name: x.name, lines: x.lines, note: x.note, hasNote: !!x.note, cls: i === cur ? 'cur' : '' }, ss[i]); }),
        gap: gapOf(w.from, w.to, chRaw.k), openGap: openGap(w.from, w.to) };
      var ov = cur < 0 ? ST('success', '✓', 'Delivered') : ss[cur].st === 'error' ? ST('error', '✕', ['Deciding', 'Designing', 'In review', 'Delivering'][cur] + ' · blocked') : ST(warns ? 'warning' : ss[cur].st === 'neutral' ? 'info' : ss[cur].st, warns ? '!' : '›', ['Deciding', 'Designing', 'In review', 'Delivering'][cur] + (warns ? ' · ' + warns + ' to follow up' : ''));
      V.chOverall = ov;
    } else V.chOverall = ST('neutral', '–', '');
    V.ch = ch;
    var adr = { t: '', ctx: '', st: 'neutral', g: '', w: '', context: '', decision: '', options: [], consequences: [], file: '', ref: '', els: [] };
    if (adrRaw) {
      adr = Object.assign({ t: adrRaw.id + ' · ' + adrRaw.t, ctx: 'Decision · ' + adrRaw.date + ' · ' + adrRaw.by + ' · ' + adrRaw.plateau, context: adrRaw.context, decision: adrRaw.decision,
        options: adrRaw.options.map(function (o) { var chosen = /\((chosen|proposed)\)/.test(o); return { t: o.replace(/ \((chosen|proposed)\)/, ''), cls: chosen ? 'on' : '', mark: chosen ? '✓' : '', note: chosen ? (/proposed/.test(o) ? 'proposed' : 'chosen') : '' }; }),
        consequences: adrRaw.consequences, file: 'model/adr/' + adrRaw.id + '.md', ref: adrRaw.ref,
        els: adrRaw.els.map(function (k) { var n = VW.application.nodes[k]; return { name: n.name, layer: n.layer, type: n.type, open: openEl(n.id) }; }) }, TILE_ADR[adrRaw.status]);
    }
    V.adr = adr;
    var arb = { t: '', ctx: '', banner: '', bcls: '', checks: [], secs: [], hasAsd: false, reviewers: [], conditions: [], hasConditions: false, noReviewers: false, canDecide: false, blocked: false, hasRecorded: false, scope: '', scopeCounts: '', seeGap: set({}) };
    V.arbRd = ST('neutral', '–', '');
    if (arbRaw) {
      var rd = readinessOf(arbRaw), ssA = secsOf(arbRaw), gr = gapOf(arbRaw.from, arbRaw.to), dK = A0.decided[arbRaw.id];
      var blocked = rd[0] === 'Blocked', decidedNow = !!arbRaw.decided || dK === 'Approved' || dK === 'Approve with conditions';
      var decide = function (k) { return blocked && k !== 'Request changes' ? set({ snack: 'Fix the blocking check and write the missing section first: the board cannot approve a blocked submission.' }) : aset(function () { var o = Object.assign({}, A0.decided); o[arbRaw.id] = k; return { decided: o }; }); };
      var nonPass = checksOf(arbRaw).filter(function (c) { return c.st !== 'pass'; }).length;
      arb = { t: arbRaw.t, ctx: 'ARB · ' + PLN[arbRaw.from] + ' → ' + PLN[arbRaw.to] + ' · board on ' + arbRaw.board + ' · ' + arbRaw.by,
        bcls: rd[1] === 'bl' ? 'b-blk' : rd[1] === 'wn' || rd[1] === 'dr' ? 'b-att' : 'b-ok',
        banner: decidedNow ? (dK ? 'Decided today: ' + dK.toLowerCase() + '. The record is written back to Git by an auto-merge pull request.' : arbRaw.status + '. ' + (arbRaw.decided || '')) : blocked ? 'Blocked: a blocking check fails or an ASD section is missing. The board cannot approve until both are fixed.' : rd[0] === 'Draft' ? 'Draft: the submission is still being prepared. Reviewers are named when it leaves draft.' : rd[0] === 'Needs attention' ? 'Needs attention: ' + nonPass + ' warning' + (nonPass === 1 ? '' : 's') + ' and pending reviewers. The board can decide, with conditions.' : 'Ready for the board.',
        checks: checksOf(arbRaw), secs: ssA, hasAsd: ssA.length > 0, asdCount: ssA.filter(function (x) { return !x.missing; }).length + ' of 13 ready',
        scope: PLN[arbRaw.from] + ' → ' + PLN[arbRaw.to], scopeCounts: countOf(gr), seeGap: openGap(arbRaw.from, arbRaw.to),
        reviewers: reviewersOf(arbRaw), noReviewers: arbRaw.reviewers.length === 0, conditions: arbRaw.conditions.concat(dK === 'Approve with conditions' ? [['C' + (arbRaw.conditions.length + 1), 'Write the detailed design of collateral-service before the transition to target', 'Enterprise architecture', '15 Jan', 'Open']] : []).map(function (c) { return { id: c[0], t: c[1], owner: c[2], due: c[3], st: c[4] === 'Done' ? 'success' : 'info', g: c[4] === 'Done' ? '✓' : '…', w: c[4] }; }),
        cover: coverOf(arbRaw), coverN: coverOf(arbRaw).filter(function (c) { return c.ok; }).length + ' of 13 covered', asks: (arbRaw.asks || []).map(function (q) { return { t: q[0], ref: q[1] }; }), hasAsks: !!(arbRaw.asks && arbRaw.asks.length), reqN: (arbRaw.reqs || []).length,
        canDecide: !decidedNow && arbRaw.reviewers.length > 0, blocked: blocked, approve: decide('Approved'), approveC: decide('Approve with conditions'), changes: decide('Request changes'),
        hasRecorded: decidedNow, status: dK || arbRaw.status, recorded: dK ? 'Recorded in Git · auto-merge pull request on portfolios/facility/arb/2026-14.md · 7c1e0a4' : (arbRaw.decided || '') };
      arb.hasConditions = arb.conditions.length > 0;
      V.arbRd = rdSt(arbRaw);
    }
    V.arb = arb; V.asdGo = openP({ arb: A0.arb, asd: true });
    var TB = function (o, head, rows) { o.hasTable = true; o.thead = head; o.trows = rows.map(function (r) { return { cells: r.map(function (c, j) { return { t: c, cls: j === 0 ? 'k' : '' }; }) }; }); };
    V.asdSecs = arbRaw && arbRaw.asd ? secsOf(arbRaw).map(function (x) {
      var v = x.v || {}, o = { n: x.n, name: x.name, src: x.src, badge: x.missing ? 'err' : x.src === 'Written' ? 'ok' : 'model', hasP: !!x.text, p: x.text, missing: x.missing, write: x.write,
        hasB: !!(v.b && v.b.length), b: v.b || [], hasTable: false, thead: [], trows: [], hasAsks: false, asks: [], hasBase: false, hasTarget: false };
      if (v.table) TB(o, v.table.head, v.table.rows);
      if (x.key === 'requirements') TB(o, ['Requirement', 'Acceptance', 'Realized by'], (arbRaw.reqs || []).map(function (id) { var r = DG.reqs[id]; return [r[0] + ' · ' + id, r[1], r[2]]; }));
      if (x.key === 'baseline') { o.hasBase = true; o.hasP = true; o.p = 'Transition 1, as it will run in December 2026: the starting point of this change. Application cooperation view.'; }
      if (x.key === 'target') { o.hasTarget = true; o.hasP = true; o.p = 'Target, June 2027. Application cooperation view.'; }
      if (x.key === 'gap') { TB(o, ['Element', 'Change', 'Work package'], gapOf(arbRaw.from, arbRaw.to).map(function (g) { return [g.name, g.chgW, g.wp]; })); o.hasP = true; o.p = countOf(gapOf(arbRaw.from, arbRaw.to)) + '. Every gap item is delivered by a work package (check P3).'; }
      if (x.key === 'dd') TB(o, ['Service', 'Detailed design', 'Contracts', 'Owner'], ['facility-service', 'limit-service', 'collateral-service', 'rating-service', 'document-service'].map(function (k) { var d = DG.detail['sbb.corporate-credit.' + k];
        var n = k === 'collateral-service' && fixedOf(arbRaw, /^T6/) ? 'Drafted from the code · in review' : d.dd.length ? d.dd.map(function (id) { return DG.dds[id].layer; }).join(', ') : 'Not written · check T6';
        var c = k === 'limit-service' ? (fixedOf(arbRaw, /^O2/) ? 'OpenAPI, AsyncAPI (cc.limits added)' : 'OpenAPI · AsyncAPI channel cc.limits missing') : d.contract ? d.contract.split('/').pop() : '—'; return [k, n, c, d.owner]; }));
      if (x.key === 'decisions') { TB(o, ['Decision', 'Status', 'Consequence'], (arbRaw.adrs || []).map(function (id) { var a = adrById(id); return [id + ' · ' + a.t, a.status, a.consequences[0]]; })); o.hasAsks = true; o.asks = (arbRaw.asks || []).map(function (q) { return { t: q[0], ref: q[1] }; }); }
      if (x.key === 'questions') TB(o, ['Question', 'Status', 'Owner'], [['Which valuation provider, and under which contract?', 'ADR-CC-05 proposed', 'Facility team, Procurement'], ['Accept the MQ booking risk during the cut-over?', 'Risk R2 · asked of the board', 'Credit risk, Core banking']]);
      return o; }) : [];
    V.asdCover = arbRaw && arbRaw.asd ? coverOf(arbRaw) : []; V.asdCoverN = arbRaw && arbRaw.asd ? coverOf(arbRaw).filter(function (c) { return c.ok; }).length + ' of 13 covered' : '';
    V.asdCtx = arbRaw && arbRaw.asd ? '13 sections · ' + secsOf(arbRaw).filter(function (x) { return x.src === 'Written' && !x.missing; }).length + ' of 6 written, 7 assembled from the model' : '';
    V.asdExport = set({ snack: 'The ASD is exported as Markdown with the views as images, ready to attach to the board invitation.' });

    // ---- variant B (services lens), header, assistant context
    var LENS = [ { label: 'Request team', k: ['req', 'wf'] }, { label: 'Client team', k: ['cli', 'rat'] }, { label: 'Facility team', k: ['fac', 'lim', 'col'] }, { label: 'Platform team', k: ['gw', 'doc', 'kafka'] }, { label: 'Legacy', k: ['mono', 'fcore', 'creg', 'exp'] } ];
    V.lensGroups = LENS.map(function (g) { return { label: g.label, apps: g.k.map(function (k) { var n = VW.application.nodes[k], legacy = n.pl.indexOf('target') < 0;
      return { name: n.name, legacy: legacy, cur: vKey === 'application' && elK === k ? 'page' : 'false', pick: aset({ area: 'views', view: 'application', mode: legacy ? 'base' : 'target', el: k }) }; }) }; });
    V.ddBack = set({ view: 'arch' });
    V.archHdr = page === 'adr' ? ['Docs · Architecture decision', adrRaw.id] : page === 'arb' ? ['Docs · Architecture review', arbRaw.id] : page === 'asd' ? ['Docs · Architecture review', arbRaw.id + ' · ASD'] : page === 'change' ? ['Docs · Architecture change', DG.wps[chRaw.k].name]
      : page === 'ep' ? ['Docs · Architecture catalogue', epRaw.name] : ['Docs · Architecture', 'Corporate credit platform · ' + (area === 'catalogue' ? 'Catalogue · ' + CATN[catF][0] : area === 'process' ? 'Process · ' + { changes: 'Changes', decisions: 'Decisions', reviews: 'Reviews', roadmap: 'Roadmap' }[A0.psub] : vw.title + ' · ' + (isGap ? 'gap' : PLN[mode]))];
    V.archCtx = page === 'main' ? 'Corporate credit · ' + (area === 'views' ? vw.title : area === 'catalogue' ? 'Catalogue' : 'Process') : V.archHdr[1];
