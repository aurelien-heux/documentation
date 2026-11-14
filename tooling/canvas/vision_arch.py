"""The Architecture board inside the production vision (Docs › Architecture): the board's markup with its keys prefixed
ar_, its CSS scoped under .ar, and its logic as an ArchLogic object whose state lives in the vision's state.ar and
whose values come back through archVals(). Replaces the Docs lab's architecture area (corporate credit example).
Exports: SCREEN, CSS, CLASS_JS (before the Component class), METHOD_JS (inside it), patch_vision_js()."""
import os, re, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
# the board's generator sits next to this file (build folder) or in architecture-board/ (export bundle, tooling/)
_AB = HERE if os.path.exists(os.path.join(HERE, 'build_arch.py')) else os.path.join(HERE, 'architecture-board')
sys.path.insert(0, HERE); sys.path.insert(0, _AB)
os.environ.setdefault('ARCH_DATA', os.path.join(_AB, 'arch_data.json'))
import build_arch as B
from build_arch import sif, sfor, chip

# ------------------------------------------------------------------------------------------- markup, keys prefixed ar_
ROLE_ROW = ('<div class="rolerow" style="margin-bottom: 4px"><span class="lbl">Act as</span>' + sfor('roles', 'r', '<button type="button" class="chip {{r.cls}}" aria-pressed="{{r.on}}" onClick="{{r.pick}}">{{r.label}}</button>', 4) + '<span class="meta">The prototype\'s role for this review: owner, reviewer, chair or reader.</span></div>')
_arb_decision = B.ARB_DECISION.replace("<div class=\"cards\"><div class=\"dec\" style=\"grid-column: 1 / -1\">", "<div class=\"cards\"><div class=\"dec\" style=\"grid-column: 1 / -1\">" + ROLE_ROW, 1)
assert _arb_decision != B.ARB_DECISION
ARBPAGE = B.ARBPAGE.replace(B.ARB_DECISION, _arb_decision)
SUBHEADER = B.SUBHEADER.replace('<a href="#docs" class="ib sh-back" aria-label="Back to Docs" title="Back to Docs">', '<button type="button" class="ib sh-back" aria-label="Back to Docs" title="Back to Docs" onClick="{{goDocsHome}}">').replace(B.S.ARROW_BACK + '</a>', B.S.ARROW_BACK + '</button>', 1)
assert 'goDocsHome' in SUBHEADER and SUBHEADER.count('</a>') == 0
RAW = ('<div class="ar">' + sif('noPage', SUBHEADER + B.AREA_TABS) + B.VIEWS_AREA + B.CAT_AREA + B.PROC_AREA + B.ELEMENT + ARBPAGE + B.CHANGEPAGE + B.DOCPAGE + '</div>')
_aliases = set(re.findall(r'\bas="(\w+)"', RAW))
_keep = _aliases | {'true', 'false', 'null'}
def pre(frag):
    return re.sub(r'\{\{(\$?\w+)', lambda m: m.group(0) if m.group(1) in _keep or m.group(1).startswith('$') else '{{ar_' + m.group(1), frag)
SCREEN = '<sc-if value="{{dl_vArch}}" hint-placeholder-val="{{false}}">' + pre(RAW) + '</sc-if>'
# id attributes that the board used for labels: keep them unique in the vision
SCREEN = SCREEN.replace('id="pf-sel"', 'id="ar-pf-sel"').replace('for="pf-sel"', 'for="ar-pf-sel"').replace('id="pf-sel2"', 'id="ar-pf-sel2"').replace('for="pf-sel2"', 'for="ar-pf-sel2"').replace('id="app-sel"', 'id="ar-app-sel"').replace('for="app-sel"', 'for="ar-app-sel"')

# ------------------------------------------------------------------------------------------- CSS scoped under .ar
_own = B.CSS[len(B.S.CSS + B.S.SIM_CSS):]   # layer, glyph, selection rules and the board's own rules
def scope(css):
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find('{', i)
        if j < 0: break
        head = css[i:j].strip()
        if head.startswith('@container') or head.startswith('@media'):
            depth, k = 1, j + 1
            while k < n and depth: depth += css[k] == '{'; depth -= css[k] == '}'; k += 1
            out.append(head + '{' + scope(css[j + 1:k - 1]) + '}'); i = k; continue
        k = css.find('}', j)
        body = css[j + 1:k]
        sels = []
        for sel in head.split(','):
            sel = sel.strip()
            if not sel: continue
            if sel == ':root': sels.append('.ar')
            elif sel.startswith('main'): continue
            else: sels.append('.ar ' + sel)
        out.append(', '.join(sels) + '{' + body + '}'); i = k + 1
    return '\n'.join(out)
