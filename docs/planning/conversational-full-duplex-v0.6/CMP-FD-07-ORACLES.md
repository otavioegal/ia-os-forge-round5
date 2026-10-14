# CMP-FD-07 v0.6 — Oráculos dos dois buracos

**Nenhum oráculo foi executado.** Evidence ABSENT. NOT RUN. Não é PASS.
**IDs novos:** CMP-FD-O71..O80. Não colidem com O01..O70 nem com CMP-O-01..36.
**CMP-O-28** não é CMP-FD-O28.

A fixture `fixtures/CMP-FD-FX-03-ack.json` e o script `tools/check_fd_fx03_ack.py` não executam estes oráculos. Eles só conferem números de arquivo.

## 1. LOW-01 — OPEN BLOCKING DoR

Sete histórias. Pessoa PENDING. Effort UNSTATED. DoR NOT MET. O autor não nomeia ninguém e não estima. Sem ato humano do Founder, o estado continua **OPEN BLOCKING DoR**.

## 2. ACK

### CMP-FD-O71 — sequence zero

`ack_of_sequence = 0`, peer high-water 0, emitted 2, stream alocado.

PASS: `422 ACK_SEQUENCE_ZERO`. High-water permanece 0. Nenhuma linha nova. Zero dinheiro. Microfone fechado.

O mesmo código com peer high-water já em 2: o valor permanece 2. Não é `ACK_REGRESSION` e não é `ACK_DUPLICATE`.

FAIL: aceite, ou escrita de 0, ou ausência de código. NOT RUN.

### CMP-FD-O72 — corrida monotônica

Mesmo receptor, mesmo `ack_stream_id`, emitted `>= 2`, current inicial 0. Dois commits, `n=1` e `n=2`.

PASS nas duas ordens: o valor final é 2. Na ordem 2 depois 1, o segundo resultado é `ACK_REGRESSION` e o valor não volta a 1. Nenhuma escrita diminui o inteiro.

FAIL: final 1 depois de um 2 já cometido. NOT RUN.

### CMP-FD-O73 — regressão

Peer high-water 2, `n=1`, emitted 2.

PASS: `422 ACK_REGRESSION`. Valor permanece 2. NOT RUN.

### CMP-FD-O74 — duplicata

Peer high-water 2, `n=2`.

PASS: `ACK_DUPLICATE`. Zero efeito novo. Valor permanece 2. NOT RUN.

### CMP-FD-O75 — futuro

Emitted 2, `n=9`.

PASS: `422 ACK_FUTURE`. High-water intacto. NOT RUN.

### CMP-FD-O76 — cross-stream

Evento `CONTROL`, `ack_stream_id` do input, `n=2`, emitted do input 2, peer 0.

PASS: `ACK_ACCEPT`. O peer high-water daquele trio fica 2. A sequence do control não é a sequence reconhecida. Zero dinheiro. Microfone não abre. NOT RUN.

### CMP-FD-O77 — stream não alocado

`ack_stream_id` fora dos três da sessão.

PASS: `422 ACK_STREAM_UNALLOCATED`, corpo opaco, mesmo se o UUID existir em outra sessão. Sem escrita. NOT RUN.

### CMP-FD-O78 — par inválido

`ack_of_sequence` preenchido e `ack_stream_id` null, ou o inverso.

PASS: `422 ACK_SCOPE_MISMATCH`. Sem escrita. Sem inferir o stream pelo `stream_id` do evento. NOT RUN.

## 3. session_id

### CMP-FD-O79 — null em sessão ativa

Uma task com `execution_domain = 'CONVERSATION'`, `session_status = 'OPEN'` e `session_id` null.

PASS da spec, não executada: a contagem é 1, a migration inteira faz `ROLLBACK`, nenhum UUID é inventado, nenhuma task é apagada, o índice não nasce, a flag segue desligada.

Quando a contagem histórica é zero e o check chegou a ser validado, um insert novo com esse formato é rejeitado e não commita.

FAIL: inventar `session_id`, apagar a task, ou criar o índice mesmo assim. NOT RUN.

### CMP-FD-O80 — fora do domínio

Task com `execution_domain` diferente de `CONVERSATION` e `session_id` null.

PASS: a contagem da seção 1 de CMP-FD-13 não a inclui, e o check não a rejeita. NOT RUN.

O49, O50 e O68 da v0.5 continuam NOT RUN. O 404 opaco e o `409 ANCHOR_EXISTS` só dentro do tenant não mudam.

## 4. O que continua NOT RUN

O01..O70, os 91 oráculos v1.7 e os 36 CMP-O não foram executados. O28 continua AEC. O58 continua o apply que não cabe na fatia. Esta página não os marca como rodados.
