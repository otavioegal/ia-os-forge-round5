# CMP-FD-17 v0.13 — Cobertura quantitativa

**Estado:** relato do autor sobre o checker local. Não é PASS. Não é oráculo. `gap=0` não fecha FD11-NEW-01, NEW-LOW-03, FD12-NEW-01, FD12-NEW-02 nem FD12-NEW-03. `COVERAGE_TOTAL_PASS` não é reivindicado.

## Por que 480 e 2239 não servem

A v0.12 imprimiu `COVERAGE_RULES declared=480 exercised=480 gap=0` e `COVERAGE_OCCURRENCES declared=2239 exercised=2239 gap=0`. O parecer mostrou que o catálogo omitia objetos inline e a mutação de tipo do elemento quando o item era objeto. O `gap=0` era interno a esse catálogo. Esta pasta guarda os dois números só para rejeitá-los, em `check_fd_fx03_ack.py:1191`, e imprime `V12_CATALOG_REJECTED rules=480 occurrences=2239 reason=inline_objects_and_object_elements_omitted`. Não os trata como `schema_rules=all_declared`.

## Três contagens que não compartilham gerador

1. `expected_schema_rules` em `check_fd_fx03_ack.py:1293` lê só o schema. Para cada campo: tipo; ausência se obrigatório; UUID; const; `minLength`; formato; cardinalidade; tipo de elemento escalar; `ELEMENT_SCALAR` e `ELEMENT_LIST` se o item é objeto, e então os subcampos inline do item; extra e subcampos se o próprio campo é objeto inline; variantes de `uuid_map`; grupo parcial; `same_length`.
2. `expected_occurrences` em `check_fd_fx03_ack.py:1351` percorre a fixture e os sintéticos. Não monta job. Cada caso, cada campo presente, cada obrigatório, cada objeto inline, cada índice.
3. `stack_jobs` em `check_fd_fx03_ack.py:1464` gera as mutações e não chama os dois anteriores. `raw_slots` em `check_fd_fx03_ack.py:1410` só olha comprimentos JSON.

A execução tem de cobrir todo id esperado. Em seguida, `check_fd_fx03_ack.py:1877` exige igualdade de quantidade. Conjunto esperado contido nos jobs não basta: job extra também é `FAIL_COVERAGE_GAP`.

## O que o autor observou

Python 3.10.22. Comando: `python3 tools/check_fd_fx03_ack.py`. Exit 0.

```
COVERAGE_RULES declared=508 exercised=508 gap=0
COVERAGE_OCCURRENCES declared=2443 exercised=2443 gap=0
COVERAGE_CLASSES ABSENCE=146 CARDINALITY=9 CONST=29 ELEMENT_LIST=6 ELEMENT_MIN_LENGTH=1 ELEMENT_SCALAR=6 ELEMENT_TYPE=2 EMPTY=2 EXTRA=14 FORMAT=2 GROUP=3 INLINE_EXTRA=2 MAP=10 MIN_LENGTH=31 OCC_ABSENCE=1075 OCC_ELEMENT_LIST=28 OCC_ELEMENT_SCALAR=28 OCC_ELEMENT_TYPE=8 OCC_EMPTY=19 OCC_EXTRA=98 OCC_TYPE=1187 SAME_LENGTH=1 TYPE=180 UUID=64
RAW setup_scalar=16/16 setup_list=16/16 step_scalar=5/5 step_list=5/5 initial_scalar=7/7 initial_list=7/7 body_error_code_absence=4/4 body_opaque_type=3/3
COVERAGE_HOSTS behavioral_cases=26 synthetic_cases=4 synthetic_proves_product=false
COVERAGE_BASIS expected_walk=independent job_walk=iterative raw_slot_count=independent product_input_exhaustive=false
V12_CATALOG_REJECTED rules=480 occurrences=2239 reason=inline_objects_and_object_elements_omitted
COVERAGE_TOTAL_PASS not_claimed
```

`body_error_code_absence=4/4` e `body_opaque_type=3/3` são a conta crua do corpo inline, não uma amostra. `ELEMENT_SCALAR=6` e `ELEMENT_LIST=6` são regras de schema. `OCC_ELEMENT_SCALAR=28` e `OCC_ELEMENT_LIST=28` são índices. O host é a fixture de 26 linhas mais quatro sintéticos. Os sintéticos não passam pelo ACK semântico e não provam produto.

## O que não está coberto e portanto não é PASS

Não é exaustivo sobre todo JSON. `product_input_exhaustive=false` está impresso de propósito. Não executa PostgreSQL. Não prova O92. Uma lacuna imprime `COVERAGE_GAP` e devolve `FAIL_COVERAGE_GAP` em `check_fd_fx03_ack.py:1870` ou `check_fd_fx03_ack.py:1877`. O processo não segue para um PASS global. O banner final é `STATIC_ACK_V13_CHECK PASS_FIXTURE_ONLY` em `check_fd_fx03_ack.py:2040`.
