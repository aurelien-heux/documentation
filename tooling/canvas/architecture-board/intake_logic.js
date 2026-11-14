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
