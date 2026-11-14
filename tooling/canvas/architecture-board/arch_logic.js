const D = /*DATA*/;
const EL = {}; D.elements.forEach(e => { EL[e.id] = e; });
const ARB = {}; D.arbs.forEach(a => { ARB[a.id] = a; });
const PF = {}; D.portfolios.forEach(p => { PF[p.id] = p; });
const APPS = D.applications, APP_IDS = Object.keys(APPS);
const COMP2APP = {}; APP_IDS.forEach(a => (APPS[a].components || []).forEach(c => { COMP2APP[c] = a; }));
const NOTE = D.notation;
const TODAY = '2026-11-03';
const sid = s => String(s).replace(/[^A-Za-z0-9_]/g, '_');
const TAGS = ['baseline', 'transition-1', 'target'];
const TAG_SHORT = { baseline: 'B', 'transition-1': 'T1', 'transition-2': 'T2', target: 'T' };
const TAG_NAME = { baseline: 'Baseline', 'transition-1': 'Transition 1', target: 'Target' };
const LEVEL_NAME = { motivation: 'Motivation', requirement: 'Requirement', abb: 'ABB', sbb: 'SBB', dd: 'DD', migration: 'Migration', adr: 'ADR' };
const LEVEL_ORDER = ['motivation', 'requirement', 'abb', 'sbb', 'dd', 'migration', 'adr'];
const LAYER_ORDER = ['strategy', 'business', 'application', 'technology', 'motivation', 'implementation', 'other'];
const STATUS = { done: ['success', '✓', 'Done'], ready: ['info', 'i', 'Ready'], draft: ['warning', '!', 'Draft'], deprecated: ['error', '✕', 'Deprecated'] };
const ARB_STATUS = { draft: ['warning', '!', 'Draft'], submitted: ['info', 'i', 'Submitted'], 'in-review': ['info', 'i', 'In review'], approved: ['success', '✓', 'Approved'], 'approved-with-conditions': ['success', '✓', 'Approved with conditions'], rejected: ['error', '✕', 'Rejected'], 'changes-requested': ['warning', '!', 'Changes requested'] };
const DECISION = { approved: ['success', '✓', 'Approved'], 'approved-with-conditions': ['success', '✓', 'Approved with conditions'], 'changes-requested': ['warning', '!', 'Changes requested'], rejected: ['error', '✕', 'Rejected'], pending: ['info', 'i', 'Pending'], 'not-required': ['neutral', '–', 'Not required'] };
const READINESS = { ready: ['success', '✓', 'Ready for the board'], attention: ['warning', '!', 'Needs attention'], blocked: ['error', '✕', 'Blocked'] };
const CHECK = { pass: ['success', '✓', 'Passed'], warn: ['warning', '!', 'Warning'], fail: ['error', '✕', 'Failed'] };
const CHANGE = { new: ['new', '+', 'New'], changed: ['changed', 'Δ', 'Changed'], retired: ['retired', '−', 'Retired'] };
const TIME = { invest: ['success', '↑', 'Invest'], tolerate: ['neutral', '=', 'Tolerate'], migrate: ['warning', '→', 'Migrate'], eliminate: ['error', '✕', 'Eliminate'] };
const LIFE = { adopt: ['success', '✓', 'Adopt'], trial: ['info', 'i', 'Trial'], hold: ['warning', '!', 'Hold'], retire: ['error', '✕', 'Retire'] };
const RINGS = ['adopt', 'trial', 'hold', 'retire'];
const STEP = { done: ['success', '✓', 'Done'], progress: ['info', 'i', 'In progress'], attention: ['warning', '!', 'Needs attention'], blocked: ['error', '✕', 'Blocked'], none: ['neutral', '–', 'Not started'], skip: ['neutral', '–', 'Not needed'] };
const chip = (map, k, w) => { const v = map[k] || ['neutral', '·', k || '—']; return { cls: v[0], g: v[1], w: w || v[2], has: !!k }; };
const nochip = { cls: 'none', g: '', w: '', has: false };
const esc = s => String(s == null ? '' : s);
const htmlText = h => String(h || '').replace(/<\/(tr|p|h2|h3|li|div)>/g, '\n').replace(/<\/t[dh]>/g, ' · ').replace(/<h2[^>]*>/g, '\n').replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/\n\s*\n+/g, '\n').trim();
const title = id => (EL[id] && EL[id].title) || (ARB[id] && ARB[id].title) || (APPS[id] && APPS[id].title) || (PF[id] && PF[id].title) || id;
const kindName = e => (NOTE[e.kind] && NOTE[e.kind].name) || e.kind;
const layerOf = e => (NOTE[e.kind] && NOTE[e.kind].layer) || 'other';
const tile = e => ({ layer: layerOf(e), kind: e.kind, name: kindName(e) });
const appOf = e => COMP2APP[e.id] || (APPS[e.application] ? e.application : null);
const inP = (e, tag) => !e || !e.chain || !e.plateaus || !e.plateaus.length ? true : e.plateaus.indexOf(tag) >= 0;
const land = chain => D.landscapes[chain] || { plateaus: [], gaps: [] };
const plateauObj = (chain, tag) => land(chain).plateaus.find(p => p.tag === tag);
const byTitle = (a, b) => a.title.localeCompare(b.title);
const uniq = a => a.filter((x, i) => a.indexOf(x) === i);
const fmtDate = d => d ? d.replace(/-/g, '‑') : '—';
const relOut = id => D.relations.filter(r => r.s === id);
const relIn = id => D.relations.filter(r => r.t === id);
const elAt = (id) => EL[id];
const compApps = comps => uniq(comps.map(c => COMP2APP[c]).filter(Boolean));

function appChange(app, tag) {
  const comp = APPS[app].components[0], e = EL[comp]; if (!e) return null;
  const L = land(e.chain), g = L.gaps.find(x => x.to === tag);
  if (!g) return null; const it = g.items.find(x => x.id === comp); return it && it.change !== 'unchanged' ? it.change : null;
}
function appsRealizing(cap, tag) { return uniq(Object.keys(D.realizes).filter(c => D.realizes[c].indexOf(cap) >= 0 && inP(EL[c], tag)).map(c => COMP2APP[c]).filter(Boolean)); }
const PROCS = D.elements.filter(e => e.kind === 'business-process');
const ROLES = D.elements.filter(e => e.kind === 'business-role');
const CAPS2 = []; D.capabilities.forEach(d => d.children.forEach(c => CAPS2.push({ id: c, domain: d.id })));
const VS = D.elements.filter(e => e.kind === 'value-stream' && relIn(e.id).every(r => r.k !== 'composition'));
const stagesOf = vs => relOut(vs).filter(r => r.k === 'composition').map(r => r.t);
const coverageItems = ['Context and scope', 'Business need', 'Requirements', 'Baseline', 'Target', 'Gap and transition', 'Architecture overview', 'Detailed design', 'Decisions', 'Non-functional requirements', 'Security', 'Risks', 'Open questions'];

const VIEWS = {
  enterprise: [
    ['capmap', 'Capability map', 'CIO, enterprise architects', 'where to invest and which capabilities to strengthen', 'grid', 'One tile per capability, grouped by domain. The shade and the number show the selected measure. A warning marks a differentiating capability with low maturity, or a capability no application realizes in the selected plateau.'],
    ['coverage', 'Capability coverage', 'Enterprise and portfolio architects', 'which overlaps to rationalize and which gaps to close', 'matrix', 'Rows are capabilities, columns are portfolios. Each cell lists the applications that realize the capability in the selected plateau. Two applications in one cell are an overlap; an empty row is a gap.'],
    ['capvs', 'Capabilities × value streams', 'Business owners, enterprise architects', 'which capabilities each stage of a value stream needs', 'matrix', 'Rows are capabilities, columns are the stages of each value stream. A mark means the capability serves the stage. A capability that serves no stage is not on the critical path of any stream; a stage with no capability is a gap in the business architecture.'],
    ['roles', 'Roles × processes', 'Business architects, process owners', 'who performs, decides and is consulted in each process', 'matrix', 'Rows are business processes, columns are business roles. R performs, A decides, C is consulted, I is informed. Every process needs exactly one A in the selected plateau; the rule is checked on the row.'],
    ['tech', 'Technology radar', 'CTO, platform team, architects', 'which standards to adopt and what to retire', 'grid', 'Columns are lifecycle rings, rows are categories. Each technology shows how many applications run on it in the selected plateau. The table below lists the applications still on Hold or Retire technologies.'],
    ['roadmap', 'Enterprise roadmap', 'Executive committee, PMO', 'the order and the funding of the changes', 'timeline', 'One band per portfolio: its plateaus as milestones (◆) and its changes as bars, on one month scale. The thin line is today.'],
    ['motivation', 'Motivation', 'Executive committee, enterprise architects', 'why each change exists', 'grid', 'One row per driver: who raises it, how it is assessed, the goals it influences, the outcomes that realize them and the requirements that realize the outcomes. Principles are listed under the grid. Select a figure to open it.'],
    ['valuestreams', 'Value streams', 'Business owners', 'which capabilities each stage of a value stream needs', 'grid', 'One grid per value stream: the stages are the columns, in order; under each stage, the capabilities that serve it. The matrix view shows the same facts for every capability.'],
  ],
  portfolio: [
    ['landscape', 'Application landscape', 'Portfolio architect', 'what the portfolio looks like at each plateau', 'grid', 'Rows are capabilities, cells are the portfolio\'s applications that realize them in the selected plateau. The chip compares with the previous plateau; retired applications are faded.'],
    ['cooperation', 'Application cooperation', 'Portfolio and solution architects', 'integration and coupling between applications', 'grid', 'One row per application of the portfolio: on the left what it receives and from whom, on the right what it sends and to whom, in the selected plateau. Neighbours in other portfolios are faded. The table lists the flows.'],
    ['interaction', 'Application interaction', 'Integration architects', 'which applications exchange what, and how coupled the portfolio is', 'matrix', 'Rows are the portfolio\'s applications, columns every application they exchange with. A cell names the flow from the row to the column in the selected plateau. The last column counts a row\'s dependencies.'],
    ['procapp', 'Processes × applications', 'Business and solution architects', 'which applications a process change touches', 'matrix', 'Rows are the business processes of the portfolio, columns its applications in the selected plateau. A mark means the application supports the process. A process with no application is manual; an application supporting no process is a candidate for review.'],
    ['gap', 'Gap', 'ARB, portfolio architect', 'the scope of each transition', 'table', 'What changes between two plateaus, and the change (work package) that delivers each building block. The strip above groups the changed applications: new, changed, retired.'],
    ['data', 'Data ownership', 'Data owners, portfolio architect', 'the system of record of each business object', 'matrix', 'Rows are business objects, columns are the portfolio\'s applications. M = master (system of record), C = copy. One master per object is the rule; more is flagged.'],
    ['apptech', 'Applications × technologies', 'Platform team, portfolio architect', 'which applications depend on a standard being retired', 'matrix', 'Rows are the portfolio\'s applications in the selected plateau, columns the technology standards by category. The dot takes the lifecycle color of the standard. A row with a Retire standard needs an exit plan in the roadmap.'],
    ['roadmap', 'Roadmap', 'Portfolio architect, delivery leads', 'the order of the changes and their dependencies', 'timeline', 'One bar per change on a month grid; ◆ marks the plateaus. A change that depends on another says so under its name.'],
    ['chain', 'Requirement chain', 'Portfolio architect, ARB', 'whether every requirement is realized in the target', 'grid', 'One row per requirement: the architecture building blocks that realize it, the solution building blocks of the target that realize those, and the detailed design of each SBB. An empty cell is a traceability gap (T1, T2, T6).'],
  ],
  application: [
    ['factsheet', 'Fact sheet', 'Application owner, team lead', 'lifecycle (TIME) and what the application depends on', 'cards', 'Elements facts, the capabilities it realizes, the data it masters or copies, its flows, the platforms it runs on, and the changes and decisions that concern it.'],
    ['inside', 'Inside and neighbours', 'Solution architect, team', 'boundaries and contracts', 'grid', 'The application\'s own building blocks by kind, the applications it receives from and sends to, and the platforms it runs on. The table lists every relationship with its ArchiMate type.'],
    ['interfaces', 'Interfaces and data', 'Team, integration architects', 'contract governance', 'table', 'Interfaces with their contract status; data objects with the business object they hold and whether this application is its master.'],
  ],
};
const KIND_LABEL = { grid: 'Grid', matrix: 'Matrix', table: 'Table', timeline: 'Timeline', cards: 'Cards' };
const ROLE_VIEW = {
  owner: { label: 'Change owner', name: 'Aurélien Heux', sub: 'Corporate portfolio architect', av: 'AH' },
  reviewer: { label: 'Reviewer', name: 'Hugo Lefèvre', sub: 'Security architect', av: 'HL' },
  chair: { label: 'Board chair', name: 'Nadia Benali', sub: 'Architecture Board chair', av: 'NB' },
  reader: { label: 'Reader', name: 'Yann Dupont', sub: 'Developer · team-credit', av: 'YD' },
};
const HOW = /*HOW*/;
const CDOC = /*CDOC*/;
const DELIV = /*DELIV*/;
const INTAKE = /*INTAKE*/;

class Component extends DCLogic {
  constructor(props) {
    super(props);
    this.simHostId = 'sim-host-arch'; this.simDefault = 1440; this.simMinH = 720; this.simMaxH = 1200;
    this.state = {
      role: 'owner', area: 'elements', level: 'enterprise', pf: 'corporate', app: 'credit-origination',
      view: { enterprise: 'capmap', portfolio: 'landscape', application: 'factsheet' }, plateau: 'target', gap: 0, metric: 'maturity',
      cat: 'tree', treeMode: 'portfolio', open: { 'pf:corporate': true, 'app:corporate/credit-origination': true, 'lay:corporate/credit-origination/application': true, 'layer:business': true }, catLevel: 'all', catScope: 'all', q: '',
      proc: 'changes', page: null, pageFrom: null, arbTab: 'asd', asdSec: 0, howTab: 'steps', docs: {}, collide: {}, props: {}, threadDraft: '', docDiff: false, chFilter: 'all',
      decisions: {}, note: '', toast: null, pfFilter: 'all', howStep: 2, rend: {}, sel: null, vhist: [], zoom: 1, srcOn: false, simW: null, simAvail: 0, simAvailH: 0,
    };
  }
  /*SIM*/
  componentDidMount() { const self = this; this.simSync(); if (typeof window !== 'undefined') window.addEventListener('resize', () => self.simSync()); }
  componentDidUpdate() { this.simSync(); }
  set(o) { return () => this.setState(o); }
  sel(id) { return () => this.setState({ sel: this.state.sel === id ? null : id }); }
  snap() { const s = this.state; return { level: s.level, view: Object.assign({}, s.view), pf: s.pf, app: s.app, plateau: s.plateau, gap: s.gap, sel: s.sel, rend: Object.assign({}, s.rend) }; }
  drill(target) { return () => { const s = this.state; this.setState(Object.assign({ area: 'views', page: null, vhist: s.vhist.concat([this.snap()]), sel: null }, target)); if (typeof window !== 'undefined') window.scrollTo(0, 0); }; }
  back() { return () => { const s = this.state; if (s.page) { this.setState({ page: s.pageFrom || null, pageFrom: null }); return; } const h = s.vhist; if (!h.length) return; const l = h[h.length - 1]; this.setState({ vhist: h.slice(0, -1), level: l.level, view: l.view, pf: l.pf, app: l.app, plateau: l.plateau, gap: l.gap, sel: l.sel, rend: l.rend }); }; }
  navigateTo(e) {
    if (!e) return null; const app = appOf(e), pf = e.portfolio || (app ? APPS[app].portfolio : null);
    const V = (lv, v, extra, label) => ({ label, go: this.drill(Object.assign({ level: lv, view: Object.assign({}, this.state.view, { [lv]: v }) }, extra || {})) });
    if (e.kind === 'application-component' && app) { if (this.state.level === 'application' && this.state.app === app && this.state.view.application === 'inside') return null; return V('application', 'inside', { app, pf: APPS[app].portfolio }, 'Open the view Inside ' + APPS[app].title); }
    if (e.kind === 'application-interface' && app) return V('application', 'interfaces', { app, pf: APPS[app].portfolio }, 'Open the view Interfaces and data · ' + APPS[app].title);
    if (e.kind === 'data-object' && app) return V('portfolio', 'data', { pf: APPS[app].portfolio }, 'Open the view Data ownership · ' + PF[APPS[app].portfolio].title);
    if (e.kind === 'business-object') return V('portfolio', 'data', {}, 'Open the view Data ownership');
    if (e.kind === 'capability') { const apps = appsRealizing(e.id, 'target'); const p = apps.length ? APPS[apps[0]].portfolio : null; return p ? V('portfolio', 'landscape', { pf: p }, 'Open the view Application landscape · ' + PF[p].title) : V('enterprise', 'coverage', {}, 'Open the view Capability coverage'); }
    if (e.kind === 'value-stream') return V('enterprise', 'capvs', {}, 'Open the view Capabilities × value streams');
    if (e.kind === 'business-role') return V('enterprise', 'roles', {}, 'Open the view Roles × processes');
    if (e.kind === 'business-process' && pf) return V('portfolio', 'procapp', { pf }, 'Open the view Processes × applications · ' + PF[pf].title);
    if (e.kind === 'requirement' && pf) return V('portfolio', 'chain', { pf }, 'Open the view Requirement chain · ' + PF[pf].title);
    if ((e.kind === 'work-package' || e.kind === 'plateau') && pf) return V('portfolio', 'gap', { pf }, 'Open the view Gap · ' + PF[pf].title);
    if (['node', 'system-software', 'technology-service'].indexOf(e.kind) >= 0) return V('portfolio', 'apptech', {}, 'Open the view Applications × technologies');
    if (['driver', 'goal', 'outcome', 'stakeholder', 'assessment', 'principle'].indexOf(e.kind) >= 0 && !(this.state.level === 'enterprise' && this.state.view.enterprise === 'motivation')) return V('enterprise', 'motivation', {}, 'Open the view Motivation');
    return null;
  }
  go(id) { return () => { const from = this.state.page; if (EL[id] && EL[id].kind === 'work-package' && CDOC.docs[id]) { this.openChange(id)(); return; } this.setState({ page: ARB[id] ? { kind: 'arb', id } : { kind: 'element', id }, pageFrom: from && from.kind !== 'element' ? from : null, arbTab: 'asd', asdSec: 0 }); if (typeof window !== 'undefined') window.scrollTo(0, 0); }; }
  openArea(a) { return () => this.setState({ area: a, page: null }); }
  openView(level, view, extra) { return () => this.setState(Object.assign({ area: 'views', page: null, sel: null, level, view: Object.assign({}, this.state.view, { [level]: view }) }, extra || {})); }
  openApp(app) { return () => this.setState({ area: 'views', page: null, sel: null, level: 'application', app, pf: APPS[app].portfolio || this.state.pf }); }
  toast(msg) { const self = this; this.setState({ toast: msg }); if (typeof window !== 'undefined') setTimeout(() => { if (self.state.toast === msg) self.setState({ toast: null }); }, 4000); }

  // ---------- shell ----------
  shellVals() {
    const s = this.state, self = this, R = ROLE_VIEW[s.role];
    const v = D.validation.summary;
    const cnt = `${D.portfolios.length} portfolios · ${APP_IDS.length} applications · ${D.roadmap.workPackages.length} changes · ${D.arbs.length} reviews`;
    let summary = cnt;
    if (s.page && s.page.kind === 'element') summary = kindName(EL[s.page.id]) + ' · ' + EL[s.page.id].title;
    else if (s.page && s.page.kind === 'arb') summary = ARB[s.page.id].board + ' · ' + ARB[s.page.id].title;
    else if (s.page && s.page.kind === 'change') summary = 'Change · ' + EL[s.page.id].title;
    else if (s.page && s.page.kind === 'doc') summary = ((CDOC.docs[s.page.id] || []).find(x => x.id === s.page.doc) || {}).title + ' · ' + EL[s.page.id].title;
    else if (s.area === 'views') { const L = s.level; const vd = VIEWS[L].find(x => x[0] === s.view[L]); summary = (L === 'enterprise' ? D.enterprise.title : L === 'portfolio' ? PF[s.pf].title : APPS[s.app].title) + ' · ' + vd[1]; }
    else summary = s.area === 'elements' ? 'Elements · ' + D.elements.length : 'Process · ' + ({ intake: 'Intake', changes: 'Changes', reviews: 'Reviews', decisions: 'Decisions', checks: 'Model checks', how: 'How it works' })[s.proc];
    const openArbs = D.arbs.filter(a => a.status !== 'approved' && a.status !== 'rejected').length;
    const go = {}, pick = {}; D.elements.forEach(e => { go[sid(e.id)] = self.go(e.id); pick[sid(e.id)] = self.sel(e.id); }); D.arbs.forEach(a => { go[sid(a.id)] = self.go(a.id); }); APP_IDS.forEach(a => { go['app_' + sid(a)] = self.openApp(a); });
    return { go, pick,
      hdrFeature: 'Docs · Architecture', hdrSummary: summary, hdrPlaceholder: s.area === 'elements' && !s.page ? 'Search the architecture model, or ask' : 'Search, or ask the assistant…', onHdrQ: e => { const v = e.target.value; self.setState(Object.assign({ q: v }, v && (self.state.area !== 'elements' || self.state.page) ? { area: 'elements', page: null } : {})); }, userName: R.name, userSub: R.sub, userAv: R.av,
      roles: Object.keys(ROLE_VIEW).map(k => ({ id: k, label: ROLE_VIEW[k].label, on: s.role === k, cls: s.role === k ? 'chip-on' : '', pick: self.set({ role: k }) })),
      entTitle: D.enterprise.title, counts: cnt, modelValid: chip({ x: [v.errors ? 'error' : v.warnings ? 'warning' : 'success', v.errors ? '✕' : v.warnings ? '!' : '✓', v.errors ? `${v.errors} blocking errors` : v.warnings ? `Model valid · ${v.warnings} warnings` : 'Model valid'] }, 'x'),
      checksPassed: `${v.passed} checks passed · ${D.elements.length} elements · main @ 4a1b9e0`,
      areas: [['elements', 'Elements', String(D.elements.length)], ['views', 'Views', ''], ['process', 'Process', openArbs + ' open']].map(a => ({ id: a[0], label: a[1], n: a[2], hasN: !!a[2], on: s.area === a[0], cls: s.area === a[0] ? 'tab-on' : '', pick: self.openArea(a[0]) })),
      isViews: !s.page && s.area === 'views', isCat: !s.page && s.area === 'elements', isProc: !s.page && s.area === 'process',
      isElementPage: !!s.page && s.page.kind === 'element', isArbPage: !!s.page && s.page.kind === 'arb', isChangePage: !!s.page && s.page.kind === 'change', isDocPage: !!s.page && s.page.kind === 'doc', noPage: !s.page,
      hasToast: !!s.toast, toast: s.toast || '', closeToast: self.set({ toast: null }),
      backHome: self.back(),
    };
  }

