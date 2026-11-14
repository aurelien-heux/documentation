"""Build DocsLab.dc.html: one Docs with several sources, every one visual and every one queryable by the assistant
through the Knowledge base MCP server.

Sources: the architecture model (TOGAF building blocks in LikeC4, one view per application, with the detailed design
of each module), an AI wiki (tips, procedures and news written by the community), operational procedures
(release, organization, incidents, design system) and the new joiner path. Way in A · Spaces is adopted (30 Oct);
B Application lens and C Ask first stay for the record. The frame takes the height of the screen, so the rail's bottom items stay visible."""
import sys, os, re, json
sys.path.insert(0, os.path.dirname(__file__))
import shell as S, navgen as N, docs_lab_data as D
dst = sys.argv[1]
HERE = os.path.dirname(__file__)
CSS_LAB = re.search(r'CSS_LAB = r"""(.*?)"""', open(os.path.join(HERE, 'admin_lab_build.py'), encoding='utf-8').read(), re.S)[1]
VP = open(os.path.join(HERE, 'vision_parts.py'), encoding='utf-8').read()
AS_CSS = '\n'.join(l for l in re.search(r'CSS = CAT_CSS (?:\+ VD\.CSS )?\+ r"""(.*?)"""', VP, re.S)[1].split('\n') if l.startswith(('.as-', '@container')))

ST = 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
BACK = f'<svg width="18" height="18" viewBox="0 0 24 24" {ST}><path d="M15 6l-6 6 6 6"/></svg>'
CLOSE = f'<svg width="20" height="20" viewBox="0 0 24 24" {ST}><path d="M6 6l12 12M18 6L6 18"/></svg>'
SEND = f'<svg width="18" height="18" viewBox="0 0 24 24" {ST}><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
SPARK = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/></svg>'
CHECK = f'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5L20 7"/></svg>'
EXT = f'<svg width="16" height="16" viewBox="0 0 24 24" {ST}><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>'

CSS_DL = r"""
.stack{display:flex;flex-direction:column;gap:12px;min-width:0}
.lnk{border:0;background:transparent;padding:0;color:#35307E;font-size:13px;font-weight:600;cursor:pointer;text-decoration:underline;text-underline-offset:3px}
.meta{font-size:12px;color:#48454E}
main .meta,.as-pane .meta{white-space:normal;overflow-wrap:anywhere}
.cb{width:18px;height:18px;accent-color:#35307E;margin:0;flex:none}
.seg{display:inline-flex;border:1px solid #79757F;border-radius:16px;overflow:hidden;flex:none}
.seg button{height:36px;padding:0 14px;border:0;border-left:1px solid #79757F;background:transparent;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:13px;font-weight:600;color:#1C1B1E;cursor:pointer}
.seg button:first-child{border-left:0}.seg button[aria-pressed="true"]{background:#E3DFFF;color:#191836}
.vt{display:flex;align-items:center;gap:12px;flex-wrap:wrap;min-height:40px}
.vt h2{margin:0;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:22px;line-height:28px;font-weight:700}
.sub{font-size:14px;line-height:20px;color:#48454E;margin:0}
.askbox{display:flex;align-items:center;gap:8px;min-height:56px;padding:0 8px 0 18px;border-radius:28px;background:#FFFFFF;border:1px solid #79757F;box-sizing:border-box}
.askbox:focus-within{border:2px solid #35307E;padding-left:17px}
.askbox input{flex:1;border:0;outline:0;font:400 15px/22px 'Open Sans',system-ui,sans-serif;background:transparent;min-width:0;color:#1C1B1E}
.askbox .go{width:40px;height:40px;border:0;border-radius:50%;background:#35307E;color:#fff;display:inline-flex;align-items:center;justify-content:center;cursor:pointer;flex:none}
.spaces{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.space{display:grid;grid-template-columns:120px minmax(0,1fr);gap:16px;align-items:center;padding:14px;border-radius:12px;background:#FFFFFF;border:1px solid #E6E0EC;text-align:left;font:inherit;color:inherit;cursor:pointer;min-width:0}
.space:hover{border-color:#CAC4CF;background:#FDF8FD}.space:focus-visible{outline-offset:-3px}
.space b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:16px;display:block}
.space p{margin:4px 0 6px;font-size:13px;line-height:18px;color:#48454E}
.thumb{height:84px;border-radius:10px;background:#F7F2FA;position:relative;overflow:hidden}
.thumb i{position:absolute;display:block;border-radius:3px}
.list{list-style:none;margin:0;padding:0}.list li{display:flex;gap:12px;align-items:baseline;padding:10px 0;border-top:1px solid #ECE5F4;font-size:14px;line-height:20px}.list li:first-child{border-top:0}
.srcT{display:inline-flex;align-items:center;justify-content:center;min-width:34px;height:20px;padding:0 6px;border-radius:6px;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:10px;font-weight:800;letter-spacing:.3px;flex:none;box-sizing:border-box}
.dg-wrap{overflow-x:auto;border:1px solid #E6E0EC;border-radius:12px;background:#FFFFFF}
.dg{position:relative;min-width:640px}
.dg svg{position:absolute;inset:0;width:100%;height:100%;display:block}
.dg-hit{position:absolute;border:0;background:transparent;border-radius:4px;cursor:pointer;padding:0}
.dg-hit:hover{box-shadow:inset 0 0 0 2px #79757F}
.dg-hit[aria-pressed="true"]{box-shadow:0 0 0 3px #35307E}
.arch-split{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:16px;align-items:start}
.panel{border:1px solid #E6E0EC;border-radius:12px;background:#FFFFFF;padding:16px;display:flex;flex-direction:column;gap:10px;min-width:0}
.kv{display:grid;grid-template-columns:92px minmax(0,1fr);gap:6px 10px;font-size:13px;line-height:18px}.kv dt{color:#48454E}.kv dd{margin:0;overflow-wrap:anywhere}
.ddrow{display:flex;align-items:center;gap:10px;width:100%;padding:8px 10px;border:0;border-radius:8px;background:transparent;text-align:left;font:inherit;font-size:13px;color:#1C1B1E;cursor:pointer}.ddrow:hover{background:#F2EBFA}
.chain{display:flex;flex-wrap:wrap;align-items:center;gap:6px}
.ch{display:flex;flex-direction:column;gap:2px;padding:8px 12px;border:1px solid #CAC4CF;border-radius:10px;background:#FFFFFF;min-width:88px}
.ch b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:13px}.ch span{font-size:12px;line-height:16px;color:#48454E}
.ch-arr{color:#79757F;font-size:16px}
.steps{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
.steps li{display:flex;gap:10px;align-items:flex-start;font-size:13px;line-height:18px}
.steps .num{width:22px;height:22px;flex:none;border-radius:50%;background:#E3DFFF;color:#14085E;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:11px;font-weight:700;display:inline-flex;align-items:center;justify-content:center}
.dd-grid{display:grid;grid-template-columns:minmax(0,1fr) 220px;gap:32px;align-items:start}
.dd-sec{display:flex;flex-direction:column;gap:10px;padding:18px 0;border-top:1px solid #ECE5F4}.dd-sec:first-child{border-top:0;padding-top:4px}
.dd-sec h3{margin:0;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:17px;line-height:24px;font-weight:700}
.dd-sec p{margin:0;font-size:14px;line-height:21px}
.dd-ul{margin:0;padding-left:20px;font-size:14px;line-height:21px}
.seq{list-style:none;margin:0;padding:0;border:1px solid #E6E0EC;border-radius:12px;background:#FFFFFF;overflow:hidden}
.seq li{display:grid;grid-template-columns:28px 150px 20px 150px minmax(0,1fr);gap:8px;align-items:center;padding:8px 12px;border-top:1px solid #F2EBFA;font-size:13px}.seq li:first-child{border-top:0}
.who{display:inline-block;padding:2px 8px;border-radius:6px;background:#CFEDFA;color:#0A5570;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%;box-sizing:border-box}
.rows{border:1px solid #E6E0EC;border-radius:12px;background:#FFFFFF;overflow:hidden}
.rows>div{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr) minmax(0,1fr);gap:12px;padding:9px 12px;border-top:1px solid #F2EBFA;font-size:13px;line-height:18px}.rows>div:first-child{border-top:0}.rows .meta,.rows span{white-space:normal;overflow-wrap:anywhere}
.toc{position:sticky;top:0;display:flex;flex-direction:column;gap:2px;font-size:13px}
.toc a{padding:6px 10px;border-left:2px solid #E6E0EC;color:#48454E;text-decoration:none}.toc a:hover{color:#1C1B1E;border-left-color:#79757F}
.flow{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0;align-items:stretch}
.flow>div{position:relative;padding:14px;border:1px solid #CAC4CF;background:#FFFFFF;display:flex;flex-direction:column;gap:6px;font-size:13px;line-height:18px}
.flow>div+div{border-left:0}.flow>div:first-child{border-radius:12px 0 0 12px}.flow>div:last-child{border-radius:0 12px 12px 0}
.flow b{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:14px}
.path{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.guide{display:flex;gap:10px;align-items:center;width:100%;padding:10px 12px;border:1px solid #E6E0EC;border-radius:10px;background:#FFFFFF;text-align:left;font:inherit;font-size:13px;line-height:18px;color:#1C1B1E;cursor:pointer}.guide:hover{border-color:#CAC4CF}
.dot{width:20px;height:20px;border-radius:50%;border:1.5px solid #CAC4CF;flex:none;display:inline-flex;align-items:center;justify-content:center;box-sizing:border-box}
.dot.on{background:#35307E;border-color:#35307E;color:#fff}
.lanes-wrap{overflow-x:auto;border:1px solid #E6E0EC;border-radius:12px;background:#FFFFFF}
.lanes{display:grid;grid-template-columns:132px repeat(5,minmax(120px,1fr));min-width:780px}
.lanes>div{padding:10px;border-top:1px solid #F2EBFA;border-left:1px solid #F2EBFA;min-height:56px;box-sizing:border-box}
.lanes .lh{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:700;color:#48454E;min-height:0;border-top:0}
.lanes .ln{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:13px;font-weight:700;border-left:0}
.stp{display:flex;flex-direction:column;gap:2px;padding:8px 10px;border-radius:8px;background:#F2EBFA;border-left:3px solid #35307E;font-size:12px;line-height:16px}.stp b{font-size:13px;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif}
.stp.gate{background:#FFF2B3;border-left-color:#5E5000}.stp.prod{background:#C3F4DC;border-left-color:#006C46}
.org{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.team{display:flex;flex-direction:column;gap:2px;padding:10px 0;border-top:1px solid #F2EBFA;font-size:13px;line-height:18px}.team:first-of-type{border-top:0}
.tl{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.chk{display:flex;gap:10px;align-items:flex-start;padding:8px 0;font-size:13px;line-height:18px;cursor:pointer}
.chk.done span{color:#48454E;text-decoration:line-through;text-decoration-color:#B9B4BE}
.prog{height:8px;border-radius:4px;background:#ECE5F4;overflow:hidden}.prog i{display:block;height:100%;background:#35307E;border-radius:4px}
.av{width:32px;height:32px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:700;flex:none}
.applist{display:flex;flex-direction:column;gap:2px}
.applist .gh{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:700;color:#48454E;padding:12px 10px 4px}
.appbtn{display:flex;align-items:center;gap:8px;padding:8px 10px;border:0;border-radius:20px;background:transparent;text-align:left;font:inherit;font-size:14px;color:#1C1B1E;cursor:pointer}
.appbtn:hover{background:#F2EBFA}.appbtn[aria-current="page"]{background:#E3DFFF;color:#191836;font-weight:600}
.lens{display:grid;grid-template-columns:220px minmax(0,1fr);gap:24px;align-items:start}
.sugg{display:flex;align-items:center;gap:10px;width:100%;padding:12px 14px;border:1px solid #E6E0EC;border-radius:12px;background:#FFFFFF;text-align:left;font:inherit;font-size:14px;color:#1C1B1E;cursor:pointer}.sugg:hover{border-color:#CAC4CF;background:#FDF8FD}
.ansv{border:1px solid #E6E0EC;border-radius:12px;background:#FFFFFF;padding:16px;display:flex;flex-direction:column;gap:10px}
.srcs{display:flex;flex-direction:column;gap:4px}
.srcb{display:flex;align-items:center;gap:8px;padding:6px 8px;border:0;border-radius:8px;background:transparent;text-align:left;font:inherit;font-size:12px;color:#1C1B1E;cursor:pointer;min-width:0}.srcb:hover{background:#F2EBFA}
.srcb span{overflow-wrap:anywhere}
.fresh{font-size:11px;line-height:15px;color:#48454E}
.prov{display:flex;gap:8px;align-items:flex-start;padding:8px 10px;border-radius:8px;background:#FFF2B3;color:#3D3500;font-size:12px;line-height:17px}
.kbt .td{vertical-align:top}
.ad-mini{display:flex;flex-direction:column;gap:2px;width:220px;flex:none}
.ad-mini .h{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:700;color:#48454E;padding:12px 12px 4px}
.ad-mini a{padding:8px 12px;border-radius:20px;font-size:14px;color:#1C1B1E;text-decoration:none}.ad-mini a[aria-current="page"]{background:#E3DFFF;font-weight:600}
.pane-on .arch-split{grid-template-columns:minmax(0,1fr)!important}
.wiki{display:grid;grid-template-columns:220px minmax(0,1fr);gap:28px;align-items:start}
.wiki-nav{display:flex;flex-direction:column;gap:2px;position:sticky;top:0}
.wiki-nav .gh{font-family:Manrope,'BNPP Type','Segoe UI',system-ui,sans-serif;font-size:12px;font-weight:700;color:#48454E;padding:12px 10px 4px}
.wiki-nav .gh:first-child{padding-top:0}
.wiki-tips{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
.tipbox{display:flex;gap:10px;align-items:flex-start;padding:10px 12px;border-radius:8px;background:#E0FBFA;color:#002020;font-size:13px;line-height:19px}
.pane-on .wiki{grid-template-columns:minmax(0,1fr)}.pane-on .wiki-nav{display:none}
@container win (max-width: 1199px){.wiki{grid-template-columns:minmax(0,1fr)!important}.wiki-nav{display:none!important}.spaces{grid-template-columns:minmax(0,1fr)!important}.arch-split,.dd-grid{grid-template-columns:minmax(0,1fr)!important}.toc{display:none!important}.org{grid-template-columns:repeat(2,minmax(0,1fr))!important}.lens{grid-template-columns:minmax(0,1fr)!important}.applist{flex-direction:row!important;flex-wrap:wrap}.applist .gh{display:none}.ad-mini{display:none!important}}
@container win (max-width: 839px){.wiki-tips,.spaces,.path,.tl{grid-template-columns:minmax(0,1fr)!important}.flow{grid-template-columns:repeat(2,minmax(0,1fr))!important}.flow>div{border:1px solid #CAC4CF!important;border-radius:0!important}.seq li{grid-template-columns:22px minmax(0,1fr) 16px minmax(0,1fr)!important}.seq li>span:last-child{grid-column:2 / -1}}
@container win (max-width: 599px){.space{grid-template-columns:minmax(0,1fr)!important}.thumb{display:none}.org,.flow{grid-template-columns:minmax(0,1fr)!important}.rows>div{grid-template-columns:minmax(0,1fr)!important;gap:2px}.vt h2{font-size:20px}}
"""

