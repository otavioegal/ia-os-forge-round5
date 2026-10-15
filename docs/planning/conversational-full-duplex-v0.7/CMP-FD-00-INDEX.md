# CMP-FD-00 v0.7 — Índice

**Estado do pacote:** CANDIDATE FOR CODEX REVIEW. Não é PASS. O autor não fecha finding.
**SHA-base imutável:** `67b6536242b7401796c403a72de9a6f00feea37b`
**Parent da v0.6, que é a v0.5 auditada:** `676a01a6c0a844d18e9c70f24befda4b4ea1bc12`
**A v0.6 não é editada.** HIGH-03 e NEW-MEDIUM-06 continuam CANDIDATE. LOW-01 continua OPEN BLOCKING DoR.
**Migration, deploy, provider, gasto e BUILD-00:** não executados e não autorizados.

Lacuna desta rodada: o checker da v0.6 devolvia `ACK_STREAM_UNALLOCATED` quando `ack_of_sequence` e `ack_stream_id` eram os dois null, e a fixture não tinha a direção `ack_of_sequence` null com `ack_stream_id` preenchido.

| Arquivo | Papel |
|---|---|
| CMP-FD-02-ACK-NULL-PAIR.md | Ordem do par nulo, cobertura do checker e monotonicidade preservada |
| CMP-FD-07-ORACLES.md | O81..O83. Todos NOT RUN. LOW-01 continua aberto |
| CMP-FD-08-TRACEABILITY.md | Lacuna para texto e para o que não foi fechado |
| CMP-FD-09-CHANGE-REPORT.md | O que esta pasta acrescenta |
| CMP-FD-10-FINDING-DISPOSITION.md | Causa, path:line, negativo, CANDIDATE |
| CMP-FD-11-OPEN-QUESTIONS.md | Pendências humanas e estados preservados |
| CMP-FD-12-CONSISTENCY-REPORT.md | Alegação documental separada da checagem estática |
| fixtures/CMP-FD-FX-03-ack.json | Casos da v0.6 mais `NO_ACK` e as duas direções de `ACK_SCOPE_MISMATCH` |
| tools/check_fd_fx03_ack.py | Confere essas linhas. Não executa o protocolo |

`forge.conversation.delta.v4` permanece desligada. `forge.conversation.delta.v3` não é integrada. NEW-HIGH-04, NEW-HIGH-03, NEW-MEDIUM-05 e NEW-MEDIUM-03 continuam CANDIDATE na v0.5. NEW-MEDIUM-01 continua CLOSED pelo Codex. HIGH-01, HIGH-02, NEW-HIGH-01, NEW-HIGH-02, NEW-MEDIUM-02, NEW-MEDIUM-04 e MEDIUM-01..05 permanecem como o Codex os fechou.
