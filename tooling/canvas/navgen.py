"""Canonical AIToolbox navigation (Oct 2026): no Dashboard, Settings in the account menu,
Cookie policy (cookie icon) replaces Privacy. Replaces every <nav> drawer / rail in the given boards."""
import re, sys, itertools

UI = "Manrope, 'BNPP Type', 'Segoe UI', system-ui, sans-serif"
LIGHT = dict(bg='#EDE4FF', fg='#48454E', abg='#D4D0F9', afg='#191836', alab='#1C1B1E', bar='#35307E',
             p='#35307E', a='#278383', g='#00A56B', g1='#278383', inner='#FDF8FD', theme='l')
DARK = dict(bg='#1D1A27', fg='#CAC3DC', abg='#454364', afg='#E3DFFF', alab='#ECE5F8', bar='#C4C0FF',
            p='#A6A2F8', a='#80D5D4', g='#00F29E', g1='#80D5D4', inner='#14121E', theme='d')
_uid = itertools.count(1)

def mark(key, t, size=24):
    u = next(_uid)
    if key == 'sweep':
        return (f'<svg width="{size}" height="{size}" viewBox="0 0 64 64" aria-hidden="true" style="overflow:visible; flex: none"><defs>'
                f'<linearGradient id="nvg{u}" gradientUnits="userSpaceOnUse" x1="0" y1="35" x2="0" y2="61"><stop offset="0" stop-color="{t["a"]}"/><stop offset="1" stop-color="{t["g"]}"/></linearGradient>'
                f'<mask id="nvm{u}" maskUnits="userSpaceOnUse" x="-20" y="-20" width="104" height="104"><rect x="-20" y="-20" width="104" height="104" fill="#fff"/>'
                '<path d="M25.5 48L23.9 62" stroke="#000" stroke-width="2.6" stroke-linecap="round"/><path d="M32 48L32.0 62" stroke="#000" stroke-width="2.6" stroke-linecap="round"/><path d="M38.5 48L40.1 62" stroke="#000" stroke-width="2.6" stroke-linecap="round"/></mask></defs>'
                f'<g transform="translate(-0.8 -3.6)"><g transform="rotate(32 32 34)"><path d="M32 4V28" stroke="{t["p"]}" stroke-width="6.5" stroke-linecap="round"/><rect x="21" y="26" width="22" height="9" rx="3.5" fill="{t["p"]}"/>'
                f'<path d="M24 35H40L49 56.5Q50 61 45.5 61H18.5Q14 61 15 56.5Z" fill="url(#nvg{u})" mask="url(#nvm{u})"/></g>'
                f'<path d="M50 41.5C51.53 48.47 51.53 48.47 58.5 50C51.53 51.53 51.53 51.53 50 58.5C48.47 51.53 48.47 51.53 41.5 50C48.47 48.47 48.47 48.47 50 41.5Z" fill="{t["g"]}"/>'
                f'<path d="M58.5 33C59.22 36.28 59.22 36.28 62.5 37C59.22 37.72 59.22 37.72 58.5 41C57.78 37.72 57.78 37.72 54.5 37C57.78 36.28 57.78 36.28 58.5 33Z" fill="{t["g1"]}"/></g></svg>')
    if key == 'env':
        return (f'<svg width="{size}" height="{size}" viewBox="0 0 64 64" aria-hidden="true" style="overflow:visible; flex: none"><g transform="translate(-0.2 0.2)">'
                f'<path d="M12 50L32 32L52 14" stroke="{t["p"]}" stroke-opacity=".35" stroke-width="5" stroke-linecap="round" fill="none"/>'
                f'<circle cx="12" cy="50" r="7" fill="{t["inner"]}" stroke="{t["p"]}" stroke-width="5"/><circle cx="32" cy="32" r="7.5" fill="{t["inner"]}" stroke="{t["a"]}" stroke-width="5"/>'
                f'<circle cx="52" cy="14" r="10" fill="{t["g"]}"/><path d="M47.5 14.2l3 3 6-6" fill="none" stroke="{t["inner"]}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></g></svg>')
    if key == 'docs':
        return (f'<svg width="{size}" height="{size}" viewBox="0 0 64 64" aria-hidden="true" style="overflow:visible; flex: none"><g transform="translate(-2.7 -2.5)">'
                f'<rect x="6" y="10" width="13" height="48" rx="3.5" fill="{t["p"]}"/><path d="M9.5 20H15.5" stroke="{t["inner"]}" stroke-width="2.6" stroke-linecap="round"/>'
                f'<rect x="22" y="16" width="13" height="42" rx="3.5" fill="{t["a"]}"/><path d="M25.5 25H31.5" stroke="{t["inner"]}" stroke-width="2.6" stroke-linecap="round"/>'
                f'<rect x="38" y="13" width="13" height="46" rx="3.5" fill="{t["g"]}" transform="rotate(16 51 58)"/></g></svg>')
    if key == 'new':
        return (f'<svg width="{size}" height="{size}" viewBox="0 0 64 64" aria-hidden="true" style="overflow:visible; flex: none">'
                f'<path d="M8 27a5 5 0 0 1 5-5h9l20-11v42L22 42h-9a5 5 0 0 1-5-5z" fill="{t["p"]}"/><path d="M16 43l4 11a3 3 0 0 0 3 2h3a2 2 0 0 0 2-2.6L24.5 43z" fill="{t["a"]}"/>'
                f'<path d="M52 15.5c1.53 6.97 1.53 6.97 8.5 8.5-6.97 1.53-6.97 1.53-8.5 8.5-1.53-6.97-1.53-6.97-8.5-8.5 6.97-1.53 6.97-1.53 8.5-8.5z" fill="{t["g"]}"/>'
                f'<path d="M56 39c.72 3.28.72 3.28 4 4-3.28.72-3.28.72-4 4-.72-3.28-.72-3.28-4-4 3.28-.72 3.28-.72 4-4z" fill="{t["a"]}"/></svg>')
    if key == 'catalog':
        # Catalog · four tiles: three filled (primary, ai, tertiary) and one open slot with a plus: pieces you add to your toolbox
        return (f'<svg width="{size}" height="{size}" viewBox="0 0 64 64" aria-hidden="true" style="overflow:visible; flex: none">'
                f'<rect x="8" y="8" width="22" height="22" rx="6" fill="{t["p"]}"/><rect x="34" y="8" width="22" height="22" rx="6" fill="{t["a"]}"/><rect x="8" y="34" width="22" height="22" rx="6" fill="{t["g"]}"/>'
                f'<rect x="35.5" y="35.5" width="19" height="19" rx="5" fill="none" stroke="{t["p"]}" stroke-width="3" stroke-dasharray="4 3"/><path d="M45 40v10M40 45h10" stroke="{t["p"]}" stroke-width="3.2" stroke-linecap="round"/></svg>')
    raise KeyError(key)

