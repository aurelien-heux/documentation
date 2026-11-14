"""Build QAPatternLab.dc.html: four proposals for one Q&A open/close mechanic and one set of Q&A metadata,
each applied to a What's new release (layout D) and an Ideas detail (layout E), same content everywhere."""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
import shell as S, navgen as N
dst = sys.argv[1]

ST = 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
CHEV = f'<svg class="chev" width="20" height="20" viewBox="0 0 24 24" {ST}><path d="M6 9l6 6 6-6"/></svg>'
CHEV_R = f'<svg class="chev-r" width="20" height="20" viewBox="0 0 24 24" {ST}><path d="M9 6l6 6-6 6"/></svg>'
UP = f'<svg width="16" height="16" viewBox="0 0 24 24" {ST}><path d="M7 10v11M15 5.9l-1 4.1H21a2 2 0 0 1 2 2.3l-1.4 7a2 2 0 0 1-2 1.7H7V10l5-7a2.3 2.3 0 0 1 3 2.9z"/></svg>'
DOWN = f'<svg width="16" height="16" viewBox="0 0 24 24" {ST}><path d="M17 14V3M9 18.1l1-4.1H3a2 2 0 0 1-2-2.3l1.4-7A2 2 0 0 1 4.4 3H17v11l-5 7a2.3 2.3 0 0 1-3-2.9z"/></svg>'
TOUR_IC = f'<svg width="18" height="18" viewBox="0 0 24 24" {ST}><path d="M5 3l6 16 2.2-6.8L20 10z"/><path d="M14 14l5 5"/></svg>'
VOTE_IC = f'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 14l6-6 6 6"/></svg>'

def chips(x):
    return (f'<sc-if value="{{{{{x}.qaHasAnswered}}}}" hint-placeholder-val="{{{{true}}}}"><span class="tile ok"><i></i>{{{{{x}.qaAnsweredLabel}}}}</span></sc-if>'
            f'<sc-if value="{{{{{x}.qaHasWaiting}}}}" hint-placeholder-val="{{{{true}}}}"><span class="tile wn"><i></i>{{{{{x}.qaWaitingLabel}}}}</span></sc-if>')

def people(x):
    return (f'<span class="qp-ppl" aria-hidden="true"><sc-for list="{{{{{x}.qaPeople}}}}" as="p" hint-placeholder-count="3"><span class="av" style="background: {{{{p.bg}}}}">{{{{p.ini}}}}</span></sc-for></span>')

def region(x, inner):
    return f'<div class="qa" id="{{{{{x}.qaRegionId}}}}" role="region" aria-label="Questions">{inner}</div>'

# ---- A · summary bar: one full-width bar is both the summary and the control ----
def qa_A(x):
    bar = (f'<button type="button" class="qp-bar" id="{{{{{x}.qaTogId}}}}" aria-expanded="{{{{{x}.qaOpen}}}}" aria-controls="{{{{{x}.qaRegionId}}}}" onClick="{{{{{x}.qaToggle}}}}">'
           f'{CHEV}<span class="ui qp-t">Questions</span><span class="n">{{{{{x}.qaN}}}}</span>' + people(x) + chips(x) +
           f'<span class="meta">{{{{{x}.qaLastLabel}}}}</span><span class="qp-act">{{{{{x}.qaAction}}}}</span></button>')
    return bar + f'<sc-if value="{{{{{x}.qaOpen}}}}" hint-placeholder-val="{{{{false}}}}">' + region(x, S.qa_empty(x) + S.qa_items(x) + S.qa_ask(x)) + '</sc-if>'

# ---- B · action chip: a chip in the item's action row, the thread has its own header with Hide ----
def qa_B_chip(x):
    return S.qa_toggle(x)
def qa_B(x):
    return S.qa_block_chip(x)

