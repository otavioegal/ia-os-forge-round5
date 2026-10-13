<!--
Extrato literal de docs/source-material/chats/ChatGPT-IA-OS-FORGE-2026-10-10.json
Mensagem [74] do ramo atual (assistente), 2026-10-08 18:25 UTC.
Título no ChatGPT: "FDP-12 v1.0 — Data Architecture | IA OS Forge"
Conteúdo copiado sem edição: bloco :::writing (sem o invólucro).
Status: EXTRACTED — validação do Founder pendente.
-->

# IA OS FORGE
## FDP-12 v1.0 — DATA ARCHITECTURE

**Protocolo:** Forge Definition Protocol — FDP  
**Documento:** FDP-12  
**Produto:** IA OS Forge  
**Versão:** 1.0  
**Status:** DRAFT → REVIEW  
**Pré-requisitos:** FDP-00 a FDP-11 — APPROVED  
**Próxima etapa:** FDP-13 — Security Architecture

---

# 1. OBJETIVO

Definir a arquitetura de dados do Forge MVP.

Este documento estabelece:

- modelo de tenancy;
- organizações e usuários;
- projetos;
- ambientes;
- Project Graph;
- Project Memory;
- requirements;
- decisions;
- agents;
- integrations;
- tasks;
- Task Envelope;
- checkpoints;
- tests;
- reviews;
- documentos;
- releases;
- deployments;
- audit;
- custos;
- operações;
- RLS;
- versionamento;
- índices;
- retenção;
- migrações;
- relação Cloud ↔ Desktop.

---

# 2. PRINCÍPIO CENTRAL

O Forge não terá apenas:

> “um banco onde guardamos coisas”.

O banco precisa representar:

# **O ESTADO E A HISTÓRIA DA FÁBRICA**

Ele deverá responder:

```text id="fqpmhb"
Quem pediu?
O que foi pedido?
O que foi decidido?
O que existe no projeto?
O que está sendo construído?
Quem está construindo?
O que foi testado?
O que foi revisado?
O que está publicado?
O que aconteceu?
```

---

# 3. TECNOLOGIA BASELINE

Para o MVP:

# PostgreSQL — Supabase

Utilizado para:

- domínio Forge;
- Project Graph;
- tasks;
- decisions;
- metadata;
- audit references;
- releases;
- operações.

---

# 4. PRINCÍPIOS DE MODELAGEM

### D1 — Tenant first

Todo dado empresarial deve ter owner claro.

### D2 — Project isolation

Projetos não compartilham dados implicitamente.

### D3 — Relational first

Usar tabelas e constraints antes de transformar tudo em JSON.

### D4 — JSONB where flexibility matters

Metadata variável poderá utilizar JSONB.

### D5 — Immutable where history matters

Auditoria, versões e checkpoints não devem ser sobrescritos silenciosamente.

### D6 — Explicit ownership

Toda entidade relevante possui owner lógico.

---

# 5. SEPARAÇÃO DE DOMÍNIOS

Modelo lógico:

```text id="zdaorf"
AUTH
  ↓
CORE REFERENCES
  ↓
FORGE DOMAIN
  ↓
AUDIT / OPERATIONS
```

---

# 6. SCHEMAS RECOMENDADOS

No PostgreSQL:

```text id="6h7eqw"
auth
core
forge
audit
```

Opcional posteriormente:

```text id="vkpbyw"
ops
billing
```

---

# 7. AUTH SCHEMA

Gerenciado pelo Supabase Auth.

Exemplo:

```text id="gih56m"
auth.users
```

Forge não deverá reinventar identidade.

---

# 8. CORE SCHEMA

Contém referências compartilháveis do ecossistema.

MVP:

```text id="avjc2x"
core.organizations
core.memberships
core.agent_registry
core.model_registry
core.tool_registry
```

Se o IA OS Core tornar-se serviço separado futuramente:

> esses contratos permanecem, mesmo que as tabelas saiam do banco Forge.

---

# 9. FORGE SCHEMA

É owner dos dados específicos do produto.

Principais grupos:

```text id="in2k8b"
Projects
Graph
Requirements
Decisions
Memory
Orchestration
Execution
Quality
Artifacts
Releases
Operations
Costs
```

---

# 10. AUDIT SCHEMA

Separado conceitualmente para reduzir risco de manipulação operacional.

Principal entidade:

```text id="vy48wq"
audit.audit_events
```

---

# 11. IDENTIFICADORES

Recomendação MVP:

> UUID como identificador primário.

Todos os IDs deverão ser:

- opacos;
- não sequenciais para exposição externa;
- estáveis.

---

# 12. ORGANIZATION

Tabela:

```text id="jv5dcg"
core.organizations
```

Campos principais:

```text id="baz0rr"
id
name
slug
status
settings
created_at
updated_at
```

---

# 13. MEMBERSHIP

```text id="lpcc0s"
core.memberships
```

Campos:

```text id="14zfjt"
id
organization_id
user_id
role
status
created_at
updated_at
```

---

# 14. ROLES INICIAIS

```text id="bjhxro"
OWNER
ADMIN
BUILDER
REVIEWER
APPROVER
VIEWER
```

---

# 15. PROJECT

Tabela central:

```text id="v9u1xq"
forge.projects
```

Campos:

```text id="axko8o"
id
organization_id
name
slug
description
project_depth
lifecycle_state
health_state
build_mode
current_version
graph_revision
created_by
created_at
updated_at
archived_at
```

---

# 16. PROJECT DEPTH

Valores:

```text id="ia4bjt"
LIGHT
STANDARD
FULL
```

---

# 17. BUILD MODE

```text id="mry0gf"
AUTONOMOUS
GUIDED
RESTRICTED
```

Default:

# AUTONOMOUS

---

# 18. PROJECT LIFECYCLE STATE

Valores iniciais:

```text id="d08twb"
IDEA
DISCOVERY
RESEARCH
PLANNING
DESIGN
READY_TO_BUILD
BUILDING
TESTING
REVIEWING
READY_FOR_HUMAN_TEST
ACCEPTANCE
STAGING
READY_FOR_PRODUCTION
DEPLOYING
PRODUCTION
IMPROVING
PAUSED
BLOCKED
ARCHIVED
```

