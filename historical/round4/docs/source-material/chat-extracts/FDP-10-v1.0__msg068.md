<!--
Extrato literal de docs/source-material/chats/ChatGPT-IA-OS-FORGE-2026-10-10.json
Mensagem [68] do ramo atual (assistente), 2026-10-08 17:51 UTC.
Título no ChatGPT: "FDP-10 v1.0 — Technical Architecture | IA OS Forge"
Conteúdo copiado sem edição: bloco :::writing (sem o invólucro).
Status: EXTRACTED — validação do Founder pendente.
-->

# IA OS FORGE
## FDP-10 v1.0 — TECHNICAL ARCHITECTURE

**Protocolo:** Forge Definition Protocol — FDP  
**Documento:** FDP-10  
**Produto:** IA OS Forge  
**Versão:** 1.0  
**Status:** DRAFT → REVIEW  
**Pré-requisitos:** FDP-00 a FDP-09 — APPROVED  
**Próxima etapa:** FDP-11 — Frontend / UX Technical Specification

---

# 1. OBJETIVO

Definir a arquitetura técnica inicial capaz de implementar o MVP já aprovado.

A arquitetura deve preservar cinco propriedades:

1. experiência extremamente simples para o usuário;
2. execução autônoma;
3. continuidade entre engines;
4. segurança por design;
5. substituição futura de fornecedores sem reescrever o Forge.

---

# 2. DECISÃO ESTRUTURAL PRINCIPAL

A arquitetura será:

# **HYBRID DESKTOP + CLOUD**

```text
                    IA OS FORGE
                         │
           ┌─────────────┴─────────────┐
           │                           │
        DESKTOP                     CLOUD
           │                           │
 arquivos / Git                  identidade
 terminal                       Project Graph
 engines locais                 task state
 previews                       registries
 local runtime                  audit
 checkpoints                    sync
 secrets locais                 observability
```

O Desktop executa perto do projeto.

O Cloud mantém o estado organizacional e persistente da fábrica.

---

# 3. STACK RECOMENDADA

## Forge Desktop

**Tauri 2**

## Interface

**React + TypeScript + Vite**

## STUDIO

**tldraw SDK**

## Local Runtime

**Node.js + TypeScript sidecar**

## Cloud API

**Node.js + TypeScript + Fastify**

## Persistência Cloud

**Supabase / PostgreSQL**

## Auth

**Supabase Auth**

## Authorization

**PostgreSQL RLS + Policy Layer Forge**

## Project Graph

**PostgreSQL nodes + edges**

## Task Queue

**Supabase Queues / PGMQ**

## Artefatos

**Supabase Storage**

## Forge Cloud Runtime

**Google Cloud Run**

## Automação dos sistemas gerados

**n8n**

## Observabilidade

**OpenTelemetry**

## Código

**Git**

---

# 4. POR QUE TAURI 2

Tauri 2 utiliza frontend web dentro de WebView e backend nativo em Rust, suporta plugins e permite controlar explicitamente capacidades perigosas como shell execution. Também suporta sidecars, o que permite empacotar um runtime Node separado. citeturn812986search8turn850979search5turn514799search6

Isso atende muito bem ao Forge:

```text
UI Web
+
integração nativa
+
controle de permissões
+
CLI engines
+
filesystem
+
Git
```

---

# 5. POR QUE NÃO ELECTRON NO MVP

Electron continua tecnicamente viável e possui arquitetura madura multiprocessos. citeturn812986search3

Entretanto, a recomendação inicial é Tauri por:

- superfície de privilégio mais explícita;
- binário mais enxuto;
- melhor separação UI ↔ capacidades do sistema;
- possibilidade de manter Node em sidecar isolado.

Electron permanece alternativa de contingência.

---

# 6. ARQUITETURA DESKTOP

