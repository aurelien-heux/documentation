"""Build WhatsNewLayoutLab.dc.html: the same release content (meta, title, summary, changes, actions, feedback)
arranged in five news-item layouts, inside an unchanged page (feed + side column: champions, office hours, rating)."""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
import shell as S, navgen as N
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()

SPARK = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#006A6A" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/></svg>'
TOUR_IC = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#35307E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 3l6 16 2.2-6.8L20 10z"/><path d="M14 14l5 5"/></svg>'
VID_IC = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#35307E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3"/></svg>'

FILTERS = '<div class="filters"><span class="chip chip-on">All</span><span class="chip">Features</span><span class="chip">' + SPARK.replace('14', '18') + 'AI topics</span><span class="chip">Fixes</span><span class="chip">Policies</span><span style="flex: 1"></span><span class="chip">Mark all as read</span></div>'

# ---- the atoms: identical in every layout ----
VERSION = '<sc-if value="{{r.hasVersion}}" hint-placeholder-val="{{true}}"><span class="mono" style="font-size: 13px; color: #14085E; background: #E3DFFF; padding: 2px 8px; border-radius: 4px">{{r.version}}</span></sc-if>'
TYPE = '<span class="tag" style="background: {{r.typeBg}}; color: {{r.typeFg}}"><sc-if value="{{r.isAi}}" hint-placeholder-val="{{false}}">' + SPARK + '</sc-if>{{r.typeLabel}}</span>'
ACTION = '<sc-if value="{{r.action}}" hint-placeholder-val="{{false}}"><span class="tile wn"><i></i>{{r.actionLabel}}</span></sc-if>'
DATE = '<span class="meta">{{r.meta}}</span>'
UNREAD = '<sc-if value="{{r.unread}}" hint-placeholder-val="{{true}}"><span style="display: inline-flex; align-items: center; gap: 6px; font-size: 12px; color: #48454E"><span style="width: 8px; height: 8px; border-radius: 50%; background: #35307E"></span>New</span></sc-if>'
TITLE = '<div class="ttl" style="font-size: 18px; line-height: 24px">{{r.title}}</div>'
SUMMARY = '<p style="margin: 0; font-size: 14px; line-height: 20px; color: #48454E; max-width: 72ch">{{r.summary}}</p>'
BULLETS = '<sc-if value="{{r.hasBullets}}" hint-placeholder-val="{{true}}"><ul class="chg"><sc-for list="{{r.bullets}}" as="b" hint-placeholder-count="2"><li><span class="tag" style="background: {{b.bg}}; color: {{b.fg}}; flex: none">{{b.tag}}</span><span><b>{{b.lead}}</b> — {{b.text}}</span></li></sc-for></ul></sc-if>'
B_READ = '<span class="btn t">{{r.readLabel}}</span>'
B_TOUR = '<sc-if value="{{r.hasTour}}" hint-placeholder-val="{{true}}"><span class="chip">' + TOUR_IC + 'Try it in the app · 3 steps</span></sc-if>'
B_VIDEO = '<sc-if value="{{r.hasVideo}}" hint-placeholder-val="{{true}}"><span class="chip">' + VID_IC + 'Watch · {{r.videoLen}}</span></sc-if>'
B_ACK = '<sc-if value="{{r.hasAck}}" hint-placeholder-val="{{false}}"><span class="chip">I have read and understood</span></sc-if>'
USEFUL = '<span style="font-size: 13px; color: #48454E">Was this useful?</span><span class="chip">Yes</span><span class="chip">No</span>'
QTOG = S.qa_toggle('r')
DISC = ''  # the Discussion summary bar at the end of the item is the only control (pattern A)
QA = S.qa_block('r')
STAT = '<span class="meta">{{r.helpfulStat}}</span>'

