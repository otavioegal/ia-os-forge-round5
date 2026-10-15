# CMP-FD-02 v0.8 — Isolamento, negativos e replay do ACK

**Estado:** PROPOSTA. CANDIDATE FOR CODEX REVIEW. Não é PASS. Não aprova `cmp.media.duplex.v1`.
**Não edita** v0.1–v0.7, a baseline FDP-16A v1.7, CMP v0.3, ata, ADR nem parecer.
**HIGH-03** permanece PARTIAL. Esta página não o fecha. Os oráculos continuam NOT RUN.
**Achados que o Codex fechou na v0.7** (FD07-01 a FD07-04) não são reabertos. O par null e as duas direções de `ACK_SCOPE_MISMATCH` continuam antes de stream não alocado.

Não há downgrade para half-duplex. O `stream_id` do evento não entra na decisão nem no digest. Ack não liquida, não abre microfone e não cria ledger novo.

## 1. Chave

O high-water é um inteiro por chave, dentro do tenant do canal:

`(organization_id, project_id, session_id, ack_stream_id, receiver_participant_id)`

O scope lógico da v0.6 permanece. A unique física da v0.6 permanece. Outro tenant não é travado e não é atualizado. Outra sessão, outro stream alocado ou outro receiver participante é outra chave. Aceite sobe só a chave alvo. Nenhuma outra chave muda.

A fixture traz no mínimo dois streams alocados e dois receivers, mais uma segunda sessão e uma chave de outro `organization_id`. O checker guarda o mapa e falha com `FAIL_FOREIGN_KEY` se uma chave não alvo mudar. Isso é modelo estático. Não é lock e não é o teste PostgreSQL.

## 2. Ordem, primeiro casamento

`n` é `ack_of_sequence`. `S` é `ack_stream_id`. Não há linha seguinte se uma linha casou.

| # | Condição | Resultado | Escrita |
|---|---|---|---|
| 1 | exatamente um dos dois campos é null | `422 ACK_SCOPE_MISMATCH` | nenhuma |
| 2 | os dois são null | `NO_ACK`. Não é 422. Não é stream não alocado | nenhuma |
| 3 | org ou projeto do comando não é o do canal | `404 NOT_FOUND`, corpo opaco | nenhuma. Sem lock na linha estrangeira |
| 4 | receiver não é participante desta sessão neste tenant | `404 NOT_FOUND`, corpo opaco. Não cria linha | nenhuma |
| 5 | `S` não é stream alocado desta sessão | `422 ACK_STREAM_UNALLOCATED`, corpo opaco | nenhuma |
| 6 | `n = 0` | `422 ACK_SEQUENCE_ZERO` | nenhuma |
| 7 | `n < 0` | `422 ACK_REGRESSION`, estágio `negative`, antes da comparação com o peer | nenhuma |
| 8 | mesmo `command_id` e mesmo digest | transporte `200`, `replay=true`, `IDEMPOTENT_REPLAY` | nenhuma nova |
| 9 | mesmo `command_id` e digest diferente | `409 IDEMPOTENCY_KEY_REUSED` | nenhuma |
| 10 | mesmo `event_id` já aplicado | `EVENT_DEDUPE` | nenhuma nova |
| 11 | `n > emitted_high_water` | `422 ACK_FUTURE` | nenhuma |
| 12 | `n < peer_ack_high_water` | `422 ACK_REGRESSION`, estágio `regression` | nenhuma |
| 13 | `n = peer_ack_high_water` | `ACK_DUPLICATE` | nenhuma |
| 14 | `peer < n <= emitted` | `ACK_ACCEPT` | uma, só essa chave, só para cima |

O corpo opaco de 3, 4 e 5 é `{"error_code":"NOT_FOUND","retryable":false,"terminal":true}` no 404, e o 422 de stream não alocado não revela linha de outro tenant. `opaque=false` quando o código específico é a resposta.