```text
┌─────────────────────────────────────────────┐
│                TAURI DESKTOP                │
│                                             │
│  ┌───────────────────────────────────────┐  │
│  │ React / TypeScript UI                 │  │
│  │                                       │  │
│  │ Projects                              │  │
│  │ STUDIO                                │  │
│  │ Orchestrator Chat                     │  │
│  │ Decisions                             │  │
│  │ Build Progress                        │  │
│  └──────────────────┬────────────────────┘  │
│                     │ Tauri IPC              │
│  ┌──────────────────▼────────────────────┐  │
│  │ Minimal Rust Host                    │  │
│  │ permissions / OS bridge / updater    │  │
│  └──────────────────┬────────────────────┘  │
│                     │                       │
│  ┌──────────────────▼────────────────────┐  │
│  │ Forge Local Runtime — Node/TS        │  │
│  │                                       │  │
│  │ Execution Router                     │  │
│  │ Git Manager                          │  │
│  │ Engine Adapters                      │  │
│  │ Test Runner                          │  │
│  │ Checkpoint Manager                   │  │
│  │ Local Journal                        │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

---

# 7. PRINCÍPIO DO RUST HOST

O Rust não será onde escreveremos toda a lógica do Forge.

Sua função principal será:

- shell seguro;
- filesystem;
- process lifecycle;
- secure storage;
- updater;
- IPC;
- capabilities.

A inteligência da fábrica permanece majoritariamente TypeScript.

---

# 8. NODE SIDECAR

A documentação atual do Tauri suporta explicitamente Node.js como sidecar empacotado. citeturn514799search9

Esse runtime será responsável por:

```text
Codex Adapter
Claude Code Adapter
Grok Adapter
AIOX Adapter
Git
Task execution
Tests
Build processes
Preview processes
```

---

# 9. UI NÃO EXECUTA SHELL DIRETAMENTE

Fluxo:

```text
React UI
   ↓
Tauri IPC
   ↓
Permission boundary
   ↓
Local Runtime
   ↓
Approved command
```

Nunca:

```text
Browser component
   ↓
unrestricted shell
```

---

# 10. IPC LOCAL

Recomendação MVP:

> **JSON-RPC/structured messages entre host e sidecar.**

Preferencialmente via:

- stdin/stdout;
- Tauri channels/events.

Evitar abrir servidor local desnecessário.

---

# 11. PROTOCOLO LOCAL

Mensagens conceituais:

```text
task.start
task.pause
task.resume

engine.execute
engine.cancel

git.status
git.checkpoint

test.run

preview.start
```

Todas tipadas.

---

# 12. FRONTEND

Stack:

```text
React
TypeScript
Vite
```

Com arquitetura baseada em:

- feature modules;
- typed contracts;
- state store;
- event-driven updates.

---

# 13. DESIGN SYSTEM

O Forge deverá possuir um Design System próprio.

A implementação poderá utilizar primitives maduras, mas:

> IA OS Forge deverá manter tokens e componentes próprios.

Isso permitirá consistência entre:

- Home;
- STUDIO;
- Decision Center;
- Build;
- Operations.

---

# 14. STUDIO — TLDRAW

tldraw foi validado como escolha inicial.

Sua documentação suporta:

- canvas customizável;
- shapes próprias;
- controle programático;
- agentes lendo e alterando canvas;
- conteúdo gerado por IA;
- workflows visuais. citeturn812986search0turn812986search1turn812986search7

---

# 15. STUDIO NÃO É SOURCE OF TRUTH

Fluxo:

```text
PROJECT GRAPH
      ↓
VIEW MODEL
      ↓
TLDRAW
```

Alteração estrutural:

```text
TLDRAW
 ↓
CHANGE COMMAND
 ↓
PROJECT GRAPH
 ↓
VALIDATION
 ↓
STUDIO REFRESH
```

---

# 16. PROJECT GRAPH — DECISÃO

Não introduzir Neo4j ou outro graph database no MVP.

Utilizar:

# PostgreSQL

com tabelas conceituais:

```text
project_nodes
project_edges
```

---

# 17. POR QUE POSTGRES

O Graph inicial é relativamente pequeno e estruturado.

PostgreSQL suporta consultas recursivas para navegação hierárquica e relações, inclusive detecção de ciclos e caminhos. citeturn816963search0

Logo:

> um segundo banco especializado seria complexidade prematura.

---

# 18. PROJECT NODE

Estrutura conceitual:

```text
project_nodes

id
organization_id
project_id
type
title
description
status
version
metadata jsonb
created_at
updated_at
```

---

# 19. PROJECT EDGE

```text
project_edges

id
project_id
source_node_id
target_node_id
relationship
metadata jsonb
created_at
```

---

# 20. GRAPH SERVICE

Não permitir que qualquer módulo faça consultas arbitrárias ao Graph.

Criar:

# Project Graph Service

Responsável por:

```text
createNode
updateNode
createEdge
removeEdge
queryImpact
getContext
validateGraph
snapshotGraph
```

---

# 21. GRAPH VERSIONING

Mudanças estruturais gerarão:

```text
graph_revision
```

Snapshots importantes serão associados a:

- Plan Approval;
- Build Start;
- Ready for Human Test;
- Release.

---

# 22. DATABASE

Escolha do MVP:

# Supabase PostgreSQL

A plataforma fornece PostgreSQL completo, Auth, RLS e extensões; sua documentação também recomenda RLS para proteger tabelas expostas. citeturn850979search12turn850979search3turn850979search4

---

# 23. POR QUE SUPABASE

Já existe experiência no ecossistema IA OS Company e ele reduz quantidade de infraestrutura inicial.

No MVP utilizar:

```text
Postgres
Auth
RLS
Storage
Realtime
Queues
Vault quando apropriado
```

---

# 24. SUPABASE NÃO É CONTRATO DE DOMÍNIO

O Forge utilizará repositories/services próprios.

Evitar:

```text
UI → tabela diretamente
```

para lógica crítica.

Preferir:

```text
UI
 ↓
