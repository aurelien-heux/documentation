"""Build CatalogLab.dc.html (v2, minimal): the Catalog, a rail destination where people publish and use skills, and
where the platform publishes tools (Deploy environment, Create Jira ticket…) and MCP servers (DevOps, Knowledge base),
for the assistant and for Sweep. Minimal by default: a card is a name, one line and who made it; status and actions
appear only where they decide something. The skill publication process is explicit: Write · Test · Submit · Review ·
Published. Screens: Catalog (Browse · Mine), an item page, Publish a skill (the process), Administration › Core ›
Catalog (Review · Items · Policies) and Administration › Sweep › Tools and skills (per phase). View as user, champion
or platform admin."""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
import shell as S, navgen as N
dst = sys.argv[1]
HERE = os.path.dirname(__file__)
CSS_LAB = re.search(r'CSS_LAB = r"""(.*?)"""', open(os.path.join(HERE, 'admin_lab_build.py'), encoding='utf-8').read(), re.S)[1]

ST = 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
BACK = f'<svg width="18" height="18" viewBox="0 0 24 24" {ST}><path d="M15 6l-6 6 6 6"/></svg>'
PLUS = f'<svg width="18" height="18" viewBox="0 0 24 24" {ST}><path d="M12 5v14M5 12h14"/></svg>'
CHECK = f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5L20 7"/></svg>'
SEARCH = f'<svg width="18" height="18" viewBox="0 0 24 24" {ST}><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>'
LOCK = f'<svg width="18" height="18" viewBox="0 0 24 24" {ST}><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>'
MARK_SWEEP = N.mark('sweep', N.LIGHT, 22)
MARK_NEW = N.mark('new', N.LIGHT, 22)

CSS_CAT = r"""
.kind{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:10px;flex:none;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:11px;font-weight:800;letter-spacing:.3px}
.k-skill{background:#E3DFFF;color:#14085E}.k-tool{background:#C3F4DC;color:#00391E}.k-mcp{background:#9CF1F0;color:#002020}
.cat-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.ccard{display:flex;flex-direction:column;gap:8px;padding:16px;border-radius:12px;background:#FFFFFF;border:1px solid #E6E0EC;text-align:left;font:inherit;color:inherit;cursor:pointer;min-width:0}
.ccard:hover{border-color:#CAC4CF;background:#FDF8FD}.ccard:focus-visible{outline-offset:-3px}
.ccard p{margin:0;font-size:13px;line-height:18px;color:#48454E;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.meta{font-size:12px;color:#48454E;white-space:normal}
.seg{display:inline-flex;border:1px solid #79757F;border-radius:16px;overflow:hidden}
.seg button{height:36px;padding:0 14px;border:0;border-left:1px solid #79757F;background:transparent;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:13px;font-weight:600;color:#1C1B1E}
.seg button:first-child{border-left:0}.seg button[aria-pressed="true"]{background:#E3DFFF;color:#191836}
.proc{display:flex;align-items:center;gap:0;flex-wrap:wrap}
.proc .s{display:flex;align-items:center;gap:8px;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:13px;font-weight:600;color:#48454E}
.proc .s b{width:22px;height:22px;border-radius:50%;border:1px solid #CAC4CF;font-size:11px;display:inline-flex;align-items:center;justify-content:center}
.proc .s.on{color:#191836}.proc .s.on b{background:#35307E;border-color:#35307E;color:#fff}
.proc .s.done{color:#48454E}.proc .s.done b{background:#E3DFFF;border-color:#E3DFFF;color:#191836}
.proc .ln{width:28px;height:1px;background:#CAC4CF;margin:0 8px}
.plain{list-style:none;margin:0;padding:0}.plain li{padding:8px 0;border-top:1px solid #ECE5F4;font-size:14px;line-height:20px;display:flex;gap:10px;align-items:baseline}.plain li:first-child{border-top:0}
.pane{border:1px solid #CAC4CF;border-radius:12px;background:#FAF4FF;display:flex;flex-direction:column;gap:12px;padding:16px;min-width:0}
.bub{align-self:flex-end;max-width:80%;padding:10px 14px;border-radius:16px 16px 4px 16px;background:#E3DFFF;color:#191836;font-size:14px;line-height:20px}
.trace{border:1px solid #CAC4CF;border-radius:12px;padding:10px 12px;font-size:13px;display:flex;flex-direction:column;gap:6px;background:#FFFFFF}
.lnk{border:0;background:transparent;padding:0;color:#35307E;font-size:13px;font-weight:600;cursor:pointer;text-decoration:underline;text-underline-offset:3px}
.radio{display:flex;gap:12px;align-items:flex-start;padding:12px 14px;border:1px solid #CAC4CF;border-radius:12px;cursor:pointer;font-size:14px;line-height:18px}
.radio input{margin:2px 0 0;width:18px;height:18px;accent-color:#35307E;flex:none}.radio.on{border-color:#35307E;background:#F2EBFA}
.cb{width:18px;height:18px;accent-color:#35307E;margin:0}
.phase-tbl .td{text-align:center}.phase-tbl .td:first-child{text-align:left}
.narrow{max-width:760px}
.pstep{display:flex;gap:14px;align-items:flex-start;padding:10px 0;border-top:1px solid #ECE5F4}.pstep:first-of-type{border-top:0}
.pstep .num{width:24px;height:24px;flex:none;border-radius:50%;background:#E3DFFF;color:#14085E;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:700;display:inline-flex;align-items:center;justify-content:center}
@container win (max-width: 1199px){.cat-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important}.r-split{grid-template-columns:minmax(0,1fr)!important}}
@container win (max-width: 839px){.cat-grid{grid-template-columns:minmax(0,1fr)!important}.proc .s span{display:none}.proc .ln{width:16px}}
@container win (max-width: 599px){.ccard{padding:12px}.bub{max-width:100%}.seg button{padding:0 10px}}
"""

# ---------------------------------------------------------------------------
# Catalog: Browse · Mine
# ---------------------------------------------------------------------------
CARD = ('<sc-for list="{{items}}" as="it" hint-placeholder-count="6"><button type="button" class="ccard" onClick="{{it.open}}">'
        '<div class="row" style="gap: 10px; min-width: 0"><span class="kind {{it.kcls}}">{{it.kab}}</span><div class="ui" style="flex: 1; min-width: 0; font-size: 15px; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis">{{it.name}}</div></div>'
        '<p>{{it.desc}}</p>'
        '<div class="row" style="gap: 8px; margin-top: auto"><span class="meta">{{it.byShort}}</span><span style="flex: 1"></span><span class="meta">{{it.usageShort}}</span></div>'
        '</button></sc-for>')

CATALOG = '''<sc-if value="{{sCatalog}}" hint-placeholder-val="{{true}}"><div class="stack" style="gap: 16px">
  <div class="row r-wrap" style="gap: 0; border-bottom: 1px solid #CAC4CF"><div role="tablist" aria-label="Catalog" style="display: flex; gap: 0"><sc-for list="{{cTabs}}" as="t" hint-placeholder-count="2"><button type="button" role="tab" class="tab {{t.cls}}" aria-selected="{{t.on}}" onClick="{{t.pick}}">{{t.label}}<sc-if value="{{t.hasN}}" hint-placeholder-val="{{false}}"><span class="n">{{t.n}}</span></sc-if></button></sc-for></div><span style="flex: 1"></span><button type="button" class="btn f btn-i" onClick="{{goNew}}">''' + PLUS + '''New skill</button></div>
  <sc-if value="{{tBrowse}}" hint-placeholder-val="{{true}}">
  <div class="row r-wrap" style="gap: 12px"><div class="seg" role="group" aria-label="Kind"><sc-for list="{{kindChips}}" as="c" hint-placeholder-count="4"><button type="button" aria-pressed="{{c.on}}" onClick="{{c.pick}}">{{c.label}}</button></sc-for></div><span style="flex: 1"></span><div class="fld ad-search" style="min-height: 40px; padding: 8px 12px; width: 280px"><label for="cat-q">Search</label><div class="row" style="gap: 8px">''' + SEARCH + '''<input id="cat-q" type="text" placeholder="Name, tool, team…"></div></div></div>
  <div class="cat-grid">''' + CARD + '''</div>
  </sc-if>
  <sc-if value="{{tMine}}" hint-placeholder-val="{{false}}">
  <div class="card" style="padding: 0; overflow: hidden"><div class="ad-tscroll"><table class="ad-tbl" style="width: 100%; border-collapse: collapse">
    <thead><tr><th class="th">Skill</th><th class="th">Stage</th><th class="th">Who can use it</th><th class="th">Version</th><th class="th"></th></tr></thead>
    <tbody><sc-for list="{{mine}}" as="it" hint-placeholder-count="3"><tr class="rw"><td class="td"><b class="ui">{{it.name}}</b><div class="meta">{{it.usageShort}}</div></td><td class="td"><span class="tile {{it.stTile}}"><i></i>{{it.stage}}</span></td><td class="td"><span style="font-size: 13px">{{it.audience}}</span></td><td class="td"><span class="mono" style="font-size: 13px">{{it.version}}</span></td><td class="td" style="text-align: right"><button type="button" class="chip" style="height: 28px" onClick="{{it.next}}">{{it.nextLabel}}</button></td></tr></sc-for></tbody></table></div></div>
  </sc-if>
</div></sc-if>'''