---

# 19. PROJECT HEALTH

```text id="962g59"
HEALTHY
NEEDS_ATTENTION
BLOCKED
INCIDENT
```

---

# 20. PROJECT MEMBERSHIP

Opcionalmente:

```text id="1oqn8h"
forge.project_memberships
```

Utilizado quando um projeto precisar restringir permissões além da organização.

Campos:

```text id="lyysqz"
project_id
user_id
role
created_at
```

---

# 21. ENVIRONMENTS

```text id="ew5duf"
forge.environments
```

Campos:

```text id="qb7eoo"
id
organization_id
project_id
name
type
status
config
created_at
updated_at
```

---

# 22. ENVIRONMENT TYPES

```text id="9vk151"
LOCAL
DEV
TEST
STAGING
PRODUCTION
```

---

# 23. PROJECT GRAPH

O Graph terá estrutura genérica:

```text id="caeqvm"
forge.project_nodes
forge.project_edges
```

---

# 24. PROJECT NODE

Campos:

```text id="wc5tci"
id
organization_id
project_id
node_type
title
description
status
version
metadata
created_by
created_at
updated_at
deleted_at
```

---

# 25. NODE TYPES MVP

```text id="d3s41p"
BUSINESS_OBJECTIVE
REQUIREMENT
DECISION
FEATURE
AGENT
DATA_ENTITY
INTEGRATION
STORY
TASK
CODE_COMPONENT
TEST
REVIEW
RELEASE
DEPLOYMENT
```

---

# 26. PROJECT EDGE

Campos:

```text id="d95j57"
id
organization_id
project_id
source_node_id
target_node_id
relationship
metadata
created_at
deleted_at
```

---

# 27. RELATIONSHIP TYPES

```text id="no181h"
REQUIRES
IMPLEMENTS
DEPENDS_ON
USES
VALIDATED_BY
AFFECTS
INCLUDED_IN
DEPLOYED_AS
SUPERSEDES
GENERATED_FROM
```

---

# 28. EDGE CONSTRAINT

Source e target deverão pertencer ao:

> mesmo projeto,

salvo contratos explicitamente definidos no futuro.

Isso evita relações cross-project acidentais.

---

# 29. GRAPH REVISION

Tabela:

```text id="m1ts74"
forge.graph_revisions
```

Campos:

```text id="ncjz11"
id
project_id
revision_number
reason
created_by
created_at
```

---

# 30. GRAPH CHANGE SET

```text id="cpc8un"
forge.graph_changes
```

Relaciona alterações a uma revision.

Campos:

```text id="27hjri"
revision_id
entity_type
entity_id
operation
before_state
after_state
```

---

# 31. GRAPH SNAPSHOT

Para marcos importantes:

```text id="b7143f"
forge.graph_snapshots
```

Exemplos:

- Plan Approved;
- Build Start;
- Ready for Human Test;
- Release.

---

# 32. NÃO SNAPSHOTAR TUDO INDISCRIMINADAMENTE

Snapshots completos deverão ser reservados para marcos.

Alterações comuns:

> revisions + change sets.

---

# 33. DOMAIN TABLES + GRAPH

O Project Graph não substituirá todas as tabelas específicas.

Exemplo:

```text id="i4tl74"
forge.requirements
```

possui dados próprios e aponta para:

```text id="f6m859"
project_nodes.id
```

---

# 34. PADRÃO

```text id="k0u1go"
DOMAIN ENTITY
      ↕
GRAPH NODE
```

Domain table guarda profundidade funcional.

Graph guarda relações transversais.

---

# 35. REQUIREMENTS

```text id="u60d0s"
forge.requirements
```

Campos:

```text id="de0rnp"
id
organization_id
project_id
graph_node_id
requirement_key
type
title
description
priority
risk_level
status
acceptance_criteria
source
version
created_at
updated_at
```

---

# 36. REQUIREMENT TYPES

```text id="ahfvw6"
BUSINESS
FUNCTIONAL
NON_FUNCTIONAL
UX
AI
COMPLIANCE
SECURITY
```

---

# 37. PRIORITY

```text id="r5cfhv"
P0
P1
P2
```

---

# 38. DECISIONS

```text id="ohsysp"
forge.decisions
```

Campos:

```text id="53c4ab"
id
organization_id
project_id
graph_node_id
decision_type
title
context
recommendation
status
risk_level
created_by
resolved_by
created_at
resolved_at
```

---

# 39. DECISION OPTIONS

```text id="e1eaht"
forge.decision_options
```

Campos:

```text id="059kmy"
decision_id
label
description
impact
risk
recommended
```

---

# 40. APPROVALS

```text id="gspbdc"
forge.approvals
```

Campos:

```text id="27sc9a"
id
decision_id
project_id
actor_id
approval_type
decision
comment
created_at
```

---

# 41. APPROVAL VALUES

```text id="h2iw9i"
APPROVED
REJECTED
CANCELLED
```

---

# 42. PROJECT MEMORY

```text id="sd4ezw"
forge.memory_entries
```

Campos:

```text id="2k3gks"
id
organization_id
project_id
type
title
summary
content
source_type
source_id
importance
created_at
superseded_by
```

---

# 43. MEMORY TYPES

```text id="qup0it"
DECISION
LEARNING
CONSTRAINT
ASSUMPTION
INCIDENT
FEEDBACK
CONTEXT
```

---

# 44. CHAT NÃO É MEMORY

Mensagens completas ficarão separadas.

Project Memory deverá conter:

> informação consolidada útil ao projeto.

---

# 45. ORCHESTRATOR THREADS

```text id="d0dqno"
forge.threads
```

Campos:

```text id="0pglif"
id
project_id
type
created_at
```

---

# 46. MESSAGES

```text id="1npy9j"
forge.messages
```

Campos:

```text id="qzgfel"
id
thread_id
project_id
role
message_type
content
metadata
created_at
```

---

# 47. MESSAGE ROLES

```text id="ffg5p3"
USER
ORCHESTRATOR
SYSTEM
AGENT
```

---

# 48. DOCUMENTS

```text id="4vyaql"
forge.documents
```

Campos:

```text id="cvo9fa"
id
project_id
document_type
title
status
current_version_id
created_at
updated_at
```

