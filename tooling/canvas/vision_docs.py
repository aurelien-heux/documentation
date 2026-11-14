"""The Docs lab (way in A · Spaces, adopted 30 Oct) inside the production vision: the same fragments with their keys prefixed dl_,
and the same logic turned into a docsVals(ctx) method whose state lives in state.dl. Questions go through the vision's
assistant: dlMatch() routes documentation questions to the knowledge-base answers of the lab (with their picture,
sources and version), and the answer's sources open the Docs pages. Administration › Core › Knowledge base shows the
sources. Exports: CSS, SCREENS, ADMIN_KB, JS, PANE_EXTRA."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs_lab_data as D

_src = open(os.path.join(HERE, 'docs_lab_build.py'), encoding='utf-8').read()
_cut = _src.index('\nHDR = S.header(False)')
_argv = sys.argv; sys.argv = ['x', '/dev/null']
_ns = {'__file__': os.path.join(HERE, 'docs_lab_build.py'), '__name__': 'docslab'}
exec(_src[:_cut], _ns)
sys.argv = _argv

# --- fragments: way in A only, keys prefixed ----------------------------------------------------------------
_frags = _ns['HOME_A'] + _ns['ARCH'] + _ns['DDV'] + _ns['AIV'] + _ns['OPSV'] + _ns['NEWV']
_aliases = set(re.findall(r'\bas="(\w+)"', _frags + _ns['KBV']))
def pre(frag):
    return re.sub(r'\{\{(\w+)', lambda m: m.group(0) if m.group(1) in _aliases or m.group(1) in ('true', 'false', 'null') else '{{dl_' + m.group(1), frag)

SCREENS = '<sc-if value="{{vDocs}}" hint-placeholder-val="{{false}}"><div class="stack" style="gap: 16px">' + pre(_frags) + '</div></sc-if>'
SCREENS = SCREENS.replace('class="thumb"', 'class="dl-thumb"')

# Administration › Core › Knowledge base: the lab's page without its own navigation and title
_kb = _ns['KBV']
_kb_body = _kb[_kb.index('<p class="sub"'):_kb.rindex('\n  </div>\n</div></sc-if>')]  # the stack's children, up to its own close
ADMIN_KB = pre('<sc-if value="{{aKb}}" hint-placeholder-val="{{false}}"><div class="stack" style="gap: 16px">'
               '<div class="row r-wrap" style="gap: 12px; align-items: flex-start">' + _kb_body.replace('<p class="sub" style="max-width: 760px">', '<p class="sub" style="max-width: 760px; flex: 1; min-width: 240px">', 1).split('</p>', 1)[0] + '</p><button type="button" class="btn t" onClick="{{kbAdd}}">Add a source</button></div>'
               + _kb_body.split('</p>', 1)[1] + '</div></sc-if>')

CSS = (_ns['CSS_DL'] + _ns['ARC'].CSS).replace('.thumb{', '.dl-thumb{').replace('.thumb i{', '.dl-thumb i{').replace('.thumb{display:none}', '.dl-thumb{display:none}')

# extra blocks in the vision's assistant turns, for knowledge-base answers
PANE_EXTRA = ('<sc-if value="{{t.dChain}}" hint-placeholder-val="{{false}}"><div class="chain"><sc-for list="{{t.chain}}" as="c" hint-placeholder-count="3"><div class="ch"><b>{{c.t}}</b><span>{{c.sub}}</span></div><sc-if value="{{c.more}}" hint-placeholder-val="{{true}}"><span class="ch-arr" aria-hidden="true">→</span></sc-if></sc-for></div></sc-if>'
              '<sc-if value="{{t.dSteps}}" hint-placeholder-val="{{false}}"><ol class="steps"><sc-for list="{{t.steps}}" as="c" hint-placeholder-count="3"><li><span class="num">{{c.n}}</span><span><b class="ui">{{c.t}}</b><span class="meta" style="display: block">{{c.sub}}</span></span></li></sc-for></ol></sc-if>'
              '<sc-if value="{{t.dList}}" hint-placeholder-val="{{false}}"><ul class="list" style="border: 1px solid #E6E0EC; border-radius: 12px; background: #FFFFFF; padding: 0 12px"><sc-for list="{{t.list}}" as="c" hint-placeholder-count="3"><li style="font-size: 13px; align-items: center"><span class="dot {{c.cls}}">{{c.mark}}</span><span style="flex: 1">{{c.t}}<span class="meta" style="display: block">{{c.sub}}</span></span></li></sc-for></ul></sc-if>'
              '<sc-if value="{{t.dProv}}" hint-placeholder-val="{{false}}"><div class="prov"><b>Draft</b><span>{{t.prov}}</span></div></sc-if>'
              '<sc-if value="{{t.dSrc}}" hint-placeholder-val="{{false}}"><div class="srcs"><span class="meta">Sources</span><sc-for list="{{t.sources}}" as="x" hint-placeholder-count="2"><button type="button" class="srcb" onClick="{{x.go}}"><span class="srcT" style="background: {{x.bg}}; color: {{x.fg}}">{{x.ab}}</span><span>{{x.label}}</span></button></sc-for></div><div class="fresh">{{t.fresh}}</div></sc-if>')

# --- logic ------------------------------------------------------------------------------------------------------
_L = _ns['LOGIC']
_a = _L.index('    // ---- architecture')
_b = _L.index('    return Object.assign(sim, V, {')
_mid = _L[_a:_b]
_obj = _L[_b + len('    return Object.assign(sim, V, {'):_L.rindex('    });\n  }\n}')]
_old_go = "    var go = function (o) { return set(Object.assign({ snack: null }, o)); };"
assert _old_go in _mid
_mid = _mid.replace(_old_go, "    var go = function (o) { return function (e) { if (e && e.preventDefault) e.preventDefault(); var p = patchOf(Object.assign({ snack: null }, o)); p.screen = 'docs'; p.tourId = null; self.setState(Object.assign({}, ctx.closeAll, p)); }; };")
_mid = _mid.replace('__DG__', D.js_data())
_hdr_src = _L[_L.index('    var SRC = {'):_L.index('    var cInline')]

JS = r'''
  // Docs (from the Docs lab, way in A · Spaces): state in state.dl, keys returned with the dl_ prefix
  docsVals(ctx) {
    var self = this, S0 = this.state, DG = __DGDATA__;
    var D0 = { variant: 'A', view: 'home', arch: null, dd: 'dd.cc-facility.domain', opsTab: 'release', nj: { d1: true, d2: true, d3: true, w1: true }, wiki: null };  // way in A · Spaces, adopted 30 Oct
    var s = Object.assign({}, D0, S0.dl || {}, { turns: [], asOpen: false, draft: '', snack: null, live: '' });
    var sim = {}, ON = ctx.ON, val = ctx.val;
    var patchOf = function (o, e) {
      var p = (typeof o === 'function' ? o(e) : o) || {}, top = {}, dl = Object.assign({}, D0, self.state.dl || {});
      Object.keys(p).forEach(function (k) {
        if (k === 'snack') top.snack = p.snack ? { text: p.snack, action: '', act: '' } : null;
        else if (k === 'asOpen') { if (p.asOpen) top.as = Object.assign({}, self.state.as || {}, { open: true }); }
        else if (k === 'turns' || k === 'draft' || k === 'live' || k === 'variant') {}
        else if (k === 'arTarget') top.arTarget = p.arTarget;
        else dl[k] = p[k];
      });
      top.dl = dl; return top;
    };
    var set = function (o) { return function (e) { if (e && e.preventDefault) e.preventDefault(); self.setState(patchOf(o, e)); }; };
''' + _hdr_src + r'''    var cInline = false;
    var ask = function (qid, text) { return function (e) { if (e && e.preventDefault) e.preventDefault(); self.setState(self.asAsk(text, true)); }; };
    var sendDraft = function () {};
''' + _mid + r'''    self._dlAnswerOf = answerOf;
    var R = Object.assign({}, V, {''' + _obj + r'''    });
    R.goKb = ctx.role === 'platform' ? function (e) { if (e && e.preventDefault) e.preventDefault(); self.setState(Object.assign({}, ctx.closeAll, { screen: 'admin', adminView: 'kb', mview: 'list', tourId: null })); }
      : set({ snack: 'Platform admins manage the knowledge base sources in Administration.' });
    R.aKb = ctx.akey === 'kb' && S0.screen === 'admin';
    var out = {}; Object.keys(R).forEach(function (k) { out['dl_' + k] = R[k]; });
    return out;
  }
  // documentation questions answered from the knowledge base, with sources (null: not a documentation question)
  dlMatch(t) {
    t = (t || '').toLowerCase();
    if (/hotfix|release train|on thursday/.test(t)) return 'ops_hotfix';
    if (/why .*export|nightly exports/.test(t)) return 'arch_why';
    if (/\barb\b|ready for the board/.test(t)) return 'arb_ready';
    if (/facility (become|becomes|get) active|when .*facility.*active/.test(t)) return 'dd_expire';
    if (/facility service|limit-service|what depends on/.test(t)) return 'arch_dep';
    if (/write a skill|skill that creates/.test(t)) return 'ai_skill';
    if (/first week|new joiner|onboarding|i just joined/.test(t)) return 'new_week';
    if (/who is on.?call|on.?call for|on.?call this week/.test(t)) return 'org_oncall';
    if (/collateral register|inferred/.test(t)) return 'arch_inferred';
    if (/paste|secrets?|which data/.test(t)) return 'ai_data';
    if (/what do .* mean|what does .* mean|glossary/.test(t)) return 'glossary';
    return null;
  }
'''.replace('__DGDATA__', 'null')
JS = JS.replace('__DGDATA__', D.js_data())
assert '__DG__' not in JS and '__DGDATA__' not in JS
