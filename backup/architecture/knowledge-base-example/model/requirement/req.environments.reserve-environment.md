---
id: req.environments.reserve-environment
level: requirement
updatedAt: '2026-10-14'
acceptance:
- given: an Environment E with no active Reservation
  when: a user reserves E for 4 hours with a reason
  then: a Reservation is created, active until now + 4 h, and the user becomes its Holder
- given: an active Reservation of scope application on E for Application A
  when: another user reserves Module M of A on E
  then: the request is refused with the Holder and expiresAt (INV-ENV-05)
- given: an active Reservation R held by the user
  when: the user extends R by 2 hours
  then: R expires 2 hours later, within the 24 h maximum
- given: an active Reservation whose expiresAt is reached
  when: the expiry job runs
  then: the Reservation moves to expired and EVT-RESERVATION-EXPIRED is published
decisionTable:
- case: no overlapping active Reservation
  outcome: OK
- case: overlapping Reservation, same Holder
  outcome: OK
- case: overlapping Reservation, other Holder
  outcome: KO
  reason: INV-ENV-05
- case: duration over 24 h
  outcome: KO
  reason: INV-ENV-07
- case: production tier
  outcome: KO
  reason: INV-ENV-14
operational:
  p95LatencyMs: 300
  activeReservationsMax: 500
---

Teams protect a placement while they test, without asking the platform team and without a
spreadsheet nobody enforces. Every Reservation expires, so a forgotten one never blocks an
Environment for long.

## Out of scope

Reservations on production Environments; priority or queueing between teams.
