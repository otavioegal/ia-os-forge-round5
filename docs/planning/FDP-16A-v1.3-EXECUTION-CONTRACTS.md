# FDP-16A v1.3 — Execution contracts
Status: ROUND 6 — CANDIDATE FOR CODEX REVIEW. DRAFT / NOT APPROVED / NOT READY FOR BUILD / NO BUILD-00 AUTHORIZATION. No tests executed. No staging drills executed. No Founder approval inferred.
Companion normative annex to [FDP-16-v1.3-AIOX-EXECUTION-ENGINES.md](FDP-16-v1.3-AIOX-EXECUTION-ENGINES.md).
This annex is the normalization of stored enums and payloads. It replaces the v1.1 deferral that postponed normalization to a future ADR. No further ADR is required before implementation of these contracts unless a field below changes, which then requires a Change Decision.
Supersedes, as a proposal only: historical/round4/docs/planning/FDP-16A-v1.1-EXECUTION-CONTRACTS.md. The v1.1 file is retained and is not normative.

Normative sources preserved: FDP-12 Task status (QUEUED, READY, RUNNING, WAITING, RETRYING, HANDOFF, REVIEWING, BLOCKED, COMPLETED, FAILED, CANCELLED). Build and Attempt use different enums and different tables so they cannot collide with Task.

## 1. Type conventions
- Identifiers: UUID, serialized as canonical lowercase strings. Never integers.
- Timestamps: RFC 3339 UTC (`date-time`). All of them are required unless a column is explicitly nullable below.
- Money: `int64` minor units. No floats. Currency is a separate `currency` string, default `USD`, fixed for the MVP ledger.
- Digests: lowercase hex SHA-256, pattern `^[0-9a-f]{64}$`.
- Versions: optimistic `version` is `int64`, starts at 1, increments by 1.
- Idempotency key material: UTF-8 strings, trimmed, with internal whitespace collapsed to a single space before hashing. Hash input is the concatenation documented in section 7, not a language-specific object hash.
- Nullability is stated per field. Omitted required fields are validation errors `422 VALIDATION`. Unknown fields are rejected.

## 2. Common record header
Every durable aggregate includes:

| Field | Type | Null | Constraint |
|---|---|---|---|
| id | uuid | no | primary key |
| organization_id | uuid | no | FK organization, RLS predicate |
| project_id | uuid | no | FK project, same organization |
| version | int64 | no | >= 1, CAS target |
| correlation_id | uuid | no | copied from the originating command |
| created_at | date-time | no | set by the database |
| updated_at | date-time | no | set by the database |

RLS and application policy both enforce `organization_id`. Application policy also enforces project membership (AUTHZ-02). RLS is not a reason to skip the application check.

Identity rule: `id` is the only primary key of each aggregate table. On the build, task, attempt, lease, checkpoint, evidence_bundle and deployment_approval tables, the names `build_id`, `task_id`, `attempt_id`, `lease_id`, `checkpoint_id`, `bundle_id` and `approval_id` are generated columns that must equal `id`. They are not a second independent key. A foreign key in another table uses that name and references `referenced_table.id`. `operation.id` is the operation row key. `operation_ref` is the business idempotency key and is not an alias of `operation.id`.

## 3. Aggregate schemas

### 3.1 Build
| Field | Type | Null | Constraint |
|---|---|---|---|
| build_id | uuid | no | same as id |
| plan_revision | string | no | matches an existing plan |
| graph_revision | string | no | matches an existing graph |
| policy_version | string | no | matches the policy row used at StartBuild |
| budget_limit_minor | int64 | no | >= 0 |
| budget_spent_minor | int64 | no | >= 0 |
| budget_reserved_minor | int64 | no | >= 0 |
| currency | string | no | `USD` in MVP |
| status | enum | no | PLANNED, AWAITING_APPROVAL, QUEUED, RUNNING, TESTING, REVIEWING, READY_FOR_HUMAN_TEST, BLOCKED, CHANGES_REQUESTED, FAILED, CANCELLED |
| evidence_ref | uuid | yes | required once status is READY_FOR_HUMAN_TEST |
| stop_latch | bool | no | default false |

