# CMP-FD-08 v0.10 — Rastreabilidade

**Estado:** PROPOSTA. Não é PASS.

| Fonte | Uso |
|---|---|
| SHA `422277f82efbc001140b5857095c4840e668e270` | v0.9 auditada. Não editada |
| Parecer `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.9-2026-10-15.md` | FAIL DOCUMENT-ONLY |
| CMP-FD-14 | cadeia lida do blob, v0.2 NOT_VERIFIED |

| Finding | Texto v0.10 | Negativo | Estado |
|---|---|---|---|
| NEW-MEDIUM-09 | CMP-FD-14. Checker histórico:48 e checker histórico:293 | O92 NOT RUN. A leitura Git não é oráculo | CANDIDATE |
| NEW-LOW-02 | CMP-FD-15. Checker ACK:782-783 e checker ACK:985 | schema não prova produto | CANDIDATE |
| FD07-07 | CMP-FD-13 | O92, O93 NOT RUN | OPEN |
| HIGH-03 | CMP-FD-02 | O92 NOT RUN | PARTIAL |
| LOW-01 | CMP-FD-07 | sem pessoa | OPEN BLOCKING DoR |
| FD07-08 / NEW-MEDIUM-07 | CMP-FD-02. Fixture com original 422 | O96..O99 NOT RUN | CLOSED documental pelo parecer v0.9 |
| FD07-09 / NEW-MEDIUM-08 | blobs de planejamento nos dois commits | não reabre o escopo | CLOSED documental pelo parecer v0.9 |
| FD07-05 / FD07-06 | fixture:543 `n=-1`. Ordem da v0.9 | lock real não demonstrado | CLOSED documental pelo parecer v0.9 |
| NEW-MEDIUM-06 | não reescrito | migration NOT RUN | CLOSED documental |

O01..O99, 91 oráculos v1.7 e 36 CMP-O: NOT RUN. CMP-O-28 não é CMP-FD-O28.
