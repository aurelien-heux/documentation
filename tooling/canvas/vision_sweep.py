"""Sweep in the production vision, aligned on the running application (aitoolbox dev, Oct 2026):
runs launched from a Jira ticket (Launch a pipeline: Jira ticket ID, base branch, Bitbucket project), the run page with
the agents' pipeline (SWEEP orchestrator, Jira planner, Frontend and Backend in parallel with Planner, Coder and Reviewer,
Integration check) and the live console (Logs, Tool calls, LLM calls, Filter lines).
Exports: SCREEN (main content), DIALOG (overlay), CSS, JS (methods swDefaults, swModel, sweepVals, sweepTick, swAnswer)."""
import shell as S

I_SEARCH = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>'
I_REFRESH = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 12a8 8 0 1 1-2.3-5.7"/><path d="M20 4v5h-5"/></svg>'
I_PLAY = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>'
I_SPARK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#006A6A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/></svg>'
I_DL = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11M7 10l5 5 5-5M5 20h14"/></svg>'
I_X = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>'
I_EMPTY = '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M7 10l3 2-3 2M12 15h4"/></svg>'

# ------------------------------------------------------------------ runs list
LIST = ('<sc-if value="{{sw_list}}" hint-placeholder-val="{{true}}">'
  '<div class="sw-tool">'
    '<label class="sw-q">' + I_SEARCH + '<input type="search" placeholder="Ticket" aria-label="Search by ticket" value="{{sw_q}}" onChange="{{sw_onQ}}"></label>'
    '<select class="sel sw-sel" aria-label="Status" value="{{sw_status}}" onChange="{{sw_onStatus}}"><option value="all">All statuses</option><option value="Running">Running</option><option value="Succeeded">Succeeded</option><option value="Failed">Failed</option><option value="Cancelled">Cancelled</option></select>'
    '<span class="meta r-hide-c">{{sw_count}}</span>'
    '<span style="flex: 1"></span>'
    '<button type="button" class="ib" aria-label="Refresh" title="Refresh" style="margin: 0" onClick="{{sw_refresh}}">' + I_REFRESH + '</button>'
    '<button type="button" class="btn f btn-i sw-new" data-anchor="sweep.run" onClick="{{sw_openDlg}}">' + I_PLAY + 'New run</button>'
  '</div>'
  '<div class="card" style="padding: 0; overflow: hidden">'
    '<sc-if value="{{sw_hasRows}}" hint-placeholder-val="{{true}}">'
    '<table class="sw-tbl">'
      '<colgroup><col style="width: 34%"><col style="width: 22%"><col style="width: 20%"><col style="width: 14%"><col style="width: 10%"></colgroup>'
      '<thead><tr><th class="th">Ticket</th><th class="th">Status</th><th class="th">Pull requests</th><th class="th">Started</th><th class="th">Duration</th></tr></thead>'
      '<tbody><sc-for list="{{sw_rows}}" as="r" hint-placeholder-count="5"><tr class="rw">'
        '<td class="td"><button type="button" class="sw-key" onClick="{{r.open}}">{{r.key}}</button><div class="sw-ttl" title="{{r.title}}">{{r.title}}</div></td>'
        '<td class="td"><span class="tile {{r.tile}}"><i></i>{{r.status}}</span><div class="sw-sub">{{r.now}}</div></td>'
        '<td class="td"><sc-if value="{{r.hasPr}}" hint-placeholder-val="{{true}}"><button type="button" class="chip sw-ai" data-anchor="{{r.anchor}}" onClick="{{r.openSum}}">' + I_SPARK + '{{r.prs}}</button></sc-if><sc-if value="{{r.noPr}}" hint-placeholder-val="{{false}}"><span class="meta">{{r.prs}}</span></sc-if></td>'
        '<td class="td"><div style="font-size: 13px">{{r.started}}</div><div class="sw-sub">{{r.by}}</div></td>'
        '<td class="td" style="font-size: 13px; color: #48454E">{{r.dur}}</td>'
      '</tr></sc-for></tbody>'
    '</table></sc-if>'
    '<sc-if value="{{sw_noRows}}" hint-placeholder-val="{{false}}"><div class="sw-empty"><span class="sw-emic">' + I_EMPTY + '</span><b class="ui" style="font-size: 18px">No runs match</b><span style="font-size: 14px; color: #48454E">No run for “{{sw_q}}” with this status. Clear the filters, or launch one with New run.</span><button type="button" class="btn o" onClick="{{sw_clear}}">Clear filters</button></div></sc-if>'
  '</div>'
  ''
'</sc-if>')

# ------------------------------------------------------------------ run page
ACTIONS = ('<sc-if value="{{sw_r.canCancel}}" hint-placeholder-val="{{true}}"><button type="button" class="btn o" onClick="{{sw_askCancel}}">Cancel run</button></sc-if>'
           '<sc-if value="{{sw_r.canRerun}}" hint-placeholder-val="{{false}}"><button type="button" class="btn o" onClick="{{sw_rerun}}">Re-run</button></sc-if>')
SUB = S.subheader('{{sw_back}}', 'Back to runs', '{{sw_r.key}}', ctx='{{sw_r.ctx}}', actions=ACTIONS,
                  after='<span class="tile {{sw_r.tile}}"><i></i>{{sw_r.status}}</span>')

RESULT = (
  '<sc-if value="{{sw_confirm}}" hint-placeholder-val="{{false}}"><div class="sw-res neu" role="alertdialog" aria-label="Cancel this run?"><div style="flex: 1; min-width: 220px"><b class="ui">Cancel this run?</b><div style="font-size: 13px; margin-top: 2px">The agents stop where they are. Nothing is pushed and no pull request is opened.</div></div><button type="button" class="btn x" onClick="{{sw_keep}}">Keep running</button><button type="button" class="btn f sm sw-danger" onClick="{{sw_cancel}}">Cancel run</button></div></sc-if>'
  '<sc-if value="{{sw_r.isOk}}" hint-placeholder-val="{{false}}"><div class="sw-res ok"><span class="tile ok"><i></i>Succeeded</span><div style="flex: 1; min-width: 220px"><b class="ui">{{sw_r.resTitle}}</b><div style="font-size: 13px; margin-top: 2px">{{sw_r.resText}}</div></div></div></sc-if>'
  '<sc-if value="{{sw_r.isFail}}" hint-placeholder-val="{{false}}"><div class="sw-res err"><span class="tile er"><i></i>Failed</span><div style="flex: 1; min-width: 220px"><b class="ui">{{sw_r.resTitle}}</b><div style="font-size: 13px; margin-top: 2px">{{sw_r.resText}}</div></div><button type="button" class="btn f sm" onClick="{{sw_rerunFrom}}">Re-run from the integration check</button><button type="button" class="btn o sm" onClick="{{sw_rerun}}">Re-run all</button></div></sc-if>'
  '<sc-if value="{{sw_r.isCancel}}" hint-placeholder-val="{{false}}"><div class="sw-res neu"><span class="tile ne"><i></i>Cancelled</span><div style="flex: 1; min-width: 220px"><b class="ui">{{sw_r.resTitle}}</b><div style="font-size: 13px; margin-top: 2px">{{sw_r.resText}}</div></div></div></sc-if>'
  '<sc-if value="{{sw_hasPrs}}" hint-placeholder-val="{{false}}"><div class="card sw-prs"><div class="row" style="justify-content: space-between; margin-bottom: 4px"><b class="ui" style="font-size: 16px">Pull requests</b><span class="meta">Bitbucket · {{sw_r.project}}</span></div>'
    '<sc-for list="{{sw_prs}}" as="p" hint-placeholder-count="2"><div class="sw-pr">'
      '<div style="flex: 1; min-width: 200px"><b class="ui" style="font-size: 14px">{{p.repo}} #{{p.num}}</b><sc-if value="{{p.draft}}" hint-placeholder-val="{{false}}"> <span class="tag" style="background: #ECE5F4">Draft</span></sc-if><div class="sw-sub">{{p.title}} · {{p.diff}}</div></div>'
      '<button type="button" class="chip sw-ai" data-anchor="{{p.anchor}}" aria-expanded="{{p.open}}" onClick="{{p.toggle}}">' + I_SPARK + 'Review summary</button>'
      '<button type="button" class="chip" onClick="{{p.bb}}">Open in Bitbucket</button>'
      '<sc-if value="{{p.open}}" hint-placeholder-val="{{false}}"><div class="sw-sum"><div class="meta" style="white-space: normal; margin-bottom: 6px">Written by the Reviewer agent from the diff and the run logs</div><ul><sc-for list="{{p.points}}" as="b" hint-placeholder-count="4"><li><b>{{b.k}}</b> {{b.v}}</li></sc-for></ul>'
        '<div class="row r-wrap" style="gap: 8px; margin-top: 8px"><span style="font-size: 13px">Was this summary useful?</span><button type="button" class="chip" aria-pressed="{{p.up}}" style="{{p.upS}}" onClick="{{p.rateUp}}">Useful</button><button type="button" class="chip" aria-pressed="{{p.down}}" style="{{p.downS}}" onClick="{{p.rateDown}}">Not useful</button><sc-if value="{{p.rated}}" hint-placeholder-val="{{false}}"><span class="meta">Thanks, the platform team sees it.</span></sc-if></div></div></sc-if>'
    '</div></sc-for></div></sc-if>')

