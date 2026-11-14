"""Build project/Architecture.dc.html, the Architecture feature prototype (Meridian Bank) for the AIToolbox design canvas.
usage: python3 build_arch.py <arch_data.json> <out .dc.html>"""
import json, sys, os, re, urllib.parse, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # shell.py, navgen.py, markup_check.py live one level up in the export bundle
import shell as S, navgen as N, gen_graphs as G
from how_data import HOW
from markup_check import check

D = json.load(open(os.environ.get('ARCH_DATA') or sys.argv[1], encoding='utf-8'))
OUT = sys.argv[2] if len(sys.argv) > 2 else None
UI = N.UI
ST = S.ST

# ----------------------------------------------------------------------------------------------- CSS
LAYERS = {'strategy': ('#F8E5C4', '#6E4A0E'), 'business': ('#FFF2B3', '#5E5000'), 'application': ('#CFEDFA', '#0A5570'), 'technology': ('#D5EDC7', '#2C5A1C'),
          'physical': ('#CBE7D4', '#1C5631'), 'motivation': ('#ECDDF6', '#5A2C80'), 'implementation': ('#F6DCEB', '#7A2457'), 'other': ('#FBE3C8', '#7A4000')}
glyph_css = ''.join(f'.axg-{k}{{--g:url("data:image/svg+xml,{urllib.parse.quote(chr(60) + "svg xmlns=" + chr(34) + "http://www.w3.org/2000/svg" + chr(34) + " viewBox=" + chr(34) + "0 0 24 24" + chr(34) + " fill=" + chr(34) + "none" + chr(34) + " stroke=" + chr(34) + "black" + chr(34) + " stroke-width=" + chr(34) + "1.6" + chr(34) + " stroke-linecap=" + chr(34) + "round" + chr(34) + " stroke-linejoin=" + chr(34) + "round" + chr(34) + chr(62) + v["svg"] + chr(60) + "/svg" + chr(62), safe="")}")}}\n' for k, v in D['notation'].items())
layer_css = ''.join(f'.ax-l-{k}{{--ax-fill:{f};--ax-ink:{i}}}\n' for k, (f, i) in LAYERS.items())