---

# 49. DOCUMENT VERSIONS

```text id="bdrr05"
forge.document_versions
```

Campos:

```text id="hwzxkv"
id
document_id
version
content_location
content_hash
source
created_by
created_at
```

---

# 50. DOCUMENT STATUS

```text id="qcuwt5"
DRAFT
CURRENT
STALE
SUPERSEDED
ARCHIVED
```

---

# 51. ARTIFACT REGISTRY

```text id="22zwig"
forge.artifacts
```

Para:

- diagrams;
- screenshots;
- reports;
- test evidence;
- review files;
- generated files.

Campos:

```text id="e0xoe3"
id
project_id
artifact_type
name
storage_location
content_hash
metadata
created_at
```

---

# 52. ARTIFACT LINKS

```text id="mq3a42"
forge.artifact_links
```

Relaciona artifact a:

- task;
- test;
- review;
- release;
- decision.

---

# 53. AGENTS

O Core possui Agent Registry.

Forge armazenará apenas uso/configuração contextual.

```text id="nchfqc"
forge.project_agents
```

---

# 54. PROJECT AGENT

Campos:

```text id="eagnu9"
id
project_id
agent_registry_id
role
version
config
status
created_at
```

---

# 55. INTEGRATIONS

```text id="gh0t40"
forge.integrations
```

Campos:

```text id="n8zfoi"
id
organization_id
project_id
integration_type
provider
status
credential_reference
environment_scope
config
created_at
updated_at
```

---

# 56. CREDENTIAL_REFERENCE

Somente referência.

Nunca:

> secret bruto.

---

# 57. STORIES

```text id="lvc9iu"
forge.stories
```

Campos:

```text id="7ht2j6"
id
project_id
graph_node_id
story_key
title
description
priority
status
acceptance_criteria
created_at
updated_at
```

---

# 58. TASKS

Tabela fundamental:

```text id="adjdjq"
forge.tasks
```

Campos:

```text id="xtzdbv"
id
organization_id
project_id
graph_node_id
story_id
parent_task_id
task_type
title
objective
status
priority
risk_level
assigned_agent_role
preferred_engine_id
current_attempt_id
progress_weight
created_at
updated_at
started_at
completed_at
```

---

# 59. TASK DEPENDENCIES

```text id="glcr5t"
forge.task_dependencies
```

Campos:

```text id="bz8pwt"
task_id
depends_on_task_id
dependency_type
```

---

# 60. DEPENDENCY TYPES

```text id="m7z3hs"
BLOCKS
REQUIRES
OPTIONAL
```

---

# 61. TASK STATUS

```text id="4v3kaf"
QUEUED
READY
RUNNING
WAITING
RETRYING
HANDOFF
REVIEWING
BLOCKED
COMPLETED
FAILED
CANCELLED
```

---

# 62. TASK ENVELOPE

O Task Envelope será composto por dados de várias tabelas, não necessariamente uma coluna gigante.

View lógica:

```text id="32807v"
Task
+
Requirements
+
Dependencies
+
Context
+
Attempt
+
Files
+
Tests
+
Checkpoint
```

---

# 63. TASK CONTEXT

Dados variáveis:

```text id="nirphr"
forge.task_context
```

Campos:

```text id="pt01fh"
task_id
context_type
reference_type
reference_id
priority
metadata
```

---

# 64. TASK ATTEMPTS

Cada execução:

```text id="aqi3hp"
forge.task_attempts
```

Campos:

```text id="e2epcm"
id
task_id
attempt_number
agent_id
engine_id
model_id
status
started_at
ended_at
failure_type
failure_reason
cost
metadata
```

---

# 65. POR QUE ATTEMPT SEPARADO

Uma Task pode passar por:

```text id="9652ph"
Claude Code
↓ fail
Codex
↓ complete
```

A Task continua sendo uma.

Attempts são vários.

---

# 66. ENGINE HANDOFF

Não altera ID da Task.

Cria:

> novo attempt.

E registra:

```text id="jt5mxw"
HANDOFF event
```

---

# 67. CHECKPOINTS

```text id="sqifup"
forge.task_checkpoints
```

Campos:

```text id="zzs2tx"
id
task_id
attempt_id
checkpoint_type
git_ref
graph_revision
test_state
next_action
metadata
created_at
```

---

# 68. CHECKPOINT TYPES

```text id="uqfoh4"
AUTO
MILESTONE
PRE_HANDOFF
PRE_MERGE
PRE_RISKY_ACTION
MANUAL
```

---

# 69. TASK EVENTS

```text id="87wmw2"
forge.task_events
```

Append-oriented.

Exemplos:

```text id="g4tclj"
STARTED
PROGRESS
TEST_FAILED
RETRY
HANDOFF
CHECKPOINT
REVIEW_STARTED
COMPLETED
```

---

# 70. TEST DEFINITIONS

```text id="0fsuh6"
forge.tests
```

Campos:

```text id="9e99d6"
id
project_id
graph_node_id
test_key
type
title
target_type
target_id
criticality
created_at
```

---

# 71. TEST TYPES

```text id="q6v5zc"
UNIT
INTEGRATION
E2E
AUTHORIZATION
SECURITY
AGENT
REGRESSION
CONTRACT
```

---

# 72. TEST RUNS

```text id="vy8zzd"
forge.test_runs
```

Campos:

```text id="khtvlu"
id
project_id
task_id
release_id
environment_id
status
started_at
ended_at
summary
artifact_id
```

---

# 73. TEST RESULTS

```text id="byjyzr"
forge.test_results
```

Campos:

```text id="izt4nc"
test_run_id
test_id
status
duration_ms
message
evidence_artifact_id
```

---

# 74. REVIEW

```text id="8mf5di"
forge.reviews
```

Campos:

```text id="44kimz"
id
project_id
graph_node_id
review_type
target_type
target_id
reviewer_agent_id
reviewer_engine_id
status
started_at
completed_at
summary
```

---

# 75. REVIEW TYPES

```text id="zlrxas"
INDEPENDENT
SECURITY
ARCHITECTURE
QUALITY
RELEASE
```

---

# 76. FINDINGS

```text id="1r58xu"
forge.findings
```

Campos:

```text id="8qz726"
id
project_id
review_id
finding_type
severity
title
description
target_type
target_id
status
resolution
created_at
resolved_at
```

---

# 77. SEVERITY

```text id="67arfy"
INFO
LOW
MEDIUM
HIGH
CRITICAL
```

---

# 78. FINDING STATUS

```text id="6kxe42"
OPEN
FIXING
RESOLVED
ACCEPTED_RISK
DISMISSED
```

HIGH/CRITICAL:

> não podem simplesmente desaparecer.

---

# 79. REPOSITORY

```text id="3v2kvw"
forge.repositories
```

Campos:

```text id="df8jf8"
id
project_id
provider
remote_reference
default_branch
local_path_reference
created_at
```

Cloud não precisa armazenar path local real quando inadequado.

---

# 80. CODE COMPONENT

O Graph poderá referenciar:

```text id="og6t4d"
forge.code_components
```

Campos:

```text id="nb46ca"
id
project_id
graph_node_id
repository_id
component_type
logical_path
metadata
```

---

# 81. NÃO INDEXAR CADA LINHA DE CÓDIGO

Granularidade:

- module;
- service;
- package;
- major component.

---

# 82. RELEASES

```text id="pf4k2v"
forge.releases
```

Campos:

```text id="00jmxq"
id
project_id
graph_node_id
version
status
source_git_ref
graph_revision
created_at
approved_at
```

---

# 83. RELEASE STATUS

```text id="0v5d54"
DRAFT
CANDIDATE
APPROVED
DEPLOYED
SUPERSEDED
ROLLED_BACK
```

---

# 84. RELEASE ITEMS

```text id="5bkhoz"
forge.release_items
```

Relaciona Release a:

- features;
- stories;
- fixes;
- migrations.

---

# 85. DEPLOYMENTS

```text id="lpzzmi"
forge.deployments
```

Campos:

```text id="q5xo6h"
id
project_id
graph_node_id
release_id
environment_id
status
provider
external_reference
started_at
completed_at
health_status
rollback_of
```

---

# 86. DEPLOYMENT STATUS

```text id="ehfktq"
QUEUED
DEPLOYING
VERIFYING
SUCCESS
FAILED
ROLLING_BACK
ROLLED_BACK
```

---

# 87. DEPLOYMENT EVENTS

```text id="eqb6sa"
forge.deployment_events
```

Para timeline detalhada.

---

# 88. OPERATIONS

MVP:

```text id="eh2dtu"
forge.operational_metrics
forge.incidents
forge.improvement_proposals
```

---

# 89. OPERATIONAL METRICS

Não armazenar telemetria massiva diretamente na tabela do produto.

Guardar:

- agregados;
- referências;
- KPIs essenciais.

Telemetria bruta pode residir no backend de observabilidade.

---

# 90. INCIDENTS

```text id="utwlxm"
forge.incidents
```

Campos:

```text id="9zhwt7"
id
project_id
environment_id
severity
title
status
detected_at
resolved_at
summary
```

---

# 91. IMPROVEMENT PROPOSALS

```text id="66zfql"
forge.improvement_proposals
```

Origem:

- metric;
- incident;
- user feedback;
- agent observation.

Pode posteriormente gerar:

> Requirement / Change Request.

---

# 92. CHANGE REQUESTS

```text id="4fhx5i"
forge.change_requests
```

Campos:

```text id="uqwkl2"
id
project_id
source
title
description
impact_level
scope_classification
status
created_at
```

---

# 93. CHANGE REQUEST → GRAPH

Mudança aprovada deverá gerar ou atualizar:

- requirement;
- decision;
- affected nodes;
- stories/tasks.

---

# 94. BUDGETS

```text id="7navw5"
forge.budgets
```

Escopo possível:

- project;
- build;
- operation.

Campos:

```text id="u8gzn7"
id
project_id
budget_type
soft_limit
hard_limit
currency
period
```

---

# 95. USAGE RECORDS

```text id="lrfyf7"
forge.usage_records
```

Campos:

```text id="8x7qrf"
project_id
task_id
attempt_id
provider
resource_type
quantity
unit
estimated_cost
recorded_at
```

---

# 96. COST NÃO PRECISA SER 100% EXATO NO MVP

Mas arquitetura deve permitir:

> atribuição por projeto/task.

---

# 97. AUDIT EVENTS

```text id="kjg798"
audit.audit_events
```

Campos:

```text id="26eedo"
id
organization_id
project_id
actor_type
actor_id
action
resource_type
resource_id
authorization
result
trace_id
metadata
created_at
```

---

# 98. AUDIT É APPEND-ONLY

Usuários comuns:

> não UPDATE.

> não DELETE.

---

# 99. ACTOR TYPES

```text id="53i9qk"
USER
AGENT
ENGINE
SERVICE
SYSTEM
```

---

# 100. AUDIT × TASK EVENTS

Não são iguais.

### Task Events

Explicam execução da task.

### Audit Events

Explicam ação relevante de segurança/governança.

Alguns eventos gerarão ambos.

---

# 101. AGENT REGISTRY

Core:

```text id="jpw6ql"
core.agent_registry
```

Campos conceituais:

```text id="kwvjhl"
id
owner_product
role
version
capabilities
policy_profile
status
```

---

# 102. MODEL REGISTRY

```text id="ge4zo7"
core.model_registry
```

Campos:

```text id="bwpoue"
id
provider
model_key
capabilities
privacy_class
cost_metadata
status
```

---

# 103. TOOL REGISTRY

```text id="bxj3s1"
core.tool_registry
```

Campos:

```text id="z0nff3"
id
provider
tool_key
capabilities
risk_class
status
```

---

# 104. ENGINE REGISTRY

Embora Execution Router permaneça Forge:

```text id="2b1j80"
forge.engine_registry
```

MVP:

- Codex;
- Claude Code;
- Grok placeholder;
- AIOX runner.

---

# 105. ENGINE FIELDS

```text id="jm5f9v"
id
engine_key
adapter
capabilities
minimum_version
status
metadata
```

---

# 106. ENGINE HEALTH

Cloud pode guardar último estado conhecido:

```text id="yd989d"
forge.engine_health
```

Mas o estado local real vem do Desktop Runtime.

