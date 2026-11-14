"""Build FeedbackAdminLab.dc.html: three ways to administer feedback, in the adopted admin shell (B, sidebar).
1 · In each feature (applied): every feature module has a Feedback section that embeds the FeedbackProfile editor
    owned by Community; Community > Listening keeps the overview, the shared cap, surveys and the inbox.
A · Community > Feedback: Listening becomes Feedback, admin only, and holds everything (profiles editable there).
B · Feedback module: its own admin group and remote module (feedback-admin) beside Core; Community keeps
    Releases, Tours, Ideas triage and Insights; the Sweep group keeps a shortcut.
View as platform admin or Sweep admin to see how rights scope each variant."""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
import shell as S, navgen as N
dst = sys.argv[1]
HERE = os.path.dirname(__file__)
CSS_LAB = re.search(r'CSS_LAB = r"""(.*?)"""', open(os.path.join(HERE, 'admin_lab_build.py'), encoding='utf-8').read(), re.S)[1]
CSS_FB = r"""
.bar{height:8px;border-radius:4px;background:#ECE5F4;overflow:hidden;flex:1;min-width:40px}.bar i{display:block;height:100%;background:#35307E;border-radius:4px}
.fbl-note{display:flex;gap:12px;align-items:flex-start;padding:12px 16px;border-radius:12px;background:#FFF8E6;border:1px solid #F0D58C;font-size:13px;line-height:18px}
.fbl-saved{display:flex;gap:10px;align-items:center;padding:10px 16px;border-radius:12px;background:#C3F4DC;color:#00391E;font-size:13px}
.ad-gh svg.fbg{color:#35307E}
.tile.ai{background:#9CF1F0;color:#002020}
"""

ST = 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
FB_ICON = f'<svg class="fbg" width="22" height="22" viewBox="0 0 24 24" {ST}><path d="M4 5h16v11H9l-5 4z"/><path d="M9 10h6M9 13h3"/></svg>'

TREE = (f'<nav class="ad-side" aria-label="Administration"><sc-for list="{{{{groups}}}}" as="g" hint-placeholder-count="4"><div class="ad-g"><div class="ad-gh"><sc-if value="{{{{g.isSweep}}}}" hint-placeholder-val="{{{{false}}}}">{N.mark("sweep", N.LIGHT, 22)}</sc-if><sc-if value="{{{{g.isNew}}}}" hint-placeholder-val="{{{{false}}}}">{N.mark("new", N.LIGHT, 22)}</sc-if><sc-if value="{{{{g.isFb}}}}" hint-placeholder-val="{{{{false}}}}">{FB_ICON}</sc-if><span>{{{{g.label}}}}</span></div>'
        '<sc-for list="{{g.items}}" as="s" hint-placeholder-count="4"><a href="#fbl-{{s.key}}" class="ad-ni {{s.cls}}" aria-current="{{s.cur}}" onClick="{{s.pick}}"><span style="flex: 1">{{s.label}}</span><sc-if value="{{s.hasN}}" hint-placeholder-val="{{false}}"><span class="n">{{s.n}}</span></sc-if></a></sc-for></div></sc-for></nav>')

SUBTABS = '''<sc-if value="{{hasSub}}" hint-placeholder-val="{{true}}"><div class="row r-wrap fbp-tabs" role="tablist" aria-label="{{pageTitle}}" style="gap: 0; border-bottom: 1px solid #CAC4CF"><sc-for list="{{subTabs}}" as="t" hint-placeholder-count="3"><button type="button" role="tab" class="tab {{t.cls}}" aria-selected="{{t.on}}" onClick="{{t.pick}}">{{t.label}}<sc-if value="{{t.hasN}}" hint-placeholder-val="{{false}}"><span class="n">{{t.n}}</span></sc-if></button></sc-for><span style="flex: 1"></span><span class="tile in"><i></i>{{capTile}}</span></div></sc-if>'''

SCOPE = '''<sc-if value="{{hasScope}}" hint-placeholder-val="{{false}}"><div class="fbl-note"><span class="tile wn" style="flex: none"><i></i>Sweep admin</span><span>{{scopeNote}}</span></div></sc-if>
<sc-if value="{{hasSaved}}" hint-placeholder-val="{{false}}"><div class="fbl-saved"><b>{{savedName}} feedback profile saved.</b> Changes apply within 5 minutes.</div></sc-if>'''

