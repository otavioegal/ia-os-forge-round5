# IA OS FORGE
## FDP-15 v1.0 — INTEGRATION / ADAPTER SPECIFICATION

**Protocolo:** Forge Definition Protocol — FDP  
**Documento:** FDP-15  
**Produto:** IA OS Forge  
**Versão:** 1.0  
**Status:** DRAFT → REVIEW  
**Autoria:** Claude Code (Builder), 2026-10-10, por autorização expressa do Founder; revisão independente: Codex  
**Pré-requisitos:** FDP-00 a FDP-13 — APPROVED; FDP-14 — aprovação a confirmar pelo Founder  
**Próxima etapa:** FDP-16 — AIOX / Execution Engines

> Convenção de rastreabilidade: referências como "(FDP-10 §42)" indicam a decisão já aprovada que fundamenta o item. Este documento consolida e detalha essas decisões; quando propõe algo novo, isso aparece como **PROPOSTA**, sujeita ao gate deste FDP.

---

# 1. OBJETIVO

Definir formalmente como o Forge conversa com tudo o que está fora do seu núcleo:

- engines de engenharia;
- provedores de modelos;
- ferramentas e serviços externos;
- o IA OS Core.

O escopo vem do FDP-14 §211. Contratos de integração para:

- IA OS Core;
- Supabase;
- Git/GitHub;
- AIOX;
- Codex;
- Claude Code;
- Grok;
- OpenRouter;
- direct model providers;
- n8n;
- Google;
- WhatsApp;
- Cloud Run;
- storage;
- observability;
- future providers.

E os mecanismos comuns:

- Adapter Interface;
- Capability Registry;
- health;
- retries;
- idempotency;
- secrets;
- risk;
- timeouts;
- versioning;
- fallback;
- test doubles;
- contract tests;
- anti-lock-in rules.

---

# 2. PRINCÍPIO CENTRAL

# **CONTRACTS BEFORE VENDORS.**

(FDP-00, P5.)

Toda integração segue a mesma forma (FDP-01 §38):

```text
ForgeContract
    ↓
Adapter
    ↓
Provider
```

O domínio do Forge conhece contratos e capacidades.

Só o adapter conhece o fornecedor.

---

# 3. O QUE ESTE DOCUMENTO NÃO DEFINE

- funcionamento interno do AIOX e das engines de execução → **FDP-16**;
- estratégia completa de testes → **FDP-17**;
- deploy, release e rollback → **FDP-18**;
- priorização e estimativas → **FDP-19 / FDP-20**;
- escolha comercial definitiva de cada fornecedor;
- qualquer integração com MAJU, que segue fora do escopo do portfólio.

---

# 4. VOCABULÁRIO

Entidades do Integration Domain (FDP-02 §22):

```text
Integration         uma conexão configurada de um projeto com um serviço
Provider            o fornecedor externo (Google, GitHub, OpenAI…)
Capability          uma ação permitida e nomeada (calendar.write)
Adapter             o código que implementa capabilities para um provider
CredentialReference referência a uma credencial guardada fora do banco
Webhook             entrada assíncrona vinda do provider
ExternalAPI         a API concreta do provider
```

Exemplo:

```text
Integration: Google Calendar
Capability:  calendar.create_event
Adapter:     GoogleCalendarAdapter
Credential:  cred_ref → Credential Service
```

---

# 5. TRÊS FAMÍLIAS DE ADAPTER

## Engine Adapters

Executam trabalho de engenharia. Escolhidos pelo **Execution Router**.

```text
CodexAdapter
ClaudeCodeAdapter
GrokAdapter
AioxAdapter
```

(FDP-10 §42.)

## Model Adapters

Chamam modelos. Escolhidos pelo **Model Router**.

```text
OpenRouterAdapter
OpenAIAdapter
AnthropicAdapter
XAIAdapter
GoogleAdapter
LocalModelAdapter
```

(FDP-10 §57.)

## Tool / Integration Adapters

Executam capabilities em serviços externos. Escolhidos pelo **Tool Router**.

