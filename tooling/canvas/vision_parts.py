"""Fragments for ProductionVision.dc.html (AIToolbox production vision): the Catalog screens and admin pages (taken from
the Catalog lab, keys prefixed cat_), the Environments and Docs pages, and the assistant pane (keys prefixed as)."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import shell as S, navgen as N, vision_docs as VD

# --- reuse the Catalog lab fragments as they are, with their keys prefixed -------------------------------
_src = open(os.path.join(HERE, 'catalog_lab_build.py'), encoding='utf-8').read()
_cut = _src.index('\nbody = (BODY')
_argv = sys.argv; sys.argv = ['x', '/dev/null']
_ns = {'__file__': os.path.join(HERE, 'catalog_lab_build.py'), '__name__': 'catlab'}
exec(_src[:_cut], _ns)
sys.argv = _argv

CAT_KEYS = ['sCatalog', 'sItem', 'sNew', 'cTabs', 'tBrowse', 'tMine', 'kindChips', 'items', 'mine', 'goNew', 'goCatalog', 'sk', 'reportIt',
            'proc', 'nWrite', 'nTest', 'nSubmit', 'nReview', 'nDone', 'nsName', 'onNsName', 'nsDesc', 'onNsDesc', 'nsBody', 'onNsBody', 'nsEx1', 'onNsEx1',
            'toolChips', 'srcLink', 'pickSrcGit', 'saveDraft', 'toWrite', 'toTest', 'toSubmit', 'nsNameOr', 'nsEx1Or', 'checks', 'tryN', 'tryTools',
            'tryNeedsAppr', 'tryApprQ', 'tryApprArgs', 'tryApprove', 'tryAnswer', 'scopes', 'scopeOrg', 'submitCta', 'submit', 'simulateApprove', 'openMine', 'doneText',
            'aTabs', 'aReview', 'rvList', 'rvOpen', 'queue', 'rv', 'rvBack', 'rvChecks', 'rvNotReady', 'rvPublish', 'rvChanges', 'aItems', 'adminItems',
            'aPolicies', 'policyRows', 'aSweep', 'phases', 'sweepRows']
_rx = re.compile(r'\{\{(' + '|'.join(sorted(CAT_KEYS, key=len, reverse=True)) + r')\b')
def pre(frag):
    return _rx.sub(lambda m: '{{cat_' + m.group(1), frag)

CAT_CSS = _ns['CSS_CAT']
CAT_SCREENS = pre(_ns['CATALOG'] + _ns['ITEM'] + _ns['NEWSKILL'])
CAT_ADMIN = pre('<sc-if value="{{aCatalog}}" hint-placeholder-val="{{false}}"><div class="row r-wrap" role="tablist" aria-label="Catalog" style="gap: 0; border-bottom: 1px solid #CAC4CF"><sc-for list="{{aTabs}}" as="t" hint-placeholder-count="3"><button type="button" role="tab" class="tab {{t.cls}}" aria-selected="{{t.on}}" onClick="{{t.pick}}">{{t.label}}<sc-if value="{{t.hasN}}" hint-placeholder-val="{{false}}"><span class="n">{{t.n}}</span></sc-if></button></sc-for></div></sc-if>'
                + _ns['REVIEW'] + _ns['ITEMS_T'] + _ns['POLICIES'] + _ns['SWEEP_TOOLS']).replace('{{aCatalog}}', '{{cat_aCatalog}}')
# the Catalog lab wraps Review in aReview with a default hint of true: in the vision it must default to hidden
CAT_ADMIN = CAT_ADMIN.replace('<sc-if value="{{cat_aReview}}" hint-placeholder-val="{{true}}">', '<sc-if value="{{cat_aReview}}" hint-placeholder-val="{{false}}">')

ST = 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
LOCK = f'<svg width="18" height="18" viewBox="0 0 24 24" {ST}><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>'
SEND = f'<svg width="20" height="20" viewBox="0 0 24 24" {ST}><path d="M12 19V5M5 12l7-7 7 7"/></svg>'
CLOSE = f'<svg width="20" height="20" viewBox="0 0 24 24" {ST}><path d="M6 6l12 12M18 6L6 18"/></svg>'
NEWC = f'<svg width="20" height="20" viewBox="0 0 24 24" {ST}><path d="M12 5v14M5 12h14"/></svg>'
TOOLS = f'<svg width="18" height="18" viewBox="0 0 24 24" {ST}><path d="M14 7a4 4 0 0 1 5 5l-9 9-3-3 9-9M5 19l-1 1"/></svg>'
SEARCH = f'<svg width="18" height="18" viewBox="0 0 24 24" {ST}><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>'

# --- Environments and Docs ---------------------------------------------------------------------------------
ENV = '''<sc-if value="{{vEnv}}" hint-placeholder-val="{{false}}"><div class="stack" style="gap: 16px">
  <div class="row r-wrap" style="gap: 8px 16px; align-items: center">
    <label for="env-app" class="lbl" style="font-size: 12px; font-weight: 600; color: #48454E">Application</label>
    <select id="env-app" class="sel" value="{{envApp}}" onChange="{{envOnApp}}" aria-describedby="env-app-h"><sc-for list="{{envApps}}" as="a" hint-placeholder-count="4"><option value="{{a.id}}">{{a.label}}</option></sc-for></select>
    <span id="env-app-h" class="meta">{{envAppNote}}</span>
    <span style="flex: 1"></span>
    <span class="meta">Observed by Kubernetes and ArgoCD · {{envObservedAt}}</span>
  </div>
  <div class="card env-card" style="padding: 0; overflow: hidden"><div class="ad-tscroll"><table class="ad-tbl env-tbl" style="width: 100%; border-collapse: collapse">
    <thead><tr><th class="th" style="width: 20%">Environment</th><th class="th">What runs · observed</th><th class="th" style="width: 17%">Reservation</th><th class="th" style="width: 1%"><span class="sr-only">Actions</span></th></tr></thead>
    <tbody><sc-for list="{{envRows}}" as="e" hint-placeholder-count="6"><tr class="rw"><td class="td" data-col="Environment"><b class="ui">{{e.name}}</b><div class="meta">{{e.tier}}</div><sc-if value="{{e.isUpstream}}" hint-placeholder-val="{{false}}"><span class="tag" style="margin-top: 4px">Upstream · {{e.tracked}} · {{e.mode}}</span></sc-if><sc-if value="{{e.hasUpstream}}" hint-placeholder-val="{{true}}"><div class="meta">falls back on {{e.upstream}}</div></sc-if></td>
      <td class="td" data-col="What runs"><sc-for list="{{e.mods}}" as="m" hint-placeholder-count="2"><div class="env-mod"><span class="mono env-m1">{{m.module}}</span><span class="env-m2"><span class="mono">{{m.branch}}</span><span class="meta"> · {{m.where}}</span></span><span class="env-m3"><span class="mono">{{m.version}} @ {{m.commit}}</span><span class="meta"> · {{m.source}} · {{m.at}}</span><sc-if value="{{m.drift}}" hint-placeholder-val="{{false}}"> <span class="tile wn"><i></i>{{m.driftText}}</span></sc-if></span></div></sc-for></td>
      <td class="td" data-col="Reservation"><sc-if value="{{e.hasRes}}" hint-placeholder-val="{{false}}"><span class="tile in"><i></i>{{e.resHolder}}</span><div class="meta" style="margin-top: 4px">{{e.resScope}} · until {{e.resUntil}}</div></sc-if><sc-if value="{{e.noRes}}" hint-placeholder-val="{{true}}"><span class="meta">—</span></sc-if></td>
      <td class="td env-actions" data-col=""><sc-if value="{{e.canAct}}" hint-placeholder-val="{{true}}"><button type="button" class="chip" style="height: 32px" onClick="{{e.deploy}}">Deploy</button><sc-if value="{{e.canReserve}}" hint-placeholder-val="{{true}}"> <button type="button" class="chip" style="height: 32px" onClick="{{e.reserve}}">Reserve</button></sc-if><sc-if value="{{e.mine}}" hint-placeholder-val="{{false}}"> <button type="button" class="chip" style="height: 32px" onClick="{{e.extend}}">Extend</button> <button type="button" class="chip" style="height: 32px" onClick="{{e.release}}">Release</button></sc-if></sc-if><sc-if value="{{e.isUpstream}}" hint-placeholder-val="{{false}}"><span class="meta">Follows its branch</span></sc-if></td></tr></sc-for></tbody></table></div></div>
</div></sc-if>'''

DOCS = '''<sc-if value="{{vDocs}}" hint-placeholder-val="{{false}}"><div class="stack" style="gap: 16px; max-width: 860px">
  <sc-for list="{{docRows}}" as="d" hint-placeholder-count="4"><div class="card" style="display: flex; gap: 14px; align-items: flex-start; padding: 16px 20px"><div style="flex: 1; min-width: 0"><b class="ui" style="font-size: 15px">{{d.title}}</b><div style="font-size: 13px; line-height: 18px; color: #48454E; margin-top: 4px">{{d.desc}}</div><div style="font-size: 12px; color: #48454E; margin-top: 6px">{{d.meta}}</div></div></div></sc-for>
  <span style="font-size: 12px; color: #48454E">Search them, or ask about them, from the search bar at the top: the assistant reads the same pages through the Knowledge base, with their source.</span>
</div></sc-if>'''

SCREENS = CAT_SCREENS + ENV + VD.SCREENS  # Docs: the Docs lab, way in A · Spaces

# --- assistant pane --------------------------------------------------------------------------------------
PANE = '''<sc-if value="{{asOpen}}" hint-placeholder-val="{{false}}"><aside class="as-pane" aria-label="Assistant">
  <div class="as-hd">''' + S.BOT + '''<div style="flex: 1; min-width: 0"><div class="ui" style="font-size: 15px; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis">{{asTitle}}</div><div style="font-size: 12px; color: #48454E">{{asCtx}}</div></div>
    <button type="button" class="ib" aria-label="New conversation" onClick="{{asNew}}">''' + NEWC + '''</button><button type="button" class="ib" aria-label="Close assistant" onClick="{{asClose}}">''' + CLOSE + '''</button></div>
  <div class="as-body" aria-live="polite">
    <sc-if value="{{asEmpty}}" hint-placeholder-val="{{true}}"><div class="stack" style="gap: 10px; padding: 8px 0"><div class="ui" style="font-size: 18px; font-weight: 700">How can I help?</div><span style="font-size: 13px; color: #48454E">{{asHint}}</span><div class="stack" style="gap: 8px; margin-top: 4px"><sc-for list="{{asSugg}}" as="g" hint-placeholder-count="2"><button type="button" class="as-sugg" onClick="{{g.go}}">{{g.t}}</button></sc-for></div></div></sc-if>
    <sc-for list="{{asTurns}}" as="t" hint-placeholder-count="2">
      <sc-if value="{{t.hasQ}}" hint-placeholder-val="{{true}}"><div class="as-q">{{t.q}}</div></sc-if>
      <div class="as-a">
        <sc-if value="{{t.hasTrace}}" hint-placeholder-val="{{true}}"><div class="as-trace"><b class="ui" style="font-size: 12px">Used {{t.n}} tools</b><sc-for list="{{t.trace}}" as="x" hint-placeholder-count="2"><div class="row" style="gap: 8px"><span class="as-src" style="background: {{x.bg}}; color: {{x.fg}}">{{x.ab}}</span><span style="flex: 1; font-size: 13px">{{x.label}}</span><span style="font-size: 11px; color: {{x.stc}}">{{x.st}}</span></div></sc-for></div></sc-if>
        <sc-if value="{{t.waiting}}" hint-placeholder-val="{{false}}"><div class="as-appr"><div class="row" style="gap: 8px">''' + LOCK + '''<b class="ui" style="font-size: 14px">{{t.apTitle}}</b></div><div class="mono" style="font-size: 12px; color: #48454E; white-space: pre-line">{{t.apArgs}}</div><div style="font-size: 12px; color: #48454E">{{t.apWhy}}</div><div class="row" style="justify-content: flex-end; gap: 8px"><button type="button" class="btn x sm" onClick="{{t.decline}}">Don’t run</button><button type="button" class="btn f sm" onClick="{{t.approve}}">{{t.apCta}}</button></div></div></sc-if>
        <div style="font-size: 14px; line-height: 20px; white-space: pre-line">{{t.answer}}</div>
        <sc-if value="{{t.hasPills}}" hint-placeholder-val="{{false}}"><div class="srcs"><sc-for list="{{t.pills}}" as="s" hint-placeholder-count="3"><span class="src-pill">{{s.t}}</span></sc-for></div></sc-if>
        <sc-if value="{{t.hasProps}}" hint-placeholder-val="{{false}}"><sc-for list="{{t.props}}" as="p" hint-placeholder-count="4"><div class="prop-card"><span class="lbl">→ {{p.section}}</span><p>{{p.text}}</p><div class="row" style="gap: 8px; align-items: center"><sc-if value="{{p.inserted}}" hint-placeholder-val="{{false}}"><span class="tile ok"><i></i>Inserted</span></sc-if><span style="flex: 1"></span><sc-if value="{{p.canInsert}}" hint-placeholder-val="{{true}}"><button type="button" class="chip" style="height: 28px; font-size: 12px" onClick="{{p.replace}}">Replace section</button><button type="button" class="chip chip-on" style="height: 28px; font-size: 12px" onClick="{{p.insert}}">Insert into section</button></sc-if></div></div></sc-for></sc-if>
        <sc-if value="{{t.hasQual}}" hint-placeholder-val="{{false}}"><div class="prop-card"><b class="ui" style="font-size: 14px">{{t.qual.title}}</b><dl class="qual"><dt>Origin</dt><dd>{{t.qual.origin}}</dd><dt>Enters at</dt><dd>{{t.qual.enters}} · {{t.qual.skips}}</dd><dt>Kind</dt><dd>{{t.qual.kind}}</dd><dt>Scope</dt><dd>{{t.qual.scope}}</dd><dt>First</dt><dd>{{t.qual.docs}}</dd><dt>Next gate</dt><dd>{{t.qual.gate}}</dd></dl><sc-if value="{{t.qual.hasOverlap}}" hint-placeholder-val="{{false}}"><span class="tile wn"><i></i>{{t.qual.overlap}}</span></sc-if></div></sc-if>
        <sc-if value="{{t.hasReplies}}" hint-placeholder-val="{{false}}"><div class="srcs" role="group" aria-label="Suggested replies"><sc-for list="{{t.replies}}" as="r" hint-placeholder-count="3"><button type="button" class="chip" style="height: auto; min-height: 28px; font-size: 12px; padding: 4px 10px; text-align: left; white-space: normal" onClick="{{r.pick}}">{{r.t}}</button></sc-for></div></sc-if>
        ''' + VD.PANE_EXTRA + '''
        <sc-if value="{{t.hasLink}}" hint-placeholder-val="{{false}}"><button type="button" class="chip" style="height: 28px; align-self: flex-start" onClick="{{t.linkGo}}">{{t.linkLabel}}</button></sc-if>
        <div class="row" style="gap: 4px"><button type="button" class="ib" style="width: 32px; height: 32px; margin: 0" aria-label="Good answer" aria-pressed="{{t.good}}" onClick="{{t.thumbUp}}"><svg width="16" height="16" viewBox="0 0 24 24" ''' + ST + '''><path d="M7 11v9H4v-9zM7 11l4-8a2 2 0 0 1 3 2l-1 4h6a2 2 0 0 1 2 2l-2 7a2 2 0 0 1-2 2H7"/></svg></button><button type="button" class="ib" style="width: 32px; height: 32px; margin: 0" aria-label="Bad answer" onClick="{{t.thumbDown}}"><svg width="16" height="16" viewBox="0 0 24 24" ''' + ST + '''><path d="M17 13V4h3v9zM17 13l-4 8a2 2 0 0 1-3-2l1-4H5a2 2 0 0 1-2-2l2-7a2 2 0 0 1 2-2h10"/></svg></button></div>
      </div>
    </sc-for>
  </div>
  <sc-if value="{{asMenu}}" hint-placeholder-val="{{false}}"><div class="as-menu" role="dialog" aria-label="Tools, skills and MCP servers">
    <div class="as-mh">Tools</div><sc-for list="{{asTools}}" as="m" hint-placeholder-count="3"><button type="button" class="as-mi" role="switch" aria-checked="{{m.on}}" onClick="{{m.toggle}}"><span style="flex: 1; min-width: 0; text-align: left">{{m.name}}<span style="display: block; font-size: 11px; color: #48454E">{{m.note}}</span></span><span class="tgl" aria-hidden="true"><span class="tgl-t"></span></span></button></sc-for>
    <div class="as-mh">Skills</div><sc-for list="{{asSkills}}" as="m" hint-placeholder-count="3"><button type="button" class="as-mi" role="switch" aria-checked="{{m.on}}" onClick="{{m.toggle}}"><span style="flex: 1; min-width: 0; text-align: left">{{m.name}}<span style="display: block; font-size: 11px; color: #48454E">{{m.note}}</span></span><span class="tgl" aria-hidden="true"><span class="tgl-t"></span></span></button></sc-for>
    <div class="as-mh">MCP servers</div><sc-for list="{{asMcp}}" as="m" hint-placeholder-count="2"><button type="button" class="as-mi" role="switch" aria-checked="{{m.on}}" onClick="{{m.toggle}}"><span style="flex: 1; min-width: 0; text-align: left">{{m.name}}<span style="display: block; font-size: 11px; color: #48454E">{{m.note}}</span></span><span class="tgl" aria-hidden="true"><span class="tgl-t"></span></span></button></sc-for>
    <div class="row" style="padding: 10px 12px 4px; border-top: 1px solid #ECE5F4"><button type="button" class="lnk" onClick="{{asBrowse}}">Browse the Catalog</button></div>
  </div></sc-if>
  <div class="as-comp">
    <div class="row" style="gap: 6px; flex-wrap: wrap"><span class="as-chip">{{asCtx}}</span><sc-if value="{{asHasDoc}}" hint-placeholder-val="{{false}}"><button type="button" class="chip" style="height: 24px; font-size: 12px" onClick="{{asDocGo}}">{{asDocLabel}}</button></sc-if></div>
    <textarea id="as-in" rows="2" aria-label="Ask the assistant" placeholder="Ask about this page…" value="{{asDraft}}" onChange="{{asOnDraft}}" onKeyDown="{{asKey}}"></textarea>
    <div class="row" style="gap: 8px"><button type="button" class="chip" style="height: 32px" aria-expanded="{{asMenu}}" onClick="{{asToggleMenu}}">''' + TOOLS + '''Tools<span class="n">{{asCount}}</span></button><span style="flex: 1"></span><button type="button" class="as-send" aria-label="Send" onClick="{{asSendDraft}}">''' + SEND + '''</button></div>
  </div>
  <div style="font-size: 11px; line-height: 15px; color: #48454E; text-align: center; padding: 6px 16px 10px">The assistant can make mistakes. Check important information before you act on it.</div>
</aside></sc-if>'''

CSS = CAT_CSS + VD.CSS + r""".env-mod{display:grid;grid-template-columns:minmax(120px,.8fr) minmax(160px,1fr) minmax(220px,1.4fr);gap:2px 16px;align-items:baseline;padding:3px 0;font-size:13px}.env-mod+.env-mod{border-top:1px dashed #E6E0EC;margin-top:4px;padding-top:7px}.env-m1{font-weight:600}.env-mod .mono{font-size:13px}@container win (max-width: 1199px){.env-mod{grid-template-columns:1fr}.env-m2,.env-m3{padding-left:0}}
.env-tbl .td{vertical-align:top}.env-actions{text-align:right;white-space:nowrap}
@container win (max-width: 839px){.env-tbl,.env-tbl tbody,.env-tbl tr,.env-tbl td{display:block;min-width:0}.env-tbl thead{display:none}.env-tbl{min-width:0!important}.env-tbl tr.rw{padding:8px 0;border-bottom:1px solid #E6E0EC}.env-tbl .td{border:0;padding:6px 16px;height:auto;min-height:0;white-space:normal}.env-tbl .td[data-col]:not([data-col=""])::before{content:attr(data-col);display:block;font:600 11px/16px Manrope,system-ui,sans-serif;letter-spacing:.4px;text-transform:uppercase;color:#48454E;margin-bottom:2px}.env-tbl tr.rw .td[data-col="Environment"]::before{display:none}.env-actions{text-align:left;white-space:normal;padding-bottom:12px}}

.stack{display:flex;flex-direction:column;gap:12px;min-width:0}
.as-pane{width:400px;flex:none;display:flex;flex-direction:column;border-left:1px solid #CAC4CF;background:#FAF4FF;position:relative;min-height:0}
.as-hd{display:flex;align-items:center;gap:10px;padding:12px 8px 12px 16px;border-bottom:1px solid #E6E0EC}
.as-body{flex:1;overflow:auto;padding:16px;display:flex;flex-direction:column;gap:12px}
.as-sugg{border:1px solid #CAC4CF;border-radius:12px;background:#FFFFFF;padding:10px 12px;text-align:left;font:inherit;font-size:13px;color:#1C1B1E;cursor:pointer}
.as-sugg:hover{background:#F2EBFA}
.as-q{align-self:flex-end;max-width:85%;padding:10px 14px;border-radius:16px 16px 4px 16px;background:#E3DFFF;color:#191836;font-size:14px;line-height:20px}
.as-a{display:flex;flex-direction:column;gap:8px}
.as-trace{border:1px solid #CAC4CF;border-radius:12px;padding:8px 10px;display:flex;flex-direction:column;gap:6px;background:#FFFFFF}
.as-src{width:22px;height:22px;border-radius:6px;display:inline-flex;align-items:center;justify-content:center;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:9px;font-weight:800;flex:none}
.as-appr{border:1px solid #79757F;border-radius:12px;background:#F2EBFA;padding:12px;display:flex;flex-direction:column;gap:8px}
.as-comp{margin:0 12px;border:1px solid #79757F;border-radius:16px;background:#FFFFFF;padding:10px 12px;display:flex;flex-direction:column;gap:6px}
.as-comp:focus-within{border:2px solid #35307E;padding:9px 11px}
.as-comp textarea{border:0;outline:0;resize:none;font:400 14px/20px 'Open Sans',system-ui,sans-serif;color:#1C1B1E;background:transparent}
.as-chip{display:inline-flex;align-items:center;height:24px;padding:0 8px;border-radius:8px;background:#E3DFFF;color:#191836;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:600}
.as-send{width:36px;height:36px;border:0;border-radius:50%;background:#35307E;color:#FFFFFF;display:inline-flex;align-items:center;justify-content:center;cursor:pointer}
.as-menu{position:absolute;left:12px;right:12px;bottom:150px;max-height:60%;overflow:auto;background:#F2EBFA;border-radius:12px;box-shadow:0 1px 2px rgba(0,0,0,.3),0 2px 6px 2px rgba(0,0,0,.15);padding:6px 0;z-index:5}
.as-mh{padding:10px 12px 4px;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:700;color:#48454E}
.as-pane .srcs{display:flex;flex-wrap:wrap;gap:4px}.as-pane .qual{display:grid;grid-template-columns:76px 1fr;gap:3px 10px;margin:0;font-size:13px;line-height:18px}.as-pane .qual dt{color:#48454E}.as-pane .qual dd{margin:0}.as-pane .src-pill{font-size:11px;line-height:16px;padding:2px 8px;border-radius:8px;background:#ECE5F4;color:#48454E}.as-pane .prop-card{border:1px solid #CAC4CF;border-left:4px solid #80D5D4;border-radius:8px;padding:8px 12px;display:flex;flex-direction:column;gap:6px;background:#FFFFFF}.as-pane .prop-card p{margin:0;font-size:13px;line-height:19px}.as-pane .prop-card .lbl{font:600 11px/16px Manrope,sans-serif;letter-spacing:.4px;text-transform:uppercase;color:#48454E}.as-pane .chip-on{background:#E3DFFF;border-color:#E3DFFF;color:#191836}
.as-mi{display:flex;width:100%;gap:12px;align-items:center;padding:6px 12px;font:inherit;font-size:13px;color:inherit;background:none;border:0;cursor:pointer}.as-mi:hover{background:rgba(53,48,126,.06)}.as-mi:focus-visible{outline:2px solid #35307E;outline-offset:-2px}.tgl{position:relative;flex:none;width:36px;height:20px;border-radius:10px;background:#E6E0EC;border:2px solid #79757F;box-sizing:border-box;transition:background .15s,border-color .15s}.tgl-t{position:absolute;top:50%;left:3px;width:10px;height:10px;margin-top:-5px;border-radius:50%;background:#79757F;transition:left .15s,width .15s,height .15s,margin .15s,background .15s}.as-mi[aria-checked="true"] .tgl{background:#35307E;border-color:#35307E}.as-mi[aria-checked="true"] .tgl-t{left:18px;width:14px;height:14px;margin-top:-7px;background:#FFFFFF}.as-mi:hover .tgl-t{background:#49454F}.as-mi[aria-checked="true"]:hover .tgl-t{background:#ECE5F4}@media (prefers-reduced-motion: reduce){.tgl,.tgl-t{transition:none}}
.lnk{border:0;background:transparent;padding:0;color:#35307E;font-size:13px;font-weight:600;cursor:pointer;text-decoration:underline;text-underline-offset:3px}
@container win (max-width: 1199px){.as-pane{position:absolute;top:0;right:0;bottom:0;width:100%;max-height:none;z-index:25;border-left:0}}
"""