PROFILES = '''<sc-if value="{{vProfiles}}" hint-placeholder-val="{{false}}">
<div class="card" style="padding: 0; overflow: hidden"><div class="ad-tscroll"><table class="ad-tbl" style="width: 100%; border-collapse: collapse">
  <thead><tr><th class="th">Feedback profile</th><th class="th">Status</th><th class="th">Entry points</th><th class="th">Questions</th><th class="th">Sampling</th><th class="th">Routing</th><th class="th"></th></tr></thead>
  <tbody><sc-for list="{{profiles}}" as="p" hint-placeholder-count="5">
    <tr class="rw" style="{{p.rowStyle}}"><td class="td"><b class="ui">{{p.name}}</b><div class="meta">{{p.sub}}</div></td><td class="td"><span class="tile {{p.tile}}"><i></i>{{p.status}}</span></td><td class="td"><span style="font-size: 13px">{{p.entries}}</span></td><td class="td">{{p.nq}} of 3</td><td class="td">{{p.sampling}}</td><td class="td"><span style="font-size: 13px">{{p.routing}}</span></td><td class="td" style="text-align: right; white-space: nowrap"><button type="button" class="chip" style="height: 28px" aria-label="{{p.aria}}" onClick="{{p.go}}">{{p.cta}}</button></td></tr>
  </sc-for></tbody></table></div></div>
<div class="meta" style="white-space: normal">{{profilesNote}}</div>
</sc-if>'''

EDITOR = '<sc-if value="{{fpEditing}}" hint-placeholder-val="{{false}}">' + S.ADMIN_FEEDBACK + '</sc-if>'

INBOX = '''<sc-if value="{{vInbox}}" hint-placeholder-val="{{false}}">
<div class="row r-wrap" style="gap: 8px"><sc-for list="{{inChips}}" as="t" hint-placeholder-count="5"><button type="button" class="chip" aria-pressed="{{t.on}}" style="{{t.style}}" aria-disabled="{{t.locked}}" onClick="{{t.pick}}">{{t.label}}<span class="n">{{t.n}}</span></button></sc-for></div>
<sc-for list="{{inbox}}" as="f" hint-placeholder-count="3"><div class="card" style="display: flex; gap: 14px; align-items: flex-start; padding: 16px 20px"><span class="av" style="background: {{f.bg}}; flex: none">{{f.ini}}</span><div class="stack" style="gap: 6px; flex: 1"><div class="row r-wrap" style="gap: 8px"><b class="ui" style="font-size: 14px">{{f.who}}</b><span class="tag" style="background: #E3DFFF; color: #14085E">{{f.feature}}</span><span class="tag" style="background: #ECE5F4">{{f.source}}</span><span class="meta">{{f.when}}</span></div><p style="margin: 0; font-size: 14px; line-height: 20px">{{f.text}}</p><div class="row r-wrap" style="gap: 8px"><button type="button" class="chip" style="height: 28px">Reply</button><button type="button" class="chip" style="height: 28px">Route to Jira</button><button type="button" class="chip" style="height: 28px">Propose as idea</button></div></div></div></sc-for>
<div class="meta" style="white-space: normal">{{inboxNote}}</div>
</sc-if>'''

POLICY = '''<sc-if value="{{vPolicy}}" hint-placeholder-val="{{false}}"><div class="ocard stack" style="gap: 10px">
  <div class="row r-wrap" style="gap: 8px"><span class="ui" style="font-size: 14px; font-weight: 700">Solicitation policy</span><span class="meta">one cap per user, shared by feedback prompts, micro-surveys and NPS</span></div>
  <div class="row r-wrap" style="gap: 8px"><span class="meta" style="width: 96px">At most</span><sc-for list="{{capChips}}" as="t" hint-placeholder-count="3"><button type="button" class="chip" aria-pressed="{{t.on}}" style="{{t.style}}" aria-disabled="{{t.locked}}" onClick="{{t.pick}}">{{t.label}}</button></sc-for><span class="meta">{{capNote}}</span></div>
  <div class="meta" style="white-space: normal">The Feedback page button and thumbs on AI answers are user-initiated and never count against the cap. Prompts are never shown during a running action and are always dismissible.</div>
</div></sc-if>'''

SURVEYS = '''<sc-if value="{{vSurveys}}" hint-placeholder-val="{{false}}"><div class="card" style="padding: 0; overflow: hidden"><div class="ad-tscroll"><table class="ad-tbl" style="width: 100%; border-collapse: collapse">
  <thead><tr><th class="th">Survey</th><th class="th">Type</th><th class="th">Trigger</th><th class="th">Status</th><th class="th">Responses</th></tr></thead>
  <tbody><sc-for list="{{surveys}}" as="v" hint-placeholder-count="3"><tr class="rw"><td class="td"><b class="ui">{{v.name}}</b><div class="meta">{{v.q}}</div></td><td class="td"><span class="tag" style="background: #ECE5F4">{{v.type}}</span></td><td class="td"><span style="font-size: 13px">{{v.trigger}}</span></td><td class="td"><span class="tile {{v.tile}}"><i></i>{{v.status}}</span></td><td class="td">{{v.resp}}</td></tr></sc-for></tbody></table></div></div></sc-if>'''