```text
GitAdapter / GitHubAdapter
SupabaseAdapter
N8nAdapter
GoogleWorkspaceAdapter
WhatsAppProviderAdapter
CloudRunDeployAdapter
StorageAdapter
TelemetryExporterAdapter
IA OS Core clients
```

---

# 6. CAPABILITY-FIRST

A camada superior pede capacidade, não fornecedor (FDP-05 §75; FDP-04 §137).

Preferir:

```text
deploy.application
```

Em vez de:

```text
call_cloud_run_api
```

O Router escolhe o adapter. Trocar de fornecedor não muda o Orchestrator, o Project Graph nem a UX.

---

# 7. CAPABILITY KEY

Formato:

```text
<domínio>.<ação>
```

Exemplos (FDP-10 §59):

```text
calendar.write
database.migrate
git.commit
browser.search
deploy.application
```

Regras:

- minúsculas, ponto como separador;
- verbo explícito;
- uma capability, uma intenção;
- variações de risco viram capabilities distintas quando o risco muda (ex.: `database.migrate.test` × `database.migrate.production`).

---

# 8. ADAPTER INTERFACE

Interface comum a todas as famílias:

```text
describe()               → AdapterDescriptor
health()                 → HealthReport
invoke(InvocationRequest) → InvocationResult
cancel(invocation_id)    → CancelResult
```

Engine Adapters acrescentam as operações de continuidade do FDP-06 §14:

```text
start_task()
resume_task()
pause_task()
cancel_task()
get_status()
capture_checkpoint()
get_artifacts()
get_diff()
get_test_results()
```

Nem toda engine suporta tudo nativamente. O adapter normaliza as diferenças e declara o que não suporta.

---

# 9. ADAPTER DESCRIPTOR

Cada adapter publica (FDP-05 §58; FDP-13 §74):

```text
adapter_key
family                 ENGINE | MODEL | TOOL
provider
adapter_version        semver
contract_version
capabilities[]
risk_level             LOW | MEDIUM | HIGH | CRITICAL (por capability)
data_access            classes de dado acessadas
environment_access     LOCAL | TEST | STAGING | PRODUCTION
side_effects           NONE | INTERNAL | EXTERNAL_REVERSIBLE | EXTERNAL_IRREVERSIBLE
required_credentials[] referências, nunca valores
supported_operations[]
limits                 rate limits / quotas conhecidos
owner
status                 ENABLED | DISABLED | DEPRECATED
```

Um adapter que não declara algo é tratado pela política mais restritiva.

---

# 10. INVOCATION REQUEST

Envelope padrão de chamada:

```text
invocation_id
operation_ref          estável entre retries e attempts (ver §21)
idempotency_key        obrigatório quando side_effects ≠ NONE
capability
input                  validado contra schema
organization_id
project_id
task_id
attempt_id
environment
credential_reference   quando necessário
data_classification
timeout_class
trace_context          OpenTelemetry
```

O envelope nunca carrega segredo (FDP-13 §51).

---

# 11. INVOCATION RESULT

Resultado normalizado:

```text
status        SUCCEEDED | FAILED | CANCELLED | TIMED_OUT | BLOCKED
output        validado contra schema de saída
artifacts[]   referências
cost          { value, currency, kind: ESTIMATED | CONFIRMED }
error         { type, retryable, provider_code, message_redacted }
evidence[]    referências para o Evidence Service
trace_ids
```

Custo estimado e custo confirmado ficam separados (FDP-14, R7).

---

# 12. CAPABILITY REGISTRY

Fonte de verdade sobre o que pode ser feito e por quem.

Usa os registros já previstos no modelo de dados (FDP-12):

```text
core.tool_registry       provider, tool_key, capabilities, risk_class, status   (§103)
forge.engine_registry    engine_key, adapter, capabilities, minimum_version, status   (§104–105)
forge.integrations       conexões por projeto e ambiente, credential_reference   (§55)
```

Cada capability registrada declara:

```text
capability_key
description
input_schema_ref
output_schema_ref
risk_level
side_effects
allowed_environments
adapters[]            com prioridade
```

