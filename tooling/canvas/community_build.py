"""Assemble CommunityLive.dc.html from live/p1..p5 with the shared shell, nav variants and header handlers."""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
import navgen as N, shell as S

SRC = os.path.join(os.path.dirname(__file__), '..', 'adoption', 'src', 'live')
DST = sys.argv[1]
parts = ''.join(open(os.path.join(SRC, f'p{i}.html'), encoding='utf-8').read() for i in range(1, 6))

# header with handlers
h = S.header(False)
h = h.replace('<button type="button" class="ui" style="display: inline-flex; align-items: center; gap: 6px; height: 32px;', '<button type="button" class="ui" onClick="{{askAssistant}}" style="display: inline-flex; align-items: center; gap: 6px; height: 32px;')
h = h.replace('aria-label="Open assistant">', 'aria-label="Open assistant" data-anchor="header.assistant" onClick="{{askAssistant}}">')
h = h.replace('<div role="search"', '<div role="search" data-anchor="header.ask"')
h = h.replace('class="ib hdr-menu" aria-label="Open navigation"', 'class="ib hdr-menu" aria-label="Open navigation" onClick="{{toggleNav}}"')
h = h.replace('class="ib hdr-sbtn" aria-label="Search"', 'class="ib hdr-sbtn" aria-label="Search" data-anchor="header.ask" onClick="{{askAssistant}}"')
assert 'data-anchor="header.ask"' in h
h = h.replace('aria-label="Notifications, 3 unread">', 'aria-label="Notifications, 3 unread" data-anchor="header.bell" aria-expanded="{{panel}}" onClick="{{togglePanel}}" style="background: {{bellBg}}">')
h = h.replace('aria-expanded="false" style=""', 'aria-expanded="{{help}}" onClick="{{toggleHelp}}" style="background: {{helpBg}}"')
h = h.replace('aria-haspopup="menu" style="display: inline-flex; align-items: center; gap: 10px; height: 44px; padding: 0 10px 0 6px; border: 0; border-radius: 16px; background: transparent;',
              'aria-haspopup="menu" aria-expanded="{{menu}}" onClick="{{toggleMenu}}" style="display: inline-flex; align-items: center; gap: 10px; height: 44px; padding: 0 10px 0 6px; border: 0; border-radius: 16px; background: {{menuBg}};')
assert h.count('{{') == 15, h.count('{{')

# nav variants
def wire(nav, drawer):
    nav = nav.replace('href="#sweep"', 'href="#sweep" data-anchor="rail.sweep" onClick="{{goSweep}}"').replace('href="#new"', 'href="#new" data-anchor="rail.community" onClick="{{goCommunity}}"').replace('href="#admin"', 'href="#admin" onClick="{{goAdmin}}"')
    i = nav.index('<a href="#admin"'); j = nav.index('</a>', i) + 4
    nav = nav[:i] + '<sc-if value="{{showAdminNav}}" hint-placeholder-val="{{true}}">' + nav[i:j] + '</sc-if>' + nav[j:]
    lab = 'Collapse navigation' if drawer else 'Open navigation'
    nav = nav.replace(f'aria-label="{lab}"', f'aria-label="{lab}" aria-expanded="{"true" if drawer else "false"}" onClick="{{{{toggleNav}}}}"')
    assert 'toggleNav' in nav
    return nav
nav = (f'<sc-if value="{{{{navNewD}}}}" hint-placeholder-val="{{{{false}}}}">{wire(N.drawer(N.LIGHT, "new"), True)}</sc-if>'
       f'<sc-if value="{{{{navSweepD}}}}" hint-placeholder-val="{{{{false}}}}">{wire(N.drawer(N.LIGHT, "sweep"), True)}</sc-if>'
       f'<sc-if value="{{{{navNewR}}}}" hint-placeholder-val="{{{{true}}}}">{wire(N.rail(N.LIGHT, "new"), False)}</sc-if>'
       f'<sc-if value="{{{{navSweepR}}}}" hint-placeholder-val="{{{{false}}}}">{wire(N.rail(N.LIGHT, "sweep"), False)}</sc-if>'
       f'<sc-if value="{{{{navAdminD}}}}" hint-placeholder-val="{{{{false}}}}">{wire(N.drawer(N.LIGHT, "admin"), True)}</sc-if>'
       f'<sc-if value="{{{{navAdminR}}}}" hint-placeholder-val="{{{{false}}}}">{wire(N.rail(N.LIGHT, "admin"), False)}</sc-if>')