OVERVIEW = '''<sc-if value="{{vOverview}}" hint-placeholder-val="{{false}}">
<div class="row r-kpis" style="gap: 16px; align-items: stretch"><sc-for list="{{kpis}}" as="k" hint-placeholder-count="4"><div class="kpi"><b>{{k.v}}</b><span>{{k.label}}</span></div></sc-for></div>
<div class="r-g2" style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px">
  <div class="card stack" style="gap: 10px"><div class="h2">New feedback by feature · 7 days</div><sc-for list="{{byFeat}}" as="b" hint-placeholder-count="4"><div class="row" style="gap: 12px"><span class="ui" style="width: 110px; font-size: 13px; font-weight: 600">{{b.label}}</span><div class="bar"><i style="width: {{b.pct}}"></i></div><span style="width: 28px; font-size: 13px; text-align: right">{{b.n}}</span></div></sc-for></div>
  <div class="card stack" style="gap: 10px"><div class="row" style="justify-content: space-between"><div class="h2">Themes</div><span class="tile ai"><i></i>By the assistant</span></div><div class="row r-wrap" style="gap: 8px"><sc-for list="{{themes}}" as="t" hint-placeholder-count="4"><span class="chip" style="height: 28px; font-size: 12px">{{t.label}}<span class="n">{{t.n}}</span></span></sc-for></div>
    <div class="h2" style="font-size: 15px; margin-top: 6px">Needs attention</div><sc-for list="{{attention}}" as="a" hint-placeholder-count="2"><div class="row" style="gap: 10px; padding: 6px 0; border-top: 1px solid #ECE5F4"><span class="tile {{a.tile}}" style="flex: none"><i></i>{{a.kind}}</span><span style="font-size: 13px; line-height: 18px">{{a.text}}</span></div></sc-for></div>
</div>
</sc-if>'''

CONTENT = (SCOPE + SUBTABS + OVERVIEW + PROFILES + EDITOR + INBOX + SURVEYS + POLICY
           + '<sc-if value="{{vOther}}" hint-placeholder-val="{{false}}">' + S.ADMIN_PLACEHOLDER + '</sc-if>')

PROPOSAL = ('<div class="ad-split">' + TREE + S.ADMIN_SELECT +
            '<div class="stack" style="gap: 16px; min-width: 0">' + S.ADMIN_MODLINE + CONTENT + '</div></div>')

