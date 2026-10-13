# IA OS Forge — FDP-18 v1.2 — Deployment and Rollback
Status: ROUND 5 — CANDIDATE FOR INDEPENDENT REVIEW. DRAFT / NOT APPROVED / NOT READY FOR BUILD / NO BUILD-00 AUTHORIZATION. No tests executed. No staging drills executed. No Founder approval inferred.
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
