# CMP-FD-08 v0.6 — Rastreabilidade

**Estado:** PROPOSTA. Não é PASS.

| Fonte | Uso |
|---|---|
| SHA `676a01a6c0a844d18e9c70f24befda4b4ea1bc12` | v0.5 auditada, não editada |
| Auditoria Codex da v0.5, 14/10/2026 | FAIL DOCUMENT-ONLY nos dois pontos abaixo |
| FDP-16A v1.7 seção 3.2 | task sem `session_id`; por isso a opção A não se aplica |
| CMP-FD-02 v0.5 | ACK anterior, histórico |

| Achado | Texto v0.6 | Negativo |
|---|---|---|
| HIGH-03 sequence zero | CMP-FD-02:23-31 e a linha 44 | O71 |
| HIGH-03 monotonicidade | CMP-FD-02:54-102 | O72, O73, O74 |
| HIGH-03 demais casos de ACK | CMP-FD-02:35-50 | O75, O76, O77, O78 |
| NEW-MEDIUM-06 | CMP-FD-13:5 e CMP-FD-13:18-68 | O79, O80 |
| LOW-01 | CMP-FD-07:9-11 | Ready sem pessoa |

| Já fechado ou ainda só candidato | Onde esta pasta não mexe |
|---|---|
| NEW-HIGH-04, NEW-HIGH-03, NEW-MEDIUM-05, NEW-MEDIUM-03 | v0.5, continuam CANDIDATE |
| NEW-MEDIUM-01 | CLOSED pelo Codex |
| HIGH-01, HIGH-02, NEW-HIGH-01, NEW-HIGH-02, NEW-MEDIUM-02, NEW-MEDIUM-04, MEDIUM-01..05 | fechados pelo Codex |

O71..O80, O01..O70, 91 oráculos v1.7 e 36 CMP-O: NOT RUN. CMP-O-28 não é CMP-FD-O28.
