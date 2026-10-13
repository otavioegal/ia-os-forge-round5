# FDP-18A v1.1 — Controlled Recovery Runbooks
Status: DRAFT / NOT CERTIFIED / NO STAGING DRILLS. Companion to FDP-18 v1.1. This is not authorization to execute on production.

## Common mandatory record
Each runbook requires: runbook_id/version, immutable release digest, environment, named primary/backup on-call, detector query, numeric threshold/unit and observation window approved from staging measurements, policy and approval IDs, backup/restore point, RPO/RTO targets and measured values, step transcript, start/stop timestamps, health and RLS verification, independent reviewer and evidence hashes. Missing field blocks release readiness. Concrete deployment commands must come from versioned, reviewed operator scripts; no improvised production commands.

| Runbook | Preconditions | Detector/trigger | Authorized action | Verification | Failure branch |
|---|---|---|---|---|---|
| RB-APP | previous healthy image digest, compatible schema, routing snapshot | error/latency or smoke beyond approved measured window | Release Operator freezes rollout and restores routing to known-good immutable revision through approved release workflow | API smoke, health, tenant RLS, audit, queue and cost policy over observation window | Safe Mode, escalate Release/Security |
| RB-SCHEMA | migration_set_hash, verified backup, expand/contract matrix, DB/Security approval | checksum, RLS or compatibility failure | stop dependent writes; prefer reviewed forward fix; destructive restore only with separate human gate | schema integrity, row reconciliation, RLS negative cases, audit, RPO/RTO | keep writes disabled and escalate |
| RB-RUNNER | watchdog lease state, operation ledger and checkpoint | lease expired or fencing mismatch | fence runner, revoke grants, reconcile external receipts, increment epoch, create new Attempt only after reconciliation | no duplicate external effect, same Task, valid checkpoint, audit | WAITING reconciliation, no blind retry |
| RB-DESKTOP | previous signed build, local journal snapshot | bad signature, boot smoke or journal integrity | block update, preserve journal, restore verified signed build using approved updater | signature, project-root boundary, sidecar compatibility, audit sync | Safe Mode and desktop operator |
| RB-SECRET | Security incident reference, vault rotation path | exposed credential, unexpected egress, invalid grant | kill switch, revoke and rotate scoped secrets, invalidate sessions, preserve redacted evidence | old credential denied, new scoped, tenant isolation and audit | containment remains active |

## Staging certification procedure
1. Assign named primary/backup on-call and independent reviewer; select synthetic tenant fixture and immutable release.
2. Approve exact threshold, query, observation window, RPO/RTO target and versioned command/job references based on measured staging baseline.
3. Capture baseline, verify restore point and policy; inject a synthetic failure and record detector timestamps.
4. Execute only approved staging workflow, record output hashes, stop/resume decisions and side effects.
5. Run health, RLS, audit, cost and regression tests, measure elapsed time and actual RPO/RTO.
6. Attach immutable drill report, reviewer findings and corrective actions; certify only if all positive/negative checks pass and no Critical/High remains.

Until exact scripts, quantitative thresholds and staging drill evidence are supplied, these are **operational specifications, not certified executable runbooks**. Production deployment remains blocked.
