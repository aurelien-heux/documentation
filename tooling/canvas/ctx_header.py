"""Apply the header-context rule to the static boards: no breadcrumb, no page title block; the feature name and a
summary sit in the top app bar right of the logo; going back uses a subheader chip.
usage: python3 ctx_header.py <boards dir>  (idempotent)"""
import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import shell as S

D = sys.argv[1]
UI = "Manrope, 'BNPP Type', 'Segoe UI', system-ui, sans-serif"
BACK = '<path d="M15 6l-6 6 6 6"/>'

def back_chip(label, dark=False):
    fg, bd = ('#ECE5F8', '#948DA5') if dark else ('#1C1B1E', '#79757F')
    return (f'<span style="display: inline-flex; align-items: center; gap: 6px; height: 32px; padding: 0 12px 0 8px; border-radius: 8px; border: 1px solid {bd}; color: {fg}; font-family: {UI}; font-size: 14px; font-weight: 500; white-space: nowrap">'
            f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{BACK}</svg>{label}</span>')

CRUMB = re.compile(r'<div style="display: flex;(?: align-items: center;)? gap: 8px; font-family: \'Open Sans\', system-ui, sans-serif; font-size: 12px; color: #[0-9A-F]{6}"><span>(Workspace|Docs|Settings)</span>.*?</div>', re.S)
LOGO_END = 'Toolbox</span></span></div></div>'

def insert_ctx(seg, feature, summary, dark):
    # seg = one header's markup; the logo cell is <div style="justify-self: start"><div ...>LOGO</div></div>
    if 'class="hctx"' in seg: return seg
    i = seg.find('<div style="justify-self: start">')
    if i < 0: return seg
    j = seg.find(LOGO_END, i)
    if j < 0: return seg
    j += len(LOGO_END) - len('</div>')
    out = seg[:i] + '<div style="justify-self: stretch; display: flex; align-items: center; min-width: 0; overflow: hidden">' + seg[i + len('<div style="justify-self: start">'):j] + S.ctx(feature, summary, dark) + seg[j:]
    return out

def process(path, feature, summary):
    s = open(path, encoding='utf-8').read(); orig = s
    # 1 · breadcrumbs
    s = CRUMB.sub('', s)
    # 2 · AppShell title block: <div align flex-end gap 16px><div flex 1><h1>Sweep</h1><p>summary</p></div>BUTTONS…
    TB = re.compile(r'<div style="display: flex; align-items: flex-end; gap: 16px"><div style="flex: 1"><h1[^>]*>([^<]*)</h1><p[^>]*>([^<]*)</p></div>')
    found = TB.search(s)
    if found:
        feature, summary = found.group(1), found.group(2)
        s = TB.sub('<div style="display: flex; align-items: center; justify-content: flex-end; gap: 16px">', s)
    # 3 · Feedback boards: three screens, each with its own title block → subheader with a back chip, context in the header
    FB = re.compile(r'<div style="display: flex; align-items: flex-end; gap: 12px"><div style="flex: 1; display: flex; flex-direction: column; gap: 6px"><div style="display: flex; align-items: center; gap: 12px"><span style="[^"]*font-size: 30px[^"]*">([^<]*)</span>(<span[^>]*>[^<]*</span>)</div><span style="[^"]*">([^<]*)</span></div>')
    SCREENS = {
        'Sweep run #482': ('Runs', 'Sweep · Run #482'),
        'Feedback · Sweep': ('Listening', 'Administration · Community'),
    }
    def rep(mm):
        back = SCREENS.get(mm.group(1), ('Back',))[0]
        return ('<div style="display: flex; align-items: center; gap: 12px">' + back_chip(back) +
                f'<span style="font-family: {UI}; font-size: 18px; line-height: 24px; font-weight: 600; color: #1C1B1E">{mm.group(1)}</span>{mm.group(2)}<span style="flex: 1"></span>')
    # 4 · AssistantLive
    s = s.replace('<div class="crumbs">Sweep</div>\n      <h1>Runs</h1>\n', '')
    # 5 · per header: context block, title block, docs crumb
    parts = re.split(r'(<header[^>]*>)', s)
    for k in range(1, len(parts), 2):
        dark = '#1D1A27' in parts[k]
        seg = parts[k + 1]
        f2, s2 = feature, summary
        m = FB.search(seg)
        if m:
            t = m.group(1)
            if t in SCREENS:
                f2 = SCREENS[t][1]
                s2 = m.group(3) if t == 'Sweep run #482' else 'Listening · feedback profile · Sweep'
            seg = FB.sub(rep, seg)
        if 'Rotate a secret' in seg:
            f2, s2 = 'Docs · Platform guide', 'Secrets · updated 3 days ago · 4 min read'
            seg = seg.replace('<div style="max-width: 720px; display: flex; flex-direction: column; gap: 14px"><span style="font-family: Manrope',
                              '<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 4px">' + back_chip('Platform guide', True) + '</div><div style="max-width: 720px; display: flex; flex-direction: column; gap: 14px"><span style="font-family: Manrope', 1)
        parts[k + 1] = insert_ctx(seg, f2, s2, dark)
    s = ''.join(parts)
    if s != orig:
        open(path, 'w', encoding='utf-8').write(s)
    return s != orig

PLAN = {
    'AppShell': ('Sweep', '24 pipelines across 4 environments · last sync 2 min ago'),
    'AppShellDark': ('Sweep', '24 pipelines across 4 environments · last sync 2 min ago'),
    'AppShellOverlays': ('Sweep', '24 pipelines across 4 environments · last sync 2 min ago'),
    'AppShellOverlaysDark': ('Sweep', '24 pipelines across 4 environments · last sync 2 min ago'),
    'AppShellRail': ('Sweep', '24 pipelines across 4 environments · last sync 2 min ago'),
    'AppShellRailDark': ('Sweep', '24 pipelines across 4 environments · last sync 2 min ago'),
    'Feedback': ('Sweep · Run #482', 'credit-request · 7 phases · 14 min 01 s · started by Aurélien Heux'),
    'FeedbackLive': ('Sweep · Run #482', 'credit-request · 7 phases · 14 min 01 s · started by Aurélien Heux'),
    'HeaderIdeas': ('Sweep · Runs', '24 pipelines across 4 environments · last sync 2 min ago'),
    'HeaderIdeasLive': ('Sweep · Runs', '24 pipelines across 4 environments · last sync 2 min ago'),
    'Tooltip': ('Sweep · Runs', 'staging · credit-request'),
}
for name, (f, sm) in PLAN.items():
    p = os.path.join(D, name + '.dc.html')
    if os.path.exists(p):
        print(name, 'changed' if process(p, f, sm) else 'unchanged')
