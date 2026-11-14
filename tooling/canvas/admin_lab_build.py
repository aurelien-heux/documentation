"""Build AdminLayoutLab.dc.html: four proposals for the shell of the Administration module (how core and feature
administration are reached), with the same content in each: Core (Users and permissions, Groups, Audit log, General),
Core (General, Users and permissions, Groups, Audit log), Sweep (Connectors) and Community (Releases, Tours, Feedback,
Ideas, Insights). Four pages carry content (General, Users and permissions, Sweep · Connectors, Community · Feedback
with the FeedbackProfile editor); the others are placeholders. View as platform admin or Sweep admin to see how rights filter the navigation."""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
import shell as S, navgen as N
dst = sys.argv[1]

ST = 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
BACK = f'<svg width="18" height="18" viewBox="0 0 24 24" {ST}><path d="M15 6l-6 6 6 6"/></svg>'
PLUS = f'<svg width="18" height="18" viewBox="0 0 24 24" {ST}><path d="M12 5v14M5 12h14"/></svg>'
SEARCH = f'<svg width="18" height="18" viewBox="0 0 24 24" {ST}><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>'
MARK_SWEEP = N.mark('sweep', N.LIGHT, 22)
MARK_NEW = N.mark('new', N.LIGHT, 22)

# ---------------------------------------------------------------------------
# shared content (identical in every proposal)
# ---------------------------------------------------------------------------
USERS, CONNECTORS, GENERAL, PLACEHOLDER, MODLINE = S.ADMIN_USERS, S.ADMIN_CONNECTORS, S.ADMIN_GENERAL, S.ADMIN_PLACEHOLDER, S.ADMIN_MODLINE
LISTENING = '''<div class="stack">
  <div class="row r-wrap" style="gap: 8px"><span class="tab tab-on">{{profilesTab}}</span><span class="tab">Inbox<span class="n">{{inboxN}}</span></span><sc-if value="{{hasCore}}" hint-placeholder-val="{{true}}"><span class="tab">Surveys<span class="n">3</span></span></sc-if><span class="tab">Feedback prompts</span><span style="flex: 1"></span><span class="tile in"><i></i>Shared cap · 1 prompt per user every 7 days</span></div>
  <div class="card" style="padding: 0; overflow: hidden"><div class="ad-tscroll"><table class="ad-tbl" style="width: 100%; border-collapse: collapse">
    <thead><tr><th class="th">Feedback profile</th><th class="th">Status</th><th class="th">Entry points</th><th class="th">Questions</th><th class="th">Routing</th><th class="th"></th></tr></thead>
    <tbody>
      <sc-for list="{{profiles}}" as="p" hint-placeholder-count="4">
      <tr class="rw"><td class="td"><b class="ui">{{p.name}}</b><div class="meta">{{p.owner}}</div></td><td class="td"><span class="tile {{p.tile}}"><i></i>{{p.status}}</span></td><td class="td"><span style="font-size: 13px">{{p.entries}}</span></td><td class="td">{{p.q}} of 3</td><td class="td"><span style="font-size: 13px">{{p.route}}</span></td><td class="td" style="text-align: right; white-space: nowrap"><button type="button" class="chip" style="height: 28px" aria-label="Edit the {{p.name}} feedback profile" onClick="{{p.go}}">Edit</button></td></tr>
      </sc-for>
    </tbody></table></div></div>
  <div class="meta" style="white-space: normal">{{profilesNote}}</div>
  <sc-if value="{{fpOn}}" hint-placeholder-val="{{true}}">''' + S.ADMIN_FEEDBACK + '''</sc-if>
</div>'''

CONTENT = ('<sc-if value="{{pGeneral}}" hint-placeholder-val="{{true}}">' + GENERAL + '</sc-if>'
           '<sc-if value="{{pUsers}}" hint-placeholder-val="{{false}}">' + USERS + '</sc-if>'
           '<sc-if value="{{pConnectors}}" hint-placeholder-val="{{false}}">' + CONNECTORS + '</sc-if>'
           '<sc-if value="{{pListening}}" hint-placeholder-val="{{false}}">' + LISTENING + '</sc-if>'
           '<sc-if value="{{pOther}}" hint-placeholder-val="{{false}}">' + PLACEHOLDER + '</sc-if>')

