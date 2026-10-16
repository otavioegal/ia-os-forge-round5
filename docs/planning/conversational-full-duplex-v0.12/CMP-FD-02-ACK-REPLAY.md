# CMP-FD-02 v0.12 — Replay preservado

**Estado:** PROPOSTA. CANDIDATE FOR CODEX REVIEW. Não é PASS.
**Não edita** v0.1–v0.11, a baseline, CMP v0.3, ata, ADR nem parecer.

O parecer da v0.11 manteve, no limite documental, FD07-01..06, FD07-08, NEW-MEDIUM-07, NEW-MEDIUM-08 e FD07-09 no escopo dos blobs de planejamento. NEW-LOW-02 ficou CLOSED documental, não executado. Esta página não reabre esses itens e não reescreve a ordem de decisão.

O lookup continua depois do tenant e antes do receiver mutável. Um replay de `422` volta em transporte 200 com o corpo e o digest originais. Digest diferente devolve `409` e não troca a linha. Outro tenant recebe `404` opaco antes do lookup. O par null continua antes da consulta. `n < 0` continua no estágio `negative`. A fixture conserva `n=-1` em `fixtures/CMP-FD-FX-03-ack.json:543`. Ack não abre microfone, não move dinheiro e não cria ledger novo.

A cobertura nova roda antes da decisão e não altera o resultado das 26 linhas.
