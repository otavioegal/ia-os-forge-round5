# CMP-FD-01 v0.3 — Ledger, teto pai e escopo

**Estado:** PROPOSTA. Não integrada. Não executada. Não é PASS.
**Schema id proposto:** `forge.conversation.delta.v2`. Não altera o arquivo histórico FDP-16A v1.7.
**Achados alvo:** HIGH-01, NEW-HIGH-01, NEW-HIGH-02, NEW-HIGH-03, NEW-MEDIUM-01. Fechamento não declarado pelo autor.

A v0.2 criava um Build por sessão e copiava `budget_limit_minor` do comando de abertura. Isso multiplicava o teto. A v0.3 revoga essa proposta. O texto da v0.2 não é editado; deixa de ser a proposta vigente.

## 1. O que permanece

- Ator novo `conversation_router`, só no delta. Não é `coding_engine`. Não chama `InvokeCapability`.
- Comando próprio `ReserveConversationalCapability`. O efeito monetário de reserva é o mesmo de `InvokeCapability`: uma Operation `RESERVED`, uma reservation `HELD`, `reserved_minor += estimate`, nenhuma chamada de provider na transação.
- Prova só por `forge.provider_ingest`. O roteador não captura prova. AQ-12 continua não decidido: sem prova conclusiva, HELD, sem recibo fictício.
- `Task.build_id` continua NOT NULL. `Operation.task_id` continua NOT NULL.
- Famílias de adapter continuam ENGINE, MODEL, TOOL. Sem quarta família (AQ-03).
- Denylist da âncora: `deploy.`, `release.`, `terminal.`, `shell.`, `vault.`, `secret.`, `credential.`, `ledger.reconcile`, `ledger.proof_ingest`, `DeployRelease`, `MergeTask`, `StopBuild`, `InvokeCapability`. Código `403 CAPABILITY_FORBIDDEN_ON_ANCHOR`.
- Task de sessão não entra no DAG de produto: `dependency_task_ids = {}`, zero `TaskAttempt`, zero lease, zero worktree, zero checkpoint. `ClaimTask`, `SubmitForReview`, `VerifyTask`, `BeginHandoff`, `MergeTask`: `409 NOT_A_BUILD_DAG_TASK`.
- Lock intra-build depois do primeiro lock, na ordem v1.7: Operation, depois Reservation, depois ManualReconciliation. Nunca invertida.
- Não existe tabela `conversation_ledger`. Não há moeda nova. `pending_actual_minor` não é atribuído por regra nova.

## 2. Três números que não se confundem

| Nome | Onde vive | Quem escreve | O que é |
|---|---|---|---|
| Teto do projeto conversacional | `build.budget_limit_minor` do único Build `CONVERSATIONAL_BUDGET_ROOT` do projeto, igual a `authorization.ceiling_minor` | só `AuthorizeConversationalBudget`, ator `human` | o único teto das sessões daquele projeto |
| Fatia da sessão | `task.session_slice_minor` | `OpenConversationalAnchor`, depois do lock, como parcela do teto | cap da sessão. Não é dinheiro e não soma um teto novo |
| Gasto e reserva | `budget_spent_minor` e `budget_reserved_minor` do mesmo Build pai | só o protocolo v1.7 de reserva, liquidação e release | o ledger |

Invariantes, todos no mesmo Build pai:

1. `budget_spent_minor + budget_reserved_minor <= budget_limit_minor` em linha comprometida.
2. `build.budget_limit_minor = authorization.ceiling_minor` da autorização `ACTIVE` daquele projeto.
3. Soma de `session_slice_minor` das tasks em `OPEN`, `CLOSING` ou `ORPHAN_HELD` `<= budget_limit_minor`.
4. Para cada task, soma das reservations `HELD` mais o que já foi `SETTLED` nessa task `<= session_slice_minor`.

Abrir a sessão A com fatia X e a sessão B com fatia X, quando o teto é X, viola a invariante 3. O segundo comando não cria Build, não altera `budget_limit_minor` e não reserva.