ACTIONS_ROW = '<div class="row" style="gap: 8px; flex-wrap: wrap">' + B_READ + B_TOUR + B_VIDEO + B_ACK + '</div>'
FOOT_ROW = '<div class="row foot" style="flex-wrap: wrap">' + USEFUL + '<span style="margin-left: 8px">' + DISC + '</span><span style="margin-left: auto">' + STAT + '</span></div>'
META_ROW = '<div class="row" style="gap: 8px; flex-wrap: wrap">' + VERSION + TYPE + ACTION + DATE + '<span style="margin-left: auto">' + UNREAD + '</span></div>'

def card(inner, extra=''):
    return '<sc-for list="{{rels}}" as="r" hint-placeholder-count="3"><article class="card" style="padding: 20px 24px; ' + extra + '">' + inner + '</article></sc-for>'

# A · stacked (today)
A = card('<div class="stack">' + META_ROW + TITLE + SUMMARY + BULLETS + ACTIONS_ROW + FOOT_ROW + QA + '</div>')

# B · meta gutter: meta stacked in a 140 px left column, content on the right
GUTTER = '<div class="gut">' + VERSION + TYPE + ACTION + DATE + UNREAD + '</div>'
B = card('<div class="lay-b" style="display: grid; grid-template-columns: 156px minmax(0, 1fr); gap: 20px">' + GUTTER + '<div class="stack">' + TITLE + SUMMARY + BULLETS + ACTIONS_ROW + FOOT_ROW + QA + '</div></div>')

# C · split: what changed on the left, what to do on the right
RAIL = ('<div class="rail">' + '<div class="stack" style="gap: 8px; align-items: stretch">' + B_READ + B_TOUR + B_VIDEO + B_ACK + '</div>'
        '<div class="stack" style="gap: 8px; border-top: 1px solid #CAC4CF; padding-top: 12px"><div class="row" style="gap: 8px; flex-wrap: wrap">' + USEFUL + '</div>' + DISC + STAT + '</div></div>')
C = card('<div class="stack"><div class="lay-c" style="display: grid; grid-template-columns: minmax(0, 1fr) 240px; gap: 24px; align-items: start"><div class="stack">' + META_ROW + TITLE + SUMMARY + BULLETS + '</div>' + RAIL + '</div>' + QA + '</div>')

# D · changelog: changes as a table, actions and feedback on one line
BULLETS_T = '<sc-if value="{{r.hasBullets}}" hint-placeholder-val="{{true}}"><div class="chgt"><sc-for list="{{r.bullets}}" as="b" hint-placeholder-count="2"><div class="chgr"><span><span class="tag" style="background: {{b.bg}}; color: {{b.fg}}">{{b.tag}}</span></span><b>{{b.lead}}</b><span>{{b.text}}</span></div></sc-for></div></sc-if>'
UP = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 10v11M15 5.9l-1 4.1H21a2 2 0 0 1 2 2.3l-1.4 7a2 2 0 0 1-2 1.7H7V10l5-7a2.3 2.3 0 0 1 3 2.9z"/></svg>'
DOWN = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17 14V3M9 18.1l1-4.1H3a2 2 0 0 1-2-2.3l1.4-7A2 2 0 0 1 4.4 3H17v11l-5 7a2.3 2.3 0 0 1-3-2.9z"/></svg>'
FEED_D = '<span class="row" style="gap: 8px; margin-left: auto; flex-wrap: nowrap">' + DISC + '<span style="font-size: 13px; color: #48454E; margin-left: 4px">Useful?</span><span class="chip thumb" aria-label="Useful: yes">' + UP + '</span><span class="chip thumb" aria-label="Useful: no">' + DOWN + '</span></span>'
D = card('<div class="stack">' + META_ROW + TITLE + SUMMARY + BULLETS_T + '<div class="row foot" style="gap: 8px; flex-wrap: wrap">' + B_READ + B_TOUR + B_VIDEO + B_ACK + FEED_D + '</div>' + QA + '</div>')

