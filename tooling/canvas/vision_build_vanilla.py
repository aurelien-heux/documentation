"""Assemble ProductionVision.dc.html (AIToolbox production vision) from vision/p1..p5 + vision.js and vision_parts:
Sweep, Environments, Docs, Catalog, Community, Administration and the assistant pane in one prototype."""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
import navgen as N, shell as S, vision_parts as VP, vision_sweep as VS

SRC = os.path.join(os.path.dirname(__file__), 'vision-prototype-src')
DST = sys.argv[1]
parts = ''.join(open(os.path.join(SRC, f'p{i}.html'), encoding='utf-8').read() for i in range(1, 6))

# header with handlers
h = S.header(False)
h = h.replace('<button type="button" class="ui" style="display: inline-flex; align-items: center; gap: 6px; height: 32px;', '<button type="button" class="ui" onClick="{{hdrAsk}}" style="display: inline-flex; align-items: center; gap: 6px; height: 32px;')
h = h.replace('<input id="sh-q" type="text" placeholder="Search, or ask the assistant…"', '<input id="sh-q" type="text" placeholder="Search, or ask the assistant…" value="{{asDraft}}" onChange="{{asOnDraft}}" onKeyDown="{{hdrKey}}"')
h = h.replace('aria-label="Open assistant">', 'aria-label="Open assistant" data-anchor="header.assistant" onClick="{{askAssistant}}">')
h = h.replace('<div role="search"', '<div role="search" data-anchor="header.ask"')
h = h.replace('class="ib hdr-menu" aria-label="Open navigation"', 'class="ib hdr-menu" aria-label="Open navigation" onClick="{{toggleNav}}"')
h = h.replace('class="ib hdr-sbtn" aria-label="Search"', 'class="ib hdr-sbtn" aria-label="Search" data-anchor="header.ask" onClick="{{askAssistant}}"')
assert 'data-anchor="header.ask"' in h
h = h.replace('aria-label="Notifications, 3 unread">', 'aria-label="Notifications, 3 unread" data-anchor="header.bell" aria-expanded="{{panel}}" onClick="{{togglePanel}}" style="background: {{bellBg}}">')
h = h.replace('aria-expanded="false" style=""', 'aria-expanded="{{help}}" onClick="{{toggleHelp}}" style="background: {{helpBg}}"')
h = h.replace('aria-haspopup="menu" style="display: inline-flex; align-items: center; gap: 10px; height: 44px; padding: 0 10px 0 6px; border: 0; border-radius: 16px; background: transparent;',
              'aria-haspopup="menu" aria-expanded="{{menu}}" onClick="{{toggleMenu}}" style="display: inline-flex; align-items: center; gap: 10px; height: 44px; padding: 0 10px 0 6px; border: 0; border-radius: 16px; background: {{menuBg}};')
assert h.count('{{') == 18, h.count('{{')

# nav variants
def wire(nav, drawer):
    nav = nav.replace('href="#sweep"', 'href="#sweep" data-anchor="rail.sweep" onClick="{{goSweep}}"').replace('href="#new"', 'href="#new" data-anchor="rail.community" onClick="{{goCommunity}}"').replace('href="#admin"', 'href="#admin" onClick="{{goAdmin}}"')
    nav = nav.replace('href="#catalog"', 'href="#catalog" data-anchor="rail.catalog" onClick="{{goCatalog}}"').replace('href="#env"', 'href="#env" onClick="{{goEnv}}"').replace('href="#docs"', 'href="#docs" onClick="{{goDocs}}"')
    i = nav.index('<a href="#admin"'); j = nav.index('</a>', i) + 4
    nav = nav[:i] + '<sc-if value="{{showAdminNav}}" hint-placeholder-val="{{true}}">' + nav[i:j] + '</sc-if>' + nav[j:]
    lab = 'Collapse navigation' if drawer else 'Open navigation'
    nav = nav.replace(f'aria-label="{lab}"', f'aria-label="{lab}" aria-expanded="{"true" if drawer else "false"}" onClick="{{{{toggleNav}}}}"')
    assert 'toggleNav' in nav
    return nav
VARS = [('navNew', 'new'), ('navSweep', 'sweep'), ('navAdmin', 'admin'), ('navCat', 'catalog'), ('navEnv', 'env'), ('navDocs', 'docs')]
nav = ''.join(f'<sc-if value="{{{{{v}D}}}}" hint-placeholder-val="{{{{false}}}}">{wire(N.drawer(N.LIGHT, k, catalog=True), True)}</sc-if>'
              f'<sc-if value="{{{{{v}R}}}}" hint-placeholder-val="{{{{{"true" if k == "sweep" else "false"}}}}}">{wire(N.rail(N.LIGHT, k, catalog=True), False)}</sc-if>' for v, k in VARS)

for k in ['sweep','env','docs','new','catalog']:
    parts = parts.replace(f'<!--MARK:{k}-->', N.mark(k, N.LIGHT, 26))
def wire_bar(bar):
    bar = bar.replace('href="#sweep"', 'href="#sweep" data-anchor="rail.sweep" onClick="{{goSweep}}"').replace('href="#new"', 'href="#new" data-anchor="rail.community" onClick="{{goCommunity}}"').replace('href="#env"', 'href="#env" onClick="{{goEnv}}"').replace('href="#docs"', 'href="#docs" onClick="{{goDocs}}"')
    return bar.replace('type="button" aria-label="Open assistant"', 'type="button" aria-label="Open assistant" data-anchor="header.assistant" onClick="{{askAssistant}}"')