Invariant: `budget_spent_minor + budget_reserved_minor <= budget_limit_minor` except during a single transaction that is rolling back a denied reservation. A committed row must satisfy it.

### 3.2 Task
| Field | Type | Null | Constraint |
|---|---|---|---|
| task_id | uuid | no | stable across attempts |
| build_id | uuid | no | FK build |
| dependency_task_ids | uuid[] | no | may be empty; each id must exist in the same build |
| goal | string | no | 1..4000 chars, untrusted text |
| acceptance | string | no | 1..4000 chars |
| status | enum | no | exactly QUEUED, READY, RUNNING, WAITING, RETRYING, HANDOFF, REVIEWING, BLOCKED, COMPLETED, FAILED, CANCELLED |
| blocked_reason | string | yes | required when status is BLOCKED; otherwise null |
| ready_for_human_test | bool | no | not a task column. This flag exists only on Build and is derived. Writers must reject it on Task. |

`CLAIMED_DONE` is not a member of the enum. A completion claim is an event, not a status.

### 3.3 TaskAttempt
| Field | Type | Null | Constraint |
|---|---|---|---|
| attempt_id | uuid | no | |
| task_id | uuid | no | FK task |
| sequence | int32 | no | >= 1, unique per task |
| engine_id | string | no | allowlisted |
| lease_id | uuid | yes | null only before claim and after terminal |
| fencing_epoch | int64 | no | >= 0 |
| heartbeat_at | date-time | yes | null until first heartbeat |
| worktree_ref | string | yes | required while RUNNING |
| checkpoint_ref | uuid | yes | required to leave HANDOFF |
| status | enum | no | CREATED, QUEUED, PROVISIONING, RUNNING, PAUSED, SUCCEEDED, FAILED, CANCELLED, TIMED_OUT, LOST |
| terminal | bool | no | true iff status in SUCCEEDED, FAILED, CANCELLED, TIMED_OUT, LOST |

At most one non-terminal attempt per task.

### 3.4 Operation
| Field | Type | Null | Constraint |
|---|---|---|---|
| operation_ref | string | no | 1..128 chars, stable for one intent |
| task_id | uuid | no | |
| capability | string | no | catalog id |
| normalized_input_digest | sha256 | no | |
| external_receipt | string | yes | null until the provider answers |
| status | enum | no | RESERVED, DISPATCHED, SETTLED, RELEASED, DENIED, CANCELLED, RECONCILING, BLOCKED_RECONCILIATION |
| reconciliation_state | enum | no | NOT_NEEDED, REQUIRED, MATCHED, MATCHED_NO_EFFECT, AMBIGUOUS |
| estimated_minor | int64 | no | >= 0; 0 only for capabilities whose descriptor says side_effects NONE |
| settled_minor | int64 | yes | null until SETTLED; then >= 0 |

Unique index: `(project_id, task_id, operation_ref, capability, normalized_input_digest)`. `attempt_id` is not part of the key and is not a column of this table. Attempts reference operations; operations do not belong to one attempt.

### 3.5 Lease
| Field | Type | Null | Constraint |
|---|---|---|---|
| lease_id | uuid | no | |
| attempt_id | uuid | no | |
| task_id | uuid | no | |
| owner | string | no | runner id |
| epoch | int64 | no | increments by 1 on each successful acquire |
| expires_at | date-time | no | |
| heartbeat_at | date-time | no | |

A lease is valid only when `expires_at > now` and `epoch` equals the attempt's `fencing_epoch`.

### 3.6 Checkpoint
| Field | Type | Null | Constraint |
|---|---|---|---|
| checkpoint_id | uuid | no | |
| task_id | uuid | no | |
| attempt_id | uuid | no | the attempt that wrote it, which becomes terminal on handoff |
| git_ref | string | no | |
| git_ref_digest | sha256 | no | |
| graph_revision | string | no | |
| operation_ledger_watermark | string | no | last committed operation id |
| dependency_lock_digest | sha256 | no | |
| digest | sha256 | no | hash of the canonical checkpoint document |

