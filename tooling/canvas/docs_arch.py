"""Architecture space of the Docs lab: the Corporate credit platform as a practical example, drawn with the AIToolbox
ArchiMate notation (archimate_ds) and read like LikeC4 views.

Three areas, one navigation pattern (area tabs, then a side list):
- Catalogue: the building blocks of the model by ArchiMate layer; an element page with its relationships, plateaus,
  detailed design, decisions, review and LikeC4 source.
- Views: the LikeC4 views by TOGAF ADM phase, on each plateau and as gaps between two plateaus; select an element to
  see its relationships, open it in the catalogue.
- Process: how a change goes through the architecture process (decide · design · review · deliver), one change per work
  package, with the decisions (ADR), reviews (ARB, ASD) and the roadmap (plateaus, work packages, gaps).
Markup, CSS and the JS logic (ARCH_JS, injected into docs_lab_build.LOGIC)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shell as S, docs_lab_data as D, archimate_ds as AX

def mkey(k, m):
    return f'lcv_{k}_{m.replace("-", "_")}'

def status(obj, p=''):
    return f'<span class="status st-{{{{{obj}.{p}st}}}}"><span class="tile" aria-hidden="true">{{{{{obj}.{p}g}}}}</span>{{{{{obj}.{p}w}}}}</span>'

def table(head, rows_key, alias, count, cells, cls=''):
    th = ''.join(f'<th class="th">{h}</th>' for h in head)
    return (f'<div class="card" style="padding: 0; overflow: hidden"><div class="ad-tscroll"><table class="ad-tbl {cls}" style="width: 100%; border-collapse: collapse">'
            f'<thead><tr>{th}</tr></thead><tbody><sc-for list="{{{{{rows_key}}}}}" as="{alias}" hint-placeholder-count="{count}"><tr class="rw">{cells}</tr></sc-for></tbody></table></div></div>')

TILE = '<span class="ax-tile ax-l-{{%s.layer}}" aria-hidden="true"><i class="axg axg-{{%s.type}}"></i></span>'
TILE_LG = '<span class="ax-tile lg ax-l-{{%s.layer}}" aria-hidden="true"><i class="axg axg-{{%s.type}}"></i></span>'
TRACK = '<span class="ax-track" aria-label="{{%s.trackAria}}"><sc-for list="{{%s.track}}" as="t" hint-placeholder-count="3"><span class="{{t.cls}}" title="{{t.name}}">{{t.ab}}</span></sc-for></span>'
CHG = '<sc-if value="{{%s.hasChg}}" hint-placeholder-val="{{false}}"><span class="ax-change {{%s.chg}}"><b aria-hidden="true">{{%s.chgG}}</b>{{%s.chgW}}</span></sc-if>'

# ------------------------------------------------------------------ area navigation (tabs + side list)
AREA_TABS = ('<div class="row r-wrap" role="tablist" aria-label="Architecture" style="gap: 0; margin-top: -8px">'
             '<sc-for list="{{areaTabs}}" as="t" hint-placeholder-count="3"><button type="button" role="tab" class="tab {{t.cls}}" aria-selected="{{t.on}}" onClick="{{t.pick}}">{{t.label}}<span class="n">{{t.n}}</span></button></sc-for></div>')

SIDE = ('<nav class="a-nav" aria-label="{{anavLabel}}"><sc-for list="{{anav}}" as="g" hint-placeholder-count="3"><div class="a-gh">{{g.label}}</div>'
        '<sc-for list="{{g.items}}" as="i" hint-placeholder-count="3"><button type="button" class="a-item {{i.lv}}" aria-current="{{i.cur}}" onClick="{{i.pick}}">'
        '<sc-if value="{{i.hasTile}}" hint-placeholder-val="{{false}}"><span class="ax-tile ax-l-{{i.layer}}" aria-hidden="true"><i class="axg axg-{{i.type}}"></i></span></sc-if>'
        '<sc-if value="{{i.hasSwatch}}" hint-placeholder-val="{{false}}"><span class="swatch ax-l-{{i.layer}}" aria-hidden="true"></span></sc-if>'
        '<span class="a-it">{{i.label}}<sc-if value="{{i.hasSub}}" hint-placeholder-val="{{false}}"><span class="a-sub">{{i.sub}}</span></sc-if></span>'
        '<sc-if value="{{i.hasN}}" hint-placeholder-val="{{true}}"><span class="a-n">{{i.n}}</span></sc-if></button></sc-for></sc-for></nav>')

# ------------------------------------------------------------------ Views: the LikeC4 canvas
DIAGRAMS = ''.join(f'<sc-if value="{{{{{mkey(k, m)}}}}}" hint-placeholder-val="{{{{{"true" if (k, m) == ("landscape", "base") else "false"}}}}}">{D.render(k, m)[0]}</sc-if>' for k, m in D.DIAGRAM_KEYS)
LEGENDS = ''.join(f'<sc-if value="{{{{{mkey(k, m)}}}}}" hint-placeholder-val="{{{{false}}}}">{D.legend(k, m)}</sc-if>' for k, m in D.DIAGRAM_KEYS)

CARD = ('<sc-if value="{{lcHasEl}}" hint-placeholder-val="{{false}}"><div class="lc-card" role="region" aria-label="Element details">'
        '<div class="row" style="gap: 10px; align-items: flex-start">' + TILE_LG % ('lcEl', 'lcEl') +
        '<div style="flex: 1; min-width: 0"><b class="ui" style="font-size: 15px; line-height: 20px; overflow-wrap: anywhere">{{lcEl.name}}</b><div class="meta">{{lcEl.kind}}</div></div>'
        '<button type="button" class="ib" aria-label="Close the details" style="margin: -6px -6px 0 0!important" onClick="{{lcClose}}"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div>'
        + CHG % ('lcEl', 'lcEl', 'lcEl', 'lcEl') +
        '<sc-if value="{{lcEl.hasDesc}}" hint-placeholder-val="{{true}}"><p class="lc-desc">{{lcEl.desc}}</p></sc-if>'
        '<dl class="kv" style="margin: 0"><dt>Plateaus</dt><dd>' + TRACK % ('lcEl', 'lcEl') + '</dd><dt>Owner</dt><dd>{{lcEl.owner}}</dd><dt>Origin</dt><dd>{{lcEl.origin}}</dd></dl>'
        '<sc-if value="{{lcEl.hasRels}}" hint-placeholder-val="{{true}}"><div class="lc-rels"><span class="meta">In this view</span><sc-for list="{{lcEl.rels}}" as="r" hint-placeholder-count="3"><button type="button" class="lc-rel" onClick="{{r.pick}}"><span class="lc-verb">{{r.verb}}</span>' + TILE % ('r', 'r') + '<span style="flex: 1; min-width: 0; text-align: left">{{r.name}}<sc-if value="{{r.hasLabel}}" hint-placeholder-val="{{false}}"><span class="meta" style="display: block">{{r.label}}</span></sc-if></span></button></sc-for></div></sc-if>'
        '<sc-if value="{{lcEl.hasNav}}" hint-placeholder-val="{{false}}"><button type="button" class="btn f sm lc-open" onClick="{{lcEl.nav}}">{{lcEl.navLabel}}</button></sc-if><div class="row r-wrap" style="gap: 8px; padding-top: 4px"><button type="button" class="btn t sm" onClick="{{lcEl.open}}">Open in the catalogue</button><sc-if value="{{lcEl.hasDd}}" hint-placeholder-val="{{false}}"><button type="button" class="chip" style="height: 32px" onClick="{{lcEl.dd}}">Detailed design</button></sc-if></div>'
        '</div></sc-if>')

CANVAS = ('<div class="lc" data-likec4-view="{{lc.viewId}}">'
          '<div class="lc-panel"><span class="lc-mark" aria-hidden="true">LikeC4</span><sc-if value="{{lcCanBack}}" hint-placeholder-val="{{false}}"><button type="button" class="lc-pb" aria-label="Back to the previous view" title="Back" onClick="{{lcBack}}"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg></button></sc-if><nav class="lc-crumb" aria-label="View path"><span class="lc-root">corporate-credit</span><sc-for list="{{lcCrumbs}}" as="c" hint-placeholder-count="2"><span class="lc-sep" aria-hidden="true">›</span><button type="button" class="lc-cb" aria-current="{{c.cur}}" onClick="{{c.pick}}">{{c.label}}</button></sc-for></nav><code class="lc-id">{{lc.viewId}}</code></div>'
          '<div class="lc-zoom" role="group" aria-label="Zoom"><button type="button" aria-label="Zoom in" onClick="{{lcZin}}">+</button><button type="button" aria-label="Zoom out" onClick="{{lcZout}}">−</button><button type="button" aria-label="Fit to the screen" class="fit" onClick="{{lcFit}}">Fit</button></div>'
          '<div class="lc-scroll" style="height: {{lc.h}}px"><div class="lc-stage sel-{{lcSel}}" style="zoom: {{lc.zoom}}">' + DIAGRAMS + '</div></div>'
          + CARD + '</div>')

VIEW_TOOLS = ('<div class="row r-wrap" style="gap: 12px; align-items: center">'
              '<sc-if value="{{lc.hasModes}}" hint-placeholder-val="{{true}}"><div class="seg" role="group" aria-label="Plateau"><sc-for list="{{lcModes}}" as="c" hint-placeholder-count="4"><button type="button" aria-pressed="{{c.on}}" onClick="{{c.pick}}">{{c.label}}</button></sc-for></div></sc-if>'
              '<sc-if value="{{lc.isGap}}" hint-placeholder-val="{{false}}"><div class="seg" role="group" aria-label="Compare"><sc-for list="{{lcPairs}}" as="c" hint-placeholder-count="3"><button type="button" aria-pressed="{{c.on}}" onClick="{{c.pick}}">{{c.label}}</button></sc-for></div></sc-if>'
              '<span class="meta" style="flex: 1; min-width: 200px; white-space: normal">{{lc.note}}</span></div>')

VIEWS_MAIN = ('<div class="stack" style="gap: 12px; min-width: 0">'
              '<div class="v-head"><span class="a-kicker">{{lc.phase}}</span><h2 class="v-t">{{lc.title}}</h2><p class="v-sub">{{lc.sub}}</p></div>'
              + VIEW_TOOLS + CANVAS + LEGENDS +
              '<div class="row r-wrap" style="gap: 10px"><span class="meta" style="flex: 1; min-width: 220px; white-space: normal">Generated by LikeC4 from model/corporate-credit/*.c4 · main @ 4a1b9e0 · drawn with the AIToolbox ArchiMate notation. Select an element to see its relationships.</span>'
              '<button type="button" class="lnk" aria-expanded="{{lc.srcOn}}" onClick="{{lcSrc}}">{{lc.srcLabel}}</button></div>'
              '<sc-if value="{{lc.srcOn}}" hint-placeholder-val="{{false}}"><pre class="lc-src">{{lc.src}}</pre></sc-if></div>')

# ------------------------------------------------------------------ Catalogue
CAT_MAIN = ('<div class="stack" style="gap: 12px; min-width: 0">'
            '<div class="v-head"><span class="a-kicker">Catalogue</span><h2 class="v-t">{{catTitle}}</h2><p class="v-sub">{{catSub}}</p></div>'
            + table(['Element', 'Type', 'Owner', 'Plateaus', 'In the target', 'Design', 'Origin'], 'catRows', 'e', 8,
                    '<td class="td"><button type="button" class="cat-name" onClick="{{e.open}}">' + TILE % ('e', 'e') + '<span style="min-width: 0"><b class="ui">{{e.name}}</b><span class="meta mono" style="display: block">{{e.id}}</span></span></button></td>'
                    '<td class="td"><span style="font-size: 13px">{{e.kind}}</span></td><td class="td"><span style="font-size: 13px">{{e.owner}}</span></td>'
                    '<td class="td">' + TRACK % ('e', 'e') + '</td><td class="td">' + CHG % ('e', 'e', 'e', 'e') + '<sc-if value="{{e.noChg}}" hint-placeholder-val="{{false}}"><span class="meta">—</span></sc-if></td>'
                    '<td class="td"><span class="meta">{{e.design}}</span></td><td class="td"><span class="meta">{{e.origin}}</span></td>', 'cat-tbl')
            + '<span class="meta" style="white-space: normal">{{catCount}} · The catalogue is generated from the model on every build. Ask the header’s search bar what depends on an element.</span></div>')

EL_PAGE = ('<sc-if value="{{epOpen}}" hint-placeholder-val="{{false}}">'
           + S.subheader('{{pBack}}', '{{pBackLabel}}', '{{ep.name}}', ctx='{{ep.kind}} · {{ep.id}}', lead=TILE_LG % ('ep', 'ep'),
                         actions='<button type="button" class="btn x" onClick="{{epEdit}}">Propose a change</button>') +
           '<div class="ep-grid"><div class="stack" style="gap: 20px; min-width: 0">'
           '<sc-if value="{{ep.inferred}}" hint-placeholder-val="{{false}}"><div class="prov"><b>Draft</b><span>Inferred from the code (confidence 0.7, extracted 21 Oct). An architect has not authored it yet.</span></div></sc-if>'
           '<sc-if value="{{ep.hasDesc}}" hint-placeholder-val="{{true}}"><p style="margin: 0; font-size: 15px; line-height: 22px; max-width: 72ch">{{ep.desc}}</p></sc-if>'
           '<section class="ep-sec"><h3>Properties</h3><dl class="kv" style="margin: 0"><dt>Type</dt><dd>{{ep.kind}} · {{ep.layerName}} layer</dd><dt>Owner</dt><dd>{{ep.owner}}</dd>'
           '<sc-if value="{{ep.hasRealizes}}" hint-placeholder-val="{{false}}"><dt>Realizes</dt><dd class="mono">{{ep.realizes}}</dd></sc-if>'
           '<sc-if value="{{ep.hasContract}}" hint-placeholder-val="{{false}}"><dt>Contract</dt><dd class="mono" style="font-size: 12px">{{ep.contract}}</dd></sc-if>'
           '<dt>Origin</dt><dd>{{ep.origin}}</dd><dt>Plateaus</dt><dd>' + TRACK % ('ep', 'ep') + ' <span class="meta">{{ep.plText}}</span></dd></dl></section>'
           '<section class="ep-sec"><h3>Relationships</h3>' + table(['Relationship', 'Element', 'Label', 'Plateaus'], 'ep.rels', 'r', 4,
               '<td class="td"><span style="font-size: 13px; white-space: nowrap">{{r.verb}}</span></td>'
               '<td class="td"><button type="button" class="cat-name" onClick="{{r.open}}">' + TILE % ('r', 'r') + '<span>{{r.name}}</span></button></td>'
               '<td class="td"><span class="meta">{{r.label}}</span></td><td class="td"><span class="meta">{{r.pl}}</span></td>') + '</section>'
           '<section class="ep-sec"><h3>Shown in views</h3><div class="row r-wrap" style="gap: 8px"><sc-for list="{{ep.views}}" as="v" hint-placeholder-count="2"><button type="button" class="chip" style="height: 32px" onClick="{{v.open}}">{{v.label}}</button></sc-for></div></section>'
           '</div><div class="stack" style="gap: 16px; min-width: 0">'
           '<div class="panel"><b class="ui" style="font-size: 15px">Detailed design</b><sc-if value="{{ep.hasDd}}" hint-placeholder-val="{{true}}"><sc-for list="{{ep.dds}}" as="d" hint-placeholder-count="3"><button type="button" class="ddrow" onClick="{{d.open}}"><span class="srcT" style="background: #E3DFFF; color: #14085E">DD</span><span style="flex: 1">{{d.label}}</span></button></sc-for></sc-if><sc-if value="{{ep.noDd}}" hint-placeholder-val="{{false}}"><span class="meta" style="white-space: normal">{{ep.ddNote}}</span></sc-if></div>'
           '<sc-if value="{{ep.hasAdrs}}" hint-placeholder-val="{{true}}"><div class="panel"><b class="ui" style="font-size: 15px">Decisions</b><sc-for list="{{ep.adrs}}" as="a" hint-placeholder-count="2"><button type="button" class="ddrow" onClick="{{a.open}}"><span class="srcT" style="background: #CFEDFA; color: #0A5570">ADR</span><span style="flex: 1">{{a.t}}</span>' + status('a') + '</button></sc-for></div></sc-if>'
           '<sc-if value="{{ep.hasArb}}" hint-placeholder-val="{{false}}"><div class="panel"><b class="ui" style="font-size: 15px">Review</b><button type="button" class="ddrow" onClick="{{ep.openArb}}"><span class="srcT" style="background: #ECE5F4; color: #48454E">ARB</span><span style="flex: 1">{{ep.arb}}</span>' + status('epArbSt') + '</button></div></sc-if>'
           '<div class="panel"><b class="ui" style="font-size: 15px">LikeC4 source</b><span class="meta mono">{{ep.path}}</span><pre class="lc-src" style="margin: 0">{{ep.src}}</pre></div>'
           '</div></div></sc-if>')

# ------------------------------------------------------------------ Process
PROCESS_STEPS = ''.join(f'<div class="pr-step"><span class="pr-n">{i}</span><div><b class="ui">{t}</b><span class="meta" style="display: block; white-space: normal">{d}</span></div></div>' for i, t, d in [
    (1, 'Decide', 'An ADR per significant choice, in model/adr. Accepted ones are never edited.'),
    (2, 'Design', 'The ASD for the board, the detailed design in each service repository.'),
    (3, 'Review', 'The ARB: checks run on every build, reviewers decide, recorded in Git.'),
    (4, 'Deliver', 'The work package closes its gap and reaches the next plateau.')])

P_CHANGES = ('<div class="stack" style="gap: 12px; min-width: 0">'
             '<div class="v-head"><span class="a-kicker">Process</span><h2 class="v-t">Changes</h2><p class="v-sub">Each change is a work package. It goes through four steps before it reaches its plateau.</p></div>'
             '<div class="pr-steps">' + PROCESS_STEPS + '</div>'
             + table(['Change', 'Decide', 'Design', 'Review', 'Deliver'], 'chRows', 'c', 4,
                     '<td class="td"><button type="button" class="cat-name" onClick="{{c.open}}"><span><b class="ui">{{c.name}}</b><span class="meta" style="display: block; white-space: normal">{{c.scope}}</span></span></button></td>'
                     '<td class="td">' + status('c', 's1') + '</td><td class="td">' + status('c', 's2') + '</td><td class="td">' + status('c', 's3') + '</td><td class="td">' + status('c', 's4') + '</td>', 'ch-tbl')
             + '</div>')

P_DECISIONS = ('<div class="stack" style="gap: 12px; min-width: 0">'
               '<div class="v-head"><span class="a-kicker">Process · Decide</span><h2 class="v-t">Architecture decisions</h2><p class="v-sub">MADR files in model/adr. Immutable once accepted: a new decision supersedes an old one.</p></div>'
               '<div class="row"><span style="flex: 1"></span><button type="button" class="btn t" onClick="{{adrNew}}">Propose a decision</button></div>'
               + table(['Decision', 'Status', 'Plateau', 'Date'], 'adrRows', 'a', 6,
                       '<td class="td"><button type="button" class="cat-name" onClick="{{a.open}}"><span><b class="ui">{{a.t}}</b><span class="meta" style="display: block">{{a.id}} · {{a.by}}</span></span></button></td><td class="td">' + status('a') + '</td><td class="td"><span style="font-size: 13px">{{a.plateau}}</span></td><td class="td"><span class="meta">{{a.date}}</span></td>')
               + '</div>')

P_REVIEWS = ('<div class="stack" style="gap: 12px; min-width: 0">'
             '<div class="v-head"><span class="a-kicker">Process · Review</span><h2 class="v-t">Architecture reviews</h2><p class="v-sub">ARB submissions. Readiness is computed on every build: a failing blocking check or a missing ASD section blocks the board.</p></div>'
             + table(['Submission', 'Scope', 'Board', 'Readiness'], 'arbRows', 'a', 3,
                     '<td class="td"><button type="button" class="cat-name" onClick="{{a.open}}"><span><b class="ui">{{a.t}}</b><span class="meta" style="display: block">{{a.id}} · {{a.by}}</span></span></button></td><td class="td"><span style="font-size: 13px; white-space: nowrap">{{a.scope}}</span></td><td class="td"><span class="meta">{{a.board}}</span></td><td class="td">' + status('a') + '</td>')
             + '</div>')

P_ROADMAP = ('<div class="stack" style="gap: 16px; min-width: 0">'
             '<div class="v-head"><span class="a-kicker">Process · Deliver</span><h2 class="v-t">Roadmap</h2><p class="v-sub">Plateaus, the work packages between them and what changes from one to the next.</p></div>'
             '<div class="road"><sc-for list="{{plats}}" as="p" hint-placeholder-count="3"><div class="panel" style="gap: 8px"><div class="row" style="gap: 8px"><span class="ax-tile ax-l-implementation" aria-hidden="true"><i class="axg axg-plateau"></i></span><b class="ui" style="font-size: 16px; flex: 1">{{p.name}}</b>' + status('p') + '</div>'
             '<span class="meta">{{p.when}}</span><p style="margin: 0; font-size: 13px; line-height: 19px">{{p.desc}}</p>'
             '<sc-if value="{{p.hasWps}}" hint-placeholder-val="{{true}}"><div class="stack" style="gap: 6px; padding-top: 6px; border-top: 1px solid #ECE5F4"><span class="meta">Work packages to get here</span><sc-for list="{{p.wps}}" as="w" hint-placeholder-count="2"><button type="button" class="ddrow" onClick="{{w.open}}"><span class="ax-tile ax-l-implementation" aria-hidden="true"><i class="axg axg-work-package"></i></span><span style="flex: 1; text-align: left">{{w.name}}<span class="meta" style="display: block">{{w.team}} · {{w.when}}</span></span></button></sc-for></div></sc-if></div></sc-for></div>'
             '<div class="row r-wrap" style="gap: 12px"><b class="ui" style="font-size: 16px">Gap</b><div class="seg" role="group" aria-label="Gap between"><sc-for list="{{pairChips}}" as="c" hint-placeholder-count="3"><button type="button" aria-pressed="{{c.on}}" onClick="{{c.pick}}">{{c.label}}</button></sc-for></div><span class="meta" style="flex: 1; min-width: 160px">{{gapSummary}}</span><button type="button" class="btn t" onClick="{{gapOnView}}">Open the gap view</button></div>'
             + table(['Element', 'Change', 'Work package', 'Review'], 'gapRowsV', 'g', 5,
                     '<td class="td"><button type="button" class="cat-name" onClick="{{g.open}}">' + TILE % ('g', 'g') + '<span><b class="ui">{{g.name}}</b><span class="meta" style="display: block">{{g.kind}}</span></span></button></td>'
                     '<td class="td"><span class="ax-change {{g.chg}}"><b aria-hidden="true">{{g.chgG}}</b>{{g.chgW}}</span></td><td class="td"><span style="font-size: 13px">{{g.wp}}</span></td><td class="td"><button type="button" class="lnk" onClick="{{g.openArb}}">{{g.arb}}</button></td>')
             + '</div>')

CH_PAGE = ('<sc-if value="{{chOpen}}" hint-placeholder-val="{{false}}">'
           + S.subheader('{{pBack}}', '{{pBackLabel}}', '{{ch.name}}', ctx='{{ch.ctx}}', after=status('chOverall')) +
           '<p style="margin: 0; font-size: 15px; line-height: 22px; max-width: 72ch">{{ch.why}}</p>'
           '<div class="ch-steps"><sc-for list="{{ch.steps}}" as="x" hint-placeholder-count="4"><div class="ch-step {{x.cls}}"><div class="row" style="gap: 10px"><span class="pr-n">{{x.n}}</span><b class="ui" style="font-size: 16px; flex: 1">{{x.name}}</b></div>' + status('x') +
           '<sc-for list="{{x.lines}}" as="l" hint-placeholder-count="2"><button type="button" class="ddrow" onClick="{{l.open}}"><span class="srcT" style="background: {{l.bg}}; color: {{l.fg}}">{{l.ab}}</span><span style="flex: 1; text-align: left; min-width: 0">{{l.t}}<span class="meta" style="display: block; white-space: normal">{{l.sub}}</span></span></button></sc-for>'
           '<sc-if value="{{x.hasNote}}" hint-placeholder-val="{{false}}"><span class="meta" style="white-space: normal">{{x.note}}</span></sc-if></div></sc-for></div>'
           '<section class="ep-sec"><h3>What changes</h3>' + table(['Element', 'Change', 'Plateaus'], 'ch.gap', 'g', 4,
               '<td class="td"><button type="button" class="cat-name" onClick="{{g.open}}">' + TILE % ('g', 'g') + '<span><b class="ui">{{g.name}}</b><span class="meta" style="display: block">{{g.kind}}</span></span></button></td>'
               '<td class="td"><span class="ax-change {{g.chg}}"><b aria-hidden="true">{{g.chgG}}</b>{{g.chgW}}</span></td><td class="td">' + TRACK % ('g', 'g') + '</td>') +
           '<div class="row" style="padding-top: 8px"><button type="button" class="btn t" onClick="{{ch.openGap}}">Open the gap view</button></div></section></sc-if>')

ADR_PAGE = ('<sc-if value="{{adrOpen}}" hint-placeholder-val="{{false}}">' + S.subheader('{{pBack}}', '{{pBackLabel}}', '{{adr.t}}', ctx='{{adr.ctx}}', after=status('adr')) +
            '<article class="stack" style="gap: 0; max-width: 760px">'
            '<section class="dd-sec"><h3>Context</h3><p>{{adr.context}}</p></section>'
            '<section class="dd-sec"><h3>Decision</h3><p>{{adr.decision}}</p></section>'
            '<section class="dd-sec"><h3>Options considered</h3><ul class="list"><sc-for list="{{adr.options}}" as="o" hint-placeholder-count="3"><li style="font-size: 14px; align-items: center"><span class="dot {{o.cls}}">{{o.mark}}</span><span style="flex: 1">{{o.t}}</span><span class="meta">{{o.note}}</span></li></sc-for></ul></section>'
            '<section class="dd-sec"><h3>Consequences</h3><ul class="dd-ul"><sc-for list="{{adr.consequences}}" as="b" hint-placeholder-count="3"><li>{{b}}</li></sc-for></ul></section>'
            '<section class="dd-sec"><h3>Elements</h3><div class="row r-wrap" style="gap: 6px"><sc-for list="{{adr.els}}" as="e" hint-placeholder-count="3"><button type="button" class="chip" style="height: 32px" onClick="{{e.open}}">' + TILE % ('e', 'e') + '{{e.name}}</button></sc-for></div></section>'
            '<div class="row r-wrap" style="gap: 14px; padding-top: 14px; border-top: 1px solid #ECE5F4"><span class="meta mono">{{adr.file}}</span><span class="meta">relates to {{adr.ref}}</span><span style="flex: 1"></span><button type="button" class="lnk" onClick="{{adrEdit}}">Propose a change</button></div>'
            '</article></sc-if>')

COVER = '<div class="panel cov" style="gap: 0"><div class="row" style="padding-bottom: 6px"><b class="ui" style="font-size: 15px; flex: 1">What the ASD must cover</b><span class="meta">{{%s}}</span></div><sc-for list="{{%s}}" as="c" hint-placeholder-count="6"><div class="chk-row" style="align-items: center"><span style="flex: 1; min-width: 0">{{c.t}}<span class="meta" style="display: block">{{c.sec}} · {{c.note}}</span></span><span class="status st-{{c.st}}"><span class="tile" aria-hidden="true">{{c.g}}</span>{{c.w}}</span></div></sc-for></div>'
ARB_PAGE = ('<sc-if value="{{arbOpen}}" hint-placeholder-val="{{false}}">' + S.subheader('{{pBack}}', '{{pBackLabel}}', '{{arb.t}}', ctx='{{arb.ctx}}', after=status('arbRd'),
                                                                                   actions='<sc-if value="{{arb.hasAsd}}" hint-placeholder-val="{{true}}"><button type="button" class="btn t" onClick="{{asdGo}}">Open the ASD</button></sc-if>') +
            '<div class="banner {{arb.bcls}}">{{arb.banner}}</div><div class="arb-grid"><div class="stack" style="gap: 16px; min-width: 0">'
            '<div class="panel" style="gap: 0"><b class="ui" style="font-size: 15px; padding-bottom: 6px">Checks</b><sc-for list="{{arb.checks}}" as="c" hint-placeholder-count="5"><div class="check {{c.st}}"><span class="tile solo st-{{c.sc}}" aria-hidden="true">{{c.mark}}</span><div style="flex: 1; min-width: 0"><b>{{c.label}}</b><span class="id">{{c.g}} · {{c.word}}</span><sc-if value="{{c.hasNote}}" hint-placeholder-val="{{false}}"><ul><li>{{c.note}}</li></ul></sc-if></div><sc-if value="{{c.canFix}}" hint-placeholder-val="{{false}}"><button type="button" class="chip" style="height: 28px; white-space: nowrap" onClick="{{c.fix}}">Open a fix</button></sc-if></div></sc-for></div>'
            '<sc-if value="{{arb.hasAsd}}" hint-placeholder-val="{{true}}">' + COVER % ('arb.coverN', 'arb.cover') + '</sc-if>'
            '<sc-if value="{{arb.hasAsd}}" hint-placeholder-val="{{true}}"><div class="panel" style="gap: 0"><div class="row" style="padding-bottom: 6px"><b class="ui" style="font-size: 15px; flex: 1">Architecture Solution Design</b><span class="meta">{{arb.asdCount}}</span></div><sc-for list="{{arb.secs}}" as="x" hint-placeholder-count="5"><div class="chk-row" style="align-items: center"><span class="meta" style="width: 22px">{{x.n}}</span><span style="flex: 1">{{x.name}}</span><span class="src-badge {{x.badge}}">{{x.state}}</span><sc-if value="{{x.missing}}" hint-placeholder-val="{{false}}"><button type="button" class="chip" style="height: 28px; white-space: nowrap" onClick="{{x.write}}">Write it</button></sc-if></div></sc-for></div></sc-if>'
            '</div><div class="stack" style="gap: 16px; min-width: 0">'
            '<div class="panel"><b class="ui" style="font-size: 15px">Scope</b><span style="font-size: 14px">{{arb.scope}}</span><span class="meta">{{arb.scopeCounts}}</span><button type="button" class="lnk" style="align-self: flex-start" onClick="{{arb.seeGap}}">Open the gap view</button></div>'
            '<div class="panel" style="gap: 0"><b class="ui" style="font-size: 15px; padding-bottom: 6px">Reviewers</b><sc-for list="{{arb.reviewers}}" as="r" hint-placeholder-count="3"><div class="chk-row" style="align-items: center; flex-wrap: wrap"><span style="flex: 1; min-width: 0">{{r.who}}<span class="meta" style="display: block">{{r.role}}</span></span>' + status('r') + '<sc-if value="{{r.hasNote}}" hint-placeholder-val="{{false}}"><span class="rv-note">{{r.note}}</span></sc-if></div></sc-for><sc-if value="{{arb.noReviewers}}" hint-placeholder-val="{{false}}"><span class="meta">Reviewers are named when the submission leaves draft.</span></sc-if></div>'
            '<sc-if value="{{arb.hasConditions}}" hint-placeholder-val="{{true}}"><div class="panel" style="gap: 0"><b class="ui" style="font-size: 15px; padding-bottom: 6px">Conditions</b><sc-for list="{{arb.conditions}}" as="b" hint-placeholder-count="2"><div class="chk-row"><span class="srcT" style="background: #ECE5F4; color: #48454E">{{b.id}}</span><span style="flex: 1; min-width: 0">{{b.t}}<span class="meta" style="display: block">{{b.owner}} · due {{b.due}}</span></span>' + status('b') + '</div></sc-for></div></sc-if>'
            '<sc-if value="{{arb.hasAsks}}" hint-placeholder-val="{{false}}"><div class="panel" style="gap: 0"><b class="ui" style="font-size: 15px; padding-bottom: 6px">Asked of the board</b><sc-for list="{{arb.asks}}" as="q" hint-placeholder-count="3"><div class="chk-row"><span class="pr-n" style="width: 22px; height: 22px; font-size: 11px">?</span><span style="flex: 1; min-width: 0">{{q.t}}<span class="meta" style="display: block">{{q.ref}}</span></span></div></sc-for></div></sc-if>'
            '<sc-if value="{{arb.canDecide}}" hint-placeholder-val="{{true}}"><div class="panel"><b class="ui" style="font-size: 15px">Your decision</b><span class="meta">Emma Laurent · Enterprise architecture</span><div class="row r-wrap" style="gap: 8px"><button type="button" class="btn f" aria-disabled="{{arb.blocked}}" onClick="{{arb.approve}}">Approve</button><button type="button" class="btn t" aria-disabled="{{arb.blocked}}" onClick="{{arb.approveC}}">With conditions</button><button type="button" class="btn x" onClick="{{arb.changes}}">Request changes</button></div><sc-if value="{{arb.blocked}}" hint-placeholder-val="{{false}}"><span class="meta" style="white-space: normal">Approval is unavailable while a blocking check fails or a section is missing.</span></sc-if></div></sc-if>'
            '<sc-if value="{{arb.hasRecorded}}" hint-placeholder-val="{{false}}"><div class="panel"><b class="ui" style="font-size: 15px">Decision</b><span style="font-size: 14px">{{arb.status}}</span><span class="meta" style="white-space: normal">{{arb.recorded}}</span></div></sc-if>'
            '</div></div></sc-if>')

_W, _H = D.size(D.VIEWS['application'])
_STATIC = lambda m, tag: f'<div class="lc lc-static"><div class="lc-scroll" style="height: {round(_H * .58) + 4}px"><div class="lc-stage sel-none" style="zoom: .58">{D.render("application", m, interactive=False)[0]}</div></div></div>'
ASD_PAGE = ('<sc-if value="{{asdOpen}}" hint-placeholder-val="{{false}}">' + S.subheader('{{pBack}}', '{{pBackLabel}}', 'ASD · {{arb.t}}', ctx='{{asdCtx}}', actions='<button type="button" class="btn x" onClick="{{asdExport}}">Export as Markdown</button>') +
            '<div class="dd-grid"><article class="stack" style="gap: 0; max-width: 940px; min-width: 0">' + COVER % ('asdCoverN', 'asdCover') +
            '<sc-for list="{{asdSecs}}" as="x" hint-placeholder-count="5"><section class="dd-sec"><div class="asd-head"><h5><span class="num">{{x.n}}</span>{{x.name}}</h5><span class="src-badge {{x.badge}}">{{x.src}}</span></div>'
            '<sc-if value="{{x.hasP}}" hint-placeholder-val="{{true}}"><p>{{x.p}}</p></sc-if>'
            '<sc-if value="{{x.hasB}}" hint-placeholder-val="{{false}}"><ul class="dd-ul"><sc-for list="{{x.b}}" as="b" hint-placeholder-count="2"><li>{{b}}</li></sc-for></ul></sc-if>'
            '<sc-if value="{{x.hasTable}}" hint-placeholder-val="{{false}}"><div class="dd-tbl"><table><thead><tr><sc-for list="{{x.thead}}" as="hd" hint-placeholder-count="3"><th>{{hd}}</th></sc-for></tr></thead><tbody><sc-for list="{{x.trows}}" as="tr" hint-placeholder-count="3"><tr><sc-for list="{{tr.cells}}" as="cl" hint-placeholder-count="3"><td class="{{cl.cls}}">{{cl.t}}</td></sc-for></tr></sc-for></tbody></table></div></sc-if>'
            '<sc-if value="{{x.hasAsks}}" hint-placeholder-val="{{false}}"><div class="asks"><b class="ui">Asked of the board</b><ol><sc-for list="{{x.asks}}" as="q" hint-placeholder-count="3"><li>{{q.t}} <span class="meta">{{q.ref}}</span></li></sc-for></ol></div></sc-if>'
            '<sc-if value="{{x.missing}}" hint-placeholder-val="{{false}}"><div class="prov"><b>Missing</b><span>Written in the submission file. The board cannot decide without it.</span></div><div><button type="button" class="chip" style="height: 32px" onClick="{{x.write}}">Write it</button></div></sc-if>'
            '<sc-if value="{{x.hasRows}}" hint-placeholder-val="{{false}}"><div class="rows"><sc-for list="{{x.rows}}" as="r" hint-placeholder-count="3"><div><b class="ui" style="font-size: 13px">{{r.a}}</b><span>{{r.b}}</span><span class="meta">{{r.c}}</span></div></sc-for></div></sc-if>'
            '<sc-if value="{{x.hasBase}}" hint-placeholder-val="{{false}}">' + _STATIC('tr1', 'b') + '</sc-if>'
            '<sc-if value="{{x.hasTarget}}" hint-placeholder-val="{{false}}">' + _STATIC('target', 't') + '</sc-if>'
            '</section></sc-for></article>'
            '<nav class="toc" aria-label="On this page"><span class="meta" style="padding: 0 10px 6px">13 sections</span><sc-for list="{{asdSecs}}" as="x" hint-placeholder-count="5"><a href="#asd">{{x.name}}</a></sc-for></nav></div></sc-if>')

ARCH = ('<sc-if value="{{vArch}}" hint-placeholder-val="{{false}}"><div class="stack arch-ds" style="gap: 16px">'
        '<sc-if value="{{archMain}}" hint-placeholder-val="{{true}}">' + S.subheader('{{goHome}}', 'Back to Docs', 'Corporate credit platform', ctx='Architecture model · {{archCounts}} · main @ 4a1b9e0') +
        AREA_TABS + '<div class="a-body">' + SIDE + '<div class="a-main">'
        '<sc-if value="{{arCat}}" hint-placeholder-val="{{false}}">' + CAT_MAIN + '</sc-if>'
        '<sc-if value="{{arViews}}" hint-placeholder-val="{{true}}">' + VIEWS_MAIN + '</sc-if>'
        '<sc-if value="{{prChanges}}" hint-placeholder-val="{{false}}">' + P_CHANGES + '</sc-if>'
        '<sc-if value="{{prDecisions}}" hint-placeholder-val="{{false}}">' + P_DECISIONS + '</sc-if>'
        '<sc-if value="{{prReviews}}" hint-placeholder-val="{{false}}">' + P_REVIEWS + '</sc-if>'
        '<sc-if value="{{prRoadmap}}" hint-placeholder-val="{{false}}">' + P_ROADMAP + '</sc-if>'
        '</div></div></sc-if>' + EL_PAGE + CH_PAGE + ADR_PAGE + ARB_PAGE + ASD_PAGE + '</div></sc-if>')

HOME_B = ('<sc-if value="{{homeB}}" hint-placeholder-val="{{false}}"><div class="lens arch-ds">'
          '<nav class="applist" aria-label="Services"><sc-for list="{{lensGroups}}" as="g" hint-placeholder-count="3"><div class="gh">{{g.label}}</div><sc-for list="{{g.apps}}" as="a" hint-placeholder-count="2"><button type="button" class="appbtn" aria-current="{{a.cur}}" onClick="{{a.pick}}"><span style="flex: 1">{{a.name}}</span><sc-if value="{{a.legacy}}" hint-placeholder-val="{{false}}"><span class="meta">legacy</span></sc-if></button></sc-for></sc-for></nav>'
          '<div class="stack" style="gap: 12px; min-width: 0"><div class="vt"><h2>Corporate credit platform</h2><span class="meta">Application cooperation · pick a service</span></div>' + VIEW_TOOLS + CANVAS +
          '<div class="row r-wrap" style="gap: 8px; padding-top: 8px; border-top: 1px solid #ECE5F4"><span class="meta">Across the organisation</span><button type="button" class="chip" style="height: 32px" onClick="{{go_arch}}">All architecture</button><button type="button" class="chip" style="height: 32px" onClick="{{go_ai}}">AI wiki</button><button type="button" class="chip" style="height: 32px" onClick="{{go_ops}}">Operations</button><button type="button" class="chip" style="height: 32px" onClick="{{go_new}}">New joiner</button></div>'
          '</div></div></sc-if>')

# ------------------------------------------------------------------ CSS
_keys = sorted({n['k'] for v in D.VIEWS.values() for n in v['nodes']})
SEL_CSS = ''.join(f'.sel-{k} .n-{k}{{outline:2px solid var(--md-sys-color-primary);outline-offset:2px}}.sel-{k} .e-{k}{{color:var(--md-sys-color-primary)!important;opacity:1!important}}.sel-{k} .e-{k} .ln{{stroke-width:2.2}}.sel-{k} .lc-lbl.e-{k}{{opacity:1;color:var(--md-sys-color-primary)}}' for k in _keys)
_types = sorted({n['kind'] for v in D.VIEWS.values() for n in v['nodes']} | {'Plateau', 'Work package'})

CSS = AX.CSS + AX.glyph_masks(_types) + r"""
.arch-ds .status .tile,.arch-ds .tile.solo{padding:0;margin:0;gap:0;flex:none}
.arch-ds .status{margin:0}
.arch-ds .check{align-items:flex-start}
.arch-ds .check ul{margin:2px 0 0}
.a-body{display:grid;grid-template-columns:232px minmax(0,1fr);gap:24px;align-items:start}
.a-nav{display:flex;flex-direction:column;gap:2px;position:sticky;top:0}
.a-gh{font:700 11px/16px Manrope,'Segoe UI',system-ui,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#48454E;padding:14px 12px 4px}
.a-gh:first-child{padding-top:2px}
.a-item{display:flex;align-items:center;gap:10px;width:100%;box-sizing:border-box;min-height:40px;padding:6px 12px;border:0;border-radius:999px;background:transparent;color:#1C1B1E;font:500 14px/18px 'Open Sans',system-ui,sans-serif;text-align:left;cursor:pointer}
.a-item:hover{background:rgba(53,48,126,.08)}
.a-item[aria-current="page"]{background:#E3DFFF;color:#191836;font-weight:600}
.a-it{flex:1;min-width:0}.a-sub{display:block;font-size:11px;line-height:15px;color:#48454E;font-weight:500}
.a-n{font:600 12px/16px Manrope,system-ui,sans-serif;color:#48454E}
.a-item .swatch{width:20px;height:14px;border-radius:3px;background:var(--ax-fill);box-shadow:inset 0 0 0 1px var(--ax-ink);flex:none}
.a-main{min-width:0}
.v-head{display:flex;flex-direction:column;gap:2px}
.a-kicker{font:700 11px/16px Manrope,system-ui,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#48454E}
.v-t{margin:0;font:700 22px/28px Manrope,'Segoe UI',system-ui,sans-serif}
.v-sub{margin:0;font-size:14px;line-height:20px;color:#48454E;max-width:80ch}
.lc{position:relative;border:1px solid #CAC4CF;border-radius:16px;overflow:hidden;background-color:#FDF8FD;background-image:radial-gradient(#CAC4CF 1px,transparent 1.3px);background-size:20px 20px}
.lc-scroll{overflow:auto;overscroll-behavior:contain}
.lc-stage{transform-origin:0 0}
.lc-panel{position:absolute;left:12px;top:12px;z-index:5;display:flex;align-items:center;gap:10px;flex-wrap:wrap;max-width:calc(100% - 24px);padding:6px 10px 6px 8px;border-radius:12px;background:#FFFFFF;box-shadow:0 1px 2px rgba(0,0,0,.3),0 1px 3px 1px rgba(0,0,0,.15);font-size:13px}
.lc-mark{font:800 11px/16px Manrope,system-ui,sans-serif;padding:2px 6px;border-radius:4px;background:#ECE5F4;color:#48454E}
.lc-crumb{font:600 13px/18px Manrope,system-ui,sans-serif;color:#1C1B1E}
.lc-id{font:600 12px/16px 'Open Sans',system-ui,sans-serif;color:#48454E;background:#F2EBFA;padding:1px 6px;border-radius:4px}
.dd-pic{margin:10px 0 0;overflow:auto;border:1px solid #CAC4CF;border-radius:16px;background-color:#FDF8FD;background-image:radial-gradient(#CAC4CF 1px,transparent 1.3px);background-size:20px 20px;max-width:100%}
.dd-pic .lc-lbl{z-index:3}
.sm-st{position:absolute;z-index:2;box-sizing:border-box;border:1.5px solid #48454E;border-radius:24px;background:#FFFFFF;display:flex;align-items:center;justify-content:center;gap:8px;font:600 13px/16px 'Open Sans',system-ui,sans-serif;color:#1C1B1E;text-align:center;padding:0 14px}
.sm-st.start{border-color:#35307E;box-shadow:inset 0 0 0 1px #35307E}.sm-st.end{border-width:3px;border-style:double}
.sm-init{width:10px;height:10px;border-radius:50%;background:#35307E;flex:none}
.er-ent{position:absolute;z-index:2;box-sizing:border-box;border:1px solid var(--ax-application-ink);border-radius:4px;background:#FFFFFF;overflow:hidden;font-size:12px}
.er-ent b{display:block;padding:8px 10px;background:var(--ax-application-fill);font:700 13px/18px Manrope,system-ui,sans-serif;border-bottom:1px solid var(--ax-application-ink)}
.er-ent ul{list-style:none;margin:0;padding:2px 0}.er-ent li{display:grid;grid-template-columns:24px minmax(0,1fr) auto;gap:6px;padding:3px 10px;line-height:18px}
.er-k{font:700 10px/18px Manrope,system-ui,sans-serif;color:#7A2457}.er-n{font-family:'JetBrains Mono',ui-monospace,Menlo,monospace;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.er-t{color:#48454E;font-family:'JetBrains Mono',ui-monospace,Menlo,monospace;font-size:11px}
.er-c{font:700 12px Manrope,system-ui,sans-serif;fill:#48454E}
.hx-ad{position:absolute;z-index:2;box-sizing:border-box;width:178px;padding:6px 10px;border-radius:8px;background:#FFFFFF;border:1px solid var(--ax-application-ink);font-size:12px;line-height:16px}
.hx-ad b{display:block;font:700 13px/16px Manrope,system-ui,sans-serif}.hx-ad.out{width:236px;color:#48454E}.hx-ad.out b{color:#1C1B1E}
.hx-lab{position:absolute;z-index:2;text-align:center;font:600 12px/16px Manrope,system-ui,sans-serif;color:var(--ax-application-ink)}
.hx-dom{position:absolute;z-index:2;text-align:center;font-size:12px;line-height:16px;color:#1C1B1E}.hx-dom b{display:block;font:700 14px/18px Manrope,system-ui,sans-serif}
.hx-cap{position:absolute;z-index:2;font:700 11px/16px Manrope,system-ui,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#48454E}
.dd-tbl{overflow-x:auto;border:1px solid #CAC4CF;border-radius:12px;background:#FFFFFF;margin-top:8px}
.dd-tbl table{width:100%;border-collapse:collapse;font-size:13px;line-height:18px}
.dd-tbl th{text-align:left;padding:8px 12px;font:700 11px/16px Manrope,system-ui,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#48454E;border-bottom:1px solid #CAC4CF}
.dd-tbl td{padding:8px 12px;border-top:1px solid #ECE5F4;vertical-align:top}.dd-tbl tr:first-child td{border-top:0}.dd-tbl td.k{font-weight:600;white-space:nowrap}
.dd-api{list-style:none;margin:8px 0 0;padding:0;border:1px solid #CAC4CF;border-radius:12px;background:#FFFFFF}
.dd-api li{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:8px 12px;border-top:1px solid #ECE5F4;font-size:13px}.dd-api li:first-child{border-top:0}
.dd-api code{font:600 13px/18px 'JetBrains Mono',ui-monospace,Menlo,monospace}.dd-api .op{color:#48454E}
.mth{min-width:52px;text-align:center;padding:2px 6px;border-radius:4px;font:700 11px/16px Manrope,system-ui,sans-serif}
.m-get{background:#CFEDFA;color:#0A5570}.m-post{background:#ACF4A2;color:#1B5F1F}.m-put{background:#FFDEA0;color:#6A4E00}.m-delete{background:#FFDAD6;color:#93000A}
.rv-note{display:block;flex-basis:100%;margin-top:2px;padding:6px 8px;border-radius:8px;background:#F2EBFA;font-size:12px;line-height:17px;color:#1C1B1E}
.asks{margin-top:10px;padding:10px 14px;border-radius:12px;background:#F2EBFA;font-size:14px}.asks ol{margin:6px 0 0;padding-left:20px}.asks li{margin:3px 0}
.lc-pb{width:28px;height:28px;border:0;border-radius:8px;background:#F2EBFA;color:#1C1B1E;display:inline-flex;align-items:center;justify-content:center;cursor:pointer}.lc-pb:hover{background:#E3DFFF}
.lc-crumb{display:flex;align-items:center;gap:4px;flex-wrap:wrap;font:600 13px/18px Manrope,system-ui,sans-serif;color:#1C1B1E}
.lc-root{color:#48454E;font-weight:600}.lc-sep{color:#79757F}
.lc-cb{border:0;background:transparent;padding:2px 4px;border-radius:6px;font:inherit;color:#35307E;cursor:pointer}.lc-cb:hover{background:rgba(53,48,126,.08)}.lc-cb[aria-current="true"]{color:#1C1B1E;cursor:default}.lc-cb[aria-current="true"]:hover{background:transparent}
.lc-nav{position:absolute;z-index:4;width:24px;height:24px;border:0;border-radius:6px;background:#FFFFFF;color:#35307E;display:inline-flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,.3),0 1px 3px 1px rgba(0,0,0,.15)}
.lc-nav:hover{background:#E3DFFF}.lc-nav:focus-visible{outline:2px solid #35307E;outline-offset:2px}
.lc-open{align-self:flex-start}
.a-item.a-l1{padding-left:28px}.a-item.a-l2{padding-left:44px}
.lc-zoom{position:absolute;left:12px;bottom:12px;z-index:5;display:flex;flex-direction:column;border-radius:12px;background:#FFFFFF;box-shadow:0 1px 2px rgba(0,0,0,.3),0 1px 3px 1px rgba(0,0,0,.15);overflow:hidden}
.lc-zoom button{width:36px;height:32px;border:0;border-top:1px solid #ECE5F4;background:transparent;color:#1C1B1E;font:600 16px/1 Manrope,system-ui,sans-serif;cursor:pointer}
.lc-zoom button:first-child{border-top:0}.lc-zoom button.fit{font-size:11px}
.lc-zoom button:hover{background:rgba(53,48,126,.08)}
.lc-card{position:absolute;right:12px;top:12px;z-index:6;width:300px;max-height:calc(100% - 24px);overflow:auto;box-sizing:border-box;display:flex;flex-direction:column;gap:10px;padding:14px 16px;border-radius:16px;background:#FFFFFF;box-shadow:0 2px 6px 2px rgba(0,0,0,.15),0 1px 2px rgba(0,0,0,.3)}
.lc-card .ax-change{align-self:flex-start}
.lc-desc{margin:0;font-size:13px;line-height:19px}
.lc-rels{display:flex;flex-direction:column;gap:2px;padding-top:6px;border-top:1px solid #ECE5F4}
.lc-rel{display:flex;align-items:center;gap:8px;width:100%;padding:6px 6px;border:0;border-radius:8px;background:transparent;font:400 13px/17px 'Open Sans',system-ui,sans-serif;color:#1C1B1E;cursor:pointer}
.lc-rel:hover{background:rgba(53,48,126,.06)}
.lc-verb{width:84px;flex:none;font-size:12px;color:#48454E;text-align:left}
.lc-legend{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center}
.lc-legend .lg-i{display:inline-flex;align-items:center;gap:6px;font-size:12px;color:#48454E}
.lc-legend .swatch{width:28px;height:18px;border-radius:4px;background:var(--ax-fill);box-shadow:inset 0 0 0 1px var(--ax-ink)}
.lc-src{margin:0;padding:12px 14px;border-radius:12px;background:#1D1A27;color:#E6E1E6;font:400 12px/18px 'JetBrains Mono',ui-monospace,Menlo,Consolas,monospace;white-space:pre-wrap;overflow-wrap:anywhere}
.lc-static{background-image:none}
.lc-stage:not(.sel-none) .edge{opacity:.22}
.lc-stage:not(.sel-none) .lc-lbl{opacity:.35}
.cat-name{display:flex;align-items:center;gap:10px;padding:0;border:0;background:transparent;text-align:left;cursor:pointer;color:#1C1B1E;font:inherit;min-width:0}
.cat-name:hover b,.cat-name:hover>span:last-child{text-decoration:underline}
.cat-tbl .td,.ch-tbl .td{vertical-align:middle}
.ep-grid{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:24px;align-items:start}
.ep-sec{display:flex;flex-direction:column;gap:10px}
.ep-sec h3{margin:0;font:700 16px/24px Manrope,'Segoe UI',system-ui,sans-serif}
.pr-steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;counter-reset:s}
.pr-step{display:flex;gap:10px;align-items:flex-start;padding:12px;border-radius:12px;background:#F2EBFA;font-size:14px;position:relative}
.pr-n{width:28px;height:28px;border-radius:8px;background:#ECE5F4;display:inline-grid;place-items:center;font:700 13px/1 Manrope,system-ui,sans-serif;flex:none;color:#1C1B1E}
.pr-step .pr-n{background:#FFFFFF}
.ch-steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;align-items:stretch}
.ch-step{display:flex;flex-direction:column;gap:10px;padding:14px 16px;border-radius:16px;background:#FFFFFF;box-shadow:0 1px 2px rgba(0,0,0,.3),0 1px 3px 1px rgba(0,0,0,.15)}
.ch-step .status{align-self:flex-start}
.ch-step.cur{box-shadow:0 0 0 2px #35307E,0 1px 3px 1px rgba(0,0,0,.15)}
.road{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.arb-grid{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:16px;align-items:start}
.banner{padding:10px 14px;border-radius:12px;font-size:14px;line-height:20px}
.b-blk{background:#FFDAD6;color:#410002}.b-att{background:#FFDEA0;color:#3F2E00}.b-ok{background:#ACF4A2;color:#0B3910}
.chk-row{display:flex;gap:10px;align-items:flex-start;padding:8px 0;border-top:1px solid #F2EBFA;font-size:13px;line-height:18px}
.pane-on .a-body{grid-template-columns:minmax(0,1fr)}.pane-on .a-nav{flex-direction:row;flex-wrap:wrap;position:static}.pane-on .a-gh{display:none}.pane-on .a-item{width:auto}
.pane-on .arb-grid,.pane-on .ep-grid{grid-template-columns:minmax(0,1fr)}.pane-on .ch-steps,.pane-on .pr-steps{grid-template-columns:repeat(2,minmax(0,1fr))}
@container win (max-width: 1199px){.a-body{grid-template-columns:minmax(0,1fr)!important}.a-nav{flex-direction:row!important;flex-wrap:wrap;position:static!important;gap:6px!important}.a-gh{display:none}.a-item{width:auto!important;min-height:36px;border:1px solid #CAC4CF}.a-item[aria-current="page"]{border-color:#E3DFFF}
.arb-grid,.ep-grid{grid-template-columns:minmax(0,1fr)!important}.ch-steps,.pr-steps{grid-template-columns:repeat(2,minmax(0,1fr))!important}}
@container win (max-width: 839px){.road,.ch-steps,.pr-steps{grid-template-columns:minmax(0,1fr)!important}
.lc-card{position:static;width:auto;max-height:none;margin:0 12px 12px;box-shadow:none;border:1px solid #CAC4CF}.lc-panel .lc-id{display:none}
.cat-tbl thead,.ch-tbl thead{display:none}.cat-tbl,.cat-tbl tbody,.ch-tbl,.ch-tbl tbody{display:block}.cat-tbl tr,.ch-tbl tr{display:flex;flex-wrap:wrap;gap:6px 12px;padding:12px 16px;border-top:1px solid #CAC4CF}.cat-tbl td,.ch-tbl td{display:block;border:0!important;padding:0!important;height:auto!important}.cat-tbl td:first-child,.ch-tbl td:first-child{flex-basis:100%}}
""" + open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_lc_css.txt'), encoding='utf-8').read() + SEL_CSS

# ------------------------------------------------------------------ JS logic (inserted into the lab's renderVals; DG = docs_lab_data.js_data())
ARCH_JS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs_arch.js'), encoding='utf-8').read()
