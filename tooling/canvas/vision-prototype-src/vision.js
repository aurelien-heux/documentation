  // =====================================================================================================
  // AIToolbox production vision: Catalog (screens and admin), Environments, Docs, and the assistant pane.
  // State lives in s.cat (catalog) and s.as (assistant); the catalog's "Add to my assistant" feeds the
  // assistant's Tools menu, and Deploy / Reserve on Environments send their request to the assistant.
  // =====================================================================================================
  visionVals(ctx) {
    var s = this.state, self = this, set = ctx.set, val = ctx.val, ON = ctx.ON, role = ctx.role;
    var C = Object.assign({ tab: 'browse', kind: 'all', skill: 'm1', added: { m1: true, m2: true, t1: true, t3: true }, step: 1, nsName: '', nsDesc: '', nsBody: '', nsEx1: '', nsTools: { t_logs: true, t_jira: true }, src: 'app', scope: 'team', tryAppr: false, published: null, aTab: 'review', rv: null, rvChecks: {}, pol: {}, sweepOn: { s1: { coder: true }, m1: { coder: true, integration: true }, m2: { jira: true, planner: true, reviewer: true }, t1: { integration: true }, t3: { jira: true, reviewer: true } } }, s.cat || {});
    var A = Object.assign({ open: false, turns: [], draft: '', menu: false, off: {} }, s.as || {});
    // patch helpers: cset({catPatch}, {topLevelPatch}); aset likewise for the assistant
    var cset = function (p, top) { return set(function (e) { var pp = typeof p === 'function' ? p(e) : p; return Object.assign({ cat: Object.assign({}, self.state.cat || {}, pp) }, top || {}); }); };
    var catNow = function () { return Object.assign({}, C, self.state.cat || {}); };
    var asNow = function () { return Object.assign({}, A, self.state.as || {}); };
    var snack = function (t) { return { snack: { text: t, action: '', act: '' } }; };
    var V = {};

    // ---------------- catalog data ----------------
    var TOOLS = {
      t_deploy: { name: 'Deploy environment', write: true, src: 'Environments' }, t_reserve: { name: 'Reserve environment', write: true, src: 'Environments' },
      t_jira: { name: 'Create Jira ticket', write: true, src: 'Jira' }, t_logs: { name: 'Read run logs', write: false, src: 'Sweep' },
      t_pipe: { name: 'Run pipeline', write: true, src: 'DevOps' }, t_pipestat: { name: 'Read pipeline status', write: false, src: 'DevOps' },
      t_build: { name: 'Read build logs', write: false, src: 'DevOps' }, t_pr: { name: 'Open pull request', write: true, src: 'DevOps' },
      t_kb: { name: 'Search the knowledge base', write: false, src: 'Knowledge base' }, t_arch: { name: 'Query the architecture model', write: false, src: 'Knowledge base' }
    };
    var ITEMS = [
      { id: 'm1', kind: 'MCP server', name: 'DevOps', by: 'Platform team', team: 'Platform', aud: 'Everyone', usage: 3100, version: '2.3', tools: ['t_pipestat', 't_build', 't_pipe', 't_pr'], works: ['Assistant', 'Sweep'], desc: 'Pipelines, builds, deployments and pull requests on the DevOps platform.', examples: ['Why did the credit-request pipeline fail last night?', 'Re-run lint-api on main'], source: 'MCP · devops.example.internal', reviewed: true },
      { id: 'm2', kind: 'MCP server', name: 'Knowledge base', by: 'Platform team', team: 'Platform', aud: 'Everyone', usage: 2480, version: '1.4', tools: ['t_kb', 't_arch'], works: ['Assistant', 'Sweep'], desc: 'Docs, runbooks, the architecture model and ARB decisions, searched and read with their source. Reads only.', examples: ['What is the rollback procedure for facility-management?', 'Which modules depend on client-referential?'], source: 'MCP · kb.example.internal', reviewed: true },
      { id: 't1', kind: 'Tool', name: 'Deploy environment', by: 'Environments team', team: 'Release', aud: 'Everyone', usage: 860, version: '1.2', tools: ['t_deploy'], works: ['Assistant', 'Sweep'], desc: 'Deploys a module branch or a release to an environment: checks reservations, opens the auto-merge pull request and follows the first rollout.', examples: ['Deploy credit-request 4.6.1 to staging-2'], source: 'Built-in · Environments', reviewed: true },
      { id: 't2', kind: 'Tool', name: 'Reserve environment', by: 'Environments team', team: 'Release', aud: 'Everyone', usage: 310, version: '1.2', tools: ['t_reserve'], works: ['Assistant'], desc: 'Reserves an environment for a module until a date, with a reason; extend or release it later.', examples: ['Reserve staging-2 until Friday'], source: 'Built-in · Environments', reviewed: true },
      { id: 't3', kind: 'Tool', name: 'Create Jira ticket', by: 'Platform team', team: 'Platform', aud: 'Everyone', usage: 640, version: '2.1', tools: ['t_jira'], works: ['Assistant', 'Sweep'], desc: 'Creates a ticket in the project of the repository, with the run or the conversation attached as context.', examples: ['Open a Jira ticket for the flaky facility export test'], source: 'Jira connector', reviewed: true },
      { id: 's1', kind: 'Skill', name: 'Spring Boot 3 migration', by: 'Marta Kowalski', team: 'Client', aud: 'Everyone', usage: 212, version: '1.4.0', tools: ['t_logs', 't_pipe', 't_pr'], works: ['Assistant', 'Sweep'], desc: 'Upgrades a service to Spring Boot 3, runs the pipeline and opens a pull request with what changed.', examples: ['Migrate credit-request to Spring Boot 3 on a branch'], source: 'Git · client/skill-spring-boot-3', reviewed: true },
      { id: 's2', kind: 'Skill', name: 'Incident runbook', by: 'Lucas Bernard', team: 'Facility', aud: 'Everyone', usage: 188, version: '1.1.0', tools: ['t_kb', 't_logs', 't_jira'], works: ['Assistant'], desc: 'Walks the on-call engineer through the incident checklist with the right runbook, recent logs, and a ticket at the end.', examples: ['Facility exports are failing since 02:00, where do I start?'], source: 'Written in the app', reviewed: true },
      { id: 's3', kind: 'Skill', name: 'Release notes from changelog', by: 'Sami Ben Ali', team: 'Platform', aud: 'Everyone', usage: 356, version: '2.0.1', tools: ['t_pipestat', 't_kb'], works: ['Assistant'], desc: 'Drafts a What’s new entry from the changelog and the pull request summaries.', examples: ['Draft the release notes for 4.6.1'], source: 'Git · platform/skill-release-notes', reviewed: true },
      { id: 's4', kind: 'Skill', name: 'Deploy to staging with checks', by: 'Karim Ouali', team: 'Request', aud: 'Request', usage: 41, version: '0.4.0', tools: ['t_pipestat', 't_reserve', 't_deploy'], works: ['Assistant', 'Sweep'], desc: 'Checks the pipeline is green, reserves a staging environment if needed, deploys, then reports the rollout.', examples: ['Ship my branch to staging'], source: 'Written in the app', reviewed: false },
      { id: 's5', kind: 'Skill', name: 'Flaky test triage', by: 'you', team: 'Request', aud: 'Just you', usage: 6, version: '0.1.0', tools: ['t_logs', 't_jira'], works: ['Assistant'], desc: 'Finds tests that fail only sometimes, groups them by cause and opens one ticket per cause.', examples: ['Which tests were flaky this week on credit-request?'], source: 'Written in the app', mine: true, stage: 'Draft' },
      { id: 's6', kind: 'Skill', name: 'Liquibase changelog review', by: 'Yann Dupont', team: 'Environments', aud: 'Everyone', usage: 0, version: '1.0.0', tools: ['t_kb', 't_jira'], works: ['Assistant', 'Sweep'], desc: 'Reviews a Liquibase changelog: destructive changes, missing rollbacks, naming.', examples: ['Review the changelog in PR #4830'], source: 'Git · environments/skill-liquibase-review', stage: 'In review' }
    ];
    var byId = function (id) { return ITEMS.filter(function (it) { return it.id === id; })[0]; };
    var KAB = { Skill: 'SK', Tool: 'TL', 'MCP server': 'MCP' }, KCLS = { Skill: 'k-skill', Tool: 'k-tool', 'MCP server': 'k-mcp' };
    var lower = function (t) { return t.charAt(0).toLowerCase() + t.slice(1); };
    var goItem = function (id) { return set(function () { return Object.assign({ screen: 'catalog', cat: Object.assign({}, self.state.cat || {}, { view: 'item', skill: id }) }, ctx.closeAll); }); };
    var deco = function (it) { return Object.assign({}, it, { kab: KAB[it.kind], kcls: KCLS[it.kind], byShort: it.kind === 'Skill' ? it.by + ' · ' + it.team : it.by, usageShort: it.usage ? it.usage.toLocaleString('en') + ' uses' : 'Not used yet', audience: it.aud, open: goItem(it.id) }); };
    var published = ITEMS.filter(function (it) { return !it.stage && (it.aud === 'Everyone' || it.aud === 'Request'); });
    var view = C.view || 'list', onCat = s.screen === 'catalog';

    V.cat_sCatalog = onCat && view === 'list'; V.cat_sItem = onCat && view === 'item'; V.cat_sNew = onCat && view === 'new';
    V.cat_cTabs = [ { k: 'browse', label: 'Browse' }, { k: 'mine', label: 'My skills', n: 1 + (C.published ? 0 : 0) } ].map(function (t) { var on = C.tab === t.k; return { label: t.label, n: t.n, hasN: !!t.n, on: on, cls: on ? 'tab-on' : '', pick: cset({ tab: t.k }) }; });
    V.cat_tBrowse = C.tab === 'browse'; V.cat_tMine = C.tab === 'mine';
    V.cat_kindChips = [ { k: 'all', label: 'All' }, { k: 'Skill', label: 'Skills' }, { k: 'Tool', label: 'Tools' }, { k: 'MCP server', label: 'MCP servers' } ].map(function (k) { return { label: k.label, on: C.kind === k.k, pick: cset({ kind: k.k }) }; });
    V.cat_items = published.filter(function (it) { return C.kind === 'all' || it.kind === C.kind; }).sort(function (a, b) { return b.usage - a.usage; }).map(deco);
    var STAGE_TILE = { Draft: 'ne', 'In review': 'wn', Published: 'ok' };
    var mineRaw = ITEMS.filter(function (it) { return it.mine; });
    if (C.published) mineRaw = [ { id: 'sNew', kind: 'Skill', name: C.nsName || 'Flaky test triage', by: 'you', team: 'Request', aud: C.published.aud, usage: 0, version: '1.0.0', tools: [], works: ['Assistant'], desc: C.nsDesc, examples: [], stage: C.published.stage } ];
    V.cat_mine = mineRaw.map(function (it) { var st = it.stage || 'Published'; return Object.assign(deco(it), { stage: st, stTile: STAGE_TILE[st], nextLabel: st === 'Draft' ? 'Continue' : st === 'In review' ? 'Open' : 'New version', next: st === 'Draft' ? cset({ view: 'new', step: 1, nsName: it.name, nsDesc: it.desc, nsEx1: it.examples[0] || '', published: null }) : goItem('s5') }); });
    V.cat_cTabs[1].n = V.cat_mine.length; V.cat_cTabs[1].hasN = true;
    V.cat_goNew = cset({ view: 'new', step: 1, published: null, tryAppr: false }); V.cat_goCatalog = cset({ view: 'list' });

    // item page
    var skRaw = byId(C.skill) || ITEMS[0], sk = deco(skRaw), added = !!C.added[sk.id], writes = sk.tools.filter(function (k) { return TOOLS[k].write; });
    Object.assign(sk, { by: sk.kind === 'Skill' ? sk.by + ' · ' + sk.team : sk.by, version: 'v' + sk.version,
      forAssistant: sk.works.indexOf('Assistant') >= 0, added: added, addLabel: added ? 'In my assistant' : 'Add to my assistant', addCls: added ? 't' : 'f',
      toggleAdd: set(function () { var c = catNow(), a = Object.assign({}, c.added); a[sk.id] = !added; return Object.assign({ cat: Object.assign({}, self.state.cat || {}, { added: a }) }, snack(!added ? sk.name + ' is in your assistant’s Tools menu.' : sk.name + ' removed from your assistant.')); }),
      writes: writes.length > 0, writeNote: 'Asks before it does anything that changes something: ' + writes.map(function (k) { return lower(TOOLS[k].name); }).join(', ') + '.',
      hasEx: sk.examples.length > 0, examples: sk.examples.map(function (t) { return { text: t, tryIt: set(function () { return self.asAsk(t, true); }) }; }),
      toolsTitle: sk.kind === 'MCP server' ? 'Tools it provides' : sk.kind === 'Tool' ? 'Action' : 'Uses',
      tools: sk.tools.map(function (k) { var t = TOOLS[k]; return { name: t.name, note: (t.write ? 'changes something · ' : '') + t.src }; }),
      foot: [sk.reviewed ? 'Reviewed' : (sk.stage || (sk.aud === 'Everyone' ? '' : 'Shared with ' + sk.aud)), sk.usage ? sk.usage.toLocaleString('en') + ' uses in 30 days' : '', sk.works.join(' and '), sk.source].filter(Boolean).join(' · ') });
    var qaAs = role === 'platform' ? { who: 'Aurélien Heux', role: 'Platform team' } : null;
    var SKQA = { s1: [ { id: 'vq1', ini: 'YD', bg: '#C3F4DC', who: 'Yann Dupont', when: '2 days ago', d: 2, text: 'Does it handle Spring Security 6 config, or do we do that by hand?', r: [ { id: 'vq1a', ini: 'MK', bg: '#9CF1F0', who: 'Marta Kowalski', role: 'Author', when: 'yesterday', d: 1, text: 'Since 1.4.0 it rewrites the common patterns and stops to ask on anything custom.' } ] } ], m1: [ { id: 'vq2', ini: 'NR', bg: '#E3DFFF', who: 'Nadia Rahal', when: 'yesterday', d: 1, text: 'Can it read pipelines of repositories my team does not own?', r: [ { id: 'vq2a', ini: 'SB', bg: '#FFDEA0', who: 'Sami Ben Ali', role: 'Platform team', when: 'today', d: 0.3, text: 'Only those you can open on the DevOps platform: it uses your own rights.' } ] } ] };
    Object.assign(sk, this.qaVals('cat-' + sk.id, SKQA[sk.id] || [], 'Ask the author or share how it went…', qaAs, false));
    V.cat_sk = sk; V.cat_reportIt = set(snack('Reported to Community › Feedback with the item and its version attached.'));

    // publish a skill
    var stepName = ['Write', 'Test', 'Submit', 'Review', 'Published'], skipped = C.published && C.scope !== 'org';
    V.cat_proc = stepName.map(function (l, i) { var n = i + 1; return { n: n, label: l, cls: n === C.step ? 'on' : (n < C.step && !(n === 4 && skipped) ? 'done' : ''), cur: n === C.step ? 'step' : 'false', more: i < stepName.length - 1 }; });
    ['nWrite', 'nTest', 'nSubmit', 'nReview', 'nDone'].forEach(function (k, i) { V['cat_' + k] = C.step === i + 1; });
    var nsTools = Object.keys(TOOLS).filter(function (k) { return C.nsTools[k]; }), nsWrites = nsTools.filter(function (k) { return TOOLS[k].write; });
    ['nsName', 'nsDesc', 'nsBody', 'nsEx1'].forEach(function (k) { V['cat_' + k] = C[k]; V['cat_on' + k.charAt(0).toUpperCase() + k.slice(1)] = cset(function (e) { var o = {}; o[k] = val(e); return o; }); });
    V.cat_toolChips = ['t_logs', 't_kb', 't_pipestat', 't_jira', 't_deploy', 't_pr'].map(function (k) { var on = !!C.nsTools[k]; return { label: TOOLS[k].name, on: on, style: on ? ON : '', pick: cset(function () { var t = Object.assign({}, catNow().nsTools); t[k] = !on; return { nsTools: t }; }) }; });
    V.cat_srcLink = C.src === 'git' ? 'Reading devops.example.internal/request/skill-flaky-tests · write here instead' : 'Or import from a Git repository'; V.cat_pickSrcGit = cset({ src: C.src === 'git' ? 'app' : 'git' });
    V.cat_saveDraft = set(snack('Draft saved in Mine.')); V.cat_toWrite = cset({ step: 1 }); V.cat_toTest = cset({ step: 2 }); V.cat_toSubmit = cset({ step: 3 });
    var nsNameOr = C.nsName || 'Flaky test triage'; V.cat_nsNameOr = nsNameOr; V.cat_nsEx1Or = C.nsEx1 || 'Which tests were flaky this week on credit-request?';
    var G = '#006D3B', Am = '#7A5900';
    V.cat_checks = [ { label: 'Manifest', note: 'Name, one line, ' + nsTools.length + ' tools, 1 example', icon: '✓', color: G }, { label: 'No secrets in the text', note: 'Instructions and example scanned', icon: '✓', color: G },
      { label: 'Tools exist', note: nsTools.map(function (k) { return TOOLS[k].name; }).join(', ') || 'None: instructions only', icon: '✓', color: G },
      { label: nsWrites.length ? 'Changes something' : 'Reads only', note: nsWrites.length ? 'Because of ' + nsWrites.map(function (k) { return TOOLS[k].name; }).join(', ') + '. It will ask first.' : 'Worked out from its tools', icon: nsWrites.length ? '!' : '✓', color: nsWrites.length ? Am : G } ];
    var wTool = nsWrites[0], tt = nsTools.slice(0, 3).map(function (k) { var t = TOOLS[k]; return { name: t.name, st: t.write ? (C.tryAppr ? 'done' : 'waiting for you') : 'done' }; });
    V.cat_tryN = tt.length; V.cat_tryTools = tt; V.cat_tryNeedsAppr = !!wTool && !C.tryAppr; V.cat_tryApprQ = wTool ? TOOLS[wTool].name + '?' : ''; V.cat_tryApprArgs = wTool === 't_jira' ? 'project SWP · “Flaky: FacilityExportTest” · Bug' : 'credit-request · feature/flaky · staging-2'; V.cat_tryApprove = cset({ tryAppr: true });
    V.cat_tryAnswer = wTool && !C.tryAppr ? 'Three tests in FacilityExportTest fail on and off, all for one cause: a fixed timestamp in the fixture. I can ' + lower(TOOLS[wTool].name) + ' once you approve.' : 'Three tests in FacilityExportTest fail on and off, all for one cause: a fixed timestamp in the fixture. Fix: use the test clock.' + (wTool === 't_jira' ? ' Ticket SWP-1288 created.' : '');
    V.cat_scopes = [ { k: 'me', label: 'Just me', note: 'Live at once, for you only.' }, { k: 'team', label: 'My team · Request', note: 'Live at once. Your team is responsible for it.' }, { k: 'org', label: 'Everyone', note: 'A platform admin reviews it first.' } ].map(function (x) { var on = C.scope === x.k; return Object.assign(x, { on: on, cls: on ? 'on' : '', pick: cset({ scope: x.k }) }); });
    V.cat_scopeOrg = C.scope === 'org'; V.cat_submitCta = C.scope === 'org' ? 'Send for review' : 'Publish';
    V.cat_submit = cset(function () { var org = catNow().scope === 'org'; return { step: org ? 4 : 5, published: { aud: org ? 'Everyone, once reviewed' : ({ me: 'Just you', team: 'Request' }[catNow().scope]), stage: org ? 'In review' : 'Published' } }; });
    V.cat_simulateApprove = cset({ step: 5, published: { aud: 'Everyone', stage: 'Published' } }); V.cat_openMine = cset({ view: 'list', tab: 'mine' });
    var pubAud = C.published ? C.published.aud : '';
    V.cat_doneText = '“' + nsNameOr + '” is published for ' + ({ 'Just you': 'you', Everyone: 'everyone' }[pubAud] || 'your team') + '. It is in the assistant’s Tools menu now; a new version goes through Test again.';

    // admin pages: Core › Catalog and Sweep › Tools and skills
    var akey = ctx.akey;
    var aDefs = [ { k: 'review', label: 'Review', n: 2 }, { k: 'items', label: 'Items' }, { k: 'policies', label: 'Policies' } ];
    var aTab = C.aTab;
    V.cat_aCatalog = ctx.isA && akey === 'catalog';
    V.cat_aTabs = aDefs.map(function (t) { var on = aTab === t.k; return { label: t.label, n: t.n, hasN: !!t.n, on: on, cls: on ? 'tab-on' : '', pick: cset({ aTab: t.k, rv: null }) }; });
    V.cat_aReview = V.cat_aCatalog && aTab === 'review'; V.cat_aItems = V.cat_aCatalog && aTab === 'items'; V.cat_aPolicies = V.cat_aCatalog && aTab === 'policies'; V.cat_aSweep = ctx.isA && akey === 'stools';
    V.cat_rvList = !C.rv; V.cat_rvOpen = !!C.rv;
    V.cat_queue = [ { id: 's6', name: 'Liquibase changelog review', by: 'Yann Dupont · Environments', when: '2 days ago', desc: 'Destructive changes, missing rollbacks, naming.' }, { id: 'q2', name: 'Explain a failed quality gate', by: 'Emma Laurent · Docs', when: 'yesterday', desc: 'Says what to fix first, with the lines.' } ].map(function (q) { return Object.assign(q, { open: cset({ rv: q.id }) }); });
    var rvDefs = [ 'I tried it and it does what it says', 'No sensitive data in the instructions or the example', 'The actions that change something are needed' ];
    V.cat_rvChecks = rvDefs.map(function (l, i) { var on = !!C.rvChecks[i]; return { label: l, on: on, toggle: cset(function () { var c = Object.assign({}, catNow().rvChecks); c[i] = !on; return { rvChecks: c }; }) }; });
    var rvReady = rvDefs.every(function (l, i) { return C.rvChecks[i]; });
    var rv = { name: 'Liquibase changelog review', by: 'Yann Dupont · Environments', when: 'submitted 2 days ago', body: '1. Read the changelog files in the pull request.\n2. Flag destructive changes and changesets without a rollback.\n3. Check naming against the conventions in the knowledge base.\n4. For anything blocking, create one Jira ticket in the project of the repository and link it in the review.', tools: 'Search the knowledge base, Create Jira ticket', note: 'tried on 6 pull requests in Environments' };
    Object.assign(rv, this.qaVals('cat-rv-s6', [ { id: 'vrq1', ini: 'MK', bg: '#9CF1F0', who: 'Marta Kowalski', role: 'Champion', when: 'yesterday', d: 1, text: 'One ticket per pull request, not one per finding?', r: [ { id: 'vrq1a', ini: 'YD', bg: '#C3F4DC', who: 'Yann Dupont', role: 'Author', when: 'today', d: 0.3, text: 'Yes, step 4 says one ticket; the other findings go in the review comment.' } ] } ], 'Write to the author…', qaAs || { who: 'Aurélien Heux', role: '' }, false));
    V.cat_rv = rv; V.cat_rvBack = cset({ rv: null }); V.cat_rvNotReady = !rvReady;
    V.cat_rvPublish = rvReady ? cset({ rv: null }, snack('Liquibase changelog review is published for everyone. Yann Dupont is notified.')) : set({});
    V.cat_rvChanges = cset({ rv: null }, snack('Yann Dupont sees your request in the skill’s discussion.'));
    V.cat_adminItems = ITEMS.filter(function (it) { return C.kind === 'all' || it.kind === C.kind; }).map(deco);
    V.cat_policyRows = [ ['t_deploy', 'ask', 'ask'], ['t_reserve', 'ask', 'off'], ['t_jira', 'ask', 'always'], ['t_pipe', 'ask', 'always'], ['t_pr', 'ask', 'always'] ].map(function (w) { var k = w[0], pk = C.pol[k] || {}; return { name: TOOLS[k].name, src: TOOLS[k].src, a: pk.a || w[1], s: pk.s || w[2], onA: cset(function (e) { var p = Object.assign({}, catNow().pol); p[k] = Object.assign({}, pk, { a: val(e) }); return { pol: p }; }), onS: cset(function (e) { var p = Object.assign({}, catNow().pol); p[k] = Object.assign({}, pk, { s: val(e) }); return { pol: p }; }) }; });
    var PH = ['jira', 'planner', 'coder', 'reviewer', 'integration']; V.cat_phases = ['Jira planner', 'Planner', 'Coder', 'Reviewer', 'Integration check'];
    V.cat_sweepRows = ITEMS.filter(function (it) { return it.works.indexOf('Sweep') >= 0 && !it.stage && it.aud === 'Everyone'; }).map(function (it) { var d = deco(it), on = C.sweepOn[it.id] || {}; return { name: it.name, kab: d.kab, kcls: d.kcls, cells: PH.map(function (p) { var v = !!on[p]; return { on: v, aria: it.name + ' in ' + p, toggle: cset(function () { var all = Object.assign({}, catNow().sweepOn); all[it.id] = Object.assign({}, on); all[it.id][p] = !v; return { sweepOn: all }; }) }; }) }; });

    // ---------------- Environments and Docs ----------------
    V.vEnv = s.screen === 'env'; V.vDocs = s.screen === 'docs';
    // Environments (CTX-ENV): non-production only; a Placement is a branch; what runs is observed, with its source and time
    var ENVS = [
      { id: 'dev', tier: 'Development · Upstream environment', upstream: null, tracked: 'develop', mode: 'automatic' },
      { id: 'int', tier: 'Integration · Upstream environment', upstream: null, tracked: 'release/4.6', mode: 'team-triggered' },
      { id: 'dev-1', tier: 'Development', upstream: 'dev' }, { id: 'dev-2', tier: 'Development', upstream: 'dev' },
      { id: 'staging-1', tier: 'Staging', upstream: 'int' }, { id: 'staging-2', tier: 'Staging', upstream: 'int' } ];
    var ENV_APPS = { 'credit-request': ['request-service', 'request-portal'], facility: ['facility-service', 'facility-portal'], collateral: ['collateral-service'], client: ['client-portal', 'client-referential'] };
    var LOCAL = { 'dev-1': { 'request-service': 'feature/e2ecc-103870', 'request-portal': 'feature/e2ecc-103870' }, 'dev-2': { 'facility-portal': 'feature/e2ecc-103894' }, 'staging-1': { 'request-service': 'hotfix/4.6.1' } };
    var RES = { 'staging-1': { holder: 'Lucas Bernard · Facility', scope: 'application facility', until: 'Fri 18:00', mine: false }, 'dev-2': { holder: 'Aurélien Heux', scope: 'module facility-portal', until: 'today 18:00', mine: true } };
    var VER = { develop: '4.7.0-SNAPSHOT', 'release/4.6': '4.6.0', 'hotfix/4.6.1': '4.6.1-rc1' };
    var hsh = function (str) { var h = 7, i; for (i = 0; i < str.length; i++) h = (h * 31 + str.charCodeAt(i)) % 1000003; return h; };
    var shaOf = function (seed) { return ('0000000' + (hsh(seed) * 2654435761 % 268435456).toString(16)).slice(-7); };
    var E = Object.assign({ app: 'credit-request' }, s.env || {});
    var envApp = ENV_APPS[E.app] ? E.app : 'credit-request';
    V.envApp = envApp; V.envApps = Object.keys(ENV_APPS).map(function (k) { return { id: k, label: k }; });
    V.envOnApp = set(function (e) { return { env: Object.assign({}, self.state.env || {}, { app: val(e) }) }; });
    V.envAppNote = ENV_APPS[envApp].length + (ENV_APPS[envApp].length > 1 ? ' modules' : ' module');
    V.envObservedAt = '11:05';
    var rows = ENVS.map(function (en) {
      var up = en.upstream ? ENVS.filter(function (x) { return x.id === en.upstream; })[0] : null;
      var mods = ENV_APPS[envApp].map(function (m, i) {
        var loc = (LOCAL[en.id] || {})[m], branch = loc || (up ? up.tracked : en.tracked), where = en.upstream ? (loc ? 'local placement' : 'from ' + en.upstream) : 'tracked branch';
        var drift = en.id === 'staging-2' && m === ENV_APPS[envApp][0];
        return { module: m, branch: branch, where: where, version: VER[branch] || '4.7.0-SNAPSHOT', commit: shaOf(en.id + m + branch), source: i % 2 ? 'ArgoCD' : 'Kubernetes', at: en.id === 'dev-2' && loc ? '11:11' : '11:05', drift: drift, driftText: drift ? 'Drift · ArgoCD out of sync since 10:40' : '' };
      });
      var res = RES[en.id] || null, mod0 = ENV_APPS[envApp][0];
      return { name: en.id, tier: en.tier, isUpstream: !en.upstream, hasUpstream: !!en.upstream, upstream: en.upstream || '', tracked: en.tracked || '', mode: en.mode || '', mods: mods,
        hasRes: !!res, noRes: !res, resHolder: res ? res.holder : '', resScope: res ? res.scope : '', resUntil: res ? res.until : '', mine: !!(res && res.mine), canAct: !!en.upstream, canReserve: !res,
        deploy: set(function () { return self.asAsk('Deploy ' + envApp + '/' + mod0 + ' from develop to ' + en.id, true); }),
        reserve: set(function () { return self.asAsk('Reserve ' + en.id + ' for ' + envApp + '/' + mod0 + ' until Friday', true); }),
        extend: set(function () { return snack(en.id + ': your reservation of ' + (res ? res.scope : '') + ' now ends tomorrow 18:00.'); }),
        release: set(function () { return snack(en.id + ': reservation released.'); }) };
    });
    V.envRows = rows;
    Object.assign(V, this.docsVals(ctx));
    Object.assign(V, this.sweepVals(ctx));

    // ---------------- header for the new screens ----------------
    var HDR = { catalog: view === 'item' ? ['Catalog · ' + sk.kind, sk.name] : view === 'new' ? ['Catalog · Publish a skill', stepName[C.step - 1] + ' · ' + nsNameOr] : ['Catalog', published.length + ' items for the assistant and Sweep'],
      env: ['Environments', '6 environments · non-production · ' + envApp], docs: [V.dl_hdrFeature, V.dl_hdrSummary], sweep: V.sw_hdr };
    if (HDR[s.screen]) { V.hdrFeature = HDR[s.screen][0]; V.hdrSummary = HDR[s.screen][1]; }
    var other = ['catalog', 'env', 'docs'].indexOf(s.screen) >= 0;
    V.navCatD = s.screen === 'catalog' && !!s.navOpen; V.navCatR = s.screen === 'catalog' && !s.navOpen;
    V.navEnvD = s.screen === 'env' && !!s.navOpen; V.navEnvR = s.screen === 'env' && !s.navOpen;
    V.navDocsD = s.screen === 'docs' && !!s.navOpen; V.navDocsR = s.screen === 'docs' && !s.navOpen;
    V.navBarEnv = s.screen === 'env'; V.navBarDocs = s.screen === 'docs'; V.navBarCat = s.screen === 'catalog';
    V.goCatalog = set(Object.assign({ screen: 'catalog', tourId: null, cat: Object.assign({}, s.cat || {}, { view: 'list' }) }, ctx.closeAll));
    V.goEnv = set(Object.assign({ screen: 'env', tourId: null }, ctx.closeAll)); V.goDocs = set(function () { return Object.assign({ screen: 'docs', tourId: null, dl: Object.assign({}, self.state.dl || {}, { view: 'home', wiki: null }) }, ctx.closeAll); });

    // ---------------- assistant pane ----------------
    var ctxName = { sweep: V.sw_ctx, community: 'Community', admin: 'Administration', catalog: 'Catalog', env: 'Environments', docs: 'Docs' }[s.screen] || 'AIToolbox';
    V.asOpen = A.open; V.asCtx = ctxName; V.asTitle = A.turns.length ? (A.turns[0].q.length > 38 ? A.turns[0].q.slice(0, 36) + '…' : A.turns[0].q) : 'Assistant';
    V.askAssistant = set(function () { var a = asNow(); return { as: Object.assign({}, self.state.as || {}, { open: !a.open, menu: false }), panel: false, menu: false, help: false }; });
    V.asClose = set(function () { return { as: Object.assign({}, self.state.as || {}, { open: false, menu: false }) }; });
    V.asNew = set(function () { return { as: Object.assign({}, self.state.as || {}, { turns: [], draft: '', menu: false }) }; });
    var SUGG = { sweep: V.sw_sugg, env: ['Deploy credit-request 4.6.1 to staging-2', 'Is staging healthy?'], catalog: ['What is in my assistant?', 'Facility exports are failing since 02:00, where do I start?'],
      community: ['Summarize what’s new in 4.6', 'Open a Jira ticket for the flaky facility export test'], docs: ['Is the facility ARB ready for the board?', 'What depends on the Facility service?', 'How do I ship a hotfix on Thursday?'], admin: ['Which connectors need attention?', 'What is in my assistant?'] }[s.screen] || ['Is staging healthy?'];
    V.asSugg = SUGG.map(function (t) { return { t: t, go: set(function () { return self.asAsk(t, true); }) }; });
    V.asHint = 'I know this page. I can use the tools, skills and MCP servers in your assistant: add more from the Catalog.';
    V.asEmpty = !A.turns.length;
    V.asTurns = A.turns.map(function (t, i) {
      var upd = function (patch) { return set(function () { var a = asNow(), turns = a.turns.map(function (x, j) { return j === i ? Object.assign({}, x, typeof patch === 'function' ? patch(x) : patch) : x; }); return { as: Object.assign({}, self.state.as || {}, { turns: turns }) }; }); };
      var ST = { ok: ['done', '#006D3B'], run: ['waiting for you', '#7A5900'], warn: ['not available', '#7A5900'], no: ['not run', '#48454E'] };
      var dA = t.dq && self._dlAnswerOf ? self._dlAnswerOf(t.dq) : null;
      if (dA) t = Object.assign({}, t, { trace: dA.trace.map(function (x) { return Object.assign({}, x, { s: 'ok' }); }), answer: dA.answer });
      var dX = dA ? { dChain: dA.hasChain, chain: dA.chain, dSteps: dA.hasSteps, steps: dA.steps, dList: dA.hasList, list: dA.list, dProv: dA.hasProv, prov: dA.prov, dSrc: true, sources: dA.sources, fresh: dA.fresh }
        : { dChain: false, chain: [], dSteps: false, steps: [], dList: false, list: [], dProv: false, prov: '', dSrc: false, sources: [], fresh: '' };
      return Object.assign(dX, { q: t.q, hasQ: true, hasPills: false, pills: [], hasProps: false, props: [], hasQual: false, qual: {}, hasReplies: false, replies: [], n: t.trace.length, hasTrace: t.trace.length > 0, trace: t.trace.map(function (x) { return Object.assign({}, x, { st: ST[x.s][0], stc: ST[x.s][1] }); }),
        waiting: t.state === 'approval', apTitle: t.ap ? t.ap.title : '', apArgs: t.ap ? t.ap.args : '', apWhy: t.ap ? t.ap.why : '', apCta: t.ap ? t.ap.cta : '',
        approve: upd(function (x) { return { state: 'done', trace: x.trace.map(function (y) { return y.s === 'run' ? Object.assign({}, y, { s: 'ok', label: x.ap.doneLabel }) : y; }), answer: x.ap.doneAnswer }; }),
        decline: upd(function (x) { return { state: 'done', trace: x.trace.map(function (y) { return y.s === 'run' ? Object.assign({}, y, { s: 'no' }) : y; }), answer: 'Okay, nothing was run.' }; }),
        answer: t.state === 'approval' ? t.pre || '' : t.answer, hasLink: !!t.link && t.state !== 'approval', linkLabel: t.link ? t.link.label : '', linkGo: t.link ? goItem(t.link.id) : set({}),
        good: !!t.good, thumbUp: upd(function (x) { return { good: !x.good }; }), thumbDown: set(snack('Thanks. Tell us what was wrong in the form: it goes to Community › Feedback.')) });
    });
    V.asDraft = A.draft; V.asOnDraft = set(function (e) { return { as: Object.assign({}, self.state.as || {}, { draft: val(e) }) }; });
    V.asSendDraft = set(function () { var t = (asNow().draft || '').trim(); return t ? self.asAsk(t, false) : {}; });
    V.asKey = function (e) { if (e && e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); var t = ((self.state.as || {}).draft || (e.target && e.target.value) || '').trim(); if (t) self.setState(self.asAsk(t, false)); } };
    V.hdrKey = function (e) { if (e && e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); var t = ((self.state.as || {}).draft || (e.target && e.target.value) || '').trim(); if (t) self.setState(self.asAsk(t, true)); } };
    V.hdrAsk = set(function () { var a = asNow(), t = (a.draft || '').trim(); return t ? self.asAsk(t, true) : { as: Object.assign({}, self.state.as || {}, { open: !a.open, menu: false }), panel: false, menu: false, help: false }; });
    V.mainPaneCls = A.open ? 'pane-on' : '';
    V.asMenu = A.menu; V.asToggleMenu = set(function () { return { as: Object.assign({}, self.state.as || {}, { menu: !asNow().menu }) }; });
    V.asBrowse = set(function () { return Object.assign({ screen: 'catalog', as: Object.assign({}, self.state.as || {}, { menu: false }), cat: Object.assign({}, self.state.cat || {}, { view: 'list', tab: 'browse' }) }, ctx.closeAll); });
    var tog = function (id) { return set(function () { var a = asNow(), off = Object.assign({}, a.off); off[id] = !off[id]; return { as: Object.assign({}, self.state.as || {}, { off: off }) }; }); };
    var BUILT_T = [ { id: 'b_runs', name: 'Search runs', note: 'Sweep · reads' }, { id: 'b_logs', name: 'Read run logs', note: 'Sweep · reads' }, { id: 'b_env', name: 'Query environments', note: 'Environments · reads' } ];
    var BUILT_S = [ { id: 'b_sweep', name: 'Sweep', note: 'Built-in' }, { id: 'b_docs', name: 'Docs', note: 'Built-in' }, { id: 'b_envs', name: 'Environments', note: 'Built-in' } ];
    var addedOf = function (kind) { return ITEMS.filter(function (it) { return it.kind === kind && C.added[it.id]; }); };
    V.asTools = BUILT_T.concat(addedOf('Tool').map(function (it) { return { id: it.id, name: it.name, note: it.by + ' · asks first' }; })).map(function (m) { return Object.assign(m, { on: !A.off[m.id], toggle: tog(m.id) }); });
    V.asSkills = BUILT_S.concat(addedOf('Skill').map(function (it) { return { id: it.id, name: it.name, note: 'Catalog · ' + it.by }; })).map(function (m) { return Object.assign(m, { on: !A.off[m.id], toggle: tog(m.id) }); });
    V.asMcp = addedOf('MCP server').map(function (it) { return { id: it.id, name: it.name, note: it.tools.length + ' tools · ' + it.by, on: !A.off[it.id], toggle: tog(it.id) }; });
    V.asCount = V.asTools.concat(V.asSkills, V.asMcp).filter(function (m) { return m.on; }).length;
    return V;
  }
  // the assistant's answer engine: returns the state patch that opens the pane and adds a turn
  asAsk(q, open) {
    var self = this, s = this.state, C = Object.assign({ added: { m1: true, m2: true, t1: true, t3: true } }, s.cat || {}), A = Object.assign({ open: false, turns: [], draft: '', menu: false, off: {} }, s.as || {});
    var has = function (id) { return !!C.added[id] && !A.off[id]; };
    var SRC = { SW: ['SW', '#E3DFFF', '#14085E'], EN: ['EN', '#E3DFFF', '#14085E'], DO: ['DO', '#9CF1F0', '#002020'], KB: ['KB', '#9CF1F0', '#002020'], SK: ['SK', '#FFDEA0', '#261900'], TL: ['TL', '#C3F4DC', '#00391E'] };
    var tr = function (k, label, st) { var x = SRC[k]; return { ab: x[0], bg: x[1], fg: x[2], label: label, s: st || 'ok' }; };
    var l = q.toLowerCase(), t = { q: q, trace: [], state: 'done', answer: '' };
    var missing = function (id, what) { var it = { m1: 'DevOps', m2: 'Knowledge base', t1: 'Deploy environment', t2: 'Reserve environment', t3: 'Create Jira ticket', s2: 'Incident runbook' }[id]; t.answer = 'I can’t ' + what + ' here: ' + it + ' isn’t in your assistant. Add it from the Catalog and ask again.'; t.link = { label: 'Open ' + it + ' in the Catalog', id: id }; };
    var dq = this.dlMatch(l), sa = null;
    if (dq && !has('m2')) missing('m2', 'read the knowledge base');
    else if (dq) { var DL = s.dl || {}; t.dq = { q: dq, text: q, el: DL.el || 'api', app: DL.app || 'environments' }; }
    else if (/re-?run|rerun|pipeline/.test(l)) {
      if (!has('m1')) missing('m1', 'start a pipeline');
      else { var rk = ((l.match(/e2ecc-\d+/) || ['e2ecc-103861'])[0]).toUpperCase(), fromI = /integration/.test(l);
        t.trace = [tr('SW', 'Read the last run of ' + rk), tr('DO', 'Run pipeline sweep-' + rk.toLowerCase(), 'run')]; t.state = 'approval'; t.pre = fromI ? rk + ' failed at the integration check. I can re-run only that step on the same branch.' : 'I can re-run ' + rk + ' from the start on develop.';
        t.ap = { title: 'Re-run ' + rk + (fromI ? ' from the integration check?' : '?'), args: 'ticket: ' + rk + '\nfrom: ' + (fromI ? 'integration check' : 'start') + '\nbase branch: develop\nBitbucket project: E2ECC', why: 'Run pipeline (DevOps MCP server) changes something, so it asks first.', cta: 'Re-run', doneLabel: 'Started sweep-' + rk.toLowerCase() + '-2', doneAnswer: 'Started sweep-' + rk.toLowerCase() + '-2' + (fromI ? ': only the integration check runs, about 1 minute.' : '.') + ' Follow it in Sweep.' }; }
    } else if ((sa = this.swAnswer(l))) {
      t.trace = sa.trace.map(function (x) { return tr(x[0], x[1]); }); t.answer = sa.answer;
    } else if (/reserve/.test(l)) {
      var envR = (l.match(/(dev-\d|staging-\d)/) || [null, 'staging-2'])[1], tgtR = (l.match(/for ([a-z-]+\/[a-z-]+)/) || [null, 'credit-request/request-service'])[1];
      if (!has('t2')) missing('t2', 'reserve an environment');
      else { t.trace = [tr('EN', 'Checked ' + envR + ': no reservation on ' + tgtR), tr('TL', 'Reserve environment', 'run')]; t.state = 'approval'; t.pre = 'Nobody holds ' + tgtR + ' on ' + envR + '. I can reserve it for you.';
        t.ap = { title: 'Reserve ' + tgtR + ' on ' + envR + ' until Friday 18:00?', args: 'environment: ' + envR + '\nscope: module ' + tgtR + '\nuntil: Friday 18:00\nreason: testing before the release', why: 'Reserve environment changes something, so it asks first.', cta: 'Reserve', doneLabel: 'Reserved until Friday 18:00', doneAnswer: tgtR + ' is reserved for you on ' + envR + ' until Friday 18:00. Extend or release it from Environments.' }; }
    } else if (/deploy|ship/.test(l)) {
      var env = (l.match(/(dev-\d|staging-\d)/) || [null, 'dev-1'])[1], tgt = (l.match(/deploy ([a-z-]+\/[a-z-]+)/) || [null, 'credit-request/request-service'])[1], br = (l.match(/from ([a-z0-9\/._-]+)/) || [null, 'develop'])[1];
      if (!has('t1')) missing('t1', 'deploy');
      else { t.trace = [tr('EN', 'Checked ' + env + ': no reservation on ' + tgt), tr('TL', 'Deploy environment', 'run')]; t.state = 'approval';
        t.pre = 'The build of ' + br + ' is green. The deployment opens an auto-merge pull request on the descriptor repository, then the first rollout starts.';
        t.ap = { title: 'Deploy ' + tgt + ' from ' + br + ' to ' + env + '?', args: 'module: ' + tgt + '\nbranch: ' + br + '\nenvironment: ' + env, why: 'Deploy environment changes something, so it asks first.', cta: 'Deploy', doneLabel: 'Pull request opened · first rollout started', doneAnswer: 'Descriptor pull request merged; the first rollout of ' + tgt + ' (' + br + ') on ' + env + ' is running. I’ll tell you when it is live.' }; }
    } else if (/ticket|jira/.test(l)) {
      if (!has('t3')) missing('t3', 'create a ticket');
      else { t.trace = (has('m2') ? [tr('KB', 'Searched for similar issues: none open')] : []).concat([tr('TL', 'Create Jira ticket', 'run')]); t.state = 'approval'; t.pre = 'I drafted the ticket with the run attached.';
        t.ap = { title: 'Create a Jira ticket in SWP?', args: 'project: SWP\ntype: Bug\ntitle: Flaky FacilityExportTest (fixed timestamp in the fixture)\nlinks: E2ECC-103861', why: 'Create Jira ticket changes something, so it asks first.', cta: 'Create ticket', doneLabel: 'Created SWP-1288', doneAnswer: 'Created SWP-1288 and linked E2ECC-103861.' }; }
    } else if (/incident|facility|export|runbook|on-?call|where do i start/.test(l)) {
      if (has('s2')) { t.trace = [tr('SK', 'Using skill: Incident runbook')].concat(has('m2') ? [tr('KB', 'Read the facility-exports runbook')] : []).concat([tr('SW', 'Read the logs of the export job')]);
        t.answer = '1. The export job fails at 02:00 on a timeout to the facility database (3 runs in a row).\n2. The runbook says: check the replica lag first; it is 14 min now, above the 5 min threshold.\n3. Next: fail over the export to the primary (runbook step 4), then open a ticket for the replica.\nI can open the ticket when you are ready.'; }
      else { t.trace = [tr('SW', 'Read the logs of the export job')]; t.answer = 'The export job fails at 02:00 on a timeout to the facility database. The Incident runbook skill walks through the checklist step by step, with the right runbook.'; t.link = { label: 'Open Incident runbook in the Catalog', id: 's2' }; }
    } else if (/staging|health/.test(l)) {
      t.trace = [tr('EN', 'Checked staging-2 health')].concat(has('m2') ? [tr('KB', 'Read the staging runbook')] : []); t.answer = 'staging-2 is degraded since 09:51: 3 of 5 health checks fail on the search service (index mapping v12, code expects v13). staging-1 and dev-1 are healthy.' + (has('m2') ? ' The runbook says to rebuild the index mapping before deploying.' : '');
    } else if (/rollback|procedure|summari[sz]e “|docs?/.test(l)) {
      if (!has('m2')) missing('m2', 'read the knowledge base'); else { t.trace = [tr('KB', 'Read “Rollback procedure for facility-management”')]; t.answer = 'Roll back when error rate stays above 2 % for 10 minutes. Freeze writes, redeploy the previous release, run the 5 health checks, then reopen writes. Source: Knowledge base · Runbook · Facility.'; }
    } else if (/what.?s new|4\.6/.test(l)) {
      t.trace = [tr('SW', 'Read What’s new · 4.6')]; t.answer = '4.6 brings approval cards for assistant tools (anything that changes something asks first) and PR summaries in Sweep. The assistant model changes on 10 November.';
    } else if (/my assistant|catalog|skills?|tools?/.test(l)) {
      var names = ['m1', 'm2', 't1', 't2', 't3', 's1', 's2', 's3', 's4'].filter(has).map(function (id) { return { m1: 'DevOps', m2: 'Knowledge base', t1: 'Deploy environment', t2: 'Reserve environment', t3: 'Create Jira ticket', s1: 'Spring Boot 3 migration', s2: 'Incident runbook', s3: 'Release notes from changelog', s4: 'Deploy to staging with checks' }[id]; });
      t.answer = 'Built in: Search runs, Read run logs, Query environments, and the Sweep, Docs and Environments skills. From the Catalog: ' + (names.join(', ') || 'nothing yet') + '. Add or remove items from the Catalog or the Tools menu.';
    } else if (/connector/.test(l)) {
      t.trace = [tr('SW', 'Read Sweep › Connectors')]; t.answer = 'SonarQube: its token expires in 6 days. Artifactory is not connected. The DevOps platform, Jira and Teams are fine.';
    } else {
      t.trace = [tr('SW', 'Searched today’s runs')]; t.answer = 'Today in Sweep (Bitbucket project E2ECC): 5 runs. 1 running (E2ECC-103894), 2 succeeded, 1 failed at the integration check (E2ECC-103861), 1 cancelled. On Environments, staging-2 is degraded.';
    }
    return { as: Object.assign({}, A, { open: open || A.open, turns: A.turns.concat([t]), draft: '', menu: false }), panel: false, menu: false, help: false };
  }
