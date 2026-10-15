# CMP-FD-08 v0.7 — Rastreabilidade

**Estado:** PROPOSTA. Não é PASS.

| Fonte | Uso |
|---|---|
| SHA `67b6536242b7401796c403a72de9a6f00feea37b` | v0.6 auditada, não editada |
| SHA `676a01a6c0a844d18e9c70f24befda4b4ea1bc12` | v0.5, parent da v0.6, não editada |
| CMP-FD-02 v0.6:41-42 | norma já existente do par null e do mismatch |
| `check_fd_fx03_ack.py` v0.6:34-37 | causa: ou-exclusivo nas linhas 34-35; `None` cai em `not in allocated` na linha 36 |
| fixture v0.6:131-141 | só `FX03-PAIR-INVALID`, uma direção |

| Item | Texto v0.7 | Negativo |
|---|---|---|
| Par null é `NO_ACK` | CMP-FD-02:24 e checker:59-60 | O81 |
| Uma direção sequence-only | CMP-FD-02:23 e CMP-FD-02:36 | O82 |
| Uma direção stream-only | CMP-FD-02:23 e CMP-FD-02:36 | O83 |
| Sem efeito nos três | CMP-FD-02:34 e checker:118-125 | O81..O83 |
| Cobertura só da fixture | CMP-FD-02:11-13 | não é oráculo |
| Monotonicidade preservada | CMP-FD-02:42-44 e checker:75-80 | O72, O73, ainda NOT RUN |
| HIGH-03 | não fechado. Sequence zero permanece em CMP-FD-02 v0.6:23-31. O lock permanece em CMP-FD-02 v0.6:54-102 | O71..O78 NOT RUN |
| NEW-MEDIUM-06 | não fechado. CMP-FD-13 v0.6 não é editada | O79, O80 NOT RUN |
| LOW-01 | CMP-FD-07:9 | OPEN BLOCKING DoR |

| Já fechado ou ainda só candidato | Onde esta pasta não mexe |
|---|---|
| NEW-HIGH-04, NEW-HIGH-03, NEW-MEDIUM-05, NEW-MEDIUM-03 | v0.5, continuam CANDIDATE |
| NEW-MEDIUM-01 | CLOSED pelo Codex |
| HIGH-01, HIGH-02, NEW-HIGH-01, NEW-HIGH-02, NEW-MEDIUM-02, NEW-MEDIUM-04, MEDIUM-01..05 | fechados pelo Codex |

O71..O83, O01..O70, 91 oráculos v1.7 e 36 CMP-O: NOT RUN. CMP-O-28 não é CMP-FD-O28.