  // ---------- views ----------
  viewVals() {
    const s = this.state, self = this, L = s.level, cur = s.view[L];
    const lv = [['enterprise', 'Enterprise'], ['portfolio', 'Portfolio'], ['application', 'Application']];
    const list = VIEWS[L].map(v => ({ id: v[0], title: v[1], who: v[2], kind: KIND_LABEL[v[4]], kcls: 'vk-' + v[4], on: cur === v[0], cls: cur === v[0] ? 'sl-on' : '', pick: self.openView(L, v[0]) }));
    const vd = VIEWS[L].find(v => v[0] === cur);
    const chain = L === 'portfolio' ? s.pf : L === 'application' ? (APPS[s.app].portfolio) : null;
    const plats = chain ? land(chain).plateaus : TAGS.map(t => ({ tag: t, title: TAG_NAME[t], description: t === 'baseline' ? 'As it runs today, in every portfolio.' : t === 'target' ? 'The target of every portfolio.' : 'The first transition of every portfolio.' }));
    const pl = plats.find(p => p.tag === s.plateau) || plats[plats.length - 1];
    const tag = pl.tag;
    const out = {
      levels: lv.map(l => ({ id: l[0], label: l[1], on: L === l[0], cls: L === l[0] ? 'seg-on' : '', pick: self.set({ level: l[0], sel: null }) })),
      isEnt: L === 'enterprise', isPf: L === 'portfolio', isApp: L === 'application',
      pfs: D.portfolios.map(p => ({ id: p.id, title: p.title, on: s.pf === p.id })), pf: s.pf,
      pickPf: e => self.setState({ pf: e.target.value }),
      apps: APP_IDS.filter(a => APPS[a].portfolio === s.pf).map(a => ({ id: a, title: APPS[a].title })), app: s.app,
      pickApp: e => self.setState({ app: e.target.value }),
      sideList: list, viewTitle: vd[1], viewFor: vd[2], viewDecides: vd[3], viewHow: vd[5], viewKind: KIND_LABEL[vd[4]],
      scopeLabel: (L === 'enterprise' ? 'Enterprise · ' + D.enterprise.title : L === 'portfolio' ? 'Portfolio · ' + PF[s.pf].title : 'Application · ' + APPS[s.app].title).toUpperCase(),
      plateaus: plats.map(p => ({ tag: p.tag, title: p.title, on: tag === p.tag, cls: tag === p.tag ? 'seg-on' : '', pick: self.set({ plateau: p.tag }) })),
      plateauNote: (pl.description || '') + (pl.date ? ' · ' + pl.date : ''),
      hasPlateau: ['capmap', 'coverage', 'roles', 'tech', 'landscape', 'cooperation', 'interaction', 'procapp', 'data', 'apptech', 'chain', 'inside'].indexOf(cur) >= 0,
      gds: [], hasGds: false, relRows: [], hasRelRows: false,
    };
    ['capmap', 'coverage', 'capvs', 'roles', 'tech', 'entroadmap', 'motivation', 'valuestreams', 'landscape', 'cooperation', 'interaction', 'procapp', 'gap', 'data', 'apptech', 'pfroadmap', 'chain', 'factsheet', 'inside', 'interfaces'].forEach(k => { out['v_' + k] = false; });
    const key = (L === 'enterprise' && cur === 'roadmap') ? 'entroadmap' : (L === 'portfolio' && cur === 'roadmap') ? 'pfroadmap' : cur;
    out['v_' + key] = true;
    out.isMatrix = vd[4] === 'matrix';
    const fn = this['v_' + key];
    if (fn) Object.assign(out, fn.call(this, tag, chain));
    // rendering: grid by default, diagram (SVG) where lines carry information
    const DIAG = { motivation: 'motivation', valuestreams: 'valuestreams', cooperation: 'coop_' + sid(s.pf), gap: 'gap_' + sid(s.pf) + '_' + Math.min(s.gap, Math.max(0, land(s.pf).gaps.length - 1)), chain: 'chain_' + sid(s.pf), inside: 'inside_' + sid(s.app) };
    const hasDiagram = !!DIAG[cur], rend = hasDiagram && s.rend[cur] === 'diagram' ? 'diagram' : 'grid';
    out.hasDiagram = hasDiagram; out.isDiagram = rend === 'diagram'; out.showGrids = !!out.hasGds && rend !== 'diagram';
    out.rendSeg = [['grid', 'Grid'], ['diagram', 'Diagram']].map(r => ({ id: r[0], label: r[1], on: rend === r[0], cls: rend === r[0] ? 'seg-on' : '', pick: () => self.setState({ rend: Object.assign({}, self.state.rend, { [cur]: r[0] }) }) }));
    out.gOn = rend === 'diagram' ? { [DIAG[cur]]: true } : {};
    out.zoomStyle = 'zoom: ' + s.zoom; out.zoomIn = self.set({ zoom: Math.min(1.6, Math.round((s.zoom + 0.2) * 10) / 10) }); out.zoomOut = self.set({ zoom: Math.max(0.5, Math.round((s.zoom - 0.2) * 10) / 10) }); out.zoomFit = self.set({ zoom: 1 });
    out.selSid = s.sel ? sid(s.sel) : 'none';
    // frame panel: mark, back, crumbs, view id
    const scope = L === 'enterprise' ? 'ent' : L === 'portfolio' ? s.pf : s.app;
    out.viewId = (L === 'enterprise' ? 'ent' : L === 'portfolio' ? 'pf_' + sid(s.pf) : 'app_' + sid(s.app)) + '_' + cur + (out.hasPlateau ? '_' + sid(tag) : '');
    out.frameMark = rend === 'diagram' ? 'LikeC4' : 'Grid'; if (rend === 'diagram') out.viewKind = 'Diagram';
    out.canBack = s.vhist.length > 0; out.goBack = self.back();
    const crumbs = [{ label: D.enterprise.title, go: self.drill({ level: 'enterprise' }) }];
    if (L !== 'enterprise') crumbs.push({ label: PF[s.pf].title, go: self.drill({ level: 'portfolio', pf: s.pf }) });
    if (L === 'application') crumbs.push({ label: APPS[s.app].title, go: self.drill({ level: 'application', app: s.app }) });
    crumbs.push({ label: vd[1], cur: true, go: () => {} });
    out.crumbs = crumbs.map((c, i) => Object.assign({ cur: false, more: i < crumbs.length - 1 }, c));
    // view source (the generated LikeC4 view)
    const ids = this.collectIds(out);
    out.srcOn = s.srcOn; out.toggleSrc = self.set({ srcOn: !s.srcOn }); out.srcLabel = s.srcOn ? 'Hide the view source' : 'Show the view source';
    out.viewSrc = `view ${out.viewId} ${L === 'enterprise' ? '' : 'of ' + scope + ' '}{\n  title '${vd[1]}'\n  description '${vd[3]}'\n${out.hasPlateau ? "  // plateau " + tag + " · membership from relationships, never tags\n" : ''}  include\n${ids.slice(0, 60).map(i => '    ' + i).join(',\n')}${ids.length > 60 ? ',\n    // … ' + (ids.length - 60) + ' more' : ''}\n  autoLayout TopBottom\n}`;
    out.generatedLine = 'Generated from model/bb/*.c4 · main @ 4a1b9e0 · drawn with the AIToolbox ArchiMate notation · select a figure to see its relationships';
    // element card
    out.card = this.cardOf(s.sel, ids, cur);
    out.hasCard = !!out.card.has; out.frameCls = out.card.has ? 'has-card' : '';
    return out;
  }
  collectIds(obj) {
    const found = {}, seen = [];
    const walk = (o, d) => { if (!o || d > 14 || typeof o !== 'object') return; if (seen.indexOf(o) >= 0) return; seen.push(o);
      if (Array.isArray(o)) { o.forEach(x => walk(x, d + 1)); return; }
      if (typeof o.id === 'string' && EL[o.id]) found[o.id] = true;
      Object.keys(o).forEach(k => { if (k !== 'go' && k !== 'pick' && k !== 'card' && k !== 'crumbs' && typeof o[k] === 'object') walk(o[k], d + 1); }); };
    walk(obj, 0); return Object.keys(found);
  }
  cardOf(id, ids, cur) {
    const self = this, e = id ? EL[id] : null; if (!e) return { has: false };
    const RN = { realization: ['realizes', 'realized by'], serving: ['serves', 'served by'], composition: ['composed of', 'part of'], aggregation: ['aggregates', 'in plateau'], assignment: ['assigned to', 'assigned'], access: ['accesses', 'accessed by'], flow: ['flows to', 'flow from'], triggering: ['triggers', 'triggered by'], influence: ['influences', 'influenced by'], association: ['associated with', 'associated with'] };
    const inView = D.relations.filter(r => (r.s === id && ids.indexOf(r.t) >= 0) || (r.t === id && ids.indexOf(r.s) >= 0) ).filter(r => !(r.k === 'aggregation' && EL[r.s] && EL[r.s].kind === 'plateau'));
    const all = D.relations.filter(r => r.s === id || r.t === id).filter(r => !(r.k === 'aggregation' && EL[r.s] && EL[r.s].kind === 'plateau'));
    const use = inView.length ? inView : all.slice(0, 8);
    const rels = use.map(r => { const out = r.s === id, o = out ? r.t : r.s, oe = EL[o]; return { verb: (RN[r.k] || [r.k, r.k])[out ? 0 : 1], label: r.l || '', hasLabel: !!r.l, name: title(o), layer: oe ? layerOf(oe) : 'other', kind: oe ? oe.kind : '', hasTile: !!oe, inView: ids.indexOf(o) >= 0, pick: oe ? self.sel(o) : () => {}, ext: !!r.ext }; });
    const app = appOf(e), nav = self.navigateTo(e);
    const ORIGIN = e.ext ? 'Prototype data' : (e._path || '').indexOf('changes/') >= 0 ? 'Change file · ' + (e._path || '').split('/').pop() : 'Model · authored';
    return { has: true, id, title: e.title, kind: kindName(e), layer: layerOf(e), k: e.kind, desc: e.description || '', hasDesc: !!e.description, owner: e.owner || '—', origin: ORIGIN, track: self.track(e), hasTrack: !!self.track(e).length,
      change: e.change ? chip(CHANGE, e.change) : nochip, hasChange: !!e.change, status: e.status ? chip(STATUS, e.status) : nochip, hasStatus: !!e.status,
      rels, hasRels: !!rels.length, relsTitle: inView.length ? 'In this view' : 'In the model (none in this view)',
      hasNav: !!nav, navLabel: nav ? nav.label : '', nav: nav ? nav.go : () => {}, open: self.go(id), hasDd: !!(e.dd && e.dd.length), dd: e.dd && e.dd.length ? self.go(e.dd[0]) : () => {}, close: self.set({ sel: null }),
      hasApp: !!app && e.kind !== 'application-component', appTitle: app ? APPS[app].title : '', openApp: app ? self.openApp(app) : () => {} };
  }
  // -- generic matrix: {cols:[{label,sub,title}], rows:[{group,label,head:{...},cells:[{txt,cls,title,go}]}], legend:[{cls,g,w,note}]}
  mxHead(e, extra) { return Object.assign({ id: e.id, label: e.title, sub: kindName(e), layer: layerOf(e), kind: e.kind, go: this.sel(e.id), selCls: this.state.sel === e.id ? 'mx-sel' : '', hasTile: true, warn: false, warnText: '' }, extra || {}); }
  appHead(a) { const c = APPS[a].components[0]; return { id: c, label: APPS[a].title, sub: PF[APPS[a].portfolio] ? PF[APPS[a].portfolio].title : '', layer: 'application', kind: 'application-component', go: this.sel(c), selCls: this.state.sel === c ? 'mx-sel' : '', hasTile: true, warn: false, warnText: '' }; }
  cell(txt, cls, ttl, go) { return { txt: txt || '', cls: cls || (txt ? 'on' : 'off'), title: ttl || '', go: go || null, hasGo: !!go }; }