PIPE = ('<div class="card sw-pipe"><div class="row" style="justify-content: space-between"><h3 class="ui">Pipeline</h3><span class="meta">{{sw_r.stepsDone}}</span></div>'
  '<div class="sw-steps"><sc-for list="{{sw_steps}}" as="x" hint-placeholder-count="12">'
    '<sc-if value="{{x.isHead}}" hint-placeholder-val="{{false}}"><div class="sw-head {{x.lv}}">{{x.name}}</div></sc-if>'
    '<sc-if value="{{x.isStep}}" hint-placeholder-val="{{true}}"><button type="button" class="sw-st {{x.lv}}" aria-pressed="{{x.on}}" title="{{x.hint}}" onClick="{{x.pick}}"><span class="sti {{x.st}}" aria-hidden="true">{{x.glyph}}</span><span style="min-width: 0"><b>{{x.name}}</b><small>{{x.sub}}</small></span></button></sc-if>'
  '</sc-for></div>'
  '<div class="meta" style="white-space: normal; margin-top: 8px">Select a step to see only its lines.</div></div>')

CONSOLE = ('<div class="sw-con">'
  '<div class="sw-ch">'
    '<span class="sw-live {{sw_liveCls}}"><i></i>{{sw_liveLabel}}</span><span class="sw-n">{{sw_lines}}</span>'
    '<div role="tablist" aria-label="Console" class="row" style="gap: 6px"><sc-for list="{{sw_tabs}}" as="t" hint-placeholder-count="3"><button type="button" role="tab" class="sw-tab" aria-selected="{{t.on}}" onClick="{{t.pick}}">{{t.label}}</button></sc-for></div>'
    '<span style="flex: 1"></span>'
    '<sc-if value="{{sw_stepOn}}" hint-placeholder-val="{{false}}"><button type="button" class="sw-tab sw-stepchip" onClick="{{sw_stepOff}}" aria-label="Show all steps">{{sw_stepName}}' + I_X + '</button></sc-if>'
    '<label class="sw-flt"><input type="search" placeholder="Filter lines" aria-label="Filter lines" value="{{sw_filter}}" onChange="{{sw_onFilter}}"></label>'
    '<button type="button" class="ib sw-ib" aria-label="Download the log" title="Download the log" onClick="{{sw_download}}">' + I_DL + '</button>'
  '</div>'
  '<div class="sw-body" data-follow="{{sw_follow}}" tabindex="0" aria-label="Run log" aria-live="off">'
    # logs
    '<sc-if value="{{sw_tLogs}}" hint-placeholder-val="{{true}}">'
      '<sc-if value="{{sw_bannerOff}}" hint-placeholder-val="{{true}}"><button type="button" class="sw-fold" onClick="{{sw_bannerToggle}}"><span class="no">1–10</span><span>OpenHands SDK v1.30.0 · startup banner hidden</span><span class="sw-show">Show</span></button></sc-if>'
      '<sc-if value="{{sw_bannerOn}}" hint-placeholder-val="{{false}}"><sc-for list="{{sw_banner}}" as="b" hint-placeholder-count="10"><div class="sw-ln sw-bn"><span class="no">{{b.n}}</span><span class="bt">{{b.t}}</span></div></sc-for><button type="button" class="sw-fold" onClick="{{sw_bannerToggle}}"><span class="no"></span><span class="sw-show">Hide the banner</span></button></sc-if>'
      '<sc-for list="{{sw_log}}" as="l" hint-placeholder-count="8"><div class="sw-ln {{l.k}}"><span class="no">{{l.n}}</span><span class="tm">{{l.t}}</span><span class="wh {{l.wc}}">{{l.who}}</span><span class="ev">{{l.ev}}</span><span class="ms">{{l.msg}}</span></div></sc-for>'
      '<sc-if value="{{sw_noLines}}" hint-placeholder-val="{{false}}"><div class="sw-none">No line matches “{{sw_filter}}”.</div></sc-if>'
      '<sc-if value="{{sw_cursor}}" hint-placeholder-val="{{true}}"><div class="sw-ln"><span class="no"></span><span class="sw-cur" aria-hidden="true"></span></div></sc-if>'
    '</sc-if>'
    # tool calls
    '<sc-if value="{{sw_tTools}}" hint-placeholder-val="{{false}}">'
      '<div class="sw-tc sw-th"><span>Time</span><span>Agent</span><span>Tool</span><span>Arguments → result</span><span>Took</span></div>'
      '<sc-for list="{{sw_tools}}" as="c" hint-placeholder-count="6"><div class="sw-tc {{c.k}}"><span class="tm">{{c.t}}</span><span class="{{c.wc}}">{{c.who}}</span><span class="tl">{{c.tool}}</span><span class="ms">{{c.args}} → {{c.res}}</span><span class="tm">{{c.dur}}</span></div></sc-for>'
      '<sc-if value="{{sw_noTools}}" hint-placeholder-val="{{false}}"><div class="sw-none">No tool call yet.</div></sc-if>'
    '</sc-if>'
    # LLM calls
    '<sc-if value="{{sw_tLlm}}" hint-placeholder-val="{{false}}">'
      '<div class="sw-sumline">{{sw_llmSum}}</div>'
      '<div class="sw-tc sw-th"><span>Time</span><span>Agent</span><span>Purpose</span><span>Tokens</span><span>Took</span></div>'
      '<sc-for list="{{sw_llm}}" as="c" hint-placeholder-count="5"><div class="sw-tc"><span class="tm">{{c.t}}</span><span class="{{c.wc}}">{{c.who}}</span><span class="tl">{{c.purpose}}</span><span class="ms">{{c.tok}}</span><span class="tm">{{c.lat}}</span></div></sc-for>'
      '<sc-if value="{{sw_noLlm}}" hint-placeholder-val="{{false}}"><div class="sw-none">No LLM call yet.</div></sc-if>'
    '</sc-if>'
  '</div>'
  '<div class="sw-cf"><span>Model {{sw_r.model}} · self-hosted</span><span style="flex: 1"></span><sc-if value="{{sw_live}}" hint-placeholder-val="{{true}}"><button type="button" class="sw-tab" aria-pressed="{{sw_follow}}" onClick="{{sw_followToggle}}">{{sw_followLabel}}</button></sc-if></div>'
'</div>')

RUN = ('<sc-if value="{{sw_run}}" hint-placeholder-val="{{false}}"><div class="stack" style="gap: 16px">' + SUB + RESULT +
       '<div class="sw-grid">' + PIPE + CONSOLE + '</div></div></sc-if>')

SCREEN = ('<!-- ============ SWEEP · runs from a Jira ticket, agents pipeline, live console ============ -->'
          '<sc-if value="{{isSweep}}" hint-placeholder-val="{{false}}"><div class="stack" style="gap: 16px">' + LIST + RUN + '</div></sc-if>')

# ------------------------------------------------------------------ Launch a pipeline (overlay)
DIALOG = ('<sc-if value="{{sw_dlg}}" hint-placeholder-val="{{false}}"><div class="scrim" onClick="{{sw_closeDlg}}"></div>'
  '<div class="dlg sw-dlg" role="dialog" aria-modal="true" aria-label="New run">'
    '<div class="row" style="justify-content: space-between; margin-bottom: 4px"><h2 class="ui" style="margin: 0; font-size: 22px; line-height: 28px">New run</h2><button type="button" class="ib" aria-label="Close" style="margin: 0" onClick="{{sw_closeDlg}}">' + I_X.replace('16', '20') + '</button></div>'
    '<div class="fld {{sw_fTk}}"><label for="sw-tk">Jira ticket ID*</label><input id="sw-tk" type="text" autocomplete="off" placeholder="E2ECC-110995" value="{{sw_f.ticket}}" onChange="{{sw_onTk}}" aria-describedby="sw-tk-h" aria-invalid="{{sw_tkBad}}"></div>'
    '<div id="sw-tk-h" class="sw-help {{sw_tkHelpCls}}">{{sw_tkHelp}}</div>'
    '<sc-if value="{{sw_jira}}" hint-placeholder-val="{{false}}"><div class="sw-jira"><span class="tile in"><i></i>{{sw_j.type}}</span><div style="min-width: 0; flex: 1"><b class="ui" style="font-size: 14px">{{sw_j.title}}</b><div class="sw-sub">{{sw_j.team}} team · {{sw_j.ac}} acceptance criteria · {{sw_j.repos}}</div></div></div></sc-if>'
    '<div class="fld" style="margin-top: 16px"><label for="sw-br">Base branch*</label><input id="sw-br" type="text" value="{{sw_f.branch}}" onChange="{{sw_onBr}}" aria-describedby="sw-br-h"></div>'
    '<div id="sw-br-h" class="sw-help">Git base branch for diffs (default: develop)</div>'
    '<div class="fld" style="margin-top: 16px"><label for="sw-pj">Bitbucket project*</label><input id="sw-pj" type="text" value="{{sw_f.project}}" onChange="{{sw_onPj}}" aria-describedby="sw-pj-h"></div>'
    '<div id="sw-pj-h" class="sw-help">Bitbucket project where the target repositories are (default: E2ECC)</div>'
    '<div class="row" style="justify-content: flex-end; gap: 8px; margin-top: 20px"><button type="button" class="btn x" onClick="{{sw_closeDlg}}">Cancel</button><button type="button" class="btn f" aria-disabled="{{sw_cantGo}}" onClick="{{sw_dispatch}}">Start</button></div>'
  '</div></sc-if>')