Resume rejects the checkpoint when any stored digest does not recompute.

### 3.7 EvidenceBundle
| Field | Type | Null | Constraint |
|---|---|---|---|
| bundle_id | uuid | no | |
| task_id | uuid | no | |
| commit_hash | sha256 | no | |
| test_run_ids | string[] | no | length >= 1 to verify |
| review_id | uuid | no | reviewer actor must differ from builder |
| findings | object[] | no | may be empty; each has severity |
| artifact_hashes | sha256[] | no | |
| decision | enum | no | PASS, FAIL |

### 3.8 DeploymentApproval
| Field | Type | Null | Constraint |
|---|---|---|---|
| approval_id | uuid | no | alias of id on this table; single use |
| release_id | uuid | no | FK release |
| environment_id | uuid | no | FK forge.environments.id (FDP-12 §21). This is the environment identity, not the type. Two PRODUCTION rows are different ids. |
| environment_class | enum | no | LOCAL, DEV, TEST, STAGING, PRODUCTION. Must equal environments.type of environment_id. |
| source_git_hash | sha256 | no | |
| artifact_digest | sha256 | no | |
| graph_revision | string | no | |
| migration_set_hash | sha256 | no | |
| policy_version | string | no | |
| approver_actor_ref | string | no | human actor, not a coding engine |
| approver_scope | string | no | must name the same environment_id |
| expires_at | date-time | no | |
| consumed_at | date-time | yes | null until use; set in the same transaction as the deploy intent |
| revoked_at | date-time | yes | |

## 4. Command and event envelopes
### 4.1 CommandEnvelope (schema id `forge.command.v1`)
| Field | Type | Null | Constraint |
|---|---|---|---|
| command_id | uuid | no | idempotency of the command itself |
| command_type | string | no | one of the catalog |
| actor_ref | string | no | |
| actor_class | enum | no | human, security_operator, release_agent, coding_engine, reviewer, system |
| organization_id | uuid | no | |
| project_id | uuid | no | |
| expected_version | int64 | yes | required for mutations of an existing aggregate |
| correlation_id | uuid | no | |
| policy_version | string | no | |
| issued_at | date-time | no | |
| payload | object | no | schema depends on command_type |

### 4.2 EventEnvelope (schema id `forge.event.v1`)
| Field | Type | Null | Constraint |
|---|---|---|---|
| event_id | uuid | no | dedupe key |
| event_type | string | no | |
| aggregate_type | string | no | |
| aggregate_id | uuid | no | |
| aggregate_version | int64 | no | version after the write |
| causation_id | uuid | no | command_id or prior event_id |
| correlation_id | uuid | no | |
| policy_decision_ref | uuid | yes | required when a policy check ran |
| evidence_ref | uuid | yes | |
| occurred_at | date-time | no | |
| payload | object | no | |

State change and outbox insert commit in one database transaction. Delivery is at-least-once. Consumers dedupe on `event_id`. A version conflict aborts the transaction; no outbox row is written.

## 5. Command catalog
Payload fields are in addition to the envelope.