**PROPOSTA:** se o FDP-12 não comportar algum desses campos, a diferença entra como delta de modelo de dados para aprovação, sem alterar o FDP-12 por este documento.

---

# 13. RESOLUÇÃO DE CAPABILITY

Quando o Orchestrator pede uma capability, o Router:

```text
1. lista adapters registrados para a capability
2. remove os DISABLED (kill switch)
3. aplica Policy Engine (FDP-07 §21)
4. aplica política de dados (ex.: OpenRouter ALLOW | DENY | ONLY_FOR_PUBLIC — FDP-13 §68)
5. remove adapters sem credencial válida para o ambiente
6. considera health
7. ordena por prioridade, custo, histórico de desempenho
8. invoca
```

O resultado da Policy Engine é respeitado literalmente:

```text
ALLOW
ALLOW + AUDIT
ALLOW + NOTIFY
REQUIRE APPROVAL
DENY
```

---

# 14. RISCO

Toda capability tem nível de risco (FDP-07 §14–18):

```text
LOW       EXECUTE
MEDIUM    EXECUTE + LOG + VALIDATE
HIGH      HUMAN GATE (ou política empresarial equivalente)
CRITICAL  BLOCK BY DEFAULT + EXPLICIT AUTHORIZATION
```

Exemplos de classificação padrão:

```text
git.commit (branch de trabalho)        LOW
dependency.install                      MEDIUM
database.migrate.test                   MEDIUM
git.push (remoto do projeto)            MEDIUM
messaging.send (fluxo já aprovado)      MEDIUM
database.migrate.production             HIGH
deploy.application (produção)           HIGH
messaging.activate_outbound             HIGH    primeira ativação de envio a pessoas reais
database.drop.production                CRITICAL
credential.expose                       CRITICAL
```

Gate vale para a **decisão**, não para cada repetição: depois que o Founder ou a política aprova um fluxo (destinatários, templates, finalidade), os envios dentro dele são `MEDIUM` — usar API já autorizada (FDP-07 §16) sem microgate (FDP-07 §20). Mudança de destinatários, finalidade ou conteúdo fora do aprovado volta a exigir gate.

O adapter não escolhe o próprio risco em tempo de execução. O Tool Router revalida a política mesmo quando o modelo pede a chamada (FDP-13 §73).

---

# 15. HUMAN GATES

As integrações acionam os gates do FDP-07 §19:

```text
Scope Gate
Sensitive Access Gate        nova credencial ou dado sensível
Financial Commitment Gate    compra, assinatura, plano pago de provider
Destructive Action Gate
Production Gate              deploy ou mudança crítica em produção
Irreversible Action Gate
```

E respeitam a regra contrária (FDP-07 §20):

> **NÃO HAVERÁ MICROGATES.**

Trocar Codex por Claude Code, repetir uma chamada transitória ou usar uma API já autorizada não pede aprovação.

---

# 16. SECRETS

Princípio:

> **agentes recebem capacidade, não segredo bruto.**

(FDP-04 §81; FDP-05 §37.)

Regras:

1. Banco e Task Envelope guardam **referências** (FDP-12 §173; FDP-13 §51).
2. Materialização é temporária e escopada (FDP-13 §50):

```text
Credential Service
   ↓
temporary scoped materialization
   ↓
process
   ↓
revoke / clear
```

3. Escopo da credencial (FDP-07 §32):

```text
Organization
Product
Project
Environment
Capability
Expiration
```

4. Armazenamento (FDP-10 §66–67):

```text
Local       Tauri Stronghold
Platform    Google Secret Manager
Projeto     Credential Service (Supabase Vault para credenciais server-side quando adequado)
```

5. Coding engines não recebem credencial global de banco nem token administrativo de Git (FDP-12 §124; FDP-13 §86).
6. Rotação, revogação e expiração são suportadas pela arquitetura (FDP-07 §33).

---

# 17. CREDENCIAL AUSENTE

Se a credencial necessária não existe:

- a capability retorna `BLOCKED` com motivo `CREDENTIAL_REQUIRED`;
- o Forge abre um Secret Request na UX (FDP-06 §80);
- o restante do build continua quando possível.

Simple View:

> "Preciso conectar sua conta do Google Calendar para continuar esta integração."

---

# 18. TAXONOMIA DE ERROS

Todo erro de adapter é mapeado para um tipo (FDP-06 §32; FDP-14 §101–102):

```text
TRANSIENT            timeout, conexão               retryable
RATE_LIMITED         limite de uso                  retryable após espera / handoff
QUOTA_EXHAUSTED      cota esgotada                  handoff provável
AUTH                 credencial inválida/expirada   não retryable → Secret Request
APPROVAL_REQUIRED    Policy Engine: REQUIRE APPROVAL  status BLOCKED → Decision Center; prossegue após aprovação
POLICY_DENIED        Policy Engine: DENY            não retryable; não é aprovável pelo fluxo normal
VALIDATION           entrada/saída fora do schema   não retryable → corrigir
PROVIDER_FAILURE     erro do fornecedor             retryable limitado
CAPABILITY_FAILURE   provider não faz a tarefa      switch de adapter/engine
TASK_FAILURE         código/teste falhou            corrigir (não é falha de infra)
CONFLICT             estado divergente              reconciliar
UNKNOWN              não classificado               tratar como não retryable
```

A distinção **infraestrutura × código produzido** é obrigatória (FDP-14 §101).

---

# 19. TIMEOUTS

Toda invocação tem timeout explícito.

Classes:

```text
INTERACTIVE    respostas curtas para a UX
STANDARD       chamadas de API comuns
LONG_RUNNING   tarefas de engine e builds
```

Para `LONG_RUNNING`, o controle é por **heartbeat/progresso**, não só por tempo total:

- ausência de progresso dentro da janela → `STALLED`;
- `STALLED` → cancelamento e classificação da falha.

Valores concretos ficam como parâmetros de configuração, ajustados com dados do FDP-14.

---

# 20. RETRIES

- só para erros `retryable`;
- backoff exponencial com jitter;
- número máximo de tentativas por tipo de erro;
- respeito a budget e aos thresholds de custo (FDP-14 §205);
- nunca repetir efeito colateral sem `idempotency_key`.

Retry de invocação não cria nova Task Attempt.

Troca de engine cria nova Task Attempt (handoff), preservando o contexto no Forge (FDP-04 §54).

---

# 21. IDEMPOTENCY

Obrigatória para capabilities com `side_effects ≠ NONE`.

A chave identifica a **operação**, não a tentativa:

```text
operation_ref    id estável atribuído quando o Orchestrator decide a operação
                 e persistido no Forge (Task / Project Graph)
idempotency_key = hash(project_id, task_id, operation_ref, capability, input normalizado)
```

Regras:

- `attempt_id` **não** entra na chave: retries e handoff para outra engine reutilizam o mesmo `operation_ref` e, portanto, a mesma chave;
- uma nova operação intencional (por exemplo, um segundo deploy pedido depois de uma mudança) recebe novo `operation_ref`;
- usar idempotência nativa do provider quando existir;
- caso contrário, o Forge mantém registro de chaves já executadas e devolve o resultado anterior em replay;
- replay é auditado.

**PROPOSTA:** o registro de idempotência é persistido como delta de modelo de dados a aprovar junto com o FDP-12.

---

# 22. HEALTH

São duas taxonomias distintas. O `HealthReport` carrega um discriminador e nunca mistura estados:

```text
HealthReport
  health_domain   EXECUTION | INTEGRATION
  state           conforme o domínio
  checked_at
  source          PASSIVE | ACTIVE
  detail
```

`EXECUTION` — engines e provedores de modelo (FDP-06 §68–69; FDP-10 §46):

```text
AVAILABLE
DEGRADED
RATE_LIMITED
UNAVAILABLE
UNKNOWN
```

`INTEGRATION` — tool / integration adapters (FDP-14 §89):

