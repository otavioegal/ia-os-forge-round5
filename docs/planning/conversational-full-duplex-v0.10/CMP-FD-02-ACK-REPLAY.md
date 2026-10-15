# CMP-FD-02 v0.10 — Replay preservado

**Estado:** PROPOSTA. CANDIDATE FOR CODEX REVIEW. Não é PASS.
**Não edita** v0.1–v0.9, a baseline, CMP v0.3, ata, ADR nem parecer.

O parecer da v0.9 fechou documentalmente FD07-08 e NEW-MEDIUM-07, com limite estático. Esta página não os reabre e não muda a ordem.

O lookup continua depois do tenant e antes do receiver mutável. Um replay de `422 ACK_FUTURE` volta em transporte 200 com o corpo original. Digest diferente não troca a linha. Outro tenant recebe `404` antes do lookup. `n < 0` continua no estágio `negative`, com a fixture em `n=-1`. Ack não abre microfone, não move dinheiro e não cria ledger novo.

HIGH-03 permanece PARTIAL. FD07-07 permanece OPEN. O92 e O93 permanecem NOT RUN. A flag `forge.conversation.delta.v4` permanece desligada.
