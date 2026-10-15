# CMP-FD-07 v0.8 — Oráculos novos

**Nenhum oráculo foi executado.** Evidence ABSENT. NOT RUN. Não é PASS.
**IDs novos:** CMP-FD-O84 a CMP-FD-O95. Não colidem com O01..O83 nem com CMP-O-01..36.
**CMP-O-28** não é CMP-FD-O28.

O checker estático não executa estes oráculos. `PASS_FIXTURE_ONLY` não é execução de oráculo e não é PASS do pacote.

## 1. LOW-01 — OPEN BLOCKING DoR

Sete histórias. Pessoa PENDING. Effort UNSTATED. DoR NOT MET. O autor não nomeia ninguém e não estima. Sem ato humano do Founder, o estado continua **OPEN BLOCKING DoR**.

## 2. Novos critérios, todos NOT RUN

### CMP-FD-O84 — sequence negativa

`n=-1`, stream alocado, peer 2. Critério, não executado: `422 ACK_REGRESSION` no estágio anterior à comparação com o peer. High-water permanece 2. Dinheiro zero. Microfone fechado. NOT RUN.

### CMP-FD-O85 — efeitos de toda linha negativa

Critério, não executado: zero, futuro, regressão, duplicata, unallocated, mismatch, ambos null e sequence negativa não movem high-water, não movem dinheiro, não abrem microfone e declaram `opaque` só no 404 e no stream não alocado. NOT RUN.

### CMP-FD-O86 — isolamento do trio

Dois streams, dois receivers, operações intercaladas. Critério, não executado: só a chave `{session, ack_stream, receiver}` alvo muda, dentro do tenant. NOT RUN.

### CMP-FD-O87 — tenant errado

Critério, não executado: `404 NOT_FOUND` opaco, sem lock e sem escrita na linha do outro tenant. NOT RUN.

### CMP-FD-O88 — receiver ausente

Critério, não executado: `404 NOT_FOUND` opaco, sem criar linha. O outro receiver da sessão não muda. NOT RUN.

### CMP-FD-O89 — mesmo command_id

Critério, não executado: transporte 200, `replay=true`, high-water estável, sem segundo outbox, sem dinheiro, sem microfone. NOT RUN.

### CMP-FD-O90 — outro command_id, mesmo n

Critério, não executado: `ACK_DUPLICATE`, delta zero de transporte e de dinheiro. NOT RUN.

### CMP-FD-O91 — crash antes do commit

Critério, não executado: nenhuma linha de `command_commit`, nenhum outbox, high-water anterior. O retry não é replay. NOT RUN.

### CMP-FD-O92 — corrida PostgreSQL do mesmo trio

Critério, não executado: barreira real, as duas ordens, final 2, nunca 2 depois 1, perdedor `ACK_REGRESSION` ou `ACK_DUPLICATE`. NOT RUN.

### CMP-FD-O93 — trios distintos sem lock compartilhado

Critério, não executado: as duas transações não esperam a mesma linha. NOT RUN.

### CMP-FD-O94 — event_id repetido

Critério, não executado: segunda entrega não aplica o domínio de novo. NOT RUN.

### CMP-FD-O95 — command_id reusado com outro digest

Critério, não executado: `409 IDEMPOTENCY_KEY_REUSED`, sem escrita. NOT RUN.

## 3. O que continua NOT RUN

O71..O83 continuam NOT RUN. O72 continua a corrida que esta pasta não executou. O84..O95 também não foram executados. O checker estático não os promove.

O01..O70, os 91 oráculos v1.7 e os 36 CMP-O não foram executados. O28 continua AEC. O58 continua o apply que não cabe na fatia.

HIGH-03 permanece PARTIAL. NEW-MEDIUM-06 permanece fechado documentalmente pelo parecer da v0.7, com migration NOT RUN. O79 e O80 continuam NOT RUN.
