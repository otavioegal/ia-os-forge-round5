# CMP-FD-00 v0.6 — Índice

**Estado do pacote:** CANDIDATE FOR CODEX REVIEW. Não é PASS. O autor não fecha finding.
**SHA-base imutável:** `676a01a6c0a844d18e9c70f24befda4b4ea1bc12`
**A v0.5 permanece** CANDIDATE FOR CODEX REVIEW e FAIL DOCUMENT-ONLY na auditoria de 14/10/2026. Esta pasta não a edita.
**Migration, deploy, provider, gasto e BUILD-00:** não executados e não autorizados.

Dois pontos desta rodada:

1. HIGH-03: `ack_of_sequence = 0` passa a ter código, e o peer high-water só sobe sob lock e predicado `n > atual`.
2. NEW-MEDIUM-06: task conversacional ativa não entra no índice com `session_id` null. A opção é a B.

| Arquivo | Papel |
|---|---|
| CMP-FD-02-ACK-MONOTONIC.md | Decisão fechada do ACK e escrita monotônica |
| CMP-FD-07-ORACLES.md | O71..O80. Todos NOT RUN. LOW-01 continua aberto |
| CMP-FD-08-TRACEABILITY.md | Achado para texto |
| CMP-FD-09-CHANGE-REPORT.md | O que esta pasta acrescenta |
| CMP-FD-10-FINDING-DISPOSITION.md | Causa, path:line, negativo, CANDIDATE |
| CMP-FD-11-OPEN-QUESTIONS.md | Pendências humanas |
| CMP-FD-12-CONSISTENCY-REPORT.md | Alegação documental separada da checagem estática |
| CMP-FD-13-MIGRATION-SESSION-ID.md | Contagem de null, check e índice. Não executada |
| fixtures/CMP-FD-FX-03-ack.json | Casos positivos, negativos e as duas ordens da corrida |
| tools/check_fd_fx03_ack.py | Confere os números da fixture. Não executa o protocolo |

NEW-HIGH-04, NEW-HIGH-03, NEW-MEDIUM-05 e NEW-MEDIUM-03 continuam apenas CANDIDATE, como na v0.5. NEW-MEDIUM-01 continua CLOSED pelo Codex. HIGH-01, HIGH-02, NEW-HIGH-01, NEW-HIGH-02, NEW-MEDIUM-02, NEW-MEDIUM-04 e MEDIUM-01..05 permanecem como o Codex os fechou. LOW-01 permanece OPEN BLOCKING DoR.