  v_capmap(tag) {
    const s = this.state, self = this;
    const metrics = [['maturity', 'Maturity'], ['investment', 'Investment'], ['applications', 'Applications']];
    const INV = { none: 0, low: 1, medium: 2, high: 3 };
    const domains = D.capabilities.map(d => ({ id: d.id, title: d.title, caps: d.children.map(c => {
      const e = EL[c], md = e.meta || {}, apps = appsRealizing(c, tag), mat = Number(md.maturity || 0), inv = INV[md.investment || 'none'];
      const val = s.metric === 'maturity' ? mat : s.metric === 'investment' ? inv : apps.length;
      const max = s.metric === 'maturity' ? 5 : s.metric === 'investment' ? 3 : Math.max(3, apps.length);
      const shade = Math.round(8 + 48 * (max ? val / max : 0));
      const warn = (md.strategic === 'differentiating' && mat < 3) ? 'Strengthen' : apps.length === 0 ? 'No application' : '';
      return { id: c, title: e.title, val: s.metric === 'investment' ? (md.investment || 'none') : String(val), den: s.metric === 'maturity' ? '/5' : '', strategic: md.strategic || '', napps: apps.length + (apps.length === 1 ? ' app' : ' apps'), warn, hasWarn: !!warn, style: `background: color-mix(in srgb, #35307E ${shade}%, #FFFFFF)`, selCls: s.sel === c ? 'ax-sel' : '', go: self.sel(c) };
    }) }));
    return { metrics: metrics.map(m => ({ id: m[0], label: m[1], on: s.metric === m[0], cls: s.metric === m[0] ? 'seg-on' : '', pick: self.set({ metric: m[0] }) })), domains };
  }
  v_coverage(tag) {
    const self = this, cols = D.portfolios.map(p => ({ label: p.title, sub: p.applications.length + ' apps', title: p.title }));
    const rows = []; let gaps = 0, overlaps = 0;
    D.capabilities.forEach(d => {
      rows.push({ group: true, label: d.title, isRow: false });
      d.children.forEach(c => {
        const apps = appsRealizing(c, tag); const cells = D.portfolios.map(p => { const a = apps.filter(x => APPS[x].portfolio === p.id); if (a.length > 1) overlaps++; return self.cell(a.map(x => APPS[x].title).join(' · '), a.length > 1 ? 'warn' : a.length ? 'on' : 'off', a.length > 1 ? 'Overlap: ' + a.length + ' applications realize this capability in one portfolio' : '', null); });
        if (!apps.length) gaps++;
        rows.push({ group: false, isRow: true, head: self.mxHead(EL[c], { warn: !apps.length, warnText: 'Gap: no application' }), cells });
      });
    });
    return { mx: { cols, rows, legend: [{ cls: 'on', g: '', w: 'Realized', note: 'applications in the plateau' }, { cls: 'warn', g: '!', w: 'Overlap', note: 'two applications in one portfolio' }, { cls: 'off', g: '', w: 'Gap', note: 'row with no application' }], headLabel: 'Capability', summary: `${gaps} gaps · ${overlaps} overlaps · ${TAG_NAME[tag]}` } };
  }
  v_capvs(tag) {
    const self = this; const cols = [], groups = [];
    VS.forEach(vs => { const st = stagesOf(vs.id); groups.push({ label: vs.title, span: st.length }); st.forEach(sg => cols.push({ id: sg, label: EL[sg].title, sub: vs.title, title: EL[sg].title, go: self.sel(sg), stage: sg })); });
    const rows = []; let unused = 0;
    D.capabilities.forEach(d => {
      rows.push({ group: true, label: d.title, isRow: false });
      d.children.forEach(c => {
        const served = relOut(c).filter(r => r.k === 'serving' && EL[r.t] && EL[r.t].kind === 'value-stream').map(r => r.t);
        const cells = cols.map(col => { const on = served.indexOf(col.stage) >= 0; return self.cell(on ? '●' : '', on ? 'dot' : 'off', on ? EL[c].title + ' serves ' + col.label : '', null); });
        if (!served.length) unused++;
        rows.push({ group: false, isRow: true, head: self.mxHead(EL[c], { warn: !served.length, warnText: 'Serves no stage' }), cells });
      });
    });
    const stageGaps = cols.filter((col, i) => !rows.some(r => r.isRow && r.cells[i].cls === 'dot')).length;
    return { mx: { cols, colGroups: groups, hasGroups: true, rows, legend: [{ cls: 'dot', g: '●', w: 'Serves', note: 'the capability serves the stage (ArchiMate serving)' }, { cls: 'warn', g: '!', w: 'Off the path', note: 'capability serving no stage' }], headLabel: 'Capability', summary: `${VS.length} value streams · ${cols.length} stages · ${unused} capabilities off every stream · ${stageGaps} stages without a capability` } };
  }
  v_roles(tag) {
    const self = this, cols = ROLES.map(r => ({ id: r.id, label: r.title, sub: r.description, title: r.title, go: self.sel(r.id) }));
    const rows = []; let noA = 0;
    D.portfolios.forEach(p => {
      const procs = PROCS.filter(e => e.portfolio === p.id && inP(e, tag));
      if (!procs.length) return;
      rows.push({ group: true, label: p.title, isRow: false });
      procs.forEach(pr => {
        const asg = relIn(pr.id).filter(r => r.k === 'assignment');
        const hasA = asg.some(r => r.raci === 'A');
        if (!hasA) noA++;
        rows.push({ group: false, isRow: true, head: self.mxHead(pr, { warn: !hasA, warnText: 'No role decides (A)' }), cells: ROLES.map(r => { const a = asg.find(x => x.s === r.id); return self.cell(a ? a.raci : '', a ? 'raci-' + a.raci : 'off', a ? r.title + ' ' + a.l + ' · ' + pr.title : '', null); }) });
      });
    });
    return { mx: { cols, rows, legend: [{ cls: 'raci-R', g: 'R', w: 'Performs', note: 'responsible' }, { cls: 'raci-A', g: 'A', w: 'Decides', note: 'accountable, one per process' }, { cls: 'raci-C', g: 'C', w: 'Consulted', note: '' }, { cls: 'raci-I', g: 'I', w: 'Informed', note: '' }], headLabel: 'Business process', summary: `${rows.filter(r => r.isRow).length} processes in ${TAG_NAME[tag]} · ${ROLES.length} roles · ${noA} without a decider`, ext: 'Roles and assignments are prototype data: the Meridian Bank model has no business roles yet.' } };
  }
  v_tech(tag) {
    const self = this, cats = uniq(D.technology.map(t => t.category));
    const rows = cats.map(c => ({ label: c, cells: RINGS.map(r => ({ ring: r, items: D.technology.filter(t => t.category === c && t.lifecycle === r).map(t => { const n = compApps(t.usedBy.filter(u => inP(EL[u], tag))).length; return { id: t.id, title: EL[t.id].title, n: String(n), cls: 'life-' + r + (self.state.sel === t.id ? ' ax-sel' : ''), go: self.sel(t.id) }; }) })) }));
    const risky = []; D.technology.filter(t => t.lifecycle === 'hold' || t.lifecycle === 'retire').forEach(t => compApps(t.usedBy.filter(u => inP(EL[u], tag))).forEach(a => risky.push({ app: APPS[a].title, appId: a, tech: EL[t.id].title, ring: chip(LIFE, t.lifecycle), time: chip(TIME, APPS[a].time), pf: PF[APPS[a].portfolio].title, go: self.openApp(a) })));
    risky.sort((a, b) => (a.ring.w + a.app).localeCompare(b.ring.w + b.app));
    return { rings: RINGS.map(r => ({ id: r, label: LIFE[r][2], hint: { adopt: 'Default for new work', trial: 'Allowed in a bounded scope', hold: 'No new use', retire: 'Being removed' }[r] })), techRows: rows, risky, riskyN: risky.length + ' application uses of Hold or Retire standards in ' + TAG_NAME[tag] };
  }
  roadmapBands(pfIds) {
    const self = this, M = D.roadmap.months, n = M.length, pct = i => (100 * i / n).toFixed(2) + '%';
    const pos = d => { const i = M.indexOf(d.slice(0, 7)); if (i < 0) return d < M[0] ? 0 : 100; return 100 * (i + (Number(d.slice(8, 10)) - 1) / 30) / n; };
    const today = pos(TODAY).toFixed(2) + '%';
    return { months: M.map(m => ({ label: m.slice(5) === '01' ? m.slice(0, 4) : m.slice(5), cls: m.slice(5) === '01' ? 'y' : '' })), todayStyle: 'left: ' + today, bands: pfIds.map(p => {
      const Lp = land(p);
      return { id: p, title: PF[p].title, go: self.openView('portfolio', 'roadmap', { pf: p }),
        plateaus: Lp.plateaus.filter(x => x.date).map((x, i) => ({ title: x.title, style: 'left: ' + pos(x.date).toFixed(2) + '%; top: ' + (i % 2 ? 16 : 2) + 'px' })),
        wps: D.roadmap.workPackages.filter(w => w.chain === p).map(w => { const l = pos(w.start), r = pos(w.end), arb = D.arbs.find(a => a.workItemId === w.workItemId); return { id: w.id, title: w.title, cls: 'wp-' + w.status + (arb ? ' wp-' + arb.status : ''), style: `left: ${l.toFixed(2)}%; width: ${Math.max(2, r - l).toFixed(2)}%`, dep: w.dependsOn.length ? 'after ' + w.dependsOn.map(title).join(', ') : '', hasDep: !!w.dependsOn.length, klass: w.class, arb: arb ? chip(ARB_STATUS, arb.status) : nochip, hasArb: !!arb, goArb: arb ? self.go(arb.id) : null, go: self.go(w.id), dates: w.start + ' → ' + w.end }; }) };
    }) };
  }
  v_entroadmap() { return { rm: this.roadmapBands(D.portfolios.map(p => p.id)) }; }
  v_pfroadmap(tag, chain) { return { rm: this.roadmapBands([chain]) }; }
  fig(id, extra) { const e = EL[id]; const n = NOTE[e.kind] || { layer: 'other', shape: 'square', name: e.kind }; const f = Object.assign({ id, title: e.title, kind: e.kind, layer: n.layer, shape: n.shape, kname: n.name, cls: '', rel: '', hasRel: false, go: this.sel(id) }, extra || {}); if (this.state.sel === id) f.cls += ' ax-sel'; return f; }
  gcell(figs, note, cls) { return { figs, note: note || '', hasNote: !!note, cls: cls || '', empty: !figs.length }; }
  grid(title, cols, rows, note) { return { title, note: note || '', hasNote: !!note, cols: cols.map(c => typeof c === 'string' ? { label: c, sub: '' } : c), rows, tpl: cols.map(() => 'minmax(150px, 1fr)').join(' ') }; }
  v_motivation() {
    const self = this, drivers = D.elements.filter(e => e.kind === 'driver');
    const rows = drivers.map(d => {
      const stake = relIn(d.id).filter(r => r.k === 'association' && EL[r.s].kind === 'stakeholder').map(r => self.fig(r.s));
      const assess = relIn(d.id).filter(r => r.k === 'association' && EL[r.s].kind === 'assessment').map(r => self.fig(r.s));
      const goals = relOut(d.id).filter(r => r.k === 'influence').map(r => r.t);
      const outcomes = uniq([].concat.apply([], goals.map(g => relIn(g).filter(r => r.k === 'realization' && EL[r.s].kind === 'outcome').map(r => r.s))));
      const reqs = uniq([].concat.apply([], outcomes.map(o => relIn(o).filter(r => r.k === 'realization' && EL[r.s].kind === 'requirement').map(r => r.s))));
      return { cells: [self.gcell(stake), self.gcell([self.fig(d.id)]), self.gcell(assess), self.gcell(goals.map(g => self.fig(g, { rel: 'influences', hasRel: true }))), self.gcell(outcomes.map(o => self.fig(o, { rel: 'realizes the goal', hasRel: true }))), self.gcell(reqs.map(r => self.fig(r, { rel: 'realizes the outcome', hasRel: true })), reqs.length ? '' : 'No requirement yet', reqs.length ? '' : 'gd-warn')] };
    });
    const principles = D.elements.filter(e => e.kind === 'principle').map(p => self.fig(p.id));
    return { gds: [self.grid('Why each change exists', ['Stakeholder', 'Driver', 'Assessment', 'Goal', 'Outcome', 'Requirement'], rows, 'Read left to right: who cares, about what, measured how, towards which goal, with which outcome, delivered by which requirement.'), self.grid('Principles that constrain every change', principles.map(() => ({ label: 'Principle', sub: 'applies to every change' })), [{ cells: principles.map(p => self.gcell([p])) }], '')], hasGds: true };
  }
  v_valuestreams() {
    const self = this;
    const gds = VS.map(vs => { const st = stagesOf(vs.id); const nxt = {}; relOut(vs.id).forEach(() => {}); D.relations.filter(r => r.k === 'triggering' && st.indexOf(r.s) >= 0).forEach(r => { nxt[r.s] = r.t; }); const first = st.filter(x => Object.keys(nxt).every(k => nxt[k] !== x)); const order = []; let cur = first[0] || st[0]; while (cur && order.indexOf(cur) < 0) { order.push(cur); cur = nxt[cur]; }
      const cols = order.map((sg, i) => ({ label: (i + 1) + ' · ' + EL[sg].title, sub: i + 1 < order.length ? 'triggers the next stage ›' : 'last stage' }));
      const row = { cells: order.map(sg => { const caps = relIn(sg).filter(r => r.k === 'serving').map(r => self.fig(r.s, { rel: 'serves', hasRel: true })); return self.gcell(caps, caps.length ? '' : 'No capability serves this stage', caps.length ? '' : 'gd-warn'); }) };
      return self.grid(vs.title, cols, [row], 'Stages are the columns, in order; each cell lists the capabilities that serve the stage.'); });
    return { gds, hasGds: true };
  }
  v_landscape(tag, chain) {
    const self = this, p = PF[chain], Lp = land(chain), i = Lp.plateaus.findIndex(x => x.tag === tag), prev = i > 0 ? Lp.plateaus[i - 1].tag : null;
    const apps = p.applications;
    const caps = uniq([].concat.apply([], apps.map(a => (D.realizes[APPS[a].components[0]] || []))));
    const rows = caps.map(c => {
      const cells = apps.filter(a => (D.realizes[APPS[a].components[0]] || []).indexOf(c) >= 0 && (inP(EL[APPS[a].components[0]], tag) || (prev && inP(EL[APPS[a].components[0]], prev)))).map(a => {
        const inNow = inP(EL[APPS[a].components[0]], tag), ch = appChange(a, tag);
        const cid = APPS[a].components[0]; return { id: cid, title: APPS[a].title, time: chip(TIME, APPS[a].time), change: ch ? chip(CHANGE, ch) : nochip, hasChange: !!ch, cls: (!inNow ? 'ax-retired' : '') + (self.state.sel === cid ? ' ax-sel' : ''), go: self.sel(cid) };
      });
      return { id: c, title: EL[c].title, n: cells.filter(x => x.cls.indexOf('ax-retired') < 0).length + ' application' + (cells.filter(x => x.cls.indexOf('ax-retired') < 0).length === 1 ? '' : 's'), cells, selCls: self.state.sel === c ? 'ax-sel' : '', go: self.sel(c) };
    });
    return { lsRows: rows };
  }
  flowsOf(chain, tag) { return D.flows.filter(f => (COMP2APP[f.source] && APPS[COMP2APP[f.source]].portfolio === chain || COMP2APP[f.target] && APPS[COMP2APP[f.target]].portfolio === chain) && inP(EL[f.source], tag) && inP(EL[f.target], tag)); }
  v_cooperation(tag, chain) {
    const self = this, fl = this.flowsOf(chain, tag), mine = PF[chain].applications.filter(a => inP(EL[APPS[a].components[0]], tag));
    const nf = (c, lbl, dir) => self.fig(c, { rel: (dir === 'in' ? '← ' : '→ ') + lbl, hasRel: true, cls: APPS[COMP2APP[c]].portfolio === chain ? '' : 'ax-muted', sub: PF[APPS[COMP2APP[c]].portfolio].title });
    const rows = mine.map(a => { const c = APPS[a].components[0]; const ins = fl.filter(f => f.target === c).map(f => nf(f.source, f.title, 'in')); const outs = fl.filter(f => f.source === c).map(f => nf(f.target, f.title, 'out')); return { cells: [self.gcell(ins, ins.length ? '' : 'receives nothing'), self.gcell([self.fig(c)], '', 'gd-self'), self.gcell(outs, outs.length ? '' : 'sends nothing')] }; });
    return { gds: [self.grid(PF[chain].title + ' · ' + TAG_NAME[tag], [{ label: 'Receives from', sub: 'application · what flows in' }, { label: 'Application', sub: 'of the portfolio' }, { label: 'Sends to', sub: 'application · what flows out' }], rows, 'Faded figures are applications of another portfolio.')], hasGds: true,
      flowRows: fl.map(f => ({ from: APPS[COMP2APP[f.source]].title, to: APPS[COMP2APP[f.target]].title, what: f.title, goFrom: self.openApp(COMP2APP[f.source]), goTo: self.openApp(COMP2APP[f.target]), pfFrom: PF[APPS[COMP2APP[f.source]].portfolio].title, pfTo: PF[APPS[COMP2APP[f.target]].portfolio].title })), flowN: fl.length + ' flows in ' + TAG_NAME[tag] };
  }
  v_interaction(tag, chain) {
    const self = this, mine = PF[chain].applications.filter(a => inP(EL[APPS[a].components[0]], tag));
    const fl = D.flows.filter(f => inP(EL[f.source], tag) && inP(EL[f.target], tag));
    const others = uniq([].concat.apply([], mine.map(a => fl.filter(f => COMP2APP[f.source] === a).map(f => COMP2APP[f.target]).concat(fl.filter(f => COMP2APP[f.target] === a).map(f => COMP2APP[f.source]))))).filter(Boolean);
    const colApps = uniq(mine.concat(others.filter(o => mine.indexOf(o) < 0).sort((a, b) => (APPS[a].portfolio + APPS[a].title).localeCompare(APPS[b].portfolio + APPS[b].title))));
    const cols = colApps.map(a => ({ id: APPS[a].components[0], label: APPS[a].title, sub: PF[APPS[a].portfolio].title, title: APPS[a].title, go: self.sel(APPS[a].components[0]), cls: APPS[a].portfolio === chain ? '' : 'mx-ext' })).concat([{ label: 'Depends on', sub: 'count', title: 'Number of applications this one sends to or reads from', cls: 'mx-sum' }]);
    const rows = mine.map(a => { let n = 0; const cells = colApps.map(b => { if (a === b) return self.cell('', 'diag', '', null); const out = fl.filter(f => COMP2APP[f.source] === a && COMP2APP[f.target] === b).map(f => f.title); const inn = fl.filter(f => COMP2APP[f.source] === b && COMP2APP[f.target] === a).length; if (out.length || inn) n++; return self.cell(out.join(' · ') || (inn ? '←' : ''), out.length ? 'on' : inn ? 'in' : 'off', out.length ? APPS[a].title + ' → ' + APPS[b].title + ': ' + out.join(', ') : inn ? 'receives ' + inn + ' flow' + (inn > 1 ? 's' : '') + ' from ' + APPS[b].title : '', null); }); cells.push(self.cell(String(n), n > 4 ? 'warn' : 'sum', n > 4 ? 'Highly coupled: more than 4 dependencies' : '', null)); return { group: false, isRow: true, head: self.appHead(a), cells }; });
    return { mx: { cols, rows, legend: [{ cls: 'on', g: '', w: 'Sends', note: 'flow from the row to the column, with its name' }, { cls: 'in', g: '←', w: 'Receives only', note: 'the column sends to the row' }, { cls: 'warn', g: '!', w: 'Coupled', note: 'more than 4 dependencies' }], headLabel: 'Application', summary: `${mine.length} applications · ${others.filter(o => mine.indexOf(o) < 0).length} neighbours in other portfolios · ${fl.filter(f => mine.indexOf(COMP2APP[f.source]) >= 0 || mine.indexOf(COMP2APP[f.target]) >= 0).length} flows in ${TAG_NAME[tag]}` } };
  }
  v_procapp(tag, chain) {
    const self = this, apps = PF[chain].applications.filter(a => inP(EL[APPS[a].components[0]], tag));
    const procs = PROCS.filter(p => p.portfolio === chain && inP(p, tag));
    const cols = apps.map(a => ({ id: APPS[a].components[0], label: APPS[a].title, sub: TIME[APPS[a].time][2], title: APPS[a].title, go: self.sel(APPS[a].components[0]) }));
    const unused = apps.filter(a => !procs.some(p => relIn(p.id).some(r => r.k === 'serving' && COMP2APP[r.s] === a)));
    const rows = procs.map(p => { const sup = relIn(p.id).filter(r => r.k === 'serving').map(r => COMP2APP[r.s]); const n = apps.filter(a => sup.indexOf(a) >= 0).length; return { group: false, isRow: true, head: self.mxHead(p, { warn: !n, warnText: 'Manual: no application supports it' }), cells: apps.map(a => self.cell(sup.indexOf(a) >= 0 ? '●' : '', sup.indexOf(a) >= 0 ? 'dot' : 'off', sup.indexOf(a) >= 0 ? APPS[a].title + ' supports ' + p.title : '', null)) }; });
    return { mx: { cols, rows, legend: [{ cls: 'dot', g: '●', w: 'Supports', note: 'application component serves the process' }, { cls: 'warn', g: '!', w: 'Manual', note: 'process with no application' }], headLabel: 'Business process', summary: `${procs.length} processes · ${apps.length} applications in ${TAG_NAME[tag]} · ${unused.length} application${unused.length === 1 ? '' : 's'} supporting no process (${unused.map(a => APPS[a].title).join(', ') || '—'})`, ext: 'The supports relationships are prototype data (application component serving a business process).' } };
  }
  v_gap(tag, chain) {
    const self = this, Lp = land(chain), gi = Math.min(this.state.gap, Lp.gaps.length - 1), g = Lp.gaps[gi];
    const items = g.items.filter(it => it.change !== 'unchanged'); const rows = items.map(it => { const e = EL[it.id]; const wp = it.addressedBy.map(w => ({ title: title(w), go: self.go(w), arb: (D.arbs.find(a => a.workItemId === (EL[w] || {}).workItemId) || {}).id })); const arb = wp.length && wp[0].arb ? ARB[wp[0].arb] : null; const rq = self.reqOfItem(it.id, it.addressedBy); const tks = it.change === 'retired' ? self.ticketsReplacing(it.id) : self.ticketsForEl(it.id); const tdone = tks.filter(t => t.state === 'done').length; return { id: it.id, title: e.title, kind: kindName(e), layer: layerOf(e), k: e.kind, change: chip(CHANGE, it.change), level: LEVEL_NAME[e.level], track: self.track(e), by: wp, hasBy: !!wp.length, reqId: rq, dl: tks.length ? tdone + '/' + tks.length + (tks.length > 1 ? ' tickets' : ' ticket') : '—', dlCls: tks.length ? (tdone === tks.length ? 'dl-done' : tks.some(t => t.state === 'doing') ? 'dl-doing' : '') : '', arb: arb ? chip(ARB_STATUS, arb.status) : nochip, hasArb: !!arb, goArb: arb ? self.go(arb.id) : null, go: self.go(it.id) }; });
    const n = { new: 0, changed: 0, retired: 0 }; items.forEach(it => { n[it.change] = (n[it.change] || 0) + 1; });
    return { gaps: Lp.gaps.map((x, i) => ({ label: TAG_NAME[x.from] + ' → ' + TAG_NAME[x.to], on: i === gi, cls: i === gi ? 'seg-on' : '', pick: self.set({ gap: i }) })), gapRows: rows, gapReqs: uniq(rows.map(r => r.reqId).filter(Boolean)).map(q => ({ title: title(q), go: self.go(q) })), hasGapReqs: rows.some(r => r.reqId), gapSummary: `${n.new} new · ${n.changed} changed · ${n.retired} retired · delivered by ${uniq([].concat.apply([], items.map(it => it.addressedBy))).map(title).join(', ')}`,
      gds: [self.grid('Applications that change · ' + TAG_NAME[g.from] + ' → ' + TAG_NAME[g.to], ['New', 'Changed', 'Retired'], [{ cells: ['new', 'changed', 'retired'].map(ch => self.gcell(g.items.filter(it => it.change === ch && EL[it.id].kind === 'application-component').map(it => self.fig(it.id, { cls: 'ax-chg-' + ch })), '', '')) }], 'Application components only; the table lists every building block of the gap.')], hasGds: true };
  }
  v_data(tag, chain) {
    const self = this, apps = PF[chain].applications.filter(a => inP(EL[APPS[a].components[0]], tag));
    const bos = uniq(D.data.filter(d => inP(EL[d.id], tag)).map(d => d.bo)).sort((a, b) => title(a).localeCompare(title(b)));
    const rows = []; let multi = 0;
    bos.forEach(bo => { const ds = D.data.filter(d => d.bo === bo && inP(EL[d.id], tag)); const cells = apps.map(a => { const d = ds.find(x => COMP2APP[x.component] === a); return self.cell(d ? (d.mode === 'master' ? 'M' : 'C') : '', d ? 'mode-' + d.mode : 'off', d ? APPS[a].title + ' holds a ' + d.mode + ' of ' + title(bo) + ' (' + EL[d.id].title + ')' : '', d ? self.sel(d.id) : null); }); const masters = ds.filter(x => x.mode === 'master'); const elsewhere = masters.filter(x => apps.indexOf(COMP2APP[x.component]) < 0); if (masters.length > 1) multi++; if (!cells.some(c => c.cls !== 'off')) return; rows.push({ group: false, isRow: true, head: self.mxHead(EL[bo], { warn: masters.length > 1, warnText: masters.length + ' masters', sub: masters.length ? 'master: ' + masters.map(x => APPS[COMP2APP[x.component]].title).join(', ') : 'no master' }), cells }); });
    return { mx: { cols: apps.map(a => ({ id: APPS[a].components[0], label: APPS[a].title, sub: TIME[APPS[a].time][2], title: APPS[a].title, go: self.sel(APPS[a].components[0]) })), rows, legend: [{ cls: 'mode-master', g: 'M', w: 'Master', note: 'system of record' }, { cls: 'mode-copy', g: 'C', w: 'Copy', note: 'reads a copy' }, { cls: 'warn', g: '!', w: 'Several masters', note: 'one master per object is the rule' }], headLabel: 'Business object', summary: `${rows.length} business objects held in the portfolio · ${multi} with more than one master (enterprise-wide)` } };
  }
  v_apptech(tag, chain) {
    const self = this, apps = PF[chain].applications.filter(a => inP(EL[APPS[a].components[0]], tag));
    const cats = uniq(D.technology.map(t => t.category)); const techs = []; const groups = cats.map(c => { const ts = D.technology.filter(t => t.category === c); ts.forEach(t => techs.push(t)); return { label: c, span: ts.length }; });
    const cols = techs.map(t => ({ id: t.id, label: EL[t.id].title, sub: LIFE[t.lifecycle][2], title: EL[t.id].title + ' · ' + LIFE[t.lifecycle][2], go: self.sel(t.id), cls: 'life-h-' + t.lifecycle }));
    let risky = 0;
    const rows = apps.map(a => { const comp = APPS[a].components[0]; const used = techs.filter(t => t.usedBy.indexOf(comp) >= 0); const bad = used.some(t => t.lifecycle === 'retire'); if (bad) risky++; return { group: false, isRow: true, head: self.appHead(a), cells: techs.map(t => { const on = t.usedBy.indexOf(comp) >= 0; return self.cell(on ? '●' : '', on ? 'life-' + t.lifecycle : 'off', on ? APPS[a].title + ' runs on ' + EL[t.id].title + ' (' + LIFE[t.lifecycle][2] + ')' : '', null); }) }; }).map(r => { r.head.warn = r.cells.some(c => c.cls === 'life-retire'); r.head.warnText = 'Uses a Retire standard'; return r; });
    return { mx: { cols, colGroups: groups, hasGroups: true, rows, legend: RINGS.map(r => ({ cls: 'life-' + r, g: '●', w: LIFE[r][2], note: { adopt: 'default for new work', trial: 'bounded scope', hold: 'no new use', retire: 'exit planned' }[r] })), headLabel: 'Application', summary: `${apps.length} applications in ${TAG_NAME[tag]} · ${risky} on a Retire standard` } };
  }
  v_chain(tag, chain) {
    const self = this, reqs = D.elements.filter(e => e.kind === 'requirement' && e.portfolio === chain);
    const rows = reqs.map(r => { const abbs = relIn(r.id).filter(x => x.k === 'realization' && EL[x.s].level === 'abb').map(x => x.s); let sbbs = uniq([].concat.apply([], abbs.map(a => relIn(a).filter(x => x.k === 'realization' && EL[x.s].level === 'sbb' && inP(EL[x.s], tag)).map(x => x.s)))); sbbs = uniq(sbbs.concat([].concat.apply([], sbbs.map(b => relIn(b).filter(x => x.k === 'composition' && EL[x.s].kind === 'application-component').map(x => x.s))))); const dds = sbbs.filter(sb => EL[sb].kind === 'application-component'); const withDd = dds.filter(sb => (EL[sb].dd || []).length);
      return { cells: [self.gcell([self.fig(r.id)]), self.gcell(abbs.map(a => self.fig(a, { rel: 'realizes', hasRel: true })), abbs.length ? '' : 'No ABB realizes it (T4)', abbs.length ? '' : 'gd-warn'), self.gcell(sbbs.map(b => self.fig(b, { rel: 'realizes', hasRel: true })), sbbs.length ? '' : 'Nothing in ' + TAG_NAME[tag], sbbs.length ? '' : 'gd-warn'), self.gcell(withDd.map(sb => self.fig(EL[sb].dd[0], { rel: 'for ' + EL[sb].title, hasRel: true })), dds.length ? (withDd.length + '/' + dds.length + ' components have a DD' + (withDd.length < dds.length ? ' (T6)' : '')) : 'No application component', withDd.length < dds.length ? 'gd-warn' : '')] }; });
    return { gds: [self.grid(PF[chain].title + ' · ' + TAG_NAME[tag], [{ label: 'Requirement', sub: 'need' }, { label: 'Architecture building blocks', sub: 'what' }, { label: 'Solution building blocks', sub: 'with what · ' + TAG_NAME[tag] }, { label: 'Detailed design', sub: 'how (text)' }], rows, '')], hasGds: true };
  }
  track(e) { if (!e || !e.chain || ['abb', 'sbb'].indexOf(e.level) < 0) return []; return land(e.chain).plateaus.map(p => ({ s: TAG_SHORT[p.tag] || p.tag, on: (e.plateaus || []).indexOf(p.tag) >= 0, cls: (e.plateaus || []).indexOf(p.tag) >= 0 ? 'on' : '', title: p.title })); }
  v_factsheet() {
    const self = this, a = this.state.app, A = APPS[a], comp = A.components[0], e = EL[comp];
    const caps = (D.realizes[comp] || []).map(c => ({ title: EL[c].title, go: self.go(c), layer: 'strategy', kind: 'capability' }));
    const data = D.data.filter(d => d.component === comp).map(d => ({ title: EL[d.id].title, bo: title(d.bo), mode: chip({ master: ['success', 'M', 'Master'], copy: ['neutral', 'C', 'Copy'] }, d.mode), go: self.go(d.id) }));
    const outs = D.flows.filter(f => COMP2APP[f.source] === a).map(f => ({ what: f.title, other: APPS[COMP2APP[f.target]].title, go: self.openApp(COMP2APP[f.target]), dir: '→' }));
    const ins = D.flows.filter(f => COMP2APP[f.target] === a).map(f => ({ what: f.title, other: APPS[COMP2APP[f.source]].title, go: self.openApp(COMP2APP[f.source]), dir: '←' }));
    const tech = D.technology.filter(t => t.usedBy.indexOf(comp) >= 0).map(t => ({ title: EL[t.id].title, life: chip(LIFE, t.lifecycle), go: self.go(t.id) }));
    const wps = D.roadmap.workPackages.filter(w => A.components.some(c => w.scope.new.indexOf(c) >= 0 || w.scope.changed.indexOf(c) >= 0 || w.scope.retired.indexOf(c) >= 0)).map(w => ({ title: w.title, klass: w.class, status: chip(STATUS, w.status), go: self.go(w.id), what: w.scope.new.indexOf(comp) >= 0 ? 'new' : w.scope.retired.indexOf(comp) >= 0 ? 'retired' : 'changed' }));
    const adrs = D.elements.filter(x => x.level === 'adr' && (x.affects || []).some(c => A.components.indexOf(c) >= 0)).map(x => ({ title: x.title, go: self.go(x.id) }));
    const ifaces = D.elements.filter(x => x.kind === 'application-interface' && A.components.indexOf(x.id) < 0 && x.application === a).map(x => ({ title: x.title, contract: x.contract || 'no contract file', hasContract: !!x.contract, go: self.go(x.id) }));
    const health = self.healthOf(a);
    return { fs: { title: A.title, id: a, health, hasHealth: !!health, pf: PF[A.portfolio].title, goPf: self.openView('portfolio', 'landscape', { pf: A.portfolio }), time: chip(TIME, A.time), crit: A.criticality, owner: A.owner, sourcing: A.sourcing, hosting: A.hosting, track: self.track(e), status: chip(STATUS, e.status), change: e.change ? chip(CHANGE, e.change) : nochip, hasChange: !!e.change, goComp: self.go(comp),
      caps, data, flows: outs.concat(ins), tech, wps, adrs, ifaces, nCaps: caps.length, nData: data.length, nFlows: outs.length + ins.length, nTech: tech.length, nWps: wps.length, nAdrs: adrs.length, nIfaces: ifaces.length } };
  }
  v_inside(tag) {
    const self = this, a = this.state.app, A = APPS[a], c = A.components[0];
    const own = D.elements.filter(e => e.scopeType === 'application' && e.application === a);
    const byKind = k => own.filter(e => e.kind === k).map(e => self.fig(e.id, { rel: e.kind === 'data-object' ? (relIn(e.id).filter(r => r.k === 'access').map(r => r.l).join(', ')) : e.kind === 'application-interface' ? 'exposed by the component' : '', hasRel: e.kind !== 'application-component' }));
    const ins = D.flows.filter(f => f.target === c && inP(EL[f.source], tag)).map(f => self.fig(f.source, { rel: '← ' + f.title, hasRel: true, cls: 'ax-muted' }));
    const outs = D.flows.filter(f => f.source === c && inP(EL[f.target], tag)).map(f => self.fig(f.target, { rel: '→ ' + f.title, hasRel: true, cls: 'ax-muted' }));
    const tech = relIn(c).filter(r => r.k === 'serving' && EL[r.s].scopeType === 'enterprise').map(r => self.fig(r.s, { rel: 'serves', hasRel: true, cls: 'ax-muted' }));
    const row = { cells: [self.gcell(ins, ins.length ? '' : 'nothing in ' + TAG_NAME[tag]), self.gcell(byKind('application-component')), self.gcell(byKind('application-interface').concat(byKind('application-service')), own.some(e => e.kind === 'application-interface') ? '' : 'no interface'), self.gcell(byKind('data-object'), own.some(e => e.kind === 'data-object') ? '' : 'no data object'), self.gcell(outs, outs.length ? '' : 'nothing in ' + TAG_NAME[tag]), self.gcell(tech, tech.length ? '' : 'no platform')] };
    const RN = { flow: 'Flow', serving: 'Serving', access: 'Access', composition: 'Composition', realization: 'Realization', aggregation: 'Aggregation', association: 'Association' };
    const ids = own.map(e => e.id);
    const relRows = D.relations.filter(r => (ids.indexOf(r.s) >= 0 || ids.indexOf(r.t) >= 0) && !(r.k === 'aggregation' && EL[r.s].kind === 'plateau')).map(r => ({ kind: RN[r.k] || r.k, from: title(r.s), to: title(r.t), label: r.l || '', goFrom: self.go(r.s), goTo: self.go(r.t), ext: !!r.ext }));
    return { gds: [self.grid(A.title + ' · ' + TAG_NAME[tag], [{ label: 'Receives from', sub: 'flows in' }, { label: 'Component', sub: 'the application' }, { label: 'Interfaces · services', sub: 'contracts' }, { label: 'Data objects', sub: 'master or copy' }, { label: 'Sends to', sub: 'flows out' }, { label: 'Platforms', sub: 'serving technology' }], [row], '')], hasGds: true, relRows, hasRelRows: !!relRows.length, relN: relRows.length + ' relationships' };
  }
  v_interfaces() {
    const self = this, a = this.state.app, A = APPS[a];
    const ifaces = D.elements.filter(x => x.kind === 'application-interface' && x.application === a).map(x => ({ title: x.title, contract: x.contract || '—', hasContract: !!x.contract, status: chip(STATUS, x.status), ok: chip({ y: ['success', '✓', 'Contract file'], n: ['warning', '!', 'No contract file'] }, x.contract ? 'y' : 'n'), realizes: relOut(x.id).filter(r => r.k === 'realization').map(r => title(r.t)).join(', ') || '—', track: self.track(x), go: self.go(x.id) }));
    const data = D.data.filter(d => COMP2APP[d.component] === a).map(d => ({ title: EL[d.id].title, bo: title(d.bo), goBo: self.go(d.bo), mode: chip({ master: ['success', 'M', 'Master'], copy: ['neutral', 'C', 'Copy'] }, d.mode), access: relOut(d.component).filter(r => r.k === 'access' && r.t === d.id).map(r => r.l).join(', ') || '—', track: self.track(EL[d.id]), go: self.go(d.id) }));
    return { ifRows: ifaces, dataRows: data, ifN: ifaces.length + ' interfaces · ' + data.length + ' data objects' };
  }

