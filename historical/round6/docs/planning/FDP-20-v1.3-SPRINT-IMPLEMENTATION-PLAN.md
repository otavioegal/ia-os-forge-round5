# IA OS Forge — FDP-20 v1.3 — Sprint and implementation plan
Status: ROUND 6 — CANDIDATE FOR CODEX REVIEW. DRAFT / NOT APPROVED / NOT READY FOR BUILD / NO BUILD-00 AUTHORIZATION. No tests executed. No staging drills executed. No Founder approval inferred.
No dates and no cost ceiling are set. Effort calibration is an open pendency. Spikes have not run.

## Preconditions that are still open
Founder confirmation of FDP-14, Founder approval of FDP-15, independent Codex review of this v1.3 set, and a separate decision to authorize BUILD-00. This document is a candidate for that review, not the authorization.

## Milestones
| Phase | Stories | Exit intended | Current evidence |
|---|---|---|---|
| BUILD-00 | SPIKE-01 through SPIKE-09 only | spike reports and a test scaffold | NOT RUN; not authorized |
| SPRINT-01 | F-001, F-002, F-004 schema skeleton, F-005, F-006, F-007, F-015, F-026, F-027, F-028, F-029 decision function, F-030 denial, F-031, F-032, F-033, F-034 | SECURITY FOUNDATION | NOT STARTED |
| SPRINT-02 | F-003, F-004 transitions, F-008, F-009, F-010 | plan and navigation demo | NOT STARTED |
| SPRINT-03 | F-011, F-012, F-014 stub, F-035, F-036 | execution gate; engines only if SPRINT-01 gate is actually green | NOT STARTED |
| SPRINT-04 | F-013, F-014 full, F-016, F-017, F-037, F-038, F-039 | review and derived human-test flag | NOT STARTED |
| SPRINT-05 | F-018, F-019, F-022, F-041 | synthetic Customer Operations demo | NOT STARTED |
| SPRINT-06 | F-020, F-021, F-029 integration, F-030 full path, F-040; F-023 and F-024 optional | release readiness specification | NOT STARTED; drills not run |
| Unscheduled | F-025 | none | requires a future Change Decision |

SPRINT-03 must not call a side-effecting engine unless the SECURITY FOUNDATION exit is truly met. Writing this table does not meet it.

## Spikes (FDP-10 §115 themes, still NOT RUN)
| Spike | Pass | Fail |
|---|---|---|
| SPIKE-01 Tauri to Node sidecar stream | ordered fixture frames arrive and the preview origin gains no privileged IPC | a frame handler invokes a tool |
| SPIKE-02 Codex adapter | describe, invoke, cancel, status on a synthetic task | the adapter's grant set changes during the run |
| SPIKE-03 Claude Code adapter | same contract as SPIKE-02 | a resolved secret appears in the adapter log |
| SPIKE-04 Envelope handoff | same task id, new attempt, same operation_ref, provider counter unchanged | a second provider execution or a second task |
| SPIKE-05 Two worktrees | each task writes only its worktree; conflict is detected | both tasks write one shared index |
| SPIKE-06 Graph impact | same node set for the same revision, foreign project excluded | set changes across two reads or includes the other project |
| SPIKE-07 tldraw sync | round trip keeps node ids; illegal edge rejected | an id is dropped or a cross-project edge is stored |
| SPIKE-08 PGMQ | one winner of two claims; stale epoch denied | two valid leases or a stale write commits |
| SPIKE-09 Shell scope | allowlisted command inside the root works | traversal or an off-list command runs |

Owner role and timebox for each spike: PENDING HUMAN ASSIGNMENT and PENDING CALIBRATION. A spike failure is recorded, not waived.

## Frozen stack
Repeated from FDP-18 v1.3 so sprint planning cannot drift. The normative copy is FDP-18. MVP: Tauri 2, React/TypeScript/Vite, Node sidecar, tldraw, Supabase PostgreSQL/Auth/RLS/Storage, Supabase Queues/PGMQ, Git worktrees, Fastify, Cloud Run, OpenTelemetry, n8n, Codex, Claude Code. P1 prepared: Grok, OpenRouter, remote workers. Deferred: Temporal, Neo4j, Redis/BullMQ, Kafka, Kubernetes.

## Required set for READY_FOR_HUMAN_TEST
F-039 may derive the flag only when every story in the required set is COMPLETED with its evidence bundle and the security-foundation gate is recorded. The sprint table is not this set.

Required: F-001, F-002, F-003, F-004, F-005, F-006, F-007, F-008, F-009, F-010, F-011, F-012, F-013, F-014, F-015, F-016, F-017, F-018, F-019, F-026, F-027, F-028, F-029, F-030, F-031, F-032, F-033, F-034, F-035, F-036, F-037, F-038.

Not required for the flag: F-020 (release), F-021 (dashboard, P2), F-022 (P2 eval scores), F-023 (P2 bridge), F-024 (P2 optional adapters), F-025 (P3, unscheduled), F-040 (desktop updater), F-041 (metrics, recorded after the demo, not a precondition of the flag).

F-039 is the derivation story. It is not a member of its own prerequisite list.

## Readiness wording
This plan is a candidate for Codex review. It is not READY FOR BUILD. A later decision that the plan is READY FOR BUILD would still not, by itself, authorize BUILD-00. Stories are not operationally READY while owners and timeboxes are pending.