STROKE = 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
ICON = {
    'secrets': '<circle cx="8" cy="12" r="4"/><path d="M12 12h9M18 12v3M15 12v2"/>',
    'logs': '<path d="M5 4h14v16H5zM8 8h8M8 12h8M8 16h5"/>',
    'tools': '<path d="M14 7a4 4 0 0 1 5 5l-9 9-3-3 9-9M5 19l-1 1"/>',
    'cookie': '<path d="M21 12.3A9 9 0 1 1 11.7 3a3 3 0 0 0 3.3 3.6 3 3 0 0 0 3.4 3.4 3 3 0 0 0 2.6 2.3z"/><path d="M8.5 9.5h.01M15.5 15.5h.01M9.5 15h.01M12.5 12h.01"/>',
    'menu': '<path d="M3 6h18M3 12h18M3 18h18"/>',
    'admin': '<path d="M12 3l7 3v5c0 4.6-3 8.4-7 10-4-1.6-7-5.4-7-10V6z"/><circle cx="12" cy="10.5" r="2.5"/><path d="M8.5 16.5c.8-1.6 2-2.4 3.5-2.4s2.7.8 3.5 2.4"/>',
    'ext': '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
}
def icon(k, size=22):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" {STROKE} style="flex: none; margin: 0 1px">{ICON[k]}</svg>'

ITEMS = [('sweep', 'Sweep', 'mark', '3'), ('env', 'Environments', 'mark', ''), ('docs', 'Docs', 'mark', ''), ('new', 'Community', 'mark', '3 new')]
CATALOG_ITEM = ('catalog', 'Catalog', 'mark', '')
def items(catalog=False):
    return ITEMS[:3] + ([CATALOG_ITEM] if catalog else []) + ITEMS[3:]