  // ---------- elements ----------
  catVals() {
    const s = this.state, self = this, q = s.q.trim().toLowerCase();
    const segs = [['applications', 'Applications'], ['tree', 'Tree'], ['elements', 'All elements']];
    const out = { catSegs: segs.map(c => ({ id: c[0], label: c[1], on: s.cat === c[0], cls: s.cat === c[0] ? 'seg-on' : '', pick: self.set({ cat: c[0] }) })), isCatApps: s.cat === 'applications', isCatTree: s.cat === 'tree', isCatEls: s.cat === 'elements', q: s.q, onQ: e => self.setState({ q: e.target.value }), clearQ: self.set({ q: '' }), hasQ: !!q };
    const match = e => !q || (e.title + ' ' + e.id + ' ' + kindName(e) + ' ' + (e.owner || '')).toLowerCase().indexOf(q) >= 0;
    // applications table
    out.appRows = APP_IDS.filter(a => !q || (APPS[a].title + ' ' + a + ' ' + APPS[a].owner).toLowerCase().indexOf(q) >= 0).map(a => { const e = EL[APPS[a].components[0]]; return { id: a, title: APPS[a].title, pf: PF[APPS[a].portfolio].title, time: chip(TIME, APPS[a].time), crit: APPS[a].criticality, owner: APPS[a].owner, hosting: APPS[a].hosting, track: self.track(e), change: e.change ? chip(CHANGE, e.change) : nochip, hasChange: !!e.change, go: self.openApp(a) }; });
    // tree
    const open = s.open; const isOpen = (id, dflt) => open[id] == null ? !!dflt : !!open[id];
    const tog = id => () => { const o = Object.assign({}, self.state.open); o[id] = !isOpen(id, false); self.setState({ open: o }); };
    const nodes = [];
    const leaf = (e, depth) => nodes.push({ id: e.id, isLeaf: true, depth, pad: 'padding-left: ' + (16 + depth * 22) + 'px', title: e.title, sub: kindName(e) + (e.scopeType === 'enterprise' && depth > 1 ? ' · shared' : ''), layer: layerOf(e), kind: e.kind, status: e.status ? chip(STATUS, e.status) : nochip, hasStatus: !!e.status, change: e.change ? chip(CHANGE, e.change) : nochip, hasChange: !!e.change, track: self.track(e), ext: !!e.ext, go: self.go(e.id) });
    const branch = (id, label, sub, depth, n, children, dflt, extra) => { const o = isOpen(id, dflt) || !!q; nodes.push(Object.assign({ id, isLeaf: false, isBranchClosed: !(isOpen(id, dflt) || !!q), depth, pad: 'padding-left: ' + (16 + depth * 22) + 'px', title: label, sub, n: String(n), open: o, chev: o ? '▾' : '▸', toggle: tog(id), cls: 'tn-' + depth, hasTile: false, layer: '', kind: '' }, extra || {})); if (o) children(); };
    const byLayer = (els, depth, prefix, dflt) => { const present = LAYER_ORDER.filter(l => els.some(e => layerOf(e) === l)); if (present.length === 1 && depth > 1) { els.filter(match).sort(byTitle).forEach(e => leaf(e, depth)); return; } LAYER_ORDER.forEach(l => { const xs = els.filter(e => layerOf(e) === l).filter(match).sort(byTitle); if (!xs.length) return; branch(prefix + '/' + l, D.layers[l], xs.length + ' elements', depth, xs.length, () => xs.forEach(e => leaf(e, depth + 1)), dflt); }); };
    const nonApp = D.elements.filter(e => e.level !== 'adr' && e.level !== 'dd');
    if (s.treeMode === 'portfolio') {
      const ent = nonApp.filter(e => e.scopeType === 'enterprise' || !e.scopeType);
      const entM = ent.filter(match).length;
      if (entM) branch('ent', D.enterprise.title + ' · shared', 'enterprise scope: capabilities, value streams, roles, business objects, standards, motivation', 0, entM, () => byLayer(ent, 1, 'ent', false), false, { hasTile: true, layer: 'strategy', kind: 'capability' });
      D.portfolios.forEach(p => {
        const pfEls = nonApp.filter(e => e.scopeType === 'portfolio' && e.portfolio === p.id);
        const appIds = p.applications; const total = pfEls.filter(match).length + appIds.reduce((n, a) => n + nonApp.filter(e => e.scopeType === 'application' && e.application === a).filter(match).length, 0);
        if (!total && q) return;
        branch('pf:' + p.id, p.title, appIds.length + ' applications · ' + p.owner, 0, total, () => {
          const pm = pfEls.filter(match);
          if (pm.length) branch('pfel:' + p.id, 'Portfolio building blocks', 'processes, services, requirements, changes, plateaus', 1, pm.length, () => byLayer(pfEls, 2, 'pfel:' + p.id, false), false);
          appIds.forEach(a => { const ae = nonApp.filter(e => e.scopeType === 'application' && e.application === a); const am = ae.filter(match).length; if (!am && q) return; const c = EL[APPS[a].components[0]]; branch('app:' + p.id + '/' + a, APPS[a].title, TIME[APPS[a].time][2] + ' · ' + APPS[a].owner + ' · ' + APPS[a].hosting, 1, am, () => byLayer(ae, 2, 'lay:' + p.id + '/' + a, true), false, { hasTile: true, layer: 'application', kind: 'application-component', change: c.change ? chip(CHANGE, c.change) : nochip, hasChange: !!c.change, track: self.track(c), goApp: self.openApp(a), hasGoApp: true }); });
        }, p.id === 'corporate');
      });
    } else {
      LAYER_ORDER.forEach(l => { const xs = D.elements.filter(e => layerOf(e) === l); const xm = xs.filter(match); if (!xm.length) return; branch('layer:' + l, D.layers[l], uniq(xs.map(e => e.kind)).length + ' types', 0, xm.length, () => { uniq(xs.map(e => e.kind)).sort().forEach(k => { const ks = xs.filter(e => e.kind === k).filter(match).sort(byTitle); if (!ks.length) return; branch('type:' + l + '/' + k, NOTE[k] ? NOTE[k].name : k, '', 1, ks.length, () => ks.forEach(e => leaf(e, 2)), false, { hasTile: true, layer: l, kind: k }); }); }, l === 'business'); });
    }
    out.aFlat = !!q; out.aTree = !q; out.aRows = q ? D.elements.filter(e => e.level !== 'dd' && e.level !== 'adr').filter(match).sort(byTitle).slice(0, 80).map(e => self.rowOf(e)) : []; out.aN = q ? D.elements.filter(e => e.level !== 'dd' && e.level !== 'adr').filter(match).length + ' elements match' : D.elements.filter(e => e.level !== 'dd' && e.level !== 'adr').length + ' elements';
    out.tree = nodes; out.treeModes = [['portfolio', 'By portfolio'], ['layer', 'By layer']].map(t => ({ id: t[0], label: t[1], on: s.treeMode === t[0], cls: s.treeMode === t[0] ? 'seg-on' : '', pick: self.set({ treeMode: t[0] }) }));
    out.treeN = nodes.filter(n => n.isLeaf).length + ' elements shown';
    out.expandAll = () => { const o = {}; nodes.forEach(n => { if (!n.isLeaf) o[n.id] = true; }); D.portfolios.forEach(p => { o['pf:' + p.id] = true; p.applications.forEach(a => { o['app:' + p.id + '/' + a] = true; LAYER_ORDER.forEach(l => { o['lay:' + p.id + '/' + a + '/' + l] = true; }); }); }); self.setState({ open: o }); };
    out.collapseAll = () => { const o = {}; nodes.forEach(n => { if (!n.isLeaf) o[n.id] = false; }); self.setState({ open: o }); };
    // all elements
    const levels = [['all', 'All']].concat(LEVEL_ORDER.map(l => [l, LEVEL_NAME[l]]));
    const scopes = [['all', 'All scopes'], ['enterprise', 'Enterprise'], ['portfolio', 'Portfolio'], ['application', 'Application']];
    const els = D.elements.filter(e => (s.catLevel === 'all' || e.level === s.catLevel) && (s.catScope === 'all' || (e.scopeType || 'application') === s.catScope) && match(e)).sort((a, b) => (LEVEL_ORDER.indexOf(a.level) - LEVEL_ORDER.indexOf(b.level)) || a.title.localeCompare(b.title));
    out.catLevels = levels.map(l => ({ id: l[0], label: l[1], n: l[0] === 'all' ? D.elements.length : D.elements.filter(e => e.level === l[0]).length, on: s.catLevel === l[0], cls: s.catLevel === l[0] ? 'chip-on' : '', pick: self.set({ catLevel: l[0] }) }));
    out.catScopes = scopes.map(l => ({ id: l[0], label: l[1], on: s.catScope === l[0] })); out.catScope = s.catScope; out.pickScope = e => self.setState({ catScope: e.target.value });
    out.elRows = els.slice(0, 160).map(e => self.rowOf(e));
    out.elN = els.length + ' elements' + (els.length > 160 ? ' · first 160 shown' : '');
    return out;
  }