sel_css = ''.join(f'.selwrap.sel-{G.SID(e["id"])} [data-sid="{G.SID(e["id"])}"]{{outline:3px solid #35307E;outline-offset:3px}}\n' for e in D['elements'])
CSS = S.CSS + S.SIM_CSS + layer_css + glyph_css + sel_css + r"""
:root{--primary:#35307E;--on-surface:#1C1B1E;--muted:#48454E;--outline:#79757F;--ov:#CAC4CF;--surface:#FDF8FD;--sc-low:#FAF4FF;--sc:#F8F1FF;--sc-high:#F2EBFA;--sc-highest:#ECE5F4;--white:#FFFFFF}
.h1{margin:0;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:24px;line-height:32px;font-weight:700;color:#1C1B1E}
.h3{margin:0;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:16px;line-height:24px;font-weight:600;color:#1C1B1E}
.meta{font-size:12px;line-height:16px;color:#48454E}
.lbl{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:11px;font-weight:700;letter-spacing:.6px;text-transform:uppercase;color:#48454E}
.body{font-size:14px;line-height:20px;color:#1C1B1E}
.muted{color:#48454E}
.lnk{background:none;border:0;padding:0;font:inherit;color:#35307E;cursor:pointer;text-decoration:underline;text-underline-offset:2px;text-align:left}
.lnk:hover{color:#14085E}
.app{display:flex;flex-direction:column;background:#FDF8FD;color:#1C1B1E;font-family:'Open Sans',system-ui,sans-serif;position:relative;overflow:clip}
.bodyrow{display:flex;flex:1;min-height:0;align-items:stretch}
main{flex:1;min-width:0;padding:16px 32px 48px;box-sizing:border-box;display:flex;flex-direction:column;gap:16px}
.tabs{display:flex;align-items:center;border-bottom:1px solid #CAC4CF;overflow-x:auto}
.area{display:flex;gap:24px;flex-wrap:wrap;align-items:flex-start}
.side{flex:0 0 256px;display:flex;flex-direction:column;gap:12px;min-width:0}
.content{flex:999 1 560px;min-width:0;display:flex;flex-direction:column;gap:16px}
.sl{display:flex;flex-direction:column;gap:2px;width:100%;padding:8px 12px;border:0;border-radius:12px;background:transparent;text-align:left;font:inherit;color:#1C1B1E;cursor:pointer}
.sl:hover{background:rgba(53,48,126,.06)}
.sl-on{background:#E3DFFF}
.sl b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:14px;font-weight:600;display:flex;align-items:center;gap:8px}
.sl span{font-size:12px;color:#48454E}
.vk{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:10px;font-weight:700;letter-spacing:.4px;text-transform:uppercase;padding:1px 6px;border-radius:4px;background:#F2EBFA;color:#48454E;margin-left:auto}
.vk-matrix{background:#E3DFFF;color:#191836}.vk-graph{background:#CFEDFA;color:#0A5570}
.seg{display:inline-flex;flex-wrap:wrap;border:1px solid #79757F;border-radius:16px;overflow:hidden;max-width:100%;background:#FDF8FD}
.seg button{height:40px;padding:0 16px;border:0;background:transparent;color:#1C1B1E;cursor:pointer;display:inline-flex;align-items:center;gap:6px;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:14px;font-weight:600;white-space:nowrap}
.seg button + button{border-left:1px solid #79757F}
.seg button:hover{background:rgba(53,48,126,.06)}
.seg .seg-on{background:#E3DFFF;color:#191836}
.seg.small button{height:32px;padding:0 12px;font-size:13px}
.seg.full{display:grid;grid-template-columns:repeat(3,minmax(0,1fr))}.seg.full button{justify-content:center;padding:0 4px;font-size:13px}
.sel{height:40px;padding:0 12px;border:1px solid #79757F;border-radius:4px;background:#FDF8FD;font:400 14px 'Open Sans',system-ui,sans-serif;color:#1C1B1E;width:100%;box-sizing:border-box}
.st{display:inline-flex;align-items:center;gap:6px;height:26px;padding:0 10px 0 5px;border-radius:4px;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;line-height:16px;font-weight:600;white-space:nowrap;vertical-align:middle}
.st .tile{width:16px;height:16px;border-radius:4px;display:inline-grid;place-items:center;font-family:'Open Sans',system-ui,sans-serif;font-size:11px;font-weight:700;line-height:1;flex:none}
.st-success{background:#ACF4A2;color:#1B5F1F}.st-success .tile{background:#1B5F1F;color:#fff}
.st-info{background:#E3DFFF;color:#14085E}.st-info .tile{background:#35307E;color:#fff}
.st-warning{background:#FFDEA0;color:#6A4E00}.st-warning .tile{background:#6A4E00;color:#fff}
.st-error{background:#FFDAD6;color:#410002}.st-error .tile{background:#93000A;color:#fff}
.st-neutral{background:#ECE5F4;color:#48454E}.st-neutral .tile{background:#79757F;color:#fff}
.st-none{display:none}
.st.sm{height:22px;font-size:11px;padding:0 8px 0 4px}.st.sm .tile{width:14px;height:14px;font-size:10px}
.chg{display:inline-flex;align-items:center;gap:6px;height:24px;padding:0 8px 0 4px;border-radius:4px;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:600;white-space:nowrap;vertical-align:middle}
.chg b{width:16px;height:16px;border-radius:3px;display:inline-grid;place-items:center;font:700 12px/1 'Open Sans',system-ui,sans-serif}
.chg-new{background:#ACF4A2;color:#1B5F1F}.chg-new b{background:#1B5F1F;color:#fff}
.chg-changed{background:#FFDEA0;color:#6A4E00}.chg-changed b{background:#6A4E00;color:#fff}
.chg-retired{background:#FFDAD6;color:#410002}.chg-retired b{background:#93000A;color:#fff}
.chg-none{display:none}
.trk{display:inline-flex;gap:2px;vertical-align:middle}
.trk span{min-width:20px;height:18px;padding:0 4px;box-sizing:border-box;border:1px dashed #CAC4CF;border-radius:4px;font:600 10px/16px 'Open Sans',system-ui,sans-serif;color:#79757F;text-align:center}
.trk span.on{border:1px solid #35307E;background:#E3DFFF;color:#14085E}
.ax-tile{width:20px;height:20px;border-radius:4px;display:inline-grid;place-items:center;flex:none;background:var(--ax-fill);color:var(--ax-ink);box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--ax-ink) 35%,transparent);vertical-align:middle}
.ax-tile.lg{width:32px;height:32px;border-radius:8px}
.axg{display:block;width:16px;height:16px;background:currentColor;-webkit-mask:var(--g) center/contain no-repeat;mask:var(--g) center/contain no-repeat}
.ax-tile.lg .axg{width:24px;height:24px}
.ax-box{position:absolute;width:var(--ax-w,176px);height:var(--ax-h,56px);background:var(--ax-ink);padding:1px;box-sizing:border-box;border:0;cursor:pointer;font:inherit;color:inherit;text-align:center}
.ax-box>.ax-in{position:relative;display:flex;align-items:center;justify-content:center;width:100%;height:100%;background:var(--ax-fill);color:#1C1B1E;box-sizing:border-box;padding:6px 24px 6px 8px;font:600 12px/15px 'Open Sans',system-ui,sans-serif;text-align:center}
.ax-box .ax-name{overflow-wrap:anywhere;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.ax-box .ax-glyph{position:absolute;top:5px;right:5px;width:16px;height:16px;color:var(--ax-ink)}
.ax-box:hover>.ax-in{background:color-mix(in srgb,#35307E 10%,var(--ax-fill))}
.ax-box:focus-visible{outline:2px solid #35307E;outline-offset:3px}
.ax-shape-rounded,.ax-shape-rounded>.ax-in{border-radius:12px}
.ax-shape-ellipse,.ax-shape-ellipse>.ax-in{border-radius:50%}
.ax-shape-chamfer{clip-path:polygon(10px 0,calc(100% - 10px) 0,100% 10px,100% calc(100% - 10px),calc(100% - 10px) 100%,10px 100%,0 calc(100% - 10px),0 10px)}
.ax-shape-chamfer>.ax-in{clip-path:polygon(9.6px 0,calc(100% - 9.6px) 0,100% 9.6px,100% calc(100% - 9.6px),calc(100% - 9.6px) 100%,9.6px 100%,0 calc(100% - 9.6px),0 9.6px)}
.ax-shape-object>.ax-in{background:linear-gradient(var(--ax-ink),var(--ax-ink)) 0 20px/100% 1px no-repeat,var(--ax-fill);align-items:flex-start;padding-top:2px}
.ax-chg-new{box-shadow:0 0 0 2px #1B5F1F}.ax-chg-changed{box-shadow:0 0 0 2px #6A4E00;}.ax-chg-changed>.ax-in{border:2px dotted #6A4E00}.ax-chg-retired{opacity:.45}.ax-chg-retired .ax-name{text-decoration:line-through}
.ax-muted{opacity:.6}
.ax-retired{opacity:.45}.ax-retired .ax-name{text-decoration:line-through}
.gv-scroll{overflow:auto;border:1px solid #CAC4CF;border-radius:12px;background:#FDF8FD;background-image:radial-gradient(#CAC4CF 1px,transparent 1px);background-size:16px 16px;max-height:720px}
.gv{position:relative}
.gv-edges{position:absolute;left:0;top:0;pointer-events:none}
.gv-lbl{font:600 10px 'Open Sans',system-ui,sans-serif;fill:#48454E;paint-order:stroke;stroke:#FDF8FD;stroke-width:3px;stroke-linejoin:round}
.gv-lane{position:absolute;border:1px dashed #B88A2B;border-radius:4px;box-sizing:border-box;padding:6px 8px;background:rgba(253,248,253,.5)}
.gv-band{position:absolute;border:1px dashed #B88A2B;border-radius:4px;box-sizing:border-box;padding:6px 8px}
.gv-lt{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:11px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;color:#7A4000}
.gv-crumbs{display:inline-flex;align-items:center;gap:8px;padding:6px 10px;border-radius:8px;background:#F2EBFA;font-size:12px;color:#48454E}
.gv-crumbs b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;color:#1C1B1E}
.legend{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;font-size:12px;color:#48454E}
.legend .sw{display:inline-block;width:14px;height:14px;border-radius:3px;background:var(--ax-fill);box-shadow:inset 0 0 0 1px var(--ax-ink);vertical-align:-2px;margin-right:6px}
.legend .ln{display:inline-block;width:28px;border-top:2px solid #48454E;vertical-align:3px;margin-right:6px}
.legend .ln.d{border-top-style:dashed}.legend .ln.t{border-top-style:dotted}
.mx-wrap{overflow:auto;border:1px solid #CAC4CF;border-radius:12px;background:#FFFFFF;max-height:760px}
table.mx{border-collapse:separate;border-spacing:0;font-size:13px;min-width:100%}
table.mx th,table.mx td{border-bottom:1px solid #ECE5F4;border-right:1px solid #F2EBFA}
table.mx thead th{position:sticky;top:0;z-index:2;background:#F8F1FF;vertical-align:bottom;padding:6px 6px;text-align:left}
table.mx thead tr:first-child th{top:0}
table.mx .mx-corner{position:sticky;left:0;z-index:3;background:#F8F1FF;min-width:220px;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:11px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;color:#48454E;vertical-align:bottom}
table.mx .mx-grp{text-align:center;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:11px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;color:#48454E;border-bottom:2px solid #CAC4CF}
table.mx .mx-col{min-width:76px;max-width:140px}
table.mx .mx-colin{display:flex;flex-direction:column;gap:2px;min-height:64px;justify-content:flex-end}
table.mx .mx-cl{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:600;line-height:14px;color:#1C1B1E;overflow-wrap:normal;hyphens:auto}
table.mx .mx-cs{font-size:10px;color:#48454E;line-height:12px}
table.mx .mx-colb{background:none;border:0;padding:0;font:inherit;text-align:left;cursor:pointer;color:inherit;width:100%}
table.mx .mx-ext .mx-cl{color:#48454E;font-weight:500}
table.mx .mx-sum{background:#ECE5F4}
table.mx .mx-g th{position:sticky;left:0;background:#FAF4FF;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:11px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;color:#48454E;padding:10px 8px 4px;text-align:left;z-index:1}
table.mx .mx-rh{position:sticky;left:0;z-index:1;background:#FFFFFF;padding:4px 8px;text-align:left;font-weight:400;min-width:220px;max-width:280px}
table.mx .mx-rh .mx-rhb{display:flex;align-items:center;gap:8px;background:none;border:0;padding:4px 0;font:inherit;text-align:left;cursor:pointer;color:inherit;width:100%}
table.mx .mx-rt{display:flex;flex-direction:column;min-width:0}
table.mx .mx-rt b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:13px;font-weight:600;line-height:16px}
table.mx .mx-rt span{font-size:11px;color:#48454E;line-height:14px}
table.mx .mx-rhw{display:flex;flex-direction:column;align-items:flex-start;gap:2px}
table.mx td.mx-c{text-align:center;padding:4px 6px;height:36px;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:600;color:#1C1B1E;vertical-align:middle;max-width:160px}
table.mx td.mx-off{color:#CAC4CF}
table.mx td.mx-on{background:#E3DFFF;color:#14085E;font-weight:500;font-size:11px;text-align:left}
table.mx td.mx-in{color:#79757F;background:#FAF4FF}
table.mx td.mx-diag{background:repeating-linear-gradient(45deg,#F2EBFA 0 4px,#FFFFFF 4px 8px)}
table.mx td.mx-warn{background:#FFDEA0;color:#6A4E00}
table.mx td.mx-sum{background:#F2EBFA}
table.mx td.mx-dot{color:#35307E;font-size:16px}
table.mx table.mx td.mx-raci-R{background:#E3DFFF;color:#14085E}table.mx td.mx-raci-A{background:#35307E;color:#fff}table.mx td.mx-raci-C{background:#F2EBFA;color:#48454E}table.mx td.mx-raci-I{color:#79757F}
table.mx td.mx-mode-master{background:#ACF4A2;color:#1B5F1F}table.mx td.mx-mode-copy{background:#ECE5F4;color:#48454E}
table.mx td.mx-life-adopt{color:#1B5F1F;font-size:16px}table.mx td.mx-life-trial{color:#35307E;font-size:16px}table.mx td.mx-life-hold{color:#6A4E00;font-size:16px}table.mx td.mx-life-retire{color:#93000A;font-size:16px}
th.life-h-adopt .mx-cs{color:#1B5F1F}th.life-h-trial .mx-cs{color:#35307E}th.life-h-hold .mx-cs{color:#6A4E00}th.life-h-retire .mx-cs{color:#93000A;font-weight:700}
.lg-c{display:inline-grid;place-items:center;min-width:22px;height:22px;padding:0 5px;border-radius:4px;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:11px;font-weight:700;margin-right:6px;border:1px solid #CAC4CF;background:#fff;color:#1C1B1E}
.lg-c.mx-on{background:#E3DFFF;color:#14085E}.lg-c.mx-in{color:#79757F;background:#FAF4FF}.lg-c.mx-warn{background:#FFDEA0;color:#6A4E00}.lg-c.mx-off{color:#CAC4CF}.lg-c.mx-dot{color:#35307E;font-size:14px}
.lg-c.mx-raci-R{background:#E3DFFF;color:#14085E}.lg-c.mx-raci-A{background:#35307E;color:#fff}.lg-c.mx-raci-C{background:#F2EBFA;color:#48454E}.lg-c.mx-raci-I{color:#79757F}
.lg-c.mx-mode-master{background:#ACF4A2;color:#1B5F1F}.lg-c.mx-mode-copy{background:#ECE5F4;color:#48454E}
.lg-c.mx-life-adopt{color:#1B5F1F}.lg-c.mx-life-trial{color:#35307E}.lg-c.mx-life-hold{color:#6A4E00}.lg-c.mx-life-retire{color:#93000A}
.gd-wrap{overflow:auto;border:1px solid #CAC4CF;border-radius:12px;background:#fff}
.gd{display:grid;min-width:100%}
.gd-h{padding:8px 10px;background:#F8F1FF;border-bottom:1px solid #CAC4CF;border-right:1px solid #F2EBFA;display:flex;flex-direction:column;gap:2px;position:sticky;top:0;z-index:1}
.gd-h b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:700;letter-spacing:.4px;text-transform:uppercase;color:#48454E}
.gd-h span{font-size:11px;color:#48454E}
.gd-c{padding:10px;border-bottom:1px solid #ECE5F4;border-right:1px solid #F2EBFA;display:flex;flex-direction:row;flex-wrap:wrap;gap:10px;min-height:72px;align-items:flex-start;align-content:flex-start;background-image:radial-gradient(#ECE5F4 1px,transparent 1px);background-size:12px 12px}
.gd-c.gd-self{background:#FAF4FF;background-image:none}
.gd-c.gd-warn{background:#FFF4DE;background-image:none}
.gd-note{font-size:11px}
.figw{display:flex;flex-direction:column;gap:3px;flex:0 1 176px;min-width:140px}
.figw .rel{font:600 10px/12px 'Open Sans',system-ui,sans-serif;color:#48454E;padding-left:2px}
.axf{position:relative;width:100%;min-height:48px;background:var(--ax-ink);padding:1px;box-sizing:border-box;border:0;cursor:pointer;font:inherit;color:inherit;text-align:center;display:block}
.axf>.ax-in{position:relative;display:flex;align-items:center;justify-content:center;width:100%;min-height:46px;background:var(--ax-fill);color:#1C1B1E;box-sizing:border-box;padding:6px 24px 6px 8px;font:600 12px/15px 'Open Sans',system-ui,sans-serif;text-align:center}
.axf .ax-name{overflow-wrap:anywhere}
.axf .ax-glyph{position:absolute;top:5px;right:5px;width:16px;height:16px;color:var(--ax-ink)}
.axf:hover>.ax-in{background:color-mix(in srgb,#35307E 10%,var(--ax-fill))}
.axf:focus-visible{outline:2px solid #35307E;outline-offset:3px}
.axf.ax-chg-new{box-shadow:0 0 0 2px #1B5F1F}.axf.ax-chg-changed>.ax-in{border:2px dotted #6A4E00}.axf.ax-chg-retired{opacity:.45}.axf.ax-chg-retired .ax-name{text-decoration:line-through}
.axf.ax-muted{opacity:.6}
.vframe{display:grid;grid-template-columns:minmax(0,1fr);gap:16px;align-items:start}
.vframe.has-card{grid-template-columns:minmax(0,1fr) 320px}
.vbody{display:flex;flex-direction:column;gap:12px;min-width:0}
.vpanel{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:6px 10px;border-radius:12px;background:#F2EBFA;font-size:12px;color:#48454E}
.vp-mark{font:700 11px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;padding:2px 6px;border-radius:4px;background:#fff;border:1px solid #CAC4CF;color:#1C1B1E}
.vp-back{width:28px;height:28px;border:0;border-radius:8px;background:#fff;color:#35307E;cursor:pointer;display:inline-grid;place-items:center}
.vp-back:hover{background:#E3DFFF}
.vp-cb{background:none;border:0;padding:0;color:#35307E;font:600 13px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;cursor:pointer}
.vp-cb:hover{text-decoration:underline}
.vp-cb[aria-current="true"]{color:#1C1B1E;cursor:default;text-decoration:none}
.vp-sep{color:#79757F}
.vp-id{font:600 11px 'Open Sans',system-ui,sans-serif;color:#48454E;background:#fff;padding:2px 6px;border-radius:4px;margin-left:auto}
.zoomg{display:inline-flex;border:1px solid #CAC4CF;border-radius:8px;overflow:hidden;background:#fff}
.zoomg button{width:30px;height:28px;border:0;background:transparent;font:600 13px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;color:#1C1B1E;cursor:pointer;border-left:1px solid #CAC4CF}
.zoomg button:first-child{border-left:0}.zoomg button.fit{width:auto;padding:0 10px;font-size:12px}
.zoomg button:hover{background:rgba(53,48,126,.06)}
.ax-sel{outline:3px solid #35307E;outline-offset:2px}
.axf.ax-sel{outline-offset:3px}
table.mx .mx-rh.mx-sel{background:#E3DFFF}table.mx .mx-rh.mx-sel .mx-rt b{color:#14085E}
.capcell.ax-sel,.techchip.ax-sel{outline-offset:2px}
.card-el{border:1px solid #CAC4CF;border-radius:12px;background:#fff;padding:14px;display:flex;flex-direction:column;gap:10px;position:sticky;top:8px;min-width:0}
.card-el .ce-h{display:flex;align-items:flex-start;gap:10px}
.card-el .ce-h b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:15px;line-height:20px;overflow-wrap:anywhere;display:block}
.card-el .ce-desc{margin:0;font-size:13px;line-height:19px;color:#1C1B1E}
.card-el .ce-rel{display:flex;align-items:center;gap:8px;width:100%;padding:6px 0;border:0;border-top:1px solid #F2EBFA;background:none;font:inherit;text-align:left;color:#1C1B1E;cursor:pointer}
.card-el .ce-rel:hover{background:rgba(53,48,126,.04)}
.card-el .ce-verb{font-size:11px;color:#48454E;min-width:84px}
.card-el .ce-rel .nm{flex:1;min-width:0;font-size:13px}
.card-el .ce-rel .nm span{display:block;font-size:11px;color:#48454E}
.card-el .ce-rel.off{opacity:.6}
.btn.sm{height:34px;padding:0 14px;font-size:13px}
.gv-zoomwrap{display:inline-block;min-width:100%}
@container win (max-width: 1199px){.vframe.has-card{grid-template-columns:1fr}.card-el{order:-1;position:static}}
.ext-note{display:flex;gap:10px;align-items:flex-start;padding:10px 12px;border-radius:8px;background:#F2EBFA;font-size:12px;color:#48454E;line-height:16px}
.ext-note b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;color:#1C1B1E;white-space:nowrap}
.capdom{border:1px solid #CAC4CF;border-radius:12px;padding:12px;background:#FFFFFF;display:flex;flex-direction:column;gap:8px;min-width:0}
.capdom .lbl{color:#1C1B1E}
.capcell{display:flex;flex-direction:column;gap:6px;padding:10px 12px;border:1px solid color-mix(in srgb,#6E4A0E 45%,transparent);border-radius:12px;background:#F8E5C4;color:#1C1B1E;font:inherit;text-align:left;cursor:pointer}
.capcell:hover{border-color:#35307E}
.capcell .cc-t{display:flex;align-items:flex-start;gap:8px;justify-content:space-between;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:14px;font-weight:600;line-height:18px}
.capcell .cc-v{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:18px;font-weight:700;line-height:18px;white-space:nowrap}
.capcell .cc-v small{font-size:11px;font-weight:600;color:#48454E}
.capcell .cc-m{display:flex;gap:10px;font-size:12px;color:#48454E}
.tb{overflow:auto;border:1px solid #CAC4CF;border-radius:12px;background:#FFFFFF}
.tb table{border-collapse:collapse;width:100%;font-size:14px}
.tb .th{height:44px;padding:0 12px;text-align:left;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:11px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;color:#48454E;white-space:nowrap;background:#F8F1FF;position:sticky;top:0}
.tb .td{padding:8px 12px;border-top:1px solid #ECE5F4;vertical-align:middle;color:#1C1B1E}
.tb tr.rowb{cursor:pointer}.tb tr.rowb:hover td{background:rgba(53,48,126,.06)}
.tb .tt{display:flex;align-items:center;gap:10px;min-width:0}
.tb .tt .ttx{display:flex;flex-direction:column;min-width:0}
.tb .tt b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:14px;font-weight:600;line-height:18px}
.tb .tt span{font-size:11px;color:#48454E;line-height:14px;font-weight:600}
.rowbtn{background:none;border:0;padding:0;font:inherit;color:inherit;text-align:left;cursor:pointer;display:flex;align-items:center;gap:10px;min-width:0;width:100%}
.lsrow{display:grid;grid-template-columns:180px minmax(0,1fr);gap:12px;align-items:start;padding:10px 12px;border:1px solid #CAC4CF;border-radius:12px;background:#FFFFFF}
.lshead{display:flex;flex-direction:column;gap:4px}
.lshead button{display:flex;align-items:center;gap:8px;background:#F8E5C4;border:1px solid #6E4A0E;border-radius:8px;padding:8px 10px;font:600 13px/16px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;color:#1C1B1E;text-align:left;cursor:pointer}
.lscells{display:flex;flex-wrap:wrap;gap:12px}
.lsapp{display:flex;flex-direction:column;gap:6px;align-items:flex-start}
.lsapp .figb{position:relative;width:148px;height:52px;background:#0A5570;padding:1px;border:0;cursor:pointer;font:inherit;text-align:center}
.lsapp .figb>span{display:flex;align-items:center;justify-content:center;width:100%;height:100%;background:#CFEDFA;box-sizing:border-box;padding:4px 22px 4px 8px;font:600 12px/14px 'Open Sans',system-ui,sans-serif;color:#1C1B1E}
.lsapp .figb .axg{position:absolute;top:4px;right:4px;color:#0A5570;width:14px;height:14px}
.lsapp .figb:hover>span{background:color-mix(in srgb,#35307E 10%,#CFEDFA)}
.lsapp.ax-retired .figb{opacity:.45}.lsapp.ax-retired .figb>span{text-decoration:line-through}
.lsapp .chips{display:flex;gap:4px;flex-wrap:wrap}
.radar{display:grid;grid-template-columns:120px repeat(4,minmax(0,1fr));border:1px solid #CAC4CF;border-radius:12px;overflow:hidden;background:#fff}
.radar>div{padding:8px 10px;border-bottom:1px solid #ECE5F4;border-right:1px solid #F2EBFA;min-height:44px;display:flex;flex-direction:column;gap:6px}
.radar .rh{background:#F8F1FF;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:700}
.radar .rh small{display:block;font-size:11px;font-weight:400;color:#48454E}
.radar .rc{background:#FAF4FF;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:700;color:#48454E;justify-content:center}
.techchip{display:inline-flex;align-items:center;gap:6px;height:28px;padding:0 10px 0 8px;border-radius:8px;border:1px solid #CAC4CF;background:#fff;font:600 12px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;color:#1C1B1E;cursor:pointer;text-align:left;width:fit-content;max-width:100%}
.techchip i{width:8px;height:8px;border-radius:50%;flex:none}
.techchip .n{margin-left:2px}
.life-adopt i{background:#1B5F1F}.life-trial i{background:#35307E}.life-hold i{background:#6A4E00}.life-retire i{background:#93000A}
.rm{border:1px solid #CAC4CF;border-radius:12px;background:#fff;overflow:auto}
.rm-in{min-width:760px;position:relative}
.rm-months{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(0,1fr);margin-left:200px;border-bottom:1px solid #CAC4CF;background:#F8F1FF}
.rm-months span{font:600 10px/28px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;color:#48454E;text-align:center;border-left:1px solid #F2EBFA;overflow:hidden}
.rm-months span.y{color:#1C1B1E;font-weight:700}
.rm-band{display:grid;grid-template-columns:200px minmax(0,1fr);border-bottom:1px solid #ECE5F4}
.rm-band .rm-h{padding:10px 12px;display:flex;flex-direction:column;gap:2px;border-right:1px solid #ECE5F4}
.rm-band .rm-h button{background:none;border:0;padding:0;font:600 13px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;color:#35307E;text-align:left;cursor:pointer}
.rm-track{position:relative;min-height:56px;padding:8px 0;background-image:repeating-linear-gradient(90deg,#F2EBFA 0 1px,transparent 1px calc(100% / 19))}
.rm-today{position:absolute;top:0;bottom:0;width:0;border-left:2px solid #93000A;z-index:1}
.rm-pl{position:absolute;top:2px;transform:translateX(-50%);font-size:11px;color:#1C1B1E;white-space:nowrap}
.rm-pl b{color:#35307E}
.rm-wp{position:relative;height:28px;margin:4px 0;display:flex;align-items:center}
.rm-bar{position:absolute;height:28px;border-radius:6px;background:#E3DFFF;border:1px solid #35307E;display:flex;align-items:center;gap:6px;padding:0 8px;box-sizing:border-box;font:600 11px/1 Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;color:#14085E;cursor:pointer;overflow:hidden;white-space:nowrap;text-align:left}
.rm-bar.wp-draft{background:#FAF4FF;border-style:dashed;color:#48454E}
.rm-bar.wp-approved,.rm-bar.wp-approved-with-conditions{background:#ACF4A2;border-color:#1B5F1F;color:#1B5F1F}
.rm-bar.wp-in-review{background:#FFDEA0;border-color:#6A4E00;color:#6A4E00}
.rm-dep{position:absolute;left:0;top:30px;font-size:10px;color:#48454E;white-space:nowrap}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}
.cardx{border:1px solid #CAC4CF;border-radius:12px;background:#fff;padding:12px 14px;display:flex;flex-direction:column;gap:8px;min-width:0}
.cardx .lbl{display:flex;justify-content:space-between;align-items:center}
.kv{display:grid;grid-template-columns:auto minmax(0,1fr);gap:4px 12px;font-size:13px}
.kv dt{color:#48454E;margin:0}.kv dd{margin:0;color:#1C1B1E;overflow-wrap:anywhere}
.kv-stack{grid-template-columns:1fr;gap:2px 0}.kv-stack dd{margin-bottom:8px}
.rows{display:flex;flex-direction:column}
.rows .row{display:flex;align-items:center;gap:10px;width:100%;padding:6px 0;border:0;border-top:1px solid #F2EBFA;background:none;font:inherit;color:inherit;text-align:left;cursor:pointer;min-width:0}
.rows .row:first-child{border-top:0}
.rows .row:hover{background:rgba(53,48,126,.04)}
.rows .row .txt{display:flex;flex-direction:column;min-width:0;flex:1}
.rows .row .txt b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:13px;font-weight:600;line-height:16px}
.rows .row .txt span{font-size:11px;color:#48454E;line-height:14px}
.tree{border:1px solid #CAC4CF;border-radius:12px;background:#fff;overflow:hidden}
.tn{display:flex;align-items:center;gap:8px;min-height:40px;border-top:1px solid #F2EBFA;padding-right:12px}
.tn:first-child{border-top:0}
.tn-0{background:#FAF4FF}
.tn .tog{width:28px;height:28px;border:0;border-radius:8px;background:transparent;color:#48454E;font-size:12px;cursor:pointer;flex:none;display:inline-grid;place-items:center}
.tn .tog:hover{background:rgba(53,48,126,.08)}
.tn .tnb{display:flex;align-items:center;gap:8px;flex:1;min-width:0;background:none;border:0;padding:6px 0;font:inherit;color:inherit;text-align:left;cursor:pointer}
.tn .tnb:hover b{color:#35307E}
.tn .tnt{display:flex;flex-direction:column;min-width:0}
.tn .tnt b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:13px;font-weight:600;line-height:16px}
.tn .tnt span{font-size:11px;color:#48454E;line-height:14px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tn .path{font-size:11px;color:#48454E}
.tn .cnt{font-size:11px;padding:1px 7px;border-radius:8px;background:#F2EBFA;color:#48454E;font-weight:600}
.tn .tnr{display:flex;align-items:center;gap:8px;flex:none}
.leafsp{width:28px;flex:none}
.cc{border:1px solid #CAC4CF;border-radius:12px;background:#fff;padding:14px 16px;display:flex;flex-direction:column;gap:10px}
.cc-h{display:flex;align-items:flex-start;gap:12px;flex-wrap:wrap}
.cc-h .h3{flex:1 1 240px}
.steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
.step{display:flex;flex-direction:column;gap:4px;padding:8px 10px;border-radius:8px;background:#FAF4FF;border:1px solid #ECE5F4}
.step.step-attention{background:#FFDEA0;border-color:#FFDEA0}.step.step-blocked{background:#FFDAD6}
.step .lbl{font-size:10px}
.step .note{font-size:11px;color:#48454E;line-height:14px}
.flow{display:flex;align-items:stretch;gap:0;overflow:auto;padding:2px 0 12px}
.ph{flex:1 1 0;min-width:92px;padding:6px 8px;border:1px solid #CAC4CF;border-radius:8px;background:#FAF4FF;display:flex;flex-direction:column;gap:1px;font:inherit;text-align:left;color:#1C1B1E;cursor:default;position:relative}
.ph b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:600;line-height:16px}
.ph span{font-size:10px;color:#48454E;line-height:13px}
.ph .pn{position:absolute;top:4px;right:6px;font:700 10px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;color:#79757F}
.ph-done{background:#ACF4A2;border-color:#1B5F1F}.ph-done span{color:#1B5F1F}
.ph-current{background:#E3DFFF;border-color:#35307E;box-shadow:inset 0 0 0 1px #35307E}
.ph-skipped{border-style:dashed;color:#48454E}.ph-skipped b{color:#48454E}.ph-skipped .pn{opacity:.6}
.ph-todo{background:#FAF4FF}
.ph .ent{position:absolute;left:8px;bottom:-9px;font:700 9px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;letter-spacing:.3px;text-transform:uppercase;color:#35307E;background:#fff;padding:0 4px;border-radius:3px;border:1px solid #35307E}
.gt{width:26px;height:26px;flex:none;align-self:center;margin:0 6px;display:grid;place-items:center;position:relative}
.gt::before{content:"";position:absolute;inset:3px;transform:rotate(45deg);border:1px solid #35307E;background:#fff;border-radius:2px}
.gt i{position:relative;font:700 9px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-style:normal;color:#35307E}
.gt-passed::before{background:#35307E}.gt-passed i{color:#fff}
.gt-pending::before{background:#FFDEA0;border-color:#6A4E00}.gt-pending i{color:#6A4E00}
.gt-attention::before{background:#FFDEA0;border-color:#6A4E00}.gt-attention i{color:#6A4E00}
.gt-blocked::before{background:#FFDAD6;border-color:#93000A}.gt-blocked i{color:#93000A}
.gt-todo::before{border-color:#CAC4CF}.gt-todo i{color:#79757F}
.gt-skipped{opacity:.4}.gt-skipped::before{border-style:dashed}
.gt.lg{width:40px;height:40px;margin:0 10px}.gt.lg i{font-size:11px}
.nx{width:14px;flex:none;align-self:center;border-top:1px solid #79757F;margin:0 2px}
button.ph{cursor:pointer}button.ph:hover{border-color:#35307E}
.gatecard{border:1px solid #35307E;border-radius:12px;background:#fff;padding:12px 14px;display:flex;flex-direction:column;gap:6px}
.kl{display:inline-flex;align-items:center;height:22px;padding:0 8px;border-radius:4px;font:700 11px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;background:#ECE5F4;color:#48454E;text-transform:capitalize}
.kl-re-architecting{background:#E3DFFF;color:#14085E}.kl-incremental{background:#CFEDFA;color:#0A5570}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}
.kpi{border:1px solid #CAC4CF;border-radius:12px;background:#fff;padding:12px 14px;display:flex;flex-direction:column;gap:2px}
.kpi b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:24px;font-weight:700;line-height:28px}
.kpi span{font-size:12px;color:#48454E}
.asd{display:grid;grid-template-columns:240px minmax(0,1fr);gap:24px;align-items:start}
.toc{display:flex;flex-direction:column;gap:2px;position:sticky;top:8px}
.toc button{display:grid;grid-template-columns:20px minmax(0,1fr) auto;gap:8px;align-items:center;padding:6px 8px;border:0;border-radius:8px;background:none;font:inherit;font-size:13px;color:#1C1B1E;text-align:left;cursor:pointer}
.toc button:hover{background:rgba(53,48,126,.06)}
.toc .toc-on{background:#E3DFFF}
.toc .n{font-size:11px;color:#48454E}
.toc .dot{width:10px;height:10px;border-radius:50%}
.dot-covered{background:#1B5F1F}.dot-partly,.dot-thin{background:#6A4E00}.dot-missing{background:#93000A}
.asec{display:flex;flex-direction:column;gap:10px;padding:14px 0 18px;border-bottom:1px solid #ECE5F4}
.asec-h{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.asec-h .num{width:24px;height:24px;border-radius:6px;background:#F2EBFA;display:inline-grid;place-items:center;font:700 12px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;color:#48454E}
.src{font:700 10px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;letter-spacing:.4px;text-transform:uppercase;padding:2px 6px;border-radius:4px}
.src-written{background:#ACF4A2;color:#1B5F1F}.src-model{background:#E3DFFF;color:#14085E}
.prose{font-size:14px;line-height:21px;color:#1C1B1E;white-space:pre-line}
.rev{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
.rev .cardx.me{border-color:#35307E;box-shadow:inset 0 0 0 1px #35307E}
.rev .who{display:flex;align-items:center;gap:10px}
.rev .who .av{width:36px;height:36px;font-size:14px}
.rev .who b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:14px;display:block}
.rev .who span{font-size:12px;color:#48454E}
.note{font-size:13px;color:#1C1B1E;padding:8px 10px;border-radius:8px;background:#FAF4FF;border-left:3px solid #E3DFFF}
.dec{border:1px solid #CAC4CF;border-radius:12px;background:#fff;padding:16px;display:flex;flex-direction:column;gap:12px}
.dec .acts{display:flex;gap:8px;flex-wrap:wrap}
.btn[aria-disabled="true"]{opacity:.45;cursor:not-allowed}
.btn.d{background:#93000A;color:#fff}
.btn.w{background:#FFDEA0;color:#6A4E00}
.banner{display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:8px;background:#FFDEA0;color:#6A4E00;font-size:13px}
.hsteps{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:4px;border:1px solid #CAC4CF;border-radius:16px;overflow:hidden;background:#FDF8FD}
.hsteps button{display:flex;flex-direction:column;gap:2px;padding:10px 12px;border:0;background:transparent;font:inherit;text-align:left;cursor:pointer;color:#1C1B1E;border-left:1px solid #CAC4CF}
.hsteps button:first-child{border-left:0}
.hsteps button b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:14px}
.hsteps button span{font-size:11px;color:#48454E}
.hsteps .hs-on{background:#E3DFFF}
.lanes{display:grid;grid-template-columns:150px repeat(5,minmax(0,1fr));border:1px solid #CAC4CF;border-radius:12px;overflow:hidden;background:#fff;font-size:12px;min-width:760px}
.lanes>div{padding:8px 10px;border-bottom:1px solid #ECE5F4;border-right:1px solid #F2EBFA;min-height:40px;line-height:16px}
.lanes .lh{background:#F8F1FF;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-weight:700;font-size:12px}
.lanes .lh small{display:block;font-weight:400;color:#48454E;font-size:11px}
.lanes .lw{background:#FAF4FF;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-weight:700}
.lanes .lw small{display:block;font-weight:400;color:#48454E;font-size:11px}
.toast{position:absolute;left:24px;bottom:24px;z-index:40;display:flex;align-items:center;gap:12px;padding:12px 8px 12px 16px;border-radius:4px;background:#313033;color:#F4EFF4;font-size:14px;box-shadow:0 1px 3px rgba(0,0,0,.3),0 4px 8px 3px rgba(0,0,0,.15);max-width:560px}
.toast button{border:0;background:transparent;color:#F4EFF4;font:inherit;cursor:pointer;padding:4px 8px}
.srch{display:flex;align-items:center;gap:8px;height:40px;padding:0 12px;border:1px solid #79757F;border-radius:16px;background:#FDF8FD;flex:1 1 220px;min-width:0}
.srch input{flex:1;min-width:0;border:0;outline:0;background:transparent;font:400 14px 'Open Sans',system-ui,sans-serif;color:#1C1B1E}
.srch button{border:0;background:none;color:#48454E;cursor:pointer;font-size:14px}
.ok-dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px}
pre.srcbox{margin:0;padding:12px;border-radius:8px;background:#F2EBFA;font:600 12px/18px 'Open Sans',system-ui,sans-serif;color:#1C1B1E;white-space:pre-wrap;overflow:auto;max-height:280px}
.htmlbox{font-size:13px;line-height:19px}
.htmlbox table{border-collapse:collapse;font-size:12px}
.htmlbox td,.htmlbox th{border:1px solid #ECE5F4;padding:4px 8px;text-align:left}
@container win (max-width: 1199px){.asd{grid-template-columns:1fr}.toc{position:static;flex-direction:row;flex-wrap:wrap}.toc button{grid-template-columns:auto auto}.toc .n{display:none}}
@container win (max-width: 839px){.side{flex-basis:100%}.steps{grid-template-columns:repeat(2,minmax(0,1fr))}.lsrow{grid-template-columns:1fr}.hsteps{grid-template-columns:1fr}.hsteps button{border-left:0;border-top:1px solid #CAC4CF}.kpis{grid-template-columns:repeat(2,minmax(0,1fr))}}
@container win (max-width: 599px){main{padding:12px 16px 100px}.mx-corner,.mx-rh{min-width:150px!important}.area{gap:12px}.radar{grid-template-columns:90px repeat(4,minmax(0,1fr))}.tn{flex-wrap:wrap;row-gap:0;padding:4px 8px 6px 0}.tn .tnb{flex:1 1 180px}.tn .tnr{flex:0 0 auto;margin-left:36px;padding-bottom:2px}.tn .tnr .track{display:none}.tn .tnt span{white-space:normal}.tabs{overflow-x:auto;flex-wrap:nowrap;scrollbar-width:none}.tabs .tab{white-space:nowrap;flex:none}}
.vsep{width:1px;height:20px;background:#CAC4CF;margin:0 4px}
.colcard .txt,.prop .txt{display:flex;flex-direction:column;gap:2px;min-width:0}.colcard .txt b,.prop .txt b{font:600 14px/20px Manrope,sans-serif}.colcard .txt span,.prop .txt span{font-size:13px;line-height:19px;color:#48454E}
.colcard .row{flex-wrap:wrap}.colcard{border:1px solid #CAC4CF;border-left:4px solid #6A4E00;border-radius:12px;padding:12px 16px;background:#FFF8E6;display:flex;flex-direction:column;gap:8px}.colcard.col-same-element{border-left-color:#93000A;background:#FFEDEA}.colcard.col-base-moved{border-left-color:#35307E;background:#F2EBFA}
.pk{display:inline-flex;align-items:center;height:24px;padding:0 8px;border-radius:8px;background:#ECE5F4;color:#1C1B1E;font:600 11px/16px Manrope,sans-serif;letter-spacing:.2px;white-space:nowrap}.pk-code-without-model{background:#FFDEA0;color:#261900}.pk-model-without-code{background:#FFDAD6;color:#410002}.pk-undeclared-contract{background:#FFDEA0;color:#261900}.pk-documentation-from-code{background:#9CF1F0;color:#002020}.pk-stale-documentation{background:#E6E0EC}
.nextg{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}@container win (max-width: 839px){.nextg{grid-template-columns:1fr}}
.dph{border:1px solid #CAC4CF;border-radius:12px;background:#FFFFFF;overflow:hidden}.dph.ph-done{border-color:#CAC4CF}.dph.ph-current{border-color:#35307E;box-shadow:inset 4px 0 0 #35307E}
.dph-h{display:flex;align-items:center;gap:10px;padding:10px 16px;background:#FAF4FF;border-bottom:1px solid #E6E0EC}.dph-h .pn{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:#E3DFFF;color:#191836;font:700 11px/1 Manrope,sans-serif}.dph.ph-current .dph-h .pn{background:#35307E;color:#FFFFFF}
.docrows{display:flex;flex-direction:column}.docrow{display:grid;grid-template-columns:minmax(0,1fr) auto auto;gap:4px 16px;align-items:center;width:100%;padding:10px 16px;border:0;border-top:1px solid #E6E0EC;background:transparent;text-align:left;font:inherit;color:inherit;cursor:pointer}.docrow:first-child{border-top:0}.docrow:hover{background:#F8F1FF}.docrow:focus-visible{outline:2px solid #35307E;outline-offset:-2px}
.dr-t{display:flex;flex-direction:column;gap:2px;min-width:0}.dr-t b{font:600 14px/20px Manrope,sans-serif}.dr-m{min-width:0}.dr-a{font:600 13px/20px Manrope,sans-serif;color:#35307E;white-space:nowrap}
.src-model{color:#006D3B}.src-code{color:#006A6A}.src-written{color:#48454E}
@container win (max-width: 839px){.docrow{grid-template-columns:minmax(0,1fr) auto}.dr-a{grid-column:1 / -1;justify-self:end}}
.sec .row .lnk+.lnk{margin-left:14px}.sr-only{position:absolute!important;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.nextline{display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:14px;padding:8px 12px;border-radius:12px;background:#FAF4FF}.nextline b{font-family:Manrope,sans-serif;font-weight:600}
.colline{display:flex;align-items:center;gap:10px;flex-wrap:wrap;font-size:13px;padding:8px 12px;border-radius:12px;background:#FFF8E6;border-left:4px solid #6A4E00}.colline.col-same-element{background:#FFEDEA;border-left-color:#93000A}.colline.col-base-moved{background:#F2EBFA;border-left-color:#35307E}
.doclist{display:flex;flex-direction:column;gap:10px}.sec-h .lnk+.lnk{margin-left:12px}
.docstatus{display:flex;gap:12px;align-items:center;flex-wrap:wrap;padding:8px 12px;border-radius:12px;background:#FAF4FF}
.og{display:inline-grid;place-items:center;width:22px;height:22px;flex:none;border-radius:6px;font:700 11px/1 Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;background:#ECE5F4;color:#48454E}.og-ticket{background:#E3DFFF;color:#14085E}.og-chat{background:#CFEDFA;color:#0A5570}.og-idea{background:#F2EBFA;color:#48454E}.og-radar{background:#DFF3D8;color:#1B5F1F}.og-adr{background:#FFDEA0;color:#6A4E00}.og-pr{background:#1D1A27;color:#FFFFFF}.og-finding{background:#FFE9C7;color:#6A4E00}.og-incident{background:#FFDAD6;color:#93000A}.orow{display:flex;align-items:center;gap:6px;min-width:0;font-size:12px;line-height:16px;color:#48454E}.orow b{font-weight:600;color:#1C1B1E}.tg{display:inline-flex;align-items:center;height:20px;padding:0 6px;border-radius:4px;background:#191836;color:#FFFFFF;font:700 10px/1 Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;letter-spacing:.4px;white-space:nowrap}.trk2{display:flex;align-items:center;gap:0}.trk2 .d{width:22px;height:22px;border-radius:50%;border:1px solid #CAC4CF;background:#FFFFFF;display:grid;place-items:center;font:700 10px/1 Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;color:#79757F}.trk2 .d.ph-done{background:#ACF4A2;border-color:#1B5F1F;color:#1B5F1F}.trk2 .d.ph-current{background:#35307E;border-color:#35307E;color:#FFFFFF}.trk2 .d.ph-skipped{border-style:dashed;background:#FFFFFF;color:#79757F}.trk2 .d.ph-todo{background:#FAF4FF}.trk2 .l{width:10px;height:1px;background:#CAC4CF}.trk2 .gt{width:22px;height:22px;margin:0 2px}.tgrp{border:1px solid #CAC4CF;border-radius:12px;overflow:hidden;background:#FFFFFF}.tgrp .tg-h{display:flex;align-items:center;gap:8px;padding:8px 14px;background:#F8F1FF;font:700 11px/16px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;letter-spacing:.5px;text-transform:uppercase;color:#48454E}.trow{display:grid;grid-template-columns:minmax(200px,1.3fr) 290px minmax(200px,1.4fr) auto;gap:6px 16px;align-items:center;width:100%;box-sizing:border-box;padding:10px 14px;border:0;border-top:1px solid #ECE5F4;background:#FFFFFF;font:inherit;text-align:left;color:#1C1B1E;cursor:pointer}.trow:hover{background:#FAF4FF}.trow:focus-visible{outline:2px solid #35307E;outline-offset:-2px}.trow .t1{display:flex;flex-direction:column;gap:3px;min-width:0}.trow .t1 b{font:600 14px/20px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif}.trow .t3{display:flex;flex-direction:column;gap:2px;min-width:0;font-size:12px;line-height:16px;color:#48454E}.trow .t3 b{font:600 13px/18px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;color:#1C1B1E}.trow .t4{display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end}.trow-new{box-shadow:inset 4px 0 0 #35307E}.tlegend{display:flex;align-items:center;gap:6px 14px;flex-wrap:wrap;font-size:12px;color:#48454E}.sigrow{display:flex;align-items:flex-start;gap:12px;padding:10px 14px;border-top:1px solid #ECE5F4;flex-wrap:wrap}.sigrow .s1{flex:1 1 320px;display:flex;flex-direction:column;gap:3px;min-width:0}.sigrow .s1 b{font:600 14px/20px Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;color:#1C1B1E}.sigrow .s2{display:flex;gap:6px;flex-wrap:wrap;align-items:center}@container win (max-width: 1199px){.trow{grid-template-columns:minmax(0,1fr) 290px}.trow .t3,.trow .t4{grid-column:1 / -1;justify-content:flex-start}}@container win (max-width: 699px){.trow{grid-template-columns:1fr}.trk2{overflow:auto}}
.dline{display:flex;align-items:stretch;gap:6px;flex-wrap:wrap;padding:10px 16px}.dli{display:flex;flex-direction:column;gap:2px;min-width:0;flex:1 1 150px;padding:8px 10px;border:1px solid #CAC4CF;border-radius:10px;background:#fff;text-align:left;font:inherit;color:inherit}button.dli{cursor:pointer}button.dli:hover{background:#F8F1FF}button.dli:focus-visible{outline:2px solid #35307E;outline-offset:2px}.dli .lbl{font-size:10px}.dli b{font:600 14px/20px Manrope,sans-serif;color:#1C1B1E;overflow-wrap:anywhere}.dli .s{font-size:12px;line-height:16px;color:#48454E}.dl-arrow{align-self:center;color:#79757F;font-size:16px;flex:none}.tkrow{cursor:default}.tkrow .tk-k{min-width:76px;font-size:12px;color:#48454E}.tkrow .txt span .lnk{font-size:12px}.dl-done{color:#1B5F1F;font-weight:600}.dl-doing{color:#35307E;font-weight:600}.ctx-verb{min-width:150px;font:600 11px/16px Manrope,sans-serif;letter-spacing:.4px;text-transform:uppercase;color:#48454E}@container win (max-width: 599px){.dli{flex-basis:100%}.dl-arrow{display:none}.ctx-row{flex-wrap:wrap;row-gap:2px}.ctx-verb{min-width:0;flex-basis:100%}.tkrow{flex-wrap:wrap}.tkrow .tk-k{flex:1}.tkrow .txt{order:3;flex-basis:100%}}
.docgrid{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(320px,1fr);gap:16px;align-items:start}@container win (max-width: 1199px){.docgrid{grid-template-columns:1fr}.docthread{position:static!important}}
.docmain{display:flex;flex-direction:column;gap:10px;min-width:0}.prog{width:120px;height:6px;border-radius:3px;background:#E6E0EC;overflow:hidden;display:inline-block}.prog i{display:block;height:100%;background:#35307E}
.sec{border:1px solid #CAC4CF;border-radius:12px;padding:10px 16px 12px;background:#FFFFFF;display:flex;flex-direction:column;gap:6px}.sec-h{display:flex;align-items:center;gap:10px}.sec-h .pn{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:#ECE5F4;color:#1C1B1E;font:700 11px/1 Manrope,sans-serif}.sec.sec-empty{background:#FDF8FD;border-style:dashed}.sec.sec-inserted{border-color:#35307E}.sec.sec-changed{box-shadow:inset 4px 0 0 #6A4E00;background:#FFF8E6}
.docthread{position:sticky;top:12px;display:flex;flex-direction:column;gap:8px;border:1px solid #CAC4CF;border-radius:12px;background:#FFFFFF;padding:12px;max-height:calc(100vh - 48px)}.th-h{display:flex;align-items:center;gap:8px}.th-list{display:flex;flex-direction:column;gap:10px;overflow:auto;min-height:0;padding-right:4px}
.turn{display:flex;flex-direction:column;gap:4px}.turn p{margin:0;font-size:14px;line-height:20px}.turn.user p{background:#E3DFFF;color:#191836;border-radius:12px 12px 2px 12px;padding:8px 12px;align-self:flex-end;max-width:92%}.turn.user{align-items:flex-end}.turn.agent p{background:#F8F1FF;border-radius:12px 12px 12px 2px;padding:8px 12px}
.srcs{display:flex;flex-wrap:wrap;gap:4px}.src-pill{font-size:11px;line-height:16px;padding:2px 8px;border-radius:8px;background:#ECE5F4;color:#48454E}
.prop-card{border:1px solid #CAC4CF;border-left:4px solid #80D5D4;border-radius:8px;padding:8px 12px;display:flex;flex-direction:column;gap:6px;background:#FFFFFF}.prop-card p{margin:0;font-size:13px;line-height:19px}
.th-ask{display:flex;gap:8px;align-items:center}.th-ask .in{flex:1;height:40px;padding:0 12px;border:1px solid #79757F;border-radius:4px;font:inherit;font-size:14px;background:#FFFFFF;color:#1C1B1E}.th-ask .in:focus{outline:0;border:2px solid #35307E}
"""

