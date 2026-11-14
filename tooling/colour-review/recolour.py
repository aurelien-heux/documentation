import re, json, os, sys
S = '/tmp/claude-0/-home-claude/7965e1dc-e9df-573c-8252-b3af265ef67c/scratchpad/'
SKIP = {'RunButton2.dc.html', 'RunButton3.dc.html', 'HoverStates.dc.html', 'SweepPurples.dc.html', 'ColourLab.dc.html', 'AccessibilityPlan.dc.html', 'Main.dc.html'}
GLOBAL = {'514F71': '484454', 'C6C2EA': 'CAC3D7', '2E2D4D': '322E3D', '454364': '484454', '191836': '1D1A28', 'D4D0F9': 'DED7EB',
          '1B5F1F': '0B5314', '6A4E00': '5C4300', '006A6A': '004F50', '50FFAF': 'DCEAB4', '002111': '2A340F', '005232': '404B23'}

def hx(h):  # keep the case of the source
    return h

def sub_hex(s, old, new):
    return re.sub('#' + old + r'\b', lambda m: '#' + (new if m.group(0)[1:].isupper() or m.group(0)[1:].isdigit() else new.lower()), s, flags=re.I)

def block(b):
    if len(b) > 600:   # theme maps and long rules: global maps only
        return b
    has = lambda h: re.search('#' + h + r'\b', b, re.I)
    if has('E3DFFF') and has('191836'):
        b = sub_hex(b, 'E3DFFF', 'DED7EB')
    if has('005232') and has('50FFAF'):
        b = sub_hex(b, '005232', 'DCEAB4'); b = sub_hex(b, '50FFAF', '39235F')
    if has('50FFAF') and has('002111'):   # light tertiary-container chips
        b = sub_hex(b, '50FFAF', 'DCEAB4'); b = sub_hex(b, '002111', '39235F')
    if has('DCEAB4') and has('39235F'):   # Run button: the Sweep purple label stays, the edge goes
        b = re.sub(r'\s*box-shadow:\s*inset 0 0 0 1px #39235F\s*;?', '', b, flags=re.I)
    b = re.sub(r'(background(?:-color)?:\s*)#00F29E', lambda m: m.group(1) + '#BFCC99', b, flags=re.I)
    return b

def recolour(s):
    s = re.sub(r'style="([^"]*)"', lambda m: 'style="' + block(m.group(1)) + '"', s)
    s = re.sub(r'\{([^{}]*)\}', lambda m: '{' + block(m.group(1)) + '}', s)
    s = re.sub(r"'([^'\n]{0,400})'", lambda m: "'" + block(m.group(1)) + "'", s)
    for a, b in GLOBAL.items():
        s = sub_hex(s, a, b)
    s = re.sub(r'rgba\(\s*212,\s*208,\s*249,', 'rgba(222, 215, 235,', s)
    s = discussion(s)
    return s

def rule(s, sel, fn):
    return re.sub(re.escape(sel) + r'\{([^}]*)\}', lambda m: sel + '{' + fn(m.group(1)) + '}', s)

def discussion(s):
    # Discussion panel (5.0.1): white panel, no tint, no primary border or shadow when open, neutral chevron
    s = rule(s, '.qa-panel', lambda b: re.sub(r'background:[^;]+', 'background:' + ('var(--c-ffffff)' if 'var(' in b else '#FFFFFF'), b))
    s = rule(s, '.qa-panel.open', lambda b: '')
    s = rule(s, '.qa-panel .qa-bar', lambda b: re.sub(r'background:[^;]+', 'background:transparent', b))
    s = rule(s, '.qa-panel .qa-bar:hover', lambda b: re.sub(r'background:[^;]+', 'background:rgba(57, 35, 95,.06)', b))
    s = rule(s, '.qa-panel .qa-bar[aria-expanded="true"]', lambda b: re.sub(r'background:[^;]+', 'background:transparent', b))
    s = rule(s, '.qa-ppl .av', lambda b: re.sub(r'box-shadow:0 0 0 2px [^;}]+', 'box-shadow:0 0 0 2px ' + ('var(--c-ffffff)' if 'var(' in b else '#FFFFFF'), b))
    s = rule(s, '.qa-bar .chev', lambda b: re.sub(r'color:[^;]+', 'color:' + ('var(--c-48454e)' if 'var(' in b else '#48454E'), b, count=1))
    return s

dirs = [S + 'artifact-files/41ee9433-6ce3-4631-925e-a51eab1c0cf0/project', S + 'split/labs/project', S + 'split/prototypes/project']
changed = {}
for d in dirs:
    keep = json.load(open(os.path.join(d, 'canvas.json')))['boards']
    for f in sorted(keep):
        if f in SKIP: continue
        p = os.path.join(d, f); s = open(p).read(); n = recolour(s)
        if n != s:
            open(p, 'w').write(n); changed.setdefault(d, []).append(f)
for d, fs in changed.items(): print(d.split('scratchpad/')[1], len(fs), fs)