| Command | Actor class | Payload (type, null) | Preconditions | Committed effect | Denial |
|---|---|---|---|---|---|
| StartBuild | human or system under policy | plan_revision string no; graph_revision string no | plan approval matches revision; stop_latch false; security foundation gate id present | Build PLANNED or AWAITING_APPROVAL becomes QUEUED; event BuildQueued | 409 APPROVAL_REVISION_MISMATCH; 409 STOP_LATCH; 403 SECURITY_FOUNDATION_RED |
| DependenciesSatisfied | system | task_id uuid | all dependency tasks COMPLETED | Task QUEUED to READY | 409 DEPENDENCY_OPEN |
| ClaimTask | system | task_id uuid; owner string | status READY or RETRYING; no valid lease | creates lease epoch+1; Task to RUNNING; attempt to RUNNING | 409 LEASE_HELD; 409 ILLEGAL_TRANSITION |
| Heartbeat | system | lease_id; epoch int64 | epoch matches and lease unexpired | extends expires_at by lease_ttl | 409 FENCED |
| InvokeCapability | coding_engine via gateway | capability string; operation_ref string; input object; estimated_cost_minor int64 | grant, budget headroom, ledger not blocked, stop latch, safe mode | one transaction inserts operation RESERVED and increments reserved_minor by the estimate; no provider call inside that transaction | 402 BUDGET_EXCEEDED; 403 CAPABILITY_NOT_GRANTED; 409 STOP_LATCH; 409 RECONCILIATION_REQUIRED; 409 SAFE_MODE |
| DispatchOperation | system | operation_ref | operation is RESERVED and reservation is HELD | status becomes DISPATCHED; money columns do not change | 409 NOT_RESERVED |
| RecordReceipt | system | operation_ref; receipt string; actual_minor int64 | operation DISPATCHED or RECONCILING | settlement transaction in section 8A | 409 RECEIPT_MISMATCH; 409 OVER_ESTIMATE_BLOCKED; 402 BUDGET_EXCEEDED |
| ReleaseReservation | system | operation_ref; reason | proven no external effect | reserved_minor decreases by the full estimate; spent unchanged; operation RELEASED or CANCELLED | 409 EFFECT_NOT_DISPROVEN |
| BlockReconciliation | system | operation_ref | no receipt query is available, or the query is inconclusive | operation BLOCKED_RECONCILIATION; reservation stays HELD; redispatch forbidden | none; this is the safe stop |
| AwaitExternal | system | operation_ref | operation DISPATCHED without receipt | Task RUNNING to WAITING | 409 ILLEGAL_TRANSITION |
| ScheduleRetry | system | task_id; class enum | class is transient and attempts remain | Task to RETRYING; no new external call yet | 409 RETRY_EXHAUSTED; 409 PERMANENT_FAULT |
| BeginHandoff | system | checkpoint payload | digests verify | Task to HANDOFF; old attempt terminal; grants revoked | 409 CHECKPOINT_INVALID |
| CompleteHandoff | system | task_id | new attempt inserted; scope not expanded | Task HANDOFF to READY | 403 SCOPE_EXPANDED |
| SubmitForReview | coding_engine | task_id; claim text | attempt running | Task RUNNING to REVIEWING; event is a claim, not completion | 409 ILLEGAL_TRANSITION |
| ReviewDecision | reviewer | review_id; decision; findings | actor is not the author | may move REVIEWING to BLOCKED or leave it ready to verify | 403 REVIEWER_IS_AUTHOR; 409 HIGH_FINDING_OPEN |
| VerifyTask | reviewer or system | bundle_id | tests referenced, review pass, bundle complete | Task REVIEWING to COMPLETED | 409 EVIDENCE_MISSING; 403 DERIVED_ONLY |
| BlockTask | system or security_operator | reason string | non-terminal | Task to BLOCKED | 409 TERMINAL_STATE |
| UnblockTask | security_operator or system | reason | BLOCKED and dependencies allow | Task to READY, or QUEUED if dependencies are open | 403 NOT_OPERATOR |
| FailTask | system | reason | non-terminal | Task to FAILED | 409 TERMINAL_STATE |
| CancelTask | human or security_operator | reason | non-terminal | Task to CANCELLED; grants revoked | 403 NOT_OPERATOR; 409 TERMINAL_STATE |
| StopBuild | security_operator | build_id | authenticated operator | stop_latch true; new effects denied | 403 NOT_STOP_OPERATOR |
| ClearStop | security_operator | build_id; authorization_ref | a new authorization distinct from the stop command | stop_latch false | 403 NOT_STOP_OPERATOR |
| MergeTask | reviewer | task_id; base_hash | base unchanged, review pass, tests green | merge commit recorded | 403 SEPARATION_OF_DUTIES; 409 MERGE_CONFLICT; 409 HIGH_FINDING_OPEN |
| DeployRelease | release_agent | approval_id plus the full tuple in section 8B | exact unexpired unconsumed match on every tuple field | consumed_at set in the same transaction as the deploy intent | 403 CODING_ENGINE_CANNOT_DEPLOY; 409 APPROVAL_MISMATCH; 409 APPROVAL_EXPIRED; 409 APPROVAL_REPLAY |