for k in ['sweep','env','docs','new']:
    parts = parts.replace(f'<!--MARK:{k}-->', N.mark(k, N.LIGHT, 26))
def wire_bar(bar):
    bar = bar.replace('href="#sweep"', 'href="#sweep" data-anchor="rail.sweep" onClick="{{goSweep}}"').replace('href="#new"', 'href="#new" data-anchor="rail.community" onClick="{{goCommunity}}"')
    return bar.replace('type="button" aria-label="Open assistant"', 'type="button" aria-label="Open assistant" data-anchor="header.assistant" onClick="{{askAssistant}}"')
bar = (f'<sc-if value="{{{{navBarNew}}}}" hint-placeholder-val="{{{{true}}}}">{wire_bar(S.navbar(N.LIGHT, "new"))}</sc-if>'
       f'<sc-if value="{{{{navBarSweep}}}}" hint-placeholder-val="{{{{false}}}}">{wire_bar(S.navbar(N.LIGHT, "sweep"))}</sc-if>'
       f'<sc-if value="{{{{navBarAdmin}}}}" hint-placeholder-val="{{{{false}}}}">{wire_bar(S.navbar(N.LIGHT, "none"))}</sc-if>')
chips = open(os.path.join(SRC, 'rolechips.frag'), encoding='utf-8').read().strip()
chips = chips.replace('border: 1px dashed #79757F; border-radius: 12px; align-self: flex-start', 'margin-right: 8px; padding-right: 12px; border-right: 1px solid #CAC4CF')
parts = (parts.replace('<!--ADMINCSS-->', S.ADMIN_CSS).replace('<!--ADMIN:TREE-->', S.admin_tree('ad-side')).replace('<!--ADMIN:SELECT-->', S.ADMIN_SELECT)
         .replace('<!--ADMIN:USERS-->', S.ADMIN_USERS).replace('<!--ADMIN:RUNNERS-->', S.ADMIN_RUNNERS).replace('<!--ADMIN:CONNECTORS-->', S.ADMIN_CONNECTORS).replace('<!--ADMIN:GENERAL-->', S.ADMIN_GENERAL).replace('<!--ADMIN:PLACEHOLDER-->', S.ADMIN_PLACEHOLDER).replace('<!--ADMIN:FEEDBACK-->', S.ADMIN_FEEDBACK).replace('<!--ADMIN:FBTABS-->', S.ADMIN_FEEDBACK_TABS).replace('/*ADMINJS*/', S.ADMIN_JS))
parts = parts.replace('<!--QATOG:it-->', S.qa_toggle('it')).replace('<!--QATOG:sel-->', S.qa_toggle('sel')).replace('<!--QACSS-->', S.QA_CSS).replace('<!--QA:it-->', S.qa_block('it')).replace('<!--QA:sel-->', S.qa_block('sel')).replace('/*QAJS*/', S.QA_JS)
parts = (parts.replace('<!--SIMCSS-->', S.SIM_CSS).replace('<!--SIMBAR-->', S.sim_bar(chips)).replace('<!--SIMOPEN-->', S.sim_open('sim-host-cl', 'height: {{simFrameH}}px'))
         .replace('<!--SIMCLOSE-->', S.SIM_CLOSE).replace('<!--NAVBAR-->', bar).replace('/*SIMJS*/', S.SIM_JS))
out = parts.replace('<!--CSS-->', S.CSS).replace('<!--HEADER-->', h).replace('<!--NAV-->', nav)
out = re.sub(r'<!--[^\n]*?-->', '', out)  # strip authoring comments
assert '<!--' not in out
for t in ['sc-if', 'sc-for']:
    assert len(re.findall(rf'<{t}\b', out)) == len(re.findall(rf'</{t}>', out)), t
open(DST, 'w', encoding='utf-8').write(out)
print(len(out))
