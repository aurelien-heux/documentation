"""Delivery line of the simplified metamodel v4 (project doc architecture-metamodel-v4.md), as observed data.

Tickets come from the ticketing tool (CTX-ORC work items), commits and pull requests from Git, versions from CI.
None of it is in the LikeC4 model: these are observed nodes of the knowledge base, keyed by the ticket key, the sha
and the tag. Reference date: Tue 3 Nov 2026 (TODAY in arch_logic.js). Everything here is prototype data for
Meridian Bank."""

def t(key, title, state, implements, requirement, **kw):
    d = {'key': key, 'title': title, 'state': state, 'implements': implements, 'requirement': requirement, 'replaces': [], 'acceptance': 0}
    d.update(kw); return d

def c(sha, repo, ticket, at, via, touches, msg, **kw):
    d = {'sha': sha, 'repo': repo, 'ticket': ticket, 'at': at, 'via': via, 'touches': touches, 'msg': msg}
    d.update(kw); return d

# ticket state: done · doing · todo
TICKETS = {
    'imp.corporate.credit-request-v1': [
        t('CRD-201', 'Credit request API and workflow', 'done', ['sbb.credit-request-service.api', 'sbb.credit-request-service.credit-request-service'], 'req.corporate.credit-decision-48h', acceptance=6),
        t('CRD-202', 'Credit request data store', 'done', ['sbb.credit-request-service.credit-request-data'], 'req.corporate.credit-decision-48h', replaces=['sbb.credit-origination.credit-request-data'], acceptance=4),
        t('CRD-203', 'Pricing engine service and API', 'done', ['sbb.pricing-engine.pricing-engine', 'sbb.pricing-engine.api', 'abb.corporate.pricing-service'], 'req.corporate.credit-decision-48h', replaces=['sbb.pricing-workbook.pricing-workbook'], acceptance=5),
        t('CRD-204', 'Decision in 48 hours: SLA timers and escalation', 'doing', ['sbb.credit-request-service.credit-request-service', 'abb.corporate.credit-decision-service'], 'req.corporate.credit-decision-48h', acceptance=3),
        t('CRD-205', 'Switch off the pricing workbook', 'todo', [], 'req.corporate.credit-decision-48h', replaces=['sbb.pricing-workbook.pricing-workbook', 'abb.corporate.credit-application-process'], acceptance=2),
    ],
    'imp.payments.sepa-instant-v1': [
        t('PAY-310', 'Instant payment API (SCT Inst)', 'doing', ['sbb.instant-payments.api', 'sbb.instant-payments.instant-payments', 'abb.payments.instant-payment-service'], 'req.payments.instant-payments', acceptance=7),
        t('PAY-311', 'Payment hub routing for the instant rail', 'doing', ['sbb.payment-hub.payment-hub', 'abb.payments.payment-processing'], 'req.payments.instant-payments', acceptance=4),
        t('PAY-312', 'Sanctions screening in real time', 'todo', ['sbb.sanctions-screening.sanctions-screening'], 'req.payments.instant-payments', acceptance=3),
        t('PAY-313', 'Fraud scoring under 200 ms', 'todo', ['sbb.fraud-detection.fraud-detection'], 'req.payments.instant-payments', acceptance=3),
    ],
    'imp.retail.digital-onboarding-v1': [
        t('RET-4420', 'Onboarding API and identity check', 'doing', ['sbb.digital-onboarding.api', 'sbb.digital-onboarding.digital-onboarding', 'abb.retail.account-opening-service'], 'req.retail.online-onboarding', acceptance=8),
        t('RET-4421', 'Customer copy for onboarding', 'todo', ['sbb.digital-onboarding.customer-copy'], 'req.retail.online-onboarding', replaces=['sbb.branch-account-opening.customer-copy'], acceptance=2),
        t('RET-4422', 'Onboarding entry point in mobile banking', 'todo', ['sbb.mobile-banking.mobile-banking'], 'req.retail.online-onboarding', acceptance=3),
        t('RET-4423', 'Retire branch account opening', 'todo', [], 'req.retail.online-onboarding', replaces=['sbb.branch-account-opening.branch-account-opening', 'abb.retail.branch-onboarding-process'], acceptance=2),
    ],
    'imp.retail.web-on-mobile-platform': [
        t('RET-4510', 'Margin grid on the credit request screen', 'doing', ['sbb.web-banking.web-banking'], None, acceptance=2, note='Started before G3: the design is drafted from the code (see the detailed design of this change)'),
    ],
}