Builds `PRODUCT` continuam com o teto próprio da v1.7. Esta proposta não os funde com o teto conversacional e não os usa como âncora. Fundir os dois números seria outra decisão humana; está em CMP-FD-11. O defeito fechado aqui é a multiplicação **entre sessões**.

## 3. Agregados

### 3.1 Autorização — não é ledger

Tabela proposta `forge.conversational_budget_authorization`. Não tem `spent`, `reserved`, movement nem prova.

| Campo | Tipo | Null | Regra |
|---|---|---|---|
| authorization_id | uuid | no | PK |
| organization_id | uuid | no | |
| project_id | uuid | no | o projeto pertence à organização |
| ceiling_minor | int64 | no | `>= 0` |
| currency | string | no | `USD` |
| policy_version | string | no | |
| authorized_by_actor_ref | string | no | humano |
| authorized_by_actor_class | enum | no | literal `human` |
| status | enum | no | `ACTIVE`, `SUPERSEDED`, `REVOKED` |
| command_id | uuid | no | único |
| version | int64 | no | começa em 1 |

No máximo uma linha `ACTIVE` por `(organization_id, project_id)`.

`conversation_router`, `coding_engine`, adapter e modelo recebem `403 ACTOR_FORBIDDEN` se chamarem este comando.

### 3.2 Build pai

Um por `(organization_id, project_id)`.

| Campo | Regra |
|---|---|
| kind | `CONVERSATIONAL_BUDGET_ROOT` |
| plan_revision | literal `conversational-budget-root-plan-v1` |
| graph_revision | literal `conversational-budget-root-graph-v1` |
| budget_limit_minor | copiado da autorização na mesma transação. Jamais do payload de abertura de sessão |
| budget_spent_minor, budget_reserved_minor | 0 na criação |
| status | `SESSION_ACTIVE` enquanto a autorização está `ACTIVE` ou existe reservation não terminal. `SESSION_CLOSED` só no fecho do próprio root, nunca porque uma sessão fechou |
| authorization_id | FK da autorização `ACTIVE` que fixou o teto |

Status `SESSION_ACTIVE` e `SESSION_CLOSED` continuam ilegais em Build `PRODUCT` (`409 ILLEGAL_BUILD_KIND`). Consumidor que não conhece o valor falha fechado. Não trata `SESSION_ACTIVE` como `RUNNING` de produto.

O grafo root tem as tasks de sessão e **zero arestas**. Não é membro de plano de sprint. Task de produto não depende dele e ele não depende de task de produto (`409 DAG_KIND_MIX`, `409 GRAPH_KIND_MIX`).

`DeriveRhft`, `MarkTesting`, `MarkReviewing`, `SubmitForApproval`, `ApprovePlan` neste Build: `409 ILLEGAL_BUILD_KIND`.

### 3.3 Task de sessão

Uma task por `session_id`. Várias tasks apontam para o **mesmo** `build_id`. `build_id` NOT NULL.

| Campo | Regra |
|---|---|
| execution_domain | `CONVERSATIONAL_SESSION` |
| session_status | `OPEN`, `CLOSING`, `CLOSED`, `ORPHAN_HELD` |
| status de task | `SESSION_OPEN`, `SESSION_CLOSING`, `SESSION_CLOSED`, `SESSION_ORPHAN_HELD`. Não usar `RUNNING` |
| session_slice_minor | int64 `>= 0`, parcela, não teto novo |
| dependency_task_ids | `{}` |
| goal / acceptance | literais de sistema, não texto do modelo |

Índice único: uma task em `OPEN|CLOSING|ORPHAN_HELD` por `session_id`. Sessão fechada não reabre a mesma task.

## 4. A transação de reserva

Uma transação. Isolamento `REPEATABLE READ` ou `SERIALIZABLE`, mais os locks abaixo. Isolamento sem esta ordem não basta.