Forge API
 ↓
Domain Service
 ↓
Database
```

---

# 25. AUTH

Supabase Auth será a solução inicial.

Fluxo desktop:

```text
Tauri
 ↓
OAuth / Login
 ↓
Supabase Auth
 ↓
JWT
 ↓
Forge Cloud
```

---

# 26. RLS

RLS funcionará como segunda camada de proteção.

Mas:

> RLS não substitui regras de domínio.

Teremos:

```text
Application authorization
+
Database RLS
```

---

# 27. TASK QUEUE

Decisão MVP:

# Supabase Queues / PGMQ

As filas atuais são Postgres-native e oferecem entrega durável, visibility windows e arquivamento. citeturn850979search0turn850979search1

---

# 28. POR QUE NÃO REDIS NO MVP

Adicionar Redis apenas para filas aumentaria:

- infraestrutura;
- secrets;
- observabilidade;
- custo;
- operação.

PGMQ permite usar o Postgres que já precisamos.

---

# 29. POR QUE NÃO TEMPORAL NO MVP

Temporal é uma plataforma robusta para Durable Execution e pode manter workflows após falhas. citeturn812986search4turn812986search6

Entretanto, no MVP já teremos:

```text
Task Graph
+
Task Envelope
+
Postgres state
+
PGMQ
+
Git checkpoints
```

Introduzir Temporal agora criaria uma segunda grande plataforma de execução.

### Decisão

> **DEFER TEMPORAL.**

Manter arquitetura preparada para futura adoção se a complexidade justificar.

---

# 30. TASK PERSISTENCE

Tabelas centrais:

```text
project_tasks
task_dependencies
task_attempts
task_checkpoints
task_artifacts
task_events
```

---

# 31. TASK SOURCE OF TRUTH

Cloud:

> estado persistente da task.

Local runtime:

> estado de execução + local journal.

Git:

> estado do código.

---

# 32. LOCAL JOURNAL

Desktop terá armazenamento local pequeno.

Recomendação:

# SQLite

para:

- process state;
- local runner state;
- pending sync;
- local cache;
- runtime recovery metadata.

Não será o banco central do Project Graph.

---

# 33. RECONCILIATION

Após restart:

```text
SQLite journal
+
Cloud Task State
+
Git
+
Project Graph
```

serão reconciliados.

---

# 34. SOURCE OF TRUTH MATRIX

| Informação | Source of Truth |
|---|---|
| Usuário | IA OS Core/Auth |
| Organização | IA OS Core |
| Projeto | Forge Cloud |
| Project Graph | PostgreSQL |
| Task state | PostgreSQL |
| Código | Git |
| Local execution | Local Journal |
| Test evidence | Artifact/Test Registry |
| Release | Forge Release Registry |
| Deployment | Deployment Registry |
| Audit | Audit Store |

---

# 35. CLOUD CONTROL PLANE

Arquitetura inicial:

```text
┌──────────────────────────────┐
│      FORGE CLOUD API         │
│      Node / Fastify          │
├──────────────────────────────┤
│ Project Service              │
│ Graph Service                │
│ Task Service                 │
│ Decision Service             │
│ JEV                          │
│ Model Router                 │
│ Tool Router                  │
│ Policy Engine                │
│ Audit                        │
└─────────────┬────────────────┘
              │
              ▼
         SUPABASE
```

---

# 36. FASTIFY

O Cloud Control Plane utilizará inicialmente:

# Node.js + TypeScript + Fastify

Motivos arquiteturais:

- mesma linguagem do runtime;
- contratos compartilháveis;
- baixo overhead;
- bom suporte a APIs e workers.

---

# 37. DEPLOY DO FORGE CLOUD

Escolha inicial:

# Google Cloud Run

Cloud Run atualmente suporta services, jobs e worker pools executados em containers gerenciados. citeturn908523search3turn908523search4

Isso atende:

- API;
- background workers;
- futuras execuções remotas.

---

# 38. CLOUD RUN TOPOLOGY

MVP:

```text
Cloud Run Service
└── Forge API

