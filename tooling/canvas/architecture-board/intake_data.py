"""Intake (qualification) data for the Architecture board: the signals that are not a change yet, what was qualified
before, where each existing change comes from, and the script of the qualification conversation in the assistant.
Decision of 2026-11-10: intake from signals, plus an explicit request in the assistant with chat iteration; intake
and ongoing changes are two separate places. Meridian Bank, reference date Tue 3 Nov 2026."""

ORIGINS = {
    'ticket': {'name': 'Business request', 'g': 'T', 'entry': 'new-need'},
    'chat': {'name': 'Request in the assistant', 'g': 'C', 'entry': 'new-need'},
    'idea': {'name': 'Exploration', 'g': 'E', 'entry': 'exploration'},
    'radar': {'name': 'Technology standard', 'g': 'S', 'entry': 'evolution'},
    'adr': {'name': 'Decision', 'g': 'D', 'entry': 'decision'},
    'pr': {'name': 'Code first', 'g': 'P', 'entry': 'small-tweak'},
    'finding': {'name': 'Model finding', 'g': 'F', 'entry': 'post-delivery'},
    'incident': {'name': 'Incident', 'g': 'I', 'entry': 'post-delivery'},
}

# where the changes of the board come from
CHANGE_ORIGIN = {
    'imp.corporate.credit-request-v1': ['ticket', 'CRD-101', 'Corporate product owner', '2 Mar'],
    'imp.payments.sepa-instant-v1': ['ticket', 'PAY-240', 'Payments product owner', '4 May'],
    'imp.retail.digital-onboarding-v1': ['ticket', 'RET-4410', 'Retail product owner', '15 Apr'],
    'imp.risk.data-platform-v1': ['idea', 'Exploration', 'Risk domain architect', '2 Nov'],
    'imp.corporate.facility-service-v1': ['adr', 'ADR · Split the credit monolith', 'Architecture Board', '8 Sep'],
    'imp.retail.web-on-mobile-platform': ['ticket', 'RET-4310', 'Digital channels product owner', '12 Aug'],
    'imp.payments.iso20022-cross-border': ['adr', 'ADR · ISO 20022 for cross-border', 'Architecture Board', '1 Sep'],
    'imp.risk.legacy-data-exit': ['radar', 'Technology radar · SAS 9 moved to Retire', 'CTO office', '3 Aug'],
}

def sig(id, kind, ref, by, at, title, text, entry, klass, pf, scope, ask, replies, attach=None, overlap=''):
    return {'id': id, 'kind': kind, 'ref': ref, 'by': by, 'at': at, 'title': title, 'text': text, 'entry': entry, 'klass': klass, 'pf': pf, 'scope': scope,
            'ask': ask, 'replies': replies, 'attach': attach, 'overlap': overlap}

# each signal: the one question the assistant asks before proposing, and the short answers offered ([label, changes])
SIGNALS = [
    sig('s-freeze', 'ticket', 'RET-4588', 'Cards product owner', 'today 09:10', 'Instant card freeze from the mobile app', 'Customers want to freeze a card themselves, in seconds.',
        'new-need', 're-architecting', 'retail', 'mobile-banking, card-management',
        'Is there a committed need with a measure, or is it still an idea to explore?',
        [['Committed: freeze in under 5 seconds', {}], ['Still exploring', {'entry': 'exploration'}]]),
    sig('s-pr412', 'pr', 'PR web-banking #412 · local, coding assistant', 'Web banking developer', 'today 08:47', 'Session timeout banner', 'A pull request touches web-banking without a ticket or a change.',
        'small-tweak', 'simplification', 'retail', 'web-banking',
        'Does it change an interface or the data of the module, or only the screen?',
        [['Only the screen', {}], ['It changes the session API', {'entry': 'evolution', 'klass': 'incremental'}]],
        attach='imp.retail.web-on-mobile-platform', overlap='Web on mobile platform changes the same module'),
    sig('s-angular', 'radar', 'Technology radar · Angular 15 moved to Hold', 'CTO office', 'yesterday', 'Leave Angular 15', 'Three applications still build on Angular 15.',
        'evolution', 'incremental', 'retail', 'web-banking, backoffice, branch-portal',
        'One change for the three applications, or one per application?',
        [['One change, three applications', {}], ['Start with web-banking only', {'scope': 'web-banking'}]],
        attach='imp.retail.web-on-mobile-platform', overlap='Web on mobile platform already rebuilds web-banking'),
    sig('s-refunds', 'finding', 'Reconciliation · code differs from the model', 'Knowledge base', 'yesterday', 'payment-hub exposes /v2/refunds', 'The endpoint is in the code and in the contract, not in the model.',
        'post-delivery', 'simplification', 'payments', 'payment-hub',
        'Is the endpoint meant to stay?',
        [['Yes, add it to the baseline', {}], ['No, it should be removed from the code', {'dismiss': 'Not an architecture change · ticket for the team'}]]),
    sig('s-adr34', 'adr', 'ADR-034 accepted', 'Architecture Board', '30 Oct', 'Event contracts in AsyncAPI 3', 'The decision changes how event interfaces are described.',
        'decision', 'incremental', 'payments', 'instant-payments, payment-hub',
        'Does it apply to the interfaces already being built, or only to new ones?',
        [['Also to the ones being built', {}], ['Only to new interfaces', {'dismiss': 'No change needed · the standard applies from now on'}]],
        attach='imp.payments.sepa-instant-v1', overlap='SEPA instant payments is building the same event interfaces'),
    sig('s-inc301', 'incident', 'INC-88301', 'Payments on-call', '31 Oct', 'Sanctions list reload fixed in production', 'The reload moved from nightly to hourly during the incident.',
        'post-delivery', 'simplification', 'payments', 'sanctions-screening',
        'Is the hourly reload the new normal?',
        [['Yes, keep it', {}], ['No, it goes back to nightly', {'dismiss': 'Temporary fix · nothing to record'}]]),
]

