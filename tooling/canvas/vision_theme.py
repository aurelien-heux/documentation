"""Light and dark themes for the production vision, as a token pass over the assembled page.

Every colour literal of the light design (CSS rules, inline styles, colours produced by the logic) becomes a CSS custom
property `--c-<hex>`; one block holds the light values, one the dark values of the design system (DSR-02, component
rules), applied by `data-theme="dark"` on the window frame or by the viewer's system preference when the frame says
`system`. SVG presentation attributes keep their light literal and are re-coloured by attribute selectors. Surfaces that
are dark by design in the light theme (the console, source blocks) keep their light-theme colours in dark.
Light renders exactly as before: the tokens resolve to the same values."""
import re

# light → dark, by design-system role. A hex used in two roles is split by property: FFFFFF as a background is
# surface-container-lowest (0F0C19), as text or an icon it is on-primary (2A2473).
DARK = {
    'FDF8FD': '14121E', 'FFFFFF': '0F0C19', 'FAF4FF': '1D1A27', 'F8F1FF': '23202D', 'F2EBFA': '2B2836', 'ECE5F4': '363341', 'E6E0EC': '3D3A48', 'E6E1E6': '3D3A48',
    'F7F2FA': '1D1A27', 'EFE7F7': '23202D', 'ECDDF6': '2B2836', 'F4EFF4': '322E3C', 'EDE4FF': '1D1A27', 'D4D0F9': '454364', 'CAC4CF': '494458', 'A9A4AE': '8F8A96',
    'B9B4BE': '5F5B66', '79757F': '948DA5', '49454F': 'CAC3DC', '48454E': 'CAC3DC', '1C1B1E': 'ECE5F8', '191836': 'E3DFFF', '14085E': 'E3DFFF', '322F37': 'E6E1E6',
    '313033': 'E6DFF2', '1D1A27': 'ECE5F8', 'CAC3DC': '48454E', 'ECE5F8': '1C1B1E',
    '35307E': 'C4C0FF', 'C4C0FF': '413C8A', 'E3DFFF': '454364', '0D0B14': 'ECE5F8', '00F29E': '006C44', '2A2473': 'FFFFFF',
    '9CF1F0': '004F50', '002020': '9CF1F0', '80D5D4': '80D5D4', '003737': '003737', '006A6A': '80D5D4', '278383': '80D5D4', 'E0FBFA': '004F50', 'F2FBFB': '004F50', '8C88C8': '8C88C8',
    '1B5F1F': '91D888', 'ACF4A2': '0B3910', '0B3910': 'ACF4A2', '2C5A1C': '91D888', 'D5EDC7': '1C5631', 'CBE7D4': '1C5631', 'E8F7EE': '0B3910', 'C3F4DC': '005232', '00391E': 'C3F4DC',
    '006D3B': '7DDBA4', '7DDBA4': '006D3B', '00A56B': '00F29E', '008857': '00F29E', '006C46': '50FFAF', '1C5631': '91D888',
    '6A4E00': 'FCBC00', 'FFDEA0': '5E5000', '5E5000': 'FFDEA0', 'FFF2B3': '3D3500', '3D3500': 'FFF2B3', '3F2E00': 'FFF2B3', '261900': 'FFDEA0', '7A5900': 'FFDEA0', '7A4000': 'FFDCC2',
    'FFDCC2': '7A4000', '4A2800': 'FFDCC2', '6E4A0E': 'F0D58C', 'F0D58C': '6E4A0E', 'FBE3C8': '6E4A0E', 'F8E5C4': '3F2E00', 'B88A2B': 'F0D58C', 'E8A400': 'FCBC00', 'FFF8E6': '3D3500', 'FFF4DE': '3F2E00',
    '93000A': 'FFB4AB', 'FFDAD6': '93000A', '410002': 'FFDAD6', 'BA1A1A': 'FFB4AB', 'FFB4AB': '93000A', 'FFEDEA': '410002',
    'CFEDFA': '0A5570', '0A5570': 'CFEDFA', '7A2457': 'F2B8D9', 'F6DCEB': '7A2457', 'F2B8D9': '7A2457', '5A2C80': 'D4D0F9',
}
TEXT_WHITE = '2A2473'
TEXT_PROPS = {'color', 'fill', 'stroke', 'caret-color', '-webkit-text-fill-color'}
DARK_SURFACES = '.sw-con, .lc-src, .srcbox, pre.code'
HEX = re.compile(r'#([0-9A-Fa-f]{6})\b')
LAYER = re.compile(r'rgba\(53,\s*48,\s*126,\s*(\.?\d*\.?\d+)\)')


