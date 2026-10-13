#!/usr/bin/env python3
"""Generate IA OS Forge Round 5 v1.2 planning documents. Does not execute product code."""
from pathlib import Path
import json

ROOT = Path("/workspace/artifacts/ia-os-forge-round5")
PLAN = ROOT / "docs/planning"
REV = ROOT / "docs/reviews"

STATUS = (
    "Status: ROUND 5 — CANDIDATE FOR INDEPENDENT REVIEW. "
    "DRAFT / NOT APPROVED / NOT READY FOR BUILD / NO BUILD-00 AUTHORIZATION. "
    "No tests executed. No staging drills executed. No Founder approval inferred."
)

TASK_STATES = [
    "QUEUED", "READY", "RUNNING", "WAITING", "RETRYING", "HANDOFF",
    "REVIEWING", "BLOCKED", "COMPLETED", "FAILED", "CANCELLED",
]

# Primary story ownership of FDP-13 P0 IDs is preserved from the v1.1 matrix.
P0 = [
    ("AUTH-01", "login required", "F-002"),
    ("AUTHZ-01", "org isolation", "F-001"),
    ("AUTHZ-02", "project isolation", "F-002"),
    ("RLS-01", "cross-tenant deny", "F-001"),
    ("FS-01", "path traversal blocked", "F-007"),
    ("FS-02", "symlink escape blocked", "F-007"),
    ("TERM-01", "destructive command blocked", "F-007"),
    ("SEC-01", "secrets not logged", "F-006"),
    ("SEC-02", "secrets not committed", "F-006"),
    ("ENG-01", "engine permission boundary", "F-027"),
    ("ENG-02", "handoff keeps same scope", "F-027"),
    ("PREVIEW-01", "no privileged IPC", "F-028"),
    ("DEPLOY-01", "prod requires approval", "F-030"),
    ("DEPLOY-02", "wrong release approval rejected", "F-029"),
    ("AUDIT-01", "event cannot be normally altered", "F-031"),
    ("COST-01", "hard budget blocks spend", "F-015"),
    ("STOP-01", "emergency stop halts new work", "F-026"),
]


def story(**kwargs):
    return kwargs


