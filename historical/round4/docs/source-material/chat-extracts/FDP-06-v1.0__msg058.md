<!--
Extrato literal de docs/source-material/chats/ChatGPT-IA-OS-FORGE-2026-10-10.json
Mensagem [58] do ramo atual (assistente), 2026-10-08 17:12 UTC.
Título no ChatGPT: "FDP-06 v1.0 — Execution & Continuity Blueprint | IA OS Forge"
Conteúdo copiado sem edição: bloco :::writing (sem o invólucro).
Status: EXTRACTED — validação do Founder pendente.
-->

# IA OS FORGE
## FDP-06 v1.0 — EXECUTION & CONTINUITY BLUEPRINT

**Protocolo:** Forge Definition Protocol — FDP  
**Documento:** FDP-06  
**Produto:** IA OS Forge  
**Versão:** 1.0  
**Status:** DRAFT → REVIEW  
**Pré-requisitos:** FDP-00 a FDP-05 — APPROVED  
**Próxima etapa:** FDP-07 — Security & Governance Blueprint

---

# 1. OBJETIVO

Definir como o Forge transforma um **plano aprovado** em um sistema construído, testado, revisado e pronto para teste humano, sem exigir microautorizações durante a engenharia.

O FDP-06 especifica conceitualmente:

- Autonomous Build;
- Execution Controller;
- filas e dependências;
- AIOX;
- Codex;
- Claude Code;
- Grok;
- Execution Router;
- capabilities;
- Task Envelope;
- Git/checkpoints;
- worktrees/isolamento;
- execução paralela;
- retries;
- timeout;
- watchdog;
- recuperação;
- engine handoff;
- context packaging;
- OpenRouter/model fallback;
- controle de custo;
- evidências;
- estados de execução;
- critérios de conclusão.

---

# 2. PRINCÍPIO FUNDAMENTAL

Depois que o usuário aprovar:

```text
ESCOPO
+
PLANO
+
PERMISSÕES
+
ORÇAMENTO/POLÍTICAS
```

e selecionar:

# CONSTRUIR PROJETO

o comportamento padrão será:

> **Forge trabalha autonomamente até entregar uma versão construída, revisada e pronta para teste.**

---

# 3. EXPERIÊNCIA EXTERNA

Para o usuário:

```text
PLANO APROVADO
      ↓
CONSTRUIR
      ↓
Forge trabalhando
      ↓
Produto pronto para teste
```

---

# 4. COMPLEXIDADE INTERNA

Internamente:

```text
PLAN
 ↓
TASK GRAPH
 ↓
QUEUE
 ↓
ROUTING
 ↓
EXECUTION
 ↓
CHECKPOINT
 ↓
TEST
 ↓
FIX
 ↓
RETEST
 ↓
REVIEW
 ↓
SECURITY
 ↓
INTEGRATION
 ↓
BUILD VALIDATION
 ↓
READY FOR HUMAN TEST
```

Toda essa complexidade deverá permanecer invisível no **Simple View**.

---

# 5. AUTONOMOUS BUILD CONTROLLER

Será o controlador lógico da fase BUILD.

Responsabilidades:

- receber plano aprovado;
- gerar ou carregar task graph;
- organizar dependências;
- iniciar trabalhos;
- selecionar executores;
- controlar paralelismo;
- acompanhar progresso;
- detectar falhas;
- disparar retries;
- trocar engine;
- solicitar reviews;
- consolidar resultados;
- controlar budget;
- atualizar Project Graph;
- decidir quando o build está efetivamente concluído.

---

# 6. BUILD NÃO É UMA ÚNICA SESSÃO DE IA

Um build poderá durar:

- minutos;
- horas;
- múltiplas sessões;
- diferentes engines;
- diferentes máquinas.

Logo:

> **sessão de modelo não pode ser a unidade persistente de execução.**

A unidade persistente será a tarefa mantida pelo Forge.

---

# 7. TASK GRAPH

