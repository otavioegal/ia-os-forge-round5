# CMP-FD-15 v0.10 — Campos obrigatórios

**Estado:** CANDIDATE. Não é PASS. O checker estático não prova produto.

A lista de nomes obrigatórios e permitidos está em [fixtures/CMP-FD-FX-03-ack.schema.json](fixtures/CMP-FD-FX-03-ack.schema.json). O checker carrega esse arquivo. Não há uma segunda lista escondida que aceite a ausência.

Antes de qualquer decisão de ACK:

- falta de campo obrigatório: `FAIL_SCHEMA`;
- chave fora do conjunto permitido: `FAIL_EXTRA_KEY`;
- UUID inválido ou tipo errado: `FAIL_UUID` ou `FAIL_TYPE`;
- grupo parcial de outcome, stored ou witness: `FAIL_SCHEMA`.

Isso vale para o documento, o canal, cada initial key, cada kind de caso, o passo, o setup e o attempt. A remoção de cada um desses nomes é exercida no checker. Uma exceção nessa remoção seria `FAIL_SCHEMA_EXCEPTION`, não um sucesso. O harness antigo de valores, inclusive `peer_ack_high_water_before` e `expected_stage`, permanece.

`proves_product` continua false. `PASS_FIXTURE_ONLY` não é PASS do pacote.
