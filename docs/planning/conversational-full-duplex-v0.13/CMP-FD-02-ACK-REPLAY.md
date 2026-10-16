# CMP-FD-02 v0.13 — Replay preservado

**Estado:** PROPOSTA. CANDIDATE FOR CODEX REVIEW. Não é PASS.
**Não edita** v0.1–v0.12, a baseline, CMP v0.3, ata, ADR nem parecer.

O parecer da v0.12 manteve, no limite documental, FD07-01..06, FD07-08, NEW-MEDIUM-07, NEW-MEDIUM-08 e FD07-09 no escopo dos blobs de planejamento. NEW-LOW-02 ficou CLOSED documental, não executado. NEW-MEDIUM-06 ficou CLOSED documental, migration NOT RUN. Esta página não reabre esses itens e não reescreve a ordem de decisão.

A ordem continua esta. Par com um lado null devolve `ACK_SCOPE_MISMATCH` antes de qualquer lookup. Os dois null devolvem `NO_ACK`. Tenant diferente devolve `404 NOT_FOUND` opaco e não consulta `command_commit`. No mesmo tenant, o mesmo `command_id` com o mesmo digest é replay em transporte 200 do outcome armazenado. Digest diferente devolve `409 IDEMPOTENCY_KEY_REUSED` e não troca a linha. Só então entram receiver mutável e alocação. `n==0` é `ACK_SEQUENCE_ZERO`. `n<0` é `ACK_REGRESSION` no estágio `negative`, antes da comparação com o peer. Dedupe de `event_id` vem depois. Futuro, regressão e duplicata de commit devolvem o outcome original 422 e gravam só `command_commit`. Accept grava o original 200, o outbox, e sobe só a chave de isolamento `(organization_id, project_id, session_id, ack_stream_id, receiver_participant_id)`.

O replay guarda `original_outcome_code`, corpo e digest. Transporte 200 não é outcome 422. O 409 não muta. O 404 de tenant acontece antes do lookup. A fixture conserva `ack_of_sequence: -1` em `fixtures/CMP-FD-FX-03-ack.json:543`. Ack não abre microfone, não move dinheiro e não cria ledger novo.

A cobertura nova roda antes da decisão e não altera o resultado das 26 linhas.