`n < 0` não espera o passo 12. Com peer já em 2, o estágio tem de ser `negative`. Se o ramo sumir, o mesmo inteiro cairia em `regression` e a fixture falha com `FAIL_STAGE`.

## 3. Efeito dos negativos

Toda linha negativa declara e o checker lê, sem exceção: `zero_effect`, `zero_new_effect`, `zero_money`, `opens_mic`, `opaque`, `writes_high_water`, código, estágio, high-water antes/depois e o delta dos contadores.

`zero_effect` é verdadeiro quando não há escrita e o high-water da chave observada não muda. `zero_new_effect` é verdadeiro quando esse high-water não muda e todos os contadores abaixo ficam em delta zero. `zero_money` é verdadeiro e `opens_mic` é falso em toda linha desta fixture, inclusive no aceite. O aceite não é linha negativa: `zero_effect` e `zero_new_effect` são falsos nele, porque a chave sobe.

Contadores observáveis, todos sobre registros já existentes. Nenhum ledger novo:

| Contador | O que conta | No ACK |
|---|---|---|
| `money_movements` | movimento de dinheiro | sempre 0 |
| `mic_opens` | abertura de microfone | sempre 0 |
| `financial_audits` | audit `budget.settled` ou equivalente | sempre 0 |
| `transport_effects` | efeito de domínio do aceite | +1 só no `ACK_ACCEPT` |
| `outbox_appends` | outbox do `event_id` | +1 só no `ACK_ACCEPT`, na mesma transação |
| `command_commit_rows` | linha de `forge.command_commit` | +1 só no `ACK_ACCEPT` |

Virar qualquer campo declarado de uma linha negativa tem de fazer o checker sair com erro específico e não zero: `FAIL_ZERO_EFFECT`, `FAIL_ZERO_NEW_EFFECT`, `FAIL_MONEY`, `FAIL_OPENS_MIC`, `FAIL_OPAQUE`, `FAIL_WRITE`, `FAIL_CODE`, `FAIL_AFTER` ou `FAIL_COUNTER`. Isso é autochecagem do arquivo. Não é oráculo.

`FX03-NEGATIVE-SEQUENCE` é `n=-1`, stream alocado, peer 2, código `ACK_REGRESSION`, escrita zero, high-water 2, dinheiro zero, microfone fechado.

## 4. Identidade durável

Não há tabela nova. O comando usa `forge.command_commit`, unique `(organization_id, project_id, command_id)`, como na v0.5 seção 7. O digest é SHA-256 do JSON canônico, chaves ordenadas, separadores `( ",", ":" )`, UTF-8, sem o `stream_id` do evento. O evento de outbox usa `event_id` de `forge.event.v1`, dedupe do consumidor, baseline seção 4.2 e seção 10.

Na mesma transação do `ACK_ACCEPT`: sobe a chave, insere `command_commit`, insere um outbox. Sem audit financeiro. Crash antes do commit, inclusive `40001`: nenhuma das três fica. O retry do mesmo `command_id` não é replay e pode aceitar uma vez. O modelo `FX03-ROLLBACK-BEFORE-COMMIT` só ilustra essa frase. O oráculo correspondente é NOT RUN. Não houve banco.

Replay do mesmo `command_id` e mesmo digest: transporte 200, `replay=true`, outcome original, high-water estável, delta zero, sem segundo outbox e sem segundo efeito de transporte. Digest diferente: `409 IDEMPOTENCY_KEY_REUSED`, sem escrita. Outro `command_id` com `n` já igual ao peer: `ACK_DUPLICATE`, delta zero. O mesmo `event_id` já aplicado, com outro `command_id` que de outro modo aceitaria: `EVENT_DEDUPE`, high-water estável.

## 5. O que esta página não é

O replay sequencial `FX03-RACE-*` não é concorrência, não toma `SELECT FOR UPDATE` e não prova o predicado SQL. A corrida PostgreSQL está em CMP-FD-13 e permanece NOT RUN. `forge.conversation.delta.v4` permanece desligada. A v3 não é integrada. LOW-01 não é tocado.
