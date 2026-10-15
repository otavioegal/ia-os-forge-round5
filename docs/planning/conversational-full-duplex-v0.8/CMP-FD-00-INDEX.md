# CMP-FD-00 v0.8 — Índice

**Estado do pacote:** CANDIDATE FOR CODEX REVIEW. Não é PASS. O autor não fecha finding.
**SHA auditado da v0.7:** `1a71dfa44fc2c88174c113e5c68eddc18d6cfad3`
**Parent em que esta pasta entra:** o HEAD que já contém o parecer da v0.7. A v0.7 não é editada.
**Migration, deploy, provider, gasto e BUILD-00:** não executados e não autorizados.
**`forge.conversation.delta.v4`:** desligada. A v3 não é integrada.

Esta pasta responde a FD07-05, FD07-06, FD07-07, FD07-08 e FD07-09. Não declara esses findings fechados.

| Arquivo | Papel |
|---|---|
| CMP-FD-02-ACK-ISOLATION.md | Ordem, chave, efeitos e replay sobre `command_commit` |
| CMP-FD-07-ORACLES.md | O84..O95. Todos NOT RUN. LOW-01 aberto |
| CMP-FD-08-TRACEABILITY.md | Finding para texto. v0.5/v0.6 sem parecer |
| CMP-FD-09-CHANGE-REPORT.md | O que esta pasta acrescenta |
| CMP-FD-10-FINDING-DISPOSITION.md | Causa, path:line, negativo, CANDIDATE ou estado herdado |
| CMP-FD-11-OPEN-QUESTIONS.md | Pendências humanas |
| CMP-FD-12-CONSISTENCY-REPORT.md | Alegação separada da checagem estática |
| CMP-FD-13-CONCURRENCY-SPEC.md | SQL herdada e teste PostgreSQL futuro. NOT RUN |
| CMP-FD-14-HISTORICAL-CHAIN.md | Cadeia real de pareceres |
| fixtures/CMP-FD-FX-03-ack.json | Negativos, isolamento, replay e rollback modelado |
| fixtures/CMP-FD-FX-04-historical-manifest.json | SHA-256 dos pacotes v0.1–v0.7 |
| tools/check_fd_fx03_ack.py | Checker estático. Não executa oráculo |
| tools/check_fd_historical_manifest.py | Relê hashes. Somente leitura |

HIGH-03 permanece PARTIAL. NEW-MEDIUM-06 permanece CLOSED documentalmente pelo parecer da v0.7, migration NOT RUN. LOW-01 permanece OPEN BLOCKING DoR. FD07-01 a FD07-04 permanecem CLOSED documentalmente pelo mesmo parecer. NEW-HIGH-04, NEW-HIGH-03, NEW-MEDIUM-05 e NEW-MEDIUM-03 continuam CANDIDATE. NEW-MEDIUM-01 continua CLOSED pelo Codex. HIGH-01, HIGH-02, NEW-HIGH-01, NEW-HIGH-02, NEW-MEDIUM-02, NEW-MEDIUM-04 e MEDIUM-01..05 permanecem como o Codex os fechou.