CSS = scope(_own) + '\n.ar{display:flex;flex-direction:column;gap:16px;min-width:0}\n.ar .simbar{display:none}\n'

# ------------------------------------------------------------------------------------------- logic
_L = B.logic   # the board's logic: consts, HOW, class Component
_cls = _L.index('class Component extends DCLogic {')
CONSTS = _L[:_cls]
_body = _L[_cls:]
_body = _body.replace('class Component extends DCLogic {', 'class ArchLogic {')
_body = _body.replace("  constructor(props) {\n    super(props);\n    this.simHostId = 'sim-host-arch'; this.simDefault = 1440; this.simMinH = 720; this.simMaxH = 1200;\n    this.state = {", "  constructor(host) {\n    this.host = host;\n    this.state = {")
# remove the sim methods and lifecycle
_i = _body.index('  simSync() {'); _j = _body.index('  set(o) {')
_body = _body[:_i] + "  setState(o) { const p = typeof o === 'function' ? o(this.state) : o; if (p) Object.assign(this.state, p); this.host.setState({ arTick: ((this.host.state.arTick || 0) + 1) % 1000000 }); }\n" + _body[_j:]
_body = _body.replace("  toast(msg) { const self = this; this.setState({ toast: msg }); if (typeof window !== 'undefined') setTimeout(() => { if (self.state.toast === msg) self.setState({ toast: null }); }, 4000); }",
                      "  toast(msg) { this.host.setState({ snack: { text: msg, action: '', act: '' } }); }")
_body = _body.replace("    return Object.assign({}, this.simVals(), this.shellVals(),", "    return Object.assign({}, this.shellVals(),")
assert 'simVals' not in _body and 'ArchLogic' in _body and 'setState(o)' in _body
CLASS_JS = CONSTS + _body + '\n'
METHOD_JS = r'''
  // Architecture (Docs › Architecture): the Architecture board's logic, state in state.ar, keys returned with the ar_ prefix
  archVals(ctx) {
    var self = this, s = this.state;
    if (!this._ar) this._ar = new ArchLogic(this);
    var A = this._ar, asDraft = ((s.as || {}).draft || '');
    // a navigation target set by the Docs home or an assistant source: applied once to the board's state
    if (s.arTarget) { Object.assign(A.state, { sel: null, vhist: [] }, s.arTarget); s.arTarget = null; }
    // the header's search field is the elements's filter while the elements is open
    if (((s.dl || {}).view === 'arch') && s.screen === 'docs' && A.state.area === 'elements' && !A.state.page) A.state.q = asDraft; else A.state.q = '';
    var R = A.renderVals();
    R.onQ = function () {}; R.clearQ = function (e) { if (e && e.preventDefault) e.preventDefault(); self.setState({ as: Object.assign({}, self.state.as || {}, { draft: '' }) }); };
    R.goDocsHome = function (e) { if (e && e.preventDefault) e.preventDefault(); self.setState({ dl: Object.assign({}, self.state.dl || {}, { view: 'home' }) }); };
    var out = {}; Object.keys(R).forEach(function (k) { out['ar_' + k] = R[k]; });
    return out;
  }
'''

