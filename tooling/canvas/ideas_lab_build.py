import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
import shell as S, navgen as N
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()

FILTERS = '''<div class="filters"><span class="chip chip-on">All<span class="n">6</span></span><span class="chip">Proposed<span class="n">2</span></span><span class="chip">Under review<span class="n">1</span></span><span class="chip">Planned<span class="n">1</span></span><span class="chip">In progress<span class="n">1</span></span><span class="chip">Delivered<span class="n">1</span></span><span style="flex: 1"></span><span class="sel">Most votes</span></div>'''

ROW = '''<div class="row" style="gap: 12px; align-items: flex-start"><span class="vote {{i.vcls}}"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 14l6-6 6 6"/></svg>{{i.votes}}</span><div style="flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 6px"><div class="row" style="gap: 8px; flex-wrap: wrap"><span class="tile {{i.tile}}"><i></i>{{i.status}}</span><span class="tag" style="background: #ECE5F4">{{i.area}}</span><span class="meta">{{i.who}} · {{i.when}}</span></div><div class="ttl" style="font-size: 16px; line-height: 22px">{{i.title}}</div><div style="font-size: 13px; line-height: 18px; color: #48454E; max-width: 72ch">{{i.body}}</div><div class="row meta" style="gap: 16px"><span>{{i.nq}} messages</span><span class="lnk" style="font-size: 12px">Follow</span></div></div></div>'''

DETAIL = '''<div class="detail">
  <div class="row" style="gap: 8px; flex-wrap: wrap"><span class="tile in"><i></i>Planned</span><span class="tag" style="background: #ECE5F4">Sweep</span><span class="meta">Marta Kowalski · 12 Sep</span></div>
  <div class="ttl" style="font-size: 20px; line-height: 26px">Re-run only the failed checks</div>
  <div style="font-size: 14px; line-height: 20px; max-width: 72ch">When one check fails on a big PR, I have to re-run the whole sweep. A partial re-run from the PR page would save 10 minutes each time.</div>
  <div class="row"><span class="vbtn"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 14l6-6 6 6"/></svg>48 · Voted</span><span class="chip chip-on">Following</span></div>
  <div class="steps"><sc-for list="{{track}}" as="t" hint-placeholder-count="5"><span class="step"><b style="background: {{t.dot}}"></b><span style="color: {{t.color}}">{{t.label}}</span><sc-if value="{{t.hasWhen}}" hint-placeholder-val="{{true}}"><span class="meta">{{t.when}}</span></sc-if></span><sc-if value="{{t.notLast}}" hint-placeholder-val="{{true}}"><span class="stepline"></span></sc-if></sc-for></div>
  <div style="display: flex; gap: 8px; align-items: flex-start; padding: 8px 12px; border-radius: 8px; background: #F2EBFA; font-size: 13px; line-height: 18px"><span class="tile ne" style="flex: none"><i></i>Platform team</span><span>Planned for 4.8: partial re-run from the PR page. Design review on 5 Nov.</span></div>
  QA_HERE
</div>'''
DETAIL = DETAIL.replace('QA_HERE', S.qa_block('idq'))

LIST = '<sc-for list="{{ideas}}" as="i" hint-placeholder-count="4"><div class="irow {{i.cls}}" style="flex-direction: column; gap: 0">' + ROW + '</div></sc-for>'
# in the expanded row the row itself is the header: the detail block continues after it, without repeating status, title and text
REST = DETAIL[DETAIL.index('  <div class="row"><span class="vbtn">'):]
REST = '<div class="detail">\n' + REST
LISTX = ('<sc-for list="{{ideas}}" as="i" hint-placeholder-count="4"><div class="irow {{i.cls}}" style="flex-direction: column; gap: 12px">' + ROW +
         '<sc-if value="{{i.open}}" hint-placeholder-val="{{false}}"><div class="xdetail" style="border-top: 1px solid #CAC4CF; padding-top: 12px; padding-left: 68px">' + REST + '</div></sc-if></div></sc-for>')

s = s.replace('<!--FILTERS-->', FILTERS).replace('<!--LISTX-->', LISTX).replace('<!--LIST-->', LIST).replace('<!--DETAIL-->', DETAIL)
s = (s.replace('<!--SIMCSS-->', S.SIM_CSS).replace('<!--QACSS-->', S.QA_CSS).replace('<!--SIMBAR-->', S.sim_bar()).replace('<!--SIMOPEN-->', S.sim_open('sim-host-il', 'height: 1000px'))
     .replace('<!--SIMCLOSE-->', S.SIM_CLOSE).replace('<!--NAVBAR-->', S.navbar(N.LIGHT, 'new')).replace('/*SIMJS*/', S.SIM_JS).replace('/*QAJS*/', S.QA_JS))
s = s.replace('<!--CSS-->', S.CSS).replace('<!--HEADER-->', S.header(False, 'Community · Ideas', 'Vote once per idea; the platform team answers within two weeks')).replace('<!--RAIL-->', N.rail(N.LIGHT, 'new'))
s = re.sub(r'<!-- [^\n]*? -->', '', s)
assert '<!--' not in s
for t in ['sc-if', 'sc-for']:
    assert len(re.findall(rf'<{t}\b', s)) == len(re.findall(rf'</{t}>', s)), t
open(dst, 'w', encoding='utf-8').write(s); print(len(s))