# ---------------------------------------------------------------------------------------------------------
# Shared pieces
# ---------------------------------------------------------------------------------------------------------
def turn_markup(lst):
    return ('<sc-for list="{{' + lst + '}}" as="t" hint-placeholder-count="1">'
            '<div class="as-q">{{t.q}}</div><div class="as-a">'
            '<div class="as-trace"><b class="ui" style="font-size: 12px">Knowledge base · {{t.n}}</b><sc-for list="{{t.trace}}" as="x" hint-placeholder-count="2"><div class="row" style="gap: 8px"><span class="srcT" style="background: {{x.bg}}; color: {{x.fg}}">{{x.ab}}</span><span style="flex: 1; font-size: 12px; overflow-wrap: anywhere">{{x.label}}</span></div></sc-for></div>'
            '<div style="font-size: 14px; line-height: 20px">{{t.answer}}</div>'
            '<sc-if value="{{t.hasChain}}" hint-placeholder-val="{{false}}"><div class="chain"><sc-for list="{{t.chain}}" as="c" hint-placeholder-count="3"><div class="ch"><b>{{c.t}}</b><span>{{c.sub}}</span></div><sc-if value="{{c.more}}" hint-placeholder-val="{{true}}"><span class="ch-arr" aria-hidden="true">→</span></sc-if></sc-for></div></sc-if>'
            '<sc-if value="{{t.hasSteps}}" hint-placeholder-val="{{false}}"><ol class="steps"><sc-for list="{{t.steps}}" as="c" hint-placeholder-count="3"><li><span class="num">{{c.n}}</span><span><b class="ui">{{c.t}}</b><span class="meta" style="display: block">{{c.sub}}</span></span></li></sc-for></ol></sc-if>'
            '<sc-if value="{{t.hasList}}" hint-placeholder-val="{{false}}"><ul class="list" style="border: 1px solid #E6E0EC; border-radius: 12px; background: #FFFFFF; padding: 0 12px"><sc-for list="{{t.list}}" as="c" hint-placeholder-count="3"><li style="font-size: 13px; align-items: center"><span class="dot {{c.cls}}">{{c.mark}}</span><span style="flex: 1">{{c.t}}<span class="meta" style="display: block">{{c.sub}}</span></span></li></sc-for></ul></sc-if>'
            '<sc-if value="{{t.hasProv}}" hint-placeholder-val="{{false}}"><div class="prov"><b>Draft</b><span>{{t.prov}}</span></div></sc-if>'
            '<div class="srcs"><span class="meta">Sources</span><sc-for list="{{t.sources}}" as="x" hint-placeholder-count="2"><button type="button" class="srcb" onClick="{{x.go}}"><span class="srcT" style="background: {{x.bg}}; color: {{x.fg}}">{{x.ab}}</span><span>{{x.label}}</span></button></sc-for></div>'
            '<div class="fresh">{{t.fresh}}</div>'
            '</div></sc-for>')

PANE = ('<sc-if value="{{paneOn}}" hint-placeholder-val="{{false}}"><aside class="as-pane" aria-label="Assistant">'
        '<div class="as-hd">' + S.BOT + '<div style="flex: 1; min-width: 0"><div class="ui" style="font-size: 15px; font-weight: 700">Assistant</div><div style="font-size: 12px; color: #48454E">Answers from the knowledge base, with sources</div></div>'
        '<button type="button" class="ib" aria-label="Close assistant" onClick="{{asClose}}">' + CLOSE + '</button></div>'
        '<div class="as-body" aria-live="polite">'
        '<sc-if value="{{asEmpty}}" hint-placeholder-val="{{true}}"><div class="stack" style="gap: 10px; padding: 8px 0"><div class="ui" style="font-size: 18px; font-weight: 700">Ask the docs</div><span style="font-size: 13px; color: #48454E">Architecture, detailed design, AI guides, procedures and onboarding. Every answer says where it comes from and how fresh it is.</span><div class="stack" style="gap: 8px; margin-top: 4px"><sc-for list="{{asSugg}}" as="g" hint-placeholder-count="3"><button type="button" class="as-sugg" onClick="{{g.go}}">{{g.t}}</button></sc-for></div></div></sc-if>'
        + turn_markup('turns') +
        '</div>'
        '<div class="as-comp"><textarea id="dl-as-in" rows="2" aria-label="Ask the docs" placeholder="Ask about this page…" value="{{draft}}" onChange="{{onDraft}}" onKeyDown="{{onKey}}"></textarea>'
        '<div class="row" style="gap: 8px"><span class="as-chip">{{asCtx}}</span><span style="flex: 1"></span><button type="button" class="as-send" aria-label="Send" onClick="{{send}}">' + SEND + '</button></div></div>'
        '<div style="font-size: 11px; line-height: 15px; color: #48454E; text-align: center; padding: 6px 16px 10px">The assistant can make mistakes. Check the source before you act on it.</div>'
        '</aside></sc-if>')


ASKBTN = '<button type="button" class="btn t btn-i" onClick="{{openPane}}">' + SPARK + 'Ask</button>'

THUMBS = {
    'arch': '<i style="left:12px;top:14px;width:30px;height:18px;background:#FFF2B3;border:1.5px solid #5E5000"></i><i style="left:50px;top:14px;width:30px;height:18px;background:#CFEDFA;border:1.5px solid #0A5570"></i><i style="left:50px;top:48px;width:30px;height:18px;background:#CFEDFA;border:1.5px solid #0A5570"></i><i style="left:88px;top:48px;width:22px;height:18px;background:#D5EDC7;border:1.5px solid #2C5A1C"></i><i style="left:43px;top:23px;width:7px;height:1.5px;background:#48454E"></i><i style="left:65px;top:33px;width:1.5px;height:15px;background:#48454E"></i><i style="left:81px;top:57px;width:7px;height:1.5px;background:#48454E"></i>',
    'ai': '<i style="left:14px;top:14px;width:60px;height:16px;border-radius:8px 8px 8px 2px;background:#9CF1F0"></i><i style="left:44px;top:36px;width:62px;height:16px;border-radius:8px 8px 2px 8px;background:#E3DFFF"></i><i style="left:14px;top:58px;width:46px;height:14px;border-radius:7px 7px 7px 2px;background:#9CF1F0"></i>',
    'ops': '<i style="left:12px;top:22px;width:96px;height:2px;background:#CAC4CF"></i><i style="left:12px;top:16px;width:14px;height:14px;border-radius:50%;background:#35307E"></i><i style="left:40px;top:16px;width:14px;height:14px;border-radius:50%;background:#35307E"></i><i style="left:68px;top:16px;width:14px;height:14px;border-radius:50%;background:#FFF2B3;border:1.5px solid #5E5000;box-sizing:border-box"></i><i style="left:94px;top:16px;width:14px;height:14px;border-radius:50%;background:#C3F4DC;border:1.5px solid #006C46;box-sizing:border-box"></i><i style="left:12px;top:46px;width:60px;height:8px;background:#E6E0EC"></i><i style="left:12px;top:60px;width:84px;height:8px;background:#E6E0EC"></i>',
    'new': '<i style="left:14px;top:16px;width:12px;height:12px;background:#35307E"></i><i style="left:32px;top:18px;width:60px;height:8px;background:#E6E0EC"></i><i style="left:14px;top:36px;width:12px;height:12px;background:#35307E"></i><i style="left:32px;top:38px;width:48px;height:8px;background:#E6E0EC"></i><i style="left:14px;top:56px;width:12px;height:12px;background:#FFFFFF;border:1.5px solid #CAC4CF;box-sizing:border-box"></i><i style="left:32px;top:58px;width:70px;height:8px;background:#E6E0EC"></i>',
}
SPACE_CARDS = ''.join(f'<sc-if value="{{{{sp_{k}}}}}" hint-placeholder-val="{{{{true}}}}"><button type="button" class="space" onClick="{{{{go_{k}}}}}"><div class="thumb" aria-hidden="true">{THUMBS[k]}</div><div style="min-width: 0"><b>{{{{spT_{k}}}}}</b><p>{{{{spD_{k}}}}}</p><span class="meta">{{{{spM_{k}}}}}</span></div></button></sc-if>' for k in ['arch', 'ai', 'ops', 'new'])

RECENT = '''<div class="stack" style="gap: 4px"><div class="ui" style="font-size: 13px; font-weight: 700; color: #48454E">Recently updated</div>
  <ul class="list"><sc-for list="{{recent}}" as="r" hint-placeholder-count="4"><li><span class="srcT" style="background: {{r.bg}}; color: {{r.fg}}">{{r.ab}}</span><button type="button" class="lnk" style="text-decoration: none; color: #1C1B1E; font-size: 14px; text-align: left; flex: 1" onClick="{{r.go}}">{{r.t}}</button><span class="meta" style="white-space: nowrap">{{r.when}}</span></li></sc-for></ul></div>'''

KBLINE = '<div class="row r-wrap" style="gap: 8px; font-size: 12px; color: #48454E"><span>Knowledge base · 7 sources · updated today 08:41</span><button type="button" class="lnk" style="font-size: 12px" onClick="{{goKb}}">Sources</button></div>'

# Architecture: the Corporate credit platform (markup in docs_arch.py)
import docs_arch as ARC
ARCH = ARC.ARCH