```text
HEALTHY
DEGRADED
DISCONNECTED
FAILED
```

Fontes de health:

- **passiva:** resultado das invocações reais;
- **ativa:** sonda barata, sem efeito colateral e com limite de frequência.

Engine detection no Desktop (FDP-10 §45):

```text
installed?
authenticated?
version?
capabilities?
health?
```

O resultado alimenta os Routers.

---

# 23. FALLBACK

## Engines (FDP-06 §31–32)

```text
Preferred Engine
      ↓ falhou por CAPABILITY / QUOTA / UNAVAILABLE
Alternative Engine
      ↓
Generic AIOX Runner
      ↓
BLOCKED
```

Falha não significa trocar de engine imediatamente: `TRANSIENT` → retry; `TASK_FAILURE` → corrigir; `ARCHITECTURE FAILURE` → replan.

## Modelos

Model Router com primário e fallback, respeitando política de privacidade do projeto:

```text
direct provider only
local models only
OpenRouter ALLOW | DENY | ONLY_FOR_PUBLIC
```

(FDP-07 §109; FDP-13 §68.)

## Ferramentas

Outro adapter registrado para a mesma capability, se permitido pela política. Sem alternativa: `BLOCKED` + Decision Center ou Secret Request.

---

# 24. KILL SWITCH

Deve ser possível desabilitar (FDP-13 §147):

- engine;
- model provider;
- tool adapter.

Escopos: global, organização, projeto.

Efeito:

- o Router exclui o item imediatamente;
- invocações em curso de risco HIGH/CRITICAL são canceladas;
- as demais podem concluir, conforme política.

---

# 25. VERSIONING

- `adapter_version` em semver;
- `contract_version` independente;
- mudança incompatível nunca é silenciosa (FDP-05 §44);
- versão anterior suportada durante janela de transição declarada;
- adapters podem ser marcados `DEPRECATED` antes de removidos;
- engines têm `minimum_version` (FDP-12 §105).

Mudanças relevantes em adapters de engine e em Routers exigem revisão independente (FDP-13 §202–203; FDP-07 §105).

---

# 26. OBSERVABILITY

Toda invocação gera trace OpenTelemetry com correlação Project / Task / Attempt (FDP-14 §6–8).

Métricas mínimas por adapter:

```text
invocation success
output parsing success
cancellation success
latência
custo (estimado × confirmado)
erros por tipo
```

(FDP-14 §99.)

Domain events:

```text
AdapterInvoked
AdapterSucceeded
AdapterFailed
IntegrationHealthChanged
EngineHealthChanged
CredentialRequested
AdapterDisabled
```

Logs com redaction: sem segredos, sem prompts ou código-fonte brutos por padrão (FDP-14 §20–21).

---

# 27. TEST DOUBLES

Todo adapter entrega um **double** que implementa a mesma interface:

- determinístico;
- registra as chamadas recebidas;
- permite injetar cada tipo de erro da taxonomia;
- simula timeout, cancelamento e health.

Testes unitários e de integração do Forge não chamam provider real.

Para Model Adapters, gravações de respostas (record/replay) são permitidas apenas com redaction.

---

# 28. CONTRACT TESTS

Uma suíte de contrato por família, executada contra o double e contra o adapter real.

## Engine Adapters (FDP-10 §104)

```text
start
capture output
cancel
failure detection
checkpoint
resume / handoff context
```

## Tool Adapters

```text
describe
health
invoke (schema de entrada/saída)
cancel
idempotency (replay devolve o mesmo resultado)
mapeamento de erros
```

## Model Adapters

```text
resposta válida
mapeamento de erros e rate limit
relato de custo
respeito à política de privacidade
```

Execução contra providers reais:

- apenas em contas/ambientes de teste;
- suíte separada, disparada sob política (não em todo commit);
- nunca contra produção de cliente.

---

# 29. ANTI-LOCK-IN RULES

