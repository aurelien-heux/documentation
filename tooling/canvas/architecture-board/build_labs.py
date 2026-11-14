"""Views lab and Process lab: four alternatives each on navigation, display and content, same shell and data.
usage: ARCH_DATA=arch_data.json python3 build_labs.py <ViewsLab.dc.html> <ProcessLab.dc.html>"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # shell.py, navgen.py, markup_check.py live one level up in the export bundle
import build_arch as B
from build_arch import sif, sfor, chip, chg, track, tile, I_CHEV, S, ROLE_CHIPS, HEADER, RAIL, NAVBAR, SUBHEADER, ELEMENT, ARBPAGE, TOAST, CSS

OUT_V, OUT_P = sys.argv[1], sys.argv[2]

LAB_CSS = CSS + r"""
.labbar{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:8px 12px;border-radius:12px;background:#FFFFFF;border:1px solid #CAC4CF}
.labnote{display:flex;flex-direction:column;gap:4px;padding:12px 16px;border-radius:12px;background:#FFFFFF;border:1px solid #CAC4CF;font-size:13px;line-height:19px;color:#1C1B1E}
.labnote b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif}
.placeholder{display:flex;gap:16px;align-items:center;padding:24px;border:1px solid #CAC4CF;border-radius:12px;background:#FAF4FF;font-size:14px;color:#48454E}
.grph{padding:14px 12px 4px;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:11px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;color:#48454E}
.sl .sc{font-size:10px;font-weight:700;letter-spacing:.4px;text-transform:uppercase;padding:1px 6px;border-radius:4px;background:#F2EBFA;color:#48454E;margin-left:auto}
.gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
.gcard{display:flex;flex-direction:column;gap:6px;padding:14px 16px;border:1px solid #CAC4CF;border-radius:12px;background:#fff;font:inherit;text-align:left;cursor:pointer;color:#1C1B1E;min-height:120px}
.gcard:hover{border-color:#35307E}
.gcard .gt{display:flex;align-items:center;gap:8px;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:15px;font-weight:600}
.gcard .gt .vk{margin-left:auto}
.gcard .gf{font-size:12px;color:#48454E}
.gcard .gd{font-size:13px;color:#1C1B1E}
.gthumb{height:44px;border-radius:8px;background:repeating-linear-gradient(90deg,#F2EBFA 0 22px,#fff 22px 24px),repeating-linear-gradient(0deg,#F2EBFA 0 10px,#fff 10px 12px);border:1px solid #ECE5F4}
.gthumb.k-matrix{background:repeating-linear-gradient(90deg,#E3DFFF 0 18px,#fff 18px 20px),repeating-linear-gradient(0deg,#F8F1FF 0 8px,#fff 8px 10px)}
.gthumb.k-timeline{background:linear-gradient(90deg,transparent 30%,#E3DFFF 30% 60%,transparent 60%),linear-gradient(0deg,#fff 0 30%,#F2EBFA 30% 34%,#fff 34% 64%,#F2EBFA 64% 68%,#fff 68%)}
.gthumb.k-table{background:repeating-linear-gradient(0deg,#F2EBFA 0 1px,#fff 1px 11px)}
.gthumb.k-cards{background:repeating-linear-gradient(90deg,#F8F1FF 0 60px,#fff 60px 68px)}
.rolerow{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.kan{display:grid;grid-template-columns:repeat(7,minmax(180px,1fr));gap:10px;overflow:auto}
.kcol{display:flex;flex-direction:column;gap:8px;min-width:0}
.kcol .kh{display:flex;align-items:center;gap:8px;padding:8px 10px;border-radius:8px;background:#F8F1FF;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:700;letter-spacing:.4px;text-transform:uppercase;color:#48454E}
.kcol .kh .n{margin-left:auto}
.kcard{display:flex;flex-direction:column;gap:6px;padding:10px 12px;border:1px solid #CAC4CF;border-radius:12px;background:#fff;font:inherit;text-align:left;cursor:pointer;color:#1C1B1E}
.kcard:hover{border-color:#35307E}
.kcard b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:13px;font-weight:600;line-height:17px}
.kcard .meta{line-height:15px}
.kcard.k-attention{background:#FFF4DE;border-color:#FFDEA0}
.kcard.k-blocked{background:#FFDAD6}
.agenda{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:24px;align-items:start}
.sess{border:1px solid #CAC4CF;border-radius:12px;background:#fff;padding:12px 14px;display:flex;flex-direction:column;gap:8px}
.sess .sh{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.sess .sh b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:16px}
.sess .sh .date{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:13px;color:#35307E;font-weight:700}
.sess.past{opacity:.7}
.inbox{display:flex;flex-direction:column;gap:8px}
.task{display:flex;align-items:center;gap:12px;padding:10px 12px;border:1px solid #CAC4CF;border-radius:12px;background:#fff;font:inherit;text-align:left;cursor:pointer;color:#1C1B1E}
.task:hover{border-color:#35307E}
.task .tt{flex:1;display:flex;flex-direction:column;min-width:0}
.task .tt b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:14px;font-weight:600}
.task .tt span{font-size:12px;color:#48454E}
.task .due{font-size:12px;color:#48454E;white-space:nowrap}
.task.t-due{border-color:#6A4E00;background:#FFF4DE}
@container win (max-width: 1199px){.agenda{grid-template-columns:1fr}.kan{grid-template-columns:repeat(7,210px)}}
"""

# ---------------------------------------------------------------------------------------------- Views lab
VIEWS_JS = r"""
  viewsLabVals() {
    const s = this.state, self = this, V = s.variant || 'A';
    const variants = [['A', 'By level · adopted'], ['B', 'By ADM phase'], ['C', 'Gallery'], ['D', 'By role']];
    const NOTES = {
      A: ['A · By steering level — adopted (2026-11-03)', 'A level picker (Enterprise · Portfolio · Application), then a side list of the views at that level, each tagged with its rendering and who it is for. The scope selects (portfolio, application) sit under the level picker.', 'The level is the first choice: it matches the reading axis (DEC-KB-20) and keeps each list at 3 to 9 items.'],
      B: ['B · By TOGAF ADM phase', 'No level picker: one side list grouped by ADM phase, Vision · Business · Information systems · Technology · Opportunities and migration · Governance, as DEC-KB-10 first described it. The scope is a tag on the item and the portfolio or application select appears in the view header only when the view needs it.', 'Speaks TOGAF to architects; longer list (20 items) and the level is no longer visible at a glance.'],
      C: ['C · Gallery', 'No side list: a page of cards, one per view, grouped by level, each with its rendering, who it is for and what it decides. A card opens the view full width, the subheader goes back to the gallery.', 'Best way in for newcomers and for a page that will grow; one click more per view for daily users, who come back to the same three views.'],
      D: ['D · By role', 'A row of role chips (CIO, portfolio architect, solution architect, data owner, CTO, PMO, business owner) replaces the level picker; the side list shows that role\'s views in reading order. Everything else is one chip away (All).', 'Fastest for daily use; roles are the "For" line of each view, so the mapping is data, not a second configuration; hides views until someone switches role.'],
    };
    const n = NOTES[V];
    const out = { labVariants: variants.map(v => ({ id: v[0], label: v[0] + ' · ' + v[1], on: V === v[0], cls: V === v[0] ? 'chip-on' : '', pick: self.set({ variant: v[0], galOpen: false }) })), labTitle: n[0], labText: n[1], labDelta: n[2], vA: V === 'A', vB: V === 'B', vC: V === 'C', vD: V === 'D' };
    const L = s.level, cur = s.view[L];
    const item = (lv, id) => { const v = VIEWS[lv].find(x => x[0] === id); const on = L === lv && cur === id; return { id: lv + '/' + id, title: v[1], who: v[2], decides: v[3], kind: KIND_LABEL[v[4]], kcls: 'vk-' + v[4], kthumb: 'k-' + v[4], scope: lv === 'enterprise' ? 'Enterprise' : lv === 'portfolio' ? 'Portfolio' : 'Application', on, cls: on ? 'sl-on' : '', pick: self.openView(lv, id, { galOpen: true }) }; };
    // B · phases
    const PH = [['Vision · A', [['enterprise', 'motivation']]], ['Business · B', [['enterprise', 'valuestreams'], ['enterprise', 'capmap'], ['enterprise', 'coverage'], ['enterprise', 'capvs'], ['enterprise', 'roles'], ['portfolio', 'procapp']]], ['Information systems · C', [['portfolio', 'landscape'], ['portfolio', 'cooperation'], ['portfolio', 'interaction'], ['portfolio', 'data'], ['application', 'factsheet'], ['application', 'inside'], ['application', 'interfaces']]], ['Technology · D', [['enterprise', 'tech'], ['portfolio', 'apptech']]], ['Opportunities & migration · E–F', [['portfolio', 'gap'], ['enterprise', 'roadmap'], ['portfolio', 'roadmap']]], ['Governance · G–H', [['portfolio', 'chain']]]];
    out.phases = PH.map(p => ({ label: p[0], items: p[1].map(x => item(x[0], x[1])) }));
    out.needsPf = L !== 'enterprise'; out.needsApp = L === 'application';
    // C · gallery
    out.galOpen = !!s.galOpen; out.galClosed = !s.galOpen;
    out.gallery = [['enterprise', 'Enterprise · CIO, enterprise architects'], ['portfolio', 'Portfolio · portfolio architects, ARB'], ['application', 'Application · application leads, teams']].map(g => ({ label: g[1], cards: VIEWS[g[0]].map(v => item(g[0], v[0])) }));
    out.backToGallery = self.set({ galOpen: false });
    // D · roles
    const RV = [['all', 'All', null], ['cio', 'CIO', [['enterprise', 'capmap'], ['enterprise', 'coverage'], ['enterprise', 'roadmap'], ['enterprise', 'motivation']]], ['pfa', 'Portfolio architect', [['portfolio', 'landscape'], ['portfolio', 'gap'], ['portfolio', 'roadmap'], ['portfolio', 'chain'], ['portfolio', 'interaction'], ['portfolio', 'procapp']]], ['sol', 'Solution architect', [['portfolio', 'cooperation'], ['application', 'inside'], ['application', 'interfaces'], ['application', 'factsheet']]], ['data', 'Data owner', [['portfolio', 'data'], ['application', 'interfaces']]], ['cto', 'CTO · platform', [['enterprise', 'tech'], ['portfolio', 'apptech']]], ['pmo', 'PMO', [['enterprise', 'roadmap'], ['portfolio', 'roadmap'], ['portfolio', 'gap']]], ['biz', 'Business owner', [['enterprise', 'valuestreams'], ['enterprise', 'capvs'], ['enterprise', 'roles']]]];
    const rv = s.roleV || 'pfa';
    out.roleChips = RV.map(r => ({ id: r[0], label: r[1], on: rv === r[0], cls: rv === r[0] ? 'chip-on' : '', pick: self.set({ roleV: r[0] }) }));
    const sel = RV.find(r => r[0] === rv);
    out.roleList = sel[2] ? sel[2].map(x => item(x[0], x[1])) : [].concat.apply([], ['enterprise', 'portfolio', 'application'].map(lv => VIEWS[lv].map(v => item(lv, v[0]))));
    out.roleLabel = sel[1];
    return out;
  }
"""
SCOPE_SELECTS = ('<div class="rolerow">' + sif('needsPf', '<label class="lbl" for="pf-sel3">Portfolio</label><select id="pf-sel3" class="sel" style="width: auto" value="{{pf}}" onChange="{{pickPf}}">' + sfor('pfs', 'p', '<option value="{{p.id}}">{{p.title}}</option>', 4) + '</select>') + sif('needsApp', '<label class="lbl" for="app-sel3">Application</label><select id="app-sel3" class="sel" style="width: auto" value="{{app}}" onChange="{{pickApp}}">' + sfor('apps', 'p', '<option value="{{p.id}}">{{p.title}}</option>', 6) + '</select>') + '</div>')
SL_ITEM = '<button type="button" class="sl {{v.cls}}" aria-current="{{v.on}}" onClick="{{v.pick}}"><b>{{v.title}}<span class="vk {{v.kcls}}">{{v.kind}}</span></b><span>{{v.who}} · <span class="sc" style="margin: 0">{{v.scope}}</span></span></button>'
VA = sif('vA', B.VIEWS_AREA.replace("<sc-if value=\"{{isViews}}\" hint-placeholder-val=\"{{false}}\">", "").rsplit('</sc-if>', 1)[0])
VIEW_BLOCKS_LAB = B.VIEW_BLOCKS.replace(B.DIAGRAM, '')
assert VIEW_BLOCKS_LAB != B.VIEW_BLOCKS
VB = sif('vB', '<div class="area"><div class="side"><nav aria-label="Views by ADM phase" style="display: flex; flex-direction: column; gap: 2px">' + sfor('phases', 'ph', '<span class="grph">{{ph.label}}</span>' + sfor('ph.items', 'v', SL_ITEM, 4), 6) + '</nav></div><div class="content">' + SCOPE_SELECTS + B.VIEW_HEAD + VIEW_BLOCKS_LAB + '</div></div>')
VC = sif('vC', sif('galClosed', sfor('gallery', 'g', '<span class="lbl">{{g.label}}</span><div class="gal">' + sfor('g.cards', 'v', '<button type="button" class="gcard" onClick="{{v.pick}}"><span class="gt">{{v.title}}<span class="vk {{v.kcls}}">{{v.kind}}</span></span><span class="gthumb {{v.kthumb}}"></span><span class="gf">For {{v.who}}</span><span class="gd">Decides {{v.decides}}</span></button>', 6) + '</div>', 3))
  + sif('galOpen', '<div class="rolerow"><button type="button" class="chip" onClick="{{backToGallery}}">‹ All views</button>' + SCOPE_SELECTS + '</div><div class="content">' + B.VIEW_HEAD + VIEW_BLOCKS_LAB + '</div>'))
VD = sif('vD', '<div class="rolerow"><span class="lbl">I am</span>' + sfor('roleChips', 'r', '<button type="button" class="chip {{r.cls}}" aria-pressed="{{r.on}}" onClick="{{r.pick}}">{{r.label}}</button>', 8) + '</div><div class="area"><div class="side"><span class="lbl">Views for {{roleLabel}}</span><nav aria-label="Views for this role" style="display: flex; flex-direction: column; gap: 2px">' + sfor('roleList', 'v', SL_ITEM, 5) + '</nav>' + SCOPE_SELECTS + '</div><div class="content">' + B.VIEW_HEAD + VIEW_BLOCKS_LAB + '</div></div>')
VIEWS_LAB_AREA = sif('isViews', VA + VB + VC + VD)

# ---------------------------------------------------------------------------------------------- Process lab
PROC_JS = r"""
  procLabVals() {
    const s = this.state, self = this, V = s.variant || 'A';
    const variants = [['A', 'By object · adopted'], ['B', 'Board'], ['C', 'Agenda & roadmap'], ['D', 'Inbox']];
    const NOTES = {
      A: ['A · By object — adopted (2026-11-03)', 'A side list by kind of object: Changes, Reviews, Decisions, Model checks, How it works. Changes are cards with their four steps; reviews a table; the ARB page has four tabs.', 'Complete and predictable; nothing tells you what needs you today.'],
      B: ['B · Board: the changes by phase', 'One board, the six phases of the adjusted TOGAF flow plus Delivered; each change is a card in the column of its current phase, tinted when it waits at a gate that needs attention or is blocked, with its class, entry point, portfolio and review status. Decisions, checks and the process guide are chips above the board.', 'Shows the flow, the gates and the bottlenecks at a glance; cards carry less than the current ones (no phase strip), and the board is seven columns wide.'],
      C: ['C · Agenda and roadmap', 'The Process opens on the board calendar: one card per ARB session with its date, its submissions and their readiness, then the enterprise roadmap under it and, on the right, the conditions and asks by due date. Reviews, decisions and checks are reached from the cards.', 'Content-first: it adds what the current page lacks (sessions, due dates); it serves the chair and the PMO more than the change owner.'],
      D: ['D · Inbox: what needs you', 'A first list computed from the model for the person viewing (owner: changes to model, requests to address, conditions due; reviewer: decisions pending; chair: boards ready or waiting; reader: nothing to do), then everything else as compact rows.', 'Role-aware and action-first; depends on the roles being known (SSO, CODEOWNERS) and on the rules staying simple.'],
    };
    const n = NOTES[V];
    const out = { labVariants: variants.map(v => ({ id: v[0], label: v[0] + ' · ' + v[1], on: V === v[0], cls: V === v[0] ? 'chip-on' : '', pick: self.set({ variant: v[0] }) })), labTitle: n[0], labText: n[1], labDelta: n[2], vA: V === 'A', vB: V === 'B', vC: V === 'C', vD: V === 'D' };
    const WPS = D.roadmap.workPackages;
    const arbOf = w => D.arbs.find(a => a.workItemId === w.workItemId);
    // B · board
    const cols = HOW.phases.map(ph => ({ label: ph.n + ' · ' + ph.title, sub: ph.gate ? 'then ' + ph.gate.id + ' · ' + ph.gate.title : 'no gate' })).concat([{ label: 'Delivered', sub: 'plateau → new baseline' }]);
    out.kanban = cols.map((c, i) => ({ label: c.label, sub: c.sub, cards: WPS.map(w => ({ w, f: self.flowOf(w) })).filter(x => x.f.cur === i).map(x => { const a = arbOf(x.w); const st = x.f.gateState; return { title: x.w.title, pf: PF[x.w.chain].title, klass: x.w.class, klassCls: 'kl-' + x.w.class, note: x.f.now, chip: chip({ pending: ['info', 'i', x.f.gatePending ? 'At ' + x.f.gatePending : 'In progress'], attention: ['warning', '!', x.f.gatePending + ' · needs attention'], blocked: ['error', '✕', x.f.gatePending + ' · blocked'] }, x.f.gatePending ? st : 'pending'), cls: 'k-' + (x.f.gatePending ? st : 'progress'), arb: a ? chip(ARB_STATUS, a.status) : nochip, hasArb: !!a, entry: x.f.entry.name, go: a && i === 2 ? self.go(a.id) : self.go(x.w.id), dates: x.w.start + ' → ' + x.w.end }; }), n: 0 })).map(c => Object.assign(c, { n: String(c.cards.length) }));
    out.boardExtras = [['decisions', 'Decisions'], ['checks', 'Model checks'], ['how', 'How it works']].map(x => ({ id: x[0], label: x[1], on: s.bExtra === x[0], cls: s.bExtra === x[0] ? 'chip-on' : '', pick: () => self.setState({ bExtra: self.state.bExtra === x[0] ? null : x[0], proc: x[0] }) }));
    out.bDecisions = s.bExtra === 'decisions'; out.bChecks = s.bExtra === 'checks'; out.bHow = s.bExtra === 'how';
    // C · agenda
    const sessions = {}; D.arbs.forEach(a => { (sessions[a.boardDate] = sessions[a.boardDate] || { date: a.boardDate, board: a.board, subs: [] }).subs.push(a); });
    out.sessions = Object.values(sessions).sort((x, y) => x.date.localeCompare(y.date)).map(se => ({ date: se.date, board: se.board, past: se.date < TODAY, cls: se.date < TODAY ? 'past' : '', when: se.date < TODAY ? 'held' : 'upcoming', subs: se.subs.map(a => ({ title: a.title, pf: PF[a.application].title, status: chip(ARB_STATUS, a.status), ready: chip(READINESS, a.readiness.readiness), pending: a.reviewers.filter(r => r.decision === 'pending').length + ' pending · ' + a.reviewers.filter(r => r.decision === 'changes-requested').length + ' change request', cov: self.coverage(a).n + '/13', go: self.go(a.id), asks: (a.asks || []).filter(x => x.status === 'pending').length })) }));
    const dues = []; D.arbs.forEach(a => { a.conditions.forEach(c => dues.push({ kind: 'Condition ' + c.id, text: c.text, owner: c.owner, due: c.due, status: chip({ open: ['warning', '!', 'Open'], closed: ['success', '✓', 'Closed'], met: ['success', '✓', 'Met'] }, c.status), go: self.go(a.id), arb: a.board })); (a.asks || []).forEach(x => dues.push({ kind: 'Ask ' + x.id, text: x.text, owner: 'the board', due: a.boardDate, status: chip({ pending: ['info', 'i', 'Pending'], accepted: ['success', '✓', 'Accepted'] }, x.status), go: self.go(a.id), arb: a.board })); });
    out.dues = dues.sort((x, y) => x.due.localeCompare(y.due));
    out.rm = self.roadmapBands(D.portfolios.map(p => p.id));
    // D · inbox
    const role = s.role, tasks = [];
    const T = (title, sub, due, go, urgent) => tasks.push({ title, sub, due: due || '', go, cls: urgent ? 't-due' : '' });
    if (role === 'owner') {
      WPS.filter(w => w.chain === 'corporate').forEach(w => { const a = arbOf(w); const st = self.stepStatus(w);
        if (a && a.readiness.counts.changesRequested) T('Address the change request on ' + a.board, a.reviewers.find(r => r.decision === 'changes-requested').note, 'before ' + a.boardDate, self.go(a.id), true);
        if (a && a.updatedSinceReview) T('Branch moved after review · ' + w.title, 'Ask the chair for a delta review, or stop pushing to ' + a.branch, '', self.go(a.id), false);
        if (!a && w.status === 'draft') T('Finish the design of ' + w.title, st[1].note + ' · then Submit to ARB', w.end, self.go(w.id), false);
        if (a) a.conditions.filter(c => c.status === 'open').forEach(c => T('Condition ' + c.id + ' · ' + c.text, 'owner ' + c.owner + ' · ' + a.board, c.due, self.go(a.id), false)); });
    } else if (role === 'reviewer') {
      D.arbs.forEach(a => { const me = a.reviewers.find(r => r.role === 'Security architect'); if (me && me.decision === 'pending') T('Record your decision on ' + a.board, a.title + ' · board on ' + a.boardDate, a.boardDate, self.go(a.id), a.status !== 'draft'); if (me && me.decision === 'changes-requested') T('Waiting for the owner · ' + a.board, 'You requested: ' + me.note, '', self.go(a.id), false); });
    } else if (role === 'chair') {
      D.arbs.filter(a => a.status === 'in-review' || a.status === 'submitted').forEach(a => { const pend = a.reviewers.filter(r => r.decision === 'pending').length, chg = a.readiness.counts.changesRequested; T((pend || chg ? 'Not ready to decide · ' : 'Ready to decide · ') + a.board, (pend ? pend + ' reviewer pending' : '') + (chg ? (pend ? ' · ' : '') + chg + ' change request' : '') + (a.updatedSinceReview ? ' · updated since review: choose delta or full review' : ''), a.boardDate, self.go(a.id), !pend && !chg); });
      D.arbs.filter(a => a.status === 'draft').forEach(a => T('Draft on the agenda · ' + a.board, a.title + ' · readiness ' + READINESS[a.readiness.readiness][2].toLowerCase(), a.boardDate, self.go(a.id), false));
    }
    out.tasks = tasks; out.hasTasks = !!tasks.length; out.noTasks = !tasks.length; out.taskN = tasks.length + (tasks.length === 1 ? ' thing needs you' : ' things need you') + ' · ' + ROLE_VIEW[role].label;
    out.rest = WPS.map(w => { const a = arbOf(w), st = self.stepStatus(w), f = self.flowOf(w), cur = st.find(x => x.chip.cls !== 'success' && x.cls !== 'step-skip') || st[3]; return { title: w.title, pf: PF[w.chain].title, klass: w.class, klassCls: 'kl-' + w.class, step: f.now, chip: cur.chip, note: '', arb: a ? chip(ARB_STATUS, a.status) : nochip, hasArb: !!a, go: self.go(w.id) }; });
    return out;
  }
"""
PA = sif('vA', B.PROC_AREA.replace("<sc-if value=\"{{isProc}}\" hint-placeholder-val=\"{{false}}\">", "").rsplit('</sc-if>', 1)[0])
KCARD = '<button type="button" class="kcard {{c.cls}}" onClick="{{c.go}}"><b>{{c.title}}</b><span class="meta">{{c.pf}} · {{c.dates}} · entered as {{c.entry}}</span><span style="display: flex; gap: 6px; flex-wrap: wrap; align-items: center"><span class="kl {{c.klassCls}}">{{c.klass}}</span>' + chip('c.arb', 'sm') + '</span>' + chip('c.chip', 'sm') + '<span class="meta">{{c.note}}</span></button>'
PB = sif('vB', '<div class="rolerow"><span class="meta">One card per change, in the column of its current step.</span><span style="flex: 1"></span>' + sfor('boardExtras', 'x', '<button type="button" class="chip {{x.cls}}" aria-pressed="{{x.on}}" onClick="{{x.pick}}">{{x.label}}</button>', 3) + '</div>'
  '<div class="kan">' + sfor('kanban', 'k', '<div class="kcol"><div class="kh" title="{{k.sub}}">{{k.label}}<span class="n">{{k.n}}</span></div><span class="meta" style="padding: 0 4px">{{k.sub}}</span>' + sfor('k.cards', 'c', KCARD, 2) + '</div>', 7) + '</div>'
  + sif('bDecisions', B.DECISIONS.replace("<sc-if value=\"{{p_decisions}}\" hint-placeholder-val=\"{{false}}\">", "").rsplit('</sc-if>', 1)[0])
  + sif('bChecks', B.CHECKS.replace("<sc-if value=\"{{p_checks}}\" hint-placeholder-val=\"{{false}}\">", "").rsplit('</sc-if>', 1)[0])
  + sif('bHow', B.HOWTAB.replace("<sc-if value=\"{{p_how}}\" hint-placeholder-val=\"{{false}}\">", "").rsplit('</sc-if>', 1)[0]))
PC = sif('vC', '<div class="agenda"><div style="display: flex; flex-direction: column; gap: 12px"><span class="lbl">Architecture Board · sessions</span>' + sfor('sessions', 'se', '<div class="sess {{se.cls}}"><div class="sh"><span class="date">{{se.date}}</span><b>{{se.board}}</b><span class="meta">{{se.when}}</span></div><div class="rows">' + sfor('se.subs', 'a', '<button type="button" class="row" onClick="{{a.go}}">' + tile("'implementation'", "'work-package'") + '<span class="txt"><b>{{a.title}}</b><span>{{a.pf}} · {{a.pending}} · ASD {{a.cov}}</span></span>' + chip('a.ready', 'sm') + chip('a.status', 'sm') + I_CHEV + '</button>', 1) + '</div></div>', 4)
  + '<span class="lbl">Enterprise roadmap</span>' + B.ROADMAP + '</div>'
  '<div style="display: flex; flex-direction: column; gap: 8px"><span class="lbl">Conditions and asks · by due date</span><div class="inbox">' + sfor('dues', 'd', '<button type="button" class="task" onClick="{{d.go}}"><span class="tt"><b>{{d.kind}} · {{d.arb}}</b><span>{{d.text}}</span><span>owner {{d.owner}}</span></span><span class="due">{{d.due}}</span>' + chip('d.status', 'sm') + '</button>', 4) + '</div></div></div>')
PD = sif('vD', '<span class="lbl">{{taskN}}</span>' + sif('hasTasks', '<div class="inbox">' + sfor('tasks', 't', '<button type="button" class="task {{t.cls}}" onClick="{{t.go}}"><span class="tt"><b>{{t.title}}</b><span>{{t.sub}}</span></span><span class="due">{{t.due}}</span>' + I_CHEV + '</button>', 3) + '</div>') + sif('noTasks', '<div class="placeholder"><span class="st st-success"><span class="tile">✓</span>Nothing needs you</span>Switch the prototype to Change owner, Reviewer or Board chair to see their inbox.</div>')
  + '<span class="lbl">Everything else · 8 changes</span><div class="inbox">' + sfor('rest', 'r', '<button type="button" class="task" onClick="{{r.go}}">' + tile("'implementation'", "'work-package'") + '<span class="tt"><b>{{r.title}}</b><span>{{r.pf}} · {{r.step}}: {{r.note}}</span></span><span class="kl {{r.klassCls}}">{{r.klass}}</span>' + chip('r.arb', 'sm') + chip('r.chip', 'sm') + '</button>', 8) + '</div>')
PROC_LAB_AREA = sif('isProc', PA + PB + PC + PD)

def make(title, area_default, js, area_html, other_html, out, preview_h):
    logic = B.logic
    logic = logic.replace("decisions: {}, note: '', toast: null, pfFilter: 'all',", "decisions: {}, note: '', toast: null, pfFilter: 'all', variant: 'A', galOpen: false, roleV: 'pfa', bExtra: null,")
    logic = logic.replace("role: 'owner', area: 'elements', level: 'enterprise',", f"role: 'owner', area: '{area_default}', level: 'enterprise',")
    fn = 'viewsLabVals' if 'viewsLabVals' in js else 'procLabVals'
    logic = logic.replace("  renderVals() {\n    return Object.assign({}, this.simVals(), this.shellVals(), this.viewVals(), this.catVals(), this.pageVals(), this.procVals(), this.arbVals());\n  }",
                          js + "  renderVals() {\n    return Object.assign({}, this.simVals(), this.shellVals(), this.viewVals(), this.catVals(), this.pageVals(), this.procVals(), this.arbVals(), this." + fn + "());\n  }")
    logic = logic.replace("const hasDiagram = !!DIAG[cur],", "const hasDiagram = false && !!DIAG[cur],")
    assert "hasDiagram = false &&" in logic
    assert fn in logic and 'variant:' in logic
    lab_bar = ('<div class="labbar" role="group" aria-label="Lab"><span class="simlab">' + title.upper() + ' · PICK ONE</span>' + sfor('labVariants', 'v', '<button type="button" class="chip {{v.cls}}" aria-pressed="{{v.on}}" onClick="{{v.pick}}">{{v.label}}</button>', 4) + '</div>'
               '<div class="labnote"><b>{{labTitle}}</b><span>{{labText}}</span><span class="meta">{{labDelta}}</span></div>')
    body = ('<div style="display: flex; flex-direction: column; gap: 12px; padding: 12px; background: #ECE5F4; min-height: 100vh; box-sizing: border-box; font-family: \'Open Sans\', system-ui, sans-serif">'
            + lab_bar + S.sim_bar(ROLE_CHIPS) + S.sim_open('sim-host-arch')
            + '<div class="app" style="min-height: {{simFrameH}}px">' + HEADER + '<div class="bodyrow">' + RAIL + '<main>'
            + sif('noPage', SUBHEADER + B.AREA_TABS) + area_html + other_html + ELEMENT + ARBPAGE
            + '</main></div>' + NAVBAR + TOAST + '</div>' + S.SIM_CLOSE + '</div>')
    assert '</script' not in logic and '</script' not in body
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
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
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1440,"height":{preview_h}}}}}'>
{logic}
</script>
</body>
</html>
'''
    B.emit(page, out)

PH = lambda what: '<div class="placeholder"><span class="st st-info"><span class="tile">i</span>Not in the lab</span>' + what + ' are on the Architecture board; this lab only changes the ' + ('Views' if 'Views' not in what else 'Process') + ' area.</div>'
make('Views lab', 'views', VIEWS_JS, VIEWS_LAB_AREA, sif('isCat', PH('Catalogue and Process')) + sif('isProc', PH('Catalogue and Process')), OUT_V, 1400)
make('Process lab', 'process', PROC_JS, PROC_LAB_AREA, sif('isCat', PH('Catalogue and Views')) + sif('isViews', PH('Catalogue and Views')), OUT_P, 1400)