Cloud Run Worker
└── Cloud Task Worker
```

Posteriormente:

```text
Remote Build Workers
Research Workers
Evaluation Workers
```

---

# 39. BUILD LOCAL PRIMEIRO

Construção de código no MVP será preferencialmente:

# LOCAL

porque o Forge precisa:

- acessar projeto;
- Git;
- CLI engines;
- arquivos;
- ferramentas instaladas.

---

# 40. REMOTE BUILD

Será suportado arquiteturalmente, porém não é requisito P0.

Futuro:

```text
Task
 ↓
Remote Runner
 ↓
isolated environment
 ↓
Git branch
```

---

# 41. EXECUTION ROUTER

Componente lógico:

```text
ExecutionRouter
```

Interface:

```text
selectEngine(task, capabilities, policy)
execute(task)
handoff(task)
cancel(task)
```

---

# 42. ENGINE ADAPTERS

```text
CodexAdapter
ClaudeCodeAdapter
GrokAdapter
AioxAdapter
```

Nenhum domínio deverá chamar CLI diretamente.

---

# 43. CODEX / CLAUDE CODE

P0:

```text
CodexAdapter
ClaudeCodeAdapter
```

A implementação exata de comandos e capabilities será definida no FDP-16.

---

# 44. GROK

Adapter será preparado na interface.

Implementação real:

> P1 se capability disponível e estável.

---

# 45. ENGINE DETECTION

Desktop deverá detectar:

```text
installed?
authenticated?
version?
capabilities?
health?
```

Resultado alimenta o Execution Router.

---

# 46. ENGINE STATE

```text
AVAILABLE
DEGRADED
RATE_LIMITED
UNAVAILABLE
```

---

# 47. HANDOFF

```text
ENGINE A
   ↓
failure
   ↓
Task Envelope
+
Git checkpoint
+
Graph context
+
tests
   ↓
ENGINE B
```

---

# 48. GIT ARCHITECTURE

Cada Forge Project estará ligado a um Git repository.

---

# 49. MAIN WORKTREE

Representa estado integrado do projeto.

---

# 50. TASK WORKTREE

Quando paralelismo exigir:

```text
main
 ├── task-US-12
 ├── task-US-13
 └── task-US-14
```

Git suporta múltiplas worktrees associadas ao mesmo repositório. citeturn816963search4

---

# 51. WORKTREE POLICY

Criar quando:

- tarefas paralelas modificam código;
- isolamento reduz conflito.

Não criar para toda pequena operação.

---

# 52. MERGE CONTROLLER

Fluxo:

```text
Task completed
 ↓
Tests
 ↓
Review
 ↓
Merge candidate
 ↓
Merge
 ↓
Integration tests
```

---

# 53. AIOX

Será integrado através de:

```text
AioxAdapter
```

Entradas:

- story;
- acceptance criteria;
- context;
- policy.

Saídas:

- execution result;
- artifacts;
- findings;
- status.

---

# 54. AIOX NÃO ARMAZENA ESTADO CANÔNICO

Se AIOX desaparecer amanhã:

> Forge deverá continuar conhecendo o projeto.

---

# 55. JEV

Será implementado como serviço de decisão no Cloud Control Plane.

Inicialmente:

```text
rules
+
scoring
+
LLM reasoning where appropriate
```

Não será um modelo único.

---

# 56. DECISION FLOW

```text
Task
 ↓
JEV
 ├─ risk
 ├─ policy
 ├─ specialist
 ├─ model
 ├─ tool
 ├─ engine
 └─ review
```

---

# 57. MODEL ROUTER

Adapter-based:

```text
OpenRouterAdapter
OpenAIAdapter
AnthropicAdapter
XAIAdapter
GoogleAdapter
LocalModelAdapter
```

---

# 58. OPENROUTER

Continua opcional.

Nunca:

> único gateway obrigatório.

---

# 59. TOOL ROUTER

Tools registrados por capability.

Exemplo:

```text
calendar.write
database.migrate
git.commit
browser.search
deploy.application
```

---

# 60. N8N — DECISÃO IMPORTANTE

n8n será utilizado para:

> **automações de negócio dos sistemas construídos.**

Não será o motor principal de execução do próprio Forge.

---

# 61. MOTIVO

O Forge Build Controller precisa controlar:

- tasks;
- Git;
- worktrees;
- engines;
- retries;
- checkpoints;
- reviews;
- policy.

Isso é domínio central do Forge.

n8n permanece excelente adapter para workflows externos e business automation; sua documentação o posiciona justamente como plataforma para conectar APIs e automações, inclusive AI. citeturn514799search0

---

# 62. GENERATED APP STACK — MVP

Para o primeiro Customer Operations System:

```text
Frontend
React + TypeScript + Vite

Backend
Node + TypeScript + Fastify

Database/Auth
Supabase

Automations
n8n