1. Nenhum código de domínio chama SDK, API ou CLI de fornecedor diretamente (FDP-10 §42).
2. Camadas superiores falam em capability (FDP-05 §75).
3. O estado do projeto pertence ao Forge, não à engine (FDP-04 §54).
4. Supabase fica atrás de repositories e services; não é contrato de domínio (FDP-10 §24).
5. OpenRouter é opcional; rota direta sempre possível (FDP-10 §58; FDP-08 §41).
6. n8n serve às automações de negócio dos sistemas gerados, não à execução do próprio Forge (FDP-10 §60).
7. Nada de "super adapter": uma responsabilidade por integração (FDP-05 §60).
8. Dados do usuário exportáveis em formato aberto de cada integração crítica.
9. **PROPOSTA:** toda capability crítica deve ter alternativa registrada ou ausência documentada antes de liberar o produto para clientes.

---

# 30. IA OS CORE

Interface mínima (FDP-10 §85):

```text
IdentityClient
OrganizationClient
AgentRegistryClient
ModelRegistryClient
ToolRegistryClient
AuditClient
```

Mecanismos (FDP-05 §10):

```text
API Contracts           requisição direta (REST/JSON + typed contracts)
Events                  comunicação assíncrona
Capability Invocation   pedir ação permitida a outro serviço
```

Regras:

- clientes podem nascer dentro do monorepo e ser extraídos depois;
- contract tests impedem que atualização do Core quebre o Forge (FDP-05 §45);
- o Forge pode estender adapters comuns do Core (FDP-05 §59).

---

# 31. SUPABASE

Uso (FDP-10):

```text
PostgreSQL         via repositories
Auth
Storage
Queues / PGMQ
Vault              credenciais server-side, quando adequado
```

Capabilities típicas:

```text
database.query          MEDIUM   escopo do projeto
database.migrate.test   MEDIUM
database.migrate.production  HIGH   Production Gate
storage.put / storage.get    LOW–MEDIUM conforme dado
```

Coding engines nunca recebem a credencial global do banco (FDP-12 §124). Acesso passa por adapter escopado.

---

# 32. GIT / GITHUB

Git local (obrigatório no MVP — FDP-08 §52):

```text
git.init
git.commit           checkpoint
git.diff
git.rollback.dev     rollback de desenvolvimento
```

GitHub (quando o projeto usa remoto):

```text
repo.create
git.push
pr.create
```

Regras:

- credenciais escopadas por repositório; nunca token administrativo global (FDP-13 §86);
- `git.push --force` e reescrita de histórico em branch compartilhada: CRITICAL, bloqueado por padrão;
- cada Forge Project ligado a um repositório (FDP-10 §48).

---

# 33. AIOX

`AioxAdapter` cobre o **AIOX API Runner** como engine genérica de fallback (FDP-04 §47; FDP-06 §31).

O contrato segue o Engine Adapter deste documento.

Funcionamento interno, squads e orquestração AIOX: **FDP-16**.

---

# 34. CODEX

`CodexAdapter` — engine de engenharia do MVP (FDP-08 §43).

O adapter controla (FDP-13 §59):

```text
working directory
context
allowed tools
environment
output capture
cancellation
```

Capability profile típico (FDP-13 §60):

```text
repository_read
repository_write
terminal
tests
git
```

A engine não escolhe os próprios privilégios; pedidos passam por JEV + Policy (FDP-13 §61).

---

# 35. CLAUDE CODE

`ClaudeCodeAdapter` — engine de engenharia do MVP (FDP-08 §43).

Mesmo contrato e mesmas restrições do Codex.

Continuidade entre Codex e Claude Code depende do contexto persistido pelo Forge, não da memória da engine (FDP-04 §54).

---

# 36. GROK

`GrokAdapter` — objetivo do MVP, condicionado à validação técnica (FDP-04 §153; FDP-08 §43).

Até lá: registrado como placeholder no Engine Registry (FDP-12 §104), status `DISABLED`, sem impedir o build.

---

# 37. OPENROUTER

Rota opcional para modelos (FDP-04 §43–44):

- acesso unificado;
- failover de provider;
- fallback de modelo;
- custo.