# qualified before today: the link between intake and the changes
QUALIFIED = [
    {'kind': 'ticket', 'ref': 'RET-4410', 'title': 'Open an account online in 10 minutes', 'outcome': 'Change opened', 'change': 'imp.retail.digital-onboarding-v1', 'by': 'Retail portfolio architect', 'at': '15 Apr'},
    {'kind': 'radar', 'ref': 'Technology radar · SAS 9 moved to Retire', 'title': 'Leave SAS 9', 'outcome': 'Change opened', 'change': 'imp.risk.legacy-data-exit', 'by': 'Risk domain architect', 'at': '3 Aug'},
    {'kind': 'pr', 'ref': 'Sweep run E2ECC-103870 · PR web-banking #409', 'title': 'Margin grid on the credit request screen', 'outcome': 'Attached', 'change': 'imp.retail.web-on-mobile-platform', 'by': 'Retail portfolio architect', 'at': 'today 10:40'},
    {'kind': 'chat', 'ref': 'Corporate product owner', 'title': 'Second pricing engine for SME', 'outcome': 'Dismissed · one pricing engine, extend its grid', 'change': None, 'by': 'Corporate portfolio architect', 'at': '15 Oct'},
]

# a free request typed in the assistant: recognised by its words, else treated as a new need
MATCH = [['freeze', 's-freeze'], ['card', 's-freeze'], ['adr', 's-adr34'], ['asyncapi', 's-adr34'], ['pr ', 's-pr412'], ['pull request', 's-pr412'], ['angular', 's-angular'], ['refund', 's-refunds'], ['incident', 's-inc301'], ['sanction', 's-inc301']]
EXAMPLES = ['Customers want to freeze a card themselves from the mobile app.', 'ADR-034 was accepted: event contracts move to AsyncAPI 3.', 'A pull request changed web-banking and there is no ticket.']
FIRST_DOCS = {0: ['need', 'req'], 1: ['add'], 2: ['asd', 'model', 'adr'], 3: ['gap'], 4: ['roadmap', 'dd'], 5: ['dor'], 6: ['baseline']}
GATE_BY = {'G1': 'Portfolio architect', 'G2': 'Architecture Board · domain architects and product stakeholders', 'G3': 'The portfolio\'s architect with the tech leads', 'G4': 'Change owner confirms · portfolio architect promotes'}
TOGAF = ['A', 'B · C · D', 'B · C · D', 'E', 'F', 'G', 'H']

INTAKE = {'origins': ORIGINS, 'changeOrigin': CHANGE_ORIGIN, 'signals': SIGNALS, 'qualified': QUALIFIED, 'match': MATCH, 'examples': EXAMPLES, 'firstDocs': FIRST_DOCS, 'gateBy': GATE_BY, 'togaf': TOGAF}