# ---- C · section heading: the heading of the Questions section is the disclosure ----
def qa_C(x):
    return (f'<div class="qp-sec"><h3 class="qp-h"><button type="button" id="{{{{{x}.qaTogId}}}}" aria-expanded="{{{{{x}.qaOpen}}}}" aria-controls="{{{{{x}.qaRegionId}}}}" onClick="{{{{{x}.qaToggle}}}}">'
            f'{CHEV_R}Questions<span class="n">{{{{{x}.qaN}}}}</span></button>'
            f'<span class="qp-hmeta">' + chips(x) + f'<span class="meta">{{{{{x}.qaLastLabel}}}}</span></span></h3>'
            f'<sc-if value="{{{{{x}.qaOpen}}}}" hint-placeholder-val="{{{{false}}}}">' + region(x, S.qa_empty(x) + S.qa_items(x) + S.qa_ask(x)) + '</sc-if></div>')

# ---- D · preview first: the latest answered question is always shown, "Show all" opens the rest ----
def qa_D(x):
    head = (f'<div class="qa-h"><span class="ui" style="font-size: 14px; font-weight: 600">Questions · {{{{{x}.qaN}}}}</span>' + chips(x) +
            f'<span class="meta" style="margin-left: auto">{{{{{x}.qaLastLabel}}}}</span></div>')
    more = (f'<sc-if value="{{{{{x}.qaHasMore}}}}" hint-placeholder-val="{{{{true}}}}"><button type="button" class="qp-more" id="{{{{{x}.qaTogId}}}}" aria-expanded="{{{{{x}.qaOpen}}}}" aria-controls="{{{{{x}.qaRegionId}}}}" onClick="{{{{{x}.qaToggle}}}}">'
            f'{{{{{x}.qaMoreAction}}}}{CHEV}</button></sc-if>')
    body = (f'<div id="{{{{{x}.qaRegionId}}}}">' + S.qa_empty(x) +
            f'<sc-if value="{{{{{x}.qaClosed}}}}" hint-placeholder-val="{{{{true}}}}">' + S.qa_items(x, 'qaTopList') + '</sc-if>'
            f'<sc-if value="{{{{{x}.qaOpen}}}}" hint-placeholder-val="{{{{false}}}}">' + S.qa_items(x) + '</sc-if></div>')
    return f'<div class="qa qp-prev" role="region" aria-label="Questions">' + head + body + more + S.qa_ask(x) + '</div>'

QA = {'A': S.qa_block, 'B': qa_B, 'C': qa_C, 'D': qa_D}

def release(v):
    chip = qa_B_chip('r') if v == 'B' else ''
    return ('<article class="card qp-item" aria-labelledby="qp-rt-' + v + '">'
            '<div class="row" style="gap: 8px; flex-wrap: wrap"><span class="mono ver">4.6.0</span><span class="tag" style="background: #E3DFFF; color: #14085E">Feature release</span><span class="meta">24 Oct · Sweep, Assistant, Environments</span>'
            '<span class="meta" style="margin-left: auto; display: inline-flex; align-items: center; gap: 6px"><span style="width: 8px; height: 8px; border-radius: 50%; background: #35307E"></span>New</span></div>'
            '<h2 class="ui ttl" id="qp-rt-' + v + '">Approval cards for assistant tools, PR summaries in Sweep</h2>'
            '<p class="sum">The assistant now asks before any tool that changes something, and Sweep writes a review summary on every pull request.</p>'
            '<div class="chgt" role="table" aria-label="Changes in this release"><div class="chgr" role="row"><span role="cell"><span class="tag" style="background: #E3DFFF; color: #14085E">New</span></span><b role="cell">Approval card</b><span role="cell">A tool that deploys, deletes or edits waits for Run or Don’t run.</span></div>'
            '<div class="chgr" role="row"><span role="cell"><span class="tag" style="background: #9CF1F0; color: #002020">AI</span></span><b role="cell">Sweep PR summaries</b><span role="cell">Written from the diff and the pipeline logs.</span></div></div>'
            '<div class="row foot" style="gap: 8px; flex-wrap: wrap"><span class="btn t">Read the notes · 4 min</span><span class="chip">' + TOUR_IC + 'Try it in the app</span>'
            '<span class="row" style="gap: 8px; margin-left: auto; flex-wrap: nowrap">' + chip + '<span class="meta" style="font-size: 13px">Useful?</span><span class="chip thumb" aria-label="Useful: yes">' + UP + '</span><span class="chip thumb" aria-label="Useful: no">' + DOWN + '</span></span></div>'
            + QA[v]('r') + '</article>')