# ---------------------------------------------------------------------------
# Item page: one column, one action
# ---------------------------------------------------------------------------
ITEM = '''<sc-if value="{{sItem}}" hint-placeholder-val="{{false}}"><div class="stack narrow" style="gap: 20px">
  ''' + S.subheader('{{goCatalog}}', 'Back to the Catalog', '{{sk.name}}', ctx='{{sk.kind}} by {{sk.by}} · {{sk.version}}', lead='<span class="kind {{sk.kcls}}">{{sk.kab}}</span>', actions='<sc-if value="{{sk.forAssistant}}" hint-placeholder-val="{{true}}"><button type="button" class="btn {{sk.addCls}} btn-i" aria-pressed="{{sk.added}}" onClick="{{sk.toggleAdd}}"><sc-if value="{{sk.added}}" hint-placeholder-val="{{false}}">' + CHECK + '</sc-if>{{sk.addLabel}}</button></sc-if>') + '''
  <p style="margin: 0; font-size: 15px; line-height: 22px">{{sk.desc}}</p>
  <sc-if value="{{sk.writes}}" hint-placeholder-val="{{false}}"><div class="row" style="gap: 8px; font-size: 13px; color: #48454E">''' + LOCK + '''<span>{{sk.writeNote}}</span></div></sc-if>
  <sc-if value="{{sk.hasEx}}" hint-placeholder-val="{{true}}"><div class="stack" style="gap: 6px"><div class="ui" style="font-size: 13px; font-weight: 700; color: #48454E">Try asking</div><ul class="plain"><sc-for list="{{sk.examples}}" as="e" hint-placeholder-count="2"><li><span style="flex: 1">“{{e.text}}”</span><button type="button" class="lnk" onClick="{{e.tryIt}}">Try it</button></li></sc-for></ul></div></sc-if>
  <div class="stack" style="gap: 6px"><div class="ui" style="font-size: 13px; font-weight: 700; color: #48454E">{{sk.toolsTitle}}</div><ul class="plain"><sc-for list="{{sk.tools}}" as="t" hint-placeholder-count="3"><li><span style="flex: 1">{{t.name}}</span><span class="meta">{{t.note}}</span></li></sc-for></ul></div>
  ''' + S.qa_block('sk') + '''
  <div class="row r-wrap" style="gap: 8px"><span class="meta">{{sk.foot}}</span><span style="flex: 1"></span><button type="button" class="lnk" onClick="{{reportIt}}">Report a problem</button></div>
</div></sc-if>'''

# ---------------------------------------------------------------------------
# Publish a skill: Write · Test · Submit · Review · Published
# ---------------------------------------------------------------------------
PROC = '<div class="proc" aria-label="Publication process"><sc-for list="{{proc}}" as="p" hint-placeholder-count="5"><span class="s {{p.cls}}" aria-current="{{p.cur}}"><b>{{p.n}}</b><span>{{p.label}}</span></span><sc-if value="{{p.more}}" hint-placeholder-val="{{true}}"><span class="ln"></span></sc-if></sc-for></div>'

NEWSKILL = '''<sc-if value="{{sNew}}" hint-placeholder-val="{{false}}"><div class="stack" style="gap: 20px">
  ''' + S.subheader('{{goCatalog}}', 'Back to the Catalog', 'Publish a skill', ctx='Your skill: {{nsNameOr}}', actions=PROC) + '''
  <sc-if value="{{nWrite}}" hint-placeholder-val="{{true}}"><div class="card stack narrow" style="gap: 16px; padding: 24px">
    <div class="h2">Write</div>
    <div class="fld"><label for="ns-name">Name</label><input id="ns-name" type="text" value="{{nsName}}" onChange="{{onNsName}}" placeholder="Short, says what it does"></div>
    <div class="fld"><label for="ns-desc">One line</label><input id="ns-desc" type="text" value="{{nsDesc}}" onChange="{{onNsDesc}}" placeholder="Shown in the Catalog and in the assistant’s Tools menu"></div>
    <div class="fld" style="min-height: 150px"><label for="ns-body">Instructions</label><textarea id="ns-body" rows="6" value="{{nsBody}}" onChange="{{onNsBody}}" placeholder="How to proceed, step by step. Say when to stop and ask."></textarea></div>
    <div class="stack" style="gap: 8px"><span class="meta">Tools it may use</span><div class="row r-wrap" style="gap: 8px"><sc-for list="{{toolChips}}" as="t" hint-placeholder-count="6"><button type="button" class="chip" aria-pressed="{{t.on}}" style="{{t.style}}" onClick="{{t.pick}}"><sc-if value="{{t.on}}" hint-placeholder-val="{{false}}">''' + CHECK + '''</sc-if>{{t.label}}</button></sc-for></div></div>
    <div class="fld" style="min-height: 44px; padding: 10px 12px"><label for="ns-ex1">Example request</label><input id="ns-ex1" type="text" value="{{nsEx1}}" onChange="{{onNsEx1}}"></div>
    <div class="row r-wrap" style="gap: 8px"><button type="button" class="lnk" onClick="{{pickSrcGit}}">{{srcLink}}</button><span style="flex: 1"></span><button type="button" class="btn x" onClick="{{saveDraft}}">Save draft</button><button type="button" class="btn f" onClick="{{toTest}}">Test it</button></div>
  </div></sc-if>
  <sc-if value="{{nTest}}" hint-placeholder-val="{{false}}"><div class="r-split" style="display: grid; grid-template-columns: minmax(0, 1fr) 360px; gap: 24px; align-items: start">
    <div class="stack" style="gap: 10px"><div class="h2">Test</div><span class="meta">The assistant with your skill on, for this conversation only.</span>
      <div class="pane"><div class="bub">{{nsEx1Or}}</div>
        <div class="trace"><b class="ui" style="font-size: 13px">Used {{tryN}} tools</b><sc-for list="{{tryTools}}" as="t" hint-placeholder-count="2"><div class="row" style="gap: 8px"><span style="flex: 1">{{t.name}}</span><span class="meta">{{t.st}}</span></div></sc-for></div>
        <sc-if value="{{tryNeedsAppr}}" hint-placeholder-val="{{false}}"><div class="card" style="border: 1px solid #79757F; box-shadow: none; background: #F2EBFA; display: flex; flex-direction: column; gap: 8px"><div class="row" style="gap: 8px">''' + LOCK + '''<b class="ui" style="font-size: 14px">{{tryApprQ}}</b></div><div class="mono" style="font-size: 12px; color: #48454E">{{tryApprArgs}}</div><div class="row" style="justify-content: flex-end; gap: 8px"><button type="button" class="btn x sm">Don’t run</button><button type="button" class="btn f sm" onClick="{{tryApprove}}">Run</button></div></div></sc-if>
        <div style="font-size: 14px; line-height: 20px">{{tryAnswer}}</div>
      </div>
    </div>
    <div class="stack" style="gap: 10px"><div class="h2" style="font-size: 16px">Checks</div><ul class="plain"><sc-for list="{{checks}}" as="c" hint-placeholder-count="4"><li><span style="width: 20px; color: {{c.color}}">{{c.icon}}</span><span style="flex: 1">{{c.label}}<span class="meta" style="display: block">{{c.note}}</span></span></li></sc-for></ul>
      <div class="row" style="gap: 8px; justify-content: flex-end"><button type="button" class="btn x" onClick="{{toWrite}}">Edit</button><button type="button" class="btn f" onClick="{{toSubmit}}">Continue</button></div></div>
  </div></sc-if>
  <sc-if value="{{nSubmit}}" hint-placeholder-val="{{false}}"><div class="card stack narrow" style="gap: 14px; padding: 24px">
    <div class="h2">Submit</div><span class="meta">Who can use it</span>
    <sc-for list="{{scopes}}" as="sc" hint-placeholder-count="3"><label class="radio {{sc.cls}}"><input type="radio" name="ns-scope" checked="{{sc.on}}" onChange="{{sc.pick}}"><span style="flex: 1"><b class="ui">{{sc.label}}</b><br><span class="meta">{{sc.note}}</span></span></label></sc-for>
    <sc-if value="{{scopeOrg}}" hint-placeholder-val="{{false}}"><div class="fld" style="min-height: 72px"><label for="ns-note">Note for the reviewer</label><textarea id="ns-note" rows="2" placeholder="What it is for, who tried it"></textarea></div></sc-if>
    <div class="row" style="gap: 8px; justify-content: flex-end"><button type="button" class="btn x" onClick="{{toTest}}">Back</button><button type="button" class="btn f" onClick="{{submit}}">{{submitCta}}</button></div>
  </div></sc-if>
  <sc-if value="{{nReview}}" hint-placeholder-val="{{false}}"><div class="card stack narrow" style="gap: 12px; padding: 24px">
    <div class="h2">In review</div>
    <p style="margin: 0; font-size: 14px; line-height: 20px">A platform admin reviews “{{nsNameOr}}”. You are notified; until then it stays usable by you.</p>
    <div class="row" style="gap: 8px"><button type="button" class="btn t" onClick="{{openMine}}">Open in Mine</button><span style="flex: 1"></span><button type="button" class="lnk" onClick="{{simulateApprove}}">Simulate approval</button></div>
  </div></sc-if>
  <sc-if value="{{nDone}}" hint-placeholder-val="{{false}}"><div class="card stack narrow" style="gap: 12px; padding: 24px">
    <div class="h2">Published</div>
    <p style="margin: 0; font-size: 14px; line-height: 20px">{{doneText}}</p>
    <div class="row" style="gap: 8px"><button type="button" class="btn f" onClick="{{openMine}}">Open in Mine</button><button type="button" class="btn x" onClick="{{goCatalog}}">Back to the Catalog</button></div>
  </div></sc-if>
</div></sc-if>'''