# ---------------------------------------------------------------------------------------------------------
# Home, three ways in
# ---------------------------------------------------------------------------------------------------------
HOME_A = '''<sc-if value="{{homeA}}" hint-placeholder-val="{{true}}"><div class="stack" style="gap: 20px; max-width: 1040px">
  <div class="spaces">''' + SPACE_CARDS + '''</div>
  ''' + RECENT + KBLINE + '''
</div></sc-if>'''

HOME_B = ARC.HOME_B

HOME_C = '''<sc-if value="{{homeC}}" hint-placeholder-val="{{false}}"><div class="stack" style="gap: 20px; max-width: 820px; width: 100%; align-self: center">
  <div class="stack" style="gap: 6px; text-align: center; padding-top: 12px"><h2 class="ui" style="margin: 0; font-size: 26px; line-height: 34px">What do you need to know?</h2><span class="sub">Ask in the search bar at the top, or start with one of these. Answers come with their source.</span></div>
  <sc-if value="{{cEmpty}}" hint-placeholder-val="{{true}}"><div class="stack" style="gap: 8px"><sc-for list="{{cSugg}}" as="g" hint-placeholder-count="5"><button type="button" class="sugg" onClick="{{g.go}}"><span class="srcT" style="background: {{g.bg}}; color: {{g.fg}}">{{g.ab}}</span><span style="flex: 1">{{g.t}}</span></button></sc-for></div></sc-if>
  <sc-if value="{{cHasTurns}}" hint-placeholder-val="{{false}}"><div class="ansv">''' + turn_markup('turns') + '''<div class="row"><button type="button" class="lnk" onClick="{{asClear}}">New question</button></div></div></sc-if>
  <div class="row r-wrap" style="gap: 8px; justify-content: center"><span class="meta">Browse</span><button type="button" class="chip" style="height: 32px" onClick="{{go_arch}}">Architecture</button><button type="button" class="chip" style="height: 32px" onClick="{{go_ai}}">AI wiki</button><button type="button" class="chip" style="height: 32px" onClick="{{go_ops}}">Operations</button><button type="button" class="chip" style="height: 32px" onClick="{{go_new}}">New joiner</button></div>
  ''' + KBLINE + '''
</div></sc-if>'''

# ---------------------------------------------------------------------------------------------------------
# Detailed design
# ---------------------------------------------------------------------------------------------------------
DD_PICS = ''.join(f'<sc-if value="{{{{x.{k}}}}}" hint-placeholder-val="{{{{false}}}}">{h}</sc-if>' for k, h in D.dd_diagrams())
DDV = '''<sc-if value="{{vDd}}" hint-placeholder-val="{{false}}"><div class="stack arch-ds" style="gap: 14px">
  ''' + S.subheader('{{ddBack}}', 'Back to the architecture', '{{dd.title}}', ctx='{{dd.hexLayer}} · {{dd.commit}}') + '''
  <div class="row r-wrap" style="gap: 12px"><sc-if value="{{dd.hasLayers}}" hint-placeholder-val="{{true}}"><div class="seg" role="group" aria-label="Layer" style="max-width: 100%; overflow-x: auto"><sc-for list="{{dd.layers}}" as="c" hint-placeholder-count="5"><button type="button" aria-pressed="{{c.on}}" onClick="{{c.pick}}">{{c.label}}</button></sc-for></div></sc-if></div>
  <div class="row r-wrap" style="gap: 6px 14px; font-size: 12px; color: #48454E"><span class="mono">{{dd.id}}</span><span>realizes <span class="mono">{{dd.realizes}}</span></span><span>design intent · tier 1</span><span class="mono">{{dd.path}}</span></div>
  <div class="dd-grid">
    <article class="stack" style="gap: 0; max-width: 980px; min-width: 0">
      <sc-for list="{{dd.secs}}" as="x" hint-placeholder-count="3"><section class="dd-sec"><h3>{{x.h}}</h3>
        <sc-if value="{{x.hasP}}" hint-placeholder-val="{{true}}"><p>{{x.p}}</p></sc-if>
        <sc-if value="{{x.hasB}}" hint-placeholder-val="{{false}}"><ul class="dd-ul"><sc-for list="{{x.b}}" as="b" hint-placeholder-count="3"><li>{{b}}</li></sc-for></ul></sc-if>
        <sc-if value="{{x.hasChain}}" hint-placeholder-val="{{false}}"><div class="chain"><sc-for list="{{x.chain}}" as="c" hint-placeholder-count="4"><div class="ch"><b>{{c.t}}</b><span>{{c.sub}}</span></div><sc-if value="{{c.more}}" hint-placeholder-val="{{true}}"><span class="ch-arr" aria-hidden="true">→</span></sc-if></sc-for></div></sc-if>
        <sc-if value="{{x.hasSeq}}" hint-placeholder-val="{{false}}"><ol class="seq"><sc-for list="{{x.seq}}" as="m" hint-placeholder-count="4"><li><span class="meta">{{m.n}}</span><span class="who">{{m.f}}</span><span aria-label="to" style="color: #79757F">→</span><span class="who">{{m.t}}</span><span>{{m.msg}}</span></li></sc-for></ol></sc-if>
        <sc-if value="{{x.hasPic}}" hint-placeholder-val="{{false}}">''' + DD_PICS + '''<span class="meta" style="display: block; margin-top: 4px">{{x.pic}}</span></sc-if>
        <sc-if value="{{x.hasTable}}" hint-placeholder-val="{{false}}"><div class="dd-tbl"><table><thead><tr><sc-for list="{{x.thead}}" as="hd" hint-placeholder-count="3"><th>{{hd}}</th></sc-for></tr></thead><tbody><sc-for list="{{x.trows}}" as="tr" hint-placeholder-count="3"><tr><sc-for list="{{tr.cells}}" as="cl" hint-placeholder-count="3"><td class="{{cl.cls}}">{{cl.t}}</td></sc-for></tr></sc-for></tbody></table></div></sc-if>
        <sc-if value="{{x.hasApi}}" hint-placeholder-val="{{false}}"><ul class="dd-api"><sc-for list="{{x.api}}" as="op" hint-placeholder-count="3"><li><span class="mth {{op.mcls}}">{{op.m}}</span><code>{{op.path}}</code><span class="op">{{op.op}}</span><span class="meta">{{op.resp}}</span></li></sc-for></ul></sc-if>
        <sc-if value="{{x.hasRows}}" hint-placeholder-val="{{false}}"><div class="rows"><sc-for list="{{x.rows}}" as="r" hint-placeholder-count="3"><div><b class="ui" style="font-size: 13px">{{r.a}}</b><span>{{r.b}}</span><span class="meta">{{r.c}}</span></div></sc-for></div></sc-if>
      </section></sc-for>
      <div class="row r-wrap" style="gap: 14px; padding-top: 14px; border-top: 1px solid #ECE5F4"><button type="button" class="lnk" onClick="{{ddSite}}">Read on the Doc Site</button><span style="flex: 1"></span><button type="button" class="lnk" onClick="{{ddEdit}}">Propose a change</button></div>
    </article>
    <nav class="toc" aria-label="On this page"><span class="meta" style="padding: 0 10px 6px">On this page</span><sc-for list="{{dd.secs}}" as="x" hint-placeholder-count="3"><a href="#dd">{{x.h}}</a></sc-for></nav>
  </div>
</div></sc-if>'''

# ---------------------------------------------------------------------------------------------------------
# AI wiki: tips, procedures and news written by the community
PLUS_ICON = f'<svg width="18" height="18" viewBox="0 0 24 24" {ST}><path d="M12 5v14M5 12h14"/></svg>'
# ---------------------------------------------------------------------------------------------------------
AIV = '''<sc-if value="{{vAi}}" hint-placeholder-val="{{false}}"><div class="stack" style="gap: 16px">
  <sc-if value="{{wikiAtHome}}" hint-placeholder-val="{{true}}">''' + S.subheader('{{goHome}}', 'Back to Docs', 'AI wiki', ctx='Tips, procedures and news from the community · {{wikiCount}} pages', actions='<button type="button" class="btn t btn-i" onClick="{{wikiNew}}">' + PLUS_ICON + 'New page</button>') + '''</sc-if>
  <sc-if value="{{wikiOnPage}}" hint-placeholder-val="{{false}}">''' + S.subheader('{{wikiHome}}', 'Back to the AI wiki', '{{wp.title}}', ctx='{{wp.ctx}}', actions='<button type="button" class="btn x" onClick="{{wikiEdit}}">Edit</button>') + '''</sc-if>
  <div class="wiki">
    <nav class="wiki-nav" aria-label="AI wiki"><sc-for list="{{wikiNav}}" as="c" hint-placeholder-count="3"><div class="gh">{{c.label}}</div><sc-for list="{{c.pages}}" as="g" hint-placeholder-count="3"><button type="button" class="appbtn" aria-current="{{g.cur}}" onClick="{{g.open}}"><span style="flex: 1">{{g.t}}</span></button></sc-for></sc-for></nav>
    <div class="stack" style="gap: 20px; min-width: 0; max-width: 760px">
      <sc-if value="{{wikiAtHome}}" hint-placeholder-val="{{true}}">
        <div class="stack" style="gap: 4px"><div class="ui" style="font-size: 13px; font-weight: 700; color: #48454E">News</div>
          <ul class="list"><sc-for list="{{wikiNews}}" as="g" hint-placeholder-count="3"><li><span class="meta" style="width: 52px; flex: none">{{g.date}}</span><span style="flex: 1"><button type="button" class="lnk" style="text-decoration: none; color: #1C1B1E; font-size: 14px; font-weight: 600; text-align: left" onClick="{{g.open}}">{{g.t}}</button><span class="meta" style="display: block">{{g.sum}}</span></span></li></sc-for></ul></div>
        <div class="stack" style="gap: 8px"><div class="ui" style="font-size: 13px; font-weight: 700; color: #48454E">Tips</div>
          <div class="wiki-tips"><sc-for list="{{wikiTips}}" as="g" hint-placeholder-count="4"><button type="button" class="guide" style="flex-direction: column; align-items: flex-start; gap: 4px" onClick="{{g.open}}"><b class="ui">{{g.t}}</b><span class="meta">{{g.sum}}</span></button></sc-for></div></div>
        <div class="stack" style="gap: 4px"><div class="ui" style="font-size: 13px; font-weight: 700; color: #48454E">Procedures</div>
          <ul class="list"><sc-for list="{{wikiProcs}}" as="g" hint-placeholder-count="4"><li><span style="flex: 1"><button type="button" class="lnk" style="text-decoration: none; color: #1C1B1E; font-size: 14px; font-weight: 600; text-align: left" onClick="{{g.open}}">{{g.t}}</button><span class="meta" style="display: block">{{g.sum}}</span></span><span class="meta">{{g.n}} steps</span></li></sc-for></ul></div>
      </sc-if>
      <sc-if value="{{wikiOnPage}}" hint-placeholder-val="{{false}}"><article class="stack" style="gap: 0">
        <sc-for list="{{wp.secs}}" as="x" hint-placeholder-count="3"><section class="dd-sec"><sc-if value="{{x.hasH}}" hint-placeholder-val="{{true}}"><h3>{{x.h}}</h3></sc-if>
          <sc-if value="{{x.hasP}}" hint-placeholder-val="{{true}}"><p>{{x.p}}</p></sc-if>
          <sc-if value="{{x.hasB}}" hint-placeholder-val="{{false}}"><ul class="dd-ul"><sc-for list="{{x.b}}" as="b" hint-placeholder-count="3"><li>{{b}}</li></sc-for></ul></sc-if>
          <sc-if value="{{x.hasSteps}}" hint-placeholder-val="{{false}}"><ol class="steps"><sc-for list="{{x.steps}}" as="c" hint-placeholder-count="3"><li><span class="num">{{c.n}}</span><span>{{c.t}}</span></li></sc-for></ol></sc-if>
          <sc-if value="{{x.hasTip}}" hint-placeholder-val="{{false}}"><div class="tipbox"><b class="ui">Tip</b><span>{{x.tip}}</span></div></sc-if>
        </section></sc-for>
        <div class="row r-wrap" style="gap: 8px 14px; padding-top: 14px; border-top: 1px solid #ECE5F4"><span class="meta">Written by {{wp.by}} · {{wp.edits}}</span><span style="flex: 1"></span><span class="meta">Related</span><sc-for list="{{wp.related}}" as="r" hint-placeholder-count="2"><button type="button" class="chip" style="height: 28px" onClick="{{r.open}}">{{r.t}}</button></sc-for></div>
      </article></sc-if>
    </div>
  </div>
</div></sc-if>'''