SECTION_CHIPS = '''<div class="row ad-chips" style="gap: 8px"><sc-for list="{{sections}}" as="s" hint-placeholder-count="4"><button type="button" class="chip" aria-pressed="{{s.on}}" style="{{s.style}}" onClick="{{s.pick}}">{{s.label}}<sc-if value="{{s.hasN}}" hint-placeholder-val="{{false}}"><span class="n">{{s.n}}</span></sc-if></button></sc-for></div>'''

nav_tree = S.admin_tree

SELECT_FALLBACK = S.ADMIN_SELECT

# ---------------------------------------------------------------------------
# the four proposals
# ---------------------------------------------------------------------------
# A · Hub and modules (today)
HUB = f'''<sc-if value="{{{{hasCore}}}}" hint-placeholder-val="{{{{true}}}}"><h2 class="h2">Platform</h2>
<div class="r-g3" style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px"><sc-for list="{{{{hubCore}}}}" as="c" hint-placeholder-count="4">
  <div class="card stack" style="gap: 8px; min-height: 120px"><div class="row" style="justify-content: space-between"><div class="ui" style="font-size: 16px; font-weight: 600">{{{{c.label}}}}</div><sc-if value="{{{{c.hasN}}}}" hint-placeholder-val="{{{{false}}}}"><span class="tile wn"><i></i>{{{{c.n}}}} requests</span></sc-if></div><div style="flex: 1; font-size: 13px; line-height: 18px; color: #48454E">{{{{c.sub}}}}</div><div class="row"><span class="mono" style="font-size: 11px; color: #48454E">platform-core@2.3</span><span style="flex: 1"></span><button type="button" class="btn t sm" onClick="{{{{c.pick}}}}">Open</button></div></div>
</sc-for></div></sc-if>
<h2 class="h2" style="margin-top: 8px">Features</h2>
<div class="r-g2" style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px"><sc-for list="{{{{hubFeat}}}}" as="f" hint-placeholder-count="2">
  <div class="card stack" style="gap: 12px; padding: 20px"><div class="row"><span style="width: 40px; height: 40px; border-radius: 12px; background: #EDE4FF; display: inline-flex; align-items: center; justify-content: center; flex: none"><sc-if value="{{{{f.isSweep}}}}" hint-placeholder-val="{{{{true}}}}">{MARK_SWEEP}</sc-if><sc-if value="{{{{f.isNew}}}}" hint-placeholder-val="{{{{false}}}}">{MARK_NEW}</sc-if></span><div style="flex: 1; min-width: 0"><div class="ui" style="font-size: 16px; font-weight: 700">{{{{f.label}}}}</div><div style="font-size: 12px; color: #48454E">Owned by {{{{f.owner}}}} · your role: {{{{f.role}}}}</div></div><button type="button" class="btn f sm" onClick="{{{{f.pick}}}}">Manage</button></div>
  <div class="stack" style="gap: 6px"><sc-for list="{{{{f.stats}}}}" as="x" hint-placeholder-count="3"><div class="row" style="gap: 8px; font-size: 13px"><span class="tile {{{{x.tile}}}}" style="min-width: 28px; justify-content: center"><i></i>{{{{x.v}}}}</span><span>{{{{x.label}}}}</span></div></sc-for></div>
  <div class="row" style="border-top: 1px solid #ECE5F4; padding-top: 10px; font-size: 11px; color: #48454E"><span class="mono">{{{{f.remote}}}}</span><span style="flex: 1"></span><span>{{{{f.scope}}}}</span></div></div>
</sc-for></div>'''
A = ('<sc-if value="{{isA}}" hint-placeholder-val="{{true}}">'
     '<sc-if value="{{hubOn}}" hint-placeholder-val="{{true}}"><div class="stack" style="gap: 16px">' + HUB + '</div></sc-if>'
     '<sc-if value="{{hubOff}}" hint-placeholder-val="{{false}}"><div class="stack" style="gap: 16px">'
     + S.subheader('{{goHub}}', 'Back to Administration', '{{groupLabel}}', ctx='Settings and rights for this module', actions=SECTION_CHIPS.replace('class="row ad-chips"', 'class="row ad-chips ad-chips-a"'))
     + MODLINE + CONTENT + '</div></sc-if></sc-if>')

