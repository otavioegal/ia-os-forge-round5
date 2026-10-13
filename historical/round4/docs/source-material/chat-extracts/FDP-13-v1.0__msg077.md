<!--
Extrato literal de docs/source-material/chats/ChatGPT-IA-OS-FORGE-2026-10-10.json
Mensagem [77] do ramo atual (assistente), 2026-10-08 18:33 UTC.
Título no ChatGPT: "FDP-13 v1.0 — Security Architecture | IA OS Forge"
Conteúdo copiado sem edição: bloco :::writing (sem o invólucro).
Status: EXTRACTED — validação do Founder pendente.
-->

# IA OS FORGE
## FDP-13 v1.0 — SECURITY ARCHITECTURE

**Protocolo:** Forge Definition Protocol — FDP  
**Documento:** FDP-13  
**Produto:** IA OS Forge  
**Versão:** 1.0  
**Status:** DRAFT → REVIEW  
**Pré-requisitos:** FDP-00 a FDP-12 — APPROVED  
**Próxima etapa:** FDP-14 — Observability & Evaluation Architecture

---

# 1. OBJETIVO

Transformar os princípios de segurança e governança já aprovados em uma arquitetura técnica executável.

O FDP-07 definiu:

> o que o Forge deve proteger e quando o humano deve intervir.

O FDP-13 define:

> como esses controles serão tecnicamente impostos.

---

# 2. PRINCÍPIO CENTRAL

A segurança do Forge não poderá depender de:

- “o agente obedecer”;
- prompts;
- boa intenção;
- convenção de equipe.

Controles críticos devem existir:

# FORA DO MODELO

```text
LLM / Agent
    ↓
Policy
    ↓
Capability Boundary
    ↓
Adapter
    ↓
Tool / Engine / Resource
```

---

# 3. PRINCÍPIO DE DEFESA EM PROFUNDIDADE

Nenhum controle isolado será considerado suficiente.

Modelo:

```text
IDENTITY
   +
AUTHORIZATION
   +
POLICY
   +
SANDBOX
   +
SCOPED CREDENTIALS
   +
RLS
   +
AUDIT
   +
REVIEW
   +
HUMAN GATES
```

---

# 4. TRUST ZONES

Arquitetura dividida em zonas:

```text
ZONE 0 — Human
ZONE 1 — Forge UI
ZONE 2 — Tauri Host
ZONE 3 — Local Runtime
ZONE 4 — Coding Engines
ZONE 5 — Forge Cloud
ZONE 6 — Data Plane
ZONE 7 — External Providers
ZONE 8 — Generated Application
ZONE 9 — Production
```

Cada transição é uma fronteira de confiança.

---

# 5. ZONE 0 — HUMAN

O humano é fonte autorizada de:

- intenção;
- aprovação;
- mudança de escopo;
- produção;
- ações irreversíveis.

Mas:

> identidade humana também precisa ser autenticada e autorizada.

---

# 6. ZONE 1 — FORGE UI

React/Tauri WebView.

Pode:

- exibir;
- solicitar ações;
- enviar comandos tipados.

Não pode diretamente:

- executar shell irrestrito;
- acessar filesystem irrestrito;
- acessar service-role key;
- acessar production credentials.

---

# 7. ZONE 2 — TAURI HOST

Responsável por:

- boundary nativa;
- IPC autorizado;
- secure storage;
- lifecycle;
- capabilities;
- updater.

Não deverá conter lógica de negócio extensa.

---

# 8. ZONE 3 — LOCAL RUNTIME

Node/TypeScript sidecar.

Responsável por:

- Git;
- worktrees;
- CLI engines;
- test runners;
- preview;
- local journal.

Opera com:

> escopo explícito por projeto/task.

---

# 9. ZONE 4 — CODING ENGINES

Exemplos:

- Codex;
- Claude Code;
- Grok.

Devem ser considerados:

# UNTRUSTED EXECUTORS WITH SCOPED CAPABILITIES

Mesmo sendo ferramentas legítimas.

---

# 10. ZONE 5 — FORGE CLOUD

Control Plane:

- Orchestrator;
- JEV;
- Policy Engine;
- Graph Service;
- Task Service;
- Decision Service;
- Audit;
- Routers.

É o principal ponto de aplicação de política global.

---

# 11. ZONE 6 — DATA PLANE

Inclui:

- PostgreSQL;
- Supabase Auth;
- Storage;
- Queues;
- secret references.

Proteção:

- RLS;
- service identities;
- schema boundaries;
- constraints;
- encryption gerenciada.

---

# 12. ZONE 7 — EXTERNAL PROVIDERS

Inclui:

- model providers;
- OpenRouter;
- GitHub;
- Google;
- n8n;
- deployment providers.

Nunca presumir confiança implícita.

---

# 13. ZONE 8 — GENERATED APPLICATION

Aplicações construídas pelo Forge são:

> conteúdo não confiável até serem validadas.

Preview nunca herda privilégios do Forge Desktop.

---

# 14. ZONE 9 — PRODUCTION

Maior nível de proteção.

Regras específicas:

- credenciais separadas;
- deploy via adapter;
- gate humano;
- rollback;
- audit;
- health checks.

---

# 15. IDENTITY ARCHITECTURE

Identidades relevantes:

```text
Human User
Organization
Service
Agent
Engine
Tool
Deployment Actor
```