# ---------------------------------------------------------------------------------------------------------
# Operations
# ---------------------------------------------------------------------------------------------------------
OPSV = '''<sc-if value="{{vOps}}" hint-placeholder-val="{{false}}"><div class="stack" style="gap: 18px">
  ''' + S.subheader('{{goHome}}', 'Back to Docs', 'Operations', ctx='Releases, teams and incidents') + '''
  <div class="row r-wrap" role="tablist" aria-label="Operations" style="gap: 0; border-bottom: 1px solid #CAC4CF"><sc-for list="{{opsTabs}}" as="t" hint-placeholder-count="4"><button type="button" role="tab" class="tab {{t.cls}}" aria-selected="{{t.on}}" onClick="{{t.pick}}">{{t.label}}</button></sc-for></div>
  <sc-if value="{{oRelease}}" hint-placeholder-val="{{true}}"><div class="stack" style="gap: 12px">
    <div class="row r-wrap" style="gap: 8px"><b class="ui" style="font-size: 16px">Weekly release train</b><span class="meta" style="flex: 1">release/weekly-train.md · owner Release team · reviewed 12 Oct</span></div>
    <div class="lanes-wrap"><div class="lanes"><div class="lh"></div><sc-for list="{{days}}" as="d" hint-placeholder-count="5"><div class="lh">{{d}}</div></sc-for>
      <sc-for list="{{lanes}}" as="l" hint-placeholder-count="3"><div class="ln">{{l.name}}</div><sc-for list="{{l.cells}}" as="c" hint-placeholder-count="5"><div><sc-if value="{{c.has}}" hint-placeholder-val="{{false}}"><div class="stp {{c.cls}}"><b>{{c.t}}</b><span>{{c.sub}}</span></div></sc-if></div></sc-for></sc-for></div></div>
    <div class="panel" style="flex-direction: row; flex-wrap: wrap; align-items: center; gap: 10px 16px"><b class="ui">Hotfix, any day</b><div class="chain" style="flex: 1; min-width: 280px"><sc-for list="{{hotfix}}" as="c" hint-placeholder-count="4"><div class="ch"><b>{{c.t}}</b><span>{{c.sub}}</span></div><sc-if value="{{c.more}}" hint-placeholder-val="{{true}}"><span class="ch-arr" aria-hidden="true">→</span></sc-if></sc-for></div></div>
  </div></sc-if>
  <sc-if value="{{oOrg}}" hint-placeholder-val="{{false}}"><div class="stack" style="gap: 12px">
    <div class="row r-wrap" style="gap: 8px"><b class="ui" style="font-size: 16px">Portfolios and teams</b><span class="meta" style="flex: 1">From the application catalog and the on-call schedule · this week</span></div>
    <div class="org"><sc-for list="{{org}}" as="p" hint-placeholder-count="4"><div class="panel" style="gap: 0"><b class="ui" style="font-size: 15px; padding-bottom: 6px">{{p.name}}</b><sc-for list="{{p.teams}}" as="t" hint-placeholder-count="2"><div class="team"><b class="ui">{{t.name}}</b><span class="meta">Lead {{t.lead}}</span><span class="meta">On call {{t.oncall}}</span></div></sc-for></div></sc-for></div>
  </div></sc-if>
  <sc-if value="{{oInc}}" hint-placeholder-val="{{false}}"><div class="stack" style="gap: 14px; max-width: 980px">
    <b class="ui" style="font-size: 16px">Severity and response</b>
    <div class="rows"><div style="grid-template-columns: 60px minmax(0, 1fr) minmax(0, 1fr) minmax(0, 1fr)"><b class="meta">Level</b><b class="meta">First response</b><b class="meta">Who is paged</b><b class="meta">Updates</b></div><sc-for list="{{sev}}" as="r" hint-placeholder-count="4"><div style="grid-template-columns: 60px minmax(0, 1fr) minmax(0, 1fr) minmax(0, 1fr)"><b class="ui">{{r.l}}</b><span>{{r.a}}</span><span>{{r.b}}</span><span>{{r.c}}</span></div></sc-for></div>
    <b class="ui" style="font-size: 16px">Runbooks</b>
    <ul class="list"><sc-for list="{{runbooks}}" as="r" hint-placeholder-count="3"><li><span style="flex: 1">{{r.t}}<span class="meta" style="display: block">{{r.m}}</span></span></li></sc-for></ul>
  </div></sc-if>
  <sc-if value="{{oDs}}" hint-placeholder-val="{{false}}"><div class="stack" style="gap: 14px; max-width: 860px">
    <div class="panel"><div class="row r-wrap" style="gap: 12px"><b class="ui" style="font-size: 16px; flex: 1">AIToolbox design system</b><button type="button" class="btn t btn-i" onClick="{{openDs}}">''' + EXT + '''Open</button></div>
      <p style="margin: 0; font-size: 14px; line-height: 20px">Night &amp; neon color roles, type scale, components for Angular Material, feature marks, the ArchiMate notation, and the rules every screen follows: minimal by default, one primary action, status as a chip.</p>
      <span class="meta">Design System artifact · owner Platform team · changed 29 Oct</span></div>
    <b class="ui" style="font-size: 16px">Change the design system</b>
    <div class="chain"><div class="ch"><b>Propose</b><span>in Community › Ideas</span></div><span class="ch-arr">→</span><div class="ch"><b>Lab</b><span>alternatives side by side</span></div><span class="ch-arr">→</span><div class="ch"><b>Decide</b><span>one adopted, kept for the record</span></div><span class="ch-arr">→</span><div class="ch"><b>Publish</b><span>component rules and Angular</span></div></div>
  </div></sc-if>
</div></sc-if>'''

# ---------------------------------------------------------------------------------------------------------
# New joiner
# ---------------------------------------------------------------------------------------------------------
NEWV = '''<sc-if value="{{vNew}}" hint-placeholder-val="{{false}}"><div class="stack" style="gap: 18px; max-width: 1100px">
  ''' + S.subheader('{{goHome}}', 'Back to Docs', 'New joiner', ctx='Day 1 · Week 1 · Month 1') + '''
  <div class="stack" style="gap: 6px"><div class="row" style="gap: 12px"><div class="prog" style="flex: 1; max-width: 420px"><i style="width: {{njPct}}%"></i></div><span class="meta">{{njDone}} of {{njTotal}} done</span></div></div>
  <div class="tl"><sc-for list="{{njCols}}" as="c" hint-placeholder-count="3"><div class="panel" style="gap: 0"><b class="ui" style="font-size: 15px; padding-bottom: 4px">{{c.label}}</b><sc-for list="{{c.items}}" as="i" hint-placeholder-count="3"><label class="chk {{i.cls}}"><input type="checkbox" class="cb" checked="{{i.on}}" onChange="{{i.toggle}}"><span>{{i.t}}</span></label></sc-for></div></sc-for></div>
  <div class="spaces" style="grid-template-columns: repeat(3, minmax(0, 1fr))">
    <div class="panel"><b class="ui">People to meet</b><sc-for list="{{people}}" as="p" hint-placeholder-count="3"><div class="row" style="gap: 10px"><span class="av" style="background: {{p.bg}}">{{p.ini}}</span><span style="flex: 1; min-width: 0; font-size: 13px; line-height: 18px">{{p.name}}<span class="meta" style="display: block">{{p.role}}</span></span></div></sc-for></div>
    <div class="panel"><b class="ui">Your access</b><span class="meta">Created from the directory when you joined</span><sc-for list="{{access}}" as="a" hint-placeholder-count="3"><div class="row" style="gap: 8px; font-size: 13px"><span style="flex: 1">{{a.t}}</span><span class="tile {{a.cls}}"><i></i>{{a.st}}</span></div></sc-for></div>
    <div class="panel"><b class="ui">Words you will hear</b><sc-for list="{{glossary}}" as="g" hint-placeholder-count="3"><div style="font-size: 13px; line-height: 18px"><b class="ui">{{g.t}}</b> · <span style="color: #48454E">{{g.d}}</span></div></sc-for></div>
  </div>
</div></sc-if>'''

# ---------------------------------------------------------------------------------------------------------
# Administration › Core › Knowledge base
# ---------------------------------------------------------------------------------------------------------
KBV = '''<sc-if value="{{vKb}}" hint-placeholder-val="{{false}}"><div class="row" style="gap: 24px; align-items: flex-start">
  <nav class="ad-mini" aria-label="Administration"><span class="h">Core</span><a href="#kb">General</a><a href="#kb">Users and permissions</a><a href="#kb">Catalog</a><a href="#kb" aria-current="page">Knowledge base</a><span class="h">Sweep</span><a href="#kb">Connectors</a></nav>
  <div class="stack" style="gap: 16px; flex: 1; min-width: 0">
    <div class="vt"><h2>Knowledge base</h2><span style="flex: 1"></span><button type="button" class="btn t" onClick="{{kbAdd}}">Add a source</button></div>
    <p class="sub" style="max-width: 760px">What the assistant and Sweep can read, through the Knowledge base MCP server. Each source is indexed when it is published; nothing is written by hand.</p>
    <div class="card" style="padding: 0; overflow: hidden"><div class="ad-tscroll"><table class="ad-tbl kbt" style="width: 100%; border-collapse: collapse">
      <thead><tr><th class="th">Source</th><th class="th">From</th><th class="th">Indexed as</th><th class="th">Updated</th><th class="th">Status</th></tr></thead>
      <tbody><sc-for list="{{kbRows}}" as="r" hint-placeholder-count="6"><tr class="rw"><td class="td"><div class="row" style="gap: 8px"><span class="srcT" style="background: {{r.bg}}; color: {{r.fg}}">{{r.ab}}</span><b class="ui">{{r.name}}</b></div></td><td class="td"><span style="font-size: 13px">{{r.from}}</span></td><td class="td"><span style="font-size: 13px">{{r.as}}</span><div class="meta">{{r.n}}</div></td><td class="td"><span class="meta">{{r.when}}</span></td><td class="td"><span class="tile {{r.cls}}"><i></i>{{r.st}}</span></td></tr></sc-for></tbody></table></div></div>
    <div class="spaces">
      <div class="panel"><b class="ui">Tools the assistant uses</b><ul class="list"><sc-for list="{{kbTools}}" as="t" hint-placeholder-count="5"><li style="font-size: 13px"><span class="mono" style="flex: none; width: 160px">{{t.n}}</span><span class="meta" style="flex: 1">{{t.d}}</span></li></sc-for></ul></div>
      <div class="panel"><b class="ui">Answer quality</b><span style="font-size: 14px">52 questions with their expected sources run on every publish: <b>49 pass</b>.</span><span class="meta">Failing: 2 on the Collateral register (inferred, no architect yet), 1 on the hotfix procedure (two pages disagree).</span><button type="button" class="lnk" style="align-self: flex-start" onClick="{{kbEval}}">See the questions</button></div>
    </div>
  </div>
</div></sc-if>'''