# ----------------------------------------------------------------------------------------------- helpers
def chip(h, extra=''):
    """A status chip bound to an object {cls,g,w}; hidden when cls is 'none'."""
    return f'<span class="st st-{{{{{h}.cls}}}}{(" " + extra) if extra else ""}"><span class="tile" aria-hidden="true">{{{{{h}.g}}}}</span>{{{{{h}.w}}}}</span>'
def chg(h): return f'<span class="chg chg-{{{{{h}.cls}}}}"><b aria-hidden="true">{{{{{h}.g}}}}</b>{{{{{h}.w}}}}</span>'
def track(h, var='t'): return f'<span class="trk" aria-label="Plateaus"><sc-for list="{{{{{h}}}}}" as="{var}" hint-placeholder-count="3"><span class="{{{{{var}.cls}}}}" title="{{{{{var}.title}}}}">{{{{{var}.s}}}}</span></sc-for></span>'
def tile(layer, kind, lg=False): return f'<span class="ax-tile{" lg" if lg else ""} ax-l-{{{{{layer}}}}}" aria-hidden="true"><i class="axg axg-{{{{{kind}}}}}"></i></span>'
def sif(cond, inner, dflt='false'): return f'<sc-if value="{{{{{cond}}}}}" hint-placeholder-val="{{{{{dflt}}}}}">{inner}</sc-if>'
def sfor(lst, var, inner, n=3): return f'<sc-for list="{{{{{lst}}}}}" as="{var}" hint-placeholder-count="{n}">{inner}</sc-for>'
ICON = lambda d, s=18: f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" {ST}>{d}</svg>'
I_SEARCH = ICON('<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>')
I_CHEV = ICON('<path d="M9 6l6 6-6 6"/>', 16)
I_INFO = ICON('<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>', 16)
I_COPY = ICON('<rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/>', 16)