---

# 16. HUMAN AUTHENTICATION

Baseline:

# Supabase Auth

Desktop obtém sessão autenticada.

---

# 17. SESSION MODEL

Sessão deverá possuir:

- user identity;
- organization context;
- expiration;
- refresh;
- revocation path.

---

# 18. DESKTOP TOKEN STORAGE

Tokens de sessão não deverão ser persistidos em plaintext.

Baseline:

> secure local storage via Tauri/Stronghold-compatible mechanism.

---

# 19. TOKEN EXPOSURE

React UI deverá receber apenas o necessário para comunicação.

Quando possível:

> lifecycle de sessão gerenciado pelo host/runtime.

---

# 20. ORGANIZATION CONTEXT

Toda requisição de domínio deverá resolver:

```text
user
+
organization
+
project
+
role
```

---

# 21. PROJECT CONTEXT

Acesso a projeto não será inferido apenas pelo ID enviado pelo cliente.

Backend sempre revalida:

> membership + policy.

---

# 22. SERVICE IDENTITIES

Serviços Cloud terão identidades próprias.

Exemplos:

```text
forge-api
forge-worker
forge-release-agent
```

---

# 23. NÃO COMPARTILHAR IDENTIDADE ENTRE SERVIÇOS

Evitar:

> uma única credencial com acesso total.

---

# 24. AUTHORIZATION LAYERS

```text
Application Policy
      +
Domain Authorization
      +
Database RLS
```

As três podem atuar simultaneamente.

---

# 25. POLICY ENGINE

Inputs:

```text
actor
organization
project
resource
action
environment
risk
data_classification
budget
context
```

Outputs:

```text
ALLOW
ALLOW_AUDIT
ALLOW_NOTIFY
REQUIRE_APPROVAL
DENY
```

---

# 26. POLICY ENFORCEMENT POINTS

Devem existir em:

1. Cloud API;
2. Local Runtime;
3. Tool Adapters;
4. Engine Adapters;
5. Deployment Adapter.

---

# 27. NÃO CONFIAR NO FRONTEND PARA BLOQUEAR

Botão escondido:

> não é controle de segurança.

Backend precisa aplicar política.

---

# 28. RLS

Baseline:

> todas as tabelas tenant-scoped expostas devem ter RLS.

---

# 29. RLS — ORGANIZATION

Usuário só acessa linha quando:

```text
membership.organization_id
=
row.organization_id
```

e papel permite.

---

# 30. RLS — PROJECT

Quando project membership existir:

> aplicar restrição adicional.

---

# 31. RLS — SERVICE OPERATIONS

Workers privilegiados não utilizarão sessão de usuário.

Usarão:

> identidade de serviço + rotas backend controladas.

---

# 32. SERVICE ROLE KEY

Nunca poderá estar em:

- React;
- Tauri UI;
- coding engine;
- repo do cliente;
- logs.

---

# 33. DATABASE PRIVILEGE SEPARATION

Idealmente:

```text
app_user
service_worker
migration_role
audit_writer
```

com privilégios distintos.

---

# 34. MIGRATION ROLE

Alteração de schema:

> credencial separada da aplicação normal.

---

# 35. PRODUCTION DATABASE

Coding engines não recebem:

> acesso direto persistente.

Se uma tarefa exige operação:

```text
Task
→ authorized capability
→ DB Adapter
→ policy
→ environment
```

---

# 36. LOCAL FILESYSTEM SECURITY

Cada projeto deverá ter:

```text
project_root
```

como boundary padrão.

---

# 37. PATH VALIDATION

Toda operação de arquivo deverá:

1. canonicalizar path;
2. verificar se permanece dentro do workspace;
3. negar path traversal;
4. registrar exceções relevantes.

---

# 38. PROIBIR PATH TRAVERSAL

Exemplos bloqueados:

```text
../../
C:\Windows\
/etc/
~/.ssh/
```

salvo capability explícita.

---

# 39. SYMLINK SECURITY

Resolver symlinks antes de validar boundary.

Objetivo:

> impedir escape indireto do workspace.

---

# 40. FILE CAPABILITIES

Exemplos:

```text
fs.read.project
fs.write.project
fs.read.artifact
fs.write.artifact
```

Não:

```text
fs.full_computer
```

por padrão.

---

# 41. TERMINAL SECURITY

Todo comando passa pelo Local Runtime.

Não permitir:

> WebView → shell bruto.

---

# 42. COMMAND MODEL

Comando deve carregar:

```text
task_id
cwd
command
args
environment
timeout
capability
risk
```

---

# 43. COMMAND CLASSIFICATION

Exemplos:

### LOW
`npm test`

### MEDIUM
`npm install package`

### HIGH
migration production

### CRITICAL
destructive system command.

---

# 44. BLOCKED COMMAND PATTERNS

Policy deverá identificar ações como:

- privilege escalation;
- deletion outside project;
- credential harvesting;
- destructive system modifications.

---

# 45. NÃO DEPENDER SÓ DE REGEX

Regex ajuda.

Mas segurança deverá combinar:

- capability;
- cwd;
- environment;
- command category;
- policy.

---

# 46. PROCESS EXECUTION

Cada processo deverá possuir:

- parent task;
- timeout;
- process ID;
- stdout/stderr capture;
- cancellation path.

---