CSS = r"""
.sw-tool{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.sw-q{display:flex;align-items:center;gap:8px;height:48px;width:280px;max-width:100%;box-sizing:border-box;padding:0 12px;border:1px solid #79757F;border-radius:12px;background:#FDF8FD;color:#48454E;cursor:text}
.sw-q input{flex:1;min-width:0;border:0;outline:0;background:transparent;font:400 15px/22px 'Open Sans',system-ui,sans-serif;color:#1C1B1E}
.sw-q:focus-within{border-color:#35307E;box-shadow:inset 0 0 0 1px #35307E}
.sw-sel{height:48px;min-width:180px;border-radius:12px}
.sw-new{background:#1D1A27!important;justify-content:center;min-width:132px}
.sw-tbl{width:100%;border-collapse:collapse;table-layout:fixed}
.sw-tbl .td{vertical-align:middle}
.sw-key{background:transparent;border:0;padding:0;font:700 14px/20px Manrope,'Segoe UI',system-ui,sans-serif;color:#35307E;cursor:pointer;text-align:left}
.sw-key:hover{text-decoration:underline}
.sw-ttl{font-size:13px;line-height:18px;color:#1C1B1E;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sw-sub{font-size:12px;line-height:16px;color:#48454E;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sw-tbl .tile{margin:0}
.sw-ai{height:32px;background:#9CF1F0;border-color:#9CF1F0;color:#002020;max-width:100%;overflow:hidden;text-overflow:ellipsis}
.sw-empty{display:flex;flex-direction:column;align-items:center;gap:8px;padding:48px 16px;text-align:center}
.sw-emic{width:72px;height:72px;border-radius:999px;background:#1D1A27;display:inline-flex;align-items:center;justify-content:center;margin-bottom:8px}
.sw-res{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:12px 16px;border-radius:12px;border:1px solid transparent}
.sw-res .tile{margin:0}
.sw-res.ok{background:#E8F7EE;border-color:#C3F4DC;color:#00391E}
.sw-res.err{background:#FFEDEA;border-color:#FFDAD6;color:#410002}
.sw-res.neu{background:#F2EBFA;border-color:#E6E0EC;color:#1C1B1E}
.sw-danger{background:#BA1A1A!important}
.sw-prs{display:flex;flex-direction:column;gap:0}
.sw-pr{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:10px 0;border-top:1px solid #E6E0EC}
.sw-pr:first-of-type{border-top:0}
.sw-sum{flex-basis:100%;box-sizing:border-box;margin-top:4px;padding:12px 16px;border-radius:12px;background:#F2FBFB;border:1px solid #9CF1F0}
.sw-sum ul{margin:0;padding-left:18px;font-size:13px;line-height:20px}
.sw-grid{display:grid;grid-template-columns:288px minmax(0,1fr);gap:16px;align-items:start}
.sw-pipe h3{margin:0;font-size:16px;line-height:24px;font-weight:700}
.sw-steps{display:flex;flex-direction:column;margin-top:8px}
.sw-st{display:flex;align-items:flex-start;gap:12px;width:100%;box-sizing:border-box;padding:6px 8px;border:0;border-radius:8px;background:transparent;text-align:left;cursor:pointer;color:#1C1B1E}
.sw-st:hover{background:rgba(53,48,126,.08)}
.sw-st[aria-pressed="true"]{background:#E3DFFF}
.sw-st b{display:block;font:600 14px/20px Manrope,'Segoe UI',system-ui,sans-serif}
.sw-st small{display:block;font:600 11px/16px Manrope,'Segoe UI',system-ui,sans-serif;letter-spacing:.2px;color:#48454E}
.sw-head{font:700 11px/16px Manrope,'Segoe UI',system-ui,sans-serif;letter-spacing:.6px;text-transform:uppercase;color:#48454E;padding:10px 8px 2px}
.sw-l1{margin-left:16px;width:calc(100% - 16px)}.sw-l2{margin-left:32px;width:calc(100% - 32px);border-left:2px solid #E6E0EC;border-radius:0 8px 8px 0}
.sti{flex:none;width:20px;height:20px;border-radius:999px;box-sizing:border-box;display:inline-flex;align-items:center;justify-content:center;font:700 12px/1 Manrope,system-ui,sans-serif;margin-top:2px}
.sti.pend{border:2px solid #79757F}.sti.notrun{border:2px solid #CAC4CF}.sti.skip,.sti.reused{border:2px dashed #79757F}
.sti.done{background:#006D3B;color:#FFFFFF}.sti.fail{background:#BA1A1A;color:#FFFFFF}.sti.cancel{background:#48454E;color:#FFFFFF}
.sti.run{border:2px solid #35307E;border-right-color:transparent;animation:sw-spin 1s linear infinite}
@keyframes sw-spin{to{transform:rotate(360deg)}}
@keyframes sw-pulse{50%{opacity:.35}}
@keyframes sw-blink{50%{opacity:0}}
.sw-con{background:#1D1A27;border-radius:16px;color:#E6E1E6;overflow:hidden;display:flex;flex-direction:column;min-width:0}
.sw-ch{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:10px 12px;border-bottom:1px solid #322F37}
.sw-live{display:inline-flex;align-items:center;gap:6px;font:700 12px/16px Manrope,system-ui,sans-serif;color:#7DDBA4;letter-spacing:.6px;text-transform:uppercase}
.sw-live i{width:8px;height:8px;border-radius:999px;background:#7DDBA4;animation:sw-pulse 1.6s ease-in-out infinite}
.sw-live.off{color:#A9A4AE}.sw-live.off i{background:#79757F;animation:none}
.sw-n{font-size:12px;color:#A9A4AE;margin-right:4px}
.sw-tab{height:32px;padding:0 12px;border-radius:8px;border:1px solid #48454E;background:transparent;color:#E6E1E6;font:600 13px/1 Manrope,system-ui,sans-serif;cursor:pointer;display:inline-flex;align-items:center;gap:6px;white-space:nowrap}
.sw-tab:hover{background:rgba(255,255,255,.08)}
.sw-tab[aria-selected="true"],.sw-tab[aria-pressed="true"]{background:#E3DFFF;border-color:#E3DFFF;color:#191836}
.sw-stepchip{border-color:#C4C0FF;color:#C4C0FF}
.sw-flt{display:flex;align-items:center;height:32px;padding:0 10px;border:1px solid #48454E;border-radius:8px;box-sizing:border-box}
.sw-flt input{background:transparent;border:0;outline:0;color:#E6E1E6;font:400 13px/18px 'Open Sans',system-ui,sans-serif;width:140px}
.sw-flt input::placeholder{color:#A9A4AE}
.sw-flt:focus-within{border-color:#C4C0FF}
.sw-ib{color:#E6E1E6!important;width:32px!important;height:32px!important;margin:0!important}
.sw-ib:hover{background:rgba(255,255,255,.08)!important}
.sw-body{height:520px;overflow:auto;padding:8px 0;font:400 12.5px/20px 'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;outline:0}
.sw-body:focus-visible{box-shadow:inset 0 0 0 2px #C4C0FF}
.sw-ln{display:grid;grid-template-columns:44px 72px 116px 80px minmax(0,1fr);gap:0 12px;padding:0 16px 0 0;white-space:pre-wrap;word-break:break-word}
.sw-ln:hover{background:rgba(255,255,255,.04)}
.sw-ln .no,.sw-fold .no{color:#79757F;text-align:right}
.sw-ln .tm,.sw-tc .tm{color:#A9A4AE}
.sw-ln .ev{color:#CAC4CF}
.sw-bn .bt{grid-column:2 / 6;color:#CAC4CF}
.w-master{color:#C4C0FF}.w-system{color:#A9A4AE}.w-caf{color:#9CF1F0}.w-jira{color:#FFDEA0}.w-fe{color:#9CF1F0}.w-be{color:#C3F4DC}.w-int{color:#F2B8D9}
.k-ok .ms{color:#7DDBA4}.k-warn .ms{color:#FFDEA0}.k-err .ms,.k-err .tl{color:#FFB4AB}.k-cancel .ms{color:#CAC4CF}
.sw-fold{display:grid;grid-template-columns:44px minmax(0,1fr) auto;gap:0 12px;width:100%;padding:2px 16px 2px 0;margin:0 0 4px;border:0;background:rgba(255,255,255,.04);color:#A9A4AE;font:inherit;text-align:left;cursor:pointer}
.sw-fold:hover{background:rgba(255,255,255,.08)}
.sw-show{color:#C4C0FF;font-weight:600}
.sw-cur{display:inline-block;width:8px;height:16px;margin-top:2px;background:#E6E1E6;animation:sw-blink 1s step-end infinite;grid-column:2}
.sw-none{padding:16px;color:#A9A4AE}
.sw-tc{display:grid;grid-template-columns:72px 116px 168px minmax(0,1fr) 56px;gap:0 12px;padding:2px 16px;white-space:pre-wrap;word-break:break-word}
.sw-tc .tl{color:#C4C0FF}
.sw-th{color:#A9A4AE;font-family:Manrope,system-ui,sans-serif;font-size:11px;font-weight:700;letter-spacing:.6px;text-transform:uppercase;padding-bottom:6px}
.sw-sumline{padding:4px 16px 10px;color:#E6E1E6}
.sw-cf{display:flex;align-items:center;gap:8px;min-height:44px;padding:6px 12px;border-top:1px solid #322F37;font-size:12px;color:#A9A4AE}
.sw-dlg{width:520px!important}
.sw-help{font-size:12px;line-height:16px;color:#48454E;padding:4px 16px 0}
.sw-help.bad{color:#BA1A1A}
.fld.bad{border-color:#BA1A1A;box-shadow:inset 0 0 0 1px #BA1A1A}
.fld.bad label{color:#BA1A1A}
.sw-jira{display:flex;gap:12px;align-items:flex-start;margin-top:8px;padding:10px 12px;border-radius:12px;background:#FFFFFF;border:1px solid #E6E0EC}
.sw-jira .tile{margin:0}
@media (prefers-reduced-motion: reduce){.sti.run{animation:none;border-right-color:#35307E;border-style:dotted}.sw-live i,.sw-cur{animation:none}}
@container win (max-width: 1199px){
.sw-grid{grid-template-columns:minmax(0,1fr)}
.sw-steps{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:2px 8px}
.sw-steps .sw-head{grid-column:1 / -1}
.sw-l1,.sw-l2{margin-left:0;width:100%}
.sw-body{height:440px}
}
@container win (max-width: 839px){
.sw-tbl colgroup,.sw-tbl thead{display:none}
.sw-tbl,.sw-tbl tbody{display:block}
.sw-tbl tr{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:6px 12px;padding:12px 16px;border-top:1px solid #CAC4CF}
.sw-tbl tr:first-child{border-top:0}
.sw-tbl td{display:block;border:0!important;height:auto!important;padding:0!important;min-width:0}
.sw-tbl td:nth-child(2){text-align:right}
.sw-tbl td:nth-child(3){grid-column:1 / 3}
.sw-tbl td:nth-child(5){text-align:right;align-self:end}
.sw-q{width:100%;flex:1 1 100%}
.sw-sel{flex:1}
.sw-ln{grid-template-columns:32px 64px minmax(0,1fr)}
.sw-ln .ev{display:none}
.sw-ln .ms{grid-column:3}
.sw-bn .bt{grid-column:2 / 4}
.sw-tc{grid-template-columns:64px minmax(0,1fr)}
.sw-tc>span:nth-child(3),.sw-tc>span:nth-child(5){display:none}
.sw-tc .ms{grid-column:1 / 3;padding-bottom:6px}
.sw-flt{flex:1}.sw-flt input{width:100%}
.sw-body{height:400px}
.sw-steps{grid-template-columns:minmax(0,1fr)}
}
"""

