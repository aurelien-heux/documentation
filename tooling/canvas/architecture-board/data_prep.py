"""Compact the Meridian Bank model (MODEL of backup/architecture/pages/architecture-meridian-bank.html) for the Architecture board, and add
the prototype's business extension: business roles, role × process (RACI) and the application components that
serve each business process. Everything added is marked ext: true so the board can say so.
usage: python3 data_prep.py <mb_model.json> <arch_data.json>"""
import json, sys, re

src, dst = sys.argv[1], sys.argv[2]
m = json.load(open(src, encoding='utf-8'))

KEEP = ['id', 'level', 'kind', 'title', 'scope', 'scopeType', 'portfolio', 'chain', 'description', 'plateaus', 'change',
        'status', 'owner', 'module', 'workItemId', 'contract', 'adr', 'domainRef', '_path', 'addressedBy', 'dd', 'view',
        'acceptance', 'decisionTable', 'operational', 'updatedAt', 'decision', 'affects', 'realizes', 'dependsOn', 'application']
META = ['level', 'parent', 'maturity', 'investment', 'strategic', 'lifecycle', 'category', 'start', 'end', 'class', 'date']

def strip_html(h):
    h = re.sub(r'<svg.*?</svg>', '', h or '', flags=re.S)
    h = re.sub(r'<div class="diagram">.*?</div></div>', '', h, flags=re.S)
    return h

els = []
for e in m['elements']:
    d = {k: e[k] for k in KEEP if k in e and e[k] not in (None, [], '', {})}
    md = {k: v for k, v in (e.get('metadata') or {}).items() if k in META}
    if md: d['meta'] = md
    if e.get('_html'):
        d['html'] = strip_html(e['_html'])[:4000]
    d['src'] = (e.get('_source') or '')[:600]
    els.append(d)

rels = [{'s': r['source'], 't': r['target'], 'k': r['kind'], 'l': r.get('title') or ''} for r in m['relations']]

# ---------------------------------------------------------------- business extension (prototype data)
roles = [
    ('role.ent.relationship-manager', 'Relationship manager', 'Corporate front office'),
    ('role.ent.credit-analyst', 'Credit analyst', 'Credit department'),
    ('role.ent.credit-committee', 'Credit committee', 'Delegated decision body'),
    ('role.ent.credit-back-office', 'Credit back office', 'Facility administration'),
    ('role.ent.branch-advisor', 'Branch advisor', 'Retail network'),
    ('role.ent.customer', 'Customer', 'Retail or corporate client (external)'),
    ('role.ent.payments-ops', 'Payments operations', 'Payment factory'),
    ('role.ent.compliance-officer', 'Compliance officer', 'KYC, AML and sanctions'),
    ('role.ent.reporting-analyst', 'Regulatory reporting analyst', 'Finance'),
    ('role.ent.risk-manager', 'Risk manager', 'Credit risk'),
]
for rid, title, desc in roles:
    els.append({'id': rid, 'level': 'abb', 'kind': 'business-role', 'title': title, 'scope': 'ent', 'scopeType': 'enterprise',
                'description': desc, 'plateaus': [], 'status': 'done', 'owner': 'Head of business architecture',
                '_path': 'model/bb/enterprise-roles.c4', 'ext': True,
                'src': f"{rid.split('.')[-1]} = business-role '{title}' {{\n  #done\n  metadata {{ owner 'Head of business architecture' }}\n}}"})

# RACI per process: R performs, A decides, C consulted, I informed
RACI = {
    'abb.corporate.credit-request-process': {'relationship-manager': 'R', 'credit-analyst': 'R', 'credit-committee': 'A', 'credit-back-office': 'I', 'customer': 'C', 'risk-manager': 'C'},
    'abb.corporate.facility-setup-process': {'credit-back-office': 'R', 'relationship-manager': 'C', 'credit-committee': 'I', 'customer': 'I', 'risk-manager': 'I'},
    'abb.corporate.credit-application-process': {'relationship-manager': 'R', 'credit-analyst': 'R', 'credit-committee': 'A', 'credit-back-office': 'R', 'customer': 'C'},
    'abb.retail.online-onboarding-process': {'customer': 'R', 'compliance-officer': 'A', 'branch-advisor': 'I'},
    'abb.retail.branch-onboarding-process': {'branch-advisor': 'R', 'customer': 'C', 'compliance-officer': 'C'},
    'abb.payments.instant-payment-process': {'customer': 'R', 'payments-ops': 'A', 'compliance-officer': 'C'},
    'abb.payments.payment-processing': {'payments-ops': 'A', 'compliance-officer': 'C', 'customer': 'I'},
    'abb.risk.regulatory-reporting-process': {'reporting-analyst': 'R', 'risk-manager': 'A', 'compliance-officer': 'C'},
}
RACI_LABEL = {'R': 'performs', 'A': 'decides', 'C': 'consulted', 'I': 'informed'}
for p, roles_ in RACI.items():
    for r, v in roles_.items():
        rels.append({'s': f'role.ent.{r}', 't': p, 'k': 'assignment', 'l': RACI_LABEL[v], 'raci': v, 'ext': True})