O plano de implementação será transformado em um grafo de tarefas.

Exemplo:

```text
Auth
 ├── Data model
 ├── API
 ├── Login UI
 └── Tests

Dashboard
 └── depende de Auth

Deployment
 └── depende de Auth + Dashboard
```

O sistema sabe:

- o que pode rodar agora;
- o que está bloqueado;
- o que pode rodar em paralelo.

---

# 8. WORK UNIT

Cada nó executável do Task Graph será uma **Work Unit**.

Tipos possíveis:

```text
ANALYZE
DESIGN
CODE
MIGRATE
CONFIGURE
INTEGRATE
TEST
FIX
REVIEW
SECURITY_CHECK
DOCUMENT
BUILD
DEPLOY_PREP
```

---

# 9. TASK ENVELOPE

Cada Work Unit importante possuirá um envelope persistente.

Estrutura conceitual:

```text
Task ID
Project ID
Objective
Type
Requirements
Acceptance Criteria
Dependencies
Constraints
Risk Level
Budget
Allowed Tools
Allowed Environments
Current Agent
Current Engine
Relevant Files
Relevant Decisions
Graph Context
Test State
Review State
Git State
Checkpoint
Attempts
Progress
Next Action
Status
```

---

# 10. O TASK ENVELOPE É O PASSAPORTE DA TAREFA

A execução não deve depender da memória de:

- Codex;
- Claude Code;
- Grok;
- um chat;
- um agente.

Se a engine mudar:

> o envelope continua.

---

# 11. EXECUTION ROUTER

Responsável por selecionar a engine adequada.

Inicialmente:

```text
Codex
Claude Code
Grok
AIOX-compatible runner
```

Posteriormente:

```text
Future Engine A
Future Engine B
Local Coding Engine
```

---

# 12. CRITÉRIOS DE ROTEAMENTO

O Router poderá considerar:

```text
Task type
Capabilities
Repository size
Context needs
Tools
Latency
Cost
Quota
Availability
Historical performance
Review defect rate
Risk level
Privacy requirements
```

---

# 13. CAPABILITY MODEL

Engines deverão ser tratadas por capabilities.

Exemplo:

```text
ENGINE: Codex

Capabilities:
repository_read
repository_write
terminal
tests
refactor
parallel_tasks
```

A arquitetura não deve depender de nomes comerciais para sempre.

---

# 14. EXECUTION ENGINE ADAPTER

Cada engine deverá idealmente possuir adapter.

Contrato conceitual:

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

Nem toda engine suportará nativamente todas as operações.

O adapter normaliza diferenças.

---

# 15. AIOX

AIOX permanecerá como framework preferencial de engenharia.

Função:

> organizar papéis, workflows e práticas de desenvolvimento.

Forge continuará responsável por:

- estado;
- Project Graph;
- Task Envelope;
- políticas;
- engines;
- continuidade.

---

# 16. DIVISÃO AIOX × FORGE

```text
FORGE
  ↓
define missão + estado + política
  ↓
AIOX
  ↓
organiza execução de engenharia
  ↓
ENGINE
  ↓
Codex / Claude Code / Grok
```

---

# 17. AIOX NÃO SERÁ UM PONTO ÚNICO DE FALHA

Se uma parte da execução puder ser realizada sem AIOX:

> arquitetura deverá permitir.

Forge deverá manter contratos próprios.

---

# 18. EXECUÇÃO ISOLADA

Tarefas paralelas não deverão editar indiscriminadamente a mesma área do projeto.

Preferir:

- worktrees;
- branches;
- sandboxes;
- diretórios isolados;
- locks lógicos.

---

# 19. GIT COMO PARTE DA CONTINUIDADE

Git será uma das âncoras da linha de produção.

Usos:

- checkpoints;
- versionamento;
- diff;
- branches/worktrees;
- rollback;
- reconstrução do estado;
- evidência.

---

# 20. CHECKPOINT

Checkpoint deverá capturar, conforme necessário:

```text
Git reference
Task state
Graph state
Relevant artifacts
Tests
Findings
Next action
Engine state metadata
```

---

# 21. MOMENTOS DE CHECKPOINT

Checkpoint obrigatório ou recomendado:

- antes de operação de maior risco;
- após milestone da tarefa;
- antes de engine handoff;
- após testes aprovados;
- antes de merge;
- antes de migration relevante;
- antes de staging.

---

# 22. CHECKPOINT NÃO É APENAS COMMIT

Um commit pode existir sem contexto suficiente.

Checkpoint Forge acrescenta:

> o que estávamos tentando fazer e qual o próximo passo.

---

# 23. ENGINE HANDOFF

Fluxo:

```text
ENGINE A
   ↓
interrupção
   ↓
CAPTURE CHECKPOINT
   ↓
BUILD CONTROLLER
   ↓
EXECUTION ROUTER
   ↓
ENGINE B
   ↓
LOAD CONTEXT PACKAGE
   ↓
RESUME
```

---

# 24. CONTEXT PACKAGE

Engine substituta recebe apenas contexto relevante.

Exemplo:

```text
Task objective
Acceptance criteria
Relevant requirements
Relevant ADRs
Relevant Graph nodes
Files/modules
Current diff
Test failures
Review findings
Git checkpoint
Previous attempts
Next action
```

---

# 25. EVITAR CONTEXT DUMP

Não enviar o projeto inteiro indiscriminadamente.

Benefícios:

- menor custo;
- melhor foco;
- menos alucinação;
- menor exposição de dados;
- maior velocidade.

---

# 26. CONTEXT BUILDER

Componente lógico responsável por consultar:

- Project Graph;
- Project Memory;
- Artifact Registry;
- Git;
- Task Envelope;

e montar o pacote mínimo necessário.

---

# 27. CONTEXT POLICY

O pacote respeitará:

- permissions;
- data classification;
- task scope;
- engine privacy policy.

---

# 28. OPENROUTER

OpenRouter continuará no plano como:

# Model Gateway / Continuity Layer

para workloads baseados em API.

Poderá ajudar em:

- provider fallback;
- model fallback;
- disponibilidade;
- custo;
- uniformização de acesso.

---

# 29. OPENROUTER NÃO RESOLVE ENGINE HANDOFF

Distinção obrigatória:

```text
OpenRouter
→ modelos/API
```

```text
Execution Continuity
→ Codex / Claude Code / Grok / engines
```

São problemas diferentes.

---

# 30. MODEL FALLBACK

Para tarefas API:

```text
Preferred Model
      X
Fallback Model
      X
Alternative Provider
```

Desde que:

- política permita;
- privacidade permita;
- custo permaneça dentro do limite.

---

# 31. ENGINE FALLBACK

Para tarefas de engenharia:

```text
Preferred Engine
      X
Alternative Engine
      X
Generic AIOX Runner
      X
BLOCKED
```

---

# 32. FALHA NÃO SIGNIFICA IMEDIATAMENTE TROCAR ENGINE

Tipos de falha:

### TRANSIENT
timeout, conexão.

→ retry.

### QUOTA
limite de uso.

→ handoff provável.

### TASK FAILURE
código/teste falhou.

→ corrigir.

### ENGINE CAPABILITY FAILURE
engine não consegue tarefa.

→ switch.

### ARCHITECTURE FAILURE
plano inadequado.

→ replan.

---

# 33. RETRY MANAGER

Políticas por categoria.

Exemplo:

```text
Network failure
→ retry 3x

Tool timeout
→ retry / alternative tool

Same coding failure
→ reviewer/replan

Quota
→ engine switch
```

---

# 34. RETRY BUDGET

Retries custam:

- tempo;
- tokens;
- compute;
- dinheiro.

Logo cada tarefa terá limite razoável.

---

# 35. LOOP DETECTION

Se o sistema observar:

```text
fix
fail
fix
fail
fix
fail
```