def idea(v):
    chip = qa_B_chip('d') if v == 'B' else ''
    return ('<section class="card qp-item" aria-labelledby="qp-it-' + v + '">'
            '<div class="row" style="gap: 8px; flex-wrap: wrap"><span class="tile in"><i></i>Planned</span><span class="tag" style="background: #ECE5F4">Sweep</span><span class="meta">Marta Kowalski · 12 Sep</span></div>'
            '<h2 class="ui ttl" id="qp-it-' + v + '">Re-run only the failed checks</h2>'
            '<p class="sum">When one check fails on a big PR, I have to re-run the whole sweep. A partial re-run from the PR page would save 10 minutes each time.</p>'
            '<div class="row" style="gap: 8px; flex-wrap: wrap"><span class="vbtn">' + VOTE_IC + '48 · Voted</span><span class="chip chip-on">Following</span>' + chip + '</div>'
            '<div class="steps"><span class="step"><b style="background: #00A56B"></b>Proposed</span><span class="stepline"></span><span class="step"><b style="background: #00A56B"></b>Under review</span><span class="stepline"></span><span class="step"><b style="background: #35307E"></b>Planned · 2 Oct</span><span class="stepline"></span><span class="step" style="color: #79757F"><b style="background: #CAC4CF"></b>Delivered</span></div>'
            '<div class="note"><span class="tile ne" style="flex: none"><i></i>Platform team</span><span>Planned for 4.8: partial re-run from the PR page. Design review on 5 Nov.</span></div>'
            + QA[v]('d') + '</section>')

def frame_body(v):
    return (f'<sc-if value="{{{{is{v}}}}}" hint-placeholder-val="{{{{{"true" if v == "A" else "false"}}}}}"><div class="qp-two">'
            '<div class="stack"><span class="qp-lab">What’s new · release (layout D)</span>' + release(v) + '</div>'
            '<div class="stack"><span class="qp-lab">Ideas · idea detail (layout E)</span>' + idea(v) + '</div></div></sc-if>')

