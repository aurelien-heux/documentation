"""Keep ProductionVision.dc.html under the canvas limit of 2 MiB per board file (a larger board is not shown).

Lossless: CSS comments and line breaks inside <style>; comment-only lines and indentation of the script, outside
template literals. One content cut: the LikeC4 source of each element ("src" in the architecture data) is left out of
the vision, so the Source card does not show there; the standalone Architecture board keeps it."""
import re, sys
LIMIT = 2 * 1024 * 1024
MARGIN = 24 * 1024

def css_min(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    css = re.sub(r'\s*\n\s*', '\n', css)
    css = re.sub(r'\s*([{};,])\s*\n', r'\1', css)
    return re.sub(r'\n+', '\n', css).strip('\n')

def js_min(js):
    out, in_tpl = [], False
    for line in js.split('\n'):
        if not in_tpl:
            st = line.lstrip()
            if st.startswith('//'): continue
            line = st
        out.append(line)
        if line.count('`') % 2: in_tpl = not in_tpl
    return '\n'.join(out)

def shrink(page):
    page = re.sub(r'(<style>)(.*?)(</style>)', lambda m: m.group(1) + '\n' + css_min(m.group(2)) + '\n' + m.group(3), page, flags=re.S)
    i = page.index('<script type="text/x-dc"'); j = page.index('>', i) + 1; k = page.rindex('</script>')
    # markup: runs of whitespace between tags become one line break (still whitespace for HTML); inline styles lose
    # the optional spaces after ';' and ':'
    mk = re.sub(r'>\s{2,}<', '>\n<', page[:i])
    mk = re.sub(r' style="([^"]*)"', lambda m: ' style="' + re.sub(r';\s+', ';', re.sub(r':\s+', ':', m.group(1))).rstrip(';') + '"', mk)
    page = mk + page[i:]; i = page.index('<script type="text/x-dc"'); j = page.index('>', i) + 1; k = page.rindex('</script>')
    js = re.sub(r',"src":"(?:[^"\\]|\\.)*"(?=[,}])', '', page[j:k])
    return page[:j] + js_min(js) + page[k:]

def check(page, name='page'):
    n = len(page.encode('utf-8'))
    print('size', name, n, 'of', LIMIT, '(' + str(round(100 * n / LIMIT)) + '%)')
    if n > LIMIT - MARGIN: raise SystemExit(name + ': ' + str(n) + ' bytes is within ' + str(MARGIN) + ' of the 2 MiB board limit; cut content before publishing')

if __name__ == '__main__':
    p = sys.argv[1]; s = shrink(open(p, encoding='utf-8').read()); open(p, 'w', encoding='utf-8').write(s); check(s, p)
