# Fechamento dos findings — Codex Round 5 para baseline v1.3
Estado da entrega: ROUND 6 — CANDIDATE FOR CODEX REVIEW.
Este registro não é o parecer do Codex. Nenhum teste de produto foi executado. Nenhuma aprovação foi inferida.

| Campo | HIGH-01 |
|---|---|
| ID | HIGH-01 — Ledger financeiro e ciclo de Operation |
| Causa-raiz | A v1.2 reservava orçamento, mas não definia liquidação, liberação, custo real diferente do estimado, concorrência nem estados terminais. `RECEIPT` não era um protocolo contábil. |
| Correção | Seção 8A de FDP-16A v1.3: transações de reserva, dispatch, settlement, release e bloqueio. Invariante `spent + reserved <= limit`. `spent` só aumenta no settlement. Uma operation_ref liquida no máximo uma vez. Oráculos LEDGER-01 a LEDGER-05 em F-015. |
| Arquivo | docs/planning/FDP-16A-v1.3-EXECUTION-CONTRACTS.md; FDP-19A v1.3 F-015; matriz v1.3 |
| Evidência | FDP-16A seção 8A, linha 305; matriz LEDGER-01..05; F-015 lista esses ids |
| Verificação | Busca: não resta status terminal `RECEIPT` como fim da contabilidade. O checker exigiu os cinco oráculos e a seção 8A. Resultado: presentes. |
| Estado | RESOLVIDO |

| Campo | HIGH-02 |
|---|---|
| ID | HIGH-02 — DeploymentApproval |
| Causa-raiz | `environment_id` era um enum de tipo, então dois ambientes PRODUCTION não se distinguiam, e os oráculos só cobriam digest, expiração e replay. |
| Correção | `environment_id` é uuid da linha `forge.environments` (FDP-12 §21). `environment_class` guarda o tipo (FDP-12 §22). A seção 8B compara o tuple inteiro e devolve `mismatch_field`. Oráculos DEPLOY-04 a DEPLOY-11, um por campo, além de DEPLOY-02 e DEPLOY-03. |
| Arquivo | FDP-16A v1.3 seções 3.8 e 8B; F-029; matriz v1.3 |
| Evidência | FDP-16A linha 325; matriz linha 67 (DEPLOY-05, dois PRODUCTION); F-029 linha 1269 |
| Verificação | Confirmação de que `environment_id \| enum` não existe mais e de que DEPLOY-04..11 são linhas únicas. |
| Estado | RESOLVIDO |

| Campo | HIGH-03 |
|---|---|
| ID | HIGH-03 — Interfaces dos Engine Adapters |
| Causa-raiz | F-012 exigia só describe/health/invoke/cancel e parte das operações, e dependia de F-011 mesmo citando vault de F-006. FDP-15 ainda não está aprovado, mas a v1.2 encolhia a superfície e alegava compatibilidade. |
| Correção | F-012 depende de F-011 e de F-006. Os nove métodos de FDP-15 §8 / FDP-06 linhas 353–361 devem ser declarados como suportados ou não suportados. Método ausente das duas listas falha ADAPT-01. FDP-15 continua pendente de aprovação; a lista não é tratada como aprovada. |
| Arquivo | FDP-19A v1.3 F-012; matriz ADAPT-01; FDP-16 v1.3 |
| Evidência | Source de F-012 cita FDP-15 linhas 227–232 e o estado pendente |
| Verificação | `start_task` presente na história e nos passos de ADAPT-01. A frase de aprovação do FDP-15 não foi adicionada. |
| Estado | RESOLVIDO |

| Campo | HIGH-04 |
|---|---|
| ID | HIGH-04 — Papel do AIOX |
| Causa-raiz | FDP-06 §15 e §17 dizem framework preferencial e não ponto único de falha. F-013 v1.2 dizia que o adapter AIOX era a única entrada do MVP. |
| Correção | Caminho preferencial Forge → AIOX → engine. Fallback `FORGE_DIRECT` só para side_effects NONE ou INTERNAL. Deploy e efeitos externos continuam negados. Estado, logs e evidência ficam nas tabelas do Forge nos dois caminhos. Change Decision só para deixar de preferir o AIOX. Teste AIOX-01. |
| Arquivo | FDP-16 v1.3 linha 6; F-013 linhas 566–573; matriz AIOX-01 linha 59 |
| Evidência | A frase "only supported orchestrator entry" não existe na v1.3 |
| Verificação | Busca negativa por essa frase no registro e no FDP-16. Resultado: ausente. |
| Estado | RESOLVIDO |

| Campo | HIGH-05 |
|---|---|
| ID | HIGH-05 — Cobertura dos oráculos |
| Causa-raiz | A matriz não tinha passos, e F-016 apontava QUEUE-01 e ENG-02 para requisitos de checkpoint, grants, attempt novo e crash que esses oráculos não testavam. |
| Correção | Coluna Steps em toda linha. HANDOFF-01 cobre digest inválido, attempt anterior terminal, revogação de grant, um único attempt não terminal e crash no meio do handoff. ENGINE-ALLOW-01, REVIEW-01, CTX-01 e BRIDGE-01 fecham buracos equivalentes de F-011, F-017, F-036 e F-023. A matriz v1.3 continua sendo a única autoridade de PASS/FAIL. |
| Arquivo | FDP-TRACEABILITY-MATRIX-v1.3-CANONICAL.md; F-016 linha 695 |
| Evidência | HANDOFF-01 na linha 60 da matriz |
| Verificação | Todo id citado em `Tests:` das 41 histórias existe como linha da matriz. F-016 não cita mais QUEUE-01. |
| Estado | RESOLVIDO |