bar = ''.join(f'<sc-if value="{{{{{v}}}}}" hint-placeholder-val="{{{{{"true" if k == "sweep" else "false"}}}}}">{wire_bar(S.navbar(N.LIGHT, k))}</sc-if>' for v, k in [('navBarNew', 'new'), ('navBarSweep', 'sweep'), ('navBarAdmin', 'none'), ('navBarCat', 'none'), ('navBarEnv', 'env'), ('navBarDocs', 'docs')])
chips = open(os.path.join(SRC, 'rolechips.frag'), encoding='utf-8').read().strip()
chips = chips.replace('border: 1px dashed #79757F; border-radius: 12px; align-self: flex-start', 'margin-right: 8px; padding-right: 12px; border-right: 1px solid #CAC4CF')
parts = (parts.replace('<!--ADMINCSS-->', S.ADMIN_CSS).replace('<!--ADMIN:TREE-->', S.admin_tree('ad-side')).replace('<!--ADMIN:SELECT-->', S.ADMIN_SELECT)
         .replace('<!--ADMIN:USERS-->', S.ADMIN_USERS).replace('<!--ADMIN:RUNNERS-->', S.ADMIN_RUNNERS).replace('<!--ADMIN:CONNECTORS-->', '<!--ADMIN:CONNECTORS-->').replace('<!--ADMIN:GENERAL-->', S.ADMIN_GENERAL).replace('<!--ADMIN:PLACEHOLDER-->', S.ADMIN_PLACEHOLDER).replace('<!--ADMIN:FEEDBACK-->', S.ADMIN_FEEDBACK).replace('<!--ADMIN:FBTABS-->', S.ADMIN_FEEDBACK_TABS).replace('/*ADMINJS*/', S.ADMIN_JS))
parts = parts.replace('<!--QATOG:it-->', S.qa_toggle('it')).replace('<!--QATOG:sel-->', S.qa_toggle('sel')).replace('<!--QACSS-->', S.QA_CSS).replace('<!--QA:it-->', S.qa_block('it')).replace('<!--QA:sel-->', S.qa_block('sel')).replace('/*QAJS*/', S.QA_JS)
parts = (parts.replace('<!--SIMCSS-->', S.SIM_CSS).replace('<!--SIMBAR-->', S.sim_bar(chips)).replace('<!--SIMOPEN-->', S.sim_open('sim-host-cl', 'height: {{simFrameH}}px'))
         .replace('<!--SIMCLOSE-->', S.SIM_CLOSE).replace('<!--NAVBAR-->', bar).replace('/*SIMJS*/', S.SIM_JS))
# Sweep, aligned on the running application: runs from Jira tickets, agents pipeline, live console
CONN = (S.ADMIN_CONNECTORS
        .replace('<b class="ui">DevOps platform</b><div class="meta">devops.example.internal · also used by the DevOps MCP server</div>', '<b class="ui">Bitbucket</b><div class="meta">bitbucket.example.internal · project E2ECC · also used by the DevOps MCP server</div>')
        .replace('Repositories, pipelines, pull requests', 'Clones, branches and pull requests opened by the agents')
        .replace('Projects SWP, PAY, CB · used by Create Jira ticket', 'Projects E2ECC, SWP · read by the Jira planner')
        .replace('Blocking findings become tickets', 'Tickets the runs start from')
        .replace('Quality gate in the Test phase', 'Quality gate in the integration check'))
_llm = ('<tr class="rw"><td class="td"><b class="ui">LLM endpoint</b><div class="meta">openai/qwen3.6-27b · self-hosted, egress guarded</div></td><td class="td"><span style="font-size: 13px">Planner, Coder and Reviewer agents</span></td>'
        '<td class="td">1 model</td><td class="td"><span class="tile ok"><i></i>Connected</span></td><td class="td"><span class="meta">2 min ago</span></td><td class="td" style="text-align: right"><button type="button" class="chip" style="height: 28px">Configure</button></td></tr>')
_i = CONN.index('<tr class="rw"><td class="td"><b class="ui">Microsoft Teams</b>'); CONN = CONN[:_i] + _llm + CONN[_i:]
assert 'Bitbucket' in CONN and 'integration check' in CONN
parts = parts.replace('<!--ADMIN:CONNECTORS-->', CONN)
parts = parts.replace('<!--VISION:SWEEP-->', VS.SCREEN).replace('<!--VISION:SWEEPDLG-->', VS.DIALOG).replace('<!--VISIONCSS-->', VS.CSS + '<!--VISIONCSS-->')
parts = parts.replace('/*VISIONJS*/', VS.JS + '/*VISIONJS*/')
parts = (parts.replace('<!--VISIONCSS-->', VP.CSS).replace('<!--VISION:SCREENS-->', VP.SCREENS).replace('<!--VISION:PANE-->', VP.PANE)
         .replace('<!--VISION:ADMIN-->', VP.CAT_ADMIN + VP.VD.ADMIN_KB).replace('/*VISIONJS*/', open(os.path.join(SRC, 'vision.js'), encoding='utf-8').read() + VP.VD.JS))
parts = parts.replace('What a run may use in each phase.', 'What each agent of a run may use.')
out = parts.replace('<!--CSS-->', S.CSS).replace('<!--HEADER-->', h).replace('<!--NAV-->', nav)
out = re.sub(r'<!--[^\n]*?-->', '', out)  # strip authoring comments
assert '<!--' not in out
for t in ['sc-if', 'sc-for']:
    assert len(re.findall(rf'<{t}\b', out)) == len(re.findall(rf'</{t}>', out)), t
import markup_check
_errs = markup_check.check(out)
assert not _errs, '\n'.join(_errs[:10])
open(DST, 'w', encoding='utf-8').write(out)
print(len(out))