não deve continuar indefinidamente.

Ação:

> chamar diagnóstico/reviewer/replan.

---

# 36. WATCHDOG

Monitorará:

- tarefa sem progresso;
- heartbeat perdido;
- retries excessivos;
- custo anormal;
- tool loop;
- engine frozen;
- deadlock;
- queue starvation.

---

# 37. HEARTBEAT

Execuções longas deverão sinalizar:

> ainda estou ativo.

Ausência prolongada:

> suspected stalled task.

---

# 38. TIMEOUT

Timeout será específico por tipo de tarefa.

Exemplo:

- lint: curto;
- integration test: maior;
- full build: maior ainda.

Não usar um timeout universal.

---

# 39. DEADLOCK

Se:

```text
Task A depende de B
Task B depende de A
```

Forge deverá detectar.

Resultado:

> dependency conflict → replan.

---

# 40. PARALLEL EXECUTION

O Forge deverá utilizar paralelismo para produtividade.

Exemplo:

```text
                 ┌─ Backend
IMPLEMENT PLAN ──┼─ Frontend
                 ├─ Test preparation
                 └─ Documentation
```

---

# 41. CONDIÇÕES PARA PARALELISMO

Permitido quando:

- dependências independentes;
- áreas de edição separadas;
- interfaces acordadas;
- merge controlado;
- orçamento permite.

---

# 42. PARALLELISM LIMIT

Não maximizar número de agentes apenas porque é possível.

Mais agentes significam:

- mais custo;
- mais conflito;
- maior coordenação.

O JEV deverá buscar paralelismo útil.

---

# 43. WORKTREE STRATEGY

Hipótese preferencial para código:

```text
Task A → Worktree A
Task B → Worktree B
Task C → Worktree C
```

Depois:

```text
Validate
Merge
Integration tests
```

A decisão técnica definitiva virá depois.

---

# 44. MERGE CONTROLLER

Responsabilidades:

- verificar conflitos;
- integrar mudanças;
- executar testes;
- atualizar Graph;
- criar checkpoint.

---

# 45. CONFLITO DE MERGE

Primeiro:

> resolver automaticamente quando seguro.

Se estrutural:

> architectural reconciliation.

Humano apenas se consequência de negócio for relevante.

---

# 46. BUILD QUEUE

Estados:

```text
QUEUED
READY
RUNNING
WAITING
RETRYING
HANDOFF
REVIEW
BLOCKED
COMPLETED
FAILED
CANCELLED
```

---

# 47. PRIORIDADES

```text
CRITICAL
HIGH
NORMAL
LOW
```

Mas prioridade não ignora dependências.

---

# 48. PARTIAL BLOCKING

Um bloqueio deve afetar apenas subgrafo necessário.

Exemplo:

Calendar credential ausente.

Pode continuar:

- dashboard;
- CRM;
- UI;
- outros testes.

---

# 49. BUILD PROGRESS

Progresso será derivado de trabalho real.

Exemplo:

```text
Tasks:
32/40

Tests:
54/61

Reviews:
5/7
```

Interface:

> Construção 80%.

---

# 50. PROGRESS WEIGHTING

Nem toda task pesa igual.

Uma story complexa não vale o mesmo que atualizar um texto.

Modelo de weighting deverá ser definido tecnicamente depois.

---

# 51. EVIDENCE STORE

Toda conclusão relevante deverá possuir evidência.

Exemplos:

```text
Task complete
→ commit/diff

Test passed
→ test execution result

Review passed
→ review artifact

Security passed
→ security report
```

---

# 52. CLAIMED DONE × VERIFIED

Internamente:

```text
CLAIMED_DONE
      ↓
VERIFY
      ↓
VERIFIED
```

Simple View só mostra:

> concluído

depois de VERIFIED.

---

# 53. TEST-FIRST QUANDO APROPRIADO

O Forge poderá escolher:

- test-first;
- code-first;
- contract-first;

conforme tipo de tarefa.

Não impor metodologia única universal.