BODY = '''<div style="width: 1440px; min-height: 2000px; box-sizing: border-box; background: #FDF8FD; color: #1C1B1E; display: flex; flex-direction: column">
  <div style="padding: 20px 32px 12px; display: flex; flex-direction: column; gap: 12px">
    <div style="display: flex; align-items: center; gap: 16px">
      <h1 class="ui" style="margin: 0; font-size: 24px; line-height: 32px; font-weight: 700; white-space: nowrap">Feedback administration lab</h1>
      <span style="font-size: 14px; color: #48454E">Three places to administer feedback, in the adopted admin sidebar. Users still give feedback inside each feature (page button, after an action, thumbs on AI answers); only the administration moves. Same profiles, inbox, surveys and cap in each variant. View as platform admin or Sweep admin to see how rights scope it.</span>
    </div>
    <div class="r-g3" style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px">
      <sc-for list="{{tabs}}" as="t" hint-placeholder-count="3">
        <button type="button" class="ttab {{t.cls}}" aria-pressed="{{t.on}}" onClick="{{t.pick}}"><span class="row" style="gap: 8px"><span style="width: 24px; height: 24px; border-radius: 999px; background: {{t.numBg}}; color: {{t.numFg}}; font-family: Manrope, 'BNPP Type', 'Segoe UI', system-ui, sans-serif; font-size: 12px; font-weight: 700; display: inline-flex; align-items: center; justify-content: center">{{t.k}}</span><span class="ui" style="font-size: 14px; font-weight: 600">{{t.name}}</span></span><span style="font-size: 12px; line-height: 16px; color: #48454E">{{t.sub}}</span><sc-if value="{{t.cur}}" hint-placeholder-val="{{false}}"><span class="tile ok"><i></i>Adopted</span></sc-if></button>
      </sc-for>
    </div>
    <div class="row" style="gap: 12px; flex-wrap: wrap">SIMBAR<span class="row" style="gap: 8px; padding: 6px 8px 6px 12px; border: 1px dashed #79757F; border-radius: 12px"><span class="ui" style="font-size: 12px; font-weight: 600; color: #48454E">View as</span><sc-for list="{{roleChips}}" as="r" hint-placeholder-count="2"><button type="button" class="chip" style="height: 28px; font-size: 12px; {{r.style}}" aria-pressed="{{r.on}}" onClick="{{r.pick}}">{{r.label}}</button></sc-for></span><span class="row r-wrap" style="gap: 8px; padding: 6px 8px 6px 12px; border: 1px dashed #79757F; border-radius: 12px"><span class="ui" style="font-size: 12px; font-weight: 600; color: #48454E">Go to</span><sc-for list="{{goChips}}" as="r" hint-placeholder-count="3"><button type="button" class="chip" style="height: 28px; font-size: 12px; {{r.style}}" aria-pressed="{{r.on}}" onClick="{{r.pick}}">{{r.label}}</button></sc-for></span></div>
  </div>

  <div style="margin: 0 32px; border-radius: 12px; overflow: hidden; border: 1px solid #CAC4CF">
  SIMOPEN
  <div style="position: relative; width: 100%; height: 100%; display: flex; flex-direction: column; background: #FDF8FD; overflow: hidden">
    HEADER
    <div style="flex: 1; display: flex; min-height: 0">
      <div class="ad-railwrap">RAIL</div>
      <main style="position: relative; flex: 1; min-width: 0; padding: 20px 32px 24px; box-sizing: border-box; display: flex; flex-direction: column; gap: 16px; overflow: auto">
        PROPOSAL
      </main>
    </div>
    NAVBAR
  </div>
  SIMCLOSE
  </div>

  <div style="padding: 20px 32px 32px; display: grid; grid-template-columns: minmax(0, 1fr) 420px; gap: 24px; align-items: start">
    <div class="card" style="padding: 0; overflow: hidden">
      <table class="cmp" style="width: 100%; border-collapse: collapse">
        <thead><tr><th style="width: 24px"></th><th style="width: 120px">Variant</th><th>A profile is edited in</th><th>A Sweep admin needs</th><th>Overview across features</th><th>Natural owner</th><th>Cost</th><th>Trade-off</th></tr></thead>
        <tbody>
          <sc-for list="{{rows}}" as="r" hint-placeholder-count="3">
            <tr class="{{r.cls}}"><td><span class="ui" style="font-weight: 700">{{r.k}}</span></td><td><span class="ui" style="font-weight: 600">{{r.name}}</span></td><td>{{r.where}}</td><td>{{r.sweep}}</td><td>{{r.overview}}</td><td>{{r.owner}}</td><td>{{r.cost}}</td><td style="color: #48454E">{{r.trade}}</td></tr>
          </sc-for>
        </tbody>
      </table>
    </div>
    <div style="display: flex; flex-direction: column; gap: 16px">
      <div class="card" style="display: flex; flex-direction: column; gap: 8px">
        <div class="row" style="justify-content: space-between"><span class="h2">Adopted · A</span><span class="tile ok"><i></i>Community › Feedback</span></div>
        <div style="font-size: 13px; line-height: 18px; color: #48454E">The platform team reads the inbox, so feedback stays in Community, next to ideas, releases and discussions: listen, decide, ship, announce in one module. Every profile is edited in Community › Feedback; a feature admin gets the scoped right <b style="color: #1C1B1E">Feedback · &lt;feature&gt;</b>, separate from Community admin, and sees only their profile, their inbox and the cap (read-only). Applied to the live Community prototype.</div>
        <div style="font-size: 13px; line-height: 18px; color: #48454E"><b style="color: #1C1B1E">Kept reversible.</b> FeedbackProfile stays a component of its own and the right is per feature, so moving to <b style="color: #1C1B1E">B</b> later (a dedicated team takes the inbox, or an Overview across features is needed) is moving one group in the sidebar. <b style="color: #1C1B1E">1</b> fits if feature teams one day own their feedback end to end.</div>
      </div>
      <div class="ocard" style="display: flex; flex-direction: column; gap: 6px; font-size: 13px; line-height: 18px; color: #48454E">
        <span class="ui" style="font-size: 14px; font-weight: 700; color: #1C1B1E">Same in every variant</span>
        <span>The FeedbackProfile editor (entry points, up to 3 questions, sampling, routing, options, live preview), one inbox with reply / route to Jira / propose as idea (with the author’s consent), surveys, and one solicitation cap per user set by the platform team. Bugs go to Jira, never to Ideas.</span>
      </div>
    </div>
  </div>
</div>'''