CSS_LAB = """
.tile{display:inline-flex;align-items:center;gap:6px;height:24px;padding:0 8px;border-radius:4px;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:600;white-space:nowrap}
.tile i{width:8px;height:8px;border-radius:2px;background:currentColor}
.ok{background:#C3F4DC;color:#00391E}.wn{background:#FFDEA0;color:#261900}.in{background:#E3DFFF;color:#14085E}.ne{background:#ECE5F4;color:#1C1B1E}
.ttab{display:flex;flex-direction:column;align-items:flex-start;gap:4px;padding:12px 14px;border-radius:12px;border:1px solid #CAC4CF;background:#FDF8FD;text-align:left;cursor:pointer;min-width:0}
.ttab:hover{background:rgba(53,48,126,.06)}
.ttab-on{border-color:#35307E;box-shadow:inset 0 0 0 1px #35307E;background:#F2EBFA}
.cmp td,.cmp th{padding:10px 12px;font-size:13px;line-height:18px;vertical-align:top;border-top:1px solid #CAC4CF}
.cmp th{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:600;letter-spacing:.5px;text-transform:uppercase;color:#48454E;text-align:left;border-top:0}
.cmp tr.on td{background:#F2EBFA}
.row{display:flex;align-items:center;gap:12px}
.stack{display:flex;flex-direction:column;gap:12px;min-width:0}
.meta{font-size:12px;color:#48454E;white-space:nowrap}
.lnk{background:transparent;border:0;padding:0;color:#35307E;font-family:'Open Sans',system-ui,sans-serif;font-size:13px;font-weight:600}
.ttl{margin:0;font-size:20px;line-height:28px;font-weight:700;color:#1C1B1E}
.sum{margin:0;font-size:14px;line-height:20px;color:#48454E;max-width:72ch}
.ver{font-size:13px;color:#14085E;background:#E3DFFF;padding:2px 8px;border-radius:4px}
.foot{border-top:1px solid #CAC4CF;padding-top:12px}
.chgt{border:1px solid #CAC4CF;border-radius:8px;overflow:hidden}
.chgr{display:grid;grid-template-columns:72px 170px minmax(0,1fr);gap:12px;align-items:start;padding:8px 12px;font-size:13px;line-height:18px;border-top:1px solid #ECE5F4}
.chgr:first-child{border-top:0}
.thumb{width:40px;justify-content:center;padding:0}
.vbtn{display:inline-flex;align-items:center;gap:6px;height:40px;padding:0 14px;border-radius:16px;background:#E3DFFF;color:#191836;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:14px;font-weight:700}
.steps{display:flex;flex-wrap:wrap;align-items:center;gap:6px 0;padding:10px 12px;border-radius:8px;background:#F2EBFA}
.step{display:flex;align-items:center;gap:6px;font-size:12px;white-space:nowrap}
.step b{width:10px;height:10px;border-radius:50%;flex:none}
.stepline{flex:1;height:2px;background:#CAC4CF;min-width:10px;margin:0 6px}
.note{display:flex;gap:8px;align-items:flex-start;padding:8px 12px;border-radius:8px;background:#F2EBFA;font-size:13px;line-height:18px}
.qp-item{display:flex;flex-direction:column;gap:12px;padding:20px 24px}
.qp-two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:24px;align-items:start}
.qp-lab{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:700;letter-spacing:.4px;color:#48454E;text-transform:uppercase}
.qp-ppl{display:inline-flex;flex:none;padding-left:4px}.qp-ppl .av{width:24px;height:24px;font-size:9px;letter-spacing:-.2px;margin-left:-4px;box-shadow:0 0 0 2px #F7F2FA}
/* A · summary bar */
.qp-bar{width:100%;min-height:48px;box-sizing:border-box;display:flex;align-items:center;gap:10px;flex-wrap:nowrap;padding:8px 14px 8px 10px;border:1px solid #CAC4CF;border-radius:12px;background:#F7F2FA;color:#1C1B1E;text-align:left;font:inherit}
.qp-bar:hover{background:#EFE7F7}
.qp-bar[aria-expanded="true"]{border-color:#35307E;background:#F2EBFA;box-shadow:inset 0 0 0 1px #35307E}
.qp-bar .chev,.qp-more .chev{flex:none;color:#35307E;transition:transform .2s cubic-bezier(.2,0,0,1)}
.qp-bar[aria-expanded="true"] .chev,.qp-more[aria-expanded="true"] .chev{transform:rotate(180deg)}
.qp-t{font-size:14px;font-weight:700}
.qp-bar>*{flex:none}.qp-bar>.meta{flex:0 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis}
.qp-act{margin-left:auto;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:13px;font-weight:600;color:#35307E}
.qp-bar + .qa{margin-top:-4px}
/* C · section heading */
.qp-sec{border-top:1px solid #CAC4CF;padding-top:4px}
.qp-h{margin:0;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.qp-h button{min-height:44px;display:inline-flex;align-items:center;gap:6px;padding:0 10px 0 2px;border:0;border-radius:8px;background:transparent;color:#1C1B1E;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:16px;font-weight:700}
.qp-h button:hover{background:rgba(53,48,126,.06)}
.qp-h .chev-r{color:#35307E;transition:transform .2s cubic-bezier(.2,0,0,1)}
.qp-h button[aria-expanded="true"] .chev-r{transform:rotate(90deg)}
.qp-hmeta{margin-left:auto;display:inline-flex;align-items:center;gap:8px;flex-wrap:wrap}
/* D · preview first */
.qp-prev .qa-q:first-child{border-top:1px solid #CAC4CF}
.qp-more{align-self:flex-start;min-height:40px;display:inline-flex;align-items:center;gap:4px;margin:4px 0;padding:0 10px 0 12px;border:0;border-radius:8px;background:transparent;color:#35307E;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:14px;font-weight:600}
.qp-more:hover{background:rgba(53,48,126,.06)}
@media (prefers-reduced-motion: reduce){.qp-bar .chev,.qp-more .chev,.qp-h .chev-r{transition:none}}
@container win (max-width: 1199px){.qp-two{grid-template-columns:minmax(0,1fr)!important}}
@container win (max-width: 599px){.qp-bar{flex-wrap:wrap!important}.qp-item{padding:16px!important}.chgr{grid-template-columns:auto minmax(0,1fr)!important}.chgr>span:last-child{grid-column:1 / -1}.qp-hmeta{margin-left:0}}
"""