É **proibido** ler `budget_spent_minor`, `budget_reserved_minor`, `budget_limit_minor`, `stop_latch` ou estado de reconciliação antes de o passo C1 ter obtido o lock. Autorização não monetária pode ocorrer na fase A.

### Fase A — estática, sem lock e sem coluna monetária

1. Campo desconhecido, inclusive `budget_limit_minor`, `expected_version` da v0.2, ou teto numérico: `422 UNKNOWN_FIELD`. Nada é escrito.
2. `channel.organization_id = command.organization_id` e o mesmo para `project_id`. Senão `422 CHANNEL_SCOPE`.
3. `actor_class = conversation_router`. Senão `403 ACTOR_FORBIDDEN`.
4. `actor_ref` é o principal de gateway host-attested. Senão `403 ACTOR_IMPERSONATION`. Texto de modelo não altera o envelope.
5. Se o comando for `InvokeCapability`: `403 CONVERSATION_COMMAND_REQUIRED`.
6. Capability fora da allowlist ou na denylist: `403 CAPABILITY_NOT_GRANTED` ou `403 CAPABILITY_FORBIDDEN_ON_ANCHOR`.
7. `expected_task_version` e `expected_build_version` presentes, int64 `>= 1`. Ausência ou null: `422 VALIDATION`.
8. `estimated_cost_minor >= 0`. Consent epoch e capture generation iguais aos correntes quando a capability lê áudio. Classificação e `execution_location` conferidos com o registry, não com o adapter.

### Fase B — identidade, ainda sem coluna monetária

As leituras desta fase pedem só `id`, `organization_id`, `project_id`, `build_id`, `execution_domain`, `session_status`, `kind`. O predicado SQL inclui a org e o projeto do canal. Não existe segunda consulta sem esse predicado.

1. Task `WHERE id = :task_id AND organization_id = :channel_org AND project_id = :channel_project`. Zero linhas: `404 NOT_FOUND`.
2. Build `WHERE id = task.build_id AND organization_id = task.organization_id AND project_id = task.project_id`. Zero linhas: `404 NOT_FOUND`.
3. Sessão com o mesmo par org/projeto. Senão `404 NOT_FOUND`.
4. Se o comando trouxer `build_id` e ele for diferente de `task.build_id`: `409 BUILD_TASK_MISMATCH`. Não se carrega Build de outro tenant para explicar a diferença.
5. Task de produto, kind errado ou sessão não `OPEN`: `409 NOT_SESSION_ANCHOR`, `409 BUILD_KIND_MISMATCH` ou `409 SESSION_NOT_OPEN`.

Predicados que precisam ser todos verdadeiros antes do lock monetário:

- canal = comando = sessão = task = build, em `organization_id` e em `project_id`;
- `project.organization_id = organization_id`;
- `task.build_id = build.id`;
- a Operation que for inserida copia org, projeto e `task_id` da task já resolvida. Não copia de um campo solto que discorde.

`404 NOT_FOUND` tem corpo fixo `{"error_code":"NOT_FOUND","retryable":false,"terminal":true}`. Não inclui org estrangeira, projeto estrangeiro, saldo, goal nem um booleano de existência. O mesmo corpo vale se o UUID não existe e se existe em outro tenant. O audit fica na org do canal, tipo `authz.scope_denied`, com o UUID pedido e a razão `OUT_OF_SCOPE`, sem colunas do recurso estrangeiro. Projeção visível ao cliente não contém esse detalhe.

### Fase C — locks, ordem única, nunca invertida

1. `SELECT` do Build pai `FOR UPDATE`. Este é o primeiro lock. As sessões do projeto compartilham esta linha, então dois gastos distintos serializam aqui.
2. `SELECT` da Task `FOR UPDATE`.
3. Se já existe Operation da chave de idempotência, `SELECT` dela `FOR UPDATE`.
4. Se já existe Reservation, `SELECT` dela `FOR UPDATE`.
5. Se o comando for ler ManualReconciliation, esse lock é o último.

Insert de Operation nova só depois do lock do Build. Nenhum contador foi lido antes do passo 1.

