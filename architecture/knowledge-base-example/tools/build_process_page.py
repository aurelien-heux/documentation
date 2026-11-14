"""Generates the Architecture Change Process page (flow swimlanes + Git timeline + steps)."""
import html, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'architecture-change-process.html'
TOKENS = (ROOT / 'design-system' / 'archimate' / 'tokens-bridge.css').read_text()
TOKENS = re.sub(r'/\*.*?\*/', '', TOKENS, count=1, flags=re.S)

esc = html.escape

# ---------------------------------------------------------------- flow swimlanes
LX = 150                      # lane label column
COLS = {'trigger': 260, 'decide': 490, 'designA': 720, 'designB': 950,
        'review': 1180, 'deliverA': 1410, 'deliverB': 1640}
W = 1780
HEAD = 72
LANES = [  # key, label, sublabel, height
    ('people', 'People', ['requester', 'architect, teams'], 124),
    ('toolbox', 'Toolbox', ['Architecture ›', 'Process'], 124),
    ('ci', 'Agents & CI', ['drafts, checks,', 'builds'], 124),
    ('board', 'ARB', ['Architecture Board', 'reviewers by role'], 124),
    ('git', 'Git', ['central and', 'Application repos'], 168),
]
LANE_Y = {}
y = HEAD
for k, _, _, h in LANES:
    LANE_Y[k] = (y, h)
    y += h
H = y + 8
NW, NH = 180, 72


def cy(lane):
    y0, h = LANE_Y[lane]
    return y0 + (62 if lane == 'git' else h / 2)


NODES = {
    'T1': ('people', 'trigger', 'Change request', ['ticket, chat, condition']),
    'T2': ('ci', 'trigger', 'Drift detected', ['nightly reconciliation']),
    'C1': ('toolbox', 'decide', 'Open a change', ['class, plateaus,', 'reviewers, work package']),
    'C2': ('git', 'decide', 'change/WP-FAC-02', ['branch + draft PR', 'in the central repo']),
    'D1': ('people', 'designA', 'Model the change', ['building blocks, ASD', 'DD in Application repos']),
    'D2': ('git', 'designA', 'Branch commits', ['DD and contract PRs', 'reference WP-FAC-02']),
    'D3': ('ci', 'designB', 'Agents, validator', ['draft DD and SBBs', 'checks · preview pr-88']),
    'D4': ('toolbox', 'designB', 'Gap and checks', ['baseline → target', 'on the preview build']),
    'R1': ('toolbox', 'review', 'Submit to ARB', ['readiness gate', 'ASD frozen at the sha']),
    'R2': ('board', 'review', 'Board decision', ['each reviewer records', 'a Checkpoint']),
    'R3': ('git', 'review', 'Decision and merge', ['bot commits ARB record', 'tag arb/facility-2026-14']),
    'V1': ('toolbox', 'deliverA', 'Track delivery', ['Work items · conditions', 'due dates']),
    'V2': ('people', 'deliverA', 'Implement', ['code, contracts, DD', 'in Application repos']),
    'V3': ('ci', 'deliverB', 'Conformance', ['code vs target', '(tier-3 extraction)']),
    'V4': ('toolbox', 'deliverB', 'Plateau reached', ['architect confirms', 'conditions closed']),
    'V5': ('git', 'deliverB', 'Promote plateau', ['target becomes baseline', 'and a plateau tag']),
}


def node_box(k):
    lane, col, *_ = NODES[k]
    x, yc = COLS[col], cy(lane)
    return x - NW / 2, yc - NH / 2, x + NW / 2, yc + NH / 2


def L(k):  # left mid
    x0, y0, x1, y1 = node_box(k); return x0, (y0 + y1) / 2
def R(k):
    x0, y0, x1, y1 = node_box(k); return x1, (y0 + y1) / 2
def T(k):
    x0, y0, x1, y1 = node_box(k); return (x0 + x1) / 2, y0
def B(k):
    x0, y0, x1, y1 = node_box(k); return (x0 + x1) / 2, y1


def path(points):
    return 'M' + ' L'.join(f'{x:.0f},{y:.0f}' for x, y in points)


EDGES = []  # (points, cls, label, (lx, ly), anchor)

def edge(points, label=None, at=None, cls='e', anchor='middle'):
    EDGES.append((points, cls, label, at, anchor))

