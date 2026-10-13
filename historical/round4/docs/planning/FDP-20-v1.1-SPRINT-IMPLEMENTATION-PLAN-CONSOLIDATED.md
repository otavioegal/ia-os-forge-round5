# IA OS Forge — FDP-20 v1.0 — Sprint & Implementation Plan
**Status: CONSOLIDATED DRAFT v1.1 — INDEPENDENT REVIEW PENDING; NOT APPROVED. REVISED DRAFT — INDEPENDENT REVIEW PENDING. BUILD NOT AUTHORIZED.**
**Preconditions:** formal closure of FDP-14, FDP-15, independent review of FDP-16…20, Founder approval of Planning Baseline. No dates/cost ceilings invented; capture effort evidence after spikes.
## Normative milestone and dependency table
| Phase | Work items | Required evidence | Exit gate |
|---|---|---|---|
| BUILD-00 | SPIKE-01…09 (FDP-10), architecture ADRs, mock queues, scoped lab, test fixtures | nine spike reports with hypotheses, owner, timebox, measurements and decisions; CI test scaffold | Builder review + Founder-authorized BUILD-00 |
| SPRINT-01 | Finish F-001/002/005/006/007/015/026–034; F-004 persistence skeleton for leases | Full P0 positive/negative suite, RLS isolation, stop/safe-mode, operation ledger, release denial tests | **SECURITY FOUNDATION COMPLETE** and independent PASS |
| SPRINT-02 | F-003/004/008/009/010, STUDIO System/Flow/Screens/Plan, preview | acceptance demo, plan approvals, Time to First Visual baseline, isolated preview tests | UX/security review |
| SPRINT-03 | F-011/012/014(minimal)/035/036, scoped sandbox, capability-safe adapters | Task DAG, Context Builder, rule-based JEV (or explicitly deny-by-default routing stub), adapter contracts | EXECUTION GATE and no policy bypass |
| SPRINT-04 | F-013/014(full)/016/017/037/038/039, handoff and merges | checkpoint/handoff, independent findings, Build Report, VERIFIED/RHFT | REVIEW + TEST READINESS |
| SPRINT-05 | F-018/019/041 Customer Operations demonstration and evals | vertical synthetic test, generated app health, model evals, Human Interruption Rate, Time to First Visual | PRODUCT MVP |
| SPRINT-06 | F-020/021(minimal)/029/030(full)/040 | immutable release, exact approval-binding test, signed updater, staging rollback/restore drill | RELEASE READINESS; production only after separate Founder hard gate |

**Gate rule:** SECURITY FOUNDATION COMPLETE is a blocking prerequisite before SPRINT-03 can invoke any side-effecting engine. JEV policy min or deny-by-default stub must exist before routing execution; full router may be expanded in SPRINT-04. In SPRINT-06, F-029/030 are integration and release-verification work; their mandatory security foundations were implemented/tested in SPRINT-01.

## BUILD-00 spike cards
These are planning experiments only until implementation order. Each uses fixture in isolated DEV, source commit, owner role, hypothesis, measurable success criteria, timebox approved from available staffing, report hash, decision/ADR and impact on roadmap. SPIKE-01..09 below were reconciled with the literal FDP-10 section 115. Acceptance contracts below specify planned tests; none have run.
| ID | Working hypothesis and evaluation | Owner | Evidence |
|---|---|---|---|
| SPIKE-01 | Tauri → Node sidecar → streaming | Desktop | IPC and streamed UI trace |
| SPIKE-02 | Run Codex through its engine adapter | Integration | Codex adapter contract report |
| SPIKE-03 | Run Claude Code through its engine adapter | Integration | Claude adapter contract report |
| SPIKE-04 | Task Envelope + real engine handoff | Orchestration | checkpoint/handoff report |
| SPIKE-05 | Git worktree parallel task | DevEx | concurrent isolation and merge report |
| SPIKE-06 | Project Graph + impact query | Data | graph query/impact report |
| SPIKE-07 | tldraw ↔ Graph synchronization | Frontend | bidirectional sync proof |
| SPIKE-08 | PGMQ task claim/retry | Backend | claim/retry/idempotency report |
| SPIKE-09 | Security scope of shell | Security | denied unsafe shell command report |