# 47. CHILD PROCESS LIFECYCLE

Ao cancelar task:

> processos filhos devem ser encerrados de modo controlado.

---

# 48. ENVIRONMENT VARIABLES

Engine só recebe variáveis necessárias.

Evitar herdar automaticamente:

> todo ambiente do usuário.

---

# 49. ENV ALLOWLIST

Exemplo:

```text
PATH
PROJECT_ROOT
TEMP
FORGE_TASK_ID
authorized provider vars
```

---

# 50. SECRET INJECTION

Quando secret for necessário:

```text
Credential Service
   ↓
temporary scoped materialization
   ↓
process
   ↓
revoke / clear
```

---

# 51. NÃO GRAVAR SECRET EM TASK ENVELOPE

Task Envelope guarda:

> credential reference.

Não valor.

---

# 52. LOCAL SECRET STORE

Baseline:

> Stronghold-compatible encrypted vault.

Guardar:

- local auth material;
- CLI references quando necessário;
- encrypted tokens apropriados.

---

# 53. CLOUD SECRET STORE

Separar:

### Platform secrets
Cloud secret manager.

### Project credentials
Credential Service.

### Database-side encrypted references
quando aplicável.

---

# 54. CREDENTIAL SERVICE

Interface conceitual:

```text
getCapabilityCredential()
rotateCredential()
revokeCredential()
testCredential()
```

---

# 55. CREDENTIAL POLICY

Antes de fornecer credencial:

- actor autorizado?
- projeto autorizado?
- ambiente?
- capability?
- data classification?
- expiration?

---

# 56. TEMPORARY CREDENTIALS

Preferir tokens:

- temporários;
- mínimos;
- revogáveis.

---

# 57. CREDENTIAL AUDIT

Uso de credencial sensível deverá gerar:

> audit event.

---

# 58. ENGINE SECURITY

Codex/Claude Code/Grok são executores.

Nunca:

> autoridades de segurança.

---

# 59. ENGINE ADAPTER

Adapter deve controlar:

- working directory;
- context;
- allowed tools;
- environment;
- output capture;
- cancellation.

---

# 60. ENGINE CAPABILITY PROFILE

Exemplo:

```text
repository_read
repository_write
terminal
tests
git
```

---

# 61. ENGINE DOES NOT CHOOSE ITS OWN PRIVILEGES

Uma engine não poderá solicitar livremente:

> “preciso de acesso total”.

Pedido passa por:

> JEV + Policy.

---

# 62. ENGINE HANDOFF SECURITY

Ao trocar engine:

- novo attempt;
- nova autorização;
- novo context package;
- mesmos limites de task.

---

# 63. HANDOFF NÃO AMPLIA PERMISSÃO

Engine B não recebe mais acesso que Engine A apenas por assumir tarefa.

---

# 64. CONTEXT MINIMIZATION

Context Builder deverá excluir:

- secrets;
- outros projetos;
- dados desnecessários;
- arquivos fora do escopo.

---

# 65. CONTEXT CLASSIFICATION

Cada item de contexto poderá carregar:

```text
classification
source
allowed_providers
```

---

# 66. MODEL DATA POLICY

Antes de enviar conteúdo a modelo:

```text
classification
+
provider policy
+
project policy
```

---

# 67. EXEMPLO

Projeto determina:

> SENSITIVE → direct Anthropic only.

Model Router deve respeitar.

---

# 68. OPENROUTER

É provider/gateway opcional.

Projeto pode configurar:

```text
ALLOW
DENY
ONLY_FOR_PUBLIC
```

---

# 69. LOCAL MODEL FUTURO

Projetos restritos poderão usar:

> local-only path.

Arquitetura deverá suportar.

---

# 70. PROMPT INJECTION BOUNDARY

Conteúdo externo entra rotulado:

# UNTRUSTED_CONTENT

---

# 71. EXTERNAL CONTENT SOURCES

- web;
- documents;
- repos externos;
- emails;
- RAG;
- issues;
- API responses.

---

# 72. EXTERNAL CONTENT NÃO ALTERA POLICY

Nenhum texto externo poderá:

- adicionar permission;
- mudar scope;
- aprovar produção;
- autorizar gasto.

---

# 73. TOOL CALL AUTHORIZATION

Mesmo se modelo pedir:

> tool.execute(...)

Tool Router revalida política.

---

# 74. TOOL ADAPTER SECURITY

Cada adapter deverá declarar:

```text
capabilities
risk_level
data_access
environment_access
side_effects
```

---

# 75. READ VS WRITE

Capabilities distintas.

Exemplo:

```text
calendar.read
calendar.write
```

---

# 76. DESTRUCTIVE CAPABILITY

Exemplo:

```text
database.delete
deployment.destroy
```

sempre terá risk elevado.

---

# 77. EXTERNAL API ALLOWLIST

Projeto poderá ter allowlist:

- providers;
- hosts;
- domains.

---

# 78. NETWORK EGRESS — MVP

MVP deverá ao menos controlar e auditar:

- adapters conhecidos;
- engines autorizadas;
- provider endpoints principais.

---

# 79. NETWORK EGRESS — FUTURO

Container/firewall baseado em:

- host allowlist;
- protocol;
- environment;
- task.

---

# 80. SANDBOX V1

MVP:

```text
project-root isolation
worktree isolation
restricted env
no privilege elevation
scoped processes
limited credentials
```