# trigger → decide
a, b = R('T1'), L('C1'); edge([a, (375, a[1]), (375, b[1]), b])
a = R('T2'); edge([a, (375, a[1]), (375, b[1] + 0.1)])
# decide
a, b = B('C1'), T('C2'); edge([a, b], 'creates', (a[0] + 8, 430), anchor='start')
a, b = R('C1'), L('D1'); edge([a, (605, a[1]), (605, b[1]), b], 'architect', (613, 232), anchor='start')
# design
a, b = B('D1'), T('D2'); edge([a, b], 'each save is a commit', (712, 470), anchor='end')
a, b = R('D2'), L('D3'); edge([a, (835, a[1]), (835, b[1]), b], 'build', (843, 470), anchor='start')
a, b = T('D3'), B('D4'); edge([a, b], 'results', (a[0] + 8, 333), anchor='start')
a, b = R('D4'), L('R1'); edge([a, b])
# review
a, b = B('R1'), T('R2'); edge([a, b], 'readiness ok', (a[0] + 8, 404), anchor='start')
a, b = B('R2'), T('R3'); edge([a, b], 'approve', (a[0] + 8, 586), anchor='start')
a, b = L('R2'), R('D1'); edge([a, (1065, a[1]), (1065, b[1]), b], 'request changes', (1057, 150), cls='e loop', anchor='end')
# deliver
a, b = R('R3'), L('V1'); edge([a, (1295, a[1]), (1295, b[1]), b], 'merged = approved target', (1303, 444), anchor='start')
a, b = T('V1'), B('V2'); edge([a, b], 'Work items', (a[0] + 8, 194), anchor='start')
a, b = R('V2'), L('V3'); edge([a, (1525, a[1]), (1525, b[1]), b], 'code PRs', (1517, 314), anchor='end')
a, b = T('V3'), B('V4'); edge([a, b], 'conforms', (a[0] + 8, 333), anchor='start')
a, b = R('V4'), R('V5'); edge([a, (1754, a[1]), (1754, b[1]), b], 'promote', (1746, 452), anchor='end')
# simplification fast path
a, b = B('C2'), B('R3'); fy = LANE_Y['git'][0] + 146
edge([a, (a[0], fy), (b[0], fy), b], 'Simplification: checks green + CODEOWNERS approve, no board',
     ((a[0] + b[0]) / 2, fy - 8), cls='e fast')

LANE_CLS = {'people': 'n-people', 'toolbox': 'n-toolbox', 'ci': 'n-ci', 'board': 'n-board', 'git': 'n-git'}

PHASES = [
    ('0', 'Trigger', ['TOGAF Phase H · change request'], COLS['trigger'], 230),
    ('1', 'Decide', ['Phase H → A · Statement of', 'Architecture Work'], COLS['decide'], 230),
    ('2', 'Design', ['Phases B–F · target, gap and roadmap'], (COLS['designA'] + COLS['designB']) / 2, 460),
    ('3', 'Review', ['Phase G · Architecture Board'], COLS['review'], 230),
    ('4', 'Deliver', ['Phases G–H · Architecture Contract,', 'implementation'], (COLS['deliverA'] + COLS['deliverB']) / 2, 460),
]