---

# 54. TEST PIPELINE

Padrão adaptativo:

```text
STATIC CHECK
 ↓
UNIT
 ↓
INTEGRATION
 ↓
E2E
 ↓
AGENT EVALS
 ↓
SECURITY
 ↓
REGRESSION
```

Somente testes aplicáveis são executados.

---

# 55. AUTO-FIX LOOP

```text
TEST FAIL
   ↓
DIAGNOSE
   ↓
FIX
   ↓
RETEST
```

Sem pedir autorização.

---

# 56. REVIEW PIPELINE

Após feature/milestone:

```text
BUILDER RESULT
      ↓
INDEPENDENT REVIEW
      ↓
FINDINGS
      ↓
FIX
      ↓
RE-REVIEW if needed
```

---

# 57. REVIEW SEVERITY

```text
INFO
LOW
MEDIUM
HIGH
CRITICAL
```

HIGH/CRITICAL exigem tratamento antes de Ready for Human Test, salvo exceção formal.

---

# 58. SECURITY REVIEW

Automaticamente acionado para mudanças relevantes em:

- auth;
- permissions;
- secrets;
- data sensitivity;
- external integrations;
- tenancy;
- deployment;
- network exposure.

---

# 59. DOCUMENTATION SYNC

Enquanto constrói:

- PRD;
- architecture;
- ADR;
- Graph;
- test status;

devem ser marcados/atualizados conforme mudança.

---

# 60. NÃO ACEITAR DOCUMENTAÇÃO FALSA

Se implementação divergir do documento:

> documento não permanece CURRENT silenciosamente.

Deve:

- atualizar;
- ou marcar stale;
- ou gerar finding.

---

# 61. BUDGET CONTROLLER

Controlará:

```text
Build budget
Task budget
Premium model budget
Engine usage
Tool costs
Cloud build costs
```

---

# 62. SOFT LIMIT

Ao atingir limite intermediário:

> otimizar routing.

Não interromper imediatamente.

---

# 63. HARD LIMIT

Se ultrapassar limite explicitamente definido:

> bloquear novas ações pagas e gerar Decision Required.

---

# 64. COST-AWARE ROUTING

Exemplo:

Task simples:

> modelo low-cost.

Task crítica:

> modelo/engine de maior capacidade.

Não utilizar premium como padrão automático.

---

# 65. PERFORMANCE-AWARE ROUTING

Custo sozinho não determina rota.

Se modelo barato gera retrabalho:

> pode ser economicamente pior.

Forge deverá futuramente aprender custo total por resultado.

---

# 66. EXECUTION HISTORY

Registrar:

```text
Task type
Engine
Model
Duration
Cost
Retries
Review findings
Success
```

---

# 67. EXECUTION INTELLIGENCE

Com tempo, isso poderá melhorar:

> quem deve executar o quê.

Essa inteligência poderá tornar-se ativo estratégico do Forge.

---

# 68. ENGINE HEALTH

Forge deverá conhecer estado:

```text
AVAILABLE
DEGRADED
RATE_LIMITED
UNAVAILABLE
UNKNOWN
```

---

# 69. PROVIDER HEALTH

Mesma lógica para:

- OpenRouter;
- OpenAI;
- Anthropic;
- xAI;
- Google;
- ferramentas.

---

# 70. ROUTING COM HEALTH

Não enviar trabalho crítico para engine indisponível conhecida.

---

# 71. FALLBACK NÃO DEVE ALTERAR QUALIDADE SILENCIOSAMENTE

Se fallback cair abaixo de capability mínima:

> não executar.

Exemplo:

modelo alternativo não suporta ferramenta necessária.

Resultado:

> procurar outra opção ou bloquear task.

---

# 72. SECURITY OF EXECUTION

Cada task possuirá:

- allowed paths;
- allowed tools;
- allowed environment;
- allowed network scope;
- capability limits.

---

# 73. FILESYSTEM SCOPE