## 6. Task transition matrix
Rows are the current Task status. Columns are commands. `—` means denied with `409 ILLEGAL_TRANSITION` and an audit event. Terminal states COMPLETED, FAILED and CANCELLED reject every command in this table. Read queries are allowed and are not commands.

| From \ Command | DependenciesSatisfied | ClaimTask | AwaitExternal | ScheduleRetry | BeginHandoff | CompleteHandoff | SubmitForReview | VerifyTask | BlockTask | UnblockTask | FailTask | CancelTask |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| QUEUED | READY | — | — | — | — | — | — | — | BLOCKED | — | FAILED | CANCELLED |
| READY | — | RUNNING | — | — | — | — | — | — | BLOCKED | — | FAILED | CANCELLED |
| RUNNING | — | — | WAITING | RETRYING | HANDOFF | — | REVIEWING | — | BLOCKED | — | FAILED | CANCELLED |
| WAITING | — | — | — | RETRYING | HANDOFF | — | — | — | BLOCKED | — | FAILED | CANCELLED |
| RETRYING | — | RUNNING | — | — | HANDOFF | — | — | — | BLOCKED | — | FAILED | CANCELLED |
| HANDOFF | — | — | — | — | — | READY | — | — | BLOCKED | — | FAILED | CANCELLED |
| REVIEWING | — | — | — | RETRYING | — | — | — | COMPLETED | BLOCKED | — | FAILED | CANCELLED |
| BLOCKED | — | — | — | — | — | — | — | — | — | READY or QUEUED | FAILED | CANCELLED |
| COMPLETED | — | — | — | — | — | — | — | — | — | — | — | — |
| FAILED | — | — | — | — | — | — | — | — | — | — | — | — |
| CANCELLED | — | — | — | — | — | — | — | — | — | — | — | — |

Additional denials that apply even when the cell is not `—`:
- VerifyTask from REVIEWING without a bundle stays REVIEWING and returns 409 EVIDENCE_MISSING. It does not go to COMPLETED.
- ScheduleRetry when the retry budget is exhausted goes to BLOCKED with reason RETRY_EXHAUSTED instead of RETRYING.
- ScheduleRetry for a permanent policy fault goes to BLOCKED with that policy reason and is not retried.
- UnblockTask from BLOCKED goes to QUEUED when any dependency is not COMPLETED, otherwise READY.
- ClaimTask from RETRYING also requires a reconciled ledger (section 8).

Heartbeat, InvokeCapability, RecordReceipt, StopBuild and DeployRelease do not by themselves change Task status, except InvokeCapability may move RUNNING to WAITING through AwaitExternal when the provider is asynchronous.

## 7. Attempt and Build transitions
These matrices use the same denial rule as Task: a cell with `—` is `409 ILLEGAL_TRANSITION` and an audit event. Terminal states do not reopen.

### 7.1 Attempt
Watchdog may set TIMED_OUT or LOST only from PROVISIONING, RUNNING or PAUSED. CREATED and QUEUED are not executing. The watchdog command on those two states returns `409 NOT_EXECUTING` and does not change the row. Cancel is the way out of CREATED or QUEUED.

| From \ Command | Enqueue | Provision | Start | Pause | Resume | Succeed | Fail | Cancel | WatchdogExpire |
|---|---|---|---|---|---|---|---|---|---|
| CREATED | QUEUED | — | — | — | — | — | FAILED | CANCELLED | — |
| QUEUED | — | PROVISIONING | — | — | — | — | FAILED | CANCELLED | — |
| PROVISIONING | — | — | RUNNING | — | — | — | FAILED | CANCELLED | TIMED_OUT or LOST |
| RUNNING | — | — | — | PAUSED | — | SUCCEEDED | FAILED | CANCELLED | TIMED_OUT or LOST |
| PAUSED | — | — | — | — | RUNNING | — | FAILED | CANCELLED | TIMED_OUT or LOST |
| SUCCEEDED | — | — | — | — | — | — | — | — | — |
| FAILED | — | — | — | — | — | — | — | — | — |
| CANCELLED | — | — | — | — | — | — | — | — | — |
| TIMED_OUT | — | — | — | — | — | — | — | — | — |
| LOST | — | — | — | — | — | — | — | — | — |