def drawer(t, active='sweep', version='v4.6.0', admin=True, catalog=False):
    sec = lambda txt: f'<div style="padding: 18px 16px 8px; font-family: {UI}; font-size: 12px; font-weight: 600; letter-spacing: .5px; color: {t["fg"]}">{txt}</div>'
    out = [f'<nav aria-label="Primary" class="nav-side nav-drawer" style="width: 300px; flex: none; display: flex; flex-direction: column; padding: 12px; box-sizing: border-box; background: {t["bg"]}">',
           f'<div style="height: 48px; display: flex; align-items: center; padding: 0 4px"><button type="button" aria-label="Collapse navigation" style="position: relative; width: 40px; height: 40px; border: 0; border-radius: 999px; background: transparent; color: {t["fg"]}; display: inline-flex; align-items: center; justify-content: center; margin: 4px">{icon("menu")}</button></div>',
           sec('Workspace')]
    for it in items(catalog):
        if it is None:
            out.append(sec('Platform')); continue
        k, label, kind, cnt = it
        on = k == active
        g = mark(k, t) if kind == 'mark' else icon(k)
        st = (f'background: {t["abg"]}; color: {t["afg"]}; box-shadow: inset 3px 0 0 {t["bar"]}; font-weight: 700' if on
              else f'background: transparent; color: {t["fg"]}; font-weight: 500')
        lab = t['alab'] if on else t['fg']
        c = f'<span style="font-family: {UI}; font-size: 12px; font-weight: 600; color: {t["afg"] if on else t["fg"]}">{cnt}</span>' if cnt else ''
        cur = ' aria-current="page"' if on else ''
        out.append(f'<a href="#{k}"{cur} style="display: flex; align-items: center; gap: 12px; height: 56px; padding: 0 24px 0 16px; border-radius: 16px; {st}; font-family: {UI}; font-size: 14px; text-decoration: none">{g}<span style="flex: 1; color: {lab}">{label}</span>{c}</a>')
    out.append('<div style="flex: 1"></div>')
    if admin:
        out.append(admin_drawer_item(t, active == 'admin'))
    out.append(f'<a href="#cookies" target="_blank" rel="noopener" style="display: flex; align-items: center; gap: 12px; height: 56px; padding: 0 24px 0 16px; border-radius: 16px; background: transparent; color: {t["fg"]}; font-family: {UI}; font-size: 14px; font-weight: 500; text-decoration: none">{icon("cookie")}<span style="flex: 1; color: {t["fg"]}">Cookie policy</span>{icon("ext", 18)}</a>')
    out.append('</nav>')
    return ''.join(out)

def rail(t, active='sweep', version='v4.6.0', admin=True, catalog=False):
    def item(k, label, g, on=False, href=None, ext=False):
        st = (f'background: {t["abg"]}; box-shadow: inset 3px 0 0 {t["bar"]}; color: {t["afg"]}' if on else f'background: transparent; color: {t["fg"]}')
        lab = (f'font-weight: 700; color: {t["alab"]}' if on else f'font-weight: 500; color: {t["fg"]}')
        cur = ' aria-current="page"' if on else ''
        tgt = ' target="_blank" rel="noopener"' if ext else ''
        return (f'<a href="{href or "#" + k}"{cur}{tgt} title="{label}" style="display: flex; flex-direction: column; align-items: center; gap: 4px; width: 72px; text-decoration: none">'
                f'<span style="position: relative; width: 56px; height: 32px; border-radius: 16px; {st}; display: inline-flex; align-items: center; justify-content: center">{g}</span>'
                f'<span style="font-family: {UI}; font-size: 11px; letter-spacing: -.1px; {lab}; white-space: nowrap">{label}</span></a>')
    out = [f'<nav aria-label="Primary" class="nav-side nav-rail" style="width: 80px; flex: none; display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 12px 0; box-sizing: border-box; background: {t["bg"]}">',
           f'<div style="height: 48px; display: flex; align-items: center"><button type="button" aria-label="Open navigation" style="position: relative; width: 40px; height: 40px; border: 0; border-radius: 999px; background: transparent; color: {t["fg"]}; display: inline-flex; align-items: center; justify-content: center; margin: 4px">{icon("menu")}</button></div>']
    short = {}
    for it in items(catalog):
        if it is None:
            break  # Platform items live in the drawer opened from the rail menu
        k, label, kind, cnt = it
        out.append(item(k, short.get(k, label), mark(k, t), on=(k == active)))
    out.append('<div style="flex: 1"></div>')
    if admin:
        out.append(item('admin', 'Admin', icon('admin'), on=(active == 'admin')))
    out.append(item('cookies', 'Cookies', icon('cookie'), href='#cookies', ext=True))
    out.append('</nav>')
    return ''.join(out)

def admin_drawer_item(t, on=False):
    st = (f'background: {t["abg"]}; color: {t["afg"]}; box-shadow: inset 3px 0 0 {t["bar"]}; font-weight: 700' if on
          else f'background: transparent; color: {t["fg"]}; font-weight: 500')
    cur = ' aria-current="page"' if on else ''
    return (f'<a href="#admin"{cur} style="display: flex; align-items: center; gap: 12px; height: 56px; padding: 0 24px 0 16px; border-radius: 16px; {st}; font-family: {UI}; font-size: 14px; text-decoration: none">'
            f'{icon("admin")}<span style="flex: 1; color: {t["alab"] if on else t["fg"]}">Administration</span></a>')

def admin_rail_item(t, on=False):
    return rail(t, 'admin' if on else 'none', admin=True).split('<div style="flex: 1"></div>')[1].split('<a href="#cookies"')[0]

def replace_navs(path, builder):
    s = open(path, encoding='utf-8').read()
    navs = list(re.finditer(r'<nav\b.*?</nav>', s, flags=re.S))
    res, last = [], 0
    for i, m in enumerate(navs):
        new = builder(i, m.group(0))
        if new is None:
            continue
        res.append(s[last:m.start()]); res.append(new); last = m.end()
    res.append(s[last:])
    s2 = ''.join(res)
    open(path, 'w', encoding='utf-8').write(s2)
    return len(navs)