# B · Admin sidebar
B = ('<sc-if value="{{isB}}" hint-placeholder-val="{{false}}"><div class="ad-split">'
     + nav_tree('ad-side') + SELECT_FALLBACK +
     '<div class="stack" style="gap: 16px; min-width: 0">' + MODLINE + CONTENT + '</div></div></sc-if>')

# C · Scope tabs and section chips
C = ('<sc-if value="{{isC}}" hint-placeholder-val="{{false}}"><div class="stack" style="gap: 16px">'
     '<div role="tablist" class="ad-tabs" aria-label="Administration"><sc-for list="{{groups}}" as="g" hint-placeholder-count="3"><button type="button" role="tab" class="tab {{g.tabCls}}" aria-selected="{{g.on}}" onClick="{{g.pick}}">'
     f'<sc-if value="{{{{g.isSweep}}}}" hint-placeholder-val="{{{{false}}}}">{MARK_SWEEP}</sc-if><sc-if value="{{{{g.isNew}}}}" hint-placeholder-val="{{{{false}}}}">{MARK_NEW}</sc-if>{{{{g.label}}}}</button></sc-for></div>'
     + SECTION_CHIPS + MODLINE + CONTENT + '</div></sc-if>')

# D · Admin console: the rail gives way to the admin tree
D = ('<sc-if value="{{isD}}" hint-placeholder-val="{{false}}"><div class="stack" style="gap: 16px; min-width: 0">' + SELECT_FALLBACK.replace('class="ad-select row"', 'class="ad-select ad-select-d row"') + MODLINE + CONTENT + '</div></sc-if>')
D_TREE = ('<sc-if value="{{isD}}" hint-placeholder-val="{{false}}"><div class="ad-console"><a href="#app" class="ad-back" onClick="{{noop}}">' + BACK + '<span>Back to AIToolbox</span></a>'
          '<div class="ad-ch"><span class="ad-shield">' + N.icon('admin') + '</span><div><div class="ui" style="font-size: 14px; font-weight: 700">Administration</div><div class="meta" style="white-space: normal">{{scopeLabel}}</div></div></div>'
          + nav_tree('ad-tree') + '</div></sc-if>')