BODY = '''<div style="width: 1440px; min-height: 2000px; box-sizing: border-box; background: #FDF8FD; color: #1C1B1E; display: flex; flex-direction: column">
  <div style="padding: 20px 32px 12px; display: flex; flex-direction: column; gap: 12px">
    <div style="display: flex; align-items: center; gap: 16px">
      <h1 class="ui" style="margin: 0; font-size: 24px; line-height: 32px; font-weight: 700; white-space: nowrap">Q&amp;A pattern lab</h1>
      <span style="font-size: 14px; color: #48454E">One way to open and close questions, and one set of Q&amp;A metadata, for every feature. Each proposal is applied to a What’s new release and to an idea, with the same content; only the control and the summary change. Open and close them, with the mouse and with Tab, Enter and Space.</span>
    </div>
    <div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px">
      <sc-for list="{{tabs}}" as="t" hint-placeholder-count="4">
        <button type="button" class="ttab {{t.cls}}" aria-pressed="{{t.on}}" onClick="{{t.pick}}"><span class="row" style="gap: 8px"><span style="width: 24px; height: 24px; border-radius: 999px; background: {{t.numBg}}; color: {{t.numFg}}; font-family: Manrope, 'BNPP Type', 'Segoe UI', system-ui, sans-serif; font-size: 12px; font-weight: 700; display: inline-flex; align-items: center; justify-content: center">{{t.k}}</span><span class="ui" style="font-size: 14px; font-weight: 600">{{t.name}}</span></span><span style="font-size: 12px; line-height: 16px; color: #48454E">{{t.sub}}</span><sc-if value="{{t.rec}}" hint-placeholder-val="{{false}}"><span class="tile ok"><i></i>Adopted</span></sc-if><sc-if value="{{t.cur}}" hint-placeholder-val="{{false}}"><span class="tile ne"><i></i>Today</span></sc-if></button>
      </sc-for>
    </div>
    <div class="row" style="gap: 12px; flex-wrap: wrap">SIMBAR<span class="row" style="gap: 8px"><button type="button" class="chip" onClick="{{openAll}}">Open both</button><button type="button" class="chip" onClick="{{closeAll}}">Close both</button></span></div>
  </div>

  <div style="margin: 0 32px; border-radius: 12px; overflow: hidden; border: 1px solid #CAC4CF">
  SIMOPEN
  <div style="position: relative; width: 100%; height: 100%; display: flex; flex-direction: column; background: #FDF8FD; overflow: hidden">
    HEADER
    <div style="flex: 1; display: flex; min-height: 0">
      RAIL
      <main style="position: relative; flex: 1; min-width: 0; padding: 20px 32px 24px; box-sizing: border-box; display: flex; flex-direction: column; gap: 16px; overflow: auto">
        FRAMES
      </main>
    </div>
    NAVBAR
  </div>
  SIMCLOSE
  </div>

  <div style="padding: 20px 32px 32px; display: grid; grid-template-columns: minmax(0, 1fr) 420px; gap: 24px; align-items: start">
    <div class="card" style="padding: 0; overflow: hidden">
      <table class="cmp" style="width: 100%; border-collapse: collapse">
        <thead><tr><th style="width: 30px"></th><th style="width: 120px">Proposal</th><th>The control</th><th>Closed, you see</th><th>Open, you see</th><th>Close with · focus</th><th>Trade-off</th></tr></thead>
        <tbody>
          <sc-for list="{{rows}}" as="r" hint-placeholder-count="4">
            <tr class="{{r.cls}}"><td><span class="ui" style="font-weight: 700">{{r.k}}</span></td><td><span class="ui" style="font-weight: 600">{{r.name}}</span></td><td>{{r.control}}</td><td>{{r.closed}}</td><td>{{r.open}}</td><td>{{r.close}}</td><td style="color: #48454E">{{r.trade}}</td></tr>
          </sc-for>
        </tbody>
      </table>
    </div>
    <div style="display: flex; flex-direction: column; gap: 16px">
      <div class="card" style="display: flex; flex-direction: column; gap: 8px">
        <div class="row" style="justify-content: space-between"><span class="h2">Adopted · A + Show more</span><span class="tile ok"><i></i>Summary bar</span></div>
        <div style="font-size: 13px; line-height: 18px; color: #48454E">One full-width bar, always at the end of the item, is both the summary and the only control, in What’s new and in Ideas alike. Closed, it already answers “is there anything for me?” (count, who asked, answered and waiting, last answer); open, it stays where it was, above the thread, and closes it again. Applied to the live Community prototype and to both layout labs.</div>
        <div style="font-size: 13px; line-height: 18px; color: #48454E"><b style="color: #1C1B1E">Show more.</b> The bar is the header of one expansion panel; open, the panel shows three questions, newest first. The link “Show 3 more questions” adds the next three under them, says where you are (“3 of 7 shown”), moves the focus to the first new question and announces it. Closing the panel goes back to the first three.</div>
      </div>
      <div class="ocard" style="display: flex; flex-direction: column; gap: 6px; font-size: 13px; line-height: 18px; color: #48454E">
        <span class="ui" style="font-size: 14px; font-weight: 700; color: #1C1B1E">One set of Q&amp;A metadata, everywhere</span>
        <span><b style="color: #1C1B1E">Summary</b> (item level): Questions · count, up to three askers, “n answered” and “n waiting” StatusChips (only when not zero), “Last answer 2 days ago” (or “No answer yet”).</span>
        <span><b style="color: #1C1B1E">Compact summary</b> (lists, admin, notifications): “3 questions · 1 waiting”, the same words in the Ideas list rows, the Administration triage and the release list.</span>
        <span><b style="color: #1C1B1E">Question</b>: asker, date, question, Waiting for an answer. <b style="color: #1C1B1E">Answer</b>: Answered, who, role chip (Platform team, Champion, Author), date, text.</span>
        <span>Every control: `aria-expanded` + `aria-controls`, state shown by the chevron and the selected look (never by the label alone), Enter and Space, focus kept on the control.</span>
      </div>
    </div>
  </div>
</div>'''

