<!--
Extrato literal de docs/source-material/chats/ChatGPT-IA-OS-FORGE-2026-10-10.json
Mensagem [80] do ramo atual (assistente), 2026-10-08 18:55 UTC.
Título no ChatGPT: "FDP-14 v1.0 — Observability & Evaluation Architecture | IA OS Forge"
Conteúdo copiado sem edição: bloco :::writing (sem o invólucro).
Status: EXTRACTED — validação do Founder pendente.
-->

# IA OS FORGE
## FDP-14 v1.0 — OBSERVABILITY & EVALUATION ARCHITECTURE

**Protocolo:** Forge Definition Protocol — FDP  
**Documento:** FDP-14  
**Produto:** IA OS Forge  
**Versão:** 1.0  
**Status:** DRAFT → REVIEW  
**Pré-requisitos:** FDP-00 a FDP-13 — APPROVED  
**Próxima etapa:** FDP-15 — Integration / Adapter Specification

---

# 1. OBJETIVO

Definir como o Forge observará, medirá e avaliará:

- projetos;
- builds;
- tasks;
- agentes;
- engines;
- modelos;
- tools;
- testes;
- reviews;
- segurança;
- custos;
- deploys;
- aplicações produzidas;
- operação em produção;
- melhoria contínua.

O objetivo não é coletar o máximo de dados.

É responder:

> **O sistema está funcionando?**

> **A construção está avançando?**

> **O resultado é confiável?**

> **Quanto custou?**

> **Por que falhou?**

> **O que precisa melhorar?**

---

# 2. PRINCÍPIO CENTRAL

O Forge deverá ser:

# OBSERVABLE BY DESIGN

Nenhuma execução crítica deverá acontecer como uma caixa-preta impossível de reconstruir.

---

# 3. MAS OBSERVABILIDADE NÃO É UX

Internamente:

```text id="aw1nml"
Logs
Traces
Metrics
Events
Evals
Costs
Findings
```

Externamente, no Simple View:

```text id="m5gcns"
Building
72%

Tests healthy
No action required
```

---

# 4. TRÊS CAMADAS

## Layer 1 — Operational Observability

O que está acontecendo?

## Layer 2 — Quality Evaluation

O trabalho está correto?

## Layer 3 — Business Outcome

O sistema produzido está gerando valor?

---

# 5. TELEMETRY MODEL

Baseline:

```text id="mxm2ds"
LOGS
+
METRICS
+
TRACES
+
DOMAIN EVENTS
+
EVALUATIONS
```

---

# 6. OPENTELEMETRY

OpenTelemetry será o padrão de instrumentação.

Objetivo:

> evitar acoplamento do Forge a um único fornecedor de observabilidade.

---

# 7. TELEMETRY BACKEND

O backend específico poderá ser escolhido posteriormente.

A aplicação deverá emitir telemetria por contratos OpenTelemetry.

---

# 8. CORRELATION MODEL

Toda execução importante deverá carregar:

```text id="eqg7a7"
trace_id
organization_id
project_id
task_id
attempt_id
agent_id
engine_id
release_id
environment_id
```

quando aplicável.

---

# 9. TRACE PRINCIPAL DE BUILD

Exemplo:

```text id="u3ovcr"
Build Started
 ↓
Task Selected
 ↓
JEV Decision
 ↓
Execution Router
 ↓
Claude Code
 ↓
Tests
 ↓
Review
 ↓
Graph Update
 ↓
Task Completed
```

Tudo correlacionável.

---

# 10. TASK TRACE

Cada attempt deverá possuir trace próprio.

Uma mesma Task pode ter:

```text id="ntpehq"
Attempt 1
Claude Code

Attempt 2
Codex
```

com traces separados, ligados à mesma Task.

---

# 11. ENGINE HANDOFF TRACE

Evento explícito:

```text id="0g8srl"
engine.handoff
```

Deverá registrar:

- task;
- engine anterior;
- nova engine;
- motivo;
- checkpoint;
- outcome.

---

# 12. LOGGING PRINCIPLE

Logs deverão ser:

- estruturados;
- pesquisáveis;
- correlacionáveis;
- classificados.

Evitar logs puramente textuais sem contexto.

---

# 13. LOG STRUCTURE

Exemplo conceitual:

```text id="9z85rr"
timestamp
severity
service
event
project_id
task_id
attempt_id
trace_id
message
metadata
```

---

# 14. LOG SEVERITY

```text id="wb694s"
DEBUG
INFO
WARN
ERROR
CRITICAL
```

---

# 15. DEBUG

Detalhes úteis para desenvolvimento.

Não necessariamente enviados ou retidos em produção por longo período.

---

# 16. INFO

Eventos normais significativos.

Exemplo:

> task.started

---

# 17. WARN

Anomalia recuperável.

Exemplo:

> engine retry.

---

# 18. ERROR

Ação falhou.

---

# 19. CRITICAL

