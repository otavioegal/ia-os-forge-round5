# CMP-FD-15 v0.15 — Schema fechado antes da decisão

**Estado:** CANDIDATE. Não é PASS. O checker estático não prova produto. As regras de campo da v0.13 foram mantidas. O id passou a `cmp.fd.fx03.schema.v0.15` em `fixtures/CMP-FD-FX-03-ack.schema.json:2`. O const do documento é `cmp.fd.fx03.ack.v0.15` na linha 38. Isso não é regra nova de produto.

A DSL desta pasta não é JSON Schema. Não há `allOf`, `oneOf`, `anyOf`, `$ref`, `enum`, `format`, `minimum`, `maximum` nem keyword `nullable`. Nulidade entra só pelos tipos `nullable_int` e `nullable_uuid`. Os dois aparecem no schema. Um keyword `nullable` é desconhecido e é recusado.

`dsl_problems` em `check_fd_fx03_ack.py:1246` percorre o schema e devolve `FAIL_UNKNOWN_KEYWORD` para chave fora do conjunto, `FAIL_UNRESOLVED_REF` para `ref` que não nomeia objeto, e `FAIL_DSL` para tipo, `const`, `minLength`, `minItems`, grupo ou `same_length` incoerentes. `schema_error` chama isso em `check_fd_fx03_ack.py:957`, antes da decisão de ACK. Bool não passa como int: `value_error` devolve `FAIL_TYPE` para `True` contra `int` em `check_fd_fx03_ack.py:828`. `0` contra `bool` é `FAIL_TYPE` em `check_fd_fx03_ack.py:838`. `None` é aceito em `nullable_int` na linha 832 e em `nullable_uuid` na linha 822, e recusado em `int` na linha 828.

| Situação | Código | Não é |
|---|---|---|
| Campo obrigatório ausente | `FAIL_SCHEMA` | decisão de ACK |
| Chave fora da lista | `FAIL_EXTRA_KEY` | decisão de ACK |
| Tipo errado, inclusive `True` em inteiro e `0` em booleano | `FAIL_TYPE` | decisão de ACK |
| UUID malformado | `FAIL_UUID` | decisão de ACK |
| Keyword desconhecido, inclusive `allOf` e `nullable` | `FAIL_UNKNOWN_KEYWORD` | sucesso de schema |
| `ref` que não resolve | `FAIL_UNRESOLVED_REF` | decisão de ACK |
| Chave JSON duplicada | `FAIL_DUPLICATE_KEY` | sucesso de parse |
| Literal normativo diferente da referência | `FAIL_SEMANTIC_DRIFT` | gap=0 |
| Referência que alega aprovação humana | `FAIL_INVENTED_APPROVAL` | ratificação |
| Regra ou ocorrência fora da lista publicada | `FAIL_ID_MANIFEST` | PASS global |

A fixture negativa `fixtures/CMP-FD-FX-06-unknown-keyword.json` não é autoridade. Ela existe para o checker recusar `allOf`. Se essa recusa faltar, o processo não segue para `PASS_FIXTURE_ONLY`.

`product_input_exhaustive=false`. Fechar a DSL deste arquivo não fecha todo JSON possível do produto.
