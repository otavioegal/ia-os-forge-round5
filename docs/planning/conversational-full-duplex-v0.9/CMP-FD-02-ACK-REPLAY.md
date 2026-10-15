# CMP-FD-02 v0.9 — Replay com outcome original

**Estado:** PROPOSTA. CANDIDATE FOR CODEX REVIEW. Não é PASS. Não aprova `cmp.media.duplex.v1`.
**Não edita** v0.1–v0.8, a baseline, CMP v0.3, ata, ADR nem parecer.
**HIGH-03** permanece PARTIAL. FD07-07 permanece OPEN. O92 e O93 permanecem NOT RUN.
**FD07-05 e FD07-06** permanecem CLOSED documentalmente pelo parecer da v0.8. Esta página não os reabre.

Não há downgrade para half-duplex. O `stream_id` do evento não entra na decisão nem no digest. Ack não liquida, não abre microfone e não cria ledger novo.

## 1. Ordem

`n` é `ack_of_sequence`. `S` é `ack_stream_id`. O primeiro casamento encerra a decisão.

| # | Condição | Resultado | Escrita |
|---|---|---|---|
| 1 | exatamente um dos dois campos é null | `422 ACK_SCOPE_MISMATCH` | nenhuma |
| 2 | os dois são null | `NO_ACK` | nenhuma |
| 3 | org ou projeto não é o do canal | `404 NOT_FOUND` opaco | nenhuma. Sem ler `command_commit` de outro tenant |
| 4 | mesma chave `(org, project, command_id)` e mesmo `command_digest` | transporte `200`, `replay=true`, outcome original guardado | nenhuma nova |
| 5 | mesma chave e digest diferente | `409 IDEMPOTENCY_KEY_REUSED` | nenhuma. A linha guardada não é trocada |
| 6 | receiver não é mais participante | `404 NOT_FOUND` opaco | nenhuma |
| 7 | `S` não está alocado nesta sessão | `422 ACK_STREAM_UNALLOCATED` opaco | nenhuma |
| 8 | `n = 0` | `422 ACK_SEQUENCE_ZERO` | nenhuma |
| 9 | `n < 0` | `422 ACK_REGRESSION`, estágio `negative` | nenhuma |
| 10 | `event_id` já aplicado | `EVENT_DEDUPE` | nenhuma nova |
| 11 | `n > emitted` | `422 ACK_FUTURE` | só `command_commit` |
| 12 | `n < peer` | `422 ACK_REGRESSION`, estágio `regression` | só `command_commit` |
| 13 | `n = peer` | `422 ACK_DUPLICATE` | só `command_commit` |
| 14 | `peer < n <= emitted` | `200 ACK_ACCEPT` | a chave, `command_commit` e um outbox |

Os passos 4 e 5 ficam depois do tenant e antes das validações mutáveis de receiver, alocação e sequência. Tirar o receiver depois do commit não reescreve o outcome e não autoriza outro tenant. Um `command_id` novo, com o receiver já ausente, continua `404`.

`n < 0` continua antes da comparação com o peer. `FX03-NEGATIVE-SEQUENCE` segue com `n=-1`, high-water 2, dinheiro zero e microfone fechado. O harness também muta `peer_ack_high_water_before` e `expected_stage`.

## 2. command_commit

Não há tabela nova. A linha é a da v0.5, seção 7:

| Campo | Regra |
|---|---|
| organization_id, project_id, command_id | unicidade, só deste tenant |
| command_digest | SHA-256 do JSON canônico do comando, sem o `stream_id` do evento |
| original_outcome_code | o HTTP de negócio cometido. Pode ser 200 ou 422. Não é o transporte do replay |
| original_outcome_body | o corpo canônico cometido |
| outcome_digest | SHA-256 desse corpo |

O replay devolve `transport_status=200`, `replay=true`, `original_outcome_code` e `original_outcome_body` iguais aos guardados. `transport_status` não é `original_outcome_code`. Um original `422 ACK_FUTURE` volta em transporte 200 com esse 422. Não vira `IDEMPOTENT_REPLAY` dentro do corpo. Não cria segundo `event_id`, segundo outbox nem segundo movimento.

Digest diferente: `409 IDEMPOTENCY_KEY_REUSED`. A linha anterior permanece. Não há segundo evento.

Pre-lock (passos 1 a 3 e 6 a 9) não grava `command_commit`. Pós-lock (passos 11 a 14) grava. Só o aceite soma outbox e efeito de transporte. Dinheiro e microfone ficam em zero. Crash antes do commit, inclusive `40001`, não deixa linha. O modelo `FX03-ROLLBACK-BEFORE-COMMIT` não é banco. O91 permanece NOT RUN.

## 3. O que não é

O replay sequencial `FX03-RACE-*` não é PostgreSQL e não prova O92. A flag `forge.conversation.delta.v4` permanece desligada. A v3 não é integrada. O checker estático não prova produto.
