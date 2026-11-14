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
    const plateau = pl && pl.reaches ? title(pl.reaches) : '';
    const version = rel.length ? rel.map(v => v.tag).join(' · ') + (pl ? ' · next ' + pl.tag.split(' ').pop() + (plateau ? ' reaches ' + plateau : '') : '') : pl ? pl.tag + ' · ' + pl.at + (plateau ? ' · reaches ' + plateau : '') : 'No version yet';
    const g3 = dl.fl.phases[4] && dl.fl.phases[4].state === 'done';
    return { hasReq: !!dl.req, req: dl.req ? title(dl.req) : 'No requirement yet', goReq: dl.req ? self.go(dl.req) : null,
      gap: self.gapCountsOf(w), goGap: self.openView('portfolio', 'gap', { pf: w.chain }),
      tickets: dl.total ? dl.done + '/' + dl.total + ' done' : 'None yet', ticketsSub: dl.total ? (dl.doing ? dl.doing + ' in progress' : dl.done === dl.total ? 'all delivered' : 'none in progress') : (g3 ? 'to create' : 'after G3 · Ready to build'),
      commits: dl.cs.length ? String(dl.cs.length) : '0', commitsSub: dl.last ? 'last ' + dl.last.sha + ' · ' + dl.last.at : 'no commit yet',
      version, hasVersions: !!dl.vs.length, versionSub: pl && plateau ? 'then the plateau' : rel.length ? rel[rel.length - 1].note || '' : '',
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
    return { has: true, chain, standards: std, hasStandards: !!std.length, req: req ? title(req) : '', hasReq: !!req, goReq: req ? self.go(req) : null, reqRows: req && EL[req].acceptance ? EL[req].acceptance.length + ' acceptance rows' : '' };
  }
  howAgentsVals() { return { howMcp: DELIV.mcp.server, howMcpTools: DELIV.mcp.tools.map(t => ({ name: t[0], arg: t[1], what: t[2] })), howMcpClients: DELIV.mcp.clients.map(c => ({ name: c[0], how: c[1] })) }; }