BODY = '''<div style="width: 1440px; box-sizing: border-box; background: #FDF8FD; color: #1C1B1E; display: flex; flex-direction: column">
  <div style="padding: 20px 32px 12px; display: flex; flex-direction: column; gap: 12px">
    <div style="display: flex; align-items: center; gap: 16px">
      <h1 class="ui" style="margin: 0; font-size: 24px; line-height: 32px; font-weight: 700; white-space: nowrap">Docs lab</h1>
      <span style="font-size: 14px; color: #48454E">One Docs, several sources: the architecture model (a worked example in the AIToolbox ArchiMate notation: Elements, LikeC4 views by TOGAF phase, Process), an AI wiki written by the community (tips, procedures, news), operational procedures (release, organization, incidents, design system) and the new joiner path. Everything is visual, and everything can be asked through the Knowledge base. Search and questions go through the header’s search bar only; going back is a subheader. Way in A · Spaces is adopted; B and C stay for the record. Press Play.</span>
    </div>
    <div class="row" style="gap: 12px; flex-wrap: wrap">SIMBAR<span class="row r-wrap" style="gap: 8px; padding: 6px 8px 6px 12px; border: 1px dashed #79757F; border-radius: 12px"><span class="ui" style="font-size: 12px; font-weight: 600; color: #48454E">Way in</span><sc-for list="{{variantChips}}" as="r" hint-placeholder-count="3"><button type="button" class="chip" style="height: 28px; font-size: 12px; {{r.style}}" aria-pressed="{{r.on}}" onClick="{{r.pick}}">{{r.label}}</button></sc-for></span><span class="row r-wrap" style="gap: 8px; padding: 6px 8px 6px 12px; border: 1px dashed #79757F; border-radius: 12px"><span class="ui" style="font-size: 12px; font-weight: 600; color: #48454E">Screen</span><sc-for list="{{screenChips}}" as="r" hint-placeholder-count="7"><button type="button" class="chip" style="height: 28px; font-size: 12px; {{r.style}}" aria-pressed="{{r.on}}" onClick="{{r.pick}}">{{r.label}}</button></sc-for></span></div>
  </div>
  <div style="margin: 0 32px; border-radius: 12px; overflow: hidden; border: 1px solid #CAC4CF">
  SIMOPEN
  <div style="position: relative; width: 100%; height: 100%; display: flex; flex-direction: column; background: #FDF8FD; overflow: hidden">
    HEADER
    <div style="position: relative; flex: 1; display: flex; min-height: 0">
      <sc-if value="{{railDocs}}" hint-placeholder-val="{{true}}"><div class="ad-railwrap" style="display: flex">RAIL_DOCS</div></sc-if><sc-if value="{{railAdm}}" hint-placeholder-val="{{false}}"><div class="ad-railwrap" style="display: flex">RAIL_ADM</div></sc-if>
      <main class="{{mainCls}}" style="position: relative; flex: 1; min-width: 0; padding: 20px 32px 24px; box-sizing: border-box; display: flex; flex-direction: column; gap: 16px; overflow-y: auto">
        <div aria-live="polite" style="position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0)">{{live}}</div>
        @@VIEWS@@
        <sc-if value="{{hasSnack}}" hint-placeholder-val="{{false}}"><div role="status" style="position: sticky; bottom: 8px; align-self: flex-start; display: flex; align-items: center; gap: 16px; padding: 12px 16px; border-radius: 8px; background: #322F35; color: #F5EFF7; font-size: 14px; box-shadow: 0 4px 8px 3px rgba(0,0,0,.15); max-width: 100%; box-sizing: border-box">{{snack}}<button type="button" class="ib" aria-label="Dismiss" style="margin: -8px -8px -8px 0; color: #F5EFF7" onClick="{{closeSnack}}">✕</button></div></sc-if>
      </main>
      @@PANE@@
    </div>
    NAVBAR
  </div>
  SIMCLOSE
  </div>
  <div style="padding: 20px 32px 32px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; align-items: start">
    <div class="card stack" style="gap: 8px; padding: 20px"><span class="h2">Way in · A adopted</span>
      <ul class="list">
        <li><b class="ui" style="width: 18px">A</b><span style="flex: 1"><b class="ui">Spaces</b> · four spaces, each with its own picture: views, a learning path, a release train, a checklist. <span class="tile ok" style="margin: 4px 0 2px"><i></i>Adopted 30 Oct</span><span class="meta" style="display: block">One entry for everyone; the architecture space opens on Elements, Views and Process. Also in the production vision.</span></span></li>
        <li><b class="ui" style="width: 18px">B</b><span style="flex: 1"><b class="ui">Application lens</b> · pick an application and see its view, design, procedures and decisions together. <span class="meta" style="display: block">Not adopted, kept for the record: best for architects and leads; weaker for the AI wiki and onboarding, which belong to no application.</span></span></li>
        <li><b class="ui" style="width: 18px">C</b><span style="flex: 1"><b class="ui">Ask first</b> · suggested questions are the page; the header’s search bar asks, and answers come back as pictures with their sources. <span class="meta" style="display: block">Not adopted, kept for the record: fast for people who know what they want; hides what exists from people who do not. Asking stays in the header for everyone.</span></span></li>
      </ul></div>
    <div class="card stack" style="gap: 8px; padding: 20px"><span class="h2">One knowledge base, seven sources</span>
      <ul class="list" style="font-size: 13px">
        <li><span class="srcT" style="background: #CFEDFA; color: #0A5570">ARCH</span><span style="flex: 1">Architecture model · LikeC4 and Markdown in the central repository · one document per element, plus graph tools</span></li>
        <li><span class="srcT" style="background: #E3DFFF; color: #14085E">DD</span><span style="flex: 1">Detailed design · Markdown in each application repository · one document per section</span></li>
        <li><span class="srcT" style="background: #ECE5F4; color: #48454E">API</span><span style="flex: 1">Contracts · OpenAPI and AsyncAPI · one document per operation</span></li>
        <li><span class="srcT" style="background: #9CF1F0; color: #002020">AI</span><span style="flex: 1">AI wiki · community pages: tips, procedures, news · one document per section</span></li>
        <li><span class="srcT" style="background: #FFDCC2; color: #4A2800">OPS</span><span style="flex: 1">Procedures · doc site · one document per section</span></li>
        <li><span class="srcT" style="background: #C3F4DC; color: #00391E">NEW</span><span style="flex: 1">New joiner · doc site, plus your access from the directory</span></li>
        <li><span class="srcT" style="background: #FFF2B3; color: #5E5000">GLO</span><span style="flex: 1">Glossary · domain reference · one document per term</span></li>
      </ul></div>
    <div class="card stack" style="gap: 8px; padding: 20px"><span class="h2">Rules</span>
      <ul class="list" style="font-size: 13px">
        <li>Pictures are generated from a model or from Markdown. No fact lives only in a picture, so the assistant can answer it from the header’s search bar.</li>
        <li>Every answer lists its sources (id or path) and the version: plateau, commit, date.</li>
        <li>A source inferred from code is a draft until an architect authors it, and answers say so.</li>
        <li>The docs are never edited from here: Propose a change opens a pull request.</li>
        <li>The frame takes the height of the screen (up to 1080 px in this lab), so Administration and Cookie policy stay at the bottom of the rail.</li>
      </ul></div>
  </div>
</div>'''