Nunca gateway obrigatório (FDP-10 §58). Política por projeto: `ALLOW | DENY | ONLY_FOR_PUBLIC` (FDP-13 §68).

---

# 38. DIRECT MODEL PROVIDERS

```text
OpenAIAdapter
AnthropicAdapter
XAIAdapter
GoogleAdapter
LocalModelAdapter
```

Cada um declara:

- modelos suportados;
- classes de dado permitidas;
- limites;
- forma de relatar custo.

Projetos podem exigir `direct provider only` ou `local models only` (FDP-07 §109).

---

# 39. N8N

n8n é recurso externo **do sistema gerado** (FDP-10 §100).

O Forge cria e configura workflows por adapter autorizado:

```text
automation.workflow.create     MEDIUM
automation.workflow.activate   HIGH quando dispara efeitos externos reais
```

n8n não é o motor de execução do próprio Forge (FDP-10 §60).

---

# 40. GOOGLE

Integrações Google Workspace (ex.: Calendar, Drive, Gmail) via OAuth com escopos mínimos.

Capabilities de exemplo:

```text
calendar.read            LOW
calendar.create_event    MEDIUM
mail.send                MEDIUM dentro de fluxo aprovado
mail.activate_outbound   HIGH   primeira ativação de envio a terceiros (gate único)
```

Nova conexão OAuth aciona Sensitive Access Gate.

---

# 41. WHATSAPP

Via provedor de API oficial de WhatsApp Business.

Regras:

- a ativação do envio a pessoas reais é `HIGH` (`messaging.activate_outbound`, Production Gate); depois, envios dentro do fluxo aprovado são `MEDIUM` (§14);
- respeito a opt-in, templates aprovados e janelas de atendimento do provedor;
- mensagens recebidas entram por webhook e são **conteúdo, não autoridade** (FDP-07 §42).

---

# 42. CLOUD RUN

`CloudRunDeployAdapter` implementa `deploy.application` para aplicações geradas.

- deploy em produção: `HIGH`, Production Gate;
- Release separado de Deployment (FDP-12);
- rollback e estratégias de deploy: **FDP-18**.

---

# 43. STORAGE

`StorageAdapter` para artefatos e arquivos:

```text
storage.put
storage.get
storage.signed_url
storage.delete      MEDIUM; HIGH em produção
```

Implementação inicial: Supabase Storage. Contrato não expõe o fornecedor.

---

# 44. OBSERVABILITY

`TelemetryExporterAdapter` exporta via OTLP (FDP-14 §6–7).

O backend de observabilidade é substituível; o Forge não depende de API proprietária para instrumentar.

---

# 45. FUTURE PROVIDERS

Checklist para incluir qualquer novo provider:

```text
1. Adapter Descriptor completo
2. capabilities e risco revisados
3. test double
4. contract tests passando
5. revisão de segurança (zonas de confiança — FDP-13 §12)
6. health definido
7. kill switch funcionando
8. documentação de credenciais e escopos
9. revisão independente
```

Provider externo nunca recebe confiança implícita (FDP-13 §12).

---

# 46. UX DAS INTEGRAÇÕES

Pontos de contato já previstos no FDP-11 (§161–165):

- Engine Setup;
- Engine Health;
- Secrets UX.

Simple View mostra:

- o que está conectado;
- o que precisa ser conectado;
- o que está com problema, em linguagem simples.

Expert View mostra descriptor, health, versões, métricas e erros.

---

# 47. ESCOPO DO MVP

Coerente com o FDP-08:

```text
Execution   Codex + Claude Code; Grok se tecnicamente validado
Models      rota direta + OpenRouter opcional
Tools       Git, GitHub (se usado), Supabase, automação (n8n),
            research/browser, testing, deployment (Cloud Run)
Secrets     separados do código, masking, escopos, separação de ambientes
```

Google e WhatsApp entram conforme o primeiro sistema gerado exigir. **PROPOSTA:** confirmar no Backlog (FDP-19).

Credential Broker avançado pode vir depois do MVP (FDP-08 §69).

