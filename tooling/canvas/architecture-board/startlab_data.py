"""Change start lab · example data: changes on every phase of the adjusted TOGAF flow and at every gate, with where
each one comes from; incoming signals that are not a change yet. Meridian Bank, reference date Tue 3 Nov 2026.
Lab data: it borrows the names of the board's changes but spreads them so every phase and gate has an example."""

# origin kinds: how a change reaches architecture
ORIGINS = [
    {'id': 'ticket', 'name': 'Business request', 'sub': 'a ticket from a product owner', 'entry': 'new-need', 'g': 'T'},
    {'id': 'chat', 'name': 'Conversation', 'sub': 'a question to the assistant', 'entry': 'new-need', 'g': 'C'},
    {'id': 'idea', 'name': 'Exploration', 'sub': 'an architect tries a target', 'entry': 'exploration', 'g': 'E'},
    {'id': 'radar', 'name': 'Technology standard', 'sub': 'the radar moves a technology', 'entry': 'evolution', 'g': 'S'},
    {'id': 'adr', 'name': 'Decision', 'sub': 'an ADR or a board condition', 'entry': 'decision', 'g': 'D'},
    {'id': 'pr', 'name': 'Code first', 'sub': 'a pull request, Sweep or local', 'entry': 'small-tweak', 'g': 'P'},
    {'id': 'finding', 'name': 'Model finding', 'sub': 'a check or the reconciliation', 'entry': 'post-delivery', 'g': 'F'},
    {'id': 'incident', 'name': 'Incident', 'sub': 'fixed in production first', 'entry': 'post-delivery', 'g': 'I'},
]

# per phase: TOGAF letters, the documents the phase produces, and who reviews at its gate (decisions of 2026-11-09)
PHASES = [
    {'togaf': 'A', 'togafName': 'Preliminary · Phase A', 'docs': ['Need', 'Statement of Architecture Work'], 'gateBy': 'Portfolio architect'},
    {'togaf': 'B · C · D', 'togafName': 'Phases B, C, D on the baseline', 'docs': ['Baseline architecture (ADD)'], 'gateBy': ''},
    {'togaf': 'B · C · D', 'togafName': 'Phases B, C, D on the target', 'docs': ['Target architecture (ADD)', 'ASD', 'ADR'], 'gateBy': 'Architecture Board · domain architects and product stakeholders'},
    {'togaf': 'E', 'togafName': 'Phase E', 'docs': ['Gap table'], 'gateBy': ''},
    {'togaf': 'F', 'togafName': 'Phase F', 'docs': ['Roadmap', 'Detailed design per module'], 'gateBy': 'The portfolio\'s architect with the tech leads'},
    {'togaf': 'G', 'togafName': 'Phase G', 'docs': ['Detailed design kept in step', 'Contracts'], 'gateBy': 'Change owner confirms · portfolio architect promotes'},
    {'togaf': 'H', 'togafName': 'Phase H · the plateau is the new baseline', 'docs': ['Model · baseline'], 'gateBy': ''},
]

def ch(id, title, pf, klass, origin, entry, cur, now, nxt, docs, gate=None, last=None, crit=None, closed=False, deliv=''):
    return {'id': id, 'title': title, 'pf': pf, 'klass': klass,
            'origin': dict(zip(['kind', 'ref', 'by', 'at', 'text'], origin)), 'entry': entry, 'cur': cur, 'now': now, 'next': nxt,
            'docs': [{'name': d[0], 'state': d[1]} for d in docs],
            'gate': dict(zip(['id', 'state', 'note', 'by'], gate)) if gate else None,
            'last': dict(zip(['id', 'outcome', 'at', 'by', 'note'], last)) if last else None,
            'crit': crit or [], 'closed': closed, 'deliv': deliv}

