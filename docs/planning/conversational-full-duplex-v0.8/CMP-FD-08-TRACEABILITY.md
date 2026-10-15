# CMP-FD-08 v0.8 — Rastreabilidade

**Estado:** PROPOSTA. Não é PASS.

| Fonte | Uso |
|---|---|
| SHA `1a71dfa44fc2c88174c113e5c68eddc18d6cfad3` | v0.7 auditada pelo parecer de 15/10/2026. Não editada |
| Parecer `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.7-2026-10-15.md` | FAIL DOCUMENT-ONLY. FD07-05..09 |
| CMP-FD-14:5 | v0.5/v0.6 candidatos, sem parecer independente incorporado |
| CMP-FD-14:13-19 | pareceres que realmente existem, com SHA e veredito do arquivo |

| Finding | Texto v0.8 | Negativo | Estado nesta pasta |
|---|---|---|---|
| FD07-05 | CMP-FD-02:32 e CMP-FD-02:47-64. Checker:170-172 e checker:404 | O84, O85 | CANDIDATE |
| FD07-06 | CMP-FD-02:14-18 e CMP-FD-02:28-30. Checker:138-143 e checker:442-468 | O86, O87, O88 | CANDIDATE |
| FD07-07 | CMP-FD-13:9-57. A fixture sequencial está marcada em CMP-FD-02:76 | O92, O93 | CANDIDATE. Teste NOT RUN |
| FD07-08 | CMP-FD-02:33-35 e CMP-FD-02:68-72. Checker:219-235 e checker:518 | O89, O90, O91, O94, O95 | CANDIDATE |
| FD07-09 | CMP-FD-14:5-23 | manifest FX-04 | CANDIDATE |
| HIGH-03 | não fechado. Falta execução de O92 | O71..O83 e O92 continuam NOT RUN | PARTIAL |
| NEW-MEDIUM-06 | não reescrito. Opção B permanece na v0.6 | O79, O80 NOT RUN | CLOSED documental pelo parecer v0.7 |
| LOW-01 | CMP-FD-07:9-11 | sem pessoa | OPEN BLOCKING DoR |
| FD07-01..04 | preservados. Checker:155-157 mantém o par null | O81..O83 NOT RUN | CLOSED documental pelo parecer v0.7 |

O71..O95, O01..O70, 91 oráculos v1.7 e 36 CMP-O: NOT RUN. CMP-O-28 não é CMP-FD-O28.