### 7.2 Build
`blocked_from` is a nullable build status written only when entering BLOCKED, and cleared by Unblock. Unblock returns to `blocked_from`. If `blocked_from` is null, Unblock is denied. DeriveRhft is a system command, never a coding-engine command, and it runs only when the F-039 predicate over the FDP-20 required set is true. READY_FOR_HUMAN_TEST, FAILED and CANCELLED do not transition to a production state in this contract.

| From \ Command | SubmitForApproval | ApprovePlan | StartBuild | MarkTesting | MarkReviewing | DeriveRhft | RequestChanges | Block | Unblock | Fail | Cancel |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PLANNED | AWAITING_APPROVAL | — | — | — | — | — | — | BLOCKED | — | FAILED | CANCELLED |
| AWAITING_APPROVAL | — | QUEUED | — | — | — | — | CHANGES_REQUESTED | BLOCKED | — | FAILED | CANCELLED |
| CHANGES_REQUESTED | AWAITING_APPROVAL | — | — | — | — | — | — | BLOCKED | — | FAILED | CANCELLED |
| QUEUED | — | — | RUNNING | — | — | — | — | BLOCKED | — | FAILED | CANCELLED |
| RUNNING | — | — | — | TESTING | — | — | CHANGES_REQUESTED | BLOCKED | — | FAILED | CANCELLED |
| TESTING | — | — | — | — | REVIEWING | — | CHANGES_REQUESTED | BLOCKED | — | FAILED | CANCELLED |
| REVIEWING | — | — | — | — | — | READY_FOR_HUMAN_TEST | CHANGES_REQUESTED | BLOCKED | — | FAILED | CANCELLED |
| BLOCKED | — | — | — | — | — | — | — | — | value of blocked_from | FAILED | CANCELLED |
| READY_FOR_HUMAN_TEST | — | — | — | — | — | — | — | — | — | — | — |
| FAILED | — | — | — | — | — | — | — | — | — | — | — |
| CANCELLED | — | — | — | — | — | — | — | — | — | — | — |

## 8. Retry, idempotency, lease and fencing
Configuration id `forge.retry.v1`. These numbers are planning defaults so an implementer can code without waiting for a staging sample. They are not measured SLOs, not RPO/RTO, and not proof of performance. Changing them is a configuration revision, not a silent edit.

| Parameter | Value | Meaning |
|---|---|---|
| max_attempts | 5 | includes the first try |
| base_delay_ms | 250 | |
| multiplier | 2 | |
| cap_delay_ms | 30000 | |
| jitter | full | sleep = random integer in `[0, min(cap, base * 2^(n-1))]` milliseconds |
| lease_ttl_ms | 30000 | |
| heartbeat_interval_ms | 10000 | |
| transient classes | TIMEOUT, NETWORK_RESET, HTTP_429, HTTP_503, LEASE_LOST_AFTER_NO_EFFECT | eligible for ScheduleRetry |
| permanent classes | POLICY_DENY, AUTH_DENY, VALIDATION, BUDGET_EXCEEDED, UNSUPPORTED_CAPABILITY | BlockTask, no retry |
| ambiguous classes | TIMEOUT_AFTER_DISPATCH, UNKNOWN_RECEIPT | Task to WAITING, reconciliation_state AMBIGUOUS, no new call |

Exhaustion after max_attempts sets BLOCKED / RETRY_EXHAUSTED and does not call the provider again.

Idempotency digest input, UTF-8, fields separated by newline: `project_id`, `task_id`, `operation_ref`, `capability`, canonical JSON of normalized input with sorted keys. The digest is stored. A second attempt does not dispatch when the existing operation is SETTLED, RELEASED, DISPATCHED, RECONCILING or BLOCKED_RECONCILIATION. A new business intent must use a new operation_ref. The gateway rejects a reused operation_ref whose digest differs (`409 OPERATION_REF_REUSED`). Re-arming the same operation_ref is allowed only when status is RELEASED and reconciliation_state is MATCHED_NO_EFFECT, and that re-arm is a new reservation transaction, not a second spent.