---

# 48. DECISÕES FROZEN DO FDP-15

1. Toda integração segue ForgeContract → Adapter → Provider.
2. Camadas superiores pedem capability, nunca fornecedor.
3. Três famílias de adapter: Engine, Model, Tool.
4. Interface comum: describe, health, invoke, cancel.
5. Engine Adapters implementam também as operações de continuidade do FDP-06.
6. Todo adapter publica Adapter Descriptor; o que não for declarado recebe a política mais restritiva.
7. Capability Registry é a fonte de verdade sobre o que pode ser feito.
8. Risco segue LOW / MEDIUM / HIGH / CRITICAL do FDP-07.
9. Não haverá microgates para ações dentro da política.
10. Segredos nunca trafegam em envelopes; só referências.
11. Erros são mapeados para taxonomia única, com `retryable` explícito.
12. Idempotency key é obrigatória para efeitos colaterais e estável entre retries e attempts (`operation_ref`).
13. Health tem fonte passiva e ativa.
14. Fallback segue a ordem do FDP-06 e a política de privacidade do projeto.
15. Kill switch existe para engine, provider e adapter.
16. Mudança incompatível de contrato nunca é silenciosa.
17. Todo adapter tem test double e contract tests.
18. Testes contra providers reais só em ambientes de teste.
19. OpenRouter é opcional; n8n serve aos sistemas gerados.
20. Nenhum fornecedor detém o estado do projeto.

---

# 49. PRINCIPAIS RISCOS

## R1 — Adapter vazando secret

Mitigação:
referências + materialização temporária + redaction + secret scanning.

## R2 — Capability com risco subdeclarado

Mitigação:
revisão do descriptor + política mais restritiva por padrão + revalidação no Tool Router.

## R3 — Retry duplicando efeito externo

Mitigação:
idempotency key obrigatória + registro de replay.

## R4 — Fallback mudando destino de dados

Mitigação:
política de privacidade aplicada antes do fallback.

## R5 — Contract drift de provider

Mitigação:
contract tests contra ambiente de teste + versionamento.

## R6 — Lock-in silencioso

Mitigação:
anti-lock-in rules; e, se aprovada, a **PROPOSTA** do §29 item 9 (alternativa registrada para capabilities críticas).

## R7 — Approval fatigue

Mitigação:
sem microgates; gates só nos casos do FDP-07.

## R8 — Explosão de adapters

Mitigação:
checklist de inclusão + uma responsabilidade por adapter.

---

# 50. CRITÉRIO DE SUCESSO

O FDP-15 estará corretamente implementado quando conseguirmos:

> trocar Codex por Claude Code no meio de um build sem perder contexto;

> desligar um provider de modelo e o build continuar pela rota permitida;

> repetir uma chamada de deploy sem publicar duas vezes;

> adicionar um provider novo sem mudar Orchestrator, Project Graph ou UX;

> rodar todos os testes do Forge sem tocar em nenhum provider real;

> responder "qual adapter falhou, por quê e quanto custou" com evidência.

---

# 51. PRINCÍPIO FINAL

O Forge vai conversar com muitos fornecedores.

Nenhum deles pode ser dono do projeto.

# **INTEGRATE COMMODITY.  
OWN THE CONTRACT.**

---

# 52. PRÓXIMA ETAPA

Com aprovação:

# **FDP-16 — AIOX / EXECUTION ENGINES**

Detalharemos:

- AIOX como framework e runner;
- ciclo de vida das engines;
- handoff entre engines na prática;
- checkpoints e retomada;
- limites de cada engine no MVP.

---

# 53. GATE FDP-15

**Status recomendado:** REVIEW → aprovação do Founder

Com aprovação:

```text
FDP-10 ✅ Technical Architecture
FDP-11 ✅ Frontend / UX
FDP-12 ✅ Data Architecture
FDP-13 ✅ Security Architecture
FDP-14 ⏳ Observability & Evaluation (confirmar)
FDP-15 ⏳ Integration / Adapter Specification
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

## FDP-15 — FIM