TKROWS = lambda lst: sfor(lst, 't', '<div class="row tkrow"><span class="mono tk-k">{{t.key}}</span><span class="txt"><b>{{t.title}}</b><span>' + sif('t.hasImpl', 'implements ' + sfor('t.implements', 'i', '<button type="button" class="lnk" onClick="{{i.go}}">{{i.title}}</button> ', 2)) + sif('t.hasReplaces', 'retires ' + sfor('t.replaces', 'i', '<button type="button" class="lnk" onClick="{{i.go}}">{{i.title}}</button> ', 2)) + '· {{t.commits}}</span>' + sif('t.hasNote', '<span class="meta">{{t.note}}</span>') + '</span>' + chip('t.chip', 'sm') + '</div>', 4)
DLI = lambda lbl, v, sub, go=None: ('<button type="button" class="dli" onClick="{{' + go + '}}">' if go else '<span class="dli">') + '<span class="lbl">' + lbl + '</span><b>{{' + v + '}}</b>' + ('<span class="s">{{' + sub + '}}</span>' if sub else '') + ('</button>' if go else '</span>')
DELIVERY = ('<div class="dph"><div class="dph-h"><h3 class="h3">Delivery</h3><span class="meta">from the ticketing tool, Git and CI · not in the model</span></div><div class="dline">'
  + DLI('Requirement', 'ch.dl.req', None, 'ch.dl.goReq') + '<span class="dl-arrow" aria-hidden="true">›</span>' + DLI('Gap', 'ch.dl.gap', None, 'ch.dl.goGap') + '<span class="dl-arrow" aria-hidden="true">›</span>' + DLI('Tickets', 'ch.dl.tickets', 'ch.dl.ticketsSub') + '<span class="dl-arrow" aria-hidden="true">›</span>' + DLI('Commits', 'ch.dl.commits', 'ch.dl.commitsSub') + '<span class="dl-arrow" aria-hidden="true">›</span>' + DLI('Version', 'ch.dl.version', 'ch.dl.versionSub') + '</div>'
  + sif('ch.dl.hasTickets', '<div class="rows" style="padding: 0 16px 6px">' + TKROWS('ch.dl.rows') + '</div>') + sif('ch.dl.noTickets', '<p class="meta" style="margin: 0; padding: 0 16px 12px">{{ch.dl.noTicketsNote}}</p>') + '</div>')
MARK = '<svg width="32" height="32" viewBox="0 0 64 64" aria-hidden="true" style="flex: none"><g fill="none" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="6" width="30" height="12" rx="4" stroke="#35307E" stroke-width="4"/><rect x="17" y="26" width="30" height="12" rx="4" stroke="#35307E" stroke-width="4"/><rect x="28" y="46" width="30" height="12" rx="4" stroke="#35307E" stroke-width="4"/><path d="M12 18v14h5M23 38v14h5" stroke="#278383" stroke-width="3" stroke-dasharray="3 4"/></g><circle cx="51" cy="52" r="3.5" fill="#00A56B"/></svg>'

# ----------------------------------------------------------------------------------------------- shell
HEADER = (S.header().replace('<input id="sh-q" type="text" placeholder="Search, or ask the assistant…"', '<input id="sh-q" type="text" placeholder="{{hdrPlaceholder}}" value="{{q}}" onChange="{{onHdrQ}}"').replace('Aurélien Heux, platform admin, account menu', 'Account menu').replace('Aurélien Heux', '{{userName}}').replace('platform · admin', '{{userSub}}').replace('<span class="av">AH</span>', '<span class="av">{{userAv}}</span>'))
RAIL = N.rail(N.LIGHT, 'docs', catalog=True)
NAVBAR = S.navbar(None, 'docs')
ROLE_CHIPS = ('<span class="simlab">PROTOTYPE · VIEW AS</span>' + sfor('roles', 'r', '<button type="button" class="chip {{r.cls}}" aria-pressed="{{r.on}}" onClick="{{r.pick}}">{{r.label}}</button>', 4) + '<span style="width: 1px; height: 24px; background: #CAC4CF; margin: 0 6px"></span>')
SUBHEADER = (f'<div class="subhdr"><a href="#docs" class="ib sh-back" aria-label="Back to Docs" title="Back to Docs">{S.ARROW_BACK}</a>'
             f'<div class="sh-txt">{MARK}<h2 class="sh-t">{{{{entTitle}}}}</h2><span class="sh-c">Architecture model · {{{{counts}}}}</span></div>'
             f'<div class="sh-act">{chip("modelValid")}<span class="meta">{{{{checksPassed}}}}</span></div></div>')
AREA_TABS = ('<div class="tabs" role="tablist" aria-label="Architecture areas">' + sfor('areas', 'a', '<button type="button" role="tab" class="tab {{a.cls}}" aria-selected="{{a.on}}" onClick="{{a.pick}}">{{a.label}}' + sif('a.hasN', '<span class="n">{{a.n}}</span>') + '</button>') + '</div>')

# ----------------------------------------------------------------------------------------------- views area
SIDE_VIEWS = ('<div class="side"><span class="lbl">Level</span><div class="seg full" role="group" aria-label="Level">' + sfor('levels', 'l', '<button type="button" class="{{l.cls}}" aria-pressed="{{l.on}}" onClick="{{l.pick}}">{{l.label}}</button>') + '</div>'
  + sif('isPf', '<label class="lbl" for="pf-sel">Portfolio</label><select id="pf-sel" class="sel" value="{{pf}}" onChange="{{pickPf}}">' + sfor('pfs', 'p', '<option value="{{p.id}}">{{p.title}}</option>', 4) + '</select>')
  + sif('isApp', '<label class="lbl" for="pf-sel2">Portfolio</label><select id="pf-sel2" class="sel" value="{{pf}}" onChange="{{pickPf}}">' + sfor('pfs', 'p', '<option value="{{p.id}}">{{p.title}}</option>', 4) + '</select><label class="lbl" for="app-sel">Application</label><select id="app-sel" class="sel" value="{{app}}" onChange="{{pickApp}}">' + sfor('apps', 'p', '<option value="{{p.id}}">{{p.title}}</option>', 6) + '</select>')
  + '<nav aria-label="Views" style="display: flex; flex-direction: column; gap: 2px">' + sfor('sideList', 'v', '<button type="button" class="sl {{v.cls}}" aria-current="{{v.on}}" onClick="{{v.pick}}"><b>{{v.title}}<span class="vk {{v.kcls}}">{{v.kind}}</span></b><span>{{v.who}}</span></button>', 6) + '</nav></div>')

VIEW_HEAD = ('<div style="display: flex; flex-direction: column; gap: 6px"><span class="lbl">{{scopeLabel}}</span><div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap"><h2 class="h1" style="font-size: 22px; line-height: 28px">{{viewTitle}}</h2><span class="vk">{{viewKind}}</span></div>'
             '<p class="body" style="margin: 0"><b style="font-family: Manrope, sans-serif">For</b> {{viewFor}} &nbsp; <b style="font-family: Manrope, sans-serif">Decides</b> {{viewDecides}}</p>'
             '<details class="meta" style="font-size: 13px"><summary style="cursor: pointer; color: #35307E; font-weight: 600">How to read this view</summary><p class="body" style="margin: 6px 0 0; max-width: 72ch">{{viewHow}}</p></details></div>'
             + '<div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap">' + sif('hasPlateau', '<div class="seg" role="group" aria-label="Plateau">' + sfor('plateaus', 'p', '<button type="button" class="{{p.cls}}" aria-pressed="{{p.on}}" onClick="{{p.pick}}">{{p.title}}</button>') + '</div><span class="meta">{{plateauNote}}</span>') + sif('hasDiagram', '<span style="flex: 1"></span><span class="lbl">Rendering</span><div class="seg small" role="group" aria-label="Rendering">' + sfor('rendSeg', 'r', '<button type="button" class="{{r.cls}}" aria-pressed="{{r.on}}" onClick="{{r.pick}}">{{r.label}}</button>', 2) + '</div>') + '</div>')

MATRIX = sif('isMatrix',
  '<div style="display: flex; flex-direction: column; gap: 10px"><span class="meta">{{mx.summary}}</span>' + sif('mx.ext', '<div class="ext-note"><b>Prototype data</b><span>{{mx.ext}}</span></div>')
  + '<div class="mx-wrap"><table class="mx"><thead>'
  + sif('mx.hasGroups', '<tr><th class="mx-corner"></th>' + sfor('mx.colGroups', 'g', '<th class="mx-grp" colSpan="{{g.span}}">{{g.label}}</th>') + '</tr>')
  + '<tr><th class="mx-corner">{{mx.headLabel}}</th>' + sfor('mx.cols', 'c', '<th class="mx-col {{c.cls}}" title="{{c.title}}"><button type="button" class="mx-colb" onClick="{{c.go}}"><span class="mx-colin"><span class="mx-cl">{{c.label}}</span><span class="mx-cs">{{c.sub}}</span></span></button></th>', 6) + '</tr></thead><tbody>'
  + sfor('mx.rows', 'r', sif('r.group', '<tr class="mx-g"><th colSpan="40">{{r.label}}</th></tr>')
      + sif('r.isRow', '<tr><th class="mx-rh {{r.head.selCls}}"><span class="mx-rhw"><button type="button" class="mx-rhb" onClick="{{r.head.go}}">' + tile('r.head.layer', 'r.head.kind') + '<span class="mx-rt"><b>{{r.head.label}}</b><span>{{r.head.sub}}</span></span></button>' + sif('r.head.warn', '<span class="st st-warning sm" title="{{r.head.warnText}}"><span class="tile" aria-hidden="true">!</span>{{r.head.warnText}}</span>') + '</span></th>'
      + sfor('r.cells', 'c', '<td class="mx-c mx-{{c.cls}}" title="{{c.title}}">{{c.txt}}</td>', 6) + '</tr>'), 8)
  + '</tbody></table></div><div class="legend">' + sfor('mx.legend', 'l', '<span><span class="lg-c mx-{{l.cls}}">{{l.g}}</span><b>{{l.w}}</b> {{l.note}}</span>', 3) + '</div></div>')

CAPMAP = sif('v_capmap', '<div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap"><span class="lbl">Measure</span><div class="seg small" role="group" aria-label="Measure">' + sfor('metrics', 'm', '<button type="button" class="{{m.cls}}" aria-pressed="{{m.on}}" onClick="{{m.pick}}">{{m.label}}</button>') + '</div></div>'
  '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 12px">' + sfor('domains', 'd', '<div class="capdom"><span class="lbl">{{d.title}}</span>' + sfor('d.caps', 'c', '<button type="button" class="capcell {{c.selCls}}" style="{{c.style}}" onClick="{{c.go}}"><span class="cc-t"><span>{{c.title}}</span><span class="cc-v">{{c.val}}<small>{{c.den}}</small></span></span><span class="cc-m"><span>{{c.strategic}}</span><span>{{c.napps}}</span></span>' + sif('c.hasWarn', '<span class="st st-warning sm"><span class="tile" aria-hidden="true">!</span>{{c.warn}}</span>') + '</button>', 4) + '</div>', 7) + '</div>'
  '<div class="legend"><span><span class="lg-c" style="background: color-mix(in srgb, #35307E 80%, #fff)"></span>high</span><span><span class="lg-c" style="background: color-mix(in srgb, #35307E 10%, #fff)"></span>low</span><span>differentiating · core · commodity from the capability metadata (strategic)</span></div>')

TECH = sif('v_tech', '<div class="radar"><div class="rh">Category</div>' + sfor('rings', 'r', '<div class="rh">{{r.label}}<small>{{r.hint}}</small></div>', 4)
  + sfor('techRows', 'row', '<div class="rc">{{row.label}}</div>' + sfor('row.cells', 'c', '<div>' + sfor('c.items', 'i', '<button type="button" class="techchip {{i.cls}}" onClick="{{i.go}}"><i aria-hidden="true"></i>{{i.title}}<span class="n">{{i.n}}</span></button>', 2) + '</div>', 4), 6) + '</div>'
  '<span class="lbl">{{riskyN}}</span><div class="tb"><table><thead><tr><th class="th">Application</th><th class="th">Portfolio</th><th class="th">Standard</th><th class="th">Lifecycle</th><th class="th">TIME</th></tr></thead><tbody>'
  + sfor('risky', 'r', '<tr class="rowb" onClick="{{r.go}}"><td class="td"><b style="font-family: Manrope, sans-serif">{{r.app}}</b></td><td class="td">{{r.pf}}</td><td class="td">{{r.tech}}</td><td class="td">' + chip('r.ring') + '</td><td class="td">' + chip('r.time') + '</td></tr>', 6) + '</tbody></table></div>')

ROADMAP = ('<div class="rm"><div class="rm-in"><div class="rm-months">' + sfor('rm.months', 'm', '<span class="{{m.cls}}">{{m.label}}</span>', 19) + '</div>'
  + sfor('rm.bands', 'b', '<div class="rm-band"><div class="rm-h"><button type="button" onClick="{{b.go}}">{{b.title}}</button><span class="meta">{{b.plateaus.length}} plateaus</span></div><div class="rm-track"><span class="rm-today" style="{{rm.todayStyle}}" title="Today"></span>'
      + sfor('b.plateaus', 'p', '<span class="rm-pl" style="{{p.style}}"><b>◆</b> {{p.title}}</span>', 3)
      + '<div style="height: 30px"></div>' + sfor('b.wps', 'w', '<div class="rm-wp"><button type="button" class="rm-bar {{w.cls}}" style="{{w.style}}" title="{{w.title}} · {{w.dates}} · {{w.klass}}" onClick="{{w.go}}">{{w.title}}</button>' + sif('w.hasDep', '<span class="rm-dep" style="{{w.style}}">{{w.dep}}</span>') + '</div>', 3) + '</div></div>', 4) + '</div></div>'
  '<div class="legend"><span><span class="lg-c mx-on">■</span>ready · planned</span><span><span class="lg-c" style="background: #ACF4A2; color: #1B5F1F">■</span>approved by the board</span><span><span class="lg-c mx-warn">■</span>in review</span><span><span class="lg-c mx-off" style="border-style: dashed">■</span>draft</span><span><b style="color: #35307E">◆</b> plateau</span><span><span style="display: inline-block; width: 2px; height: 14px; background: #93000A; vertical-align: -2px; margin-right: 6px"></span>today</span></div>')
ENTROADMAP = sif('v_entroadmap', ROADMAP)
PFROADMAP = sif('v_pfroadmap', ROADMAP)

LANDSCAPE = sif('v_landscape', '<div style="display: flex; flex-direction: column; gap: 8px">' + sfor('lsRows', 'r', '<div class="lsrow"><div class="lshead"><button type="button" class="{{r.selCls}}" onClick="{{r.go}}">' + tile("'strategy'", "'capability'") + '{{r.title}}</button><span class="meta">{{r.n}}</span></div><div class="lscells">' + sfor('r.cells', 'c', '<div class="lsapp {{c.cls}}"><button type="button" class="figb" onClick="{{c.go}}"><span>{{c.title}}</span><i class="axg axg-application-component" aria-hidden="true"></i></button><span class="chips">' + chip('c.time', 'sm') + chg('c.change') + '</span></div>', 3) + '</div></div>', 6) + '</div>'
  '<div class="legend"><span>' + ''.join(f'<span class="st st-{c} sm" style="margin-right: 4px"><span class="tile">{g}</span>{w}</span>' for c, g, w in [('success', '↑', 'Invest'), ('neutral', '=', 'Tolerate'), ('warning', '→', 'Migrate'), ('error', '✕', 'Eliminate')]) + ' TIME lifecycle</span><span>' + ''.join(f'<span class="chg chg-{c}" style="margin-right: 4px"><b>{g}</b>{w}</span>' for c, g, w in [('new', '+', 'New'), ('changed', 'Δ', 'Changed'), ('retired', '−', 'Retired')]) + ' since the previous plateau</span></div>')

FIG = ('<span class="figw"><button type="button" class="axf ax-l-{{f.layer}} ax-shape-{{f.shape}} {{f.cls}}" onClick="{{f.go}}" title="{{f.kname}} · {{f.title}}"><span class="ax-in"><span class="ax-name">{{f.title}}</span></span><i class="axg axg-{{f.kind}} ax-glyph" aria-hidden="true"></i></button>' + sif('f.hasRel', '<span class="rel">{{f.rel}}</span>') + '</span>')
GRIDS = sif('showGrids', sfor('gds', 'g', '<div style="display: flex; flex-direction: column; gap: 8px"><div style="display: flex; align-items: baseline; gap: 12px; flex-wrap: wrap"><span class="lbl">{{g.title}}</span>' + sif('g.hasNote', '<span class="meta">{{g.note}}</span>') + '</div><div class="gd-wrap"><div class="gd" style="grid-template-columns: {{g.tpl}}">'
  + sfor('g.cols', 'c', '<div class="gd-h"><b>{{c.label}}</b><span>{{c.sub}}</span></div>', 4)
  + sfor('g.rows', 'r', '<div style="display: contents">' + sfor('r.cells', 'c', '<div class="gd-c {{c.cls}}">' + sfor('c.figs', 'f', FIG, 2) + sif('c.hasNote', '<span class="meta gd-note">{{c.note}}</span>') + '</div>', 4) + '</div>', 3)
  + '</div></div></div>', 2)
  + '<div class="legend">' + ''.join(f'<span><span class="sw ax-l-{k}"></span>{v}</span>' for k, v in [('strategy', 'Strategy'), ('business', 'Business'), ('application', 'Application'), ('technology', 'Technology'), ('motivation', 'Motivation'), ('implementation', 'Implementation')]) + '<span>the relationship is the column, its name under the figure</span><span><span class="lg-c" style="box-shadow: 0 0 0 2px #1B5F1F; border: 0"> </span>new</span><span><span class="lg-c" style="border: 2px dotted #6A4E00"> </span>changed</span><span><span class="lg-c" style="opacity: .45; background: #CAC4CF" aria-hidden="true"> </span>retired · faded = other portfolio or platform</span></div>')