LOGIC = r'''
class Component extends DCLogic {
  constructor(props) { super(props); this.simHostId = 'sim-host-dl'; this.simDefault = 1374; this.simMinH = 560; this.simMaxH = 1080;
    this.state = { variant: 'A', view: 'home', arch: null, dd: 'dd.cc-facility.domain', opsTab: 'release', nj: { d1: true, d2: true, d3: true, w1: true }, wiki: null, asOpen: false, turns: [], draft: '', snack: null, live: '', simW: null, simAvail: 0, simAvailH: 0 }; }
/*SIMJS*/
  componentDidMount() { var self = this; this.simSync(); if (typeof window !== 'undefined') window.addEventListener('resize', function () { self.simSync(); }); }
  componentDidUpdate() { this.simSync(); }
  match(t) {
    t = (t || '').toLowerCase();
    if (/hotfix|release train|thursday/.test(t)) return 'ops_hotfix';
    if (/why .*export|nightly export/.test(t)) return 'arch_why';
    if (/\barb\b|ready for the board|readiness/.test(t)) return 'arb_ready';
    if (/active|activat/.test(t)) return 'dd_expire';
    if (/depend|impact|limit-service/.test(t)) return 'arch_dep';
    if (/skill|jira/.test(t)) return 'ai_skill';
    if (/first week|joiner|onboard|joined/.test(t)) return 'new_week';
    if (/on.?call|paged/.test(t)) return 'org_oncall';
    if (/paste|secret|which data/.test(t)) return 'ai_data';
    if (/collateral register|inferred|draft/.test(t)) return 'arch_inferred';
    if (/word|mean|module|work item|checkpoint|plateau/.test(t)) return 'glossary';
    return 'default';
  }
  renderVals() {
    var s = this.state, self = this, sim = this.simVals(), DG = __DG__;
    var set = function (o) { return function (e) { if (e && e.preventDefault) e.preventDefault(); self.setState(typeof o === 'function' ? o(e) : o); }; };
    var val = function (e) { return e && e.target ? e.target.value : ''; };
    var ON = 'background: #E3DFFF; border-color: #E3DFFF; color: #191836';
    var SRC = { ARCH: ['#CFEDFA', '#0A5570'], DD: ['#E3DFFF', '#14085E'], API: ['#ECE5F4', '#48454E'], AI: ['#9CF1F0', '#002020'], OPS: ['#FFDCC2', '#4A2800'], NEW: ['#C3F4DC', '#00391E'], GLO: ['#FFF2B3', '#5E5000'], ADR: ['#CFEDFA', '#0A5570'], DIR: ['#ECE5F4', '#48454E'], CAT: ['#E3DFFF', '#14085E'] };
    var tileOf = function (ab) { var c = SRC[ab] || SRC.API; return { ab: ab, bg: c[0], fg: c[1] }; };
    var cInline = s.variant === 'C' && s.view === 'home';
    var ask = function (qid, text, extra) { return set(function () { return Object.assign({ turns: s.turns.concat([{ q: qid, text: text, el: s.el, app: s.app }]), draft: '', asOpen: !(s.variant === 'C' && (extra && extra.view ? extra.view : s.view) === 'home'), live: 'Answer ready' }, extra || {}); }); };
    var sendDraft = function () { var t = (s.draft || '').trim(); if (!t) return; self.setState({ turns: s.turns.concat([{ q: self.match(t), text: t, el: s.el, app: s.app }]), draft: '', asOpen: !cInline, live: 'Answer ready' }); };

/*ARCHJS*/
    // ---- detailed design
    var ddRaw = DG.dds[s.dd] || DG.dds['dd.cc-facility.domain'];
    var sibl = Object.keys(DG.dds).filter(function (k) { return DG.dds[k].module === ddRaw.module; });
    var mk = function (arr, more) { return arr.map(function (c, i) { return { t: c[0], sub: c[1], more: i < arr.length - 1 }; }); };
    var dd = { kind: ddRaw.kind, id: ddRaw.id, title: ddRaw.title, path: ddRaw.path, realizes: ddRaw.realizes, commit: ddRaw.commit,
      hasLayers: sibl.length > 1, layers: sibl.map(function (k) { return { label: DG.dds[k].layer, on: k === ddRaw.id, pick: set({ dd: k }) }; }),
      secs: ddRaw.sections.map(function (x, i) { var o = { h: x.h, hasP: !!x.p, p: x.p || '', hasB: !!x.b, b: x.b || [], hasChain: !!x.chain, chain: x.chain ? mk(x.chain) : [], hasSeq: !!x.seq, seq: (x.seq || []).map(function (m, i) { return { n: i + 1, f: m[0], t: m[1], msg: m[2] }; }), hasRows: !!x.rows, rows: (x.rows || []).map(function (r) { return { a: r[0], b: r[1], c: r[2] }; }),
        hasTable: !!x.table, thead: x.table ? x.table.head : [], trows: x.table ? x.table.rows.map(function (r) { return { cells: r.map(function (c, j) { return { t: c, cls: j === 0 ? 'k' : '' }; }) }; }) : [],
        hasApi: !!x.api, api: (x.api || []).map(function (r) { return { m: r[0], mcls: 'm-' + r[0].toLowerCase(), path: r[1], op: r[2], resp: r[3] }; }), hasPic: !!(x.sm || x.er || x.hex),
        pic: x.sm ? 'State machine · generated from the domain model' : x.er ? 'Data model · generated from the Liquibase changelog' : x.hex ? 'Hexagonal architecture of ' + ddRaw.module : '' };
        o['g_' + ddRaw.id.replace(/[.-]/g, '_') + '_' + i] = true; return o; }) };
    dd.ctx = dd.kind ? '' : '';
    var HEXL = { domain: 'Domain · center of the hexagon', 'domain-events': 'Domain · events', ports: 'Ports · edge of the hexagon', application: 'Application · use cases', infrastructure: 'Infrastructure · adapters', api: 'Inbound adapter · API', 'data-model': 'Outbound adapter · data model' };
    dd.hexLayer = HEXL[ddRaw.kind] || 'Design intent';

    // ---- answers: what the knowledge base returns (tools, text, a picture, sources, version)
    var go = function (o) { return set(Object.assign({ snack: null }, o)); };
    var njDefs = [ ['d1', 'Day 1', 'Collect your laptop and badge'], ['d2', 'Day 1', 'Sign in to AIToolbox: your accounts come from the directory'], ['d3', 'Day 1', 'Meet your buddy'],
      ['w1', 'Week 1', 'Read How we work: Modules, Work items, Checkpoints'], ['w2', 'Week 1', 'Take the AIToolbox tour (8 min)'], ['w3', 'Week 1', 'Clone client-referential and run it locally'], ['w4', 'Week 1', 'Reserve a staging environment once, with your buddy'],
      ['m1', 'Month 1', 'Ship your first pull request through Sweep'], ['m2', 'Month 1', 'Shadow a Thursday release'], ['m3', 'Month 1', 'Attend an architecture review (ARB)'], ['m4', 'Month 1', 'Improve one doc page with Propose a change'] ];
    var ANS = {
      arch_dep: { trace: [['KB', 'find · facility service → sbb.facility-service.facility-service'], ['ARCH', 'impact · 2 hops · target']], answer: 'In the target, the Facility service is called by the Credit request service and the Corporate client hub; its Facility API contract is a check in ARB 2026-14.',
        list: [['Credit request service', 'sets the facility up once the request is approved', ''], ['Corporate client hub', 'reads the facility status for the client view', ''], ['ARB 2026-14', 'T6 · detailed design still thin for the Facility API', '']],
        sources: [['ARCH', 'Inside Facility service · target', { view: 'arch', arTarget: { area: 'views', page: null, level: 'application', app: 'facility-service', pf: 'corporate', plateau: 'target', view: { enterprise: 'capmap', portfolio: 'landscape', application: 'inside' } } }], ['ARCH', 'ARB 2026-14 · in review', { view: 'arch', arTarget: { area: 'process', proc: 'reviews', page: { kind: 'arb', id: 'arb.corporate.2026-14' }, arbTab: 'asd' } }], ['DD', 'dd.cc-facility.domain', { view: 'dd', dd: 'dd.cc-facility.domain' }]], fresh: 'Architecture model · main @ 4a1b9e0 · today' },
      dd_expire: { trace: [['KB', 'find · facility active → 2 sections'], ['DD', 'get · dd.cc-facility.domain § Facility lifecycle']], answer: 'A facility becomes active only when the contract is signed, its limit is booked in limit-service and collateral covers at least 100 % of the amount.',
        chain: [['Approved', 'by the decision'], ['Contracted', 'agreement signed'], ['Active', 'limit booked, collateral ≥ 100 %']],
        sources: [['DD', 'dd.cc-facility.domain § Facility lifecycle', { view: 'dd', dd: 'dd.cc-facility.domain' }], ['ADR', 'Split the credit origination monolith by business capability', { view: 'arch', arTarget: { area: 'elements', page: { kind: 'element', id: 'adr.corporate.split-credit-monolith' } } }]], fresh: 'facility-service @ 3e91c0a · 22 Oct · authored' },
      ops_hotfix: { trace: [['KB', 'find · hotfix Thursday → release/hotfix.md, release/weekly-train.md']], answer: 'Thursday is a production day, so a hotfix joins the 19:00 window. Only an S1 goes out sooner, within 2 hours.',
        steps: [['Branch from the tag', 'hotfix/… from v4.6.0'], ['Sweep checks pass', 'review summary, tests, quality gate'], ['Release manager approves', 'in Environments, inside the window'], ['Production', '19:00 with the train, or within 2 h for an S1'], ['Note in What’s new', 'one line, linked to the ticket']],
        sources: [['OPS', 'release/hotfix.md', { view: 'ops', opsTab: 'release' }], ['OPS', 'release/weekly-train.md', { view: 'ops', opsTab: 'release' }]], fresh: 'Operations doc site · reviewed 12 Oct by the Release team' },
      ai_skill: { trace: [['KB', 'find · write a skill, Jira → 2 wiki pages'], ['CAT', 'Catalog · Create Jira ticket']], answer: 'Write it in the Catalog with Create Jira ticket among its tools. That tool changes something, so the skill asks before it creates a ticket, and publishing it to everyone goes through a review.',
        steps: [['Catalog › New skill', 'name, one line, instructions'], ['Pick Create Jira ticket', 'the skill now asks first'], ['Test', 'automatic checks and one try'], ['Submit', 'your team at once, everyone after review']],
        sources: [['AI', 'AI wiki › Publish a skill to everyone', { view: 'ai', wiki: 'p1' }], ['AI', 'AI wiki › Turn a long prompt into a skill', { view: 'ai', wiki: 't4' }]], fresh: 'AI wiki · updated 27 Oct' },
      ai_data: { trace: [['KB', 'find · data rules → AI wiki › Data you may share']], answer: 'Code, logs, run results and internal docs are fine. Never paste secrets, tokens or client data: names, accounts, amounts. Mask them first.',
        list: [['Allowed', 'code, logs, run results, internal docs', ''], ['Mask first', 'client names, account numbers, amounts', ''], ['Never', 'passwords, tokens, keys', '']],
        sources: [['AI', 'AI wiki › Data you may share with the assistant', { view: 'ai', wiki: 'p4' }]], fresh: 'AI wiki · reviewed by the Security team on 15 Oct' },
      new_week: { trace: [['KB', 'get · onboarding/week-1.md'], ['DIR', 'directory · your access and your team']], answer: 'Your first week has four things after day 1.', week: true,
        sources: [['NEW', 'onboarding/week-1.md', { view: 'new' }], ['NEW', 'onboarding/access.md', { view: 'new' }]], fresh: 'Onboarding doc site · updated 20 Oct' },
      org_oncall: { trace: [['KB', 'find · on call Facility management → organization/facility.md'], ['OPS', 'on-call schedule · this week']], answer: 'Lucas Bernard is on call for Facility management until Monday 09:00, then Hugo Martin. For an S1, page through the incident channel; the runbook is Rollback procedure for facility-management.',
        sources: [['OPS', 'organization/facility.md', { view: 'ops', opsTab: 'org' }], ['OPS', 'incidents/rollback-facility-management.md', { view: 'ops', opsTab: 'inc' }]], fresh: 'Operations doc site and on-call schedule · today' },
      arch_inferred: { trace: [['KB', 'find · Collateral management → sbb.collateral-management.collateral-management'], ['ARCH', 'get · origin, owner, plateaus']], answer: 'Collateral management is owned by team-credit. Its design was documented from the code; no architect has authored it yet. It stays in the target and is called by the Facility service for collateral-service.',
        prov: 'Origin inferred, confidence 0.7, extracted 21 Oct. Treat it as a draft; ask Lucas Bernard before relying on it.',
        sources: [['ARCH', 'Collateral management · documented from code', { view: 'arch', arTarget: { area: 'elements', page: { kind: 'element', id: 'sbb.collateral-management.collateral-management' } } }]], fresh: 'Architecture model · main @ 4a1b9e0 · today' },
      arch_why: { trace: [['KB', 'find · nightly exports → adr.risk.lakehouse'], ['ARCH', 'get · data warehouse, plateaus']], answer: 'The data warehouse sees facilities a day late and the nightly export fails about twice a month. The lakehouse decision replaces it with governed data products fed by business events in the target.',
        list: [['Exposure visible within a minute', 'facility events on the event backbone', ''], ['Data warehouse retired in the target', 'work package Lakehouse data platform', ''], ['Versioned contracts', 'AsyncAPI, checked on every build', '']],
        sources: [['ADR', 'A lakehouse with governed data products replaces the data warehouse', { view: 'arch', arTarget: { area: 'elements', page: { kind: 'element', id: 'adr.risk.lakehouse' } } }], ['ARCH', 'Gap · Risk & finance', { view: 'arch', arTarget: { area: 'views', page: null, level: 'portfolio', pf: 'risk', plateau: 'target', view: { enterprise: 'capmap', portfolio: 'gap', application: 'factsheet' } } }]], fresh: 'Architecture model · main @ 4a1b9e0 · today' },
      arb_ready: { trace: [['KB', 'get · arb.corporate.2026-14'], ['ARCH', 'validate · checks and ASD sections']], answer: '', arbq: true,
        sources: [['ARCH', 'ARB 2026-14 · Facility service out of the monolith', { view: 'arch', arTarget: { area: 'process', proc: 'reviews', page: { kind: 'arb', id: 'arb.corporate.2026-14' }, arbTab: 'checks' } }]], fresh: 'Validation of main @ 4a1b9e0 · today' },
      glossary: { trace: [['GLO', 'find · glossary, domain reference §5']], answer: 'Here are the words people use most in your first weeks.',
        list: [['Module', 'part of an application, one repository or a part of one', ''], ['Work item', 'the unit of work a Checkpoint decides on', ''], ['Checkpoint', 'a decision people take: a review, an approval', ''], ['Plateau', 'a stable state of the architecture: baseline, target', '']],
        sources: [['GLO', 'domain reference § 5 · Vocabulary', { view: 'new' }]], fresh: 'Glossary · domain reference · 22 Oct' },
      default: { trace: [['KB', 'find · 7 sources']], answer: 'I did not find a precise answer. The closest pages are below; you can also ask about an application, a procedure, or your first week.',
        sources: [['OPS', 'release/weekly-train.md', { view: 'ops', opsTab: 'release' }], ['ARCH', 'Meridian Bank · application landscape', { view: 'arch', arTarget: { area: 'views', page: null, level: 'portfolio', pf: 'corporate', view: { enterprise: 'capmap', portfolio: 'landscape', application: 'factsheet' } } }], ['NEW', 'onboarding/week-1.md', { view: 'new' }]], fresh: 'Knowledge base · today 08:41' }
    };
    var srcTo = function (o) { return o; };
    var answerOf = function (tn) {
      var a = ANS[tn.q] || ANS['default'], nd = null;
      if (a.arbq) { a = Object.assign({}, a, { answer: 'ARB 2026-14 (Facility service out of the credit origination monolith) is in review for the board of 12 November. What is left:', list: [['T6 · detailed design', 'thin for the Facility API', ''], ['Reviewer · Security', 'decision pending', ''], ['Updated since the review', 'change/WP-FAC-02 @ 7c1e9a0 → re-submit', '']] }); }
      var list = (a.list || []).map(function (r) { return { t: r[0], sub: r[1], cls: '', mark: '' }; });
      if (a.week) list = njDefs.filter(function (d) { return d[1] === 'Week 1'; }).map(function (d) { var on = !!s.nj[d[0]]; return { t: d[2], sub: on ? 'Done' : 'To do', cls: on ? 'on' : '', mark: on ? '✓' : '' }; });
      return { q: tn.text, n: a.trace.length + (a.trace.length > 1 ? ' calls' : ' call'), trace: a.trace.map(function (x) { return Object.assign(tileOf(x[0]), { label: x[1] }); }), answer: a.answer,
        hasChain: !!a.chain, chain: a.chain ? mk(a.chain) : [], hasSteps: !!a.steps, steps: (a.steps || []).map(function (c, i) { return { n: i + 1, t: c[0], sub: c[1] }; }),
        hasList: list.length > 0, list: list, hasProv: !!a.prov, prov: a.prov || '',
        sources: a.sources.map(function (x) { return Object.assign(tileOf(x[0]), { label: x[1], go: go(srcTo(x[2])) }); }), fresh: a.fresh };
    };
    var turns = s.turns.map(answerOf);
    var SUGG = {
      home: [['ops_hotfix', 'How do I ship a hotfix on Thursday?', 'OPS'], ['arch_dep', 'What depends on the Facility service?', 'ARCH'], ['arch_why', 'Why do we replace the nightly exports?', 'ARCH'], ['ai_skill', 'How do I write a skill that creates Jira tickets?', 'AI'], ['new_week', 'What should I do in my first week?', 'NEW']],
      arch: [['arb_ready', 'Is the facility ARB ready for the board?', 'ARCH'], ['arch_dep', 'What depends on the Facility service?', 'ARCH'], ['arch_why', 'Why do we replace the nightly exports?', 'ARCH']],
      dd: [['dd_expire', 'When does a facility become active?', 'DD'], ['arch_dep', 'What depends on the Facility service?', 'ARCH']],
      ai: [['ai_skill', 'How do I write a skill that creates Jira tickets?', 'AI'], ['ai_data', 'Which data can I paste into the assistant?', 'AI']],
      ops: [['ops_hotfix', 'How do I ship a hotfix on Thursday?', 'OPS'], ['org_oncall', 'Who is on call for Facility management this week?', 'OPS']],
      new: [['new_week', 'What should I do in my first week?', 'NEW'], ['glossary', 'What do Module and Checkpoint mean?', 'GLO']],
      kb: [['arch_dep', 'What depends on the Facility service?', 'ARCH']] };
    var suggOf = function (v) { return (SUGG[v] || SUGG.home).map(function (g) { return Object.assign(tileOf(g[2]), { t: g[1], go: ask(g[0], g[1]) }); }); };

    // ---- home
    var WIKI = [
      { id: 'n1', cat: 'news', t: 'The assistant now reads the architecture model', sum: 'Ask what depends on an application, who owns it, what changes in the target.', by: 'Platform team', date: '28 Oct', edits: '1 edit',
        secs: [ { p: 'Ask about any application in plain words: what depends on it, who owns it, what changes in the target plateau. Answers cite the element ids and the model version.' }, { h: 'Try it', b: ['What depends on the Facility service?', 'Is the facility ARB ready for the board?'] } ], rel: ['t2'] },
      { id: 'n2', cat: 'news', t: 'Sweep review summaries cite the lines they talk about', sum: 'Each finding now links to the line in the pull request.', by: 'Sweep team', date: '21 Oct', edits: '2 edits',
        secs: [ { p: 'Review summaries now link every finding to the line in the pull request, and say which pipeline log it comes from.' }, { tip: 'Rate a summary with the thumbs: the ratings tune the next model update.' } ], rel: ['t1'] },
      { id: 'n3', cat: 'news', t: 'The Catalog is open: publish your own skills', sum: 'Skills for you or your team go live at once; for everyone after a review.', by: 'Platform team', date: '14 Oct', edits: '3 edits',
        secs: [ { p: 'Anyone can now write a skill in the Catalog and use it in the assistant and in Sweep. Skills for you or your team go live at once; skills for everyone are reviewed first.' } ], rel: ['p1', 't4'] },
      { id: 't1', cat: 'tip', t: 'Ask from the page you are on', sum: 'The assistant gets the page as context: “why did this fail?” is enough.', by: 'Marta Kowalski', date: '27 Oct', edits: '4 edits by 3 people',
        secs: [ { p: 'The assistant knows the page you ask from: the run, the environment or the document. Short questions work.' }, { h: 'Instead of', b: ['Pasting the logs of run 4821 and asking what went wrong', 'Explaining which environment you mean'] }, { tip: 'Open the run, then type “why did this fail?” in the search bar and press Ask.' } ], rel: ['t2'] },
      { id: 't2', cat: 'tip', t: 'Ask for the source, then check its date', sum: 'Every answer lists where it comes from and how fresh it is.', by: 'Sami Ben Ali', date: '24 Oct', edits: '2 edits',
        secs: [ { p: 'Answers list their sources and the version they come from. Open the source when the answer decides something.' }, { b: ['A draft source is flagged: ask its owner before you rely on it.', 'An old date means the page may be out of date: say so in Feedback.'] } ], rel: ['p3'] },
      { id: 't3', cat: 'tip', t: 'Keep secrets and client data out of prompts', sum: 'Mask names, accounts and amounts before you paste anything.', by: 'Security team', date: '15 Oct', edits: '1 edit',
        secs: [ { p: 'The assistant runs inside the company, but prompts are logged. Mask client data and never paste credentials.' }, { tip: 'Replace a client name with “Client A” and an amount with “X EUR”: the answer is just as good.' } ], rel: ['p4'] },
      { id: 't4', cat: 'tip', t: 'Turn a long prompt into a skill', sum: 'If you paste the same instructions twice, make them a skill.', by: 'Lucas Bernard', date: '20 Oct', edits: '2 edits',
        secs: [ { p: 'A prompt you reuse belongs in a skill: write the instructions once, pick the tools it may use, and call it by name.' }, { tip: 'Start with “just me”, use it for a week, then share it with your team.' } ], rel: ['p1'] },
      { id: 'p1', cat: 'proc', t: 'Publish a skill to everyone', sum: 'Write, test, submit, review, published.', by: 'Platform team', date: '27 Oct', edits: '5 edits',
        secs: [ { p: 'Skills for everyone are reviewed by a platform admin.' }, { h: 'Steps', steps: ['In the Catalog, choose New skill and write the instructions.', 'Pick the tools it may use; tools that change something make it ask first.', 'Test it: the checks and one try in the assistant.', 'Submit it to everyone and add a note for the reviewer.', 'Answer the reviewer in the skill’s discussion.'] } ], rel: ['t4', 'n3'] },
      { id: 'p2', cat: 'proc', t: 'Request a new MCP server', sum: 'For a tool the assistant cannot reach yet.', by: 'Platform team', date: '18 Oct', edits: '1 edit',
        secs: [ { h: 'Steps', steps: ['Check the Catalog: it may exist already.', 'Open an idea in Community › Ideas with what it should read or do.', 'The platform team answers within a week and plans it with you.'] } ], rel: ['p1'] },
      { id: 'p3', cat: 'proc', t: 'Report a wrong answer', sum: 'Thumbs down, say why, the source owner is told.', by: 'Platform team', date: '16 Oct', edits: '2 edits',
        secs: [ { h: 'Steps', steps: ['Press thumbs down under the answer.', 'Say what was wrong in one line.', 'The owner of the source gets it in Community › Feedback.'] } ], rel: ['t2'] },
      { id: 'p4', cat: 'proc', t: 'Data you may share with the assistant', sum: 'What is fine, what to mask, what never to paste.', by: 'Security team', date: '15 Oct', edits: '3 edits',
        secs: [ { h: 'Fine', b: ['Code, logs and run results', 'Internal documentation and procedures'] }, { h: 'Mask first', b: ['Client names, account numbers, amounts'] }, { h: 'Never', b: ['Passwords, tokens, private keys'] } ], rel: ['t3'] }
    ];
    var spaces = { arch: ['Architecture', 'Meridian Bank: the elements, the views by steering level, the changes and the reviews.', '4 portfolios · 31 applications · 227 elements · 8 changes'], ai: ['AI wiki', 'Tips, procedures and news about our AI tools, written by the community.', WIKI.length + ' pages · news from 28 Oct'], ops: ['Operations', 'Release train, organization and on-call, incidents, the design system.', 'Release · Organization · Incidents · Design system'], new: ['New joiner', 'The first day, week and month, the people to meet and the access to ask for.', '11 steps'] };
    Object.keys(spaces).forEach(function (k) { V['sp_' + k] = true; V['spT_' + k] = spaces[k][0]; V['spD_' + k] = spaces[k][1]; V['spM_' + k] = spaces[k][2]; V['go_' + k] = go(k === 'ai' ? { view: 'ai', wiki: null } : k === 'arch' ? { view: 'arch', arTarget: { area: 'elements', page: null } } : { view: k }); });
    var recent = [ ['ARCH', 'Meridian Bank · ARB 2026-14 Facility service out of the monolith, updated', 'yesterday', { view: 'arch', arTarget: { area: 'process', proc: 'reviews', page: { kind: 'arb', id: 'arb.corporate.2026-14' }, arbTab: 'asd' } }], ['OPS', 'Weekly release train: go / no-go moved to 16:00', '12 Oct', { view: 'ops', opsTab: 'release' }], ['AI', 'News: the assistant now reads the architecture model', '28 Oct', { view: 'ai', wiki: 'n1' }], ['DD', 'facility-service · Domain: facility lifecycle', '22 Oct', { view: 'dd', dd: 'dd.cc-facility.domain' }] ].map(function (r) { return Object.assign(tileOf(r[0]), { t: r[1], when: r[2], go: go(r[3]) }); });

    // ---- AI, operations, new joiner
    var aiOpen = function (id) { return go({ view: 'ai', wiki: id }); };
    var wikiNav = [ ['news', 'News'], ['tip', 'Tips'], ['proc', 'Procedures'] ].map(function (c) { return { label: c[1], pages: WIKI.filter(function (w) { return w.cat === c[0]; }).map(function (w) { return { t: w.t, cur: s.wiki === w.id ? 'page' : 'false', open: aiOpen(w.id) }; }) }; });
    var wRaw = WIKI.filter(function (w) { return w.id === s.wiki; })[0] || null;
    var CATN = { news: 'News', tip: 'Tip', proc: 'Procedure' };
    var wp = wRaw ? { title: wRaw.t, ctx: CATN[wRaw.cat] + ' · ' + wRaw.by + ' · ' + (wRaw.cat === 'news' ? wRaw.date : 'updated ' + wRaw.date), by: wRaw.by, edits: wRaw.edits,
      secs: wRaw.secs.map(function (x) { return { hasH: !!x.h, h: x.h || '', hasP: !!x.p, p: x.p || '', hasB: !!x.b, b: x.b || [], hasSteps: !!x.steps, steps: (x.steps || []).map(function (t, i) { return { n: i + 1, t: t }; }), hasTip: !!x.tip, tip: x.tip || '' }; }),
      related: (wRaw.rel || []).map(function (id) { var r = WIKI.filter(function (w) { return w.id === id; })[0]; return { t: r.t, open: aiOpen(id) }; }) } : { title: '', ctx: '', by: '', edits: '', secs: [], related: [] };
    var byCat = function (c) { return WIKI.filter(function (w) { return w.cat === c; }).map(function (w) { return { t: w.t, sum: w.sum, date: w.date, n: (w.secs.filter(function (x) { return x.steps; })[0] || { steps: [] }).steps.length, open: aiOpen(w.id) }; }); };
    var OTABS = [['release', 'Release'], ['org', 'Organization'], ['inc', 'Incidents'], ['ds', 'Design system']];
    var opsTab = s.opsTab;
    var opsTabs = OTABS.map(function (t) { var on = opsTab === t[0]; return { label: t[1], on: on, cls: on ? 'tab-on' : '', pick: set({ opsTab: t[0] }) }; });
    var C = function (t, sub, cls) { return { has: true, t: t, sub: sub, cls: cls || '' }; }, E = { has: false };
    var lanes = [ { name: 'Teams', cells: [C('Merge to main', 'by 18:00'), E, C('Verify on staging', 'owners sign off'), E, C('Hypercare', 'watch dashboards')] }, { name: 'Release manager', cells: [E, C('Code freeze', '12:00 · cut release/4.6'), C('Go / no-go', '16:00', 'gate'), E, C('Release notes', 'in What’s new')] }, { name: 'Platform', cells: [E, C('Deploy to staging', 'after the freeze'), E, C('Production', '19:00 – 21:00', 'prod'), E] } ];
    var njTotal = njDefs.length, njDone = njDefs.filter(function (d) { return s.nj[d[0]]; }).length;
    var njCols = ['Day 1', 'Week 1', 'Month 1'].map(function (lbl) { return { label: lbl, items: njDefs.filter(function (d) { return d[1] === lbl; }).map(function (d) { var on = !!s.nj[d[0]]; return { t: d[2], on: on, cls: on ? 'done' : '', toggle: set(function () { var n = Object.assign({}, s.nj); n[d[0]] = !on; return { nj: n }; }) }; }) }; });

    // ---- lab chrome
    var VIEW_HDR = { home: ['Docs', 'Architecture, AI wiki, procedures and onboarding · one knowledge base'], arch: V.archHdr, dd: ['Docs · Detailed design', dd.title], ai: ['Docs · AI wiki', wRaw ? wRaw.t : 'Tips, procedures and news'], ops: ['Docs · Operations', { release: 'Weekly release train', org: 'Portfolios and teams', inc: 'Incidents', ds: 'Design system' }[opsTab]], new: ['Docs · New joiner', 'Week 1 · ' + njDone + ' of ' + njTotal + ' done'], kb: ['Administration · Core', 'Knowledge base · 7 sources'] };
    var hdr = VIEW_HDR[s.view] || VIEW_HDR.home;
    var SCREENS = [['home', 'Docs home'], ['arch', 'Architecture'], ['dd', 'Detailed design'], ['ai', 'AI wiki'], ['ops', 'Operations'], ['new', 'New joiner'], ['kb', 'Admin · Knowledge base']];
    var screenChips = SCREENS.map(function (x) { var on = s.view === x[0]; return { label: x[1], on: on, style: on ? ON : '', pick: set({ view: x[0], snack: null }) }; });
    var variantChips = [['A', 'A · Spaces (adopted)'], ['B', 'B · Application lens'], ['C', 'C · Ask first']].map(function (x) { var on = s.variant === x[0]; return { label: x[1], on: on, style: on ? ON : '', pick: set({ variant: x[0], view: 'home', snack: null, asOpen: false, turns: [], arch: x[0] === 'B' ? Object.assign({}, A0, PAGES, { trail: [], area: 'views', view: 'application', mode: 'target', el: 'fac' }) : A0 }) }; });
    var ctxName = { home: 'Docs', arch: V.archCtx, dd: dd.title, ai: wRaw ? wRaw.t : 'AI wiki', ops: 'Operations', new: 'New joiner', kb: 'Knowledge base' }[s.view] || 'Docs';
    var askPh = s.variant === 'C' ? 'Ask a question, or search the docs…' : 'Ask the docs, or search…';

    return Object.assign(sim, V, {
      variantChips: variantChips, screenChips: screenChips, hdrFeature: hdr[0], hdrSummary: hdr[1], live: s.live || '',
      railDocs: s.view !== 'kb', railAdm: s.view === 'kb', hasSnack: !!s.snack, snack: s.snack || '', closeSnack: set({ snack: null }),
      homeA: s.view === 'home' && s.variant === 'A', homeB: s.view === 'home' && s.variant === 'B', homeC: s.view === 'home' && s.variant === 'C',
      vArch: s.view === 'arch', vDd: s.view === 'dd', vAi: s.view === 'ai', vOps: s.view === 'ops', vNew: s.view === 'new', vKb: s.view === 'kb',
      hdrAsk: function (e) { if (e && e.preventDefault) e.preventDefault(); if ((s.draft || '').trim()) sendDraft(); else self.setState({ asOpen: !cInline }); },
      goHome: go({ view: 'home' }), goKb: go({ view: 'kb' }), openPane: set({ asOpen: true }), asClose: set({ asOpen: false }), asClear: set({ turns: [] }),
      paneOn: !!s.asOpen && !cInline, mainCls: s.asOpen && !cInline ? 'pane-on' : '', asEmpty: turns.length === 0, asSugg: suggOf(s.view), asCtx: ctxName, turns: turns,
      draft: s.draft, onDraft: function (e) { self.setState({ draft: val(e) }); }, onKey: function (e) { if (e && e.key === 'Enter' && !e.shiftKey) { if (e.preventDefault) e.preventDefault(); sendDraft(); } }, send: function (e) { if (e && e.preventDefault) e.preventDefault(); sendDraft(); }, askPh: askPh,
      cEmpty: turns.length === 0, cHasTurns: turns.length > 0, cSugg: suggOf('home'), recent: recent,
      dd: dd, ddAsk: ask('dd_expire', 'How does a reservation expire?'), ddSite: set({ snack: 'Opens the page on the Environments doc site (Zensical), with Open in Architecture at the top.' }), ddEdit: set({ snack: 'Opens a pull request on ' + dd.path + '. The change is validated before review.' }),
      wikiAtHome: !wRaw, wikiOnPage: !!wRaw, wikiCount: WIKI.length, wikiNav: wikiNav, wp: wp, wikiNews: byCat('news'), wikiTips: byCat('tip'), wikiProcs: byCat('proc'), wikiHome: set({ wiki: null }), wikiNew: set({ snack: 'Opens the editor for a new page. A champion reviews it before it appears.' }), wikiEdit: set({ snack: 'Opens the page in the editor. Your change appears once a champion has reviewed it.' }),
      opsTabs: opsTabs, oRelease: opsTab === 'release', oOrg: opsTab === 'org', oInc: opsTab === 'inc', oDs: opsTab === 'ds',
      days: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], lanes: lanes, hotfix: mk([['Branch from the tag', 'hotfix/…'], ['Sweep checks', 'must pass'], ['Approval', 'release manager'], ['Production', 'next window, or 2 h for S1']]), askHotfix: ask('ops_hotfix', 'How do I ship a hotfix on Thursday?'),
      org: [ { name: 'Delivery platform', teams: [ { name: 'Environments', lead: 'Yann Dupont', oncall: 'Sami Ben Ali' }, { name: 'Sweep', lead: 'Aurélien Heux', oncall: 'Inès Moreau' }, { name: 'Docs', lead: 'Emma Laurent', oncall: '—' } ] }, { name: 'Request', teams: [ { name: 'Request intake', lead: 'Karim Ouali', oncall: 'Priya Sharma' }, { name: 'Request workflow', lead: 'Tom Girard', oncall: 'Tom Girard' } ] }, { name: 'Client', teams: [ { name: 'Client referential', lead: 'Marta Kowalski', oncall: 'Léo Martin' }, { name: 'Client onboarding', lead: 'your manager', oncall: '—' } ] }, { name: 'Facility', teams: [ { name: 'Facility management', lead: 'Lucas Bernard', oncall: 'Lucas Bernard' }, { name: 'Facility exports', lead: 'Nadia Haddad', oncall: 'Hugo Martin from Monday' } ] } ],
      sev: [ { l: 'S1', a: '15 min, around the clock', b: 'On call and the incident manager', c: 'Status page and Teams, every 30 min' }, { l: 'S2', a: '1 h, working hours', b: 'On call', c: 'Teams channel' }, { l: 'S3', a: 'Next working day', b: 'The owning team', c: 'The ticket' }, { l: 'S4', a: 'Backlog', b: '—', c: '—' } ],
      runbooks: [ ['Rollback procedure for facility-management', 'Facility team · updated 3 days ago', 'org_oncall', 'Who is on call for Facility management this week?'], ['Facility exports are failing', 'Facility team · updated 21 Oct', 'arch_inferred', 'Who owns the Facility exports design?'], ['Staging is down', 'Environments · updated 8 Oct', 'default', 'Staging is down, what do I do?'] ].map(function (r) { return { t: r[0], m: r[1], ask: ask(r[2], r[3]) }; }),
      openDs: set({ snack: 'Opens the AIToolbox design system.' }),
      njCols: njCols, njDone: njDone, njTotal: njTotal, njPct: Math.round(njDone / njTotal * 100),
      people: [ { ini: 'B', bg: '#9CF1F0', name: 'Your buddy', role: 'Named by your team lead on day 1' }, { ini: 'M', bg: '#E3DFFF', name: 'Your manager', role: 'Weekly one-to-one' }, { ini: 'PT', bg: '#FFF2B3', name: 'Platform team', role: 'AIToolbox, Sweep, the assistant' }, { ini: 'RT', bg: '#C3F4DC', name: 'Release team', role: 'Thursday release, 19:00' } ],
      access: [ { t: 'Git', st: 'From the directory', cls: 'ok' }, { t: 'Jira', st: 'From the directory', cls: 'ok' }, { t: 'DevOps platform', st: 'From the directory', cls: 'ok' }, { t: 'Production logs', st: 'Ask your manager', cls: 'wn' } ],
      glossary: [ { t: 'Module', d: 'part of an application' }, { t: 'Work item', d: 'what a Checkpoint decides on' }, { t: 'Checkpoint', d: 'a decision people take' }, { t: 'Plateau', d: 'a stable state of the architecture' } ], askWords: ask('glossary', 'What do Module and Checkpoint mean?'),
      kbRows: [ ['ARCH', 'Architecture model', 'Architecture repository · LikeC4, Markdown', 'one document per element, plus graph tools', '227 elements · 20 views', 'today 08:41 · main @ 4a1b9e0', 'Indexed', 'ok'], ['DD', 'Detailed design', '41 module fragments · application repositories', 'one document per section', '1,214 sections', 'today 07:55', '2 drafts', 'wn'], ['API', 'Contracts', 'OpenAPI, AsyncAPI', 'one document per operation', '612 operations', 'today 07:55', 'Indexed', 'ok'], ['AI', 'AI wiki', 'Community wiki · tips, procedures, news', 'one document per section', '11 pages', '28 Oct', 'Indexed', 'ok'], ['OPS', 'Operational procedures', 'Doc site · release, organization, incidents, design system', 'one document per section', '214 sections', '12 Oct', 'Indexed', 'ok'], ['NEW', 'New joiner', 'Doc site · onboarding, plus the directory', 'one document per section', '58 sections', '20 Oct', 'Indexed', 'ok'], ['GLO', 'Glossary', 'Domain reference § 5', 'one document per term, with synonyms', '140 terms', '22 Oct', 'Indexed', 'ok'] ].map(function (r) { return Object.assign(tileOf(r[0]), { name: r[1], from: r[2], as: r[3], n: r[4], when: r[5], st: r[6], cls: r[7] }); }),
      kbTools: [ { n: 'kb.find', d: 'search by meaning and by id, filtered by source, application, plateau' }, { n: 'kb.get', d: 'one element or one section, with its path and version' }, { n: 'arch.neighbours', d: 'what an element uses and what uses it' }, { n: 'arch.impact', d: 'what a change touches, across applications' }, { n: 'arch.path_to_requirement', d: 'why an element exists' } ],
      kbAdd: set({ snack: 'Sources are added from a connector: a Git repository, a doc site or a directory.' }), kbEval: set({ snack: 'Opens the 52 evaluation questions and their expected sources.' })
    });
  }
}
'''