---

# 81. SANDBOX V2

P1/P2:

- container;
- isolated network;
- ephemeral filesystem;
- disposable build runner.

---

# 82. WORKTREE SECURITY

Cada worktree ligado a:

- task;
- branch;
- permitted path.

---

# 83. MERGE SECURITY

Nenhuma task paralela deve escrever direto na branch integrada sem processo definido.

---

# 84. MERGE FLOW

```text
task worktree
→ tests
→ review
→ merge candidate
→ integration tests
→ merge
```

---

# 85. GIT SECURITY

Registrar:

- commit;
- author logical;
- task;
- attempt.

---

# 86. GIT REMOTE CREDENTIALS

Devem ser escopadas.

Não fornecer token administrativo global ao coding agent.

---

# 87. PREVIEW SECURITY

Aplicação gerada deve abrir:

> isolada do Forge host.

---

# 88. PREVIEW NÃO HERDA TAURI CAPABILITIES

Preview não pode chamar:

- filesystem;
- shell;
- secret store;

do Forge.

---

# 89. PREVIEW CONTENT SECURITY

Aplicar:

- CSP apropriada;
- origin isolation;
- sanitized embedding;
- no privileged IPC.

---

# 90. GENERATED CODE TRUST

Código produzido por IA começa como:

# UNVERIFIED

---

# 91. PROMOTION STATES

Conceitualmente:

```text
GENERATED
TESTED
REVIEWED
SECURITY_CHECKED
ACCEPTED
RELEASED
```

---

# 92. SUPPLY CHAIN

Dependência nova deverá registrar:

- package;
- version;
- source;
- task;
- reason.

---

# 93. DEPENDENCY CHECK

Pipeline deverá procurar:

- known vulnerabilities;
- suspicious packages;
- lockfile inconsistency;
- unexpected source.

---

# 94. LOCKFILE POLICY

Alterações de lockfile devem ser:

> parte explícita do diff.

---

# 95. PACKAGE SCRIPTS

Dependências podem executar install scripts.

Para pacotes desconhecidos:

> elevar atenção conforme risco.

---

# 96. TYPO-SQUATTING

Pacotes com nome muito similar a populares:

> warning/review.

---

# 97. CODE SECURITY PIPELINE

Conforme stack:

```text
lint
typecheck
dependency scan
secret scan
tests
security rules
review
```

---

# 98. SECRET SCANNING

Antes de commit/release:

> procurar tokens/chaves acidentalmente incluídos.

---

# 99. PRODUCTION BOUNDARY

Coding engines não publicam diretamente.

---

# 100. RELEASE AGENT

Deploy passa por componente especializado:

```text
Approved Release
      ↓
Release Agent
      ↓
Deployment Adapter
```

---

# 101. PRODUCTION GATE

Pré-requisitos:

- human approval;
- release candidate;
- tests;
- security;
- rollback strategy;
- valid credentials.

---

# 102. DEPLOY CREDENTIALS

Deployment Adapter recebe credencial.

Coding Engine:

> não.

---

# 103. CLOUD RUN IAM

Cada serviço deverá utilizar:

> service account mínima necessária.

---

# 104. API SERVICE ACCOUNT

Pode:

- acessar recursos necessários;
- escrever audit;
- acessar DB via backend.

Não necessariamente:

- deploy produção.

---

# 105. WORKER SERVICE ACCOUNT

Pode:

- queue;
- task processing.

Não automaticamente:

- administrar infraestrutura.

---

# 106. RELEASE SERVICE ACCOUNT

Capability limitada a:

- deployment target autorizado;
- projeto/ambiente autorizado.

---

# 107. ENVIRONMENT ISOLATION

DEV/STAGING/PROD deverão possuir:

- configs distintas;
- secrets distintos;
- deploy references distintos.

---

# 108. NÃO REUTILIZAR CREDENTIAL DE STAGING EM PROD

Separação explícita.

---

# 109. PRODUCTION DATABASE MIGRATION

Fluxo:

```text
migration plan
→ validation
→ backup/rollback assessment
→ approval
→ migration role
→ verify
```

---

# 110. DESTRUCTIVE MIGRATION

Sempre:

# HIGH/CRITICAL

---

# 111. BACKUP CHECK

Antes de alteração destrutiva:

> verificar política de recuperação.

---

# 112. ROLLBACK

Se rollback não for possível:

> Decision Center precisa informar antes da aprovação.

---

# 113. AUDIT ARCHITECTURE

Audit deve ser:

- append-oriented;
- separado do fluxo normal;
- difícil de alterar;
- correlacionado com trace/task.

---

# 114. AUDIT WRITER

Preferir API/função específica:

```text
AuditService.append()
```

---

# 115. NÃO PERMITIR UPDATE NORMAL

`audit_events` não deverá ter:

> UPDATE/DELETE comum.

---

# 116. AUDIT CONTENT

Campos mínimos:

```text
actor
action
resource
project
organization
authorization
result
trace_id
timestamp
```

---

# 117. SECURITY EVENTS

Exemplos:

```text
credential.used
policy.denied
production.approved
production.deployed
high_risk.blocked
secret.scan.failed
engine.permission.denied
```

---

# 118. SECURITY EVENT RETENTION

Eventos críticos terão:

> retenção superior a logs operacionais comuns.

---