LOGIC = r'''
class Component extends DCLogic {
  constructor(props) { super(props); this.simHostId = 'sim-host-qa'; this.simDefault = 1374; this.state = { v: 'A', simW: null, simAvail: 0, qaOpen: { r1: false, i1: false } }; }
/*SIMJS*/
/*QAJS*/
  componentDidMount() { var self = this; this.simSync(); if (typeof window !== 'undefined') window.addEventListener('resize', function () { self.simSync(); }); }
  componentDidUpdate() { this.simSync(); this.qaFocusSync(); }
  renderVals() {
    var s = this.state, self = this, sim = this.simVals(), QA = this.qaSeed(), as = { who: 'Aurélien Heux', role: 'Platform team' };
    var set = function (o) { return function (e) { if (e && e.preventDefault) e.preventDefault(); self.setState(o); }; };
    var defs = [
      { k: 'A', name: 'Summary bar', sub: 'One bar at the end of the item; Show more by three.', control: 'A full-width bar (48 px) at the end of the item: chevron, Questions, count, askers, answered and waiting, last answer, Show / Hide.', closed: 'The whole summary', open: 'The same bar, selected, with the thread under it', close: 'The same bar · focus stays on it', trade: 'Heavier at the end of a short item; one more surface.', rec: true, adopted: true },
      { k: 'B', name: 'Action chip', sub: 'A chip in the item’s action row.', control: 'A “Questions · n” chip in the action row (release) or next to Vote and Follow (idea); the thread has its own header with Hide questions.', closed: 'Count and a waiting dot', open: 'Selected chip; thread header with count, answered, waiting', close: 'The chip, or Hide questions · focus back on the chip', trade: 'Two controls; the chip sits far from the thread on long items.' },
      { k: 'C', name: 'Section heading', sub: 'The Questions heading is the button.', control: 'The h3 “Questions” is a disclosure button (chevron, count); answered, waiting and last answer on the same line.', closed: 'Heading, chips and last answer', open: 'Chevron turned, thread under the heading', close: 'The heading · focus stays on it', trade: 'Lighter, but a smaller target and easy to miss when closed.' },
      { k: 'D', name: 'Preview first', sub: 'The latest answer is always shown.', control: 'Header with the metadata, the latest answered question, “Show all 3 questions · 1 waiting”, the ask field.', closed: 'Metadata, one answered question, ask field', open: 'Every question; Show fewer', close: 'Show fewer · focus stays on it', trade: 'Tallest closed state; the preview repeats on every item.' }
    ];
    var tabs = defs.map(function (d) { var on = s.v === d.k; return { k: d.k, name: d.name, sub: d.sub, on: on, cls: on ? 'ttab-on' : '', numBg: on ? '#35307E' : '#E3DFFF', numFg: on ? '#FFFFFF' : '#14085E', rec: !!d.rec, cur: !!d.cur, pick: set({ v: d.k }) }; });
    var rows = defs.map(function (d) { return Object.assign({}, d, { cls: s.v === d.k ? 'on' : '' }); });
    var deco = function (q) { return Object.assign(q, { qaAction: q.qaOpen ? 'Hide' : 'Show', qaMoreAction: q.qaOpen ? 'Show fewer' : q.qaMoreLabel }); };
    var r = deco(this.qaVals('r1', QA.r1, 'Ask about this release…', as, false));
    var d = deco(this.qaVals('i1', QA.i1, 'Ask the author or the platform team…', as, false));
    return Object.assign(sim, { tabs: tabs, rows: rows, r: r, d: d,
      openAll: set({ qaOpen: { r1: true, i1: true } }), closeAll: set({ qaOpen: { r1: false, i1: false } }),
      isA: s.v === 'A', isB: s.v === 'B', isC: s.v === 'C', isD: s.v === 'D' });
  }
}
'''