## Per-sprint ready/done
Before sprint: accepted stories and source requirement, scoped permissions and tenant, allowed effects, tests, owner role and rollback plan. After sprint: versioned evidence, tests green, no Critical/High open, independent reviewer, UX demonstration, traceability and audit. Security exceptions cannot bypass a hard gate by agent declaration.

## Ownership and project boundaries
Founder approves high-impact scope, budget and production; Builder engineers in sandbox after plan; Reviewer independent from Builder; Synkra AIOX orchestrates under policy. No production changes in Ethereal, ORAdv or MAJU, no credential access and no irreversible commands by default.

## Frozen stack
Tauri 2; React/TypeScript/Vite; Node/TypeScript sidecar; tldraw; Supabase/PostgreSQL/Auth/RLS/Storage; Supabase Queues/PGMQ; Git e worktrees; Fastify; Cloud Run; OpenTelemetry; n8n; Codex e Claude Code. Componentes preparados/P1: Grok, OpenRouter e remote build workers. Adiados: Temporal, Neo4j, Redis/BullMQ, Kafka e Kubernetes. Complementos como Stronghold preservam o baseline, nao revogam componentes da lista. Parameter ADRs do not reopen these choices. Technology replacement requires Change Decision and Founder gate.

## Readiness
READY FOR BUILD only after each FDP has consistent text, no Critical/High review findings, traceable tests, signed planning baseline and explicit Founder decision. READY FOR BUILD is not permission to start BUILD-00.


## Spike acceptance contracts — FDP-10 §115 (source-fidelity preserved)

Each spike must have signed owner/timebox before BUILD-00 execution, an isolated fixture and one reproducible evidence artifact. Failure is explicitly documented, not waived. All statuses NOT RUN; approval for BUILD-00 remains a separate human hard gate.

| Spike | Hypothesis / isolated fixture | Pass/Fail oracle | Dependency | Output / ADR effect |
|---|---|---|---|---|
| SPIKE-01 | Tauri / Node sidecar stream sends correlated test frames | pass if ordered data reaches desktop without privileged preview path; fail on boundary bypass | Tauri sandbox fixture | IPC trace + architecture compatibility ADR |
| SPIKE-02 | Codex engine adapter handles synthetic task | pass contract invoke/cancel/status/test; fail capability elevation | adapter harness | adapter contract report + compatibility ADR |
| SPIKE-03 | Claude Code engine adapter handles synthetic task | pass invoke/cancel/status/test; fail credential leak | adapter harness | adapter contract report + compatibility ADR |
| SPIKE-04 | Task Envelope survives checkpoint and handoff | pass same task, new attempt, stable operation_ref and no repeat effect | SPIKE-02/03 | handoff event report + envelope ADR |
| SPIKE-05 | Two tasks use separate Git worktrees | pass isolation and conflict detection; fail shared mutable writes | scoped Git repo | diff/merge trace + worktree ADR |
| SPIKE-06 | Project Graph impact query gives stable affected nodes | pass deterministic query/links and correct isolation | mock graph fixtures | query results + graph index ADR |
| SPIKE-07 | tldraw / Graph sync round-trip preserves identity | pass no lost edges and rejection of invalid changes | SPIKE-06 | sync fixture hash + conflict ADR |
| SPIKE-08 | PGMQ claim/retry respects lease/fencing | pass stale claim denied, replay deduped | disposable queue schema | transaction trace + queue ADR |
| SPIKE-09 | Shell rejects out-of-project calls | pass valid commands; fail on traversal/unsafe subprocess | sandbox runner | signed allow/deny trace + sandbox ADR |

Each SPIKE record includes assigned owner (role), approved timebox, environment, hypothesis, fixture hash, positive/negative oracle, measurements, result and decision/ADR link. This table adds acceptance contracts, not evidence that spikes have run.
