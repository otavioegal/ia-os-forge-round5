# CMP-FD-02 v0.11 — Replay preservado

**Estado:** PROPOSTA. CANDIDATE FOR CODEX REVIEW. Não é PASS.
**Não edita** v0.1–v0.10, a baseline, CMP v0.3, ata, ADR nem parecer.

O parecer da v0.10 manteve fechados, no limite documental, FD07-01..06, FD07-08, NEW-MEDIUM-07, NEW-MEDIUM-08 e FD07-09 no escopo dos blobs de planejamento. Esta página não os reabre.

O lookup continua depois do tenant e antes do receiver mutável. Um replay de `422` volta em transporte 200 com o corpo e o digest originais. Digest diferente devolve `409` e não troca a linha. Outro tenant recebe `404` antes do lookup. O par null continua antes da consulta. `n < 0` continua no estágio `negative`. A fixture conserva `n=-1`. Ack não abre microfone, não move dinheiro e não cria ledger novo.

HIGH-03 permanece PARTIAL. FD07-07 permanece OPEN. O92 e O93 permanecem NOT RUN. A flag `forge.conversation.delta.v4` permanece desligada.