Lease acquire is a single transaction: lock the task row, check no valid lease, insert lease, increment epoch, set attempt RUNNING. The loser receives 409 LEASE_HELD. A writer whose epoch does not match receives 409 FENCED and the write is aborted. The watchdog is the only actor that may expire a lease, and only from attempt states PROVISIONING, RUNNING or PAUSED (section 7.1). It sets the attempt TIMED_OUT or LOST, revokes grants, and moves a RUNNING task to WAITING with reason RECONCILIATION_REQUIRED if an operation is DISPATCHED, RECONCILING or BLOCKED_RECONCILIATION, otherwise to RETRYING if attempts remain.

## 8A. Budget reservation, settlement and release
This section is the only accounting protocol. `spent_minor + reserved_minor <= budget_limit_minor` is a committed-row invariant. `reserved_minor` equals the sum of HELD reservation rows for that build. `spent_minor` increases only inside a settlement transaction. One operation_ref has at most one settlement.

Reservation row fields: `reservation_id` uuid PK, `operation_id` uuid FK, `estimated_minor` int64, `settled_minor` int64 null, `status` HELD or SETTLED or RELEASED.

| Step | Transaction contents | Money after commit | Forbidden |
|---|---|---|---|
| Deny before reserve | no operation row, or a DENIED row with no reservation; audit `budget.denied` | unchanged | do not increment reserved |
| Reserve | lock the build row; insert operation RESERVED; insert reservation HELD; `reserved += estimated` | spent unchanged; reserved includes this estimate | do not call the provider in this transaction |
| Concurrent second reserve of the same key | unique index rejects; no second reservation | unchanged by the loser | do not add the estimate twice |
| Dispatch | operation RESERVED to DISPATCHED | unchanged | do not change spent or reserved |
| Crash after reserve, before dispatch | operation still RESERVED, no provider call observed | reservation still HELD | do not reserve again; either dispatch the same row or ReleaseReservation |
| Settle when actual <= estimate | operation SETTLED; reservation SETTLED; `settled_minor = actual`; `spent += actual`; `reserved -= estimate` | the unused estimate-actual is released, not spent | do not leave the remainder reserved |
| Settle when actual > estimate and `spent + reserved - estimate + actual <= limit` | same settlement shape, using actual | spent grows by actual, reserved drops by the whole estimate | do not settle only the estimate and ignore the difference |
| actual > estimate and the inequality fails | operation stays RECONCILING; reservation stays HELD; audit `budget.over_estimate` | unchanged | do not raise spent over the limit and do not call the provider again |
| Provider failure or cancel with a proof of no effect | operation RELEASED or CANCELLED; reservation RELEASED; `reserved -= estimate` | spent unchanged | do not keep the reservation |
| Timeout after dispatch | operation RECONCILING; reservation stays HELD | unchanged until settlement or release | do not release before no-effect is proven; do not redispatch |

There is no committed path that spends money without a SETTLED operation, holds a reservation after SETTLED or RELEASED, or settles the same operation_ref twice.

## 8B. Deployment tuple
At the moment of the side effect, Release.Decide compares the request to the approval with exact equality of every field below. The first mismatch returns `409 APPROVAL_MISMATCH` with `mismatch_field` set to that field name, and does not set `consumed_at`.

Compared fields, in this order: `release_id`, `environment_id`, `environment_class`, `source_git_hash`, `artifact_digest`, `graph_revision`, `migration_set_hash`, `policy_version`, `approver_actor_ref`, `approver_scope`.

`environment_id` is the row id from `forge.environments` (FDP-12 §21, lines 422–440). `environment_class` is that row's `type` (FDP-12 §22, lines 444–452). An approval for PRODUCTION environment A does not authorize PRODUCTION environment B. Expiration and replay remain separate denials and are tested by DEPLOY-03. Each other field has its own negative oracle DEPLOY-04 through DEPLOY-11.

