# CMP-FD-01 v0.4 — Settlement, tenant e CAS

**Estado:** PROPOSTA. CANDIDATE FOR CODEX REVIEW. Não é PASS. O autor não fecha finding.
**Schema proposto:** `forge.conversation.delta.v3`. Não edita FDP-16A v1.7. Não liga flag. Não integra `forge.conversation.delta.v2`.
**Achados alvo:** NEW-HIGH-04, NEW-HIGH-03, NEW-MEDIUM-01, NEW-MEDIUM-06. HIGH-01, NEW-HIGH-01 e NEW-HIGH-02 permanecem como o Codex os fechou; as regras abaixo os repetem para não regressar.

## 1. Invariantes que não se reabrem

- `conversation_router` não é `coding_engine` e não chama `InvokeCapability`.
- O primeiro lock monetário é o Build pai `CONVERSATIONAL_BUDGET_ROOT` da org e do projeto do canal. Só depois se lê `budget_spent_minor`, `budget_reserved_minor`, `budget_limit_minor`, `stop_latch` ou reconciliação.
- Ordem depois desse lock: Task, Operation, Reservation, ManualReconciliation. Nunca invertida.
- Um root por `(organization_id, project_id)`. `OpenConversationalAnchor` rejeita `budget_limit_minor` com `422 UNKNOWN_FIELD`.
- Fatias abertas somam no máximo o teto. O comando de abertura não cria teto.
- Prova só por `forge.provider_ingest`. Sem prova conclusiva, HELD. Sem recibo fictício.
- `Task.build_id` e `Operation.task_id` continuam NOT NULL. A task de sessão fica fora do DAG.
- Não há segundo ledger nem moeda nova.

## 2. NEW-HIGH-04 — a fatia também limita o settlement

A reserva continua comparando só o estimate. Isso não basta. FDP-16A v1.7 permite `actual > estimate` quando o teto do Build ainda comporta. Numa task conversacional esse caminho tem de passar também pela fatia.

Símbolos, lidos só depois do lock do Build pai:

| Símbolo | Definição |
|---|---|
| S | soma de `settled_minor` das operations desta task já `SETTLED`. A operation corrente ainda não entra |
| H | soma de `estimated_minor` das reservations `HELD` desta task, **incluindo** a reservation corrente |
| E | `estimated_minor` da reservation corrente |
| A | `actual_minor` da prova `RECEIPT` conclusiva |
| L | `session_slice_minor` da task. Não é reescrito por este comando |
| R | `budget_spent_minor + budget_reserved_minor - E + A` do root |

Checagem de fatia, obrigatória: `S + H - E + A <= L`.
Checagem de root, a da v1.7: `R <= budget_limit_minor`.

`H` inclui E. Subtrair E e somar A troca o estimate pelo actual. Não subtrair E duas vezes.

### 2.1 RecordReceipt conversacional

Ator continua `system`. Roteador, adapter e modelo: `403 ACTOR_FORBIDDEN`.

1. Fase estática e fase de identidade, sem coluna monetária e sem lock de linha de outro tenant. Seção 3.
2. `SELECT` do Build pai do canal `FOR UPDATE`. Este é o primeiro lock.
3. `SELECT` da Task `FOR UPDATE`, já filtrada pela org e pelo projeto.
4. `SELECT` da Operation `FOR UPDATE` com predicado de tenant.
5. `SELECT` da Reservation `FOR UPDATE` com predicado de tenant.
6. ManualReconciliation por último, só se o comando a lê.
7. **Lookup de `command_id` antes de qualquer CAS.** Seção 4. Se o lookup decide replay ou `IDEMPOTENCY_KEY_REUSED`, parar. Não comparar versão.
8. Só então CAS de `expected_task_version` e `expected_build_version`.
9. Reler S, H, E, L, spent, reserved e o teto.
10. Se a prova não é conclusiva, ou há contradição de provas: valem as regras v1.7 de `409 PROOF_INCONCLUSIVE` ou `409 PROOF_CONFLICT`. Nenhum movimento. Nenhuma fatia alterada. Provas conservadas.
11. Se `R > budget_limit_minor`: caminho v1.7 de over-estimate. Operation `RECONCILING`, reservation `HELD`, um `pending_provider_cost` com razão `OVER_ESTIMATE`, `spent` e `reserved` inalterados. Não liquidar. Não elevar L.
12. Se o root comporta e `S + H - E + A > L`: **zero settlement**. Operation `RECONCILING`. Reservation `HELD`. `spent` e `reserved` inalterados. L inalterado. Um `pending_provider_cost` com razão aditiva `SESSION_SLICE`, valor A, único em `(operation_id, proof_id)`. Retorno `409 SESSION_SLICE_EXCEEDED`. Não é `200`.
13. Se as duas checagens passam: um movimento. `spent += A`, `reserved -= E`, operation `SETTLED`, reservation `SETTLED`. Audit `budget.settled` e outbox na mesma transação.
14. Proibido na mesma transação: chamar provider, inserir segunda reservation, apagar prova, inventar refund, aumentar L, criar segundo movimento.

