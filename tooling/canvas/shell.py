"""Shared AIToolbox shell (header + default rail) and base CSS for the Adoption boards.
Replaces <!--CSS-->, <!--HEADER-->, <!--RAIL--> in a board source."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import navgen as N
UI = N.UI

CSS = """body{margin:0;font-family:'Open Sans',system-ui,sans-serif}
button{cursor:pointer} a{color:#35307E}a:hover{color:#14085E}
:focus-visible{outline:2px solid #35307E;outline-offset:2px}
.ui{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif}
.ib{position:relative;width:40px;height:40px;border:0;border-radius:999px;background:transparent;color:#48454E;display:inline-flex;align-items:center;justify-content:center;margin:4px}
.ib:hover{background:rgba(53,48,126,.06)}
.btn{height:40px;padding:0 24px;border:0;border-radius:16px;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:14px;font-weight:600;display:inline-flex;align-items:center;gap:8px;white-space:nowrap;text-decoration:none}
.btn-i{padding-left:16px}
.f{background:#35307E;color:#FFFFFF}.t{background:#E3DFFF;color:#191836}.o{background:transparent;border:1px solid #79757F;color:#35307E}.x{background:transparent;color:#35307E;padding:0 12px}
.chip{height:32px;padding:0 12px;border-radius:8px;border:1px solid #79757F;background:transparent;color:#1C1B1E;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:14px;font-weight:500;display:inline-flex;align-items:center;gap:6px;white-space:nowrap;text-decoration:none}
.chip:hover{background:rgba(53,48,126,.06)}
.chip-on{background:#E3DFFF;border-color:#E3DFFF;color:#191836}
.tag{display:inline-flex;align-items:center;gap:6px;height:24px;padding:0 8px;border-radius:4px;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:600;white-space:nowrap}
.tagt{padding-left:4px}
.env{display:inline-flex;align-items:center;height:24px;padding:0 10px;border-radius:8px;background:#E3DFFF;color:#191836;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:600;white-space:nowrap}
.mono{font-family:'Open Sans',system-ui,sans-serif;font-weight:600}
.card{background:#FFFFFF;border-radius:12px;padding:16px;box-shadow:0 1px 2px rgba(0,0,0,.3),0 1px 3px 1px rgba(0,0,0,.15)}
.ocard{background:#FDF8FD;border:1px solid #CAC4CF;border-radius:12px;padding:16px}
.tab{height:48px;padding:0 16px;border:0;background:transparent;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:14px;font-weight:600;display:inline-flex;align-items:center;gap:8px;border-radius:3px 3px 0 0;color:#48454E;border-bottom:3px solid transparent}
.tab-on{color:#35307E;border-bottom:3px solid #35307E}
.n{font-size:11px;padding:1px 6px;border-radius:6px;background:#F2EBFA;color:#48454E}
.fld{position:relative;box-sizing:border-box;min-height:56px;border:1px solid #79757F;border-radius:4px;padding:16px 16px 10px;background:#FDF8FD}
.fld label{position:absolute;top:-9px;left:12px;padding:0 4px;background:#FDF8FD;font-size:12px;line-height:16px;color:#48454E}
.fld input,.fld textarea,.fld select{width:100%;border:0;outline:0;background:transparent;font:400 16px/24px 'Open Sans',system-ui,sans-serif;color:#1C1B1E;padding:0;resize:none}
.av{width:32px;height:32px;border-radius:999px;background:#D4D0F9;color:#191836;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:13px;font-weight:700;display:inline-flex;align-items:center;justify-content:center;flex:none}
.h2{margin:0;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:18px;line-height:24px;font-weight:600;color:#1C1B1E}
.th{height:48px;padding:0 12px;text-align:left;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:600;letter-spacing:.5px;text-transform:uppercase;color:#48454E;white-space:nowrap}
.td{height:52px;padding:6px 12px;font-size:14px;color:#1C1B1E;border-top:1px solid #CAC4CF;vertical-align:middle}
.mi{width:100%;height:48px;padding:0 16px;border:0;background:transparent;display:flex;align-items:center;gap:12px;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:14px;font-weight:500;color:#1C1B1E;text-align:left;text-decoration:none}
.mi:hover{background:rgba(53,48,126,.06)}"""

ST = 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
BOT = '<svg width="24" height="24" viewBox="0 0 64 64" aria-hidden="true" style="overflow:visible"><g transform="translate(-3.200 -8.150) scale(1.1)"><path d="M26 56h-3a9 9 0 0 1-9-9v-4.0l-5-4 5-4v-4.0a9 9 0 0 1 9-9h2.0l7-5 7 5h2.0a9 9 0 0 1 9 9v4.0l5 4-5 4v4.0a9 9 0 0 1-9 9h-3" fill="none" stroke="#35307E" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/><path d="M26 37l6 5-6 5" fill="none" stroke="#35307E" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M35 49h5" fill="none" stroke="#008857" stroke-width="4.5" stroke-linecap="round"/></g></svg>'
BELL = '<svg width="24" height="24" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="8" r="3.6" fill="#35307E"/><path d="M32 9C22 9 17 17 17 27V38L12 46Q11 48.5 13.5 48.5H50.5Q53 48.5 52 46L47 38V27C47 17 42 9 32 9Z" fill="#35307E"/><circle cx="32" cy="53.5" r="5" fill="#278383"/></svg>'
LOGO = '<svg width="32" height="28" viewBox="0 0 74 64" aria-hidden="true"><mask id="sh-lg" maskUnits="userSpaceOnUse" x="0" y="0" width="74" height="64"><rect width="74" height="64" fill="#fff"/><rect x="37" y="3" width="36" height="24" rx="7" fill="#000"/></mask><g mask="url(#sh-lg)"><path d="M21 23v-6a6 6 0 0 1 6-6h10a6 6 0 0 1 6 6v6" fill="none" stroke="#0D0B14" stroke-width="6" stroke-linecap="round"/><rect x="4" y="22" width="56" height="36" rx="10" fill="#0D0B14"/><path d="M17.5 33l8 7-8 7" fill="none" stroke="#FFFFFF" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M33.5 47h13" fill="none" stroke="#00F29E" stroke-width="5.5" stroke-linecap="round"/></g><rect x="39.5" y="5.5" width="31" height="19" rx="5" fill="#80D5D4"/><text x="55" y="20" text-anchor="middle" font-family="Manrope, sans-serif" font-weight="800" font-size="14" fill="#003737">AI</text></svg>'

def ctx(feature, summary, dark=False):
    """Page context block of the top app bar: feature name (line 1) and summary (line 2), right of the logo.
    Replaces page titles and breadcrumbs; going back uses a subheader."""
    fg, mut, div = ('#ECE5F8', '#CAC3DC', '#494458') if dark else ('#1C1B1E', '#48454E', '#CAC4CF')
    return (f'<div class="hctx" style="display: flex; flex-direction: column; justify-content: center; gap: 1px; min-width: 0; margin-left: 16px; padding-left: 16px; border-left: 1px solid {div}">'
            f'<span class="hf" style="font-family: {UI}; font-size: 14px; line-height: 18px; font-weight: 600; color: {fg}; white-space: nowrap; overflow: hidden; text-overflow: ellipsis">{feature}</span>'
            f'<span class="hs" style="font-family: \'Open Sans\', system-ui, sans-serif; font-size: 12px; line-height: 16px; color: {mut}; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 380px">{summary}</span></div>')

def header(help_open=False, feature='{{hdrFeature}}', summary='{{hdrSummary}}'):
    hb = 'background: #D4D0F9; color: #191836' if help_open else ''
    return f'''<header class="hdr" style="height: 64px; flex: none; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; gap: 16px; padding: 0 8px 0 24px; background: #EDE4FF; border-bottom: 2px solid #FDF8FD">
    <div style="justify-self: stretch; display: flex; align-items: center; min-width: 0; overflow: hidden"><button type="button" class="ib hdr-menu" aria-label="Open navigation"><svg width="22" height="22" viewBox="0 0 24 24" {ST}><path d="M4 7h16M4 12h16M4 17h16"/></svg></button><a href="#home" aria-label="AIToolbox home" style="display: flex; align-items: center; gap: 10px; text-decoration: none">{LOGO}<span class="hdr-wm" style="font-family: Manrope, sans-serif; font-weight: 800; font-size: 20px; letter-spacing: -0.035em; line-height: 1"><span style="color: #1C1B1E">AI</span><span style="color: #35307E">Toolbox</span></span></a>{ctx(feature, summary)}</div>
    <div role="search" class="hdr-search" style="width: 440px; height: 44px; box-sizing: border-box; display: flex; align-items: center; gap: 10px; padding: 0 6px 0 14px; border-radius: 16px; background: #FFFFFF; color: #48454E">
      <svg width="20" height="20" viewBox="0 0 24 24" {ST}><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
      <label for="sh-q" style="position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0)">Search, or ask the assistant</label>
      <input id="sh-q" type="text" placeholder="Search, or ask the assistant…" style="flex: 1; min-width: 0; border: 0; outline: 0; background: transparent; font: 400 14px 'Open Sans', system-ui, sans-serif; color: #1C1B1E">
      <span class="mono hdr-kbd" style="font-size: 11px; padding: 2px 8px; border-radius: 6px; border: 1px solid #CAC4CF">⌘K</span>
      <button type="button" class="ui" style="display: inline-flex; align-items: center; gap: 6px; height: 32px; padding: 0 12px 0 8px; border: 0; border-radius: 12px; background: #9CF1F0; color: #002020; font-size: 12px; font-weight: 700">{BOT.replace('width="24" height="24"','width="22" height="22"')}<span class="hdr-asklabel">Ask</span></button>
    </div>
    <div style="justify-self: end; display: flex; align-items: center">
      <button type="button" class="ib hdr-sbtn" aria-label="Search"><svg width="22" height="22" viewBox="0 0 24 24" {ST}><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg></button>
      <button type="button" class="ib hdr-asst" aria-label="Open assistant">{BOT}</button>
      <button type="button" class="ib hdr-bell" aria-label="Notifications, 3 unread">{BELL}<span class="ui" style="position: absolute; top: 3px; left: 22px; min-width: 18px; height: 18px; padding: 0 5px; box-sizing: border-box; border-radius: 9px; background: #93000A; color: #FFFFFF; font-size: 11px; font-weight: 700; line-height: 18px; text-align: center; box-shadow: 0 0 0 2px #EDE4FF">3</span></button>
      <button type="button" class="ib hdr-help" aria-label="Help" aria-haspopup="menu" aria-expanded="{'true' if help_open else 'false'}" style="{hb}"><svg width="22" height="22" viewBox="0 0 24 24" {ST}><circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1 .9-1 1.7M12 17h.01"/></svg></button>
      <span class="hdr-div" style="width: 1px; height: 24px; background: #CAC4CF; margin: 0 6px"></span>
      <button type="button" class="hdr-user" aria-label="Aurélien Heux, platform admin, account menu" aria-haspopup="menu" style="display: inline-flex; align-items: center; gap: 10px; height: 44px; padding: 0 10px 0 6px; border: 0; border-radius: 16px; background: transparent; color: #48454E; margin-right: 8px"><span class="av">AH</span><span class="hdr-uname" style="display: flex; flex-direction: column; align-items: flex-start; line-height: 1.15"><span class="ui" style="font-size: 13px; font-weight: 700; color: #1C1B1E; white-space: nowrap">Aurélien Heux</span><span style="font-size: 11px; color: #48454E">platform · admin</span></span><svg class="hdr-chev" width="18" height="18" viewBox="0 0 24 24" {ST}><path d="M6 9l6 6 6-6"/></svg></button>
    </div>
  </header>'''

def tabs(active):
    items = [("What's new", '3 new'), ('Guides', ''), ('Ideas', '12'), ('Manage', 'admin')]
    out = ['<div role="tablist" aria-label="Community" style="display: flex; align-items: center; border-bottom: 1px solid #CAC4CF">']
    for name, n in items:
        on = name == active
        out.append(f'<button type="button" role="tab" class="tab{" tab-on" if on else ""}" aria-selected="{"true" if on else "false"}">{name}{f"<span class=n>{n}</span>" if n else ""}</button>')
    out.append('</div>')
    return ''.join(out)

def build(src, dst, active='new', help_open=False):
    s = open(src, encoding='utf-8').read()
    s = s.replace('<!--CSS-->', CSS).replace('<!--HEADER-->', header(help_open)).replace('<!--RAIL-->', N.rail(N.LIGHT, active))
    for a in ["What's new", 'Guides', 'Ideas']:
        s = s.replace(f'<!--TABS:{a}-->', tabs(a))
    assert '<!--' not in s.replace('<!--TABS', ''), 'placeholder left'
    open(dst, 'w', encoding='utf-8').write(s)
    return len(s)

# ---------------------------------------------------------------------------
# Window-width simulator: a control bar outside the frame, and container queries
# inside it (the frame is the `win` container, so every proposal reacts to the
# simulated width, not to the canvas width). Size classes follow the DS:
# Compact <600 · Medium 600–839 · Expanded 840–1199 · Large 1200–1599 · XL ≥1600.
# ---------------------------------------------------------------------------
SIM_CSS = """.simbar{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:8px 12px;border-radius:12px;background:#FFFFFF;border:1px solid #CAC4CF}
.simbar .chip{height:28px;padding:0 10px;font-size:12px}
.simlab{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:700;color:#48454E;letter-spacing:.3px}
.simrange{flex:1 1 180px;min-width:140px;max-width:360px;accent-color:#35307E;margin:0 4px}
.simval{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:13px;color:#48454E;white-space:nowrap}
.simval b{color:#1C1B1E}
.simhost{width:100%;display:flex;justify-content:center;align-items:flex-start;overflow:clip;background-color:#ECE5F4;background-image:radial-gradient(#CAC4CF 1px,transparent 1px);background-size:12px 12px}
.simframe{container:win / inline-size;flex:none;box-sizing:border-box}
.nav-bar{display:none}
.hdr-sbtn,.hdr-menu{display:none!important}
@container win (max-width: 1199px){
.hdr{grid-template-columns:minmax(0,1fr) minmax(180px,320px) auto!important;gap:12px!important}
.hdr-search{width:100%!important}
.hctx .hs,.hdr-uname,.hdr-div,.hdr-asklabel,.hdr-wm{display:none!important}
.hdr-search button{padding:0 6px!important}
main{padding-left:24px!important;padding-right:24px!important}
}
@container win (max-width: 839px){
.hdr{grid-template-columns:minmax(0,1fr) minmax(150px,260px) auto!important;gap:8px!important;padding-left:16px!important}
.hdr-kbd,.hdr-help,.hdr-chev{display:none!important}
.nav-drawer{position:absolute!important;left:0;top:0;height:100vh;max-height:100%;overflow:auto;z-index:30;box-shadow:0 1px 3px rgba(0,0,0,.3),0 4px 8px 3px rgba(0,0,0,.15);border-radius:0 16px 16px 0}
}
@container win (max-width: 599px){
.hdr{height:56px!important;grid-template-columns:minmax(0,1fr) auto!important;padding:0 4px 0 12px!important}
.hdr-search{display:none!important}
.hdr-sbtn,.hdr-menu{display:inline-flex!important}
.hdr-asst{display:none!important}
.hdr-menu{margin:0 4px 0 -8px!important}
.hdr .ib{margin:4px 0!important}
.hctx{margin-left:10px!important;padding-left:10px!important}
.hdr-user{padding:0 4px!important;margin-right:0!important}
.nav-rail{display:none!important}
.nav-bar{display:flex!important}
main{padding-left:16px!important;padding-right:16px!important;padding-top:16px!important}
}"""

# ---------------------------------------------------------------------------
# Subheader: going back is never a button on its own. The back arrow sits in one row with the page title, the
# context (parent, key facts) and the page actions, so it costs one line and says where you are.
# ---------------------------------------------------------------------------
ARROW_BACK = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>'
SUBHDR_CSS = """.subhdr{display:flex;align-items:flex-start;gap:4px 8px;min-height:48px;flex-wrap:wrap;min-width:0;padding-bottom:8px;border-bottom:1px solid #CAC4CF}
.subhdr .sh-back{flex:none;margin:0 0 0 -8px!important;color:#1C1B1E;cursor:pointer}
.subhdr .sh-back:hover{background:rgba(28,27,30,.08)}
.sh-txt{flex:1 1 240px;min-width:0;display:flex;align-items:center;gap:12px;flex-wrap:nowrap;padding-top:6px}
.sh-t{margin:0;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:20px;line-height:28px;font-weight:700;color:#1C1B1E;min-width:0;flex:0 1 auto;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sh-txt>.tile,.sh-txt>.kind,.sh-txt>span:not(.sh-c){flex:none}
.sh-c{position:relative;flex:0 100 auto;min-width:0;padding-left:13px;font-size:13px;line-height:18px;color:#48454E;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sh-c::before{content:"";position:absolute;left:0;top:50%;width:1px;height:20px;margin-top:-10px;background:#CAC4CF}
.sh-act{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-left:auto;min-height:48px}
@container win (max-width: 599px){.sh-t{font-size:18px;line-height:24px;white-space:normal}.sh-txt{flex-wrap:wrap;gap:2px 12px;flex-basis:160px}.sh-c{flex-basis:100%;padding-left:0;white-space:normal}.sh-c::before{display:none}}
"""

SIM_CSS = SUBHDR_CSS + SIM_CSS

def subheader(on_click, back_label, title, ctx='', actions='', lead='', after='', cls='', tag='button'):
    """One row: back arrow (named by where it goes), optional lead (a kind tile), the title, what follows the title
    (a status chip), the context in body-small, then the page actions on the right."""
    attrs = f'type="button" onClick="{on_click}"' if tag == 'button' else 'role="button" tabindex="0"'
    return (f'<div class="subhdr {cls}"><{tag} {attrs} class="ib sh-back" aria-label="{back_label}" title="{back_label}">{ARROW_BACK}</{tag}>'
            f'<div class="sh-txt">{lead}<h2 class="sh-t">{title}</h2>{after}' + (f'<span class="sh-c">{ctx}</span>' if ctx else '') + '</div>'
            + (f'<div class="sh-act">{actions}</div>' if actions else '') + '</div>')

def sim_bar(extra=''):
    """Width controls; `extra` is markup placed before them (e.g. the prototype role chips)."""
    return (f'<div class="simbar" role="group" aria-label="Simulated window width">{extra}'
            '<span class="simlab">WINDOW</span>'
            '<sc-for list="{{simPresets}}" as="sp" hint-placeholder-count="7"><button type="button" class="chip {{sp.cls}}" aria-pressed="{{sp.on}}" title="{{sp.title}}" onClick="{{sp.pick}}">{{sp.label}}</button></sc-for>'
            '<input type="range" class="simrange" min="360" max="1920" step="10" value="{{simW}}" aria-label="Window width in pixels" onChange="{{simInput}}">'
            '<span class="simval"><b>{{simW}} px</b> · {{simClass}}<sc-if value="{{simScaled}}" hint-placeholder-val="{{false}}"> · shown at {{simPct}}</sc-if></span></div>')

def sim_open(host_id, extra_style=''):
    return (f'<div class="simhost" id="{host_id}"><div class="simframe" style="width: {{{{simW}}}}px; zoom: {{{{simZoom}}}}; {extra_style}">')

SIM_CLOSE = '</div></div>'

def navbar(t=None, active='new'):
    """Bottom NavigationBar for Compact windows: the rail destinations and the Assistant (the top-bar menu opens the drawer: Administration, Cookie policy)."""
    t = t or N.LIGHT
    items = [('sweep', 'Sweep'), ('env', 'Environments'), ('docs', 'Docs'), ('new', 'Community')]
    out = [f'<nav aria-label="Primary" class="nav-bar" style="position: sticky; bottom: 0; z-index: 3; height: 80px; flex: none; box-sizing: border-box; justify-content: space-around; align-items: center; padding: 0 4px; background: {t["bg"]}; border-top: 1px solid #CAC4CF">']
    def cell(k, label, g, on, tag='a'):
        pill = f'background: {t["abg"]}; color: {t["afg"]}' if on else f'background: transparent; color: {t["fg"]}'
        lab = f'font-weight: 700; color: {t["alab"]}' if on else f'font-weight: 500; color: {t["fg"]}'
        cur = ' aria-current="page"' if on else ''
        attrs = f'href="#{k}"{cur}' if tag == 'a' else 'type="button" aria-label="Open assistant"'
        return (f'<{tag} {attrs} style="display: flex; flex-direction: column; align-items: center; gap: 4px; min-width: 56px; padding: 0; border: 0; background: transparent; text-decoration: none">'
                f'<span style="width: 64px; height: 32px; border-radius: 16px; {pill}; display: inline-flex; align-items: center; justify-content: center">{g}</span>'
                f'<span style="font-family: {UI}; font-size: 11px; {lab}; white-space: nowrap">{label}</span></{tag}>')
    for k, label in items:
        out.append(cell(k, label, N.mark(k, t), k == active))
    out.append(cell('assistant', 'Assistant', BOT, False, 'button'))
    out.append('</nav>')
    return ''.join(out)

# Methods pasted into each board's Component (ES5). The board sets this.simHostId and this.simDefault.
SIM_JS = r"""
  simSync() {
    if (typeof document === 'undefined') return;
    var h = document.getElementById(this.simHostId); if (!h) return;
    var a = Math.round(h.clientWidth);
    // screen-fit boards: the frame takes the height left under the controls, so the rail's bottom items stay on screen
    var top = h.getBoundingClientRect().top + (window.scrollY || 0), ah = Math.round((window.innerHeight || 0) - top - 12);
    var o = {};
    if (a > 0 && Math.abs((this.state.simAvail || 0) - a) > 1) o.simAvail = a;
    if (ah > 0 && Math.abs((this.state.simAvailH || 0) - ah) > 1) o.simAvailH = ah;
    if (o.simAvail || o.simAvailH) this.setState(o);
  }
  simScale() {
    // rects are divided by this before positioning anything inside the (possibly zoomed) frame
    if (typeof document === 'undefined') return 1;
    var h = document.getElementById(this.simHostId), f = h && h.firstElementChild;
    if (!f || !this._simW) return 1;
    var z = f.getBoundingClientRect().width / this._simW;
    return z > 0.05 ? z : 1;
  }
  simVals() {
    var s = this.state, self = this, avail = s.simAvail || this.simDefault;
    var fit = s.simW == null, W = fit ? Math.max(360, Math.min(1920, avail)) : s.simW;
    var z = W > avail ? avail / W : 1;
    this._simW = W;
    var cls = W < 600 ? 'Compact' : W < 840 ? 'Medium' : W < 1200 ? 'Expanded' : W < 1600 ? 'Large' : 'Extra-large';
    var pick = function (v) { return function (e) { if (e && e.preventDefault) e.preventDefault(); self.setState({ simW: v }); }; };
    var P = [[null, 'Fit'], [360, 'Compact'], [600, 'Medium'], [840, 'Expanded'], [1200, 'Large'], [1440, 'Large'], [1920, 'Extra-large']];
    return {
      simW: W, simZoom: String(Math.round(z * 1000) / 1000), simFrameH: Math.round(Math.max(this.simMinH || 560, Math.min(this.simMaxH || 100000, s.simAvailH || this.simDefaultH || 900)) / z), simClass: cls, simScaled: z < 0.999, simPct: Math.round(z * 100) + ' %',
      simCompact: W < 600, simMediumUp: W >= 600, simExpandedUp: W >= 840, simLargeUp: W >= 1200,
      simPresets: P.map(function (p) { var v = p[0], on = fit ? v === null : v === W; return { label: v === null ? 'Fit · ' + Math.round(avail) : String(v), title: p[1], on: on, cls: on ? 'chip-on' : '', pick: pick(v) }; }),
      simInput: function (e) { var v = parseInt((e && e.target && e.target.value) || W, 10); if (v && v !== self.state.simW) self.setState({ simW: v }); }
    };
  }
"""

# ---------------------------------------------------------------------------
# Discussion: one expansion panel for What's new items and Ideas. Header = summary
# bar; body = threads (latest activity first, pages of three): an opening message
# and its replies, each with the author's role chip when they have one (Platform
# team, Champion, Author), Reply, Show more, and the new-message field.
# Same markup and same logic (qaVals) everywhere it appears.
# ---------------------------------------------------------------------------
QA_CSS = """.qa{display:flex;flex-direction:column}
.qa-h{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding-bottom:10px}
.qa-q{display:flex;gap:12px;padding:12px 0;border-top:1px solid #CAC4CF}
.qa-q p{margin:4px 0 0;font-size:14px;line-height:20px;color:#1C1B1E;max-width:72ch}
.qa-q .qtext{font-weight:600}
.qa-a{margin-top:8px;padding:8px 12px;border-radius:8px;background:#F2EBFA}
.qa-a p{font-weight:400}
.qa .sm{height:32px;padding:0 14px;border-radius:12px;font-size:13px}
.qa-empty{padding:12px 0;border-top:1px solid #CAC4CF;font-size:13px;line-height:18px;color:#48454E}
.qa-ask{display:flex;gap:12px;align-items:center;padding-top:12px;border-top:1px solid #CAC4CF}
.qa .meta{font-size:12px;color:#48454E;white-space:nowrap}
.qa{animation:qa-in .2s cubic-bezier(.2,0,0,1) both}
@keyframes qa-in{from{opacity:0;transform:translateY(-4px)}}
.qa-tog[aria-expanded="true"]{background:#E3DFFF;border-color:#E3DFFF;color:#191836}
.qa-tog svg.chev{transition:transform .2s cubic-bezier(.2,0,0,1)}
.qa-tog[aria-expanded="true"] svg.chev{transform:rotate(180deg)}
.qa-hide{margin-left:auto;height:32px;padding:0 8px 0 12px;border:0;border-radius:8px;background:transparent;color:#35307E;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:13px;font-weight:600;display:inline-flex;align-items:center;gap:4px}
.qa-hide:hover{background:rgba(53,48,126,.08)}
.qa-wait{width:8px;height:8px;border-radius:50%;background:#E8A400;flex:none}
/* summary bar: the one control of every thread, and its summary */
.qa-bar{width:100%;min-height:48px;box-sizing:border-box;display:flex;align-items:center;gap:6px 10px;flex-wrap:wrap;padding:8px 14px 8px 10px;border:1px solid #CAC4CF;border-radius:12px;background:#F7F2FA;color:#1C1B1E;text-align:left;font:inherit;cursor:pointer}
.qa-bar .meta{font-size:12px;color:#48454E;white-space:nowrap}
.qa-bar>*{flex:none}.qa-bar>.meta{flex:0 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis}
.qa-bar:hover{background:#EFE7F7}
.qa-bar[aria-expanded="true"]{border-color:#35307E;background:#F2EBFA;box-shadow:inset 0 0 0 1px #35307E}
.qa-bar .chev{color:#35307E;transition:transform .2s cubic-bezier(.2,0,0,1)}
.qa-bar[aria-expanded="true"] .chev{transform:rotate(180deg)}
.qa-bar-t{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:14px;font-weight:700}
.qa-bar-act{margin-left:auto;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:13px;font-weight:600;color:#35307E}
.qa-ppl{display:inline-flex;padding-left:4px}.qa-ppl .av{width:24px;height:24px;font-size:9px;letter-spacing:-.2px;margin-left:-4px;box-shadow:0 0 0 2px #F7F2FA}
/* expansion panel: one container per thread, the summary bar is its header */
.qa-panel{border:1px solid #CAC4CF;border-radius:12px;background:#FDF8FD;overflow:hidden}
.qa-panel.open{border-color:#35307E;box-shadow:0 1px 2px rgba(0,0,0,.3),0 1px 3px 1px rgba(0,0,0,.15)}
.qa-panel .qa-bar{border:0;border-radius:0;background:#F7F2FA;padding:8px 16px 8px 12px}
.qa-panel .qa-bar:hover{background:#EFE7F7}
.qa-panel .qa-bar[aria-expanded="true"]{background:#F2EBFA;box-shadow:none;border-bottom:1px solid #CAC4CF}
.qa-panel .qa-bar:focus-visible{outline:2px solid #35307E;outline-offset:-3px;border-radius:10px}
.qa-panel .qa{padding:0 16px 12px}
.qa-panel .qa-list>.qa-q:first-child,.qa-panel .qa-empty{border-top:0}
.qa-q:focus{outline:none}.qa-q:focus-visible{outline:2px solid #35307E;outline-offset:2px;border-radius:8px}
/* show more: pages of three questions */
.qa-morebar{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:10px 0 8px;border-top:1px solid #CAC4CF}
.qa-more{min-height:32px;padding:0;border:0;background:transparent;color:#35307E;font-family:'Open Sans',system-ui,sans-serif;font-size:14px;font-weight:600;text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:1px;cursor:pointer}
.qa-more:hover{text-decoration-thickness:2px;color:#14085E}
.qa-live{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
/* discussion threads: the opening message, its replies indented under it, Reply */
.qa-q .qtext{font-weight:400}
.qa-replies{margin:10px 0 0;padding-left:14px;border-left:2px solid #E3DFFF;display:flex;flex-direction:column;gap:10px}
.qa-r{display:flex;gap:10px}.qa-r .av{width:24px;height:24px;font-size:10px}
.qa-r p{margin:2px 0 0;font-size:14px;line-height:20px;color:#1C1B1E;max-width:72ch}
.qa-r:focus{outline:none}.qa-r:focus-visible{outline:2px solid #35307E;outline-offset:2px;border-radius:6px}
.qa-earlier{align-self:flex-start;min-height:24px;font-size:13px}
.qa-acts{gap:12px!important;margin-top:8px}
.qa-reply{margin-top:8px;gap:8px!important}
@container win (max-width: 599px){.qa-bar{flex-wrap:wrap!important}.qa-q>.av{width:24px;height:24px;font-size:10px}.qa-q{gap:8px!important}.qa-replies{padding-left:10px}}
@media (prefers-reduced-motion: reduce){.qa{animation:none}.qa-tog svg.chev,.qa-bar .chev{transition:none}}"""

_PLUS = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>'

_CHEV = '<svg class="chev" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
_CHEV_UP = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 15l6-6 6 6"/></svg>'

def qa_toggle(x):
    """Disclosure button for a Q&A thread: label, waiting dot, chevron; aria-expanded / aria-controls; selected look when open."""
    return (f'<button type="button" class="chip qa-tog" id="{{{{{x}.qaTogId}}}}" aria-expanded="{{{{{x}.qaOpen}}}}" aria-controls="{{{{{x}.qaRegionId}}}}" aria-label="{{{{{x}.qaTogAria}}}}" onClick="{{{{{x}.qaToggle}}}}">'
            f'{{{{{x}.qaTogLabel}}}}<sc-if value="{{{{{x}.qaHasWaiting}}}}" hint-placeholder-val="{{{{false}}}}"><span class="qa-wait" aria-hidden="true"></span></sc-if>{_CHEV}</button>')

def qa_block_chip(x):
    """Former pattern (B in the Q&A pattern lab): thread header with Hide questions, opened by qa_toggle(). Kept for the record."""
    return (f'<sc-if value="{{{{{x}.qaOpen}}}}" hint-placeholder-val="{{{{true}}}}"><div class="qa" id="{{{{{x}.qaRegionId}}}}" role="region" aria-label="Questions">'
            f'<div class="qa-h"><span class="ui" style="font-size: 14px; font-weight: 600">Questions · {{{{{x}.qaN}}}}</span>'
            f'<sc-if value="{{{{{x}.qaHasAnswered}}}}" hint-placeholder-val="{{{{true}}}}"><span class="tile ok"><i></i>{{{{{x}.qaAnsweredLabel}}}}</span></sc-if>'
            f'<sc-if value="{{{{{x}.qaHasWaiting}}}}" hint-placeholder-val="{{{{true}}}}"><span class="tile wn"><i></i>{{{{{x}.qaWaitingLabel}}}}</span></sc-if>'
            f'<button type="button" class="qa-hide" aria-controls="{{{{{x}.qaRegionId}}}}" aria-expanded="true" onClick="{{{{{x}.qaHide}}}}">Hide questions{_CHEV_UP}</button>'
            '</div>'
            + qa_empty(x) + qa_items(x) + qa_ask(x) +
            '</div></sc-if>')

def qa_empty(x):
    return (f'<sc-if value="{{{{{x}.qaEmpty}}}}" hint-placeholder-val="{{{{false}}}}"><div class="qa-empty">No messages yet. Start the discussion: champions and the platform team take part.</div></sc-if>')

def _msg_head(m):
    return ('<div class="row" style="gap: 8px; flex-wrap: wrap"><b class="ui" style="font-size: 13px">{{' + m + '.who}}</b>'
            '<sc-if value="{{' + m + '.hasRole}}" hint-placeholder-val="{{false}}"><span class="tile {{' + m + '.roleTile}}"><i></i>{{' + m + '.role}}</span></sc-if>'
            '<span class="meta">{{' + m + '.when}}</span></div>')

def qa_items(x, lst='qa'):
    """The threads of a discussion: the opening message, then its replies (the last two, earlier ones behind a link), Reply, and the reply field."""
    return (f'<sc-for list="{{{{{x}.{lst}}}}}" as="q" hint-placeholder-count="2"><div class="qa-q" id="qa-q-{{{{q.id}}}}" tabindex="-1">'
            '<span class="av" style="background: {{q.bg}}">{{q.ini}}</span><div style="flex: 1; min-width: 0">'
            + _msg_head('q') + '<p class="qtext">{{q.text}}</p>'
            '<sc-if value="{{q.hasReplies}}" hint-placeholder-val="{{true}}"><div class="qa-replies" id="qa-rp-{{q.id}}">'
            '<sc-if value="{{q.hasHidden}}" hint-placeholder-val="{{false}}"><button type="button" class="qa-more qa-earlier" aria-controls="qa-rp-{{q.id}}" onClick="{{q.showEarlier}}">{{q.earlierLabel}}</button></sc-if>'
            '<sc-for list="{{q.shownReplies}}" as="m" hint-placeholder-count="2"><div class="qa-r" id="qa-m-{{m.id}}" tabindex="-1"><span class="av" style="background: {{m.bg}}">{{m.ini}}</span><div style="flex: 1; min-width: 0">'
            + _msg_head('m') + '<p>{{m.text}}</p></div></div></sc-for></div></sc-if>'
            '<div class="row qa-acts"><button type="button" class="lnk" aria-expanded="{{q.replying}}" aria-controls="qa-rf-{{q.id}}" onClick="{{q.startReply}}">Reply</button><span class="meta">{{q.repliesLabel}}</span></div>'
            '<sc-if value="{{q.replying}}" hint-placeholder-val="{{false}}"><div class="row qa-reply" id="qa-rf-{{q.id}}"><div class="fld" style="flex: 1; min-height: 40px; padding: 8px 12px"><label for="{{q.replyId}}">Reply to {{q.who}}</label><input id="{{q.replyId}}" type="text" value="{{q.replyDraft}}" onChange="{{q.onReplyDraft}}" placeholder="Everyone in the thread is notified"></div><button type="button" class="btn f sm" onClick="{{q.sendReply}}">Send</button></div></sc-if>'
            '</div></div></sc-for>')

def qa_ask(x):
    return (f'<div class="qa-ask"><span class="av">AH</span><div class="fld" style="flex: 1; min-height: 44px; padding: 10px 12px"><label for="{{{{{x}.qaAskId}}}}">New message</label><input id="{{{{{x}.qaAskId}}}}" type="text" value="{{{{{x}.qaDraft}}}}" onChange="{{{{{x}.qaOnDraft}}}}" placeholder="{{{{{x}.qaPlaceholder}}}}"></div><button type="button" class="btn t" onClick="{{{{{x}.qaAsk}}}}">Post</button></div>')

def qa_bar(x):
    """Summary bar: the header and only control of the Discussion panel. Same in every feature."""
    chev = _CHEV.replace('width="18" height="18"', 'width="20" height="20"')
    return (f'<button type="button" class="qa-bar" id="{{{{{x}.qaTogId}}}}" aria-expanded="{{{{{x}.qaOpen}}}}" aria-controls="{{{{{x}.qaRegionId}}}}" aria-label="{{{{{x}.qaBarAria}}}}" onClick="{{{{{x}.qaToggle}}}}">'
            f'{chev}<span class="qa-bar-t">Discussion</span>'
            f'<sc-if value="{{{{{x}.qaHasPeople}}}}" hint-placeholder-val="{{{{true}}}}"><span class="qa-ppl" aria-hidden="true"><sc-for list="{{{{{x}.qaPeople}}}}" as="p" hint-placeholder-count="3"><span class="av" style="background: {{{{p.bg}}}}">{{{{p.ini}}}}</span></sc-for></span></sc-if>'
            f'<span class="meta">{{{{{x}.qaCountsLabel}}}}</span>'
            f'<sc-if value="{{{{{x}.qaTeamIn}}}}" hint-placeholder-val="{{{{true}}}}"><span class="tile ne"><i></i>Platform team replied</span></sc-if>'
            f'<span class="meta">{{{{{x}.qaLastLabel}}}}</span><span class="qa-bar-act">{{{{{x}.qaAction}}}}</span></button>')

def qa_more(x):
    """Show more: the next three threads, with where you are; focus moves to the first new thread."""
    return (f'<sc-if value="{{{{{x}.qaHasNext}}}}" hint-placeholder-val="{{{{true}}}}"><div class="qa-morebar">'
            f'<button type="button" class="qa-more" aria-controls="{{{{{x}.qaListId}}}}" onClick="{{{{{x}.qaShowMore}}}}">{{{{{x}.qaMoreBtn}}}}</button>'
            f'<span class="meta">{{{{{x}.qaShownLabel}}}}</span></div></sc-if>'
            f'<span class="qa-live" role="status" aria-live="polite">{{{{{x}.qaLive}}}}</span>')

def qa_block(x):
    """Discussion as one expansion panel: the summary bar is the header; open, the body holds the threads (pages of three), Show more and the new-message field."""
    return (f'<div class="qa-panel {{{{{x}.qaPanelCls}}}}">' + qa_bar(x) + f'<sc-if value="{{{{{x}.qaOpen}}}}" hint-placeholder-val="{{{{false}}}}"><div class="qa" id="{{{{{x}.qaRegionId}}}}" role="region" aria-label="Discussion">'
            + qa_empty(x) + f'<div class="qa-list" id="{{{{{x}.qaListId}}}}">' + qa_items(x, 'qaPage') + '</div>' + qa_more(x) + qa_ask(x) + '</div></sc-if></div>')

QA_JS = r"""
  qaSeed() {
    // threads, latest activity first; r = replies; d = days since the message (for "Last reply"); role chips for the team, champions and authors
    var T = 'Platform team', C = 'Champion', A = 'Author';
    var SB = { ini: 'SB', bg: '#FFDEA0', who: 'Sami Ben Ali', role: T }, MK = { ini: 'MK', bg: '#9CF1F0', who: 'Marta Kowalski', role: C }, MKA = { ini: 'MK', bg: '#9CF1F0', who: 'Marta Kowalski', role: A };
    var P = function (o, extra) { return Object.assign({}, o, extra); };
    return {
      r1: [
        { id: 'r1t1', ini: 'PS', bg: '#9CF1F0', who: 'Priya Sharma', when: '3 h ago', d: 0.12, text: 'Can a repository opt out of PR summaries? Some of ours only hold generated code.', r: [
          P(MK, { id: 'r1t1m1', when: '2 h ago', d: 0.08, text: 'Not today as far as I know. You can collapse the summary on each pull request in the meantime.' }),
          { id: 'r1t1m2', ini: 'PS', bg: '#9CF1F0', who: 'Priya Sharma', when: '1 h ago', d: 0.04, text: 'Collapsing works for us until then, thanks.' } ] },
        { id: 'r1t2', ini: 'EL', bg: '#FFDEA0', who: 'Emma Laurent', when: '5 h ago', d: 0.2, text: 'Do PR summaries run on draft pull requests?', r: [] },
        { id: 'r1t3', ini: 'NR', bg: '#E3DFFF', who: 'Nadia Rahal', when: 'yesterday', d: 1, text: 'Is the approval card shown in the VS Code extension too?', r: [
          P(SB, { id: 'r1t3m1', when: 'today', d: 0.5, text: 'Not yet: the extension opens the approval in the browser. Native cards come with 4.7.' }),
          { id: 'r1t3m2', ini: 'NR', bg: '#E3DFFF', who: 'Nadia Rahal', when: 'today', d: 0.45, text: 'Good to know. Is there a date for 4.7?' },
          P(SB, { id: 'r1t3m3', when: 'today', d: 0.4, text: 'Mid-December; it will be announced here in What’s new.' }) ] },
        { id: 'r1t4', ini: 'YD', bg: '#C3F4DC', who: 'Yann Dupont', when: 'yesterday', d: 1, text: 'Do the ratings on PR summaries change anything, or are they just stats?', r: [
          P(MK, { id: 'r1t4m1', when: 'yesterday', d: 1, text: 'They feed the summary prompt directly, so ask your reviewers to rate them: that is how summaries get better for your repositories.' }) ] },
        { id: 'r1t5', ini: 'KO', bg: '#9CF1F0', who: 'Karim Ouali', when: 'yesterday', d: 1, text: 'Is there a size limit on the diff for a summary?', r: [
          P(MK, { id: 'r1t5m1', when: 'yesterday', d: 1, text: 'Above 5 000 changed lines the summary covers the files with the most changes and says so at the top.' }) ] },
        { id: 'r1t6', ini: 'LB', bg: '#FFDEA0', who: 'Lucas Bernard', when: '2 days ago', d: 2, text: 'Does the approval card also show up when a skill calls the tool, not only in chat?', r: [
          P(SB, { id: 'r1t6m1', when: '2 days ago', d: 2, text: 'Yes. Any tool that deploys, deletes or edits asks first, whoever calls it: chat, a skill or an MCP server.' }),
          { id: 'r1t6m2', ini: 'LB', bg: '#FFDEA0', who: 'Lucas Bernard', when: '2 days ago', d: 2, text: 'Perfect, that covers our deploy skill.' },
          { id: 'r1t6m3', ini: 'TD', bg: '#C3F4DC', who: 'Thomas Durand', when: 'yesterday', d: 1, text: 'Same for us with our MCP server: confirmed in staging.' } ] },
        { id: 'r1t7', ini: 'TD', bg: '#C3F4DC', who: 'Thomas Durand', when: '2 days ago', d: 2, text: 'Can I see afterwards who approved a tool call?', r: [
          P(SB, { id: 'r1t7m1', when: '2 days ago', d: 2, text: 'Yes, in the activity log of the run: who approved, when, and the arguments that were sent.' }) ] }
      ],
      r2: [
        { id: 'r2t1', ini: 'YD', bg: '#C3F4DC', who: 'Yann Dupont', when: '3 days ago', d: 3, text: 'Will the old model stay available for a fallback period?', r: [
          P(SB, { id: 'r2t1m1', when: '3 days ago', d: 3, text: 'Two weeks, per workspace, from Settings › Assistant. After 17 Nov the switch is final.' }),
          { id: 'r2t1m2', ini: 'YD', bg: '#C3F4DC', who: 'Yann Dupont', when: '2 days ago', d: 2, text: 'Thanks. We will test on our staging workspace first.' } ] },
        { id: 'r2t2', ini: 'LB', bg: '#FFDEA0', who: 'Lucas Bernard', when: '3 days ago', d: 3, text: 'Do MCP servers pinned to the old tool schema need a redeploy before 10 November?', r: [] }
      ],
      r3: [], r4: [],
      i1: [
        { id: 'i1t1', ini: 'EL', bg: '#FFDEA0', who: 'Emma Laurent', when: '15 Oct', d: 13, text: 'Will the partial re-run work from the CLI as well?', r: [
          P(MKA, { id: 'i1t1m1', when: '16 Oct', d: 12, text: 'That is the next step if the PR page works out; I opened a separate idea for it.' }) ] },
        { id: 'i1t2', ini: 'YD', bg: '#C3F4DC', who: 'Yann Dupont', when: '12 Oct', d: 16, text: 'Could the PR page list the checks that will run again before I confirm?', r: [
          P(MKA, { id: 'i1t2m1', when: '13 Oct', d: 15, text: 'Good point, I added it to the description.' }),
          P(SB, { id: 'i1t2m2', when: '14 Oct', d: 14, text: 'We will show the list in the confirmation dialog.' }) ] },
        { id: 'i1t3', ini: 'NR', bg: '#E3DFFF', who: 'Nadia Rahal', when: '6 Oct', d: 22, text: 'Would the re-run reuse the build cache of the failed run?', r: [
          P(SB, { id: 'i1t3m1', when: '9 Oct', d: 19, text: 'Yes, when the commit is the same, the artifacts of the failed run are reused.' }) ] },
        { id: 'i1t4', ini: 'LB', bg: '#FFDEA0', who: 'Lucas Bernard', when: '4 Oct', d: 24, text: 'Would scheduled sweeps get the partial re-run too, or only runs started from a pull request?', r: [
          P(MKA, { id: 'i1t4m1', when: '5 Oct', d: 23, text: 'From the PR page first: that is where the 10 minutes are lost. Scheduled sweeps could follow.' }),
          { id: 'i1t4m2', ini: 'LB', bg: '#FFDEA0', who: 'Lucas Bernard', when: '5 Oct', d: 23, text: 'Makes sense, scheduled sweeps can wait.' } ] },
        { id: 'i1t5', ini: 'PS', bg: '#9CF1F0', who: 'Priya Sharma', when: '25 Sep', d: 33, text: 'Same here on monorepos: a full re-run is 25 minutes for us.', r: [
          { id: 'i1t5m1', ini: 'YD', bg: '#C3F4DC', who: 'Yann Dupont', when: '26 Sep', d: 32, text: 'Same, and a docs-only change should skip the Test phase too.' },
          P(SB, { id: 'i1t5m2', when: '2 Oct', d: 26, text: 'Docs-only detection is a separate idea, worth opening.' }) ] }
      ],
      i2: [ { id: 'i2t1', ini: 'MK', bg: '#9CF1F0', who: 'Marta Kowalski', when: '6 Oct', d: 22, text: 'Would the exported conversation include the tool calls, or only the messages?', r: [] } ],
      i3: [], i4: [], i5: [], i6: []
    };
  }
  qaFocusSync() {
    // after Show more / Show earlier replies, focus goes to the first message that appeared
    if (typeof document === 'undefined') return;
    var el = null;
    if (this._qaFocus) { el = document.getElementById(this._qaFocus); this._qaFocus = null; }
    else if (this._qaFocusQ) { el = document.getElementById(this._qaFocusQ); this._qaFocusQ = null; }
    if (el) try { el.focus(); } catch (e) {}
  }
  qaVals(key, base, placeholder, me, defOpen) {
    // me: { who, role } when the viewer posts with a role chip (platform team, author), else null
    var s = this.state, self = this, om = s.qaOpen || {}, open = om[key] === undefined ? !!defOpen : !!om[key];
    var ex = (s.qaExtra || {})[key] || [], rx = s.qaReplies || {}, ing = s.qaReplying || {}, rd = s.qaReplyDrafts || {}, er = s.qaEarlier || {}, dr = s.qaDrafts || {};
    var up = function (path, k, v) { var o = {}; o[path] = Object.assign({}, self.state[path] || {}); o[path][k] = v; return o; };
    var click = function (f) { return function (e) { if (e && e.preventDefault) e.preventDefault(); self.setState(f()); }; };
    var typed = function (path, k) { return function (e) { self.setState(up(path, k, e && e.target ? e.target.value : '')); }; };
    var roleTile = function (r) { return r === 'Champion' ? 'in' : 'ne'; };
    var deco = function (m) { return Object.assign({}, m, { hasRole: !!m.role, role: m.role || '', roleTile: roleTile(m.role) }); };
    var mine = function (id, t) { return { id: id, ini: 'AH', bg: '#D4D0F9', who: 'Aurélien Heux', role: me ? me.role : '', when: 'just now', d: 0, text: t }; };
    // your new threads first, then the seed (latest activity first)
    var list = ex.slice().reverse().concat(base || []).map(function (q) {
      var replies = (q.r || []).concat(rx[q.id] || []).map(deco), all = !!er[q.id], KEEP = 2;
      var shown = all || replies.length <= KEEP ? replies : replies.slice(replies.length - KEEP), hidden = replies.length - shown.length;
      return Object.assign(deco(q), {
        replies: replies, shownReplies: shown, hasReplies: replies.length > 0, hasHidden: hidden > 0,
        earlierLabel: 'Show ' + hidden + (hidden > 1 ? ' earlier replies' : ' earlier reply'),
        showEarlier: function (e) { if (e && e.preventDefault) e.preventDefault(); if (replies[0]) self._qaFocusQ = 'qa-m-' + replies[0].id; self.setState(up('qaEarlier', q.id, true)); },
        repliesLabel: replies.length ? replies.length + (replies.length > 1 ? ' replies' : ' reply') : 'No reply yet',
        lastD: replies.length ? Math.min.apply(null, replies.map(function (m) { return m.d; })) : q.d,
        teamIn: replies.some(function (m) { return m.role === 'Platform team'; }),
        replying: !!ing[q.id], replyId: 'qa-rf-in-' + q.id, replyDraft: rd[q.id] || '', onReplyDraft: typed('qaReplyDrafts', q.id),
        startReply: click(function () { return up('qaReplying', q.id, !(self.state.qaReplying || {})[q.id]); }),
        sendReply: click(function () { var t = ((self.state.qaReplyDrafts || {})[q.id] || '').trim(); if (!t) return {}; var cur = (self.state.qaReplies || {})[q.id] || [];
          return Object.assign(up('qaReplies', q.id, cur.concat([mine(q.id + '-r' + (cur.length + 1), t)])), up('qaReplyDrafts', q.id, ''), up('qaReplying', q.id, false), up('qaEarlier', q.id, true)); })
      });
    });
    var nMsg = list.reduce(function (n, q) { return n + 1 + q.replies.length; }, 0);
    var people = []; list.forEach(function (q) { [q].concat(q.replies).forEach(function (m) { if (people.length < 3 && !people.some(function (p) { return p.ini === m.ini; })) people.push({ ini: m.ini, bg: m.bg }); }); });
    var lastD = list.length ? Math.min.apply(null, list.map(function (q) { return q.lastD; })) : null;
    var lastWhen = (function () { var best = null; list.forEach(function (q) { [q].concat(q.replies).forEach(function (m) { if (!best || m.d < best.d) best = m; }); }); return best ? best.when : ''; })();
    var teamIn = list.some(function (q) { return q.teamIn; });
    var setOpen = function (v) { return function (e) { if (e && e.preventDefault) e.preventDefault();
      var o = Object.assign({}, self.state.qaOpen || {}); o[key] = v; var sh = Object.assign({}, self.state.qaShown || {}); delete sh[key]; var lv = Object.assign({}, self.state.qaLive || {}); delete lv[key];
      self.setState({ qaOpen: o, qaShown: sh, qaLive: lv }); }; };
    // pages of three threads: Show more reveals the next three and moves focus to the first of them
    var PAGE = 3, shownN = Math.max(PAGE, (s.qaShown || {})[key] || PAGE), nextN = Math.min(PAGE, Math.max(0, list.length - shownN));
    var showMore = function (e) { if (e && e.preventDefault) e.preventDefault(); var first = list[shownN]; if (first) self._qaFocusQ = 'qa-q-' + first.id;
      var n = Math.min(list.length, shownN + PAGE), sh = Object.assign({}, self.state.qaShown || {}); sh[key] = n; var lv = Object.assign({}, self.state.qaLive || {}); lv[key] = (n - shownN) + (n - shownN > 1 ? ' more threads shown, ' : ' more thread shown, ') + n + ' of ' + list.length;
      self.setState({ qaShown: sh, qaLive: lv }); };
    var counts = list.length + (list.length === 1 ? ' thread' : ' threads') + ' · ' + nMsg + (nMsg === 1 ? ' message' : ' messages');
    return { qaOpen: open, qaClosed: !open, qaPanelCls: open ? 'open' : '', qaAction: open ? 'Hide' : 'Show', qaListId: 'qa-l-' + key,
      qaToggle: setOpen(!open), qaTogId: 'qa-t-' + key, qaRegionId: 'qa-r-' + key,
      qaPage: list.slice(0, shownN), qaHasNext: nextN > 0, qaNextN: nextN, qaMoreBtn: 'Show ' + nextN + ' more thread' + (nextN > 1 ? 's' : ''), qaShowMore: showMore,
      qaShownLabel: Math.min(shownN, list.length) + ' of ' + list.length + ' threads shown', qaLive: (s.qaLive || {})[key] || '',
      qaCountsLabel: list.length ? counts : '', qaTeamIn: teamIn, qaHasPeople: people.length > 0, qaPeople: people,
      qaLastLabel: lastWhen ? 'Last message ' + lastWhen : 'No messages yet',
      qaBarAria: 'Discussion · ' + (list.length ? counts.replace(' · ', ', ') : 'no messages yet') + (teamIn ? ', platform team replied' : '') + (lastWhen ? ', last message ' + lastWhen : ''),
      qaSummary: list.length ? counts : 'No messages yet', qaMsgCount: nMsg,
      qa: list, qaN: list.length, qaEmpty: !list.length,
      qaAskId: 'qa-ask-' + key, qaDraft: dr[key] || '', qaPlaceholder: placeholder, qaOnDraft: typed('qaDrafts', key),
      qaAsk: click(function () { var t = ((self.state.qaDrafts || {})[key] || '').trim(); if (!t) return {}; var cur = (self.state.qaExtra || {})[key] || []; var m = mine(key + '-t' + (cur.length + 1), t); m.r = [];
        return Object.assign(up('qaExtra', key, cur.concat([m])), up('qaDrafts', key, '')); }) };
  }
"""

# ---------------------------------------------------------------------------
# Administration shell (B · admin sidebar, adopted in the Administration layout lab):
# a 240 px sidebar with Core and one group per feature module, a grouped Section
# select below 1200 px, and the shared pages (General, Users and permissions, Sweep · Connectors,
# placeholders). Same markup in the lab and in the live prototype.
# ---------------------------------------------------------------------------
_AST = 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
_ABACK = f'<svg width="18" height="18" viewBox="0 0 24 24" {_AST}><path d="M15 6l-6 6 6 6"/></svg>'
_APLUS = f'<svg width="18" height="18" viewBox="0 0 24 24" {_AST}><path d="M12 5v14M5 12h14"/></svg>'
_ASEARCH = f'<svg width="18" height="18" viewBox="0 0 24 24" {_AST}><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>'

ADMIN_CSS = """.r-wrap{flex-wrap:wrap}
.ad-tscroll{overflow-x:auto}.ad-tbl{min-width:600px}
.ad-two{display:grid;grid-template-columns:minmax(0,1fr);gap:16px;align-items:start}
.ad-two:has(.ad-detail){grid-template-columns:minmax(0,1fr) 340px}
.ad-detail{display:flex;flex-direction:column;gap:14px;padding:20px}
.ad-fs{display:flex;flex-direction:column;gap:8px;padding-top:12px;border-top:1px solid #CAC4CF}
.ad-fl{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:700;letter-spacing:.3px;color:#48454E;text-transform:uppercase}
.ad-opt{display:flex;gap:10px;align-items:flex-start;font-size:14px;line-height:18px;cursor:pointer}.ad-opt input{margin:2px 0 0;width:18px;height:18px;accent-color:#35307E;flex:none}
.ad-opt .meta{white-space:normal}
.ad-search input{border:0;outline:0;background:transparent;font:400 14px 'Open Sans',system-ui,sans-serif;color:#1C1B1E;min-width:0;flex:1}
tr.rw[role="button"]{cursor:pointer}tr.rw.on td{background:#F2EBFA}tr.rw:focus-visible{outline:2px solid #35307E;outline-offset:-2px}
.ad-split{display:grid;grid-template-columns:240px minmax(0,1fr);gap:24px;align-items:start}
.ad-side{position:sticky;top:0;display:flex;flex-direction:column;gap:4px;padding:4px 0}
.ad-g{display:flex;flex-direction:column;gap:2px;padding-bottom:10px}
.ad-gh{display:flex;align-items:center;gap:8px;padding:10px 12px 6px;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:700;letter-spacing:.4px;text-transform:uppercase;color:#48454E}
.ad-ni{display:flex;align-items:center;gap:8px;height:40px;padding:0 12px 0 16px;border-radius:16px;color:#1C1B1E;text-decoration:none;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:14px;font-weight:500}
.ad-ni:hover{background:rgba(53,48,126,.06)}
.ad-ni.on{background:#E3DFFF;color:#191836;font-weight:700;box-shadow:inset 3px 0 0 #35307E}
.ad-select,.ad-select.row{display:none}
@container win (max-width: 1199px){
.ad-split{grid-template-columns:minmax(0,1fr)!important}.ad-side{display:none!important}.ad-select{display:flex!important}
.ad-two:has(.ad-detail){grid-template-columns:minmax(0,1fr)!important}
}
@container win (max-width: 839px){.ad-search{width:100%!important}}
@container win (max-width: 599px){.ad-detail{padding:16px}.ad-banner{flex-direction:column;align-items:flex-start!important}.fbp .card{padding:16px!important}.fbp .step{flex-wrap:wrap}.fbp .step .fld{flex:1 1 100%!important;order:3}.fbp .step .sel{flex:1;min-width:0}.fbp-tabs .tile{white-space:normal;flex-basis:100%;margin:8px 0}}
.fbp-tabs .tile{max-width:100%}
/* FeedbackProfile: self-contained, so any feature module can embed it */
.fbp .step{display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:12px;border:1px solid #CAC4CF;background:#FDF8FD}.fbp .num{width:24px;height:24px;flex:none;border-radius:999px;background:#E3DFFF;color:#14085E;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:700;display:inline-flex;align-items:center;justify-content:center}.fbp .sel-s{height:32px;font-size:13px}.fbp .pop{box-sizing:border-box;border-radius:12px;background:#F2EBFA;box-shadow:0 1px 2px rgba(0,0,0,.3),0 2px 6px 2px rgba(0,0,0,.15)}"""

ADMIN_USERS = '''<div class="stack">
  <div class="row r-wrap" style="gap: 8px 12px"><span class="tile ok" style="flex: none"><i></i>Directory sync · 10 min ago</span><span style="flex: 1"></span></div>
  <div class="row r-wrap" style="gap: 8px">
    <sc-for list="{{uFilters}}" as="f" hint-placeholder-count="3"><button type="button" class="chip" aria-pressed="{{f.on}}" style="{{f.style}}" onClick="{{f.pick}}">{{f.label}}<span class="n">{{f.n}}</span></button></sc-for>
    <span style="flex: 1"></span>
    <div class="fld ad-search" style="min-height: 40px; padding: 8px 12px; width: 240px"><label for="ad-q">Search</label><div class="row" style="gap: 8px">''' + _ASEARCH + '''<input id="ad-q" type="text" placeholder="Name, email, team…"></div></div>
  </div>
  <div class="ad-two">
    <div class="card" style="padding: 0; overflow: hidden; min-width: 0">
      <div class="ad-tscroll"><table class="ad-tbl" style="width: 100%; border-collapse: collapse">
        <thead><tr><th class="th">User</th><th class="th">Admin rights</th><th class="th">Team</th><th class="th">Last active</th></tr></thead>
        <tbody>
          <sc-for list="{{users}}" as="u" hint-placeholder-count="6">
            <tr class="rw {{u.cls}}" tabindex="0" role="button" aria-pressed="{{u.on}}" onClick="{{u.pick}}">
              <td class="td"><div class="row" style="gap: 10px"><span class="av" style="background: {{u.bg}}">{{u.ini}}</span><div style="min-width: 0"><div class="ui" style="font-weight: 600; white-space: nowrap">{{u.name}}</div><div class="mono" style="font-size: 11px; color: #48454E">{{u.mail}}</div></div></div></td>
              <td class="td"><div class="row" style="gap: 6px; flex-wrap: wrap"><sc-for list="{{u.rights}}" as="r" hint-placeholder-count="2"><span class="tag" style="background: {{r.bg}}">{{r.label}}</span></sc-for><sc-if value="{{u.pending}}" hint-placeholder-val="{{false}}"><span class="tile wn"><i></i>{{u.pendingLabel}}</span></sc-if><sc-if value="{{u.noRights}}" hint-placeholder-val="{{false}}"><span class="meta">None</span></sc-if></div></td>
              <td class="td"><span style="font-size: 13px">{{u.groups}}</span></td>
              <td class="td"><span class="meta">{{u.last}}</span></td>
            </tr>
          </sc-for>
        </tbody>
      </table></div>
      <div class="row" style="padding: 10px 16px; border-top: 1px solid #CAC4CF; font-size: 12px; color: #48454E"><span>{{uCount}}</span><span style="flex: 1"></span><button type="button" class="chip" style="height: 28px">Next</button></div>
    </div>
    <sc-if value="{{hasUsr}}" hint-placeholder-val="{{true}}">
    <aside class="card ad-detail" aria-label="Admin rights of {{usr.name}}">
      <div class="row" style="justify-content: space-between"><div class="row" style="gap: 10px"><span class="av" style="background: {{usr.bg}}">{{usr.ini}}</span><div><div class="ui" style="font-weight: 700">{{usr.name}}</div><div class="mono" style="font-size: 11px; color: #48454E">{{usr.mail}}</div></div></div><button type="button" class="ib" aria-label="Close" style="margin: -8px -8px -8px 0" onClick="{{closeUsr}}"><svg width="20" height="20" viewBox="0 0 24 24" ''' + _AST + '''><path d="M6 6l12 12M18 6L6 18"/></svg></button></div>
      <div class="meta" style="white-space: normal">Team <b style="color: #1C1B1E">{{usr.groups}}</b>, from the directory</div>
      <sc-if value="{{usr.pending}}" hint-placeholder-val="{{false}}"><div class="ocard row r-wrap ad-banner" style="gap: 8px; border-color: #E8A400; background: #FFF4DE"><span style="flex: 1; min-width: 0; font-size: 13px; line-height: 18px">Asks for <b>{{usr.pendingRight}}</b></span><button type="button" class="chip" style="height: 28px">Decline</button><button type="button" class="btn f sm">Approve</button></div></sc-if>
      <div class="ad-fs"><div class="ad-fl">Admin rights</div>
        <label class="ad-opt"><input type="checkbox" checked="{{usr.admin}}"> <span><b>Platform admin</b><br><span class="meta">Everything, including users, groups and the audit log</span></span></label>
        <label class="ad-opt"><input type="checkbox" checked="{{usr.sweep}}"> <span><b>Sweep admin</b><br><span class="meta">Connectors</span></span></label>
        <label class="ad-opt"><input type="checkbox" checked="{{usr.community}}"> <span><b>Community admin</b><br><span class="meta">Releases, tours, feedback, ideas, insights</span></span></label>
        <label class="ad-opt"><input type="checkbox" checked="{{usr.fbSweep}}"> <span><b>Feedback · Sweep</b><br><span class="meta">Sweep feedback profile and inbox, in Community › Feedback</span></span></label></div>
      <div class="row" style="justify-content: flex-end; gap: 8px; padding-top: 4px"><button type="button" class="btn x" onClick="{{closeUsr}}">Cancel</button><button type="button" class="btn f">Save</button></div>
    </aside>
    </sc-if>
  </div>
</div>'''

ADMIN_RUNNERS = '''<div class="stack">
  <div class="row r-kpis" style="gap: 16px"><div class="kpi"><b>12</b><span>runners</span></div><div class="kpi"><b>11</b><span>online</span></div><div class="kpi"><b>3</b><span>jobs queued</span></div><div class="kpi"><b>40 s</b><span>average wait</span></div></div>
  <div class="row r-wrap" style="gap: 8px"><span class="chip chip-on">All pools</span><span class="chip">client</span><span class="chip">facility</span><span class="chip">shared</span><span style="flex: 1"></span><button type="button" class="btn f btn-i">''' + _APLUS + '''Add runner</button></div>
  <div class="card" style="padding: 0; overflow: hidden"><div class="ad-tscroll"><table class="ad-tbl" style="width: 100%; border-collapse: collapse">
    <thead><tr><th class="th">Runner</th><th class="th">Pool</th><th class="th">Status</th><th class="th">Version</th><th class="th">Jobs today</th><th class="th">Last job</th></tr></thead>
    <tbody>
      <tr class="rw"><td class="td"><b class="ui">runner-cli-01</b></td><td class="td">client</td><td class="td"><span class="tile ok"><i></i>Online</span></td><td class="td"><span class="mono">4.6.0</span></td><td class="td">38</td><td class="td"><span class="meta">2 min ago</span></td></tr>
      <tr class="rw"><td class="td"><b class="ui">runner-cli-02</b></td><td class="td">client</td><td class="td"><span class="tile ok"><i></i>Online</span></td><td class="td"><span class="mono">4.6.0</span></td><td class="td">31</td><td class="td"><span class="meta">6 min ago</span></td></tr>
      <tr class="rw"><td class="td"><b class="ui">runner-fac-01</b></td><td class="td">facility</td><td class="td"><span class="tile wn"><i></i>Draining</span></td><td class="td"><span class="mono">4.5.2</span></td><td class="td">12</td><td class="td"><span class="meta">1 h ago</span></td></tr>
      <tr class="rw"><td class="td"><b class="ui">runner-shared-07</b></td><td class="td">shared</td><td class="td"><span class="tile er"><i></i>Offline</span></td><td class="td"><span class="mono">4.6.0</span></td><td class="td">0</td><td class="td"><span class="meta">yesterday</span></td></tr>
    </tbody></table></div></div>
</div>'''

# Core > General: the landing section for platform admins
ADMIN_GENERAL = '''<div class="stack">
  <div class="card stack" style="gap: 16px; padding: 24px; max-width: 760px">
    <div class="h2">Workspace</div>
    <div class="fld"><label for="g-name">Workspace name</label><input id="g-name" type="text" value="AIToolbox"></div>
    <div class="row r-wrap" style="gap: 16px"><div class="fld" style="flex: 1 1 220px"><label for="g-lang">Default language</label><input id="g-lang" type="text" value="English"></div><div class="fld" style="flex: 1 1 220px"><label for="g-tz">Time zone</label><input id="g-tz" type="text" value="Europe/Paris (CET)"></div></div>
    <div class="fld"><label for="g-sup">Support contact</label><input id="g-sup" type="text" value="Platform team · Teams channel “AIToolbox support”"></div>
  </div>
  <div class="card stack" style="gap: 12px; padding: 24px; max-width: 760px">
    <div class="h2">Retention</div>
    <div class="row r-wrap" style="gap: 8px"><span class="meta" style="width: 140px">Audit log</span><span class="chip chip-on">90 days</span><span class="chip">1 year</span><span class="chip">3 years</span></div>
    <div class="row r-wrap" style="gap: 8px"><span class="meta" style="width: 140px">Feedback and surveys</span><span class="chip">6 months</span><span class="chip chip-on">12 months</span><span class="chip">24 months</span></div>
    <div class="row r-wrap" style="gap: 8px"><span class="meta" style="width: 140px">Assistant history</span><span class="chip chip-on">30 days</span><span class="chip">90 days</span></div>
    <div class="row" style="justify-content: flex-end; gap: 8px; border-top: 1px solid #CAC4CF; padding-top: 16px"><button type="button" class="btn x">Cancel</button><button type="button" class="btn f">Save</button></div>
  </div>
</div>'''

# Sweep > Connectors: the only Sweep section kept for now (the outside services Sweep reads from and writes to)
ADMIN_CONNECTORS = '''<div class="stack">
  <div class="row r-wrap" style="gap: 8px"><span style="flex: 1"></span><button type="button" class="btn f btn-i">''' + _APLUS + '''Add connector</button></div>
  <div class="card" style="padding: 0; overflow: hidden"><div class="ad-tscroll"><table class="ad-tbl" style="width: 100%; border-collapse: collapse">
    <thead><tr><th class="th">Connector</th><th class="th">Used for</th><th class="th">Scope</th><th class="th">Status</th><th class="th">Last sync</th><th class="th"></th></tr></thead>
    <tbody>
      <tr class="rw"><td class="td"><b class="ui">DevOps platform</b><div class="meta">devops.example.internal · also used by the DevOps MCP server</div></td><td class="td"><span style="font-size: 13px">Repositories, pipelines, pull requests</span></td><td class="td">64 repositories</td><td class="td"><span class="tile ok"><i></i>Connected</span></td><td class="td"><span class="meta">2 min ago</span></td><td class="td" style="text-align: right"><button type="button" class="chip" style="height: 28px">Configure</button></td></tr>
      <tr class="rw"><td class="td"><b class="ui">Jira</b><div class="meta">Projects SWP, PAY, CB · used by Create Jira ticket</div></td><td class="td"><span style="font-size: 13px">Blocking findings become tickets</span></td><td class="td">3 projects</td><td class="td"><span class="tile ok"><i></i>Connected</span></td><td class="td"><span class="meta">10 min ago</span></td><td class="td" style="text-align: right"><button type="button" class="chip" style="height: 28px">Configure</button></td></tr>
      <tr class="rw"><td class="td"><b class="ui">Microsoft Teams</b><div class="meta">Run notifications</div></td><td class="td"><span style="font-size: 13px">Run results and failures</span></td><td class="td">12 channels</td><td class="td"><span class="tile ok"><i></i>Connected</span></td><td class="td"><span class="meta">1 h ago</span></td><td class="td" style="text-align: right"><button type="button" class="chip" style="height: 28px">Configure</button></td></tr>
      <tr class="rw"><td class="td"><b class="ui">SonarQube</b><div class="meta">Quality gate</div></td><td class="td"><span style="font-size: 13px">Quality gate in the Test phase</span></td><td class="td">1 instance</td><td class="td"><span class="tile wn"><i></i>Token expires in 6 days</span></td><td class="td"><span class="meta">3 h ago</span></td><td class="td" style="text-align: right"><button type="button" class="chip" style="height: 28px">Renew token</button></td></tr>
      <tr class="rw"><td class="td"><b class="ui">Artifactory</b><div class="meta">Build artifacts</div></td><td class="td"><span style="font-size: 13px">Publish and scan artifacts</span></td><td class="td">—</td><td class="td"><span class="tile ne"><i></i>Not connected</span></td><td class="td"><span class="meta">—</span></td><td class="td" style="text-align: right"><button type="button" class="chip" style="height: 28px">Connect</button></td></tr>
    </tbody></table></div></div>
</div>'''

ADMIN_PLACEHOLDER = '''<div class="ocard" style="display: flex; gap: 16px; align-items: center; padding: 24px"><span class="tile ne" style="flex: none"><i></i>{{pageTitle}}</span><span style="font-size: 14px; color: #48454E">This section is not in the lab. It uses the same shell, with its own content.</span></div>'''

ADMIN_MODLINE = '''<sc-if value="{{isFeaturePage}}" hint-placeholder-val="{{true}}"><div class="row r-wrap" style="gap: 8px; font-size: 12px; color: #48454E"><span class="tag" style="background: #ECE5F4">Remote module</span><span class="mono">{{modRemote}}</span><span>· owned by {{modOwner}}</span><span style="flex: 1"></span><span>{{modScope}}</span></div></sc-if>'''

ADMIN_FEEDBACK = '''<div class="r-split fbp" style="display: grid; grid-template-columns: minmax(0, 1fr) 380px; gap: 24px; align-items: start">
  <div class="card" style="display: flex; flex-direction: column; gap: 14px; padding: 24px">
    <div class="row r-wrap" style="justify-content: space-between; gap: 8px"><div style="min-width: 0"><h2 class="h2">{{fp.name}} · feedback profile</h2><div style="font-size: 12px; color: #48454E; margin-top: 2px">FeedbackProfile component · one editor for every feature’s profile</div></div><button type="button" class="chip" aria-pressed="{{fp.on}}" style="{{fp.onStyle}}" onClick="{{fp.toggle}}"><sc-if value="{{fp.on}}" hint-placeholder-val="{{true}}"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5L20 7"/></svg></sc-if>{{fp.onLabel}}</button></div>
    <div class="row" style="flex-wrap: wrap"><span style="font-size: 13px; color: #48454E; width: 96px">Entry points</span><sc-for list="{{fp.entryChips}}" as="t" hint-placeholder-count="4"><button type="button" class="chip" aria-pressed="{{t.on}}" style="{{t.style}}" onClick="{{t.pick}}"><sc-if value="{{t.on}}" hint-placeholder-val="{{false}}"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5L20 7"/></svg></sc-if>{{t.label}}</button></sc-for></div>
    <div class="ui" style="font-size: 12px; font-weight: 700; color: #48454E">Questions · {{fp.nq}} of 3</div>
    <sc-for list="{{fp.qs}}" as="q" hint-placeholder-count="2">
      <div class="step" style="align-items: center"><span class="num">{{q.n}}</span><select class="sel sel-s" aria-label="Question type" value="{{q.type}}" onChange="{{q.onType}}"><option value="thumbs">Thumbs</option><option value="scale">Scale 1–5</option><option value="nps">NPS 0–10</option><option value="single">Single choice</option><option value="multi">Multiple choice</option><option value="text">Text</option></select><div class="fld" style="flex: 1; min-width: 0; min-height: 40px; padding: 8px 12px"><input type="text" aria-label="Question {{q.n}}" value="{{q.text}}" onChange="{{q.onText}}"></div><button type="button" class="ib" aria-label="Remove question {{q.n}}" style="width: 32px; height: 32px; margin: 0" onClick="{{q.del}}"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/></svg></button></div>
    </sc-for>
    <sc-if value="{{fp.canAdd}}" hint-placeholder-val="{{true}}"><button type="button" class="chip" style="align-self: flex-start" onClick="{{fp.addQ}}"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>Add question</button></sc-if>
    <div class="row" style="flex-wrap: wrap"><span style="font-size: 13px; color: #48454E; width: 96px">Sampling</span><sc-for list="{{fp.samplingChips}}" as="t" hint-placeholder-count="4"><button type="button" class="chip" aria-pressed="{{t.on}}" style="{{t.style}}" onClick="{{t.pick}}">{{t.label}}</button></sc-for><span style="font-size: 12px; color: #48454E">after-action prompts only</span></div>
    <div class="row" style="flex-wrap: wrap"><label for="fp-route" style="font-size: 13px; color: #48454E; width: 96px">Routing</label><select id="fp-route" class="sel sel-s" value="{{fp.routing}}" onChange="{{fp.onRouting}}"><option value="inbox">Team inbox only</option><option value="jira">Inbox + Jira project</option><option value="teams">Inbox + Teams channel</option></select><span style="font-size: 12px; color: #48454E">Bugs always go to Jira; never to Ideas</span></div>
    <div class="row" style="flex-wrap: wrap"><span style="font-size: 13px; color: #48454E; width: 96px">Options</span><sc-for list="{{fp.optChips}}" as="t" hint-placeholder-count="2"><button type="button" class="chip" aria-pressed="{{t.on}}" style="{{t.style}}" onClick="{{t.pick}}"><sc-if value="{{t.on}}" hint-placeholder-val="{{false}}"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5L20 7"/></svg></sc-if>{{t.label}}</button></sc-for></div>
    <div class="row" style="justify-content: flex-end; gap: 8px; border-top: 1px solid #CAC4CF; padding-top: 16px"><sc-if value="{{fp.canClose}}" hint-placeholder-val="{{false}}"><button type="button" class="btn x" onClick="{{fp.close}}">Close</button></sc-if><button type="button" class="btn f" onClick="{{fp.save}}">Save profile</button></div>
  </div>
  <div style="display: flex; flex-direction: column; gap: 12px; min-width: 0">
    <div class="ui" style="font-size: 12px; font-weight: 700; color: #48454E">Preview · side sheet in {{fp.name}}</div>
    <div class="pop" style="position: static; width: auto; max-width: 360px; padding: 16px; display: flex; flex-direction: column; gap: 12px">
      <div class="row" style="justify-content: space-between"><span class="ui" style="font-size: 16px; font-weight: 700">Feedback · {{fp.name}}</span><span style="font-size: 12px; color: #48454E">Goes to {{fp.owner}}</span></div>
      <sc-for list="{{fp.qs}}" as="q" hint-placeholder-count="2"><div><div class="ui" style="font-size: 14px; font-weight: 600; margin-bottom: 6px">{{q.textOr}}</div><span class="tag" style="background: #ECE5F4">{{q.typeLabel}}</span></div></sc-for>
      <sc-if value="{{fp.noQ}}" hint-placeholder-val="{{false}}"><span style="font-size: 13px; color: #48454E">Add at least one question.</span></sc-if>
      <sc-if value="{{fp.ctx}}" hint-placeholder-val="{{true}}"><div class="row" style="gap: 6px; font-size: 12px; color: #48454E"><span class="chip chip-on" style="height: 28px; font-size: 12px">Attach context</span>page, run, environment, app version</div></sc-if>
      <div class="row" style="justify-content: flex-end"><span class="btn f sm">Send</span></div>
    </div>
  </div>
</div>'''

# Feature Feedback section header: Profile / Inbox sub-tabs and the shared cap, read-only (set in Community > Listening)
ADMIN_FEEDBACK_TABS = '''<div class="r-subtabs row r-wrap fbp-tabs" role="tablist" aria-label="Feedback" style="gap: 0; border-bottom: 1px solid #CAC4CF"><sc-for list="{{sfTabs}}" as="t" hint-placeholder-count="2"><button type="button" class="tab" role="tab" aria-selected="{{t.on}}" style="{{t.style}}" onClick="{{t.pick}}">{{t.label}}<sc-if value="{{t.hasN}}" hint-placeholder-val="{{false}}"><span class="n">{{t.n}}</span></sc-if></button></sc-for><span style="flex: 1"></span><span class="tile in" title="Set by the platform team in Community › Listening"><i></i>{{capLabel}} · set in Community</span></div>'''

def admin_tree(cls='ad-side'):
    """Grouped navigation (B sidebar, D drawer): Core · Sweep · Community, filtered by rights."""
    return (f'<nav class="{cls}" aria-label="Administration"><sc-for list="{{{{groups}}}}" as="g" hint-placeholder-count="3"><div class="ad-g"><div class="ad-gh"><sc-if value="{{{{g.isSweep}}}}" hint-placeholder-val="{{{{false}}}}">{N.mark('sweep', N.LIGHT, 22)}</sc-if><sc-if value="{{{{g.isNew}}}}" hint-placeholder-val="{{{{false}}}}">{N.mark('new', N.LIGHT, 22)}</sc-if><span>{{{{g.label}}}}</span></div>'
            '<sc-for list="{{g.items}}" as="s" hint-placeholder-count="4"><a href="#adm-{{s.key}}" class="ad-ni {{s.cls}}" aria-current="{{s.cur}}" onClick="{{s.pick}}"><span style="flex: 1">{{s.label}}</span><sc-if value="{{s.hasN}}" hint-placeholder-val="{{false}}"><span class="n">{{s.n}}</span></sc-if></a></sc-for></div></sc-for></nav>')

ADMIN_SELECT = '''<div class="ad-select row" style="gap: 8px"><label for="ad-sel" class="meta">Section</label><select id="ad-sel" class="sel" value="{{page}}" onChange="{{onSelect}}"><sc-for list="{{groups}}" as="g" hint-placeholder-count="3"><optgroup label="{{g.label}}"><sc-for list="{{g.items}}" as="s" hint-placeholder-count="4"><option value="{{s.key}}">{{s.label}}</option></sc-for></optgroup></sc-for></select></div>'''


ADMIN_JS = r"""
  adminUsers() {
    // Users and permissions: filters, the table, the Edit rights panel. State: uf (filter), usel (selected user id).
    var s = this.state, self = this, ON = 'background: #E3DFFF; border-color: #E3DFFF; color: #191836';
    var set = function (o) { return function (e) { if (e && e.preventDefault) e.preventDefault(); self.setState(o); }; };
    var U = [
      { id: 'u1', ini: 'AH', bg: '#D4D0F9', name: 'Aurélien Heux', mail: 'aurelien.heux@bnpp.example', admin: true, sweep: true, community: true, groups: 'Platform', last: 'today' },
      { id: 'u2', ini: 'MK', bg: '#9CF1F0', name: 'Marta Kowalski', mail: 'marta.kowalski@bnpp.example', admin: false, sweep: true, community: false, groups: 'Client', last: '2 h ago' },
      { id: 'u3', ini: 'SB', bg: '#FFDEA0', name: 'Sami Ben Ali', mail: 'sami.benali@bnpp.example', admin: true, sweep: false, community: true, groups: 'Platform', last: '1 h ago' },
      { id: 'u4', ini: 'PS', bg: '#9CF1F0', name: 'Priya Sharma', mail: 'priya.sharma@bnpp.example', admin: false, sweep: false, community: true, groups: 'Request', last: 'yesterday' },
      { id: 'u5', ini: 'LB', bg: '#FFDEA0', name: 'Lucas Bernard', mail: 'lucas.bernard@bnpp.example', admin: false, sweep: false, community: false, groups: 'Facility', last: '3 days ago', pending: 'Sweep admin' },
      { id: 'u6', ini: 'YD', bg: '#C3F4DC', name: 'Yann Dupont', mail: 'yann.dupont@bnpp.example', admin: false, sweep: false, community: false, fbSweep: true, groups: 'Client', last: 'today' }
    ];
    var uf = s.uf === 'admins' || s.uf === 'req' ? s.uf : 'all';
    var isAdm = function (u) { return u.admin || u.sweep || u.community || u.fbSweep; };
    var uFilters = [ { k: 'all', label: 'All', n: '1,284' }, { k: 'admins', label: 'Admins', n: 46 }, { k: 'req', label: 'Requests', n: 1 } ].map(function (f) { var on = uf === f.k; return { label: f.label, n: f.n, on: on, style: on ? ON : '', pick: set({ uf: f.k }) }; });
    var users = U.filter(function (u) { return uf === 'all' || (uf === 'admins' && isAdm(u)) || (uf === 'req' && u.pending); }).map(function (u) {
      var rights = (u.admin ? [{ label: 'Platform admin', bg: '#E3DFFF' }] : []).concat(u.sweep ? [{ label: 'Sweep admin', bg: '#ECE5F4' }] : [], u.community ? [{ label: 'Community admin', bg: '#ECE5F4' }] : [], u.fbSweep ? [{ label: 'Feedback · Sweep', bg: '#ECE5F4' }] : []), on = s.usel === u.id;
      return Object.assign({}, u, { on: on, cls: on ? 'on' : '', rights: rights, noRights: !rights.length && !u.pending, pending: !!u.pending, pendingLabel: u.pending ? u.pending + ' requested' : '', pick: set({ usel: on ? null : u.id }) });
    });
    var selRaw = U.filter(function (u) { return u.id === s.usel; })[0];
    return { uFilters: uFilters, users: users, uCount: uf === 'all' ? '1–6 of 1,284' : users.length + ' shown', hasUsr: !!selRaw, closeUsr: set({ usel: null }),
      usr: selRaw ? Object.assign({}, selRaw, { pending: !!selRaw.pending, pendingRight: selRaw.pending || '', fbSweep: !!selRaw.fbSweep }) : {} };
  }
  adminGroups(platform, counts) {
    // the navigation groups, filtered by rights: a platform admin sees everything; a Sweep admin sees the Sweep group and,
    // under Community, only "Feedback · Sweep" (scoped right Feedback · <feature>, separate from Community admin)
    var c = counts || {};
    var ALL = [
      { key: 'core', label: 'Core', core: true, items: [ { key: 'general', label: 'General' }, { key: 'users', label: 'Users and permissions', n: c.users }, { key: 'groups', label: 'Groups' }, { key: 'audit', label: 'Audit log' } ] },
      { key: 'sweep', label: 'Sweep', isSweep: true, remote: 'sweep-admin@1.4', owner: 'Platform team', items: [ { key: 'connectors', label: 'Connectors', n: c.connectors } ] },
      { key: 'new', label: 'Community', isNew: true, remote: 'community-admin@4.6', owner: 'Platform team', items: [ { key: 'releases', label: 'Releases', n: c.releases }, { key: 'tours', label: 'Tours', n: c.tours }, { key: 'listen', label: 'Feedback', n: c.listen }, { key: 'ideas', label: 'Ideas', n: c.ideas }, { key: 'insights', label: 'Insights' } ] }
    ];
    return ALL.filter(function (g) { return platform || !g.core; }).map(function (g) {
      var items = g.items.filter(function (i) { return platform || g.key === 'sweep' || i.key === 'listen'; }).map(function (i) { return Object.assign({}, i, !platform && i.key === 'listen' ? { label: 'Feedback · Sweep', n: c.listenScoped } : {}); });
      return Object.assign({}, g, { items: items });
    });
  }
  feedbackProfiles(s, set, opts) {
    // FeedbackProfile: the editor for one feature's feedback form, used in Community > Feedback > Profiles (kept as its own component).
    // s.fp holds the edits per profile key; opts.onSave(name) returns the state patch shown after saving
    var o = opts || {}, ON = 'background: #E3DFFF; border-color: #E3DFFF; color: #191836';
    var val = function (e) { return e && e.target ? e.target.value : ''; };
    var FP0 = {
      sweep: { name: 'Sweep', owner: 'Sweep team', home: 'Community › Feedback', on: true, entries: { page: true, after: true, ai: false, global: false }, qs: [ { type: 'scale', text: 'How did this Sweep run go?' }, { type: 'single', text: 'Which phase needs work?' }, { type: 'text', text: 'Anything to add?' } ], sampling: '20', routing: 'jira', anon: true, ctx: true },
      env: { name: 'Environments', owner: 'Release team', home: 'Community › Feedback', on: true, entries: { page: true, after: true, ai: false, global: false }, qs: [ { type: 'thumbs', text: 'Did this deployment go as expected?' }, { type: 'text', text: 'What went wrong?' } ], sampling: '10', routing: 'inbox', anon: false, ctx: true },
      docs: { name: 'Docs', owner: 'Platform team', home: 'Community › Feedback', on: true, entries: { page: true, after: false, ai: false, global: false }, qs: [ { type: 'thumbs', text: 'Was this page useful?' } ], sampling: '100', routing: 'inbox', anon: true, ctx: true },
      assistant: { name: 'Assistant', owner: 'AI platform team', home: 'Community › Feedback', on: true, entries: { page: false, after: false, ai: true, global: false }, qs: [ { type: 'thumbs', text: 'Rate this answer' }, { type: 'single', text: 'What was wrong?' } ], sampling: '100', routing: 'teams', anon: false, ctx: true },
      global: { name: 'AIToolbox (global)', owner: 'Platform team', home: 'Community › Feedback', on: true, entries: { page: false, after: false, ai: false, global: true }, qs: [ { type: 'text', text: 'Tell us anything about AIToolbox' } ], sampling: '100', routing: 'inbox', anon: true, ctx: false }
    };
    var FPS = Object.assign({}, FP0, s.fp || {});
    var ENTRY = { page: 'Page button', after: 'After an action', ai: 'On AI answers', global: 'Account menu' };
    var ROUTE = { inbox: 'Team inbox', jira: 'Inbox + Jira', teams: 'Inbox + Teams' };
    var QT = { thumbs: 'Thumbs', scale: 'Scale 1–5', nps: 'NPS 0–10', single: 'Single choice', multi: 'Multiple choice', text: 'Text' };
    var setFp = function (key, patch) { var all = Object.assign({}, s.fp || {}); all[key] = Object.assign({}, FPS[key], patch); return { fp: all }; };
    var summary = function (k) { var p = FPS[k]; return { key: k, name: p.name, owner: p.owner, home: p.home, status: p.on ? 'On' : 'Off', tile: p.on ? 'ok' : 'ne', entries: Object.keys(p.entries).filter(function (e) { return p.entries[e]; }).map(function (e) { return ENTRY[e]; }).join(', ') || '—', nq: p.qs.length, sampling: p.entries.after ? p.sampling + '%' : '—', routing: ROUTE[p.routing] }; };
    var editor = function (fk, extra) {
      var fpv = FPS[fk]; if (!fpv) return {};
      return Object.assign({
        key: fk, name: fpv.name, owner: fpv.owner, on: fpv.on, onLabel: fpv.on ? 'Profile on' : 'Profile off', onStyle: fpv.on ? ON : '', toggle: set(setFp(fk, { on: !fpv.on })),
        entryChips: Object.keys(ENTRY).map(function (e) { return { label: ENTRY[e], on: !!fpv.entries[e], style: fpv.entries[e] ? ON : '', pick: set(function () { var en = Object.assign({}, fpv.entries); en[e] = !en[e]; return setFp(fk, { entries: en }); }) }; }),
        nq: fpv.qs.length, canAdd: fpv.qs.length < 3, noQ: fpv.qs.length === 0, addQ: set(setFp(fk, { qs: fpv.qs.concat([{ type: 'text', text: '' }]) })),
        qs: fpv.qs.map(function (q, i) { var upd = function (patch) { var arr = fpv.qs.map(function (x) { return Object.assign({}, x); }); Object.assign(arr[i], patch); return setFp(fk, { qs: arr }); }; return { n: i + 1, type: q.type, text: q.text, textOr: q.text || 'Question ' + (i + 1), typeLabel: QT[q.type], onType: set(function (e) { return upd({ type: val(e) }); }), onText: set(function (e) { return upd({ text: val(e) }); }), del: set(function () { return setFp(fk, { qs: fpv.qs.filter(function (x, k) { return k !== i; }) }); }) }; }),
        samplingChips: ['10', '20', '50', '100'].map(function (v) { return { label: v + '%', on: fpv.sampling === v, style: fpv.sampling === v ? ON : '', pick: set(setFp(fk, { sampling: v })) }; }),
        routing: fpv.routing, onRouting: set(function (e) { return setFp(fk, { routing: val(e) }); }),
        optChips: [ { k: 'anon', label: 'Allow anonymous' }, { k: 'ctx', label: 'Attach context' } ].map(function (x) { return { label: x.label, on: !!fpv[x.k], style: fpv[x.k] ? ON : '', pick: set(function () { var p = {}; p[x.k] = !fpv[x.k]; return setFp(fk, p); }) }; }),
        ctx: !!fpv.ctx, canClose: false, close: set({}),
        save: set(function () { return o.onSave ? o.onSave(fpv.name) : {}; })
      }, extra || {});
    };
    return { FPS: FPS, keys: Object.keys(FPS), summary: summary, editor: editor };
  }
  adminNav(groupsRaw, curKey, go) {
    // groups / sections holes for the sidebar, the select and the section chips; `go(key)` returns the click handler
    var find = function (key) { for (var i = 0; i < groupsRaw.length; i++) for (var j = 0; j < groupsRaw[i].items.length; j++) if (groupsRaw[i].items[j].key === key) return { g: groupsRaw[i], s: groupsRaw[i].items[j] }; return null; };
    var cur = find(curKey) || find(groupsRaw[0].items[0].key);
    var groups = groupsRaw.map(function (g) { var on = g.key === cur.g.key; return Object.assign({}, g, { on: on, tabCls: on ? 'tab-on' : '', pick: go(g.items[0].key),
      items: g.items.map(function (i) { var o = i.key === cur.s.key; return Object.assign({}, i, { on: o, cur: o ? 'page' : 'false', cls: o ? 'on' : '', hasN: !!i.n, pick: go(i.key) }); }) }); });
    var ON = 'background: #E3DFFF; border-color: #E3DFFF; color: #191836';
    var sections = cur.g.items.map(function (i) { var o = i.key === cur.s.key; return Object.assign({}, i, { on: o, style: o ? ON : '', hasN: !!i.n, pick: go(i.key) }); });
    return { cur: cur, groups: groups, sections: sections };
  }
"""