| Campo | HIGH-06 |
|---|---|
| ID | HIGH-06 — Rastreabilidade |
| Causa-raiz | A linha Source apontava para o próprio índice v1.2 e para a matriz gerada. |
| Correção | Cada história separa requisito herdado (documento, seção ou linha), estado de aprovação da fonte, FDP-14, FDP-15 e o que é proposta nova da v1.3. Onde o extrato não contém o requisito, isso está escrito, em vez de inventar uma linha. |
| Arquivo | FDP-19A v1.3, bloco Source de F-001 a F-041 |
| Evidência | 41 ocorrências de `- Inherited:`. F-001 cita FDP-13 linhas 2273 e 2275. F-008 declara que a tela não tem uma linha de extrato. |
| Verificação | A frase `FDP-19 v1.2 index` não aparece. Nenhuma história diz que FDP-14 ou FDP-15 já foram aprovados. |
| Estado | RESOLVIDO |

| Campo | MEDIUM-01 |
|---|---|
| ID | MEDIUM-01 — Estados de Build e Attempt |
| Causa-raiz | Só Task tinha matriz. A prosa do watchdog permitia expirar CREATED. CHANGES_REQUESTED e desbloqueio não tinham destino. |
| Correção | Seções 7.1 e 7.2. Watchdog em CREATED ou QUEUED devolve 409 NOT_EXECUTING. Unblock de Build volta para `blocked_from`. DeriveRhft só sai de REVIEWING. |
| Arquivo | FDP-16A v1.3 seções 7.1 e 7.2 |
| Evidência | Termo `blocked_from` e `NOT_EXECUTING` no contrato |
| Verificação | Presentes no texto gerado e exigidos pelo checker. |
| Estado | RESOLVIDO |

| Campo | MEDIUM-02 |
|---|---|
| ID | MEDIUM-02 — Identidade dos agregados |
| Causa-raiz | `id` e `task_id` / `build_id` / `attempt_id` coexistiam sem dizer se eram a mesma coluna. |
| Correção | Regra de identidade na linha 33 de FDP-16A: a chave primária é `id`; os outros nomes são colunas geradas iguais a `id`, exceto `operation_ref`, que não é alias de `operation.id`. |
| Arquivo | FDP-16A v1.3, linha 33 |
| Evidência | Parágrafo "Identity rule" |
| Verificação | Leitura direta dessa linha. |
| Estado | RESOLVIDO |

| Campo | MEDIUM-03 |
|---|---|
| ID | MEDIUM-03 — Recuperação sem API de receipt |
| Causa-raiz | O crash pós-dispatch mandava consultar "the provider receipt API" para todo provider. |
| Correção | Seção 8C. `receipt_query` é SUPPORTED ou ABSENT. Se for ABSENT, o estado é BLOCKED_RECONCILIATION, a reserva permanece HELD e o redispatch é proibido até um humano registrar prova. LEDGER-05 testa isso. |
| Arquivo | FDP-16A v1.3 linha 332 e linha 371 |
| Evidência | A instrução antiga "reconcile with the provider receipt API" foi removida |
| Verificação | Busca negativa por essa frase. Resultado: ausente. |
| Estado | RESOLVIDO |

| Campo | MEDIUM-04 |
|---|---|
| ID | MEDIUM-04 — Conjunto de READY_FOR_HUMAN_TEST |
| Causa-raiz | F-039 dizia que FDP-20 listava as tarefas obrigatórias, mas FDP-20 só tinha sprints, inclusive P2 e opcionais. |
| Correção | FDP-20 v1.3, seção "Required set for READY_FOR_HUMAN_TEST", linha 40. Lista fechada do que entra e do que não entra. F-039 aponta para essa seção, não para a tabela de sprint. |
| Arquivo | FDP-20-v1.3-SPRINT-IMPLEMENTATION-PLAN.md linha 40; F-039 |
| Evidência | F-020, F-021, F-022, F-023, F-024, F-025, F-040 e F-041 estão fora do conjunto |
| Verificação | A seção existe e F-025 continua sem sprint. |
| Estado | RESOLVIDO |

| Campo | MEDIUM-05 |
|---|---|
| ID | MEDIUM-05 — Prontidão das 41 histórias |
| Causa-raiz | Critério técnico e pendência de pessoa/horas estavam no mesmo DoR, o que permitia ler as histórias como prontas para execução. |
| Correção | DoR técnico e DoR operacional separados. O operacional diz explicitamente que não está atendido. Nenhuma história é marcada READY. |
| Arquivo | FDP-19A v1.3, em todas as histórias |
| Evidência | "Definition of Ready — operational" e "Not met" |
| Verificação | A pendência de nomes e timeboxes continua aberta de propósito e está na lista pós-revisão. Isso não reabre o texto técnico. |
| Estado | RESOLVIDO no texto. A nomeação humana permanece pendência, não finding documental em aberto. |

## O que não foi reaberto
C03, C04, C06 e C08 permanecem como o Codex os aceitou. Os 17 P0, a matriz única, as classes A/B/C e os metadados de não aprovação foram mantidos. Os 11 estados de Task não mudaram. BUILD-00 não foi autorizado.