# gate state: waiting · review · changes · rejected          last outcome: approved · conditions
# document state: todo · chat · working · pr · reviewed · published
CHANGES = [
    # 0 · Vision
    ch('c-treasury', 'Real-time balance for corporate treasurers', 'Corporate', 're-architecting',
       ('ticket', 'CRD-260', 'Corporate product owner', '29 Oct', 'Treasurers ask for intraday balances across entities; today the figure is end of day.'),
       'new-need', 0, 'Need and scope being drafted in the assistant', 'Change owner · finish the Statement of Architecture Work, then ask for G1',
       [('Need', 'working'), ('Statement of Architecture Work', 'chat')]),
    ch('c-psd3', 'Open banking consent refresh (PSD3)', 'Retail', 'incremental',
       ('chat', 'Assistant conversation', 'Retail product owner', '30 Oct', '"Consents must be renewed every 180 days under PSD3. What has to change?"'),
       'new-need', 0, 'Waiting at G1 · class to confirm', 'Portfolio architect · confirm the class and the reviewers',
       [('Need', 'published'), ('Statement of Architecture Work', 'pr')],
       gate=('G1', 'waiting', 'Asked on 2 Nov · scope: 2 applications, Transition 2', 'Portfolio architect · Retail'), crit=[1, 1, 0]),
    ch('c-cash', 'Branch cash forecasting', 'Retail', 'incremental',
       ('ticket', 'RET-4391', 'Branch network lead', '21 Oct', 'Forecast the cash each branch needs from the withdrawal history.'),
       'new-need', 0, 'Back in Vision after G1', 'Requester · add the measures, then ask again',
       [('Need', 'working'), ('Statement of Architecture Work', 'working')],
       gate=('G1', 'changes', 'Sent back on 28 Oct · "The need has no measure: which forecast error is acceptable?"', 'Portfolio architect · Retail'), crit=[0, 1, 1]),
    # 1 · Baseline
    ch('c-oracle', 'Retire Oracle 12 from the payment stores', 'Payments', 're-architecting',
       ('radar', 'Technology radar · Oracle 12 moved to Retire', 'CTO office', '14 Oct', 'Oracle 12 leaves support in 2027; three payment stores still run on it.'),
       'evolution', 1, 'Baseline being corrected · agents propose 3 stores missing from the model', 'Change owner · accept or reject the 3 proposals',
       [('Baseline architecture (ADD)', 'working'), ('Model · baseline', 'pr')],
       last=('G1', 'approved', '20 Oct', 'Portfolio architect · Payments', 'Scope: 3 stores, 2 applications')),
    ch('c-dispute', 'Card dispute handling rework', 'Retail', 're-architecting',
       ('ticket', 'RET-4402', 'Cards product owner', '6 Oct', 'A dispute takes 12 days on average; the target is 3.'),
       'new-need', 1, 'Reading the baseline of the dispute process', 'Change owner · confirm the baseline, start the target',
       [('Baseline architecture (ADD)', 'chat')],
       last=('G1', 'approved', '28 Oct', 'Portfolio architect · Retail', 'Class confirmed: re-architecting')),
    # 2 · Target
    ch('c-riskdata', 'Risk data platform', 'Risk', 're-architecting',
       ('idea', 'Exploration', 'Risk domain architect', '2 Nov', 'Could one platform replace the four risk data marts? No committed need yet.'),
       'exploration', 2, 'Target being modelled · ASD started', 'Change owner · G2 decides whether this becomes a change',
       [('Target architecture (ADD)', 'working'), ('ASD', 'chat'), ('ADR · platform choice', 'todo')]),
    ch('c-facility', 'Facility service extraction', 'Corporate', 're-architecting',
       ('ticket', 'CRD-188', 'Corporate product owner', '8 Sep', 'Facilities must change without redeploying the credit monolith.'),
       'evolution', 2, 'At G2 · in review', 'Security architect and Corporate product owner · record a decision',
       [('Target architecture (ADD)', 'pr'), ('ASD', 'pr'), ('ADR-029 · facility data ownership', 'reviewed')],
       gate=('G2', 'review', 'Board of 12 Nov · 3 of 5 reviewers decided', 'Architecture Board · domain architects and product stakeholders'), crit=[1, 1, 0]),
    ch('c-iso', 'ISO 20022 for cross-border payments', 'Payments', 're-architecting',
       ('ticket', 'PAY-290', 'Payments product owner', '1 Sep', 'SWIFT MT messages end in November 2027.'),
       'new-need', 2, 'Back in Target after G2', 'Change owner · complete the target, submit again for 12 Nov',
       [('Target architecture (ADD)', 'working'), ('ASD', 'working')],
       gate=('G2', 'changes', 'Board of 22 Oct · changes requested: "The sanctions screening path is not in the target"', 'Architecture Board'), crit=[0, 1, 0]),
    ch('c-sme', 'Second pricing engine for SME', 'Corporate', 're-architecting',
       ('chat', 'Assistant conversation', 'Corporate product owner', '22 Sep', '"Can SME pricing get its own engine?"'),
       'exploration', 2, 'Closed · the board record is kept', 'Nothing',
       [('ASD', 'published')],
       gate=('G2', 'rejected', 'Board of 15 Oct · rejected: "One pricing engine; extend its grid"', 'Architecture Board'), crit=[1, 0, 0], closed=True),
    # 3 · Gap analysis
    ch('c-legacy', 'Legacy data exit', 'Risk', 're-architecting',
       ('radar', 'Technology radar · SAS 9 moved to Retire', 'CTO office', '3 Aug', 'The four risk data marts run on SAS 9.'),
       'evolution', 3, 'Gap computed: 4 new · 2 changed · 6 retired · 1 retired block has no work package', 'Change owner · plan the block without work package, or explain it',
       [('Gap table', 'working')],
       last=('G2', 'conditions', '20 Oct', 'Architecture Board', '2 conditions open · owner Risk data lead · due 30 Nov')),
    ch('c-kafka', 'Kafka as the event backbone', 'Payments', 'incremental',
       ('adr', 'ADR-031 accepted', 'Architecture Board', '27 Oct', 'New event interfaces use Kafka instead of MQ.'),
       'decision', 3, 'Entered at Gap analysis · the decision changes 5 interfaces of the target', 'Change owner · confirm the gap, then plan',
       [('Gap table', 'chat'), ('ADR-031', 'published')]),
    # 4 · Plateau
    ch('c-webmobile', 'Web on mobile platform', 'Retail', 're-architecting',
       ('ticket', 'RET-4310', 'Digital channels product owner', '12 Aug', 'One front end for web and mobile banking.'),
       'evolution', 4, 'Waiting at G3', 'Tech lead web-banking · finish the detailed design · Change owner · declare the order with Digital onboarding',
       [('Roadmap', 'published'), ('Detailed design · web-banking', 'working'), ('Detailed design · mobile-banking', 'reviewed')],
       gate=('G3', 'waiting', 'Asked on 31 Oct · detailed design missing for 1 module · order with Digital onboarding not declared', 'Retail architect with the tech leads'), crit=[0, 1, 0]),
    ch('c-hub', 'Payment hub partitioning', 'Payments', 'incremental',
       ('finding', 'Model check · capacity', 'Payments architect', '9 Oct', 'The hub reaches 80% of its throughput at month end.'),
       'evolution', 4, 'Work packages and dates being drafted', 'Change owner · draft the roadmap, then ask for G3',
       [('Roadmap', 'chat'), ('Detailed design · payment-hub', 'todo')],
       last=('G2', 'approved', '24 Oct', 'Portfolio architect · Payments', 'Incremental: no board')),
    # 5 · Implementation
    ch('c-credit', 'Credit request and pricing services', 'Corporate', 're-architecting',
       ('ticket', 'CRD-101', 'Corporate product owner', '2 Mar', 'A credit decision in 48 hours instead of 9 days.'),
       'new-need', 5, '3/5 tickets done · 1 in progress · last commit 30 Oct', 'Team · CRD-204 and CRD-205 · version 1.4.0 on 8 Dec reaches Transition 1',
       [('Detailed design · credit-request', 'published'), ('Contract · credit-request API', 'published')],
       last=('G3', 'approved', '2 Jun', 'Corporate architect with the tech leads', ''), deliv='3/5 tickets · 6 commits · credit-request 1.3.0 released'),
    ch('c-sepa', 'SEPA instant payments', 'Payments', 're-architecting',
       ('ticket', 'PAY-240', 'Payments product owner', '4 May', 'Instant transfers for retail and corporate clients.'),
       'new-need', 5, '0/4 tickets done · 2 in progress · last commit yesterday', 'Team · PAY-310 and PAY-311',
       [('Detailed design · instant-payments', 'reviewed'), ('Contract · instant payment events', 'published')],
       last=('G3', 'conditions', '1 Sep', 'Payments architect with the tech leads', '1 condition open · fraud scoring under 200 ms · due 15 Dec'), deliv='0/4 tickets · 3 commits · no version yet'),
    ch('c-margin', 'Margin grid on the credit request screen', 'Retail', 'simplification',
       ('pr', 'Sweep run E2ECC-103870 · PR web-banking #409', 'Web banking developer', 'today 10:22', 'Code first: the screen changed before any change was opened.'),
       'small-tweak', 5, 'Definition of Ready only · detailed design drafted from the pull request', 'Tech lead (CODEOWNERS) · approve the pull request and the design update',
       [('Detailed design · web-banking', 'working')], deliv='1 ticket · 1 commit (Sweep)'),
    ch('c-onboarding', 'Digital onboarding', 'Retail', 're-architecting',
       ('ticket', 'RET-4410', 'Retail product owner', '15 Apr', 'Open an account online in 10 minutes.'),
       'evolution', 5, 'Waiting at G4', 'Team · add the endpoint to the model or remove it · close condition C3',
       [('Detailed design · digital-onboarding', 'published'), ('Contract · onboarding API', 'published')],
       gate=('G4', 'waiting', 'Asked on 2 Nov · 1 endpoint in the code is not in the model · 2 of 3 conditions closed', 'Change owner confirms · portfolio architect promotes'), crit=[1, 0, 0],
       deliv='4/4 tickets · 9 commits · digital-onboarding 1.0.0 released'),
    # 6 · Delivered
    ch('c-tokens', 'Card tokenization', 'Retail', 're-architecting',
       ('ticket', 'RET-3980', 'Cards product owner', '12 Jan', 'Card numbers never leave the vault.'),
       'new-need', 6, 'Delivered · Transition 1 promoted on 12 Oct, it is the new baseline', 'Nothing',
       [('Model · baseline', 'published')],
       last=('G4', 'approved', '12 Oct', 'Portfolio architect · Retail', 'Conformance green · 3 conditions closed'), deliv='6/6 tickets · card-vault 2.0.0 released'),
    ch('c-timeout', 'Payment timeout raised to 8 s', 'Payments', 'simplification',
       ('incident', 'INC-88213', 'Payments on-call', '26 Oct', 'Fixed in the code during the incident; the model still says 5 s.'),
       'post-delivery', 6, 'Baseline catching up · the reconciliation proposed the update', 'Payments architect · accept the baseline update (no gate)',
       [('Model · baseline', 'pr')]),
]