RELS = sif('hasRelRows', '<span class="lbl">{{relN}}</span><div class="tb"><table><thead><tr><th class="th">From</th><th class="th">Relationship</th><th class="th">To</th><th class="th">Label</th></tr></thead><tbody>' + sfor('relRows', 'r', '<tr><td class="td"><button type="button" class="lnk" onClick="{{r.goFrom}}">{{r.from}}</button></td><td class="td">{{r.kind}}' + sif('r.ext', ' <span class="vk">proto</span>') + '</td><td class="td"><button type="button" class="lnk" onClick="{{r.goTo}}">{{r.to}}</button></td><td class="td mono" style="font-size: 12px">{{r.label}}</td></tr>', 8) + '</tbody></table></div>')

COOP_TABLE = sif('v_cooperation', '<span class="lbl">{{flowN}}</span><div class="tb"><table><thead><tr><th class="th">From</th><th class="th">Flow</th><th class="th">To</th></tr></thead><tbody>' + sfor('flowRows', 'f', '<tr><td class="td"><button type="button" class="lnk" onClick="{{f.goFrom}}">{{f.from}}</button> <span class="meta">{{f.pfFrom}}</span></td><td class="td">{{f.what}}</td><td class="td"><button type="button" class="lnk" onClick="{{f.goTo}}">{{f.to}}</button> <span class="meta">{{f.pfTo}}</span></td></tr>', 6) + '</tbody></table></div>')

GAP_HEAD = sif('v_gap', '<div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap"><div class="seg" role="group" aria-label="Transition">' + sfor('gaps', 'g', '<button type="button" class="{{g.cls}}" aria-pressed="{{g.on}}" onClick="{{g.pick}}">{{g.label}}</button>', 2) + '</div><span class="meta">{{gapSummary}}</span>' + sif('hasGapReqs', '<span class="meta">· justified by ' + sfor('gapReqs', 'q', '<button type="button" class="lnk" onClick="{{q.go}}">{{q.title}}</button> ', 1) + '</span>') + '</div>')
GAP = sif('v_gap', '<div class="tb"><table><thead><tr><th class="th">Building block</th><th class="th">Change</th><th class="th">Level</th><th class="th">Plateaus</th><th class="th">Addressed by</th><th class="th">Delivery</th><th class="th">Review</th></tr></thead><tbody>'
  + sfor('gapRows', 'r', '<tr><td class="td"><button type="button" class="rowbtn" onClick="{{r.go}}">' + tile('r.layer', 'r.k') + '<span class="tt"><span class="ttx"><b>{{r.title}}</b><span>{{r.kind}}</span></span></span></button></td><td class="td">' + chg('r.change') + '</td><td class="td">{{r.level}}</td><td class="td">' + track('r.track') + '</td><td class="td">' + sfor('r.by', 'b', '<button type="button" class="lnk" onClick="{{b.go}}">{{b.title}}</button>', 1) + '</td><td class="td {{r.dlCls}}">{{r.dl}}</td><td class="td">' + sif('r.hasArb', '<button type="button" class="lnk" onClick="{{r.goArb}}">' + chip('r.arb', 'sm') + '</button>') + '</td></tr>', 8) + '</tbody></table></div>')

FACTS = sif('v_factsheet', '<div class="cards">'
  '<div class="cardx" style="grid-column: 1 / -1"><div class="cc-h"><h3 class="h3">{{fs.title}}</h3>' + chip('fs.time') + chip('fs.status') + chg('fs.change') + track('fs.track') + '</div><dl class="kv"><dt>Portfolio</dt><dd><button type="button" class="lnk" onClick="{{fs.goPf}}">{{fs.pf}}</button></dd><dt>Criticality</dt><dd>{{fs.crit}}</dd><dt>Owner</dt><dd class="mono">{{fs.owner}}</dd><dt>Sourcing · hosting</dt><dd>{{fs.sourcing}} · {{fs.hosting}}</dd><dt>Elements id</dt><dd class="mono">{{fs.id}}</dd><dt>Component</dt><dd><button type="button" class="lnk" onClick="{{fs.goComp}}">open the application component</button></dd></dl></div>'
  '<div class="cardx"><span class="lbl">Capabilities realized <span class="n">{{fs.nCaps}}</span></span><div class="rows">' + sfor('fs.caps', 'c', '<button type="button" class="row" onClick="{{c.go}}">' + tile('c.layer', 'c.kind') + '<span class="txt"><b>{{c.title}}</b></span>' + I_CHEV + '</button>') + '</div></div>'
  '<div class="cardx"><span class="lbl">Data <span class="n">{{fs.nData}}</span></span><div class="rows">' + sfor('fs.data', 'd', '<button type="button" class="row" onClick="{{d.go}}">' + tile("'application'", "'data-object'") + '<span class="txt"><b>{{d.title}}</b><span>{{d.bo}}</span></span>' + chip('d.mode', 'sm') + '</button>') + '</div></div>'
  '<div class="cardx"><span class="lbl">Flows <span class="n">{{fs.nFlows}}</span></span><div class="rows">' + sfor('fs.flows', 'f', '<button type="button" class="row" onClick="{{f.go}}"><span class="mono" style="width: 16px; text-align: center">{{f.dir}}</span><span class="txt"><b>{{f.other}}</b><span>{{f.what}}</span></span>' + I_CHEV + '</button>', 4) + '</div></div>'
  '<div class="cardx"><span class="lbl">Platforms <span class="n">{{fs.nTech}}</span></span><div class="rows">' + sfor('fs.tech', 't', '<button type="button" class="row" onClick="{{t.go}}">' + tile("'technology'", "'system-software'") + '<span class="txt"><b>{{t.title}}</b></span>' + chip('t.life', 'sm') + '</button>') + '</div></div>'
  '<div class="cardx"><span class="lbl">Changes <span class="n">{{fs.nWps}}</span></span><div class="rows">' + sfor('fs.wps', 'w', '<button type="button" class="row" onClick="{{w.go}}">' + tile("'implementation'", "'work-package'") + '<span class="txt"><b>{{w.title}}</b><span>{{w.what}} this application · {{w.klass}}</span></span>' + chip('w.status', 'sm') + '</button>', 2) + '</div></div>'
  + sif('fs.hasHealth', '<div class="cardx"><span class="lbl">Documentation</span><dl class="kv kv-stack"><dt>Coverage</dt><dd>' + chip('fs.health.covChip', 'sm') + ' {{fs.health.coverage}} · {{fs.health.contracts}}</dd><dt>Freshness</dt><dd>' + chip('fs.health.freshChip', 'sm') + ' {{fs.health.fresh}}</dd><dt>Origin</dt><dd>' + chip('fs.health.originChip', 'sm') + '</dd><dt>Drift</dt><dd>' + chip('fs.health.driftChip', 'sm') + ' {{fs.health.drifts}}</dd><dt>Owner</dt><dd>{{fs.health.owner}}</dd></dl></div>') +
  '<div class="cardx"><span class="lbl">Decisions <span class="n">{{fs.nAdrs}}</span></span><div class="rows">' + sfor('fs.adrs', 'a', '<button type="button" class="row" onClick="{{a.go}}">' + tile("'other'", "'decision'") + '<span class="txt"><b>{{a.title}}</b></span>' + I_CHEV + '</button>', 1) + '</div></div>'
  '<div class="cardx"><span class="lbl">Interfaces <span class="n">{{fs.nIfaces}}</span></span><div class="rows">' + sfor('fs.ifaces', 'i', '<button type="button" class="row" onClick="{{i.go}}">' + tile("'application'", "'application-interface'") + '<span class="txt"><b>{{i.title}}</b><span class="mono">{{i.contract}}</span></span></button>', 1) + '</div></div>'
  '</div>')

IFACES = sif('v_interfaces', '<span class="lbl">{{ifN}}</span><div class="tb"><table><thead><tr><th class="th">Interface</th><th class="th">Realizes</th><th class="th">Contract</th><th class="th">Status</th><th class="th">Plateaus</th></tr></thead><tbody>'
  + sfor('ifRows', 'i', '<tr class="rowb" onClick="{{i.go}}"><td class="td"><span class="tt">' + tile("'application'", "'application-interface'") + '<b>{{i.title}}</b></span></td><td class="td">{{i.realizes}}</td><td class="td"><span class="mono" style="font-size: 12px">{{i.contract}}</span> ' + chip('i.ok', 'sm') + '</td><td class="td">' + chip('i.status', 'sm') + '</td><td class="td">' + track('i.track') + '</td></tr>', 2) + '</tbody></table></div>'
  '<div class="tb"><table><thead><tr><th class="th">Data object</th><th class="th">Business object</th><th class="th">Role</th><th class="th">Access</th><th class="th">Plateaus</th></tr></thead><tbody>'
  + sfor('dataRows', 'd', '<tr class="rowb" onClick="{{d.go}}"><td class="td"><span class="tt">' + tile("'application'", "'data-object'") + '<b>{{d.title}}</b></span></td><td class="td">{{d.bo}}</td><td class="td">' + chip('d.mode', 'sm') + '</td><td class="td">{{d.access}}</td><td class="td">' + track('d.track') + '</td></tr>', 3) + '</tbody></table></div>')

DIAGRAM = sif('isDiagram', '<div class="gv-zoomwrap" style="{{zoomStyle}}"><div class="selwrap sel-{{selSid}}">' + G.build_all(D) + '</div></div>')
PANEL = ('<div class="vpanel"><span class="vp-mark">{{frameMark}}</span>' + sif('canBack', '<button type="button" class="vp-back" aria-label="Back to the previous view" title="Back" onClick="{{goBack}}">' + ICON('<path d="M15 6l-6 6 6 6"/>', 16) + '</button>')
         + '<nav aria-label="View path" style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap">' + sfor('crumbs', 'c', '<button type="button" class="vp-cb" aria-current="{{c.cur}}" onClick="{{c.go}}">{{c.label}}</button>' + sif('c.more', '<span class="vp-sep" aria-hidden="true">›</span>'), 3) + '</nav>'
         + sif('isDiagram', '<div class="zoomg" role="group" aria-label="Zoom"><button type="button" aria-label="Zoom in" onClick="{{zoomIn}}">+</button><button type="button" aria-label="Zoom out" onClick="{{zoomOut}}">−</button><button type="button" class="fit" onClick="{{zoomFit}}">Fit</button></div>')
         + '<code class="vp-id">{{viewId}}</code></div>')
CARD = sif('hasCard', '<aside class="card-el" aria-label="Element details"><div class="ce-h">' + tile('card.layer', 'card.k', True) + '<div style="flex: 1; min-width: 0"><b>{{card.title}}</b><span class="meta">{{card.kind}}</span></div><button type="button" class="ib" aria-label="Close the details" style="margin: -6px -6px 0 0" onClick="{{card.close}}">✕</button></div>'
  + '<div style="display: flex; gap: 6px; flex-wrap: wrap">' + chg('card.change') + chip('card.status', 'sm') + '</div>' + sif('card.hasDesc', '<p class="ce-desc">{{card.desc}}</p>')
  + '<dl class="kv"><dt>Plateaus</dt><dd>' + track('card.track') + '</dd><dt>Owner</dt><dd class="mono" style="font-size: 12px">{{card.owner}}</dd><dt>Origin</dt><dd>{{card.origin}}</dd></dl>'
  + sif('card.hasRels', '<span class="lbl">{{card.relsTitle}}</span><div style="display: flex; flex-direction: column">' + sfor('card.rels', 'r', '<button type="button" class="ce-rel" onClick="{{r.pick}}"><span class="ce-verb">{{r.verb}}</span>' + sif('r.hasTile', tile('r.layer', 'r.kind')) + '<span class="nm">{{r.name}}' + sif('r.hasLabel', '<span>{{r.label}}</span>') + '</span>' + sif('r.ext', '<span class="vk">proto</span>') + '</button>', 4) + '</div>')
  + sif('card.hasNav', '<button type="button" class="btn f sm" style="align-self: flex-start" onClick="{{card.nav}}">{{card.navLabel}}</button>')
  + '<div style="display: flex; gap: 8px; flex-wrap: wrap; align-items: center"><button type="button" class="btn t sm" onClick="{{card.open}}">Open in the elements</button>' + sif('card.hasDd', '<button type="button" class="chip" onClick="{{card.dd}}">Detailed design</button>') + sif('card.hasApp', '<button type="button" class="chip" onClick="{{card.openApp}}">Fact sheet · {{card.appTitle}}</button>') + '</div></aside>')
FOOT = ('<div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap"><span class="meta" style="flex: 1; min-width: 220px">{{generatedLine}}</span><button type="button" class="lnk" aria-expanded="{{srcOn}}" onClick="{{toggleSrc}}">{{srcLabel}}</button></div>' + sif('srcOn', '<pre class="srcbox">{{viewSrc}}</pre>'))
VIEW_BLOCKS = '<div class="vframe {{frameCls}}"><div class="vbody">' + PANEL + CAPMAP + MATRIX + TECH + ENTROADMAP + PFROADMAP + LANDSCAPE + GAP_HEAD + GRIDS + DIAGRAM + COOP_TABLE + GAP + RELS + FACTS + IFACES + FOOT + '</div>' + CARD + '</div>'
VIEWS_AREA = sif('isViews', '<div class="area">' + SIDE_VIEWS + '<div class="content">' + VIEW_HEAD + VIEW_BLOCKS + '</div></div>')

# ----------------------------------------------------------------------------------------------- elements
SEARCH = ('<div class="srch">' + I_SEARCH + '<label for="cat-q" style="position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0)">Filter the elements</label><input id="cat-q" type="text" placeholder="Filter by name, id, type or owner" value="{{q}}" onChange="{{onQ}}">' + sif('hasQ', '<button type="button" aria-label="Clear" onClick="{{clearQ}}">✕</button>') + '</div>')
CAT_APPS = sif('isCatApps', '<span class="meta">Every application with its portfolio and lifecycle. Open one to see its fact sheet.</span><div class="tb"><table><thead><tr><th class="th">Application</th><th class="th">Portfolio</th><th class="th">TIME</th><th class="th">Criticality</th><th class="th">Owner</th><th class="th">Hosting</th><th class="th">Plateaus</th><th class="th">Change</th></tr></thead><tbody>'
  + sfor('appRows', 'a', '<tr class="rowb" onClick="{{a.go}}"><td class="td"><span class="tt">' + tile("'application'", "'application-component'") + '<span class="ttx"><b>{{a.title}}</b><span class="mono">{{a.id}}</span></span></span></td><td class="td">{{a.pf}}</td><td class="td">' + chip('a.time', 'sm') + '</td><td class="td">{{a.crit}}</td><td class="td mono" style="font-size: 12px">{{a.owner}}</td><td class="td">{{a.hosting}}</td><td class="td">' + track('a.track') + '</td><td class="td">' + chg('a.change') + '</td></tr>', 8) + '</tbody></table></div>')
CAT_TREE = sif('isCatTree', '<div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap"><div class="seg small" role="group" aria-label="Tree by">' + sfor('treeModes', 'm', '<button type="button" class="{{m.cls}}" aria-pressed="{{m.on}}" onClick="{{m.pick}}">{{m.label}}</button>', 2) + '</div><span class="meta">{{treeN}}</span><span style="flex: 1"></span><button type="button" class="btn x" onClick="{{expandAll}}">Expand all</button><button type="button" class="btn x" onClick="{{collapseAll}}">Collapse all</button></div>'
  '<div class="tree" role="tree">' + sfor('tree', 'n',
      sif('n.isLeaf', '<div class="tn" role="treeitem" style="{{n.pad}}"><span class="leafsp"></span><button type="button" class="tnb" onClick="{{n.go}}">' + tile('n.layer', 'n.kind') + '<span class="tnt"><b>{{n.title}}</b><span>{{n.sub}}</span></span></button><span class="tnr">' + sif('n.ext', '<span class="vk" title="Prototype data">proto</span>') + chg('n.change') + track('n.track') + chip('n.status', 'sm') + '</span></div>')
      + sif('n.open', '<div class="tn {{n.cls}}" role="treeitem" aria-expanded="true" style="{{n.pad}}"><button type="button" class="tog" aria-label="Collapse" onClick="{{n.toggle}}">▾</button><button type="button" class="tnb" onClick="{{n.toggle}}">' + sif('n.hasTile', tile('n.layer', 'n.kind')) + '<span class="tnt"><b>{{n.title}}</b><span>{{n.sub}}</span></span></button><span class="tnr">' + sif('n.hasGoApp', '<button type="button" class="lnk" style="font-size: 12px" onClick="{{n.goApp}}">fact sheet</button>') + chg('n.change') + track('n.track') + '<span class="cnt">{{n.n}}</span></span></div>')
      + sif('n.isBranchClosed', '<div class="tn {{n.cls}}" role="treeitem" aria-expanded="false" style="{{n.pad}}"><button type="button" class="tog" aria-label="Expand" onClick="{{n.toggle}}">▸</button><button type="button" class="tnb" onClick="{{n.toggle}}">' + sif('n.hasTile', tile('n.layer', 'n.kind')) + '<span class="tnt"><b>{{n.title}}</b><span>{{n.sub}}</span></span></button><span class="tnr">' + sif('n.hasGoApp', '<button type="button" class="lnk" style="font-size: 12px" onClick="{{n.goApp}}">fact sheet</button>') + chg('n.change') + track('n.track') + '<span class="cnt">{{n.n}}</span></span></div>'), 12)
  + '</div>')
CAT_ELS = sif('isCatEls', '<div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap">' + sfor('catLevels', 'l', '<button type="button" class="chip {{l.cls}}" aria-pressed="{{l.on}}" onClick="{{l.pick}}">{{l.label}} <span class="n">{{l.n}}</span></button>', 8) + '<select class="sel" style="width: auto; height: 32px" aria-label="Scope" value="{{catScope}}" onChange="{{pickScope}}">' + sfor('catScopes', 'sc', '<option value="{{sc.id}}">{{sc.label}}</option>', 4) + '</select><span class="meta">{{elN}}</span></div>'
  '<div class="tb"><table><thead><tr><th class="th">Element</th><th class="th">Level</th><th class="th">Scope</th><th class="th">Owner</th><th class="th">Plateaus</th><th class="th">Change</th><th class="th">Status</th><th class="th">Origin</th></tr></thead><tbody>'
  + sfor('elRows', 'e', '<tr class="rowb" onClick="{{e.go}}"><td class="td"><span class="tt">' + tile('e.layer', 'e.k') + '<span class="ttx"><b>{{e.title}}</b><span>{{e.kind}} · <span class="mono" style="font-weight: 400">{{e.id}}</span></span></span></span></td><td class="td">{{e.level}}</td><td class="td">{{e.scope}}</td><td class="td mono" style="font-size: 12px">{{e.owner}}</td><td class="td">' + track('e.track') + '</td><td class="td">' + chg('e.change') + '</td><td class="td">' + chip('e.status', 'sm') + '</td><td class="td meta">{{e.origin}}</td></tr>', 10) + '</tbody></table></div>')