DRAFT_JS = r"""    // drafting mode of the assistant pane: the thread of an architecture document (DEC-KB-38); the person inserts, the agent proposes
    V.asHasDoc = false; V.asDocLabel = ''; V.asDocGo = set({});
    if (A.docCtx && this._ar) { var DT = this._ar.docTurns(A.docCtx.wid, A.docCtx.did); if (DT) {
      V.asTitle = 'Drafting · ' + DT.title; V.asCtx = DT.change; V.asEmpty = false;
      V.asTurns = DT.turns.map(function (t) { return { q: t.q, hasQ: t.hasQ, n: 0, hasTrace: false, trace: [], waiting: false, apTitle: '', apArgs: '', apWhy: '', apCta: '', approve: set({}), decline: set({}), answer: t.answer, hasLink: false, linkLabel: '', linkGo: set({}), good: false, thumbUp: set({}), thumbDown: set({}), hasPills: t.hasSources, pills: t.sources, hasProps: t.hasProps, props: t.props, hasQual: false, qual: {}, hasReplies: false, replies: [], dChain: false, chain: [], dSteps: false, steps: [], dList: false, list: [], dProv: false, prov: '', dSrc: false, sources: [], fresh: '' }; });
      V.asHasDoc = true; V.asDocLabel = 'Open the document · ' + DT.progress + ' sections'; V.asDocGo = function () { DT.openDoc(); };
      V.asSendDraft = set(function () { var t = (asNow().draft || '').trim(); if (t) DT.ask(t); return { as: Object.assign({}, self.state.as || {}, { draft: '' }) }; });
      V.asKey = function (e) { if (e && e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); var t = ((self.state.as || {}).draft || (e.target && e.target.value) || '').trim(); if (t) { DT.ask(t); self.setState({ as: Object.assign({}, self.state.as || {}, { draft: '' }) }); } } };
      V.asNew = set(function () { return { as: Object.assign({}, self.state.as || {}, { turns: [], draft: '', menu: false, docCtx: null }) }; });
      V.asClose = set(function () { return { as: Object.assign({}, self.state.as || {}, { open: false, menu: false, docCtx: null }) }; });
    } }
    // intake mode of the assistant pane: a signal or a request is qualified in conversation, then becomes a change (decision of 2026-11-10)
    if (A.intakeCtx && !A.docCtx && this._ar) { var IT = this._ar.intakeTurns(); if (IT) {
      V.asTitle = IT.title; V.asCtx = IT.ctx; V.asEmpty = false;
      V.asTurns = IT.turns.map(function (t) { return { q: t.q, hasQ: t.hasQ, n: 0, hasTrace: false, trace: [], waiting: false, apTitle: '', apArgs: '', apWhy: '', apCta: '', approve: set({}), decline: set({}), answer: t.answer, hasLink: t.hasLink, linkLabel: t.linkLabel, linkGo: t.linkGo || set({}), good: false, thumbUp: set({}), thumbDown: set({}), hasPills: false, pills: [], hasProps: false, props: [], hasQual: t.hasQual, qual: t.qual, hasReplies: t.hasReplies, replies: t.replies, dChain: false, chain: [], dSteps: false, steps: [], dList: false, list: [], dProv: false, prov: '', dSrc: false, sources: [], fresh: '' }; });
      V.asSendDraft = set(function () { var t = (asNow().draft || '').trim(); if (t) IT.ask(t); return { as: Object.assign({}, self.state.as || {}, { draft: '' }) }; });
      V.asKey = function (e) { if (e && e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); var t = ((self.state.as || {}).draft || (e.target && e.target.value) || '').trim(); if (t) { IT.ask(t); self.setState({ as: Object.assign({}, self.state.as || {}, { draft: '' }) }); } } };
      V.asNew = set(function () { return { as: Object.assign({}, self.state.as || {}, { turns: [], draft: '', menu: false, intakeCtx: false }) }; });
      V.asClose = set(function () { return { as: Object.assign({}, self.state.as || {}, { open: false, menu: false, intakeCtx: false }) }; });
    } }"""


def patch_vision_js(js):
    """Hook archVals into the vision's visionVals: values and the header context when the architecture space is open."""
    a = "    Object.assign(V, this.docsVals(ctx));\n"
    assert a in js
    js = js.replace(a, a + "    Object.assign(V, this.archVals(ctx));\n", 1)
    b = "    if (HDR[s.screen]) { V.hdrFeature = HDR[s.screen][0]; V.hdrSummary = HDR[s.screen][1]; }\n"
    assert b in js
    js = js.replace(b, b + "    if (s.screen === 'docs' && (s.dl || {}).view === 'arch') { V.hdrFeature = V.ar_hdrFeature; V.hdrSummary = V.ar_hdrSummary; }\n", 1)
    c = "    V.mainPaneCls = A.open ? 'pane-on' : '';\n"
    assert c in js
    js = js.replace(c, c + DRAFT_JS, 1)
    return js