LOGIC = LOGIC.replace('/*ARCHJS*/', ARC.ARCH_JS)
HDR = S.header(False)
HDR = HDR.replace('<input id="sh-q" type="text" placeholder="Search, or ask the assistant…"', '<input id="sh-q" type="text" placeholder="Search, or ask the docs…" value="{{draft}}" onChange="{{onDraft}}" onKeyDown="{{onKey}}"', 1)
HDR = HDR.replace('<button type="button" class="ui" style="display: inline-flex; align-items: center; gap: 6px; height: 32px;', '<button type="button" class="ui" onClick="{{hdrAsk}}" style="display: inline-flex; align-items: center; gap: 6px; height: 32px;', 1)
HDR = HDR.replace('class="ib hdr-asst" aria-label="Open assistant"', 'class="ib hdr-asst" aria-label="Open assistant" onClick="{{openPane}}"', 1).replace('class="ib hdr-sbtn" aria-label="Search"', 'class="ib hdr-sbtn" aria-label="Search" onClick="{{openPane}}"', 1)
assert '{{hdrAsk}}' in HDR and '{{onDraft}}' in HDR
views = HOME_A + HOME_B + HOME_C + ARCH + DDV + AIV + OPSV + NEWV + KBV
body = (BODY.replace('SIMBAR', S.sim_bar()).replace('SIMOPEN', S.sim_open('sim-host-dl', 'height: {{simFrameH}}px')).replace('SIMCLOSE', S.SIM_CLOSE)
        .replace('HEADER', HDR).replace('RAIL_DOCS', N.rail(N.LIGHT, 'docs', catalog=True)).replace('RAIL_ADM', N.rail(N.LIGHT, 'admin', catalog=True))
        .replace('NAVBAR', S.navbar(N.LIGHT, 'docs')).replace('@@VIEWS@@', views).replace('@@PANE@@', PANE))