LOGIC = r'''
class Component extends DCLogic {
  constructor(props) { super(props); this.simHostId = 'sim-host-fbl'; this.simDefault = 1374; this.state = { v: 'A', role: 'platform', page: 'cfeed', sub: {}, fp: null, fpEdit: null, inF: 'all', cap: '7', saved: null, simW: null, simAvail: 0 }; }
/*SIMJS*/
/*ADMINJS*/
  componentDidMount() { var self = this; this.simSync(); if (typeof window !== 'undefined') window.addEventListener('resize', function () { self.simSync(); }); }
  componentDidUpdate() { this.simSync(); }
  renderVals() {
    var s = this.state, self = this, sim = this.simVals();
    var set = function (o) { return function (e) { if (e && e.preventDefault) e.preventDefault(); self.setState(typeof o === 'function' ? o(e) : o); }; };
    var ON = 'background: #E3DFFF; border-color: #E3DFFF; color: #191836';
    var v = s.v, platform = s.role === 'platform';
    var LAND = { '1': 'sfeed', A: 'cfeed', B: 'b-overview' };
    var defs = [
      { k: '1', name: 'In each feature', sub: 'A Feedback section in every feature module, with the shared editor from Community; Listening keeps the overview.',
        where: 'The feature’s Feedback section (Sweep › Feedback)', sweep: 'The Sweep right only', overview: 'Community › Listening, read-only', owner: 'Each feature team', cost: 'Shared component, a section per module', trade: 'Feedback settings are spread across modules; the cross-feature view is read-only.' },
      { k: 'A', name: 'Community › Feedback', sub: 'Listening becomes Feedback, admin only: profiles, inbox, surveys and the cap all live in Community.', cur: true,
        where: 'Community › Feedback › Profiles', sweep: 'A scoped Community right (Feedback · Sweep)', overview: 'Yes, same page', owner: 'Community team', cost: 'Lowest: a rename and editable profiles', trade: 'Community grows; a Sweep admin goes through Community to tune Sweep.' },
      { k: 'B', name: 'Feedback module', sub: 'Its own admin group and remote module beside Core; Community keeps communication, Sweep keeps a shortcut.',
        where: 'Feedback › Profiles', sweep: 'Feedback admin, scoped to Sweep', overview: 'Yes, an Overview page', owner: 'Platform or support team', cost: 'One more module and one more right', trade: 'Feedback and ideas sit in two modules; a hop between them.' }
    ];
    var tabs = defs.map(function (d) { var on = v === d.k; return { k: d.k, name: d.name, sub: d.sub, cur: !!d.cur, on: on, cls: on ? 'ttab-on' : '', numBg: on ? '#35307E' : '#E3DFFF', numFg: on ? '#FFFFFF' : '#14085E', pick: set({ v: d.k, page: LAND[d.k], fpEdit: null, saved: null, inF: 'all' }) }; });
    var rows = defs.map(function (d) { return Object.assign({}, d, { cls: v === d.k ? 'on' : '' }); });

    // ---- navigation per variant, filtered by rights
    var core = { key: 'core', label: 'Core', core: true, items: [ { key: 'general', label: 'General' }, { key: 'users', label: 'Users and permissions', n: 1 }, { key: 'groups', label: 'Groups' }, { key: 'audit', label: 'Audit log' } ] };
    var sw = [ { key: 'connectors', label: 'Connectors', n: 1 } ];
    if (v === '1') sw.push({ key: 'sfeed', label: 'Feedback', n: 2 });
    if (v === 'B') sw.push({ key: 'sfeedlink', label: 'Feedback ↗', n: 2 });
    var sweep = { key: 'sweep', label: 'Sweep', isSweep: true, remote: 'sweep-admin@1.4', owner: 'Platform team', items: sw };
    var cm = [ { key: 'releases', label: 'Releases', n: 5 }, { key: 'tours', label: 'Tours', n: 4 } ];
    if (v === '1') cm.push({ key: 'listen', label: 'Listening', n: 6 });
    if (v === 'A') cm.push({ key: 'cfeed', label: platform ? 'Feedback' : 'Feedback · Sweep', n: platform ? 6 : 2 });
    cm.push({ key: 'ideas', label: 'Ideas triage', n: 5 }, { key: 'insights', label: 'Insights' });
    var comm = { key: 'new', label: 'Community', isNew: true, remote: 'community-admin@4.6', owner: 'Platform team', items: cm };
    var fbg = { key: 'fb', label: 'Feedback', isFb: true, remote: 'feedback-admin@1.0', owner: 'Platform team', items: [ { key: 'b-overview', label: 'Overview' }, { key: 'b-inbox', label: 'Inbox', n: platform ? 6 : 2 }, { key: 'b-profiles', label: 'Profiles', n: platform ? 5 : 1 }, { key: 'b-surveys', label: 'Surveys', n: 3 }, { key: 'b-policy', label: 'Solicitation policy' } ] };
    var all = v === 'B' ? [core, fbg, sweep, comm] : [core, sweep, comm];
    var groupsRaw = platform ? all : all.filter(function (g) { return !g.core; }).map(function (g) {
      if (g.key === 'new') return v === 'A' ? Object.assign({}, g, { items: g.items.filter(function (i) { return i.key === 'cfeed'; }) }) : null;
      if (g.key === 'fb') return Object.assign({}, g, { items: g.items.filter(function (i) { return i.key !== 'b-surveys'; }) });
      return g;
    }).filter(Boolean);
    var go = function (key) { return key === 'sfeedlink' ? set({ page: 'b-inbox', inF: 'Sweep', fpEdit: null, saved: null }) : set({ page: key, fpEdit: null, saved: null }); };
    var nav = this.adminNav(groupsRaw, s.page, go), cur = nav.cur, key = cur.s.key;
    var FBKEYS = ['sfeed', 'listen', 'cfeed', 'b-overview', 'b-inbox', 'b-profiles', 'sfeedlink'];
    var goChips = [];
    groupsRaw.forEach(function (g) { g.items.forEach(function (i) { if (FBKEYS.indexOf(i.key) >= 0) { var on = key === i.key; goChips.push({ label: g.label + ' · ' + i.label, on: on, style: on ? ON : '', pick: go(i.key) }); } }); });
    var roleChips = [ { k: 'platform', label: 'Platform admin' }, { k: 'sweep', label: 'Sweep admin' } ].map(function (r) { var on = s.role === r.k; return { label: r.label, on: on, style: on ? ON : '', pick: set({ role: r.k, page: LAND[v], fpEdit: null, saved: null, inF: r.k === 'sweep' ? 'Sweep' : 'all' }) }; });

    // ---- sub-tabs (variant 1 Feedback section and Listening; variant A Community › Feedback)
    var SUBS = { sfeed: [ { k: 'profile', label: 'Profile' }, { k: 'inbox', label: 'Inbox', n: 2 } ],
      listen: [ { k: 'profiles', label: 'Feedback profiles', n: 5 }, { k: 'surveys', label: 'Surveys', n: 3 }, { k: 'inbox', label: 'Inbox', n: 6 } ],
      cfeed: platform ? [ { k: 'profiles', label: 'Profiles', n: 5 }, { k: 'inbox', label: 'Inbox', n: 6 }, { k: 'surveys', label: 'Surveys', n: 3 }, { k: 'policy', label: 'Solicitation policy' } ] : [ { k: 'profiles', label: 'Profile' }, { k: 'inbox', label: 'Inbox', n: 2 }, { k: 'policy', label: 'Solicitation policy' } ] };
    var subDefs = SUBS[key] || null, sub = subDefs ? ((s.sub || {})[key] || subDefs[0].k) : null;
    var subTabs = (subDefs || []).map(function (t) { var on = sub === t.k; return { label: t.label, n: t.n, hasN: !!t.n, on: on, cls: on ? 'tab-on' : '', pick: set(function () { var o = Object.assign({}, s.sub || {}); o[key] = t.k; return { sub: o, fpEdit: null, saved: null }; }) }; });
    var view = key === 'b-overview' ? 'overview' : key === 'b-inbox' ? 'inbox' : key === 'b-profiles' ? 'profiles' : key === 'b-surveys' ? 'surveys' : key === 'b-policy' ? 'policy' : key === 'sfeed' ? (sub === 'inbox' ? 'inbox' : 'feat') : (key === 'listen' || key === 'cfeed') ? sub : 'other';

    // ---- profiles (shared FeedbackProfile logic)
    var FB = this.feedbackProfiles(s, set, { onSave: function (name) { return { saved: name }; } });
    var readOnly = v === '1';
    var keys = FB.keys.filter(function (k) { return platform || k === 'sweep'; });
    var profiles = keys.map(function (k) { var p = FB.summary(k), mine = !readOnly || k === 'global', open = s.fpEdit === k || (!platform && !s.fpEdit && k === 'sweep' && !readOnly);
      return Object.assign(p, { sub: 'Owner: ' + p.owner + (readOnly ? ' · edited in ' + p.home : ''), rowStyle: open ? 'box-shadow: inset 3px 0 0 #35307E' : '',
        cta: mine ? 'Edit' : 'Open in ' + p.name, aria: (mine ? 'Edit the ' : 'Open the ') + p.name + ' feedback profile',
        go: mine ? set({ fpEdit: s.fpEdit === k ? null : k, saved: null }) : k === 'sweep' ? go('sfeed') : set({}) }); });
    var editKey = view === 'feat' ? 'sweep' : view === 'profiles' ? (readOnly ? (s.fpEdit === 'global' ? 'global' : null) : (s.fpEdit || (!platform ? 'sweep' : null))) : null;
    var fp = editKey ? FB.editor(editKey, { canClose: platform && view !== 'feat', close: set({ fpEdit: null }) }) : {};
    var profilesNote = readOnly ? 'Read-only overview: each feature edits its profile in its own Feedback section, with the same editor. Only the global profile is edited here.' : (v === 'A' ? 'All profiles are edited here, in Community. Feature admins see only their own feature’s profile.' : 'All profiles are edited in the Feedback module. Feature admins see only their own feature’s profile.');

    // ---- inbox
    var IN = [
      { ini: 'YD', bg: '#C3F4DC', who: 'Yann Dupont', feature: 'Sweep', source: 'After a run', when: '1 h ago', text: 'The Test phase took 9 minutes on a docs-only change. Could Sweep skip tests when only Markdown changed?' },
      { ini: 'NR', bg: '#E3DFFF', who: 'Nadia Rahal', feature: 'Assistant', source: 'AI answer', when: '3 h ago', text: 'Answer cited a log line that does not exist in the run. Reason picked: wrong facts.' },
      { ini: 'LB', bg: '#FFDEA0', who: 'Lucas Bernard', feature: 'Environments', source: 'Page button', when: 'yesterday', text: 'The promotion button is disabled with no reason shown. I lost 20 minutes before asking in Teams.' },
      { ini: 'PS', bg: '#9CF1F0', who: 'Priya Sharma', feature: 'Sweep', source: 'Page button', when: 'yesterday', text: 'Love the PR summaries. Would be great to choose which reviewers get them by email.' },
      { ini: 'MK', bg: '#9CF1F0', who: 'Marta Kowalski', feature: 'Docs', source: 'Page button', when: '2 days ago', text: 'The runner setup page still shows the old CLI flags.' },
      { ini: 'LB', bg: '#FFDEA0', who: 'Lucas Bernard', feature: 'Assistant', source: 'Discussion', when: '3 days ago', text: 'No reply for 2 working days: “Do MCP servers pinned to the old tool schema need a redeploy before 3 November?”' }
    ];
    var locked = !platform || key === 'sfeed', inCur = locked ? 'Sweep' : s.inF;
    var inChips = ['all', 'Sweep', 'Environments', 'Docs', 'Assistant'].filter(function (k) { return !locked || k === 'Sweep'; }).map(function (k) { var on = inCur === k; return { label: k === 'all' ? 'All features' : k, n: IN.filter(function (f) { return k === 'all' || f.feature === k; }).length, on: on, style: on ? ON : '', locked: locked, pick: set({ inF: k }) }; });
    var inbox = IN.filter(function (f) { return inCur === 'all' || f.feature === inCur; });
    var inboxNote = key === 'sfeed' ? 'The Listening inbox component, filtered on Sweep and embedded in the Sweep module.' : (key === 'b-inbox' && s.inF === 'Sweep' && platform ? 'Opened from Sweep › Feedback ↗: the same module, filtered on Sweep.' : 'One inbox for every feature; filter by feature.');

    // ---- policy, surveys, overview
    var capChips = [ { k: '7', label: '1 prompt / 7 days' }, { k: '14', label: '1 prompt / 14 days' }, { k: '30', label: '1 prompt / 30 days' } ].map(function (c) { var on = s.cap === c.k; return { label: c.label, on: on, style: on ? ON : '', locked: !platform, pick: platform ? set({ cap: c.k }) : set({}) }; });
    var surveys = [ { name: 'Run experience', q: 'How easy was it to understand why this run failed?', type: 'Micro-survey', trigger: 'After a failed run', status: 'Live', tile: 'ok', resp: 214 }, { name: 'Quarterly NPS', q: 'How likely are you to recommend AIToolbox?', type: 'NPS', trigger: 'Every 90 days', status: 'Live', tile: 'ok', resp: 388 }, { name: 'Secrets policy check', q: 'I have read the new secrets policy', type: 'Check', trigger: 'Next sign-in', status: 'Scheduled', tile: 'ne', resp: '—' } ];
    var kpis = platform ? [ { v: '38', label: 'new this week' }, { v: '1.4 days', label: 'median first reply' }, { v: '4.1 / 5', label: 'after-action score' }, { v: '18 %', label: 'users prompted this week' } ] : [ { v: '14', label: 'new this week · Sweep' }, { v: '0.9 days', label: 'median first reply' }, { v: '3.8 / 5', label: 'after-run score' }, { v: '20 %', label: 'sampling' } ];
    var BF = [ { label: 'Sweep', n: 14 }, { label: 'Assistant', n: 11 }, { label: 'Environments', n: 7 }, { label: 'Docs', n: 6 } ].filter(function (b) { return platform || b.label === 'Sweep'; });
    var byFeat = BF.map(function (b) { return { label: b.label, n: b.n, pct: Math.round(b.n / 14 * 100) + '%' }; });
    var themes = (platform ? [ { label: 'Slow test phase', n: 9 }, { label: 'Wrong facts in answers', n: 6 }, { label: 'Disabled with no reason', n: 4 }, { label: 'Outdated docs', n: 3 } ] : [ { label: 'Slow test phase', n: 9 }, { label: 'Reviewer emails', n: 3 } ]);
    var attention = platform ? [ { kind: 'No reply', tile: 'wn', text: '3 items older than 2 working days (Assistant 2, Docs 1)' }, { kind: 'Spike', tile: 'er', text: 'Environments: 5 “disabled with no reason” since yesterday' } ] : [ { kind: 'No reply', tile: 'wn', text: '1 Sweep item older than 2 working days' } ];

    var SCOPE = { '1': 'You see the Sweep module only; feedback is one of its sections, next to Connectors. No Community right is needed.', A: 'Community shows only “Feedback · Sweep”: your profile, the Sweep inbox and the cap (read-only). Releases, tours and ideas stay hidden.', B: 'The Feedback module is filtered on Sweep (right “Feedback admin · Sweep”). Surveys stay with the platform team and the cap is read-only.' };
    var SUMM = { users: '1,284 users from the directory · 46 admins · 1 request', groups: '18 groups', audit: 'Last 90 days', general: 'Workspace, language, time zone, retention', connectors: '5 connectors · 1 needs attention', sfeed: 'Feedback profile and Sweep inbox', listen: 'All feedback profiles (read-only), surveys, inbox', cfeed: platform ? 'Profiles, inbox, surveys, solicitation policy' : 'Sweep profile, Sweep inbox, cap (read-only)', releases: '5 releases', tours: '4 tours', ideas: '5 ideas to triage', insights: 'Feedback forms, surveys and tours, last 30 days', 'b-overview': platform ? 'Every feature, last 7 days' : 'Sweep, last 7 days', 'b-inbox': platform ? '6 new' : '2 new · Sweep', 'b-profiles': platform ? '5 profiles' : 'Sweep profile', 'b-surveys': '3 surveys', 'b-policy': '1 prompt per user every ' + s.cap + ' days' };
    return Object.assign(sim, { tabs: tabs, rows: rows, roleChips: roleChips, goChips: goChips,
      groups: nav.groups, page: key, pageTitle: cur.s.label, onSelect: function (e) { var k = e && e.target ? e.target.value : null; if (k) go(k)(e); },
      hdrFeature: 'Administration · ' + cur.g.label, hdrSummary: cur.s.label + ' · ' + (SUMM[key] || ''),
      isFeaturePage: !cur.g.core, modRemote: cur.g.remote || '', modOwner: cur.g.owner || '', modScope: platform ? 'Full module' : (cur.g.key === 'sweep' ? 'Full module' : 'Scoped to Sweep'),
      hasScope: !platform && FBKEYS.indexOf(key) >= 0, scopeNote: SCOPE[v], hasSaved: !!s.saved, savedName: s.saved || '',
      hasSub: !!subDefs, subTabs: subTabs, capTile: 'Shared cap · 1 prompt per user every ' + s.cap + ' days' + (platform ? '' : ' · set by the platform team'),
      vOverview: view === 'overview', vProfiles: view === 'profiles', vInbox: view === 'inbox', vSurveys: view === 'surveys', vPolicy: view === 'policy' || (key === 'listen' && view === 'profiles'), vOther: view === 'other',
      profiles: profiles, profilesNote: profilesNote, fpEditing: !!editKey, fp: fp,
      inChips: inChips, inbox: inbox, inboxNote: inboxNote, capChips: capChips, capNote: platform ? 'Applies to every feature' : 'Set by the platform team', surveys: surveys,
      kpis: kpis, byFeat: byFeat, themes: themes, attention: attention });
  }
}
'''

