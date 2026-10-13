# Fechamento dos findings — Codex Round 6 para baseline v1.4
Estado da entrega: ROUND 7 — CANDIDATE FOR CODEX REVIEW.
Este registro não é o parecer do Codex. Não declara PASS. Nenhum teste de produto foi executado. Nenhuma aprovação foi inferida.
Os cinco HIGH e os cinco MEDIUM que o Codex marcou como fechados no Round 6 não foram reabertos.

| Campo | HIGH-01 |
|---|---|
| ID | HIGH-01 — concorrência de settlement e release |
| Situação no parecer | PARCIALMENTE ABERTO. A v1.3 serializava a reserva, mas não duas liquidações, nem receipt contra release, nem duas liberações, nem o retry depois do commit. |
| Causa-raiz | A frase "at most one settlement" não dizia qual writer vencia nem o que o perdedor devolvia. LEDGER-01 era sequencial. LEDGER-06 só cobria reserva. |
| Correção | FDP-16A v1.4 seção 8A.1. Uma transação, lock `FOR UPDATE` na ordem Build, Operation, Reservation, autorização por último. Depois do lock, a releitura decide: se já existe `forge.operation_money_movement` para aquele `operation_id`, o perdedor recebe 409 ALREADY_SETTLED ou 409 ALREADY_RELEASED e não grava dinheiro nem outbox. A unicidade de `operation_id` e de `command_id` faz o rollback junto com o contador. Retry do mesmo `command_id` é 200 IDEMPOTENT_REPLAY. Retry com outro `command_id` não redispacha. Custo real acima do limite não insere movement e não aumenta `spent`. |
| Arquivo | docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md |
| Evidência | Lock order na linha 357. Tabela das quatro corridas nas linhas 388–391. Constraint na linha 376. Oráculos LEDGER-07 a LEDGER-10 na matriz v1.4, linhas 68–71. F-015 cita esses ids na linha 651. |
| Prova pedida | Dois receipts: um SETTLED, `spent` aumenta uma vez, perdedor 409 ALREADY_SETTLED. Receipt contra release: um único tipo de movement. Duas releases: `reserved` cai uma vez. Retry tardio: o mesmo command_id não move dinheiro de novo e um command_id novo não chama o provider. |
| Estado neste builder | CORRIGIDO NESTA CANDIDATA. Não é fechamento do Codex. |

| Campo | NEW-HIGH-07 |
|---|---|
| ID | NEW-HIGH-07 — ator, comando e evidência da reconciliação manual |
| Situação no parecer | ABERTO. O catálogo dava RecordReceipt e ReleaseReservation só a `system`, sem `evidence_ref`. A máquina da v1.3 mandava um humano executar esses mesmos comandos em BLOCKED_RECONCILIATION. |
| Causa-raiz | Havia duas autoridades para o mesmo efeito. Não dava para implementar as duas sem escolher uma. |
| Correção | Uma autoridade só, seção 8A.2. RecordReceipt e ReleaseReservation continuam sendo comandos de `system` e são recusados em BLOCKED_RECONCILIATION com 409 HUMAN_RECONCILIATION_REQUIRED. O humano `security_operator` só envia ApproveManualReconciliation, com `evidence_ref` de uma evidência já gravada, decisão PROVEN_RECEIPT ou PROVEN_NO_EFFECT, capability `ledger.reconcile` decidida pelo Policy Service e não pelo modelo. PROVEN_RECEIPT exige um segundo operador (ConfirmManualReconciliation); o mesmo ator recebe 403 SELF_CONFIRM. Nenhum desses comandos move dinheiro. Quem move é ApplyAuthorizedReconciliation, comando seguinte do `system`, que consome a autorização na mesma transação do movement e não chama o provider. `coding_engine` recebe 403. Evidência ausente, sem digest ou escrita pelo coding engine não autoriza. Decisão ambígua é 422 e não cria autorização. |
| Arquivo | docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md; FDP-19A v1.4 F-015; matriz v1.4 |
| Evidência | Catálogo nas linhas 203–208. Seção 8A.2 na linha 401. Transições nas linhas 342–347. API nas linhas 434–438. LEDGER-11 linha 72 da matriz. LEDGER-12 linha 73. |
| Prova pedida | Um humano não liquida por RecordReceipt. Sem evidência o estado e o dinheiro ficam parados. No-effect autorizado libera uma vez, sem aumentar `spent`. Receipt provado não aumenta `spent` até o segundo operador e o apply do system. O coding engine não passa. |
| Estado neste builder | CORRIGIDO NESTA CANDIDATA. Não é fechamento do Codex. |

## O que permanece fechado e não foi reescrito
HIGH-02 a HIGH-06 e M01 a M05, como o parecer Round 6 os deixou. Tuple de deploy, superfície de adapter, AIOX preferencial, HANDOFF-01, identidade, matrizes de Task, Attempt e Build, conjunto de READY_FOR_HUMAN_TEST e DoR operacional continuam. FDP-18, FDP-18A e FDP-20 permanecem v1.3, sem edição de regra.
