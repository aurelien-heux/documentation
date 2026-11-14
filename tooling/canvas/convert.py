"""Convert canvas boards (.dc.html) into self-contained HTML pages that run in any browser.
usage: python3 convert.py <src_dir> <out_dir>"""
import os, re, sys, html, json

HERE = os.path.dirname(os.path.abspath(__file__))
RUNTIME = open(os.path.join(HERE, 'dc-standalone.js'), encoding='utf-8').read()

def between(s, a, b):
    i = s.find(a)
    if i < 0: return None, -1, -1
    j = s.find(b, i + len(a))
    return s[i + len(a):j], i, j + len(b)

def convert(src):
    s = open(src, encoding='utf-8').read()
    title = (re.search(r'<title>(.*?)</title>', s, re.S) or [None, 'AIToolbox'])[1]
    xdc, _, _ = between(s, '<x-dc>', '</x-dc>')
    helmet, hi, hj = between(xdc, '<helmet>', '</helmet>')
    body = xdc[:hi] + xdc[hj:] if helmet is not None else xdc
    m = re.search(r'<script type="text/x-dc" data-dc-script[^>]*>(.*?)</script>', s, re.S)
    logic = m.group(1) if m else ''
    props = re.search(r"data-props='(.*?)'", s, re.S)
    width = None
    if props:
        try: width = json.loads(props.group(1)).get('$preview', {}).get('width')
        except Exception: pass
    # sc-if / sc-for → <template> so the HTML parser keeps them inside tables and selects
    body = re.sub(r'<sc-(if|for)\b', lambda m: f'<template data-sc="{m.group(1)}"', body)
    body = re.sub(r'</sc-(if|for)>', '</template>', body)
    assert '</script' not in body.lower(), src
    logic = logic.replace('</script', '<\\/script')
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{helmet or ''}
<style>html,body{{margin:0}} #dc-root{{min-width:{width or 0}px}}</style>
</head>
<body>
<div id="dc-root"></div>
<script type="text/html" id="dc-template">{body}</script>
<script type="text/plain" id="dc-logic">{logic}</script>
<script>{RUNTIME}</script>
</body>
</html>
'''

if __name__ == '__main__':
    src_dir, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    for f in sorted(os.listdir(src_dir)):
        if not f.endswith('.dc.html'): continue
        out = os.path.join(out_dir, f.replace('.dc.html', '.html'))
        open(out, 'w', encoding='utf-8').write(convert(os.path.join(src_dir, f)))
        print(f, '->', os.path.basename(out))
