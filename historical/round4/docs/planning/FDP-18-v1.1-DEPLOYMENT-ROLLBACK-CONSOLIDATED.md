# IA OS Forge — FDP-18 v1.0 — Deployment / Rollback
**Status: CONSOLIDATED DRAFT v1.1 — INDEPENDENT REVIEW PENDING; NOT APPROVED. REVISED DRAFT — INDEPENDENT REVIEW PENDING.** This is a specification, not permission for production execution.

## 1. Frozen MVP stack (FDP-10)
Tauri 2; React/TypeScript/Vite; Node/TypeScript sidecar; tldraw; Supabase PostgreSQL/Auth/RLS/Storage; Supabase Queues/PGMQ; Git/worktrees; Fastify; Cloud Run; OpenTelemetry; n8n; Codex + Claude Code. Preparados P1: Grok, OpenRouter e remote build workers. Adiados: Temporal, Neo4j, Redis/BullMQ, Kafka e Kubernetes. Tauri Stronghold permanece mecanismo de segredos local.

Nenhuma escolha congelada e reaberta por ADR de parametros. Substituicao exige Change Decision e aprovacao do Founder.

## 2. Separation of environments and duties
DEV, STAGING and PROD are isolated by identity, secrets, storage, network and data classifications. Staging uses synthetic data. Coding Engine may generate release candidate artifacts, but only separate Release Agent can invoke publishing/deployment capabilities, subject to authenticated human hard gate. Builder, Reviewer and Approver remain separate. Release and Deployment are distinct records.

## 3. Deployment approval binding
DeploymentApproval includes approval_id, release_id, source_git_hash, artifact_digest, graph_revision, environment_id, migration_set_hash, policy_version, approved_by, approved_at, expires_at, purpose, scope, revocation_state and consumed_at. Verify exact tuple at side-effect time: no replay, wrong environment, changed image/release/graph/migration, stale approval or policy mismatch. Material changes invalidate approval; attempts to bypass trigger audit and deny. User approval of plan does not approve release or deployment.

## 4. Pipeline
Protected commit → reproducible build → SBOM, secret scan and static checks → FDP-17 suite → independent review → signed immutable Release → STAGING deploy → smoke, RLS, tenant, cost and health test → rollback rehearsal → human production approval bound to artifact → canary/rollout controlled by Release Agent. No implicit pushes or production migrations.

## 5. Operational runbooks
### RB-APP (cloud app)
Detector: error budget breach/failed staging smoke or post-rollout health threshold; threshold measured and approved in staging. Owner Release Operator. Action: stop rollout and drain traffic; revert to prior immutable image while protecting DB compatibility. Verify health probes, tenant isolation, API smoke and audit continuity. Record release hashes, timestamps, metrics and approving actor.
### RB-SCHEMA (migration)
Detector: migration integrity/RLS failure or incompatibility. Owner DB Operator and Security Reviewer. Freeze writes and revoke migration capability. Use expand/contract and forward recovery by default; restore only from verified backups with authorized destructive gate. Check integrity, indexes, tenant/RLS, data reconciliation and audit. Preserve migration_set_hash.
### RB-RUNNER (lease loss)
Detector: watchdog expired lease/fencing epoch. Owner Execution Operator. Revoke old tool grants; confirm operation ledger/external side effects; create a fresh Attempt only after reconciliation and checkpoint validation. Verify no duplicated effects.
### RB-DESKTOP (signed updater)
Detector: signature invalid, boot smoke failed or journal inconsistent. Owner Desktop Operator. Block package and recover previous verified signed version; journal reconciliation without privileged IPC bypass. Verify local project root, saved state and audit sync.
### RB-SECRET (credential exposure)
Detector: secret scan, unexpected egress or expired credential. Owner Security Operator. Revoke/rotate scoped refs, invalidate sessions and evaluate exposure. Verify previously issued credential cannot access resources; create incident record.

## 6. Measurability
For every runbook record runbook_version, detection signal, measured baseline, approved threshold, observation window, responder role/oncall routing, evidence ID, recovery step, return-to-service check, rollback/forward-fix branch, test date and outcome. RPO/RTO are measured from rehearsal, not invented. Critical exceptions require authenticated decision. No runbook is certified until drilled in STAGING.

## 7. Recovery controls
Backups are tested, immutable releases retained, feature flags/kill switches available, staging restore repeated, schema/app compatibility matrix maintained. PROD deployment blocked if approval replay test, backup restore, tenancy/RLS tests, checksum verification or audit writer test fails. Release Agent cannot override an independent review FAIL.

## 8. Gate
Pending independent review, staging rehearsal, environment isolation evidence and Founder authorization per actual production release. No BUILD-00 authorization.
