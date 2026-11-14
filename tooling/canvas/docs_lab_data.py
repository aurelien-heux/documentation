"""Data for the Docs lab architecture space: a practical example, the Corporate credit platform, a microservice
application for the corporate credit business, owned by the Request, Client and Facility teams.

The model is TOGAF / ArchiMate as data, drawn with the AIToolbox ArchiMate notation (archimate_ds): every element has a
design-system type (layer → color, aspect → shape, type → glyph), every relationship an ArchiMate relationship type
(line style and end markers). One LikeC4 view per ADM phase and plateau (landscape, motivation, value stream,
application cooperation, data, deployment, migration), as LikeC4 generates them from the model; gap views compare two
plateaus. Every fact in a picture also exists as text the knowledge base can index."""
import json
import archimate_ds as AX

PL_NAME = {'base': 'Baseline', 'tr1': 'Transition 1', 'target': 'Target'}
PL_ID = {'base': 'baseline', 'tr1': 'transition_1', 'target': 'target'}
PL_TAG = {'base': '#baseline', 'tr1': '#transition-1', 'target': '#target'}
ALL = ['base', 'tr1', 'target']
GAPS = {'gap-base-tr1': ('base', 'tr1'), 'gap-tr1-target': ('tr1', 'target'), 'gap-base-target': ('base', 'target')}
FW, FH = 176, 72          # design-system figure, size M

def N(k, name, kind, c, r, pl=ALL, **kw):
    assert kind in AX.TYPES, kind
    d = {'k': k, 'name': name, 'kind': kind, 'c': c, 'r': r, 'pl': list(pl)}
    d.update(kw)
    return d

def E(s, t, rel, label='', pl=ALL):
    assert rel in AX.RELS, rel
    return (s, t, rel, label, list(pl))