# application components that serve each business process (TOGAF Application/Function matrix)
SUPPORT = {
    'abb.corporate.credit-request-process': ['credit-request-service', 'pricing-engine', 'client-hub', 'credit-risk-engine'],
    'abb.corporate.facility-setup-process': ['facility-service', 'collateral-management', 'core-banking'],
    'abb.corporate.credit-application-process': ['credit-origination', 'pricing-workbook', 'client-hub'],
    'abb.retail.online-onboarding-process': ['digital-onboarding', 'mobile-banking', 'crm', 'core-banking'],
    'abb.retail.branch-onboarding-process': ['branch-account-opening', 'branch-workstation', 'core-banking'],
    'abb.payments.instant-payment-process': ['instant-payments', 'payment-hub', 'sanctions-screening', 'fraud-detection'],
    'abb.payments.payment-processing': ['payment-hub', 'sepa-gateway', 'swift-connector', 'sanctions-screening'],
    'abb.risk.regulatory-reporting-process': ['regulatory-reporting', 'data-platform', 'data-warehouse', 'general-ledger'],
}
APPS = m['levels']['applications']
for p, apps in SUPPORT.items():
    for a in apps:
        comp = APPS[a]['components'][0]
        rels.append({'s': comp, 't': p, 'k': 'serving', 'l': 'supports', 'ext': True})

# business role glyph for the notation (ArchiMate business role: a cylinder lying on its side; drawn simply)
notation = {k: {'name': v['name'], 'layer': v['layer'], 'shape': v['shape'], 'svg': v['svg']} for k, v in m['notation'].items()}
notation['business-role'] = {'name': 'Business role', 'layer': 'business', 'shape': 'square',
                             'svg': '<path d="M4 8.5h11a3.5 3.5 0 0 1 0 7H4"/><ellipse cx="4.5" cy="12" rx="2" ry="3.5"/>'}
notation['decision'] = {'name': 'Decision record', 'layer': 'other', 'shape': 'square', 'svg': '<path d="M6 3.5h9l3.5 3.5v13.5H6z"/><path d="M9 11h6M9 14.5h6M9 18h4"/>'}
notation['api'] = {'name': 'DD · API', 'layer': 'other', 'shape': 'square', 'svg': '<path d="M8 7 3.5 12 8 17M16 7l4.5 5-4.5 5M13.5 5l-3 14"/>'}
notation['domain'] = {'name': 'DD · domain', 'layer': 'other', 'shape': 'square', 'svg': '<path d="M8 7 3.5 12 8 17M16 7l4.5 5-4.5 5M13.5 5l-3 14"/>'}

# ARB extension: asks to the board, review commit, pull request
arbs = m['arbs']
EXT_ARB = {
    'arb.corporate.2026-14': {'pr': 88, 'reviewedSha': '7c1e9a0', 'branch': 'change/WP-FAC-02', 'updatedSinceReview': True,
                              'asks': [{'id': 'A1', 'text': 'Accept the cut-over of live facilities over one weekend, with the monolith read-only.', 'status': 'pending'},
                                       {'id': 'A2', 'text': 'Decide the archive format for closed facilities: keep them in the monolith schema, or export to the document archive.', 'status': 'pending'},
                                       {'id': 'A3', 'text': 'Confirm the switch-off date of the credit origination monolith (2027-06-30).', 'status': 'pending'}]},
    'arb.corporate.2026-09': {'pr': 61, 'reviewedSha': '2b8d4c1', 'branch': 'change/WP-REQ-01', 'updatedSinceReview': False, 'asks': []},
    'arb.payments.2026-11': {'pr': 74, 'reviewedSha': '9e0a3f5', 'branch': 'change/WP-PAY-03', 'updatedSinceReview': False,
                             'asks': [{'id': 'A1', 'text': 'Accept real-time sanctions screening latency of 400 ms within the 10 s scheme budget.', 'status': 'accepted'}]},
    'arb.risk.2026-16': {'pr': 97, 'reviewedSha': None, 'branch': 'change/WP-RSK-01', 'updatedSinceReview': False, 'asks': []},
}
for a in arbs:
    a.update(EXT_ARB.get(a['id'], {}))
    a.pop('_path', None)

out = {
    'enterprise': m['levels']['enterprise'],
    'elements': els, 'relations': rels, 'arbs': arbs,
    'landscapes': m['landscapes'],
    'portfolios': m['levels']['portfolios'], 'applications': m['levels']['applications'],
    'capabilities': m['levels']['capabilities'], 'realizes': m['levels']['realizes'],
    'technology': m['levels']['technology'], 'data': m['levels']['data'], 'flows': m['levels']['flows'],
    'roadmap': m['levels']['roadmap'], 'validation': m['validation'], 'notation': notation, 'layers': m['layers'],
    'raciLabel': RACI_LABEL,
}
json.dump(out, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('elements', len(els), 'relations', len(rels), 'bytes', len(json.dumps(out, ensure_ascii=False, separators=(',', ':'))))
