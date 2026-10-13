# IA OS Forge — FDP-16 v1.3 — AIOX / Execution Engines
Status: ROUND 6 — CANDIDATE FOR CODEX REVIEW. DRAFT / NOT APPROVED / NOT READY FOR BUILD / NO BUILD-00 AUTHORIZATION. No tests executed. No staging drills executed. No Founder approval inferred.
Supersedes as proposed baseline: historical/round5 FDP-16 v1.2. Does not modify source extracts FDP-06, FDP-10, FDP-12 or FDP-13.

## 1. Boundaries
Forge owns the Project Graph, Build, Task, TaskAttempt, Operation ledger, policy decisions, budget ledger and evidence. Synkra AIOX is the preferred engineering framework (FDP-06 §15). It is not the only entry and not a single point of failure (FDP-06 §17). When AIOX health is not ok, Attempt Manager uses orchestrator_path FORGE_DIRECT for capabilities whose side_effects are NONE or INTERNAL, and still writes Forge state. Deploy and external side effects stay denied on that path. Replacing the preference for AIOX requires a Change Decision. Using the fallback does not. Claude Code and Codex are the MVP engines. Grok and OpenRouter stay prepared P1 and are not on the MVP allowlist until a grant says so. The Execution Router chooses an engine, the Model Router chooses a model, and the Tool Gateway authorizes a capability. The model is not the policy enforcement point.

## 2. Canonical aggregates
Field-level schemas, nullability and unique keys are normative in FDP-16A v1.3, not restated as a competing list here.
Task status is exactly the FDP-12 enum: QUEUED, READY, RUNNING, WAITING, RETRYING, HANDOFF, REVIEWING, BLOCKED, COMPLETED, FAILED, CANCELLED.
Build and Attempt enums are those in FDP-16A sections 3.1 and 3.3. They are different columns in different tables.

## 3. State ownership
Build Controller alone transitions Build. Task Service alone transitions Task. Attempt Manager alone transitions Attempt. The Tool Gateway alone writes Operation and budget reservation rows. Transitions are the matrices in FDP-16A sections 6 and 7. The v1.1 sentence that postponed enum normalization to an ADR before code stays withdrawn. FDP-16A v1.3 is that normalization, plus the ledger and deployment tuple added in this round.

CLAIMED_DONE is an event payload, never a stored status. COMPLETED is reached only by VerifyTask from REVIEWING. READY_FOR_HUMAN_TEST is a derived Build flag specified in F-039.

## 4. Scheduling
The plan compiler rejects cycles and missing dependencies (DAG-01, story F-035). A blocked task stops its dependents only. The queue, lease, heartbeat and fencing rules are FDP-16A section 8 and story F-032. Two writers cannot hold a valid lease on the same task.

## 5. Idempotency and handoff
Normative key and crash sequences are FDP-16A sections 7, 8, 8A, 8C and 10, stories F-015 and F-034. attempt_id is not part of the operation key. Handoff creates a new attempt and revokes the old grant (F-016, HANDOFF-01, ENG-02).

## 6. Adapters, context, review, merge
Adapters implement the common methods describe, health, invoke and cancel, and engine adapters declare start_task, resume_task, pause_task, cancel_task, get_status, capture_checkpoint, get_artifacts, get_diff and get_test_results as supported or unsupported (F-012). Silent emulation is forbidden. FDP-15 is still pending approval. Context packs exclude other projects and resolved secrets (F-036). Reviewer and author are different actors (F-017). Merge conflicts pause (F-037). Autonomous, Guided and Restricted modes do not bypass these gates.

## 7. Security observability contract
Required audit event names, so tests have something to look for: authz.allowed, authz.denied, budget.denied, budget.reserved, budget.settled, budget.released, budget.over_estimate, budget.reconciliation_blocked, operation.dispatched, lease.fenced, stop.latched, approval.consumed, injection.ignored.
Required span names: forge.api.request, forge.gateway.invoke, forge.adapter.invoke, forge.watchdog.tick.
Spans must not contain secret values (SEC-01). A dashboard is not on this path (F-021).

## 8. Privilege and dependency direction
The allowed direction is: human policy decision, then Policy Service, then Gateway, then Adapter. The reverse write is forbidden. Concrete denials are in FDP-16A section 9 and stories F-002, F-015, F-026, F-027, F-029 and F-030. No circular authority is introduced by the orchestrator preference for AIOX: AIOX calls the gateway and does not own policy.

## 9. Acceptance pointers
Behavioral acceptance is the story register FDP-19A v1.3. Oracles are only in the traceability matrix v1.3. This document does not carry a second copy of pass/fail text.

## 10. Gate
Pending independent review. No code, build or deploy is authorized by publishing this draft.
