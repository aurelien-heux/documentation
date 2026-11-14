"""Align the prototypes on the business teams Request, Client and Facility (with Delivery platform for the
platform teams). People keep one team everywhere: Priya Sharma and Karim Ouali · Request, Marta Kowalski · Client,
Lucas Bernard · Facility, Yann Dupont · Environments, Emma Laurent · Docs. Apps: credit-request (was payments-api),
facility-management (was core-ledger), facility exports (was ledger exports), client-referential (was payments-gateway).
usage: python3 teams_align.py <file>…  (idempotent)"""
import sys
PAIRS = [
    ("Yann Dupont', team: 'Payments'", "Yann Dupont', team: 'Environments'"),
    ("Yann Dupont · Payments", "Yann Dupont · Environments"),
    ("Karim Ouali', team: 'Payments', aud: 'Payments'", "Karim Ouali', team: 'Request', aud: 'Request'"),
    ("by: 'you', team: 'Payments'", "by: 'you', team: 'Request'"),
    ("user: { who: 'Priya Sharma', team: 'Payments' }", "user: { who: 'Priya Sharma', team: 'Request' }"),
    ("it.aud === 'Payments'", "it.aud === 'Request'"),
    ("label: 'My team · Payments'", "label: 'My team · Request'"),
    ("{ me: 'Just you', team: 'Payments' }", "{ me: 'Just you', team: 'Request' }"),
    ("tried on 6 pull requests in Payments", "tried on 6 pull requests in Environments"),
    ("Emma Laurent · Core banking", "Emma Laurent · Docs"),
    ("payments/skill-spring-boot-3", "client/skill-spring-boot-3"),
    ("payments/skill-liquibase-review", "environments/skill-liquibase-review"),
    ("payments/skill-flaky-tests", "request/skill-flaky-tests"),
    ("Rate limits on the payouts API", "Rate limits on the credit request API"),
    ("payments-gateway", "client-referential"),
    ("payments-api", "credit-request"),
    ("LedgerExportTest", "FacilityExportTest"),
    ("ledger-exports", "facility-exports"),
    ("Ledger exports", "Facility exports"),
    ("flaky ledger export test", "flaky facility export test"),
    ("flaky ledger test", "flaky facility export test"),
    ("ledger exports", "facility exports"),
    ("ledger export", "facility export"),
    ("ledger database", "facility database"),
    ("core-ledger", "facility-management"),
    ("Core ledger", "Facility management"),
    ("Core banking plans around", "The Facility team plans around"),
    ("Payments 3.1 · Core banking 4.2 · Data 4.5", "Client 3.1 · Facility 4.2 · Request 4.5"),
    ("Payments, Core banking, Data…", "Client, Facility, Request…"),
    ("Team · Payments", "Team · Request"),
    ("runner-pay-0", "runner-cli-0"),
    ("runner-cb-01", "runner-fac-01"),
    (">payments<", ">client<"),
    ("core-banking", "facility"),
    ("Core banking", "Facility"),
    ("Data platform", "Request"),
    ("Payments", "Client"),
]
for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read(); o = s
    for a, b in PAIRS:
        s = s.replace(a, b)
    if s != o:
        open(p, 'w', encoding='utf-8').write(s); print('aligned', p)
