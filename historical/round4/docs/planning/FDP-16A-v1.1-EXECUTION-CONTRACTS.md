# FDP-16A v1.1 — Execution contracts
Status: DRAFT / NOT APPROVED. Companion normative annex to FDP-16 v1.1; no tests executed.

## Durable aggregates and fields
Every record: id, organization_id, project_id, version, correlation_id, created_at, updated_at. RLS and application policy both enforce isolation.
- Build: build_id, plan_revision, graph_revision, policy_version, budget_limit_minor, budget_spent_minor, reserved_minor, status, evidence_ref.
- Task: task_id, build_id, dependency_task_ids, goal, acceptance, status with literal FDP-12 enum QUEUED READY RUNNING WAITING RETRYING HANDOFF REVIEWING BLOCKED COMPLETED FAILED CANCELLED.
- TaskAttempt: attempt_id, task_id, sequence, engine_id, lease_id, fencing_epoch, heartbeat_at, worktree_ref, checkpoint_ref, status.
- Operation: operation_ref, task_id, capability, normalized_input_digest, external_receipt, status, reconciliation_state; unique by project_id/task_id/operation_ref/capability/input digest, not attempt_id.
- Lease: lease_id, attempt_id, task_id, owner, epoch, expires_at, heartbeat_at; epoch increments atomically on reacquisition.
- Checkpoint: checkpoint_id, task_id, attempt_id, git_ref, graph_revision, operation_ledger_watermark, digest.
- EvidenceBundle: bundle_id, task_id, commit_hash, test_run_ids, review_id, findings, artifact_hashes, decision.
- DeploymentApproval: approval_id, release_id, source_git_hash, artifact_digest, graph_revision, migration_set_hash, environment_id, policy_version, expires_at, consumed_at, revoked_at, approved_by.

## Command and event envelopes
Commands contain command_id, actor_ref, org/project, expected_version, correlation_id, policy_version, capability, operation_ref and issued_at. Events contain event_id, aggregate_id/version, causation_id, correlation_id, policy_decision_ref, evidence_ref and timestamp. State update plus outbox event is one DB transaction; delivery at least once, dedupe by event_id. Compare-and-swap rejects version conflict.

| Command | Preconditions | Effect | Denial |
|---|---|---|---|
| StartBuild | plan revision approved and security foundation green | PLANNED to QUEUED, BuildQueued | approval mismatch, STOP |
| ClaimTask | dependencies COMPLETED and no valid lease | atomic lease/epoch, TaskClaimed | stale or concurrent claim |
| Heartbeat | matching lease and epoch | lease extension | stale fencing |
| InvokeCapability | scope, grant, budget reserve, operation ledger reconciled | durable intent/outbox and operation receipt | over-budget, unsafe tool, ambiguous retry |
| Handoff | checkpoint verified | new Attempt under same Task, stable operation_ref | invalid checkpoint |
| VerifyTask | passing tests, independent reviewer, evidence bundle | Task COMPLETED, TaskVerified | agent-only completion |
| StopBuild | authorized operator or emergency policy | STOP latch, deny new effects | unauthorized resume |
| MergeTask | unchanged base, independent review, tests green | protected merge and audit | conflict or High finding |
| DeployRelease | exact unexpired single-use human approval and Release Agent | consume approval atomically, deploy immutable digest | replay, changed tuple |

## Transition, retry and concurrency rules
Only owner service transitions each aggregate with expected version. Illegal transitions denied and audited. PlanCompiler rejects cycles/missing dependencies; blocked descendants do not stop independent branches. Transient faults retry with capped exponential backoff+jitter; permanent policy/auth/validation faults are blocked, not retried. Ambiguous external outcomes are reconciled with receipts before another attempt; no exactly-once claim without provider guarantee. Watchdog fences expired runner, revokes grant, checks operation ledger and checkpoint, then creates a new Attempt. CLAIMED_DONE is only a claim, never a persisted Task enum. Ready-for-Human-Test requires all required Tasks COMPLETED, EvidenceBundle, independent review and gates. Hard budget uses integer minor units and denies reservation when spent+reserved+new cost exceeds approved limit, before external calls.

## Mandatory contract tests (NOT RUN)
STATE-01 optimistic conflict; LEASE-01 simultaneous claims/stale fencing; RETRY-01 transient/permanent/ambiguous; IDEM-01 cross-attempt duplicate; COST-01 over-cap denial; DONE-01 agent claim without evidence; DEPLOY-02 replay/wrong artifact; DAG-01 cycles/partial blocking. Every test requires positive/negative fixtures and auditable artifacts.
