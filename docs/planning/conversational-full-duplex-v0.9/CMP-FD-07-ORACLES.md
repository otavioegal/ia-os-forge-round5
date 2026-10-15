# CMP-FD-07 v0.9 — Oráculos

**Nenhum oráculo foi executado.** NOT RUN. Não é PASS. `PASS_FIXTURE_ONLY` não é execução de oráculo e não é PASS do pacote. O checker estático não prova produto.

## 1. LOW-01 — OPEN BLOCKING DoR

Sete histórias. Pessoa PENDING. Effort UNSTATED. DoR NOT MET. O autor não nomeia responsável e não estima. Sem ato humano do Founder, o estado continua **OPEN BLOCKING DoR**.

## 2. Continuam NOT RUN

O84 a O95 continuam NOT RUN. O71 a O83 continuam NOT RUN. O92 e O93 continuam NOT RUN. O01 a O70, os 91 oráculos v1.7 e os 36 CMP-O não foram executados. CMP-O-28 não é CMP-FD-O28. O28 continua AEC. O58 continua o apply que não cabe na fatia.

## 3. Critérios novos, também NOT RUN

### CMP-FD-O96 — replay do 422

Critério, não executado no banco: um `ACK_FUTURE` cometido volta com transporte 200, `replay=true` e `original_outcome_code=422`. O corpo não é reescrito. Não há segundo `event_id`. NOT RUN.

### CMP-FD-O97 — digest diferente

Critério, não executado: `409 IDEMPOTENCY_KEY_REUSED` e a linha original permanece. NOT RUN.

### CMP-FD-O98 — receiver removido depois do commit

Critério, não executado: o replay devolve o 422 original. Um `command_id` novo para esse receiver é `404`. NOT RUN.

### CMP-FD-O99 — outro tenant

Critério, não executado: `404` opaco, sem o corpo do outro tenant e sem lock. NOT RUN.

O96 a O99 não foram executados. A checagem estática da fixture não os promove.

## 4. Estados que esta página não muda

HIGH-03 permanece PARTIAL. FD07-07 permanece OPEN. NEW-MEDIUM-06 permanece CLOSED documentalmente, migration NOT RUN. FD07-05 e FD07-06 permanecem CLOSED documentalmente pelo parecer da v0.8.