CSS_LAB = r"""
.tile{display:inline-flex;align-items:center;gap:6px;height:24px;padding:0 8px;border-radius:4px;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:600;white-space:nowrap}
.tile i{width:8px;height:8px;border-radius:2px;background:currentColor}
.ok{background:#C3F4DC;color:#00391E}.wn{background:#FFDEA0;color:#261900}.er{background:#FFDAD6;color:#410002}.in{background:#E3DFFF;color:#14085E}.ne{background:#ECE5F4;color:#1C1B1E}
.ttab{display:flex;flex-direction:column;align-items:flex-start;gap:4px;padding:12px 14px;border-radius:12px;border:1px solid #CAC4CF;background:#FDF8FD;text-align:left;cursor:pointer;min-width:0}
.ttab:hover{background:rgba(53,48,126,.06)}
.ttab-on{border-color:#35307E;box-shadow:inset 0 0 0 1px #35307E;background:#F2EBFA}
.cmp td,.cmp th{padding:10px 12px;font-size:13px;line-height:18px;vertical-align:top;border-top:1px solid #CAC4CF}
.cmp th{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:600;letter-spacing:.5px;text-transform:uppercase;color:#48454E;text-align:left;border-top:0}
.cmp tr.on td{background:#F2EBFA}
.row{display:flex;align-items:center;gap:12px}
.stack{display:flex;flex-direction:column;gap:12px;min-width:0}
.meta{font-size:12px;color:#48454E;white-space:nowrap}
.sm{height:32px;padding:0 14px;border-radius:12px;font-size:13px}
.kpi{flex:1;min-width:0;padding:12px 16px;border-radius:12px;background:#FFFFFF;box-shadow:0 1px 2px rgba(0,0,0,.3),0 1px 3px 1px rgba(0,0,0,.15)}
.kpi b{display:block;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:24px;line-height:32px;font-weight:700;color:#1C1B1E}
.kpi span{font-size:12px;color:#48454E}
.sel{height:40px;box-sizing:border-box;padding:0 36px 0 12px;border:1px solid #79757F;border-radius:8px;background:#FDF8FD;color:#1C1B1E;font:500 14px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;appearance:none;-webkit-appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2348454E' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 10px center;background-size:18px}
tr.rw:hover td{background:rgba(53,48,126,.04)}
/* C · tabs */
.ad-tabs{display:flex;align-items:center;border-bottom:1px solid #CAC4CF;overflow-x:auto;scrollbar-width:none}
.ad-tabs .tab{flex:none}
.ad-chips{flex-wrap:wrap}
/* D · console */
.ad-console{width:260px;flex:none;display:flex;flex-direction:column;gap:4px;padding:12px;box-sizing:border-box;background:#EDE4FF;min-height:100%}
.ad-back{display:flex;align-items:center;gap:8px;height:40px;padding:0 12px;border-radius:16px;color:#35307E;text-decoration:none;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:13px;font-weight:600}
.ad-back:hover{background:rgba(53,48,126,.06)}
.ad-ch{display:flex;gap:10px;align-items:center;padding:8px 12px 14px;border-bottom:1px solid #CAC4CF;margin-bottom:6px}
.ad-shield{width:36px;height:36px;border-radius:12px;background:#D4D0F9;color:#191836;display:inline-flex;align-items:center;justify-content:center;flex:none}
.ad-tree{display:flex;flex-direction:column;gap:4px}
.ad-tree .ad-ni{background:transparent}.ad-tree .ad-ni.on{background:#D4D0F9}
.ad-railwrap{display:contents}.ad-railwrap.ad-norail{display:none}
.r-wrap{flex-wrap:wrap}
.r-g3,.r-g2{min-width:0}
@container win (max-width: 1199px){
.ad-console{display:none!important}.ad-railwrap.ad-norail{display:contents!important}
.r-g3{grid-template-columns:repeat(2,minmax(0,1fr))!important}.r-kpis{flex-wrap:wrap}.r-kpis>.kpi{flex:1 1 140px}
}
@container win (max-width: 839px){.ad-chips-a{width:100%}.r-g2{grid-template-columns:minmax(0,1fr)!important}}
@container win (max-width: 599px){.r-g3{grid-template-columns:minmax(0,1fr)!important}.ad-chips .chip{height:28px;font-size:12px}}
"""