Deployment
Cloud Run
```

---

# 63. POR QUE REUTILIZAR STACK

O mesmo ecossistema TypeScript reduz:

- contexto;
- tooling;
- número de dependências;
- complexidade dos agents;
- custo de revisão.

---

# 64. PREVIEW

Forge deverá iniciar preview local do sistema gerado.

Fluxo:

```text
Build
 ↓
Local Preview Server
 ↓
Embedded Preview
 ↓
Screens View
```

---

# 65. ARTIFACT STORAGE

Artefatos grandes/sincronizados:

# Supabase Storage

Exemplos:

- screenshots;
- reports;
- generated documents;
- build artifacts pequenos;
- review attachments.

Código permanece Git.

---

# 66. SECRETS LOCAIS

Escolha:

# Tauri Stronghold

O plugin é voltado a armazenamento seguro de secrets/keys e mantém vault criptografado. citeturn514799search3turn514799search1

---

# 67. SECRETS CLOUD

Separação:

### Platform secrets

Google Secret Manager.

### Project/integration credentials

Credential Service com referências e armazenamento seguro apropriado.

Supabase Vault pode ser utilizado para determinadas credenciais server-side; ele oferece armazenamento autenticado e criptografado. citeturn908523search0turn908523search6

---

# 68. REGRA

Nenhum frontend recebe secret bruto quando não precisa.

---

# 69. AUDIT

Tabela/event store append-oriented:

```text
audit_events
```

Campos:

```text
actor
organization
project
task
action
resource
authorization
result
timestamp
metadata
```

---

# 70. EVENT MODEL

Eventos internos:

```text
forge.project.created
forge.plan.approved
forge.build.started
forge.task.started
forge.task.completed
forge.task.failed
forge.engine.switched
forge.review.completed
forge.build.ready_for_test
forge.release.deployed
```

---

# 71. EVENT DELIVERY

No MVP:

- gravação no Postgres;
- queue para processamento assíncrono;
- realtime notification quando necessário.

Não introduzir Kafka.

---

# 72. OBSERVABILITY

Padronização:

# OpenTelemetry

OTel é vendor-neutral e cobre traces, metrics e logs. citeturn812986search2turn812986search9

---

# 73. CORRELATION IDS

Toda execução deverá carregar:

```text
organization_id
project_id
task_id
attempt_id
engine_id
trace_id
```

Assim é possível reconstruir uma execução.

---

# 74. TRACING

Exemplo:

```text
User presses Build
 ↓
BuildController
 ↓
JEV
 ↓
ExecutionRouter
 ↓
CodexAdapter
 ↓
Git
 ↓
Tests
 ↓
Reviewer
```

Um trace lógico.

---

# 75. METRICS

Pelo menos:

```text
task_duration
task_success
engine_failures
engine_handoffs
test_failures
review_findings
human_interruptions
build_cost
```

---

# 76. SECURITY BOUNDARY — DESKTOP

```text
WEBVIEW
   ↓
TAURI CAPABILITIES
   ↓
RUST HOST
   ↓
NODE RUNTIME
   ↓
SCOPED CLI
```

Tauri bloqueia comandos potencialmente perigosos por padrão até que capabilities sejam configuradas. citeturn850979search5

Isso combina diretamente com o FDP-07.

---

# 77. COMMAND ALLOWLIST

Local runtime não aceitará:

```text
arbitrary privileged command
```

sem classificação.

---

# 78. EXECUTION ENVIRONMENT

Cada task recebe:

```text
cwd
allowed paths
environment variables
allowed tools
timeout
risk
```

---

# 79. SANDBOX V1

MVP:

- project directory isolation;
- worktree;
- subprocess;
- environment allowlist;
- no elevation;
- restricted secrets.

---

# 80. SANDBOX V2

P1/P2:

- container sandbox;
- advanced network egress;
- remote isolated runner.

---

# 81. DESKTOP UPDATE

Tauri possui updater próprio para atualização do app. citeturn816963search1

Updates deverão ser:

- assinados;
- versionados;
- rollback-aware.

---

# 82. MONOREPO

Estrutura recomendada:

```text
forge/
├── apps/
│   ├── desktop/
│   ├── cloud-api/
│   └── cloud-worker/
│
├── packages/
│   ├── contracts/
│   ├── project-graph/
│   ├── orchestration/
│   ├── policy/
│   ├── registries/
│   ├── execution/
│   ├── engine-adapters/
│   ├── tool-adapters/
│   ├── observability/
│   └── ui/
│
├── templates/
│   └── customer-operations/
│
└── docs/
```

---

# 83. SHARED CONTRACTS

Pacote crítico:

```text
@forge/contracts
```

Contém:

- Task Envelope;
- Project Node;
- Project Edge;
- decisions;
- events;
- API DTOs;
- execution results.

---

# 84. CONTRATOS VERSIONADOS

Mudança incompatível exige versão.

Especialmente:

```text
Desktop ↔ Cloud
Cloud ↔ Runner
Forge ↔ IA OS Core
Forge ↔ Engine Adapter
```

---

# 85. IA OS CORE INTEGRATION

Interface mínima:

```text
IdentityClient
OrganizationClient
AgentRegistryClient
ModelRegistryClient
ToolRegistryClient
AuditClient
```

Podem inicialmente ser implementados dentro do monorepo.

---

# 86. DEPENDENCY RULE

Forge domain não importa diretamente implementação do Core.

```text
Forge
 ↓