Se root e fatia falham juntos, a razão do pending é `OVER_ESTIMATE`, uma linha só. A fatia também não é violada, porque não há movimento.

`ReleaseReservation` não muda. Continua exigindo `NO_EFFECT` conclusivo e nenhuma `RECEIPT`. Pending de `SESSION_SLICE` implica `409 PENDING_COST_HELD`. Não se libera para “caber na fatia”.

Retry do mesmo `command_id` depois do commit do passo 12 ou 13: replay, sem segunda linha pending e sem segundo movimento. `40001` aborta a transação inteira. O retry não chama provider.

### 2.2 Exemplo normativo, ainda não executado

Estado: L = 50, E = 40, S = 0, H = 40, spent = 0, reserved = 40, teto do root = 100.

| A | Root | Fatia | Efeito |
|---|---|---|---|
| 70 | `0+40-40+70 = 70 <= 100` | `0+40-40+70 = 70 > 50` | zero movimento; reserved continua 40; pending `SESSION_SLICE` de 70 |
| 45 | `45 <= 100` | `45 <= 50` | um settlement; spent = 45; reserved = 0 |

O primeiro caso é o defeito da v0.3. O segundo mostra que a fatia não bloqueia um actual que cabe.

### 2.3 Resolução autorizada e fecho

Ninguém eleva L dentro de `RecordReceipt`. O único comando que altera uma fatia já aberta é `AmendSessionSlice`:

- ator `human`, capability `budget.authorize_conversation`;
- não é o roteador;
- payload: `task_id`, `new_slice_minor`, `budget_authorization_ref`, `expected_build_version`, `command_id`;
- depois do lock do Build, `new_slice_minor >= S + H` e a soma das fatias abertas, já com o valor novo, `<= budget_limit_minor`;
- senão `409 SLICE_CEILING` e L antigo permanece;
- o comando não liquida e não chama provider.

Enquanto existir operation `DISPATCHED`, `RECONCILING` ou `BLOCKED_RECONCILIATION`, ou existir `pending_provider_cost` sem movimento terminal compatível, a task não vai a `SESSION_CLOSED`. Fica `ORPHAN_HELD` ou `CLOSING`. L permanece e continua na soma das fatias. Outra sessão não herda esse resto. Isso vale para prova tardia e para `SESSION_SLICE`.

Prova tardia depois de um movimento já cometido segue a v1.7: não há segundo movimento, `spent` e `reserved` não voltam, a fatia não é reescrita, as provas ficam.

## 3. NEW-HIGH-03 — cadeia até a Reservation

Toda leitura e todo lock usam org e projeto do canal autenticado. RLS não substitui o predicado. ID global não substitui o predicado.

| Elo | Predicado mínimo | FK composta proposta |
|---|---|---|
| canal | binding autenticado | — |
| sessão | `organization_id`, `project_id`, `session_id` do canal | task referencia o root no mesmo par |
| Build root | `id`, `organization_id`, `project_id`, kind root | uma linha por org e projeto |
| Task | `id`, `organization_id`, `project_id` | `(organization_id, project_id, build_id)` → build |
| Operation | `id`, `organization_id`, `project_id`, `task_id` | `(organization_id, project_id, task_id)` → task |
| Reservation | `operation_id`, `organization_id`, `project_id` | `(organization_id, project_id, operation_id)` → operation `(organization_id, project_id, id)` |