# ---------------------------------------------------------------------------
# Administration
# ---------------------------------------------------------------------------
ADMIN_TREE = (f'<nav class="ad-side" aria-label="Administration"><sc-for list="{{{{groups}}}}" as="g" hint-placeholder-count="3"><div class="ad-g"><div class="ad-gh"><sc-if value="{{{{g.isSweep}}}}" hint-placeholder-val="{{{{false}}}}">{MARK_SWEEP}</sc-if><sc-if value="{{{{g.isNew}}}}" hint-placeholder-val="{{{{false}}}}">{MARK_NEW}</sc-if><span>{{{{g.label}}}}</span></div>'
              '<sc-for list="{{g.items}}" as="s" hint-placeholder-count="5"><a href="#cl-{{s.key}}" class="ad-ni {{s.cls}}" aria-current="{{s.cur}}" onClick="{{s.pick}}"><span style="flex: 1">{{s.label}}</span><sc-if value="{{s.hasN}}" hint-placeholder-val="{{false}}"><span class="n">{{s.n}}</span></sc-if></a></sc-for></div></sc-for></nav>')

REVIEW = '''<sc-if value="{{aReview}}" hint-placeholder-val="{{true}}">
  <sc-if value="{{rvList}}" hint-placeholder-val="{{true}}">
  <div class="card" style="padding: 0; overflow: hidden"><div class="ad-tscroll"><table class="ad-tbl" style="width: 100%; border-collapse: collapse">
    <thead><tr><th class="th">Skill</th><th class="th">Author</th><th class="th">Submitted</th><th class="th"></th></tr></thead>
    <tbody><sc-for list="{{queue}}" as="q" hint-placeholder-count="3"><tr class="rw"><td class="td"><b class="ui">{{q.name}}</b><div class="meta">{{q.desc}}</div></td><td class="td"><span style="font-size: 13px">{{q.by}}</span></td><td class="td"><span class="meta">{{q.when}}</span></td><td class="td" style="text-align: right"><button type="button" class="chip" style="height: 28px" onClick="{{q.open}}">Review</button></td></tr></sc-for></tbody></table></div></div>
  </sc-if>
  <sc-if value="{{rvOpen}}" hint-placeholder-val="{{false}}"><div class="stack narrow" style="gap: 16px">
    ''' + S.subheader('{{rvBack}}', 'Back to the review queue', '{{rv.name}}', ctx='{{rv.by}} · {{rv.when}}') + '''
    <div class="stack" style="gap: 6px"><div class="ui" style="font-size: 13px; font-weight: 700; color: #48454E">Instructions</div><div style="font-size: 14px; line-height: 20px; white-space: pre-line">{{rv.body}}</div><span class="meta">Uses {{rv.tools}} · {{rv.note}}</span></div>
    <div class="stack" style="gap: 8px"><div class="ui" style="font-size: 13px; font-weight: 700; color: #48454E">Before publishing</div><sc-for list="{{rvChecks}}" as="c" hint-placeholder-count="3"><label class="row" style="gap: 10px; font-size: 14px; cursor: pointer"><input type="checkbox" class="cb" checked="{{c.on}}" onChange="{{c.toggle}}"><span style="flex: 1">{{c.label}}</span></label></sc-for></div>
    ''' + S.qa_block('rv') + '''
    <div class="row r-wrap" style="gap: 8px; justify-content: flex-end"><button type="button" class="btn x" onClick="{{rvChanges}}">Ask for changes</button><button type="button" class="btn f" aria-disabled="{{rvNotReady}}" onClick="{{rvPublish}}">Publish</button></div>
  </div></sc-if>
</sc-if>'''

ITEMS_T = '''<sc-if value="{{aItems}}" hint-placeholder-val="{{false}}">
  <div class="row r-wrap" style="gap: 12px"><div class="seg" role="group" aria-label="Kind"><sc-for list="{{kindChips}}" as="c" hint-placeholder-count="4"><button type="button" aria-pressed="{{c.on}}" onClick="{{c.pick}}">{{c.label}}</button></sc-for></div><span style="flex: 1"></span><button type="button" class="btn t btn-i">''' + PLUS + '''Add tool or MCP server</button></div>
  <div class="card" style="padding: 0; overflow: hidden"><div class="ad-tscroll"><table class="ad-tbl" style="width: 100%; border-collapse: collapse">
    <thead><tr><th class="th">Item</th><th class="th">Owner</th><th class="th">Who can use it</th><th class="th">Uses · 30 days</th><th class="th"></th></tr></thead>
    <tbody><sc-for list="{{adminItems}}" as="it" hint-placeholder-count="8"><tr class="rw"><td class="td"><div class="row" style="gap: 10px"><span class="kind {{it.kcls}}" style="width: 30px; height: 30px; font-size: 10px; border-radius: 8px">{{it.kab}}</span><b class="ui">{{it.name}}</b></div></td><td class="td"><span style="font-size: 13px">{{it.byShort}}</span></td><td class="td"><span style="font-size: 13px">{{it.audience}}</span></td><td class="td">{{it.usage}}</td><td class="td" style="text-align: right"><button type="button" class="chip" style="height: 28px" onClick="{{it.open}}">Open</button></td></tr></sc-for></tbody></table></div></div>
</sc-if>'''

POLICIES = '''<sc-if value="{{aPolicies}}" hint-placeholder-val="{{false}}"><div class="stack narrow" style="gap: 20px">
  <div class="stack" style="gap: 6px"><div class="h2">Who can publish</div><ul class="plain">
    <li><span style="flex: 1">Skills for yourself or your team</span><span class="meta">Everyone · automatic checks</span></li>
    <li><span style="flex: 1">Skills for everyone</span><span class="meta">After review by a champion or a platform admin</span></li>
    <li><span style="flex: 1">Tools and MCP servers</span><span class="meta">Platform team</span></li></ul></div>
  <div class="stack" style="gap: 6px"><div class="h2">Actions that change something</div><span class="meta">The most a user can allow. Users can only be stricter.</span>
    <div class="card" style="padding: 0; overflow: hidden; margin-top: 6px"><div class="ad-tscroll"><table class="ad-tbl" style="width: 100%; border-collapse: collapse">
      <thead><tr><th class="th">Action</th><th class="th">Assistant</th><th class="th">Sweep runs</th></tr></thead>
      <tbody><sc-for list="{{policyRows}}" as="p" hint-placeholder-count="5"><tr class="rw"><td class="td"><b class="ui">{{p.name}}</b><div class="meta">{{p.src}}</div></td><td class="td"><select class="sel sel-s" aria-label="Assistant ceiling for {{p.name}}" value="{{p.a}}" onChange="{{p.onA}}"><option value="ask">Ask first</option><option value="always">Allowed</option><option value="off">Off</option></select></td><td class="td"><select class="sel sel-s" aria-label="Sweep ceiling for {{p.name}}" value="{{p.s}}" onChange="{{p.onS}}"><option value="ask">Ask first</option><option value="always">Allowed</option><option value="off">Off</option></select></td></tr></sc-for></tbody></table></div></div>
    <span class="meta">Reading (searching the knowledge base, reading logs and pipelines) is allowed everywhere.</span></div>
</div></sc-if>'''

