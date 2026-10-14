# CMP-FD-01 v0.5 — Settlement em todo comando que liquida

**Estado:** PROPOSTA. CANDIDATE FOR CODEX REVIEW. Não é PASS. O autor não fecha finding.
**Schema proposto:** `forge.conversation.delta.v4`, nasce desligada. Não integra `forge.conversation.delta.v3`. Não edita FDP-16A v1.7.
**Achado alvo:** NEW-HIGH-04 ainda PARTIAL na v0.4. NEW-MEDIUM-01 permanece CLOSED; a seção 7 só separa o transporte do outcome original.
**Pacote histórico:** a v0.4 não é editada. Onde esta página repete uma regra, é para o pacote não depender do arquivo antigo.

## 1. Invariantes que não se reabrem

- `conversation_router` não é `coding_engine` e não chama `InvokeCapability`. Não chama `ApplyAuthorizedReconciliation`.
- O primeiro lock monetário é o Build pai `CONVERSATIONAL_BUDGET_ROOT` da org e do projeto do canal. Só depois se lê `budget_spent_minor`, `budget_reserved_minor`, `budget_limit_minor`, `stop_latch` ou reconciliação.
- Ordem depois desse lock: Task, Operation, Reservation, ManualReconciliation. Nunca invertida.
- Um root por `(organization_id, project_id)`. `OpenConversationalAnchor` rejeita `budget_limit_minor` com `422 UNKNOWN_FIELD`.
- A soma das fatias com `session_status` em `OPEN`, `CLOSING` ou `ORPHAN_HELD` não passa do teto do root. O comando de abertura não cria teto.
- Prova só por `forge.provider_ingest`. Sem prova conclusiva, não há movimento.
- Não há segundo ledger, segunda moeda, refund inventado nem segundo movimento.
- `expected_task_version` e `expected_build_version` são int64 obrigatórios nos comandos monetários desta página. Ausência não é null aceito: `422 VALIDATION`.

## 2. Fórmula, só depois do lock

Símbolos, lidos só com o Build pai já em `FOR UPDATE`:

| Símbolo | Definição |
|---|---|
| S | soma de `settled_minor` das operations desta task já `SETTLED`. A operation corrente não entra |
| H | soma de `estimated_minor` das reservations `HELD` desta task, **incluindo** a reservation corrente |
| E | `estimated_minor` da reservation corrente |
| A | `actual_minor` da prova `RECEIPT` conclusiva que este comando quer liquidar |
| L | `session_slice_minor` da task. Este comando não reescreve L |
| R | `budget_spent_minor + budget_reserved_minor - E + A` do root |

Checagem de fatia: `S + H - E + A <= L`.
Checagem de root, a da v1.7: `R <= budget_limit_minor`.

`H` inclui E. Subtrair E uma vez e somar A troca o estimate pelo actual. Não subtrair E duas vezes.

`held_task_restante` do prompt v0.4 é este H, não o held excluindo a reservation corrente. Excluir E de H faria `S + 0 - E + A` caber 70 numa fatia 50. Isso é o defeito, não a conta.

## 3. Quem pode inserir SETTLEMENT

Nesta task conversacional, os únicos comandos que podem inserir movimento `SETTLEMENT` são:

1. `RecordReceipt`, ator `system`, status `DISPATCHED` ou `RECONCILING`;
2. `ApplyAuthorizedReconciliation` com decisão `PROVEN_RECEIPT`, ator `system`, status `BLOCKED_RECONCILIATION`, autorização `AUTHORIZED` e não consumida.

Qualquer outro comando que inseriria `SETTLEMENT` é negado. Não há terceira via.

`ApproveManualReconciliation` e `ConfirmManualReconciliation` não liquidam. Não consomem a autorização até o apply. Não são o portão da fatia. O portão é obrigatório no comando que insere o movimento, antes do insert.

`ApplyAuthorizedReconciliation` com `PROVEN_NO_EFFECT` insere `RELEASE`, não `SETTLEMENT`. Não usa a fórmula para gastar. Se existir `RECEIPT` conclusivo ou qualquer `pending_provider_cost`, o resultado é `409 PENDING_COST_HELD` ou `409 PROOF_CONFLICT`, autorização não consumida, zero movimento. Não se libera para caber na fatia.

## 4. Ordem comum, inclusive no apply

1. Fase estática e identidade no tenant do canal. Sem coluna monetária. Sem `SELECT FOR UPDATE` de outro tenant.
2. `SELECT` do Build pai `FOR UPDATE`. Primeiro lock.
3. Task `FOR UPDATE`, predicado de tenant.
4. Operation `FOR UPDATE`, predicado de tenant.
5. Reservation `FOR UPDATE`, predicado de tenant.
6. ManualReconciliation por último, só se o comando a lê, predicado de tenant.
7. Lookup de `command_commit` por `(organization_id, project_id, command_id)` **antes** do CAS. Seção 7.
8. CAS de `expected_task_version` e `expected_build_version`.
9. Reler S, H, E, L, spent, reserved, teto e, no apply, o status da autorização.
10. Só então a decisão financeira.