A Reservation ganha `organization_id` e `project_id` NOT NULL, copiados da Operation na transação que a insere. Não vêm de campo solto do cliente.

Consulta de Operation ou Reservation existente: `WHERE id = :id AND organization_id = :channel_org AND project_id = :channel_project`. Zero linhas: `404 NOT_FOUND` com corpo `{"error_code":"NOT_FOUND","retryable":false,"terminal":true}`. O mesmo corpo se o UUID não existe e se existe em outro tenant. Não se faz `SELECT FOR UPDATE` numa linha de outro tenant. Não se altera contador de lá. O audit fica na org do canal, sem colunas do recurso estrangeiro.

Ingest de prova: o `operation_id` tem de ser o que foi gravado no dispatch deste tenant. Um id de outro tenant no payload do provider não seleciona aquela linha e não insere prova nela.

Replay de `command_id` também é filtrado por org e projeto. Não revela commit de outro tenant.

O37, na v0.4, tem um subcaso por elo: sessão, Build, Task, Operation e Reservation. Todos NOT RUN.

## 4. NEW-MEDIUM-01 — replay antes do CAS

Registro durável `forge.command_commit`, escrito só no commit da transação que também escreve outbox e audit:

| Campo | Regra |
|---|---|
| command_id | uuid, único junto com org e projeto |
| organization_id, project_id | os do canal |
| command_digest | SHA-256 do JSON canônico abaixo |
| outcome_code | o código HTTP cometido, inclusive `409 SESSION_SLICE_EXCEEDED` quando esse 409 foi commit de reconciliação |
| outcome_digest | SHA-256 do corpo de resposta canônico |
| created_at | relógio do banco |

Digest do comando, UTF-8, chaves ordenadas, sem espaço, **incluindo** `expected_task_version` e `expected_build_version`, e excluindo qualquer campo desconhecido. O digest não inclui a version corrente do banco. Replay byte a byte conserva o digest mesmo depois que o banco andou.

Ordem, depois dos locks e da validação de escopo, sem exceção:

1. `SELECT` do `command_commit` desta org e deste projeto, `FOR UPDATE` se a linha existe.
2. Se existe e o digest é igual: `200 IDEMPOTENT_REPLAY` com o outcome guardado. **Não** executar o passo de CAS. Não escrever de novo.
3. Se existe e o digest difere: `409 IDEMPOTENCY_KEY_REUSED`. Não escrever.
4. Se não existe: comparar `expected_task_version` e `expected_build_version` com as linhas já lockadas. Divergência: `409 VERSION_CONFLICT`, rollback, **sem** inserir `command_commit`.
5. Se o CAS passa: seguir a decisão financeira e inserir o `command_commit` no mesmo commit.

Crash antes do commit: não há linha. Repetir o mesmo `command_id` não é replay; é nova tentativa. Se ninguém andou a version, pode comprometer uma vez. Se andou, `409 VERSION_CONFLICT`. Não há efeito duplo.

Dois `command_id` distintos continuam serializados pelo lock do Build. Não viram replay um do outro.

`command_commit` não se apaga em rollback de schema. É o mesmo tipo de retenção do audit.

O38 da v0.3 fica subordinado a esta ordem. Versão velha num comando **novo** continua `409 VERSION_CONFLICT`. Versão velha num `command_id` **já cometido** com o mesmo digest é replay.

## 5. NEW-MEDIUM-06 — sessão não é única no mundo

Índice único parcial: `(organization_id, project_id, session_id)` onde `session_status` está em `OPEN`, `CLOSING` ou `ORPHAN_HELD`.

Não existe índice único só em `session_id`.

Mesmo UUID de sessão em duas organizações: duas tasks, dois roots se os projetos diferem, nenhum erro, nenhuma resposta que cite a outra org.

Segunda abertura no mesmo org e projeto, com status ainda aberto: `409 ANCHOR_EXISTS`. Esse código só aparece depois que a linha foi encontrada **neste** tenant. Não serve para sondar outro tenant.

## 6. Oráculos

O35, O36 e O40 permanecem, NOT RUN. O37 é expandido. O41 e O42 cobrem a fatia no settlement. O43, O44 e O45 cobrem replay e CAS. O49 e O50 cobrem a unicidade composta. Nenhum foi executado.