# ------------------------------------------------------------------------------------------------------------------
# Views. Grid coordinates (column, row); cw / rh = column and row pitch in px. groups = LikeC4 compound nodes,
# drawn as ArchiMate groupings: (label, first column, last column, last row).
# ------------------------------------------------------------------------------------------------------------------
VIEWS = {
    'landscape': {
        'title': 'Landscape', 'phase': 'enterprise', 'sub': 'Applications of the corporate credit business, by portfolio',
        'modes': ['base', 'tr1', 'target', 'gap'], 'cw': 264, 'rh': 128, 'top': 112,
        'groups': [('Request portfolio', 0, 0, 3), ('Client portfolio', 1, 1, 3), ('Facility portfolio', 2, 2, 3), ('Shared and external', 3, 3, 3)],
        'nodes': [
            N('portal', 'Advisor portal', 'Application component', 0, 0, owner='Request team', id='app.advisor-portal'),
            N('mono', 'Credit origination', 'Application component', 0, 1, ['base', 'tr1'], chg=['gap-base-tr1'], owner='Request team', id='app.credit-origination', nav='base_mono'),
            N('ccp', 'Corporate credit platform', 'Application component', 0, 2, ['tr1', 'target'], owner='Request, Client and Facility teams', id='app.corporate-credit', nav='application'),
            N('crm', 'CRM (Salesforce)', 'Application component', 0, 3, owner='Sales tools', id='app.crm', ext=True),
            N('cref', 'Client referential', 'Application component', 1, 0, owner='Client team', id='app.client-referential'),
            N('reng', 'Rating engine', 'Application component', 1, 1, ['base', 'tr1'], owner='Client team', id='app.rating-engine'),
            N('kyc', 'KYC system', 'Application component', 1, 2, owner='Compliance IT', id='app.kyc', ext=True),
            N('fcore', 'Facility core', 'Application component', 2, 0, ['base', 'tr1'], owner='Facility team', id='app.facility-core'),
            N('creg', 'Collateral register', 'Application component', 2, 1, ['base', 'tr1'], owner='Facility team', id='app.collateral-register'),
            N('pricing', 'Pricing workbook (Excel)', 'Application component', 2, 2, ['base'], owner='Credit analysts', id='app.pricing-workbook'),
            N('lake', 'Data lake', 'Application component', 3, 0, owner='Data team', id='app.data-lake', ext=True),
            N('ledger', 'Core banking ledger', 'Application component', 3, 1, owner='Core banking', id='app.core-banking-ledger', ext=True),
            N('archive', 'Document archive (GED)', 'Application component', 3, 2, owner='Document services', id='app.document-archive', ext=True),
            N('bo', 'BusinessObjects reports', 'Application component', 3, 3, ['base', 'tr1'], owner='Data team', id='app.bo-reports'),
        ],
        'edges': [E('mono', 'portal', 'serving', 'serves', ['base', 'tr1']), E('ccp', 'portal', 'serving', 'serves', ['tr1', 'target']),
                  E('mono', 'ccp', 'serving', 'facility set-up', ['tr1']), E('crm', 'portal', 'serving', 'client meetings'),
                  E('cref', 'mono', 'serving', 'client data', ['base']), E('cref', 'ccp', 'serving', 'client data', ['tr1', 'target']),
                  E('kyc', 'cref', 'serving', 'KYC status'), E('reng', 'mono', 'serving', 'rating', ['base']), E('reng', 'ccp', 'serving', 'rating', ['tr1']),
                  E('creg', 'mono', 'serving', 'collateral', ['base', 'tr1']), E('pricing', 'mono', 'flow', 'margins, by hand', ['base']), E('mono', 'fcore', 'flow', 'facilities', ['base', 'tr1']),
                  E('fcore', 'lake', 'flow', 'nightly export', ['base', 'tr1']), E('fcore', 'ledger', 'flow', 'bookings', ['base', 'tr1']), E('fcore', 'bo', 'flow', 'reports', ['base', 'tr1']),
                  E('ccp', 'ledger', 'flow', 'bookings', ['target']), E('ccp', 'lake', 'flow', 'events', ['tr1', 'target']),
                  E('mono', 'archive', 'flow', 'contracts', ['base', 'tr1']), E('ccp', 'archive', 'flow', 'contracts', ['target'])],
    },
    'motivation': {
        'title': 'Motivation', 'phase': 'A', 'sub': 'Why the platform changes: stakeholders, drivers, goals, principles, requirements',
        'modes': ['target'], 'cw': 248, 'rh': 140, 'top': 88, 'groups': [],
        'nodes': [
            N('st1', 'Corporate clients', 'Stakeholder', 0, 0, id='mot.cc.corporate-clients'),
            N('dr1', 'Decisions take 15 days', 'Driver', 1, 0, id='mot.cc.decision-time'),
            N('dr2', 'EBA loan origination guidelines', 'Driver', 2, 0, id='mot.cc.eba-loan-origination'),
            N('st2', 'Credit risk', 'Stakeholder', 3, 0, id='mot.cc.credit-risk'),
            N('p1', 'Read client data, never copy it', 'Principle', 0, 1, id='mot.ent.read-never-copy'),
            N('g1', 'Decide in 5 days', 'Goal', 1, 1, id='mot.cc.decide-in-5-days'),
            N('g2', 'One view of exposure', 'Goal', 2, 1, id='mot.cc.one-view-of-exposure'),
            N('p2', 'Events over batch', 'Principle', 3, 1, id='mot.ent.events-over-batch'),
            N('r1', 'Decision in 5 working days', 'Requirement', 0, 2, id='req.corporate-credit.decision-time'),
            N('r2', 'Limit check before the decision', 'Requirement', 1, 2, id='req.corporate-credit.limit-check'),
            N('r3', 'Four-eyes above 5 M EUR', 'Requirement', 2, 2, id='req.corporate-credit.four-eyes'),
            N('r4', 'Every decision traceable', 'Requirement', 3, 2, id='req.corporate-credit.audit'),
        ],
        'edges': [E('st1', 'dr1', 'association', 'concerned by'), E('st2', 'dr2', 'association', 'concerned by'),
                  E('dr1', 'g1', 'influence'), E('dr2', 'g2', 'influence'),
                  E('r1', 'g1', 'realization'), E('r2', 'g1', 'realization'), E('r3', 'g2', 'realization'), E('r4', 'g2', 'realization'),
                  E('p1', 'r1', 'influence'), E('p2', 'r4', 'influence')],
    },
    'business': {
        'title': 'Value stream', 'phase': 'B', 'sub': 'The corporate credit value stream, who performs each stage, which services serve them. Open a stage to see its business processes.',
        'modes': ['target'], 'cw': 216, 'rh': 140, 'top': 88, 'groups': [],
        'nodes': [
            N('s1', 'Request', 'Value stream', 0, 0, id='str.cc.request'),
            N('s2', 'Analyse', 'Value stream', 1, 0, id='str.cc.analyse'),
            N('s3', 'Decide', 'Value stream', 2, 0, id='str.cc.decide', nav='stage_decide'),
            N('s4', 'Contract', 'Value stream', 3, 0, id='str.cc.contract'),
            N('s5', 'Set up the facility', 'Value stream', 4, 0, id='str.cc.set-up', nav='stage_setup'),
            N('s6', 'Monitor', 'Value stream', 5, 0, id='str.cc.monitor'),
            N('a1', 'Relationship manager', 'Business role', 0, 1, id='bus.cc.relationship-manager'),
            N('a2', 'Credit analyst', 'Business role', 1, 1, id='bus.cc.credit-analyst'),
            N('a3', 'Credit committee', 'Business role', 2, 1, id='bus.cc.credit-committee'),
            N('a5', 'Facility officer', 'Business role', 4, 1, id='bus.cc.facility-officer'),
            N('v1', 'Credit request', 'Application service', 0, 2, id='sbb.credit-request-api'),
            N('v2', 'Rating', 'Application service', 1, 2, id='sbb.rating-api'),
            N('v3', 'Credit decision', 'Application service', 2, 2, id='sbb.decision-api'),
            N('v4', 'Contract drafting', 'Application service', 3, 2, id='sbb.document-api'),
            N('v5', 'Facility set-up', 'Application service', 4, 2, id='sbb.facility-api'),
            N('v6', 'Limit check', 'Application service', 5, 2, id='sbb.limit-api'),
        ],
        'edges': [E('s1', 's2', 'flow'), E('s2', 's3', 'flow'), E('s3', 's4', 'flow'), E('s4', 's5', 'flow'), E('s5', 's6', 'flow'),
                  E('a1', 's1', 'assignment'), E('a2', 's2', 'assignment'), E('a3', 's3', 'assignment'), E('a5', 's5', 'assignment'),
                  E('v1', 'a1', 'serving'), E('v2', 'a2', 'serving'), E('v3', 'a3', 'serving'), E('v4', 's4', 'serving'), E('v5', 'a5', 'serving'), E('v6', 's6', 'serving')],
    },
    'stage_decide': {
        'title': 'Decide', 'parent': 'business', 'phase': 'B', 'sub': 'Value stream stage · the business processes that take the credit decision',
        'modes': ['target'], 'cw': 232, 'rh': 140, 'top': 88, 'groups': [],
        'nodes': [
            N('e1', 'Credit file complete', 'Business event', 0, 0, id='bus.cc.event.file-complete'),
            N('p1', 'Present the credit file', 'Business process', 1, 0, id='bus.cc.present-file'),
            N('p2', 'Committee decision', 'Business process', 2, 0, id='bus.cc.committee-decision', nav='process_committee'),
            N('p3', 'Four-eyes approval', 'Business process', 3, 0, id='bus.cc.four-eyes'),
            N('e2', 'Credit decided', 'Business event', 4, 0, id='bus.cc.event.decided'),
            N('a2', 'Credit analyst', 'Business role', 1, 1, id='bus.cc.credit-analyst'),
            N('a3', 'Credit committee', 'Business role', 2, 1, id='bus.cc.credit-committee'),
            N('a4', 'Senior approver', 'Business role', 3, 1, id='bus.cc.senior-approver'),
            N('o1', 'Credit file', 'Business object', 1, 2, id='bus.cc.credit-file'),
            N('v3', 'Credit decision', 'Application service', 2, 2, id='sbb.decision-api'),
            N('o2', 'Credit decision record', 'Business object', 3, 2, id='bus.cc.decision-record'),
            N('v6', 'Limit check', 'Application service', 4, 2, id='sbb.limit-api'),
        ],
        'edges': [E('e1', 'p1', 'triggering'), E('p1', 'p2', 'triggering'), E('p2', 'p3', 'triggering', 'above 5 M EUR'), E('p3', 'e2', 'triggering'),
                  E('a2', 'p1', 'assignment'), E('a3', 'p2', 'assignment'), E('a4', 'p3', 'assignment'),
                  E('p1', 'o1', 'access', 'writes'), E('p3', 'o2', 'access', 'writes'), E('v3', 'p2', 'serving'), E('v6', 'p2', 'serving', 'limit check')],
    },
    'process_committee': {
        'title': 'Committee decision', 'parent': 'stage_decide', 'phase': 'B', 'sub': 'Business process · each step, who does it and the application services behind it',
        'modes': ['target'], 'cw': 232, 'rh': 140, 'top': 88, 'groups': [],
        'nodes': [
            N('e1', 'File on the agenda', 'Business event', 0, 0, id='bus.cc.event.on-agenda'),
            N('s1', 'Check completeness', 'Business process', 1, 0, id='bus.cc.committee.check-completeness'),
            N('s2', 'Check group limits', 'Business process', 2, 0, id='bus.cc.committee.check-limits'),
            N('s3', 'Debate and vote', 'Business process', 3, 0, id='bus.cc.committee.vote'),
            N('e2', 'Decision recorded', 'Business event', 4, 0, id='bus.cc.event.decision-recorded'),
            N('r1', 'Committee secretary', 'Business role', 1, 1, id='bus.cc.committee-secretary'),
            N('r2', 'Credit committee', 'Business role', 3, 1, id='bus.cc.credit-committee'),
            N('v1', 'Credit decision', 'Application service', 1, 2, id='sbb.decision-api', nav='application'),
            N('v2', 'Limit check', 'Application service', 2, 2, id='sbb.limit-api', nav='application'),
            N('d1', 'Credit decision record', 'Business object', 4, 1, id='bus.cc.decision-record'),
        ],
        'edges': [E('e1', 's1', 'triggering'), E('s1', 's2', 'triggering'), E('s2', 's3', 'triggering', 'within limits'), E('s3', 'e2', 'triggering'),
                  E('r1', 's1', 'assignment'), E('r2', 's3', 'assignment'), E('v1', 's1', 'serving'), E('v2', 's2', 'serving', 'under 200 ms'),
                  E('s3', 'd1', 'access', 'writes')],
    },
    'stage_setup': {
        'title': 'Set up the facility', 'parent': 'business', 'phase': 'B', 'sub': 'Value stream stage · from the signed contract to an active facility',
        'modes': ['target'], 'cw': 232, 'rh': 140, 'top': 88, 'groups': [],
        'nodes': [
            N('e1', 'Contract signed', 'Business event', 0, 0, id='bus.cc.event.contract-signed'),
            N('p1', 'Book the limit', 'Business process', 1, 0, id='bus.cc.book-limit'),
            N('p2', 'Link the collateral', 'Business process', 2, 0, id='bus.cc.link-collateral'),
            N('p3', 'Activate the facility', 'Business process', 3, 0, id='bus.cc.activate-facility', nav='cmp_facility'),
            N('e2', 'Facility active', 'Business event', 4, 0, id='bus.cc.event.facility-active'),
            N('a5', 'Facility officer', 'Business role', 2, 1, id='bus.cc.facility-officer'),
            N('v6', 'Limit check', 'Application service', 1, 2, id='sbb.limit-api'),
            N('v7', 'Collateral valuation', 'Application service', 2, 2, id='sbb.collateral-api'),
            N('v5', 'Facility set-up', 'Application service', 3, 2, id='sbb.facility-api', nav='cmp_facility'),
            N('o3', 'Facility', 'Business object', 4, 1, id='bus.cc.facility'),
        ],
        'edges': [E('e1', 'p1', 'triggering'), E('p1', 'p2', 'triggering'), E('p2', 'p3', 'triggering', 'collateral ≥ 100 %'), E('p3', 'e2', 'triggering'),
                  E('a5', 'p2', 'assignment'), E('a5', 'p3', 'assignment'), E('v6', 'p1', 'serving'), E('v7', 'p2', 'serving'), E('v5', 'p3', 'serving'),
                  E('p3', 'o3', 'access', 'activates')],
    },
    'application': {
        'title': 'Application cooperation', 'phase': 'C', 'sub': 'The microservices and how they work together. Open a service to see inside it.',
        'modes': ['base', 'tr1', 'target', 'gap'], 'cw': 264, 'rh': 136, 'top': 88, 'groups': [],
        'nodes': [
            N('portal', 'Advisor portal', 'Application component', 0, 0, ext=True, id='app.advisor-portal'),
            N('gw', 'API gateway', 'Application interface', 1, 0, ['tr1', 'target'], id='sbb.api-gateway', wp='wp1'),
            N('req', 'credit-request-service', 'Application component', 2, 0, ['tr1', 'target'], id='sbb.credit-request-service', wp='wp1', nav='cmp_request'),
            N('cli', 'client-service', 'Application component', 3, 0, ['tr1', 'target'], id='sbb.client-service', wp='wp1'),
            N('cref', 'Client referential', 'Application component', 4, 0, ext=True, id='app.client-referential'),
            N('mono', 'Credit origination', 'Application component', 0, 1, ['base', 'tr1'], chg=['gap-base-tr1'], id='app.credit-origination', wp='wp4', nav='base_mono'),
            N('rat', 'rating-service', 'Application component', 1, 1, ['target'], id='sbb.rating-service', wp='wp2'),
            N('wf', 'decision-workflow', 'Application process', 2, 1, ['tr1', 'target'], id='sbb.decision-workflow', wp='wp1', nav='process_committee'),
            N('doc', 'document-service', 'Application component', 3, 1, ['target'], id='sbb.document-service', wp='wp2'),
            N('reng', 'Rating engine', 'Application component', 4, 1, ['base', 'tr1'], id='app.rating-engine', wp='wp2'),
            N('pricing', 'Pricing workbook (Excel)', 'Application component', 0, 2, ['base'], id='app.pricing-workbook', wp='wp1'),
            N('lim', 'limit-service', 'Application component', 1, 2, ['target'], id='sbb.credit-request-service.credit-request-service', wp='wp2'),
            N('fac', 'facility-service', 'Application component', 2, 2, ['target'], id='sbb.facility-service.facility-service', wp='wp2', nav='cmp_facility'),
            N('col', 'collateral-service', 'Application component', 3, 2, ['target'], id='sbb.collateral-service', wp='wp2'),
            N('kyc', 'KYC system', 'Application component', 4, 2, ext=True, id='app.kyc'),
            N('creg', 'Collateral register', 'Application component', 0, 3, ['base', 'tr1'], id='app.collateral-register', wp='wp2'),
            N('fcore', 'Facility core', 'Application component', 1, 3, ['base', 'tr1'], id='app.facility-core', wp='wp4'),
            N('ledger', 'Core banking ledger', 'Application component', 2, 3, ext=True, id='app.core-banking-ledger'),
            N('bo', 'BusinessObjects reports', 'Application component', 3, 3, ['base', 'tr1'], id='app.bo-reports', wp='wp3'),
            N('kafka', 'cc.events', 'Application event', 4, 3, ['tr1', 'target'], id='sbb.events', wp='wp1'),
            N('exp', 'Nightly facility exports', 'Application process', 1, 4, ['base', 'tr1'], id='app.facility-exports', wp='wp3'),
            N('archive', 'Document archive (GED)', 'Application component', 3, 4, ext=True, id='app.document-archive'),
            N('lake', 'Data lake', 'Application component', 4, 4, ext=True, id='app.data-lake'),
        ],
        'edges': [
            E('mono', 'portal', 'serving', 'serves', ['base']), E('cref', 'mono', 'serving', 'client data', ['base']), E('reng', 'mono', 'serving', 'rating', ['base']),
            E('kyc', 'mono', 'serving', 'KYC status', ['base']), E('pricing', 'mono', 'flow', 'margins', ['base']),
            E('creg', 'mono', 'serving', 'collateral', ['base', 'tr1']), E('mono', 'fcore', 'flow', 'facilities', ['base', 'tr1']),
            E('fcore', 'ledger', 'flow', 'bookings', ['base', 'tr1']), E('fcore', 'exp', 'flow', 'facilities', ['base', 'tr1']), E('exp', 'lake', 'flow', 'nightly load', ['base', 'tr1']),
            E('fcore', 'bo', 'flow', 'reports', ['base', 'tr1']), E('mono', 'archive', 'flow', 'contracts', ['base', 'tr1']),
            E('gw', 'portal', 'serving', 'serves', ['tr1', 'target']), E('gw', 'req', 'flow', 'routes', ['tr1', 'target']), E('cli', 'req', 'serving', 'client', ['tr1', 'target']),
            E('cref', 'cli', 'serving', 'client data', ['tr1', 'target']), E('kyc', 'cli', 'serving', 'KYC status', ['tr1', 'target']), E('req', 'wf', 'triggering', 'starts', ['tr1', 'target']),
            E('mono', 'wf', 'serving', 'facility set-up', ['tr1']), E('reng', 'wf', 'serving', 'rating', ['tr1']), E('wf', 'kafka', 'triggering', 'publishes', ['tr1']),
            E('rat', 'wf', 'serving', 'rating', ['target']), E('doc', 'wf', 'serving', 'contract', ['target']), E('lim', 'wf', 'serving', 'limit check', ['target']),
            E('wf', 'fac', 'triggering', 'set up', ['target']), E('fac', 'lim', 'flow', 'books limit', ['target']), E('col', 'fac', 'serving', 'collateral', ['target']),
            E('fac', 'ledger', 'flow', 'bookings', ['target']), E('fac', 'kafka', 'triggering', 'publishes', ['target']), E('kafka', 'lake', 'flow', 'streams', ['tr1', 'target']),
            E('doc', 'archive', 'flow', 'contracts', ['target']),
        ],
    },
    'base_mono': {
        'title': 'Inside Credit origination', 'parent': 'application', 'phase': 'C', 'sub': 'Baseline · the monolith’s modules, its shared Oracle schema and its batch and file interfaces',
        'modes': ['base'], 'cw': 248, 'rh': 136, 'top': 120,
        'groups': [('Credit origination · WebLogic 12c', 1, 3, 2)],
        'nodes': [
            N('portal', 'Advisor portal', 'Application component', 0, 0, ext=True, id='app.advisor-portal'),
            N('m1', 'Request module', 'Application component', 1, 0, ['base'], id='app.credit-origination.request'),
            N('m2', 'Decision module', 'Application component', 2, 0, ['base'], id='app.credit-origination.decision'),
            N('m3', 'Facility module', 'Application component', 3, 0, ['base'], id='app.credit-origination.facility'),
            N('m4', 'Collateral module', 'Application component', 1, 1, ['base'], id='app.credit-origination.collateral'),
            N('m5', 'Pricing import', 'Application process', 2, 1, ['base'], id='app.credit-origination.pricing-import'),
            N('m6', 'Reports module', 'Application component', 3, 1, ['base'], id='app.credit-origination.reports'),
            N('db', 'Schema CREDIT (Oracle)', 'Data object', 2, 2, ['base'], id='data.credit-origination.schema'),
            N('cref', 'Client referential', 'Application component', 0, 1, ext=True, id='app.client-referential'),
            N('reng', 'Rating engine', 'Application component', 0, 2, ['base', 'tr1'], id='app.rating-engine'),
            N('fcore', 'Facility core', 'Application component', 4, 0, ['base', 'tr1'], id='app.facility-core'),
            N('ledger', 'Core banking ledger', 'Application component', 4, 1, ext=True, id='app.core-banking-ledger'),
            N('pricing', 'Pricing workbook (Excel)', 'Application component', 4, 2, ['base'], id='app.pricing-workbook'),
        ],
        'edges': [E('m1', 'portal', 'serving', 'screens'), E('m1', 'm2', 'triggering', 'submits'), E('m2', 'm3', 'triggering', 'approved'),
                  E('m4', 'm3', 'serving', 'collateral'), E('cref', 'm1', 'serving', 'nightly copy'), E('reng', 'm2', 'serving', 'rating'),
                  E('m3', 'fcore', 'flow', 'facilities'), E('fcore', 'ledger', 'flow', 'MQ bookings'), E('pricing', 'm5', 'flow', 'CSV upload'),
                  E('m5', 'db', 'access', 'writes'), E('m6', 'db', 'access', 'reads'), E('m2', 'db', 'access', 'writes')],
    },
    'cmp_facility': {
        'title': 'Inside facility-service', 'parent': 'application', 'phase': 'C', 'sub': 'Hexagonal architecture · inbound adapters and use cases around the domain, outbound ports to the other services. Each element opens its detailed design.',
        'modes': ['target'], 'cw': 248, 'rh': 144, 'top': 120,
        'groups': [('Inbound adapters', 0, 0, 2), ('Application · use cases', 1, 1, 2), ('Outbound ports', 2, 2, 4), ('Domain', 0, 1, 4, 3)],
        'nodes': [
            N('rest', 'REST API /facilities', 'Application interface', 0, 0, id='sbb.facility-service.facility-service.rest', dd='dd.cc-facility.api'),
            N('lis', 'Decision events listener', 'Application interface', 0, 1, id='sbb.facility-service.facility-service.listener', dd='dd.cc-facility.infrastructure'),
            N('job', 'Covenant review job', 'Application process', 0, 2, id='sbb.facility-service.facility-service.review-job', dd='dd.cc-facility.infrastructure'),
            N('uc1', 'Set up a facility', 'Application function', 1, 0, id='sbb.facility-service.facility-service.set-up', dd='dd.cc-facility.application'),
            N('uc2', 'Amend a facility', 'Application function', 1, 1, id='sbb.facility-service.facility-service.amend', dd='dd.cc-facility.application'),
            N('uc3', 'Review a facility', 'Application function', 1, 2, id='sbb.facility-service.facility-service.review', dd='dd.cc-facility.application'),
            N('cov', 'Covenant', 'Data object', 0, 3, id='data.cc.covenant', dd='dd.cc-facility.domain'),
            N('agg', 'Facility (aggregate)', 'Data object', 1, 3, id='data.cc.facility', dd='dd.cc-facility.domain'),
            N('evt', 'FacilityActivated', 'Application event', 1, 4, id='sbb.facility-service.facility-service.activated', dd='dd.cc-facility.domain-events'),
            N('ver', 'FacilityVersion', 'Data object', 0, 4, id='data.cc.facility-version', dd='dd.cc-facility.data-model'),
            N('pt1', 'LimitBooking', 'Application interface', 2, 0, id='sbb.facility-service.facility-service.limit-booking', dd='dd.cc-facility.ports'),
            N('pt2', 'CollateralLink', 'Application interface', 2, 1, id='sbb.facility-service.facility-service.collateral-link', dd='dd.cc-facility.ports'),
            N('pt3', 'LedgerBooking', 'Application interface', 2, 2, id='sbb.facility-service.facility-service.ledger-booking', dd='dd.cc-facility.ports'),
            N('pt4', 'EventPublisher', 'Application interface', 2, 3, id='sbb.facility-service.facility-service.event-publisher', dd='dd.cc-facility.ports'),
            N('pt5', 'FacilityStore', 'Application interface', 2, 4, id='sbb.facility-service.facility-service.store', dd='dd.cc-facility.data-model'),
            N('lim', 'limit-service', 'Application component', 3, 0, id='sbb.credit-request-service.credit-request-service'),
            N('col', 'collateral-service', 'Application component', 3, 1, id='sbb.collateral-service'),
            N('ledger', 'Core banking ledger', 'Application component', 3, 2, ext=True, id='app.core-banking-ledger'),
            N('kafka', 'cc.events', 'Application event', 3, 3, id='sbb.events'),
            N('pg', 'PostgreSQL 16 · facility', 'System software', 3, 4, id='std.postgresql'),
        ],
        'edges': [E('rest', 'uc1', 'flow', 'POST'), E('lis', 'uc1', 'flow', 'approved'), E('rest', 'uc2', 'flow', 'amend'), E('job', 'uc3', 'triggering', 'yearly'),
                  E('uc1', 'agg', 'access', 'creates'), E('uc3', 'cov', 'access', 'tests'), E('agg', 'cov', 'composition'), E('agg', 'ver', 'composition'), E('agg', 'evt', 'triggering', 'raises'),
                  E('pt1', 'uc1', 'serving'), E('pt2', 'uc1', 'serving'), E('pt3', 'uc1', 'serving'), E('pt4', 'evt', 'serving', 'outbox'), E('pt5', 'agg', 'serving', 'stores'),
                  E('pt1', 'lim', 'flow', 'REST'), E('pt2', 'col', 'flow', 'REST'), E('pt3', 'ledger', 'flow', 'IBM MQ'), E('pt4', 'kafka', 'flow', 'Kafka'), E('pt5', 'pg', 'flow', 'JPA')],
    },
    'cmp_request': {
        'title': 'Inside credit-request-service', 'parent': 'application', 'phase': 'C', 'sub': 'Hexagonal architecture · the request from draft to decision',
        'modes': ['target'], 'cw': 248, 'rh': 144, 'top': 120,
        'groups': [('Inbound adapters', 0, 0, 1), ('Application · use cases', 1, 1, 1), ('Outbound ports', 2, 2, 2), ('Domain', 0, 1, 2, 2)],
        'nodes': [
            N('rest', 'REST API /requests', 'Application interface', 0, 0, id='sbb.credit-request-service.rest', dd='dd.cc-request.api'),
            N('uc1', 'Create a request', 'Application function', 1, 0, id='sbb.credit-request-service.create', dd='dd.cc-request.domain'),
            N('uc2', 'Submit a request', 'Application function', 1, 1, id='sbb.credit-request-service.submit', dd='dd.cc-request.domain'),
            N('evt', 'RequestSubmitted', 'Application event', 0, 2, id='sbb.credit-request-service.submitted', dd='dd.cc-request.domain'),
            N('agg', 'Credit request (aggregate)', 'Data object', 1, 2, id='data.cc.credit-request', dd='dd.cc-request.domain'),
            N('pt1', 'ClientReader', 'Application interface', 2, 0, id='sbb.credit-request-service.client-reader', dd='dd.cc-request.domain'),
            N('pt2', 'WorkflowStarter', 'Application interface', 2, 1, id='sbb.credit-request-service.workflow-starter', dd='dd.cc-request.domain'),
            N('pt3', 'RequestStore', 'Application interface', 2, 2, id='sbb.credit-request-service.store', dd='dd.cc-request.data-model'),
            N('cli', 'client-service', 'Application component', 3, 0, id='sbb.client-service'),
            N('wf', 'decision-workflow', 'Application process', 3, 1, id='sbb.decision-workflow'),
            N('pg', 'PostgreSQL 16 · request', 'System software', 3, 2, id='std.postgresql'),
        ],
        'edges': [E('rest', 'uc1', 'flow', 'POST'), E('rest', 'uc2', 'flow', 'submit'), E('uc2', 'agg', 'access', 'submits'), E('uc1', 'agg', 'access', 'creates'),
                  E('agg', 'evt', 'triggering', 'raises'), E('pt1', 'uc1', 'serving'), E('pt2', 'uc2', 'serving'), E('pt3', 'agg', 'serving', 'stores'),
                  E('pt1', 'cli', 'flow', 'REST'), E('pt2', 'wf', 'flow', 'Camunda'), E('pt3', 'pg', 'flow', 'JPA')],
    },
    'data': {
        'title': 'Data', 'phase': 'C', 'sub': 'Business data and the service that owns each',
        'modes': ['target'], 'cw': 248, 'rh': 140, 'top': 88, 'groups': [],
        'nodes': [
            N('d2', 'Client', 'Data object', 0, 0, owner='client-service', id='data.cc.client'),
            N('d1', 'Credit request', 'Data object', 1, 0, owner='credit-request-service', id='data.cc.credit-request', dd='dd.cc-request.data-model'),
            N('d3', 'Rating', 'Data object', 2, 0, owner='rating-service', id='data.cc.rating'),
            N('d8', 'Credit event', 'Data object', 3, 0, owner='cc.events (Kafka)', id='data.cc.credit-event'),
            N('d5', 'Limit', 'Data object', 0, 1, owner='limit-service', id='data.cc.limit', dd='dd.cc-limit.domain'),
            N('d4', 'Facility', 'Data object', 1, 1, owner='facility-service', id='data.cc.facility', dd='dd.cc-facility.data-model'),
            N('d6', 'Collateral', 'Data object', 2, 1, owner='collateral-service', id='data.cc.collateral'),
            N('d7', 'Contract', 'Data object', 1, 2, owner='document-service', id='data.cc.contract'),
            N('d9', 'Covenant', 'Data object', 2, 2, owner='facility-service', id='data.cc.covenant', dd='dd.cc-facility.domain'),
        ],
        'edges': [E('d1', 'd2', 'association', 'for'), E('d1', 'd3', 'association', 'uses'), E('d4', 'd1', 'association', 'results from'),
                  E('d4', 'd5', 'association', 'consumes'), E('d4', 'd6', 'association', 'secured by'), E('d7', 'd4', 'association', 'formalises'),
                  E('d8', 'd4', 'association', 'about'), E('d4', 'd9', 'composition', 'has')],
    },
    'technology': {
        'title': 'Deployment', 'phase': 'D', 'sub': 'Where the platform runs, today and in the target',
        'modes': ['base', 'target', 'gap'], 'cw': 248, 'rh': 136, 'top': 120,
        'groups': [('OpenShift cluster · cc-prod', 1, 2, 1)],
        'nodes': [
            N('lb', 'API gateway (Kong)', 'Technology service', 0, 0, ['target'], id='std.kong'),
            N('ns1', 'Namespace cc-request', 'Node', 1, 0, ['target'], id='tec.cc.ns-request'),
            N('ns2', 'Namespace cc-client', 'Node', 2, 0, ['target'], id='tec.cc.ns-client'),
            N('pg', 'PostgreSQL 16', 'System software', 3, 0, ['target'], id='std.postgresql'),
            N('wls', 'WebLogic 12c cluster', 'Node', 0, 1, ['base'], id='tec.cc.weblogic'),
            N('ns3', 'Namespace cc-facility', 'Node', 1, 1, ['target'], id='tec.cc.ns-facility'),
            N('kaf', 'Kafka', 'System software', 2, 1, ['target'], id='std.kafka'),
            N('vault', 'Vault', 'System software', 3, 1, ['target'], id='std.vault'),
            N('ora', 'Oracle 12c RAC', 'System software', 0, 2, ['base'], id='tec.cc.oracle'),
            N('batch', 'Control-M', 'Technology service', 1, 2, ['base'], id='std.control-m'),
            N('argo', 'ArgoCD', 'System software', 2, 2, ['target'], id='std.argocd'),
            N('mq', 'IBM MQ', 'System software', 3, 2, id='std.ibm-mq'),
            N('sftp', 'SFTP gateway', 'Technology service', 0, 3, ['base'], id='std.sftp'),
            N('bos', 'BusinessObjects server', 'Node', 1, 3, ['base'], id='tec.cc.bo-server'),
        ],
        'edges': [E('lb', 'ns1', 'serving', 'routes', ['target']), E('ns1', 'kaf', 'flow', 'events', ['target']), E('ns3', 'kaf', 'flow', 'events', ['target']),
                  E('pg', 'ns2', 'serving', 'stores', ['target']), E('vault', 'ns3', 'serving', 'secrets', ['target']), E('argo', 'ns3', 'serving', 'deploys', ['target']),
                  E('ns3', 'mq', 'flow', 'ledger bookings', ['target']), E('ora', 'wls', 'serving', 'stores', ['base']), E('wls', 'mq', 'flow', 'ledger bookings', ['base']),
                  E('batch', 'ora', 'access', 'extracts', ['base']), E('batch', 'sftp', 'flow', 'exports', ['base']), E('bos', 'ora', 'access', 'reads', ['base'])],
    },
    'migration': {
        'title': 'Migration', 'phase': 'EF', 'sub': 'Plateaus, the gaps between them and the work packages that close them',
        'modes': ['target'], 'cw': 248, 'rh': 140, 'top': 88, 'groups': [],
        'nodes': [
            N('pb', 'Baseline · today', 'Plateau', 0, 0, id='imp.corporate-credit.baseline', nav='landscape', navMode='base'),
            N('pt', 'Transition 1 · Dec 2026', 'Plateau', 2, 0, id='imp.corporate-credit.transition-1', nav='landscape', navMode='tr1'),
            N('pg', 'Target · Jun 2027', 'Plateau', 4, 0, id='imp.corporate-credit.target', nav='landscape', navMode='target'),
            N('g1', 'Strangle the monolith', 'Gap', 1, 1, id='imp.corporate-credit.gap-1'),
            N('g2', 'Retire the monolith and Oracle', 'Gap', 3, 1, id='imp.corporate-credit.gap-2'),
            N('w1', 'Extract client and request', 'Work package', 1, 2, id='imp.corporate-credit.wp1'),
            N('w2', 'Extract facility, limits, collateral', 'Work package', 2, 2, id='imp.corporate-credit.wp2'),
            N('w3', 'Events replace nightly exports', 'Work package', 3, 2, id='imp.corporate-credit.wp3'),
            N('w4', 'Retire Credit origination', 'Work package', 4, 2, id='imp.corporate-credit.wp4'),
        ],
        'edges': [E('pb', 'pt', 'triggering', 'Dec 2026'), E('pt', 'pg', 'triggering', 'Jun 2027'),
                  E('g1', 'pb', 'association'), E('g1', 'pt', 'association'), E('g2', 'pt', 'association'), E('g2', 'pg', 'association'),
                  E('w1', 'g1', 'realization', 'closes'), E('w2', 'g2', 'realization'), E('w3', 'g2', 'realization'), E('w4', 'g2', 'realization')],
    },
}
VIEW_ORDER = ['landscape', 'motivation', 'business', 'stage_decide', 'process_committee', 'stage_setup', 'application', 'base_mono', 'cmp_facility', 'cmp_request', 'data', 'technology', 'migration']
PHASES = [('enterprise', 'Enterprise', 'Portfolio of applications'), ('A', 'Phase A · Architecture vision', 'Why the change'),
          ('B', 'Phase B · Business architecture', 'Who does what'), ('C', 'Phase C · Information systems', 'Applications and data'),
          ('D', 'Phase D · Technology architecture', 'Where it runs'), ('EF', 'Phases E–F · Opportunities and migration', 'How we get there')]