BODY = '''<div style="width: 1440px; min-height: 2080px; box-sizing: border-box; background: #FDF8FD; color: #1C1B1E; display: flex; flex-direction: column">
  <div style="padding: 20px 32px 12px; display: flex; flex-direction: column; gap: 12px">
    <div style="display: flex; align-items: center; gap: 16px">
      <h1 class="ui" style="margin: 0; font-size: 24px; line-height: 32px; font-weight: 700; white-space: nowrap">Administration layout lab</h1>
      <span style="font-size: 14px; color: #48454E">Four shells for the Administration module, same content in each: Core (general, users and permissions, groups, audit log) and the two feature modules, Sweep and Community. General, Users and permissions, Sweep · Connectors and Community · Feedback carry content; the other sections are placeholders. View as platform admin or Sweep admin to see how rights filter the navigation.</span>
    </div>
    <div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px">
      <sc-for list="{{tabs}}" as="t" hint-placeholder-count="4">
        <button type="button" class="ttab {{t.cls}}" aria-pressed="{{t.on}}" onClick="{{t.pick}}"><span class="row" style="gap: 8px"><span style="width: 24px; height: 24px; border-radius: 999px; background: {{t.numBg}}; color: {{t.numFg}}; font-family: Manrope, 'BNPP Type', 'Segoe UI', system-ui, sans-serif; font-size: 12px; font-weight: 700; display: inline-flex; align-items: center; justify-content: center">{{t.k}}</span><span class="ui" style="font-size: 14px; font-weight: 600">{{t.name}}</span></span><span style="font-size: 12px; line-height: 16px; color: #48454E">{{t.sub}}</span><sc-if value="{{t.rec}}" hint-placeholder-val="{{false}}"><span class="tile ok"><i></i>Adopted</span></sc-if><sc-if value="{{t.cur}}" hint-placeholder-val="{{false}}"><span class="tile ne"><i></i>Today</span></sc-if></button>
      </sc-for>
    </div>
    <div class="row" style="gap: 12px; flex-wrap: wrap">SIMBAR<span class="row" style="gap: 8px; padding: 6px 8px 6px 12px; border: 1px dashed #79757F; border-radius: 12px"><span class="ui" style="font-size: 12px; font-weight: 600; color: #48454E">View as</span><sc-for list="{{roleChips}}" as="r" hint-placeholder-count="2"><button type="button" class="chip" style="height: 28px; font-size: 12px; {{r.style}}" aria-pressed="{{r.on}}" onClick="{{r.pick}}">{{r.label}}</button></sc-for></span><span class="row" style="gap: 8px; padding: 6px 8px 6px 12px; border: 1px dashed #79757F; border-radius: 12px"><span class="ui" style="font-size: 12px; font-weight: 600; color: #48454E">Go to</span><sc-for list="{{goChips}}" as="r" hint-placeholder-count="3"><button type="button" class="chip" style="height: 28px; font-size: 12px; {{r.style}}" aria-pressed="{{r.on}}" onClick="{{r.pick}}">{{r.label}}</button></sc-for></span></div>
  </div>

  <div style="margin: 0 32px; border-radius: 12px; overflow: hidden; border: 1px solid #CAC4CF">
  SIMOPEN
  <div style="position: relative; width: 100%; height: 100%; display: flex; flex-direction: column; background: #FDF8FD; overflow: hidden">
    HEADER
    <div style="flex: 1; display: flex; min-height: 0">
      <div class="ad-railwrap {{railCls}}">RAIL</div>
      D_TREE
      <main style="position: relative; flex: 1; min-width: 0; padding: 20px 32px 24px; box-sizing: border-box; display: flex; flex-direction: column; gap: 16px; overflow: auto">
        PROPOSALS
      </main>
    </div>
    NAVBAR
  </div>
  SIMCLOSE
  </div>

  <div style="padding: 20px 32px 32px; display: grid; grid-template-columns: minmax(0, 1fr) 420px; gap: 24px; align-items: start">
    <div class="card" style="padding: 0; overflow: hidden">
      <table class="cmp" style="width: 100%; border-collapse: collapse">
        <thead><tr><th style="width: 30px"></th><th style="width: 130px">Shell</th><th>Landing</th><th>Reaching a section</th><th>Rights</th><th>Below 1200 px</th><th>Trade-off</th></tr></thead>
        <tbody>
          <sc-for list="{{rows}}" as="r" hint-placeholder-count="4">
            <tr class="{{r.cls}}"><td><span class="ui" style="font-weight: 700">{{r.k}}</span></td><td><span class="ui" style="font-weight: 600">{{r.name}}</span></td><td>{{r.landing}}</td><td>{{r.reach}}</td><td>{{r.rights}}</td><td>{{r.small}}</td><td style="color: #48454E">{{r.trade}}</td></tr>
          </sc-for>
        </tbody>
      </table>
    </div>
    <div style="display: flex; flex-direction: column; gap: 16px">
      <div class="card" style="display: flex; flex-direction: column; gap: 8px">
        <div class="row" style="justify-content: space-between"><span class="h2">Adopted · B</span><span class="tile ok"><i></i>Admin sidebar</span></div>
        <div style="font-size: 13px; line-height: 18px; color: #48454E">One page with a 240 px sidebar: Core, then one group per feature module, each group being what the remote module declares in its manifest. Every section is one click away and the current one is always visible; rights simply remove groups and items (a Sweep admin sees Sweep, and Feedback · Sweep under Community). New feature modules add a group; nothing else moves. Below 1200 px the sidebar becomes a grouped Section select above the content. Applied to the live Community prototype.</div>
        <div style="font-size: 13px; line-height: 18px; color: #48454E"><b style="color: #1C1B1E">Second choice: D</b>, the console, if Administration becomes a place people stay in for long sessions: the admin tree takes the rail’s place and the page gets the full width, at the cost of leaving the app’s navigation.</div>
        <div style="font-size: 13px; line-height: 18px; color: #48454E"><b style="color: #1C1B1E">A</b> keeps a hub that is pleasant to land on but adds a click to every section and a back chip to every page; <b style="color: #1C1B1E">C</b> needs two rows (scope tabs, section chips) and the scope tabs scroll on phones.</div>
      </div>
      <div class="ocard" style="display: flex; flex-direction: column; gap: 6px; font-size: 13px; line-height: 18px; color: #48454E">
        <span class="ui" style="font-size: 14px; font-weight: 700; color: #1C1B1E">Same in every shell</span>
        <span><b style="color: #1C1B1E">Core</b> (platform admins only): General (landing), Users and permissions, Groups, Audit log. Accounts come from the company directory (SSO), so Users and permissions only gives admin rights: filters All, Admins, Requests, search, the user table (admin rights, team, last active) and an Admin rights panel (Platform admin, Sweep admin, Community admin, Feedback · Sweep; approve or decline a request).</span>
        <span><b style="color: #1C1B1E">Sweep</b> (remote module sweep-admin@1.4): Connectors. <b style="color: #1C1B1E">Community</b> (community-admin@4.6): Releases, Tours, Feedback, Ideas, Insights. Feature pages carry the Remote module line (id, owner, scope).</span>
        <span>Header context: “Administration · Core” over the section, or “Administration · Sweep” over the section. Administration stays the last rail destination; the rail’s own active item is Admin.</span>
      </div>
    </div>
  </div>
</div>'''