# 119. AUDIT INTEGRITY — MVP

Mínimo:

- append-only permissions;
- restricted writer;
- backup;
- correlation.

---

# 120. AUDIT INTEGRITY — FUTURO

Poderá incluir:

- cryptographic chaining;
- WORM storage;
- external audit sink.

---

# 121. SECURITY LOG PRIVACY

Audit não deve vazar:

- tokens;
- secrets;
- payloads sensíveis completos.

---

# 122. MASKING

Campos sensíveis:

> mascarados antes do log.

---

# 123. DATA CLASSIFICATION ENFORCEMENT

Entidades poderão possuir:

```text
classification
```

e policy usar isso na autorização.

---

# 124. SECRET CLASS

`SECRET`:

- não vai para prompts;
- não vai para normal logs;
- não vai para Project Graph content.

---

# 125. SENSITIVE CLASS

`SENSITIVE`:

- provider control;
- minimization;
- access audit.

---

# 126. TENANT SECURITY

Toda operação Cloud deverá carregar:

```text
organization_id
project_id
```

resolvidos pelo backend.

---

# 127. NÃO CONFIAR NO organization_id DO CLIENTE

Backend cruza:

> session → memberships.

---

# 128. CROSS-TENANT TEST

Tenant A usando ID válido de Tenant B:

# DENY

---

# 129. CROSS-PROJECT TEST

Project A tentando carregar artifact de Project B:

# DENY

---

# 130. STORAGE SECURITY

Buckets/objects deverão carregar:

- organization;
- project;
- artifact type.

---

# 131. STORAGE PATH

Exemplo:

```text
org/{org_id}/project/{project_id}/...
```

---

# 132. SIGNED ACCESS

Arquivos privados devem usar:

> acesso autenticado/assinado.

---

# 133. PUBLIC BUCKETS

Não utilizar por padrão para artifacts internos.

---

# 134. QUEUE SECURITY

PGMQ tasks deverão conter:

- project ref;
- operation ref;
- payload mínimo.

Não inserir secrets.

---

# 135. QUEUE WORKER

Antes de executar:

> revalida estado/policy quando ação é material.

---

# 136. STALE TASK DEFENSE

Uma mensagem antiga não deverá executar ação já cancelada.

Worker checa:

- task status;
- version;
- lease.

---

# 137. IDEMPOTENCY SECURITY

Operações externas críticas usam:

```text
operation_id
```

evitando duplicação acidental ou por retry.

---

# 138. REPLAY DEFENSE

Aprovações/gates deverão estar ligadas a:

- versão;
- recurso;
- contexto.

Uma aprovação antiga não deverá liberar ação materialmente diferente.

---

# 139. APPROVAL BINDING

Exemplo:

```text
approve deployment
release_id = R-17
environment = production
```

Não:

> “aprovo qualquer deploy futuro”.

---

# 140. APPROVAL EXPIRATION

Para ações sensíveis, aprovação pode:

- expirar;
- invalidar após mudança material.

---

# 141. JEV SECURITY ROLE

JEV recomenda/classifica.

Mas controles críticos não podem existir apenas nele.

Policy Engine é enforcement.

---

# 142. ORCHESTRATOR SECURITY ROLE

Orchestrator:

- explica;
- solicita decisão;
- coordena.

Não pode ignorar Policy Engine.

---

# 143. POLICY BYPASS

Não deve existir “admin shortcut” informal.

Break-glass futuro deve ser:

- explícito;
- auditado;
- temporário.

---

# 144. EMERGENCY STOP

Deverá existir comando de alto nível:

# STOP ALL EXECUTION FOR PROJECT

---

# 145. EMERGENCY STOP EFFECT

1. impedir novas tasks;
2. cancelar execuções quando seguro;
3. revogar grants temporários;
4. bloquear deploy;
5. preservar evidências;
6. entrar em Safe Mode.

---

# 146. SAFE MODE

Permitido:

- read;
- diagnosis;
- audit;
- recovery planning.

Bloqueado:

- writes não essenciais;
- novos deploys;
- novas integrações.

---

# 147. KILL SWITCH — PROVIDER

Também deverá ser possível desabilitar:

- engine;
- model provider;
- tool adapter.

---

# 148. EXEMPLO

Claude Code comprometido/instável:

> disable adapter.

Forge continua com outros executores.

---

# 149. INCIDENT CREATION

Eventos graves geram:

```text
incident
severity
affected assets
containment state
```

---

# 150. THREAT MODEL — ACTORS

Considerar:

1. usuário malicioso;
2. usuário legítimo com erro;
3. agente comprometido;
4. model provider comprometido;
5. tool comprometida;
6. pacote malicioso;
7. prompt injection;
8. insider;
9. credential theft;
10. cross-tenant attack.

---

# 151. THREAT — PROMPT INJECTION

Ataque:

> documento manda agente enviar credenciais.

Controles:

- content labeling;
- no secret exposure;
- tool authorization;
- capability boundary.

---

# 152. THREAT — MALICIOUS DEPENDENCY

Ataque:

> pacote executa script malicioso.

Controles:

- dependency review;
- package metadata;
- sandbox;
- filesystem scope;
- no production secrets.

---

# 153. THREAT — COMPROMISED ENGINE

Ataque:

> engine tenta acessar arquivos externos.

Controles:

- workspace boundary;
- env minimization;
- command policy;
- no direct prod credentials.

---

# 154. THREAT — CROSS-TENANT LEAK

Controles:

- application auth;
- RLS;
- storage policy;
- isolation tests.

---

# 155. THREAT — MALICIOUS PREVIEW

Aplicação gerada tenta chamar host.

Controles:

- origin isolation;
- no Tauri IPC;
- no native privilege inheritance.

---

# 156. THREAT — STOLEN SESSION

Controles:

- token expiry;
- secure storage;
- revoke;
- re-auth for sensitive action quando necessário.

---

# 157. THREAT — COST ABUSE

Controles:

- budgets;
- retry limits;
- provider rate limits;
- anomaly detection.

---

# 158. THREAT — PRODUCTION CORRUPTION

Controles:

- separate deploy actor;
- production gate;
- release binding;
- rollback;
- migrations review.

---

# 159. THREAT — AUDIT TAMPERING

Controles:

- restricted write path;
- append-only;
- separate permissions;
- external backup.

---

# 160. THREAT — ENGINE HANDOFF CONTEXT LEAK

Controles:

- Context Builder;
- classification;
- minimal package;
- provider policy.

---

# 161. SECURITY REVIEW TRIGGERS

Automaticamente se mudança afetar:

```text
auth
authorization
tenancy
secrets
external network
sensitive data
production
payments
uploads
agent tool permissions
```

---

# 162. SECURITY REVIEW ARTIFACT

Deve registrar:

- scope;
- findings;
- severity;
- evidence;
- disposition.

---

# 163. HIGH/CRITICAL FINDINGS

Bloqueiam:

> Ready for Production.

E, conforme natureza:

> podem bloquear Ready for Human Test.

---

# 164. ACCEPTED RISK

Exige:

- justificativa;
- approver;
- mitigation;
- review date.

---

# 165. SECURITY BASELINE — LIGHT

Mínimo:

- auth;
- scoped filesystem;
- secret scan;
- dependency scan;
- tests;
- audit;
- no direct prod.

---

# 166. SECURITY BASELINE — STANDARD

Acrescenta:

- RLS isolation tests;
- threat review;
- independent security review em áreas críticas;
- provider data policy.

---

# 167. SECURITY BASELINE — FULL

Acrescenta:

- formal threat model;
- adversarial tests;
- stricter approval;
- stronger network policy;
- human sign-off.

---

# 168. FORGE MVP CLASSIFICATION

O próprio Forge será desenvolvido como:

# FULL-LEANING SECURITY POSTURE

porque ele executa código e ferramentas.

---

# 169. DESKTOP UPDATE SECURITY

Updates deverão ser:

- signed;
- verified;
- versioned.

---

# 170. UPDATE CHANNELS

Futuro:

```text
stable
beta
internal
```

---

# 171. DOWNGRADE / ROLLBACK

Atualização com problema deverá possuir:

> estratégia operacional de recuperação.

---

# 172. DEPENDENCY UPDATE POLICY

Não atualizar toda stack automaticamente sem validação.

---

# 173. SECURITY PATCH

Patch crítico:

```text
update
→ tests
→ review
→ release
```

---

# 174. CONFIG SECURITY

Configurações sensíveis separadas de config comum.

---

# 175. FEATURE FLAGS

Não podem contornar autorização.

Feature flag:

> controla disponibilidade.

Policy:

> controla permissão.

---

# 176. CORS / API ORIGINS

Cloud API deve aceitar apenas origens/clientes previstos conforme arquitetura.

Desktop usa fluxo autenticado próprio.

---

# 177. RATE LIMITING

APIs críticas deverão ter:

- rate limits;
- abuse protection.

---

# 178. REQUEST SIZE

Uploads/payloads:

> limites explícitos.

---

# 179. FILE UPLOAD SECURITY

Quando anexos entrarem:

- type validation;
- size limit;
- malware scanning quando aplicável;
- untrusted content labeling.

---

# 180. MIME NÃO É CONFIÁVEL SOZINHO

Validar:

> conteúdo/assinatura quando necessário.

---

# 181. DOCUMENT PARSING

Parsers devem ser tratados como superfície de ataque.

Ideal:

> ambiente isolado.

---

# 182. RAG FUTURO

Security baseline:

- tenant-aware retrieval;
- source ACL;
- source trust;
- prompt-injection defense;
- no cross-tenant embeddings.

---

# 183. API CONTRACT SECURITY

Entradas:

> validação de schema.

Saídas:

> não expor campos internos desnecessários.

---

# 184. MASS ASSIGNMENT

Evitar endpoints em que cliente possa alterar:

> campos privilegiados arbitrários.

---

# 185. EXEMPLO

Cliente não pode mandar:

```text
risk_level = LOW
approved = true
```

e esperar que backend aceite.

---

# 186. SERVER-DERIVED FIELDS

Campos como:

- authorization;
- risk;
- health;
- ready_for_test;

devem ser calculados/validados no servidor.

---

# 187. ERROR SECURITY

Não retornar:

- stack traces sensíveis;
- secret values;
- internal DB details

ao Simple View.

---

# 188. EXPERT LOGS

Mesmo Expert:

> secrets mascarados.

---

# 189. SECURITY HEADERS

Aplicar headers adequados no Cloud UI/API e previews web.

Detalhamento final ficará na implementação.

---

