# CMP-FD-10 v0.7 — Disposição

**Estado:** CANDIDATE FOR CODEX REVIEW, salvo LOW-01. O autor não escreve PASS e não fecha finding.

## Lacuna do checker v0.6 — par null

- Causa: em `docs/planning/conversational-full-duplex-v0.6/tools/check_fd_fx03_ack.py:34-35` o ou-exclusivo trata só um campo null. Os dois null não casam essas linhas. A linha 36, `ack_stream_id not in allocated`, casa `None`, e a linha 37 devolve `ACK_STREAM_UNALLOCATED`. A fixture v0.6, `docs/planning/conversational-full-duplex-v0.6/fixtures/CMP-FD-FX-03-ack.json:131-141`, só tem `FX03-PAIR-INVALID`: sequence 1 e `ack_stream_id` null. Não há linha com os dois null e não há linha com sequence null e stream alocado. A norma já estava em CMP-FD-02 v0.6:41-42 e não é a causa.
- Texto: CMP-FD-02:23 é `ACK_SCOPE_MISMATCH` quando exatamente um campo é null. CMP-FD-02:24 é `NO_ACK` quando os dois são null, sem 422 e sem stream não alocado. CMP-FD-02:25-32 mantêm a ordem seguinte: não alocado, zero, negativo, futuro, regressão, duplicata, aceite. CMP-FD-02:34 e CMP-FD-02:36 fixam efeito zero e proíbem herdar `stream_id`. O checker:57-58 devolve `ACK_SCOPE_MISMATCH` no ou-exclusivo. O checker:59-60 devolve `NO_ACK` antes do checker:61-62, que só então testa stream não alocado. O checker:66, :68, :74, :76, :78 e :80 preservam zero, negativo, futuro, regressão, duplicata e aceite. O checker:75-76 não escreve na regressão. O checker:79-80 só aceita para um inteiro maior. O checker:118-125 exige microfone fechado, dinheiro zero e high-water igual nos três casos. A fixture:157-172 é `FX03-NO-ACK`. A fixture:173-187 é sequence-only. A fixture:188-202 é stream-only, com `ack_stream_id` alocado.
- Negativo: O81, O82 e O83, CMP-FD-07:15, CMP-FD-07:23 e CMP-FD-07:31. NOT RUN como protocolo.
- Status: CANDIDATE. A checagem estática não fecha o achado.

## HIGH-03

- Texto que permanece: CMP-FD-02 v0.6:23-31 para sequence zero e CMP-FD-02 v0.6:54-102 para o lock monotônico. Esta pasta não os substitui e não os dá como executados.
- Status: CANDIDATE. O71..O78 continuam NOT RUN.

## NEW-MEDIUM-06

- Texto que permanece: CMP-FD-13 v0.6. Esta pasta não edita esse arquivo e não executa a contagem, o check nem o índice.
- Status: CANDIDATE. O79 e O80 continuam NOT RUN.

## LOW-01

- Texto: CMP-FD-07:9. Pessoa PENDING. Effort UNSTATED. DoR NOT MET.
- Status: OPEN BLOCKING DoR. Não é CANDIDATE de fechamento.

## Não redispostos

NEW-HIGH-04, NEW-HIGH-03, NEW-MEDIUM-05 e NEW-MEDIUM-03 continuam CANDIDATE na v0.5. NEW-MEDIUM-01 continua CLOSED pelo Codex. HIGH-01, HIGH-02, NEW-HIGH-01, NEW-HIGH-02, NEW-MEDIUM-02, NEW-MEDIUM-04 e MEDIUM-01..05 permanecem fechados pelo Codex. Esta página não os reabre e não os confirma de novo.