CAT_FLAT = sif('aFlat', '<div class="tree">' + sfor('aRows', 'e', '<div class="tn" style="padding-left: 12px"><button type="button" class="tnb" onClick="{{e.go}}">' + tile('e.layer', 'e.k') + '<span class="tnt"><b>{{e.title}}</b><span class="path">{{e.kind}} · {{e.path}}</span></span></button><span class="tnr">' + chg('e.change') + track('e.track') + chip('e.status', 'sm') + '</span></div>', 8) + '</div>')
CAT_AREA = sif('isCat', '<div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap"><span class="lbl">Group by</span><div class="seg small" role="group" aria-label="Group by">' + sfor('treeModes', 'm', '<button type="button" class="{{m.cls}}" aria-pressed="{{m.on}}" onClick="{{m.pick}}">{{m.label}}</button>', 2) + '</div><span class="meta">{{aN}}</span>' + sif('hasQ', '<button type="button" class="chip" onClick="{{clearQ}}">✕ Clear the search</button>') + '<span style="flex: 1"></span><button type="button" class="btn x" onClick="{{expandAll}}">Expand all</button><button type="button" class="btn x" onClick="{{collapseAll}}">Collapse all</button></div>'
  + sif('aTree', '<div class="tree" role="tree">' + CAT_TREE.replace("<sc-if value=\"{{isCatTree}}\" hint-placeholder-val=\"{{false}}\">", "").rsplit('</sc-if>', 1)[0].split('<div class="tree" role="tree">', 1)[1]) + CAT_FLAT)

# ----------------------------------------------------------------------------------------------- element page
REL_ROW = lambda lst: sfor(lst, 'r', '<button type="button" class="row" onClick="{{r.go}}"><span class="meta" style="min-width: 110px">{{r.verb}}{{r.label}}</span>' + sif('r.hasTile', tile('r.layer', 'r.kind')) + '<span class="txt"><b>{{r.other}}</b></span>' + sif('r.ext', '<span class="vk">proto</span>') + I_CHEV + '</button>', 4)
ELEMENT = sif('isElementPage',
  S.subheader('{{backHome}}', '{{el.backLabel}}', '{{el.title}}', '{{el.kind}} · {{el.level}} ({{el.levelHint}}) · {{el.scope}}', chip('el.status') + chg('el.change') + track('el.track'), lead=tile('el.layer', 'el.k', True))
  + sif('el.ext', '<div class="ext-note"><b>Prototype data</b><span>This element was added for the prototype (business roles and process support); it is not in the Meridian Bank model files yet.</span></div>')
  + '<div class="cards"><div class="cardx" style="grid-column: 1 / -1">' + sif('el.hasDesc', '<p class="body" style="margin: 0">{{el.desc}}</p>') + '<dl class="kv"><dt>Owner</dt><dd class="mono">{{el.owner}}</dd><dt>Source</dt><dd class="mono" style="font-size: 12px">{{el.path}}</dd>' + sif('el.hasModule', '<dt>Module</dt><dd class="mono">{{el.module}}</dd>') + sif('el.hasWi', '<dt>Work item</dt><dd class="mono">{{el.wi}}</dd>') + sif('el.hasContract', '<dt>Contract</dt><dd class="mono">{{el.contract}}</dd>') + sfor('el.meta', 'm', '<dt>{{m.k}}</dt><dd>{{m.v}}</dd>', 2) + sif('el.hasApp', '<dt>Application</dt><dd><button type="button" class="lnk" onClick="{{el.goApp}}">{{el.appTitle}} · fact sheet</button></dd>') + '</dl>'
  + sif('el.hasArb', '<div class="ext-note" style="background: #E3DFFF"><b>Review</b><button type="button" class="lnk" onClick="{{el.arb.go}}">{{el.arb.title}}</button>' + chip('el.arb.status', 'sm') + '</div>') + '</div>'
  + sif('el.hasDecision', '<div class="cardx" style="grid-column: 1 / -1"><span class="lbl">Decision · {{el.domainRef}}</span><p class="body" style="margin: 0">{{el.decision}}</p>' + sif('el.hasAffects', '<span class="lbl">Affects</span><div class="rows">' + sfor('el.affects', 'a', '<button type="button" class="row" onClick="{{a.go}}"><span class="txt"><b>{{a.title}}</b></span>' + I_CHEV + '</button>') + '</div>') + '</div>')
  + sif('el.hasAcceptance', '<div class="cardx" style="grid-column: 1 / -1"><span class="lbl">Acceptance criteria · each row becomes a test</span><div class="tb"><table><thead><tr><th class="th">Given</th><th class="th">When</th><th class="th">Then</th></tr></thead><tbody>' + sfor('el.acceptance', 'a', '<tr><td class="td">{{a.given}}</td><td class="td">{{a.when}}</td><td class="td">{{a.then}}</td></tr>') + '</tbody></table></div>'
      + sif('el.hasDecTable', '<span class="lbl">Decision table</span><div class="tb"><table><thead><tr><th class="th">Case</th><th class="th">Outcome</th><th class="th">Reason</th></tr></thead><tbody>' + sfor('el.decTable', 'd', '<tr><td class="td">{{d.c}}</td><td class="td">' + sif('d.ok', '<span class="st st-success sm"><span class="tile">✓</span>OK</span>') + sif('d.ok', '', 'true').replace('<sc-if value="{{d.ok}}" hint-placeholder-val="{{true}}"></sc-if>', '') + '<span class="mono">{{d.outcome}}</span></td><td class="td mono">{{d.reason}}</td></tr>') + '</tbody></table></div>')
      + sif('el.hasOperational', '<span class="lbl">Operational figures</span><dl class="kv">' + sfor('el.operational', 'o', '<dt class="mono">{{o.k}}</dt><dd>{{o.v}}</dd>', 2) + '</dl>') + '</div>')
  + sif('el.rq.has', '<div class="cardx" style="grid-column: 1 / -1"><span class="lbl">Delivery · {{el.rq.progress}}</span>' + sif('el.rq.hasGaps', '<span class="meta">Gaps it justifies, by change</span><div class="rows">' + sfor('el.rq.gaps', 'g', '<button type="button" class="row" onClick="{{g.go}}">' + tile("'implementation'", "'work-package'") + '<span class="txt"><b>{{g.title}}</b><span>{{g.sub}}</span></span>' + chip('g.status', 'sm') + '</button>', 2) + '</div>') + sif('el.rq.hasRows', '<span class="meta">Tickets that realize it</span><div class="rows">' + TKROWS('el.rq.rows') + '</div>') + '</div>')
  + sif('el.ctx.has', '<div class="cardx" style="grid-column: 1 / -1"><span class="lbl">Context for code generation</span><span class="meta">What agents get from the knowledge base — Sweep runs and your coding assistant alike.' + sif('el.ctx.hasReq', ' Realizes <button type="button" class="lnk" onClick="{{el.ctx.goReq}}">{{el.ctx.req}}</button> · {{el.ctx.reqRows}}') + '</span><div class="rows">' + sfor('el.ctx.chain', 'x', '<button type="button" class="row ctx-row" onClick="{{x.go}}"><span class="ctx-verb">{{x.verb}}</span>' + tile('x.layer', 'x.k') + '<span class="txt"><b>{{x.title}}</b><span>{{x.kind}}' + sif('x.sub', ' · {{x.sub}}') + '</span></span>' + I_CHEV + '</button>', 4) + '</div>' + sif('el.ctx.hasStandards', '<span class="meta">Standards given with it: {{el.ctx.standards}}</span>') + '</div>')
  + '<div class="cardx"><span class="lbl">Relationships <span class="n">{{el.nRel}}</span></span>' + sif('el.hasOuts', '<span class="meta">Outgoing</span><div class="rows">' + REL_ROW('el.outs') + '</div>') + sif('el.hasIns', '<span class="meta">Incoming</span><div class="rows">' + REL_ROW('el.ins') + '</div>') + '</div>'
  + '<div class="cardx"><span class="lbl">Where it appears</span><div class="rows">' + sfor('el.views', 'v', '<button type="button" class="row" onClick="{{v.go}}"><span class="txt"><b>{{v.label}}</b></span>' + I_CHEV + '</button>') + '</div>'
      + sif('el.hasWps', '<span class="lbl">Changes</span><div class="rows">' + sfor('el.wps', 'w', '<button type="button" class="row" onClick="{{w.go}}">' + tile("'implementation'", "'work-package'") + '<span class="txt"><b>{{w.title}}</b><span>{{w.what}} this element</span></span>' + chip('w.status', 'sm') + '</button>', 1) + '</div>')
      + sif('el.dl.hasRows', '<span class="lbl">Delivered by</span><div class="rows">' + TKROWS('el.dl.rows') + '</div>') + sif('el.dl.hasReplacedBy', '<span class="lbl">Replaced by</span><div class="rows">' + sfor('el.dl.replacedBy', 'r', '<button type="button" class="row" onClick="{{r.goBy}}"><span class="txt"><b>{{r.by}}</b><span>{{r.key}} · {{r.title}}</span></span>' + chip('r.chip', 'sm') + '</button>', 1) + '</div>') + sif('el.dl.hasCommits', '<span class="meta">{{el.dl.commits}}</span>')
      + sif('el.hasDd', '<span class="lbl">Detailed design</span><div class="rows">' + sfor('el.dd', 'd', '<button type="button" class="row" onClick="{{d.go}}">' + tile("'other'", "'domain'") + '<span class="txt"><b>{{d.title}}</b></span>' + chip('d.status', 'sm') + '</button>', 1) + '</div>')
      + sif('el.hasRealizes', '<span class="lbl">Realizes</span><div class="rows">' + sfor('el.realizes', 'd', '<button type="button" class="row" onClick="{{d.go}}"><span class="txt"><b>{{d.title}}</b></span>' + I_CHEV + '</button>', 1) + '</div>')
      + sif('el.hasAdrs', '<span class="lbl">Decisions</span><div class="rows">' + sfor('el.adrs', 'd', '<button type="button" class="row" onClick="{{d.go}}">' + tile("'other'", "'decision'") + '<span class="txt"><b>{{d.title}}</b></span>' + I_CHEV + '</button>', 1) + '</div>') + '</div>'
  + sif('el.hasHtml', '<div class="cardx" style="grid-column: 1 / -1"><span class="lbl">Content</span><div class="htmlbox prose" style="white-space: normal">{{el.htmlText}}</div></div>')
  + sif('el.hasSrc', '<div class="cardx" style="grid-column: 1 / -1"><span class="lbl">Source · {{el.lang}}</span><pre class="srcbox">{{el.src}}</pre></div>')
  + '</div>')

# ----------------------------------------------------------------------------------------------- process
SIDE_PROC = '<div class="side"><nav aria-label="Process" style="display: flex; flex-direction: column; gap: 2px">' + sfor('procList', 'p', '<button type="button" class="sl {{p.cls}}" aria-current="{{p.on}}" onClick="{{p.pick}}"><b>{{p.title}}</b><span>{{p.who}}</span></button>', 5) + '</nav></div>'
OG = lambda p: '<span class="og {{' + p + '.cls}}" aria-hidden="true">{{' + p + '.g}}</span>'
MINITRACK = ('<span class="trk2" role="img" aria-label="Phases of the change">' + sfor('c.flow', 'f', '<span class="d {{f.cls}}" title="{{f.title}} · {{f.state}}">{{f.n}}</span>' + sif('f.hasGate', '<span class="gt {{f.gateCls}}" title="{{f.gateTitle}}"><i>{{f.gate}}</i></span>') + sif('f.noGate', '<span class="l"></span>'), 6) + '<span class="d {{c.deliveredCls}}" title="Delivered · {{c.deliveredState}}">✓</span></span>')
TLEGEND = ('<div class="tlegend" aria-hidden="true"><span class="trk2"><span class="d ph-done">1</span></span>done<span class="trk2"><span class="d ph-current">2</span></span>current<span class="trk2"><span class="d ph-skipped">0</span></span>skipped, the change entered later'
           '<span class="gt gt-passed" style="margin: 0"><i>G</i></span>gate passed<span class="gt gt-attention" style="margin: 0"><i>G</i></span>waiting<span class="gt gt-blocked" style="margin: 0"><i>G</i></span>blocked</div>')
CHANGES = sif('p_changes', '<div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap">' + sfor('pfFilters', 'f', '<button type="button" class="chip {{f.cls}}" aria-pressed="{{f.on}}" onClick="{{f.pick}}">{{f.label}}</button>', 5) + '<span class="vsep" aria-hidden="true"></span>' + sfor('chFilters', 'f', '<button type="button" class="chip {{f.cls}}" aria-pressed="{{f.on}}" onClick="{{f.pick}}">{{f.label}}</button>', 3) + '</div>' + TLEGEND
  + sfor('changeGroups', 'g', '<div class="tgrp"><div class="tg-h">{{g.pf}}<span style="margin-left: auto">{{g.count}}</span></div>'
    + sfor('g.rows', 'c', '<button type="button" class="trow {{c.rowCls}}" onClick="{{c.openChange}}"><span class="t1"><b>{{c.title}}</b>' + sif('c.hasOg', '<span class="orow">' + OG('c.og') + '<span><b>{{c.og.name}}</b> · {{c.og.ref}}</span></span>') + '</span>' + MINITRACK
      + '<span class="t3"><span><span class="tg">TOGAF {{c.togaf}}</span> <b>{{c.phaseNow}}</b></span><span>{{c.now}}</span><span>{{c.docShort}}' + sif('c.hasDlLine', ' · {{c.dlLine}}') + '</span></span>'
      '<span class="t4">' + sif('c.hasGchip', chip('c.gchip', 'sm')) + sif('c.isNew', '<span class="st st-info sm"><span class="tile" aria-hidden="true">+</span>New from intake</span>') + '</span></button>', 3) + '</div>', 4)
  + sif('noChanges', '<span class="meta">No change matches these filters.</span>'))
INTAKE = sif('p_intake', '<div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap"><span class="meta" style="flex: 1 1 320px">What arrives is qualified here: it becomes a change at the right phase, joins an existing change, or is dismissed.</span><button type="button" class="btn f" onClick="{{intakeNew}}">New request · ask the assistant</button></div>'
  '<div class="tgrp"><div class="tg-h">To qualify<span style="margin-left: auto">{{intakeCount}}</span></div>'
  + sfor('intakeOpen', 'g', '<div class="sigrow">' + OG('g') + '<span class="s1"><b>{{g.title}}</b><span class="meta"><b style="color: #1C1B1E">{{g.oName}}</b> · {{g.ref}} · {{g.by}} · {{g.at}}</span><span style="font-size: 13px; line-height: 18px">{{g.text}}</span>'
    '<span class="meta">Suggested: {{g.suggestion}}' + sif('g.hasOverlap', ' · {{g.overlap}}') + '</span></span>'
    '<span class="s2"><button type="button" class="btn f sm" onClick="{{g.qualify}}">Qualify in the assistant</button><button type="button" class="btn o sm" onClick="{{g.create}}">Open as suggested</button>' + sif('g.hasAttach', '<button type="button" class="btn o sm" onClick="{{g.attach}}">{{g.attachLabel}}</button>') + '<button type="button" class="btn t sm" onClick="{{g.dismiss}}">Dismiss</button></span></div>', 6)
  + sif('noIntakeOpen', '<div class="sigrow"><span class="meta">Nothing to qualify.</span></div>') + '</div>'
  '<div class="tgrp"><div class="tg-h">Qualified</div>' + sfor('intakeHist', 'r', '<div class="sigrow">' + OG('r') + '<span class="s1"><b>{{r.title}}</b><span class="meta"><b style="color: #1C1B1E">{{r.oName}}</b> · {{r.ref}} · {{r.who}}</span></span><span class="s2">' + chip('r.chip', 'sm') + sif('r.hasChange', '<button type="button" class="lnk" onClick="{{r.goChange}}">{{r.change}}</button>') + '</span></div>', 4) + '</div>')
REVIEWS = sif('p_reviews', '<span class="meta">Every ARB submission with its readiness. Readiness = Blocked (a blocking check fails or a required section is missing), Needs attention (warnings, a pending reviewer, a change request, an open condition) or Ready for the board.</span><div class="tb"><table><thead><tr><th class="th">Submission</th><th class="th">Portfolio · scope</th><th class="th">Status</th><th class="th">Readiness</th><th class="th">Board</th><th class="th">Reviewers</th><th class="th">ASD</th><th class="th">Conditions</th></tr></thead><tbody>'
  + sfor('arbRows', 'a', '<tr class="rowb" onClick="{{a.go}}"><td class="td"><span class="tt"><span class="ttx"><b>{{a.title}}</b><span>{{a.board}} · <span class="mono" style="font-weight: 400">{{a.id}}</span> · {{a.owner}}</span></span></span></td><td class="td">{{a.pf}}<br><span class="meta">{{a.scope}}</span></td><td class="td">' + chip('a.status', 'sm') + '</td><td class="td">' + chip('a.ready', 'sm') + '</td><td class="td">{{a.date}}</td><td class="td">{{a.reviewers}} approved · {{a.pending}} pending</td><td class="td">{{a.cov}} covered</td><td class="td">{{a.cond}} open</td></tr>', 4) + '</tbody></table></div>')
DECISIONS = sif('p_decisions', '<span class="meta">Architecture decision records (MADR). Immutable once accepted; each names its domain decision.</span><div class="tb"><table><thead><tr><th class="th">Decision</th><th class="th">Portfolio</th><th class="th">Ref</th><th class="th">Affects</th><th class="th">Status</th><th class="th">Updated</th></tr></thead><tbody>'
  + sfor('adrRows', 'a', '<tr class="rowb" onClick="{{a.go}}"><td class="td"><span class="tt">' + tile("'other'", "'decision'") + '<span class="ttx"><b>{{a.title}}</b><span style="font-weight: 400; white-space: normal">{{a.decision}}</span></span></span></td><td class="td">{{a.pf}}</td><td class="td mono">{{a.ref}}</td><td class="td">{{a.affects}}</td><td class="td">' + chip('a.status', 'sm') + '</td><td class="td">{{a.updated}}</td></tr>', 4) + '</tbody></table></div>')
