"""The AIToolbox ArchiMate notation (design system 4.5), as used by the Docs lab architecture space.

Source of truth: the ArchiMate notation page (archimate_notation.json = its notation.json: 62 element types with layer,
aspect, shape and 24 px glyph; 11 relationships with line style and end markers; the change chips) and its CSS
(archimate_ds.css: .ax-box figures, .ax-tile, .ax-change, .ax-track, review components). Nothing here redefines a
colour, a shape or a glyph: the type decides everything."""
import os, json, re, html, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
N = json.load(open(os.path.join(HERE, 'archimate_notation.json'), encoding='utf-8'))
TYPES = {e['name']: e for e in N['elements']}          # 'Application component' -> element type
RELS = {r['id']: r for r in N['relationships']}
LAYERS = {l['id']: l for l in N['layers']}
CHANGE = {c['id']: c for c in N['change']}

# light theme only in the lab; the roles are the AIToolbox token values (tokens 4.5.0)
TOKENS = ('.arch-ds{--md-sys-color-primary:#35307E;--md-sys-color-on-primary:#FFFFFF;--md-sys-color-secondary-container:#E3DFFF;--md-sys-color-on-secondary-container:#191836;'
          '--md-sys-color-surface:#FDF8FD;--md-sys-color-surface-container-lowest:#FFFFFF;--md-sys-color-surface-container-low:#FAF4FF;--md-sys-color-surface-container:#F8F1FF;--md-sys-color-surface-container-high:#F2EBFA;--md-sys-color-surface-container-highest:#ECE5F4;'
          '--md-sys-color-on-surface:#1C1B1E;--md-sys-color-on-surface-variant:#48454E;--md-sys-color-outline:#79757F;--md-sys-color-outline-variant:#CAC4CF;--md-sys-color-focus-ring:#35307E;'
          '--md-sys-color-success:#1B5F1F;--md-sys-color-on-success:#FFFFFF;--md-sys-color-success-container:#ACF4A2;--md-sys-color-on-success-container:#1B5F1F;'
          '--md-sys-color-warning:#6A4E00;--md-sys-color-on-warning:#FFFFFF;--md-sys-color-warning-container:#FFDEA0;--md-sys-color-on-warning-container:#6A4E00;'
          '--md-sys-color-error:#93000A;--md-sys-color-on-error:#FFFFFF;--md-sys-color-error-container:#FFDAD6;--md-sys-color-on-error-container:#410002;'
          "--md-sys-typescale-brand-family:'BNPP Type','Manrope','Segoe UI',system-ui,sans-serif;--md-sys-typescale-plain-family:'Open Sans','Segoe UI',system-ui,sans-serif;"
          + ''.join(f'--ax-{l["id"]}-fill:{l["light"]["fill"]};--ax-{l["id"]}-ink:{l["light"]["ink"]};' for l in N['layers']) + '}\n')

_css = open(os.path.join(HERE, 'archimate_ds.css'), encoding='utf-8').read()
# review components are page-level classes in the notation page: scope them to the architecture space
_i = _css.index('/* review components */')
_rev = re.sub(r'/\*.*?\*/', '', _css[_i + len('/* review components */'):], flags=re.S)
_rev = re.sub(r'(^|\})\s*([^{}@]+)\{', lambda m: m.group(1) + '\n' + ','.join('.arch-ds ' + x.strip() for x in m.group(2).split(',')) + '{', _rev)
CSS = TOKENS + _css[:_i] + _rev

def svg_glyph(t, cls='ax-glyph'):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{TYPES[t]["svg"]}</svg>')

def glyph_masks(type_names):
    """One CSS class per glyph, for type tiles inside lists (sc-for cannot carry raw SVG): .axg-<id>."""
    out = ['.ax-tile i.axg,.axg{display:block;width:16px;height:16px;background:currentColor;-webkit-mask:var(--g) center/contain no-repeat;mask:var(--g) center/contain no-repeat}',
           '.ax-tile.lg i.axg{width:24px;height:24px}']
    for t in sorted(set(type_names)):
        e = TYPES[t]
        s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="black" stroke-width="1.6" '
             f'stroke-linecap="round" stroke-linejoin="round">{e["svg"].replace("currentColor", "black")}</svg>')
        out.append(f'.axg-{e["id"]}{{--g:url("data:image/svg+xml,{urllib.parse.quote(s, safe="")}")}}')
    return '\n'.join(out)

# end markers, local coordinates: tip at (0,0), pointing along +x (DS shapes from the notation page)
MARK = {
    'arrow': ('<path d="M0 0L-10 -5V5Z" fill="currentColor"/>', 10),
    'open': ('<path d="M-10 -6L0 0L-10 6" fill="none" stroke="currentColor" stroke-width="1.6"/>', 0),
    'small': ('<path d="M-7 -4L0 0L-7 4" fill="none" stroke="currentColor" stroke-width="1.6"/>', 0),
    'triangle': ('<path d="M0 0L-11 -6V6Z" fill="#FFFFFF" stroke="currentColor" stroke-width="1.4"/>', 11),
    'diamond': ('<path d="M0 0L-6 -4L-12 0L-6 4Z" fill="currentColor"/>', 12),
    'odiamond': ('<path d="M0 0L-6 -4L-12 0L-6 4Z" fill="#FFFFFF" stroke="currentColor" stroke-width="1.4"/>', 12),
    'dot': ('<circle cx="-3" cy="0" r="3" fill="currentColor"/>', 3),
    'none': ('', 0),
}
DASH = {'solid': '', 'dashed': ' stroke-dasharray="6 4"', 'dotted': ' stroke-dasharray="2 3"'}

def rel_sample(rel_id, w=56):
    """A short relationship line with its markers, for legends and relationship lists."""
    r = RELS[rel_id]
    hm, hl = MARK[r['target']]; tm, tl = MARK[r['source']]
    col = '#48454E' if rel_id == 'association' else '#1C1B1E'
    return (f'<svg width="{w}" height="14" viewBox="0 0 {w} 14" aria-hidden="true" style="color: {col}; flex: none">'
            f'<line x1="{2 + tl}" y1="7" x2="{w - 2 - hl}" y2="7" stroke="currentColor" stroke-width="1.6"{DASH[r["line"]]}/>'
            f'<g transform="translate({w - 2} 7)">{hm}</g><g transform="translate(2 7) rotate(180)">{tm}</g></svg>')

def esc(s):
    return html.escape(str(s), quote=True)