### Fase D — leitura monetária e decisão, só agora

1. Reler `build.version`, `task.version`, `stop_latch`, `budget_limit_minor`, `budget_spent_minor`, `budget_reserved_minor`, bloqueio de reconciliação, `session_slice_minor`, `authorization.ceiling_minor`.
2. Se `build.budget_limit_minor <> authorization.ceiling_minor`: `409 BUDGET_AUTHORIZATION_MISMATCH`. Sem reserva.
3. Se `task.version <> expected_task_version` ou `build.version <> expected_build_version`: rollback, `409 VERSION_CONFLICT`, corpo com `mismatch_aggregate` = `task` ou `build`. Contadores iguais ao valor anterior. Zero Operation nova. Zero Reservation nova.
4. `stop_latch` true: `409 STOP_LATCH`. Reconciliação bloqueante: `409 RECONCILIATION_REQUIRED`. Safe mode: `409 SAFE_MODE`.
5. `headroom = budget_limit_minor - budget_spent_minor - budget_reserved_minor`. Se `estimated_cost_minor > headroom`: `402 BUDGET_EXCEEDED`. Sem insert.
6. Se a soma já comprometida da task mais o estimate excede `session_slice_minor`: `402 BUDGET_EXCEEDED`. Sem insert.
7. Mesma chave e mesmo digest já `RESERVED`, `DISPATCHED`, `RECONCILING`, `BLOCKED_RECONCILIATION` ou `SETTLED`: não criar segunda reservation. Mesmo `command_id` já comprometido: `200 IDEMPOTENT_REPLAY`, mesmo que a version corrente já tenha andado. `command_id` novo com version velha: `409 VERSION_CONFLICT`, não replay.
8. `operation_ref` reutilizado com digest diferente: `409 OPERATION_REF_REUSED`.
9. Só então: insert Operation `RESERVED`, insert reservation `HELD`, `reserved_minor += estimated_cost_minor`, incrementar `task.version` e `build.version`, audit `budget.reserved` e outbox na mesma transação.
10. Proibido chamar provider nesta transação.

Dois comandos distintos com estimates que juntos passam do headroom: o primeiro a obter C1 compromete; o segundo lê o contador já incrementado e recebe `402`. Não há caminho em que os dois leiam o mesmo headroom e os dois comprometam. A constraint de unicidade continua necessária para a mesma chave; ela não substitui o lock para chaves diferentes.

Replay de `command_id` que não chegou a commit, com version já mudada por outro comando: `409 VERSION_CONFLICT`. Não vira sucesso.

## 5. Comandos

### AuthorizeConversationalBudget

- Ator: `human`, capability `budget.authorize_conversation`, Policy Service. Não é o roteador.
- Payload: `organization_id`, `project_id`, `ceiling_minor >= 0`, `currency=USD`, `policy_version`, `command_id`. Sem `task_id`. Sem provider.
- Primeira vez, quando o root não existe: a transação insere a autorização e o Build com `spent=0`, `reserved=0`, `limit=ceiling_minor`. Não há headroom anterior para ler. Duas criações concorrentes: a unicidade `(organization_id, project_id, kind)` faz a perdedora falhar sem segundo teto.
- Emenda, quando o root existe: C1 primeiro, só então ler `spent` e `reserved`. Novo teto `< spent + reserved`: `409 CEILING_BELOW_COMMITTED`, teto antigo permanece. Sucesso substitui o número; não soma. A autorização anterior fica `SUPERSEDED`.
- Revogação: status `REVOKED`. Não apaga Operation, reservation, movement nem prova. Novas reservas e novas sessões recebem `409 BUDGET_AUTHORITY_REQUIRED`. HELD continua HELD.

### OpenConversationalAnchor