body = (BODY.replace('SIMBAR', S.sim_bar()).replace('SIMOPEN', S.sim_open('sim-host-fbl', 'height: 1080px')).replace('SIMCLOSE', S.SIM_CLOSE)
        .replace('HEADER', S.header(False)).replace('RAIL', N.rail(N.LIGHT, 'admin')).replace('NAVBAR', S.navbar(N.LIGHT, 'none')).replace('PROPOSAL', PROPOSAL))
logic = LOGIC.replace('/*SIMJS*/', S.SIM_JS).replace('/*ADMINJS*/', S.ADMIN_JS)
out = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>Feedback administration lab, three variants</title>\n<script src="./support.js"></script>\n</head>\n<body>\n<x-dc>\n<helmet>\n'
       '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&amp;family=Open+Sans:wght@400;600;700&amp;display=swap">\n'
       '<style>\n' + S.CSS + '\n' + S.SIM_CSS + S.ADMIN_CSS + CSS_LAB + CSS_FB + '</style>\n</helmet>\n' + body + '\n</x-dc>\n'
       '<script type="text/x-dc" data-dc-script data-props=\'{"$preview":{"width":1440,"height":2000}}\'>' + logic + '</script>\n</body>\n</html>\n')
for t in ['sc-if', 'sc-for']:
    assert len(re.findall(rf'<{t}\b', out)) == len(re.findall(rf'</{t}>', out)), t
for ph in ['SIMBAR', 'PROPOSAL', 'HEADER', 'NAVBAR', 'SIMOPEN']:
    assert ph not in out, ph
open(dst, 'w', encoding='utf-8').write(out); print(len(out))