frames = ''.join(frame_body(v) for v in 'ABCD')
body = (BODY.replace('SIMBAR', S.sim_bar()).replace('SIMOPEN', S.sim_open('sim-host-qa', 'height: 1200px')).replace('SIMCLOSE', S.SIM_CLOSE)
        .replace('HEADER', S.header(False, 'Community', 'Questions on releases and ideas')).replace('RAIL', N.rail(N.LIGHT, 'new'))
        .replace('NAVBAR', S.navbar(N.LIGHT, 'new')).replace('FRAMES', frames))
logic = LOGIC.replace('/*SIMJS*/', S.SIM_JS).replace('/*QAJS*/', S.QA_JS)
out = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>Q&amp;A pattern lab, one open/close mechanic and one set of metadata</title>\n<script src="./support.js"></script>\n</head>\n<body>\n<x-dc>\n<helmet>\n'
       '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&amp;family=Open+Sans:wght@400;600;700&amp;display=swap">\n'
       '<style>\n' + S.CSS + '\n' + S.SIM_CSS + '\n' + S.QA_CSS + CSS_LAB + '</style>\n</helmet>\n' + body + '\n</x-dc>\n'
       '<script type="text/x-dc" data-dc-script data-props=\'{"$preview":{"width":1440,"height":2000}}\'>' + logic + '</script>\n</body>\n</html>\n')
for t in ['sc-if', 'sc-for']:
    assert len(re.findall(rf'<{t}\b', out)) == len(re.findall(rf'</{t}>', out)), t
assert 'SIMBAR' not in out and 'FRAMES' not in out
open(dst, 'w', encoding='utf-8').write(out); print(len(out))