Core Contracts
 ↓
Core Adapter
```

---

# 87. OFFLINE STRATEGY

MVP será:

# ONLINE-FIRST, LOCAL-EXECUTION

Isso significa:

- cloud é necessário para orchestration completa;
- código continua local;
- checkpoints locais permanecem;
- falhas temporárias de rede não devem corromper projeto.

Offline completo será posterior.

---

# 88. NETWORK FAILURE

Se Cloud desconectar:

```text
active safe task
→ pode chegar a checkpoint

new cloud-dependent tasks
→ wait

state
→ local journal

reconnect
→ reconcile
```

---

# 89. FAILURE RECOVERY

Ao reiniciar Forge:

```text
Load local journal
 ↓
Read Git state
 ↓
Contact Cloud
 ↓
Reconcile Tasks
 ↓
Detect abandoned attempts
 ↓
Resume safely
```

---

# 90. IDEMPOTENCY KEYS

Ações remotas importantes deverão usar:

```text
operation_id
```

para evitar duplicação após retries.

---

# 91. BUILD CONTROLLER

Será implementado como state machine explícita.

Não depender apenas de prompts.

---

# 92. BUILD STATE

```text
PLANNING
READY
RUNNING
PAUSING
PAUSED
TESTING
REVIEWING
BLOCKED
READY_FOR_HUMAN_TEST
FAILED
```

---

# 93. TASK STATE MACHINE

Transições permitidas deverão ser validadas pelo código.

Exemplo:

```text
READY
→ RUNNING
→ COMPLETED
```

ou:

```text
RUNNING
→ RETRYING
→ RUNNING
```

---

# 94. NÃO PERMITIR STATE CHAOS

Um agente não poderá escrever:

> “task completed”

diretamente no banco.

Precisa chamar:

```text
TaskService.complete(...)
```

que valida evidências.

---

# 95. EVIDENCE GATE

Para concluir task:

```text
expected artifacts?
tests required?
review required?
```

Só então:

> VERIFIED.

---

# 96. API STYLE

MVP:

# REST/JSON + typed contracts

Razão:

- simplicidade;
- tooling;
- fácil debugging;
- desktop/cloud interoperability.

Não precisamos GraphQL.

---

# 97. REALTIME

Atualizações de estado poderão utilizar canal realtime/websocket.

UI receberá:

```text
task.updated
build.progress
decision.required
review.completed
```

---

# 98. API SECURITY

Toda chamada cloud deverá incluir:

- identity;
- organization;
- project scope;
- policy enforcement.

---

# 99. GENERATED SYSTEM DEPLOYMENT

Customer Operations System será empacotado como container.

```text
React build
+
Fastify API
+
agent runtime
```

e publicado inicialmente no Cloud Run.

Banco permanece Supabase.

---

# 100. N8N

Workflow n8n será recurso externo do projeto gerado.

Forge cria/configura workflows através de adapter autorizado.

---

# 101. HUMAN TEST ENVIRONMENT

Antes de produção:

```text
Preview / Staging
```

com:

- URL isolada;
- dados fictícios/teste;
- release candidate.

---

# 102. PRODUCTION

Forge não terá credencial de produção permanentemente exposta aos coding agents.

Deploy ocorre através do:

# Release Agent / Deployment Adapter

após gate humano.

---

# 103. TEST ARCHITECTURE

Camadas:

```text
Unit
Integration
Contract
E2E
Engine Adapter
Security
Acceptance
```

---

# 104. ENGINE CONTRACT TESTS

Cada adapter deverá provar:

```text
start
capture output
cancel
failure detection
checkpoint
resume/handoff context
```

---

# 105. PROJECT GRAPH CONTRACT TESTS

Devem validar:

- edges válidas;
- project isolation;
- cycle controls quando necessário;
- impact query;
- version snapshot.

---

# 106. SECURITY TESTS

Obrigatórios:

- RLS;
- project isolation;
- unauthorized task access;
- secret leakage;
- terminal scope;
- production gate.

---

# 107. ARCHITECTURAL DECISIONS — RESUMO

## TA-001
Tauri 2 para Desktop.

## TA-002
React + TypeScript + Vite para UI.

## TA-003
Node/TypeScript sidecar para Local Runtime.

## TA-004
tldraw para STUDIO v1.

## TA-005
Supabase/PostgreSQL como datastore principal.

## TA-006
Project Graph sobre Postgres no MVP.

## TA-007
Supabase Queues/PGMQ para task queue.

## TA-008
Não usar Redis no MVP.

## TA-009
Não usar Temporal no MVP.

## TA-010
Fastify/TypeScript para Cloud API.

## TA-011
Cloud Run como deployment/runtime cloud inicial.

## TA-012
Git + worktrees para code isolation.

## TA-013
AIOX atrás de adapter.

## TA-014
Codex/Claude Code atrás de adapters.

## TA-015
OpenRouter opcional, nunca obrigatório.

## TA-016
n8n para business automation, não Forge orchestration.

## TA-017
OpenTelemetry como padrão de observabilidade.

## TA-018
Stronghold para secrets locais.

---

# 108. PRINCIPAIS BENEFÍCIOS

Essa arquitetura mantém apenas três tecnologias centrais na maior parte da lógica:

```text
TypeScript
PostgreSQL
Git
```

Rust aparece principalmente na casca segura do desktop.

Isso reduz a superfície cognitiva do MVP.

---

# 109. O QUE NÃO ESTAMOS CONSTRUINDO

Não construiremos agora:

- scheduler distribuído próprio sofisticado;
- banco graph dedicado;
- message broker Kafka;
- Redis cluster;
- Kubernetes;
- plataforma de secrets própria;
- cloud própria;
- canvas próprio;
- Git próprio;
- LLM próprio.

---

# 110. BUILD / BUY / INTEGRATE RESULTANTE

## BUILD

- Project Graph;
- Orchestrator;
- JEV policies;
- Decision Center;
- Build Controller;
- Task Graph;
- Execution Continuity;
- Change Impact;
- Forge UX.

## INTEGRATE

- Tauri;
- tldraw;
- Supabase;
- AIOX;
- Codex;
- Claude Code;
- Grok;
- n8n;
- Git;
- OpenRouter;
- Cloud Run;
- OpenTelemetry.

## BUY / MANAGED

- cloud infrastructure;
- database hosting;
- auth infrastructure;
- model APIs;
- observability backend.

---

# 111. PRINCIPAL RISCO TÉCNICO

Não é banco.

Não é frontend.

É:

# **EXECUTION CONTINUITY**

Precisamos provar que:

```text
Engine A
 ↓
