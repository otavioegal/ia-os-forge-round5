# CMP-FD-15 v0.11 — Schema antes da decisão

**Estado:** CANDIDATE. Não é PASS. O checker estático não prova produto.

Os nomes, os tipos e as cardinalidades estão em [fixtures/CMP-FD-FX-03-ack.schema.json](fixtures/CMP-FD-FX-03-ack.schema.json). O checker carrega esse arquivo antes de qualquer decisão de ACK.

| Situação | Código | Não é |
|---|---|---|
| Campo obrigatório ausente | `FAIL_SCHEMA` | KeyError |
| Chave não permitida | `FAIL_EXTRA_KEY` | decisão de ACK |
| UUID inválido em string | `FAIL_UUID` | `NOT_FOUND` |
| Tipo escalar errado, inclusive `true` no lugar de inteiro | `FAIL_TYPE` | regressão de high-water |
| Lista vazia em `setup`, `steps`, `commit_order` ou `expected_steps` | `FAIL_SCHEMA` | corrida |
| `commit_order` e `expected_steps` com tamanhos diferentes | `FAIL_SCHEMA` | O92 |
| `oracle_status` diferente de `NOT_RUN`, ou `executed_database=true` | `FAIL_SCHEMA` | oráculo executado |
| `concurrency=true` nesta fixture | `FAIL_SCHEMA` | prova PostgreSQL |

`rollback_model`, `interleave`, `sequential_replay`, `replay_receiver_removed` e `replay_cross_tenant` entram nessa validação, com os objetos aninhados `attempt`, `setup`, `replay`, `fresh`, `probe`, `steps` e `counter_delta`.

A remoção de cada campo obrigatório e a troca de tipo de cada campo declarado, inclusive aninhado, são rejeitadas antes do processamento. Uma exceção seria `FAIL_SCHEMA_EXCEPTION`.

Limite: `FAIL_KEY_COHERENCE` só roda depois que presença e tipo passaram. Ele recusa receiver ou stream fora da sessão. Não é código de negócio do ACK e não é PASS.

`proves_product` continua false. `PASS_FIXTURE_ONLY` não é PASS do pacote.