---

# 107. LOCAL SQLITE

Desktop manterá banco local pequeno.

Não duplicará todo PostgreSQL.

---

# 108. LOCAL TABLES

Sugestão:

```text id="mi2dye"
runner_sessions
runner_journal
pending_sync_events
local_checkpoints
engine_health_cache
preview_processes
```

---

# 109. LOCAL JOURNAL

Serve para sobreviver a:

- restart do Desktop;
- perda temporária de Cloud;
- crash do sidecar.

---

# 110. LOCAL DATA PRINCIPLE

Guardar localmente apenas o necessário para:

> continuidade e experiência.

Não criar segundo banco completo do Forge.

---

# 111. SYNC MODEL

Cloud permanece source of truth do projeto.

Local runtime mantém:

> execution state temporário.

---

# 112. SYNC EVENT

Exemplo:

```text id="dwbsm3"
task_progress_changed
checkpoint_created
engine_health_changed
preview_started
```

---

# 113. CONFLICT RESOLUTION

Casos simples:

> server wins / latest valid state.

Casos críticos:

> reconciliation baseada em state machine.

Não utilizar last-write-wins indiscriminadamente.

---

# 114. STATE MACHINES

Estados críticos deverão ter transições controladas no backend.

Exemplo:

```text id="gpbuva"
READY
→ RUNNING
→ COMPLETED
```

Não:

```text id="bov7x3"
COMPLETED
→ RUNNING
```

sem ação explícita de reopen/retry.

---

# 115. DATABASE FUNCTIONS / SERVICES

Mudanças críticas deverão passar por:

- domain service;
- RPC/function específica quando útil;
- transaction.

Evitar updates ad hoc.

---

# 116. TRANSACTIONS

Exemplo de conclusão de task:

Em uma transação:

1. validar estado;
2. validar evidência;
3. marcar attempt;
4. marcar task;
5. atualizar Graph;
6. criar event.

---

# 117. CONSISTENCY FIRST

Evitar estados como:

```text id="fc7l5m"
Task COMPLETED
Tests missing
Graph still IN_PROGRESS
```

---

# 118. RLS — PRINCÍPIO

Toda tabela tenant-scoped deverá usar:

# ROW LEVEL SECURITY

quando exposta através da camada Supabase.

---

# 119. RLS CONTEXT

A política precisa considerar:

```text id="3ef38q"
authenticated user
organization membership
project membership
role
```

---

# 120. REGRA PADRÃO

Usuário só vê registros cuja:

```text id="zb072h"
organization_id
```

pertença a uma organização da qual é membro.

---

# 121. PROJECT-LEVEL OVERRIDE

Se existir `project_memberships`:

> projeto pode restringir acesso além da organização.

---

# 122. SERVICE WORKERS

Workers cloud utilizarão identidade de serviço própria.

Não deverão se passar por:

> usuário comum.

---

# 123. SERVICE ROLE

Chaves privilegiadas:

> somente backend controlado.

Nunca:

- Desktop;
- React;
- coding agent.

---

# 124. CODING ENGINES

Codex/Claude Code não recebem credencial de banco Cloud global.

Quando precisarem interagir:

> capability/adapter escopado.

---

# 125. RLS — PROJECT GRAPH

Nodes/edges:

> somente membros autorizados do mesmo projeto.

---

# 126. RLS — AUDIT

Usuários autorizados:

> SELECT conforme papel.

Insert:

> serviço/audit function.

Update/Delete:

> bloqueado para uso normal.

---

# 127. RLS — COST

Apenas papéis autorizados podem visualizar custo detalhado.

Simple View poderá receber agregado.

---

# 128. DATA CLASSIFICATION

Campos e entidades poderão carregar:

```text id="5pv441"
PUBLIC
INTERNAL
CONFIDENTIAL
SENSITIVE
SECRET
```

---

# 129. SECRET DATA

Não deverá ser armazenado em tabelas normais do Forge.

Guardar:

> credential_reference.

---

# 130. METADATA JSONB

Usar para:

- adapter config não sensível;
- capabilities;
- atributos opcionais;
- vendor-specific metadata.

---

# 131. NÃO USAR JSONB PARA TUDO

Campos pesquisados, relacionados ou governados frequentemente:

> colunas relacionais.

---

# 132. INDEX STRATEGY

Índices mínimos:

```text id="mb0l0h"
organization_id
project_id
status
created_at
task dependencies
graph source_node_id
graph target_node_id
```

---

# 133. COMPOSITE INDEXES

Exemplos:

```text id="7mnshf"
(project_id, status)
(project_id, node_type)
(project_id, created_at)
(task_id, attempt_number)
```

---

# 134. UNIQUE CONSTRAINTS

Exemplos:

```text id="usnlwe"
organization.slug
(project_id, requirement_key)
(project_id, story_key)
(project_id, version) for releases
```

---

# 135. FOREIGN KEYS

Usar FKs para integridade quando apropriado.

Especialmente:

- organization;
- project;
- task;
- release;
- environment.

---

# 136. SOFT DELETE

Para entidades de projeto:

> `deleted_at` quando histórico importa.

Não utilizar soft delete indiscriminadamente para:

- events;
- attempts;
- immutable records.

---

# 137. CASCADE DELETE

Evitar cascades perigosos em dados históricos.

Exclusão de projeto deverá ser:

> operação explícita governada.

---

# 138. VERSIONING

Entidades importantes terão:

- version;
- history;
- ou event/revision.

Não necessariamente todas as tabelas.

---

# 139. VERSIONAR O QUE MUDA SIGNIFICADO

Exemplos:

- requirement;
- decision;
- document;
- agent configuration;
- Graph revision;
- release.

---

# 140. NÃO VERSIONAR RUÍDO

Não precisa criar histórico completo para:

> posição de painel na UI.

---

# 141. RETENTION POLICY

Não congelar prazos exatos neste momento.

Mas categorias deverão existir:

### Permanent / long-term

- decisions;
- releases;
- audit critical;
- Project Graph history.

### Operational

- task logs;
- traces;
- raw execution output.

### Ephemeral

- caches;
- heartbeat;
- temporary preview state.

---

# 142. RETENTION CONFIG

Futuramente:

```text id="sy5dgg"
retention_policy
```

por organização/projeto/categoria.

---

# 143. RAW LOGS

Não manter indefinidamente no PostgreSQL.

Utilizar backend de observabilidade para volume alto.

Postgres guarda:

> referências/resumos importantes.

---

# 144. TELEMETRY

OpenTelemetry será source de telemetria operacional.

Forge DB guarda:

- links;
- agregados;
- eventos de negócio.

---

# 145. MIGRATIONS

Toda alteração de schema deverá utilizar migration versionada.

---

# 146. MIGRATION PRINCIPLE

Nunca:

> editar produção manualmente como procedimento normal.

---

# 147. MIGRATION FILES

Ficarão no Git.

Exemplo:

```text id="txk43i"
supabase/migrations/
```

---

# 148. MIGRATION PIPELINE

```text id="3x2csc"
DEV
 ↓
TEST
 ↓
STAGING
 ↓
PRODUCTION GATE
 ↓
PRODUCTION
```

---

# 149. DESTRUCTIVE MIGRATION

Exige:

- impacto;
- backup/rollback quando possível;
- gate;
- audit.

---

# 150. SEEDS

Teremos:

```text id="d85hjm"
seed/core
seed/demo
seed/test
```

Nunca misturar:

> dados reais do cliente.

---

# 151. MVP DEMO DATA

Customer Operations System deverá possuir dataset sintético:

- leads fictícios;
- conversas fictícias;
- appointments fictícios;
- users fictícios.

---

# 152. PII REAL

Não necessária para primeiro acceptance scenario.

---

# 153. DATABASE TESTS

Obrigatórios:

- FKs;
- constraints;
- RLS;
- cross-project isolation;
- task transitions;
- audit immutability;
- Graph relations.

---

# 154. MULTI-TENANT TEST

Tenant A tenta acessar:

> Tenant B.

Resultado:

# DENY

---

# 155. PROJECT ISOLATION TEST

Projeto A tenta ler:

> Project B

mesmo dentro da mesma organization, se política restringir.

Resultado:

> conforme membership/policy.

---

# 156. GRAPH INTEGRITY TEST

Edge aponta para node de outro projeto.

Resultado:

# REJECT

---

# 157. TASK TRANSITION TEST

Task COMPLETED recebe update direto para RUNNING.

Resultado:

# REJECT

sem operação explícita autorizada.

---

# 158. AUDIT TEST

Usuário tenta apagar audit event.

Resultado:

# DENY

---

# 159. SECRET LEAK TEST

Credential plaintext aparece em metadata.

Pipeline/security scan:

> finding.

---

# 160. PROJECT GRAPH PERFORMANCE

MVP não exige milhões de nodes.

Objetivo:

> projetos empresariais controlados.

Ainda assim índices e consultas deverão evitar scans completos desnecessários.

---

# 161. IMPACT QUERY

Fluxo:

```text id="qgsmdl"
node
 ↓
edges
 ↓
dependent nodes
 ↓
affected domains
```

Implementação inicial:

> SQL recursivo limitado.

---

# 162. MAX DEPTH

Impact analysis deverá possuir limite/configuração para evitar:

> consultas recursivas sem controle.

---

# 163. CYCLE DETECTION

Algumas relações podem permitir ciclos.

Outras não.

Exemplo:

Task dependency:

> não deve ter ciclo.

Graph genérico:

> alguns ciclos podem ser legítimos.

---

# 164. TASK DAG

Task Graph precisa ser:

# Directed Acyclic Graph

para dependências de execução.

---

# 165. CYCLE VALIDATION

Ao criar dependency:

> verificar se produz ciclo.

Se sim:

> rejeitar e gerar erro de planejamento.

---

# 166. DATA EXPORT

Arquitetura deverá permitir futuramente:

- project export;
- documents;
- Graph;
- audit permitido;
- code links.

MVP pode limitar UI.

---

# 167. DATA PORTABILITY

Um cliente não deverá ficar preso apenas porque dados estão no Forge.

Princípio:

> exportável em formatos documentados.

---

# 168. PROJECT ARCHIVE

Arquivar:

- bloqueia novas execuções;
- preserva histórico;
- não apaga imediatamente.

---

# 169. PROJECT DELETE

Operação separada de archive.

Deverá ser:

> explicitamente governada.

---

# 170. BACKUP

Supabase/Postgres backup strategy será detalhada em Deployment Architecture.

Data model deverá permitir:

> point-in-time recovery/restore conforme plano adotado.

---

# 171. DATA OWNERSHIP MATRIX

| Dado | Owner |
|---|---|
| User identity | IA OS Core/Auth |
| Organization | IA OS Core |
| Forge project | Forge |
| Project Graph | Forge |
| Tasks | Forge |
| Decisions | Forge |
| Code | Git repository |
| Secrets | Secret system |
| Tests | Forge |
| Audit | Audit domain |
| Deployment state | Forge Delivery |
| Raw telemetry | Observability system |

---

# 172. FORGE NÃO É OWNER DO CÓDIGO EM BANCO

Código fonte:

# Git

Forge guarda:

- referência;
- componentes;
- commit;
- branch/worktree.

---

# 173. FORGE NÃO É SECRET MANAGER UNIVERSAL

DB guarda:

> references.

Secrets reais:

> stores apropriados.

---

# 174. FORGE NÃO É OBSERVABILITY DATABASE

Logs volumosos:

> ferramenta de observabilidade.

Banco Forge guarda eventos relevantes.

---

# 175. DOMAIN SERVICES

Camadas principais:

```text id="12l7w9"
ProjectService
GraphService
RequirementService
DecisionService
TaskService
ReviewService
ReleaseService
DeploymentService
AuditService
```

---

# 176. UI NÃO ESCREVE DIRETAMENTE EM TABELAS CRÍTICAS

Mesmo com Supabase:

> ações de domínio passam pelo Cloud API/serviço.

---

# 177. EXCEÇÕES

Auth e alguns reads simples poderão utilizar capacidades gerenciadas diretamente quando seguro.

Mas:

> state machines não podem depender de updates diretos do browser.

---

# 178. EVENT OUTBOX — RECOMENDAÇÃO

Para eventos importantes, adotar padrão conceitual:

# Transactional Outbox

Exemplo:

na mesma transação que conclui Task:

1. update Task;
2. insert Event.

Depois worker publica/processa.

---

# 179. BENEFÍCIO

Evita:

```text id="qj8x1l"
DB mudou
mas evento se perdeu
```

---

# 180. EVENT TABLE

Pode utilizar:

```text id="jkhy06"
forge.domain_events
```

Campos:

```text id="8z5yrb"
id
aggregate_type
aggregate_id
event_type
payload
created_at
processed_at
```

---

# 181. PGMQ

Pode consumir eventos/jobs assíncronos derivados desses estados.

---

# 182. NÃO TRANSFORMAR EVENTOS EM SOURCE OF TRUTH COMPLETO

MVP não será event-sourced.

Source of truth continua relacional.

Eventos ajudam:

- audit;
- async;
- observability.

---

# 183. IDEMPOTENCY

Ações externas relevantes deverão possuir:

```text id="wk2hzb"
operation_id
```

e/ou:

```text id="bcw94t"
idempotency_key
```

---

# 184. EXEMPLO

Deployment solicitado duas vezes após retry.

Backend reconhece mesma operation:

> não publica duas releases acidentalmente.

---

# 185. UNIQUE IDEMPOTENCY

Tabela ou constraint poderá registrar:

```text id="yavj3g"
forge.operations
```

para operações críticas.

---

# 186. LOCAL ↔ CLOUD IDS

Todos os IDs importantes deverão ser gerados de forma que possam ser usados antes de sincronização, quando necessário.

UUID atende.

---

# 187. CLOCKS

Server timestamps são autoridade para eventos Cloud.

Local timestamps podem ser armazenados como observação.

---

# 188. CONCURRENCY CONTROL

Atualizações críticas poderão usar:

- version column;
- optimistic locking;
- transactions.

---

# 189. EXEMPLO

Dois processos tentam resolver mesma Decision.

Apenas um resultado válido deve vencer.

---

# 190. `updated_at` NÃO É LOCK

Entidades críticas deverão possuir:

```text id="ab0q08"
version_number
```

ou mecanismo equivalente.

---

# 191. DOCUMENT HASH

Document versions e artifacts deverão ter:

```text id="oqwhu9"
content_hash
```

para detectar alteração e duplicação.

---

# 192. GRAPH HASH — P1

Poderemos calcular hash de snapshot/revision para:

- integrity;
- cache;
- reconciliation.

Não obrigatório inicialmente.

---

# 193. DATA MIGRATION FROM MVP TO FUTURE

A arquitetura precisa suportar evolução para:

- Core separado;
- queue externa;
- graph database opcional;
- remote runners.

Sem mudar IDs lógicos das entidades principais.

---

# 194. GRAPH DATABASE FUTURO

Se impacto queries se tornarem pesadas:

```text id="j36dyb"
Postgres remains canonical
   ↓
Graph projection
   ↓
Specialized Graph Store
```

Preferível a migrar prematuramente toda verdade.

---

# 195. TEMPORAL FUTURO

Se Durable Execution se tornar complexa:

Task model atual poderá servir como:

> business state,

e Temporal como:

> execution engine.

---

# 196. DATA QUALITY

Checks automáticos deverão verificar:

- orphan records;
- invalid status;
- stale references;
- Graph inconsistencies;
- tasks without project;
- releases without revision.

---

# 197. CONSISTENCY JOB

Worker periódico poderá executar:

```text id="5tmp7b"
Project consistency check
```

e criar:

> finding

quando detectar divergência.

---

# 198. PROJECT HEALTH DATA

Health poderá derivar de:

- blocked tasks;
- critical findings;
- deployment health;
- incidents;
- engine availability.

Não será campo arbitrariamente editável.

---

# 199. DERIVED DATA

Sempre que possível distinguir:

### Canonical

dado persistente de domínio.

### Derived

percentual, health summary, dashboard aggregate.

Derived pode ser reconstruído.

---

# 200. BUILD PROGRESS

Não armazenar apenas:

```text id="dibx50"
72%
```

Fonte real:

- task weights;
- completed state;
- stage.

O percentual é derivado.

---

# 201. READY FOR HUMAN TEST

Também será derivado por rules:

```text id="dw499q"
P0 features implemented
+
critical tests pass
+
review pass
+
security pass
+
no HIGH/CRITICAL findings
+
preview ready
```

---

# 202. NÃO PERMITIR FLAG MANUAL LIVRE

Não deve existir simplesmente:

```text id="ufyzms"
ready_for_human_test = true
```

sem validação.

---

# 203. DATA ARCHITECTURE MVP — P0 TABLES

Conjunto essencial:

```text id="o84a93"
organizations
memberships
projects
environments

project_nodes
project_edges
graph_revisions

requirements
decisions
approvals
memory_entries

threads
messages
documents
document_versions
artifacts

stories
tasks
task_dependencies
task_context
task_attempts
task_checkpoints
task_events

tests
test_runs
test_results

reviews
findings

repositories
code_components

releases
deployments

audit_events
domain_events
```

---

# 204. P1 TABLES

```text id="mr11yq"
project_memberships
change_requests
usage_records
budgets
engine_health
incidents
improvement_proposals
artifact_links
release_items
deployment_events
```

Algumas poderão entrar já no MVP conforme necessidade.

---

# 205. NÃO CRIAR CENTENAS DE TABELAS ANTES DA HORA

Schemas deverão nascer junto ao backlog real.

Este Blueprint define o modelo-alvo.

---

# 206. MIGRATION SEQUENCE

Ordem lógica inicial:

```text id="39k1o6"
01 core organizations
02 memberships
03 projects/environments
04 Project Graph
05 requirements/decisions
06 memory/messages/documents
07 stories/tasks
08 execution attempts/checkpoints
09 tests/reviews/findings
10 repositories/code refs
11 releases/deployments
12 audit/events
13 RLS
14 indexes/constraints
15 seed/test data
```

---

# 207. SECURITY VALIDATION ANTES DE SEED REAL

RLS e isolation tests devem estar ativos antes de qualquer dado real de cliente.

---

# 208. CRITÉRIOS DE SUCESSO