def tok(h, text=False):
    return 'var(--c-' + h.lower() + ('-t' if text else '') + ')'


def value_pass(val, is_text):
    def hx(m):
        h = m.group(1).upper()
        if h not in DARK: return m.group(0)
        return tok(h, h == 'FFFFFF' and is_text)
    val = re.sub(r'#fff\b(?![0-9A-Fa-f])', '#FFFFFF', val, flags=re.I)
    val = HEX.sub(hx, val)
    return LAYER.sub(lambda m: 'color-mix(in srgb, var(--c-35307e) ' + str(round(float(m.group(1)) * 100)) + '%, transparent)', val)


def decls_pass(block):
    """prop: value pairs of a declaration list (a rule body or an inline style)."""
    def one(m):
        prop = m.group(1).strip().lower()
        return m.group(1) + ':' + m.group(2) + value_pass(m.group(3), prop in TEXT_PROPS)
    return re.sub(r'([a-zA-Z-]+)\s*:(\s*)([^;{}"]*)', one, block)


def css_pass(css):
    return re.sub(r'\{([^{}]*)\}', lambda m: '{' + decls_pass(m.group(1)) + '}', css)


def inline_pass(html):
    return re.sub(r'style="([^"]*)"', lambda m: 'style="' + decls_pass(m.group(1)) + '"', html)


def js_pass(js):
    def hx(m):
        h = m.group(1).upper()
        if h not in DARK: return m.group(0)
        pre = js[max(0, m.start() - 40):m.start()]
        is_text = h == 'FFFFFF' and bool(re.search(r'(fg|color|stroke|fill|ink)\s*[:=]\s*[\'"`]?\s*$', pre))
        return tok(h, is_text)
    return HEX.sub(hx, js)


def tokens_css():
    light = ''.join(f'--c-{k.lower()}:#{k};' for k in DARK) + '--c-ffffff-t:#FFFFFF;'
    dark = ''.join(f'--c-{k.lower()}:#{v};' for k, v in DARK.items()) + f'--c-ffffff-t:#{TEXT_WHITE};'
    attr = ''.join(f'.simframe [fill="#{k}"]{{fill:var(--c-{k.lower()})}}.simframe [stroke="#{k}"]{{stroke:var(--c-{k.lower()})}}' for k in DARK if k != 'FFFFFF')
    attr += '.simframe [fill="#FFFFFF"]{fill:var(--c-ffffff-t)}.simframe [stroke="#FFFFFF"]{stroke:var(--c-ffffff-t)}'
    logo = [('[fill="#0D0B14"]', 'fill:#C4C0FF'), ('[stroke="#0D0B14"]', 'stroke:#C4C0FF'), ('[stroke="#FFFFFF"]', 'stroke:#0D0B14'), ('[fill="#FFFFFF"]', 'fill:#0D0B14')]
    def darkblock(sel):
        return (f'{sel}{{{dark}color-scheme:dark}}'
                f'{sel} :is({DARK_SURFACES}){{{light}}}'
                + ''.join(f'{sel} a[aria-label="AIToolbox home"] {s}{{{d}}}' for s, d in logo))
    return ('\n/* ---- themes: light values, dark values (DSR-02), applied by data-theme or the system preference ---- */\n'
            f':root,.simframe{{{light}}}.simframe{{color-scheme:light}}\n'
            + darkblock('.simframe[data-theme="dark"]') + '\n'
            + '@media (prefers-color-scheme: dark){' + darkblock('.simframe[data-theme="system"]') + '}\n'
            + attr + '\n')


def apply(out):
    i = out.index('<script type="text/x-dc"')
    html, js = out[:i], out[i:]
    a = html.index('<style>'); b = html.index('</style>')
    html = inline_pass(html[:a]) + '<style>' + css_pass(html[a + 7:b]) + tokens_css() + '</style>' + inline_pass(html[b + 8:])
    return html + js_pass(js)
