# CMP-FD-07 v0.7 — Notas de cobertura do par nulo

**Nenhum oráculo foi executado.** Evidence ABSENT. NOT RUN. Não é PASS.
**IDs novos:** CMP-FD-O81, CMP-FD-O82 e CMP-FD-O83. Não colidem com O01..O80 nem com CMP-O-01..36.
**CMP-O-28** não é CMP-FD-O28.

`tools/check_fd_fx03_ack.py` não executa estes oráculos. Confere só códigos e inteiros da fixture. `PASS_FIXTURE_ONLY` não é execução de oráculo e não é PASS do pacote.

## 1. LOW-01 — OPEN BLOCKING DoR

Sete histórias. Pessoa PENDING. Effort UNSTATED. DoR NOT MET. O autor não nomeia ninguém e não estima. Sem ato humano do Founder, o estado continua **OPEN BLOCKING DoR**.

## 2. Par nulo — todos NOT RUN

### CMP-FD-O81 — nenhum ACK

`ack_of_sequence` null e `ack_stream_id` null. Peer high-water 2. Emitted 2. O evento pode carregar `stream_id` de control. A decisão não lê esse id.

Critério, não executado: resultado `NO_ACK`, sem 422 e sem `ACK_STREAM_UNALLOCATED`. High-water permanece 2. Nenhuma linha nova. Zero dinheiro. Microfone fechado.

Falha se classificar como stream não alocado, escrever, abrir microfone ou mover dinheiro. NOT RUN.

### CMP-FD-O82 — scope, só a sequence

`ack_of_sequence = 1` e `ack_stream_id` null. O `stream_id` do evento é um stream alocado. Peer high-water 2.

Critério, não executado: `422 ACK_SCOPE_MISMATCH`. Sem herdar o `stream_id`. High-water permanece 2. Zero dinheiro. Microfone fechado.

Falha se aceitar, se devolver `ACK_STREAM_UNALLOCATED`, ou se escrever. NOT RUN.

### CMP-FD-O83 — scope, só o stream

`ack_of_sequence` null e `ack_stream_id` de um stream alocado. Peer high-water 2.

Critério, não executado: `422 ACK_SCOPE_MISMATCH`. Não é `ACK_SEQUENCE_ZERO` e não é `ACK_STREAM_UNALLOCATED`. High-water permanece 2. Zero dinheiro. Microfone fechado.

Falha se devolver zero, unallocated ou escrita. NOT RUN.

## 3. O que continua NOT RUN

O71..O80 continuam NOT RUN e não são fechados. O71 continua sequence zero. O72 continua a corrida monotônica. O78 continua o par inválido. A fixture agora nomeia as duas direções; isso não executa O78.

O01..O70, os 91 oráculos v1.7 e os 36 CMP-O não foram executados. O28 continua AEC. O58 continua o apply que não cabe na fatia. Esta página não os marca como rodados.

HIGH-03 permanece CANDIDATE. NEW-MEDIUM-06 permanece CANDIDATE. O79 e O80 permanecem NOT RUN.
