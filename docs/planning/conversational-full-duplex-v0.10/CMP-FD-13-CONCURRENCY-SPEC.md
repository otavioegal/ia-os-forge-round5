# CMP-FD-13 v0.10 — Concorrência ainda não executada

**Nenhuma migration foi executada.** Nenhum PostgreSQL foi aberto. Não é PASS. A corrida sequencial da fixture não é O92.

FD07-07 permanece OPEN. HIGH-03 permanece PARTIAL.

A unique continua `(organization_id, project_id, session_id, ack_stream_id, receiver_participant_id)`. A SQL futura continua `INSERT ... ON CONFLICT (...) DO NOTHING`, depois `SELECT ... FOR UPDATE`, depois o único `UPDATE` guardado por `:n > peer_ack_high_water`.

O92 e O93, se um dia autorizados, exigem dois backends, barreira real, as duas ordens, duplicata, rollback `40001` sem linha parcial, e trios distintos observados por `pg_locks` ou timeout. A evidência fica fora desta pasta. Até lá, NOT RUN.

`FX03-RACE-1-THEN-2` e `FX03-RACE-2-THEN-1` continuam `concurrency=false`. NEW-MEDIUM-06 permanece CLOSED documentalmente. A migration da opção B continua NOT RUN. A flag `forge.conversation.delta.v4` permanece desligada.