logic = LOGIC.replace('/*SIMJS*/', S.SIM_JS).replace('__DG__', D.js_data())
out = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>Docs lab, several sources, one knowledge base</title>\n<script src="./support.js"></script>\n</head>\n<body>\n<x-dc>\n<helmet>\n'
       '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&amp;family=Open+Sans:wght@400;600;700&amp;display=swap">\n'
       '<style>\n' + S.CSS + '\n' + S.SIM_CSS + S.ADMIN_CSS + CSS_LAB + AS_CSS + CSS_DL + ARC.CSS + '</style>\n</helmet>\n' + body + '\n</x-dc>\n'
       '<script type="text/x-dc" data-dc-script data-props=\'{"$preview":{"width":1440,"height":1400}}\'>' + logic + '</script>\n</body>\n</html>\n')
for t in ['sc-if', 'sc-for']:
    assert len(re.findall(rf'<{t}\b', out)) == len(re.findall(rf'</{t}>', out)), t
for ph in ['SIMBAR', 'HEADER', 'NAVBAR', 'SIMOPEN', 'RAIL_DOCS', 'RAIL_ADM', '@@', '__DG__']:
    assert ph not in out, ph
import markup_check
_errs = markup_check.check(out)
assert not _errs, '\n'.join(_errs[:10])
open(dst, 'w', encoding='utf-8').write(out); print(len(out))