# component internals exist only once their service exists: the target
_seen = {}
for _k in VIEW_ORDER:
    for _n in VIEWS[_k]['nodes']:
        _seen.setdefault(_n['id'], []).append(_k)
for _k in ('cmp_facility', 'cmp_request'):
    for _n in VIEWS[_k]['nodes']:
        if _n['pl'] == ALL and not _n.get('ext') and _seen[_n['id']] == [_k]:
            _n['pl'] = ['target']


# ------------------------------------------------------------------------------------------------------------------
# Element details: what the panel shows and the knowledge base indexes, one document per element
# ------------------------------------------------------------------------------------------------------------------
def svc(owner, desc, realizes, dd, contract, adrs, origin='authored', arb=''):
    return {'owner': owner, 'desc': desc, 'realizes': realizes, 'dd': dd, 'contract': contract, 'adrs': adrs, 'origin': origin, 'arb': arb}

DETAIL = {
    'sbb.credit-request-service': svc('Request team', 'Takes a corporate credit request from the advisor portal, reads the client from client-service and starts the decision workflow.', 'abb.corporate-credit.request-intake', ['dd.cc-request.domain', 'dd.cc-request.api', 'dd.cc-request.data-model'], 'credit-request-service/contracts/requests.openapi.yaml', ['ADR-CC-01', 'ADR-CC-04'], arb='arb.request.2026-09'),
    'sbb.decision-workflow': svc('Request team', 'Runs the decision: rating, limit check, four-eyes approval above 5 M EUR, contract, facility set-up. Camunda process.', 'abb.corporate-credit.credit-decision', [], 'decision-workflow/bpmn/corporate-credit.bpmn', ['ADR-CC-03'], arb='arb.request.2026-09'),
    'sbb.client-service': svc('Client team', 'The client as the credit platform sees it: legal entity, group, KYC status. Reads the client referential; never copies it.', 'abb.corporate-credit.client-view', [], 'client-service/contracts/clients.openapi.yaml', ['ADR-CC-04'], arb='arb.request.2026-09'),
    'sbb.rating-service': svc('Client team', 'Internal rating of a corporate client, from financial statements and group links. Replaces the rating engine.', 'abb.corporate-credit.rating', [], 'rating-service/contracts/ratings.openapi.yaml', [], arb='arb.facility.2026-14'),
    'sbb.document-service': svc('Platform team', 'Drafts the credit agreement from a template and the decision; stores the signed contract.', 'abb.corporate-credit.contracting', [], 'document-service/contracts/documents.openapi.yaml', [], arb='arb.facility.2026-14'),
    'sbb.facility-service.facility-service': svc('Facility team', 'Sets up the facility once the contract is signed: books the limit, links collateral, books in the ledger, then follows drawdowns and reviews.', 'abb.corporate-credit.facility-management', ['dd.cc-facility.domain', 'dd.cc-facility.domain-events', 'dd.cc-facility.ports', 'dd.cc-facility.application', 'dd.cc-facility.infrastructure', 'dd.cc-facility.api', 'dd.cc-facility.data-model'], 'facility-service/contracts/facilities.openapi.yaml', ['ADR-CC-02', 'ADR-CC-03', 'ADR-CC-06'], arb='arb.facility.2026-14'),
    'sbb.credit-request-service.credit-request-service': svc('Facility team', 'Holds limits per client and group and answers the limit check in real time.', 'abb.corporate-credit.limits', ['dd.cc-limit.domain', 'dd.cc-limit.api'], 'limit-service/contracts/limits.asyncapi.yaml', ['ADR-CC-03'], arb='arb.facility.2026-14'),
    'sbb.collateral-service': svc('Facility team', 'Collateral linked to facilities and its valuation. Detailed design not written yet.', 'abb.corporate-credit.collateral', [], '', ['ADR-CC-05'], arb='arb.facility.2026-14'),
    'sbb.api-gateway': svc('Platform team', 'Single entry for the advisor portal: authentication, routing, rate limits.', 'abb.corporate-credit.channel-access', [], '', ['ADR-CC-01'], arb='arb.request.2026-09'),
    'sbb.events': svc('Platform team', 'Business events of the credit lifecycle: request submitted, decision taken, facility active.', 'abb.corporate-credit.credit-events', [], 'contracts/cc-events.asyncapi.yaml', ['ADR-CC-02'], arb='arb.facility.2026-14'),
    'app.credit-origination': svc('Request team', 'The monolith that runs corporate credit today. In transition 1 it keeps facilities, limits and collateral; it is retired in the target.', '—', [], '', ['ADR-CC-01'], origin='extracted'),
    'app.facility-core': svc('Facility team', 'Oracle schema of facilities and limits used by the monolith and the nightly exports. Retired in the target.', '—', [], '', ['ADR-CC-06'], origin='extracted'),
    'app.collateral-register': svc('Facility team (from the catalog)', 'Legacy register of collateral. Documented from its code; no architect has authored it yet.', '—', [], '', [], origin='inferred'),
    'app.facility-exports': svc('Facility team', 'Nightly batch that copies facilities to the data lake. Replaced by events in the target.', '—', [], '', ['ADR-CC-02'], origin='extracted'),
    'app.rating-engine': svc('Client team', 'Legacy rating engine, replaced by rating-service in the target.', '—', [], '', [], origin='extracted'),
    'app.client-referential': svc('Client team', 'Group-wide client referential. Read through client-service from transition 1.', '—', [], '', ['ADR-CC-04']),
}

