# FDP-18A v1.2 — Recovery runbooks, split by evidence class
Status: ROUND 5 — CANDIDATE FOR INDEPENDENT REVIEW. DRAFT / NOT APPROVED / NOT READY FOR BUILD / NO BUILD-00 AUTHORIZATION. No tests executed. No staging drills executed. No Founder approval inferred.
Companion to FDP-18 v1.2. These are not certified executable runbooks. No drill has been run. No threshold has been measured. No on-call person has been named.

The round-4 finding was that runbooks depended on staging numbers while being described as if they were procedures. This version splits every runbook into three classes so the dependency is explicit.

- Class A — required before BUILD as specification. Written below. An implementer can build the hooks without a measured SLO.
- Class B — required before production, filled only from staging measurements. Currently empty on purpose. Inventing a number here is a defect.
- Class C — a staging drill that must be executed before production. Not executed. Round 5 does not attach a drill report.

## Class A — common procedure requirements
Each runbook has an operator role, a detector that is a named signal rather than a number, an authorized action, a verification set and a failure branch. Concrete shell commands belong to versioned operator scripts that do not exist yet; until those scripts exist, the action is described as an intent the Release or Security role performs through the approved workflow, not as an ad-hoc command.

| ID | Class A trigger (signal, not a number) | Who may act | Authorized action | Verification before calling it recovered | If verification fails |
|---|---|---|---|---|---|
| RB-APP | rollout health signal reports failed smoke, or the error counter moves from the baseline captured for that release | Release Operator | freeze rollout and point routing at the previous immutable digest, keeping the current schema if the compatibility matrix says the previous app supports it | API smoke on synthetic tenant, RLS negative, audit insert still works, queue claim still fences, budget denial still returns 402 | leave safe mode on and escalate; do not continue the rollout |
| RB-SCHEMA | migration job reports checksum, RLS or compatibility failure | DB Operator together with Security Reviewer | stop writes that depend on the new schema; prefer a reviewed forward fix; a restore from backup is a separate human gate | schema version, row-count reconciliation query defined by the migration, RLS negative, audit insert | keep writes stopped |
| RB-RUNNER | watchdog reports lease expired or fencing mismatch | Execution Operator | revoke grants, reconcile the operation ledger, only then allow a new attempt | no second provider execution for the same operation_ref; task id unchanged; checkpoint digest verifies | task stays WAITING; no blind retry |
| RB-DESKTOP | updater reports bad signature, failed boot smoke, or journal hash mismatch | Desktop Operator | refuse the package and reinstall the previous signed build, keeping the journal | signature of the restored build, project-root check, journal hash equals the pre-update hash | safe mode; do not retry the bad package |
| RB-SECRET | secret scan hit, unexpected egress alert, or a credential used from the wrong environment | Security Operator | stop latch, revoke the vault ref, rotate, invalidate sessions, keep redacted evidence | old credential receives denial; new credential is scoped to one project; audit contains the incident id | containment stays on |

## Class B — parameters that are intentionally blank
For each runbook the following fields exist and are UNMEASURED: numeric threshold, unit, observation window, detector query text, RPO target, RTO target, primary on-call name, backup on-call name, operator script version. A release checklist treats a blank Class B field as "not ready for production". A blank Class B field does not block writing Class A code in BUILD, and it does not count as a measured value.

## Class C — drills not run
The staging procedure, when a human later authorizes it, is: name the on-call pair, choose the synthetic tenant, record the Class B numbers from an actual baseline, inject one synthetic fault, follow only the versioned script, store output hashes, and have a reviewer who did not run the script sign the report. Until that report exists, Class C is NOT EXECUTED for RB-APP, RB-SCHEMA, RB-RUNNER, RB-DESKTOP and RB-SECRET.

## What this closes and what it does not
Class A is specified. Class B and Class C stay open pendencies. This split is the correction. It is not a claim that rollback has been rehearsed.
