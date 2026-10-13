# IA OS Forge — FDP-17 v1.2 — Testing and Evaluation Strategy
Status: ROUND 5 — CANDIDATE FOR INDEPENDENT REVIEW. DRAFT / NOT APPROVED / NOT READY FOR BUILD / NO BUILD-00 AUTHORIZATION. No tests executed. No staging drills executed. No Founder approval inferred.
The only normative oracle table is [FDP-TRACEABILITY-MATRIX-v1.2-CANONICAL.md](FDP-TRACEABILITY-MATRIX-v1.2-CANONICAL.md). This document defines how tests are run. It does not redefine the 17 FDP-13 sentences and it does not point at a v1.0 or v1.1 matrix.

## 1. Layers
Static checks, unit tests, adapter contract tests, Supabase RLS tests, sandbox tests, STUDIO end-to-end tests, security cases, recovery drills and human review are separate layers. All of them use synthetic tenants. None of them has been executed in Round 5.

## 2. FDP-13 identifiers
The seventeen P0 identifiers and their literal intents remain:

| ID | Literal intent from FDP-13 §191 | Primary story |
|---|---|---|
| AUTH-01 | login required | F-002 |
| AUTHZ-01 | org isolation | F-001 |
| AUTHZ-02 | project isolation | F-002 |
| RLS-01 | cross-tenant deny | F-001 |
| FS-01 | path traversal blocked | F-007 |
| FS-02 | symlink escape blocked | F-007 |
| TERM-01 | destructive command blocked | F-007 |
| SEC-01 | secrets not logged | F-006 |
| SEC-02 | secrets not committed | F-006 |
| ENG-01 | engine permission boundary | F-027 |
| ENG-02 | handoff keeps same scope | F-027 |
| PREVIEW-01 | no privileged IPC | F-028 |
| DEPLOY-01 | prod requires approval | F-030 |
| DEPLOY-02 | wrong release approval rejected | F-029 |
| AUDIT-01 | event cannot be normally altered | F-031 |
| COST-01 | hard budget blocks spend | F-015 |
| STOP-01 | emergency stop halts new work | F-026 |

Supplementary identifiers (CAP-01, VAULT-01, IDEM-01, QUEUE-01, WATCH-01, KILL-01, SAFE-01, SUPPLY-01, ENV-01, DEPLOY-03, DAG-01, MERGE-01, DONE-01, RHFT-01, DESKTOP-01, PI-01..04, SC-01, PROD-01, PROD-05, UX-01, UX-02, and the EVAL-* ids) are defined only in the v1.2 matrix. They are not replacements for the seventeen.

## 3. What a case file contains
Each case in the matrix already states fixture, steps, pass rule and fail rule. A run, when it eventually exists, adds: test_run_id, commit_hash, policy_version, artifact hash, environment name and owner person. Those run fields are empty in this round.

A sentence of the form "security tests passed" does not close any id.

## 4. Evaluations
F-041 defines formulas for interruption rate, time to first visual, generated-app health, one hostile agent scenario and reproducibility. It explicitly does not set numeric product targets. F-022 stores multi-engine scores and cannot complete a task by itself.

## 5. Gates
- SECURITY FOUNDATION: every P0 id in the matrix has a passing positive and a passing negative artifact, and an independent reviewer records PASS. Not true today.
- READY_FOR_HUMAN_TEST: F-039 derivation only.
- Release: immutable artifact plus a staging drill that has not been run.
Zero unresolved Critical or High safety findings are required before a human may consider production. This document does not record that condition as met.