Lookup de `command_id` de outro tenant não seleciona a linha de lá e não a trava.

## 5. RecordReceipt — regra já escrita, repetida para não regredir

Ator que não é `system`: `403 ACTOR_FORBIDDEN`. A partir de `BLOCKED_RECONCILIATION`: `409 HUMAN_RECONCILIATION_REQUIRED`, zero movimento.

Prova não conclusiva ou contraditória: regras v1.7, zero movimento, L intacto.

Se `R > budget_limit_minor`: caminho v1.7. Operation `RECONCILING`, reservation `HELD`, um `pending_provider_cost` razão `OVER_ESTIMATE` se ainda não existir a linha `(operation_id, proof_id)`. Não liquidar. Não elevar L.

Se o root comporta e a fatia não: zero settlement. Operation `RECONCILING`. Reservation `HELD`. L intacto. Um pending razão `SESSION_SLICE`, valor A, único em `(operation_id, proof_id)`. Retorno `409 SESSION_SLICE_EXCEEDED`. Não é transporte de sucesso de liquidação.

Se as duas passam: um movimento. `spent += A`, `reserved -= E`, operation `SETTLED`, reservation `SETTLED`.

Se root e fatia falham juntos: uma linha só, razão `OVER_ESTIMATE`. Sem movimento.

Exemplo ainda não executado. L=50, E=40, S=0, H=40, spent=0, reserved=40, teto=100.

| A | Root | Fatia | Efeito |
|---|---|---|---|
| 70 | 70 <= 100 | 70 > 50 | zero movimento; pending `SESSION_SLICE` de 70 |
| 45 | 45 <= 100 | 45 <= 50 | um settlement; spent=45; reserved=0 |

## 6. ApplyAuthorizedReconciliation PROVEN_RECEIPT

Este é o bypass da v0.4. A baseline, FDP-16A v1.7 por volta de `:344-350`, liquida no apply quando o actual cabe no teto do Build. O delta conversacional acrescenta a fatia sem editar essa fonte.

Pré-condições da v1.7 continuam: autorização `AUTHORIZED` e não consumida, `expires_at` não passou, prova ainda conclusiva e não `CONFLICT`, operation `BLOCKED_RECONCILIATION`, grants rechecados. Falha dessas pré-condições não consome autorização e não move dinheiro.

Com as pré-condições satisfeitas, ainda sob o lock do passo 2:

1. Se `R > budget_limit_minor`: zero movimento. Operation permanece `BLOCKED_RECONCILIATION`. Reservation `HELD`. Autorização permanece `AUTHORIZED` e não consumida. Não vai a `APPLIED`. Um pending razão `OVER_ESTIMATE` se a chave `(operation_id, proof_id)` ainda não existe. Se já existe, não se insere outra linha e não se altera a razão. Retorno `409 OVER_ESTIMATE_BLOCKED`.
2. Se o root comporta e `S + H - E + A > L`: **zero settlement**. Operation permanece `BLOCKED_RECONCILIATION`. Reservation `HELD`. `spent` e `reserved` inalterados. L inalterado. Autorização permanece `AUTHORIZED` e não consumida. Um pending razão `SESSION_SLICE`, valor A, só se essa chave ainda não existe. Retorno `409 SESSION_SLICE_EXCEEDED`.
3. Se as duas falham: tratar como o item 1. Uma linha, razão `OVER_ESTIMATE`, não duas.
4. Se as duas passam: um movimento `SETTLEMENT`. `spent += A`, `reserved -= E`, operation `SETTLED`, reservation `SETTLED`, autorização `APPLIED` na mesma transação. `movement.settles_proof_id` = `proof_id` da prova liquidada. Audit `budget.settled` e outbox no mesmo commit.

Proibido nesse commit: chamar provider, segunda reservation, apagar prova, apagar pending, dar refund, aumentar L, segundo movimento.

O caso normativo do parecer, ainda não executado: E=40, A=70, L=50, root com teto 100 e headroom. O item 2 se aplica. Não o item 4.

O caso em que o actual cabe: A=45, mesmo estado. O item 4 se aplica. Um settlement. L permanece 50.

## 7. Replay — transporte separado do outcome

NEW-MEDIUM-01 fica como o Codex fechou. Esta seção não reabre a ordem. O lookup do passo 7 continua antes do CAS.

`forge.command_commit` guarda:

| Campo | Regra |
|---|---|
| organization_id, project_id, command_id | unicidade |
| command_digest | SHA-256 do JSON canônico do comando, chaves ordenadas, incluindo `expected_task_version` e `expected_build_version` |
| original_outcome_code | o código de negócio cometido, que pode ser 409 |
| original_outcome_body | o corpo canônico cometido |
| outcome_digest | SHA-256 desse corpo |

Resposta de replay, quando a linha existe e o digest é igual:

| Campo | Valor |
|---|---|
| transport_status | 200 |
| replay | true |
| original_outcome_code | o código guardado, inclusive `409` |
| original_outcome_body | o corpo guardado |