SWEEP_TOOLS = '''<sc-if value="{{aSweep}}" hint-placeholder-val="{{false}}">
  <div class="row r-wrap" style="gap: 8px"><span style="flex: 1"></span><button type="button" class="btn t btn-i" onClick="{{goCatalog}}">''' + PLUS + '''Add from the Catalog</button></div>
  <div class="card" style="padding: 0; overflow: hidden"><div class="ad-tscroll"><table class="ad-tbl phase-tbl" style="width: 100%; border-collapse: collapse">
    <thead><tr><th class="th">Item</th><sc-for list="{{phases}}" as="p" hint-placeholder-count="4"><th class="th" style="text-align: center">{{p}}</th></sc-for></tr></thead>
    <tbody><sc-for list="{{sweepRows}}" as="r" hint-placeholder-count="6"><tr class="rw"><td class="td"><div class="row" style="gap: 10px"><span class="kind {{r.kcls}}" style="width: 30px; height: 30px; font-size: 10px; border-radius: 8px">{{r.kab}}</span><b class="ui">{{r.name}}</b></div></td><sc-for list="{{r.cells}}" as="c" hint-placeholder-count="4"><td class="td"><input type="checkbox" class="cb" aria-label="{{c.aria}}" checked="{{c.on}}" onChange="{{c.toggle}}"></td></sc-for></tr></sc-for></tbody></table></div></div>
</sc-if>'''

ADMIN = ('<sc-if value="{{sAdmin}}" hint-placeholder-val="{{false}}"><div class="ad-split">' + ADMIN_TREE + S.ADMIN_SELECT +
         '<div class="stack" style="gap: 16px; min-width: 0">'
         '<sc-if value="{{aCatalog}}" hint-placeholder-val="{{true}}"><div class="row r-wrap" role="tablist" aria-label="Catalog" style="gap: 0; border-bottom: 1px solid #CAC4CF"><sc-for list="{{aTabs}}" as="t" hint-placeholder-count="3"><button type="button" role="tab" class="tab {{t.cls}}" aria-selected="{{t.on}}" onClick="{{t.pick}}">{{t.label}}<sc-if value="{{t.hasN}}" hint-placeholder-val="{{false}}"><span class="n">{{t.n}}</span></sc-if></button></sc-for></div></sc-if>'
         + REVIEW + ITEMS_T + POLICIES + SWEEP_TOOLS +
         '<sc-if value="{{aOther}}" hint-placeholder-val="{{false}}">' + S.ADMIN_PLACEHOLDER + '</sc-if>'
         '</div></div></sc-if>')

PROCESS_DOC = '''<div class="card stack" style="gap: 4px; padding: 20px">
        <div class="row r-wrap" style="justify-content: space-between; margin-bottom: 6px"><span class="h2">Skill publication process</span><span class="meta">the same for a new skill and a new version</span></div>
        <div class="pstep"><span class="num">1</span><div><b class="ui">Write</b><div class="meta">In the app, or from a Git repository (SKILL.md and skill.json; versions follow tags). A draft is usable by its author only.</div></div></div>
        <div class="pstep"><span class="num">2</span><div><b class="ui">Test</b><div class="meta">Automatic checks: the manifest, no secrets in the text, every tool exists, and whether it changes something (worked out from its tools). Then one try in the assistant with the skill on. Both are required to continue.</div></div></div>
        <div class="pstep"><span class="num">3</span><div><b class="ui">Submit</b><div class="meta">Pick who can use it: just you, your team (live at once; the team is responsible), or everyone (goes to review).</div></div></div>
        <div class="pstep"><span class="num">4</span><div><b class="ui">Review</b><div class="meta">For everyone only. A champion or a platform admin tries it, ticks three points, talks with the author in the skill’s discussion, then publishes or asks for changes. Target: 2 working days.</div></div></div>
        <div class="pstep"><span class="num">5</span><div><b class="ui">Published</b><div class="meta">In the Catalog and the assistant’s Tools menu; admins can turn it on for Sweep phases. A new version goes through Test again, and back to Review only if it adds an action that changes something. Retiring a skill names its successor and gives users 30 days.</div></div></div>
      </div>'''

BODY = '''<div style="width: 1440px; min-height: 2000px; box-sizing: border-box; background: #FDF8FD; color: #1C1B1E; display: flex; flex-direction: column">
  <div style="padding: 20px 32px 12px; display: flex; flex-direction: column; gap: 12px">
    <div style="display: flex; align-items: center; gap: 16px">
      <h1 class="ui" style="margin: 0; font-size: 24px; line-height: 32px; font-weight: 700; white-space: nowrap">Catalog lab</h1>
      <span style="font-size: 14px; color: #48454E">Skills, tools and MCP servers for the assistant and for Sweep, in a minimal interface: a card is a name, one line and who made it; status and actions appear only where they decide something. People publish skills through a five-step process; the platform publishes tools (Deploy environment, Create Jira ticket…) and MCP servers (DevOps, Knowledge base). Pick a screen and a role; press Play.</span>
    </div>
    <div class="row" style="gap: 12px; flex-wrap: wrap">SIMBAR<span class="row r-wrap" style="gap: 8px; padding: 6px 8px 6px 12px; border: 1px dashed #79757F; border-radius: 12px"><span class="ui" style="font-size: 12px; font-weight: 600; color: #48454E">Screen</span><sc-for list="{{screenChips}}" as="r" hint-placeholder-count="5"><button type="button" class="chip" style="height: 28px; font-size: 12px; {{r.style}}" aria-pressed="{{r.on}}" onClick="{{r.pick}}">{{r.label}}</button></sc-for></span><span class="row" style="gap: 8px; padding: 6px 8px 6px 12px; border: 1px dashed #79757F; border-radius: 12px"><span class="ui" style="font-size: 12px; font-weight: 600; color: #48454E">View as</span><sc-for list="{{roleChips}}" as="r" hint-placeholder-count="3"><button type="button" class="chip" style="height: 28px; font-size: 12px; {{r.style}}" aria-pressed="{{r.on}}" onClick="{{r.pick}}">{{r.label}}</button></sc-for></span></div>
  </div>

  <div style="margin: 0 32px; border-radius: 12px; overflow: hidden; border: 1px solid #CAC4CF">
  SIMOPEN
  <div style="position: relative; width: 100%; height: 100%; display: flex; flex-direction: column; background: #FDF8FD; overflow: hidden">
    HEADER
    <div style="flex: 1; display: flex; min-height: 0">
      <sc-if value="{{railCat}}" hint-placeholder-val="{{true}}"><div class="ad-railwrap">RAIL_CAT</div></sc-if><sc-if value="{{railAdm}}" hint-placeholder-val="{{false}}"><div class="ad-railwrap">RAIL_ADM</div></sc-if>
      <main style="position: relative; flex: 1; min-width: 0; padding: 20px 32px 24px; box-sizing: border-box; display: flex; flex-direction: column; gap: 16px; overflow: auto">
        <div aria-live="polite" style="position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0)">{{live}}</div>
        @@CATALOG@@ @@ITEM@@ @@NEWSKILL@@ @@ADMIN@@
        <sc-if value="{{hasSnack}}" hint-placeholder-val="{{false}}"><div role="status" style="position: sticky; bottom: 8px; align-self: flex-start; display: flex; align-items: center; gap: 16px; padding: 12px 16px; border-radius: 8px; background: #322F35; color: #F5EFF7; font-size: 14px; box-shadow: 0 4px 8px 3px rgba(0,0,0,.15)">{{snack}}<button type="button" class="ib" aria-label="Dismiss" style="margin: -8px -8px -8px 0; color: #F5EFF7" onClick="{{closeSnack}}">✕</button></div></sc-if>
      </main>
    </div>
    NAVBAR
  </div>
  SIMCLOSE
  </div>

  <div style="padding: 20px 32px 32px; display: grid; grid-template-columns: minmax(0, 1fr) 460px; gap: 24px; align-items: start">
    ''' + PROCESS_DOC + '''
    <div style="display: flex; flex-direction: column; gap: 16px">
      <div class="card stack" style="gap: 8px; padding: 20px"><span class="h2">What is in the Catalog</span>
        <ul class="plain">
          <li><span class="kind k-mcp" style="width: 30px; height: 30px; font-size: 10px; border-radius: 8px">MCP</span><span style="flex: 1"><b class="ui">DevOps</b><span class="meta" style="display: block">Pipelines, builds, deployments, pull requests</span></span></li>
          <li><span class="kind k-mcp" style="width: 30px; height: 30px; font-size: 10px; border-radius: 8px">MCP</span><span style="flex: 1"><b class="ui">Knowledge base</b><span class="meta" style="display: block">Docs, runbooks, architecture model, ARB decisions</span></span></li>
          <li><span class="kind k-tool" style="width: 30px; height: 30px; font-size: 10px; border-radius: 8px">TL</span><span style="flex: 1"><b class="ui">Deploy environment · Reserve environment</b><span class="meta" style="display: block">From Environments; they change something, so they ask first</span></span></li>
          <li><span class="kind k-tool" style="width: 30px; height: 30px; font-size: 10px; border-radius: 8px">TL</span><span style="flex: 1"><b class="ui">Create Jira ticket</b><span class="meta" style="display: block">With the run or the conversation as context</span></span></li>
          <li><span class="kind k-skill" style="width: 30px; height: 30px; font-size: 10px; border-radius: 8px">SK</span><span style="flex: 1"><b class="ui">Skills</b><span class="meta" style="display: block">Published by people: migrations, runbooks, reviews, release notes</span></span></li>
        </ul></div>
      <div class="ocard" style="font-size: 13px; line-height: 18px; color: #48454E"><b style="color: #1C1B1E">Minimal by default.</b> No tags on cards. The item page has one action (Add to my assistant) and says in one line when the item can change something. Reviewed, usage and source sit in one line of metadata. Filters are a kind switch and a search.</div>
    </div>
  </div>
</div>'''