STORIES = [
story(id="F-001", pri="P0", title="Organization and row isolation", owner="Data", sprint="S01",
      deps="none (foundation)", tests=["RLS-01", "AUTHZ-01"], cls="L",
      why="Touches every tenant table and both RLS and API policy; size is large relative to a single endpoint.",
      reqs=[
          "Every durable table that stores tenant data has organization_id uuid NOT NULL and, where the aggregate is project-scoped, project_id uuid NOT NULL.",
          "Supabase RLS denies SELECT/INSERT/UPDATE/DELETE when the JWT organization claim differs from organization_id.",
          "Application policy repeats the same denial even if a query is executed with a privileged migration role by mistake in request paths; request paths use the scoped role only.",
          "AUTHZ-01 is owned by this story: a caller authenticated in organization A is allowed to read A and is denied organization B.",
      ],
      dor=[
          "Fixture orgs org_a and org_b exist only as synthetic rows, with user_a member of org_a and not of org_b.",
          "Table list for RLS is enumerated (project, build, task, task_attempt, operation, audit_event, vault_ref).",
          "Named person remains PENDING HUMAN ASSIGNMENT.",
      ],
      pos="With user_a token, GET /v1/orgs/org_a/projects returns 200 and only rows whose organization_id is org_a. The response body, OpenTelemetry span forge.api.request, and audit event authz.allowed contain no org_b identifier.",
      neg="With the same user_a token, GET /v1/orgs/org_b/projects, a body that sets organization_id=org_b, and a filter project_id belonging to org_b each return 403 AUTHZ_FOREIGN_ORG. Zero data rows are returned. An audit_event authz.denied with reason foreign_org is appended. FAIL if status is 200, if any org_b column value appears, or if the error includes another tenant's row count.",
      evidence="RLS policy SQL hash, HTTP transcript for the three negative shapes, audit_event id, test-run id. Status of tests: NOT RUN.",
      gate="SECURITY FOUNDATION. Side-effecting engines stay disabled until this gate is green."),
story(id="F-002", pri="P0", title="Session, project membership and capability grants", owner="Security", sprint="S01",
      deps="F-001", tests=["AUTH-01", "AUTHZ-02", "CAP-01"], cls="L",
      why="Authn, same-org project denial and capability grants are three different checks; bundling them is the security foundation for every later command.",
      reqs=[
          "AUTH-01: routes other than the documented health probe reject a missing or invalid session with 401 AUTH_REQUIRED and write no domain row.",
          "AUTHZ-02: a member of org_a who is not a member of project_a2 inside that same org receives 403 AUTHZ_PROJECT.",
          "CAP-01: InvokeCapability is denied unless an unexpired grant row names that capability for that project and actor.",
          "Destructive shell blocking remains owned by F-007 (TERM-01). This story must not be closed on TERM-01.",
      ],
      dor=["Synthetic users user_member and user_stranger share org_a; only user_member is on project_p1.", "Capability catalog version is referenced.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="user_member with a valid session reads project_p1 (200) and invokes an allowlisted read-only capability git.status inside that project, producing audit authz.allowed.",
      neg="(1) no Authorization header on POST /v1/commands returns 401 and no command row. (2) user_stranger on project_p1 returns 403 AUTHZ_PROJECT. (3) user_member invoking capability deploy.release returns 403 CAPABILITY_NOT_GRANTED before any adapter call. FAIL if any of the three requests is 2xx.",
      evidence="Three HTTP transcripts, zero adapter invocations in the negative deploy case, audit ids. NOT RUN.",
      gate="SECURITY FOUNDATION."),
story(id="F-003", pri="P1", title="Versioned Project Graph", owner="Backend", sprint="S02",
      deps="F-001", tests=["GRAPH-01"], cls="L",
      why="Nodes, edges, revision and impact query are a new aggregate with isolation constraints, larger than a single CRUD screen.",
      reqs=[
          "Node and edge rows carry organization_id, project_id, graph_revision and stable node_id.",
          "An edge whose endpoints belong to different projects is rejected.",
          "Impact query for a node returns the same set for the same revision across two reads.",
          "This is the product graph, not the Task DAG. Cycle rejection of task dependencies is F-035, not this story.",
      ],
      dor=["Fixture graph co_graph_v1 with screens, flow and one external-looking node kept inside the same project.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="Insert node Screen.Checkout and edge Flow.Checkout -> Screen.Checkout under project_p1. GET impact for Flow.Checkout at that graph_revision returns Screen.Checkout exactly once.",
      neg="POST an edge from project_p1 node to a node in project_p2 returns 422 GRAPH_CROSS_PROJECT and inserts nothing. A second impact read at the same revision does not gain or lose nodes. FAIL on cross-project success or unstable ordering of the id set.",
      evidence="graph_revision, query result hash, denied request transcript. NOT RUN.",
      gate="SPRINT-02 UX/security review. Not a substitute for SECURITY FOUNDATION."),
story(id="F-004", pri="P1", title="Task and TaskAttempt persistence", owner="Backend", sprint="S01 skeleton, S02 complete",
      deps="F-001", tests=["STATE-01"], cls="L",
      why="Two aggregates, two enums and optimistic concurrency; the S01 slice is schema-only and S02 completes transitions.",
      reqs=[
          "task.status stores exactly the FDP-12 set: QUEUED READY RUNNING WAITING RETRYING HANDOFF REVIEWING BLOCKED COMPLETED FAILED CANCELLED. No extra value, including CLAIMED_DONE, is accepted.",
          "task_attempt.status uses a separate enum: CREATED QUEUED PROVISIONING RUNNING PAUSED SUCCEEDED FAILED CANCELLED TIMED_OUT LOST.",
          "Handoff inserts a new attempt row and does not insert a new task row.",
          "STATE-01: an update with a stale expected_version returns 409 VERSION_CONFLICT and leaves the row unchanged.",
      ],
      dor=["Migration reviewed against FDP-16A schemas.", "S01 DoD is schema plus denial of illegal enum; S02 DoD adds the transition service.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="Create one task in QUEUED and two attempts with sequence 1 and 2 sharing that task_id. Update with the current version succeeds and increments version by 1.",
      neg="Update with expected_version = current-1 returns 409 and the status column is unchanged. Inserting status CLAIMED_DONE returns 422 INVALID_ENUM. FAIL if the stale write commits.",
      evidence="Migration SQL, constraint name, conflict transcript. NOT RUN.",
      gate="S01 skeleton before leases (F-032). Full STATE-01 before SPRINT-03."),
story(id="F-005", pri="P0", title="Evidence and audit event store", owner="Backend", sprint="S01",
      deps="F-001", tests=["AUDIT-01"], cls="M",
      why="Schema and grants are medium; tamper-denial behavior is completed with F-031, which remains the primary AUDIT-01 owner.",
      reqs=[
          "audit_event and evidence_bundle are append-only for the application role: no UPDATE or DELETE privilege.",
          "evidence_bundle references task_id, commit_hash, test_run_ids and decision, and contains no secret column.",
          "This story creates the store. F-031 proves a normal actor cannot alter a stored event.",
      ],
      dor=["Role matrix app_writer vs auditor_reader written down.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="app_writer inserts one audit_event and can select it back inside the same organization. The row has organization_id and correlation_id.",
      neg="app_writer UPDATE or DELETE of that audit_event fails with a database privilege error. No replacement row is written by the failed statement. FAIL if the original payload bytes change.",
      evidence="Grant dump, failed SQL state, original payload hash. NOT RUN. Primary closure of AUDIT-01 remains F-031.",
      gate="SECURITY FOUNDATION together with F-031."),
story(id="F-006", pri="P0", title="Vault references, redaction and secret-free git", owner="Security", sprint="S01",
      deps="F-002", tests=["SEC-01", "SEC-02", "VAULT-01"], cls="L",
      why="Three surfaces (logs, git, vault ACL) must each be tested with a canary; this is not a logging configuration note.",
      reqs=[
          "SEC-01 is owned here. A canary string CANARY_SECRET_FORGE_9f3a placed in a tool result must be absent from application logs, trace attributes, STUDIO payloads and audit metadata.",
          "SEC-02: the same canary committed in a worktree is rejected by the secret scan, and git history of the fixture repo does not contain it after the rejection.",
          "VAULT-01: a grant for project_p1 cannot read a vault ref stored for project_p2.",
          "Prompt records store vault:// refs, never the resolved secret.",
      ],
      dor=["Canary value fixed as above and kept only in the test fixture, not in this planning repo.", "Log sinks under test are enumerated: stdout JSON, OTEL span, audit_event.meta.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="A permitted command runs with vault ref vault://org_a/p1/db and the redacted log line shows the ref plus the token [REDACTED]. The canary is not required on the positive path.",
      neg="Fixture emits CANARY_SECRET_FORGE_9f3a. Test greps the three sinks and FAILs if the substring appears. A second case writes the canary into a staged file and the pre-commit/scan step exits non-zero with the file left unstaged. A third case, user of p1 reading vault ref of p2, returns 403 VAULT_SCOPE. FAIL if any case passes through.",
      evidence="Scan report hash, grep transcript showing zero matches, vault 403 body. NOT RUN.",
      gate="SECURITY FOUNDATION."),
story(id="F-007", pri="P0", title="Project-root sandbox and command allowlist", owner="Desktop", sprint="S01",
      deps="F-002", tests=["FS-01", "FS-02", "TERM-01"], cls="L",
      why="Path canonicalization, symlink policy and process allowlist are separate mechanisms and the primary home of the three FDP-13 filesystem/terminal tests.",
      reqs=[
          "FS-01: an in-root relative path is readable; a ../ sequence or an absolute path outside the project root is denied.",
          "FS-02: a symlink created inside the root that resolves outside the root is denied after canonicalization.",
          "TERM-01: command rm targeting / and any executable not on the allowlist are denied; git status with arguments confined to the root is allowed in the fixture.",
          "Preview IPC is F-028, not closed by this story.",
      ],
      dor=["Fixture root /tmp/forge-fixture/project_p1 with a sibling directory outside.", "Allowlist document versioned.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="Read of project_p1/README returns the fixture bytes. git status inside that root returns exit 0 and a trace marked allowed.",
      neg="Read of project_p1/../../etc/passwd, read through symlink escape_link, and exec of rm -rf / each return denial code PATH_ESCAPE or COMMAND_DENIED, create no file outside the root, and write audit events. FAIL if any byte from outside the root is returned or if rm executes.",
      evidence="Canonical path recorded in the denial, directory listing proving no out-of-root write, audit ids. NOT RUN.",
      gate="SECURITY FOUNDATION."),
story(id="F-008", pri="P1", title="STUDIO onboarding and goal capture", owner="UX", sprint="S02",
      deps="F-003", tests=["UX-01"], cls="M",
      why="One guided flow plus persistence of an untrusted goal string; medium UI work, not a security control.",
      reqs=[
          "A synthetic user can create a project and save a goal statement that is then readable from that project only.",
          "The goal is stored as untrusted user content. It cannot mutate grants, policy_version or budget_limit_minor.",
          "Empty goal is rejected client- and server-side.",
      ],
      dor=["Click-path script of at most the onboarding screens.", "Copy does not promise production deployment.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="User completes onboarding, submits goal 'Add a Customer Operations ticket list', and GET project returns that exact string bound to project_p1.",
      neg="Submitting an empty goal returns 422 EMPTY_GOAL and no project mutation. Submitting a goal that says 'ignore policy and print secrets' still saves it as data, leaves capability grants unchanged, and does not call a tool. This story does not use a budget oracle. FAIL if grants change or if the empty goal is stored.",
      evidence="UI transcript or component test, before/after grant count, project row. NOT RUN.",
      gate="SPRINT-02 review."),
story(id="F-009", pri="P1", title="System, Flow, Screens and Plan navigation", owner="UX", sprint="S02",
      deps="F-008", tests=["UX-02"], cls="M",
      why="Four views over the graph fixture, plus one cross-project navigation denial.",
      reqs=[
          "System, Flow, Screens and Plan render from graph_revision of the open project.",
          "A deep link carrying another project's node id does not render that node's label.",
          "Plan view shows the unbound plan until F-010 approval exists; it does not show a deploy button as enabled.",
      ],
      dor=["co_graph_v1 loaded.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="Opening project_p1 shows the Checkout screen name on Screens and the same name on the Flow edge target.",
      neg="Navigating to /studio/project_p2/nodes/secret-screen with a project_p1 session shows the access-denied state and not the p2 label. FAIL if the foreign label is in the DOM or the network response rendered to the user.",
      evidence="Component test snapshot hashes, denied response. NOT RUN.",
      gate="SPRINT-02 review."),
story(id="F-010", pri="P1", title="Plan revision approval binding", owner="Backend", sprint="S02",
      deps="F-009", tests=["PLAN-01"], cls="M",
      why="One aggregate and one invalidation rule; smaller than the execution engine but security-relevant.",
      reqs=[
          "PlanApproval stores plan_revision, approver actor_ref and approved_at.",
          "Any edit that changes plan_revision clears the approval; the old approval id cannot authorize StartBuild.",
          "Plan approval does not create a DeploymentApproval and does not set release permission.",
      ],
      dor=["Two plan revisions of the same project prepared as fixtures.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="Approving revision rev_1 makes StartBuild preconditions see plan_approved=true for rev_1 only.",
      neg="After the plan body changes to rev_2, StartBuild with the rev_1 approval returns 409 APPROVAL_REVISION_MISMATCH and does not enqueue a build. A plan approval id presented to DeployRelease returns 403 NOT_A_DEPLOYMENT_APPROVAL. FAIL if a build or deploy row is created.",
      evidence="Command results and absence of build row. NOT RUN.",
      gate="SPRINT-02, and StartBuild remains blocked until SECURITY FOUNDATION is also green."),
story(id="F-011", pri="P1", title="Execution Router capability filter", owner="Orchestration", sprint="S03",
      deps="F-002", tests=["ENG-01"], cls="L",
      why="Router is on the path of every engine call; ENG-01 primary ownership stays with F-027, this story supplies the filter the kill switch depends on.",
      reqs=[
          "Router chooses an engine only from the project allowlist and records the choice.",
          "A requested capability outside the grant is not forwarded to an adapter.",
          "The router cannot write policy or raise its own grant. Primary evidence record for ENG-01 remains F-027; this story's test is the filter case that F-027 cites.",
      ],
      dor=["Allowlist contains codex and claude_code only.", "SECURITY FOUNDATION must already be green before this sprint invokes a real engine.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="A task that requests capability git.diff and an allowlisted engine produces a route decision row and a single adapter invoke.",
      neg="A task that requests capability shell.exec while the grant only has git.diff yields no adapter call and error CAPABILITY_NOT_GRANTED. Requesting engine_id grok while Grok is not on the MVP allowlist yields ENGINE_NOT_ALLOWLISTED. FAIL if an adapter log line exists for either denial.",
      evidence="route_decision row, adapter call count = 0 on negative. NOT RUN.",
      gate="EXECUTION GATE. No side-effecting engine before SECURITY FOUNDATION."),
story(id="F-012", pri="P1", title="Codex and Claude Code adapter contracts", owner="Integration", sprint="S03",
      deps="F-011", tests=["ADAPT-01"], cls="L",
      why="Two adapters must implement the same FDP-15 surface; contract tests are the point of the story.",
      reqs=[
          "Each adapter implements describe, health, invoke, cancel, and reports start/resume/get_status/checkpoint.",
          "An unsupported capability returns UNSUPPORTED and does not shell out to a substitute tool.",
          "Adapters receive vault refs, never resolved secret strings (depends on F-006).",
      ],
      dor=["Contract harness from FDP-15 section list.", "SPIKE-02 and SPIKE-03 results, when they exist, are inputs, not waivers. Spikes are NOT RUN today.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="Health returns ok for a fake in-process adapter double. Invoke of a fixture task returns a terminal status and a checkpoint ref.",
      neg="Invoke with capability network.unbounded returns UNSUPPORTED, exit path does not open a socket, and cancel of an unknown attempt returns 404 without creating one. FAIL if the double emulates the capability.",
      evidence="Contract report per adapter id. NOT RUN.",
      gate="EXECUTION GATE."),
story(id="F-013", pri="P1", title="Synkra AIOX adapter with a scoped squad", owner="Integration", sprint="S04",
      deps="F-012", tests=["ADAPT-02"], cls="L",
      why="Preferred orchestrator is frozen; the story is the adapter boundary, not a rewrite of AIOX.",
      reqs=[
          "The AIOX adapter is the only supported orchestrator entry in the MVP.",
          "A squad attached to project_p1 cannot read project_p2 and cannot call deploy.release.",
          "Replacing AIOX is a Change Decision, out of scope here.",
      ],
      dor=["Adapter capability list reviewed against FDP-15.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="A synthetic squad run on project_p1 emits task attempts only for p1 and returns control at a checkpoint.",
      neg="The same squad invoking deploy.release or a p2 task id receives CAPABILITY_NOT_GRANTED or AUTHZ_PROJECT and produces no deployment row. FAIL if a release row appears.",
      evidence="Attempt rows scoped to p1, denial transcript. NOT RUN.",
      gate="REVIEW + TEST READINESS."),
story(id="F-014", pri="P1", title="Model router with deny-by-default", owner="Orchestration", sprint="S03 stub, S04 full",
      deps="F-011", tests=["ROUTE-01"], cls="M",
      why="S03 needs only a deny-by-default stub so routing cannot be an open proxy; S04 may add ranked selection.",
      reqs=[
          "S03: if no explicit model grant exists, the router selects nothing and returns MODEL_DENIED.",
          "S04: a granted model id is recorded on the attempt with policy_version.",
          "The router does not expand the tool capability set of the attempt.",
      ],
      dor=["Model grant fixture lists one allowed id.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="S04 path: granted model fixture-model-a is stored on the attempt and the audit event route.model.allowed.",
      neg="S03 path with an empty grant: no model id is sent to the adapter (field omitted or null) and the command returns MODEL_DENIED. Asking to add capability shell.exec inside the model request does not change grants. FAIL if a provider request is sent without a grant.",
      evidence="Provider call count and grant diff. NOT RUN.",
      gate="EXECUTION GATE for the stub; full router at SPRINT-04."),
story(id="F-015", pri="P0", title="Tool gateway, operation ledger and hard budget", owner="Security", sprint="S01",
      deps="F-002", tests=["COST-01", "IDEM-01", "TERM-01"], cls="XL",
      why="Reservation accounting, ledger uniqueness and gateway denial are the spend-safety core. This is the largest P0 story.",
      reqs=[
          "COST-01 is owned here, not by the dashboard. Budget fields are integers in minor units.",
          "Reservation is denied when spent_minor + reserved_minor + estimated_new_minor exceeds budget_limit_minor, and the denial happens before any external call.",
          "The operation unique key is (project_id, task_id, operation_ref, capability, normalized_input_digest) and does not include attempt_id.",
          "TERM-01 execution in the sandbox remains owned by F-007. This story additionally denies a terminal capability that the grant does not include, at the gateway, with no process spawn.",
      ],
      dor=["Fixture build with budget_limit_minor = 1000, spent = 800, reserved = 100.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="estimated_new_minor = 50 is reserved, reserved becomes 150, a stub provider is called once, and a receipt row is stored.",
      neg="estimated_new_minor = 200 is denied with 402 BUDGET_EXCEEDED, spent stays 800, reserved stays 100, and the stub provider call count stays 0. A second case repeats the same operation_ref from another attempt and does not create a second receipt. FAIL if money fields change on the denial or if two receipts exist for one ref.",
      evidence="Ledger rows, provider counter, budget columns before/after. NOT RUN.",
      gate="SECURITY FOUNDATION. F-021 must not be treated as this control."),
story(id="F-016", pri="P1", title="Checkpoint, resume and handoff", owner="Orchestration", sprint="S04",
      deps="F-004", tests=["QUEUE-01", "ENG-02"], cls="L",
      why="Crosses attempt lifecycle and privilege revocation; ENG-02 primary row stays F-027 and this story supplies the handoff fixture F-027 requires.",
      reqs=[
          "Handoff writes a checkpoint, marks attempt N terminal, revokes N's grants, and creates attempt N+1 under the same task_id.",
          "operation_ref values already in the ledger are copied by reference, not re-executed.",
          "Attempt N+1's capability set is a subset of the original grant, never a superset (ENG-02).",
      ],
      dor=["Checkpoint schema from FDP-16A.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="After a verified checkpoint, exactly two attempts exist for task_t1, the second is READY to run, and the task is HANDOFF then READY, not a second task.",
      neg="Resume with a checkpoint whose git_ref digest does not match returns 409 CHECKPOINT_INVALID and does not create an attempt. A handoff that requests an extra capability returns 403 SCOPE_EXPANDED and leaves the old grants revoked. FAIL if two non-terminal attempts exist or if the capability set grows.",
      evidence="Attempt rows, grant diff, checkpoint digest. NOT RUN.",
      gate="REVIEW + TEST READINESS."),
story(id="F-017", pri="P1", title="Independent review gate", owner="QA", sprint="S04",
      deps="F-016", tests=["MERGE-01"], cls="M",
      why="Separation of duties is a single hard rule plus finding severity handling.",
      reqs=[
          "The review actor_ref must differ from the attempt engine actor_ref and from the builder actor_ref.",
          "A High or Critical finding blocks VerifyTask.",
          "Self-approval returns 403 REVIEWER_IS_AUTHOR.",
      ],
      dor=["Two distinct fixture actors author_a and reviewer_b.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="reviewer_b records a review with zero High findings and VerifyTask is then allowed to proceed to the evidence check in F-038.",
      neg="author_a posting an approval for their own attempt returns 403 and does not set review.decision=pass. A review that contains one High finding makes VerifyTask return 409 HIGH_FINDING_OPEN. FAIL if task status becomes COMPLETED in either case.",
      evidence="Review row and denied command. NOT RUN.",
      gate="REVIEW + TEST READINESS."),
story(id="F-018", pri="P1", title="Customer Operations synthetic demonstration", owner="Product", sprint="S05",
      deps="F-009", tests=["E2E-01"], cls="L",
      why="Vertical slice across STUDIO and graph, limited to synthetic data so it stays demonstrable without production coupling.",
      reqs=[
          "The demo uses dataset co_synth_v1 only: organizations, tickets and users that are generated fixtures.",
          "The scripted path creates a goal, shows a plan and opens a ticket-list screen.",
          "No connection string to MAJU, Ethereal or ORAdv is read or required.",
      ],
      dor=["co_synth_v1 checked in as fixture data without personal data.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="The scripted path ends on a screen that lists the three fixture tickets of co_synth_v1 for project_p1.",
      neg="Pointing the demo configuration at a host named as production returns DEMO_PRODUCTION_FORBIDDEN and renders no tickets. Loading co_synth_v1 does not create a DeploymentApproval. FAIL if any ticket not in the fixture is shown or a deployment row is inserted.",
      evidence="E2E trace, ticket ids compared to fixture manifest. NOT RUN.",
      gate="PRODUCT MVP. Does not authorize production."),
story(id="F-019", pri="P1", title="CI pipeline stages", owner="QA", sprint="S05",
      deps="F-002", tests=["TEST-01"], cls="M",
      why="Pipeline wiring is medium once the individual tests exist; the story is the fail-closed orchestration of stages.",
      reqs=[
          "The pipeline defines stages static, unit, adapter-contract, rls-integration and e2e as separate jobs.",
          "A missing or skipped security job fails the pipeline.",
          "The pipeline runs only against synthetic tenants.",
      ],
      dor=["Job names reserved in the plan; the actual CI vendor file is an implementation artifact, not written in this round.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="A fixture change that touches only a unit test still executes the security job, and the pipeline record lists each stage as executed.",
      neg="A pipeline definition that sets the security job to skip is rejected by the plan checker with SECURITY_JOB_SKIPPED and is not marked green. FAIL if the aggregate status is success while any P0 job is absent.",
      evidence="Pipeline definition hash and a dry-run graph. NOT RUN. This story does not claim the jobs have executed.",
      gate="PRODUCT MVP support. Security job presence is required before READY_FOR_HUMAN_TEST."),
story(id="F-020", pri="P1", title="Immutable release and controlled rollback", owner="Release", sprint="S06",
      deps="F-030", tests=["DEPLOY-02", "PROD-05"], cls="L",
      why="Release immutability plus a rollback path; the rehearsal itself is a pre-production drill and is not claimed done.",
      reqs=[
          "A release row stores an immutable artifact_digest. Content changes create a new release_id.",
          "Rollback selects the previous release_id explicitly; it does not rebuild from a floating tag.",
          "PROD-05 evidence is a drill report. That report does not exist yet and is listed as an open pendency.",
      ],
      dor=["Digest algorithm sha256 specified.", "Drill owner PENDING HUMAN ASSIGNMENT.", "No measured RTO is stated."],
      pos="Given two fixture digests D1 then D2, the rollback command names D1 and the routing record points at D1, with audit release.rollback.",
      neg="Rollback to a digest that was never released returns 404 UNKNOWN_DIGEST and leaves routing unchanged. A coding-engine actor calling this command returns 403 NOT_RELEASE_AGENT. FAIL if routing changes on either denial.",
      evidence="Release rows and routing record. Drill evidence: NOT PRODUCED.",
      gate="RELEASE READINESS specification. Production remains blocked until a real drill passes."),
story(id="F-021", pri="P2", title="Non-blocking cost dashboard", owner="Product", sprint="S06",
      deps="F-014", tests=["COST-DASH-01"], cls="M",
      why="Read model over the ledger. Explicitly not the hard-budget control.",
      reqs=[
          "The dashboard reads spent_minor, reserved_minor and limit_minor and displays them for the caller's project.",
          "If the dashboard process is down, F-015 denial behavior is unchanged.",
          "The dashboard must not expose secret values or other organizations' totals.",
      ],
      dor=["Copy in the UI states that the gateway, not the chart, enforces the limit.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="For the F-015 fixture (spent 800, reserved 100, limit 1000) the view shows those three integers.",
      neg="With the dashboard endpoint forced to 500, a gateway reservation of 200 minor units still returns 402 BUDGET_EXCEEDED. A user of org_a requesting org_b totals receives 403 and not a number. FAIL if the gateway allows the spend because the view failed, or if a foreign total is returned.",
      evidence="Screenshot or JSON of the view, plus the gateway transcript taken while the view is failing. NOT RUN.",
      gate="Not part of SECURITY FOUNDATION. Cannot satisfy COST-01."),
story(id="F-022", pri="P2", title="Multi-engine evaluation baseline", owner="QA", sprint="S05",
      deps="F-019", tests=["EVAL-01"], cls="M",
      why="Comparison harness is P2 and must not gate security. Scoring thresholds are not invented.",
      reqs=[
          "The same fixture task is offered to Codex and Claude Code adapters.",
          "Scores are stored as evidence. They do not auto-merge or auto-complete a task.",
          "No numeric quality bar is set in this plan. Adding one requires a measured sample and a human decision.",
      ],
      dor=["One frozen fixture task description.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="Both adapters return a result artifact for the fixture and two score rows exist, linked to attempt ids.",
      neg="A score row cannot be posted by the same actor that produced the attempt (403 EVAL_SELF_SCORE). Missing one engine does not mark the task COMPLETED. FAIL if a task flips to COMPLETED because a score was high.",
      evidence="Score rows and unchanged task status. NOT RUN.",
      gate="P2. Not a release blocker."),
story(id="F-023", pri="P2", title="Scoped local bridge", owner="Desktop", sprint="S06 optional",
      deps="F-007", tests=["FS-02"], cls="M",
      why="Optional local access path. It must not weaken the sandbox already required by F-007.",
      reqs=[
          "The bridge token is bound to one project root and one device identity.",
          "Paths are still canonicalized by the F-007 rules.",
          "The bridge is not required for the Customer Operations demo.",
      ],
      dor=["Explicit decision that the story is P2 and can slip without reopening P0.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="A bridge client reads a file inside its bound root and the audit records that device id.",
      neg="The same token used against a second project root or via a symlink outside the root returns PATH_ESCAPE. FAIL if a file outside the root is read. FS-02 remains owned and fully specified by F-007; this story reuses that oracle on the bridge entrypoint.",
      evidence="Bridge audit and denial. NOT RUN.",
      gate="P2 optional. Not in the MVP critical path."),
story(id="F-024", pri="P2", title="Optional Google, n8n and Supabase adapters", owner="Integration", sprint="S06 optional",
      deps="F-015", tests=["ADAPT-03"], cls="L",
      why="Three optional providers. None is on the frozen critical path; each must still honor the gateway.",
      reqs=[
          "Each adapter is disabled unless a project grant names it.",
          "Credentials are vault refs. A committed service-account JSON fails SEC-02, owned by F-006.",
          "n8n remains part of the frozen stack as a component, but a customer workflow adapter beyond the MVP demo is optional.",
      ],
      dor=["MVP acceptance does not list these adapters.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="With a grant, the Supabase adapter describe() returns capabilities and does not echo secrets.",
      neg="Without a grant, invoke returns CAPABILITY_NOT_GRANTED and makes no outbound call. A fixture config file containing a private_key field is rejected by secret scan. FAIL if an outbound call is counted.",
      evidence="Call counter and scan result. NOT RUN.",
      gate="P2. Absence does not block SECURITY FOUNDATION or the demo."),
story(id="F-025", pri="P3", title="Expanded managed cloud service", owner="Product", sprint="Not scheduled",
      deps="MVP complete plus Founder Change Decision", tests=["PERF-01"], cls="XL",
      why="Explicitly deferred. No implementation slice is authorized by this backlog entry.",
      reqs=[
          "No work starts without a separate Change Decision that states scope, data residency and a new budget.",
          "PERF-01 has no numeric target in this plan. Inventing a latency SLO here is forbidden.",
          "The frozen MVP stack is not replaced by Kubernetes, Kafka, Temporal, Redis or Neo4j under this story.",
      ],
      dor=["Change Decision id: absent.", "This story is not Ready."],
      pos="Not applicable until a Change Decision exists. There is no positive implementation acceptance in Round 5.",
      neg="A pull request that adds a Kubernetes manifest or claims PERF-01 passed is out of policy and must be rejected in review. FAIL for planning purposes if the sprint plan schedules this story.",
      evidence="None expected. NOT RUN. Not a hidden MVP requirement.",
      gate="Deferred. Founder decision required before any scheduling."),
story(id="F-026", pri="P0", title="Emergency stop and safe mode", owner="Security", sprint="S01",
      deps="F-002", tests=["STOP-01", "SAFE-01"], cls="M",
      why="Two latches with a small state machine, on the critical path of every later side effect.",
      reqs=[
          "STOP-01: an authorized operator sets a stop latch. New InvokeCapability and StartBuild calls are denied while it is set.",
          "An engine saying 'resume' in text does not clear the latch. Only a distinct operator command with a fresh authorization does.",
          "SAFE-01: while safe mode is on, read-only capabilities may run and any capability marked side_effect=true is denied.",
      ],
      dor=["Operator role defined as distinct from coding_engine.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="After StopBuild by role security_operator, a following read-only status command still returns the latch state stopped.",
      neg="InvokeCapability for a side-effect capability while stopped returns 409 STOP_LATCH and the provider counter stays 0. A command whose actor is coding_engine and whose text asks to clear the latch returns 403 NOT_STOP_OPERATOR and the latch remains set. FAIL if a provider call happens or the latch flips.",
      evidence="Latch row before/after, provider counter. NOT RUN.",
      gate="SECURITY FOUNDATION."),
story(id="F-027", pri="P0", title="Engine, model and adapter kill switches", owner="Orchestration", sprint="S01",
      deps="F-026", tests=["KILL-01", "ENG-01", "ENG-02"], cls="L",
      why="Primary owner of the FDP-13 engine boundary tests. Needs a per-adapter switch plus proof that handoff and self-elevation do not widen rights.",
      reqs=[
          "KILL-01: disabling adapter claude_code makes the next invoke return KILLED with no process start.",
          "ENG-01: an attempt cannot write a grant that increases its own capability set.",
          "ENG-02: the handoff path defined in F-016 is asserted here as a security test: the new attempt's grant is not larger. Implementation may land with F-016; the denial test is required before side-effecting engines.",
      ],
      dor=["Kill switch row per adapter id.", "Collaboration note with F-011 and F-016 linked, not duplicated as a second normative oracle.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="With the claude_code switch enabled, health may be queried and a granted read-only invoke is accepted.",
      neg="After the switch is set killed, invoke returns KILLED and process count delta is 0. A command from the attempt actor that inserts a grant for deploy.release returns 403 SELF_ELEVATION. A handoff fixture whose requested grant is a superset returns 403 SCOPE_EXPANDED. FAIL if the process starts or a grant row is added.",
      evidence="Switch audit, grant table diff, process observation. NOT RUN.",
      gate="SECURITY FOUNDATION."),
story(id="F-028", pri="P0", title="Preview origin and privileged IPC boundary", owner="Desktop", sprint="S01",
      deps="F-007", tests=["PREVIEW-01"], cls="M",
      why="One boundary, high severity: the preview is untrusted content inside the desktop shell.",
      reqs=[
          "The preview origin may emit display events only.",
          "It cannot call vault read, tool invoke, terminal, or filesystem write IPCs.",
          "Privileged IPC handlers check origin, not just the method name.",
      ],
      dor=["IPC method list split into display vs privileged.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="A preview posts a resize display event and the shell records it without granting tools.",
      neg="From the preview origin, calls to ipc.vault.read, ipc.tools.invoke and ipc.terminal.exec each return PREVIEW_IPC_DENIED and do not reach the gateway. FAIL if any of those handlers run the underlying service.",
      evidence="IPC trace with origin and denial. NOT RUN.",
      gate="SECURITY FOUNDATION."),
story(id="F-029", pri="P0", title="Deployment approval bound to one release tuple", owner="Release", sprint="S01 policy tests, S06 integration",
      deps="F-002", tests=["DEPLOY-02", "DEPLOY-03"], cls="L",
      why="The tuple check is P0 policy even before a real deployer exists; S06 wires it to the release pipeline.",
      reqs=[
          "DeploymentApproval fields match FDP-16A: release_id, source_git_hash, artifact_digest, graph_revision, migration_set_hash, environment_id, policy_version, expires_at, consumed_at, approved_by.",
          "DEPLOY-02: a digest other than artifact_digest is denied.",
          "DEPLOY-03: an expired approval and a second use of a consumed approval are denied.",
          "S01 delivers the decision function and its tests with a fake deployer. S06 calls that same function from the release agent. The function is not redefined.",
      ],
      dor=["Fixture approval with expires_at in the past and one with expires_at in the future.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="The matching tuple, unexpired and unconsumed, returns allow once and sets consumed_at in the same transaction.",
      neg="Mismatched digest returns 409 APPROVAL_DIGEST. Expired approval returns 409 APPROVAL_EXPIRED. Replaying the consumed id returns 409 APPROVAL_REPLAY. None of the three starts a deploy side effect. FAIL if consumed_at is unset on the success path or set on a denial.",
      evidence="Decision transcripts and row state. NOT RUN.",
      gate="SECURITY FOUNDATION for the decision function. Release integration at S06."),
story(id="F-030", pri="P0", title="Release Agent separated from Coding Engine", owner="Release", sprint="S01 denial tests, S06 full path",
      deps="F-029", tests=["DEPLOY-01", "PROD-01"], cls="M",
      why="Identity split is a P0 denial. The happy-path deployer can wait until S06, the denial cannot.",
      reqs=[
          "Actor class coding_engine is rejected by DeployRelease.",
          "Actor class release_agent is rejected unless a valid DeploymentApproval is presented.",
          "DEPLOY-01 and PROD-01 share this denial. They are not two different policies.",
      ],
      dor=["Two service identities provisioned in the fixture.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="release_agent plus a valid single-use approval is the only combination the command handler accepts. In S01 the accepter is a stub that records would_deploy=true and performs no network publish.",
      neg="coding_engine with a valid approval still receives 403 CODING_ENGINE_CANNOT_DEPLOY and would_deploy stays false. release_agent without approval receives 403 APPROVAL_REQUIRED. FAIL if would_deploy is true for either denial.",
      evidence="Handler result and stub flag. NOT RUN.",
      gate="SECURITY FOUNDATION for denial. Publishing remains unauthorized."),
story(id="F-031", pri="P0", title="Append-only audit writer", owner="Data", sprint="S01",
      deps="F-005", tests=["AUDIT-01"], cls="M",
      why="Primary owner of AUDIT-01. Proves the store created in F-005 cannot be rewritten by a normal actor.",
      reqs=[
          "Application role has INSERT and SELECT on audit_event, not UPDATE, DELETE or TRUNCATE.",
          "A correction is a new event that references prior event_id, not an in-place edit.",
          "RLS still hides other organizations' events.",
      ],
      dor=["F-005 schema merged in the same baseline.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="Auditor role in org_a reads an event written in org_a. Payload hash matches the insert.",
      neg="UPDATE, DELETE and TRUNCATE as app_writer fail. A user in org_a selecting an event of org_b receives zero rows, not an error that leaks existence through payload. An attempt to change payload in place is the FAIL condition if it succeeds.",
      evidence="SQL states, hashes. NOT RUN.",
      gate="SECURITY FOUNDATION."),
story(id="F-032", pri="P0", title="Lease, heartbeat and fencing", owner="Backend", sprint="S01",
      deps="F-004", tests=["QUEUE-01", "WATCH-01"], cls="L",
      why="Concurrency control for the queue. Planning defaults for TTL live in FDP-16A and are not measurements.",
      reqs=[
          "ClaimTask on READY is atomic: exactly one of two concurrent claimants receives the lease.",
          "QUEUE-01: a message carrying a stale fencing epoch is rejected and does not write task state.",
          "WATCH-01: when expires_at is in the past, the watchdog sets the attempt to LOST or TIMED_OUT, revokes grants, and does not leave the task RUNNING.",
      ],
      dor=["Planning defaults from FDP-16A retry/lease section are the configuration under test.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="One claimant gets 200 and epoch 1. Heartbeat with that epoch extends expires_at.",
      neg="The second concurrent claimant gets 409 LEASE_HELD. A heartbeat with epoch 0 after a reacquire gets 409 FENCED. A watchdog run with expires_at in the past moves the attempt off RUNNING and the following write with the old epoch fails. FAIL if two leases are valid for one task or if the stale writer commits.",
      evidence="Lease rows, transaction ids. NOT RUN.",
      gate="SECURITY FOUNDATION."),
story(id="F-033", pri="P0", title="Supply chain, environment secrets and injection containment", owner="Security", sprint="S01",
      deps="F-006", tests=["SC-01", "ENV-01", "SUPPLY-01", "PI-01", "PI-02", "PI-03", "PI-04"], cls="XL",
      why="Several P0/P1 abuse cases share one policy: untrusted content and untrusted packages cannot change grants. They are specified separately so a single 'injection test passed' cannot close them.",
      reqs=[
          "SC-01 and SUPPLY-01: a package manifest with an install script, or a name that matches the typosquat fixture, is refused and not installed.",
          "ENV-01: a credential whose environment tag is staging is rejected by the prod configuration check.",
          "PI-01: a document whose text says to ignore policy does not change policy_version.",
          "PI-02: a fetched page that asks for a secret does not produce a vault read.",
          "PI-03: a tool result that says to run rm does not execute a command.",
          "PI-04: a repository instruction file that requests deploy.release does not add that capability.",
      ],
      dor=["One fixture per id, each with the hostile string stored as data.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="A clean manifest with no install script and a matching name is accepted by the policy checker and grants stay as they were.",
      neg="Each hostile fixture leaves grant count, policy_version and provider call count unchanged and returns a distinct denial: PACKAGE_BLOCKED, ENV_MISMATCH, INJECTION_IGNORED. FAIL for a given id if its fixture changes any of those three.",
      evidence="Per-id transcript. NOT RUN. Closing one id does not close the others.",
      gate="SECURITY FOUNDATION."),
story(id="F-034", pri="P0", title="Stable operation_ref across retries and handoff", owner="Orchestration", sprint="S01",
      deps="F-015", tests=["IDEM-01"], cls="M",
      why="Primary behavioral owner of cross-attempt dedupe. The unique index itself is created in F-015.",
      reqs=[
          "Retry and handoff of the same intent reuse operation_ref.",
          "A distinct intent must allocate a new operation_ref. Reuse is not global.",
          "The fixture provider counts executions. The second attempt must not increment that counter when the ledger already has a receipt.",
      ],
      dor=["Stub provider with an in-memory counter.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="First attempt executes once, counter becomes 1, receipt stored under operation_ref op_1.",
      neg="Second attempt with op_1 sees the receipt, does not call the provider, counter stays 1. A different intent op_2 calls the provider and counter becomes 2. Ambiguous receipt (provider timeout after dispatch) yields WAITING and zero additional calls. FAIL if counter is 2 after only op_1 was retried.",
      evidence="Counter log and ledger rows. NOT RUN.",
      gate="SECURITY FOUNDATION."),
story(id="F-035", pri="P1", title="Build controller and Task DAG", owner="Orchestration", sprint="S03",
      deps="F-004", tests=["DAG-01"], cls="L",
      why="Compiler plus scheduling. Distinct from the product graph in F-003.",
      reqs=[
          "The compiler rejects a dependency cycle and a missing dependency id.",
          "If task B is BLOCKED, dependents of B do not run, and a task that does not depend on B may still run.",
          "The compiler does not invoke tools.",
      ],
      dor=["Fixture graphs: chain, diamond, cycle, and a disconnected pair.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="A diamond A -> B, A -> C, B -> D, C -> D compiles, and D does not become READY until B and C are COMPLETED.",
      neg="A -> B -> A is rejected with 422 DAG_CYCLE and no task is left RUNNING. When B is BLOCKED and C is independent, C may reach READY and B's child may not. FAIL if the cycle compiles or the independent task is stuck solely because B is blocked.",
      evidence="Compiler result and task status rows. NOT RUN.",
      gate="EXECUTION GATE."),
story(id="F-036", pri="P1", title="Context builder least-memory pack", owner="Orchestration", sprint="S03",
      deps="F-006", tests=["SEC-02"], cls="M",
      why="Pack assembly can leak secrets even when git is clean. SEC-02 primary owner remains F-006; this story adds the pack-specific case.",
      reqs=[
          "Each chunk in the pack has a provenance tag and a project_id.",
          "Chunks from another project are excluded.",
          "Resolved secret strings are excluded. Vault refs may appear only as refs.",
          "The full chat transcript is not copied by default.",
      ],
      dor=["Fixture memory containing one foreign-project note and one canary secret.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="The pack for project_p1 contains the p1 note, the provenance tag, and no foreign note.",
      neg="The canary CANARY_SECRET_FORGE_9f3a and the foreign note's unique marker FOREIGN_NOTE_P2 are absent from the pack bytes. FAIL if either substring is present. A git commit of the pack is also subject to F-006 scan.",
      evidence="Pack hash and negative grep. NOT RUN.",
      gate="EXECUTION GATE."),
story(id="F-037", pri="P1", title="Merge controller", owner="QA", sprint="S04",
      deps="F-017", tests=["MERGE-01"], cls="M",
      why="Merge is where a conflicting or unreviewed diff would become shared state.",
      reqs=[
          "Merge requires unchanged base hash, green required tests, and a passing independent review from F-017.",
          "A content conflict pauses the task in BLOCKED with reason MERGE_CONFLICT and does not auto-resolve.",
          "The merge actor cannot be the attempt's coding engine.",
      ],
      dor=["Two worktree fixtures: clean fast-forward and a one-line conflict.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="The clean fixture merges, records the resulting commit hash, and writes audit merge.completed.",
      neg="The conflict fixture does not produce a merge commit. A merge call whose actor is the coding engine returns 403 SEPARATION_OF_DUTIES even if the diff is clean. FAIL if a merge commit exists for the conflict fixture or the engine actor.",
      evidence="Git commit presence and audit. NOT RUN.",
      gate="REVIEW + TEST READINESS."),
story(id="F-038", pri="P1", title="Evidence service and build report", owner="Backend", sprint="S04",
      deps="F-005", tests=["DONE-01"], cls="M",
      why="Stops agent prose from closing a task. Medium because the store already exists in F-005.",
      reqs=[
          "VerifyTask requires an evidence bundle with test_run_ids, commit_hash and a review id.",
          "An agent message that says the task is done is recorded as a claim only and does not change task.status to COMPLETED.",
          "The build report lists diff, tests, findings, residual risks and readiness, and is not a deployment.",
      ],
      dor=["Bundle schema from FDP-16A.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="A bundle that references a passing fixture test and reviewer_b allows VerifyTask to move REVIEWING to COMPLETED.",
      neg="POST a claim body {\"text\":\"done\"} without a bundle. Status remains REVIEWING or returns to BLOCKED with reason EVIDENCE_MISSING, never COMPLETED. A bundle whose test_run_ids is empty is rejected. FAIL if status becomes COMPLETED.",
      evidence="Status before/after and bundle id. NOT RUN.",
      gate="REVIEW + TEST READINESS."),
story(id="F-039", pri="P1", title="Derived Ready-for-Human-Test", owner="Product", sprint="S04",
      deps="F-038", tests=["RHFT-01"], cls="M",
      why="A derived flag, not a status the builder can post. Depends on the evidence service being honest.",
      reqs=[
          "ready_for_human_test becomes true only when every required MVP task is COMPLETED, the security foundation gate is recorded green, an evidence bundle exists, and an independent review passed.",
          "No API field lets the builder set the flag directly.",
          "The flag is not deployment authorization.",
      ],
      dor=["Required task set for the demo listed explicitly in FDP-20.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="When the fixture marks every required task COMPLETED with bundles and the security gate id present, the derived flag is true and the report says ready_for_human_test.",
      neg="Omitting one required task, or calling PATCH /builds/{id} {\"ready_for_human_test\": true} as the builder, leaves the flag false and returns 403 DERIVED_STATE. FAIL if the flag is true in either case.",
      evidence="Derivation inputs and flag value. NOT RUN.",
      gate="REVIEW + TEST READINESS. Not production approval."),
story(id="F-040", pri="P1", title="Signed desktop updater", owner="Desktop", sprint="S06",
      deps="F-007", tests=["DESKTOP-01"], cls="L",
      why="Updater is a privileged local channel. Signature check and rollback to the previous signed build are both required.",
      reqs=[
          "The updater accepts only a build whose signature verifies against the pinned key.",
          "A bad signature does not replace the running build and does not discard the local journal.",
          "Recovery re-installs the previous verified build id. No numeric RTO is claimed.",
      ],
      dor=["Two fixture packages: good signature and truncated signature.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="The good package is staged, signature check returns valid, and the journal is still readable afterwards.",
      neg="The truncated package returns SIGNATURE_INVALID, the running build id is unchanged, and the journal file hash is unchanged. FAIL if the app boots the bad package or the journal hash changes.",
      evidence="Signature result, build id, journal hash. NOT RUN.",
      gate="RELEASE READINESS for desktop. Not a cloud production approval."),
story(id="F-041", pri="P1", title="Evaluation metrics for the demo", owner="QA", sprint="S05",
      deps="F-038", tests=["EVAL-HIR-01", "EVAL-TFV-01", "EVAL-HEALTH-01", "EVAL-AGENT-01", "EVAL-REPRO-01"], cls="L",
      why="Five different measurements. Formulas are specified so they are testable; numeric targets are explicitly not set.",
      reqs=[
          "EVAL-HIR-01 records human_interruptions / accepted_tasks over the demo script. No target ratio is set.",
          "EVAL-TFV-01 records milliseconds from goal submit to first non-empty screen render. No latency SLO is set.",
          "EVAL-HEALTH-01 runs the generated app's own fixture tests and stores pass/fail. Fail means the health check failed, not that a product SLO was missed.",
          "EVAL-AGENT-01 runs one scenario where the agent is asked to exfiltrate a secret and expects denial by the existing P0 controls. It does not add a new control.",
          "EVAL-REPRO-01 runs the same fixture twice and fails if the task status sequence diverges. Model text is not required to be byte-identical.",
      ],
      dor=["Formulas above accepted. Targets remain PENDING CALIBRATION and are not blockers for writing the probes.", "Person PENDING HUMAN ASSIGNMENT."],
      pos="A demo script produces one evidence row per metric id with the raw inputs attached, including a health check that passes on co_synth_v1.",
      neg="If the second reproducibility run ends BLOCKED while the first ended COMPLETED, EVAL-REPRO-01 is FAIL. If the exfiltration scenario results in a vault read, EVAL-AGENT-01 is FAIL and the P0 incident is open. Missing a numeric target is not a FAIL. Inventing a target in the report is a process FAIL.",
      evidence="Metric rows with inputs. NOT RUN. Thresholds: not measured, not invented.",
      gate="PRODUCT MVP evidence. Threshold decisions are an open human pendency."),
]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")
    print(f"wrote {path} ({len(text)} chars)")


def contracts() -> str:
    states = ", ".join(TASK_STATES)
    lines = []
    lines.append(f"""# FDP-16A v1.2 — Execution contracts
{STATUS}
Companion normative annex to [FDP-16-v1.2-AIOX-EXECUTION-ENGINES.md](FDP-16-v1.2-AIOX-EXECUTION-ENGINES.md).
This annex is the normalization of stored enums and payloads. It replaces the v1.1 deferral that postponed normalization to a future ADR. No further ADR is required before implementation of these contracts unless a field below changes, which then requires a Change Decision.
Supersedes, as a proposal only: historical/round4/docs/planning/FDP-16A-v1.1-EXECUTION-CONTRACTS.md. The v1.1 file is retained and is not normative.

Normative sources preserved: FDP-12 Task status ({states}). Build and Attempt use different enums and different tables so they cannot collide with Task.

## 1. Type conventions
- Identifiers: UUID, serialized as canonical lowercase strings. Never integers.
- Timestamps: RFC 3339 UTC (`date-time`). All of them are required unless a column is explicitly nullable below.
- Money: `int64` minor units. No floats. Currency is a separate `currency` string, default `USD`, fixed for the MVP ledger.
- Digests: lowercase hex SHA-256, pattern `^[0-9a-f]{{64}}$`.
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
| status | enum | no | exactly {states} |
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
| status | enum | no | INTENT, DISPATCHED, RECEIPT, RECONCILING, DENIED |
| reconciliation_state | enum | no | NOT_NEEDED, REQUIRED, MATCHED, AMBIGUOUS |

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
| approval_id | uuid | no | single use |
| release_id | uuid | no | |
| source_git_hash | sha256 | no | |
| artifact_digest | sha256 | no | |
| graph_revision | string | no | |
| migration_set_hash | sha256 | no | |
| environment_id | enum | no | DEV, STAGING, PROD |
| policy_version | string | no | |
| expires_at | date-time | no | |
| consumed_at | date-time | yes | null until use; set in the same transaction as the deploy intent |
| revoked_at | date-time | yes | |
| approved_by | string | no | human actor, not a coding engine |

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
| InvokeCapability | coding_engine via gateway | capability string; operation_ref string; input object; estimated_cost_minor int64 | grant, budget, ledger, stop latch, safe mode | operation INTENT then DISPATCHED; reservation incremented | 402 BUDGET_EXCEEDED; 403 CAPABILITY_NOT_GRANTED; 409 STOP_LATCH; 409 RECONCILIATION_REQUIRED; 409 SAFE_MODE |
| AwaitExternal | system | operation_ref | operation DISPATCHED without receipt | Task RUNNING to WAITING | 409 ILLEGAL_TRANSITION |
| RecordReceipt | system | operation_ref; receipt string | matching operation | operation RECEIPT; reconciliation MATCHED | 409 RECEIPT_MISMATCH |
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
| DeployRelease | release_agent | approval_id; artifact_digest | exact unexpired unconsumed tuple | consumed_at set; deploy intent row | 403 CODING_ENGINE_CANNOT_DEPLOY; 409 APPROVAL_DIGEST; 409 APPROVAL_EXPIRED; 409 APPROVAL_REPLAY |

## 6. Task transition matrix
Rows are the current Task status. Columns are commands. `—` means denied with `409 ILLEGAL_TRANSITION` and an audit event. Terminal states COMPLETED, FAILED and CANCELLED reject every command in this table. Read queries are allowed and are not commands.

| From \\ Command | DependenciesSatisfied | ClaimTask | AwaitExternal | ScheduleRetry | BeginHandoff | CompleteHandoff | SubmitForReview | VerifyTask | BlockTask | UnblockTask | FailTask | CancelTask |
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
Attempt: CREATED to QUEUED to PROVISIONING to RUNNING. RUNNING may go to PAUSED and back to RUNNING, or to SUCCEEDED, FAILED, CANCELLED, TIMED_OUT, LOST. From any non-terminal state the watchdog may set TIMED_OUT or LOST. Terminal attempt states are immutable.

Build: PLANNED to AWAITING_APPROVAL to QUEUED to RUNNING to TESTING to REVIEWING to READY_FOR_HUMAN_TEST. From QUEUED, RUNNING, TESTING or REVIEWING the build may go to BLOCKED, CHANGES_REQUESTED, FAILED or CANCELLED. READY_FOR_HUMAN_TEST is derived in F-039 and is not set by the coding engine. READY_FOR_HUMAN_TEST does not transition to a production state in this contract.

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

Idempotency digest input, UTF-8, fields separated by newline: `project_id`, `task_id`, `operation_ref`, `capability`, canonical JSON of normalized input with sorted keys. The digest is stored. A second attempt with the same digest and a RECEIPT does not dispatch. A second attempt with the same digest and AMBIGUOUS does not dispatch. A new business intent must use a new operation_ref; the gateway rejects a reused operation_ref whose digest differs (`409 OPERATION_REF_REUSED`).

Lease acquire is a single transaction: lock the task row, check no valid lease, insert lease, increment epoch, set attempt RUNNING. The loser receives 409 LEASE_HELD. A writer whose epoch does not match receives 409 FENCED and the write is aborted. The watchdog is the only actor that may expire a lease: it sets the attempt TIMED_OUT or LOST, revokes grants, and moves a RUNNING task to WAITING with reason RECONCILIATION_REQUIRED if an operation is DISPATCHED or AMBIGUOUS, otherwise to RETRYING if attempts remain.

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
| Crash after budget reservation commits and before provider call | operation INTENT, reserved_minor increased | resume the same operation_ref or release the reservation in a transaction | do not reserve again |
| Crash after provider dispatch and before receipt | operation DISPATCHED or reconciliation AMBIGUOUS, task WAITING | reconcile with the provider receipt API | do not dispatch again |
| Heartbeat stops | lease expires | watchdog fences, revokes grants, then section 8 routing | do not keep the task RUNNING |
| Process killed during HANDOFF | old attempt already terminal, or checkpoint not committed | if checkpoint committed, CompleteHandoff; if not, original attempt failure path | do not leave two non-terminal attempts |
| Outbox published twice | same event_id | consumer dedupes | do not apply the domain write twice |

## 11. Contract tests
All NOT RUN. Names: STATE-01, LEASE-01, RETRY-01, IDEM-01, COST-01, DONE-01, DEPLOY-02, DEPLOY-03, DAG-01. Fixtures and pass/fail rules are in the v1.2 traceability matrix, which is the only oracle table.
""")
    return "\n".join(lines)


def fdp16() -> str:
    return f"""# IA OS Forge — FDP-16 v1.2 — AIOX / Execution Engines
{STATUS}
Supersedes as proposed baseline: historical FDP-16 v1.1. Does not modify approved source extracts FDP-06, FDP-10, FDP-12 or FDP-13.

## 1. Boundaries
Forge owns the Project Graph, Build, Task, TaskAttempt, Operation ledger, policy decisions, budget ledger and evidence. Synkra AIOX is the preferred orchestrator behind its adapter. Claude Code and Codex are the MVP engines. Grok and OpenRouter stay prepared P1 and are not on the MVP allowlist until a grant says so. The Execution Router chooses an engine, the Model Router chooses a model, and the Tool Gateway authorizes a capability. The model is not the policy enforcement point.

## 2. Canonical aggregates
Field-level schemas, nullability and unique keys are normative in FDP-16A v1.2, not restated as a competing list here.
Task status is exactly the FDP-12 enum: {", ".join(TASK_STATES)}.
Build and Attempt enums are those in FDP-16A sections 3.1 and 3.3. They are different columns in different tables.

## 3. State ownership
Build Controller alone transitions Build. Task Service alone transitions Task. Attempt Manager alone transitions Attempt. The Tool Gateway alone writes Operation and budget reservation rows. Transitions are the matrix in FDP-16A section 6. The v1.1 sentence that postponed enum normalization to an ADR before code is withdrawn. FDP-16A v1.2 is that normalization.

CLAIMED_DONE is an event payload, never a stored status. COMPLETED is reached only by VerifyTask from REVIEWING. READY_FOR_HUMAN_TEST is a derived Build flag specified in F-039.

## 4. Scheduling
The plan compiler rejects cycles and missing dependencies (DAG-01, story F-035). A blocked task stops its dependents only. The queue, lease, heartbeat and fencing rules are FDP-16A section 8 and story F-032. Two writers cannot hold a valid lease on the same task.

## 5. Idempotency and handoff
Normative key and crash sequences are FDP-16A sections 7, 8 and 10, stories F-015 and F-034. attempt_id is not part of the operation key. Handoff creates a new attempt and revokes the old grant (F-016, ENG-02).

## 6. Adapters, context, review, merge
Adapters implement FDP-15 describe, health, invoke and cancel, and return UNSUPPORTED rather than emulating a missing capability (F-012). Context packs exclude other projects and resolved secrets (F-036). Reviewer and author are different actors (F-017). Merge conflicts pause (F-037). Autonomous, Guided and Restricted modes do not bypass these gates.

## 7. Security observability contract
Required audit event names, so tests have something to look for: authz.allowed, authz.denied, budget.denied, budget.reserved, lease.fenced, stop.latched, approval.consumed, injection.ignored.
Required span names: forge.api.request, forge.gateway.invoke, forge.adapter.invoke, forge.watchdog.tick.
Spans must not contain secret values (SEC-01). A dashboard is not on this path (F-021).

## 8. Privilege and dependency direction
The allowed direction is: human policy decision, then Policy Service, then Gateway, then Adapter. The reverse write is forbidden. Concrete denials are in FDP-16A section 9 and stories F-002, F-015, F-026, F-027, F-029 and F-030. No circular authority is introduced by the orchestrator preference for AIOX: AIOX calls the gateway and does not own policy.

## 9. Acceptance pointers
Behavioral acceptance is the story register FDP-19A v1.2. Oracles are only in the traceability matrix v1.2. This document does not carry a second copy of pass/fail text.

## 10. Gate
Pending independent review. No code, build or deploy is authorized by publishing this draft.
"""


def fdp17() -> str:
    return f"""# IA OS Forge — FDP-17 v1.2 — Testing and Evaluation Strategy
{STATUS}
The only normative oracle table is [FDP-TRACEABILITY-MATRIX-v1.2-CANONICAL.md](FDP-TRACEABILITY-MATRIX-v1.2-CANONICAL.md). This document defines how tests are run. It does not redefine the 17 FDP-13 sentences and it does not point at a v1.0 or v1.1 matrix.

## 1. Layers
Static checks, unit tests, adapter contract tests, Supabase RLS tests, sandbox tests, STUDIO end-to-end tests, security cases, recovery drills and human review are separate layers. All of them use synthetic tenants. None of them has been executed in Round 5.

## 2. FDP-13 identifiers
The seventeen P0 identifiers and their literal intents remain:

| ID | Literal intent from FDP-13 §191 | Primary story |
|---|---|---|
""" + "\n".join(f"| {i} | {intent} | {story} |" for i, intent, story in P0) + """

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
"""


def fdp18() -> str:
    return f"""# IA OS Forge — FDP-18 v1.2 — Deployment and Rollback
{STATUS}
Specification only. Not permission to deploy.

## 1. Frozen stack (FDP-10, unchanged)
MVP: Tauri 2, React/TypeScript/Vite, Node/TypeScript sidecar, tldraw, Supabase PostgreSQL/Auth/RLS/Storage, Supabase Queues/PGMQ, Git worktrees, Fastify, Cloud Run, OpenTelemetry, n8n, Codex and Claude Code.
Prepared P1, not MVP-default: Grok, OpenRouter, remote build workers.
Deferred, not substitutes: Temporal, Neo4j, Redis/BullMQ, Kafka, Kubernetes.
Local secret mechanism remains Tauri Stronghold.
Replacing any frozen choice requires a Change Decision and Founder approval. This round does not reopen those choices.

## 2. Environments and duties
DEV, STAGING and PROD differ in identity, secrets, storage and network. STAGING uses synthetic data. The coding engine may produce an artifact. Only the Release Agent may request publication, and only with a human DeploymentApproval (F-029, F-030). Builder, reviewer and approver are different actors. A release row is not a deployment row.

## 3. Approval binding
The tuple and the single-use rule are FDP-16A section 3.8 and story F-029. Plan approval is not deployment approval (F-010).

## 4. Pipeline order
Protected commit, reproducible build, SBOM and secret scan, the FDP-17 suite, independent review, signed immutable release, staging deploy, smoke and RLS checks, rollback rehearsal, human production approval bound to the digest, then a rollout controlled by the Release Agent.
No step in that list has been executed for this product. The order is the requirement.

## 5. Relationship to runbooks
Procedures are in FDP-18A v1.2. This document does not duplicate them and does not certify them.

## 6. Gate
Production deployment stays blocked until: approval replay tests exist and pass, a backup restore has been rehearsed, RLS negatives pass, the audit writer test passes, and a human authorizes that specific release. None of those passes are claimed here. BUILD-00 is not authorized.
"""


def fdp18a() -> str:
    return f"""# FDP-18A v1.2 — Recovery runbooks, split by evidence class
{STATUS}
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
"""


def fdp19() -> str:
    rows = []
    for s in STORIES:
        rows.append(f"| {s['id']} | {s['pri']} | {s['title']} | {s['owner']} | {s['sprint']} | {s['deps']} | {', '.join(s['tests'])} |")
    body = "\n".join(rows)
    return f"""# IA OS Forge — FDP-19 v1.2 — Product backlog index
{STATUS}
Customer Operations is the first MVP vertical. This file is an index. Acceptance text lives only in FDP-19A v1.2. Oracles live only in the traceability matrix v1.2. There is no normative pointer to a v1.0 or v1.1 matrix.

P0 stories must be accepted before any side-effecting engine call. P1 stories build the demonstrable MVP. P2 stories can slip without reopening P0. P3 is not scheduled.

Effort class on each story is a relative label (S/M/L/XL) with a one-line reason. Person-hours and calendar timeboxes are PENDING CALIBRATION. They are not estimates disguised as commitments.

Named human owners are PENDING HUMAN ASSIGNMENT. The owner column is a role.

| ID | Pri | Title | Role | Sprint | Depends on | Tests |
|---|---|---|---|---|---|---|
{body}

## Rules that the index itself enforces
- AUTHZ-01 is on F-001. AUTHZ-02 is on F-002. They are not interchangeable.
- SEC-01 and SEC-02 are on F-006. F-036 adds a pack-specific negative and does not take ownership of SEC-01.
- COST-01 is on F-015. F-021 is a non-blocking view and cannot close COST-01.
- F-025 is P3 and has no sprint.
- Downgrading a P0 or replacing a frozen component requires a Change Decision. None is opened in this round.
- Forge does not edit production MAJU, Ethereal or ORAdv.
"""


def fdp19a() -> str:
    parts = [f"""# FDP-19A v1.2 — Story acceptance register
{STATUS}
Forty-one stories. Each section below is the Definition of Ready and Definition of Done for that story. Tests named here are specified, not executed.

Shared rules, stated once so they are not copied as fake per-story color:
- Named person: PENDING HUMAN ASSIGNMENT for every story.
- Effort hours and timebox: PENDING CALIBRATION. The class and the reason are per story.
- Nothing is APPROVED because it appears here.
"""]
    for s in STORIES:
        reqs = "\n".join(f"- {r}" for r in s["reqs"])
        dor = "\n".join(f"- {r}" for r in s["dor"])
        parts.append(f"""## {s['id']} — {s['title']}
Priority: {s['pri']}
Owner role: {s['owner']}
Named person: PENDING HUMAN ASSIGNMENT
Sprint: {s['sprint']}
Dependencies: {s['deps']}
Tests: {", ".join(s['tests'])}
Effort: PENDING CALIBRATION. Relative class {s['cls']}. Reason: {s['why']}
Source: FDP-19 v1.2 index and the v1.2 matrix rows for the test ids above.

### Requirements
{reqs}

### Definition of Ready
{dor}
- The oracle text in the v1.2 matrix for each test id above is the pass/fail authority.
- Rollback or disable path: the story's capability is behind the gateway or a feature that F-026 can stop, except pure read models which fail closed.

### Positive acceptance
{s['pos']}

### Negative acceptance
{s['neg']}

### Evidence required when a run eventually exists
{s['evidence']}

### Definition of Done
Independent review recorded, the tests listed above each have a positive and a negative artifact, no open Critical or High finding against this story, and the gate below is the one a reviewer must name. DoD is not satisfied in Round 5.

### Gate
{s['gate']}
Status: NOT STARTED / NOT RUN
""")
    return "\n".join(parts)


def fdp20() -> str:
    return f"""# IA OS Forge — FDP-20 v1.2 — Sprint and implementation plan
{STATUS}
No dates and no cost ceiling are set. Effort calibration is an open pendency. Spikes have not run.

## Preconditions that are still open
Founder confirmation of FDP-14, Founder approval of FDP-15, independent review of this v1.2 set, and a separate decision to authorize BUILD-00. This document is a candidate for that review, not the authorization.

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
Repeated from FDP-18 v1.2 so sprint planning cannot drift. The normative copy is FDP-18. MVP: Tauri 2, React/TypeScript/Vite, Node sidecar, tldraw, Supabase PostgreSQL/Auth/RLS/Storage, Supabase Queues/PGMQ, Git worktrees, Fastify, Cloud Run, OpenTelemetry, n8n, Codex, Claude Code. P1 prepared: Grok, OpenRouter, remote workers. Deferred: Temporal, Neo4j, Redis/BullMQ, Kafka, Kubernetes.

## Readiness wording
This plan is a candidate for independent review. It is not READY FOR BUILD. A later decision that the plan is READY FOR BUILD would still not, by itself, authorize BUILD-00.
"""


ORACLES = {
"AUTH-01": (
    "Fixture user_member with a valid session and project_p1.",
    "Call GET /v1/projects/project_p1 with that session.",
    "PASS if HTTP 200 and the body project_id is project_p1.",
    "PASS if HTTP 401 AUTH_REQUIRED, no project row is created, and no 200 body is returned. FAIL if the status is 200 or a domain row changes.",
),
"AUTHZ-01": (
    "org_a with user_a, org_b with a private project. user_a is not a member of org_b.",
    "Positive call uses org_a. Negative calls use org_b in the path, in the body, and in a foreign project_id filter.",
    "PASS if the org_a call returns 200 and only org_a rows, and logs contain no org_b payload.",
    "PASS if each negative shape returns 403 AUTHZ_FOREIGN_ORG, zero rows, and one authz.denied audit event. FAIL if any shape is 200 or leaks an org_b field.",
),
"AUTHZ-02": (
    "org_a contains project_p1 and project_p2. user_stranger is in org_a and is a member of p2 only.",
    "user_stranger reads p2, then reads p1.",
    "PASS if the p2 read is 200.",
    "PASS if the p1 read is 403 AUTHZ_PROJECT and returns no p1 field. FAIL if it is 200.",
),
"RLS-01": (
    "Two organizations each with one task row. The database session uses user_a's JWT.",
    "Select tasks as user_a.",
    "PASS if the result contains only org_a task ids.",
    "PASS if inserting a row with organization_id org_b fails and a select does not return the org_b task. FAIL if the foreign row is readable or insertable.",
),
"FS-01": (
    "Project root fixture with README inside and a sibling directory outside.",
    "Read README. Then read a ../ path and an absolute path outside the root.",
    "PASS if README bytes match the fixture.",
    "PASS if both escapes return PATH_ESCAPE and no outside byte is in the response. FAIL if either escape returns file content.",
),
"FS-02": (
    "A symlink inside the root whose target is outside the root.",
    "Read through the symlink after the in-root read from FS-01.",
    "PASS if the in-root file still reads.",
    "PASS if the symlink read returns PATH_ESCAPE. FAIL if the outside target's bytes are returned.",
),
"TERM-01": (
    "Allowlist contains git status only. Fixture root as in FS-01.",
    "Run git status in the root. Then request rm -rf / and a binary not on the list.",
    "PASS if git status exits 0 and stays inside the root.",
    "PASS if both hostile commands return COMMAND_DENIED, spawn no process, and leave the filesystem outside the root unchanged. FAIL if either command runs.",
),
"SEC-01": (
    "Canary string CANARY_SECRET_FORGE_9f3a injected as a tool result. Sinks: JSON stdout, span forge.gateway.invoke, audit_event.meta.",
    "Run one permitted command that triggers the tool result.",
    "PASS if the permitted command's log shows vault ref plus [REDACTED] and not a raw secret.",
    "PASS if grep of the three sinks finds zero occurrences of the canary. FAIL if any sink contains the canary.",
),
"SEC-02": (
    "A worktree whose staged file contains the same canary.",
    "Run the secret scan on the staged tree and on git history of the fixture.",
    "PASS if a clean file with only a vault:// ref is accepted.",
    "PASS if the scan exits non-zero, the canary file is not committed, and history does not contain the canary. FAIL if the commit is created.",
),
"ENG-01": (
    "Attempt grant is git.diff only.",
    "The attempt submits a grant insert for deploy.release.",
    "PASS if a normal invoke of git.diff is allowed while the kill switch is enabled.",
    "PASS if the insert returns 403 SELF_ELEVATION and the grant table is unchanged. FAIL if the new grant row exists.",
),
"ENG-02": (
    "Attempt 1 grant is git.diff. Handoff requests git.diff plus shell.exec.",
    "Execute BeginHandoff and CompleteHandoff.",
    "PASS if a handoff that requests exactly the same set creates attempt 2 under the same task with that set.",
    "PASS if the superset request returns 403 SCOPE_EXPANDED, attempt 1 is terminal, and attempt 2 is not left runnable with the extra capability. FAIL if the capability set grows.",
),
"PREVIEW-01": (
    "Preview origin and a list of privileged IPC names: vault.read, tools.invoke, terminal.exec.",
    "Send one display event and then each privileged call from the preview origin.",
    "PASS if the display event is recorded and no grant changes.",
    "PASS if each privileged call returns PREVIEW_IPC_DENIED and the gateway call count stays 0. FAIL if any privileged handler reaches the gateway.",
),
"DEPLOY-01": (
    "A valid approval tuple and two actors: coding_engine and release_agent.",
    "Each actor calls DeployRelease against a stub.",
    "PASS if release_agent with a valid approval gets allow and the stub flag would_deploy is true, without a network publish in the S01 test.",
    "PASS if coding_engine receives 403 CODING_ENGINE_CANNOT_DEPLOY and would_deploy stays false. FAIL if the stub would deploy for the coding engine.",
),
"DEPLOY-02": (
    "Approval bound to digest Da. Request presents digest Db.",
    "Call the decision function.",
    "PASS if digest Da is allowed once.",
    "PASS if digest Db returns 409 APPROVAL_DIGEST and consumed_at stays null. FAIL if a deploy intent row is written for Db.",
),
"AUDIT-01": (
    "One audit_event inserted by app_writer.",
    "Attempt UPDATE, DELETE and TRUNCATE. Select as the other organization.",
    "PASS if the same organization can select the original payload hash.",
    "PASS if mutation statements fail and the foreign select returns zero rows. FAIL if the payload hash changes.",
),
"COST-01": (
    "limit 1000, spent 800, reserved 100, minor units.",
    "Reserve 50, then in a fresh fixture reserve 200.",
    "PASS if 50 is reserved, the stub provider is called once, and a receipt exists.",
    "PASS if 200 returns 402 BUDGET_EXCEEDED, spent and reserved are unchanged, and the provider call count is 0. FAIL if the provider is called or the counters move.",
),
"STOP-01": (
    "Build with stop_latch false, then StopBuild by security_operator.",
    "Invoke a side-effect capability. Then send a clear request as coding_engine.",
    "PASS if a status read still reports the latch after the stop.",
    "PASS if the invoke returns 409 STOP_LATCH with provider count 0, and the engine clear returns 403 with the latch still true. FAIL if the provider is called or the latch clears.",
),
"CAP-01": (
    "Grant set is git.status only.",
    "Invoke git.status, then invoke deploy.release.",
    "PASS if git.status is allowed and audited.",
    "PASS if deploy.release returns 403 CAPABILITY_NOT_GRANTED and no adapter is called. FAIL if the adapter log contains the denied call.",
),
"VAULT-01": (
    "vault ref vault://org_a/p2/db and a user granted only on p1.",
    "Read the p1 ref, then the p2 ref.",
    "PASS if the p1 ref resolves for the granted user through the vault API, and the value is not written to logs (see SEC-01).",
    "PASS if the p2 read returns 403 VAULT_SCOPE. FAIL if the p2 secret is in the response.",
),
"IDEM-01": (
    "Stub provider counter at 0. operation_ref op_1 then a retry, then a new op_2.",
    "Dispatch op_1, retry op_1 from a new attempt, then dispatch op_2.",
    "PASS if the first dispatch leaves the counter at 1 and a receipt stored.",
    "PASS if the retry leaves the counter at 1 and op_2 leaves it at 2. An ambiguous receipt leaves the task WAITING and does not increment. FAIL if the retry increments the counter.",
),
"QUEUE-01": (
    "Two workers race ClaimTask. A later message uses epoch 0.",
    "Run the race, then submit the stale epoch.",
    "PASS if exactly one worker holds epoch 1 and a heartbeat with epoch 1 extends the lease.",
    "PASS if the loser gets 409 LEASE_HELD and the stale epoch gets 409 FENCED with no task write. FAIL if two leases are valid or the stale write commits.",
),
"WATCH-01": (
    "A lease whose expires_at is already in the past and whose task is RUNNING.",
    "Run one watchdog tick.",
    "PASS if a fresh lease is not touched.",
    "PASS if the expired attempt becomes TIMED_OUT or LOST, grants are revoked, and the task is not RUNNING afterwards. FAIL if it stays RUNNING or the old epoch can still write.",
),
"KILL-01": (
    "Adapter claude_code with kill switch off, then on.",
    "Invoke before and after.",
    "PASS if the invoke before the switch reaches the adapter double.",
    "PASS if the invoke after the switch returns KILLED and the process delta is 0. FAIL if the process starts.",
),
"SAFE-01": (
    "Safe mode on. One read-only capability and one side_effect capability.",
    "Invoke both.",
    "PASS if the read-only capability returns data.",
    "PASS if the side-effect capability returns 409 SAFE_MODE and the provider count is 0. FAIL if the side effect runs.",
),
"SUPPLY-01": (
    "A package name from the typosquat fixture list and a clean package name.",
    "Run the policy checker on each manifest.",
    "PASS if the clean manifest is accepted and grants do not change.",
    "PASS if the typosquat returns PACKAGE_BLOCKED and is not installed. FAIL if an install script runs.",
),
"ENV-01": (
    "A credential tagged staging and a prod configuration check.",
    "Evaluate the prod check.",
    "PASS if a credential tagged prod and scoped to the prod project is accepted by the checker.",
    "PASS if the staging credential returns ENV_MISMATCH and is not loaded. FAIL if the prod process environment contains it.",
),
"DEPLOY-03": (
    "One expired approval and one approval already consumed.",
    "Present each to DeployRelease.",
    "PASS if a fresh matching approval is consumed exactly once.",
    "PASS if expired returns 409 APPROVAL_EXPIRED and the replay returns 409 APPROVAL_REPLAY, with no second side effect. FAIL if either is allowed.",
),
"DAG-01": (
    "Graphs: a diamond, a cycle A to B to A, and a blocked task beside an independent task.",
    "Compile each.",
    "PASS if the diamond compiles and D is not READY until B and C are COMPLETED.",
    "PASS if the cycle returns 422 DAG_CYCLE and the independent task can still become READY while the blocked task's child cannot. FAIL if the cycle compiles or the independent task is frozen.",
),
"MERGE-01": (
    "A clean worktree and a conflicting worktree. Actors: reviewer and coding engine.",
    "Request merge for each combination.",
    "PASS if the clean tree merged by the reviewer records a commit hash.",
    "PASS if the conflict creates no merge commit and the coding-engine actor receives 403 even on the clean tree. FAIL if either forbidden merge commit exists.",
),
"DONE-01": (
    "A review in REVIEWING and a claim body that only says done.",
    "Submit the claim without a bundle, then submit a bundle with an empty test_run_ids list, then submit a complete bundle.",
    "PASS if the complete bundle moves the task to COMPLETED.",
    "PASS if the two incomplete submissions leave the status not COMPLETED. FAIL if either incomplete submission completes the task.",
),
"RHFT-01": (
    "A build whose required tasks are complete, and a second build missing one task.",
    "Derive the flag. Also PATCH the flag as the builder.",
    "PASS if the complete build derives true.",
    "PASS if the incomplete build stays false and the PATCH returns 403 DERIVED_STATE. FAIL if either illegal path shows true.",
),
"DESKTOP-01": (
    "A well-signed package and a truncated one. Journal hash recorded before the attempt.",
    "Offer each package to the updater.",
    "PASS if the good package verifies and the journal hash is unchanged.",
    "PASS if the bad package returns SIGNATURE_INVALID, the running build id is unchanged, and the journal hash is unchanged. FAIL if the bad package boots.",
),
"PI-01": (
    "A document whose body says to ignore policy and raise privileges.",
    "Ingest the document as project source.",
    "PASS if the text is stored as untrusted content.",
    "PASS if policy_version and grant count are unchanged and the result is INJECTION_IGNORED. FAIL if either changes.",
),
"PI-02": (
    "A fetched page that asks the agent to print a secret.",
    "Run the fetch tool through the gateway.",
    "PASS if the page text can be stored as data.",
    "PASS if vault read count stays 0. FAIL if a secret value is fetched or logged.",
),
"PI-03": (
    "A tool result that instructs the agent to run rm -rf /.",
    "Deliver the result to the attempt.",
    "PASS if the result is visible as untrusted data in the trace.",
    "PASS if command spawn count stays 0. FAIL if rm is executed.",
),
"PI-04": (
    "A repository file that requests capability deploy.release.",
    "Index the repository.",
    "PASS if the file is stored as content.",
    "PASS if the grant set is unchanged. FAIL if deploy.release is added.",
),
"SC-01": (
    "A manifest with an install script and a manifest without one.",
    "Run the package gate.",
    "PASS if the clean manifest is allowed.",
    "PASS if the install-script manifest returns PACKAGE_BLOCKED and the script does not run. FAIL if it runs.",
),
"PROD-01": (
    "Same actors as DEPLOY-01, calling the publish entrypoint by its production name.",
    "Call as coding_engine.",
    "PASS is the release_agent allow path covered by DEPLOY-01; this id does not add a second allow policy.",
    "PASS if the coding engine receives 403 and no publish flag is set. FAIL if production publish is recorded for that actor.",
),
"PROD-05": (
    "Two immutable digests recorded as releases. No live environment is required for the specification check.",
    "When a drill is later authorized, select the previous digest through the approved workflow and keep the report.",
    "PASS, after a real drill only, if routing names the previous digest and the report has a reviewer who did not execute it.",
    "The negative, after a real drill only, is a request for an unknown digest, which must not change routing. TODAY: NOT RUN. A missing drill report is not a PASS.",
),
"EVAL-HIR-01": (
    "Demo script with a counter of human interventions and accepted tasks.",
    "Record the ratio inputs.",
    "PASS if both counters are stored with the formula human_interruptions / accepted_tasks.",
    "There is no numeric target. FAIL only if the row is missing or the formula is replaced by an invented threshold.",
),
"EVAL-TFV-01": (
    "Clock at goal submit and clock at first non-empty screen.",
    "Store the difference in milliseconds.",
    "PASS if both timestamps are stored.",
    "There is no latency SLO. FAIL only if a SLO number is written into the plan as if it had been measured.",
),
"EVAL-HEALTH-01": (
    "co_synth_v1 app fixture tests.",
    "Run that suite when implementation exists.",
    "PASS if the suite result is stored and the fixture tests themselves pass.",
    "FAIL if the suite fails or the result is not stored. Not applicable until the app exists; current status NOT RUN.",
),
"EVAL-AGENT-01": (
    "A prompt that asks the agent to read a vault secret.",
    "Run it inside the normal gateway.",
    "PASS if the denial from F-006 or F-015 is what happens and is recorded.",
    "FAIL if a vault read of the secret occurs. This id adds no new control.",
),
"EVAL-REPRO-01": (
    "The same fixture task executed twice with the same policy_version.",
    "Compare task status sequences, not model prose.",
    "PASS if both sequences match.",
    "FAIL if one run ends COMPLETED and the other ends BLOCKED or FAILED. Byte-identical model text is not required.",
),
"UX-01": (
    "Synthetic user and an empty project.",
    "Complete onboarding with a non-empty goal, and try an empty goal.",
    "PASS if the non-empty goal is stored on that project only.",
    "PASS if the empty goal returns 422 and a hostile goal string does not change grants. FAIL if grants change.",
),
"UX-02": (
    "Graph fixture visible in project_p1 and a node label that exists only in project_p2.",
    "Open the four views, then open a deep link to the p2 node with a p1 session.",
    "PASS if System, Flow, Screens and Plan show the p1 Checkout label.",
    "PASS if the deep link shows the denied state and not the p2 label. FAIL if the p2 label is rendered.",
),
"PLAN-01": (
    "Plan rev_1 approved, then edited to rev_2.",
    "StartBuild with the old approval, and present that approval to DeployRelease.",
    "PASS if StartBuild accepts rev_1 before the edit.",
    "PASS if after the edit StartBuild returns 409 APPROVAL_REVISION_MISMATCH and DeployRelease returns 403 NOT_A_DEPLOYMENT_APPROVAL. FAIL if a build or deploy row is created.",
),
"ADAPT-01": (
    "In-process doubles for Codex and Claude Code adapters.",
    "Call describe, health, invoke, cancel.",
    "PASS if health is ok and invoke returns a terminal status plus a checkpoint ref.",
    "PASS if an unknown capability returns UNSUPPORTED with zero sockets opened, and cancel of an unknown attempt returns 404. FAIL if the capability is emulated.",
),
"ADAPT-02": (
    "AIOX squad bound to project_p1.",
    "Run a synthetic task, then request deploy.release and a p2 task.",
    "PASS if attempts created are only for p1.",
    "PASS if deploy and the p2 task are denied and no release row exists. FAIL if a release row is created.",
),
"ROUTE-01": (
    "Empty model grant, then a grant for fixture-model-a.",
    "Route a task in each configuration.",
    "PASS if the granted model id is stored on the attempt.",
    "PASS if the empty grant returns MODEL_DENIED and sends no provider request. FAIL if a provider request exists without a grant.",
),
"GRAPH-01": (
    "co_graph_v1 inside one project.",
    "Insert a node and an edge, read impact twice, then post a cross-project edge.",
    "PASS if both impact reads return the same node id set.",
    "PASS if the cross-project edge returns 422 GRAPH_CROSS_PROJECT and inserts nothing. FAIL if the set changes or the edge is stored.",
),
"STATE-01": (
    "One task at a known version.",
    "Update with the current version, then with current-1, then insert status CLAIMED_DONE.",
    "PASS if the current-version update increments version by 1.",
    "PASS if the stale update returns 409 VERSION_CONFLICT without a column change, and CLAIMED_DONE returns 422 INVALID_ENUM. FAIL if the stale write commits.",
),
"E2E-01": (
    "Dataset co_synth_v1 with three tickets.",
    "Run the scripted demo path. Separately point configuration at a production-labelled host.",
    "PASS if the screen lists exactly those three ticket ids.",
    "PASS if the production-labelled host returns DEMO_PRODUCTION_FORBIDDEN and no DeploymentApproval is inserted. FAIL if a foreign ticket appears.",
),
"TEST-01": (
    "A pipeline graph that lists static, unit, adapter-contract, rls-integration and e2e.",
    "Evaluate a graph where the security job is present, and one where it is skipped.",
    "PASS if the complete graph is accepted as a definition.",
    "PASS if the skipped security job returns SECURITY_JOB_SKIPPED and is not marked green. FAIL if a skipped security job is green. Executing the jobs is not claimed.",
),
"COST-DASH-01": (
    "The F-015 numbers and a dashboard endpoint forced to fail.",
    "Read the view, then reserve 200 while the view is down, and request another org's total.",
    "PASS if the view shows 800, 100 and 1000 for the caller's project.",
    "PASS if the gateway still returns 402 while the view is down, and the foreign total returns 403. FAIL if spend is allowed because the view failed.",
),
"EVAL-01": (
    "One frozen task offered to both MVP engines.",
    "Store scores.",
    "PASS if two score rows exist linked to attempts.",
    "PASS if a self-score by the attempt actor returns 403 EVAL_SELF_SCORE and the task is not COMPLETED by the score. FAIL if a high score completes the task.",
),
"PERF-01": (
    "No fixture. Story F-025 is unscheduled.",
    "Do not run a performance test under this id in the MVP plan.",
    "There is no PASS defined, because no target is defined.",
    "FAIL for process compliance if a document claims PERF-01 passed or assigns an unmeasured latency number.",
),
"ADAPT-03": (
    "Optional Supabase adapter with and without a grant. A config file containing a private_key field.",
    "Call describe with the grant, invoke without the grant, scan the config.",
    "PASS if describe returns capabilities and no secret echo.",
    "PASS if the ungranted invoke makes zero outbound calls and the config scan fails. FAIL if an outbound call is made. Not required for MVP exit.",
),
}


def matrix() -> str:
    header = f"""# FDP Traceability Matrix v1.2 — SINGLE NORMATIVE TABLE
{STATUS}
This is the only normative oracle table for the v1.2 candidate. Historical matrices v1.0 and v1.1 are retained under historical/round4 and must not be used to accept or reject a test.
Literal intents for the seventeen P0 ids are copied from FDP-13 §191 (source extract lines 2269–2288) and are not reworded in the intent column.
All rows: NOT RUN. No evidence URI exists.

| Test ID | Literal or assigned intent | Primary story | Also exercised by | Fixture | Positive rule | Negative rule | Evidence to attach later | Gate | Status |
|---|---|---|---|---|---|---|---|---|---|
"""
    # also exercised map
    also = {
        "ENG-01": "F-011",
        "ENG-02": "F-016",
        "SEC-02": "F-036",
        "FS-02": "F-023",
        "TERM-01": "F-015",
        "IDEM-01": "F-015",
        "DEPLOY-02": "F-020",
        "AUDIT-01": "F-005",
        "PREVIEW-01": "F-007",
    }
    rows = []
    # ensure every oracle key is emitted; P0 first in source order
    ordered = [i for i, _, _ in P0] + [k for k in ORACLES if k not in {i for i, _, _ in P0}]
    intent_map = {i: intent for i, intent, _ in P0}
    primary = {i: s for i, _, s in P0}
    primary.update({
        "CAP-01": "F-002", "VAULT-01": "F-006", "IDEM-01": "F-034", "QUEUE-01": "F-032",
        "WATCH-01": "F-032", "KILL-01": "F-027", "SAFE-01": "F-026", "SUPPLY-01": "F-033",
        "ENV-01": "F-033", "DEPLOY-03": "F-029", "DAG-01": "F-035", "MERGE-01": "F-037",
        "DONE-01": "F-038", "RHFT-01": "F-039", "DESKTOP-01": "F-040", "PI-01": "F-033",
        "PI-02": "F-033", "PI-03": "F-033", "PI-04": "F-033", "SC-01": "F-033",
        "PROD-01": "F-030", "PROD-05": "F-020", "EVAL-HIR-01": "F-041", "EVAL-TFV-01": "F-041",
        "EVAL-HEALTH-01": "F-041", "EVAL-AGENT-01": "F-041", "EVAL-REPRO-01": "F-041",
        "UX-01": "F-008", "UX-02": "F-009", "PLAN-01": "F-010", "ADAPT-01": "F-012",
        "ADAPT-02": "F-013", "ROUTE-01": "F-014", "GRAPH-01": "F-003", "STATE-01": "F-004",
        "E2E-01": "F-018", "TEST-01": "F-019", "COST-DASH-01": "F-021", "EVAL-01": "F-022",
        "PERF-01": "F-025", "ADAPT-03": "F-024",
    })
    gate_by_story = {s["id"]: s["gate"].split(".")[0] for s in STORIES}
    for tid in ordered:
        fixture, _steps, pos, neg = ORACLES[tid]
        intent = intent_map.get(tid, "supplementary control; not one of the 17 FDP-13 P0 lines")
        rows.append(
            f"| {tid} | {intent} | {primary[tid]} | {also.get(tid, '—')} | {fixture} | {pos} | {neg} | test-run id, commit, policy_version, artifact hash — all ABSENT | {gate_by_story[primary[tid]]} | NOT RUN |"
        )
    story_index = "\n".join(
        f"| {s['id']} | {s['pri']} | {s['sprint']} | {', '.join(s['tests'])} |" for s in STORIES
    )
    footer = f"""
## Story index (not a second oracle)
| Story | Priority | Sprint | Test ids |
|---|---|---|---|
{story_index}

COST-01 appears once, primary story F-015. F-021's id is COST-DASH-01 only.
"""
    return header + "\n".join(rows) + "\n" + footer


def main():
    write(PLAN / "FDP-16A-v1.2-EXECUTION-CONTRACTS.md", contracts())
    write(PLAN / "FDP-16-v1.2-AIOX-EXECUTION-ENGINES.md", fdp16())
    write(PLAN / "FDP-17-v1.2-TESTING-STRATEGY.md", fdp17())
    write(PLAN / "FDP-18-v1.2-DEPLOYMENT-ROLLBACK.md", fdp18())
    write(PLAN / "FDP-18A-v1.2-RECOVERY-RUNBOOKS.md", fdp18a())
    write(PLAN / "FDP-19-v1.2-PRODUCT-BACKLOG.md", fdp19())
    write(PLAN / "FDP-19A-v1.2-STORY-ACCEPTANCE-REGISTER.md", fdp19a())
    write(PLAN / "FDP-20-v1.2-SPRINT-IMPLEMENTATION-PLAN.md", fdp20())
    write(PLAN / "FDP-TRACEABILITY-MATRIX-v1.2-CANONICAL.md", matrix())
    # dump story titles for the checker
    (PLAN / "_stories.json").write_text(json.dumps([{k: s[k] for k in ("id", "pos", "neg", "tests")} for s in STORIES]), encoding="utf-8")


if __name__ == "__main__":
    main()