## 8C. Provider without a receipt query
Adapter descriptor field `receipt_query` is `SUPPORTED` or `ABSENT`. It is not implied.

If `receipt_query` is SUPPORTED, reconciliation calls that query once. A receipt follows section 8A settlement. A definitive no-effect follows ReleaseReservation. An inconclusive answer follows BlockReconciliation.

If `receipt_query` is ABSENT, the operation goes to BLOCKED_RECONCILIATION immediately after an ambiguous dispatch. The reservation stays HELD. Redispatch is forbidden. A human security_operator may later record either a proven receipt (then settlement) or a proven no-effect (then release). The human record stores the evidence ref. Guessing either outcome is a contract violation.

## 9. Internal API contracts
Transport for MVP: HTTPS JSON inside the trusted network, function names below. This is the contract between components. It is not a public browser API.

| Operation | Caller | Callee | Success | Error codes |
|---|---|---|---|---|
| ApplyCommand | any service | the single owner of that aggregate | 200 CommandResult with new version and event_id | 401, 403, 402, 409, 422 |
| TaskService.Get | Build Controller, Studio | Task Service | 200 Task | 403, 404 |
| AttemptManager.Claim | queue worker | Attempt Manager | 200 lease | 409 LEASE_HELD or FENCED |
| Gateway.Invoke | adapter | Tool Gateway | 200 receipt or INTENT id | 402, 403, 409 |
| Adapter.Invoke | Attempt Manager | engine adapter | 200 status | 422 UNSUPPORTED, 409 KILLED |
| Watchdog.Tick | scheduler | Watchdog | 200 counts | none; failures are logged and retried next tick |
| Release.Decide | Release Agent | Approval service | 200 allow | 403, 409 |

Component ownership, and the reason these calls are not a cycle of authority:
- Build Controller may call Task Service. Task Service does not call an engine and does not call Build Controller.
- Attempt Manager may call Adapter and Gateway. Adapter may call Gateway. Gateway may not call Adapter or Attempt Manager. Gateway calls Policy, Budget and the Operation Ledger only.
- Policy Service does not call engines. Engines and adapters cannot call Policy writes, Budget limit writes, or DeploymentApproval inserts.
- Reviewer service reads diffs. It does not share an actor_ref with the coding engine. Merge service accepts only reviewer or release_agent as specified per command.
- Coding engine actor class cannot call DeployRelease (F-030). Release Agent cannot write task source.
- STUDIO reads projections. It is not on the authorization path. A downed STUDIO cannot weaken the gateway (F-021).

There is no allowed call path by which an engine grants itself a capability, approves its own review, or deploys.

## 10. Recovery after partial interruption
These sequences are requirements for implementation and for tests RETRY-01 and IDEM-01. They are not evidence that a drill has run.

| Failure point | Durable state that must be observed | Next action | Forbidden action |
|---|---|---|---|
| Crash before the command transaction commits | no new version, no outbox row | client may retry the same command_id | do not invent a second effect |
| Crash after budget reservation commits and before provider call | operation RESERVED, reservation HELD, provider call count unchanged | dispatch that same row or ReleaseReservation | do not create a second reservation |
| Crash after provider dispatch and before receipt | operation DISPATCHED or RECONCILING, reservation still HELD | section 8C; do not assume a receipt API exists | do not dispatch again and do not release on a guess |
| Heartbeat stops | lease expires | watchdog fences only an executing attempt, revokes grants, then section 8 routing | do not keep the task RUNNING and do not expire CREATED or QUEUED |
| Process killed during HANDOFF | checkpoint transaction either committed or not; HANDOFF-01 is the oracle | if committed, CompleteHandoff; if not, the previous attempt remains the only non-terminal one | do not leave two non-terminal attempts |
| Outbox published twice | same event_id | consumer dedupes | do not apply the domain write twice |

## 12. Contract tests
All NOT RUN. The pass/fail text is only in the v1.3 traceability matrix. Ledger cases are LEDGER-01 through LEDGER-05. Deployment component cases are DEPLOY-02 through DEPLOY-11. Handoff recovery is HANDOFF-01.