  rowOf(e) { const self = this; return { id: e.id, title: e.title, kind: kindName(e), layer: layerOf(e), k: e.kind, level: LEVEL_NAME[e.level], scope: e.scopeType === 'enterprise' ? D.enterprise.title : e.scopeType === 'portfolio' ? (PF[e.portfolio] || {}).title || e.scope : (APPS[e.application] || {}).title || e.application || '—', owner: e.owner || '—', track: self.track(e), change: e.change ? chip(CHANGE, e.change) : nochip, hasChange: !!e.change, status: e.status ? chip(STATUS, e.status) : nochip, hasStatus: !!e.status, origin: e.ext ? 'prototype' : e._path && e._path.indexOf('changes/') >= 0 ? 'change file' : 'model', path: (e.scopeType === 'enterprise' ? D.enterprise.title + ' · shared' : e.scopeType === 'portfolio' ? (PF[e.portfolio] || {}).title : ((PF[(APPS[e.application] || {}).portfolio] || {}).title || '') + ' › ' + ((APPS[e.application] || {}).title || e.application || '')) + ' › ' + D.layers[layerOf(e)], go: self.go(e.id) }; }
  // ---------- element page ----------
  pageVals() {
    const s = this.state, self = this; if (!s.page || s.page.kind !== 'element') return { el: {} };
    const e = EL[s.page.id]; if (!e) return { el: {} };
    const RN = { realization: 'realizes', serving: 'serves', composition: 'is composed of', aggregation: 'aggregates', assignment: 'is assigned to', access: 'accesses', flow: 'flows to', triggering: 'triggers', influence: 'influences', association: 'is associated with' };
    const RNI = { realization: 'is realized by', serving: 'is served by', composition: 'is part of', aggregation: 'belongs to', assignment: 'has assigned', access: 'is accessed by', flow: 'receives from', triggering: 'is triggered by', influence: 'is influenced by', association: 'is associated with' };
    const rel = (r, dir) => { const o = dir === 'out' ? r.t : r.s; const oe = EL[o]; return { verb: (dir === 'out' ? RN : RNI)[r.k] || r.k, label: r.l ? ' · ' + r.l : '', other: title(o), layer: oe ? layerOf(oe) : 'other', kind: oe ? oe.kind : '', hasTile: !!oe, go: self.go(o), ext: !!r.ext }; };
    const outs = relOut(e.id).map(r => rel(r, 'out')), ins = relIn(e.id).map(r => rel(r, 'in'));
    const app = appOf(e);
    const wps = D.roadmap.workPackages.filter(w => w.scope.new.indexOf(e.id) >= 0 || w.scope.changed.indexOf(e.id) >= 0 || w.scope.retired.indexOf(e.id) >= 0).map(w => ({ title: w.title, go: self.go(w.id), what: w.scope.new.indexOf(e.id) >= 0 ? 'introduces' : w.scope.retired.indexOf(e.id) >= 0 ? 'retires' : 'changes', status: chip(STATUS, w.status), arb: (D.arbs.find(a => a.workItemId === w.workItemId) || {}) }));
    const views = [];
    if (e.kind === 'capability') { views.push({ label: 'Capability map', go: self.openView('enterprise', 'capmap') }); views.push({ label: 'Capability coverage', go: self.openView('enterprise', 'coverage') }); views.push({ label: 'Capabilities × value streams', go: self.openView('enterprise', 'capvs') }); }
    if (e.kind === 'value-stream') views.push({ label: 'Value streams', go: self.openView('enterprise', 'valuestreams') });
    if (e.kind === 'business-process' || e.kind === 'business-role') views.push({ label: 'Roles × processes', go: self.openView('enterprise', 'roles') });
    if (e.kind === 'business-process' && e.portfolio) views.push({ label: 'Processes × applications', go: self.openView('portfolio', 'procapp', { pf: e.portfolio }) });
    if (app) { views.push({ label: 'Fact sheet · ' + APPS[app].title, go: self.openApp(app) }); views.push({ label: 'Inside and neighbours', go: self.openView('application', 'inside', { app }) }); views.push({ label: 'Application landscape · ' + PF[APPS[app].portfolio].title, go: self.openView('portfolio', 'landscape', { pf: APPS[app].portfolio }) }); }
    if (e.kind === 'business-object' || e.kind === 'data-object') views.push({ label: 'Data ownership', go: self.openView('portfolio', 'data', e.portfolio ? { pf: e.portfolio } : {}) });
    if (['node', 'system-software', 'technology-service'].indexOf(e.kind) >= 0) { views.push({ label: 'Technology radar', go: self.openView('enterprise', 'tech') }); views.push({ label: 'Applications × technologies', go: self.openView('portfolio', 'apptech') }); }
    if (e.kind === 'requirement' && e.portfolio) views.push({ label: 'Requirement chain · ' + PF[e.portfolio].title, go: self.openView('portfolio', 'chain', { pf: e.portfolio }) });
    if (['driver', 'goal', 'outcome', 'principle', 'stakeholder', 'assessment'].indexOf(e.kind) >= 0) views.push({ label: 'Motivation', go: self.openView('enterprise', 'motivation') });
    if (e.kind === 'work-package' || e.kind === 'plateau') { views.push({ label: 'Roadmap · ' + (PF[e.portfolio] || {}).title, go: self.openView('portfolio', 'roadmap', { pf: e.portfolio }) }); views.push({ label: 'Gap', go: self.openView('portfolio', 'gap', { pf: e.portfolio }) }); }
    if (wps.length && e.chain) views.push({ label: 'Gap · ' + PF[e.chain].title, go: self.openView('portfolio', 'gap', { pf: e.chain }) });
    const arb = e.level === 'adr' ? D.arbs.find(a => (a.adr || []).indexOf(e.id) >= 0) : D.arbs.find(a => a.readiness.scope.some(x => x.id === e.id));
    const html = e.html || '';
    return { el: { id: e.id, title: e.title, kind: kindName(e), layer: layerOf(e), k: e.kind, level: LEVEL_NAME[e.level] || e.level, levelHint: { motivation: 'why', requirement: 'need', abb: 'what', sbb: 'with what', dd: 'how (text)', migration: 'when', adr: 'decision' }[e.level] || '',
      scope: e.scopeType === 'enterprise' ? 'Enterprise' : e.scopeType === 'portfolio' ? 'Portfolio · ' + ((PF[e.portfolio] || {}).title || '') : app ? 'Application · ' + APPS[app].title : (e.application || '—'),
      status: e.status ? chip(STATUS, e.status) : nochip, hasStatus: !!e.status, change: e.change ? chip(CHANGE, e.change) : nochip, hasChange: !!e.change, track: self.track(e), hasTrack: !!self.track(e).length,
      desc: e.description || '', hasDesc: !!e.description, owner: e.owner || '—', path: e._path || '—', module: e.module || '', hasModule: !!e.module, wi: e.workItemId || '', hasWi: !!e.workItemId, contract: e.contract || '', hasContract: !!e.contract,
      meta: Object.keys(e.meta || {}).map(k => ({ k, v: String(e.meta[k]) })), hasMeta: !!(e.meta && Object.keys(e.meta).length),
      outs, ins, hasOuts: !!outs.length, hasIns: !!ins.length, nRel: outs.length + ins.length,
      views, hasViews: !!views.length, wps, hasWps: !!wps.length,
      dd: (e.dd || []).map(d => ({ title: title(d), go: self.go(d), status: chip(STATUS, (EL[d] || {}).status) })), hasDd: !!(e.dd && e.dd.length),
      adrs: (e.adr || []).map(a => ({ title: title(a), go: self.go(a) })), hasAdrs: !!(e.adr && e.adr.length),
      realizes: (e.realizes || []).map(r => ({ title: title(r), go: self.go(r) })), hasRealizes: !!(e.realizes && e.realizes.length),
      affects: (e.affects || []).map(r => ({ title: title(r), go: self.go(r) })), hasAffects: !!(e.affects && e.affects.length),
      decision: e.decision || '', hasDecision: !!e.decision, domainRef: e.domainRef || '',
      acceptance: e.acceptance || [], hasAcceptance: !!(e.acceptance && e.acceptance.length), decTable: (e.decisionTable || []).map(r => ({ c: r.case, ok: r.outcome === 'OK', outcome: r.outcome, reason: r.reason || '' })), hasDecTable: !!(e.decisionTable && e.decisionTable.length),
      operational: Object.keys(e.operational || {}).map(k => ({ k, v: String(e.operational[k]) })), hasOperational: !!(e.operational && Object.keys(e.operational).length),
      html, htmlText: htmlText(html), hasHtml: !!html, isDd: e.level === 'dd', isAdr: e.level === 'adr', src: e.src || '', hasSrc: !!e.src, lang: e.level === 'adr' || e.level === 'dd' ? 'Markdown · frontmatter' : 'LikeC4',
      arb: arb ? { title: arb.board + ' · ' + arb.title, status: chip(ARB_STATUS, arb.status), go: self.go(arb.id) } : null, hasArb: !!arb,
      ext: !!e.ext, backLabel: s.pageFrom ? 'Back' : ({ views: 'Back to the views', elements: 'Back to the elements', process: 'Back to the process' })[s.area],
      dl: self.elementDelivery(e), rq: e.kind === 'requirement' ? self.requirementDelivery(e) : { has: false }, ctx: self.serviceContext(e),
      goApp: app ? self.openApp(app) : null, hasApp: !!app, appTitle: app ? APPS[app].title : '' } };
  }

  // ---------- process ----------
  stepStatus(w) {
    const arb = D.arbs.find(a => a.workItemId === w.workItemId);
    const errs = arb ? arb.readiness.counts.errors : 0;
    const decide = { st: 'done', note: 'Scope, class and reviewers set' };
    let design; if (errs) design = { st: 'blocked', note: errs + ' blocking errors' }; else if (arb) design = { st: 'done', note: '0 errors · coverage ' + this.coverage(arb).n + '/13' }; else if (w.status === 'draft') design = { st: 'progress', note: 'Model on the branch · checks on each push' }; else design = { st: 'done', note: '0 errors' };
    let review; if (w.class === 'simplification') review = { st: 'skip', note: 'CODEOWNERS approve the PR' }; else if (!arb) review = { st: 'none', note: 'Submit when the design is complete' }; else if (arb.status === 'approved' || arb.status === 'approved-with-conditions') review = { st: 'done', note: arb.board + ' · ' + arb.boardDate }; else if (arb.status === 'in-review') review = { st: arb.readiness.counts.changesRequested ? 'attention' : 'progress', note: arb.readiness.counts.changesRequested ? arb.reviewers.find(r => r.decision === 'changes-requested').role + ' requested changes' : 'Board on ' + arb.boardDate }; else review = { st: 'progress', note: 'Draft · readiness ' + READINESS[arb.readiness.readiness][2].toLowerCase() };
    let deliver; const approved = arb && (arb.status === 'approved' || arb.status === 'approved-with-conditions'); const openC = arb ? arb.conditions.filter(c => c.status === 'open').length : 0;
    if (approved && w.end < TODAY) deliver = { st: openC ? 'attention' : 'done', note: openC ? openC + ' conditions still open' : 'Plateau promoted' }; else if (approved) deliver = { st: 'progress', note: 'Work items open' + (openC ? ' · ' + openC + ' condition' + (openC > 1 ? 's' : '') : '') }; else deliver = { st: 'none', note: arb && arb.conditions.length ? arb.conditions.length + ' condition' + (arb.conditions.length > 1 ? 's' : '') + ' to come' : 'After the review' };
    return [['Decide', decide], ['Design', design], ['Review', review], ['Deliver', deliver]].map(x => ({ label: x[0], chip: chip(STEP, x[1].st), note: x[1].note, cls: 'step-' + x[1].st }));
  }
  flowOf(w) {
    const st = this.stepStatus(w), arb = D.arbs.find(a => a.workItemId === w.workItemId);
    const ENTRY = { 'imp.corporate.credit-request-v1': 'new-need', 'imp.payments.sepa-instant-v1': 'new-need', 'imp.retail.digital-onboarding-v1': 'evolution', 'imp.risk.data-platform-v1': 'exploration', 'imp.corporate.facility-service-v1': 'decision', 'imp.retail.web-on-mobile-platform': 'evolution', 'imp.payments.iso20022-cross-border': 'decision', 'imp.risk.legacy-data-exit': 'evolution' };
    const entry = HOW.entries.find(e => e.id === (ENTRY[w.id] || w.entryId || (w.class === 'simplification' ? 'small-tweak' : w.class === 'incremental' ? 'evolution' : 'new-need')));
    const c = x => x.chip.cls;
    let cur, gatePending = null, gateState = 'pending';
    if (c(st[3]) === 'success') cur = 6;
    else if (c(st[2]) === 'success' || st[2].cls === 'step-skip') { cur = 5; if (c(st[3]) === 'warning') { gatePending = 'G4'; gateState = 'attention'; } }
    else if (arb) { cur = 2; gatePending = 'G2'; gateState = c(st[2]) === 'warning' ? 'attention' : c(st[2]) === 'error' ? 'blocked' : arb.readiness.readiness === 'blocked' ? 'blocked' : 'pending'; }
    else if (c(st[1]) === 'success') { cur = 4; gatePending = 'G3'; }
    else { cur = 2; }
    if (w.cur != null) { cur = w.cur; gatePending = null; }
    const first = Math.min(entry.phase, cur, 5);
    const phases = HOW.phases.map((ph, i) => { const state = i < first ? 'skipped' : i < cur ? 'done' : i === cur ? 'current' : 'todo'; return { n: ph.n, title: ph.title, sub: ph.sub, state, cls: 'ph-' + state, entered: i === first && first > 0, hasGate: !!ph.gate, noGate: !ph.gate, gate: ph.gate ? ph.gate.id : '', gateCls: ph.gate ? ('gt-' + (ph.gate.id === gatePending ? gateState : i < first ? 'skipped' : i < cur ? 'passed' : 'todo')) : '', gateTitle: ph.gate ? ph.gate.id + ' · ' + ph.gate.title + (ph.gate.id === gatePending ? ' · ' + gateState : i < cur ? ' · passed' : '') : '' }; });
    const now = cur === 6 ? 'Delivered · plateau promoted' : cur === 5 ? 'Implementation · ' + st[3].note : cur === 4 ? 'Plateau · waiting for G3 (ready to build)' : arb ? 'Target · at G2 · ' + st[2].note : 'Target · ' + st[1].note;
    return { entry, phases, cur, now: w.created ? (cur >= 6 ? 'After delivery' : HOW.phases[cur].title) + ' · opened from intake · ' + w.first + ' to draft' : now, delivered: cur === 6, gatePending, gateState };
  }
  coverage(a) {
    const self = this, written = {}; (a.sections || []).forEach(sc => { written[sc.title] = sc.html || ''; });
    const scopeSbb = a.readiness.scope.filter(x => x.change !== 'retired' && EL[x.id] && EL[x.id].kind === 'application-component');
    const withDd = scopeSbb.filter(x => (EL[x.id].dd || []).length);
    const items = coverageItems.map((t, i) => {
      let st, src, note = '';
      const w = written[t];
      if (['Requirements', 'Baseline', 'Target', 'Gap and transition', 'Detailed design', 'Decisions'].indexOf(t) >= 0) {
        src = 'model';
        if (t === 'Requirements') { st = a.requirements.length ? 'covered' : 'missing'; note = a.requirements.length + ' requirement' + (a.requirements.length > 1 ? 's' : '') + ' with acceptance rows'; }
        else if (t === 'Detailed design') { st = !scopeSbb.length ? 'covered' : withDd.length === scopeSbb.length ? 'covered' : withDd.length ? 'partly' : 'missing'; note = withDd.length + '/' + scopeSbb.length + ' application components have a DD'; }
        else if (t === 'Decisions') { st = (a.adr || []).length ? 'covered' : 'missing'; note = (a.adr || []).length + ' ADR'; }
        else { st = 'covered'; note = t === 'Gap and transition' ? a.readiness.scope.length + ' building blocks in scope' : 'generated from the plateau'; }
      } else { src = 'written'; st = w == null ? 'missing' : w.replace(/<[^>]+>/g, '').trim().length < 60 ? 'thin' : 'covered'; note = w == null ? 'section missing in the submission' : st === 'thin' ? 'one line: expand before the board' : ''; }
      if (t === 'Open questions') { const asks = (a.asks || []).length; note = (note ? note + ' · ' : '') + asks + ' ask' + (asks === 1 ? '' : 's') + ' to the board'; }
      return { i: i + 1, title: t, st, chip: chip({ covered: ['success', '✓', 'Covered'], partly: ['warning', '!', 'Partly'], thin: ['warning', '!', 'Thin'], missing: ['error', '✕', 'Missing'] }, st), src: src === 'model' ? 'From the model' : 'Written', srcCls: 'src-' + src, note, on: self.state.asdSec === i, cls: self.state.asdSec === i ? 'toc-on' : '', pick: self.set({ asdSec: i }), html: w || '', hasHtml: !!w };
    });
    return { items, n: items.filter(x => x.st === 'covered').length, partly: items.filter(x => x.st === 'partly' || x.st === 'thin').length, missing: items.filter(x => x.st === 'missing').length };
  }
  procVals() {
    const s = this.state, self = this;
    const items = [['intake', 'Intake', INTAKE.signals.filter(g => !((s.intake || {}).done || {})[g.id]).length + ' to qualify'], ['changes', 'Changes', D.roadmap.workPackages.length + ' in progress'], ['reviews', 'Reviews', D.arbs.length + ' ARB submissions'], ['decisions', 'Decisions', D.elements.filter(e => e.level === 'adr').length + ' ADRs'], ['checks', 'Model checks', D.validation.checks.length + ' checks'], ['how', 'How it works', 'flow, documents, roles, Git']];
    const out = { procList: items.map(i => ({ id: i[0], title: i[1], who: i[2], on: s.proc === i[0], cls: s.proc === i[0] ? 'sl-on' : '', pick: self.set({ proc: i[0] }) })) };
    ['intake', 'changes', 'reviews', 'decisions', 'checks', 'how'].forEach(k => { out['p_' + k] = s.proc === k; });
    Object.assign(out, self.intakeVals());
    // changes
    const pfF = [['all', 'All portfolios']].concat(D.portfolios.map(p => [p.id, p.title]));
    out.pfFilters = pfF.map(f => ({ id: f[0], label: f[1], on: s.pfFilter === f[0], cls: s.pfFilter === f[0] ? 'chip-on' : '', pick: self.set({ pfFilter: f[0] }) }));
    out.chFilters = [['all', 'All'], ['missing', 'Missing documents'], ['gate', 'Waiting for a gate']].map(f => ({ id: f[0], label: f[1], on: s.chFilter === f[0], cls: s.chFilter === f[0] ? 'chip-on' : '', pick: self.set({ chFilter: f[0] }) }));
    out.changes = D.roadmap.workPackages.filter(w => s.pfFilter === 'all' || w.chain === s.pfFilter).filter(w => { if (s.chFilter === 'all') return true; const sm = self.changeSummary(w.id); if (s.chFilter === 'missing') return sm.missing > 0; return sm.nValidated > 0; }).map(w => {
      const arb = D.arbs.find(a => a.workItemId === w.workItemId), e = EL[w.id], Lp = land(w.chain), to = Lp.plateaus.find(p => p.id === w.plateau), toI = Lp.plateaus.indexOf(to), from = Lp.plateaus[Math.max(0, toI - 1)];
      const touched = [].concat(w.scope.new, w.scope.changed, w.scope.retired);
      const overlaps = D.roadmap.workPackages.filter(o => o.id !== w.id && o.chain === w.chain && [].concat(o.scope.new, o.scope.changed, o.scope.retired).some(x => touched.indexOf(x) >= 0 || (EL[x] && COMP2APP[x] && touched.some(y => COMP2APP[y] === COMP2APP[x])))).map(o => ({ title: o.title, go: self.go(o.id), ordered: o.dependsOn.indexOf(w.id) >= 0 || w.dependsOn.indexOf(o.id) >= 0, note: (o.dependsOn.indexOf(w.id) >= 0 || w.dependsOn.indexOf(o.id) >= 0) ? '· order declared with dependsOn' : '· no order declared, C4 warns' }));
      const fl = self.flowOf(w), sm = self.changeSummary(w.id), dv = self.deliveryOf(w.id); const og = self.originOf(w.id) || { g: '', cls: '', name: '', ref: '' }; const gp = fl.gatePending ? ({ attention: ['warning', '!', fl.gatePending + ' · needs attention'], blocked: ['error', '✕', fl.gatePending + ' · blocked'], pending: ['info', '…', 'Waiting at ' + fl.gatePending] })[fl.gateState] : null; return { id: w.id, title: w.title, og, hasOg: !!og.name, isNew: !!w.created, rowCls: w.created ? 'trow-new' : '', phaseNow: fl.cur >= 6 ? 'Delivered' : HOW.phases[fl.cur].title, togaf: INTAKE.togaf[Math.min(fl.cur, 6)], gchip: gp ? { cls: gp[0], g: gp[1], w: gp[2] } : nochip, hasGchip: !!gp, deliveredState: fl.delivered ? 'done' : 'todo', docShort: sm.missing > 0 ? sm.missing + (sm.missing > 1 ? ' documents' : ' document') + ' to finish' : 'Documents ready', dlLine: dv && dv.line ? dv.line + (dv.last ? ' · last commit ' + dv.last.at : '') : '', hasDlLine: !!(dv && dv.line), docSummary: sm.nDone + ' published · ' + sm.nValidated + ' validated · ' + (sm.nWorking + sm.nDrafting) + ' in progress · ' + sm.nTodo + ' to do', docMissing: sm.missing, hasDocMissing: sm.missing > 0, openChange: self.openChange(w.id), wi: w.workItemId, pf: PF[w.chain].title, owner: w.owner, klass: w.class, klassCls: 'kl-' + w.class, from: from ? from.title : '', to: to ? to.title : '', dates: w.start + ' → ' + w.end, status: chip(STATUS, w.status), scope: `${w.scope.new.length} new · ${w.scope.changed.length} changed · ${w.scope.retired.length} retired`, steps: self.stepStatus(w), flow: fl.phases, entry: fl.entry.name, entryWhat: fl.entry.enters, now: fl.now, delivered: fl.delivered, deliveredCls: fl.delivered ? 'ph-done' : 'ph-todo', arb: arb ? { title: arb.board, status: chip(ARB_STATUS, arb.status), ready: chip(READINESS, arb.readiness.readiness), go: self.go(arb.id), pr: arb.pr, branch: arb.branch } : null, hasArb: !!arb, dep: w.dependsOn.map(d => ({ title: title(d), go: self.go(d) })), hasDep: !!w.dependsOn.length, overlaps, hasOverlaps: !!overlaps.length, adr: (w.adr || []).map(a => ({ title: title(a), go: self.go(a) })), hasAdr: !!(w.adr && w.adr.length), go: self.go(w.id), branch: 'change/' + w.id.split('.').pop() };
    });
    out.changeGroups = D.portfolios.map(p => { const rows = out.changes.filter(c => c.pf === p.title); return { pf: p.title, rows, count: rows.length }; }).filter(g => g.count);
    out.noChanges = !out.changes.length;
    // reviews
    out.arbRows = D.arbs.map(a => ({ id: a.id, board: a.board, title: a.title, pf: PF[a.application].title, scope: ((EL[a.from] || {}).title || '').split(' · ')[0] + ' → ' + ((EL[a.to] || {}).title || '').split(' · ')[0], to: (EL[a.to] || {}).title, status: chip(ARB_STATUS, a.status), ready: chip(READINESS, a.readiness.readiness), date: a.boardDate, reviewers: a.reviewers.filter(r => r.decision === 'approved' || r.decision === 'approved-with-conditions').length + '/' + a.reviewers.filter(r => r.decision !== 'not-required').length, pending: a.reviewers.filter(r => r.decision === 'pending').length, cond: a.conditions.filter(c => c.status === 'open').length, cov: self.coverage(a).n + '/13', go: self.go(a.id), wi: a.workItemId, owner: a.submittedBy }));
    // decisions
    out.adrRows = D.elements.filter(e => e.level === 'adr').map(e => ({ id: e.id, title: e.title, pf: (PF[e.application] || {}).title || e.application, status: chip(STATUS, e.status), ref: e.domainRef || '', affects: (e.affects || []).length + ' building blocks', updated: e.updatedAt || '', decision: e.decision, go: self.go(e.id) }));
    // checks
    const groups = uniq(D.validation.checks.map(c => c.group));
    out.checkGroups = groups.map(g => ({ label: g, checks: D.validation.checks.filter(c => c.group === g).map(c => ({ id: c.id, title: c.title, sev: c.severity === 'error' ? 'Blocks the merge' : 'Warning to the board', chip: chip(CHECK, c.status), items: c.items.map(it => ({ title: title(it.id), msg: it.message, go: self.go(it.id) })), hasItems: !!c.items.length, n: c.items.length ? c.items.length + ' item' + (c.items.length > 1 ? 's' : '') : '' })) }));
    out.checkSummary = `${D.validation.checks.filter(c => c.status === 'pass').length} passed · ${D.validation.checks.filter(c => c.status === 'warn').length} warnings · ${D.validation.checks.filter(c => c.status === 'fail').length} failed · run on main @ 4a1b9e0, today 08:41`;
    // how it works
    out.howTabs = [['steps', 'The flow'], ['documents', 'Documents and gates'], ['roles', 'Who does what'], ['classes', 'Three classes'], ['parallel', 'Parallel changes'], ['git', 'Git conventions'], ['agents', 'Coding assistants']].map(t => ({ id: t[0], label: t[1], on: s.howTab === t[0], cls: s.howTab === t[0] ? 'tab-on' : '', pick: self.set({ howTab: t[0] }) }));
    ['steps', 'documents', 'classes', 'roles', 'parallel', 'git', 'agents'].forEach(k => { out['how_' + k] = s.howTab === k; });
    Object.assign(out, self.howDocsVals(), self.howAgentsVals());
    out.howPhases = HOW.phases.map((ph, i) => ({ i: String(i), n: ph.n, title: ph.title, sub: ph.sub, togaf: ph.togaf, hasGate: !!ph.gate, noGate: !ph.gate, gate: ph.gate ? ph.gate.id : '', gateTitle: ph.gate ? ph.gate.title : '', on: s.howStep === i, cls: s.howStep === i ? 'ph-current' : 'ph-todo', pick: self.set({ howStep: i }) }));
    const hp = HOW.phases[Math.min(s.howStep, 5)]; out.howPhase = Object.assign({}, hp, { hasGate: !!hp.gate, noGate: !hp.gate, gate: hp.gate || { id: '', title: '', criteria: [], by: '' } }); out.howIntro = HOW.intro; out.howAfter = HOW.after; out.howEntries = HOW.entries; out.howSides = HOW.sides; out.howClasses = HOW.classes; out.howRoles = HOW.roles; out.howOutcomes = HOW.outcomes; out.howParallel = HOW.parallel; out.howAnswers = HOW.answers; out.howGit = HOW.git; out.howGuards = HOW.guards; out.howLanes = HOW.lanes;
    return out;
  }