A Data Architecture estará correta se conseguirmos responder via dados:

> Quem é o dono deste projeto?

> O que este requisito implementa?

> Quais tasks ainda faltam?

> Qual engine executou?

> Houve handoff?

> Quais testes validam esta feature?

> Quais findings estão abertos?

> Qual versão foi publicada?

> Quem aprovou produção?

> O que aconteceu ontem durante o build?

---

# 209. CENÁRIO DE CONTINUIDADE

Task T-42:

```text id="thn89o"
task T-42
  ↓
attempt 1
Claude Code
  ↓
checkpoint C-9
  ↓
attempt 2
Codex
  ↓
tests
  ↓
completed
```

Tudo rastreável sem depender do chat.

---

# 210. CENÁRIO DE TRACEABILITY

```text id="mt9hro"
Requirement R-14
 ↓ IMPLEMENTS
Feature Scheduling
 ↓ IMPLEMENTED_BY
CodeComponent scheduling-service
 ↓ VALIDATED_BY
Test T-91
 ↓ INCLUDED_IN
Release 1.0
 ↓ DEPLOYED_AS
Deployment PROD-17
```

Esse é um dos principais diferenciais do Forge.

---

# 211. CENÁRIO DE DECISION

Pagamento adiciona risco.

Banco registra:

```text id="bupr7c"
Decision
Options
Recommendation
Approval
Graph revision
Tasks generated
Audit event
```

---

# 212. CENÁRIO DE PRODUÇÃO

Nenhum deployment de produção deverá existir sem relação com:

- release;
- environment;
- approval;
- audit event.

---

# 213. CENÁRIO DE AUDITORIA

Pergunta:

> “Por que o Codex publicou isso?”

Resposta ideal:

> Ele não publicou.

Podemos demonstrar:

- Codex construiu Task;
- Reviewer validou;
- usuário aprovou Release;
- Deployment Agent publicou.

---

# 214. PRINCÍPIOS CONSOLIDADOS

### DATA-P1
Tenant first.

### DATA-P2
Project isolation by default.

### DATA-P3
Project Graph connects domain state.

### DATA-P4
Tasks survive engines.

### DATA-P5
Attempts record execution history.

### DATA-P6
Git owns code.

### DATA-P7
Secrets live outside normal project data.

### DATA-P8
Audit is append-oriented.

### DATA-P9
Production state is traceable.

### DATA-P10
Derived metrics never replace canonical state.

### DATA-P11
RLS is defense in depth, not sole authorization.

### DATA-P12
MVP stays relational first.

---

# 215. DECISÕES FROZEN DO FDP-12

1. PostgreSQL/Supabase permanece datastore principal.
2. Separação lógica `core`, `forge`, `audit`.
3. `organization_id` será base de tenancy.
4. `project_id` será base de isolamento operacional.
5. Project Graph será nodes + edges relacionais.
6. Entidades ricas terão tabelas próprias ligadas ao Graph.
7. Project Memory permanece separado de mensagens.
8. Task e Task Attempt serão entidades distintas.
9. Engine handoff cria novo Attempt, não nova Task.
10. Checkpoints persistem Git ref + state.
11. Tests/Reviews/Findings são objetos de primeira classe.
12. Releases/Deployments são separados.
13. Audit é append-oriented.
14. Secrets serão referenciados, não armazenados em plaintext.
15. RLS será obrigatório para dados tenant-scoped expostos.
16. Local SQLite será journal/cache, não source of truth.
17. Task dependencies deverão formar DAG.
18. Event Outbox é padrão recomendado.
19. MVP não será event-sourced.
20. Código continua em Git, não no banco.

---

# 216. RISCOS

## R1 — Modelo de dados grande cedo demais

Mitigação:
implementar somente tabelas exigidas pelas slices.

## R2 — JSONB virar depósito de tudo

Mitigação:
relational first.

## R3 — Graph e domain tables divergirem

Mitigação:
mutations transacionais/services.

## R4 — RLS insuficiente

Mitigação:
application authorization + RLS.

## R5 — Cross-tenant leak

Mitigação:
organization/project IDs + isolation tests.

## R6 — Audit excessivamente volumoso

Mitigação:
separar audit de raw telemetry.

## R7 — Estado local divergir da Cloud

Mitigação:
reconciliation + explicit sources of truth.

## R8 — Handoff perder contexto

Mitigação:
Task Envelope derivado de dados persistentes.

---

# 217. PRÓXIMA ETAPA

Com aprovação:

# **FDP-13 — SECURITY ARCHITECTURE**

O FDP-07 definiu **o que queremos proteger**.

O FDP-13 definirá **como tecnicamente protegeremos**:

- Tauri capabilities;
- Desktop trust boundary;
- Node sidecar;
- filesystem;
- terminal;
- process execution;
- sandbox;
- Auth;
- JWT/session;
- RLS;
- organization isolation;
- project isolation;
- secret stores;
- credentials;
- engine permissions;
- model data policy;
- network egress;
- prompt injection;
- dependency security;
- production credentials;
- Cloud Run IAM;
- Supabase roles;
- audit integrity;
- threat model;
- emergency stop;
- security tests.

---

# 218. GATE FDP-12

**Status recomendado:** APPROVE

Com aprovação:

```text id="djwahh"
FDP-10 ✅ Technical Architecture
FDP-11 ✅ Frontend Specification
FDP-12 ✅ Data Architecture
   ↓
FDP-13 Security Architecture
   ↓
FDP-14 Observability & Evaluation
   ↓
FDP-15 Integrations
   ↓
FDP-16 Execution Engines
   ↓
FDP-17 Testing Strategy
   ↓
FDP-18 Deployment
   ↓
FDP-19 Backlog
   ↓
FDP-20 Sprint Plan
   ↓
BUILD
```

---

# 219. PRINCÍPIO FINAL

O banco do Forge não deverá apenas guardar o resultado final.

Ele deverá preservar a **cadeia de compreensão e execução**:

> **por que construímos → o que decidimos → quem executou → o que mudou → como validamos → o que foi publicado.**

É isso que permitirá ao Forge continuar um projeto mesmo que mudem o agente, a engine, o modelo, o operador humano ou a versão da aplicação.

---

## FDP-12 — FIM
