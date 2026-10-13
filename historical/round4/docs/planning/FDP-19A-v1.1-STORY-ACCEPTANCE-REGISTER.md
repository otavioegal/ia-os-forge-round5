# FDP-19A v1.1 — Story-level DoR/DoD Register
Status: DRAFT. Estimates and named owners pending BUILD-00 planning; no tests run.
Each story below is a detailed planning contract, not evidence of implementation.

## F-001 — Org/project isolation, deny cross tenancy
Priority: P0; owner role: Data; dependencies: Auth.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases RLS-01, AUTHZ-02; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Org/project isolation, deny cross tenancy and emits immutable evidence for RLS-01, AUTHZ-02.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-002 — Auth/RBAC/policy deny unauthorized capability
Priority: P0; owner role: Security; dependencies: F-001.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases AUTH-01, TERM-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Auth/RBAC/policy deny unauthorized capability and emits immutable evidence for AUTH-01, TERM-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-003 — Project Graph nodes/edges versioned
Priority: P1; owner role: Backend; dependencies: F-001.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases GRAPH-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Project Graph nodes/edges versioned and emits immutable evidence for GRAPH-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-004 — Task vs Attempt persistent lifecycle
Priority: P1; owner role: Backend; dependencies: F-001.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases STATE-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Task vs Attempt persistent lifecycle and emits immutable evidence for STATE-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-005 — Immutable audit and Evidence base
Priority: P0; owner role: Backend; dependencies: F-001.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases AUDIT-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Immutable audit and Evidence base and emits immutable evidence for AUDIT-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-006 — Secure credential refs and redacted prompts
Priority: P0; owner role: Security; dependencies: F-002.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases SEC-02; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Secure credential refs and redacted prompts and emits immutable evidence for SEC-02.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-007 — Root-scoped sandbox, isolated preview
Priority: P0; owner role: Desktop; dependencies: F-002.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases FS-02, PREVIEW-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Root-scoped sandbox, isolated preview and emits immutable evidence for FS-02, PREVIEW-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-008 — STUDIO onboarding and goal entry
Priority: P1; owner role: UX; dependencies: F-003.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases UX-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves STUDIO onboarding and goal entry and emits immutable evidence for UX-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-009 — System/Flow/Screens/Plan navigable
Priority: P1; owner role: UX; dependencies: F-008.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases UX-02; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves System/Flow/Screens/Plan navigable and emits immutable evidence for UX-02.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-010 — Plan review and approval binding
Priority: P1; owner role: Backend; dependencies: F-009.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases PLAN-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Plan review and approval binding and emits immutable evidence for PLAN-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-011 — Execution Router and capability filters
Priority: P1; owner role: Orchestration; dependencies: F-002.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases ENG-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Execution Router and capability filters and emits immutable evidence for ENG-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-012 — Claude Code/Codex adapters tested
Priority: P1; owner role: Integration; dependencies: F-011.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases ADAPT-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Claude Code/Codex adapters tested and emits immutable evidence for ADAPT-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-013 — Synkra AIOX adapter/scoped squad
Priority: P1; owner role: Integration; dependencies: F-012.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases ADAPT-02; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Synkra AIOX adapter/scoped squad and emits immutable evidence for ADAPT-02.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-014 — JEV/Model Router controlled routing
Priority: P1; owner role: Orchestration; dependencies: F-011.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases ROUTE-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves JEV/Model Router controlled routing and emits immutable evidence for ROUTE-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-015 — Tool Gateway authorization, cross-attempt dedupe AND hard budget enforcement before external spend
Priority: P0; owner role: Security; dependencies: F-002.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases TERM-01, IDEM-01, COST-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Tool Gateway authorization, cross-attempt dedupe AND hard budget enforcement before external spend and emits immutable evidence for TERM-01, IDEM-01, COST-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-016 — Checkpoint, resume, handoff
Priority: P1; owner role: Orchestration; dependencies: F-004.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases QUEUE-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Checkpoint, resume, handoff and emits immutable evidence for QUEUE-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-017 — Independent review gate
Priority: P1; owner role: QA; dependencies: F-016.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases MERGE-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Independent review gate and emits immutable evidence for MERGE-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-018 — Customer Operations demo with synthetic data
Priority: P1; owner role: Product; dependencies: F-009.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases E2E-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Customer Operations demo with synthetic data and emits immutable evidence for E2E-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-019 — Static/contract/integration/e2e pipelines
Priority: P1; owner role: QA; dependencies: F-002.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases TEST-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Static/contract/integration/e2e pipelines and emits immutable evidence for TEST-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-020 — Immutable release, controlled deployment, rollback
Priority: P1; owner role: Release; dependencies: F-030.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases DEPLOY-02; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Immutable release, controlled deployment, rollback and emits immutable evidence for DEPLOY-02.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-021 — Nonblocking cost dashboard and alerts (hard budget belongs to F-015)
Priority: P2; owner role: Product; dependencies: F-014.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases COST-DASH-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Nonblocking cost dashboard and alerts (hard budget belongs to F-015) and emits immutable evidence for COST-DASH-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-022 — Multi-engine eval baselines
Priority: P2; owner role: QA; dependencies: F-019.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases EVAL-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Multi-engine eval baselines and emits immutable evidence for EVAL-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-023 — Scoped local bridge
Priority: P2; owner role: Desktop; dependencies: F-007.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases FS-02; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Scoped local bridge and emits immutable evidence for FS-02.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-024 — Optional Google/n8n/Supabase adapters
Priority: P2; owner role: Integration; dependencies: F-015.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases ADAPT-03; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Optional Google/n8n/Supabase adapters and emits immutable evidence for ADAPT-03.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-025 — Expanded managed cloud service
Priority: P3; owner role: Product; dependencies: MVP.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases PERF-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Expanded managed cloud service and emits immutable evidence for PERF-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-026 — Emergency Stop and Safe Mode
Priority: P0; owner role: Security; dependencies: F-002.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases STOP-01, SAFE-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Emergency Stop and Safe Mode and emits immutable evidence for STOP-01, SAFE-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-027 — Engine/model/adapter kill switches
Priority: P0; owner role: Orchestration; dependencies: F-026.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases KILL-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Engine/model/adapter kill switches and emits immutable evidence for KILL-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-028 — Preview isolation and privileged IPC boundary
Priority: P0; owner role: Desktop; dependencies: F-007.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases PREVIEW-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Preview isolation and privileged IPC boundary and emits immutable evidence for PREVIEW-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-029 — Approval bound to exact release, replay/expiry
Priority: P0; owner role: Release; dependencies: F-002.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases DEPLOY-02, DEPLOY-03; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Approval bound to exact release, replay/expiry and emits immutable evidence for DEPLOY-02, DEPLOY-03.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-030 — Release Agent separate from Coding Engine
Priority: P0; owner role: Release; dependencies: F-029.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases DEPLOY-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Release Agent separate from Coding Engine and emits immutable evidence for DEPLOY-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-031 — Append-only audit writer / tamper denial
Priority: P0; owner role: Data; dependencies: F-005.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases AUDIT-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Append-only audit writer / tamper denial and emits immutable evidence for AUDIT-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-032 — Stale queue defense, lease, heartbeat, fencing
Priority: P0; owner role: Backend; dependencies: F-004 base.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases QUEUE-01, WATCH-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Stale queue defense, lease, heartbeat, fencing and emits immutable evidence for QUEUE-01, WATCH-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-033 — Supply chain and environment-secret controls
Priority: P0; owner role: Security; dependencies: F-006.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases SC-01, ENV-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Supply chain and environment-secret controls and emits immutable evidence for SC-01, ENV-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-034 — Stable operation_ref across retries/handoff
Priority: P0; owner role: Orchestration; dependencies: F-015.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases IDEM-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Stable operation_ref across retries/handoff and emits immutable evidence for IDEM-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-035 — Build Controller, Task DAG, deadlock detection
Priority: P1; owner role: Orchestration; dependencies: F-004.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases DAG-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Build Controller, Task DAG, deadlock detection and emits immutable evidence for DAG-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-036 — Context Builder scoped memory
Priority: P1; owner role: Orchestration; dependencies: F-006.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases SEC-02; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Context Builder scoped memory and emits immutable evidence for SEC-02.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-037 — Merge Controller and conflict gate
Priority: P1; owner role: QA; dependencies: F-017.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases MERGE-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Merge Controller and conflict gate and emits immutable evidence for MERGE-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-038 — Evidence Service/Build Report
Priority: P1; owner role: Backend; dependencies: F-005.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases DONE-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Evidence Service/Build Report and emits immutable evidence for DONE-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-039 — VERIFIED and Ready-for-Human-Test state
Priority: P1; owner role: Product; dependencies: F-038.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases RHFT-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves VERIFIED and Ready-for-Human-Test state and emits immutable evidence for RHFT-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-040 — Signed desktop updater and recovery
Priority: P1; owner role: Desktop; dependencies: F-007.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases DESKTOP-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Signed desktop updater and recovery and emits immutable evidence for DESKTOP-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.

## F-041 — Critical evals, autonomy KPIs and generated-app health
Priority: P1; owner role: QA; dependencies: F-038.
Source: FDP-19 v1.1 and FDP-06/10/12/13/14/15 as mapped in FDP-TRACEABILITY-MATRIX-v1.1-CANONICAL.md.
DoR: named owner pending assignment; synthetic fixture and org/project scope; capability boundary; dependency proof; threat/risk assessment; positive and negative test cases EVAL-01; effort/timebox pending measurement in BUILD-00.
Positive acceptance: scoped, authenticated user/service achieves Critical evals, autonomy KPIs and generated-app health and emits immutable evidence for EVAL-01.
Negative acceptance: cross-tenant, unauthorized, stale, over-budget, failed-dependency or malformed input (as applicable) is denied and audited without side effects.
DoD: code and migrations reviewed independently; passing positive/negative tests with test-run ID, commit/policy hashes, EvidenceBundle, rollback or recovery plan, no blocking Critical/High and gate recorded.
Status: NOT STARTED / NOT RUN; gate: SECURITY FOUNDATION before side effects for P0; otherwise sprint-specific test/release gate.
