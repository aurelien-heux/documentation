import sys, re, os, glob
sys.path.insert(0, os.path.dirname(__file__))
import navgen as N
root = sys.argv[1]
skip = {'CommunityLive.dc.html'}
for f in sorted(glob.glob(os.path.join(root, '*.dc.html'))):
    if os.path.basename(f) in skip: continue
    s = open(f, encoding='utf-8').read()
    n = 0
    def fix(m):
        global n
        nav = m.group(0)
        if '#cookies' not in nav or 'href="#admin"' in nav: return nav
        t = N.DARK if '#1D1A27' in nav[:400] else N.LIGHT
        item = N.admin_drawer_item(t) if 'width: 300px' in nav[:300] else N.admin_rail_item(t)
        i = re.search(r'<a\b[^>]*href="#cookies"', nav).start()
        n += 1
        return nav[:i] + item + nav[i:]
    s2 = re.sub(r'<nav\b.*?</nav>', fix, s, flags=re.S)
    if n:
        open(f, 'w', encoding='utf-8').write(s2); print(os.path.basename(f), n)
