"""Build TourFocusLab.dc.html: the Sweep runs screen with seven tour-focus treatments and the window-width simulator."""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
import shell as S, navgen as N
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
s = (s.replace('<!--SIMCSS-->', S.SIM_CSS).replace('<!--SIMBAR-->', S.sim_bar()).replace('<!--SIMOPEN-->', S.sim_open('sim-host-tf', 'height: 640px'))
     .replace('<!--SIMCLOSE-->', S.SIM_CLOSE).replace('<!--NAVBAR-->', S.navbar(N.LIGHT, 'sweep')).replace('/*SIMJS*/', S.SIM_JS))
s = s.replace('<!--CSS-->', S.CSS).replace('<!--HEADER-->', S.header(False, 'Sweep · Runs', 'staging · credit-request · 3 open pull requests')).replace('<!--RAIL-->', N.rail(N.LIGHT, 'sweep'))
s = re.sub(r'<!-- [^\n]*? -->', '', s)
assert '<!--' not in s, re.findall(r'<!--[^>]*>', s)[:3]
for t in ['sc-if', 'sc-for']:
    assert len(re.findall(rf'<{t}\b', s)) == len(re.findall(rf'</{t}>', s)), t
open(dst, 'w', encoding='utf-8').write(s); print(len(s))
