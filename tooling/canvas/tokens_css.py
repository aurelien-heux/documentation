"""Regenerate tokens.css from tokens.json (the source of truth). Usage: python3 tokens_css.py <project dir>"""
import sys, os, json
D = sys.argv[1]
t = json.load(open(os.path.join(D, 'tokens.json'), encoding='utf-8'))
cmt = lambda s: (' /* ' + s.replace('*/', '* /') + ' */') if s else ''
out = [f'/* {t.get("name", "AIToolbox")} {t.get("version", "")} — generated from tokens.json; edit tokens.json, not this file */']
for f in t['type'].get('fonts', []):
    out.append(f"@font-face {{\n  font-family: '{f['family']}';\n  src: url('{f['file']}') format('woff2');\n  font-weight: {f.get('weight', '400')};\n  font-style: {f.get('style', 'normal')};\n  font-display: swap;\n}}")
cols = t['color']['tokens']
out.append(':root, [data-theme="light"] {\n  color-scheme: light;')
out += [f'  --{c["name"]}: {c["value"]["light"]};{cmt(c.get("usage", ""))}' for c in cols]
out += [f'  --{x["name"]}: {x["value"]};{cmt(x.get("usage", ""))}' for x in t['shadow']['tokens']]
out.append('}')
out.append('[data-theme="dark"] {\n  color-scheme: dark;')
out += [f'  --{c["name"]}: {c["value"]["dark"]};' for c in cols]
out.append('}')
out.append(':root {')
out += [f'  --{x["name"]}: {x["value"]};{cmt(x.get("usage", ""))}' for x in t['spacing']['tokens'] + t['radius']['tokens']]
out += [f'  --{x["name"]}: {x["value"]};{cmt(x.get("usage", ""))}' for x in t.get('breakpoint', {}).get('tokens', []) + t.get('layout', {}).get('tokens', [])]
fam = t['type']['families']
out += [f'  --font-ui: {fam["ui"]};', f'  --font-brand: {fam["ui"]};', f'  --font-body: {fam["body"]};', f'  --font-plain: {fam["plain"]};']
styles = []
for g in t['type']['groups']:
    for s in g['styles']:
        fv = 'var(--font-' + {'ui': 'ui', 'body': 'body', 'plain': 'plain'}[s.get('family', g['family'])] + ')'
        styles.append((s, fv))
        out.append(f'  --text-{s["name"]}: {s["fontWeight"]} {s["fontSize"]}/{s["lineHeight"]} {fv};{cmt(s.get("usage", ""))}')
out.append('}')
for s, fv in styles:
    out.append(f'.{s["name"]} {{\n  font-family: {fv};\n  font-size: {s["fontSize"]};\n  line-height: {s["lineHeight"]};\n  font-weight: {s["fontWeight"]};\n  letter-spacing: {s["letterSpacing"]};\n}}')
open(os.path.join(D, 'tokens.css'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('tokens.css', len(cols), 'colours')