CHECKS_LIST = lambda lst: sfor(lst, 'g', '<div class="cardx"><span class="lbl">{{g.label}}</span><div class="rows">' + sfor('g.checks', 'c', '<div class="row" style="cursor: default; align-items: flex-start"><span class="mono" style="min-width: 28px">{{c.id}}</span><span class="txt"><b>{{c.title}}</b><span>{{c.sev}} {{c.n}}</span>' + sif('c.hasItems', '<span class="rows" style="margin-top: 4px">' + sfor('c.items', 'i', '<button type="button" class="row" style="padding: 2px 0; border: 0" onClick="{{i.go}}"><span class="txt"><b style="font-weight: 500">{{i.title}}</b><span>{{i.msg}}</span></span>' + I_CHEV + '</button>', 2) + '</span>') + '</span>' + chip('c.chip', 'sm') + '</div>', 4) + '</div></div>', 6)
CHECKS = sif('p_checks', '<span class="meta">{{checkSummary}}</span><div class="cards">' + CHECKS_LIST('checkGroups') + '</div>')
HOWTAB = sif('p_how', '<div class="tabs" role="tablist" aria-label="How it works">' + sfor('howTabs', 't', '<button type="button" role="tab" class="tab {{t.cls}}" aria-selected="{{t.on}}" onClick="{{t.pick}}">{{t.label}}</button>', 5) + '</div>'
  + sif('how_steps', '<p class="body" style="margin: 0; max-width: 90ch">{{howIntro}}</p>'
      '<span class="lbl">Ideal flow · pick a phase</span><div class="flow">' + sfor('howPhases', 'p', '<button type="button" class="ph {{p.cls}}" aria-pressed="{{p.on}}" onClick="{{p.pick}}"><span class="pn">{{p.n}}</span><b>{{p.title}}</b><span>{{p.sub}}</span></button>' + sif('p.hasGate', '<span class="gt lg gt-todo" title="{{p.gate}} · {{p.gateTitle}}"><i>{{p.gate}}</i></span>') + sif('p.noGate', '<span class="nx"></span>'), 6) + '<div class="ph ph-todo"><b>Delivery</b><span>plateau → new baseline</span></div></div>'
      '<div class="cards"><div class="cardx"><span class="lbl">{{howPhase.n}} · {{howPhase.title}} · {{howPhase.togaf}}</span><span class="lbl">Deliverable</span><p class="body" style="margin: 0">{{howPhase.deliverable}}</p><span class="lbl">Who</span><p class="body" style="margin: 0">{{howPhase.who}}</p></div>'
      '<div class="cardx"><span class="lbl">In the toolbox</span><dl class="kv kv-stack">' + sfor('howPhase.toolbox', 't', '<dt style="font-family: Manrope, sans-serif; font-weight: 600; color: #1C1B1E">{{t.0}}</dt><dd>{{t.1}}</dd>', 3) + '</dl><span class="lbl">In Git</span><ul style="margin: 0; padding-left: 18px; font-size: 13px; line-height: 19px">' + sfor('howPhase.git', 'g', '<li>{{g}}</li>', 2) + '</ul></div>'
      + sif('howPhase.hasGate', '<div class="gatecard"><span class="lbl" style="display: flex; align-items: center; gap: 8px"><span class="gt gt-passed" style="margin: 0"><i>{{howPhase.gate.id}}</i></span>Gate · {{howPhase.gate.title}}</span><ul style="margin: 0; padding-left: 18px; font-size: 13px; line-height: 19px">' + sfor('howPhase.gate.criteria', 'c', '<li>{{c}}</li>', 3) + '</ul><span class="meta">Decided by {{howPhase.gate.by}} · a human decides (A), agents draft and check (R)</span></div>')
      + sif('howPhase.noGate', '<div class="cardx"><span class="lbl">No gate after this phase</span><p class="body" style="margin: 0">The next gate is on the following phase; this one is where a mid-chain change enters.</p></div>') + '</div>'
      '<span class="lbl">Where a change enters</span><div class="tb"><table><thead><tr><th class="th">Change</th><th class="th">Enters at</th><th class="th">What it means</th></tr></thead><tbody>' + sfor('howEntries', 'e', '<tr><td class="td"><b style="font-family: Manrope, sans-serif">{{e.name}}</b></td><td class="td">{{e.enters}}</td><td class="td" style="white-space: normal">{{e.what}}</td></tr>', 6) + '</tbody></table></div>'
      '<div class="cards">' + sfor('howSides', 'x', '<div class="cardx"><span class="lbl">Side case · {{x.name}}</span><p class="body" style="margin: 0">{{x.text}}</p></div>', 2) + '<div class="cardx"><span class="lbl">{{howAfter.title}}</span><p class="body" style="margin: 0">{{howAfter.text}}</p></div></div>'
      '<span class="lbl">Who acts in each phase</span><div style="overflow: auto"><div class="lanes" style="grid-template-columns: 150px repeat(6, minmax(0, 1fr)); min-width: 900px"><div class="lh">Lane</div><div class="lh">0 · Vision<small>need, scope</small></div><div class="lh">1 · Baseline<small>current state · ADD</small></div><div class="lh">2 · Target<small>ABB, SBB · ADD</small></div><div class="lh">3 · Gap analysis<small>baseline vs target</small></div><div class="lh">4 · Plateau<small>roadmap, WP, DD</small></div><div class="lh">5 · Implementation<small>code, PR, DoR · quality gate</small></div>'
      + sfor('howLanes', 'l', '<div class="lw">{{l.who}}<small>{{l.sub}}</small></div>' + sfor('l.cells', 'c', '<div>{{c}}</div>', 6), 5) + '</div></div>'
      '<span class="lbl">Outcomes of a gate decision</span><div class="cards">' + sfor('howOutcomes', 'o', '<div class="cardx"><span class="st st-{{o.k}}"><span class="tile">{{o.g}}</span>{{o.name}}</span><p class="body" style="margin: 0">{{o.what}}</p></div>', 3) + '</div>')
  + sif('how_documents', '<p class="body" style="margin: 0; max-width: 90ch">Every phase produces or updates a named document. A document is drafted in the chat (the agent proposes, the person inserts), consolidated in a working document on the page, validated by a person, submitted as one pull request per document and per change, and reviewed at the gate. Agents never write a document or merge anything on their own.</p>'
      '<span class="lbl">States of a document</span><div class="cards">' + sfor('howDocStates', 'x', '<div class="cardx"><h3 class="h3">{{x.t}}</h3><p class="body" style="margin: 0">{{x.d}}</p></div>', 6) + '</div>'
      '<span class="lbl">Phase × document × role</span><div class="tb"><table><thead><tr><th class="th">Document</th><th class="th">Phase</th><th class="th">Gate</th><th class="th">Source</th><th class="th">Dialogues with the agent</th><th class="th">Validates and submits</th><th class="th">Reviews at the gate</th></tr></thead><tbody>' + sfor('howDocRows', 'r', '<tr><td class="td"><b style="font-family: Manrope, sans-serif; font-weight: 600">{{r.title}}</b><div class="meta">{{r.sections}}</div></td><td class="td">{{r.phase}}</td><td class="td"><span class="gt gt-passed" style="margin: 0"><i>{{r.gate}}</i></span></td><td class="td">{{r.src}}</td><td class="td">{{r.dialog}}</td><td class="td">{{r.validates}}</td><td class="td">{{r.reviews}}</td></tr>', 12) + '</tbody></table></div>'
      '<span class="lbl">Parallel changes and documents</span><div class="cards"><div class="cardx"><h3 class="h3">Same document</h3><p class="body" style="margin: 0">Two changes hold a working document for the same DD layer or portfolio ASD. Seen when the document opens and at every gate. Answers: Sequence, Merge, Split.</p></div><div class="cardx"><h3 class="h3">Same element</h3><p class="body" style="margin: 0">Two changes touch the same SBB or contract. Seen at Validate, on the preview build of the pull request. The gate does not pass until decided.</p></div><div class="cardx"><h3 class="h3">Base moved</h3><p class="body" style="margin: 0">The other change merged while this one was drafted. Rebase by section: a three-way merge, the person chooses where they diverge; the document goes back to Working.</p></div></div>'
      '<span class="lbl">Knowledge base</span><p class="body" style="margin: 0; max-width: 90ch">Published elements and documents are nodes keyed by their Git reference (repository, path, sha). A working document is its own node, with a supersedes edge to the published one, until its pull request merges. The assistant answers from what is published first and says when a change in progress proposes something else; it never presents a draft as current.</p>')
  + sif('how_classes', '<p class="body" style="margin: 0; max-width: 80ch">TOGAF Phase H classifies each change request. In the toolbox the owner picks the class in step 1; it decides who approves and how much of the ASD is needed.</p><div class="tb"><table><thead><tr><th class="th">Class</th><th class="th">Examples</th><th class="th">Steps</th><th class="th">Who approves</th><th class="th">ASD</th></tr></thead><tbody>' + sfor('howClasses', 'c', '<tr><td class="td"><b style="font-family: Manrope, sans-serif">{{c.name}}</b></td><td class="td">{{c.ex}}</td><td class="td">{{c.steps}}</td><td class="td">{{c.who}}</td><td class="td">{{c.asd}}</td></tr>', 3) + '</tbody></table></div>')
  + sif('how_roles', '<p class="body" style="margin: 0; max-width: 80ch">Decisions are Checkpoints (INV-12): a person records them, never an agent. Automated writes to Git go through CTX-INT (INV-07). The "view as" chips above the prototype switch between these roles on the review page.</p><div class="tb"><table><thead><tr><th class="th">Role</th><th class="th">Can</th><th class="th">Cannot</th></tr></thead><tbody>' + sfor('howRoles', 'r', '<tr><td class="td"><b style="font-family: Manrope, sans-serif">{{r.role}}</b></td><td class="td" style="white-space: normal">{{r.can}}</td><td class="td" style="white-space: normal">{{r.cannot}}</td></tr>', 8) + '</tbody></table></div>')
  + sif('how_parallel', '<p class="body" style="margin: 0; max-width: 80ch">Several changes can be open on the same application at once. They can collide at three levels; each level has its own guard, and most of the work is preventing collisions rather than resolving them.</p><div class="tb"><table><thead><tr><th class="th">Level</th><th class="th">Example</th><th class="th">Caught by</th><th class="th">When</th></tr></thead><tbody>' + sfor('howParallel', 'p', '<tr><td class="td"><b style="font-family: Manrope, sans-serif">{{p.level}}</b></td><td class="td">{{p.ex}}</td><td class="td">{{p.by}}</td><td class="td">{{p.when}}</td></tr>', 3) + '</tbody></table></div>'
      '<span class="lbl">When a change is opened, its scope is compared with every open change; the owner picks one of three answers</span><div class="cards">' + sfor('howAnswers', 'a', '<div class="cardx"><h3 class="h3">{{a.name}}</h3><p class="body" style="margin: 0">{{a.what}}</p><span class="meta">{{a.rec}}</span></div>', 3) + '</div>'
      '<span class="lbl">Checks that guard parallel changes</span><div class="tb"><table><thead><tr><th class="th">Check</th><th class="th">Rule</th><th class="th">Effect</th></tr></thead><tbody>' + sfor('howGuards', 'g', '<tr><td class="td mono">{{g.id}}</td><td class="td">{{g.rule}}</td><td class="td">{{g.effect}}</td></tr>', 6) + '</tbody></table></div>')
  + sif('how_agents', '<p class="body" style="margin: 0; max-width: 90ch">Agents read the knowledge base through one MCP server, whether they run in Sweep or in a coding assistant on a developer\'s machine. They read; they never write. Their only way back into the knowledge base is a commit or a pull request.</p>'
      '<div class="cards"><div class="cardx"><span class="lbl">Server</span><code class="mono" style="font-size: 13px">{{howMcp}}</code><span class="lbl">Connect</span><dl class="kv kv-stack">' + sfor('howMcpClients', 'c', '<dt style="font-family: Manrope, sans-serif; font-weight: 600; color: #1C1B1E">{{c.name}}</dt><dd class="mono" style="font-size: 12px; white-space: normal; overflow-wrap: anywhere">{{c.how}}</dd>', 3) + '</dl></div>'
      '<div class="cardx"><span class="lbl">Tools · read only</span><div class="tb" tabindex="0" role="region" aria-label="Tools of the knowledge-base MCP server"><table><thead><tr><th class="th">Tool</th><th class="th">Takes</th><th class="th">Returns</th></tr></thead><tbody>' + sfor('howMcpTools', 't', '<tr><td class="td mono" style="font-size: 12px">{{t.name}}</td><td class="td">{{t.arg}}</td><td class="td" style="white-space: normal">{{t.what}}</td></tr>', 5) + '</tbody></table></div></div></div>')
  + sif('how_git', '<p class="body" style="margin: 0; max-width: 80ch">main holds the approved architecture: the baseline and every approved plateau. A change lives on its branch until the board decides; the board decides on one pinned commit; the decision itself is a commit.</p><div class="tb"><table><thead><tr><th class="th">Rule</th><th class="th">Convention</th><th class="th">Why</th></tr></thead><tbody>' + sfor('howGit', 'g', '<tr><td class="td"><b style="font-family: Manrope, sans-serif">{{g.rule}}</b></td><td class="td mono" style="font-size: 12px">{{g.conv}}</td><td class="td" style="white-space: normal">{{g.why}}</td></tr>', 13) + '</tbody></table></div>'))
PROPOSALS = sif('p_proposals', '<span class="meta">{{propSummary}}</span><div class="cards">' + sfor('proposals', 'p', '<div class="cardx prop"><div class="row" style="cursor: default; align-items: flex-start; gap: 10px"><span class="pk {{p.kindCls}}">{{p.kind}}</span><span class="txt" style="flex: 1"><b>{{p.title}}</b><span>' + sif('p.hasApp', '<button type="button" class="lnk" onClick="{{p.goApp}}">{{p.app}}</button> · ') + sif('p.hasChange', '<button type="button" class="lnk" onClick="{{p.goChange}}">{{p.change}}</button> · ') + '{{p.opened}} · {{p.pr}}</span></span>' + chip('p.chip', 'sm') + '</div><p class="body" style="margin: 0">{{p.detail}}</p><div class="row" style="cursor: default; gap: 8px; align-items: center"><span class="meta" style="flex: 1">Decides: {{p.who}}</span>' + sif('p.isOpen', '<button type="button" class="chip" onClick="{{p.reject}}">Reject with a reason</button><button type="button" class="chip chip-on" onClick="{{p.accept}}">Accept</button>') + '</div></div>', 6) + '</div>')
PROC_BLOCKS = INTAKE + CHANGES + REVIEWS + DECISIONS + CHECKS + HOWTAB
PROC_AREA = sif('isProc', '<div class="area">' + SIDE_PROC + '<div class="content">' + PROC_BLOCKS + '</div></div>')

# ----------------------------------------------------------------------------------------------- ARB page
LAND_ROWS = lambda lst: '<div class="tb"><table><thead><tr><th class="th">Capability</th><th class="th">Applications</th></tr></thead><tbody>' + sfor(lst, 'r', '<tr><td class="td" style="width: 220px"><b style="font-family: Manrope, sans-serif">{{r.cap}}</b></td><td class="td"><span style="display: flex; gap: 8px; flex-wrap: wrap">' + sfor('r.apps', 'a', '<button type="button" class="chip" onClick="{{a.go}}">{{a.title}} ' + chg('a.change') + '</button>', 2) + '</span></td></tr>', 6) + '</tbody></table></div>'
ASD_SECTIONS = sfor('arb.sections', 's',
  '<section class="asec" id="asd-{{s.i}}"><div class="asec-h"><span class="num">{{s.i}}</span><h3 class="h3">{{s.title}}</h3><span class="src {{s.srcCls}}">{{s.src}}</span>' + chip('s.chip', 'sm') + '<span class="meta">{{s.note}}</span></div>'
  + sif('s.isWritten', sif('s.hasHtml', '<div class="prose htmlbox" style="white-space: normal">{{s.text}}</div>') + sif('s.isMissingWritten', '<div class="banner">This section is missing in the submission file. The owner writes it before the board; the readiness gate counts it as Blocked when the class requires the full ASD.</div>'))
  + sif('s.isReq', '<div class="tb"><table><thead><tr><th class="th">Requirement</th><th class="th">Acceptance</th><th class="th">Decision table</th><th class="th">Operational</th><th class="th">Realized by</th></tr></thead><tbody>' + sfor('arb.reqs', 'r', '<tr><td class="td"><button type="button" class="rowbtn" onClick="{{r.go}}">' + tile("'motivation'", "'requirement'") + '<span class="tt"><span class="ttx"><b>{{r.title}}</b><span style="font-weight: 400; white-space: normal">{{r.desc}}</span></span></span></button></td><td class="td">{{r.acc}}</td><td class="td">{{r.ko}}</td><td class="td mono" style="font-size: 12px">{{r.ops}}</td><td class="td">' + sfor('r.realizers', 'z', '<button type="button" class="lnk" style="display: block" onClick="{{z.go}}">{{z.title}}</button>', 2) + '</td></tr>', 1) + '</tbody></table></div>')
  + sif('s.isBase', '<span class="meta">{{arb.baseTitle}} · the portfolio landscape at the from plateau, generated from the model.</span>' + LAND_ROWS('arb.baseRows'))
  + sif('s.isTarget', '<span class="meta">{{arb.targetTitle}} · the portfolio landscape at the to plateau, generated from the model.</span>' + LAND_ROWS('arb.targetRows'))
  + sif('s.isGap', '<div class="tb"><table><thead><tr><th class="th">Building block</th><th class="th">Change</th><th class="th">Level</th><th class="th">Plateaus</th><th class="th">Addressed by</th><th class="th">Design</th></tr></thead><tbody>' + sfor('arb.scope', 'x', '<tr><td class="td"><button type="button" class="rowbtn" onClick="{{x.go}}">' + tile('x.layer', 'x.k') + '<span class="tt"><span class="ttx"><b>{{x.title}}</b><span>{{x.kind}}</span></span></span></button></td><td class="td">' + chg('x.change') + '</td><td class="td">{{x.level}}</td><td class="td">' + track('x.track') + '</td><td class="td">{{x.by}}</td><td class="td">' + chip('x.dd', 'sm') + '</td></tr>', 8) + '</tbody></table></div>')
  + sif('s.isDd', '<div class="cards">' + sfor('arb.dds', 'd', '<div class="cardx"><button type="button" class="lnk" style="text-decoration: none; font: 600 14px Manrope, sans-serif" onClick="{{d.go}}">{{d.title}}</button>' + sif('d.hasDdFiles', '<div class="rows">' + sfor('d.dd', 'f', '<button type="button" class="row" onClick="{{f.go}}">' + tile("'other'", "'domain'") + '<span class="txt"><b>{{f.title}}</b><span class="mono">{{f.contract}}</span></span>' + chip('f.status', 'sm') + '</button>', 2) + '</div>') + sif('d.noDd', '<span class="st st-warning sm"><span class="tile">!</span>No detailed design yet (T6)</span>') + sfor('d.iface', 'i', '<span class="meta"><span class="ok-dot" style="{{i.dotStyle}}"></span>{{i.title}} · <span class="mono">{{i.contract}}</span></span>', 1) + '</div>', 3) + '</div><p class="meta" style="margin: 0">Tier 1 only (design intent). Contracts (OpenAPI, AsyncAPI) and the extracted code structure are linked from each DD, never restated (DEC-KB-05).</p>')
  + sif('s.isDec', '<div class="rows">' + sfor('arb.adrs', 'a', '<button type="button" class="row" onClick="{{a.go}}">' + tile("'other'", "'decision'") + '<span class="txt"><b>{{a.title}}</b><span>{{a.decision}}</span></span>' + I_CHEV + '</button>', 1) + '</div>')
  + sif('s.isOpen', sif('arb.hasAsks', '<span class="lbl">Asked of the board</span><div class="rows">' + sfor('arb.asks', 'a', '<div class="row" style="cursor: default"><span class="mono" style="min-width: 24px">{{a.id}}</span><span class="txt"><b style="font-weight: 500">{{a.text}}</b></span>' + chip('a.status', 'sm') + '</div>', 3) + '</div>'))
  + '</section>', 13)