# ------------------------------------------------------------------------------------------------------------------
# Detailed design (tier 1 design intent), per service
# ------------------------------------------------------------------------------------------------------------------
def dd(id_, title, layer, module, sections, path, commit, kind):
    return {'id': id_, 'title': title, 'layer': layer, 'kind': kind, 'module': module, 'sections': sections, 'path': path, 'commit': commit,
            'realizes': 'sbb.' + module.split('/')[0]}

HEX = {
    'facility-service': {'in': ['REST API /facilities', 'Decision events listener', 'Covenant review job'],
                         'uc': ['Set up a facility', 'Amend a facility', 'Review a facility'],
                         'dom': ['Facility', 'FacilityVersion', 'Covenant', 'Money'],
                         'out': [('LimitBooking', 'limit-service · REST'), ('CollateralLink', 'collateral-service · REST'), ('LedgerBooking', 'Core banking ledger · IBM MQ'), ('EventPublisher', 'cc.events · Kafka outbox'), ('FacilityStore', 'PostgreSQL 16 · JPA')]},
    'credit-request-service': {'in': ['REST API /requests'], 'uc': ['Create a request', 'Submit a request'], 'dom': ['CreditRequest', 'RequestedStructure'],
                               'out': [('ClientReader', 'client-service · REST'), ('WorkflowStarter', 'decision-workflow · Camunda'), ('RequestStore', 'PostgreSQL 16 · JPA')]},
}

DDS = {
    # ---------------------------------------------------------------- facility-service: the seven hexagonal files
    'dd.cc-facility.domain': dd('dd.cc-facility.domain', 'facility-service · Domain', 'Domain', 'facility-service', [
        {'h': 'Where it sits', 'hex': 'facility-service', 'p': 'The domain is the center of the hexagon: plain Java, no framework import. Use cases call it; adapters never do.'},
        {'h': 'Responsibilities', 'b': ['Owns the Facility aggregate: amount, currency, maturity, pricing, covenants, versions.', 'Decides when a facility may become active: contract signed, limit booked, collateral covered.', 'Never reads the client: the approved decision carries the client id and rating.']},
        {'h': 'Aggregate', 'table': {'head': ['Type', 'Kind', 'Holds'], 'rows': [
            ['Facility', 'Aggregate root', 'id, clientId, status, currentVersion, covenants, collateralCoverage'],
            ['FacilityVersion', 'Entity', 'amount (Money), maturity, margin, signedAt · one per amendment'],
            ['Covenant', 'Entity', 'type (leverage, interest cover, rating floor), threshold, testedAt, breached'],
            ['Money', 'Value object', 'amount, currency · arithmetic and rounding in one place']]}},
        {'h': 'Facility lifecycle · state machine', 'sm': {
            'states': [('ap', 'Approved', 0, 0, 'start'), ('ct', 'Contracted', 1, 0, ''), ('ac', 'Active', 2, 0, ''), ('cl', 'Closed', 3, 0, 'end'), ('ca', 'Cancelled', 1, 1, 'end'), ('ur', 'Under review', 2, 1, '')],
            'trans': [('ap', 'ct', 'contract signed'), ('ap', 'ca', 'offer expired (90 days)'), ('ct', 'ac', 'limit booked, collateral ≥ 100 %'), ('ac', 'ur', 'yearly · covenant breach'),
                      ('ur', 'ac', 'review passed'), ('ac', 'cl', 'repaid'), ('ur', 'cl', 'terminated')]},
         'p': 'Transitions are methods on Facility; each one checks its invariant and raises a domain event. No other code changes status.'},
        {'h': 'Invariants', 'b': ['INV-FAC-01 · a facility is Active only if its limit is booked in limit-service.', 'INV-FAC-02 · a secured facility needs collateral covering at least 100 % of the amount.',
                                  'INV-FAC-03 · amount and maturity never change after Active: an amendment creates a new FacilityVersion.', 'INV-FAC-04 · a covenant breach moves an Active facility to Under review within one business day.']},
        {'h': 'Local decisions', 'rows': [['Amendments create versions', 'Keeps the audit trail required by EBA guidelines.', 'local'], ['Limit booked before activation', 'A facility can never be drawn without a limit.', 'ADR-CC-03']]},
    ], 'facility-service/architecture/dd/domain.md', '3e91c0a · 22 Oct', 'domain'),
    'dd.cc-facility.domain-events': dd('dd.cc-facility.domain-events', 'facility-service · Domain events', 'Domain events', 'facility-service', [
        {'h': 'Events raised by the aggregate', 'table': {'head': ['Event', 'Raised when', 'Payload', 'Consumers'], 'rows': [
            ['FacilityContracted', 'contract signed', 'facilityId, versionId, signedAt', 'document-service'],
            ['FacilityActivated', 'limit booked and collateral covered', 'facilityId, clientId, amount, currency, maturity', 'data lake, limit-service, reporting'],
            ['FacilityAmended', 'new version accepted', 'facilityId, versionId, changes', 'data lake, limit-service'],
            ['CovenantBreached', 'a covenant test fails', 'facilityId, covenantType, measured, threshold', 'Facility officer inbox, Credit risk']]}},
        {'h': 'From the domain to Kafka', 'chain': [['Aggregate', 'raises the event'], ['Outbox', 'same transaction as the state'], ['Relay', 'every 2 s'], ['cc.events', 'AsyncAPI 2.6, key facilityId']]},
        {'h': 'Rules', 'b': ['Events are facts in the past tense; consumers never call back to ask for the state.', 'Schemas are versioned in contracts/cc-events.asyncapi.yaml; a breaking change needs a new event name (ADR-CC-02).']},
    ], 'facility-service/architecture/dd/domain-events.md', '3e91c0a · 22 Oct', 'domain-events'),
    'dd.cc-facility.ports': dd('dd.cc-facility.ports', 'facility-service · Ports', 'Ports', 'facility-service', [
        {'h': 'The hexagon', 'hex': 'facility-service', 'p': 'Inbound ports are the use cases; outbound ports are interfaces the domain needs, implemented by adapters in infrastructure.'},
        {'h': 'Inbound ports (use cases)', 'table': {'head': ['Port', 'Called by', 'Returns'], 'rows': [['SetUpFacility', 'Decision events listener, REST', 'FacilityId'], ['AmendFacility', 'REST, facility officer screen', 'VersionId'], ['ReviewFacility', 'Covenant review job', 'ReviewOutcome']]}},
        {'h': 'Outbound ports', 'table': {'head': ['Port', 'Purpose', 'Adapter', 'Contract'], 'rows': [
            ['LimitBooking', 'book and release a limit', 'RestLimitBooking', 'limits.openapi.yaml'], ['CollateralLink', 'link and value collateral', 'RestCollateralLink', 'collateral.openapi.yaml'],
            ['LedgerBooking', 'book the facility in the ledger', 'LedgerMqBooking', 'ledger-booking.copybook'], ['EventPublisher', 'publish domain events', 'KafkaOutboxPublisher', 'cc-events.asyncapi.yaml'],
            ['FacilityStore', 'load and save the aggregate', 'JpaFacilityStore', 'db/changelog/facility']]}},
    ], 'facility-service/architecture/dd/ports.md', '3e91c0a · 22 Oct', 'ports'),
    'dd.cc-facility.application': dd('dd.cc-facility.application', 'facility-service · Application', 'Application', 'facility-service', [
        {'h': 'Use cases', 'table': {'head': ['Use case', 'Trigger', 'Transaction'], 'rows': [['Set up a facility', 'DecisionApproved event', 'one: aggregate + outbox'], ['Amend a facility', 'POST /facilities/{id}/amendments', 'one: new version + outbox'], ['Review a facility', 'yearly job, CovenantBreached', 'one per facility']]}},
        {'h': 'Main use case · Set up a facility', 'seq': [['decision-workflow', 'facility-service', 'DecisionApproved (Kafka)'], ['facility-service', 'limit-service', 'bookLimit(client, amount)'], ['facility-service', 'collateral-service', 'linkCollateral(facility)'], ['facility-service', 'Core banking ledger', 'book facility (MQ)'], ['facility-service', 'cc.events', 'FacilityActivated (outbox)']]},
        {'h': 'Failures', 'b': ['Limit refused: the facility stays Contracted and the officer is told; nothing is booked in the ledger.', 'Ledger unavailable: the booking is retried for 4 h, then the officer gets a task; the facility is not Active until booked.']},
    ], 'facility-service/architecture/dd/application.md', '3e91c0a · 22 Oct', 'application'),
    'dd.cc-facility.infrastructure': dd('dd.cc-facility.infrastructure', 'facility-service · Infrastructure', 'Infrastructure', 'facility-service', [
        {'h': 'Adapters', 'table': {'head': ['Adapter', 'Port', 'Technology'], 'rows': [['FacilityController', 'SetUpFacility, AmendFacility', 'Spring MVC, OpenAPI generated'], ['DecisionListener', 'SetUpFacility', 'Kafka consumer, topic cc.decisions'],
            ['CovenantReviewJob', 'ReviewFacility', 'Spring scheduler, ShedLock'], ['RestLimitBooking', 'LimitBooking', 'REST, idempotency key = facilityId'], ['LedgerMqBooking', 'LedgerBooking', 'IBM MQ, request/reply'],
            ['KafkaOutboxPublisher', 'EventPublisher', 'outbox table + relay'], ['JpaFacilityStore', 'FacilityStore', 'PostgreSQL 16, Liquibase']]}},
        {'h': 'Runtime', 'b': ['Namespace cc-facility on OpenShift, 3 replicas, HPA on CPU.', 'Secrets from Vault; no credential in the image.', 'Spring Modulith checks that no adapter is imported by the domain (ArchUnit in CI).']},
    ], 'facility-service/architecture/dd/infrastructure.md', '3e91c0a · 22 Oct', 'infrastructure'),
    'dd.cc-facility.api': dd('dd.cc-facility.api', 'facility-service · API', 'API', 'facility-service', [
        {'h': 'Operations', 'api': [['POST', '/facilities', 'setUpFacility', '201 · 409 duplicate decision'], ['GET', '/facilities/{id}', 'getFacility', '200 · 404'], ['GET', '/facilities?clientId=', 'listFacilities', '200 · exposure view'],
                                    ['POST', '/facilities/{id}/amendments', 'amendFacility', '201 · 422 invariant broken'], ['POST', '/facilities/{id}/reviews', 'startReview', '202']]},
        {'h': 'Request · setUpFacility', 'table': {'head': ['Field', 'Type', 'Rule'], 'rows': [['decisionId', 'uuid', 'required, unique'], ['clientId', 'string', 'from the decision'], ['amount', 'Money', '> 0'], ['maturity', 'date', 'after today'], ['collateral[]', 'CollateralRef', 'required when secured']]}},
        {'h': 'Errors', 'b': ['Problem+JSON (RFC 9457) with a code per invariant: FAC-01 limit not booked, FAC-02 collateral below 100 %, FAC-03 amendment after Active.', 'Contract: facility-service/contracts/facilities.openapi.yaml, checked on every build.']},
    ], 'facility-service/architecture/dd/api.md', '3e91c0a · 22 Oct', 'api'),
    'dd.cc-facility.data-model': dd('dd.cc-facility.data-model', 'facility-service · Data model', 'Data model', 'facility-service', [
        {'h': 'Tables', 'er': {'entities': [
            ('facility_version', [('id', 'uuid', 'PK'), ('facility_id', 'uuid', 'FK'), ('amount', 'numeric(18,2)', ''), ('currency', 'char(3)', ''), ('maturity', 'date', ''), ('signed_at', 'timestamptz', '')]),
            ('facility', [('id', 'uuid', 'PK'), ('client_id', 'varchar(20)', ''), ('status', 'varchar(16)', ''), ('current_version', 'uuid', 'FK'), ('coverage_pct', 'numeric(5,2)', ''), ('updated_at', 'timestamptz', '')]),
            ('covenant', [('id', 'uuid', 'PK'), ('facility_id', 'uuid', 'FK'), ('type', 'varchar(24)', ''), ('threshold', 'numeric', ''), ('breached', 'boolean', '')]),
            ('outbox', [('id', 'bigserial', 'PK'), ('aggregate_id', 'uuid', ''), ('type', 'varchar(48)', ''), ('payload', 'jsonb', ''), ('sent_at', 'timestamptz', '')])],
            'rels': [(0, 1, 'n', '1', 'versions'), (1, 2, '1', 'n', 'covenants')]}},
        {'h': 'Constraints', 'b': ['check status in (APPROVED, CONTRACTED, ACTIVE, UNDER_REVIEW, CLOSED, CANCELLED)', 'check coverage_pct >= 100 when status = ACTIVE and secured (INV-FAC-02)', 'unique (facility_id, signed_at) on facility_version', 'index outbox (sent_at) where sent_at is null'],
         'p': 'Liquibase changelog db/changelog/facility/0001-facility.yaml. The schema is private to facility-service: other services use the API or events.'},
    ], 'facility-service/architecture/dd/data-model.md', '3e91c0a · 22 Oct', 'data-model'),
    # ---------------------------------------------------------------- credit-request-service
    'dd.cc-request.domain': dd('dd.cc-request.domain', 'credit-request-service · Domain', 'Domain', 'credit-request-service', [
        {'h': 'Where it sits', 'hex': 'credit-request-service', 'p': 'The request is owned here until the decision starts; the workflow owns the decision.'},
        {'h': 'Responsibilities', 'b': ['Owns the credit request: client, amount, purpose, requested structure.', 'Checks completeness before the decision starts.']},
        {'h': 'Request lifecycle · state machine', 'sm': {
            'states': [('dr', 'Draft', 0, 0, 'start'), ('sb', 'Submitted', 1, 0, ''), ('id', 'In decision', 2, 0, ''), ('ap', 'Approved', 3, 0, 'end'), ('wd', 'Withdrawn', 1, 1, 'end'), ('dc', 'Declined', 3, 1, 'end')],
            'trans': [('dr', 'sb', 'complete'), ('dr', 'wd', 'withdrawn'), ('sb', 'id', 'workflow started'), ('id', 'ap', 'approved'), ('id', 'dc', 'declined'), ('sb', 'wd', 'withdrawn')]}},
        {'h': 'Ports', 'table': {'head': ['Port', 'Direction', 'Adapter'], 'rows': [['CreateRequest, SubmitRequest', 'inbound', 'REST /requests'], ['ClientReader', 'outbound', 'client-service REST'], ['WorkflowStarter', 'outbound', 'Camunda start message'], ['RequestStore', 'outbound', 'JPA, PostgreSQL 16']]}},
    ], 'credit-request-service/architecture/dd/domain.md', 'b12f7d3 · 18 Oct', 'domain'),
    'dd.cc-request.api': dd('dd.cc-request.api', 'credit-request-service · API', 'API', 'credit-request-service', [
        {'h': 'Operations', 'api': [['POST', '/requests', 'createRequest', '201'], ['PUT', '/requests/{id}', 'updateRequest', '200 · 409 not a draft'], ['POST', '/requests/{id}/submit', 'submitRequest', '202 · 422 incomplete'], ['GET', '/requests/{id}', 'getRequest', '200']]},
        {'h': 'Contract', 'p': 'credit-request-service/contracts/requests.openapi.yaml · served through the API gateway with the advisor’s token.'},
    ], 'credit-request-service/architecture/dd/api.md', 'b12f7d3 · 18 Oct', 'api'),
    'dd.cc-request.data-model': dd('dd.cc-request.data-model', 'credit-request-service · Data model', 'Data model', 'credit-request-service', [
        {'h': 'Tables', 'er': {'entities': [
            ('credit_request', [('id', 'uuid', 'PK'), ('client_id', 'varchar(20)', ''), ('status', 'varchar(16)', ''), ('purpose', 'varchar(64)', ''), ('submitted_at', 'timestamptz', '')]),
            ('requested_tranche', [('id', 'uuid', 'PK'), ('request_id', 'uuid', 'FK'), ('amount', 'numeric(18,2)', ''), ('currency', 'char(3)', ''), ('tenor_months', 'int', '')])],
            'rels': [(0, 1, '1', 'n', 'tranches')]}},
        {'h': 'Constraints', 'b': ['check status in (DRAFT, SUBMITTED, IN_DECISION, APPROVED, DECLINED, WITHDRAWN)', 'no client data stored beyond client_id (ADR-CC-04)']},
    ], 'credit-request-service/architecture/dd/data-model.md', 'b12f7d3 · 18 Oct', 'data-model'),
    # ---------------------------------------------------------------- limit-service
    'dd.cc-limit.domain': dd('dd.cc-limit.domain', 'limit-service · Domain', 'Domain', 'limit-service', [
        {'h': 'Responsibilities', 'b': ['Holds limits per client and per group.', 'Answers a limit check in under 200 ms, before the decision.']},
        {'h': 'Limit check', 'chain': [['Request', 'client, group, amount'], ['Group exposure', 'all facilities'], ['Answer', 'within or above limit']]},
    ], 'limit-service/architecture/dd/domain.md', '7a0c2e1 · 20 Oct', 'domain'),
    'dd.cc-limit.api': dd('dd.cc-limit.api', 'limit-service · API', 'API', 'limit-service', [
        {'h': 'Operations', 'api': [['POST', '/limit-checks', 'checkLimit', '200 · p95 < 200 ms'], ['POST', '/limits/{client}/bookings', 'bookLimit', '201 · idempotent'], ['DELETE', '/limits/{client}/bookings/{id}', 'releaseLimit', '204']]},
        {'h': 'Events', 'table': {'head': ['Channel', 'Message', 'Status'], 'rows': [['cc.limits', 'LimitBooked, LimitReleased', 'missing in limits.asyncapi.yaml · ARB check O2'], ['cc.events', 'consumes FacilityActivated', 'documented']]}},
    ], 'limit-service/architecture/dd/api.md', '7a0c2e1 · 20 Oct', 'api'),
}

