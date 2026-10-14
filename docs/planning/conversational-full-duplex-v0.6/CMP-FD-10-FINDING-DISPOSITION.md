# CMP-FD-10 v0.6 — Disposição

**Estado:** CANDIDATE FOR CODEX REVIEW, salvo LOW-01. O autor não escreve PASS e não fecha finding.

## HIGH-03

- Causa: na v0.5, `ack_of_sequence = 0` com peer high-water 0 não caía em duplicata nem em aceite. A subida do high-water também não tinha lock nem predicado que impedisse diminuição.
- Texto: CMP-FD-02:23-31 define `422 ACK_SEQUENCE_ZERO`, efeito zero, sem criar linha. A ordem fechada está em CMP-FD-02:35-50; a linha 44 é `n = 0` antes de qualquer comparação. A escrita está em CMP-FD-02:54-88: `SELECT FOR UPDATE` e `UPDATE` só com `n > peer_ack_high_water`. A corrida está nas linhas 99-102: as duas ordens terminam em 2, e final 1 depois de um 2 cometido é ilegal. O stream reconhecido não sai do `stream_id` do evento, linha 7. Sem half-duplex, mesma linha.
- Negativo: O71..O78, CMP-FD-07 linhas 15, 25, 33, 39, 45, 51, 57 e 63. Fixture `fixtures/CMP-FD-FX-03-ack.json`. NOT RUN como protocolo.
- Status: CANDIDATE. O contrato de mídia não está aprovado.

## NEW-MEDIUM-06

- Causa: o unique parcial da v0.5 permite várias linhas com `session_id` null. FDP-16A v1.7 seção 3.2 não torna essa coluna `NOT NULL`. A opção A não tem constraint para citar.
- Texto: opção B em CMP-FD-13:5. Contagem em CMP-FD-13:18-28, código `NULL_ACTIVE_SESSION`, rollback da migration inteira, sem UUID inventado e sem apagar task. Check em CMP-FD-13:32-46. Índice só depois, linha 60. `task.status` fora do predicado, linha 16. `409 ANCHOR_EXISTS` na linha 72 e `404` opaco na linha 74.
- Negativo: O79 e O80, CMP-FD-07 linhas 71 e 81. NOT RUN.
- Status: CANDIDATE.

## LOW-01

- Texto: CMP-FD-07:9-11. Pessoa PENDING. Effort UNSTATED. DoR NOT MET.
- Status: OPEN BLOCKING DoR. Não é CANDIDATE de fechamento.

## Não redispostos

NEW-HIGH-04, NEW-HIGH-03, NEW-MEDIUM-05 e NEW-MEDIUM-03 continuam CANDIDATE na v0.5. NEW-MEDIUM-01 continua CLOSED pelo Codex. HIGH-01, HIGH-02, NEW-HIGH-01, NEW-HIGH-02, NEW-MEDIUM-02, NEW-MEDIUM-04 e MEDIUM-01..05 permanecem fechados pelo Codex. Esta página não os reabre e não os confirma de novo.
