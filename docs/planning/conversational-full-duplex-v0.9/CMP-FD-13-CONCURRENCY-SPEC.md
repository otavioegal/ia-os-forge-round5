# CMP-FD-13 v0.9 — Protocolo futuro de concorrência

**Nenhuma migration foi executada.** Nenhum PostgreSQL foi aberto. Não é PASS. Não é o replay sequencial da fixture. FD07-07 permanece OPEN. HIGH-03 permanece PARTIAL.

A SQL continua a da v0.6 e a grafia da v0.8. Esta página não cria tabela e não liga `forge.conversation.delta.v4`.

## 1. Sentenças, ainda não executadas

Unique física `(organization_id, project_id, session_id, ack_stream_id, receiver_participant_id)`.

`INSERT ... ON CONFLICT (...) DO NOTHING`, depois `SELECT ... FOR UPDATE`, depois o único `UPDATE` guardado por `:n > peer_ack_high_water` e por `peer_ack_high_water = :current`. `n = 0` e `n < 0` não chegam aqui. Zero linhas no `UPDATE`: reler. Menor é `ACK_REGRESSION`. Igual é `ACK_DUPLICATE`. `40001` aborta o perdedor sem `command_commit`, sem outbox e sem high-water parcial.

## 2. O92 e O93, NOT RUN

Execução só com autorização expressa do Founder. Até lá, NOT RUN. O protocolo futuro, se um dia autorizado, precisa de tudo isto, gravado fora desta pasta:

| Evidência | Exigência |
|---|---|
| Dois backends | duas sessões PostgreSQL, não duas chamadas no mesmo processo |
| Barreira | os dois esperam antes do commit. Não é lista em memória |
| Ordem 1 depois 2 | final 2. Os dois são `ACK_ACCEPT` |
| Ordem 2 depois 1 | final 2. O perdedor relê e devolve `ACK_REGRESSION`. Nunca 2 e depois 1 |
| Mesmo `n` já cometido | perdedor `ACK_DUPLICATE`. Valor intacto |
| Rollback | `40001` não deixa linha de `command_commit` nem outbox |
| O93 | outro trio, por exemplo output do outro receiver. `pg_locks` ou timeout mostra que não esperam a mesma linha |

`FX03-RACE-1-THEN-2` e `FX03-RACE-2-THEN-1` continuam `concurrency=false`. Não substituem esta tabela.

## 3. O que não entra

Não há `CREATE`, `ALTER` nem `psql` nesta pasta. NEW-MEDIUM-06 continua CLOSED documentalmente pelo parecer da v0.7. A migration da opção B continua NOT RUN.