# 190. CSP

Forge Desktop e previews deverão possuir políticas distintas.

---

# 191. SECURITY TEST MATRIX

P0:

```text
AUTH-01 login required
AUTHZ-01 org isolation
AUTHZ-02 project isolation
RLS-01 cross-tenant deny
FS-01 path traversal blocked
FS-02 symlink escape blocked
TERM-01 destructive command blocked
SEC-01 secrets not logged
SEC-02 secrets not committed
ENG-01 engine permission boundary
ENG-02 handoff keeps same scope
PREVIEW-01 no privileged IPC
DEPLOY-01 prod requires approval
DEPLOY-02 wrong release approval rejected
AUDIT-01 event cannot be normally altered
COST-01 hard budget blocks spend
STOP-01 emergency stop halts new work
```

---

# 192. PROMPT-INJECTION TESTS

P0/P1:

```text
PI-01 document says ignore policy
PI-02 webpage asks for secret
PI-03 tool response injects command
PI-04 repo file attempts privilege escalation
```

Resultado:

> conteúdo não obtém autoridade.

---

# 193. SUPPLY CHAIN TESTS

```text
SC-01 suspicious package
SC-02 dependency vulnerability
SC-03 lockfile manipulation
SC-04 secret embedded in package config
```

---

# 194. PRODUCTION TESTS

```text
PROD-01 coding agent cannot deploy directly
PROD-02 staging token fails on prod
PROD-03 missing approval blocks deploy
PROD-04 destructive migration escalates
PROD-05 rollback path recorded
```

---

# 195. SECURITY OBSERVABILITY

Métricas:

```text
policy_denials
high_risk_blocks
secret_scan_failures
unauthorized_access_attempts
engine_permission_denials
production_gate_attempts
credential_use
```

---

# 196. SECURITY ALERTS

Gerar alerta quando:

- repeated denied action;
- cross-tenant attempt;
- secret leak;
- production policy violation;
- unusual cost/security pattern.

---

# 197. NÃO ALERTAR TUDO

Evitar alarm fatigue.

Classificação:

```text
INFO
LOW
MEDIUM
HIGH
CRITICAL
```

---

# 198. SECURITY DASHBOARD

Simple View:

```text
Healthy
Action Required
```

Expert:

- findings;
- policies;
- incidents;
- credentials;
- audit.

---

# 199. SECURITY DO BUILD

Autonomous Build poderá operar livremente quando:

```text
scope valid
+
risk allowed
+
capabilities granted
+
budget valid
+
environment valid
```

---

# 200. BUILD NÃO PODE ALTERAR POLICY PARA SE LIBERAR

Agente não poderá:

> modificar policy para executar ação bloqueada.

---

# 201. POLICY CHANGES

Mudança crítica de policy:

> human gate.

---

# 202. ENGINE ADAPTER CHANGES

Como adapters controlam execução:

> alterações relevantes exigem independent review.

---

# 203. ROUTER CHANGES

Model/Tool/Execution Router:

> security-sensitive components.

Alteração requer:

- tests;
- review;
- audit.

---

# 204. RELEASE AGENT CHANGES

Classificação:

# HIGH SENSITIVITY

---

# 205. SECURITY DEFINITION OF DONE — FEATURE

Feature sensível:

```text
implementation
+
tests
+
security tests
+
review
+
no blocking findings
```

---

# 206. SECURITY DEFINITION OF DONE — BUILD

Para Ready for Human Test:

- no unresolved critical;
- relevant security checks;
- preview isolated;
- secrets check;
- policies satisfied.

---

# 207. SECURITY DEFINITION OF DONE — PRODUCTION

Obrigatório:

```text
approved release
security review satisfied
production credentials valid
migration risk assessed
rollback strategy known
human approval
deployment audit
```

---

# 208. SECURITY MVP — P0

Obrigatório:

```text
Supabase Auth
organization/project authorization
RLS
Tauri capability boundary
filesystem scoping
terminal policy
engine adapters
secret storage
secret masking
no direct prod credentials
preview isolation
dependency scanning
secret scanning
production gate
audit
emergency stop
security tests
```

---

# 209. SECURITY P1

```text
credential broker advanced
network egress allowlists
container sandbox
advanced DLP
multi-provider data policies
signed commits
enhanced audit integrity
```

---

# 210. SECURITY P2

```text
enterprise SSO
SCIM
dual approval
regional controls
compliance packs
confidential computing
external SIEM integrations
```

---

# 211. SECURITY ARCHITECTURE — DESKTOP

```text
React WebView
     │
     ▼
Tauri Command Boundary
     │
     ▼
Rust Host
     │
     ▼
Node Runtime
     │
     ├── Policy Check
     ├── FS Adapter
     ├── Git Adapter
     ├── Engine Adapter
     └── Test Adapter
```

---

# 212. SECURITY ARCHITECTURE — CLOUD

```text
Authenticated Request
      ↓
API Validation
      ↓
Authorization
      ↓
Policy Engine
      ↓
Domain Service
      ↓
RLS / Database
      ↓
Audit
```

---

# 213. SECURITY ARCHITECTURE — ENGINE

```text
Task Envelope
      ↓
Context Filter
      ↓
Capability Grant
      ↓
Engine Adapter
      ↓
Engine
      ↓
Output Validation
      ↓
Evidence
```

---