LOGIC = r'''
class Component extends DCLogic {
  constructor(props) { super(props); this.simHostId = 'sim-host-ad'; this.simDefault = 1374; this.state = { v: 'B', role: 'platform', page: 'general', hub: true, usel: 'u2', uf: 'all', fpEdit: null, fp: null, simW: null, simAvail: 0 }; }
/*SIMJS*/
/*ADMINJS*/
  componentDidMount() { var self = this; this.simSync(); if (typeof window !== 'undefined') window.addEventListener('resize', function () { self.simSync(); }); }
  componentDidUpdate() { this.simSync(); }
  renderVals() {
    var s = this.state, self = this, sim = this.simVals();
    var set = function (o) { return function (e) { if (e && e.preventDefault) e.preventDefault(); self.setState(typeof o === 'function' ? o(e) : o); }; };
    var ON = 'background: #E3DFFF; border-color: #E3DFFF; color: #191836';
    var defs = [
      { k: 'A', name: 'Hub and modules', sub: 'Today: cards, then a page with a back chip.', landing: 'A hub: Platform cards and one card per feature', reach: 'Open a card, then a section chip; back chip to the hub', rights: 'Cards disappear', small: 'Cards 2 then 1 per row; chips wrap', trade: 'One extra click to every section; no overview of where you are inside a module.' },
      { k: 'B', name: 'Admin sidebar', sub: 'A 240 px sidebar: Core, Sweep, Community.', landing: 'Users and permissions (first section you have rights on)', reach: 'One click in the sidebar; the current section is highlighted', rights: 'Groups and items disappear', small: 'Sidebar becomes a grouped Section select', trade: 'A second navigation column beside the rail; 240 px less for tables.', rec: true, adopted: true },
      { k: 'C', name: 'Scope tabs', sub: 'Tabs Core · Sweep · Community, then section chips.', landing: 'Core tab, first section', reach: 'A tab, then a chip', rights: 'Tabs and chips disappear', small: 'Tabs scroll sideways; chips wrap', trade: 'Two rows of navigation above every page; two clicks across scopes.' },
      { k: 'D', name: 'Admin console', sub: 'The admin tree takes the rail’s place.', landing: 'Users and permissions, in a dedicated console', reach: 'One click in the 260 px tree; “Back to AIToolbox” leaves it', rights: 'Groups and items disappear', small: 'Rail returns and the tree becomes a Section select', trade: 'Leaves the app shell: no rail, so Sweep or Community are two clicks away.' }
    ];
    var tabs = defs.map(function (d) { var on = s.v === d.k; return { k: d.k, name: d.name, sub: d.sub, on: on, cls: on ? 'ttab-on' : '', numBg: on ? '#35307E' : '#E3DFFF', numFg: on ? '#FFFFFF' : '#14085E', rec: !!d.rec, cur: !!d.cur, pick: set({ v: d.k }) }; });
    var rows = defs.map(function (d) { return Object.assign({}, d, { cls: s.v === d.k ? 'on' : '' }); });
    var platform = s.role === 'platform';
    // sections, filtered by rights
    var groupsRaw = this.adminGroups(platform, { users: 1, connectors: 1, releases: 5, listen: 12, listenScoped: 2, ideas: 5 });
    var go = function (key) { return set({ page: key, hub: false, usel: key === 'users' ? s.usel : null }); };
    var nav = this.adminNav(groupsRaw, s.page, go), cur = nav.cur, groups = nav.groups, sections = nav.sections;
    var hubCore = (platform ? groupsRaw[0].items : []).map(function (i) { return { label: i.label, sub: { users: '1,284 users from the directory · admin rights per feature', groups: '18 groups · Client, Facility, Request…', audit: 'Sign-ins, rights changes, admin actions · 90 days', general: 'Workspace name, time zone, retention' }[i.key], hasN: !!i.n, n: i.n, pick: go(i.key) }; });
    var hubFeat = groupsRaw.filter(function (g) { return !g.core; }).map(function (g) { return { label: g.label, isSweep: !!g.isSweep, isNew: !!g.isNew, owner: g.owner, role: platform ? 'admin (platform)' : (g.isSweep ? 'Sweep admin' : 'Feedback · Sweep'), remote: g.remote, scope: platform || g.isSweep ? 'Full module' : 'Feedback · Sweep only', pick: go(g.items[0].key),
      stats: g.isSweep ? [ { v: '4', tile: 'ok', label: 'connectors connected' }, { v: '1', tile: 'wn', label: 'token expiring in 6 days' }, { v: '1', tile: 'ne', label: 'not connected (Artifactory)' } ] : [ { v: '5', tile: 'in', label: 'releases scheduled' }, { v: '12', tile: 'wn', label: 'open items in the inbox' }, { v: '5', tile: 'ne', label: 'ideas to triage' } ] }; });
    var SUMM = { users: '1,284 users from the directory · 46 admins · 1 request', groups: '18 groups', audit: 'Last 90 days', general: 'Workspace, language, time zone, retention', connectors: '5 connectors · 1 needs attention', releases: '5 scheduled', tours: '4 tours', listen: platform ? 'Profiles, inbox, surveys, solicitation policy' : 'Sweep profile, Sweep inbox, shared cap (read-only)', ideas: '5 ideas to triage', insights: 'Feedback forms, surveys and tours, last 30 days' };
    var hubOn = s.v === 'A' && s.hub;
    var hdrFeature = hubOn ? 'Administration' : 'Administration · ' + cur.g.label, hdrSummary = hubOn ? (platform ? 'Platform admin · everything you can administer' : 'Sweep admin · Sweep, and Feedback · Sweep in Community') : cur.s.label + ' · ' + SUMM[cur.s.key];
    var au = this.adminUsers();
    var FB = this.feedbackProfiles(s, set);
    var fpOpen = platform ? (s.fpEdit || 'sweep') : 'sweep';
    var profiles = FB.keys.filter(function (k) { return platform || k === 'sweep'; }).map(function (k) { var p = FB.summary(k); return { name: p.name, owner: p.owner, status: p.status, tile: p.tile, entries: p.entries, q: p.nq, route: p.routing, go: set({ fpEdit: k }) }; });
    var roleChips = [ { k: 'platform', label: 'Platform admin' }, { k: 'sweep', label: 'Sweep admin' } ].map(function (r) { var on = s.role === r.k; return { label: r.label, on: on, style: on ? ON : '', pick: set(function () { var o = { role: r.k }; if (r.k === 'sweep' && ['users', 'groups', 'audit', 'general'].indexOf(s.page) >= 0) o.page = 'connectors'; return o; }) }; });
    var goChips = [ { k: 'general', label: 'General', core: true }, { k: 'users', label: 'Users and permissions', core: true }, { k: 'connectors', label: 'Sweep · Connectors' }, { k: 'listen', label: 'Community · Feedback' } ].filter(function (g) { return platform || !g.core; }).map(function (g) { var on = cur.s.key === g.k && !hubOn; return { label: g.label, on: on, style: on ? ON : '', pick: go(g.k) }; });
    return Object.assign(sim, { tabs: tabs, rows: rows, isA: s.v === 'A', isB: s.v === 'B', isC: s.v === 'C', isD: s.v === 'D',
      railCls: s.v === 'D' ? 'ad-norail' : '', hubOn: hubOn, hubOff: !hubOn, goHub: set({ hub: true }), noop: set({}),
      groups: groups, sections: sections, groupLabel: cur.g.label, page: cur.s.key, pageTitle: cur.s.label, onSelect: set(function (e) { return { page: e && e.target ? e.target.value : s.page, hub: false }; }),
      hubCore: hubCore, hubFeat: hubFeat, hasCore: platform, scopeLabel: platform ? 'Platform admin · everything' : 'Sweep admin · Sweep and Feedback · Sweep',
      hdrFeature: hdrFeature, hdrSummary: hdrSummary,
      isFeaturePage: !cur.g.core, modRemote: cur.g.remote || '', modOwner: cur.g.owner || '', modScope: platform || cur.g.isSweep ? 'Full module' : 'Feedback · Sweep only',
      pGeneral: cur.s.key === 'general', pUsers: cur.s.key === 'users', pConnectors: cur.s.key === 'connectors', pListening: cur.s.key === 'listen', pOther: ['general', 'users', 'connectors', 'listen'].indexOf(cur.s.key) < 0, fp: FB.editor(fpOpen), fpOn: true, profilesTab: platform ? 'Profiles' : 'Profile', inboxN: platform ? 12 : 2, profilesNote: platform ? 'Every feature’s feedback form is edited here, in Community › Feedback. Feature admins with a Feedback · <feature> right see only their own profile and inbox.' : 'Your Feedback · Sweep right covers this profile and the Sweep inbox; the cap is read-only.',
      uCount: au.uCount, uFilters: au.uFilters, users: au.users, hasUsr: au.hasUsr, usr: au.usr, closeUsr: au.closeUsr, profiles: profiles,
      roleChips: roleChips, goChips: goChips });
  }
}
'''