SERVICES = [  # Design tab
    ('credit-request-service', 'Request team', 'sbb.credit-request-service'),
    ('decision-workflow', 'Request team', 'sbb.decision-workflow'),
    ('client-service', 'Client team', 'sbb.client-service'),
    ('rating-service', 'Client team', 'sbb.rating-service'),
    ('facility-service', 'Facility team', 'sbb.facility-service.facility-service'),
    ('limit-service', 'Facility team', 'sbb.credit-request-service.credit-request-service'),
    ('collateral-service', 'Facility team', 'sbb.collateral-service'),
    ('document-service', 'Platform team', 'sbb.document-service'),
]

# ------------------------------------------------------------------------------------------------------------------
# Architecture decisions (MADR)
# ------------------------------------------------------------------------------------------------------------------
ADRS = [
    {'id': 'ADR-CC-01', 't': 'Split the credit origination monolith by business capability', 'status': 'Accepted', 'date': '3 Jun 2026', 'by': 'Corporate credit architects', 'ref': 'DEC-07', 'plateau': 'Transition 1',
     'context': 'One release a month for the whole monolith; three teams wait on each other; decisions take 15 days.',
     'decision': 'Split by capability: request, client, rating, facility, limits, collateral, documents. Strangle the monolith behind an API gateway.',
     'options': ['Keep the monolith and modularise it inside', 'Split by technical layer', 'Split by capability (chosen)'],
     'consequences': ['Each team releases on its own.', 'Data is owned by one service; others read it through its API or events.', 'A transition plateau runs both the new services and the monolith.'],
     'els': ['req', 'cli', 'gw', 'mono']},
    {'id': 'ADR-CC-02', 't': 'Events on Kafka replace the nightly facility exports', 'status': 'Accepted', 'date': '12 Sep 2026', 'by': 'Facility team, Data team', 'ref': 'DEC-KB-02', 'plateau': 'Target',
     'context': 'The data lake sees facilities a day late; the export fails about twice a month and nobody owns it.',
     'decision': 'facility-service publishes FacilityActivated and FacilityAmended on cc.events with an outbox; the data lake streams the topic.',
     'options': ['Keep the batch, add monitoring', 'Change data capture on Oracle', 'Business events with an outbox (chosen)'],
     'consequences': ['Exposure is visible within a minute.', 'The nightly exports are retired with the monolith.', 'Event contracts are versioned in AsyncAPI.'],
     'els': ['kafka', 'fac', 'exp', 'lake']},
    {'id': 'ADR-CC-03', 't': 'Check limits synchronously before the decision', 'status': 'Accepted', 'date': '30 Sep 2026', 'by': 'Facility team, Credit risk', 'ref': 'req.corporate-credit.limit-check', 'plateau': 'Target',
     'context': 'Limits are checked after the decision today; some approved credits exceed the group limit.',
     'decision': 'decision-workflow calls limit-service before the committee; facility-service books the limit before activation.',
     'options': ['Check after the decision', 'Check asynchronously and alert', 'Check synchronously before the decision (chosen)'],
     'consequences': ['limit-service must answer in under 200 ms.', 'A limit-service outage pauses decisions, not requests.'],
     'els': ['wf', 'lim', 'fac']},
    {'id': 'ADR-CC-04', 't': 'Read the client from client-service, never copy it', 'status': 'Accepted', 'date': '10 Jun 2026', 'by': 'Client team', 'ref': 'mot.ent.read-never-copy', 'plateau': 'Transition 1',
     'context': 'Three copies of client data drift apart; KYC status is often stale in credit files.',
     'decision': 'Services keep only the client id and read the client from client-service, which reads the group referential.',
     'options': ['Replicate the referential nightly', 'Read through client-service (chosen)'],
     'consequences': ['One place to change client data.', 'client-service needs 99.9 % availability.'],
     'els': ['cli', 'req', 'cref']},
    {'id': 'ADR-CC-05', 't': 'Value collateral through an external provider', 'status': 'Proposed', 'date': '24 Oct 2026', 'by': 'Facility team', 'ref': '—', 'plateau': 'Target',
     'context': 'Collateral is revalued by hand once a year; real-estate values move faster.',
     'decision': 'collateral-service calls a valuation provider for real estate quarterly; other collateral stays manual.',
     'options': ['Manual valuation', 'External provider for real estate (proposed)'],
     'consequences': ['A new external dependency to contract and secure.', 'The detailed design of collateral-service must cover it.'],
     'els': ['col']},
    {'id': 'ADR-CC-06', 't': 'Keep Oracle for facilities until the target', 'status': 'Superseded', 'date': '15 Mar 2026', 'by': 'Facility team', 'ref': '—', 'plateau': 'Transition 1',
     'context': 'Moving facilities out of Oracle during transition 1 was too risky.',
     'decision': 'Facilities stay in Facility core until facility-service exists. Superseded by ADR-CC-02 for the exports.',
     'options': ['Migrate in transition 1', 'Keep until target (chosen)'],
     'consequences': ['The monolith keeps facilities in transition 1.'],
     'els': ['fcore', 'mono']},
]

# ------------------------------------------------------------------------------------------------------------------
# Plateaus, work packages, ARB submissions, ASD
# ------------------------------------------------------------------------------------------------------------------
PLATEAUS = [
    {'k': 'base', 'name': 'Baseline', 'when': 'today', 'state': 'Live', 'tile': 'ok', 'desc': 'The Credit origination monolith on WebLogic and Oracle, nightly exports to the data lake.'},
    {'k': 'tr1', 'name': 'Transition 1', 'when': 'Dec 2026', 'state': 'In progress', 'tile': 'in', 'desc': 'API gateway, credit-request-service, client-service and decision-workflow in front of the monolith.'},
    {'k': 'target', 'name': 'Target', 'when': 'Jun 2027', 'state': 'Planned', 'tile': 'ne', 'desc': 'All capabilities in services on OpenShift, events on Kafka, the monolith and Oracle retired.'},
]
WPS = {
    'wp1': {'name': 'Extract client and request', 'from': 'base', 'to': 'tr1', 'team': 'Request and Client teams', 'when': 'Jul – Dec 2026', 'state': 'In progress'},
    'wp2': {'name': 'Extract facility, limits, collateral', 'from': 'tr1', 'to': 'target', 'team': 'Facility team', 'when': 'Jan – Apr 2027', 'state': 'Planned'},
    'wp3': {'name': 'Events replace nightly exports', 'from': 'tr1', 'to': 'target', 'team': 'Facility and Data teams', 'when': 'Feb – Mar 2027', 'state': 'Planned'},
    'wp4': {'name': 'Retire Credit origination', 'from': 'tr1', 'to': 'target', 'team': 'Request team', 'when': 'May – Jun 2027', 'state': 'Planned'},
}
REQS = {
    'req.corporate-credit.decision-time': ('Decision in 5 working days', 'From a complete file to the committee decision in ≤ 5 working days for 90 % of requests', 'decision-workflow, rating-service'),
    'req.corporate-credit.limit-check': ('Limit check before the decision', 'Group limit checked before the committee; answer in < 200 ms p95; no decision without a check', 'limit-service'),
    'req.corporate-credit.four-eyes': ('Four-eyes above 5 M EUR', 'A second approver for any facility above 5 M EUR; the approver differs from the analyst', 'decision-workflow'),
    'req.corporate-credit.audit': ('Every decision traceable', 'Every decision, amendment and booking is kept 10 years with who, when and why', 'facility-service, cc.events'),
}

