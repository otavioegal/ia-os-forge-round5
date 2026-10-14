# CMP-FD-08 v0.5 — Rastreabilidade

**Estado:** PROPOSTA. Não é PASS. Linhas lidas nesta pasta antes do commit.

| Fonte | Uso |
|---|---|
| Parecer Codex v0.4 | FAIL DOCUMENT-ONLY do SHA `90fc21c90402805959bab2fc4ae6b43dc758c66d` |
| Prompt v0.5 | ordem de reparo |
| Pacote v0.4 | histórico, não editado |
| FDP-16A v1.7 `:344-350` e `:401-413` | apply e prova tardia; fonte não editada |
| CMP v0.3 `cmp.speech.v0` | crosswalk, não substituição |
| Ata Founder e ADR AQ-07 | full-duplex natural; sem half-duplex equivalente |

| Achado | Texto v0.5 | Negativo |
|---|---|---|
| NEW-HIGH-04 | CMP-FD-01:32-37 e CMP-FD-01:88-103 | O58, O59, O60, O61, O62, O64 |
| NEW-HIGH-03 | CMP-FD-13:17-77; predicado CMP-FD-01:180 | O55, O56, O57, O70 |
| HIGH-03 | CMP-FD-02:20-79 | O65, O66, O67; FX-02 |
| NEW-MEDIUM-05 | `tools/check_fd_fx01_digests.py:17-102` | fixtures em `fixtures/negative/` |
| NEW-MEDIUM-03 | CMP-FD-07:115-160 | O28, O51, O52, O53, O54 |
| NEW-MEDIUM-06 | CMP-FD-13:87-113 | O68, O50 |
| NEW-MEDIUM-01 | permanece CLOSED; clarificação CMP-FD-01:107-132 | O69 |
| LOW-01 | CMP-FD-07:7-21 | Ready sem pessoa |

| Fechado pelo Codex | Onde a v0.5 só repete |
|---|---|
| HIGH-01 | CMP-FD-01:11, lock do Build antes da leitura monetária |
| HIGH-02 | CMP-FD-02:15; FX-01 conserva os seis carimbos e `PLAYBACK_SPAN` |
| NEW-HIGH-01 | CMP-FD-01:13 |
| NEW-HIGH-02 | CMP-FD-01:11 e o passo 2 da seção 4 |
| NEW-MEDIUM-02 | CMP-FD-02:15 |
| NEW-MEDIUM-04 | CMP-FD-02:14; CMP-FD-04:15; CMP-FD-06:12 |
| MEDIUM-01 | CMP-FD-03 |
| MEDIUM-02 | CMP-FD-04:9-15 |
| MEDIUM-03 | CMP-FD-04:21-23 |
| MEDIUM-04 | CMP-FD-05 |
| MEDIUM-05 | CMP-FD-06 |

O01..O52 não reescritos, O53..O70, 91 oráculos v1.7 e 36 CMP-O: NOT RUN. CMP-O-28 não é CMP-FD-O28.