ARB_ASD = sif('arb.tAsd', '<div class="asd"><div class="toc"><span class="lbl" style="padding: 0 8px 6px">Architecture solution design · 13 items</span>' + sfor('arb.toc', 't', '<a href="#asd-{{t.i}}" class="toc {{t.cls}}" style="text-decoration: none; display: grid; grid-template-columns: 20px minmax(0, 1fr) auto; gap: 8px; align-items: center; padding: 6px 8px; border-radius: 8px; color: #1C1B1E; font-size: 13px; position: static"><span class="n">{{t.i}}</span><span>{{t.title}}</span><span class="dot dot-{{t.st}}" title="{{t.chip.w}}"></span></a>', 13) + '<button type="button" class="btn t" style="margin-top: 12px; justify-content: center" onClick="{{arb.asdMd}}">' + I_COPY + ' Copy ASD as Markdown</button><span class="meta" style="padding: 8px">Six sections are written in the submission file; seven are assembled from the model (DEC-KB-12).</span></div><div>' + ASD_SECTIONS + '</div></div>')
ARB_CHECKS = sif('arb.tChecks', '<span class="meta">Checks run on the scope of the submission: the gap between the two plateaus, its detailed design and requirements. Blocking checks make approval unavailable; warnings go to the board.</span><div class="cards">' + CHECKS_LIST('arb.checkGroups') + '</div>')
ARB_REVIEW = sif('arb.tReview', '<span class="lbl">Reviewers by role</span><div class="rev">' + sfor('arb.reviewers', 'r', '<div class="cardx {{r.meCls}}"><div class="who"><span class="av">{{r.av}}</span><span><b>{{r.name}}</b><span>{{r.role}}</span></span></div><div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap">' + chip('r.decision') + '<span class="meta">{{r.at}}</span></div>' + sif('r.hasNote', '<div class="note">{{r.note}}</div>') + sif('r.isMe', '<span class="meta">This is you in the "Reviewer" view: record or change your decision on the Decision tab.</span>') + '</div>', 4) + '</div>'
  '<span class="lbl">Conditions · the Architecture Contract once approved</span>' + sif('arb.hasConditions', '<div class="tb"><table><thead><tr><th class="th">Id</th><th class="th">Condition</th><th class="th">Owner</th><th class="th">Due</th><th class="th">Status</th></tr></thead><tbody>' + sfor('arb.conditions', 'c', '<tr><td class="td mono">{{c.id}}</td><td class="td" style="white-space: normal">{{c.text}}</td><td class="td mono">{{c.owner}}</td><td class="td">{{c.due}}</td><td class="td">' + chip('c.status', 'sm') + '</td></tr>', 2) + '</tbody></table></div>') + sif('arb.noConditions', '<p class="meta" style="margin: 0">No conditions yet. A reviewer who approves with conditions adds them here with an owner and a due date.</p>')
  + sif('arb.hasAsks', '<span class="lbl">Asked of the board · decisions only the board can take</span><div class="rows">' + sfor('arb.asks', 'a', '<div class="row" style="cursor: default"><span class="mono" style="min-width: 24px">{{a.id}}</span><span class="txt"><b style="font-weight: 500">{{a.text}}</b></span>' + chip('a.status', 'sm') + '</div>', 3) + '</div>'))
ARB_DECISION = sif('arb.tDecision', '<div class="cards"><div class="dec" style="grid-column: 1 / -1">'
  + sif('arb.recorded', '<div class="banner" style="background: #ACF4A2; color: #1B5F1F"><b>Recorded in this session</b>' + chip('arb.record.decision', 'sm') + '<span>by {{arb.record.by}} on {{arb.record.at}} · {{arb.record.note}}</span></div>')
  + sif('arb.canSubmit', '<h3 class="h3">You own this change</h3><p class="body" style="margin: 0">Submitting runs the readiness gate, generates the ASD and freezes it at the current commit. Reviewers then record their decisions; you cannot approve your own change. After a request for changes, fix the model on the branch and re-submit.</p><div class="acts"><button type="button" class="btn f" onClick="{{arb.submit}}">' + ('{{arb.submitLabel}}') + '</button><button type="button" class="btn t" onClick="{{arb.asdMd}}">Export the ASD</button></div><span class="meta">Readiness now: </span>' + chip('arb.ready', 'sm') + '<span class="meta">{{arb.boardWhy}}</span>')
  + sif('arb.canReview', '<h3 class="h3">Your decision as Security architect</h3><div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap"><span class="meta">Current:</span>' + chip('arb.myDecision') + '<span class="meta">{{arb.myNote}}</span></div><div class="fld"><label for="dec-note">Note for the record</label><textarea id="dec-note" rows="2" placeholder="What you checked, what must change" value="{{arb.note}}" onChange="{{arb.onNote}}"></textarea></div><div class="acts"><button type="button" class="btn f" onClick="{{arb.approve}}">Approve</button><button type="button" class="btn t" onClick="{{arb.approveCond}}">Approve with conditions</button><button type="button" class="btn w" onClick="{{arb.requestChanges}}">Request changes</button><button type="button" class="btn o" onClick="{{arb.notRequired}}">Not required</button></div><span class="meta">Your decision is a Checkpoint (CMD-DECIDE-CHECKPOINT). A request for changes puts the review in Needs attention and sends the change back to Design.</span>')
  + sif('arb.canBoard', '<h3 class="h3">Board decision · {{arb.board}} · {{arb.date}}</h3><p class="body" style="margin: 0">{{arb.boardWhy}}</p><div class="fld"><label for="dec-note2">Decision note</label><textarea id="dec-note2" rows="2" placeholder="Conditions, order constraints, what the board asks" value="{{arb.note}}" onChange="{{arb.onNote}}"></textarea></div><div class="acts"><button type="button" class="btn f" aria-disabled="{{arb.boardDisabled}}" onClick="{{arb.boardApprove}}">Approve</button><button type="button" class="btn t" aria-disabled="{{arb.boardDisabled}}" onClick="{{arb.boardApproveCond}}">Approve with conditions</button><button type="button" class="btn w" onClick="{{arb.requestChanges}}">Request changes</button><button type="button" class="btn d" aria-disabled="{{arb.boardDisabled}}" onClick="{{arb.boardReject}}">Reject</button></div><span class="meta">When the Checkpoint is decided, atb-arch-bot commits the ARB record (status, decision, conditions, decidedAt, reviewedSha); arb-decision turns green; the owner merges with a merge commit through the merge queue.</span>')
  + sif('arb.isReader', '<h3 class="h3">Read only</h3><p class="body" style="margin: 0">Decisions are recorded by the reviewers and the board chair as Checkpoints; agents never decide. Switch the prototype to Reviewer or Board chair to see their actions.</p>')
  + '</div><div class="cardx"><span class="lbl">Git trail</span><dl class="kv">' + sfor('arb.git', 'g', '<dt>{{g.k}}</dt><dd class="mono" style="font-size: 12px">{{g.v}}</dd>', 5) + '</dl></div><div class="cardx"><span class="lbl">Outcomes</span><div class="rows"><div class="row" style="cursor: default"><span class="st st-success sm"><span class="tile">✓</span>Approve</span><span class="txt"><span>merge; conditions move to Deliver</span></span></div><div class="row" style="cursor: default"><span class="st st-warning sm"><span class="tile">!</span>Request changes</span><span class="txt"><span>back to Design, re-submit, the ASD is frozen again</span></span></div><div class="row" style="cursor: default"><span class="st st-error sm"><span class="tile">✕</span>Reject</span><span class="txt"><span>PR closed; only the ARB record reaches main</span></span></div></div></div></div>')
ARBPAGE = sif('isArbPage',
  S.subheader('{{backHome}}', '{{arb.backLabel}}', '{{arb.title}}', '{{arb.board}} · {{arb.pf}} · {{arb.from}} → {{arb.to}} · submitted by {{arb.submittedBy}} on {{arb.submittedAt}} · <span class="mono">{{arb.wi}}</span>', chip('arb.status') + chip('arb.ready'), lead=tile("'implementation'", "'work-package'", True))
  + sif('arb.updatedSince', '<div class="banner"><b>Updated since review</b><span>The branch {{arb.branch}} moved after the reviewed commit {{arb.sha}} (last change {{arb.updatedAt}}). The chair chooses a review of the delta only, or a full review.</span></div>')
  + '<div class="kpis"><div class="kpi"><span class="lbl">Checks on the scope</span><b>{{arb.kpi.checks}}</b><span>{{arb.kpi.checksNote}}</span></div><div class="kpi"><span class="lbl">ASD sections written</span><b>{{arb.kpi.written}}</b><span>{{arb.kpi.writtenNote}}</span></div><div class="kpi"><span class="lbl">Coverage</span><b>{{arb.kpi.cov}}</b><span>{{arb.kpi.covNote}}</span></div><div class="kpi"><span class="lbl">Reviewer decisions</span><b>{{arb.kpi.rev}}</b><span>{{arb.kpi.revNote}}</span></div><div class="kpi"><span class="lbl">Open conditions</span><b>{{arb.kpi.cond}}</b><span>{{arb.kpi.condNote}}</span></div></div>'
  + '<div class="tabs" role="tablist" aria-label="Review">' + sfor('arb.tabs', 't', '<button type="button" role="tab" class="tab {{t.cls}}" aria-selected="{{t.on}}" onClick="{{t.pick}}">{{t.label}}<span class="n">{{t.n}}</span></button>', 4) + '</div>'
  + ARB_ASD + ARB_CHECKS + ARB_REVIEW + ARB_DECISION)

# ----------------------------------------------------------------------------------------------- assembly
TOAST = sif('hasToast', '<div class="toast" role="status"><span>{{toast}}</span><button type="button" aria-label="Dismiss" onClick="{{closeToast}}">✕</button></div>')
CHANGEPAGE = sif('isChangePage',
  S.subheader('{{ch.back}}', '{{ch.backLabel}}', '{{ch.title}}', '<span class="mono">{{ch.wi}}</span> · {{ch.pf}} · {{ch.owner}} · {{ch.entry}}', after=chip('ch.status'), lead=tile("'implementation'", "'work-package'", True), actions=sif('ch.hasArb', '<button type="button" class="chip" onClick="{{ch.arb.go}}">Open the review</button>'))
  + '<div class="flow">' + sfor('ch.flow', 'f', '<div class="ph {{f.cls}}" title="{{f.title}} · {{f.state}}"><span class="pn">{{f.n}}</span><b>{{f.title}}</b><span>{{f.sub}}</span>' + sif('f.entered', '<span class="ent">enters here</span>') + '</div>' + sif('f.hasGate', '<span class="gt {{f.gateCls}}" title="{{f.gateTitle}}"><i>{{f.gate}}</i></span>') + sif('f.noGate', '<span class="nx"></span>'), 6) + '<div class="ph {{ch.deliveredCls}}"><b>Delivery</b><span>plateau → new baseline</span></div></div>'
  + sif('ch.hasOg', '<span class="orow">' + OG('ch.og') + '<span>Comes from <b>{{ch.og.name}}</b> · {{ch.og.ref}} · {{ch.og.by}} · {{ch.og.at}}</span></span>')
  + '<div class="nextline"><span class="gt gt-pending" style="margin: 0"><i>{{ch.next}}</i></span><b>{{ch.nextTitle}}</b>' + sif('ch.noNextMissing', '<span>· every document is ready · the gate can be scheduled</span>') + sif('ch.hasNextMissing', '<span>· still missing: ' + sfor('ch.nextMissing', 'd', '<button type="button" class="lnk" onClick="{{d.open}}">{{d.title}}</button> ', 3) + '</span>') + '</div>'
  + sif('ch.hasCols', sfor('ch.cols', 'c', '<div class="colline {{c.levelCls}}"><span class="pk">{{c.level}}</span><span style="flex: 1; min-width: 200px">{{c.detail}} · with <button type="button" class="lnk" onClick="{{c.goOther}}">{{c.other}}</button>' + sif('c.decided', ' · <b>{{c.answer}}</b> ({{c.by}})') + '</span>' + sif('c.isElem', sif('c.undecided', '<span class="row" style="gap: 6px; cursor: default"><button type="button" class="chip" onClick="{{c.seq}}">Sequence</button><button type="button" class="chip" onClick="{{c.merge}}">Merge</button><button type="button" class="chip" onClick="{{c.split}}">Split</button></span>')) + sif('c.isBase', sif('c.rebased', '<span class="tile ok"><i></i>Rebased</span>') + sif('c.notRebased', '<button type="button" class="chip chip-on" onClick="{{c.rebase}}">Rebase by section</button>')) + '</div>', 2))
  + sif('ch.dl.first', DELIVERY) + '<div class="doclist">' + sfor('ch.phases', 'p', '<div class="dph {{p.cls}}"><div class="dph-h"><span class="pn">{{p.n}}</span><h3 class="h3">{{p.title}}</h3>' + sif('p.hasGateLabel', '<span class="meta">{{p.gateLabel}}</span>') + '</div>' + sfor('p.docs', 'd', '<button type="button" class="docrow" onClick="{{d.open}}"><span class="dr-t"><b>{{d.title}}</b>' + sif('d.hasSub', '<span class="meta">{{d.sub}}</span>') + '</span>' + chip('d.chip', 'sm') + '<span class="dr-a">{{d.action}}</span></button>', 6) + '</div>', 7) + '</div>' + sif('ch.dl.last', DELIVERY))

DOCPAGE = sif('isDocPage',
  S.subheader('{{doc.goChange}}', 'Back to the change', '{{doc.title}}', '{{doc.change}} · {{doc.repo}} · {{doc.base}}', after=chip('doc.chip'), actions=sif('doc.canValidate', '<button type="button" class="chip" onClick="{{doc.openAssistant}}">Open in the assistant</button><button type="button" class="btn f" onClick="{{doc.validate}}">Validate and submit</button>') + sif('doc.hasPr', '<span class="chip" style="cursor: default">PR #{{doc.pr}}</span>'))
  + '<div class="docstatus"><span class="prog" aria-hidden="true"><i style="width: {{doc.pct}}"></i></span><span class="meta">{{doc.progress}} sections · {{doc.statusLine}}</span></div>'
  + sif('doc.baseMoved', '<div class="colline col-base-moved"><span class="pk">Base moved</span><span style="flex: 1; min-width: 200px">{{doc.baseNote}}</span><button type="button" class="chip chip-on" onClick="{{doc.rebase}}">Rebase by section</button></div>')
  + '<div class="docmain" style="max-width: 920px">' + sfor('doc.sections', 'x', '<section class="sec {{x.cls}}"><div class="sec-h"><span class="pn">{{x.n}}</span><h3 class="h3" style="flex: 1">{{x.title}}</h3>' + sif('x.changed', '<span class="tile wn"><i></i>Changed upstream</span>') + sif('x.hasText', sif('doc.canValidate', '<button type="button" class="lnk" onClick="{{x.edit}}">Edit</button><button type="button" class="lnk" onClick="{{x.draft}}">Rework in the assistant</button>')) + sif('x.isEmpty', '<button type="button" class="lnk" onClick="{{x.draft}}">Draft in the assistant</button>') + '</div>' + sif('x.hasText', '<p class="body" style="margin: 0">{{x.text}}</p>') + sif('x.isEmpty', '<p class="meta" style="margin: 0">Nothing yet.</p>') + '</section>', 13) + '</div>')

BODY = ('<div style="display: flex; flex-direction: column; gap: 12px; padding: 12px; background: #ECE5F4; min-height: 100vh; box-sizing: border-box; font-family: \'Open Sans\', system-ui, sans-serif">'
        + S.sim_bar(ROLE_CHIPS) + S.sim_open('sim-host-arch')
        + '<div class="app" style="min-height: {{simFrameH}}px">' + HEADER + '<div class="bodyrow">' + RAIL + '<main>'
        + sif('noPage', SUBHEADER + AREA_TABS) + VIEWS_AREA + CAT_AREA + PROC_AREA + ELEMENT + ARBPAGE + CHANGEPAGE + DOCPAGE
        + '</main></div>' + NAVBAR + TOAST + '</div>' + S.SIM_CLOSE + '</div>')

logic = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'arch_logic.js'), encoding='utf-8').read()
import change_docs, delivery_data, intake_data
logic = logic.replace('/*DATA*/', json.dumps(D, ensure_ascii=False, separators=(',', ':'))).replace('/*HOW*/', json.dumps(HOW, ensure_ascii=False, separators=(',', ':'))).replace('/*CDOC*/', json.dumps(change_docs.CDOC, ensure_ascii=False, separators=(',', ':'))).replace('/*DELIV*/', json.dumps(delivery_data.DELIV, ensure_ascii=False, separators=(',', ':'))).replace('/*INTAKE*/', json.dumps(intake_data.INTAKE, ensure_ascii=False, separators=(',', ':'))).replace('/*SIM*/', S.SIM_JS)
assert '</script' not in logic and '</script' not in BODY

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Architecture · Meridian Bank · live prototype</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&amp;family=Open+Sans:wght@400;600;700&amp;display=swap">
<style>
{CSS}
</style>
</helmet>
{BODY}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1440,"height":1320}}}}'>
{logic}
</script>
</body>
</html>
'''
def emit(page, out):
    errs = check(page)
    if errs:
        print('\n'.join(errs[:20])); sys.exit(1)
    open(out, 'w', encoding='utf-8').write(page)
    print('wrote', out, len(page), 'bytes', page.count('<sc-if'), 'sc-if', page.count('<sc-for'), 'sc-for')
if __name__ == '__main__':
    emit(page, OUT)