Evento com impacto severo ou risco alto.

---

# 20. PRIVACY IN LOGS

Logs não deverão conter por padrão:

- secrets;
- tokens;
- source code completo;
- prompts privados completos;
- documentos sensíveis;
- payloads extensos.

---

# 21. REDACTION

Pipeline de logging deverá permitir:

```text id="0xby7i"
mask
redact
hash
truncate
```

---

# 22. DOMAIN EVENTS

Eventos de negócio não são iguais a logs.

Exemplos:

```text id="5v2ph3"
forge.project.created
forge.plan.approved
forge.build.started
forge.task.completed
forge.review.failed
forge.build.ready_for_test
forge.release.deployed
```

---

# 23. DOMAIN EVENTS SÃO ESTÁVEIS

Eles representam fatos do produto.

Logs representam diagnóstico.

---

# 24. METRICS

Métricas serão agrupadas por domínio.

---

# 25. PROJECT METRICS

```text id="70cr89"
project_cycle_time
time_to_first_visual
time_to_ready_for_test
human_interruptions
changes_requested
```

---

# 26. BUILD METRICS

```text id="wfvxhm"
build_duration
build_success_rate
tasks_total
tasks_completed
tasks_failed
tasks_retried
```

---

# 27. TASK METRICS

```text id="5gpdzq"
task_duration
task_success_rate
retry_count
handoff_count
wait_time
```

---

# 28. ENGINE METRICS

```text id="qk5jc3"
engine_availability
engine_success_rate
engine_task_duration
engine_retry_rate
engine_handoff_rate
review_defects_after_engine
```

---

# 29. MODEL METRICS

```text id="ocvtv6"
model_requests
model_latency
model_failures
token_usage
estimated_cost
task_success_by_model
```

---

# 30. TOOL METRICS

```text id="9f7m3c"
tool_calls
tool_success
tool_failure
tool_latency
tool_denials
```

---

# 31. TEST METRICS

```text id="mg9tzf"
tests_total
tests_passed
tests_failed
first_pass_rate
regression_failures
```

---

# 32. REVIEW METRICS

```text id="ulhhzy"
findings_per_review
review_defect_rate
severity_distribution
repeat_findings
```

---

# 33. SECURITY METRICS

```text id="mz9aw9"
policy_denials
high_risk_blocks
secret_scan_failures
unauthorized_attempts
security_findings
```

---

# 34. DEPLOYMENT METRICS

```text id="bkz0ro"
deployment_success_rate
deployment_duration
rollback_rate
health_check_failures
```

---

# 35. OPERATIONS METRICS

Para aplicações produzidas:

```text id="55fr3f"
availability
error_rate
latency
throughput
cost
business KPIs
```

---

# 36. COST OBSERVABILITY

Custo deverá poder ser atribuído a:

```text id="hb3zqm"
organization
project
build
task
attempt
engine
model
tool
environment
```

---

# 37. COST PRINCIPLE

Não medir apenas:

> tokens.

Medir sempre que possível:

> custo por resultado útil.

---

# 38. COST PER ACCEPTED FEATURE

Uma das métricas estratégicas:

# COST PER ACCEPTED FEATURE

---

# 39. HUMAN INTERRUPTION RATE

Métrica crítica do Forge:

# HUMAN INTERRUPTION RATE

Pergunta:

> quantas vezes o usuário precisou intervir durante um build autônomo?

---

# 40. UNNECESSARY APPROVAL RATE

Também medir:

> quantas decisões humanas foram solicitadas sem serem realmente necessárias?

---

# 41. TIME TO FIRST VISUAL

Mede:

> tempo entre pedido inicial e primeira visualização útil.

Essencial para UX percebida.

---

# 42. TIME TO READY FOR HUMAN TEST

Mede o ciclo principal da fábrica.

---

# 43. AUTONOMOUS BUILD SUCCESS RATE

Percentual de builds que chegam ao Ready for Human Test:

> sem intervenção técnica externa.

---

# 44. ENGINE CONTINUITY SUCCESS

Percentual de handoffs que:

> retomam e concluem a Task corretamente.

---

# 45. DEFECT ESCAPE RATE

Defeitos relevantes descobertos apenas pelo usuário.

Quanto menor:

> melhor.

---

# 46. EVALUATION ARCHITECTURE

Observabilidade responde:

> o que aconteceu.

Evaluation responde:

> o resultado foi bom?

---

# 47. TIPOS DE EVALUATION

```text id="gv7515"
DETERMINISTIC
RULE-BASED
MODEL-BASED
HUMAN
PRODUCTION
```

---

# 48. DETERMINISTIC

Exemplos:

- test passa?
- endpoint responde?
- arquivo existe?
- migration válida?

---

# 49. RULE-BASED

Exemplos:

- todos P0 implementados?
- existe finding HIGH?
- existe approval de produção?

---

# 50. MODEL-BASED

Pode avaliar:

- qualidade de resposta;
- adherence;
- classificação;
- reasoning output;
- UX linguistic quality.

---

# 51. MODEL-BASED EVAL NÃO É AUTORIDADE ÚNICA

Nunca usar apenas:

> “outro LLM disse que está bom”

para validar requisito técnico crítico.

---

# 52. HUMAN EVAL

Necessário para:

- aceitação;
- preferências;
- qualidade subjetiva;
- produção quando gate exige.

---

# 53. PRODUCTION EVAL

Baseada em comportamento real:

- sucesso;
- erros;
- abandono;
- custo;
- conversão;
- satisfação.

---

# 54. EVALUATION OBJECTS

O Forge deverá poder avaliar:

- agent;
- prompt;
- model;
- engine;
- workflow;
- feature;
- release;
- application.

---

# 55. AGENT EVALUATION

Cada agente importante poderá possuir suite própria.

Exemplo:

```text id="ig33mm"
Discovery Agent

understands intent
asks minimal questions
does not invent requirements
captures constraints
```

---

# 56. ORCHESTRATOR EVALUATION

Avaliar:

- compreensão;
- precisão;
- interrupções desnecessárias;
- escalations corretas;
- comunicação.

---

# 57. JEV EVALUATION

Avaliar:

- risk classification;
- agent selection;
- engine routing;
- human gate correctness;
- cost efficiency.

---

# 58. EXECUTION ROUTER EVALUATION

Perguntas:

- escolheu engine adequada?
- handoff ocorreu quando necessário?
- custo foi razoável?
- tarefa chegou ao resultado?

---

# 59. SOFTWARE ENGINEER AGENT EVAL

Avaliar:

- requirements adherence;
- code quality;
- test pass rate;
- review defects;
- regression rate.

---

# 60. SECURITY REVIEWER EVAL

Avaliar:

- vulnerabilidades encontradas;
- false positives;
- missed findings;
- severity accuracy.

---

# 61. INDEPENDENT REVIEWER EVAL

Métrica importante:

> quantos defeitos reais encontra antes do usuário?

---

# 62. PROMPT VERSIONING

Prompts críticos deverão possuir:

```text id="ne7e0v"
prompt_id
version
agent_role
created_at
status
```

---

# 63. PROMPT EVAL

Nova versão de prompt não deve entrar silenciosamente.

Fluxo:

```text id="njdk3q"
Prompt v2
 ↓
Eval suite
 ↓
Compare v1 × v2
 ↓
Approve
 ↓
Activate
```

---

# 64. MODEL CHANGE EVALUATION

Trocar:

> model A por model B

deve poder ser testado contra:

- qualidade;
- custo;
- latency;
- safety.

---

# 65. ENGINE CHANGE EVALUATION

Nova engine deverá passar por:

- adapter tests;
- task benchmark;
- handoff test;
- review quality.

---

# 66. GOLDEN DATASETS

Poderemos manter conjuntos controlados para eval.

Exemplo:

```text id="x2vfb6"
Discovery examples
Architecture decisions
Coding tasks
Security cases
Prompt injection cases
```

---

# 67. GOLDEN DATA PRIVACY

Preferir:

- sintético;
- anonymized;
- explicitly approved.

Não reutilizar dados privados de clientes indiscriminadamente.

---

# 68. EVAL CASE

Estrutura:

```text id="vzcobt"
input
context
expected behavior
evaluation method
minimum score
severity
```

---

# 69. EVAL RUN

```text id="66udkh"
eval_suite
agent/model/prompt version
environment
results
cost
timestamp
```

---

# 70. EVAL RESULT

Pode ser:

```text id="iesgg0"
PASS
FAIL
WARN
```

ou score quantitativo.

---

# 71. REGRESSION GATE

Mudança em componente crítico não deverá avançar se:

> piorar significativamente uma avaliação obrigatória.

---

# 72. BASELINE

Cada agente/modelo poderá ter:

> evaluation baseline.

---

# 73. QUALITY SCORE

O Forge poderá futuramente mostrar score agregado.

Mas não no MVP como número mágico.

---

# 74. EVITAR SCORE FALSO

Não criar:

> “AI Quality = 97%”

sem metodologia verificável.

---

# 75. READY FOR HUMAN TEST EVIDENCE

O estado deverá ser derivado de evidências.

---

# 76. EVIDENCE CATEGORIES

```text id="v1axrt"
Requirements coverage
Build artifacts
Tests
Reviews
Security
Graph consistency
Preview availability
Known issues
```

---

# 77. REQUIREMENT COVERAGE

Para P0:

> Requirement → implementation → validation.

---

# 78. EVIDENCE MATRIX

Exemplo:

| Requirement | Implementation | Test | Review | Status |
|---|---|---|---|---|
| R-01 | C-14 | T-33 | RV-5 | VERIFIED |

---

# 79. READY FOR HUMAN TEST RULE

Conceitualmente:

```text id="umr2vl"
P0 implementation complete
AND
critical tests pass
AND
required reviews pass
AND
security gate pass
AND
no unresolved HIGH/CRITICAL
AND
preview available
```

---

# 80. EVIDENCE SERVICE

Criar serviço lógico:

# Evidence Service

Responsável por responder:

> esta task/feature/build possui evidência suficiente?

---

# 81. BUILD CONFIDENCE

Simple View poderá mostrar:

```text id="asf0l7"
Build verified
```

Não precisa mostrar score técnico.

---

# 82. EXPERT EVIDENCE VIEW

Pode mostrar:

- tests;
- reviews;
- commits;
- Graph links;
- findings.

---

# 83. PROJECT HEALTH

Não será campo manual.

Será derivado.

---

# 84. PROJECT HEALTH INPUTS

```text id="6dh9xs"
blocked tasks
critical findings
failed deployment
incidents
stale critical documents
provider health
```

---

# 85. HEALTH STATES

```text id="smtx5y"
HEALTHY
NEEDS_ATTENTION
BLOCKED
INCIDENT
```

---

# 86. TASK HEALTH

Possíveis sinais:

```text id="7vblhw"
running normally
stalled
retrying
blocked
high cost
```

---

# 87. ENGINE HEALTH

```text id="1bnlpk"
AVAILABLE
DEGRADED
RATE_LIMITED
UNAVAILABLE
UNKNOWN
```

---

# 88. MODEL PROVIDER HEALTH

Também deverá ser monitorado.

---

# 89. TOOL HEALTH

Integrações podem estar:

```text id="b80wje"
HEALTHY
DEGRADED
DISCONNECTED
FAILED
```

---

# 90. ALERTING

Alertas somente quando existe:

- ação;
- risco;
- degradação relevante.

---

# 91. ALERT LEVELS

```text id="4k46ix"
INFO
WARNING
HIGH
CRITICAL
```

---

# 92. SIMPLE VIEW ALERTS

Exemplos:

> “Build continues normally.”

> “Google Calendar needs authorization.”

> “Production deployment failed.”

---

# 93. EXPERT ALERTS

Podem incluir:

- trace;
- service;
- provider;
- error class;
- attempt.

---

# 94. NO ALERT FATIGUE

Retries normais não devem gerar alerta ao usuário.

---

# 95. SLO CONCEPT

O Forge deverá definir objetivos operacionais.

Não necessariamente contratos comerciais no MVP.

---

# 96. BUILD SLO EXAMPLES

Futuro:

- task state consistency;
- API availability;
- queue processing;
- event delivery.

---

# 97. CONTROL PLANE SLO

Métricas:

- availability;
- error rate;
- latency.

---

# 98. DESKTOP RELIABILITY SLO

Métricas:

- sidecar recovery;
- state reconciliation;
- crash-free sessions.

---

# 99. ENGINE ADAPTER SLO

Métricas:

- invocation success;
- output parsing success;
- cancellation success.

---

# 100. ERROR TAXONOMY

Erros deverão possuir classificação padronizada.

Exemplo:

```text id="qa5ekh"
AUTH_ERROR
POLICY_DENIED
ENGINE_UNAVAILABLE
ENGINE_TIMEOUT
TOOL_FAILURE
TEST_FAILURE
REVIEW_FAILURE
DEPLOY_FAILURE
STATE_CONFLICT
COST_LIMIT
```

---

# 101. FAILURE TYPE

Deve permitir distinguir:

> infraestrutura

de:

> código produzido.

---

# 102. RETRYABILITY

Erro deverá indicar:

```text id="uq0gxh"
retryable = true/false
```

quando determinável.

---

# 103. INCIDENT CREATION

Falhas repetidas ou críticas podem gerar Incident automaticamente.

---

# 104. INCIDENT DATA

```text id="w04y88"
severity
project
environment
timeline
affected capability
status
owner
```

---

# 105. INCIDENT TIMELINE

Pode ser reconstruída a partir de:

- domain events;
- audit;
- logs;
- traces.

---

# 106. POSTMORTEM DATA

Após incidente relevante:

- cause;
- contributing factors;
- detection gap;
- remediation;
- follow-up.

---

# 107. OPERATIONS OBSERVABILITY

Aplicações geradas pelo Forge deverão expor um mínimo comum de saúde.

---

# 108. GENERATED APP BASELINE

Incluir quando aplicável:

```text id="v67r8m"
health endpoint
structured logs
request IDs
error tracking
basic metrics
```

---

# 109. CUSTOMER OPERATIONS METRICS

Para o primeiro vertical:

```text id="mm5ftb"
leads_created
conversations_started
appointments_created
human_handoffs
agent_failures
response_latency
```

---

# 110. BUSINESS METRICS

Podem incluir:

```text id="ukqcq5"
conversion
resolution rate
booking rate
handoff rate
```

---

# 111. TECHNICAL ≠ BUSINESS HEALTH

Um sistema pode estar tecnicamente saudável mas:

> não gerar resultado.

Forge deverá distinguir.

---

# 112. VALUE LOOP

Após produção:

```text id="doivdm"
OPERATE
 ↓
MEASURE
 ↓
EVALUATE
 ↓
LEARN
 ↓
PROPOSE
 ↓
IMPROVE
```

---

# 113. IMPROVEMENT SIGNALS

Podem vir de:

- metrics;
- incidents;
- user feedback;
- agent evals;
- costs;
- review trends.

---

# 114. IMPROVEMENT PROPOSAL

Deverá conter:

```text id="598nl8"
observation
evidence
expected impact
risk
recommended change
```

---

# 115. NÃO ALTERAR PRODUÇÃO SILENCIOSAMENTE

Improvement proposal:

> não equivale a deploy automático.

---

# 116. SAFE IMPROVEMENT LOOP

```text id="jfw8uv"
signal
→ proposal
→ build in safe environment
→ test/eval
→ preview
→ gate if consequential
```

---

# 117. MODEL PERFORMANCE HISTORY

O Model Router poderá utilizar histórico:

```text id="6npnwp"
task class
model
success rate
latency
cost
review findings
```

---

# 118. ENGINE PERFORMANCE HISTORY

Execution Router poderá usar:

```text id="c5bmjd"
task class
engine
success
duration
retry rate
handoff rate
defect rate
```

---

# 119. TOOL PERFORMANCE HISTORY

Tool Router poderá considerar:

- reliability;
- latency;
- provider health;
- cost.

---

# 120. ROUTING FEEDBACK LOOP

```text id="ob9bxm"
routing decision
 ↓
execution
 ↓
outcome
 ↓
metrics
 ↓
future routing
```

---

# 121. ROUTING NÃO SERÁ AUTOAPRENDIZ NO MVP

Inicialmente:

> rules + recorded history.

Model-based optimization vem depois.

---

# 122. EVALUATION STORE

Entidades conceituais:

```text id="88vgjo"
eval_suites
eval_cases
eval_runs
eval_results
evaluation_baselines
```

---

# 123. OBSERVABILITY REFERENCES

Forge DB não precisa armazenar todo log bruto.

Guardar:

- trace IDs;
- summaries;
- relevant event references.

---

# 124. DATA RETENTION

Categorias:

### Critical evidence

Retenção longa.

### Audit

Retenção longa.

### Traces

Retenção operacional.

### Debug logs

Retenção curta.

### Raw model payloads

Minimizar ou não guardar.

---

# 125. PROMPT/RESPONSE STORAGE

Não armazenar automaticamente prompts completos de toda execução.

Preferir:

- hash;
- metadata;
- redacted samples;
- explicit debug mode.

---

# 126. DEBUG MODE

Expert/operator poderá ativar logging adicional para investigação.

Com:

- prazo;
- escopo;
- aviso de privacidade.

---

# 127. SIMPLE VIEW — OBSERVABILITY

Exibe:

```text id="nr9am7"
Project health
Build progress
Tests
Security
Pending action
Current milestone
```

---

# 128. EXPERT VIEW — OBSERVABILITY

Acrescenta:

- tasks;
- attempts;
- traces;
- engines;
- models;
- tools;
- costs;
- findings;
- incidents.

---

# 129. MANAGED FACTORY VIEW — FUTURO

Dashboard poderá mostrar:

```text id="p5xzmx"
active projects
blocked projects
build success
cost
incidents
SLA
engine health
```

---

# 130. DASHBOARD PRINCIPLE

Não mostrar dezenas de gráficos sem decisão associada.

Cada métrica deve responder:

> “O que faço com essa informação?”

---

# 131. BUILD DASHBOARD

Simple:

```text id="ja7wpk"
Progress 72%
27 / 36 tasks verified
2 running
0 blocked
```

---

# 132. TEST DASHBOARD

```text id="yz789a"
Critical tests 18/18
Other tests 42/44
2 being fixed
```

---

# 133. REVIEW DASHBOARD

```text id="j6czoa"
Independent review
3 findings
2 resolved
1 low remaining
```

---

# 134. COST DASHBOARD

```text id="ndurhg"
Current build cost
Expected range
Budget consumed
```

---

# 135. ENGINE DASHBOARD — EXPERT

```text id="3w5jgj"
Codex
Healthy

Claude Code
Rate limited

Grok
Not configured
```

---

# 136. OBSERVABILITY OF PROJECT GRAPH

Métricas possíveis:

- orphan nodes;
- stale documents;
- broken traces;
- inconsistent states.

---

# 137. GRAPH CONSISTENCY EVAL

Job periódico pode verificar:

```text id="jn99o7"
Requirement implemented but no test
Completed task without evidence
Release referencing stale Graph revision
```

---

# 138. DOCUMENT FRESHNESS EVAL

Documentos:

```text id="2xii10"
CURRENT
POTENTIALLY_STALE
OUTDATED
SUPERSEDED
```