body = (BODY.replace('SIMBAR', S.sim_bar()).replace('SIMOPEN', S.sim_open('sim-host-ad', 'height: 1000px')).replace('SIMCLOSE', S.SIM_CLOSE)
        .replace('HEADER', S.header(False)).replace('RAIL', N.rail(N.LIGHT, 'admin')).replace('D_TREE', D_TREE)
        .replace('NAVBAR', S.navbar(N.LIGHT, 'none')).replace('PROPOSALS', A + B + C + D))
logic = LOGIC.replace('/*SIMJS*/', S.SIM_JS).replace('/*ADMINJS*/', S.ADMIN_JS)
out = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>Administration layout lab, four shells for core and feature administration</title>\n<script src="./support.js"></script>\n</head>\n<body>\n<x-dc>\n<helmet>\n'
       '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&amp;family=Open+Sans:wght@400;600;700&amp;display=swap">\n'
       '<style>\n' + S.CSS + '\n' + S.SIM_CSS + S.ADMIN_CSS + CSS_LAB + '</style>\n</helmet>\n' + body + '\n</x-dc>\n'
       '<script type="text/x-dc" data-dc-script data-props=\'{"$preview":{"width":1440,"height":2080}}\'>' + logic + '</script>\n</body>\n</html>\n')
for t in ['sc-if', 'sc-for']:
    assert len(re.findall(rf'<{t}\b', out)) == len(re.findall(rf'</{t}>', out)), t
for ph in ['SIMBAR', 'PROPOSALS', 'D_TREE', 'HEADER', 'NAVBAR']:
    assert ph not in out, ph
open(dst, 'w', encoding='utf-8').write(out); print(len(out))
