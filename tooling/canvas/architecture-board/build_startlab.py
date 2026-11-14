"""Change start lab: how a change starts (three alternatives) and how the phases in progress are followed (four
alternatives), same shell and the same example data — changes on every phase and at every gate, with their origin.
usage: ARCH_DATA=arch_data.json python3 build_startlab.py <StartLab.dc.html>"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import build_arch as B
from build_arch import sif, sfor, chip, S, ROLE_CHIPS, HEADER, RAIL, NAVBAR, TOAST, CSS
import startlab_data

OUT = sys.argv[1]

LAB_CSS = CSS + r"""
.labbar{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:8px 12px;border-radius:12px;background:#FFFFFF;border:1px solid #CAC4CF}
.labbar .sep{width:1px;align-self:stretch;background:#CAC4CF;margin:0 6px}
.labnote{display:grid;grid-template-columns:1fr 1fr;gap:6px 24px;padding:12px 16px;border-radius:12px;background:#FFFFFF;border:1px solid #CAC4CF;font-size:13px;line-height:19px;color:#1C1B1E}
.labnote b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif}
.labnote div{display:flex;flex-direction:column;gap:2px}
.lm{display:flex;gap:24px;align-items:flex-start}
.lm-c{flex:1;min-width:0;display:flex;flex-direction:column;gap:16px}
.lhead{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.lhead .h2{flex:1 1 200px;margin:0;font:600 22px/28px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;color:#1C1B1E}
.og{display:inline-grid;place-items:center;width:22px;height:22px;flex:none;border-radius:6px;font:700 11px/1 Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;background:#ECE5F4;color:#48454E}
.og-ticket{background:#E3DFFF;color:#14085E}.og-chat{background:#CFEDFA;color:#0A5570}.og-idea{background:#F2EBFA;color:#48454E}.og-radar{background:#DFF3D8;color:#1B5F1F}
.og-adr{background:#FFDEA0;color:#6A4E00}.og-pr{background:#1D1A27;color:#fff}.og-finding{background:#FFE9C7;color:#6A4E00}.og-incident{background:#FFDAD6;color:#93000A}
.orow{display:flex;align-items:center;gap:6px;min-width:0;font-size:12px;line-height:16px;color:#48454E}
.orow b{font-weight:600;color:#1C1B1E}
.tg{display:inline-flex;align-items:center;height:20px;padding:0 6px;border-radius:4px;background:#191836;color:#fff;font:700 10px/1 Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;letter-spacing:.4px;white-space:nowrap}
/* A · board */
.kan{display:grid;grid-template-columns:repeat(7,minmax(200px,1fr));gap:10px;overflow:auto;padding-bottom:8px}
.kcol{display:flex;flex-direction:column;gap:8px;min-width:0}
.kh{display:flex;flex-direction:column;gap:4px;padding:8px 10px;border-radius:8px;background:#F8F1FF}
.kh .k1{display:flex;align-items:center;gap:6px;font:700 12px/16px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;letter-spacing:.3px;text-transform:uppercase;color:#1C1B1E}
.kh .k1 .n{margin-left:auto;color:#48454E}
.kh .k2{font-size:11px;line-height:15px;color:#48454E}
.kcard{display:flex;flex-direction:column;gap:6px;padding:10px 12px;border:1px solid #CAC4CF;border-radius:12px;background:#fff;font:inherit;text-align:left;cursor:pointer;color:#1C1B1E;min-width:0}
.kcard:hover{border-color:#35307E}.kcard:focus-visible,.trow:focus-visible,.adm:focus-visible,.pick:focus-visible{outline:2px solid #35307E;outline-offset:2px}
.kcard b{font:600 13px/17px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif}
.kcard.k-attention{background:#FFF8E6;border-color:#6A4E00}
.kcard.k-blocked{background:#FFEDEA;border-color:#93000A}
.kcard.k-closed{border-style:dashed;background:#FAF4FF}
.kcard.k-new{box-shadow:0 0 0 2px #35307E}
/* B · tracks */
.trk2{display:flex;align-items:center;gap:0}
.trk2 .d{width:22px;height:22px;border-radius:50%;border:1px solid #CAC4CF;background:#fff;display:grid;place-items:center;font:700 10px/1 Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;color:#79757F}
.trk2 .d.ph-done{background:#ACF4A2;border-color:#1B5F1F;color:#1B5F1F}.trk2 .d.ph-current{background:#35307E;border-color:#35307E;color:#fff}.trk2 .d.ph-skipped{border-style:dashed;opacity:.55;background:#fff}.trk2 .d.ph-todo{background:#FAF4FF}
.trk2 .l{width:10px;height:1px;background:#CAC4CF}
.trk2 .gt{width:22px;height:22px;margin:0 2px}
.trow{display:grid;grid-template-columns:minmax(220px,1.4fr) 300px minmax(200px,1.3fr) auto;gap:6px 16px;align-items:center;width:100%;padding:10px 14px;border:0;border-top:1px solid #ECE5F4;background:#fff;font:inherit;text-align:left;color:#1C1B1E;cursor:pointer}
.trow:hover{background:#FAF4FF}
.trow .t1{display:flex;flex-direction:column;gap:3px;min-width:0}
.trow .t1 b{font:600 14px/20px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif}
.tgrp{border:1px solid #CAC4CF;border-radius:12px;overflow:hidden;background:#fff}
.tgrp .tg-h{display:flex;align-items:center;gap:8px;padding:8px 14px;background:#F8F1FF;font:700 11px/16px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;letter-spacing:.5px;text-transform:uppercase;color:#48454E}
.tlegend{display:flex;align-items:center;gap:6px 14px;flex-wrap:wrap;font-size:12px;color:#48454E}
/* C · gates */
.gsec{border:1px solid #CAC4CF;border-radius:12px;background:#fff;overflow:hidden}
.gsec-h{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:10px 14px;background:#F8F1FF}
.gsec-h .gt{margin:0}.gsec-h b{font:600 15px/20px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif}
.gsec-b{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0}
.gcol{display:flex;flex-direction:column;gap:8px;padding:10px 14px;min-width:0;border-left:1px solid #ECE5F4}.gcol:first-child{border-left:0}
.gcol .none{font-size:12px;color:#79757F}
.between{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:2px 14px;font-size:12px;color:#48454E}
/* D · ADM */
.admrow{display:flex;align-items:stretch;gap:0;overflow:auto;padding:2px 2px 10px}
.adm{flex:1 1 0;min-width:118px;display:flex;flex-direction:column;gap:2px;padding:8px 10px;border:1px solid #CAC4CF;border-radius:10px;background:#fff;font:inherit;text-align:left;color:#1C1B1E;cursor:pointer}
.adm .a1{display:flex;align-items:center;gap:6px}.adm .a1 .n{margin-left:auto;font:700 16px/20px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;color:#35307E}
.adm b{font:600 13px/17px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif}.adm span.s{font-size:11px;line-height:14px;color:#48454E}
.adm-on{background:#E3DFFF;border-color:#35307E;box-shadow:inset 0 0 0 1px #35307E}
.adm-empty .a1 .n{color:#79757F}
.admd{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.4fr);gap:16px;align-items:start}
/* start */
.startc{border:1px solid #35307E;border-radius:12px;background:#fff;padding:14px 16px;display:flex;flex-direction:column;gap:12px}
.picks{display:flex;gap:8px;flex-wrap:wrap}
.pick{display:flex;align-items:center;gap:8px;padding:6px 10px;border:1px solid #79757F;border-radius:8px;background:#fff;font:inherit;color:#1C1B1E;cursor:pointer;text-align:left}
.pick .p2{display:flex;flex-direction:column}.pick .p2 b{font:600 13px/17px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif}.pick .p2 span{font-size:11px;line-height:14px;color:#48454E}
.pick-on{background:#E3DFFF;border-color:#35307E}
.result{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
.result .dli b{font-size:13px;line-height:18px}
.sigrow{display:flex;align-items:flex-start;gap:12px;padding:10px 14px;border-top:1px solid #ECE5F4;flex-wrap:wrap}
.sigrow:first-child{border-top:0}
.sigrow .s1{flex:1 1 320px;display:flex;flex-direction:column;gap:3px;min-width:0}
.sigrow .s1 b{font:600 14px/20px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif}
.sigrow .s2{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.sig-done{background:#FAF4FF}
/* assistant pane (the global pane of the product, reduced to what the lab needs) */
.apane{flex:none;width:380px;border:1px solid #CAC4CF;border-radius:16px;background:#fff;display:flex;flex-direction:column;min-height:520px;overflow:hidden}
.apane-h{display:flex;align-items:center;gap:8px;padding:10px 14px;border-bottom:1px solid #ECE5F4}.apane-h b{flex:1;font:600 15px/20px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif}
.apane-b{flex:1;display:flex;flex-direction:column;gap:10px;padding:14px;overflow:auto}
.aq{align-self:flex-end;max-width:88%;padding:8px 12px;border-radius:14px 14px 4px 14px;background:#E3DFFF;color:#191836;font-size:14px;line-height:20px}
.aa{font-size:14px;line-height:20px;color:#1C1B1E}
.asug{display:flex;flex-direction:column;gap:6px}
.asug .pick{width:100%;box-sizing:border-box}
.aprop{border:1px solid #CAC4CF;border-radius:12px;padding:10px 12px;display:flex;flex-direction:column;gap:6px}
.aprop dl{display:grid;grid-template-columns:96px 1fr;gap:3px 10px;margin:0;font-size:13px;line-height:18px}.aprop dt{color:#48454E}.aprop dd{margin:0}
.apane-f{padding:10px 14px;border-top:1px solid #ECE5F4;font-size:12px;color:#48454E}
/* detail */
.dgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.crit{display:flex;align-items:flex-start;gap:8px;font-size:13px;line-height:18px}
.crit i{flex:none;width:18px;height:18px;border-radius:50%;display:grid;place-items:center;font:700 10px/1 Manrope,sans-serif;font-style:normal;background:#ECE5F4;color:#48454E}
.crit.c-ok i{background:#ACF4A2;color:#1B5F1F}
.ph .tgf{font:700 9px/12px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;letter-spacing:.4px;color:#35307E}
@container win (max-width: 1199px){.trow{grid-template-columns:minmax(0,1fr) 300px}.trow .t3,.trow .t4{grid-column:1 / -1}.admd{grid-template-columns:1fr}.gsec-b{grid-template-columns:1fr}.gcol{border-left:0;border-top:1px solid #ECE5F4}.gcol:first-child{border-top:0}.result{grid-template-columns:repeat(2,minmax(0,1fr))}}
@container win (max-width: 839px){.lm-c.with-pane{display:none}.apane{width:100%;min-height:70vh}.dgrid{grid-template-columns:1fr}.labnote{grid-template-columns:1fr}.trow{grid-template-columns:1fr}.kan{grid-template-columns:repeat(7,220px)}}
@container win (max-width: 599px){.result{grid-template-columns:1fr}}
"""

LAB_JS = r"""
  startLabVals() {
    const s = this.state, self = this, L = s.lab || {}, P = HOW.phases, E = HOW.entries;
    const upd = o => () => self.setState({ lab: Object.assign({}, self.state.lab, o) });
    const SV = L.start || 'A', FV = L.follow || 'A';
    const ORI = {}; LAB.origins.forEach(o => { ORI[o.id] = o; });
    const entryOf = id => E.find(e => e.id === id);
    const togaf = i => LAB.phases[Math.min(i, 6)].togaf;
    const phTitle = i => i >= 6 ? 'Delivered' : P[i].title;
    const gateAfter = i => { for (let k = Math.min(i, 5); k < 6; k++) if (P[k].gate) return { g: P[k].gate, k }; return null; };
    const GATE = { waiting: ['warning', '!', 'Waiting for a decision'], review: ['info', '…', 'In review'], changes: ['warning', '↩', 'Changes requested'], rejected: ['error', '✕', 'Rejected'] };
    const OUTC = { approved: ['success', '✓', 'Passed'], conditions: ['success', '✓', 'Passed with conditions'] };
    const DOC = { todo: ['neutral', '○', 'To do'], chat: ['info', '…', 'Drafting in chat'], working: ['info', '✎', 'Working document'], pr: ['warning', '!', 'Validated, PR open'], reviewed: ['success', '✓', 'Reviewed'], published: ['success', '✓', 'Published'] };
    const all = LAB.changes.concat(L.created || []);

    // ---- one change, as every variant shows it
    const cv = c => {
      const en = entryOf(c.entry), o = ORI[c.origin.kind], first = Math.min(en.phase, c.cur);
      const gchip = c.gate ? chip(GATE, c.gate.state, c.gate.id + ' · ' + GATE[c.gate.state][2].toLowerCase()) : c.last ? chip(OUTC, c.last.outcome, c.last.id + (c.last.outcome === 'conditions' ? ' passed with conditions' : ' passed')) : nochip;
      const strip = P.map((ph, i) => { const state = i < first ? 'skipped' : i < c.cur ? 'done' : i === c.cur ? 'current' : 'todo', isPend = !!(c.gate && ph.gate && ph.gate.id === c.gate.id);
        const gst = ph.gate ? (isPend ? (c.gate.state === 'changes' || c.gate.state === 'rejected' ? 'blocked' : 'attention') : i < first ? 'skipped' : i < c.cur ? 'passed' : 'todo') : '';
        return { n: ph.n, title: ph.title, togaf: togaf(i), state, cls: 'ph-' + state, entered: i === first && first > 0, hasGate: !!ph.gate, noGate: !ph.gate, gate: ph.gate ? ph.gate.id : '', gateCls: 'gt-' + gst, gateTitle: ph.gate ? ph.gate.id + ' · ' + ph.gate.title + (isPend ? ' · ' + GATE[c.gate.state][2].toLowerCase() : gst === 'passed' ? ' · passed' : gst === 'skipped' ? ' · not needed' : '') : '', label: ph.title + ' · ' + state }; });
      return { id: c.id, title: c.title, pf: c.pf, klass: c.klass, klassCls: 'kl-' + c.klass, oG: o.g, oName: o.name, oCls: 'og-' + c.origin.kind, oRef: c.origin.ref, oBy: c.origin.by, oAt: c.origin.at, oText: c.origin.text,
        entry: en.name, enters: en.enters, phase: phTitle(c.cur), togaf: togaf(c.cur), now: c.now, next: c.next, gchip, hasGchip: gchip.cls !== 'none',
        cardCls: (c.closed ? 'k-closed' : c.gate ? (c.gate.state === 'changes' || c.gate.state === 'rejected' ? 'k-blocked' : 'k-attention') : '') + (c.isNew ? ' k-new' : ''),
        strip, deliveredCls: c.cur >= 6 ? 'ph-done' : 'ph-todo', deliveredState: c.cur >= 6 ? 'done' : 'todo', open: upd({ sel: c.id, formOpen: false, asst: null }) };
    };
    const rows = all.map(cv), byId = {}; rows.forEach((r, i) => { byId[r.id] = r; r._c = all[i]; });

    // ---- what a new change gets, from its entry point and class
    const propose = (entryId, klass) => {
      const en = entryOf(entryId), k = Math.min(en.phase, 6), light = entryId === 'small-tweak' || entryId === 'post-delivery', ga = light ? null : gateAfter(k);
      const by = !ga ? (entryId === 'small-tweak' ? 'CODEOWNERS approve the pull request' : 'The portfolio architect accepts the baseline update') : (ga.g.id === 'G2' && klass !== 're-architecting') ? 'Portfolio architect · no board for this class' : LAB.phases[ga.k].gateBy;
      return { k, entry: en.name, enters: k >= 6 ? 'After delivery' : P[k].title, togaf: togaf(k), skips: k > 0 ? 'skips ' + P.slice(0, Math.min(k, 6)).map(p => p.title).join(', ') : 'full cycle, every gate', what: en.what, docs: LAB.phases[k].docs.join(' · '), gate: ga ? ga.g.id + ' · ' + ga.g.title : 'No gate', gateBy: by };
    };
    const create = (x) => () => {
      const cur = self.state.lab || {}, list = (cur.created || []), p = propose(x.entry, x.klass), id = 'n-' + (list.length + 1);
      const c = { id, title: x.title || 'New change', pf: x.pf, klass: x.klass, origin: { kind: x.kind, ref: x.ref, by: x.by, at: x.at, text: x.text }, entry: x.entry, cur: p.k,
        now: 'Just opened · ' + LAB.phases[p.k].docs[0] + ' to draft in the assistant', next: 'Change owner · draft the ' + LAB.phases[p.k].docs[0], docs: LAB.phases[p.k].docs.map(n => ({ name: n, state: 'todo' })), gate: null, last: null, crit: [], closed: false, deliv: '', isNew: true };
      const done = Object.assign({}, cur.sigDone); if (x.sig) done[x.sig] = 'Opened as a change';
      self.setState({ lab: Object.assign({}, cur, { created: list.concat([c]), sel: id, formOpen: false, asst: null, sigDone: done }) });
    };

    // ---- the lab bar
    const SN = { A: ['A · A form in three questions', 'New change opens a short form: where it comes from, what kind of change, which scope. The entry phase, the gates and the documents are computed and shown before creating.', 'Explicit and teachable; the person must know the origin and the kind.'],
      B: ['B · In the assistant', 'New change opens the assistant pane. You say what happened in your words; the assistant recognises the origin, proposes the entry phase, class and scope, shows the overlaps, and creates the change when you confirm.', 'No vocabulary to learn, same pane as document drafting; the proposal must be right, and it stays editable.'],
      C: ['C · From the signal', 'No form first: tickets, pull requests, radar moves, findings, decisions and incidents that are not a change yet arrive in Incoming, each with a suggested entry. You open a change, attach the signal to an existing one, or dismiss it.', 'Nothing starts outside the process and the origin is never retyped; needs the connectors (ticketing, Git, radar, incidents).'] };
    const FN = { A: ['A · Board by phase', 'One column per phase with its TOGAF letter and the gate that follows; each change is a card in the column of its current phase, tinted when it waits at a gate or was sent back.', 'Shows the load per phase and where things queue; wide, and a card says little.'],
      B: ['B · Tracks', 'One row per change with its own track: phases skipped, done, current, and the gates passed or pending. Grouped by portfolio.', 'Shows where each change entered and what it skipped; best for owners; the load per phase is less visible.'],
      C: ['C · By gate', 'The four gates as sections: who decides, what waits for a decision, what was sent back, what passed recently. Changes between two gates are counted under each section.', 'Made for those who decide (architects, board, tech leads); the work between gates is only a count.'],
      D: ['D · ADM phases', 'The TOGAF phases as a strip (A, B·C·D baseline, B·C·D target, E, F, G, H) with the number of changes in each. Selecting a phase shows what it produces, its gate and criteria, and its changes.', 'Speaks TOGAF and explains the method while showing the work; one phase at a time.'] };
    const out = { vsA: SV === 'A', vsB: SV === 'B', vsC: SV === 'C', vfA: FV === 'A', vfB: FV === 'B', vfC: FV === 'C', vfD: FV === 'D',
      startVariants: ['A', 'B', 'C'].map(v => ({ label: SN[v][0], on: SV === v, cls: SV === v ? 'chip-on' : '', pick: upd({ start: v, formOpen: false, asst: null, sel: null }) })),
      followVariants: ['A', 'B', 'C', 'D'].map(v => ({ label: FN[v][0], on: FV === v, cls: FV === v ? 'chip-on' : '', pick: upd({ follow: v, sel: null }) })),
      startTitle: 'Start · ' + SN[SV][0], startText: SN[SV][1], startDelta: SN[SV][2], followTitle: 'Follow · ' + FN[FV][0], followText: FN[FV][1], followDelta: FN[FV][2] };

    // ---- page state
    const selC = L.sel ? all.find(c => c.id === L.sel) : null, asstOpen = SV === 'B' && !!L.asst;
    out.isList = !selC; out.isDetail = !!selC; out.asstOpen = asstOpen; out.paneCls = asstOpen ? 'with-pane' : '';
    out.count = all.filter(c => !c.closed && c.cur < 6).length + ' in progress · ' + all.filter(c => c.gate && !c.closed && (c.gate.state === 'waiting' || c.gate.state === 'review')).length + ' waiting at a gate';
    out.hasNewBtn = SV !== 'C'; out.newChange = SV === 'A' ? upd({ formOpen: !L.formOpen, sel: null }) : upd({ asst: { step: 0 }, sel: null }); out.newLabel = SV === 'B' ? 'New change · ask the assistant' : 'New change';
    out.backToList = upd({ sel: null });

    // ---- start A · form
    const F = Object.assign({ origin: 'ticket', klass: 'incremental', pf: 'Retail', title: '' }, L.form || {}), fEntry = F.entry || ORI[F.origin].entry, fp = propose(fEntry, F.klass);
    const setF = o => upd({ form: Object.assign({}, F, o) });
    out.formOpen = SV === 'A' && !!L.formOpen && !selC;
    out.fOrigins = LAB.origins.map(o => ({ g: o.g, cls: 'og-' + o.id, name: o.name, sub: o.sub, on: F.origin === o.id, pcls: F.origin === o.id ? 'pick-on' : '', pick: setF({ origin: o.id, entry: null }) }));
    out.fEntries = E.map(e => ({ name: e.name, sub: (e.enters.indexOf('after') === 0 ? 'enters ' : 'enters at ') + e.enters, on: fEntry === e.id, pcls: fEntry === e.id ? 'pick-on' : '', pick: setF({ entry: e.id }) }));
    out.fClasses = ['simplification', 'incremental', 're-architecting'].map(k => ({ label: k.charAt(0).toUpperCase() + k.slice(1), on: F.klass === k, cls: F.klass === k ? 'chip-on' : '', pick: setF({ klass: k }) }));
    out.fPfs = ['Corporate', 'Retail', 'Payments', 'Risk'].map(k => ({ label: k, on: F.pf === k, cls: F.pf === k ? 'chip-on' : '', pick: setF({ pf: k }) }));
    out.fTitle = F.title; out.onFTitle = e => { const v = e.target.value; self.setState({ lab: Object.assign({}, self.state.lab, { form: Object.assign({}, F, { title: v }) }) }); };
    out.fp = fp; out.fSuggested = ORI[F.origin].entry === fEntry ? 'suggested from the origin' : 'changed by you';
    out.fCreate = create({ title: F.title || 'New change from ' + ORI[F.origin].name.toLowerCase(), pf: F.pf, klass: F.klass, kind: F.origin, ref: ORI[F.origin].name, by: 'You', at: 'today', text: 'Opened from the form.', entry: fEntry });
    out.fCancel = upd({ formOpen: false });

    // ---- signals (start B and C)
    const sv = g => { const o = ORI[g.kind], p = propose(g.entry, g.klass), done = (L.sigDone || {})[g.id], at = g.attach ? byId[g.attach] : null;
      return { id: g.id, g: o.g, cls: 'og-' + g.kind, oName: o.name, ref: g.ref, by: g.by, at: g.at, title: g.title, text: g.text, pf: g.pf, scope: g.scope, klass: g.klass, klassCls: 'kl-' + g.klass, p,
        suggestion: p.entry + ' · enters at ' + p.enters + ' (TOGAF ' + p.togaf + ') · ' + p.skips, hasOverlap: !!g.overlap, overlap: g.overlap, hasAttach: !!at && !done, attachLabel: at ? 'Attach to ' + at.title : '',
        done: !!done, open0: !done, doneText: done || '', rowCls: done ? 'sig-done' : '',
        create: create({ title: g.title, pf: g.pf, klass: g.klass, kind: g.kind, ref: g.ref, by: g.by, at: g.at, text: g.text, entry: g.entry, sig: g.id }),
        attach: () => { const cur = self.state.lab || {}; self.setState({ lab: Object.assign({}, cur, { sigDone: Object.assign({}, cur.sigDone, { [g.id]: 'Attached to ' + (at ? at.title : '') }), asst: null }) }); },
        dismiss: () => { const cur = self.state.lab || {}; self.setState({ lab: Object.assign({}, cur, { sigDone: Object.assign({}, cur.sigDone, { [g.id]: 'Dismissed · no architecture impact' }) }) }); } }; };
    const sigs = LAB.signals.map(sv);
    out.showIncoming = SV === 'C' && !selC; out.signals = sigs; out.sigCount = sigs.filter(x => !x.done).length + ' to triage';

    // ---- start B · assistant pane
    const A = L.asst || {}, PROMPTS = [['s-freeze', 'Customers want to freeze a card themselves from the mobile app.'], ['s-adr34', 'ADR-034 was accepted: event contracts move to AsyncAPI 3. What changes?'], ['s-pr412', 'PR #412 changed web-banking and there is no ticket.']];
    const asel = A.sig ? sigs.find(x => x.id === A.sig) : null;
    out.aStep0 = asstOpen && !asel; out.aStep1 = asstOpen && !!asel && !asel.done; out.aStep2 = asstOpen && !!asel && asel.done;
    out.aPrompts = PROMPTS.map(p => ({ text: p[1], pick: upd({ asst: { step: 1, sig: p[0] } }) }));
    out.aQ = asel ? PROMPTS.find(p => p[0] === asel.id)[1] : ''; out.aSig = asel || { p: {} };
    out.aAnswer = asel ? ({ ticket: 'This is a new need from a business request. It starts at Vision and passes every gate.', adr: 'This comes from a decision. It does not go back to Vision: it enters at Gap analysis, on the interfaces the decision changes.', pr: 'The code changed first. For a change this small, the Definition of Ready is enough: no board, the tech lead approves.' })[asel.kind] || '' : '';
    out.aClose = upd({ asst: null }); out.aRestart = upd({ asst: { step: 0 } }); out.aToForm = upd({ start: 'A', formOpen: true, asst: null });

    // ---- follow A · board
    out.kanban = P.map((ph, i) => ({ title: ph.title, n: ph.n, togaf: togaf(i), gate: ph.gate ? 'then ' + ph.gate.id + ' · ' + ph.gate.title : 'no gate', cards: rows.filter(r => r._c.cur === i) }))
      .concat([{ title: 'Delivered', n: '', togaf: 'H', gate: 'the plateau is the new baseline', cards: rows.filter(r => r._c.cur >= 6) }]).map(k => Object.assign(k, { count: k.cards.length }));

    // ---- follow B · tracks
    out.tracks = ['Corporate', 'Retail', 'Payments', 'Risk'].map(pf => ({ pf, rows: rows.filter(r => r.pf === pf), count: rows.filter(r => r.pf === pf).length })).filter(g => g.count);

    // ---- follow C · gates
    out.gates = P.map((ph, i) => ({ ph, i })).filter(x => x.ph.gate).map(x => { const g = x.ph.gate, at = rows.filter(r => r._c.gate && r._c.gate.id === g.id);
      const wait = at.filter(r => r._c.gate.state === 'waiting' || r._c.gate.state === 'review'), back = at.filter(r => r._c.gate.state === 'changes' || r._c.gate.state === 'rejected'), passed = rows.filter(r => r._c.last && r._c.last.id === g.id);
      const before = rows.filter(r => !r._c.gate && r._c.cur <= x.i && (gateAfter(r._c.cur) || {}).k === x.i && r._c.entry !== 'small-tweak');
      const withNote = (r, note) => Object.assign({}, r, { gnote: note });
      return { id: g.id, title: g.title, by: LAB.phases[x.i].gateBy, after: 'after ' + x.ph.title + ' · TOGAF ' + togaf(x.i), criteria: g.criteria.join(' · '),
        wait: wait.map(r => withNote(r, r._c.gate.note)), hasWait: !!wait.length, noWait: !wait.length, back: back.map(r => withNote(r, r._c.gate.note)), hasBack: !!back.length, noBack: !back.length,
        passed: passed.map(r => withNote(r, r._c.last.at + ' · ' + r._c.last.by + (r._c.last.note ? ' · ' + r._c.last.note : ''))), hasPassed: !!passed.length, noPassed: !passed.length,
        before: before.length ? before.length + (before.length > 1 ? ' changes are' : ' change is') + ' on the way to ' + g.id + ': ' + before.map(r => r.title + ' (' + r.phase + ')').join(' · ') : 'Nothing on the way to ' + g.id }; });
    const nog = rows.filter(r => r._c.entry === 'small-tweak' || r._c.entry === 'post-delivery');
    out.noGate = nog; out.hasNoGate = !!nog.length;

    // ---- follow D · ADM
    const ap = L.adm === undefined ? 2 : L.adm;
    out.adm = P.map((ph, i) => ({ i, title: ph.title, sub: ph.sub })).concat([{ i: 6, title: 'Delivered', sub: 'new baseline, change management' }]).map(x => { const n = rows.filter(r => Math.min(r._c.cur, 6) === x.i).length; return { togaf: togaf(x.i), title: x.title, sub: x.sub, n, on: ap === x.i, cls: (ap === x.i ? 'adm-on' : '') + (n ? '' : ' adm-empty'), pick: upd({ adm: x.i }) }; });
    const aph = ap < 6 ? P[ap] : null, ag = aph && aph.gate;
    out.admSel = { title: ap < 6 ? aph.title : 'Delivered', togafName: LAB.phases[ap].togafName, deliverable: ap < 6 ? aph.deliverable : HOW.after.text, who: ap < 6 ? aph.who : 'The portfolio architect promotes the plateau; off-plan changes are reconciled here.', docs: LAB.phases[ap].docs.join(' · '),
      hasGate: !!ag, noGate: !ag, gate: ag ? ag.id + ' · ' + ag.title : '', gateBy: LAB.phases[ap].gateBy, crit: ag ? ag.criteria.map(t => ({ text: t })) : [], noGateText: ap >= 6 ? 'No gate: the baseline is updated, the next change starts from it.' : 'No gate after this phase: the work continues into ' + phTitle(ap + 1) + '.',
      rows: rows.filter(r => Math.min(r._c.cur, 6) === ap), hasRows: rows.some(r => Math.min(r._c.cur, 6) === ap), noRows: !rows.some(r => Math.min(r._c.cur, 6) === ap) };

    // ---- detail
    if (selC) {
      const v = byId[selC.id], en = entryOf(selC.entry), light = selC.entry === 'small-tweak' || selC.entry === 'post-delivery';
      const pg = selC.gate ? P.findIndex(ph => ph.gate && ph.gate.id === selC.gate.id) : (light || selC.cur >= 6 ? -1 : (gateAfter(selC.cur) || { k: -1 }).k), g = pg >= 0 ? P[pg].gate : null;
      out.d = Object.assign({}, v, { togafName: LAB.phases[Math.min(selC.cur, 6)].togafName, what: en.what, deliverable: selC.cur < 6 ? P[selC.cur].deliverable : HOW.after.text,
        docs: selC.docs.map(x => ({ name: x.name, chip: chip(DOC, x.state) })), hasDocs: !!selC.docs.length,
        hasG: !!g, noG: !g, gTitle: g ? g.id + ' · ' + g.title : '', gBy: selC.gate ? selC.gate.by : g ? ((g.id === 'G2' && selC.klass !== 're-architecting') ? 'Portfolio architect · no board for this class' : LAB.phases[pg].gateBy) : '', gNote: selC.gate ? selC.gate.note : 'Not asked yet',
        gChip: selC.gate ? chip(GATE, selC.gate.state) : chip({ n: ['neutral', '○', 'Next gate'] }, 'n'), crit: g ? g.criteria.map((t, i) => { const ok = !!(selC.gate && selC.crit[i]); return { text: t, g: ok ? '✓' : '○', cls: ok ? 'c-ok' : '', state: ok ? 'met' : 'not met yet' }; }) : [],
        noGText: selC.cur >= 6 && !light ? 'Every gate passed. The plateau is the new baseline.' : en.what, hasLast: !!selC.last, lastLine: selC.last ? selC.last.id + (selC.last.outcome === 'conditions' ? ' passed with conditions' : ' passed') + ' on ' + selC.last.at + ' · ' + selC.last.by + (selC.last.note ? ' · ' + selC.last.note : '') : '',
        hasDeliv: !!selC.deliv, deliv: selC.deliv, draft: () => self.toast('In the product this opens the assistant pane on the document (see the Architecture board)') });
    } else out.d = { strip: [], docs: [], crit: [], gChip: nochip, gchip: nochip };
    return out;
  }
"""

OG = lambda p: '<span class="og {{' + p + '.oCls}}" aria-hidden="true">{{' + p + '.oG}}</span>'
ORIGIN_LINE = lambda p: '<span class="orow">' + OG(p) + '<span><b>{{' + p + '.oName}}</b> · {{' + p + '.oRef}}</span></span>'
KCARD = ('<button type="button" class="kcard {{c.cardCls}}" onClick="{{c.open}}"><b>{{c.title}}</b>' + ORIGIN_LINE('c')
         + '<span class="meta">{{c.pf}} · {{c.entry}}</span>' + sif('c.hasGchip', chip('c.gchip', 'sm')) + '<span class="meta">{{c.now}}</span></button>')
MINI = ('<span class="trk2" role="img" aria-label="Phases">' + sfor('r.strip', 'f', '<span class="d {{f.cls}}" title="{{f.label}}">{{f.n}}</span>' + sif('f.hasGate', '<span class="gt {{f.gateCls}}" title="{{f.gateTitle}}"><i>{{f.gate}}</i></span>') + sif('f.noGate', '<span class="l"></span>'), 6) + '<span class="d {{r.deliveredCls}}" title="Delivered · {{r.deliveredState}}">✓</span></span>')
GROW = lambda lst: sfor(lst, 'c', '<button type="button" class="kcard {{c.cardCls}}" onClick="{{c.open}}"><b>{{c.title}}</b>' + ORIGIN_LINE('c') + '<span class="meta">{{c.gnote}}</span></button>', 2)

LABBAR = ('<div class="labbar" role="group" aria-label="Lab"><span class="simlab">START A CHANGE · PICK ONE</span>'
          + sfor('startVariants', 'v', '<button type="button" class="chip {{v.cls}}" aria-pressed="{{v.on}}" onClick="{{v.pick}}">{{v.label}}</button>', 3)
          + '<span class="sep"></span><span class="simlab">FOLLOW THE PHASES · PICK ONE</span>'
          + sfor('followVariants', 'v', '<button type="button" class="chip {{v.cls}}" aria-pressed="{{v.on}}" onClick="{{v.pick}}">{{v.label}}</button>', 4) + '</div>'
          '<div class="labnote"><div><b>{{startTitle}}</b><span>{{startText}}</span><span class="meta">{{startDelta}}</span></div><div><b>{{followTitle}}</b><span>{{followText}}</span><span class="meta">{{followDelta}}</span></div></div>')

RESULT = lambda p: ('<div class="result"><span class="dli"><span class="lbl">Enters at</span><b>{{' + p + '.enters}} <span class="tg">TOGAF {{' + p + '.togaf}}</span></b><span class="s">{{' + p + '.skips}}</span></span>'
                    '<span class="dli"><span class="lbl">Documents to draft first</span><b>{{' + p + '.docs}}</b><span class="s">drafted in the assistant, validated by you</span></span>'
                    '<span class="dli"><span class="lbl">Next gate</span><b>{{' + p + '.gate}}</b><span class="s">{{' + p + '.gateBy}}</span></span>'
                    '<span class="dli"><span class="lbl">What it means</span><b style="font-weight: 500">{{' + p + '.what}}</b></span></div>')

FORM = sif('formOpen', '<section class="startc" aria-label="New change"><h3 class="h3">New change</h3>'
  '<span class="lbl">1 · Where does it come from?</span><div class="picks" role="radiogroup" aria-label="Origin">' + sfor('fOrigins', 'o', '<button type="button" role="radio" aria-checked="{{o.on}}" class="pick {{o.pcls}}" onClick="{{o.pick}}"><span class="og {{o.cls}}" aria-hidden="true">{{o.g}}</span><span class="p2"><b>{{o.name}}</b><span>{{o.sub}}</span></span></button>', 8) + '</div>'
  '<span class="lbl">2 · What kind of change? <span style="text-transform: none; letter-spacing: 0; font-weight: 400">· {{fSuggested}}</span></span><div class="picks" role="radiogroup" aria-label="Kind of change">' + sfor('fEntries', 'e', '<button type="button" role="radio" aria-checked="{{e.on}}" class="pick {{e.pcls}}" onClick="{{e.pick}}"><span class="p2"><b>{{e.name}}</b><span>{{e.sub}}</span></span></button>', 6) + '</div>'
  '<span class="lbl">3 · Scope</span><div class="fld"><label for="f-title">Title</label><input id="f-title" type="text" placeholder="What changes, in a few words" value="{{fTitle}}" onChange="{{onFTitle}}"></div>'
  '<div style="display: flex; gap: 8px 16px; flex-wrap: wrap; align-items: center"><span class="meta">Portfolio</span>' + sfor('fPfs', 'p', '<button type="button" class="chip {{p.cls}}" aria-pressed="{{p.on}}" onClick="{{p.pick}}">{{p.label}}</button>', 4)
  + '<span class="meta" style="margin-left: 8px">Class</span>' + sfor('fClasses', 'k', '<button type="button" class="chip {{k.cls}}" aria-pressed="{{k.on}}" onClick="{{k.pick}}">{{k.label}}</button>', 3) + '</div>'
  + RESULT('fp') + '<div style="display: flex; gap: 8px; justify-content: flex-end"><button type="button" class="btn t" onClick="{{fCancel}}">Cancel</button><button type="button" class="btn f" onClick="{{fCreate}}">Create the change</button></div></section>')

INCOMING = sif('showIncoming', '<section class="tgrp" aria-label="Incoming"><div class="tg-h">Incoming · not a change yet<span style="margin-left: auto">{{sigCount}}</span></div>'
  + sfor('signals', 'g', '<div class="sigrow {{g.rowCls}}"><span class="og {{g.cls}}" aria-hidden="true">{{g.g}}</span><span class="s1"><b>{{g.title}}</b><span class="meta"><b style="color: #1C1B1E">{{g.oName}}</b> · {{g.ref}} · {{g.by}} · {{g.at}}</span><span style="font-size: 13px">{{g.text}}</span>'
    '<span class="meta">Suggested: {{g.suggestion}}' + sif('g.hasOverlap', ' · {{g.overlap}}') + '</span></span>'
    + sif('g.open0', '<span class="s2"><button type="button" class="btn f sm" onClick="{{g.create}}">Open as a change</button>' + sif('g.hasAttach', '<button type="button" class="btn o sm" onClick="{{g.attach}}">{{g.attachLabel}}</button>') + '<button type="button" class="btn t sm" onClick="{{g.dismiss}}">Dismiss</button></span>')
    + sif('g.done', '<span class="s2"><span class="st st-neutral"><span class="tile" aria-hidden="true">✓</span>{{g.doneText}}</span></span>') + '</div>', 6) + '</section>')

BOARD = sif('vfA', '<div class="kan">' + sfor('kanban', 'k', '<div class="kcol"><div class="kh"><span class="k1"><span class="tg">{{k.togaf}}</span>{{k.n}} {{k.title}}<span class="n">{{k.count}}</span></span><span class="k2">{{k.gate}}</span></div>' + sfor('k.cards', 'c', KCARD, 3) + '</div>', 7) + '</div>')
LEGEND = ('<div class="tlegend"><span class="trk2"><span class="d ph-done">1</span></span>done<span class="trk2"><span class="d ph-current">2</span></span>current<span class="trk2"><span class="d ph-skipped">0</span></span>skipped: the change entered later'
          '<span class="gt gt-passed" style="margin: 0"><i>G</i></span>gate passed<span class="gt gt-attention" style="margin: 0"><i>G</i></span>waiting<span class="gt gt-blocked" style="margin: 0"><i>G</i></span>sent back</div>')
TRACKS = sif('vfB', LEGEND + sfor('tracks', 'g', '<div class="tgrp"><div class="tg-h">{{g.pf}}<span style="margin-left: auto">{{g.count}}</span></div>'
  + sfor('g.rows', 'r', '<button type="button" class="trow" onClick="{{r.open}}"><span class="t1"><b>{{r.title}}</b>' + ORIGIN_LINE('r') + '</span>' + MINI
    + '<span class="t3"><span class="tg">TOGAF {{r.togaf}}</span> <b style="font: 600 13px Manrope, sans-serif">{{r.phase}}</b> <span class="meta">· {{r.now}}</span></span><span class="t4">' + sif('r.hasGchip', chip('r.gchip', 'sm')) + '</span></button>', 4) + '</div>', 4))
GATES = sif('vfC', sfor('gates', 'g', '<section class="gsec"><div class="gsec-h"><span class="gt gt-passed"><i>{{g.id}}</i></span><b>{{g.title}}</b><span class="meta">{{g.after}} · decided by {{g.by}}</span></div>'
  '<div class="between">Criteria: {{g.criteria}}</div>'
  '<div class="gsec-b"><div class="gcol"><span class="lbl">Waiting for a decision</span>' + sif('g.hasWait', GROW('g.wait')) + sif('g.noWait', '<span class="none">Nothing waiting</span>') + '</div>'
  '<div class="gcol"><span class="lbl">Sent back or rejected</span>' + sif('g.hasBack', GROW('g.back')) + sif('g.noBack', '<span class="none">None</span>') + '</div>'
  '<div class="gcol"><span class="lbl">Passed recently</span>' + sif('g.hasPassed', GROW('g.passed')) + sif('g.noPassed', '<span class="none">None</span>') + '</div></div>'
  '<div class="between" style="padding-bottom: 10px">{{g.before}}</div></section>', 4)
  + sif('hasNoGate', '<section class="gsec"><div class="gsec-h"><b>No gate needed</b><span class="meta">small tweaks (Definition of Ready, CODEOWNERS approve) and post-delivery updates (reconciliation)</span></div><div class="gsec-b">' + sfor('noGate', 'c', '<div class="gcol">' + KCARD + '</div>', 2) + '</div></section>'))
ADM = sif('vfD', '<div class="admrow" role="tablist" aria-label="TOGAF phases">' + sfor('adm', 'a', '<button type="button" role="tab" aria-selected="{{a.on}}" class="adm {{a.cls}}" onClick="{{a.pick}}"><span class="a1"><span class="tg">{{a.togaf}}</span><span class="n">{{a.n}}</span></span><b>{{a.title}}</b><span class="s">{{a.sub}}</span></button>', 7) + '</div>'
  '<div class="admd"><div class="cardx"><span class="lbl">{{admSel.title}} · {{admSel.togafName}}</span><span style="font-size: 14px; line-height: 20px">{{admSel.deliverable}}</span><span class="meta">Documents: {{admSel.docs}}</span><span class="meta">{{admSel.who}}</span>'
  + sif('admSel.hasGate', '<span class="lbl" style="margin-top: 6px">Gate after it · {{admSel.gate}}</span><span class="meta">Decided by {{admSel.gateBy}}</span>' + sfor('admSel.crit', 'k', '<span class="crit"><i aria-hidden="true">○</i>{{k.text}}</span>', 3))
  + sif('admSel.noGate', '<span class="meta" style="margin-top: 6px">{{admSel.noGateText}}</span>') + '</div>'
  '<div style="display: flex; flex-direction: column; gap: 8px"><span class="lbl">Changes in this phase</span>' + sif('admSel.hasRows', sfor('admSel.rows', 'c', KCARD, 3)) + sif('admSel.noRows', '<span class="meta">No change in this phase today.</span>') + '</div></div>')

DETAIL = sif('isDetail', '<div class="lhead"><button type="button" class="chip" onClick="{{backToList}}">‹ All changes</button><h2 class="h2">{{d.title}}</h2><span class="kl {{d.klassCls}}">{{d.klass}}</span>' + sif('d.hasGchip', chip('d.gchip')) + '</div>'
  '<div class="flow">' + sfor('d.strip', 'f', '<div class="ph {{f.cls}}" title="{{f.label}}"><span class="pn">{{f.n}}</span><span class="tgf">TOGAF {{f.togaf}}</span><b>{{f.title}}</b><span>{{f.state}}</span>' + sif('f.entered', '<span class="ent">enters here</span>') + '</div>' + sif('f.hasGate', '<span class="gt {{f.gateCls}}" title="{{f.gateTitle}}"><i>{{f.gate}}</i></span>') + sif('f.noGate', '<span class="nx"></span>'), 6) + '<div class="ph {{d.deliveredCls}}"><span class="tgf">TOGAF H</span><b>Delivered</b><span>new baseline</span></div></div>'
  '<div class="dgrid">'
  '<div class="cardx"><span class="lbl">Where it comes from</span><span class="orow" style="font-size: 14px">' + OG('d') + '<span><b>{{d.oName}}</b> · {{d.oRef}}</span></span><span style="font-size: 14px; line-height: 20px">{{d.oText}}</span><span class="meta">{{d.oBy}} · {{d.oAt}}</span>'
  '<span class="lbl" style="margin-top: 6px">Entered as {{d.entry}} · {{d.enters}}</span><span class="meta">{{d.what}}</span></div>'
  '<div class="cardx"><span class="lbl">Now · {{d.phase}} <span class="tg">{{d.togafName}}</span></span><span style="font-size: 14px; line-height: 20px">{{d.now}}</span>'
  + sif('d.hasDocs', '<div class="rows">' + sfor('d.docs', 'x', '<button type="button" class="row" onClick="{{d.draft}}"><span class="txt"><b>{{x.name}}</b></span>' + chip('x.chip', 'sm') + '</button>', 3) + '</div>')
  + '<span class="meta">Next: {{d.next}}</span>' + sif('d.hasDeliv', '<span class="meta">Delivery: {{d.deliv}}</span>') + '</div>'
  + sif('d.hasG', '<div class="cardx" style="grid-column: 1 / -1"><span class="lbl">Gate · {{d.gTitle}}' + chip('d.gChip', 'sm') + '</span><span style="font-size: 14px; line-height: 20px">{{d.gNote}}</span><span class="meta">Decided by {{d.gBy}}</span>'
    + sfor('d.crit', 'k', '<span class="crit {{k.cls}}"><i aria-hidden="true">{{k.g}}</i><span>{{k.text}} <span class="meta">· {{k.state}}</span></span></span>', 3) + sif('d.hasLast', '<span class="meta">Before: {{d.lastLine}}</span>') + '</div>')
  + sif('d.noG', '<div class="cardx" style="grid-column: 1 / -1"><span class="lbl">Gate</span><span style="font-size: 14px; line-height: 20px">{{d.noGText}}</span>' + sif('d.hasLast', '<span class="meta">{{d.lastLine}}</span>') + '</div>')
  + '</div>')

PROP = ('<div class="aprop"><b style="font: 600 14px/20px Manrope, sans-serif">{{aSig.title}}</b><dl><dt>Origin</dt><dd>{{aSig.oName}} · {{aSig.ref}}</dd><dt>Enters at</dt><dd>{{aSig.p.enters}} <span class="tg">TOGAF {{aSig.p.togaf}}</span> · {{aSig.p.skips}}</dd><dt>Class</dt><dd>{{aSig.klass}}</dd><dt>Scope</dt><dd>{{aSig.pf}} · {{aSig.scope}}</dd>'
        '<dt>First</dt><dd>{{aSig.p.docs}}</dd><dt>Next gate</dt><dd>{{aSig.p.gate}} · {{aSig.p.gateBy}}</dd></dl>' + sif('aSig.hasOverlap', '<span class="st st-warning" style="white-space: normal; height: auto; padding: 4px 10px 4px 5px"><span class="tile" aria-hidden="true">!</span>{{aSig.overlap}}</span>')
        + '<div style="display: flex; gap: 6px; flex-wrap: wrap"><button type="button" class="btn f sm" onClick="{{aSig.create}}">Create the change</button>' + sif('aSig.hasAttach', '<button type="button" class="btn o sm" onClick="{{aSig.attach}}">{{aSig.attachLabel}}</button>') + '<button type="button" class="btn t sm" onClick="{{aToForm}}">Adjust in the form</button></div></div>')
PANE = sif('asstOpen', '<aside class="apane" aria-label="Assistant"><div class="apane-h"><b>Assistant</b><button type="button" class="btn t sm" onClick="{{aRestart}}">New</button><button type="button" class="btn t sm" onClick="{{aClose}}" aria-label="Close the assistant">Close</button></div><div class="apane-b">'
  + sif('aStep0', '<span class="aa">Tell me what happened, in your words. I will find where it enters the process.</span><div class="asug"><span class="lbl">Examples</span>' + sfor('aPrompts', 'p', '<button type="button" class="pick" onClick="{{p.pick}}"><span class="p2"><b style="font-weight: 500">{{p.text}}</b></span></button>', 3) + '</div>')
  + sif('aStep1', '<span class="aq">{{aQ}}</span><span class="aa">{{aAnswer}}</span>' + PROP)
  + sif('aStep2', '<span class="aq">{{aQ}}</span><span class="aa">Done: {{aSig.doneText}}.</span>')
  + '</div><div class="apane-f">The same pane drafts the documents of each phase.</div></aside>')

AREA = ('<div class="lm"><div class="lm-c {{paneCls}}">'
        + sif('isList', '<div class="lhead"><h2 class="h2">Changes</h2><span class="meta">{{count}}</span>' + sif('hasNewBtn', '<button type="button" class="btn f" onClick="{{newChange}}">{{newLabel}}</button>') + '</div>' + FORM + INCOMING + BOARD + TRACKS + GATES + ADM)
        + DETAIL + '</div>' + PANE + '</div>')

logic = B.logic
logic = logic.replace("const DELIV = ", "const LAB = " + json.dumps(startlab_data.LAB, ensure_ascii=False, separators=(',', ':')) + ";\nconst DELIV = ", 1)
assert 'const LAB = ' in logic
logic = logic.replace("decisions: {}, note: '', toast: null, pfFilter: 'all',", "decisions: {}, note: '', toast: null, pfFilter: 'all', lab: { start: 'A', follow: 'A' },")
assert "lab: { start: 'A'" in logic
RV = "  renderVals() {\n    return Object.assign({}, this.simVals(), this.shellVals(), this.viewVals(), this.catVals(), this.pageVals(), this.procVals(), this.arbVals(), this.changeVals(), this.docVals(), this.proposalVals());\n  }"
assert RV in logic
logic = logic.replace(RV, LAB_JS + "  renderVals() {\n    return Object.assign({}, this.simVals(), this.shellVals(), this.startLabVals());\n  }")
assert '</script' not in logic

title = 'Change start lab'
body = ('<div style="display: flex; flex-direction: column; gap: 12px; padding: 12px; background: #ECE5F4; min-height: 100vh; box-sizing: border-box; font-family: \'Open Sans\', system-ui, sans-serif">'
        + LABBAR + S.sim_bar('') + S.sim_open('sim-host-arch')
        + '<div class="app" style="min-height: {{simFrameH}}px">' + HEADER + '<div class="bodyrow">' + RAIL + '<main>' + AREA + '</main></div>' + NAVBAR + TOAST + '</div>' + S.SIM_CLOSE + '</div>')
assert '</script' not in body
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
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1440,"height":1500}}}}'>
{logic}
</script>
</body>
</html>
'''
n_if = page.count('<sc-if'); assert n_if == page.count('</sc-if>'), (n_if, page.count('</sc-if>'))
assert page.count('<sc-for') == page.count('</sc-for>')
open(OUT, 'w', encoding='utf-8').write(page)
print('built', OUT, len(page.encode('utf-8')))