COMMITS = [
    c('a91c0f3', 'credit-request', 'CRD-201', '2 Sep', 'local', 'sbb.credit-request-service.credit-request-service', 'Credit request aggregate and workflow'),
    c('d47e2b8', 'credit-request', 'CRD-201', '9 Sep', 'sweep', 'sbb.credit-request-service.credit-request-service', 'REST API from credit-request.openapi.yaml', run='E2ECC-103702'),
    c('5be0a17', 'credit-request', 'CRD-202', '16 Sep', 'local', 'sbb.credit-request-service.credit-request-data', 'Credit request data store, migration from the monolith copy'),
    c('b7d04c9', 'pricing-engine', 'CRD-203', '25 Sep', 'sweep', 'sbb.pricing-engine.pricing-engine', 'Pricing grid service and API', run='E2ECC-103744'),
    c('3f9a1c2', 'credit-request', 'CRD-201', '18 Oct', 'local', 'sbb.credit-request-service.api', 'API v1.3: decision endpoint, contract update'),
    c('e2c71d0', 'credit-request', 'CRD-204', '30 Oct', 'sweep', 'sbb.credit-request-service.credit-request-service', 'SLA timers on the decision workflow', run='E2ECC-103851'),
    c('c3a7d14', 'payment-hub', 'PAY-311', '22 Oct', 'local', 'sbb.payment-hub.payment-hub', 'Instant rail routing, first slice'),
    c('f81b3e5', 'instant-payments', 'PAY-310', '28 Oct', 'sweep', 'sbb.instant-payments.instant-payments', 'SCT Inst request handling from the AsyncAPI contract', run='E2ECC-103833'),
    c('0a6d9c2', 'instant-payments', 'PAY-310', 'yesterday', 'local', 'sbb.instant-payments.api', 'Timeout and reject reasons'),
    c('9d3e4b1', 'digital-onboarding', 'RET-4420', '27 Oct', 'sweep', 'sbb.digital-onboarding.digital-onboarding', 'Onboarding API skeleton from the contract', run='E2ECC-103829'),
    c('7d02b18', 'web-banking', 'RET-4510', 'today 10:22', 'sweep', 'sbb.web-banking.web-banking', 'Margin grid on the credit request screen', run='E2ECC-103870'),
]

# version state: released · planned
VERSIONS = [
    {'tag': 'pricing-engine 1.0.0', 'repo': 'pricing-engine', 'at': '2 Oct', 'state': 'released', 'commits': ['b7d04c9'], 'reaches': None, 'change': 'imp.corporate.credit-request-v1', 'note': 'In staging-1'},
    {'tag': 'credit-request 1.3.0', 'repo': 'credit-request', 'at': '18 Oct', 'state': 'released', 'commits': ['a91c0f3', 'd47e2b8', '5be0a17', '3f9a1c2'], 'reaches': None, 'change': 'imp.corporate.credit-request-v1', 'note': 'In staging-1 and staging-2'},
    {'tag': 'credit-request 1.4.0', 'repo': 'credit-request', 'at': 'planned 8 Dec', 'state': 'planned', 'commits': ['e2c71d0'], 'reaches': 'imp.corporate.transition-1', 'change': 'imp.corporate.credit-request-v1', 'note': 'Reaches Transition 1 with CRD-204 and CRD-205'},
    {'tag': 'payment-hub 7.2.0', 'repo': 'payment-hub', 'at': 'planned Mar 2027', 'state': 'planned', 'commits': ['c3a7d14'], 'reaches': 'imp.payments.transition-1', 'change': 'imp.payments.sepa-instant-v1', 'note': 'Reaches Transition 1 with instant-payments 1.0.0'},
    {'tag': 'digital-onboarding 1.0.0', 'repo': 'digital-onboarding', 'at': 'planned Jan 2027', 'state': 'planned', 'commits': ['9d3e4b1'], 'reaches': 'imp.retail.transition-1', 'change': 'imp.retail.digital-onboarding-v1', 'note': 'Reaches Transition 1'},
]

# What the knowledge-base MCP server gives to a code-generation agent, besides the chain (DEC-KB-43).
STANDARDS = [
    {'id': 'ARL-CODE', 'title': 'Coding rules · Java, hexagonal modules', 'applies': ['application-component', 'application-service', 'data-object']},
    {'id': 'ARL-UI', 'title': 'UI rules · Angular, AIToolbox design system', 'applies': ['application-interface']},
]
MCP = {
    'server': 'https://kb.meridian.bank/mcp',
    'tools': [
        ['context_for_ticket', 'ticket key', 'The ticket, its acceptance criteria, the target elements it implements, the chain down to the component, contracts and standards'],
        ['context_for_module', 'application/module', 'The component, its interfaces, data objects, services, allowed dependencies, detailed design and standards'],
        ['chain', 'element id', 'Why it exists: service → process → capability → value stream, and the requirement rows it realizes'],
        ['gap', 'work package or plateau pair', 'What changes: state before → after per element, with the justifying requirement'],
        ['search', 'free text', 'Evidence with element ids and sources @ sha, the same answers as the assistant pane'],
    ],
    'clients': [
        ['Sweep', 'Already connected: every run reads its context pack from this server'],
        ['Claude Code', 'claude mcp add meridian-kb --transport http https://kb.meridian.bank/mcp'],
        ['OpenCode', 'opencode.json → "mcp": { "meridian-kb": { "type": "remote", "url": "https://kb.meridian.bank/mcp" } }'],
    ],
}

DELIV = {'tickets': TICKETS, 'commits': COMMITS, 'versions': VERSIONS, 'standards': STANDARDS, 'mcp': MCP}
