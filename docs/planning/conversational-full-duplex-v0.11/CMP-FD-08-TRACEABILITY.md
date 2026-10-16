# CMP-FD-08 v0.11 — Rastreabilidade

**Estado:** PROPOSTA. Não é PASS.

| Fonte | Uso |
|---|---|
| SHA `a5d7e8fc85cb5b5f0605937b43075ce1a0c19e08` | v0.10 auditada. Não editada |
| Parecer `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.10-2026-10-15.md` | FAIL DOCUMENT-ONLY |
| CMP-FD-16 | errata do v0.2 ainda não aprovada |

| Finding | Texto v0.11 | Negativo | Estado |
|---|---|---|---|
| NEW-MEDIUM-09 | CMP-FD-14 e CMP-FD-16. Checker histórico:48 e checker histórico:327 | leitura Git não é oráculo | CANDIDATE |
| NEW-LOW-02 / NEW-LOW-03 | CMP-FD-15. Checker ACK:777 e checker ACK:1124 | schema não prova produto | CANDIDATE |
| FD07-07 | CMP-FD-13 | O92, O93 NOT RUN | OPEN |
| HIGH-03 | CMP-FD-02 | O92 NOT RUN | PARTIAL |
| LOW-01 | CMP-FD-07 | sem pessoa | OPEN BLOCKING DoR |
| FD07-08 / NEW-MEDIUM-07 | CMP-FD-02. Transporte 200 e outcome 422 | O96..O99 NOT RUN | CLOSED documental |
| FD07-09 / NEW-MEDIUM-08 | blobs de planejamento, agora também com `bytes` | não reabre o escopo | CLOSED documental no escopo dos blobs |
| FD07-05 / FD07-06 | fixture:543 `n=-1`. Ordem preservada | lock real não demonstrado | CLOSED documental |
| NEW-MEDIUM-06 | não reescrito | migration NOT RUN | CLOSED documental |

O01..O99, 91 oráculos v1.7 e 36 CMP-O: NOT RUN. CMP-O-28 não é CMP-FD-O28.