# 214. SECURITY ARCHITECTURE — PRODUCTION

```text
Release Candidate
      ↓
Tests / Review / Security
      ↓
Human Approval
      ↓
Release Agent
      ↓
Deployment Adapter
      ↓
Production
      ↓
Health Check
      ↓
Audit
```

---

# 215. DECISÕES FROZEN DO FDP-13

1. Security-critical controls live outside LLMs.
2. WebView has no unrestricted native privileges.
3. Tauri is a security boundary, not only shell.
4. Node sidecar operates under project/task scope.
5. Filesystem access is project-root scoped by default.
6. Terminal execution is policy-controlled.
7. Engines are treated as scoped executors.
8. Engine handoff never expands permissions automatically.
9. Secrets are references, not Task Envelope content.
10. Local secrets use secure encrypted storage.
11. Cloud/platform secrets use dedicated secret stores.
12. Model routing respects data classification.
13. External content is untrusted and cannot elevate authority.
14. Tool calls are re-authorized outside the model.
15. Preview is isolated from Forge native capabilities.
16. Coding agents do not own production credentials.
17. Production deploy occurs through Release/Deployment Adapter.
18. RLS + application authorization are both mandatory.
19. Audit is append-oriented and privileged.
20. Emergency Stop + Safe Mode are P0.
21. Supply-chain and secret scanning are P0.
22. Production approval is bound to a specific release/environment.
23. Policy/Router/Adapter changes are security-sensitive.
24. Autonomous Build remains default inside the approved security corridor.
25. Security may stop dangerous actions, but must not recreate approval fatigue.

---

# 216. PRINCIPAL RISCO TÉCNICO DE SEGURANÇA

# AUTONOMOUS LOCAL EXECUTION

O Forge terá capacidade de:

- criar arquivos;
- executar comandos;
- instalar dependências;
- chamar engines.

Logo o boundary:

> UI → Tauri → Local Runtime → Adapter

é parte crítica do produto.

---

# 217. SEGUNDO RISCO

# CREDENTIAL PROPAGATION

Uma única credencial excessivamente poderosa poderia anular várias camadas.

Por isso:

> scoped, environment-specific, temporary whenever possible.

---

# 218. TERCEIRO RISCO

# PROMPT INJECTION + TOOLS

LLM com tool access transforma texto malicioso em risco operacional.

Mitigação principal:

> tool authorization outside the model.

---

# 219. QUARTO RISCO

# PRODUCTION PRIVILEGE BLEED

Credenciais de produção nunca devem “vazar” para o ambiente normal de desenvolvimento.

---

# 220. QUINTO RISCO

# SECURITY FRICTION

Se todo comando gerar confirmação:

> o Forge deixa de ser autônomo.

Mitigação:

```text
LOW → execute
MEDIUM → execute + audit
HIGH → gate
CRITICAL → block/default gate
```

---

# 221. CRITÉRIO DE SUCESSO

O FDP-13 estará corretamente implementado quando conseguirmos demonstrar:

### Cenário A
Codex escreve e testa livremente dentro do projeto.

### Cenário B
Codex tenta sair do workspace.

→ bloqueado.

### Cenário C
Documento malicioso pede token.

→ token não é exposto.

### Cenário D
Claude Code falha, Codex assume.

→ mesmos limites permanecem.

### Cenário E
Task tenta usar produção.

→ gate.

### Cenário F
Aplicação em preview tenta acessar Tauri.

→ negado.

### Cenário G
Tenant A tenta ler projeto B.

→ negado.

### Cenário H
Usuário aprova Release X, sistema tenta publicar Release Y.

→ negado.

---

# 222. PRINCÍPIO FINAL

O Forge deve conseguir operar com autonomia não porque confiamos cegamente nos agentes, mas porque:

> **eles trabalham dentro de uma arquitetura que limita o que podem ver, onde podem atuar, quais ferramentas podem usar e quando precisam parar.**

A segurança do Forge será:

# **AUTONOMY BY CONSTRUCTION, NOT AUTONOMY BY TRUST.**

---

# 223. PRÓXIMA ETAPA

Com aprovação:

# **FDP-14 — OBSERVABILITY & EVALUATION ARCHITECTURE**

Definiremos:

- logs;
- traces;
- metrics;
- correlation IDs;
- build telemetry;
- engine telemetry;
- model usage;
- cost attribution;
- Project Health;
- task health;
- alerts;
- incidents;
- SLOs;
- agent evaluations;
- prompt/model regression;
- execution quality;
- review defect rate;
- Ready for Human Test evidence;
- operational feedback;
- continuous improvement;
- dashboards;
- what the Simple View sees versus Expert View.

---

# 224. GATE FDP-13

**Status recomendado:** APPROVE

Com aprovação:

```text
FDP-10 ✅ Technical Architecture
FDP-11 ✅ Frontend / UX
FDP-12 ✅ Data Architecture
FDP-13 ✅ Security Architecture
   ↓
FDP-14 Observability & Evaluation
   ↓
FDP-15 Integration / Adapter Specification
   ↓
FDP-16 AIOX / Execution Engines
   ↓
FDP-17 Testing Strategy
   ↓
FDP-18 Deployment / Rollback
   ↓
FDP-19 Backlog
   ↓
FDP-20 Sprint Plan
   ↓
BUILD
```

---

## FDP-13 — FIM