LOGIC = r'''
class Component extends DCLogic {
  constructor(props) { super(props); this.simHostId = 'sim-host-cl'; this.simDefault = 1374; this.state = { screen: 'catalog', tab: 'browse', role: 'user', kind: 'all', skill: null, added: { s2: true, m2: true }, step: 1, nsName: '', nsDesc: '', nsBody: '', nsEx1: '', nsTools: { t_logs: true, t_jira: true }, src: 'app', scope: 'team', tryAppr: false, published: null, adminPage: 'catalog', aTab: 'review', rv: null, rvChecks: {}, pol: {}, sweepOn: { s1: { implement: true }, m1: { implement: true, test: true }, m2: { implement: true, review: true }, t1: { release: true }, t3: { review: true, test: true } }, snack: null, live: '', simW: null, simAvail: 0 }; }
/*SIMJS*/
/*ADMINJS*/
/*QAJS*/
  componentDidMount() { var self = this; this.simSync(); if (typeof window !== 'undefined') window.addEventListener('resize', function () { self.simSync(); }); }
  componentDidUpdate() { this.simSync(); this.qaFocusSync(); }
  renderVals() {
    var s = this.state, self = this, sim = this.simVals();
    var set = function (o) { return function (e) { if (e && e.preventDefault) e.preventDefault(); self.setState(typeof o === 'function' ? o(e) : o); }; };
    var val = function (e) { return e && e.target ? e.target.value : ''; };
    var ON = 'background: #E3DFFF; border-color: #E3DFFF; color: #191836';
    var role = s.role, platform = role === 'platform', champion = role === 'champion';
    var ME = { user: { who: 'Priya Sharma', team: 'Request' }, champion: { who: 'Marta Kowalski', team: 'Client' }, platform: { who: 'Aurélien Heux', team: 'Platform' } }[role];

    // ---- tools: what skills and runs can call
    var TOOLS = {
      t_deploy: { name: 'Deploy environment', write: true, src: 'Environments' },
      t_reserve: { name: 'Reserve environment', write: true, src: 'Environments' },
      t_jira: { name: 'Create Jira ticket', write: true, src: 'Jira' },
      t_logs: { name: 'Read run logs', write: false, src: 'Sweep' },
      t_pipe: { name: 'Run pipeline', write: true, src: 'DevOps' },
      t_pipestat: { name: 'Read pipeline status', write: false, src: 'DevOps' },
      t_build: { name: 'Read build logs', write: false, src: 'DevOps' },
      t_pr: { name: 'Open pull request', write: true, src: 'DevOps' },
      t_kb: { name: 'Search the knowledge base', write: false, src: 'Knowledge base' },
      t_arch: { name: 'Query the architecture model', write: false, src: 'Knowledge base' }
    };
    var ITEMS = [
      { id: 'm1', kind: 'MCP server', name: 'DevOps', by: 'Platform team', team: 'Platform', aud: 'Everyone', usage: 3100, version: '2.3', tools: ['t_pipestat', 't_build', 't_pipe', 't_pr'], works: ['Assistant', 'Sweep'], desc: 'Pipelines, builds, deployments and pull requests on the DevOps platform. Reading is open; running a pipeline or opening a pull request asks first.', examples: ['Why did the credit-request pipeline fail last night?', 'Re-run the integration stage on build 4821'], source: 'MCP · devops.example.internal', reviewed: true },
      { id: 'm2', kind: 'MCP server', name: 'Knowledge base', by: 'Platform team', team: 'Platform', aud: 'Everyone', usage: 2480, version: '1.4', tools: ['t_kb', 't_arch'], works: ['Assistant', 'Sweep'], desc: 'Docs, runbooks, the architecture model and ARB decisions, searched and read with their source. Reads only.', examples: ['What is the rollback procedure for facility-management?', 'Which modules depend on client-referential?'], source: 'MCP · kb.example.internal', reviewed: true },
      { id: 't1', kind: 'Tool', name: 'Deploy environment', by: 'Environments team', team: 'Release', aud: 'Everyone', usage: 860, version: '1.2', tools: ['t_deploy'], works: ['Assistant', 'Sweep'], desc: 'Deploys a module branch to an environment: checks reservations, opens the auto-merge pull request and follows the first rollout.', examples: ['Deploy credit-request feature/limits to staging-2'], source: 'Built-in · Environments', reviewed: true },
      { id: 't2', kind: 'Tool', name: 'Reserve environment', by: 'Environments team', team: 'Release', aud: 'Everyone', usage: 310, version: '1.2', tools: ['t_reserve'], works: ['Assistant'], desc: 'Reserves an environment for a module until a date, with a reason; extend or release it later.', examples: ['Reserve staging-2 for credit-request until Friday'], source: 'Built-in · Environments', reviewed: true },
      { id: 't3', kind: 'Tool', name: 'Create Jira ticket', by: 'Platform team', team: 'Platform', aud: 'Everyone', usage: 640, version: '2.1', tools: ['t_jira'], works: ['Assistant', 'Sweep'], desc: 'Creates a ticket in the project of the repository, with the run or the conversation attached as context.', examples: ['Open a ticket for the flaky facility export test'], source: 'Jira connector', reviewed: true },
      { id: 's1', kind: 'Skill', name: 'Spring Boot 3 migration', by: 'Marta Kowalski', team: 'Client', aud: 'Everyone', usage: 212, version: '1.4.0', tools: ['t_logs', 't_pipe', 't_pr'], works: ['Assistant', 'Sweep'], desc: 'Upgrades a service to Spring Boot 3, runs the pipeline and opens a pull request with what changed.', examples: ['Migrate credit-request to Spring Boot 3 on a branch'], source: 'Git · client/skill-spring-boot-3', reviewed: true },
      { id: 's2', kind: 'Skill', name: 'Incident runbook', by: 'Lucas Bernard', team: 'Facility', aud: 'Everyone', usage: 188, version: '1.1.0', tools: ['t_kb', 't_logs', 't_jira'], works: ['Assistant'], desc: 'Walks the on-call engineer through the incident checklist with the right runbook, recent logs, and a ticket at the end.', examples: ['Facility exports are failing since 02:00, where do I start?'], source: 'Written in the app', reviewed: true },
      { id: 's3', kind: 'Skill', name: 'Release notes from changelog', by: 'Sami Ben Ali', team: 'Platform', aud: 'Everyone', usage: 356, version: '2.0.1', tools: ['t_pipestat', 't_kb'], works: ['Assistant'], desc: 'Drafts a What’s new entry from the changelog and the pull request summaries.', examples: ['Draft the release notes for 4.6.1'], source: 'Git · platform/skill-release-notes', reviewed: true },
      { id: 's4', kind: 'Skill', name: 'Deploy to staging with checks', by: 'Karim Ouali', team: 'Request', aud: 'Request', usage: 41, version: '0.4.0', tools: ['t_pipestat', 't_reserve', 't_deploy'], works: ['Assistant', 'Sweep'], desc: 'Checks the pipeline is green, reserves a staging environment if needed, deploys, then reports the rollout.', examples: ['Ship my branch to staging'], source: 'Written in the app', reviewed: false },
      { id: 's5', kind: 'Skill', name: 'Flaky test triage', by: 'you', team: 'Request', aud: 'Just you', usage: 6, version: '0.1.0', tools: ['t_logs', 't_jira'], works: ['Assistant'], desc: 'Finds tests that fail only sometimes, groups them by cause and opens one ticket per cause.', examples: ['Which tests were flaky this week on credit-request?'], source: 'Written in the app', mine: true, stage: 'Draft' },
      { id: 's6', kind: 'Skill', name: 'Liquibase changelog review', by: 'Yann Dupont', team: 'Environments', aud: 'Everyone', usage: 0, version: '1.0.0', tools: ['t_kb', 't_jira'], works: ['Assistant', 'Sweep'], desc: 'Reviews a Liquibase changelog: destructive changes, missing rollbacks, naming.', examples: ['Review the changelog in PR #4830'], source: 'Git · environments/skill-liquibase-review', stage: 'In review' }
    ];
    var KAB = { Skill: 'SK', Tool: 'TL', 'MCP server': 'MCP' }, KCLS = { Skill: 'k-skill', Tool: 'k-tool', 'MCP server': 'k-mcp' };
    var writesOf = function (it) { return it.tools.filter(function (k) { return TOOLS[k].write; }); };
    var deco = function (it) { return Object.assign({}, it, { kab: KAB[it.kind], kcls: KCLS[it.kind], byShort: it.kind === 'Skill' ? it.by + ' · ' + it.team : it.by, usageShort: it.usage ? it.usage.toLocaleString('en') + ' uses' : 'Not used yet', audience: it.aud, open: set({ screen: 'item', skill: it.id, snack: null }) }); };
    var published = ITEMS.filter(function (it) { return !it.stage && (it.aud === 'Everyone' || it.aud === ME.team); });
    var KINDS = [ { k: 'all', label: 'All' }, { k: 'Skill', label: 'Skills' }, { k: 'Tool', label: 'Tools' }, { k: 'MCP server', label: 'MCP servers' } ];
    var kindChips = KINDS.map(function (k) { var on = s.kind === k.k; return { label: k.label, on: on, pick: set({ kind: k.k }) }; });
    var browse = published.filter(function (it) { return s.kind === 'all' || it.kind === s.kind; }).sort(function (a, b) { return b.usage - a.usage; }).map(deco);
    var STAGE_TILE = { Draft: 'ne', 'In review': 'wn', Published: 'ok' };
    var mineRaw = ITEMS.filter(function (it) { return it.mine || (role === 'champion' && it.id === 's1') || (role === 'platform' && it.id === 's3'); });
    if (s.published) mineRaw = [ { id: 'sNew', kind: 'Skill', name: s.nsName || 'Flaky test triage', by: 'you', team: ME.team, aud: s.published.aud, usage: 0, version: '1.0.0', tools: [], works: ['Assistant'], desc: s.nsDesc, examples: [], stage: s.published.stage } ].concat(mineRaw.filter(function (it) { return it.id !== 's5'; }));
    var mine = mineRaw.map(function (it) { var st = it.stage || 'Published'; return Object.assign(deco(it), { stage: st, stTile: STAGE_TILE[st], nextLabel: st === 'Draft' ? 'Continue' : st === 'In review' ? 'Open' : 'New version', next: st === 'Draft' ? set({ screen: 'new', step: 1, nsName: it.name, nsDesc: it.desc, nsEx1: it.examples[0] || '', published: null }) : set({ screen: 'item', skill: it.id === 'sNew' ? 's5' : it.id }) }); });
    var cTabs = [ { k: 'browse', label: 'Browse' }, { k: 'mine', label: 'My skills', n: mine.length } ].map(function (t) { var on = s.tab === t.k; return { label: t.label, n: t.n, hasN: !!t.n, on: on, cls: on ? 'tab-on' : '', pick: set({ tab: t.k }) }; });

    // ---- item page
    var skRaw = ITEMS.filter(function (it) { return it.id === s.skill; })[0] || ITEMS[0], sk = deco(skRaw);
    var added = !!s.added[sk.id], writes = writesOf(skRaw);
    var lower = function (t) { return t.charAt(0).toLowerCase() + t.slice(1); };
    Object.assign(sk, {
      by: sk.kind === 'Skill' ? sk.by + ' · ' + sk.team : sk.by, version: 'v' + sk.version,
      forAssistant: sk.works.indexOf('Assistant') >= 0, added: added, addLabel: added ? 'In my assistant' : 'Add to my assistant', addCls: added ? 't' : 'f',
      toggleAdd: set(function () { var a = Object.assign({}, s.added); a[sk.id] = !added; return { added: a, snack: !added ? sk.name + ' is in your assistant’s Tools menu.' : sk.name + ' removed from your assistant.' }; }),
      writes: writes.length > 0, writeNote: 'Asks before it does anything that changes something: ' + writes.map(function (k) { return lower(TOOLS[k].name); }).join(', ') + '.',
      hasEx: sk.examples.length > 0, examples: sk.examples.map(function (t) { return { text: t, tryIt: set({ snack: 'Assistant opened with ' + sk.name + ' on for this conversation.' }) }; }),
      toolsTitle: sk.kind === 'MCP server' ? 'Tools it provides' : sk.kind === 'Tool' ? 'Action' : 'Uses',
      tools: sk.tools.map(function (k) { var t = TOOLS[k]; return { name: t.name, note: (t.write ? 'changes something · ' : '') + t.src }; }),
      foot: [sk.reviewed ? 'Reviewed' : (sk.stage || (sk.aud === 'Everyone' ? '' : 'Shared with ' + sk.aud)), sk.usage ? sk.usage.toLocaleString('en') + ' uses in 30 days' : '', sk.works.join(' and '), sk.source].filter(Boolean).join(' · ')
    });
    var qaAs = platform ? { who: ME.who, role: 'Platform team' } : champion ? { who: ME.who, role: 'Champion' } : null;
    var SKQA = { s1: [ { id: 'skq1', ini: 'YD', bg: '#C3F4DC', who: 'Yann Dupont', when: '2 days ago', d: 2, text: 'Does it handle Spring Security 6 config, or do we do that by hand?', r: [ { id: 'skq1a', ini: 'MK', bg: '#9CF1F0', who: 'Marta Kowalski', role: 'Author', when: 'yesterday', d: 1, text: 'Since 1.4.0 it rewrites the common patterns and stops to ask on anything custom.' } ] } ], m1: [ { id: 'mq1', ini: 'NR', bg: '#E3DFFF', who: 'Nadia Rahal', when: 'yesterday', d: 1, text: 'Can it read pipelines of repositories my team does not own?', r: [ { id: 'mq1a', ini: 'SB', bg: '#FFDEA0', who: 'Sami Ben Ali', role: 'Platform team', when: 'today', d: 0.3, text: 'Only those you can open on the DevOps platform: it uses your own rights.' } ] } ] };
    Object.assign(sk, this.qaVals('sk-' + sk.id, SKQA[sk.id] || [], 'Ask the author or share how it went…', sk.mine ? { who: ME.who, role: 'Author' } : qaAs, false));

    // ---- publish a skill
    var stepName = ['Write', 'Test', 'Submit', 'Review', 'Published'];
    var skipped = s.published && s.scope !== 'org';
    var proc = stepName.map(function (l, i) { var n = i + 1; return { n: n, label: l, cls: n === s.step ? 'on' : (n < s.step && !(n === 4 && skipped) ? 'done' : ''), cur: n === s.step ? 'step' : 'false', more: i < stepName.length - 1 }; });
    var nsTools = Object.keys(TOOLS).filter(function (k) { return s.nsTools[k]; }), nsWrites = nsTools.filter(function (k) { return TOOLS[k].write; });
    var PICK = ['t_logs', 't_kb', 't_pipestat', 't_jira', 't_deploy', 't_pr'];
    var toolChips = PICK.map(function (k) { var on = !!s.nsTools[k]; return { label: TOOLS[k].name, on: on, style: on ? ON : '', pick: set(function () { var t = Object.assign({}, s.nsTools); t[k] = !on; return { nsTools: t }; }) }; });
    var nsNameOr = s.nsName || 'Flaky test triage', nsEx1Or = s.nsEx1 || 'Which tests were flaky this week on credit-request?';
    var G = '#006D3B', A = '#7A5900';
    var checks = [ { label: 'Manifest', note: 'Name, one line, ' + nsTools.length + ' tools, 1 example', icon: '✓', color: G },
      { label: 'No secrets in the text', note: 'Instructions and example scanned', icon: '✓', color: G },
      { label: 'Tools exist', note: nsTools.map(function (k) { return TOOLS[k].name; }).join(', ') || 'None: instructions only', icon: '✓', color: G },
      { label: nsWrites.length ? 'Changes something' : 'Reads only', note: nsWrites.length ? 'Because of ' + nsWrites.map(function (k) { return TOOLS[k].name; }).join(', ') + '. It will ask first.' : 'Worked out from its tools', icon: nsWrites.length ? '!' : '✓', color: nsWrites.length ? A : G } ];
    var wTool = nsWrites[0];
    var tryTools = nsTools.slice(0, 3).map(function (k) { var t = TOOLS[k]; return { name: t.name, st: t.write ? (s.tryAppr ? 'done' : 'waiting for you') : 'done' }; });
    var scopes = [ { k: 'me', label: 'Just me', note: 'Live at once, for you only.' }, { k: 'team', label: 'My team · ' + ME.team, note: 'Live at once. Your team is responsible for it.' }, { k: 'org', label: 'Everyone', note: 'A platform admin reviews it first.' } ].map(function (x) { var on = s.scope === x.k; return Object.assign(x, { on: on, cls: on ? 'on' : '', pick: set({ scope: x.k }) }); });
    var AUD = { me: 'Just you', team: ME.team, org: 'Everyone' };
    var submit = set(function () { var org = s.scope === 'org'; return { step: org ? 4 : 5, published: { aud: org ? 'Everyone, once reviewed' : AUD[s.scope], stage: org ? 'In review' : 'Published' }, live: org ? 'Sent for review' : 'Published' }; });

    // ---- administration
    var core = { key: 'core', label: 'Core', core: true, items: [ { key: 'general', label: 'General' }, { key: 'users', label: 'Users and permissions', n: 1 }, { key: 'groups', label: 'Groups' }, { key: 'audit', label: 'Audit log' }, { key: 'catalog', label: 'Catalog', n: 2 } ] };
    var sweep = { key: 'sweep', label: 'Sweep', isSweep: true, items: [ { key: 'connectors', label: 'Connectors', n: 1 }, { key: 'stools', label: 'Tools and skills' } ] };
    var comm = { key: 'new', label: 'Community', isNew: true, items: [ { key: 'releases', label: 'Releases' }, { key: 'tours', label: 'Tours' }, { key: 'listen', label: 'Feedback' }, { key: 'ideas', label: 'Ideas' }, { key: 'insights', label: 'Insights' } ] };
    var groupsRaw = platform ? [core, sweep, comm] : [ { key: 'core', label: 'Core', core: true, items: [ { key: 'catalog', label: 'Catalog review', n: 2 } ] } ];
    var goA = function (key) { return set({ screen: 'admin', adminPage: key, rv: null }); };
    var nav = this.adminNav(groupsRaw, s.adminPage, goA), cur = nav.cur, akey = cur.s.key;
    var aDefs = [ { k: 'review', label: 'Review', n: 2 }, { k: 'items', label: 'Items' }, { k: 'policies', label: 'Policies' } ].filter(function (t) { return platform || t.k === 'review'; });
    var aTab = aDefs.some(function (t) { return t.k === s.aTab; }) ? s.aTab : 'review';
    var aTabs = aDefs.map(function (t) { var on = aTab === t.k; return { label: t.label, n: t.n, hasN: !!t.n, on: on, cls: on ? 'tab-on' : '', pick: set({ aTab: t.k, rv: null }) }; });
    var queue = [ { id: 's6', name: 'Liquibase changelog review', by: 'Yann Dupont · Environments', when: '2 days ago', desc: 'Destructive changes, missing rollbacks, naming.' }, { id: 'q2', name: 'Explain a failed quality gate', by: 'Emma Laurent · Docs', when: 'yesterday', desc: 'Says what to fix first, with the lines.' } ].map(function (q) { return Object.assign(q, { open: set({ rv: q.id }) }); });
    var rvDefs = [ 'I tried it and it does what it says', 'No sensitive data in the instructions or the example', 'The actions that change something are needed' ];
    var rvChecks = rvDefs.map(function (l, i) { var on = !!s.rvChecks[i]; return { label: l, on: on, toggle: set(function () { var c = Object.assign({}, s.rvChecks); c[i] = !on; return { rvChecks: c }; }) }; });
    var rvReady = rvDefs.every(function (l, i) { return s.rvChecks[i]; });
    var rv = { name: 'Liquibase changelog review', by: 'Yann Dupont · Environments', when: 'submitted 2 days ago', body: '1. Read the changelog files in the pull request.\n2. Flag destructive changes and changesets without a rollback.\n3. Check naming against the conventions in the knowledge base.\n4. For anything blocking, create one Jira ticket in the project of the repository and link it in the review.', tools: 'Search the knowledge base, Create Jira ticket', note: 'tried on 6 pull requests in Environments' };
    Object.assign(rv, this.qaVals('rv-s6', [ { id: 'rvq1', ini: 'MK', bg: '#9CF1F0', who: 'Marta Kowalski', role: 'Champion', when: 'yesterday', d: 1, text: 'One ticket per pull request, not one per finding?', r: [ { id: 'rvq1a', ini: 'YD', bg: '#C3F4DC', who: 'Yann Dupont', role: 'Author', when: 'today', d: 0.3, text: 'Yes, step 4 says one ticket; the other findings go in the review comment.' } ] } ], 'Write to the author…', qaAs || { who: ME.who, role: '' }, false));
    var WRITE_ACTIONS = [ ['t_deploy', 'ask', 'ask'], ['t_reserve', 'ask', 'off'], ['t_jira', 'ask', 'always'], ['t_pipe', 'ask', 'always'], ['t_pr', 'ask', 'always'] ];
    var policyRows = WRITE_ACTIONS.map(function (w) { var k = w[0], pk = s.pol[k] || {}; return { name: TOOLS[k].name, src: TOOLS[k].src, a: pk.a || w[1], s: pk.s || w[2], onA: set(function (e) { var p = Object.assign({}, s.pol); p[k] = Object.assign({}, pk, { a: val(e) }); return { pol: p }; }), onS: set(function (e) { var p = Object.assign({}, s.pol); p[k] = Object.assign({}, pk, { s: val(e) }); return { pol: p }; }) }; });
    var PH = ['implement', 'review', 'test', 'release'];
    var sweepRows = ITEMS.filter(function (it) { return it.works.indexOf('Sweep') >= 0 && !it.stage && it.aud === 'Everyone'; }).map(function (it) { var d = deco(it), on = s.sweepOn[it.id] || {}; return { name: it.name, kab: d.kab, kcls: d.kcls, cells: PH.map(function (p) { var v = !!on[p]; return { on: v, aria: it.name + ' in ' + p, toggle: set(function () { var all = Object.assign({}, s.sweepOn); all[it.id] = Object.assign({}, on); all[it.id][p] = !v; return { sweepOn: all }; }) }; }) }; });

    // ---- lab chrome
    var SCREENS = [ { k: 'catalog', label: 'Catalog', o: { screen: 'catalog', tab: 'browse' } }, { k: 'item', label: 'Item page', o: { screen: 'item', skill: 'm1' } }, { k: 'new', label: 'Publish a skill', o: { screen: 'new', step: 1, published: null, tryAppr: false } }, { k: 'review', label: 'Admin · Review', o: { screen: 'admin', adminPage: 'catalog', aTab: 'review', rv: null } }, { k: 'stools', label: 'Admin · Sweep tools', o: { screen: 'admin', adminPage: 'stools' } } ];
    var curScreen = s.screen === 'admin' ? (s.adminPage === 'stools' ? 'stools' : 'review') : s.screen;
    var screenChips = SCREENS.map(function (x) { var on = curScreen === x.k; return { label: x.label, on: on, style: on ? ON : '', pick: set(Object.assign({ snack: null }, x.o)) }; });
    var roleChips = [ { k: 'user', label: 'User' }, { k: 'champion', label: 'Champion' }, { k: 'platform', label: 'Platform admin' } ].map(function (r) { var on = role === r.k; return { label: r.label, on: on, style: on ? ON : '', pick: set(function () { var o = { role: r.k, rv: null }; if (r.k === 'user' && s.screen === 'admin') { o.screen = 'catalog'; o.snack = 'Without a reviewer or admin right there is no Administration entry.'; } if (r.k === 'champion' && s.screen === 'admin') { o.adminPage = 'catalog'; o.aTab = 'review'; } return o; }) }; });
    var isAdm = s.screen === 'admin' && role !== 'user';
    var hdr = isAdm ? ['Administration · ' + cur.g.label, cur.s.label + ' · ' + ({ catalog: '2 skills to review', stools: 'per phase', connectors: '5 connectors' }[akey] || '')]
      : s.screen === 'item' ? ['Catalog · ' + sk.kind, sk.name] : s.screen === 'new' ? ['Catalog · Publish a skill', stepName[s.step - 1] + ' · ' + nsNameOr] : ['Catalog', published.length + ' items for the assistant and Sweep'];
    var pubAud = s.published ? s.published.aud : '';
    return Object.assign(sim, { screenChips: screenChips, roleChips: roleChips, live: s.live || '', hasSnack: !!s.snack, snack: s.snack || '', closeSnack: set({ snack: null }),
      hdrFeature: hdr[0], hdrSummary: hdr[1], railCat: !isAdm, railAdm: isAdm,
      sCatalog: s.screen === 'catalog' || (s.screen === 'admin' && role === 'user'), sItem: s.screen === 'item', sNew: s.screen === 'new', sAdmin: isAdm,
      cTabs: cTabs, tBrowse: s.tab === 'browse', tMine: s.tab === 'mine', kindChips: kindChips, items: browse, mine: mine,
      goNew: set({ screen: 'new', step: 1, published: null, tryAppr: false, snack: null }), goCatalog: set({ screen: 'catalog', snack: null }),
      sk: sk, reportIt: set({ snack: 'Reported to Community › Feedback with the item and its version attached.' }),
      proc: proc, nWrite: s.step === 1, nTest: s.step === 2, nSubmit: s.step === 3, nReview: s.step === 4, nDone: s.step === 5,
      nsName: s.nsName, onNsName: set(function (e) { return { nsName: val(e) }; }), nsDesc: s.nsDesc, onNsDesc: set(function (e) { return { nsDesc: val(e) }; }), nsBody: s.nsBody, onNsBody: set(function (e) { return { nsBody: val(e) }; }), nsEx1: s.nsEx1, onNsEx1: set(function (e) { return { nsEx1: val(e) }; }),
      toolChips: toolChips, srcLink: s.src === 'git' ? 'Reading devops.example.internal/request/skill-flaky-tests · write here instead' : 'Or import from a Git repository', pickSrcGit: set({ src: s.src === 'git' ? 'app' : 'git' }),
      saveDraft: set({ snack: 'Draft saved in Mine.' }), toWrite: set({ step: 1 }), toTest: set({ step: 2 }), toSubmit: set({ step: 3 }),
      nsNameOr: nsNameOr, nsEx1Or: nsEx1Or, checks: checks, tryN: tryTools.length, tryTools: tryTools,
      tryNeedsAppr: !!wTool && !s.tryAppr, tryApprQ: wTool ? TOOLS[wTool].name + '?' : '', tryApprArgs: wTool === 't_jira' ? 'project SWP · “Flaky: FacilityExportTest” · Bug' : wTool === 't_deploy' ? 'credit-request · feature/flaky · staging-2' : 'credit-request · build 4821', tryApprove: set({ tryAppr: true }),
      tryAnswer: wTool && !s.tryAppr ? 'Three tests in FacilityExportTest fail on and off, all for one cause: a fixed timestamp in the fixture. I can ' + lower(TOOLS[wTool].name) + ' once you approve.' : 'Three tests in FacilityExportTest fail on and off, all for one cause: a fixed timestamp in the fixture. Fix: use the test clock.' + (wTool === 't_jira' ? ' Ticket SWP-1288 created.' : ''),
      scopes: scopes, scopeOrg: s.scope === 'org', submitCta: s.scope === 'org' ? 'Send for review' : 'Publish', submit: submit,
      simulateApprove: set({ step: 5, published: { aud: 'Everyone', stage: 'Published' } }), openMine: set({ screen: 'catalog', tab: 'mine' }),
      doneText: '“' + nsNameOr + '” is published for ' + ({ 'Just you': 'you', Everyone: 'everyone' }[pubAud] || 'your team') + '. It is in the assistant’s Tools menu now; a new version goes through Test again.',
      groups: nav.groups, page: akey, pageTitle: cur.s.label, onSelect: function (e) { var k = e && e.target ? e.target.value : null; if (k) goA(k)(e); },
      aCatalog: akey === 'catalog', aTabs: aTabs, aReview: akey === 'catalog' && aTab === 'review', aItems: akey === 'catalog' && aTab === 'items', aPolicies: akey === 'catalog' && aTab === 'policies', aSweep: akey === 'stools', aOther: ['catalog', 'stools'].indexOf(akey) < 0,
      rvList: !s.rv, rvOpen: !!s.rv, queue: queue, rv: rv, rvBack: set({ rv: null }), rvChecks: rvChecks, rvNotReady: !rvReady,
      rvPublish: rvReady ? set({ rv: null, snack: 'Liquibase changelog review is published for everyone. Yann Dupont is notified.' }) : set({}), rvChanges: set({ rv: null, snack: 'Yann Dupont sees your request in the skill’s discussion.' }),
      adminItems: ITEMS.filter(function (it) { return s.kind === 'all' || it.kind === s.kind; }).map(deco), policyRows: policyRows, phases: PH, sweepRows: sweepRows });
  }
}
'''