def sig(id, kind, ref, by, at, title, text, entry, klass, pf, scope, attach=None, overlap=''):
    return {'id': id, 'kind': kind, 'ref': ref, 'by': by, 'at': at, 'title': title, 'text': text, 'entry': entry, 'klass': klass, 'pf': pf, 'scope': scope, 'attach': attach, 'overlap': overlap}

# signals that are not a change yet
SIGNALS = [
    sig('s-freeze', 'ticket', 'RET-4588', 'Cards product owner', 'today 09:10', 'Instant card freeze from the mobile app', 'Customers want to freeze a card themselves, in seconds.', 'new-need', 're-architecting', 'Retail', 'mobile-banking, card-management'),
    sig('s-pr412', 'pr', 'PR web-banking #412 · local, coding assistant', 'Web banking developer', 'today 08:47', 'Session timeout banner', 'A pull request touches web-banking without a ticket or a change.', 'small-tweak', 'simplification', 'Retail', 'web-banking', attach='c-webmobile', overlap='Web on mobile platform changes the same module'),
    sig('s-angular', 'radar', 'Technology radar · Angular 15 moved to Hold', 'CTO office', 'yesterday', 'Leave Angular 15', 'Three applications still build on Angular 15.', 'evolution', 'incremental', 'Retail', 'web-banking, backoffice, branch-portal'),
    sig('s-refunds', 'finding', 'Reconciliation · code differs from the model', 'Knowledge base', 'yesterday', 'payment-hub exposes /v2/refunds', 'The endpoint is in the code and the contract, not in the model.', 'post-delivery', 'simplification', 'Payments', 'payment-hub'),
    sig('s-adr34', 'adr', 'ADR-034 accepted', 'Architecture Board', '30 Oct', 'Event contracts in AsyncAPI 3', 'The decision changes how event interfaces are described.', 'decision', 'incremental', 'Payments', 'instant-payments, payment-hub', attach='c-kafka', overlap='Kafka as the event backbone changes the same interfaces'),
    sig('s-inc301', 'incident', 'INC-88301', 'Payments on-call', '31 Oct', 'Sanctions list reload fixed in production', 'The reload moved from nightly to hourly during the incident.', 'post-delivery', 'simplification', 'Payments', 'sanctions-screening'),
]

LAB = {'origins': ORIGINS, 'phases': PHASES, 'changes': CHANGES, 'signals': SIGNALS}