Uma tarefa não deve receber acesso ao computador inteiro sem necessidade.

Preferir:

> project directory scope.

---

# 74. TERMINAL SCOPE

Comandos poderão ser executados dentro de políticas.

Bloquear/elevar risco para:

- destructive system commands;
- access outside workspace;
- privilege escalation;
- production changes.

---

# 75. SANDBOX

Sempre que razoável:

- code execution;
- package install;
- tests;
- untrusted files;

rodar em ambiente isolado.

---

# 76. DEPENDENCY INSTALLATION

Dentro do projeto e política:

> automática.

Mas deverá verificar:

- fonte;
- licença quando aplicável;
- vulnerabilidades;
- lockfile;
- compatibility.

---

# 77. SUPPLY-CHAIN RISK

Dependências suspeitas ou comprometidas:

> Security finding.

---

# 78. MIGRATIONS

DEV/TEST:

> podem executar autonomamente dentro da política.

PRODUCTION:

> Production Gate.

---

# 79. EXTERNAL SERVICES

Criar conta paga ou serviço com compromisso financeiro:

> Human Gate.

Configurar integração já autorizada:

> automático.

---

# 80. SECRET REQUEST

Se credencial necessária não existir:

Simple View:

> “Preciso conectar sua conta do Google Calendar para continuar esta integração.”

O restante do build continua quando possível.

---

# 81. BUILD PAUSE

Usuário pode selecionar:

# PAUSAR

Forge:

1. impede novas tasks;
2. permite safe point;
3. salva checkpoints;
4. mostra estado.

---

# 82. EMERGENCY STOP

Para necessidade imediata:

> interrompe executores e preserva o máximo de estado possível.

---

# 83. RESUME

Ao continuar:

```text
Reconcile Git
Reconcile Graph
Check task leases
Check tool/provider health
Reload queue
Resume
```

---

# 84. CRASH RECOVERY

Após falha do próprio Forge:

> reconstruir estado a partir de persistência.

Nenhuma construção importante pode existir apenas em memória RAM.

---

# 85. IDEMPOTENCY

Operações críticas deverão, quando possível, ser idempotentes.

Objetivo:

> retry não duplica recurso ou ação.

---

# 86. EXEMPLO

Criar migration:

> saber se já foi criada/aplicada.

Criar webhook:

> verificar existência antes de duplicar.

---

# 87. BUILD JOURNAL

Cada build terá histórico cronológico.

Simple View:

> resumo.

Expert View:

> execução completa.

---

# 88. BUILD ARTIFACT

Ao final deverá existir um pacote lógico contendo:

```text
Version
Source revision
Project Graph baseline
Build report
Test report
Review report
Security report
Known issues
Deployment package
Documentation state
```

---

# 89. BUILD REPORT

Simple:

```text
Build concluído
47 tarefas concluídas
82 testes aprovados
0 problema crítico
1 observação menor
```

Expert:

detalhamento integral.

---

# 90. READY FOR HUMAN TEST

Esse será o objetivo padrão do Autonomous Build.

Pré-condições:

```text
Approved requirements implemented
Critical tests passed
Independent review passed
Critical/high findings resolved
Required security checks passed
Project Graph synchronized
Documentation not critically stale
Preview/staging available
Known issues disclosed
```

---

# 91. NÃO É PRODUCTION READY AUTOMATICAMENTE

Distinção:

```text
READY FOR HUMAN TEST
≠
APPROVED FOR PRODUCTION
```

---

# 92. HUMAN ACCEPTANCE

Usuário testa o produto.

Feedback gera:

```text
Change Request
      ↓
Impact
      ↓
Autonomous Fix
      ↓
Test/Review
      ↓
New Preview
```

---

# 93. RELEASE CANDIDATE

Após aceitação:

> RC — Release Candidate.

Passa por staging/final gates.

---

# 94. PRODUCTION GATE

Sempre mostra:

- versão;
- alterações;
- riscos;
- custos;
- migrations;
- rollback;
- serviços.