body = (BODY.replace('SIMBAR', S.sim_bar()).replace('SIMOPEN', S.sim_open('sim-host-cl', 'height: 1080px')).replace('SIMCLOSE', S.SIM_CLOSE)
        .replace('HEADER', S.header(False)).replace('RAIL_CAT', N.rail(N.LIGHT, 'catalog', catalog=True)).replace('RAIL_ADM', N.rail(N.LIGHT, 'admin', catalog=True))
        .replace('NAVBAR', S.navbar(N.LIGHT, 'none')).replace('@@CATALOG@@', CATALOG).replace('@@ITEM@@', ITEM).replace('@@NEWSKILL@@', NEWSKILL).replace('@@ADMIN@@', ADMIN))
logic = LOGIC.replace('/*SIMJS*/', S.SIM_JS).replace('/*ADMINJS*/', S.ADMIN_JS).replace('/*QAJS*/', S.QA_JS)
out = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>Catalog lab, skills, tools and MCP servers for the assistant and Sweep</title>\n<script src="./support.js"></script>\n</head>\n<body>\n<x-dc>\n<helmet>\n'
       '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&amp;family=Open+Sans:wght@400;600;700&amp;display=swap">\n'
       '<style>\n' + S.CSS + '\n' + S.SIM_CSS + S.QA_CSS + S.ADMIN_CSS + CSS_LAB + CSS_CAT + '</style>\n</helmet>\n' + body + '\n</x-dc>\n'
       '<script type="text/x-dc" data-dc-script data-props=\'{"$preview":{"width":1440,"height":2000}}\'>' + logic + '</script>\n</body>\n</html>\n')
for t in ['sc-if', 'sc-for']:
    assert len(re.findall(rf'<{t}\b', out)) == len(re.findall(rf'</{t}>', out)), t
for ph in ['SIMBAR', 'HEADER', 'NAVBAR', 'SIMOPEN', 'RAIL_CAT', 'RAIL_ADM', '@@']:
    assert ph not in out, ph
open(dst, 'w', encoding='utf-8').write(out); print(len(out))
