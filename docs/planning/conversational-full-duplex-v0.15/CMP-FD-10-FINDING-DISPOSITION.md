# CMP-FD-10 v0.15 — Disposição

**Estado:** CANDIDATE FOR CODEX REVIEW. O autor não escreve PASS e não fecha finding. A correção de fim de linha não altera estados.

| Finding | Estado nesta pasta |
|---|---|
| FD07-07 | OPEN. O92 e O93 NOT RUN |
| HIGH-03 | PARTIAL. Sem O92 |
| LOW-01 | OPEN BLOCKING DoR. Pessoa PENDING. Effort UNSTATED. DoR NOT MET |
| NEW-GOV-01 | OPEN. A referência continua `PENDING_HUMAN_APPROVAL`. O digest canônico não é ratificação |
| FD11-NEW-01 | PARTIAL |
| NEW-LOW-03 | PARTIAL. 508/2443 são `PASS_FIXTURE_ONLY` |
| NEW-MEDIUM-09 | PARTIAL. Parecer v0.2 `NOT_VERIFIED`. `chosen_verdict` null |
| FD12-NEW-01, FD12-NEW-02 | CLOSED só no limite documental/estático do parecer v0.13. Não é produto |
| FD12-NEW-03 | CLOSED estático, NOT RUN no parecer v0.13. Não é produto |

FD07-01..06, FD07-08, NEW-MEDIUM-07, NEW-MEDIUM-08, NEW-LOW-02 e FD07-09 permanecem CLOSED no limite documental já dado. NEW-MEDIUM-06 permanece CLOSED documentalmente, migration NOT RUN. HIGH-01, HIGH-02 e os demais já fechados pelo Codex não foram reabertos. NEW-HIGH-04, NEW-HIGH-03, NEW-MEDIUM-05 e NEW-MEDIUM-03 continuam CANDIDATE.

Nove AQs permanecem APPROVED: AQ-01, AQ-02, AQ-03, AQ-05, AQ-06, AQ-07, AQ-08, AQ-10, AQ-11. AQ-04, AQ-09 e AQ-12 permanecem DEFERRED. FDP-14, FDP-15, baseline e BUILD-00 permanecem PENDING. `forge.conversation.delta.v4` permanece desligada.

O parecer v0.2 não foi promovido a VERIFIED. `check_fd_historical_manifest.py:206` recusa `chosen_verdict` preenchido. A mutação negativa está em `check_fd_historical_manifest.py:331`.
