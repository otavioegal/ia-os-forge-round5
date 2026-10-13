# IA OS Forge — FDP-16 v1.0 — AIOX / Execution Engines
**Status: CONSOLIDATED DRAFT v1.1 — INDEPENDENT REVIEW PENDING; NOT APPROVED. REVISED DRAFT — INDEPENDENT REVIEW PENDING.** 2026-10-13.
**Supersedes for proposed baseline:** v0.1 with appended corrective amendments. Prior preserved in docs/reviews/round3-backup. Normative approved sources: FDP-06, 10, 12, 13; FDP-15 under approval; no new Founder authorization inferred.

## 1. Boundaries, architecture and control
The Forge owns Project Graph, durable Build/Task/Attempt state, policy, cost ledger and evidence. Synkra AIOX is the preferred orchestrator behind its adapter; Claude Code/Codex/Grok are interchangeable engines. The Execution Router chooses engine, Model Router chooses model, Tool Router chooses capability provider. A policy enforcement point outside the model authorizes each tool invocation. Build autonomy runs only under approved scope, plan, permission and budget. Production, destructive changes, credentials and externally consequential actions need authenticated hard gates.

## 2. Canonical aggregates
- Project: source of truth FDP-12, with tenant/project isolation and versioned graph.
- Build: build_id, project_id, plan_revision, graph_revision, policy_version, budget ceiling, status, task graph, last checkpoint, evidence bundle, approval references, correlation_id.
- Task: stable task_id, goal, acceptance criteria, dependencies, priority, risk/data classification, status and version, per FDP-12.
- TaskAttempt: attempt_id, task_id, engine id/version, scoped runner/worktree, lease_id, fencing_epoch, logs, checkpoints and terminal result. Handoff always creates a new Attempt under the same Task.
- Operation: project_id, task_id, operation_ref, capability, normalized_input, status and external result. Tracks intent across all Attempts.
- Review, Release and Deployment remain separate audited entities.

## 3. State ownership and transition contract
Build Controller alone transitions Build; Task Service alone transitions Task; Attempt Manager alone transitions Attempt. Approved FDP-12 terms are canonical for Task: QUEUED, READY, RUNNING, WAITING, RETRYING, HANDOFF, REVIEWING, BLOCKED, COMPLETED, FAILED, CANCELLED as applicable; FDP-06 labels are display aliases only where an exact mapping is documented. Build: PLANNED → AWAITING_APPROVAL → QUEUED → RUNNING → TESTING → REVIEWING → READY_FOR_HUMAN_TEST, with BLOCKED, CHANGES_REQUESTED, FAILED and CANCELLED branches. Attempt: CREATED → QUEUED → PROVISIONING → RUNNING → PAUSED → RUNNING or SUCCEEDED/FAILED/CANCELLED/TIMED_OUT/LOST.
Transitions require authenticated actor/service, matching optimistic version, valid current state, policy and prerequisite evidence; effects occur transactionally with append-oriented event emission. Illegal transitions are denied and audited. CLAIMED_DONE is only a claim; VERIFIED requires passing tests, EvidenceBundle and independent review. READY_FOR_HUMAN_TEST is derived after all MVP acceptance gates, never inferred from agent text. Exact FDP-12 enum names must be normalized in a migration-free contract ADR before code; never introduce conflicting stored enums.

## 4. Plan compiler and scheduling
Plan Compiler converts approved plan into versioned Task DAG, validates cycles and dependencies, and rejects unbounded recursion. Partial blocking affects dependent subgraph only; unrelated tasks may continue within original policy. Durable queue and outbox support retries and dedupe. Lease with heartbeat, expiry and fencing epoch ensures a stale runner cannot write. Watchdog detects stalled tasks, missing heartbeat, retry loops, deadlocks and excess budget; STOP and SAFE MODE deactivate risky capabilities at gateway. No simultaneous writers to same protected worktree.

## 5. Operation idempotency and handoff
The normalized key is hash(project_id, task_id, operation_ref, capability, normalized_input). attempt_id MUST NOT be included. The Operation Ledger is authoritative across retries and handoffs. New Attempt reuses the existing operation_ref for the same intended side effect, consults ledger and external provider before resend, and blocks ambiguous non-idempotent retries for reconciliation. New distinct intent receives new operation_ref. Use optimistic concurrency and outbox for dedupe; not all providers guarantee exactly-once execution.

## 6. Engine adapters, context, review and merge
Adapters implement FDP-15: describe, health, invoke, cancel; engine-specific start/resume/pause/get_status/checkpoint/diff/tests. Unsupported capability is explicit UNSUPPORTED, never silently emulated. Context Builder assembles least-necessary scoped, provenance-tagged memory without secrets or unrestricted chat. Merge Controller requires unchanged base hash, worktree safety, clean independent review, tests, no Critical/High findings and a policy-appropriate merge gate. Conflicts pause rather than force merge. Reviewer may not approve own code. AIOX framework preference is frozen; only its version/capabilities/isolation remain ADR parameters.
Autonomous/Guided/Restricted modes affect convenience, not hard gates.

## 7. Checkpoints and recovery
Checkpoint includes Git ref, graph revision, safe runtime state, dependency lock hash, completed operations and test evidence. Validate hashes, policy expiration, leases and project root on resume. Handoff creates new Attempt; old Attempt becomes terminal and cannot retain tool privileges. On failure revoke active tool grants; reconcile side effects before retry. Build Report summarizes diff, tests, findings, remaining risks, readiness and preview links, separate from deployment.

## 8. Security and observability
Tauri/sidecar/project-root and cloud runner boundaries, segregated tenants, RLS plus application policy, secrets as vault references, untrusted external content, network/command allowlists, spend and token budgets, kill switches, append-only audit and OpenTelemetry are mandatory. STUDIO displays engine, events, costs, checkpoints and blocking reasons without revealing secrets.

## 9. Acceptance contracts
DAG-01 reject cycle/deadlock; WATCH-01 fencing after timeout; IDEM-01 no duplicate effect across handoff; SECRET-01 minimized context; MERGE-01 no unauthorized/contradictory merge; DONE-01 claims without evidence blocked; RHFT-01 derived readiness; STOP-01 and SAFE-01 prevent side effects; QUEUE-01 stale message rejected; SUPPLY-01 unsafe dependency refused. Each has positive and negative variant in FDP-17 and evidence in traceability matrix.

## 10. Gate
Pending independent review of invariants, enum mapping, race/TOCTOU, policy and contracts. No code/build/deploy authorized. See FDP-17…20 and the traceability matrix.