ARBS = [
    {'id': 'arb.facility.2026-14', 't': 'Extract facility, limits and collateral', 'from': 'tr1', 'to': 'target', 'board': '6 Nov', 'by': 'Lucas Bernard', 'status': 'In review',
     'submitted': '21 Oct', 'workItem': 'WI-CC-412', 'reqs': list(REQS.keys()), 'adrs': ['ADR-CC-02', 'ADR-CC-03', 'ADR-CC-05'],
     'checks': [
         ['S', 'S1 · frontmatter matches the schema', 'pass', '', False], ['S', 'S2 · every reference resolves', 'pass', '', False], ['S', 'S3 · DD files realize SBBs only', 'pass', '', False],
         ['T', 'T1 · new ABB realizes a requirement', 'pass', '', False], ['T', 'T4 · every requirement is realized in the target', 'pass', '4 of 4', False],
         ['T', 'T6 · collateral-service has no detailed design', 'warn', 'Draft it from the code, or write it before the board', False],
         ['P', 'P1–P2 · every block in a plateau, change tags agree', 'pass', '', False], ['P', 'P3 · every gap item has a work package', 'pass', '10 of 10', False],
         ['O', 'O1 · owner on new and changed blocks', 'pass', '', False],
         ['O', 'O2 · contract missing for the limit events channel', 'fail', 'limit-service/contracts/limits.asyncapi.yaml has no channel cc.limits', True],
         ['D', 'D1 · referenced ADRs exist', 'pass', '', False], ['D', 'D2 · new component collateral-service needs an accepted ADR', 'warn', 'ADR-CC-05 is still proposed', False],
     ],
     'reviewers': [['Enterprise architecture', 'Emma Laurent', 'Pending', ''],
                   ['Security', 'Hugo Martin', 'Request changes', 'Show how the MQ channel to the ledger is authenticated, and who may replay a booking.'],
                   ['Credit risk', 'your manager', 'Approve with conditions', 'Accept once the limit check is proven under 200 ms in the performance test.'],
                   ['Data protection', 'Thomas Girard', 'Not required', 'No personal data beyond client ids already held by the bank.']],
     'conditions': [['C1', 'Prove the limit check under 200 ms p95 in the performance test', 'Facility team', '20 Nov', 'Open'],
                    ['C2', 'Document the MQ channel authentication and the replay procedure for ledger bookings', 'Facility team, Security', '4 Nov', 'Open']],
     'board': '6 Nov',
     'asks': [['Accept an external valuation provider for real-estate collateral', 'ADR-CC-05 · proposed'], ['Accept the MQ booking risk during the cut-over, or fund a ledger API', 'Risk R2'],
              ['Retire the nightly exports when facility-service goes live, not after', 'ADR-CC-02 · consequence']],
     'asd': {
         'context': {'p': 'Second step of the corporate credit modernisation. Facilities, limits and collateral leave the Credit origination monolith; the nightly exports to the data lake are replaced by events. Transition 1 (live in December) already runs request, client and the decision workflow in front of the monolith.',
                     'b': ['In scope: facility-service, limit-service, collateral-service, rating-service, document-service; the cc.events topic; the MQ booking to the core banking ledger.', 'Out of scope: drawdowns and repayments (core banking), the advisor portal redesign, collateral valuation of non-real-estate assets.']},
         'need': {'p': 'Credit decisions take 15 working days and group limits are checked after the decision; some approved credits exceed the group limit. Exposure reaches the data lake a day late.',
                  'table': {'head': ['Measure', 'Today', 'Target', 'Source'], 'rows': [['Decision time (90th percentile)', '15 days', '5 days', 'Credit risk dashboard, Q2'], ['Approvals above the group limit', '3 % of approvals', '0', 'Internal audit 2026-04'], ['Exposure visible in the data lake', 'next morning', '< 1 minute', 'Data team'], ['Failed nightly exports', '2 per month', '0 (retired)', 'Incident log']]}},
         'overview': {'p': 'facility-service, limit-service and collateral-service run on OpenShift; decision-workflow (Camunda) orchestrates the decision; facility-service publishes its events on cc.events through an outbox; the data lake streams the topic. Each service owns its data in its own PostgreSQL schema.',
                      'b': ['Hexagonal services (Spring Modulith): use cases in the application layer, the domain free of frameworks, adapters behind ports.', 'Synchronous calls only for the limit check and the booking; everything else is an event.', 'The ledger booking stays on IBM MQ (no ledger API before 2028).']},
         'nfr': '',
         'security': {'p': 'Secrets in Vault; service-to-service mTLS inside the cluster; client data read from client-service only (ADR-CC-04).',
                      'table': {'head': ['Threat', 'Control', 'Status'], 'rows': [['Forged booking on the MQ channel', 'Channel authentication with TLS and a dedicated MQ user per service', 'To document · condition C2'], ['Replay of a booking', 'Idempotency key = facilityId + versionId, checked by the ledger adapter', 'Designed'], ['Over-privileged service accounts', 'One Vault role per service, 24 h leases', 'Designed'], ['Tampering with decisions', 'Decisions immutable; every change is a new version with its author', 'Designed']]}},
         'risks': {'table': {'head': ['Risk', 'Impact', 'Likelihood', 'Mitigation', 'Owner'], 'rows': [['R1 · limit-service slower than 200 ms under load', 'Decisions paused', 'Medium', 'Performance test before go-live (C1), cache of group exposure', 'Facility team'], ['R2 · MQ booking fails during the cut-over', 'Facilities not booked', 'Medium', 'Dual run for 2 weeks, reconciliation report each night', 'Core banking'], ['R3 · valuation provider not contracted in time', 'Manual valuation stays', 'High', 'Keep manual valuation as fallback; ADR-CC-05 decides', 'Procurement'], ['R4 · data lake consumers depend on the export format', 'Reports break', 'Low', 'Publish a compatibility view for 3 months', 'Data team']]}},
     },
     'nfrRich': {'table': {'head': ['Requirement', 'Target', 'Evidence'], 'rows': [['Limit check latency', 'p95 < 200 ms', 'performance test on limit-service, 50 req/s'], ['Facility set-up', '< 2 s end to end', 'trace from DecisionApproved to FacilityActivated'], ['Availability', '99.9 % for limit-service and facility-service', 'SLO dashboards, same as decision-workflow'], ['Recovery point', '5 minutes', 'PostgreSQL WAL shipping, restore drill each quarter'], ['Volume', '1,200 facilities / month, 40 / hour at peak', 'Q2 volumes × 2']]}}},
    {'id': 'arb.request.2026-09', 't': 'Client and request services in front of the monolith', 'from': 'base', 'to': 'tr1', 'board': '24 Jul', 'by': 'Karim Ouali', 'status': 'Approved with conditions',
     'checks': [['S', 'S1–S3 · Structure', 'pass', '', False], ['T', 'T1–T6 · traceability', 'pass', '', False], ['P', 'P1–P4 · plateaus and gaps', 'pass', '', False], ['O', 'O1–O3 · ownership and contracts', 'pass', '', False], ['D', 'D1–D3 · decisions', 'pass', '', False]],
     'reviewers': [['Enterprise architecture', 'Emma Laurent', 'Approved', ''], ['Security', 'Hugo Martin', 'Approve with conditions', 'Pen test of the API gateway before go-live.'], ['Credit risk', 'your manager', 'Approved', '']],
     'conditions': [['C1', 'Pen test of the API gateway before go-live', 'Platform team', '14 Oct', 'Done']], 'asd': None, 'decided': 'Recorded in Git · 5d2a9f1 · 24 Jul'},
    {'id': 'arb.client.2026-11', 't': 'rating-service replaces the rating engine', 'from': 'tr1', 'to': 'target', 'board': '20 Nov', 'by': 'Marta Kowalski', 'status': 'Draft',
     'checks': [['S', 'S1–S3 · Structure', 'pass', '', False], ['T', 'T6 · rating-service has no detailed design', 'warn', '', False]],
     'reviewers': [], 'conditions': [], 'asd': None},
]
ASD_SECTIONS = [  # 13 sections: w = written in the submission, m = assembled from the model
    ('Context and scope', 'w', 'context'), ('Business need', 'w', 'need'), ('Architecture overview', 'w', 'overview'),
    ('Requirements', 'm', 'requirements'), ('Baseline', 'm', 'baseline'), ('Target', 'm', 'target'), ('Gap and transition', 'm', 'gap'),
    ('Detailed design', 'm', 'dd'), ('Non-functional requirements', 'w', 'nfr'), ('Security', 'w', 'security'), ('Decisions', 'm', 'decisions'),
    ('Risks', 'w', 'risks'), ('Open questions', 'm', 'questions'),
]

# ------------------------------------------------------------------------------------------------------------------
# Changes: what the architecture process carries, one per work package
# ------------------------------------------------------------------------------------------------------------------
CHANGES = [
    {'k': 'wp1', 'adrs': ['ADR-CC-01', 'ADR-CC-04'], 'arbs': ['arb.request.2026-09'], 'why': 'Release request and client on their own, in front of the monolith.'},
    {'k': 'wp2', 'adrs': ['ADR-CC-03', 'ADR-CC-05'], 'arbs': ['arb.facility.2026-14', 'arb.client.2026-11'], 'why': 'Facilities, limits, collateral and rating leave the monolith.'},
    {'k': 'wp3', 'adrs': ['ADR-CC-02'], 'arbs': ['arb.facility.2026-14'], 'why': 'Exposure visible within a minute instead of the next morning.'},
    {'k': 'wp4', 'adrs': ['ADR-CC-01', 'ADR-CC-06'], 'arbs': [], 'why': 'Switch off the monolith, WebLogic and Oracle.'},
]

# ------------------------------------------------------------------------------------------------------------------
# Geometry, routing and rendering of a view
# ------------------------------------------------------------------------------------------------------------------
LEFT = 40

def modes_of(v):
    out = []
    for m in v['modes']:
        if m == 'gap':
            out += [g for g in GAPS if all(p in v['modes'] for p in GAPS[g])]
        else:
            out.append(m)
    return out

def mode_name(m):
    if m in GAPS:
        a, b = GAPS[m]
        return f'Gap · {PL_NAME[a]} → {PL_NAME[b]}'
    return PL_NAME[m]

def view_id(k, m):
    if m in GAPS:
        a, b = GAPS[m]
        return f'{k}_gap_{PL_ID[a]}_{PL_ID[b]}'
    return f'{k}_{PL_ID[m]}' if len(VIEWS[k]['modes']) > 1 else k

def pos(v, n):
    return LEFT + n['c'] * v['cw'], v['top'] + n['r'] * v['rh']

def size(v):
    cols = max(n['c'] for n in v['nodes']) + 1
    rows = max(n['r'] for n in v['nodes']) + 1
    return LEFT * 2 + (cols - 1) * v['cw'] + FW, v['top'] + (rows - 1) * v['rh'] + FH + (56 if v['groups'] else 48)

def state_of(n, m):
    """visible?, gap status (new / changed / retired / unchanged / None)."""
    if m in GAPS:
        a, b = GAPS[m]
        ia, ib = a in n['pl'], b in n['pl']
        if not (ia or ib):
            return False, None
        if ia and ib:
            return True, 'changed' if m in n.get('chg', []) else 'unchanged'
        return True, 'new' if ib else 'retired'
    return m in n['pl'], None

def edge_state(pl, m):
    if m in GAPS:
        a, b = GAPS[m]
        ia, ib = a in pl, b in pl
        if not (ia or ib):
            return False, None
        return True, 'unchanged' if ia and ib else ('new' if ib else 'retired')
    return m in pl, None

def _seg_hits(x1, y1, x2, y2, r, pad=8):
    rx, ry, rw, rh = r[0] - pad, r[1] - pad, r[2] + 2 * pad, r[3] + 2 * pad
    if abs(x1 - x2) < .01:  # vertical
        return rx < x1 < rx + rw and max(min(y1, y2), ry) < min(max(y1, y2), ry + rh)
    if abs(y1 - y2) < .01:  # horizontal
        return ry < y1 < ry + rh and max(min(x1, x2), rx) < min(max(x1, x2), rx + rw)
    # diagonal: sample
    for i in range(1, 60):
        t = i / 60; x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        if rx < x < rx + rw and ry < y < ry + rh:
            return True
    return False

