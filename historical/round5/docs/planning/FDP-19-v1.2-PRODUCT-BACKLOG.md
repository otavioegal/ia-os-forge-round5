# IA OS Forge — FDP-19 v1.2 — Product backlog index
Status: ROUND 5 — CANDIDATE FOR INDEPENDENT REVIEW. DRAFT / NOT APPROVED / NOT READY FOR BUILD / NO BUILD-00 AUTHORIZATION. No tests executed. No staging drills executed. No Founder approval inferred.
Customer Operations is the first MVP vertical. This file is an index. Acceptance text lives only in FDP-19A v1.2. Oracles live only in the traceability matrix v1.2. There is no normative pointer to a v1.0 or v1.1 matrix.

P0 stories must be accepted before any side-effecting engine call. P1 stories build the demonstrable MVP. P2 stories can slip without reopening P0. P3 is not scheduled.

Effort class on each story is a relative label (S/M/L/XL) with a one-line reason. Person-hours and calendar timeboxes are PENDING CALIBRATION. They are not estimates disguised as commitments.

Named human owners are PENDING HUMAN ASSIGNMENT. The owner column is a role.

| ID | Pri | Title | Role | Sprint | Depends on | Tests |
|---|---|---|---|---|---|---|
| F-001 | P0 | Organization and row isolation | Data | S01 | none (foundation) | RLS-01, AUTHZ-01 |
| F-002 | P0 | Session, project membership and capability grants | Security | S01 | F-001 | AUTH-01, AUTHZ-02, CAP-01 |
| F-003 | P1 | Versioned Project Graph | Backend | S02 | F-001 | GRAPH-01 |
| F-004 | P1 | Task and TaskAttempt persistence | Backend | S01 skeleton, S02 complete | F-001 | STATE-01 |
| F-005 | P0 | Evidence and audit event store | Backend | S01 | F-001 | AUDIT-01 |
| F-006 | P0 | Vault references, redaction and secret-free git | Security | S01 | F-002 | SEC-01, SEC-02, VAULT-01 |
| F-007 | P0 | Project-root sandbox and command allowlist | Desktop | S01 | F-002 | FS-01, FS-02, TERM-01 |
| F-008 | P1 | STUDIO onboarding and goal capture | UX | S02 | F-003 | UX-01 |
| F-009 | P1 | System, Flow, Screens and Plan navigation | UX | S02 | F-008 | UX-02 |
| F-010 | P1 | Plan revision approval binding | Backend | S02 | F-009 | PLAN-01 |
| F-011 | P1 | Execution Router capability filter | Orchestration | S03 | F-002 | ENG-01 |
| F-012 | P1 | Codex and Claude Code adapter contracts | Integration | S03 | F-011 | ADAPT-01 |
| F-013 | P1 | Synkra AIOX adapter with a scoped squad | Integration | S04 | F-012 | ADAPT-02 |
| F-014 | P1 | Model router with deny-by-default | Orchestration | S03 stub, S04 full | F-011 | ROUTE-01 |
| F-015 | P0 | Tool gateway, operation ledger and hard budget | Security | S01 | F-002 | COST-01, IDEM-01, TERM-01 |
| F-016 | P1 | Checkpoint, resume and handoff | Orchestration | S04 | F-004 | QUEUE-01, ENG-02 |
| F-017 | P1 | Independent review gate | QA | S04 | F-016 | MERGE-01 |
| F-018 | P1 | Customer Operations synthetic demonstration | Product | S05 | F-009 | E2E-01 |
| F-019 | P1 | CI pipeline stages | QA | S05 | F-002 | TEST-01 |
| F-020 | P1 | Immutable release and controlled rollback | Release | S06 | F-030 | DEPLOY-02, PROD-05 |
| F-021 | P2 | Non-blocking cost dashboard | Product | S06 | F-014 | COST-DASH-01 |
| F-022 | P2 | Multi-engine evaluation baseline | QA | S05 | F-019 | EVAL-01 |
| F-023 | P2 | Scoped local bridge | Desktop | S06 optional | F-007 | FS-02 |
| F-024 | P2 | Optional Google, n8n and Supabase adapters | Integration | S06 optional | F-015 | ADAPT-03 |
| F-025 | P3 | Expanded managed cloud service | Product | Not scheduled | MVP complete plus Founder Change Decision | PERF-01 |
| F-026 | P0 | Emergency stop and safe mode | Security | S01 | F-002 | STOP-01, SAFE-01 |
| F-027 | P0 | Engine, model and adapter kill switches | Orchestration | S01 | F-026 | KILL-01, ENG-01, ENG-02 |
| F-028 | P0 | Preview origin and privileged IPC boundary | Desktop | S01 | F-007 | PREVIEW-01 |
| F-029 | P0 | Deployment approval bound to one release tuple | Release | S01 policy tests, S06 integration | F-002 | DEPLOY-02, DEPLOY-03 |
| F-030 | P0 | Release Agent separated from Coding Engine | Release | S01 denial tests, S06 full path | F-029 | DEPLOY-01, PROD-01 |
| F-031 | P0 | Append-only audit writer | Data | S01 | F-005 | AUDIT-01 |
| F-032 | P0 | Lease, heartbeat and fencing | Backend | S01 | F-004 | QUEUE-01, WATCH-01 |
| F-033 | P0 | Supply chain, environment secrets and injection containment | Security | S01 | F-006 | SC-01, ENV-01, SUPPLY-01, PI-01, PI-02, PI-03, PI-04 |
| F-034 | P0 | Stable operation_ref across retries and handoff | Orchestration | S01 | F-015 | IDEM-01 |
| F-035 | P1 | Build controller and Task DAG | Orchestration | S03 | F-004 | DAG-01 |
| F-036 | P1 | Context builder least-memory pack | Orchestration | S03 | F-006 | SEC-02 |
| F-037 | P1 | Merge controller | QA | S04 | F-017 | MERGE-01 |
| F-038 | P1 | Evidence service and build report | Backend | S04 | F-005 | DONE-01 |
| F-039 | P1 | Derived Ready-for-Human-Test | Product | S04 | F-038 | RHFT-01 |
| F-040 | P1 | Signed desktop updater | Desktop | S06 | F-007 | DESKTOP-01 |
| F-041 | P1 | Evaluation metrics for the demo | QA | S05 | F-038 | EVAL-HIR-01, EVAL-TFV-01, EVAL-HEALTH-01, EVAL-AGENT-01, EVAL-REPRO-01 |

## Rules that the index itself enforces
- AUTHZ-01 is on F-001. AUTHZ-02 is on F-002. They are not interchangeable.
- SEC-01 and SEC-02 are on F-006. F-036 adds a pack-specific negative and does not take ownership of SEC-01.
- COST-01 is on F-015. F-021 is a non-blocking view and cannot close COST-01.
- F-025 is P3 and has no sprint.
- Downgrading a P0 or replacing a frozen component requires a Change Decision. None is opened in this round.
- Forge does not edit production MAJU, Ethereal or ORAdv.