partial work
 ↓
checkpoint
 ↓
Engine B
 ↓
understands context
 ↓
continues correctly
```

Esse deverá ser um dos primeiros spikes técnicos.

---

# 112. SEGUNDO RISCO

# PROJECT GRAPH SYNCHRONIZATION

Evitar divergência:

```text
Graph says X
Code says Y
```

Por isso o MVP rastreia apenas granularidade útil.

---

# 113. TERCEIRO RISCO

# DESKTOP SECURITY

Executar CLIs automaticamente exige forte boundary.

Tauri capabilities + sidecar isolado + policy engine deverão ser tratados como componentes de segurança, não conveniência.

---

# 114. QUARTO RISCO

# OVER-ENGINEERING

A arquitetura deliberadamente evita:

- Temporal;
- Neo4j;
- Redis;
- Kafka;
- Kubernetes;

no MVP.

Se métricas mostrarem necessidade, podemos adicioná-los posteriormente através dos contratos existentes.

---

# 115. SPIKES OBRIGATÓRIOS ANTES DO BUILD AMPLO

### SPIKE-01
Tauri ↔ Node sidecar ↔ streaming.

### SPIKE-02
Executar Codex por adapter.

### SPIKE-03
Executar Claude Code por adapter.

### SPIKE-04
Task Envelope + handoff real.

### SPIKE-05
Git worktree parallel task.

### SPIKE-06
Project Graph + impact query.

### SPIKE-07
tldraw ↔ Graph synchronization.

### SPIKE-08
PGMQ task claim/retry.

### SPIKE-09
Security scope do shell.

---

# 116. ARQUITETURA MACRO FINAL

```text
                         HUMAN
                           │
                           ▼
