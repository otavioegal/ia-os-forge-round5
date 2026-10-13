# IA OS Forge — FDP-19 v1.0 — Product Backlog
**Status: CONSOLIDATED DRAFT v1.1 — INDEPENDENT REVIEW PENDING; NOT APPROVED. REVISED DRAFT — INDEPENDENT REVIEW PENDING.** Customer Operations is the first MVP vertical.
## Prioritization
P0 security foundation must be finished before any engine effects. P1 enables demonstrable MVP/Ready-for-Human-Test, P2 enhances operations, P3 deferred. Each story requires a detailed DoR record before implementation; this table is an index, not a claim that individual DoR records already exist. DoD requires implementation evidence, tests, independent review and appropriate gate. No feature is APPROVED merely by appearing here.
| ID | Pri | Deliverable / acceptance | Owner | Dependency | Test |
|---|---|---|---|---|---|
| F-001 | P0 | Org/project isolation, deny cross tenancy | Data | Auth | RLS-01, AUTHZ-02 |
| F-002 | P0 | Auth/RBAC/policy deny unauthorized capability | Security | F-001 | AUTH-01, TERM-01 |
| F-003 | P1 | Project Graph nodes/edges versioned | Backend | F-001 | GRAPH-01 |
| F-004 | P1 | Task vs Attempt persistent lifecycle | Backend | F-001 | STATE-01 |
| F-005 | P0 | Immutable audit and Evidence base | Backend | F-001 | AUDIT-01 |
| F-006 | P0 | Secure credential refs and redacted prompts | Security | F-002 | SEC-02 |
| F-007 | P0 | Root-scoped sandbox, isolated preview | Desktop | F-002 | FS-02, PREVIEW-01 |
| F-008 | P1 | STUDIO onboarding and goal entry | UX | F-003 | UX-01 |
| F-009 | P1 | System/Flow/Screens/Plan navigable | UX | F-008 | UX-02 |
| F-010 | P1 | Plan review and approval binding | Backend | F-009 | PLAN-01 |
| F-011 | P1 | Execution Router and capability filters | Orchestration | F-002 | ENG-01 |
| F-012 | P1 | Claude Code/Codex adapters tested | Integration | F-011 | ADAPT-01 |
| F-013 | P1 | Synkra AIOX adapter/scoped squad | Integration | F-012 | ADAPT-02 |
| F-014 | P1 | JEV/Model Router controlled routing | Orchestration | F-011 | ROUTE-01 |
| F-015 | P0 | Tool Gateway authorization, cross-attempt dedupe AND hard budget enforcement before external spend | Security | F-002 | TERM-01, IDEM-01, COST-01 |
| F-016 | P1 | Checkpoint, resume, handoff | Orchestration | F-004 | QUEUE-01 |
| F-017 | P1 | Independent review gate | QA | F-016 | MERGE-01 |
| F-018 | P1 | Customer Operations demo with synthetic data | Product | F-009 | E2E-01 |
| F-019 | P1 | Static/contract/integration/e2e pipelines | QA | F-002 | TEST-01 |
| F-020 | P1 | Immutable release, controlled deployment, rollback | Release | F-030 | DEPLOY-02 |
| F-021 | P2 | Nonblocking cost dashboard and alerts (hard budget belongs to F-015) | Product | F-014 | COST-DASH-01 |
| F-022 | P2 | Multi-engine eval baselines | QA | F-019 | EVAL-01 |
| F-023 | P2 | Scoped local bridge | Desktop | F-007 | FS-02 |
| F-024 | P2 | Optional Google/n8n/Supabase adapters | Integration | F-015 | ADAPT-03 |
| F-025 | P3 | Expanded managed cloud service | Product | MVP | PERF-01 |
| F-026 | P0 | Emergency Stop and Safe Mode | Security | F-002 | STOP-01, SAFE-01 |
| F-027 | P0 | Engine/model/adapter kill switches | Orchestration | F-026 | KILL-01 |
| F-028 | P0 | Preview isolation and privileged IPC boundary | Desktop | F-007 | PREVIEW-01 |
| F-029 | P0 | Approval bound to exact release, replay/expiry | Release | F-002 | DEPLOY-02, DEPLOY-03 |
| F-030 | P0 | Release Agent separate from Coding Engine | Release | F-029 | DEPLOY-01 |
| F-031 | P0 | Append-only audit writer / tamper denial | Data | F-005 | AUDIT-01 |
| F-032 | P0 | Stale queue defense, lease, heartbeat, fencing | Backend | F-004 base | QUEUE-01, WATCH-01 |
| F-033 | P0 | Supply chain and environment-secret controls | Security | F-006 | SC-01, ENV-01 |
| F-034 | P0 | Stable operation_ref across retries/handoff | Orchestration | F-015 | IDEM-01 |
| F-035 | P1 | Build Controller, Task DAG, deadlock detection | Orchestration | F-004 | DAG-01 |
| F-036 | P1 | Context Builder scoped memory | Orchestration | F-006 | SEC-02 |
| F-037 | P1 | Merge Controller and conflict gate | QA | F-017 | MERGE-01 |
| F-038 | P1 | Evidence Service/Build Report | Backend | F-005 | DONE-01 |
| F-039 | P1 | VERIFIED and Ready-for-Human-Test state | Product | F-038 | RHFT-01 |
| F-040 | P1 | Signed desktop updater and recovery | Desktop | F-007 | DESKTOP-01 |
| F-041 | P1 | Critical evals, autonomy KPIs and generated-app health | QA | F-038 | EVAL-01 |
## Hard prerequisites
All P0 controls above, plus their negative tests and independent security review, must be complete before side-effecting engine calls. F-035/036 and context/graph prerequisites must be completed before real autonomous build. F-037/038/039/041 must be complete before Ready-for-Human-Test. F-029/030 must exist as policy and denial tests before any deployment capability, then be integrated and exercised end-to-end during release milestone.
## Change and scope control
Forge does not edit production MAJU or Ethereal. ORAdv integrations are future; no mandatory runtime coupling. Any priority downgrade of P0 or replacement of frozen FDP-10 technology requires formal Change Decision with Founder approval. Reference FDP-TRACEABILITY-MATRIX-v1.0.md for granular cases, including all FDP-13 security IDs.
