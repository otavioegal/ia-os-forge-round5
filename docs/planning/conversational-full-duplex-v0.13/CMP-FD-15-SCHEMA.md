# CMP-FD-15 v0.13 — Schema antes da decisão

**Estado:** CANDIDATE. Não é PASS. O checker estático não prova produto. As regras de campo da v0.12 foram mantidas. O id passou a `cmp.fd.fx03.schema.v0.13` em `fixtures/CMP-FD-FX-03-ack.schema.json:2`. O const do documento é `cmp.fd.fx03.ack.v0.13` na linha 38. Objetos inline já faziam parte do schema. A v0.12 não os colocava no catálogo de mutação. Esta pasta os coloca. Isso não é regra nova de produto.

Os nomes, os tipos e as cardinalidades continuam nesse arquivo. O checker carrega o schema em `check_fd_fx03_ack.py:792` antes de qualquer decisão de ACK e recusa outro id em `check_fd_fx03_ack.py:796`.

| Situação | Código | Não é |
|---|---|---|
| Campo obrigatório ausente, inclusive `error_code` do corpo inline | `FAIL_SCHEMA` | decisão de ACK |
| Chave fora da lista, inclusive dentro do corpo inline | `FAIL_EXTRA_KEY` | decisão de ACK |
| Tipo errado, inclusive `True` em inteiro e `0` em booleano | `FAIL_TYPE` | decisão de ACK |
| UUID malformado | `FAIL_UUID` | decisão de ACK |
| Elemento de array de objeto trocado por escalar ou por lista | `FAIL_SCHEMA` | decisão de ACK |
| Lista vazia, `minLength`, const, grupo incompleto ou tamanhos desiguais | `FAIL_SCHEMA` | O92 |
| Chave JSON duplicada | `FAIL_DUPLICATE_KEY` | sucesso de parse |
| Exceção no mutador | `FAIL_SCHEMA_EXCEPTION` | sucesso |
| Regra ou ocorrência declarada sem mutação, ou job a mais | `FAIL_COVERAGE_GAP` | PASS global |

`expected_original_outcome_body` exige `error_code` (`string`, `minLength` 1) e admite `opaque`, `retryable`, `terminal` (`bool`) e `peer_ack_high_water` (`int`). Está nas linhas 317 e 529. `fields_error` já percorria esses `fields` em `check_fd_fx03_ack.py:895`. O catálogo agora também.

`rollback_model`, `interleave`, `sequential_replay`, `replay_receiver_removed` e `replay_cross_tenant` continuam fechados pelo schema. A mutação nasce de cada objeto, de cada campo inline e de cada índice de lista de objeto, não da primeira amostra e não só de `$ref`.

O host sintético não entra nas 26 linhas de decisão. `oracle_status` é `NOT_RUN` em `fixtures/CMP-FD-FX-03-ack.synthetic.json:4`. `proves_product` é false na linha 3. O positivo comportamental não tem `expected_original_outcome_body`. As regras positivas desse corpo ficam no caso sintético.

`product_input_exhaustive=false`. Isso não autoriza omitir regra que está no schema. Não se alega que todo JSON possível foi gerado. Se o passeio esperado e o gerador divergirem, o checker devolve `FAIL_COVERAGE_GAP`. `COVERAGE_TOTAL_PASS` não é reivindicado.