┌───────────────────────────────────────────────────────┐
│                 FORGE DESKTOP                        │
│                                                       │
│ React / TypeScript                                    │
│ STUDIO / tldraw                                       │
│ Chat / Decisions / Progress                           │
│               │                                       │
│               ▼                                       │
│ Tauri Security Host                                   │
│               │                                       │
│               ▼                                       │
│ Node Local Runtime                                    │
│ ├─ AIOX Adapter                                       │
│ ├─ Execution Router                                   │
│ ├─ Codex Adapter                                      │
│ ├─ Claude Code Adapter                                │
│ ├─ Git / Worktrees                                    │
│ ├─ Tests                                              │
│ └─ Local Journal                                      │
└───────────────────────┬───────────────────────────────┘
                        │
                        │ authenticated API
                        ▼
┌───────────────────────────────────────────────────────┐
│                FORGE CLOUD CONTROL PLANE              │
│                                                       │
│ Fastify / TypeScript                                  │
│                                                       │
│ Project Orchestrator                                  │
│ JEV                                                   │
│ Project Graph Service                                 │
│ Task Service                                          │
│ Decision Center                                       │
│ Policy Engine                                         │
│ Model Router                                          │
│ Tool Router                                           │
│ Audit / Observability                                 │
└───────────────────────┬───────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────┐
│                 SUPABASE / POSTGRES                   │
│                                                       │
│ Auth                                                  │
│ Project Graph                                         │
│ Project State                                         │
│ Task Graph                                            │
│ PGMQ                                                  │
│ RLS                                                   │
│ Storage                                               │
└───────────────────────────────────────────────────────┘
                        │
         ┌──────────────┼────────────────┐
         ▼              ▼                ▼
      Models          Tools          Cloud Run
 OpenRouter/direct     n8n           Deployment
 providers             APIs          Workers
```

---

# 117. ARQUITETURA DO SISTEMA GERADO

```text
CUSTOMER OPERATIONS SYSTEM

User
 ↓
React Frontend
 ↓
Fastify Backend
 ├─ AI Agent
 ├─ Business Rules
 ├─ Human Handoff
 │
 ├──── Supabase
 │      ├─ Auth
 │      ├─ Leads
 │      ├─ Conversations
 │      └─ Appointments
 │
 └──── n8n
        ├─ WhatsApp
        ├─ Calendar
        └─ notifications

Deployment
→ Cloud Run
```

---

# 118. STATUS DAS DECISÕES

### FROZEN PARA MVP

- Tauri 2
- React/TS
- Node/TS
- tldraw
- Supabase/Postgres
- PGMQ
- Git/worktrees
- Fastify
- Cloud Run
- OpenTelemetry
- n8n
- Codex + Claude Code

### PREPARADO / P1

- Grok
- OpenRouter
- remote build workers

### DEFER

- Temporal
- Neo4j
- Redis/BullMQ
- Kafka
- Kubernetes

---

# 119. GATE FDP-10

Para aprovação precisamos aceitar:

1. arquitetura híbrida Desktop + Cloud;
2. Tauri 2;
3. React/TypeScript;
4. Node sidecar;
5. tldraw;
6. Supabase/Postgres;
7. Graph relacional no MVP;
8. PGMQ;
9. Cloud Run;
10. Git/worktrees;
11. engine adapters;
12. n8n fora da orquestração central;
13. OpenTelemetry;
14. stack estreita;
15. Temporal/Neo4j/Redis/Kubernetes adiados.

---

# 120. PRÓXIMA ETAPA

Com aprovação:

# FDP-11 — FRONTEND / UX TECHNICAL SPECIFICATION

Vamos transformar o Frontend V0 já aprovado em especificação implementável:

- layout;
- navigation;
- STUDIO;
- sidebar;
- Project Orchestrator;
- Decision Center;
- Build screen;
- Test screen;
- Operations;
- Simple/Expert View;
- component hierarchy;
- frontend state;
- events;
- empty/loading/error states;
- interactions;
- accessibility;
- responsive behavior;
- tldraw integration;
- design tokens;
- prototype flows.

---

# 121. SEQUÊNCIA

```text
FDP-09 ✅ PRD
   ↓
FDP-10 ✅ Technical Architecture
   ↓
FDP-11 Frontend Specification
   ↓
FDP-12 Data Architecture
   ↓
FDP-13 Security Architecture
   ↓
FDP-14 Observability & Evaluation
   ↓
FDP-15 Integrations
   ↓
FDP-16 Execution Engines
   ↓
FDP-17 Testing
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

# 122. PRINCÍPIO FINAL

O Forge não deve ganhar robustez acumulando infraestrutura.

Deve ganhar robustez possuindo:

> **estado persistente + contratos claros + checkpoints + evidências + isolamento + componentes substituíveis.**

A arquitetura do MVP foi deliberadamente desenhada para que a complexidade principal esteja na **inteligência da fábrica**, e não na administração de infraestrutura.

---

## FDP-10 — FIM