# E · progressive: summary and actions first, the changes behind a toggle
TOGGLE = '<sc-if value="{{r.hasBullets}}" hint-placeholder-val="{{true}}"><span class="chip" style="{{r.togStyle}}" role="button" aria-expanded="{{r.open}}" onClick="{{r.toggle}}">What changed · {{r.nBullets}}<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="transform: {{r.chev}}"><path d="M6 9l6 6 6-6"/></svg></span></sc-if>'
E = card('<div class="stack">' + META_ROW + TITLE + SUMMARY + '<div class="row" style="gap: 8px; flex-wrap: wrap">' + B_READ + B_TOUR + B_VIDEO + B_ACK + TOGGLE + '</div>'
         '<sc-if value="{{r.open}}" hint-placeholder-val="{{false}}">' + BULLETS + '</sc-if>' + FOOT_ROW + QA + '</div>')

CHAMPS = '<section class="card stack" style="gap: 10px"><span class="h2">Champions near you</span><sc-for list="{{champs}}" as="c" hint-placeholder-count="3"><div class="row"><span class="av" style="background: {{c.bg}}">{{c.ini}}</span><div style="flex: 1; min-width: 0"><div class="ui" style="font-size: 14px; font-weight: 600">{{c.who}}</div><div class="meta" style="white-space: normal">{{c.team}} · {{c.topics}}</div></div><span class="chip">Ask</span></div></sc-for><span class="lnk">Become a champion</span></section>'
OFFICE = '<section class="card stack" style="gap: 10px"><div class="row" style="justify-content: space-between; flex-wrap: wrap"><span class="h2">Office hours</span><span class="tile in"><i></i>Thu 31 Oct · 14:00</span></div><p style="margin: 0; font-size: 14px; line-height: 20px; color: #48454E">Live Q&amp;A on the assistant model change with the platform team. 30 minutes, recorded.</p><div class="row" style="flex-wrap: wrap"><span class="btn t">Add to calendar</span><span class="lnk">Submit a question</span></div></section>'
NPS = '<section class="card stack" style="gap: 10px"><span class="h2">How likely are you to recommend AIToolbox to a colleague?</span><div class="scale"><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>10</span></div><div class="row" style="justify-content: space-between; font-size: 12px; color: #48454E"><span>Not likely</span><span>Very likely</span></div></section>'
SIDE = CHAMPS + OFFICE + NPS

for k, v in {'A': A, 'B': B, 'C': C, 'D': D, 'E': E}.items():
    s = s.replace(f'<!--ITEMS:{k}-->', v)
s = s.replace('<!--FILTERS-->', FILTERS).replace('<!--SIDE-->', SIDE)
s = (s.replace('<!--SIMCSS-->', S.SIM_CSS).replace('<!--QACSS-->', S.QA_CSS).replace('<!--SIMBAR-->', S.sim_bar()).replace('<!--SIMOPEN-->', S.sim_open('sim-host-wn', 'height: 1080px'))
     .replace('<!--SIMCLOSE-->', S.SIM_CLOSE).replace('<!--NAVBAR-->', S.navbar(N.LIGHT, 'new')).replace('/*SIMJS*/', S.SIM_JS).replace('/*QAJS*/', S.QA_JS))
s = s.replace('<!--CSS-->', S.CSS).replace('<!--HEADER-->', S.header(False, "Community · What's new", 'Releases, AI topics and policies for your workspace')).replace('<!--RAIL-->', N.rail(N.LIGHT, 'new'))
s = re.sub(r'<!-- [^\n]*? -->', '', s)
assert '<!--' not in s, re.findall(r'<!--[^>]*>', s)[:3]
for t in ['sc-if', 'sc-for']:
    assert len(re.findall(rf'<{t}\b', s)) == len(re.findall(rf'</{t}>', s)), t
open(dst, 'w', encoding='utf-8').write(s); print(len(s))