- Ator: `conversation_router` via gateway.
- Payload permitido: `session_id`, `organization_id`, `project_id`, `policy_version`, `budget_authorization_ref`, `command_id`, `expected_build_version`, `requested_session_slice_minor` opcional `>= 0`.
- `budget_limit_minor` no payload: `422 UNKNOWN_FIELD`. O comando não escolhe teto.
- Não insere Build. Se não há root `ACTIVE` no projeto do canal: `409 BUDGET_AUTHORITY_REQUIRED`.
- Transação: fases A e B, depois C1, depois leitura do teto e da soma das fatias abertas. A fatia pedida, ou o restante se o campo veio omitido, só é gravada se a soma nova `<= budget_limit_minor` e o `budget_authorization_ref` é a autorização `ACTIVE`. Senão `409 SLICE_CEILING` ou `409 BUDGET_AUTHORIZATION_MISMATCH`, sem task nova e sem mudança de contador.
- Omitir a fatia não eleva o teto. No máximo consome o restante já autorizado.
- Consentimento de microfone não é esta abertura.

### CloseConversationalAnchor e SweepOrphanConversationalAnchor

Iguais em regra de dinheiro à v0.2, agora sobre a task, não sobre um Build por sessão:

- Operation `DISPATCHED`, `RECONCILING` ou `BLOCKED_RECONCILIATION`: task `ORPHAN_HELD`, fatia continua contando no teto, Build pai permanece `SESSION_ACTIVE`, nenhum `ReleaseReservation`.
- Todas as operations terminais e sem prova contraditória: task `SESSION_CLOSED`, fatia sai da soma, grants de mídia revogados. O Build pai só vai a `SESSION_CLOSED` se a autorização está `REVOKED`, não há task aberta e não há reservation HELD.
- Sweep é ator `system`. TTL de planejamento `forge.conversation.anchor_orphan_ttl_ms = 120000`. Não é SLO. Timeout não libera dinheiro.

### ReserveConversationalCapability

Payload, além do envelope v1.7: `task_id`, `capability`, `operation_ref`, `input`, `normalized_input_digest`, `estimated_cost_minor`, `expected_task_version`, `expected_build_version`, `consent_grant_epoch`, `capture_generation`, `data_classification`, `execution_location`, `invocation_id`.

`build_id` não é autoridade. Se vier e discordar da task, fase B produz `409 BUILD_TASK_MISMATCH`.

Resposta 200: `operation_id`, `operation_ref`, `status=RESERVED`, `reservation_id`, `estimated_minor`, `build_id`, `task_id`, `build_version`, `task_version`, `event_id`.

Índice histórico `(project_id, task_id, operation_ref, capability, normalized_input_digest)` preservado. Constraint aditiva das capabilities conversacionais: único `(project_id, operation_ref, capability)`.

`DispatchOperation`, `RecordReceipt` e `ReleaseReservation` continuam `system`, com as provas e o lock order da v1.7. Nesta v0.3 o primeiro lock desses comandos, quando a task é conversacional, também é o Build pai. Não se lê headroom antes desse lock.

## 6. Allowlist

| Capability | Família | side_effects | Reserva |
|---|---|---|---|
| speech.transcribe | TOOL | EXTERNAL | uma por invocation |
| speech.synthesize | TOOL | EXTERNAL | uma por invocation |
| conversation.respond | MODEL | EXTERNAL | uma por turno de agente |
| conversation.show_evidence | TOOL | NONE | sem reserva se o descriptor diz NONE e o estimate é 0 |
| conversation.invite | interno | NONE | sem operation monetária |
| conversation.issue_minutes | interno | INTERNAL | sem provider e sem prova fictícia |

`media_plane` `LOCAL_PIPELINE` ou `PROVIDER_DUPLEX` não é família nova e não funde operations.

## 7. Oráculos desta seção

CMP-FD-O15, O16, O17, O18, O30, O31, O35, O36, O37, O38 e O40 em CMP-FD-07. Todos NOT RUN.

O35 é o par concorrente de estimates distintos sobre o último saldo. O36 é o par de sessões que tentam somar fatias acima do teto. O37 é o UUID válido de outro tenant. O40 é o teto autodeclarado rejeitado.