---

# 139. DOCUMENT STALENESS TRIGGER

Exemplo:

Architecture document gerado antes de grande mudança estrutural.

Resultado:

> mark potentially stale.

---

# 140. EVAL OF AUTONOMY

Precisamos medir se o Forge está realmente autônomo.

---

# 141. AUTONOMY METRICS

```text id="6q69sm"
manual interventions
human gates
unnecessary gates
auto-fixed failures
auto-resolved reviews
successful handoffs
```

---

# 142. GOVERNANCE QUALITY

Métrica crítica:

> decisões críticas foram bloqueadas corretamente?

---

# 143. FALSE GATE RATE

Quando Forge interrompe humano sem necessidade.

---

# 144. MISSED GATE RATE

Mais grave:

> Forge executa algo que deveria ter exigido aprovação.

---

# 145. SECURITY EVALS

Casos recorrentes:

- path escape;
- prompt injection;
- cross-tenant;
- secret exposure;
- unauthorized deploy.

---

# 146. ADVERSARIAL EVAL SUITE

Deverá existir antes de produção relevante.

---

# 147. AGENT BEHAVIOR REGRESSION

Atualização de agente/modelo deverá executar suas eval suites.

---

# 148. RELEASE QUALITY GATE

Release do próprio Forge deverá verificar:

- unit/integration;
- engine contracts;
- security;
- critical evals;
- regression.

---

# 149. GENERATED SYSTEM QUALITY GATE

Sistemas produzidos também terão perfil de qualidade proporcional ao nível:

```text id="nd75qe"
LIGHT
STANDARD
FULL
```

---

# 150. LIGHT EVALUATION

- critical flow;
- tests;
- basic security.

---

# 151. STANDARD EVALUATION

Acrescenta:

- agent behavior;
- independent review;
- integration failures.

---

# 152. FULL EVALUATION

Acrescenta:

- adversarial evals;
- deeper security;
- performance;
- formal acceptance.

---

# 153. PERFORMANCE OBSERVABILITY

Métricas:

- API latency;
- queue delay;
- Graph query latency;
- local runtime response;
- preview startup.

---

# 154. FRONTEND PERFORMANCE

Medir:

- app startup;
- project load;
- STUDIO load;
- realtime lag.

---

# 155. LOCAL RUNTIME METRICS

```text id="eixzw7"
sidecar uptime
process crashes
restarts
command duration
preview process health
```

---

# 156. CLOUD CONTROL PLANE METRICS

```text id="0pzn5c"
API availability
API latency
queue backlog
worker failures
DB errors
```

---

# 157. DATABASE OBSERVABILITY

Monitorar:

- query latency;
- connection usage;
- failed transactions;
- RLS policy failures quando relevante;
- queue depth.

---

# 158. PGMQ OBSERVABILITY

Métricas:

- messages ready;
- messages in-flight;
- retries;
- age of oldest task.

---

# 159. STUCK TASK DETECTION

Regra:

> task RUNNING sem heartbeat/progress além do limite.

Resultado:

- watchdog;
- retry/handoff;
- alert se necessário.

---

# 160. LOOP DETECTION

Exemplo:

```text id="e8425s"
attempt 1 fail
attempt 2 same fail
attempt 3 same fail
```

Criar:

> repeated_failure signal.

---

# 161. COST ANOMALY DETECTION

Exemplo:

> Task simples consumindo 10× histórico esperado.

Ação:

- notify JEV;
- alter routing;
- pause se hard limit.

---

# 162. BASELINE COST

Histórico futuro poderá calcular:

> custo esperado por task class.

---

# 163. INCIDENT AUTOMATION

Evento CRITICAL pode automaticamente:

- set Project Health = INCIDENT;
- notify operator;
- Safe Mode dependendo de política.

---

# 164. TRACEABILITY DA DECISÃO

Para decisão importante do JEV:

guardar:

- input summary;
- output;
- reason category;
- selected engine/model/tool;
- outcome.

---

# 165. NÃO GUARDAR CHAIN-OF-THOUGHT

Observabilidade não deve depender de capturar raciocínio interno privado do modelo.

Guardar:

> decisão estruturada e justificativa operacional suficiente.

---

# 166. DECISION RECORD

Exemplo:

```text id="ck7b2b"
Task: T-41
Decision: switch engine
Reason: Claude rate-limited
Selected: Codex
Risk: LOW
Human gate: no
Outcome: success
```

---

# 167. EVALUATION EXPLAINABILITY

Quando um eval falhar, deve indicar:

- critério;
- evidência;
- impacto.

Não apenas:

> score 0.62.

---

# 168. HUMAN REVIEW SUPPORT

Reviewer humano deverá receber:

- requirements;
- evidence;
- findings;
- changed artifacts.

Não raw telemetry excessiva.

---

# 169. QUALITY TREND

Futuro:

acompanhar qualidade por versão.

Exemplo:

```text id="bt8j1b"
v1.0 defect rate
v1.1 defect rate
v1.2 defect rate
```

---

# 170. AGENT TREND

Detectar:

> agent prompt update aumentou findings.

---

# 171. ENGINE TREND

Detectar:

> engine ficou mais lenta ou instável.

---

# 172. MODEL DRIFT

Se provider/model muda comportamento:

> eval regression pode detectar.

---

# 173. OBSERVABILITY OWNERSHIP

### Forge Platform

Observa infraestrutura Forge.

### Project

Observa build/projeto.

### Generated Application

Observa aplicação construída.

---

# 174. NÃO MISTURAR DOMÍNIOS

Logs de cliente A:

> isolados de cliente B.

---

# 175. TENANT-AWARE OBSERVABILITY

Dashboards e queries deverão respeitar:

- organization;
- project;
- environment.

---

# 176. TRACE PRIVACY

Trace metadata também pode ser sensível.

Aplicar:

- minimização;
- access control;
- retention.

---

# 177. EVAL DATA ACCESS

Golden datasets e eval results:

> acessíveis apenas conforme papel.

---

# 178. SIMPLE VIEW DOES NOT SHOW RAW COST TOKENS BY DEFAULT

Mostrar:

> custo compreensível.

Expert pode detalhar tokens/provider.

---

# 179. PROGRESS CALCULATION

Derivado de:

```text id="63wrfl"
Task weights
+
task states
+
phase
```

---

# 180. NÃO USAR TIMER PARA SIMULAR PROGRESSO

Progresso só aumenta quando trabalho real muda de estado.

---

# 181. READY FOR HUMAN TEST TIMELINE

O usuário deverá conseguir ver:

```text id="vyn7cq"
Built
Tested
Reviewed
Secured
Ready
```

---

# 182. QUALITY EVIDENCE PACKAGE

Ao finalizar Build:

```text id="svllpc"
Build Summary
Test Report
Review Report
Security Summary
Known Issues
Requirement Coverage
```

---

# 183. RELEASE EVIDENCE PACKAGE

Antes de produção:

```text id="eg201m"
Release Candidate
Acceptance
Final Tests
Security
Migration Plan
Rollback Plan
Approval
```

---

# 184. OBSERVABILITY MVP — P0

Obrigatório:

```text id="swoc4d"
OpenTelemetry instrumentation
structured logs
trace/correlation IDs
task/build metrics
engine health
test/review metrics
audit correlation
basic cost attribution
Project Health
watchdog signals
Ready-for-Test evidence
basic generated-app health
```

---

# 185. EVALUATION MVP — P0

```text id="frnvnq"
deterministic test evidence
requirement coverage
independent review
security checks
engine handoff validation
critical agent behavior evals
Ready-for-Test gate
```

---

# 186. P1

```text id="vto85v"
golden datasets
prompt regression
model comparison
advanced cost analytics
quality trends
agent scorecards
advanced dashboards
```

---

# 187. P2

```text id="pxxqqp"
predictive routing
automatic model optimization
cross-project anonymized benchmarks
advanced SLO platform
Managed Factory observability
```

---

# 188. DATA MODEL ADDITIONS

FDP-12 poderá ganhar tabelas:

```text id="rf47vp"
eval_suites
eval_cases
eval_runs
eval_results
health_snapshots
metric_summaries
```

Raw telemetry não precisa ficar no Postgres principal.

---

# 189. EVAL SUITE

Campos conceituais:

```text id="6ofqo0"
id
owner_type
owner_id
name
version
status
minimum_policy
```

---

# 190. EVAL CASE

```text id="d73011"
suite_id
input_reference
expected_behavior
evaluation_method
threshold
criticality
```

---

# 191. EVAL RUN

```text id="w5s3lx"
suite_id
target_version
model
engine
status
started_at
completed_at
cost
```

---

# 192. EVAL RESULT

```text id="l5yd6l"
case_id
status
score
evidence
finding_id
```

---

# 193. PROJECT HEALTH SERVICE

Componente lógico:

```text id="plwi9s"
ProjectHealthService
```

Inputs:

- tasks;
- findings;
- incidents;
- deployments;
- providers.

Output:

> health state + reasons.

---

# 194. BUILD PROGRESS SERVICE

Componente separado:

```text id="1c66yb"
BuildProgressService
```

Não confundir com Project Health.

---

# 195. EVIDENCE SERVICE

Já previsto.

Será responsável por:

- completion evidence;
- requirement coverage;
- Ready-for-Test eligibility.

---

# 196. EVALUATION SERVICE

Novo componente:

```text id="nruuol"
EvaluationService
```

Responsável por:

- suites;
- runs;
- regression;
- thresholds.

---

# 197. OBSERVABILITY SERVICE

Responsável por:

- instrumentation;
- correlation;
- telemetry context;
- health events.

---

# 198. COST SERVICE

Responsável por:

- usage attribution;
- estimated cost;
- budget consumption.

---

# 199. CRITICAL ARCHITECTURAL RULE

Nenhum desses serviços deverá:

> bloquear build por métrica não essencial.

Blocking deve vir de:

- explicit gate;
- policy;
- required evaluation.

---

# 200. NO METRIC-DRIVEN CHAOS

Métrica informa.

Policy decide.

---

# 201. ACCEPTANCE SCENARIO — BUILD

Ao iniciar build, devemos conseguir observar:

```text id="nlnh23"
Build
→ 18 tasks
→ 5 complete
→ 2 running
→ Codex healthy
→ Claude rate-limited
→ 0 human actions required
```

---

# 202. ACCEPTANCE SCENARIO — HANDOFF

Claude falha.

Sistema registra:

- attempt failure;
- engine health;
- handoff;
- Codex attempt;
- success;
- test evidence.

---

# 203. ACCEPTANCE SCENARIO — QUALITY

Feature implementada, mas review acha HIGH.

Resultado:

> não fica Verified.

Forge corrige e reavalia.

---

# 204. ACCEPTANCE SCENARIO — SECURITY

Prompt injection detectada.

Resultado:

- tool call bloqueado;
- security event;
- build pode continuar se seguro.

---

# 205. ACCEPTANCE SCENARIO — COST

Task ultrapassa soft threshold.

Resultado:

> routing pode mudar.

Hard threshold:

> action required.

---

# 206. ACCEPTANCE SCENARIO — OPERATIONS

Aplicação publicada começa a apresentar erro.

Forge mostra:

> Needs Attention

com causa operacional compreensível.

---

# 207. DECISÕES FROZEN DO FDP-14

1. OpenTelemetry será o padrão de instrumentação.
2. Logs serão estruturados e correlacionados.
3. Raw telemetry e domain events serão separados.
4. Project/Task/Attempt serão chaves centrais de correlação.
5. Engine handoff será explicitamente observável.
6. Costs serão atribuíveis por projeto/task/attempt quando possível.
7. Human Interruption Rate será KPI central.
8. Time to First Visual será KPI central.
9. Autonomous Build Success será KPI central.
10. Ready for Human Test dependerá de Evidence Service.
11. Evaluations serão deterministic/rule/model/human/production.
12. Model-based eval nunca será único gate para requisito técnico crítico.
13. Prompt/model/agent versions poderão ser avaliados contra baselines.
14. Project Health será derivado.
15. Build Progress será derivado de estado real.
16. No fake percentages.
17. Raw prompts/source code não serão coletados indiscriminadamente.
18. Generated applications terão health baseline mínimo.
19. Improvement loop será evidence-driven.
20. Observability deverá apoiar autonomia, não criar ruído ou approval fatigue.

---

# 208. PRINCIPAIS RISCOS

## R1 — Telemetry explosion

Mitigação:
retenção e níveis.

## R2 — Privacy leakage

Mitigação:
redaction/minimização.

## R3 — Fake quality scores

Mitigação:
evidence-based evals.

## R4 — LLM reviewing LLM endlessly

Mitigação:
deterministic tests + independent evidence.

## R5 — Dashboard overload

Mitigação:
Simple/Expert separation.

## R6 — Metrics without action

Mitigação:
priorizar indicadores decisórios.

## R7 — Cost tracking inaccurate

Mitigação:
marcar custos estimados versus confirmados.

## R8 — Evaluation overfitting

Mitigação:
varied/adversarial cases + human validation.

---

# 209. CRITÉRIO DE SUCESSO

O FDP-14 estará corretamente implementado quando conseguirmos perguntar:

> “Por que este build está demorando?”

> “Qual engine falhou?”

> “Quanto esta feature custou?”

> “Quais testes provaram que ela funciona?”

> “Por que o projeto está Needs Attention?”

> “Essa nova versão do agente ficou melhor ou pior?”

e o Forge responder com evidência, não com suposição.

---

# 210. PRINCÍPIO FINAL

O Forge não poderá ser uma fábrica que apenas **faz**.

Precisa ser uma fábrica que sabe:

> **o que fez, quanto custou, se funcionou, como foi validado e o que deve melhorar.**

Portanto:

# **NO AUTONOMY WITHOUT OBSERVABILITY.  
NO “DONE” WITHOUT EVIDENCE.**

---

# 211. PRÓXIMA ETAPA

Com aprovação:

# **FDP-15 — INTEGRATION / ADAPTER SPECIFICATION**

Definiremos formalmente os contratos de integração para:

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

Também definiremos:

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

# 212. GATE FDP-14

**Status recomendado:** APPROVE

Com aprovação:

```text id="9qodzc"
FDP-10 ✅ Technical Architecture
FDP-11 ✅ Frontend / UX
FDP-12 ✅ Data Architecture
FDP-13 ✅ Security Architecture
FDP-14 ✅ Observability & Evaluation
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

## FDP-14 — FIM