  // ---------- change and documentation process (DEC-KB-38..42) ----------
  docKey(wid, did) { return wid + '|' + did; }
  docOf(wid, did) {
    const base = (CDOC.docs[wid] || []).find(x => x.id === did); if (!base) return null;
    const ov = (this.state.docs || {})[this.docKey(wid, did)] || {};
    const tpl = CDOC.templates[base.type], th = CDOC.threads[this.docKey(wid, did)] || [];
    // sections inserted: from the thread (inserted proposals) plus the person's insertions in this session
    const inserted = {}; let static0 = 0; th.forEach((t, ti) => (t.proposals || []).forEach((p, pi) => { if (p.inserted) static0++; if (p.inserted || (ov.ins || {})[ti + ':' + pi]) inserted[p.section] = p.text; }));
    const full = ov.state === 'validated' || base.state === 'published' || base.state === 'reviewed' || base.state === 'validated';
    // sections consolidated before this session: the first K sections that no proposal filled
    const K = full ? tpl.length : Math.max(0, (base.done || 0) - static0);
    const pre = {}; let k = 0; tpl.forEach(sct => { if (!inserted[sct] && k < K) { pre[sct] = true; k++; } });
    const done = Object.keys(inserted).length + Object.keys(pre).length;
    const state = ov.state || base.state;
    return Object.assign({}, base, ov, { state, done, total: tpl.length, tpl, inserted, pre, thread: th, hist: (ov.hist || []) });
  }
  openChange(wid) { return () => { this.setState({ page: { kind: 'change', id: wid }, pageFrom: this.state.page && this.state.page.kind !== 'change' ? this.state.page : null }); if (typeof window !== 'undefined') window.scrollTo(0, 0); }; }
  openDoc(wid, did) { return () => { this.setState({ page: { kind: 'doc', id: wid, doc: did }, pageFrom: { kind: 'change', id: wid }, threadDraft: '' }); if (typeof window !== 'undefined') window.scrollTo(0, 0); }; }
  docPatch(wid, did, fn) { const k = this.docKey(wid, did), cur = (this.state.docs || {})[k] || {}; return Object.assign({}, this.state.docs || {}, { [k]: fn(cur) }); }
  insertProposal(wid, did, ti, pi, replace) {
    const self = this; return () => {
      const th = CDOC.threads[self.docKey(wid, did)] || [], p = th[ti].proposals[pi];
      self.setState({ docs: self.docPatch(wid, did, cur => Object.assign({}, cur, { state: cur.state === 'validated' ? cur.state : (cur.state || self.docOf(wid, did).state) === 'drafting' ? 'working' : (cur.state || undefined), ins: Object.assign({}, cur.ins || {}, { [ti + ':' + pi]: true }), hist: [{ when: 'now', who: ROLE_VIEW[self.state.role].name, what: (replace ? 'Replaced ' : 'Inserted into ') + p.section, from: 'thread' }].concat(cur.hist || []) })) });
      self.toast((replace ? 'Section replaced: ' : 'Inserted into ') + p.section);
    };
  }
  validateDoc(wid, did) {
    const self = this; return () => {
      const d = self.docOf(wid, did); if (!d || d.done < d.total) { self.toast(d ? (d.total - d.done) + ' sections are still empty' : 'No document'); return; }
      const pr = 200 + Object.keys(self.state.docs || {}).length + 14;
      self.setState({ docs: self.docPatch(wid, did, cur => Object.assign({}, cur, { state: 'validated', pr, by: ROLE_VIEW[self.state.role].name, at: 'today', hist: [{ when: 'now', who: ROLE_VIEW[self.state.role].name, what: 'Validated · pull request #' + pr + ' opened on ' + (d.repo === 'central' ? 'architecture-repository' : d.repo), from: 'page' }].concat(cur.hist || []) })) });
      self.toast('Validated · PR #' + pr + ' opened · waiting for ' + CDOC.typeGate[d.type]);
    };
  }
  rebaseDoc(wid, did) {
    const self = this; return () => {
      self.setState({ docs: self.docPatch(wid, did, cur => Object.assign({}, cur, { rebased: true, state: 'working', hist: [{ when: 'now', who: ROLE_VIEW[self.state.role].name, what: 'Rebased on main @ 4a1b9e0 · 2 sections merged, none diverged · PR #212 closed', from: 'page' }].concat(cur.hist || []) })) });
      self.toast('Rebased on main @ 4a1b9e0 · the document is back to Working, validate it again');
    };
  }
  askThread(wid, did) {
    const self = this; return e => {
      if (e && e.preventDefault) e.preventDefault();
      const q = (self.state.threadDraft || '').trim(); if (!q) return;
      const d = self.docOf(wid, did), named = d.tpl.find(sct => q.indexOf(sct) >= 0), empty = named || d.tpl.filter(sct => !d.inserted[sct] && !d.pre[sct])[0] || d.tpl[d.tpl.length - 1];
      const key = self.docKey(wid, did), th = CDOC.threads[key] || (CDOC.threads[key] = []);
      th.push({ who: 'user', name: ROLE_VIEW[self.state.role].name, at: 'now', text: q });
      th.push({ who: 'agent', at: 'now', text: 'Proposal for “' + empty + '”, from the model and the published documents of this change. Insert it if it fits; tell me what to change otherwise.', sources: ['model · main @ 4a1b9e0', d.repo === 'central' ? 'architecture-repository' : d.repo + ' · working documents'], proposals: [{ section: empty, inserted: false, text: 'Draft for ' + empty.toLowerCase() + ' of ' + d.title + ': ' + q + ' — written from the target model, the baseline and the decisions attached to this change. Numbers and names come from the model; nothing here is invented beyond what you asked.' }] });
      self.setState({ threadDraft: '' });
    };
  }
  openAssistant(wid, did, section) {
    const self = this; return () => {
      const draft = section ? 'Draft the section “' + section + '”' : '';
      if (self.host) { const h = self.host; h.setState({ as: Object.assign({}, h.state.as || {}, { open: true, menu: false, docCtx: { wid, did }, intakeCtx: false, draft }), panel: false, menu: false, help: false }); if (typeof document !== 'undefined') setTimeout(() => { const el = document.getElementById('as-in'); if (el) el.focus(); }, 50); }
      else self.toast('In the product this opens the assistant pane with the thread of this document' + (section ? ' on “' + section + '”' : '') + ' — see the production vision');
    };
  }
  // the thread of a document as turns for the global assistant pane (vision)
  docTurns(wid, did) {
    const self = this, d = self.docOf(wid, did); if (!d) return null;
    const readOnly = d.state === 'validated' || d.state === 'reviewed' || d.state === 'published';
    const turns = []; let q = '';
    d.thread.forEach((t, ti) => {
      if (t.who === 'user') { q = t.text; return; }
      turns.push({ q, hasQ: !!q, answer: t.text, sources: (t.sources || []).map(x => ({ t: x })), hasSources: !!(t.sources || []).length,
        props: (t.proposals || []).map((p, pi) => { const ins = !!(p.inserted || ((((self.state.docs || {})[self.docKey(wid, did)] || {}).ins || {})[ti + ':' + pi])); return { section: p.section, text: p.text, inserted: ins, canInsert: !ins && !readOnly, insert: self.insertProposal(wid, did, ti, pi, false), replace: self.insertProposal(wid, did, ti, pi, true) }; }), hasProps: !!(t.proposals || []).length });
      q = '';
    });
    return { title: d.title, change: ((D.roadmap.workPackages.find(x => x.id === wid)) || {}).title || '', turns, readOnly, ask: q2 => { self.state.threadDraft = q2; self.askThread(wid, did)({}); if (typeof document !== 'undefined') setTimeout(() => { const b = document.querySelector('.as-body'); if (b) b.scrollTop = b.scrollHeight; }, 60); }, progress: d.done + '/' + d.total, openDoc: self.openDoc(wid, did) };
  }
  decideCollision(wid, idx, answer) {
    const self = this; return () => { self.setState({ collide: Object.assign({}, self.state.collide || {}, { [wid + ':' + idx]: { answer, by: ROLE_VIEW[self.state.role].name } }) }); self.toast('Answer recorded on both changes: ' + answer); };
  }
  decideProposal(pid, state) { const self = this; return () => { self.setState({ props: Object.assign({}, self.state.props || {}, { [pid]: state }) }); self.toast(state === 'accepted' ? 'Accepted · the pull request is approved for merge' : 'Rejected with your reason · the agent will not propose it again'); }; }
  docChip(state) {
    return chip({ todo: ['neutral', '○', 'To do'], drafting: ['info', '…', 'Drafting in chat'], working: ['warning', '✎', 'Working document'], validated: ['info', '↑', 'Validated · PR open'], reviewed: ['success', '✓', 'Reviewed'], published: ['success', '✓', 'Published'] }, state);
  }
  changeSummary(wid) {
    const self = this, docs = (CDOC.docs[wid] || []).map(x => self.docOf(wid, x.id));
    const n = st => docs.filter(x => x.state === st).length;
    return { docs, nTodo: n('todo'), nDrafting: n('drafting'), nWorking: n('working'), nValidated: n('validated'), nDone: n('reviewed') + n('published'), nTotal: docs.length, missing: docs.filter(x => x.state === 'todo' || x.state === 'drafting' || x.state === 'working').length };
  }
  changeVals() {
    const s = this.state, self = this; if (!s.page || s.page.kind !== 'change') return { ch: {} };
    const w = D.roadmap.workPackages.find(x => x.id === s.page.id); if (!w) return { ch: {} };
    const arb = D.arbs.find(a => a.workItemId === w.workItemId), fl = self.flowOf(w), sm = self.changeSummary(w.id);
    const phases = HOW.phases.map((ph, i) => ({ n: ph.n, title: ph.title, gate: ph.gate ? ph.gate.id : '', hasGate: !!ph.gate, state: fl.phases[i].state, cls: 'ph-' + fl.phases[i].state, docs: [] })).concat([{ n: '', title: 'After delivery', gate: 'G4', hasGate: false, state: fl.phases[5].state === 'done' ? 'current' : 'todo', cls: 'ph-todo', docs: [] }]);
    sm.docs.forEach(d => {
      const ph = phases[Math.min(CDOC.typePhase[d.type], 6)]; const raci = CDOC.typeRaci[d.type];
      const action = d.state === 'todo' ? 'Start' : d.state === 'drafting' || d.state === 'working' ? 'Continue' : d.state === 'validated' ? 'PR #' + d.pr : d.state === 'reviewed' ? 'PR #' + d.pr + ' merged' : '@ ' + d.sha;
      const sub = d.state === 'drafting' || d.state === 'working' ? d.done + '/' + d.total + ' sections' + (d.by ? ' · ' + d.by : '') + (d.at ? ' · ' + d.at : '') + (d.source === 'code' ? ' · from code, draft' : '') : d.state === 'todo' ? (CDOC.source[d.type] ? 'generated from the model' : '') : '';
      ph.docs.push({ id: d.id, title: d.title, state: d.state, chip: self.docChip(d.state), sub, hasSub: !!sub, action, open: self.openDoc(w.id, d.id) });
    });
    const next = fl.gatePending || (fl.cur <= 1 ? 'G1' : fl.cur <= 2 ? 'G2' : fl.cur <= 4 ? 'G3' : 'G4');
    const nextDocs = sm.docs.filter(d => CDOC.typeGate[d.type] === next);
    const cols = (CDOC.collisions[w.id] || []).map((c, i) => { const dec = (s.collide || {})[w.id + ':' + i]; const o = D.roadmap.workPackages.find(x => x.id === c['with']); return { level: { 'same-document': 'Same document', 'same-element': 'Same element', 'base-moved': 'Base moved' }[c.level], levelCls: 'col-' + c.level, detail: c.detail, other: o ? o.title : c['with'], goOther: self.openChange(c['with']), decided: !!(c.answer || dec), answer: dec ? dec.answer : (c.answer || ''), by: dec ? dec.by : (c.by || ''), at: dec ? 'now' : (c.at || ''), note: c.note || '', hasNote: !!c.note, isBase: c.level === 'base-moved', isElem: c.level !== 'base-moved',
      seq: self.decideCollision(w.id, i, 'Sequence'), merge: self.decideCollision(w.id, i, 'Merge'), split: self.decideCollision(w.id, i, 'Split'), rebase: self.rebaseDoc(w.id, c.doc), rebased: !!((s.docs || {})[self.docKey(w.id, c.doc)] || {}).rebased, notRebased: !((s.docs || {})[self.docKey(w.id, c.doc)] || {}).rebased, undecided: !(c.answer || dec) }; });
    const apps = uniq([].concat(w.scope.new, w.scope.changed, w.scope.retired).map(x => COMP2APP[x]).filter(Boolean));
    const health = apps.map(a => self.healthOf(a)).filter(Boolean);
    const og = self.originOf(w.id);
    return { ch: { og: og || {}, hasOg: !!og, id: w.id, title: w.title, wi: w.workItemId, pf: PF[w.chain].title, owner: w.owner, klass: w.class, klassCls: 'kl-' + w.class, status: chip(STATUS, w.status), entry: 'entered at ' + fl.entry.enters + ' as ' + fl.entry.name, now: fl.now,
      flow: fl.phases.map(p => Object.assign({}, p)), deliveredCls: fl.delivered ? 'ph-done' : 'ph-todo',
      phases: phases.filter(p => p.docs.length).map(p => Object.assign({}, p, { n: p.n === '' ? '' : String(p.n), gateLabel: p.hasGate ? p.gate + ' reviews this phase' : (p.title === 'After delivery' ? 'after G4' : ''), hasGateLabel: p.hasGate || p.title === 'After delivery' })),
      nTotal: sm.nTotal, nDone: sm.nDone, nValidated: sm.nValidated, nWorking: sm.nWorking, nDrafting: sm.nDrafting, nTodo: sm.nTodo,
      next, nextTitle: ({ G1: 'Scope agreed', G2: 'Target approved', G3: 'Ready to build', G4: 'Delivered' })[next], nextReady: nextDocs.filter(d => d.state === 'validated' || d.state === 'reviewed' || d.state === 'published').map(d => ({ title: d.title, chip: self.docChip(d.state), open: self.openDoc(w.id, d.id) })),
      nextMissing: nextDocs.filter(d => !(d.state === 'validated' || d.state === 'reviewed' || d.state === 'published')).map(d => ({ title: d.title, chip: self.docChip(d.state), open: self.openDoc(w.id, d.id) })), noNextMissing: !nextDocs.some(d => !(d.state === 'validated' || d.state === 'reviewed' || d.state === 'published')), hasNextMissing: nextDocs.some(d => !(d.state === 'validated' || d.state === 'reviewed' || d.state === 'published')),
      hasArb: !!arb, arb: arb ? { title: arb.board + ' · ' + arb.title, status: chip(ARB_STATUS, arb.status), ready: chip(READINESS, arb.readiness.readiness), go: self.go(arb.id) } : {},
      cols, hasCols: !!cols.length, health, hasHealth: !!health.length, dl: self.changeDelivery(w.id), goEl: self.go(w.id), backLabel: s.pageFrom ? 'Back' : 'Back to the changes', back: self.back() } };
  }
  healthOf(a) {
    const A = APPS[a]; if (!A) return null; const h = CDOC.health[a] || { codeAt: '—', ddAt: '—', origin: 'written', drifts: 0, owner: A.owner };
    const comps = D.elements.filter(e => e.kind === 'application-component' && e.application === a && e.status !== 'retired'), withDd = comps.filter(e => (e.dd || []).length);
    const ifaces = D.elements.filter(e => e.kind === 'application-interface' && e.application === a), withC = ifaces.filter(e => e.contract);
    const stale = h.ddAt !== h.codeAt && !/working|today/.test(h.ddAt) && h.codeAt !== h.ddAt;
    const cov = comps.length ? Math.round(100 * withDd.length / comps.length) : 100;
    return { app: a, title: A.title, go: this.openApp(a), coverage: withDd.length + '/' + comps.length + ' components with a DD', covChip: chip({ x: [cov === 100 ? 'success' : cov >= 50 ? 'warning' : 'error', cov === 100 ? '✓' : '!', cov + '%'] }, 'x'),
      contracts: withC.length + '/' + ifaces.length + ' interfaces with a contract', fresh: 'code ' + h.codeAt + ' · design ' + h.ddAt, freshChip: chip({ x: [stale ? 'warning' : 'success', stale ? '!' : '✓', stale ? 'Design older than the code' : 'Up to date'] }, 'x'),
      origin: h.origin, originChip: chip({ x: [/code/.test(h.origin) ? 'info' : 'neutral', /code/.test(h.origin) ? '⟲' : '✎', h.origin] }, 'x'), drifts: h.drifts ? h.drifts + (h.drifts > 1 ? ' open drifts' : ' open drift') : 'No drift', driftChip: chip({ x: [h.drifts ? 'warning' : 'success', h.drifts ? '!' : '✓', h.drifts ? String(h.drifts) : '0'] }, 'x'), owner: h.owner, ownerWarn: /to confirm/.test(h.owner) };
  }
  docVals() {
    const s = this.state, self = this; if (!s.page || s.page.kind !== 'doc') return { doc: {} };
    const wid = s.page.id, d = self.docOf(wid, s.page.doc); const w = D.roadmap.workPackages.find(x => x.id === wid); if (!d || !w) return { doc: {} };
    const raci = CDOC.typeRaci[d.type], gate = CDOC.typeGate[d.type];
    const readOnly = d.state === 'validated' || d.state === 'reviewed' || d.state === 'published';
    const sections = d.tpl.map((sct, i) => { const txt = d.inserted[sct]; const pre = !!d.pre[sct]; const st = txt ? 'inserted' : pre ? 'consolidated' : 'empty'; const changed = !!(d.baseMoved && !d.rebased && (sct === 'Baseline' || sct === 'Gap and transition'));
      return { title: sct, n: i + 1, st, text: txt || (pre ? (CDOC.source[d.type] ? 'Generated from the model (main @ 4a1b9e0): ' + sct.toLowerCase() + ' of ' + w.title + '.' : sct + ' — consolidated by ' + (d.by || 'the owner') + ' on ' + (d.at || '—') + '.') : ''), hasText: !!(txt || pre), isEmpty: !(txt || pre), changed, cls: (changed ? 'sec-changed ' : '') + 'sec-' + st, edit: () => self.toast(readOnly ? 'Read-only until ' + gate + ' decides' : 'Editing ' + sct + ' (Markdown) — prototype'), draft: self.openAssistant(wid, d.id, sct) }; });
    const turns = d.thread.map((t, ti) => ({ isUser: t.who === 'user', isAgent: t.who === 'agent', name: t.who === 'user' ? t.name : 'Assistant', at: t.at, text: t.text, sources: (t.sources || []).map(x => ({ t: x })), hasSources: !!(t.sources || []).length,
      proposals: (t.proposals || []).map((p, pi) => { const ins = !!(p.inserted || ((((s.docs || {})[self.docKey(wid, d.id)] || {}).ins || {})[ti + ':' + pi])); return { section: p.section, text: p.text, inserted: ins, canInsert: !ins && !readOnly, insert: self.insertProposal(wid, d.id, ti, pi, false), replace: self.insertProposal(wid, d.id, ti, pi, true), insChip: chip({ x: ['success', '✓', 'Inserted'] }, 'x') }; }), hasProposals: !!(t.proposals || []).length }));
    const hist = d.hist.concat(Object.keys(d.inserted).map(k => ({ when: d.at || '—', who: d.by || '—', what: 'Inserted into ' + k, from: 'thread' })));
    const col = (CDOC.collisions[wid] || []).find(c => c.doc === d.id && c.level === 'base-moved');
    return { doc: { id: d.id, title: d.title, change: w.title, wi: w.workItemId, goChange: self.openChange(wid), typeTitle: CDOC.typeTitle[d.type], state: d.state, chip: self.docChip(d.state), gate, repo: d.repo === 'central' ? 'architecture-repository' : d.repo,
      base: d.sha ? 'Published @ ' + d.sha : d.base ? 'Based on main @ ' + d.base : 'No published version yet · first version of this document', hasPr: !!d.pr, pr: d.pr || '', progress: d.done + '/' + d.total, pct: Math.round(100 * d.done / d.total) + '%',
      dialog: raci[0], validates: raci[1], reviews: raci[2], readOnly, canValidate: !readOnly, complete: d.done >= d.total, validate: self.validateDoc(wid, d.id),
      baseMoved: !!(d.baseMoved && !d.rebased), baseNote: col ? col.detail : '', rebase: self.rebaseDoc(wid, d.id), rebased: !!d.rebased,
      sections, turns, openAssistant: self.openAssistant(wid, d.id, null),
      hist, hasHist: !!hist.length, isCode: d.source === 'code', isModel: !!CDOC.source[d.type], srcLabel: CDOC.source[d.type] ? 'From the model' : d.source === 'code' ? 'From code · draft' : 'Written',
      statusLine: d.state === 'validated' ? 'validated by ' + (d.by || 'the owner') + ' · PR #' + d.pr + ' · waiting for ' + gate : d.state === 'published' ? 'published @ ' + d.sha + ' · reviewed at ' + gate : d.state === 'reviewed' ? 'reviewed at ' + (d.gateDone || gate) + ' · PR #' + d.pr + ' merged' : 'validated by ' + raci[1] + ' · reviewed at ' + gate } };
  }
  proposalVals() {
    const s = this.state, self = this;
    const rows = CDOC.proposals.map(p => { const st = (s.props || {})[p.id] || p.state; const w = p.change ? D.roadmap.workPackages.find(x => x.id === p.change) : null; return { id: p.id, kind: p.kind, kindCls: 'pk-' + p.kind.toLowerCase().replace(/[^a-z]+/g, '-'), title: p.title, app: APPS[p.app] ? APPS[p.app].title : p.app, goApp: APPS[p.app] ? self.openApp(p.app) : null, hasApp: !!APPS[p.app], change: w ? w.title : '', hasChange: !!w, goChange: w ? self.openChange(w.id) : null, opened: p.opened, pr: p.pr ? '#' + p.pr + ' on ' + (p.repo === 'central' ? 'architecture-repository' : p.repo) : 'working document', who: p.who, detail: p.detail, state: st, chip: chip({ open: ['warning', '!', 'Waiting for you'], accepted: ['success', '✓', 'Accepted'], rejected: ['neutral', '✕', 'Rejected'] }, st), isOpen: st === 'open', accept: self.decideProposal(p.id, 'accepted'), reject: self.decideProposal(p.id, 'rejected') }; });
    return { proposals: rows, nOpenProposals: rows.filter(r => r.isOpen).length, propSummary: rows.filter(r => r.isOpen).length + ' waiting for a person · ' + rows.filter(r => r.state === 'accepted').length + ' accepted · ' + rows.filter(r => r.state === 'rejected').length + ' rejected · nightly reconciliation of 3 Nov, 02:10' };
  }
  howDocsVals() {
    const types = Object.keys(CDOC.typeTitle);
    return { howDocRows: types.map(t => ({ title: CDOC.typeTitle[t], phase: t === 'baseline' ? 'After G4' : HOW.phases[CDOC.typePhase[t]].n + ' · ' + HOW.phases[CDOC.typePhase[t]].title, gate: CDOC.typeGate[t], dialog: CDOC.typeRaci[t][0], validates: CDOC.typeRaci[t][1], reviews: CDOC.typeRaci[t][2], src: CDOC.source[t] ? 'From the model' : 'Written in the chat', sections: CDOC.templates[t].length + ' sections' })),
      howDocStates: [['To do', 'The template exists, nothing written.'], ['Drafting in chat', 'A thread is open; the agent proposes sections, the person inserts them.'], ['Working document', 'Sections consolidated on the page; several people, section by section; diff against the published version.'], ['Validated · PR open', 'One pull request per document and per change; read-only until the gate decides.'], ['Reviewed', 'The gate reviewed it; merged.'], ['Published', 'In Git at a sha; the starting point of the next change.']].map(x => ({ t: x[0], d: x[1] })) };
  }