def _clip(ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    tx = (FW / 2 + 3) / abs(dx) if dx else 1e9
    ty = (FH / 2 + 3) / abs(dy) if dy else 1e9
    t = min(tx, ty)
    return ax + dx * t, ay + dy * t

def route(v, A, B, rects, used=None):
    """Straight line when it is clear, otherwise the shortest orthogonal route through the gaps between figures."""
    ax, ay = pos(v, A); bx, by = pos(v, B)
    sx, sy, tx, ty = ax + FW / 2, ay + FH / 2, bx + FW / 2, by + FH / 2
    others = [r for k, r in rects.items() if k not in (A['k'], B['k'])]
    def clear(pts):
        return all(not _seg_hits(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], r) for i in range(len(pts) - 1) for r in others)
    def side(cx, cy, dx, dy):  # boundary point leaving the figure center towards (dx, dy)
        if abs(dx) >= abs(dy):
            return (cx + (FW / 2 + 3) * (1 if dx > 0 else -1), cy)
        return (cx, cy + (FH / 2 + 3) * (1 if dy > 0 else -1))
    cands = []
    p1, p2 = _clip(sx, sy, tx, ty), _clip(tx, ty, sx, sy)
    cands.append((0, [p1, p2]))
    gx = sorted(set([x + o for x in [LEFT + c * v['cw'] - (v['cw'] - FW) / 2 for c in range(0, 9)] for o in (0, -14, 14) if x + o > 6] + [LEFT - 22]))
    gy = sorted(set([y + o for y in [v['top'] + r * v['rh'] - (v['rh'] - FH) / 2 for r in range(0, 8)] for o in (0, -12, 12)] + [v['top'] + 6 * v['rh']]))
    # one bend
    if abs(tx - sx) > 1 and abs(ty - sy) > 1:
        cands.append((1, [side(sx, sy, tx - sx, 0), (tx, sy), side(tx, ty, 0, sy - ty)]))
        cands.append((1, [side(sx, sy, 0, ty - sy), (sx, ty), side(tx, ty, sx - tx, 0)]))
    # two bends through a vertical gap or a horizontal gap
    for x in gx:
        a = side(sx, sy, x - sx, 0); b = side(tx, ty, x - tx, 0)
        if (x - sx) * (a[0] - sx) > 0 and (x - tx) * (b[0] - tx) > 0:
            cands.append((2, [a, (x, sy), (x, ty), b]))
    for y in gy:
        a = side(sx, sy, 0, y - sy); b = side(tx, ty, 0, y - ty)
        if (y - sy) * (a[1] - sy) > 0 and (y - ty) * (b[1] - ty) > 0:
            cands.append((2, [a, (sx, y), (tx, y), b]))
    best = None
    for bends, pts in cands:
        if not clear(pts):
            continue
        L = sum(abs(pts[i + 1][0] - pts[i][0]) + abs(pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))
        cost = L + 120 * bends + 400 * _overlaps(pts, used or [])
        if best is None or cost < best[0]:
            best = (cost, pts)
    if best is None:  # three bends: out sideways, along a row gap, then into the target from above or below (and the mirror)
        for x in gx:
            for y in gy:
                a = side(sx, sy, x - sx, 0); b = side(tx, ty, 0, y - ty)
                if (x - sx) * (a[0] - sx) > 0 and (y - ty) * (b[1] - ty) > 0:
                    pts = [a, (x, sy), (x, y), (tx, y), b]
                    if clear(pts):
                        L = sum(abs(pts[i + 1][0] - pts[i][0]) + abs(pts[i + 1][1] - pts[i][1]) for i in range(4)) + 360 + 400 * _overlaps(pts, used or [])
                        if best is None or L < best[0]: best = (L, pts)
                a = side(sx, sy, 0, y - sy); b = side(tx, ty, x - tx, 0)
                if (y - sy) * (a[1] - sy) > 0 and (x - tx) * (b[0] - tx) > 0:
                    pts = [a, (sx, y), (x, y), (x, ty), b]
                    if clear(pts):
                        L = sum(abs(pts[i + 1][0] - pts[i][0]) + abs(pts[i + 1][1] - pts[i][1]) for i in range(4)) + 360 + 400 * _overlaps(pts, used or [])
                        if best is None or L < best[0]: best = (L, pts)
    return (best[1] if best else [p1, p2]), best is not None

def _segs(pts):
    out = []
    for i in range(len(pts) - 1):
        (x1, y1), (x2, y2) = pts[i], pts[i + 1]
        if abs(y1 - y2) < 1: out.append(('h', round(y1), min(x1, x2), max(x1, x2)))
        elif abs(x1 - x2) < 1: out.append(('v', round(x1), min(y1, y2), max(y1, y2)))
    return out

def _overlaps(pts, used):
    n = 0
    for o, c, a, b in _segs(pts):
        for o2, c2, a2, b2 in used:
            if o == o2 and abs(c - c2) < 6 and min(b, b2) - max(a, a2) > 12:
                n += 1
    return n

def _label_pos(pts, w):
    segs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    a, b = max(segs, key=lambda s: abs(s[1][0] - s[0][0]) + abs(s[1][1] - s[0][1]))
    return (a[0] + b[0]) / 2, (a[1] + b[1]) / 2

def _marker(kind, x, y, ang):
    m = AX.MARK[kind][0]
    return f'<g transform="translate({x:.1f} {y:.1f}) rotate({ang:.1f})">{m}</g>' if m else ''

import math

def render(k, m, interactive=True, uid=''):
    """One LikeC4 view as design-system markup: groupings, relationship lines with ArchiMate markers, figures, change chips."""
    v = VIEWS[k]; W, H = size(v)
    nodes = {n['k']: n for n in v['nodes']}
    vis = {n['k']: state_of(n, m) for n in v['nodes']}
    rects = {kk: (pos(v, n)[0], pos(v, n)[1], FW, FH) for kk, n in nodes.items() if vis[kk][0]}
    out = [f'<div class="lc-diagram" style="width: {W}px; height: {H}px">']
    for g in v['groups']:
        label, c0, c1, r1 = g[:4]; r0 = g[4] if len(g) > 4 else 0
        x0 = LEFT + c0 * v['cw'] - 20; y0 = v['top'] + r0 * v['rh'] - 48
        w = (c1 - c0) * v['cw'] + FW + 40; h = (r1 - r0) * v['rh'] + FH + 68
        out.append(f'<div class="lc-group" style="left: {x0}px; top: {y0}px; width: {w}px; height: {h}px"><span>{AX.esc(label)}</span></div>')
    svg = [f'<svg class="lc-edges" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true">']
    labels, warn, used, placed = [], [], [], []
    for (s_, t_, rel, lab, pl) in v['edges']:
        ok, st = edge_state(pl, m)
        if not ok or not (vis[s_][0] and vis[t_][0]):
            continue
        pts, clean = route(v, nodes[s_], nodes[t_], rects, used)
        used += _segs(pts)
        if not clean:
            warn.append(f'{k}/{m}: {s_}->{t_} crosses a figure')
        R = AX.RELS[rel]
        hm, hl = AX.MARK[R['target']]; tm, tl = AX.MARK[R['source']]
        (x1, y1), (x2, y2) = pts[0], pts[1]
        a0 = math.degrees(math.atan2(y1 - y2, x1 - x2))           # tail points back to the source
        (u1, w1), (u2, w2) = pts[-2], pts[-1]
        a1 = math.degrees(math.atan2(w2 - w1, u2 - u1))
        # shorten the line under filled markers
        def back(p, q, d):
            L = math.hypot(q[0] - p[0], q[1] - p[1]) or 1
            return (q[0] - (q[0] - p[0]) * d / L, q[1] - (q[1] - p[1]) * d / L)
        lp = list(pts)
        if hl: lp[-1] = back(pts[-2], pts[-1], hl)
        if tl: lp[0] = back(pts[1], pts[0], tl)
        d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in lp)
        cls = f'edge e-{s_} e-{t_}' + (f' g-{st}' if st else '') + (' assoc' if rel == 'association' else '')
        svg.append(f'<g class="{cls}"><path class="ln" d="{d}"{AX.DASH[R["line"]]}/>{_marker(R["target"], u2, w2, a1)}{_marker(R["source"], x1, y1, a0)}</g>')
        if lab:
            lw = len(lab) * 6.6 + 12
            def over(lx, ly):
                return [kk for kk, r in rects.items() if kk not in (s_, t_) and lx - lw / 2 < r[0] + r[2] + 2 and lx + lw / 2 > r[0] - 2 and ly - 11 < r[1] + r[3] and ly + 11 > r[1]] + \
                       ['label' for (px, py, pw) in placed if abs(px - lx) < (pw + lw) / 2 + 4 and abs(py - ly) < 20]
            segs = sorted([(pts[i], pts[i + 1]) for i in range(len(pts) - 1)], key=lambda q: -(abs(q[1][0] - q[0][0]) + abs(q[1][1] - q[0][1])))
            spots = [((a[0] + b[0]) / 2 + (b[0] - a[0]) * f, (a[1] + b[1]) / 2 + (b[1] - a[1]) * f) for a, b in segs for f in (0, -.25, .25, -.38, .38)]
            spots += [(x + (16 if abs(a[0] - b[0]) < 1 else 0) * d, y + (16 if abs(a[1] - b[1]) < 1 else 0) * d) for (a, b) in segs[:1] for (x, y) in [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)] for d in (-1, 1)]
            lx, ly = next((p for p in spots if not over(*p)), spots[0])
            if over(lx, ly):
                warn.append(f'{k}/{m}: label "{lab}" over {over(lx, ly)}')
            placed.append((lx, ly, lw))
            labels.append(f'<span class="lc-lbl e-{s_} e-{t_}{" g-" + st if st else ""}" style="left: {lx:.0f}px; top: {ly:.0f}px">{AX.esc(lab)}</span>')
    svg.append('</svg>')
    out += svg + labels
    for n in v['nodes']:
        ok, st = vis[n['k']]
        if not ok:
            continue
        t = AX.TYPES[n['kind']]; x, y = pos(v, n)
        cls = f'ax-box ax-shape-{t["shape"]} ax-l-{t["layer"]} lc-n n-{n["k"]}' + (' ax-retired' if st == 'retired' else '') + (' lc-faded' if st == 'unchanged' else '')
        aria = f'{n["name"]}, {n["kind"].lower()}' + (f', {st}' if st and st != 'unchanged' else '')
        inner = f'<span class="ax-in">{AX.svg_glyph(n["kind"])}<span class="ax-name">{AX.esc(n["name"])}</span></span>'
        if interactive:
            out.append(f'<button type="button" class="{cls}" style="left: {x}px; top: {y}px" aria-label="{AX.esc(aria)}" aria-pressed="{{{{lcOn_{n["k"]}}}}}" onClick="{{{{lcPick_{n["k"]}}}}}">{inner}</button>')
        else:
            out.append(f'<div class="{cls}" style="left: {x}px; top: {y}px" role="img" aria-label="{AX.esc(aria)}">{inner.replace("<span class=\"ax-in\">", "<span class=\"ax-in\">", 1)}</div>')
        if interactive and (n.get('nav') or n.get('dd')):
            tgt = f'the view {VIEWS[n["nav"]]["title"]}' if n.get('nav') else 'its detailed design'
            out.append(f'<button type="button" class="lc-nav" style="left: {x + FW - 30}px; top: {y + FH - 30}px" aria-label="Open {AX.esc(tgt)}" title="Open {AX.esc(tgt)}" onClick="{{{{lcNav_{k}_{n["k"]}}}}}">'
                       '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 4h6v6M20 4l-8 8M10 6H6a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-4"/></svg></button>')
        if st and st != 'unchanged':
            c = AX.CHANGE[st]
            out.append(f'<span class="ax-change {st} lc-chip" style="left: {x + 8}px; top: {y + FH - 10}px"><b aria-hidden="true">{AX.esc(c["glyph"])}</b>{c["label"]}</span>')
    out.append('</div>')
    return ''.join(out), warn

def legend(k, m):
    """What this view uses: layers, relationships, change chips."""
    v = VIEWS[k]
    vis = [n for n in v['nodes'] if state_of(n, m)[0]]
    layers = []
    for n in vis:
        l = AX.TYPES[n['kind']]['layer']
        if l not in layers:
            layers.append(l)
    rels = []
    keys = {n['k'] for n in vis}
    for (s_, t_, rel, lab, pl) in v['edges']:
        if edge_state(pl, m)[0] and s_ in keys and t_ in keys and rel not in rels:
            rels.append(rel)
    out = ['<div class="lc-legend">']
    out += [f'<span class="lg-i"><span class="swatch ax-l-{l}"></span>{AX.LAYERS[l]["label"]}</span>' for l in layers]
    out += [f'<span class="lg-i">{AX.rel_sample(r)}{AX.RELS[r]["name"]}</span>' for r in rels]
    if m in GAPS:
        sts = {state_of(n, m)[1] for n in vis}
        out += [f'<span class="ax-change {c}"><b aria-hidden="true">{AX.esc(AX.CHANGE[c]["glyph"])}</b>{AX.CHANGE[c]["label"]}</span>' for c in ['new', 'changed', 'retired'] if c in sts]
        out.append('<span class="lg-i meta">Unchanged elements are faded</span>')
    out.append('</div>')
    return ''.join(out)

DIAGRAM_KEYS = [(k, m) for k in VIEW_ORDER for m in modes_of(VIEWS[k])]

# ------------------------------------------------------------------------------------------------------------------
# Detailed design pictures: state machines, data models, the hexagon of a service
# ------------------------------------------------------------------------------------------------------------------
def dd_key(dd_id, i):
    return 'g_' + dd_id.replace('.', '_').replace('-', '_') + '_' + str(i)

def render_sm(spec):
    global FW, FH
    _fw, _fh = FW, FH
    FW, FH = 128, 48
    try:
        return _render_sm(spec)
    finally:
        FW, FH = _fw, _fh