`transport_status` não é `original_outcome_code`. Dizer só “outcome anterior” fica proibido neste pacote. Um replay de `409 SESSION_SLICE_EXCEEDED` volta em HTTP 200 com `replay=true` e `original_outcome_code=409`. Não reexecuta CAS. Não insere segundo pending nem segundo movimento.

Digest diferente na mesma chave: `409 IDEMPOTENCY_KEY_REUSED`. Sem escrita.

Chave ausente e version velha: `409 VERSION_CONFLICT`. Sem linha de `command_commit`.

Crash antes do commit, inclusive `40001`: não há linha. O retry do mesmo `command_id` não é replay. Se as versions não andaram, pode comprometer uma vez. Se andaram, `409 VERSION_CONFLICT`. Não há efeito duplo.

## 8. Pending append-only e correlação

`pending_provider_cost` continua append-only, como na v1.7. Razão aditiva `SESSION_SLICE` só para task conversacional. Unique `(operation_id, proof_id)`. Sem `UPDATE`. Sem `DELETE`.

Uma liquidação posterior não edita essa linha. A correlação é leitura:

- o movimento `SETTLEMENT` traz `settles_proof_id`;
- a projeção “historicamente resolvido” é verdadeira só quando existe exatamente um movimento `SETTLEMENT` daquela operation cujo `settles_proof_id` é o `proof_id` do pending;
- a linha de pending permanece, com a razão original;
- não há movimento negativo, não há refund, `spent` não volta.

Enquanto essa projeção for falsa, a operation não está terminal para o fecho da sessão. `ReleaseReservation` e apply `PROVEN_NO_EFFECT` que enxerguem o pending retornam `409 PENDING_COST_HELD`.

Se um pending `SESSION_SLICE` já existe e um apply posterior estoura o root, não se muda a razão para `OVER_ESTIMATE`. Não se insere segunda linha. Zero movimento. Autorização não consumida.

## 9. Amend, corrida, prova tardia, CLOSING

`AmendSessionSlice` é o único comando que altera L já aberta. Ator `human`, capability `budget.authorize_conversation`. Não é o roteador. Não liquida. Não consome autorização. Não chama provider.

Depois do lock do Build: `new_slice_minor >= S + H` e a soma das fatias abertas, já com o valor novo, `<= budget_limit_minor`. Senão `409 SLICE_CEILING` e L antigo permanece.

`AmendSessionSlice` e `ApplyAuthorizedReconciliation` serializam no mesmo Build `FOR UPDATE`. Nenhum dos dois lê S, H, L, spent ou reserved antes desse lock.

Dois desfechos legais, com L inicial 50, A=70, teto do root 100:

1. O amend commita primeiro, L passa a 80, a version do Build anda. O apply que entrou com a version antiga recebe `409 VERSION_CONFLICT`, zero movimento, autorização não consumida, sem pending novo. O retry com a version nova, ainda sob lock, relê L=80. `70 <= 80` e o root comporta. Um settlement. O pending antigo, se já existia, não é apagado.
2. O apply commita primeiro com L=50. Caminho da seção 6 item 2: pending `SESSION_SLICE`, autorização não consumida, zero movimento. O amend posterior pode elevar L e não liquida. Um apply novo, outro `command_id`, depois do amend, é que pode liquidar uma vez.

Ilegais: os dois inserem settlement; o apply liquida 70 com L ainda 50; qualquer um usa headroom lido antes do lock.

`40001` aborta a transação inteira do perdedor, inclusive pending e `command_commit` que ainda não commitou. O retry não duplica.

Prova tardia depois de um movimento: regra v1.7. Não há segundo movimento. `spent` e `reserved` não voltam. L não é reescrito. A prova fica. Pending de conflito, se a prova nova for `RECEIPT` conclusivo contraditório, é insert append-only. Não se devolve a reservation a `HELD`. Não há refund.

Fecho: enquanto existir operation `DISPATCHED`, `RECONCILING` ou `BLOCKED_RECONCILIATION`, ou existir pending cuja projeção da seção 8 não esteja historicamente resolvida, `session_status` não vai a `CLOSED`. Permanece `CLOSING` ou `ORPHAN_HELD`. L continua na soma. Outra sessão não herda o resto. Isso vale com pending `SESSION_SLICE`. Fechar a sessão não liquida e não libera.

A coluna usada neste parágrafo é `session_status`. Não é `task.status`.

## 10. Tenant no comando

Toda leitura e todo lock usam org e projeto do canal. RLS não substitui o predicado. ID global não substitui o predicado.

Consulta de Operation ou Reservation: `WHERE id = :id AND organization_id = :channel_org AND project_id = :channel_project`. Zero linhas: `404` com corpo `{"error_code":"NOT_FOUND","retryable":false,"terminal":true}`. O mesmo corpo se o UUID não existe e se existe em outro tenant. Sem lock na linha estrangeira. Sem contador alterado lá. Sem vazar existência.

A migration que torna isso uma constraint, inclusive backfill e unique de Operation, está em CMP-FD-13. Esta página não a executa.
