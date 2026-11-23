"""Agent run component boards (usage, panel version, page version, output viewer) for the design-system canvas.
Writes the four AgentRun*.dc.html / AgentOutput.dc.html boards and their entries in canvases/design-system/canvas.json.
Run from anywhere: python3 tooling/canvas/agent_run_build.py"""
import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "canvases", "design-system")

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&amp;family=Open+Sans:wght@400;600;700&amp;family=JetBrains+Mono:wght@400;500;600&amp;display=swap">
<style>
body{margin:0;font-family:'Open Sans',system-ui,sans-serif;color:#1C1B1E}
button{font-family:inherit;cursor:pointer}
a{color:#39235F}a:hover{color:#14085E}
:focus-visible{outline:2px solid #39235F;outline-offset:2px}
.ui{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif}
.k{font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:500;letter-spacing:.08em;text-transform:uppercase;color:#48454E}
.h1{margin:0;font-family:Manrope,'BNPP Type',sans-serif;font-size:45px;line-height:52px;font-weight:700;letter-spacing:-0.01em}
.lead{margin:0;max-width:980px;font-size:16px;line-height:24px;color:#48454E}
.pnl{display:flex;flex-direction:column;gap:14px;padding:20px;border-radius:16px;background:#FAF4FF;min-width:0}
.pt{font-family:Manrope,'BNPP Type',sans-serif;font-size:15px;font-weight:700}
.mt{font-size:13px;line-height:19px;color:#48454E}
.mono{font-family:'JetBrains Mono',monospace;font-size:12px}
.g2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}
.g3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}
ul.r{margin:0;padding-left:18px;display:flex;flex-direction:column;gap:6px;font-size:14px;line-height:20px}
table.tk{border-collapse:collapse;width:100%;font-size:13px;line-height:18px}
table.tk th{text-align:left;font-family:Manrope,'BNPP Type',sans-serif;font-size:12px;font-weight:700;color:#48454E;padding:6px 8px;border-bottom:1px solid #CAC4CF}
table.tk td{padding:7px 8px;border-bottom:1px solid #E6E0EC;vertical-align:top}
.do,.dont{border-radius:12px;padding:14px 16px;display:flex;flex-direction:column;gap:8px;font-size:14px;line-height:20px}
.do{background:#FFFFFF;box-shadow:inset 0 4px 0 #0B5314}.dont{background:#FFFFFF;box-shadow:inset 0 4px 0 #93000A}
.do b,.dont b{font-family:Manrope,'BNPP Type',sans-serif}
.chip{height:32px;padding:0 12px;border-radius:8px;border:1px solid #79757F;background:transparent;color:#1C1B1E;font-family:Manrope,'BNPP Type',sans-serif;font-size:13px;font-weight:600;display:inline-flex;align-items:center;gap:6px;white-space:nowrap}
.chip:hover{background:rgba(57,35,95,.06)}
.chip-on{background:#DED7EB;border-color:#DED7EB;color:#1D1A28}
.btn{height:32px;padding:0 14px;border:0;border-radius:12px;font-family:Manrope,'BNPP Type',sans-serif;font-size:13px;font-weight:600;display:inline-flex;align-items:center;gap:6px;white-space:nowrap;text-decoration:none}
.f{background:#39235F;color:#FFFFFF}.f:hover{background:#4A3470}
.o{background:transparent;border:1px solid #79757F;color:#39235F}.o:hover{background:rgba(57,35,95,.06)}
.x{background:transparent;color:#39235F;padding:0 10px}.x:hover{background:rgba(57,35,95,.06)}
/* run status chip */
.st{display:inline-flex;align-items:center;gap:6px;height:24px;padding:0 8px 0 4px;border-radius:4px;font-family:Manrope,'BNPP Type',sans-serif;font-size:12px;font-weight:700;white-space:nowrap}
.st .g{width:18px;height:18px;border-radius:3px;display:inline-flex;align-items:center;justify-content:center;font-size:11px}
.st-q{background:#ECE5F4;color:#1C1B1E}.st-q .g{background:#48454E;color:#ECE5F4}
.st-run{background:#9CF1F0;color:#002020}.st-run .g{background:#004F50;color:#9CF1F0}
.st-wait{background:#E3DFFF;color:#14085E;box-shadow:inset 0 0 0 2px #39235F}.st-wait .g{background:#39235F;color:#E3DFFF}
.st-other{background:#E3DFFF;color:#14085E}.st-other .g{background:#39235F;color:#E3DFFF}
.st-chg{background:#FFDEA0;color:#261900}.st-chg .g{background:#5F4100;color:#FFDEA0}
.st-done{background:#ACF4A2;color:#002203}.st-done .g{background:#0B5314;color:#ACF4A2}
.st-fail{background:#FFDAD6;color:#410002}.st-fail .g{background:#93000A;color:#FFDAD6}
.st-cnl{background:transparent;color:#48454E;box-shadow:inset 0 0 0 1px #79757F}.st-cnl .g{color:#48454E}
.dots{display:inline-flex;gap:3px;vertical-align:middle}
.dots i{width:4px;height:4px;border-radius:2px;background:#004F50;animation:dp 1s infinite ease-in-out}
.dots i:nth-child(2){animation-delay:.15s}.dots i:nth-child(3){animation-delay:.3s}
@keyframes dp{0%,80%,100%{opacity:.25}40%{opacity:1}}
@media (prefers-reduced-motion: reduce){.dots i{animation:none;opacity:.8}}
.ai{display:inline-flex;align-items:center;gap:4px;height:20px;padding:0 6px;border-radius:4px;background:#9CF1F0;color:#002020;font-family:Manrope,'BNPP Type',sans-serif;font-size:11px;font-weight:700;white-space:nowrap}
.mk{display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;border-radius:3px;font-weight:700;font-size:12px;flex:none}
.mk-added,.mk-ok{background:#0B5314;color:#ACF4A2}.mk-changed,.mk-warn{background:#5F4100;color:#FFDEA0}.mk-info{background:#48454E;color:#ECE5F4}.mk-err{background:#93000A;color:#FFDAD6}.mk-run{background:#004F50;color:#9CF1F0}
/* header indicator */
.ind{height:36px;padding:0 12px;border-radius:12px;border:0;display:inline-flex;align-items:center;gap:8px;font-family:Manrope,'BNPP Type',sans-serif;font-size:13px;font-weight:700;white-space:nowrap}
.ind-run{background:#9CF1F0;color:#002020}.ind-wait{background:#E3DFFF;color:#14085E;box-shadow:inset 0 0 0 2px #39235F}.ind-fail{background:#FFDAD6;color:#410002}
.band{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:12px 16px;border-radius:12px;background:#EDE4FF}
.sbox{height:40px;flex:1 1 220px;max-width:360px;border-radius:16px;background:#FFFFFF;display:flex;align-items:center;padding:0 14px;color:#48454E;font-size:14px}
/* panel parts */
.panel{background:#F8F1FF;border:1px solid #CAC4CF;border-radius:16px;display:flex;flex-direction:column;gap:12px;padding:12px;width:400px;box-sizing:border-box}
.strip{padding:10px 12px;border-radius:12px;background:#FFFFFF;border:1px solid #CAC4CF;display:flex;flex-direction:column;gap:6px}
.mrow{display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:13.5px;line-height:19px}
.mcard{background:#FFFFFF;border:1px solid #CAC4CF;border-radius:12px;padding:12px;display:flex;flex-direction:column;gap:8px}
.mcard-wait{box-shadow:inset 0 0 0 2px #39235F;border-color:#39235F}
.mu{align-self:flex-end;max-width:85%;background:#DED7EB;color:#1D1A28;border-radius:16px 16px 4px 16px;padding:8px 12px;font-size:14px;line-height:20px}
.gate{border-radius:12px;padding:12px;background:#E3DFFF;color:#14085E;box-shadow:inset 0 0 0 2px #39235F;display:flex;flex-direction:column;gap:8px;font-size:13.5px;line-height:19px}
.gate b{font-family:Manrope,'BNPP Type',sans-serif}
.gate-other{box-shadow:none}
/* page parts */
.scard{text-align:left;background:#FFFFFF;border:1px solid #CAC4CF;border-radius:12px;padding:12px;display:flex;flex-direction:column;gap:8px;min-width:0;box-sizing:border-box}
.scard-wait{box-shadow:inset 0 0 0 2px #39235F;border-color:#39235F}
.scard-sel{border-color:#39235F;box-shadow:inset 0 0 0 1px #39235F}
.sn{font-family:Manrope,'BNPP Type',sans-serif;font-size:12px;font-weight:700;color:#48454E;letter-spacing:.3px;text-transform:uppercase}
.sa{font-family:Manrope,'BNPP Type',sans-serif;font-size:15px;font-weight:700}
.adm{font-size:12px;color:#48454E;line-height:16px}
.bar{height:4px;border-radius:2px;background:#ECE5F4;overflow:hidden}
.bar i{display:block;height:4px;background:#004F50}
.bar-done i{background:#0B5314}.bar-fail i{background:#93000A}
.box{background:#FFFFFF;border:1px solid #CAC4CF;border-radius:12px;padding:14px 16px;display:flex;flex-direction:column;gap:10px;min-width:0}
.h3{margin:0;font-family:Manrope,'BNPP Type',sans-serif;font-size:16px;font-weight:700}
.steps{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:6px}
.steps li{display:flex;align-items:center;gap:10px;font-size:13.5px;line-height:19px}
.sm{width:20px;height:20px;border-radius:999px;display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;flex:none;box-sizing:border-box}
.sm-done{background:#0B5314;color:#ACF4A2}.sm-now{background:#9CF1F0;color:#002020;border:2px solid #004F50}.sm-todo{border:1.5px solid #79757F;color:#48454E}
.todo{color:#48454E}
.orow{display:flex;align-items:flex-start;gap:10px;font-size:13.5px;line-height:19px}
.orow small{display:block;color:#48454E;font-size:12px}
.log{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:4px;font-size:12.5px;line-height:18px}
.log time{font-weight:600;color:#48454E;margin-right:8px;font-variant-numeric:tabular-nums}
.tabs{display:flex;gap:4px;border-bottom:1px solid #CAC4CF;overflow-x:auto}
.tab{height:44px;padding:0 14px;border:0;background:transparent;font-family:Manrope,'BNPP Type',sans-serif;font-size:14px;font-weight:600;color:#48454E;border-bottom:3px solid transparent;display:inline-flex;align-items:center;gap:6px;white-space:nowrap}
.tab:hover{background:rgba(57,35,95,.06)}
.tab-on{color:#39235F;border-bottom-color:#39235F}
.n{font-size:11px;padding:1px 6px;border-radius:6px;background:#F2EBFA;color:#48454E}
.anno{display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;border-radius:999px;background:#39235F;color:#FFFFFF;font-family:Manrope,sans-serif;font-size:11px;font-weight:700;flex:none}
.diff{margin:0;border-radius:8px;background:#FFFFFF;border:1px solid #CAC4CF;overflow:hidden;font-family:'Open Sans',sans-serif;font-weight:600;font-size:12.5px;line-height:20px}
.diff div{padding:0 12px;white-space:pre}
.diff .a{background:#E4F8DF}.diff .d{background:#FFEDEA;text-decoration:line-through;text-decoration-color:rgba(65,0,2,.4)}.diff .h{background:#F2EBFA;color:#48454E}
.trace{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;border:1px solid #CAC4CF;border-radius:8px;background:#FFFFFF;overflow:hidden}
.trace li{display:grid;grid-template-columns:76px 22px minmax(0,1fr) 70px;gap:8px;align-items:center;padding:6px 12px;border-top:1px solid #ECE5F4;font-size:12.5px;line-height:18px}
.trace li:first-child{border-top:0}
.trace code{font-family:'Open Sans',sans-serif;font-weight:600}
.trace .d{color:#48454E;text-align:right;font-variant-numeric:tabular-nums}
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
</style>
</helmet>
"""

def board(name, title, width, body, js="class Component extends DCLogic {\n  renderVals() { return {}; }\n}", height=2000):
    html = HEAD.replace("{title}", title) + body + "\n</x-dc>\n<script type=\"text/x-dc\" data-dc-script data-props='{\"$preview\":{\"width\":%d,\"height\":%d}}'>\n%s\n</script>\n</body>\n</html>\n" % (width, height, js)
    open(os.path.join(OUT, name), "w").write(html)
    return name

ROOT = '<div style="width: {w}px; min-height: {h}px; box-sizing: border-box; background: #FDF8FD; color: #1C1B1E; display: flex; flex-direction: column; gap: 28px; padding: 56px 64px">'

def st(cls, glyph, label, dots=False):
    d = '<span class="dots" aria-hidden="true"><i></i><i></i><i></i></span>' if dots else ''
    return f'<span class="st {cls}"><span class="g" aria-hidden="true">{glyph}</span>{label}</span>{d}'

STATES = [
    ("st-q", "·", "Queued", "Created, waits for the previous agent or a free slot.", "neutral: surface-container-highest + on-surface-variant tile"),
    ("st-run", "✦", "Running", "Working on its steps. Shows the working dots and n / m steps.", "ai-container #9CF1F0 + ai #004F50 tile · the only teal state"),
    ("st-wait", "!", "Waiting for you", "At a review gate whose approver is the person looking.", "primary-container #E3DFFF + 2 px primary border (the review gate)"),
    ("st-other", "!", "Waiting for Léa Martin", "At a review gate owned by someone else: no buttons.", "primary-container, no border"),
    ("st-chg", "↩", "Changes requested", "The approver sent the output back; the previous agent runs again.", "warning-container #FFDEA0 + warning tile"),
    ("st-done", "✓", "Done", "Finished; its output is final for this run.", "success-container #ACF4A2 + success tile"),
    ("st-fail", "✕", "Failed", "Stopped on an error; Retry and View log are offered.", "error-container #FFDAD6 + error tile"),
    ("st-cnl", "–", "Cancelled", "Stopped by a person, or superseded by a newer run.", "transparent, 1 px outline"),
]

# ---------------------------------------------------------------- 1. guidance
def guidance():
    rows = "".join(f'<tr><td>{st(c, g, l, c == "st-run")}</td><td>{m}</td><td class="mt">{t}</td></tr>' for c, g, l, m, t in STATES)
    body = ROOT.format(w=1560, h=2140) + f"""
  <div style="display: flex; flex-direction: column; gap: 8px">
    <div class="k">AIToolbox · Components · Agents · decided 2026-11-23</div>
    <h1 class="h1">Agent run</h1>
    <p class="lead">An agent run is one agent working on one object (a change, a request) through its steps, up to an output and, when the output must take effect, a review gate. The same run is shown in two places: the <b>assistant panel</b>, where a person talks and acts, and the <b>object page</b>, which is the record everyone shares. The state, the steps, the output and the gate are the same data in both; only the depth differs. Example on these boards: the four TOGAF agents of a change (analysis, draft, review, implementation).</p>
  </div>
  <div class="g3">
    <div class="pnl"><span class="pt">One run, two views</span><ul class="r">
      <li><b>Panel</b>: milestones of the runs this conversation started or that wait for you. Act at the gate without leaving the chat.</li>
      <li><b>Page</b>: every run of the object in process order, all steps, the activity and the output. Link to it, review there, keep the history.</li>
      <li><b>Header indicator</b>: from anywhere, what runs and what waits for you.</li>
      <li><b>Output viewer</b>: the full output of one run, opened from either view; it has its own address.</li></ul></div>
    <div class="pnl"><span class="pt">Use the panel version when</span><ul class="r">
      <li>the person started the agents from the conversation, or asked about them there;</li>
      <li>the next thing they need is a decision (a gate) or a short answer;</li>
      <li>a run reaches a milestone: started, finished, waiting, failed. One line each, never one per step.</li></ul>
      <span class="pt">Use the page version when</span><ul class="r">
      <li>several people follow or review the object;</li>
      <li>you need every step, the activity, earlier runs or the output in full;</li>
      <li>the run was started by a signal, a schedule or another agent, not by a conversation.</li></ul></div>
    <div class="pnl"><span class="pt">Rules</span><ul class="r">
      <li>An agent output that takes effect passes a person first (PRI-01): the run stops at a gate, nothing is applied before.</li>
      <li>Only the named approver sees the gate buttons; everyone else sees “Waiting for &lt;name&gt;”.</li>
      <li>Teal means an agent is working, nothing else. Waiting for you is violet with a 2 px border, the review gate of the notation.</li>
      <li>A state is a word and a glyph, never a colour alone.</li>
      <li>A new run never overwrites an old one: run 2 is listed after run 1, which shows “Cancelled · superseded”.</li></ul></div>
  </div>
  <div class="pnl"><span class="pt">Run status · eight states, one chip</span>
    <table class="tk"><tr><th style="width: 260px">Chip</th><th>Means</th><th>Colour roles</th></tr>{rows}</table>
    <span class="mt">Order of attention when several runs are summed up (header, strip): Waiting for you → Failed → Changes requested → Running → Queued → Done.</span></div>
  <div class="g2">
    <div class="pnl"><span class="pt">Anatomy</span>
      <table class="tk"><tr><th>Part</th><th>Panel</th><th>Page</th></tr>
      <tr><td>Run status chip</td><td>strip, milestone rows</td><td>stage card, detail, viewer header</td></tr>
      <tr><td>Header indicator</td><td colspan="2">header, right of the search: count and the most urgent state; hidden when nothing runs or waits</td></tr>
      <tr><td>Run strip</td><td>pinned at the top of the conversation: current agent, state, progress, trail of the steps, Open</td><td>—</td></tr>
      <tr><td>Milestone row</td><td>started, finished (View output), waiting (gate), failed (Retry · View log)</td><td>—</td></tr>
      <tr><td>Stage track and card</td><td>—</td><td>one card per agent in process order: step number, agent, phase, state, progress, next</td></tr>
      <tr><td>Run detail</td><td>—</td><td>steps, gate, output summary, activity</td></tr>
      <tr><td>Review gate</td><td>in the milestone row</td><td>in the run detail and the viewer</td></tr>
      <tr><td>Output summary</td><td>in the finished row: title, one-line summary, View output</td><td>in the run detail: title, summary, up to 6 rows</td></tr>
      <tr><td>Output viewer</td><td colspan="2">side sheet from the panel, tab of the object page, own address: Summary, Changes, Views, Checks, Log, Files</td></tr></table></div>
    <div style="display: flex; flex-direction: column; gap: 16px; min-width: 0">
      <div class="do"><b>Do</b><span>Post one line per milestone; let the steps tick in the strip and on the page.</span><span>Name the output by what it is: Impact analysis, Draft pull request #48, Review report.</span><span>Write gates as an action on the object: Confirm the scope · Approve the change.</span><span>Link every milestone to the page (Open in change) and every output to the viewer.</span></div>
      <div class="dont"><b>Don’t</b><span>Stream every step or tool call into the conversation: it buries the gate.</span><span>Show Approve to someone who is not the approver, or approve on someone’s behalf.</span><span>Colour a run teal once it stops: teal is for working only.</span><span>Move focus or open the viewer by itself when a run finishes.</span></div>
      <div class="pnl"><span class="pt">Accessibility</span><ul class="r">
        <li>Milestone rows sit in the conversation’s <span class="mono">aria-live="polite"</span> region; step ticks are not announced.</li>
        <li>The strip is <span class="mono">role="status"</span>; the gate is a group named by its question.</li>
        <li>Working dots are <span class="mono">aria-hidden</span> and stop with <span class="mono">prefers-reduced-motion</span>; the word Running stays.</li>
        <li>Stage cards are buttons with <span class="mono">aria-pressed</span> for the selected run; tabs of the viewer are a tablist.</li></ul></div>
    </div>
  </div>
</div>"""
    return board("AgentRun.dc.html", "Agent run · usage", 1560, body, height=2140)

# ---------------------------------------------------------------- 2. panel
def panel():
    body = ROOT.format(w=1560, h=1960) + f"""
  <div style="display: flex; flex-direction: column; gap: 8px">
    <div class="k">Agent run · in the assistant panel</div>
    <h1 class="h1">Panel version</h1>
    <p class="lead">For the person in the conversation. A pinned strip says what runs now; the conversation gets one row per milestone; the gate is answered in place. Everything links to the page for the full record. Pick a moment to see the panel at that point of the run.</p>
  </div>
  <div style="display: grid; grid-template-columns: 400px minmax(0, 1fr); gap: 32px; align-items: start">
    <div style="display: flex; flex-direction: column; gap: 10px">
      <div style="display: flex; gap: 6px; flex-wrap: wrap" role="group" aria-label="Moment of the run"><sc-for list="{{{{moments}}}}" as="m" hint-placeholder-count="5"><button type="button" class="chip {{{{m.cls}}}}" aria-pressed="{{{{m.on}}}}" onClick="{{{{m.pick}}}}">{{{{m.label}}}}</button></sc-for></div>
      <aside class="panel" aria-label="Assistant">
        <div class="mrow" style="padding: 2px 4px"><b class="ui" style="font-size: 15px">✦ Assistant</b><span class="mt">CHG-14</span></div>
        <div class="strip" role="status">
          <span class="mrow"><span class="anno" aria-hidden="true">1</span><span class="st {{{{s.cls}}}}"><span class="g" aria-hidden="true">{{{{s.glyph}}}}</span>{{{{s.label}}}}</span><sc-if value="{{{{s.dots}}}}" hint-placeholder-val="{{{{true}}}}"><span class="dots" aria-hidden="true"><i></i><i></i><i></i></span></sc-if><b class="ui">✦ {{{{s.agent}}}}</b><span class="mt">{{{{s.progress}}}}</span></span>
          <span class="mrow" style="justify-content: space-between"><span class="mt">{{{{s.trail}}}}</span><a class="btn x" href="#chg-14">Open in change</a></span>
        </div>
        <div class="mu">Assess what self-service environment reservation changes, and take it to the board.</div>
        <div class="mcard"><span class="mrow"><span class="anno" aria-hidden="true">2</span><span class="mk mk-info" aria-hidden="true">✦</span><span><b class="ui">✦ Analysis agent</b> started · Phase B</span></span></div>
        <sc-for list="{{{{rows}}}}" as="r" hint-placeholder-count="2">
          <div class="mcard {{{{r.cardCls}}}}">
            <span class="mrow"><span class="anno" aria-hidden="true">{{{{r.anno}}}}</span><span class="mk {{{{r.mkCls}}}}" aria-hidden="true">{{{{r.mk}}}}</span><span><b class="ui">✦ {{{{r.agent}}}}</b> {{{{r.text}}}}</span></span>
            <sc-if value="{{{{r.hasOut}}}}" hint-placeholder-val="{{{{false}}}}"><span class="mt" style="padding-left: 56px">{{{{r.outLine}}}}</span></sc-if>
            <sc-if value="{{{{r.gate}}}}" hint-placeholder-val="{{{{false}}}}"><div class="gate" role="group" aria-label="{{{{r.gateQ}}}}"><b>Waiting for you · {{{{r.gateQ}}}}</b><span style="display: flex; gap: 8px; flex-wrap: wrap"><button type="button" class="btn f">{{{{r.ok}}}}</button><sc-if value="{{{{r.reject}}}}" hint-placeholder-val="{{{{false}}}}"><button type="button" class="btn o">Request changes</button></sc-if><a class="btn x" href="#viewer">View output</a></span></div></sc-if>
            <sc-if value="{{{{r.fail}}}}" hint-placeholder-val="{{{{false}}}}"><span style="display: flex; gap: 8px; flex-wrap: wrap"><button type="button" class="btn f">Retry</button><a class="btn x" href="#log">View log</a></span></sc-if>
            <sc-if value="{{{{r.links}}}}" hint-placeholder-val="{{{{true}}}}"><span class="mrow" style="justify-content: flex-end"><sc-if value="{{{{r.hasOut}}}}" hint-placeholder-val="{{{{false}}}}"><a class="btn x" href="#viewer">View output</a></sc-if><a class="btn x" href="#chg-14">Open in change</a></span></sc-if>
          </div>
        </sc-for>
      </aside>
    </div>
    <div style="display: flex; flex-direction: column; gap: 24px; min-width: 0">
      <div class="pnl"><span class="pt">Parts</span>
        <table class="tk"><tr><th style="width: 34px"></th><th style="width: 200px">Part</th><th>Rules</th></tr>
        <tr><td><span class="anno">1</span></td><td>Run strip</td><td>Pinned under the panel header while a run of this conversation is running or waits; shows the most urgent run (order on the usage board). Chip, agent, n / m steps, the trail of all steps (✓ done, ✦ running, ! waiting), Open in change. Steps tick here, not in the conversation. Gone when every run is done; the last milestone stays in the conversation.</td></tr>
        <tr><td><span class="anno">2</span></td><td>Milestone row · started</td><td>Glyph tile, agent name in bold, “started · &lt;phase&gt;”. While it runs the row adds n / m steps; nothing else.</td></tr>
        <tr><td><span class="anno">3</span></td><td>Milestone row · finished</td><td>✓ tile, “finished · &lt;output title&gt;”, the one-line summary, View output (opens the viewer as a side sheet) and Open in change.</td></tr>
        <tr><td><span class="anno">4</span></td><td>Milestone row · waiting</td><td>Card with the 2 px primary border and the gate: question, primary action, Request changes when the gate allows it, View output. Answering adds your reply as a user message and removes the buttons; the row keeps “Approved by you · 10:11”.</td></tr>
        <tr><td><span class="anno">5</span></td><td>Milestone row · failed</td><td>✕ tile, what failed in one line, Retry (new run) and View log.</td></tr></table></div>
      <div class="pnl"><span class="pt">Sizes and tokens</span>
        <table class="tk"><tr><th>Element</th><th>Value</th></tr>
        <tr><td>Panel width</td><td class="mono">360–480, default 400 (assistant panel spec)</td></tr>
        <tr><td>Strip, row card</td><td class="mono">surface-container-lowest, 1 px outline-variant, radius 12, padding 10–12</td></tr>
        <tr><td>Waiting row</td><td class="mono">2 px primary inset border; gate block primary-container, on-primary-container text</td></tr>
        <tr><td>Glyph tile</td><td class="mono">20 × 20, radius 3, the state’s tile colours</td></tr>
        <tr><td>Buttons</td><td class="mono">32 high: filled for the gate’s action, outlined for Request changes, text for links</td></tr>
        <tr><td>Motion</td><td class="mono">working dots 1 s loop; rows appear with the conversation’s message motion; reduced motion: none</td></tr></table></div>
      <div class="g2" style="gap: 16px">
        <div class="do"><b>Do</b><span>Keep the conversation readable: five agents make about ten rows, not fifty.</span><span>Show the gate where the person is, with the output one click away.</span></div>
        <div class="dont"><b>Don’t</b><span>Put the full output in the conversation; summary and View output.</span><span>Show runs the person neither started nor must approve; those live on the page.</span></div>
      </div>
    </div>
  </div>
</div>"""
    js = """const M = [
  { id: 'run', label: 'Draft running', s: { cls: 'st-run', glyph: '✦', label: 'Running', dots: true, agent: 'Drafting agent', progress: '2 / 4 steps', trail: 'Analysis ✓ → Draft ✦ → Review → Implementation' },
    rows: [ { anno: '3', mk: '✓', mkCls: 'mk-ok', agent: 'Analysis agent', text: 'finished · Impact analysis', outLine: '4 elements · phases B and C', hasOut: true, links: true },
            { anno: '2', mk: '✦', mkCls: 'mk-run', agent: 'Drafting agent', text: 'started · Phases B–C · 2 / 4 steps', links: true } ] },
  { id: 'wait', label: 'Review waits for you', s: { cls: 'st-wait', glyph: '!', label: 'Waiting for you', dots: false, agent: 'Review agent', progress: '5 / 5 steps', trail: 'Analysis ✓ → Draft ✓ → Review ! → Implementation' },
    rows: [ { anno: '3', mk: '✓', mkCls: 'mk-ok', agent: 'Drafting agent', text: 'finished · Draft pull request #48', outLine: 'model +38 −2 lines · 2 new views', hasOut: true, links: true },
            { anno: '4', mk: '!', mkCls: 'mk-warn', agent: 'Review agent', text: 'is ready · Review report (14 passed · 1 warning). Approve the change?', cardCls: 'mcard-wait', gate: true, gateQ: 'Approve the change', ok: 'Approve', reject: true } ] },
  { id: 'fail', label: 'Implementation failed', s: { cls: 'st-fail', glyph: '✕', label: 'Failed', dots: false, agent: 'Implementation agent', progress: '2 / 4 steps', trail: 'Analysis ✓ → Draft ✓ → Review ✓ → Implementation ✕' },
    rows: [ { anno: '3', mk: '✓', mkCls: 'mk-ok', agent: 'Review agent', text: 'approved by you · 10:11', links: true },
            { anno: '5', mk: '✕', mkCls: 'mk-err', agent: 'Implementation agent', text: 'failed · Publish the Docs pages: the Docs service did not answer (timeout after 30 s).', fail: true } ] },
  { id: 'done', label: 'All done', s: { cls: 'st-done', glyph: '✓', label: 'Done', dots: false, agent: 'Implementation agent', progress: '4 / 4 steps', trail: 'Analysis ✓ → Draft ✓ → Review ✓ → Implementation ✓' },
    rows: [ { anno: '3', mk: '✓', mkCls: 'mk-ok', agent: 'Implementation agent', text: 'finished · Delivered', outLine: 'merged · 2 diagrams · Docs page · 3 Jira items', hasOut: true, links: true } ] }
];
const BASE = { cardCls: '', hasOut: false, outLine: '', gate: false, gateQ: '', ok: '', reject: false, fail: false, links: false };
class Component extends DCLogic {
  constructor(p) { super(p); this.state = { m: 'wait' }; }
  renderVals() {
    const cur = M.find(x => x.id === this.state.m);
    return {
      moments: M.map(x => ({ label: x.label, on: x.id === cur.id, cls: x.id === cur.id ? 'chip-on' : '', pick: () => this.setState({ m: x.id }) })),
      s: cur.s, rows: cur.rows.map(r => Object.assign({}, BASE, r))
    };
  }
}"""
    return board("AgentRunPanel.dc.html", "Agent run · panel version", 1560, body, js, height=1960)

# ---------------------------------------------------------------- 3. page
def page():
    def card(n, label, agent, adm, stc, extra="", pct=0, bar="", foot="", prog=""):
        return f'''<div class="scard {extra}"><span class="sn">{n} · {label}</span><span class="sa">✦ {agent}</span><span class="adm">{adm}</span><span style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap">{stc}<span class="mt" style="font-size: 12px">{prog}</span></span><span class="bar {bar}" aria-hidden="true"><i style="width: {pct}%"></i></span><span class="adm">{foot}</span></div>'''
    track = "".join([
        card(1, "Analysis", "Analysis agent", "Phase B · requirements and impact", st("st-done", "✓", "Done"), pct=100, bar="bar-done", foot="Impact analysis · scope confirmed by Léa Martin", prog="4 / 4 steps"),
        card(2, "Draft", "Drafting agent", "Phases B–C · target architecture", st("st-done", "✓", "Done"), pct=100, bar="bar-done", foot="Draft pull request #48 · run 2", prog="3 / 3 steps"),
        card(3, "Review", "Review agent", "Architecture board · compliance", st("st-wait", "!", "Waiting for you"), extra="scard-wait scard-sel", pct=100, foot="Waits for you: approve the change", prog="5 / 5 steps"),
        card(4, "Implementation", "Implementation agent", "Publish and hand over", st("st-q", "·", "Queued"), pct=0, foot="Starts after the approval", prog=""),
    ])
    allstates = "".join([
        card("·", "Queued", "Any agent", "Before its turn", st("st-q", "·", "Queued"), foot="Starts after …"),
        card("·", "Running", "Any agent", "Steps ticking", st("st-run", "✦", "Running", True), pct=50, foot="Current step", prog="2 / 4 steps"),
        card("·", "Waiting · you", "Any agent", "You are the approver", st("st-wait", "!", "Waiting for you"), extra="scard-wait", pct=100, foot="Waits for you: …"),
        card("·", "Waiting · other", "Any agent", "Someone else approves", st("st-other", "!", "Waiting for Léa Martin"), pct=100, foot="Waits for Léa Martin"),
        card("·", "Sent back", "Any agent", "Its output was sent back", st("st-chg", "↩", "Changes requested"), pct=100, foot="Sent back to the drafting agent"),
        card("·", "Failed", "Any agent", "Stopped on an error", st("st-fail", "✕", "Failed"), pct=50, bar="bar-fail", foot="Retry · View log"),
    ])
    body = ROOT.format(w=1560, h=2100) + f"""
  <div style="display: flex; flex-direction: column; gap: 8px">
    <div class="k">Agent run · in the object page</div>
    <h1 class="h1">Page version</h1>
    <p class="lead">The record. The object (here change CHG-14) gets an <b>Agents</b> tab: one card per agent in process order, the selected run in detail, and the output viewer one click away. The header indicator brings anyone there from any page. Same chip, same gate, same data as the panel.</p>
  </div>
  <div class="pnl"><span class="pt"><span class="anno" aria-hidden="true">1</span> Header indicator</span>
    <div class="band"><span class="ui" style="font-weight: 800; font-size: 18px">AI<span style="color: #39235F">Toolbox</span></span><span class="sbox">Search, or ask the assistant</span><span style="flex: 1"></span>
      <button type="button" class="ind ind-run"><span class="dots" aria-hidden="true"><i></i><i></i><i></i></span>✦ 1 agent running</button>
      <button type="button" class="ind ind-wait">✦ 1 waiting for you</button>
      <button type="button" class="ind ind-fail">✕ 1 failed</button></div>
    <span class="mt">Right of the search, before the assistant button. Shows the most urgent state among the runs you started or must approve, with their count (“2 waiting for you”). One run: opens its object’s Agents tab; several: a menu listing them with chip, agent and object. Hidden when nothing runs, waits or failed in the last 24 h.</span></div>
  <div class="pnl"><span class="pt"><span class="anno" aria-hidden="true">2</span> Agents tab · stage track</span>
    <div style="display: flex; flex-direction: column; gap: 12px; padding: 16px; border-radius: 12px; background: #FDF8FD; border: 1px solid #CAC4CF">
      <div class="tabs" role="tablist" aria-label="Change"><button type="button" role="tab" class="tab" aria-selected="false">Overview</button><button type="button" role="tab" class="tab tab-on" aria-selected="true">✦ Agents <span class="n">2/4</span></button><button type="button" role="tab" class="tab" aria-selected="false">Model changes</button><button type="button" role="tab" class="tab" aria-selected="false">Documents</button></div>
      <div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px">{track}</div>
    </div>
    <span class="mt">One card per agent, in the order of the process (TOGAF: analysis → draft → review → implementation), never sorted by state. The card is a button that selects the run below. The tab counts done / all. A waiting card carries the 2 px border; the selected one a 1 px primary ring.</span></div>
  <div style="display: grid; grid-template-columns: minmax(0, 1.1fr) minmax(0, 1fr); gap: 24px">
    <div class="pnl"><span class="pt"><span class="anno" aria-hidden="true">3</span> Run detail</span>
      <div class="box">
        <div class="mrow"><h2 class="h3">✦ Review agent</h2><span class="ai">✦ agent</span>{st("st-wait", "!", "Waiting for you")}<span class="mt" style="margin-left: auto">Run 2 · run 1 superseded</span></div>
        <ol class="steps">
          <li><span class="sm sm-done" aria-hidden="true">✓</span>JSON Schema</li><li><span class="sm sm-done" aria-hidden="true">✓</span>References and relations</li><li><span class="sm sm-done" aria-hidden="true">✓</span>Principles (PRI-01 review gate)</li><li><span class="sm sm-done" aria-hidden="true">✓</span>View checks</li><li><span class="sm sm-done" aria-hidden="true">✓</span>Write the review report</li></ol>
        <div class="gate" role="group" aria-label="Approve the change"><b>Waiting for you · Approve the change</b><span>Your approval merges pull request #48. Request changes sends it back to the drafting agent.</span><span style="display: flex; gap: 8px; flex-wrap: wrap"><button type="button" class="btn f">Approve</button><button type="button" class="btn o">Request changes</button></span></div>
        <div class="gate gate-other"><b>Seen by everyone else · Waiting for Léa Martin</b><span>Approve the change · since 10:10</span></div>
      </div>
      <span class="mt">Steps as a checklist (✓ done, ✦ current with the teal ring, number for to do). The gate under the steps; the read-only version for anyone who is not the approver. Earlier runs are listed under the activity, never merged.</span></div>
    <div class="pnl"><span class="pt"><span class="anno" aria-hidden="true">4</span> Output summary and activity</span>
      <div class="box">
        <div class="mrow"><b class="ui" style="font-size: 15px">Review report</b><span class="mt">15 checks passed</span><a class="btn x" style="margin-left: auto" href="#viewer">View output</a></div>
        <div class="orow"><span class="mk mk-ok" aria-hidden="true">✓</span><span>JSON Schema, references, relations</span></div>
        <div class="orow"><span class="mk mk-ok" aria-hidden="true">✓</span><span>PRI-01: PRC-06 has a review gate</span></div>
        <div class="orow"><span class="mk mk-ok" aria-hidden="true">✓</span><span>Owner of APC-04 set<small>Fixed in run 2</small></span></div>
        <h3 class="h3" style="font-size: 14px; margin-top: 4px">Activity</h3>
        <ul class="log"><li><time>10:10:30</time>Waiting for Léa Martin</li><li><time>10:10:15</time>Write the review report</li><li><time>10:09:15</time>JSON Schema</li><li><time>10:09:00</time>Run 2 started</li><li><time>10:01:30</time>Run 1 · changes requested by Léa Martin</li></ul>
      </div>
      <span class="mt">Up to six rows of the output; the rest is in the viewer. Activity newest first, with the run number when there is more than one.</span></div>
  </div>
  <div class="pnl"><span class="pt">Stage card · every state</span>
    <div style="display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 12px">{allstates}</div></div>
</div>"""
    return board("AgentRunPage.dc.html", "Agent run · page version", 1560, body, height=2100)

# ---------------------------------------------------------------- 4. output viewer
def viewer():
    body = ROOT.format(w=1560, h=2000) + """
  <div style="display: flex; flex-direction: column; gap: 8px">
    <div class="k">Agent run · output</div>
    <h1 class="h1">Output viewer</h1>
    <p class="lead">Where a person reads what one run produced, before approving it or after. One view with its own address (<span class="mono">/architecture/changes/CHG-14/runs/review-2</span>): opened as a side sheet from the panel (View output), as a full view from the page, shared as a link. Tabs depend on what the agent produces. Pick an agent and a tab.</p>
  </div>
  <div style="display: grid; grid-template-columns: minmax(0, 1fr) 420px; gap: 32px; align-items: start">
    <div style="display: flex; flex-direction: column; gap: 10px; min-width: 0">
      <div style="display: flex; gap: 6px; flex-wrap: wrap" role="group" aria-label="Agent"><sc-for list="{{agents}}" as="a" hint-placeholder-count="4"><button type="button" class="chip {{a.cls}}" aria-pressed="{{a.on}}" onClick="{{a.pick}}">✦ {{a.label}}</button></sc-for></div>
      <section class="box" style="padding: 0; gap: 0; overflow: hidden" aria-label="Output viewer">
        <div style="display: flex; flex-direction: column; gap: 8px; padding: 16px 20px 0; background: #F8F1FF">
          <div class="mrow"><span class="anno" aria-hidden="true">1</span><h2 class="h3" style="font-size: 20px">{{v.title}}</h2><span class="st {{v.stCls}}"><span class="g" aria-hidden="true">{{v.glyph}}</span>{{v.stLabel}}</span><span style="margin-left: auto; display: flex; gap: 6px; flex-wrap: wrap"><sc-if value="{{v.hasPr}}" hint-placeholder-val="{{true}}"><a class="btn o" href="#pr">Open pull request #48</a></sc-if><button type="button" class="btn x">Copy link</button><button type="button" class="btn x">Download</button></span></div>
          <div class="mrow mt"><span class="ai">✦ agent</span><span>{{v.meta}}</span></div>
          <div class="tabs" role="tablist" aria-label="Output" style="border-bottom: 0"><span class="anno" aria-hidden="true" style="align-self: center">2</span><sc-for list="{{tabs}}" as="t" hint-placeholder-count="4"><button type="button" role="tab" class="tab {{t.cls}}" aria-selected="{{t.on}}" onClick="{{t.pick}}">{{t.label}} <span class="n">{{t.count}}</span></button></sc-for></div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 10px; padding: 16px 20px 20px; border-top: 1px solid #CAC4CF; min-height: 420px" role="tabpanel">
          <sc-if value="{{show.summary}}" hint-placeholder-val="{{true}}">
            <span class="mt">{{v.summary}}</span>
            <sc-for list="{{v.rows}}" as="r" hint-placeholder-count="4"><div class="orow"><span class="mk {{r.cls}}" aria-hidden="true">{{r.mark}}</span><span>{{r.text}}<small>{{r.sub}}</small></span></div></sc-for>
          </sc-if>
          <sc-if value="{{show.changes}}" hint-placeholder-val="{{false}}">
            <span class="mt">model/business.yaml · +12 −0</span>
            <div class="diff" role="img" aria-label="Diff of model/business.yaml: 12 lines added">
              <div class="h">@@ processes @@</div>
              <div>  - id: PRC-04</div>
              <div>    name: Change the architecture model</div>
              <div class="a">+ - id: PRC-06</div>
              <div class="a">+   name: Reserve an environment</div>
              <div class="a">+   status: draft</div>
              <div class="a">+   realizes: [BSV-03]</div>
              <div class="h">@@ services @@</div>
              <div class="a">+ - id: BSV-03</div>
              <div class="a">+   name: Environment reservation</div>
            </div>
            <span class="mt">model/application.yaml · +3 −1</span>
            <div class="diff" role="img" aria-label="Diff of model/application.yaml: 3 lines added, 1 removed">
              <div>  - id: APC-04</div>
              <div class="d">-   serves: []</div>
              <div class="a">+   serves: [BSV-03]</div>
              <div class="a">+   owner: team-environments</div>
            </div>
          </sc-if>
          <sc-if value="{{show.views}}" hint-placeholder-val="{{false}}">
            <span class="mt">views/reserve-environment.yaml · business workflow · rendered with PlantUML, AIToolbox theme</span>
            <div style="border: 1px solid #CAC4CF; border-radius: 12px; padding: 16px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; background: #FFFFFF" role="img" aria-label="Workflow: the requester asks for an environment, the reservation agent checks capacity and drafts the reservation, the environment owner approves, the platform reserves it">
              <div style="display: flex; flex-direction: column; gap: 10px; align-items: center"><span class="sn">Requester</span><span style="padding: 6px 12px; border-radius: 16px; background: #FFF2B3; border: 1px solid #5E5000; font-size: 12px">event · Environment needed</span><span style="padding: 6px 12px; border-radius: 16px; border: 1px solid #79757F; font-size: 12px">Pick dates and size</span></div>
              <div style="display: flex; flex-direction: column; gap: 10px; align-items: center"><span class="sn">Reservation agent</span><span style="padding: 6px 12px; border-radius: 16px; background: #9CF1F0; border: 1px solid #004F50; color: #002020; font-size: 12px">✦ agent · Check capacity</span><span style="padding: 6px 12px; border-radius: 16px; background: #9CF1F0; border: 1px solid #004F50; color: #002020; font-size: 12px">✦ agent · Draft the reservation</span></div>
              <div style="display: flex; flex-direction: column; gap: 10px; align-items: center"><span class="sn">Environment owner</span><span style="padding: 6px 12px; border-radius: 16px; background: #E3DFFF; box-shadow: inset 0 0 0 2px #39235F; color: #14085E; font-size: 12px">review gate · Approve</span><span style="padding: 6px 12px; border-radius: 16px; background: #ECE5F4; border: 1px solid #CAC4CF; font-size: 12px">system · Reserve</span></div>
            </div>
            <span class="mt">Each view of the run opens in the diagram frame of the ArchiMate notation (renderer switch, fit width, sources). Mini preview here.</span>
          </sc-if>
          <sc-if value="{{show.checks}}" hint-placeholder-val="{{false}}">
            <table class="tk"><tr><th style="width: 40px"></th><th>Check</th><th>Result</th></tr>
            <sc-for list="{{v.checks}}" as="c" hint-placeholder-count="5"><tr><td><span class="mk {{c.cls}}" aria-hidden="true">{{c.mark}}</span></td><td>{{c.name}}</td><td class="mt">{{c.res}}</td></tr></sc-for></table>
          </sc-if>
          <sc-if value="{{show.log}}" hint-placeholder-val="{{false}}">
            <span class="mt">Execution trace: every step and tool call, with its duration. Read-only; Download gives the JSON.</span>
            <ol class="trace">
              <sc-for list="{{v.trace}}" as="l" hint-placeholder-count="6"><li><span class="mt" style="font-variant-numeric: tabular-nums">{{l.t}}</span><span class="mk {{l.cls}}" aria-hidden="true">{{l.mark}}</span><span><code>{{l.call}}</code><span class="mt"> · {{l.note}}</span></span><span class="d">{{l.d}}</span></li></sc-for>
            </ol>
          </sc-if>
          <sc-if value="{{show.files}}" hint-placeholder-val="{{false}}">
            <sc-for list="{{v.files}}" as="f" hint-placeholder-count="4"><div class="orow"><span class="mk {{f.cls}}" aria-hidden="true">{{f.mark}}</span><span><a href="#file">{{f.name}}</a><small>{{f.sub}}</small></span></div></sc-for>
          </sc-if>
          <sc-if value="{{v.gate}}" hint-placeholder-val="{{false}}"><div class="gate" role="group" aria-label="{{v.gateQ}}" style="margin-top: auto"><span class="mrow"><span class="anno" aria-hidden="true">3</span><b>Waiting for you · {{v.gateQ}}</b></span><span style="display: flex; gap: 8px; flex-wrap: wrap"><button type="button" class="btn f">{{v.ok}}</button><sc-if value="{{v.reject}}" hint-placeholder-val="{{false}}"><button type="button" class="btn o">Request changes</button></sc-if></span></div></sc-if>
        </div>
      </section>
    </div>
    <div style="display: flex; flex-direction: column; gap: 24px; min-width: 0">
      <div class="pnl"><span class="pt">Parts</span><table class="tk">
        <tr><td><span class="anno">1</span></td><td><b>Header</b>: output title (what it is), run chip, agent, run number, object, start, duration, who started it, who approved it. Actions: the object the output lives in (pull request, page), Copy link, Download.</td></tr>
        <tr><td><span class="anno">2</span></td><td><b>Tabs</b> by kind of output, with counts. Summary is always first and selected when opened from a milestone; Log is always last.</td></tr>
        <tr><td><span class="anno">3</span></td><td><b>Gate</b> at the bottom while the run waits and you are the approver: you decide having read it.</td></tr></table></div>
      <div class="pnl"><span class="pt">Tabs per agent</span><table class="tk"><tr><th>Agent</th><th>Tabs</th></tr>
        <tr><td>Analysis</td><td>Summary (impacted elements with change marks) · Log</td></tr>
        <tr><td>Drafting</td><td>Summary · Changes (YAML diff per file) · Views (rendered) · Files · Log</td></tr>
        <tr><td>Review</td><td>Summary · Checks (one row per rule, failing elements linked) · Log</td></tr>
        <tr><td>Implementation</td><td>Summary · Files (published pages, tickets, merged commit) · Log</td></tr></table>
        <span class="mt">A tab appears only when it has content. Changes use the notation’s marks: added lines success-container, removed error-container struck through, never colour alone (+ and − lead each line).</span></div>
      <div class="pnl"><span class="pt">Where it opens</span><table class="tk">
        <tr><td>From the panel</td><td>Side sheet over the page, 640 wide (full screen under 840 px); the conversation stays open beside it.</td></tr>
        <tr><td>From the page</td><td>Replaces the run detail, back arrow to the Agents tab.</td></tr>
        <tr><td>From a link</td><td>The object page with the viewer open.</td></tr>
        <tr><td>Earlier runs</td><td>Same viewer with the run chip “Cancelled · superseded by run 2”; no gate.</td></tr></table></div>
      <div class="dont"><b>Don’t</b><span>Show raw model prompts or chain of thought in Log: steps, tool calls, inputs and outputs only.</span><span>Let the Download be the only way to read an output.</span></div>
    </div>
  </div>
</div>"""
    js = r"""const A = {
  analysis: { label: 'Analysis agent', title: 'Impact analysis', st: ['st-done', '✓', 'Done'], hasPr: false,
    meta: 'Analysis agent · run 1 · CHG-14 · 09:40 · 1 min · started by Léa Martin from the assistant · scope confirmed by Léa Martin 09:50',
    summary: '4 elements · phases B and C', tabs: ['summary', 'log'],
    rows: [ { mark: '+', cls: 'mk-added', text: 'PRC-06 Reserve an environment', sub: 'Business process, new' }, { mark: '+', cls: 'mk-added', text: 'BSV-03 Environment reservation', sub: 'Business service, new' }, { mark: 'Δ', cls: 'mk-changed', text: 'APC-04 Environments', sub: 'Application component, gains the reservation API' }, { mark: '+', cls: 'mk-added', text: 'DOB-09 Reservation', sub: 'Data object, new' }, { mark: '·', cls: 'mk-info', text: 'PRI-01 applies', sub: 'Reservations drafted by an agent pass a person' } ] },
  draft: { label: 'Drafting agent', title: 'Draft pull request #48', st: ['st-done', '✓', 'Done'], hasPr: true,
    meta: 'Drafting agent · run 2 · CHG-14 · 10:07 · 45 s · started by the review (changes requested)',
    summary: 'model +38 −2 lines · 2 new views', tabs: ['summary', 'changes', 'views', 'files', 'log'],
    rows: [ { mark: 'Δ', cls: 'mk-changed', text: 'model/business.yaml', sub: 'PRC-06, BSV-03 added' }, { mark: 'Δ', cls: 'mk-changed', text: 'model/application.yaml', sub: 'APC-04 serves BSV-03, owner set' }, { mark: '+', cls: 'mk-added', text: 'model/data.yaml', sub: 'DOB-09 Reservation' }, { mark: '+', cls: 'mk-added', text: 'views/reserve-environment.yaml', sub: 'Business workflow' }, { mark: '+', cls: 'mk-added', text: 'views/reservation-lifecycle.yaml', sub: 'State machine' } ] },
  review: { label: 'Review agent', title: 'Review report', st: ['st-wait', '!', 'Waiting for you'], hasPr: true, gate: true, gateQ: 'Approve the change', ok: 'Approve', reject: true,
    meta: 'Review agent · run 2 · CHG-14 · 10:09 · 1 min 15 s · started by the drafting agent',
    summary: '15 checks passed · run 1 had 1 warning', tabs: ['summary', 'checks', 'log'],
    rows: [ { mark: '✓', cls: 'mk-ok', text: 'JSON Schema, references, relations', sub: '' }, { mark: '✓', cls: 'mk-ok', text: 'PRI-01: PRC-06 has a review gate', sub: '' }, { mark: '✓', cls: 'mk-ok', text: 'Owner of APC-04 set', sub: 'Fixed in run 2' } ] },
  implement: { label: 'Implementation agent', title: 'Delivered', st: ['st-done', '✓', 'Done'], hasPr: true,
    meta: 'Implementation agent · run 1 · CHG-14 · 10:11 · 1 min 10 s · started by the approval of Léa Martin',
    summary: 'merged · published · handed over', tabs: ['summary', 'files', 'log'],
    rows: [ { mark: '✓', cls: 'mk-ok', text: 'Pull request #48 merged into main', sub: 'commit 4f2c9e1' }, { mark: '✓', cls: 'mk-ok', text: '2 diagrams rendered', sub: 'Workflow (PlantUML), life cycle (Mermaid)' }, { mark: '✓', cls: 'mk-ok', text: 'Docs page published', sub: 'Reserve an environment' }, { mark: '✓', cls: 'mk-ok', text: 'Jira ENV-231, ENV-232, ENV-233 created', sub: 'Team environments' } ] }
};
const CHECKS = [ ['✓', 'mk-ok', 'JSON Schema', 'model/*.yaml valid'], ['✓', 'mk-ok', 'References', 'every ID exists (PRC-06, BSV-03, APC-04, DOB-09)'], ['✓', 'mk-ok', 'Relations', 'realization, serving, access allowed by the metamodel'], ['✓', 'mk-ok', 'PRI-01 review gate', 'PRC-06 has a gate before the reservation takes effect'], ['✓', 'mk-ok', 'Views', 'both views render in PlantUML and Mermaid'], ['✓', 'mk-ok', 'Ownership', 'APC-04 owner: team-environments (run 1: warning)'] ];
const TRACE = {
  analysis: [ ['09:40:15', 'mk-run', '✦', 'conversation.read()', 'request and 3 messages', '0.4 s'], ['09:40:30', 'mk-run', '✦', 'model.search("environment reservation")', '7 hits', '1.2 s'], ['09:41:00', 'mk-run', '✦', 'model.impact(PRC-06, APC-04)', '4 elements, phases B, C', '2.1 s'], ['09:41:20', 'mk-ok', '✓', 'output.write("Impact analysis")', '5 rows', '0.3 s'], ['09:41:20', 'mk-info', '!', 'gate.open("Confirm the scope", Léa Martin)', 'waiting', '—'] ],
  draft: [ ['10:07:00', 'mk-run', '✦', 'review.comments(run 1)', '1 comment', '0.2 s'], ['10:07:15', 'mk-run', '✦', 'yaml.edit(model/application.yaml)', '+1 −0', '0.6 s'], ['10:07:30', 'mk-run', '✦', 'git.push(change/chg-14)', 'commit 9ab31d0', '2.4 s'], ['10:07:45', 'mk-ok', '✓', 'pr.update(#48)', 'ready for review', '0.8 s'] ],
  review: [ ['10:09:00', 'mk-run', '✦', 'schema.validate(model/)', '0 errors', '1.1 s'], ['10:09:15', 'mk-run', '✦', 'refs.check()', '0 missing', '0.7 s'], ['10:09:30', 'mk-run', '✦', 'principles.check(PRI-01)', 'gate found in PRC-06', '0.5 s'], ['10:09:50', 'mk-run', '✦', 'views.render(2)', 'PlantUML, Mermaid', '6.8 s'], ['10:10:15', 'mk-ok', '✓', 'output.write("Review report")', '15 checks', '0.3 s'], ['10:10:30', 'mk-info', '!', 'gate.open("Approve the change", Léa Martin)', 'waiting', '—'] ],
  implement: [ ['10:11:15', 'mk-run', '✦', 'pr.merge(#48)', 'commit 4f2c9e1', '3.0 s'], ['10:11:30', 'mk-run', '✦', 'views.render(2)', 'svg, light and dark', '7.2 s'], ['10:11:50', 'mk-run', '✦', 'docs.publish("Reserve an environment")', 'published', '2.6 s'], ['10:12:10', 'mk-ok', '✓', 'jira.create(ENV, 3)', 'ENV-231…233', '1.9 s'] ]
};
const FILES = {
  draft: [ ['Δ', 'mk-changed', 'model/business.yaml', '+12 −0'], ['Δ', 'mk-changed', 'model/application.yaml', '+3 −1'], ['+', 'mk-added', 'model/data.yaml', '+18 −0'], ['+', 'mk-added', 'views/reserve-environment.yaml', 'business workflow'], ['+', 'mk-added', 'views/reservation-lifecycle.yaml', 'state machine'] ],
  implement: [ ['✓', 'mk-ok', 'Pull request #48', 'merged into main · 4f2c9e1'], ['✓', 'mk-ok', 'Docs · Reserve an environment', 'published 10:11'], ['✓', 'mk-ok', 'ENV-231 Reservation API in Environments', 'Jira · team environments'], ['✓', 'mk-ok', 'ENV-232 Reservation screen', 'Jira'], ['✓', 'mk-ok', 'ENV-233 Automatic release job', 'Jira'] ]
};
const TL = { summary: 'Summary', changes: 'Changes', views: 'Views', checks: 'Checks', files: 'Files', log: 'Log' };
class Component extends DCLogic {
  constructor(p) { super(p); this.state = { a: 'review', t: 'summary' }; }
  renderVals() {
    const a = A[this.state.a]; const t = a.tabs.includes(this.state.t) ? this.state.t : 'summary';
    const trace = TRACE[this.state.a].map(x => ({ t: x[0], cls: x[1], mark: x[2], call: x[3], note: x[4], d: x[5] }));
    const files = (FILES[this.state.a] || []).map(x => ({ mark: x[0], cls: x[1], name: x[2], sub: x[3] }));
    const counts = { summary: a.rows.length, changes: 2, views: 2, checks: CHECKS.length, files: files.length, log: trace.length };
    const show = {}; Object.keys(TL).forEach(k => { show[k] = t === k; });
    return {
      agents: Object.keys(A).map(k => ({ label: A[k].label, on: this.state.a === k, cls: this.state.a === k ? 'chip-on' : '', pick: () => this.setState({ a: k, t: 'summary' }) })),
      tabs: a.tabs.map(k => ({ label: TL[k], count: counts[k], on: t === k, cls: t === k ? 'tab-on' : '', pick: () => this.setState({ t: k }) })),
      show,
      v: { title: a.title, stCls: a.st[0], glyph: a.st[1], stLabel: a.st[2], hasPr: a.hasPr, meta: a.meta, summary: a.summary, rows: a.rows, gate: !!a.gate, gateQ: a.gateQ || '', ok: a.ok || '', reject: !!a.reject,
           checks: CHECKS.map(c => ({ mark: c[0], cls: c[1], name: c[2], res: c[3] })), trace, files }
    };
  }
}"""
    return board("AgentOutput.dc.html", "Agent run · output viewer", 1560, body, js, height=2000)

names = [guidance(), panel(), page(), viewer()]

# canvas index
c = json.load(open(os.path.join(OUT, "canvas.json")))
y = 45432
specs = {
    "AgentRun.dc.html": ("Agent run · usage: one run, two views (assistant panel, object page), eight states, anatomy, rules, do and don’t, accessibility (decided 2026-11-23: option C of the Agent follow lab)", 2140, False),
    "AgentRunPanel.dc.html": ("Agent run · panel version: run strip, milestone rows (started, finished, waiting with the gate, failed), sizes and tokens · pick a moment", 1960, True),
    "AgentRunPage.dc.html": ("Agent run · page version: header indicator, Agents tab with the stage track (TOGAF: analysis, draft, review, implementation), run detail, output summary and activity, stage card in every state", 2100, False),
    "AgentOutput.dc.html": ("Agent run · output viewer: header, tabs by agent (Summary, Changes, Views, Checks, Files, Log), the gate at the bottom, where it opens · pick an agent and a tab", 2000, True),
}
for i, n in enumerate(names):
    t, h, inter = specs[n]
    e = {"x": i * 1640, "y": y, "w": 1560, "h": h, "title": t}
    if inter:
        e["is_interactive"] = True
    c["boards"][n] = e
    if n not in c["order"]:
        c["order"].append(n)
c["notes"]["t12"] = {"kind": "title1", "x": 0, "y": y - 260, "text": "Components · agent run (decided 2026-11-23): usage, panel version, page version, output viewer", "maxW": 6440}
json.dump(c, open(os.path.join(OUT, "canvas.json"), "w"), indent=2, ensure_ascii=False)
print("written", names)