def flow_svg():
    o = [f'<svg class="flow" viewBox="0 0 {W} {H}" role="img" aria-labelledby="flow-t flow-d">',
         '<title id="flow-t">Architecture change flow</title>',
         '<desc id="flow-d">Swimlanes for people, toolbox, agents and CI, the Architecture Board and Git across the steps '
         'Trigger, Decide, Design, Review and Deliver. A request becomes a change with a branch and draft pull request; '
         'the model is changed on the branch and validated on each push; the change is submitted to the board; '
         'request changes loops back to design; approval leads to a decision commit and merge; delivery ends with the '
         'plateau promoted to baseline. Simplification changes skip the board.</desc>',
         '<defs>']
    for cls in ('e', 'loop', 'fast'):
        o.append(f'<marker id="mk-{cls}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                 f'<path d="M0,0 L10,5 L0,10 z" class="mk mk-{cls}"/></marker>')
    o.append('</defs>')
    # lanes
    for i, (k, label, sub, h) in enumerate(LANES):
        y0, _ = LANE_Y[k]
        o.append(f'<rect class="lane {"alt" if i % 2 else ""}" x="0" y="{y0}" width="{W}" height="{h}"/>')
        o.append(f'<text class="lane-l" x="16" y="{y0 + 30}">{esc(label)}</text>')
        o.extend(f'<text class="lane-s" x="16" y="{y0 + 50 + j * 15}">{esc(t)}</text>' for j, t in enumerate(sub))
    o.append(f'<line class="lane-sep" x1="{LX - 8}" y1="{HEAD}" x2="{LX - 8}" y2="{H - 8}"/>')
    # phase headers
    for num, name, sub, x, w in PHASES:
        o.append(f'<rect class="ph" x="{x - w / 2 + 6}" y="8" width="{w - 12}" height="{HEAD - 16}" rx="8"/>')
        o.append(f'<text class="ph-n" x="{x}" y="{30}" text-anchor="middle">{num} · {esc(name)}</text>')
        for j, s in enumerate(sub):
            o.append(f'<text class="ph-s" x="{x}" y="{47 + j * 13}" text-anchor="middle">{esc(s)}</text>')
    # edges below nodes
    for pts, cls, label, at, anchor in EDGES:
        mk = 'loop' if 'loop' in cls else 'fast' if 'fast' in cls else 'e'
        o.append(f'<path class="{cls}" d="{path(pts)}" marker-end="url(#mk-{mk})"/>')
    # nodes
    for k, (lane, col, title, sub) in NODES.items():
        x0, y0, x1, y1 = node_box(k)
        o.append(f'<g class="node {LANE_CLS[lane]}"><rect x="{x0}" y="{y0}" width="{NW}" height="{NH}" rx="{12 if lane != "git" else 6}"/>')
        o.append(f'<text class="n-t" x="{x0 + 12}" y="{y0 + 22}">{esc(title)}</text>')
        for j, s in enumerate(sub):
            o.append(f'<text class="n-s" x="{x0 + 12}" y="{y0 + 41 + j * 16}">{esc(s)}</text>')
        o.append('</g>')
    # labels on top
    for pts, cls, label, at, anchor in EDGES:
        if label:
            lc = 'lbl loop' if 'loop' in cls else 'lbl'
            o.append(f'<text class="{lc}" x="{at[0]:.0f}" y="{at[1]:.0f}" text-anchor="{anchor}">{esc(label)}</text>')
    o.append('</svg>')
    return '\n'.join(o)


# ---------------------------------------------------------------- git timeline
GW, GH = 1300, 330
YM, YB, YA = 70, 170, 270


def git_svg():
    o = [f'<svg class="git" viewBox="0 0 {GW} {GH}" role="img" aria-labelledby="git-t git-d">',
         '<title id="git-t">Git history of one change</title>',
         '<desc id="git-d">The main branch of the central repository, the change branch change/WP-FAC-02 and the '
         'facility-service repository. The branch is opened from main, receives model and ASD commits, is submitted '
         'to the board at a pinned commit, gets a fix after a request for changes, then a bot commit recording the '
         'decision, and is merged with a merge commit tagged arb/facility-2026-14. The application repository merges '
         'its detailed design, which reaches main through a lock bump. Later main commits close the conditions and '
         'promote the plateau, tagged plateau/facility/transition-1.</desc>',
         '<defs><marker id="g-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         '<path d="M0,0 L10,5 L0,10 z" class="mk mk-e"/></marker></defs>']
    # lane labels
    for yy, t, s in ((YM, 'main', 'central repository'), (YB, 'change/WP-FAC-02', 'central repository · PR #88'),
                     (YA, 'facility-service', 'Application repository · PR #412')):
        o.append(f'<text class="g-l" x="16" y="{yy - 4}">{esc(t)}</text><text class="g-s" x="16" y="{yy + 13}">{esc(s)}</text>')
    X0 = 200
    # lines
    o.append(f'<path class="g-main" d="M{X0},{YM} L{GW - 20},{YM}" marker-end="url(#g-ar)"/>')
    o.append(f'<path class="g-br" d="M290,{YM} C330,{YM} 330,{YB} 370,{YB} L930,{YB} C970,{YB} 970,{YM} 1000,{YM}"/>')
    o.append(f'<path class="g-app" d="M400,{YA} L750,{YA} C790,{YA} 790,{YM} 830,{YM}" />')

    def dot(x, yy, cls='c'):
        o.append(f'<circle class="g-{cls}" cx="{x}" cy="{yy}" r="7"/>')

    def lab(x, yy, lines, cls='g-t', anchor='middle'):
        for j, s in enumerate(lines):
            o.append(f'<text class="{cls}" x="{x}" y="{yy + j * 15}" text-anchor="{anchor}">{esc(s)}</text>')

    def tag(x, yy, text):
        w = 8 + len(text) * 6.9
        o.append(f'<g class="g-tag"><rect x="{x - w / 2}" y="{yy}" width="{w}" height="22" rx="4"/>'
                 f'<text x="{x}" y="{yy + 15}" text-anchor="middle">{esc(text)}</text></g>')

    # main commits
    dot(230, YM); lab(230, YM - 18, ['approved baseline'])
    dot(290, YM)
    dot(830, YM, 'bot'); lab(830, YM - 33, ['lock bump', '(bot)'])
    dot(1000, YM, 'merge'); tag(1000, YM - 44, 'arb/facility-2026-14')
    lab(1000, YM - 52, ['merge commit, no squash'], 'g-t')
    dot(1100, YM); lab(1100, YM + 26, ['conditions', 'closed'])
    dot(1200, YM, 'merge'); tag(1190, YM - 44, 'plateau/facility/transition-1')
    lab(1200, YM + 26, ['promote', 'plateau'])
    # branch commits
    dot(400, YB); lab(400, YB + 26, ['open change:', 'WP, gap, ADR draft'])
    dot(500, YB); lab(500, YB - 16, ['model + gap'])
    dot(600, YB, 'pin'); lab(600, YB + 26, ['ASD · submitted', 'pinned sha 7c1e9a0'])
    dot(720, YB, 'warn'); lab(720, YB - 30, ['fix after', '“Request changes”'])
    lab(720, YB + 26, ['updated since', 'review → re-review'], 'g-t warn')
    dot(880, YB, 'bot'); lab(880, YB + 26, ['bot: ARB record', 'approved with conditions'])
    # app commits
    dot(460, YA); lab(460, YA + 26, ['DD + contract', 'change: WP-FAC-02'])
    dot(585, YA); lab(585, YA + 26, ['validated against', 'preview pr-88'])
    dot(700, YA, 'merge'); lab(700, YA + 26, ['merged · fragment', 'published'])
    # checks callout
    o.append(f'<g class="g-chk"><rect x="890" y="{YB + 58}" width="250" height="56" rx="8"/>'
             f'<text x="904" y="{YB + 80}">Required checks on PR #88</text>'
             f'<text x="904" y="{YB + 100}" class="ok">✓ arch-validate   ✓ arb-decision</text></g>')
    o.append('</svg>')
    return '\n'.join(o)


# ---------------------------------------------------------------- steps content
STEPS = [
    dict(n='0', name='Trigger', phase='TOGAF Phase H · change request',
         deliverable='Request for Architecture Work, when the change is large',
         who='Anyone can propose. The portfolio architect owns the request.',
         toolbox=[('Process › Changes', 'Propose a change: title, why, Applications concerned.'),
                  ('Header search', 'Ask the assistant to draft a change from a conversation; it fills the same form.'),
                  ('Checks, drift alerts, ARB conditions', '"Open as a change" pre-fills the request with the finding.')],
         git=['Nothing yet. The request is a draft in the toolbox, not a branch.'],
         done='An architect accepts the request and becomes the change owner.'),
    dict(n='1', name='Decide', phase='TOGAF Phase H → A · classify, then scope',
         deliverable='Statement of Architecture Work (scope, plateaus, stakeholders)',
         who='Change owner. The portfolio architect confirms the class.',
         toolbox=[('Process › Changes › New change', 'Class: simplification, incremental or re-architecting. It decides the path below.'),
                  ('Scope', 'Portfolio and Applications, from plateau → to plateau, work package (new or existing).'),
                  ('Reviewers', 'Suggested by role from the class and CODEOWNERS; the owner adjusts.'),
                  ('Process › Decisions', 'A draft ADR for each decision the change needs.'),
                  ('Overlap', 'Open changes on the same building blocks are listed; the owner sequences, combines or runs them in parallel.')],
         git=['CTX-INT creates change/WP-FAC-02 in the central repository.',
              'First commit: work package, gap stub, ADR drafts, ARB record draft (incremental and re-architecting).',
              'Draft PR #88 opens; CI publishes preview pr-88.'],
         done='Scope saved, draft PR open, preview available.'),
    dict(n='2', name='Design', phase='TOGAF Phases B, C, D (target) and E, F (gap, roadmap)',
         deliverable='Architecture Definition: target building blocks, requirements, gap, ASD, detailed design',
         who='Change owner, Application leads, agents (drafts only: a person accepts every agent change).',
         toolbox=[('Catalogue', 'Add, change or retire elements; each is tagged with its plateau and change chip.'),
                  ('Views', 'Gap view baseline → target, on the preview build, with drill-down to the DD.'),
                  ('Agent actions', 'Draft DD from the contract, propose SBBs from a new endpoint, write an ASD section from the model.'),
                  ('Process › Reviews (draft)', 'Checks with their fixes and the 13 ASD coverage items, updated on each push.')],
         git=['Every save is a commit on the branch; agent commits carry the agent as author and the person as co-author.',
              'DD and contract PRs in Application repositories set change: WP-FAC-02 and validate against preview pr-88.',
              'arch-validate runs on each push; errors block, warnings show in the PR comment.'],
         done='0 blocking errors, coverage complete or explained, reviewers assigned. "Submit to ARB" becomes available.'),
    dict(n='3', name='Review', phase='TOGAF Phase G · Architecture Board, compliance',
         deliverable='Board decision and, when approved, the Architecture Contract (conditions)',
         who='Reviewers by role, the board chair. Decisions are Checkpoints (INV-12); agents never decide.',
         toolbox=[('Process › Reviews › arb.facility.2026-14', 'Submit: the readiness gate runs, the ASD is generated and frozen at the commit.'),
                  ('Reviewers', 'Each records Approve, Approve with conditions, Request changes or Not required, with a note.'),
                  ('Conditions and asks', 'Owner, due date and status per condition; the decisions only the board can take.'),
                  ('Updated since review', 'If the branch moves after submission, a banner shows the diff since the pinned commit.')],
         git=['PR #88 leaves draft; the reviewed sha is pinned; the arb-decision check stays pending.',
              'When the Checkpoint is decided, the bot commits the ARB record (status, decision, conditions, decidedAt, reviewedSha).',
              'arb-decision turns green; the owner merges with a merge commit (no squash) so the reviewed sha stays in history.',
              'The merge goes through the merge queue: arch-validate runs on the branch plus the latest main.',
              'The merge commit is tagged arb/facility-2026-14.'],
         outcomes=[('ok', 'Approve, Approve with conditions', 'merge; conditions move to Deliver.'),
                   ('warn', 'Request changes', 'back to Design, then re-submit; the ASD is frozen again.'),
                   ('err', 'Reject', 'PR closed; the bot commits only the ARB record to main, so the decision is kept.')],
         done='Decision recorded in Git and the change merged (or closed).'),
    dict(n='4', name='Deliver', phase='TOGAF Phases G and H · implementation governance, monitoring',
         deliverable='Conformance with the Architecture Contract; the plateau reached',
         who='Application teams and their agents build; the change owner confirms conformance.',
         toolbox=[('Process › Roadmap', 'Work package status, linked Work items (CTX-ORC), conditions with due dates.'),
                  ('Conformance', 'Reconciliation compares extracted code with the target: missing SBBs, endpoints without a model element.'),
                  ('Plateau reached', 'The owner confirms when every work package of the plateau is delivered and conditions are closed.')],
         git=['Implementation PRs in Application repositories (code, contracts, DD); fragments published; lock bumps on main.',
              'A "Promote transition-1" PR: elements of the plateau become baseline, retired elements are removed.',
              'Tag plateau/facility/transition-1. The ARB record and ADRs stay as history.'],
         done='Conditions closed, conformance green, plateau promoted. The change closes.'),
]

CLASSES = [
    ('Simplification', 'Rename, owner change, a missing relationship, a description',
     'Decide → Design → merge', 'CODEOWNERS approve the PR once checks are green', 'None'),
    ('Incremental', 'A new interface on an existing SBB, a new Module inside an agreed plateau',
     'All steps', 'Portfolio architect, recorded as a Checkpoint', 'Short: context, gap, decisions'),
    ('Re-architecting', 'A new plateau, extracting a service, a new platform or data store',
     'All steps', 'Architecture Board', 'Full: the 13 coverage items'),
]

GITRULES = [
    ('Branch', 'change/&lt;work package&gt;', 'One branch and one PR per change, in the central repository.'),
    ('PR title', '[WP-FAC-02] Extract facility-service', 'The work package id links the PR, the change and the ARB record.'),
    ('Preview', '?ref=pr-88', 'Each push publishes a preview build; the toolbox shows the gap on it.'),
    ('Linked repos', 'change: WP-FAC-02', 'Frontmatter on DD files changed in Application repositories.'),
    ('Required checks', 'arch-validate · arb-decision', 'Validator errors block; arb-decision is set by the toolbox from the Checkpoint (green for simplification once CODEOWNERS approve).'),
    ('Review pin', 'reviewedSha', 'The board decides on one commit; later commits flag "updated since review".'),
    ('Bot commits', 'atb-arch-bot', 'Only the ARB record and lock bumps; credentials stay in CTX-INT (INV-07).'),
    ('Merge', 'merge commit', 'No squash, so the reviewed commit stays reachable.'),
    ('Tags', 'arb/&lt;portfolio&gt;-&lt;year&gt;-&lt;n&gt; · plateau/&lt;portfolio&gt;/&lt;plateau&gt;', 'A decision and a reached plateau are both findable in history.'),
    ('Change file', 'model/bb/changes/&lt;work package&gt;.c4', 'The work package, the blocks it introduces and its relationships; folded into the model when the plateau is promoted.'),
    ('Order', 'dependsOn', 'Work package metadata. A change cannot enter the merge queue before the change it depends on is merged.'),
    ('Merge queue', 'merge train / merge queue', 'Checks run on the result of the branch plus the latest main, one change at a time.'),
    ('Undo', 'revert PR', 'A revert is itself a change: simplification if it restores an approved state, otherwise a new review.'),
]


def li_pairs(items):
    return ''.join(f'<li><b>{esc(a)}</b><span>{esc(b)}</span></li>' for a, b in items)


def li(items):
    return ''.join(f'<li>{esc(s)}</li>' for s in items)


def steps_html():
    out = []
    for s in STEPS:
        outcomes = ''
        if s.get('outcomes'):
            outcomes = '<div class="outcomes"><h4>Outcomes</h4><ul>' + ''.join(
                f'<li><span class="chip c-{c}"><span class="tile" aria-hidden="true">{"✓" if c == "ok" else "!" if c == "warn" else "✕"}</span>{esc(a)}</span><span>{esc(b)}</span></li>'
                for c, a, b in s['outcomes']) + '</ul></div>'
        out.append(f'''
<article class="step" id="step-{s['n']}" aria-labelledby="step-{s['n']}-h">
  <header class="step-h">
    <span class="num" aria-hidden="true">{s['n']}</span>
    <div><h3 id="step-{s['n']}-h">{esc(s['name'])}</h3><p class="phase">{esc(s['phase'])}</p></div>
  </header>
  <dl class="meta"><div><dt>TOGAF deliverable</dt><dd>{esc(s['deliverable'])}</dd></div><div><dt>Who</dt><dd>{esc(s['who'])}</dd></div></dl>
  <div class="cols">
    <section><h4>In the toolbox</h4><ul class="pairs">{li_pairs(s['toolbox'])}</ul></section>
    <section><h4>In Git</h4><ul class="git-l">{li(s['git'])}</ul>{outcomes}</section>
  </div>
  <p class="done"><span class="tile" aria-hidden="true">✓</span><span><b>Done when</b> {esc(s['done'])}</span></p>
</article>''')
    return '\n'.join(out)


def classes_html():
    rows = ''.join(f'<tr><th scope="row">{esc(a)}</th><td>{esc(b)}</td><td>{esc(c)}</td><td>{esc(d)}</td><td>{esc(e)}</td></tr>'
                   for a, b, c, d, e in CLASSES)
    return ('<div class="tbl"><table><thead><tr><th scope="col">Class</th><th scope="col">Examples</th><th scope="col">Steps</th>'
            '<th scope="col">Who approves</th><th scope="col">ASD</th></tr></thead><tbody>' + rows + '</tbody></table></div>')


def git_rules_html():
    rows = ''.join(f'<tr><th scope="row">{a}</th><td><code>{b}</code></td><td>{esc(c)}</td></tr>' for a, b, c in GITRULES)
    return ('<div class="tbl"><table><thead><tr><th scope="col">Rule</th><th scope="col">Convention</th><th scope="col">Why</th></tr></thead><tbody>'
            + rows + '</tbody></table></div>')


# ---------------------------------------------------------------- parallel changes timeline
PW, PH = 1180, 300
PM, PA, PB = 70, 165, 250


def parallel_svg():
    o = [f'<svg class="git" viewBox="0 0 {PW} {PH}" role="img" aria-labelledby="par-t par-d">',
         '<title id="par-t">Two approved changes merging one after the other</title>',
         '<desc id="par-d">Change WP-FAC-02 and change WP-REQ-05 both branch from main and are both approved by the board. '
         'WP-FAC-02 merges first through the merge queue. WP-REQ-05 then takes main in, the conflict is resolved, and its own '
         'diff is compared with the diff the board approved at the pinned commit. It then goes through the merge queue, '
         'where checks run on the branch plus the latest main, and merges.</desc>',
         '<defs><marker id="p-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         '<path d="M0,0 L10,5 L0,10 z" class="mk mk-e"/></marker></defs>']
    for yy, t, sub in ((PM, 'main', 'central repository'), (PA, 'change/WP-FAC-02', 'Facility · merges first'),
                       (PB, 'change/WP-REQ-05', 'Request · merges second')):
        o.append(f'<text class="g-l" x="16" y="{yy - 4}">{esc(t)}</text><text class="g-s" x="16" y="{yy + 13}">{esc(sub)}</text>')
    o.append(f'<path class="g-main" d="M200,{PM} L{PW - 20},{PM}" marker-end="url(#p-ar)"/>')
    o.append(f'<path class="g-br" d="M240,{PM} C275,{PM} 275,{PA} 310,{PA} L560,{PA} C600,{PA} 600,{PM} 640,{PM}"/>')
    o.append(f'<path class="g-br2" d="M270,{PM} C320,{PM} 320,{PB} 370,{PB} L920,{PB} C960,{PB} 960,{PM} 1000,{PM}"/>')
    o.append(f'<path class="g-upd" d="M700,{PM} C730,{PM} 730,{PB} 760,{PB}"/>')

    def dot(x, yy, cls='c'):
        o.append(f'<circle class="g-{cls}" cx="{x}" cy="{yy}" r="7"/>')

    def lab(x, yy, lines, cls='g-t'):
        for j, t in enumerate(lines):
            o.append(f'<text class="{cls}" x="{x}" y="{yy + j * 15}" text-anchor="middle">{esc(t)}</text>')

    def tag(x, yy, text):
        w = 8 + len(text) * 6.9
        o.append(f'<g class="g-tag"><rect x="{x - w / 2}" y="{yy}" width="{w}" height="22" rx="4"/>'
                 f'<text x="{x}" y="{yy + 15}" text-anchor="middle">{esc(text)}</text></g>')

    dot(360, PA); lab(360, PA - 16, ['model + gap'])
    dot(470, PA, 'pin'); lab(470, PA - 16, ['ARB approved'])
    dot(640, PM, 'merge'); tag(640, PM - 44, 'WP-FAC-02 merged')
    dot(440, PB); lab(440, PB + 26, ['model + gap'])
    dot(560, PB, 'pin'); lab(560, PB + 26, ['ARB approved', 'pinned 5d2e8f1'])
    dot(760, PB, 'warn'); lab(760, PB + 26, ['main taken in,', 'conflict resolved'], 'g-t warn')
    dot(880, PB); lab(880, PB + 26, ['own diff', 'compared'])
    dot(1000, PM, 'merge'); tag(1000, PM - 44, 'WP-REQ-05 merged')
    o.append('</svg>')
    return '\n'.join(o)


PAGE = (pathlib.Path(__file__).parent / 'process.template.html').read_text()
PAGE = (PAGE.replace('/*__TOKENS__*/', TOKENS).replace('<!--FLOW-->', flow_svg()).replace('<!--GIT-->', git_svg()).replace('<!--PARALLEL-->', parallel_svg())
        .replace('<!--STEPS-->', steps_html()).replace('<!--CLASSES-->', classes_html()).replace('<!--GITRULES-->', git_rules_html()))
OUT.write_text(PAGE)
print(OUT, len(PAGE))
