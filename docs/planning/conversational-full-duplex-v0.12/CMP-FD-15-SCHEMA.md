# CMP-FD-15 v0.12 — Schema antes da decisão

**Estado:** CANDIDATE. Não é PASS. O checker estático não prova produto. O schema da v0.11 foi mantido nas regras. Só o id mudou, para o pacote não se autorreferenciar como v0.11.

Os nomes, os tipos e as cardinalidades estão em `fixtures/CMP-FD-FX-03-ack.schema.json:2`. O checker carrega esse arquivo antes de qualquer decisão de ACK.

| Situação | Código | Não é |
|---|---|---|
| Campo obrigatório ausente | `FAIL_SCHEMA` | decisão de ACK |
| Chave fora da lista | `FAIL_EXTRA_KEY` | decisão de ACK |
| Tipo errado, inclusive `True` em inteiro e `0` em booleano | `FAIL_TYPE` | decisão de ACK |
| UUID malformado | `FAIL_UUID` | decisão de ACK |
| Lista vazia, `minLength`, const, grupo incompleto ou tamanhos desiguais | `FAIL_SCHEMA` | O92 |
| Exceção no mutador | `FAIL_SCHEMA_EXCEPTION` | sucesso |
| Regra ou ocorrência declarada sem mutação | `FAIL_COVERAGE_GAP` | PASS global |

`rollback_model`, `interleave`, `sequential_replay`, `replay_receiver_removed` e `replay_cross_tenant` continuam fechados pelo schema. A novidade é que a mutação nasce dessa lista e de cada índice presente no host, não da primeira amostra.

O host sintético não entra nas 26 linhas de decisão. `oracle_status` é `NOT_RUN`. `proves_product` é false. Um opcional de `positive` sem host sintético derruba a cobertura.

`product_input_exhaustive=false`. Não se alega que todo JSON possível foi gerado. Alega-se só o catálogo declarado, e o checker falha se esse catálogo não for exercitado.