JS = r'''
  // ---------------- Sweep: runs from a Jira ticket, the agents' pipeline, the live console ----------------
  swDefaults() {
    return { view: 'list', run: null, q: '', status: 'all', dlg: false, f: { ticket: '', branch: 'develop', project: 'E2ECC' }, tried: false, tab: 'logs', filter: '', step: null,
      banner: false, follow: true, sum: null, rate: {}, prog: { r1: 5 }, extra: [], cancelled: {}, confirm: false };
  }
  // runs and their scripted events (deterministic: the same state always gives the same logs)
  swModel() {
    var s = this.state, W = Object.assign({}, this.swDefaults(), s.sw || {});
    var BASE = [
      { id: 'r1', key: 'E2ECC-103894', title: 'Show covenant breaches on the facility page', team: 'Facility', fe: 'facility-portal', be: 'facility-service', feFiles: ['covenant-breaches-panel.component.ts', 'facility-page.routes.ts'], beFiles: ['CovenantBreachQuery.java', 'FacilityController.java'], api: 'facility.yaml', fePr: 198, bePr: 412, by: 'Aurélien Heux', t0: '11:10:51', started: '2 min ago', live: true },
      { id: 'r2', key: 'E2ECC-103870', title: 'Add the margin grid to the credit request summary', team: 'Request', fe: 'request-portal', be: 'request-service', feFiles: ['margin-grid.component.ts', 'request-summary.page.ts'], beFiles: ['MarginGridService.java', 'RequestSummaryController.java'], api: 'request.yaml', fePr: 87, bePr: 301, by: 'Priya Sharma', t0: '10:22:04', started: '48 min ago' },
      { id: 'r3', key: 'E2ECC-103861', title: 'Expose collateral valuations to the limit-service', team: 'Facility', fe: null, be: 'collateral-service', beFiles: ['ValuationController.java', 'collateral.yaml'], api: 'collateral.yaml', bePr: 233, by: 'Yann Dupont', t0: '09:41:37', started: '1 h ago', fail: true },
      { id: 'r4', key: 'E2ECC-103855', title: 'Fix the date format on the client page', team: 'Client', fe: 'client-portal', be: null, feFiles: ['client-header.component.ts', 'date-format.pipe.ts'], api: 'client.yaml', fePr: 142, by: 'Marta Kowalski', t0: '08:57:12', started: '2 h ago' },
      { id: 'r5', key: 'E2ECC-103842', title: 'Rename the facility status labels', team: 'Facility', fe: 'facility-portal', be: 'facility-service', feFiles: ['facility-status.labels.ts', 'facility-list.component.ts'], beFiles: ['FacilityStatus.java', 'FacilityMapper.java'], api: 'facility.yaml', fePr: 197, bePr: 409, by: 'Karim Ouali', t0: '16:03:40', started: 'yesterday', cancelAt: 21, cancelBy: 'Karim Ouali' }
    ];
    var pad = function (n) { return (n < 10 ? '0' : '') + n; };
    var toS = function (t) { var p = t.split(':'); return +p[0] * 3600 + +p[1] * 60 + +p[2]; };
    var fmt = function (x) { return pad(Math.floor(x / 3600) % 24) + ':' + pad(Math.floor(x / 60) % 60) + ':' + pad(x % 60); };
    var dur = function (x) { return x < 60 ? x + ' s' : Math.floor(x / 60) + ' min' + (x % 60 ? ' ' + (x % 60) + ' s' : ''); };
    var hash = function (str) { var h = 7, i; for (i = 0; i < str.length; i++) h = (h * 31 + str.charCodeAt(i)) % 1000003; return h; };
    var sha = function (seed) { return ('0000000' + (hash(seed) * 2654435761 % 268435456).toString(16)).slice(-7); };
    var between = function (seed, lo, hi) { return lo + hash(seed) % (hi - lo + 1); };
    var statsOf = function (r, p) {
      var fe = p === 'fe', seed = r.key + p, l1 = between(seed + 'a', fe ? 60 : 40, fe ? 160 : 120), l2 = between(seed + 'b', fe ? 30 : 30, fe ? 90 : 110), del = between(seed + 'd', 2, 24);
      var files = fe ? r.feFiles : r.beFiles, nFiles = files.length + between(seed + 'f', 0, 2);
      return { base: sha(r.key + (fe ? r.fe : r.be)), commit: sha(seed + 'c'), l1: l1, l2: l2, diff: nFiles + ' files · +' + (l1 + l2) + ' −' + del, passed: between(seed + 't', fe ? 40 : 150, fe ? 95 : 320), added: between(seed + 'n', 2, 8),
        planLat: (4 + between(seed + 'p', 0, 38) / 10).toFixed(1) + ' s', codeLat: (11 + between(seed + 'w', 0, 90) / 10).toFixed(1) + ' s', revLat: (5 + between(seed + 'r', 0, 40) / 10).toFixed(1) + ' s', testTook: between(seed + 's', fe ? 14 : 26, fe ? 40 : 58) + ' s', sugg: between(seed + 'g', 0, 3) };
    };
    var script = function (r) {
      var E = [], sec = toS(r.t0), t0 = sec;
      var add = function (step, who, ev, msg, kind, x, dt) { E.push({ step: step, who: who, ev: ev, msg: msg, kind: kind || '', x: x || null, s: sec, t: fmt(sec) }); sec += (dt == null ? 3 : dt); };
      var T = function (step, who, tool, args, res, took, dt, kind) { add(step, who, 'tool', tool + ' ' + args + ' → ' + res, kind, { tool: tool, args: args, res: res, dur: took }, dt); };
      var L = function (step, who, purpose, tin, tout, lat, dt) { add(step, who, 'llm', purpose + ' · ' + tin + ' in · ' + tout + ' out · ' + lat, '', { purpose: purpose, tin: tin, tout: tout, lat: lat }, dt); };
      add('orch', 'system', 'telemetry', 'egress guards applied', '', null, 0);
      add('orch', 'system', 'startup', 'ai-dev-pipeline v0.9.0-dev0', '', null, 1);
      add('orch', 'caffeinate', 'start', 'systemd-inhibit unavailable, skipped', 'warn', null, 0);
      add('orch', 'master', 'start', r.key + (r.attempt > 1 ? ' · attempt ' + r.attempt : '') + ' · ' + r.branch + ' · ' + r.project, '', null, 0);
      add('orch', 'master', 'model', 'openai/qwen3.6-27b', '', null, 2);
      if (r.from) {
        add('orch', 'master', 'reuse', 'planner, coder and reviewer results from attempt ' + (r.attempt - 1), '', null, 2);
      } else {
        add('jira', 'jira-planner', 'start', 'reading ' + r.key, '', null, 1);
        T('jira', 'jira-planner', 'jira.get_issue', r.key, 'Story · ' + r.team + ' · 4 acceptance criteria', '0.6 s', 2);
        T('jira', 'jira-planner', 'bitbucket.list_repos', 'project=' + r.project, '23 repositories', '0.4 s', 3);
        L('jira', 'jira-planner', 'split the ticket into tracks', '3.1k', '640', '4.2 s', 5);
        add('jira', 'jira-planner', 'plan', r.fe && r.be ? '2 tracks · frontend ' + r.fe + ' · backend ' + r.be : (r.fe ? '1 track · frontend ' + r.fe + ' · no backend change' : '1 track · backend ' + r.be + ' · no frontend change'), 'ok', null, 1);
        add('orch', 'master', 'fork', r.fe && r.be ? 'frontend ∥ backend' : (r.fe ? 'frontend only' : 'backend only'), '', null, 1);
        var track = function (p, repo, files, pr, test) {
          var w = function (role) { return p + '-' + role; }, q = [], st = statsOf(r, p);
          q.push(['add', p + '_plan', w('planner'), 'start', repo + ' @ ' + r.branch]);
          q.push(['T', p + '_plan', w('planner'), 'git.clone', repo, r.branch + ' @ ' + st.base, '1.8 s', 2]);
          q.push(['L', p + '_plan', w('planner'), 'plan the change', p === 'fe' ? '4.2k' : '5.4k', p === 'fe' ? '730' : '910', st.planLat, Math.round(parseFloat(st.planLat))]);
          q.push(['add', p + '_plan', w('planner'), 'plan', files.length + ' files · ' + files.join(', '), 'ok']);
          q.push(['add', p + '_code', w('coder'), 'start', 'branch feature/' + r.key.toLowerCase()]);
          q.push(['T', p + '_code', w('coder'), 'fs.write', files[0], '+' + st.l1 + ' lines', '0.1 s', 2]);
          q.push(['L', p + '_code', w('coder'), 'write the code', p === 'fe' ? '7.6k' : '8.2k', p === 'fe' ? '1.8k' : '2.1k', st.codeLat, Math.round(parseFloat(st.codeLat))]);
          q.push(['T', p + '_code', w('coder'), 'fs.write', files[1], '+' + st.l2 + ' lines', '0.1 s', 2]);
          q.push(['T', p + '_code', w('coder'), test[0], repo, st.passed + ' passed · ' + st.added + ' added', st.testTook, parseInt(st.testTook, 10)]);
          q.push(['add', p + '_code', w('coder'), 'commit', st.commit + ' · ' + st.diff, 'ok']);
          q.push(['add', p + '_rev', w('reviewer'), 'start', 'diff against ' + r.branch]);
          q.push(['L', p + '_rev', w('reviewer'), 'review the diff', p === 'fe' ? '5.1k' : '6.0k', p === 'fe' ? '700' : '820', st.revLat, Math.round(parseFloat(st.revLat))]);
          q.push(['add', p + '_rev', w('reviewer'), 'review', '0 blocking · ' + (st.sugg === 1 ? '1 suggestion' : st.sugg + ' suggestions'), 'ok']);
          q.push(['T', p + '_rev', w('reviewer'), 'bitbucket.create_pr', repo, (r.fail ? 'draft #' : '#') + pr + ' · review summary posted', '1.2 s', 2]);
          return q;
        };
        var A = r.fe ? track('fe', r.fe, r.feFiles, r.fePr, ['npm run test']) : [];
        var B = r.be ? track('be', r.be, r.beFiles, r.bePr, ['mvn -q test']) : [];
        var run = function (e) { if (e[0] === 'add') add(e[1], e[2], e[3], e[4], e[5] || '', null, 3); else if (e[0] === 'T') T(e[1], e[2], e[3], e[4], e[5], e[6], e[7]); else L(e[1], e[2], e[3], e[4], e[5], e[6], e[7]); };
        for (var i = 0; i < Math.max(A.length, B.length); i++) { if (B[i]) run(B[i]); if (A[i]) run(A[i]); }
        add('orch', 'master', 'join', r.fe && r.be ? 'frontend and backend done' : 'track done', '', null, 1);
      }
      add('integ', 'integration', 'start', 'contract and smoke checks', '', null, 2);
      if (r.fail && !r.from) {
        T('integ', 'integration', 'contract.verify', r.api + ' vs limit-service client', '1 breaking change · valuationDate renamed to valuedOn', '3.4 s', 4, 'err');
        add('integ', 'integration', 'failed', 'breaking change for limit-service · pull request left in draft', 'err', null, 1);
        add('orch', 'master', 'failed', 'at integration check · 1 draft pull request · ' + dur(sec - t0), 'err', null, 0);
      } else {
        T('integ', 'integration', 'contract.verify', r.api + (r.from ? ' (updated in #' + (r.bePr + 2) + ')' : ''), '0 breaking changes', '3.1 s', 4);
        T('integ', 'integration', 'e2e.smoke', 'preview-' + r.key.toLowerCase(), '6/6 passed', '48 s', 49);
        add('integ', 'integration', 'done', 'all checks passed', 'ok', null, 1);
        var n = (r.fe ? 1 : 0) + (r.be ? 1 : 0);
        add('orch', 'master', 'done', r.from ? 'integration check passed · pull request ready for review · ' + dur(sec - t0 + 1) : n + ' pull request' + (n > 1 ? 's' : '') + ' opened · review summaries posted · ' + dur(sec - t0 + 1), 'ok', null, 0);
      }
      return E;
    };
    var runs = W.extra.concat(BASE).map(function (r0) {
      var r = Object.assign({ branch: 'develop', project: 'E2ECC', attempt: 1 }, r0), full = script(r), E = full;
      var cut = r.cancelAt || W.cancelled[r.id];
      if (cut) { var last = full[cut - 1]; E = full.slice(0, cut).concat([{ step: 'orch', who: 'master', ev: 'cancel', msg: 'cancelled by ' + (r.cancelBy || 'Aurélien Heux') + ' · nothing pushed', kind: 'cancel', x: null, s: last.s + 2, t: fmt(last.s + 2) }]); }
      var n = cut ? E.length : (r.live ? Math.min(W.prog[r.id] || 0, E.length) : E.length);
      var end = n >= E.length, fin = E[E.length - 1];
      var status = cut ? 'Cancelled' : !end ? 'Running' : (fin.kind === 'err' ? 'Failed' : 'Succeeded');
      return Object.assign(r, { full: full, E: E, n: n, status: status, cut: cut, t0s: toS(r.t0), stats: { fe: r.fe ? statsOf(r, 'fe') : null, be: r.be ? statsOf(r, 'be') : null } });
    });
    return { W: W, runs: runs, fmt: fmt, dur: dur };
  }
  sweepTick() {
    var s = this.state; if (s.screen !== 'sweep' || s.tourId) return;
    var M = this.swModel(), W = M.W, prog = Object.assign({}, W.prog), ch = false, fin = null;
    M.runs.forEach(function (r) { if (r.live && !r.cut && r.n < r.E.length) { prog[r.id] = r.n + 1; ch = true; if (r.n + 1 === r.E.length && r.mine) fin = r; } });
    if (!ch) return;
    var o = { sw: Object.assign({}, s.sw || {}, { prog: prog }) };
    if (fin) {
      var bad = fin.E[fin.E.length - 1].kind === 'err';
      o.snack = { text: fin.key + (bad ? ' failed at the integration check.' : ' finished: ' + fin.E[fin.E.length - 1].msg.split(' · ')[0] + '.'), action: '', act: '' };
      if (!s.microSent && !s.microShown) { o.micro = true; o.microShown = true; o.microV = null; o.snack = null; }
    }
    this.setState(o);
  }
  sweepVals(ctx) {
    var s = this.state, self = this, set = ctx.set, val = ctx.val, ON = ctx.ON;
    var M = this.swModel(), W = M.W, fmt = M.fmt, dur = M.dur;
    var put = function (patch) { return Object.assign({}, self.state.sw || {}, patch); };
    var sw = function (patch, extra) { return set(function (e) { var p = typeof patch === 'function' ? patch(e) : patch; return Object.assign({ sw: put(p) }, extra || {}); }); };
    var NOW = 13 * 3600 + 5 * 60;
    var STEPS = [ ['orch', 'SWEEP orchestrator', ''], ['jira', 'Jira planner', ''], ['#par', 'In parallel', ''], ['#fe', 'Frontend', 'sw-l1'], ['fe_plan', 'Planner', 'sw-l2'], ['fe_code', 'Coder', 'sw-l2'], ['fe_rev', 'Reviewer', 'sw-l2'],
      ['#be', 'Backend', 'sw-l1'], ['be_plan', 'Planner', 'sw-l2'], ['be_code', 'Coder', 'sw-l2'], ['be_rev', 'Reviewer', 'sw-l2'], ['integ', 'Integration check', ''] ];
    var LONG = { orch: 'SWEEP orchestrator', jira: 'Jira planner', fe_plan: 'Planner · frontend', fe_code: 'Coder · frontend', fe_rev: 'Reviewer · frontend', be_plan: 'Planner · backend', be_code: 'Coder · backend', be_rev: 'Reviewer · backend', integ: 'Integration check' };
    var GLY = { done: '✓', fail: '×', cancel: '–' };
    var stateOf = function (r, k) {
      var inFull = r.full.some(function (e) { return e.step === k; });
      var ended = r.status !== 'Running';
      if (k === 'orch') { var st0 = { Running: 'run', Succeeded: 'done', Failed: 'fail', Cancelled: 'cancel' }[r.status]; return { st: st0, a: 0, b: r.n - 1 }; }
      if (!inFull) return { st: r.from && k !== 'integ' ? 'reused' : 'skip' };
      var first = -1, lastF = -1, i;
      for (i = 0; i < r.E.length; i++) if (r.E[i].step === k) { if (first < 0) first = i; }
      for (i = 0; i < r.full.length; i++) if (r.full[i].step === k) lastF = i;
      if (first < 0 || first >= r.n) return { st: ended ? 'notrun' : 'pend' };
      if (lastF < r.n && !(r.cut && lastF >= r.cut)) return { st: r.E[lastF].kind === 'err' ? 'fail' : 'done', a: first, b: lastF };
      return { st: ended ? 'cancel' : 'run', a: first, b: Math.min(r.n, r.E.length) - 1 };
    };
    var subOf = function (r, k, x) {
      var took = x.a != null && x.b != null && x.b >= x.a ? dur(Math.max(1, r.E[x.b].s - r.E[x.a].s)) : '';
      return { run: 'Running' + (took ? ' · ' + took : ''), done: 'Done' + (took ? ' · ' + took : ''), fail: k === 'integ' ? 'Failed · 1 breaking change' : 'Failed' + (took ? ' · ' + took : ''), cancel: 'Cancelled' + (k === 'orch' && took ? ' · ' + took : ''), pend: 'Pending', notrun: 'Not run', skip: 'Not needed', reused: 'Reused from attempt ' + (r.attempt - 1) }[x.st];
    };
    var nowOf = function (r) {
      if (r.status === 'Running') { var on = ['jira', 'fe_plan', 'fe_code', 'fe_rev', 'be_plan', 'be_code', 'be_rev', 'integ'].filter(function (k) { return stateOf(r, k).st === 'run'; }).map(function (k) { return LONG[k]; }); return on.length ? on.join(', ') : (r.n < 6 ? 'Starting' : 'SWEEP orchestrator'); }
      if (r.status === 'Failed') return 'at Integration check';
      if (r.status === 'Cancelled') { var c = ['fe_code', 'be_code', 'fe_rev', 'be_rev', 'fe_plan', 'be_plan', 'jira'].filter(function (k) { return stateOf(r, k).st === 'cancel'; })[0]; return (c ? 'at ' + LONG[c] : 'before the agents started') + ' · by ' + (r.cancelBy || 'Aurélien Heux'); }
      return r.from ? 'integration check only' : 'all checks passed';
    };
    var prsOf = function (r) {
      return r.E.slice(0, r.n).filter(function (e) { return e.x && e.x.tool === 'bitbucket.create_pr'; }).map(function (e) {
        var fe = e.step.indexOf('fe') === 0; return { repo: e.x.args, num: fe ? r.fePr : r.bePr, draft: r.status === 'Failed', fe: fe, title: r.key + ' · ' + r.title, diff: (fe ? r.stats.fe : r.stats.be).diff }; });
    };
    var elapsed = function (r) { var a = r.E[0].s; return dur(Math.max(1, r.E[r.status === 'Running' ? Math.max(0, r.n - 1) : r.E.length - 1].s - a)); };
    var TILE = { Running: 'in', Succeeded: 'ok', Failed: 'er', Cancelled: 'ne' };
    var openRun = function (id, patch) { return sw(Object.assign({ view: 'run', run: id, step: null, filter: '', tab: 'logs', sum: null, confirm: false, follow: true }, patch || {}), ctx.closeAll); };

    // ---- list
    var q = (W.q || '').trim().toLowerCase();
    var rows = M.runs.filter(function (r) { return (!q || (r.key + ' ' + r.title).toLowerCase().indexOf(q) >= 0) && (W.status === 'all' || r.status === W.status); });
    var anchored = false;
    var R = {};
    R.sw_rows = rows.map(function (r) {
      var p = prsOf(r), a = '';
      if (p.length && !anchored && r.status === 'Succeeded') { a = 'sweep.summary'; anchored = true; }
      return { key: r.key, title: r.title, status: r.status, tile: TILE[r.status], now: nowOf(r), started: r.started, by: r.by, dur: r.status === 'Running' ? '—' : elapsed(r),
        prs: p.length ? (p.length + ' PR' + (p.length > 1 ? 's' : '') + (p[0].draft ? ' · draft' : '') + ' · summary') : (r.status === 'Running' ? 'Not yet' : 'None'), hasPr: !!p.length, noPr: !p.length, anchor: a,
        open: openRun(r.id), openSum: openRun(r.id, { sum: r.id + ':0' }) };
    });
    R.sw_hasRows = rows.length > 0; R.sw_noRows = !rows.length;
    var nRun = M.runs.filter(function (r) { return r.status === 'Running'; }).length;
    R.sw_count = M.runs.length + ' runs · ' + nRun + ' running';
    R.sw_q = W.q; R.sw_status = W.status;
    R.sw_onQ = sw(function (e) { return { q: val(e) }; }); R.sw_onStatus = sw(function (e) { return { status: val(e) }; });
    R.sw_clear = sw({ q: '', status: 'all' });
    R.sw_refresh = set({ snack: { text: 'Runs are up to date.', action: '', act: '' } });
    R.sw_list = W.view !== 'run'; R.sw_run = W.view === 'run';

    // ---- dialog
    var JIRA = { 'E2ECC-110995': { title: 'Notify the relationship manager when a facility nears expiry', team: 'Facility', type: 'Story', ac: 4, fe: 'facility-portal', be: 'facility-service', feFiles: ['expiry-banner.component.ts', 'facility-page.routes.ts'], beFiles: ['FacilityExpiryJob.java', 'NotificationClient.java'], api: 'facility.yaml', fePr: 199, bePr: 414 },
      'E2ECC-110870': { title: 'Show the client risk rating on the request page', team: 'Request', type: 'Story', ac: 3, fe: 'request-portal', be: null, feFiles: ['risk-rating.component.ts', 'request-page.component.ts'], api: 'request.yaml', fePr: 88 },
      'E2ECC-110812': { title: 'Store the collateral haircut per asset class', team: 'Facility', type: 'Story', ac: 5, fe: null, be: 'collateral-service', beFiles: ['HaircutPolicy.java', 'collateral.yaml'], api: 'collateral.yaml', bePr: 236 } };
    var F = Object.assign({ ticket: '', branch: 'develop', project: 'E2ECC' }, W.f), key = (F.ticket || '').trim().toUpperCase();
    var fmtOk = /^[A-Z][A-Z0-9]+-\d+$/.test(key), J = JIRA[key] || null;
    var busy = M.runs.filter(function (r) { return r.key === key && r.status === 'Running'; })[0];
    var help = 'The ticket the agents work from, for example E2ECC-110995', bad = false;
    if (key && !fmtOk) { help = 'Use the Jira key: project, dash, number (E2ECC-110995).'; bad = true; }
    else if (fmtOk && busy) { help = key + ' is already running. Open it from the list, or cancel it first.'; bad = true; }
    else if (fmtOk && !J) { help = 'No ticket ' + key + ' in Jira. Check the key, or the project you can read.'; bad = true; }
    else if (!key && W.tried) { help = 'Enter the Jira ticket ID.'; bad = true; }
    var canGo = !!J && !busy && !!(F.branch || '').trim() && !!(F.project || '').trim();
    R.sw_dlg = !!W.dlg; R.sw_f = F; R.sw_tkHelp = help; R.sw_tkBad = bad; R.sw_tkHelpCls = bad ? 'bad' : ''; R.sw_fTk = bad ? 'bad' : '';
    R.sw_jira = !!J && !busy; R.sw_j = J ? Object.assign({}, J, { repos: [J.fe, J.be].filter(Boolean).join(' · ') }) : { title: '', team: '', type: '', ac: 0, repos: '' };
    R.sw_cantGo = !canGo;
    R.sw_openDlg = sw({ dlg: true, tried: false, f: { ticket: '', branch: 'develop', project: 'E2ECC' } }, ctx.closeAll);
    R.sw_closeDlg = sw({ dlg: false });
    R.sw_onTk = sw(function (e) { return { f: Object.assign({}, F, { ticket: val(e) }) }; });
    R.sw_onBr = sw(function (e) { return { f: Object.assign({}, F, { branch: val(e) }) }; });
    R.sw_onPj = sw(function (e) { return { f: Object.assign({}, F, { project: val(e) }) }; });
    var newRun = function (base, patch) {
      var n = W.extra.length + 1, id = 'n' + n, m = NOW + n * 7;
      var r = Object.assign({}, base, { id: id, by: 'Aurélien Heux', t0: fmt(m), started: 'just now', live: true, mine: true, cancelAt: null, cancelBy: null, fail: false, from: null }, patch || {});
      var prog = Object.assign({}, W.prog); prog[id] = 1;
      return { extra: [r].concat(W.extra), prog: prog, view: 'run', run: id, dlg: false, step: null, filter: '', tab: 'logs', sum: null, confirm: false, follow: true };
    };
    R.sw_dispatch = set(function () {
      if (!canGo) return { sw: put({ tried: true }) };
      return { sw: put(newRun(Object.assign({ key: key, branch: F.branch.trim(), project: F.project.trim().toUpperCase() }, J))), snack: { text: 'Dispatched job sweep-' + key.toLowerCase() + '. Follow the agents here.', action: '', act: '' } };
    });

    // ---- run page
    var cur = M.runs.filter(function (r) { return r.id === W.run; })[0] || M.runs[0];
    var r = cur, P = prsOf(r);
    var fin = r.E[r.E.length - 1];
    var doneSteps = ['jira', 'fe_plan', 'fe_code', 'fe_rev', 'be_plan', 'be_code', 'be_rev', 'integ'].filter(function (k) { return r.full.some(function (e) { return e.step === k; }); });
    var nDone = doneSteps.filter(function (k) { return stateOf(r, k).st === 'done'; }).length;
    R.sw_r = { key: r.key, title: r.title, status: r.status, tile: TILE[r.status], project: r.project, model: 'openai/qwen3.6-27b',
      ctx: r.title + ' · started ' + r.started + ' · ' + r.branch + ' · job sweep-' + r.key.toLowerCase() + (r.attempt > 1 ? '-' + r.attempt : ''),
      canCancel: r.status === 'Running' && !W.confirm, canRerun: r.status === 'Succeeded' || r.status === 'Cancelled',
      isOk: r.status === 'Succeeded', isFail: r.status === 'Failed', isCancel: r.status === 'Cancelled',
      resTitle: r.status === 'Succeeded' ? (r.from ? 'Integration check passed in ' + elapsed(r) : P.length + ' pull request' + (P.length > 1 ? 's' : '') + ' opened in ' + elapsed(r)) : r.status === 'Failed' ? 'Failed at the integration check' : 'Cancelled ' + nowOf(r),
      resText: r.status === 'Succeeded' ? (r.from ? 'The contract check now passes with the updated ' + r.api + '. The pull request is ready for review.' : 'Ready for review.')
        : r.status === 'Failed' ? 'contract.verify found 1 breaking change in ' + r.api + ': valuationDate is renamed to valuedOn and limit-service still reads valuationDate. The pull request stays in draft. Keep the old field for one release, push to the same branch, then re-run from the integration check.'
        : 'The agents stopped. Nothing was pushed and no pull request was opened.',
      stepsDone: nDone + ' of ' + doneSteps.length + ' steps' };
    R.sw_back = sw({ view: 'list', confirm: false }, ctx.closeAll);
    R.sw_confirm = !!W.confirm && r.status === 'Running';
    R.sw_askCancel = sw({ confirm: true }); R.sw_keep = sw({ confirm: false });
    R.sw_cancel = set(function () { var c = Object.assign({}, W.cancelled); c[r.id] = r.n; return { sw: put({ cancelled: c, confirm: false }), snack: { text: r.key + ' is cancelled. Nothing was pushed.', action: '', act: '' } }; });
    var base = { key: r.key, title: r.title, team: r.team, fe: r.fe, be: r.be, feFiles: r.feFiles, beFiles: r.beFiles, api: r.api, fePr: r.fePr, bePr: r.bePr, branch: r.branch, project: r.project, attempt: (r.attempt || 1) + 1 };
    R.sw_rerun = set(function () { return { sw: put(newRun(base)), snack: { text: 'Re-running ' + r.key + ' from the start (attempt ' + base.attempt + ').', action: '', act: '' } }; });
    R.sw_rerunFrom = set(function () { return { sw: put(newRun(base, { from: 'integ' })), snack: { text: 'Re-running ' + r.key + ' from the integration check (attempt ' + base.attempt + ').', action: '', act: '' } }; });

    R.sw_hasPrs = P.length > 0;
    R.sw_prs = P.map(function (p, i) {
      var k = r.id + ':' + i, open = W.sum === k, rt = W.rate[k] || null;
      var points = p.fe ? [ { k: 'What changed', v: 'a ' + p.repo + ' component and its route, from the acceptance criteria of ' + r.key + '.' }, { k: 'Tests', v: r.stats.fe.passed + ' passed, ' + r.stats.fe.added + ' added (npm run test).' }, { k: 'Risk', v: 'low · UI only, behind the existing facility page.' }, { k: 'Suggestions', v: r.stats.fe.sugg ? r.stats.fe.sugg + ' · empty state wording, an aria-label on the table.' : 'none' } ]
        : [ { k: 'What changed', v: 'a query and an endpoint in ' + p.repo + '; ' + r.api + ' gains one operation.' }, { k: 'Tests', v: r.stats.be.passed + ' passed, ' + r.stats.be.added + ' added (mvn -q test).' }, { k: 'Risk', v: r.status === 'Failed' ? 'high · breaks the limit-service client (see the integration check).' : 'low · additive API change, contract check passed.' }, { k: 'Suggestions', v: r.stats.be.sugg ? r.stats.be.sugg + ' · a null check on the breach date.' : 'none' } ];
      var rate = function (v) { return set(function () { var m = Object.assign({}, W.rate); m[k] = v; return { sw: put({ rate: m }), ck: Object.assign({}, self.state.ck || {}, { ck2: true }), snack: { text: 'Thanks. Your rating goes to the platform team.', action: '', act: '' } }; }); };
      return Object.assign({}, p, { open: open, anchor: i === 0 ? 'sweep.summary' : '', points: points, toggle: sw({ sum: open ? null : k }), bb: set({ snack: { text: 'Opens ' + p.repo + ' #' + p.num + ' in Bitbucket.', action: '', act: '' } }),
        up: rt === 'up', down: rt === 'down', upS: rt === 'up' ? ON : '', downS: rt === 'down' ? ON : '', rated: !!rt, rateUp: rate('up'), rateDown: rate('down') });
    });

    R.sw_steps = STEPS.filter(function (d) { if (d[0] === '#fe' || /^fe_/.test(d[0])) return !!r.fe; if (d[0] === '#be' || /^be_/.test(d[0])) return !!r.be; if (d[0] === '#par') return !!(r.fe && r.be); return true; }).map(function (d) {
      if (d[0].charAt(0) === '#') return { isHead: true, isStep: false, name: d[0] === '#fe' ? 'Frontend · ' + r.fe : d[0] === '#be' ? 'Backend · ' + r.be : d[1], lv: (r.fe && r.be) ? d[2] : '' };
      var x = stateOf(r, d[0]), on = W.step === d[0];
      return { isHead: false, isStep: true, name: d[1], lv: (r.fe && r.be) || !d[2] ? d[2] : 'sw-l1', st: x.st, glyph: GLY[x.st] || '', sub: subOf(r, d[0], x), on: on, hint: 'Show only ' + LONG[d[0]] + ' lines', pick: sw({ step: on ? null : d[0], tab: 'logs' }) };
    });

    // ---- console
    var WHO = function (w) { return w === 'master' ? 'w-master' : w === 'system' ? 'w-system' : w === 'caffeinate' ? 'w-caf' : w === 'jira-planner' ? 'w-jira' : w.indexOf('fe-') === 0 ? 'w-fe' : w.indexOf('be-') === 0 ? 'w-be' : 'w-int'; };
    var shown = r.E.slice(0, r.n), f = (W.filter || '').trim().toLowerCase();
    var keep = function (e) { return (!W.step || e.step === W.step) && (!f || (e.who + ' ' + e.ev + ' ' + e.msg).toLowerCase().indexOf(f) >= 0); };
    var KC = { ok: 'k-ok', warn: 'k-warn', err: 'k-err', cancel: 'k-cancel' };
    R.sw_log = shown.map(function (e, i) { return { e: e, n: 11 + i }; }).filter(function (o) { return keep(o.e); }).map(function (o) { var e = o.e; return { n: o.n, t: e.t, who: e.who, wc: WHO(e.who), ev: e.ev, msg: e.msg, k: KC[e.kind] || '' }; });
    R.sw_noLines = !R.sw_log.length && !!(f || W.step);
    var BAN = ['+' + new Array(58).join('-') + '+', '|  OpenHands SDK v1.30.0', '|', '|  Report a bug: github.com/OpenHands/software-agent-sdk/issues', '|  Get help: openhands.dev/joinslack', '|  Scale up: openhands.dev/product/sdk', '|', '|  Set OPENHANDS_SUPPRESS_BANNER=1 to hide this message', '+' + new Array(58).join('-') + '+', ''];
    R.sw_banner = BAN.map(function (t, i) { return { n: i + 1, t: t }; });
    R.sw_bannerOn = !!W.banner && !W.step && !f; R.sw_bannerOff = !W.banner && !W.step && !f; R.sw_bannerToggle = sw({ banner: !W.banner });
    var tools = shown.filter(function (e) { return e.ev === 'tool'; }), llm = shown.filter(function (e) { return e.ev === 'llm'; });
    R.sw_tools = tools.filter(keep).map(function (e) { return { t: e.t, who: e.who, wc: WHO(e.who), tool: e.x.tool, args: e.x.args, res: e.x.res, dur: e.x.dur, k: KC[e.kind] || '' }; });
    R.sw_llm = llm.filter(keep).map(function (e) { return { t: e.t, who: e.who, wc: WHO(e.who), purpose: e.x.purpose, tok: e.x.tin + ' in · ' + e.x.tout + ' out', lat: e.x.lat }; });
    var kn = function (v) { return parseFloat(v) * (/k$/.test(v) ? 1000 : 1); }, tin = 0, tout = 0;
    llm.forEach(function (e) { tin += kn(e.x.tin); tout += kn(e.x.tout); });
    R.sw_llmSum = llm.length ? llm.length + ' calls · ' + (tin / 1000).toFixed(1) + 'k tokens in · ' + (tout / 1000).toFixed(1) + 'k out · openai/qwen3.6-27b, self-hosted' : 'No LLM call yet.';
    R.sw_noTools = !R.sw_tools.length; R.sw_noLlm = !R.sw_llm.length;
    R.sw_tabs = [ ['logs', 'Logs'], ['tools', 'Tool calls (' + tools.length + ')'], ['llm', 'LLM calls (' + llm.length + ')'] ].map(function (t) { return { label: t[1], on: W.tab === t[0], pick: sw({ tab: t[0] }) }; });
    R.sw_tLogs = W.tab === 'logs'; R.sw_tTools = W.tab === 'tools'; R.sw_tLlm = W.tab === 'llm';
    var live = r.status === 'Running';
    R.sw_live = live; R.sw_liveCls = live ? '' : 'off'; R.sw_liveLabel = live ? 'Live' : r.status;
    R.sw_lines = (10 + r.n) + ' lines'; R.sw_cursor = live && W.tab === 'logs' && !f && !W.step;
    R.sw_follow = live && W.follow !== false; R.sw_followLabel = W.follow !== false ? 'Following new lines' : 'Follow new lines';
    R.sw_followToggle = sw({ follow: W.follow === false });
    R.sw_filter = W.filter; R.sw_onFilter = sw(function (e) { return { filter: val(e) }; });
    R.sw_stepOn = !!W.step; R.sw_stepName = W.step ? LONG[W.step] : ''; R.sw_stepOff = sw({ step: null });
    R.sw_download = set({ snack: { text: 'sweep-' + r.key.toLowerCase() + '.log downloaded (' + (10 + r.n) + ' lines).', action: '', act: '' } });

    // ---- header, assistant context
    R.sw_hdr = W.view === 'run' ? ['Sweep · ' + r.key, r.status + ' · ' + (r.status === 'Running' ? nowOf(r) : r.title)] : ['Sweep · Runs', M.runs.length + ' runs · ' + nRun + ' running · Bitbucket project E2ECC'];
    R.sw_ctx = W.view === 'run' ? 'Sweep · ' + r.key : 'Sweep · Runs';
    R.sw_sugg = W.view === 'run' ? (r.status === 'Failed' ? ['Why did ' + r.key + ' fail?', 'Re-run ' + r.key + ' from the integration check'] : r.status === 'Running' ? ['What are the agents doing on ' + r.key + '?', 'Summarise the plan of the Jira planner'] : ['Summarise what the agents changed on ' + r.key, 'Why did E2ECC-103861 fail?'])
      : ['Why did E2ECC-103861 fail?', 'Re-run E2ECC-103861 from the integration check', 'What are the agents doing on E2ECC-103894?'];
    R.goSweep = set(Object.assign({ screen: 'sweep', tourId: null, sw: put({ view: 'list', dlg: false, confirm: false }) }, ctx.closeAll));
    return R;
  }
  // assistant: answers about runs (null when the question is not about a run)
  swAnswer(l) {
    var M = this.swModel(), W = M.W, runs = M.runs;
    var m = l.match(/e2ecc-\d+/), r = null;
    if (m) r = runs.filter(function (x) { return x.key.toLowerCase() === m[0]; })[0] || null;
    if (!r && /agents|plan of the jira planner|what changed/.test(l)) r = runs.filter(function (x) { return x.id === W.run; })[0] || runs.filter(function (x) { return x.status === 'Running'; })[0];
    if (!r && /why .*fail|failed run|run fail/.test(l)) r = runs.filter(function (x) { return x.status === 'Failed'; })[0];
    if (!r) return null;
    var done = function (k) { return r.E.slice(0, r.n).some(function (e) { return e.step === k && (e.ev === 'plan' || e.ev === 'commit' || e.ev === 'review' || e.ev === 'done'); }); };
    var trace = [['SW', 'Read the log of ' + r.key]];
    if (r.status === 'Failed') { trace.push(['SW', 'Read the integration check output']); return { trace: trace, answer: r.key + ' failed at the integration check: contract.verify found 1 breaking change in ' + r.api + '. valuationDate is renamed to valuedOn, and limit-service still reads valuationDate. The pull request ' + r.be + ' #' + r.bePr + ' stays in draft.\nNext: keep valuationDate as a deprecated field for one release, push to the same branch, then re-run from the integration check (about 1 minute).' }; }
    if (r.status === 'Running') {
      if (/plan/.test(l) && done('jira')) return { trace: trace, answer: 'The Jira planner read ' + r.key + ' (4 acceptance criteria) and split it into ' + (r.fe && r.be ? 'two tracks running in parallel: frontend on ' + r.fe + ' and backend on ' + r.be : 'one track on ' + (r.fe || r.be)) + '. Each track goes Planner → Coder → Reviewer, then the integration check verifies the ' + r.api + ' contract and runs the smoke tests.' };
      var on = r.E.slice(0, r.n).filter(function (e) { return e.ev === 'start'; }).map(function (e) { return e.who; });
      var last = r.E[r.n - 1];
      return { trace: trace, answer: r.key + ' has been running since ' + r.t0 + '. ' + (done('jira') ? 'The Jira planner is done (' + (r.fe && r.be ? '2 tracks' : '1 track') + '). ' : 'The Jira planner is reading the ticket. ') + 'Last line: ' + last.who + ' · ' + last.ev + ' · ' + last.msg + '.' + (on.indexOf('integration') < 0 ? ' The integration check comes last.' : '') };
    }
    if (r.status === 'Cancelled') return { trace: trace, answer: r.key + ' was cancelled by ' + (r.cancelBy || 'you') + ' while the coders were working. Nothing was pushed and no pull request was opened. Re-run it from the run page when you are ready.' };
    return { trace: trace, answer: r.key + ' succeeded' + (r.from ? ' (integration check only)' : '') + '. ' + (r.fe ? 'Frontend: ' + r.fe + ' #' + r.fePr + ', 0 blocking, 2 suggestions. ' : '') + (r.be ? 'Backend: ' + r.be + ' #' + r.bePr + ', 0 blocking, 1 suggestion. ' : '') + 'The contract check passed and the smoke tests ran 6/6. Each pull request carries a review summary.' };
  }
'''