Então:

# PUBLICAR

---

# 95. ROLLBACK PREPARATION

Antes de production deploy:

> estratégia de rollback quando tecnicamente aplicável.

---

# 96. BUILD MODES

## AUTONOMOUS

Padrão.

## GUIDED

Mais checkpoints.

## RESTRICTED

Enterprise/regulado.

---

# 97. AUTONOMOUS MODE É O PADRÃO COMERCIAL

Porque o usuário principal:

> não é desenvolvedor.

A experiência deve ser:

> **“aprovei; construa.”**

---

# 98. GUIDED MODE

Para:

- equipes técnicas;
- treinamento;
- projetos sensíveis.

Pode expor milestones adicionais.

---

# 99. RESTRICTED MODE

Pode exigir:

- dual approval;
- change ticket;
- manual reviewer;
- time window;
- explicit environment approval.

---

# 100. MVP EXECUTION SCOPE

## Obrigatório

```text
Task Graph
Task Envelope
Execution Router
Codex integration
Claude Code integration
AIOX integration
Git checkpoints
Basic worktree isolation
Retry Manager
Basic Watchdog
Context Package
Engine Handoff
Test Pipeline
Independent Review
Build Report
Ready for Human Test
```

---

# 101. GROK NO MVP

Objetivo:

> integrar como engine de primeira classe se a capacidade técnica disponível permitir.

Se não:

> contrato continua preparado e integração entra imediatamente depois.

Não bloquear MVP inteiro por uma engine.

---

# 102. OPENROUTER NO MVP

Útil para workloads API/model routing.

Não precisa ser condição para o primeiro build funcionar.

Arquitetura deve suportar:

- OpenRouter;
- acesso direto.

---

# 103. PARALLEL BUILD MVP

Começar conservador.

Exemplo:

2–4 work units paralelas quando independentes.

Não criar swarm descontrolado.

---

# 104. WATCHDOG MVP

Detectar:

- stalled task;
- lost engine;
- retry loop;
- cost anomaly;
- task timeout.

---

# 105. RECOVERY MVP

Mínimo:

```text
checkpoint
+
git state
+
task envelope
+
context package
+
engine switch
```

---

# 106. NÃO OBJETIVOS DO MVP

Não exigir inicialmente:

- centenas de engines;
- distributed scheduler global;
- Kubernetes próprio;
- advanced predictive routing;
- autonomous production self-healing;
- infinite parallelism;
- custom coding model.

---

# 107. MÉTRICAS DO BUILD

Futuras métricas essenciais:

```text
Lead time
Task success rate
First-pass test rate
Review defect rate
Retry count
Engine handoffs
Build cost
Cost per accepted feature
Human interruptions
Recovery success
```

---

# 108. MÉTRICA CRÍTICA

Uma das métricas principais:

# HUMAN INTERRUPTION RATE

O Forge deve conseguir entregar builds complexos com poucas interrupções humanas.

---

# 109. OUTRA MÉTRICA CRÍTICA

# BUILD-TO-TEST SUCCESS

Percentual de projetos que chegam a:

> Ready for Human Test

sem intervenção técnica humana externa.

---

# 110. CONTINUITY SUCCESS

Medir:

> tarefas retomadas com sucesso após falha/troca de engine.

---

# 111. SECURITY METRIC

Número de ações de alto risco bloqueadas corretamente.

---

# 112. COST METRIC

Custo efetivo para produzir funcionalidade aceita, não apenas tokens.

---

# 113. RISCOS DO FDP-06

## R1 — Continuity falsa

Engine troca, mas perde entendimento.

Mitigação:
Task Envelope + Context Builder + tests.

## R2 — Conflitos paralelos

Mitigação:
worktrees + merge controller.

## R3 — Loops caros

Mitigação:
watchdog + retry budget.

## R4 — Autonomia excessiva

Mitigação:
scoped policies + environment boundaries.

## R5 — Autonomia insuficiente