def _render_sm(spec):
    v = {'cw': 260, 'rh': 116, 'top': 24, 'nodes': [{'k': k, 'c': c, 'r': r} for (k, lab, c, r, kind) in spec['states']]}
    nodes = {n['k']: n for n in v['nodes']}
    rects = {n['k']: (pos(v, n)[0], pos(v, n)[1], FW, FH) for n in v['nodes']}
    W = LEFT * 2 + max(n['c'] for n in v['nodes']) * v['cw'] + FW; H = v['top'] + max(n['r'] for n in v['nodes']) * v['rh'] + FH + 24
    out = [f'<div class="dd-pic"><div class="lc-diagram" style="width: {W}px; height: {H}px"><svg class="lc-edges" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true">']
    labels, used, placed = [], [], []
    for (a, b, lab) in spec['trans']:
        pts, ok = route(v, nodes[a], nodes[b], rects, used); used += _segs(pts)
        (u1, w1), (u2, w2) = pts[-2], pts[-1]
        ang = math.degrees(math.atan2(w2 - w1, u2 - u1))
        L = math.hypot(u2 - u1, w2 - w1) or 1; e = (u2 - (u2 - u1) * 10 / L, w2 - (w2 - w1) * 10 / L)
        d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts[:-1] + [e])
        out.append(f'<g class="edge"><path class="ln" d="{d}"/>{_marker("arrow", u2, w2, ang)}</g>')
        segs = sorted([(pts[i], pts[i + 1]) for i in range(len(pts) - 1)], key=lambda q: -(abs(q[1][0] - q[0][0]) + abs(q[1][1] - q[0][1])))
        lw = len(lab) * 6.6 + 12
        spots = [((p[0] + q[0]) / 2 + (q[0] - p[0]) * f, (p[1] + q[1]) / 2 + (q[1] - p[1]) * f) for p, q in segs for f in (0, -.25, .25)]
        def bad(x, y):
            return any(x - lw / 2 < r[0] + r[2] and x + lw / 2 > r[0] and y - 11 < r[1] + r[3] and y + 11 > r[1] for r in rects.values()) or any(abs(px - x) < (pw + lw) / 2 + 4 and abs(py - y) < 20 for px, py, pw in placed)
        lx, ly = next((q for q in spots if not bad(*q)), spots[0]); placed.append((lx, ly, lw))
        labels.append(f'<span class="lc-lbl" style="left: {lx:.0f}px; top: {ly:.0f}px">{AX.esc(lab)}</span>')
    out.append('</svg>'); out += labels
    for (k, lab, c, r, kind) in spec['states']:
        x, y = pos(v, nodes[k])
        out.append(f'<div class="sm-st {kind}" style="left: {x}px; top: {y}px; width: {FW}px; height: {FH}px" role="img" aria-label="State {AX.esc(lab)}{", initial" if kind == "start" else ", final" if kind == "end" else ""}">'
                   f'{"<i class=sm-init></i>" if kind == "start" else ""}<span>{AX.esc(lab)}</span></div>')
    out.append('</div></div>')
    return ''.join(out)

def render_er(spec):
    ents = spec['entities']; EW, GAP = 196, 44
    hs = [36 + 24 * len(cols) for (_, cols) in ents]
    W = 24 * 2 + len(ents) * EW + (len(ents) - 1) * GAP; H = max(hs) + 48
    out = [f'<div class="dd-pic"><div class="lc-diagram" style="width: {W}px; height: {H}px"><svg class="lc-edges" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true">']
    lbl = []
    for (a, b, ca, cb, lab) in spec['rels']:
        x1 = 24 + a * (EW + GAP) + EW; x2 = 24 + b * (EW + GAP); y = 24 + 18
        if a > b:
            x1, x2 = 24 + a * (EW + GAP), 24 + b * (EW + GAP) + EW
        out.append(f'<g class="edge"><path class="ln" d="M{x1} {y} L{x2} {y}"/></g>')
        out.append(f'<text x="{x1 + (6 if x2 > x1 else -14)}" y="{y - 6}" class="er-c">{ca}</text><text x="{x2 + (-14 if x2 > x1 else 6)}" y="{y - 6}" class="er-c">{cb}</text>')
        lbl.append(f'<span class="lc-lbl" style="left: {(x1 + x2) / 2:.0f}px; top: {y + 18}px">{AX.esc(lab)}</span>')
    out.append('</svg>'); out += lbl
    for i, (name, cols) in enumerate(ents):
        x = 24 + i * (EW + GAP)
        rows = ''.join(f'<li><span class="er-k">{AX.esc(k)}</span><span class="er-n">{AX.esc(c)}</span><span class="er-t">{AX.esc(t)}</span></li>' for (c, t, k) in cols)
        out.append(f'<div class="er-ent" style="left: {x}px; top: 24px; width: {EW}px" role="img" aria-label="Table {AX.esc(name)}"><b>{AX.esc(name)}</b><ul>{rows}</ul></div>')
    out.append('</div></div>')
    return ''.join(out)

def render_hex(svc):
    h = HEX[svc]; W, H = 860, 380; cx, cy = 400, 190
    def hexpts(r):
        return ' '.join(f'{cx + r * math.cos(math.radians(a)):.1f},{cy + r * 0.82 * math.sin(math.radians(a)):.1f}' for a in range(0, 360, 60))
    out = [f'<div class="dd-pic"><div class="lc-diagram" style="width: {W}px; height: {H}px"><svg class="lc-edges" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true">',
           f'<polygon points="{hexpts(170)}" fill="var(--ax-application-fill)" stroke="var(--ax-application-ink)" stroke-width="1.5"/>',
           f'<polygon points="{hexpts(92)}" fill="#FFFFFF" stroke="var(--ax-application-ink)" stroke-width="1.2" stroke-dasharray="4 3"/>']
    n_in, n_out = len(h['in']), len(h['out'])
    for i, t in enumerate(h['in']):
        y = cy - (n_in - 1) * 30 + i * 60
        out.append(f'<path class="ln" d="M190 {y} L{cx - 150} {cy + (y - cy) * .5:.0f}" stroke="#1C1B1E" stroke-width="1.4" fill="none"/>')
    for i, (p, ext) in enumerate(h['out']):
        y = cy - (n_out - 1) * 34 + i * 68
        out.append(f'<path class="ln" d="M{cx + 150} {cy + (y - cy) * .5:.0f} L610 {y}" stroke="#1C1B1E" stroke-width="1.4" fill="none"/>')
    out.append('</svg>')
    for i, t in enumerate(h['in']):
        y = cy - (n_in - 1) * 30 + i * 60
        out.append(f'<span class="hx-ad in" style="left: 12px; top: {y - 16}px">{AX.esc(t)}</span>')
    for i, (p, ext) in enumerate(h['out']):
        y = cy - (n_out - 1) * 34 + i * 68
        out.append(f'<span class="hx-ad out" style="left: 612px; top: {y - 20}px"><b>{AX.esc(p)}</b>{AX.esc(ext)}</span>')
    out.append(f'<span class="hx-lab" style="left: {cx - 120}px; top: 34px; width: 240px">Application · {AX.esc(", ".join(h["uc"]))}</span>')
    out.append(f'<span class="hx-dom" style="left: {cx - 80}px; top: {cy - 34}px; width: 160px"><b>Domain</b>{AX.esc(" · ".join(h["dom"]))}</span>')
    out.append(f'<span class="hx-cap" style="left: 12px; top: 8px">Inbound adapters</span><span class="hx-cap" style="left: 612px; top: 8px">Outbound ports → adapters</span>')
    out.append('</div></div>')
    return ''.join(out)

def dd_diagrams():
    out = []
    for dd_id, d in DDS.items():
        for i, sec in enumerate(d['sections']):
            if sec.get('sm'): out.append((dd_key(dd_id, i), render_sm(sec['sm'])))
            if sec.get('er'): out.append((dd_key(dd_id, i), render_er(sec['er'])))
            if sec.get('hex'): out.append((dd_key(dd_id, i), render_hex(sec['hex'])))
    return out

# ------------------------------------------------------------------------------------------------------------------
# Elements: one entry per element (id), with its relationships, views and LikeC4 source
# ------------------------------------------------------------------------------------------------------------------
def elements():
    els, order = {}, []
    for k in VIEW_ORDER:
        v = VIEWS[k]
        for n in v['nodes']:
            e = els.get(n['id'])
            if not e:
                t = AX.TYPES[n['kind']]
                e = els[n['id']] = {'id': n['id'], 'name': n['name'], 'kind': n['kind'], 'type': t['id'], 'layer': t['layer'], 'shape': t['shape'],
                                    'pl': list(n['pl']), 'ext': bool(n.get('ext')), 'wp': n.get('wp', ''), 'views': [], 'rels': [], 'owner': n.get('owner', '')}
                order.append(n['id'])
            if n.get('wp'):
                e['wp'] = n['wp']
            if k in ('application', 'technology', 'landscape') and len(v['modes']) > 1:
                e['pl'] = list(n['pl']) if k == 'application' or not e.get('_plset') else e['pl']
                e['_plset'] = True
            ms = modes_of(v)
            best = next((mm for mm in ['target', 'tr1', 'base'] if mm in ms and mm in n['pl']), ms[0])
            e['views'].append([k, best, n['k']])
            nodes = {x['k']: x for x in v['nodes']}
            for (s_, t_, rel, lab, pl) in v['edges']:
                if n['k'] in (s_, t_):
                    other = nodes[t_ if s_ == n['k'] else s_]
                    r = {'dir': 'out' if s_ == n['k'] else 'in', 'rel': rel, 'other': other['id'], 'otherName': other['name'], 'otherKind': other['kind'], 'label': lab, 'pl': pl}
                    if r not in e['rels']:
                        e['rels'].append(r)
    for e in els.values():
        e.pop('_plset', None)
        d = DETAIL.get(e['id'])
        e['desc'] = d['desc'] if d else ''
        e['owner'] = (d['owner'] if d else '') or e['owner'] or ('Another application' if e['ext'] else 'Corporate credit architects')
        e['origin'] = d['origin'] if d else 'authored'
        e['dd'] = d['dd'] if d else []
        e['adrs'] = d['adrs'] if d else []
        e['arb'] = d['arb'] if d else ''
        e['realizes'] = d['realizes'] if d else ''
        e['contract'] = d['contract'] if d else ''
        e['src'] = likec4_source(e)
    return [els[i] for i in order]

def _key(eid):
    return eid.split('.')[-1]

def likec4_source(e):
    kind = AX.TYPES[e['kind']]['likec4Kind']
    tags = ' '.join(PL_TAG[p] for p in ALL if p in e['pl']) if len(e['pl']) < 3 else ''
    lines = [f"{_key(e['id'])} = {kind} '{e['name']}' {{"]
    if tags:
        lines.append(f'  {tags}')
    if e.get('origin') == 'inferred':
        lines.append('  #inferred')
    if e.get('desc'):
        lines.append(f"  description '{e['desc'][:96]}{'…' if len(e['desc']) > 96 else ''}'")
    lines.append('  metadata {')
    lines.append(f"    owner '{e['owner']}'")
    if e.get('dd'):
        lines.append(f"    dd '{DDS[e['dd'][0]]['path'].rsplit('/', 1)[0]}'")
    if e.get('origin') != 'authored':
        lines.append(f"    origin '{e['origin']}'")
    lines.append('  }')
    lines.append('}')
    for r in e['rels']:
        if r['dir'] == 'out':
            lab = f" '{r['label']}'" if r['label'] else ''
            lines.append(f"{_key(e['id'])} -[{r['rel']}]-> {_key(r['other'])}{lab}")
    return '\n'.join(lines)

def view_source(k, m):
    v = VIEWS[k]
    if m in GAPS:
        a, b = GAPS[m]
        inc = f"  include * where tag is {PL_TAG[a]} or tag is {PL_TAG[b]}\n  style * where tag is not {PL_TAG[b]} {{ opacity 40% }}"
    elif len(v['modes']) > 1:
        inc = f'  include * where tag is {PL_TAG[m]}'
    else:
        inc = '  include *'
    return f"view {view_id(k, m)} of corporate-credit {{\n  title '{v['title']} · {mode_name(m)}'\n{inc}\n  autoLayout TopBottom\n}}"

CATALOGUE = elements()

def js_data():
    views = {}
    for k in VIEW_ORDER:
        v = VIEWS[k]; W, H = size(v)
        views[k] = {'title': v['title'], 'phase': v['phase'], 'sub': v['sub'], 'modes': modes_of(v), 'base': v['modes'], 'w': W, 'h': H,
                    'ids': {m: view_id(k, m) for m in modes_of(v)}, 'src': {m: view_source(k, m) for m in modes_of(v)},
                    'parent': v.get('parent', ''),
                    'nodes': {n['k']: {'name': n['name'], 'kind': n['kind'], 'type': AX.TYPES[n['kind']]['id'], 'layer': AX.TYPES[n['kind']]['layer'],
                                       'id': n['id'], 'pl': n['pl'], 'chg': n.get('chg', []), 'wp': n.get('wp', ''), 'ext': bool(n.get('ext')),
                                       'nav': n.get('nav', ''), 'navMode': n.get('navMode', ''), 'dd': n.get('dd', '')} for n in v['nodes']},
                    'edges': [list(e) for e in v['edges']]}
    return json.dumps({'views': views, 'order': VIEW_ORDER, 'phases': PHASES, 'gaps': GAPS, 'plName': PL_NAME,
                       'layers': {l['id']: l['label'] for l in AX.N['layers']}, 'rels': {r['id']: r['name'] for r in AX.N['relationships']},
                       'cat': CATALOGUE, 'detail': DETAIL, 'dds': DDS, 'services': SERVICES, 'adrs': ADRS, 'plateaus': PLATEAUS, 'wps': WPS,
                       'arbs': ARBS, 'asd': ASD_SECTIONS, 'reqs': REQS, 'changes': CHANGES}, ensure_ascii=False)

if __name__ == '__main__':
    tot = 0
    for k, m in DIAGRAM_KEYS:
        h, w = render(k, m)
        tot += len(h)
        for x in w:
            print('WARN', x)
    print(len(DIAGRAM_KEYS), 'diagrams', tot, 'bytes', len(CATALOGUE), 'elements', len(js_data()), 'js bytes')