  // ---------- delivery line (metamodel v4 · DEC-KB-43, DEC-KB-44) ----------
  // Tickets, commits and versions are observed (ticketing, Git, CI), never modelled; the requirement that justifies a
  // gap is reached through the realization chain, then through the ticket, then through the work package.
  ticketsOf(wid) { return DELIV.tickets[wid] || []; }
  allTickets() { const self = this; return [].concat.apply([], Object.keys(DELIV.tickets).map(w => self.ticketsOf(w).map(t => Object.assign({ wid: w }, t)))); }
  commitsOf(key) { return DELIV.commits.filter(x => x.ticket === key); }
  tchip(st) { return chip({ done: ['success', '✓', 'Done'], doing: ['info', '…', 'In progress'], todo: ['neutral', '○', 'To do'] }, st); }
  commitLine(cs) { if (!cs.length) return 'No commit yet'; const last = cs[cs.length - 1]; return cs.length + (cs.length > 1 ? ' commits' : ' commit') + ' · last ' + last.sha + ' · ' + last.at + (last.via === 'sweep' ? ' · Sweep' : ''); }
  ticketRow(tk) {
    const self = this, cs = self.commitsOf(tk.key), impl = tk.implements.filter(x => EL[x]), rep = (tk.replaces || []).filter(x => EL[x]);
    return { key: tk.key, title: tk.title, state: tk.state, chip: self.tchip(tk.state), implements: impl.map(x => ({ title: title(x), go: self.go(x) })), hasImpl: !!impl.length, replaces: rep.map(x => ({ title: title(x), go: self.go(x) })), hasReplaces: !!rep.length,
      commits: self.commitLine(cs), acceptance: tk.acceptance + ' acceptance criteria', note: tk.note || '', hasNote: !!tk.note, change: tk.wid ? title(tk.wid) : '', goChange: tk.wid ? self.openChange(tk.wid) : null, hasChange: !!tk.wid };
  }
  reqByChain(id, depth, seen) {
    depth = depth || 0; seen = seen || {}; if (depth > 4 || seen[id]) return null; seen[id] = true;
    const rs = relOut(id).filter(r => ['realization', 'composition', 'aggregation', 'assignment'].indexOf(r.k) >= 0);
    for (const r of rs) { if ((EL[r.t] || {}).kind === 'requirement') return r.t; }
    for (const r of rs) { const q = this.reqByChain(r.t, depth + 1, seen); if (q) return q; }
    return null;
  }
  reqOfWp(wid) { const w = D.roadmap.workPackages.find(x => x.id === wid); if (!w) return null; const tk = this.ticketsOf(wid).find(t => t.requirement); if (tk) return tk.requirement; for (const x of [].concat(w.scope.new, w.scope.changed)) { const q = this.reqByChain(x); if (q) return q; } return null; }
  reqOfItem(id, wids) { const q = this.reqByChain(id); if (q) return q; const tk = this.allTickets().find(t => t.implements.indexOf(id) >= 0 || (t.replaces || []).indexOf(id) >= 0); if (tk && tk.requirement) return tk.requirement; for (const w of (wids || [])) { const r = this.reqOfWp(w); if (r) return r; } return null; }
  ticketsForEl(id) { return this.allTickets().filter(t => t.implements.indexOf(id) >= 0); }
  ticketsReplacing(id) { return this.allTickets().filter(t => (t.replaces || []).indexOf(id) >= 0); }
  deliveryOf(wid) {
    const self = this, w = D.roadmap.workPackages.find(x => x.id === wid); if (!w) return null;
    const tks = self.ticketsOf(wid), done = tks.filter(t => t.state === 'done').length, doing = tks.filter(t => t.state === 'doing').length;
    const cs = [].concat.apply([], tks.map(t => self.commitsOf(t.key))), vs = DELIV.versions.filter(v => v.change === wid);
    const req = self.reqOfWp(wid), fl = self.flowOf(w);
    return { w, tks, done, doing, total: tks.length, cs, vs, req, fl, line: tks.length ? done + '/' + tks.length + ' tickets done' + (doing ? ' · ' + doing + ' in progress' : '') : '', last: cs.length ? cs[cs.length - 1] : null };
  }
  gapCountsOf(w) { return `${w.scope.new.length} new · ${w.scope.changed.length} changed · ${w.scope.retired.length} retired`; }
  changeDelivery(wid) {
    const self = this, dl = self.deliveryOf(wid); if (!dl) return {};
    const w = dl.w, rel = dl.vs.filter(v => v.state === 'released'), pl = dl.vs.find(v => v.state === 'planned');
    const plateau = pl && pl.reaches ? title(pl.reaches).split(' · ')[0] : '';
    const version = rel.length ? rel[rel.length - 1].tag : pl ? pl.tag : 'None yet';
    const versionSub = rel.length && pl ? 'next ' + pl.tag.split(' ').pop() + ' · ' + pl.at + (plateau ? ' → ' + plateau : '') : pl ? pl.at + (plateau ? ' → ' + plateau : '') : rel.length ? (rel[rel.length - 1].note || '') : 'after the first ticket';
    const g3 = dl.fl.phases[4] && dl.fl.phases[4].state === 'done';
    return { hasReq: !!dl.req, req: dl.req ? title(dl.req) : 'No requirement yet', goReq: dl.req ? self.go(dl.req) : null,
      gap: self.gapCountsOf(w), goGap: self.openView('portfolio', 'gap', { pf: w.chain }),
      tickets: dl.total ? dl.done + '/' + dl.total + ' done' : 'None yet', ticketsSub: dl.total ? (dl.doing ? dl.doing + ' in progress' : dl.done === dl.total ? 'all delivered' : 'none in progress') : (g3 ? 'to create' : 'after G3 · Ready to build'),
      commits: dl.cs.length ? String(dl.cs.length) : '0', commitsSub: dl.last ? 'last ' + dl.last.sha + ' · ' + dl.last.at : 'no commit yet',
      version, hasVersions: !!dl.vs.length, versionSub, first: dl.fl.cur >= 5, last: dl.fl.cur < 5,
      rows: dl.tks.map(t => self.ticketRow(t)), hasTickets: !!dl.total, noTickets: !dl.total, noTicketsNote: g3 ? 'No ticket yet · the work packages are ready, the tickets are created in the ticketing tool' : 'No ticket before G3 (Ready to build) · code written earlier is observed anyway, by its commits',
      line: dl.line, hasLine: !!dl.line, lineAt: dl.last ? 'last commit ' + dl.last.at : '' };
  }
  elementDelivery(e) {
    const self = this, tks = self.ticketsForEl(e.id), reps = self.ticketsReplacing(e.id), cs = DELIV.commits.filter(c => c.touches === e.id);
    const replacedBy = reps.map(t => { const n = t.implements.filter(x => EL[x] && EL[x].kind === e.kind)[0] || t.implements[0]; return { key: t.key, title: t.title, chip: self.tchip(t.state), by: n ? title(n) : '', hasBy: !!n, goBy: n ? self.go(n) : null, goChange: self.openChange(t.wid) }; });
    return { rows: tks.map(t => self.ticketRow(t)), hasRows: !!tks.length, commits: self.commitLine(cs), hasCommits: !!cs.length, replacedBy, hasReplacedBy: !!replacedBy.length, has: !!(tks.length || reps.length || cs.length) };
  }
  requirementDelivery(e) {
    const self = this, tks = self.allTickets().filter(t => t.requirement === e.id), done = tks.filter(t => t.state === 'done').length;
    const wids = uniq(tks.map(t => t.wid)); const wps = D.roadmap.workPackages.filter(w => wids.indexOf(w.id) >= 0 || [].concat(w.scope.new, w.scope.changed).some(x => self.reqByChain(x) === e.id));
    const gaps = wps.map(w => ({ title: title(w.id), sub: self.gapCountsOf(w), go: self.openChange(w.id), status: chip(STATUS, w.status) }));
    return { has: !!(tks.length || wps.length), gaps, hasGaps: !!gaps.length, rows: tks.map(t => self.ticketRow(t)), hasRows: !!tks.length, progress: tks.length ? done + '/' + tks.length + ' tickets done' : 'No ticket yet', goGap: e.portfolio ? self.openView('portfolio', 'gap', { pf: e.portfolio }) : null, hasGoGap: !!e.portfolio };
  }
  serviceContext(e) {
    const self = this; if (e.kind !== 'application-service') return { has: false };
    const ifaces = relIn(e.id).filter(r => r.k === 'realization' && (EL[r.s] || {}).kind === 'application-interface').map(r => EL[r.s]);
    const apps = uniq(ifaces.map(i => i.application).filter(Boolean)), comps = apps.map(a => APPS[a] && APPS[a].components[0]).filter(Boolean);
    const data = D.data.filter(d => comps.indexOf(d.component) >= 0);
    const row = (id, verb) => ({ verb, title: title(id), kind: kindName(EL[id]), layer: layerOf(EL[id]), k: EL[id].kind, go: self.go(id), sub: EL[id].contract || (EL[id].description || '').slice(0, 80) });
    const chain = [{ verb: 'What to do', title: e.title, kind: kindName(e), layer: layerOf(e), k: e.kind, go: self.go(e.id), sub: (e.description || '').slice(0, 80) }]
      .concat(ifaces.map(i => row(i.id, 'Under which contract'))).concat(data.map(d => row(d.id, 'On which data'))).concat(comps.map(c => row(c, 'Where')));
    const kinds = uniq(chain.map(x => x.k)); const std = DELIV.standards.filter(s => s.applies.some(k => kinds.indexOf(k) >= 0));
    const req = self.reqByChain(e.id);
    return { has: true, chain, standards: std.map(x => x.id + ' · ' + x.title).join(' — '), hasStandards: !!std.length, req: req ? title(req) : '', hasReq: !!req, goReq: req ? self.go(req) : null, reqRows: req && EL[req].acceptance ? EL[req].acceptance.length + ' acceptance rows' : '' };
  }
  howAgentsVals() { return { howMcp: DELIV.mcp.server, howMcpTools: DELIV.mcp.tools.map(t => ({ name: t[0], arg: t[1], what: t[2] })), howMcpClients: DELIV.mcp.clients.map(c => ({ name: c[0], how: c[1] })) }; }
  // ---------- intake (qualification) · decision of 2026-11-10 ----------
  // Signals and explicit requests are qualified here before they become an architecture change; the conversation runs
  // in the global assistant pane (intakeTurns), the result is a change at its entry phase, an attachment or a dismissal.
  originOf(wid) { const w = D.roadmap.workPackages.find(x => x.id === wid) || {}, o = w.origin || INTAKE.changeOrigin[wid]; if (!o) return null; const k = INTAKE.origins[o[0]]; return { g: k.g, cls: 'og-' + o[0], name: k.name, ref: o[1], by: o[2], at: o[3] }; }
  qualOf(q) {
    const en = HOW.entries.find(e => e.id === q.entry), k = Math.min(en.phase, 6), light = q.entry === 'small-tweak' || q.entry === 'post-delivery';
    let ga = null; if (!light) for (let i = Math.min(k, 5); i < 6; i++) if (HOW.phases[i].gate) { ga = HOW.phases[i].gate; break; }
    return { k, entry: en.name, enters: k >= 6 ? 'After delivery' : HOW.phases[k].title, togaf: INTAKE.togaf[k], skips: k > 0 ? 'skips ' + HOW.phases.slice(0, Math.min(k, 6)).map(p => p.title).join(', ') : 'full cycle, every gate',
      docs: INTAKE.firstDocs[k].map(t => CDOC.typeTitle[t]).join(' · '), first: CDOC.typeTitle[INTAKE.firstDocs[k][0]], gate: ga ? ga.id + ' · ' + ga.title : 'No gate',
      gateBy: !ga ? (q.entry === 'small-tweak' ? 'CODEOWNERS approve the pull request' : 'The portfolio architect accepts the baseline update') : (ga.id === 'G2' && q.klass !== 're-architecting') ? 'Portfolio architect · no board for this class' : INTAKE.gateBy[ga.id] };
  }
  intakeCreate(q, n) {
    const id = 'imp.' + q.pf + '.intake-' + n, p = this.qualOf(q), tpl = D.roadmap.workPackages.find(w => w.chain === q.pf) || D.roadmap.workPackages[0];
    if (EL[id]) return id;
    const w = { id, title: q.title, status: 'draft', workItemId: 'WI-' + (1410 + n), owner: ROLE_VIEW[this.state.role].name, chain: q.pf, class: q.klass, start: '2026-11-03', end: '2027-03-31', plateau: tpl.plateau, dependsOn: [], adr: [],
      scope: { new: [], changed: [], retired: [] }, entryId: q.entry, cur: p.k, created: true, origin: [q.kind, q.ref, q.by, q.at], first: p.first };
    D.roadmap.workPackages.push(w); const el = Object.assign({}, EL[tpl.id], { id, title: q.title, status: 'draft', description: q.text, src: '', dd: [] }); D.elements.push(el); EL[id] = el;
    CDOC.docs[id] = INTAKE.firstDocs[p.k].map(t => ({ id: t, type: t, title: CDOC.typeTitle[t], state: 'todo', done: 0, repo: 'central' }));
    return id;
  }
  intakeDoneRec(q, outcome, change) { return { kind: q.kind, ref: q.ref, title: q.title, outcome, change: change || null, by: ROLE_VIEW[this.state.role].name, at: 'today' }; }
  intakeResolve(g, outcome, how) {
    const self = this; return () => { const st = self.state.intake || {}; let n = st.n || 0, change = null;
      if (how === 'create') { n++; change = self.intakeCreate(g, n); } else if (how === 'attach') change = g.attach;
      self.setState({ intake: Object.assign({}, st, { n, done: Object.assign({}, st.done, { [g.id]: self.intakeDoneRec(g, outcome, change) }) }) });
      self.toast(how === 'create' ? 'Change opened · ' + g.title : how === 'attach' ? 'Attached to ' + title(change) : 'Dismissed'); };
  }
  intakeVals() {
    const s = this.state, self = this, st = s.intake || {}, done = st.done || {};
    const sv = g => { const o = INTAKE.origins[g.kind], p = self.qualOf(g), at = g.attach ? D.roadmap.workPackages.find(w => w.id === g.attach) : null;
      return { id: g.id, g: o.g, cls: 'og-' + g.kind, oName: o.name, ref: g.ref, by: g.by, at: g.at, title: g.title, text: g.text, suggestion: p.entry + ' · enters at ' + p.enters + ' (TOGAF ' + p.togaf + ') · ' + p.skips,
        hasOverlap: !!g.overlap, overlap: g.overlap, hasAttach: !!at, attachLabel: at ? 'Attach to ' + at.title : '', qualify: self.intakeOpen(g.id), create: self.intakeResolve(g, 'Change opened', 'create'), attach: self.intakeResolve(g, 'Attached', 'attach'), dismiss: self.intakeResolve(g, 'Dismissed · no architecture impact', 'dismiss') }; };
    const open = INTAKE.signals.filter(g => !done[g.id]).map(sv);
    const OUT = r => /^Change opened/.test(r.outcome) ? ['success', '✓'] : /^Attached/.test(r.outcome) ? ['info', '↳'] : ['neutral', '–'];
    const hist = Object.keys(done).map(k => done[k]).reverse().concat(INTAKE.qualified).map(r => { const o = INTAKE.origins[r.kind], c = OUT(r), w = r.change ? D.roadmap.workPackages.find(x => x.id === r.change) : null;
      return { g: o.g, cls: 'og-' + r.kind, oName: o.name, ref: r.ref, title: r.title, chip: { cls: c[0], g: c[1], w: r.outcome }, hasChange: !!w, change: w ? w.title : '', goChange: w ? self.openChange(w.id) : null, who: r.ref === r.by ? r.at : r.by + ' · ' + r.at }; });
    return { intakeOpen: open, hasIntakeOpen: !!open.length, noIntakeOpen: !open.length, intakeCount: open.length + ' to qualify', intakeHist: hist, intakeNew: self.intakeOpen(null) };
  }
  intakeOpen(sigId) {
    const self = this; return () => { const st = self.state.intake || {}, g = sigId ? INTAKE.signals.find(x => x.id === sigId) : null;
      if (!self.host) { self.toast('In the product this opens the assistant pane to qualify the request in conversation — see the production vision'); return; }
      const chat = g ? { key: g.id, q: Object.assign({}, g), stage: 'ask', log: [{ who: 'asst', text: INTAKE.origins[g.kind].name + ' · ' + g.ref + '\n' + g.text + '\n\n' + g.ask, replies: g.replies.map(r => r[0]) }] }
        : { key: 'free-' + Object.keys(st.done || {}).length, q: null, stage: 'describe', log: [{ who: 'asst', text: 'Tell me what happened, in your words. I ask what I need, then propose how it enters the process.', replies: INTAKE.examples }] };
      self.setState({ intake: Object.assign({}, st, { chat }) });
      const h = self.host; h.setState({ as: Object.assign({}, h.state.as || {}, { open: true, menu: false, docCtx: null, intakeCtx: true, draft: '' }), panel: false, menu: false, help: false });
      if (typeof document !== 'undefined') setTimeout(() => { const el = document.getElementById('as-in'); if (el) el.focus(); }, 50); };
  }
  intakeSay(text) {
    const self = this, st = self.state.intake || {}, chat = st.chat; if (!chat || !text) return;
    const log = chat.log.concat([{ who: 'user', text }]), low = text.toLowerCase(), me = ROLE_VIEW[self.state.role].name;
    let q = chat.q, stage = chat.stage, done = st.done || {}, n = st.n || 0;
    const INTRO = { ticket: 'This is a new need from a business request.', chat: 'This is a new need.', idea: 'This is an exploration: nothing is committed until G2.', radar: 'A standard moved: the existing architecture has to evolve.', adr: 'This comes from a decision. It does not go back to Vision.', pr: 'The code changed first.', finding: 'The code and the model differ: the baseline has to catch up.', incident: 'It was fixed in production first: the baseline has to catch up.' };
    const propose = (intro) => { const p = self.qualOf(q), at = q.attach ? title(q.attach) : '';
      const replies = ['Create the change'].concat(at ? ['Attach to ' + at] : []).concat([q.klass === 'incremental' ? 'Make it re-architecting' : 'Make it incremental']).concat(q.scope.indexOf(',') > 0 ? ['Narrow the scope to ' + q.scope.split(',')[0]] : []).concat(q.entry === 'new-need' || q.entry === 'evolution' ? ['It is only an exploration'] : []);
      log.push({ who: 'asst', text: intro, replies, card: { title: q.title, origin: INTAKE.origins[q.kind].name + ' · ' + q.ref, enters: p.enters + ' · TOGAF ' + p.togaf, skips: p.skips, kind: p.entry + ' · ' + q.klass, scope: PF[q.pf].title + ' · ' + q.scope, docs: p.docs, gate: p.gate + ' · ' + p.gateBy, hasOverlap: !!q.overlap, overlap: q.overlap } }); stage = 'proposed'; };
    if (stage === 'describe') {
      const m = INTAKE.match.find(x => low.indexOf(x[0]) >= 0), g = m ? INTAKE.signals.find(x => x.id === m[1]) : null;
      q = g ? Object.assign({}, g) : { id: chat.key, title: text.length > 64 ? text.slice(0, 61) + '…' : text, text, kind: 'chat', ref: me, by: me, at: 'today', entry: 'new-need', klass: 'incremental', pf: (s => (PF[s] ? s : 'corporate'))(self.state.pf), scope: 'to be named',
        ask: 'Is there a committed need with a measure, or is it still an idea to explore?', replies: [['Committed, with a measure', {}], ['Still exploring', { entry: 'exploration' }]], attach: null, overlap: '' };
      log.push({ who: 'asst', text: (g ? 'I recognise it: ' + INTAKE.origins[g.kind].name + ' · ' + g.ref + '.\n\n' : '') + q.ask, replies: q.replies.map(r => r[0]) }); stage = 'ask';
    } else if (stage === 'ask') {
      const r = q.replies.find(x => x[0].toLowerCase() === low), mod = r ? r[1] : {};
      if (mod.dismiss) { q = Object.assign({}, q, { _dismiss: mod.dismiss }); log.push({ who: 'asst', text: 'Then it is not an architecture change. I can record it as: ' + mod.dismiss + '.', replies: ['Record it', 'Open a change anyway'] }); stage = 'dismiss'; }
      else { q = Object.assign({}, q, mod); propose(INTRO[q.kind] + ' Here is how it would enter the process. Tell me what to change, or create it.'); }
    } else if (stage === 'dismiss') {
      if (/record|yes|ok/.test(low)) { done = Object.assign({}, done, { [q.id]: self.intakeDoneRec(q, 'Dismissed · ' + q._dismiss, null) }); log.push({ who: 'asst', text: 'Recorded in Intake: dismissed.' }); stage = 'done'; }
      else propose('All right. Here is how it would enter the process.');
    } else if (stage === 'proposed') {
      if (/^create|open the change|go ahead|^yes/.test(low)) { n++; const id = self.intakeCreate(q, n), p = self.qualOf(q); done = Object.assign({}, done, { [q.id]: self.intakeDoneRec(q, 'Change opened', id) });
        log.push({ who: 'asst', text: 'Change opened: ' + q.title + '.\nIt enters at ' + p.enters + '. The first document to draft is ' + p.first + '; I can start it with you from the change page.', link: id }); stage = 'done'; }
      else if (/^attach/.test(low) && q.attach) { done = Object.assign({}, done, { [q.id]: self.intakeDoneRec(q, 'Attached', q.attach) }); log.push({ who: 'asst', text: 'Attached to ' + title(q.attach) + '. Its owner sees it on the change.', link: q.attach }); stage = 'done'; }
      else if (/re-?arch/.test(low)) { q = Object.assign({}, q, { klass: 're-architecting' }); propose('Updated: re-architecting. The target goes to the Architecture Board at G2.'); }
      else if (/incremental/.test(low)) { q = Object.assign({}, q, { klass: 'incremental' }); propose('Updated: incremental. No board at G2, the portfolio architect decides.'); }
      else if (/simplif|small/.test(low)) { q = Object.assign({}, q, { klass: 'simplification', entry: 'small-tweak' }); propose('Updated: a small tweak. Definition of Ready only.'); }
      else if (/explor/.test(low)) { q = Object.assign({}, q, { entry: 'exploration' }); propose('Updated: an exploration. It starts at Target; G2 decides whether it becomes a change.'); }
      else if (/narrow|only /.test(low)) { const one = (low.match(/to ([a-z0-9-]+)\s*$/) || [])[1] || q.scope.split(',')[0]; q = Object.assign({}, q, { scope: one.trim() }); propose('Updated: the scope is ' + one.trim() + '.'); }
      else if (/add |scope/.test(low)) { const more = text.replace(/^.*?(add|scope)\s*(to the scope)?:?\s*/i, '').replace(/\s*to the scope\.?$/i, ''); q = Object.assign({}, q, { scope: q.scope === 'to be named' ? more : q.scope + ', ' + more }); propose('Updated: scope ' + q.scope + '.'); }
      else log.push({ who: 'asst', text: 'I kept the proposal. You can change the kind (new need, exploration, small tweak), the class or the scope, or create the change.', replies: ['Create the change'] });
    } else return;
    self.setState({ intake: Object.assign({}, st, { n, done, chat: Object.assign({}, chat, { q, stage, log }) }) });
    if (typeof document !== 'undefined') setTimeout(() => { const b = document.querySelector('.as-body'); if (b) b.scrollTop = b.scrollHeight; }, 60);
  }
  // the qualification conversation as turns for the global assistant pane (vision)
  intakeTurns() {
    const self = this, chat = (self.state.intake || {}).chat; if (!chat) return null;
    const turns = []; let q = '';
    chat.log.forEach((t, i) => { if (t.who === 'user') { q = t.text; return; } const last = i === chat.log.length - 1;
      turns.push({ q, hasQ: !!q, answer: t.text, hasQual: !!t.card, qual: t.card || {}, replies: last && t.replies ? t.replies.map(r => ({ t: r, pick: () => self.intakeSay(r) })) : [], hasReplies: !!(last && t.replies && t.replies.length), hasLink: !!t.link, linkLabel: t.link ? 'Open the change' : '', linkGo: t.link ? self.openChange(t.link) : null }); q = ''; });
    return { title: 'Intake · ' + (chat.q ? chat.q.title : 'new request'), ctx: 'Qualification', turns, ask: t => self.intakeSay(t) };
  }
  // ---------- ARB page ----------
  arbVals() {
    const s = this.state, self = this; if (!s.page || s.page.kind !== 'arb') return { arb: {} };
    const a = ARB[s.page.id]; const cov = this.coverage(a); const rec = s.decisions[a.id];
    const tabs = [['asd', 'Solution design (ASD)', cov.n + '/13'], ['checks', 'Checks', a.readiness.checks.filter(c => c.status !== 'pass').length ? a.readiness.checks.filter(c => c.status !== 'pass').length + ' open' : 'all green'], ['review', 'Reviewers & conditions', a.reviewers.filter(r => r.decision === 'pending').length + ' pending'], ['decision', 'Decision', rec ? 'recorded' : ARB_STATUS[a.status][2]]];
    const scope = a.readiness.scope.map(x => { const e = EL[x.id]; return { id: x.id, title: e.title, kind: kindName(e), layer: layerOf(e), k: e.kind, change: chip(CHANGE, x.change), level: LEVEL_NAME[e.level], track: self.track(e), by: title(D.roadmap.workPackages.find(w => w.workItemId === a.workItemId).id), dd: (e.dd || []).length ? chip(STATUS, EL[e.dd[0]].status, 'DD ' + STATUS[EL[e.dd[0]].status][2].toLowerCase()) : (e.kind === 'application-component' && x.change !== 'retired' ? chip({ x: ['warning', '!', 'No DD yet'] }, 'x') : nochip), hasDd: e.kind === 'application-component' && x.change !== 'retired', go: self.go(x.id) }; });
    const reqs = a.requirements.map(r => { const e = EL[r]; return { title: e.title, desc: e.description, acc: (e.acceptance || []).length + ' rows', ko: (e.decisionTable || []).filter(x => x.outcome === 'KO').length + ' KO rules', ops: Object.keys(e.operational || {}).map(k => k + ' ' + e.operational[k]).join(' · '), realizers: relIn(r).filter(x => x.k === 'realization').map(x => ({ title: title(x.s), go: self.go(x.s) })), go: self.go(r) }; });
    const landAt = tag => { const p = PF[a.application]; return uniq([].concat.apply([], p.applications.map(ap => D.realizes[APPS[ap].components[0]] || []))).map(c => ({ cap: EL[c].title, apps: p.applications.filter(ap => (D.realizes[APPS[ap].components[0]] || []).indexOf(c) >= 0 && inP(EL[APPS[ap].components[0]], tag)).map(ap => ({ title: APPS[ap].title, change: appChange(ap, tag) ? chip(CHANGE, appChange(ap, tag)) : nochip, hasChange: !!appChange(ap, tag), go: self.openApp(ap) })) })).filter(r => r.apps.length); };
    const fromTag = EL[a.from] ? a.from.split('.').pop() : 'baseline', toTag = a.to.split('.').pop();
    const dds = scope.filter(x => x.hasDd).map(x => { const e = EL[x.id]; const d = (e.dd || []).map(id => EL[id]); return { title: x.title, go: x.go, dd: d.map(y => ({ title: y.title, status: chip(STATUS, y.status), contract: y.contract || '—', go: self.go(y.id) })), hasDdFiles: !!d.length, noDd: !d.length, iface: D.elements.filter(y => y.kind === 'application-interface' && y.application === e.application).map(y => ({ title: y.title, contract: y.contract || 'no contract file', ok: !!y.contract, dotStyle: 'background: ' + (y.contract ? '#1B5F1F' : '#6A4E00') })) }; });
    const sections = cov.items.map(it => Object.assign({}, it, { text: htmlText(it.html), isMissingWritten: it.src === 'Written' && it.st === 'missing', isWritten: it.src === 'Written', isReq: it.title === 'Requirements', isBase: it.title === 'Baseline', isTarget: it.title === 'Target', isGap: it.title === 'Gap and transition', isDd: it.title === 'Detailed design', isDec: it.title === 'Decisions', isOpen: it.title === 'Open questions' }));
    const roleCan = { owner: 'submit', reviewer: 'review', chair: 'board', reader: 'read' }[s.role];
    const me = a.reviewers.find(r => r.role === 'Security architect');
    const blocking = a.readiness.counts.errors > 0, pending = a.reviewers.filter(r => r.decision === 'pending').length, changes = a.reviewers.filter(r => r.decision === 'changes-requested').length;
    const canBoard = !blocking && !pending && !changes && a.status !== 'draft';
    const recordChip = rec ? chip(DECISION, rec.decision) : nochip;
    const record = d => () => { self.setState({ decisions: Object.assign({}, self.state.decisions, { [a.id]: { decision: d, note: self.state.note, by: ROLE_VIEW[s.role].name, at: TODAY } }), note: '' }); self.toast(roleCan === 'board' ? 'Board decision recorded as a Checkpoint · the bot commits the ARB record on ' + a.branch : 'Your decision is recorded on ' + a.id); };
    return { arb: { id: a.id, board: a.board, title: a.title, pf: PF[a.application].title, status: chip(ARB_STATUS, a.status), ready: chip(READINESS, a.readiness.readiness), from: (EL[a.from] || {}).title || fromTag, to: (EL[a.to] || {}).title || toTag, submittedBy: a.submittedBy, submittedAt: a.submittedAt, date: a.boardDate, wi: a.workItemId, pr: a.pr ? '#' + a.pr : 'not yet', branch: a.branch, sha: a.reviewedSha || 'not yet pinned', updatedSince: !!a.updatedSinceReview, updatedAt: a.updatedAt, owner: a.owner,
      kpi: { checks: a.readiness.checks.filter(c => c.status === 'pass').length + '/' + a.readiness.checks.length, checksNote: a.readiness.counts.errors + ' blocking · ' + a.readiness.counts.warnings + ' warnings', written: a.sections.length + '/7', writtenNote: '+ 6 sections from the model', cov: cov.n + '/13', covNote: cov.partly + ' partly · ' + cov.missing + ' missing', rev: a.reviewers.filter(r => r.decision === 'approved' || r.decision === 'approved-with-conditions').length + '/' + a.reviewers.filter(r => r.decision !== 'not-required').length, revNote: changes + ' change request · ' + pending + ' pending', cond: String(a.conditions.filter(c => c.status === 'open').length), condNote: 'of ' + a.conditions.length + ' condition' + (a.conditions.length === 1 ? '' : 's') + ' · ' + (a.asks || []).length + ' asks' },
      tabs: tabs.map(t => ({ id: t[0], label: t[1], n: t[2], on: s.arbTab === t[0], cls: s.arbTab === t[0] ? 'tab-on' : '', pick: self.set({ arbTab: t[0] }) })), tAsd: s.arbTab === 'asd', tChecks: s.arbTab === 'checks', tReview: s.arbTab === 'review', tDecision: s.arbTab === 'decision',
      toc: cov.items, sections, reqs, baseRows: landAt(fromTag), targetRows: landAt(toTag), baseTitle: (EL[a.from] || {}).title || '', targetTitle: (EL[a.to] || {}).title || '', scope, dds, adrs: (a.adr || []).map(x => ({ title: title(x), decision: (EL[x] || {}).decision || '', go: self.go(x) })), asks: (a.asks || []).map(x => ({ id: x.id, text: x.text, status: chip({ pending: ['info', 'i', 'Pending'], accepted: ['success', '✓', 'Accepted'], declined: ['error', '✕', 'Declined'] }, x.status) })), hasAsks: !!(a.asks && a.asks.length),
      checkGroups: uniq(a.readiness.checks.map(c => c.group)).map(g => ({ label: g, checks: a.readiness.checks.filter(c => c.group === g).map(c => ({ id: c.id, title: c.title, chip: chip(CHECK, c.status), sev: c.severity === 'error' ? 'blocks' : 'warns', items: c.items.map(it => ({ title: title(it.id), msg: it.message, go: self.go(it.id) })), hasItems: !!c.items.length })) })),
      reviewers: a.reviewers.map(r => ({ name: r.name, role: r.role, av: r.name.split(' ').map(x => x[0]).join(''), decision: chip(DECISION, r.decision), at: r.at || '', note: r.note || '', hasNote: !!r.note, isMe: s.role === 'reviewer' && r.role === 'Security architect', meCls: s.role === 'reviewer' && r.role === 'Security architect' ? 'me' : '' })),
      conditions: a.conditions.map(c => ({ id: c.id, text: c.text, owner: c.owner, due: c.due, status: chip({ open: ['warning', '!', 'Open'], closed: ['success', '✓', 'Closed'], met: ['success', '✓', 'Met'] }, c.status) })), hasConditions: !!a.conditions.length, noConditions: !a.conditions.length,
      canSubmit: roleCan === 'submit', canReview: roleCan === 'review', canBoard: roleCan === 'board', isReader: roleCan === 'read', boardEnabled: canBoard, boardWhy: blocking ? 'Approval is unavailable while blocking checks fail.' : changes ? 'A reviewer requested changes: the owner must address them and re-submit (the ASD is frozen again).' : pending ? pending + ' reviewer decision' + (pending > 1 ? 's are' : ' is') + ' still pending.' : a.status === 'draft' ? 'The submission is a draft: the owner has not run the readiness gate.' : 'All reviewers have decided; the board can record its decision.',
      myDecision: me ? chip(DECISION, me.decision) : nochip, myNote: me && me.note || '', note: s.note, onNote: e => self.setState({ note: e.target.value }),
      recorded: !!rec, record: rec ? { decision: recordChip, by: rec.by, at: rec.at, note: rec.note } : null,
      approve: record('approved'), approveCond: record('approved-with-conditions'), requestChanges: record('changes-requested'), reject: record('rejected'), notRequired: record('not-required'),
      boardDisabled: !canBoard, boardApprove: canBoard ? record('approved') : () => self.toast('Approval is unavailable: ' + (blocking ? 'a blocking check fails' : changes ? 'a reviewer requested changes' : pending ? 'a reviewer decision is pending' : 'the submission is a draft')), boardApproveCond: canBoard ? record('approved-with-conditions') : () => self.toast('Approval is unavailable while reviewers are pending or have requested changes'), boardReject: canBoard ? record('rejected') : () => self.toast('Decide once every reviewer has decided'),
      submitLabel: a.status === 'draft' ? 'Submit to ARB' : a.status === 'in-review' ? 'Re-submit after changes' : 'Submitted · ' + ARB_STATUS[a.status][2],
      submit: () => self.toast('Readiness gate run · ASD generated and frozen at ' + (a.reviewedSha || 'HEAD') + ' · PR ' + (a.pr ? '#' + a.pr : '') + ' leaves draft'),
      isDraft: a.status === 'draft', isInReview: a.status === 'in-review', isDecided: a.status === 'approved' || a.status === 'approved-with-conditions' || a.status === 'rejected',
      git: [{ k: 'Branch', v: a.branch }, { k: 'Pull request', v: a.pr ? '#' + a.pr + ' in the central repository' : 'not opened yet' }, { k: 'Reviewed commit', v: a.reviewedSha ? a.reviewedSha + (a.updatedSinceReview ? ' · updated since review' : '') : '—' }, { k: 'Required checks', v: 'arch-validate ' + (blocking ? '✕' : '✓') + ' · arb-decision ' + (a.status === 'approved' || a.status === 'approved-with-conditions' ? '✓' : 'pending') }, { k: 'On approval', v: 'bot commits the ARB record · merge commit · tag arb/' + a.application + '-' + a.board.split(' ')[1] }],
      asdMd: () => self.toast('ASD copied as Markdown (13 sections, ' + a.id + ')'), backLabel: s.pageFrom ? 'Back' : 'Back to Process · Reviews' } };
  }

  renderVals() {
    return Object.assign({}, this.simVals(), this.shellVals(), this.viewVals(), this.catVals(), this.pageVals(), this.procVals(), this.arbVals(), this.changeVals(), this.docVals(), this.proposalVals());
  }
}