Mitigação:
eliminar microgates.

## R6 — Engine lock-in

Mitigação:
adapters + capability routing.

## R7 — Build aparentemente concluído

Mitigação:
evidence-based completion.

## R8 — Context leak

Mitigação:
minimal context package + permissions.

## R9 — Corrupted project state

Mitigação:
Git + Graph snapshots + checkpoint/reconciliation.

---

# 114. DECISÕES CONSOLIDADAS

Este documento estabelece:

1. Autonomous Build Controller como componente lógico central da construção.
2. Task Graph como estrutura de trabalho.
3. Task Envelope como unidade persistente de continuidade.
4. Execution Router independente do Model Router.
5. AIOX como framework integrado, não dono do estado.
6. Codex e Claude Code como engines prioritárias.
7. Grok como engine prevista.
8. Git como âncora de versionamento e checkpoints.
9. Engine handoff automático quando possível.
10. Context Package mínimo e relevante.
11. Retries proporcionais ao tipo de falha.
12. Watchdog contra loops/travamentos/custos.
13. Paralelismo controlado.
14. Isolamento por worktree/sandbox quando adequado.
15. Test/fix/retest automáticos.
16. Review independente antes da conclusão.
17. Segurança baseada em risco.
18. Budget control sem microinterrupções.
19. Build concluído somente com evidência.
20. Objetivo final da fase: **READY FOR HUMAN TEST**.

---

# 115. ARQUITETURA DE REFERÊNCIA

```text
                APPROVED PROJECT PLAN
                         │
                         ▼
              AUTONOMOUS BUILD CONTROLLER
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
          TASK GRAPH            WATCHDOG
              │
              ▼
        EXECUTION ROUTER
      ┌───────┼─────────┐
      ▼       ▼         ▼
    CODEX   CLAUDE     GROK
            CODE
      │       │         │
      └───────┼─────────┘
              ▼
        WORKTREE/SANDBOX
              │
              ▼
          CHECKPOINT
              │
      ┌───────┴────────┐
      ▼                ▼
   TESTING          FAILURE?
      │                │
      │                ▼
      │        RETRY / HANDOFF
      │                │
      └────────┬───────┘
               ▼
      INDEPENDENT REVIEW
               │
               ▼
        SECURITY CHECK
               │
               ▼
      PROJECT GRAPH SYNC
               │
               ▼
      READY FOR HUMAN TEST
```

Transversalmente:

```text
BUDGET
RISK
AUDIT
OBSERVABILITY
PROJECT MEMORY
CONTEXT CONTROL
SECRETS POLICY
```

---

# 116. PRINCÍPIO FINAL

A linha de produção deverá ser capaz de dizer:

> **“Uma engine falhou, então continuei com outra.”**

> **“Os testes falharam, então corrigi e testei novamente.”**

> **“O reviewer encontrou problemas, então corrigi antes de entregar.”**

sem transformar o usuário em gerente técnico da construção.

A promessa operacional é:

# **APROVE O PLANO. O FORGE CONSTRÓI.**

---

# 117. PRÓXIMA ETAPA

Com aprovação deste documento:

# FDP-07 — SECURITY & GOVERNANCE BLUEPRINT

Definiremos formalmente:

- trust boundaries;
- threat model;
- least privilege;
- sandbox;
- secrets;
- credential broker;
- human gates;
- risk engine;
- production protection;
- agent isolation;
- prompt injection;
- supply-chain security;
- audit;
- privacy;
- tenant isolation;
- data classification;
- destructive actions;
- emergency stop;
- approvals;
- rollback;
- independent security review;
- governance modes.

---

# 118. GATE FDP-06

**Status recomendado:** APPROVE

Com aprovação:

```text
FDP-00 ✅
FDP-01 ✅
FDP-02 ✅
FDP-03 ✅
FDP-04 ✅
FDP-05 ✅
FDP-06 ✅
    ↓
FDP-07
Security & Governance
```

---

## FDP-06 — FIM
