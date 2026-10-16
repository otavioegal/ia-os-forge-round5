# CMP-FD-17 v0.14 — Cobertura quantitativa

**Estado:** relato do autor sobre o checker local. Não é PASS. Não é oráculo. `gap=0` não fecha FD11-NEW-01, NEW-LOW-03 nem NEW-GOV-01. `COVERAGE_TOTAL_PASS` não é reivindicado. `FULL_PRODUCT_COVERAGE false`.

## Por que 480 e 2239 continuam rejeitados

A v0.12 imprimiu `COVERAGE_RULES declared=480 exercised=480 gap=0` e `COVERAGE_OCCURRENCES declared=2239 exercised=2239 gap=0`. O parecer da v0.12 mostrou catálogo incompleto. O parecer da v0.13 não reabilitou esses números e também não reproduziu 508 nem 2443. Esta pasta guarda 480 e 2239 só em `check_fd_fx03_ack.py:1689`, com o rótulo `V12_CATALOG_REJECTED`. Não os usa como prova.

## De onde vêm 508 e 2443

Não foram reimpostos. As regras de campo não mudaram em relação à v0.13. O que mudou foi o id do schema e o const da fixture, que continuam uma regra `CONST` cada. A conta de mutação observada de novo foi 508 regras e 2443 ocorrências. A lista inteira está em `fixtures/CMP-FD-FX-07-coverage-ids.json`, gerada por `tools/enumerate_coverage_ids.py`. Esse script não importa `check_fd_fx03_ack.py`. O checker compara o conjunto em `check_fd_fx03_ack.py:1624`. Se faltar ou sobrar um ID, devolve `FAIL_ID_MANIFEST`.

Os três passeios da v0.13 continuam: `expected_schema_rules` em `check_fd_fx03_ack.py:1791`, `expected_occurrences` em `check_fd_fx03_ack.py:1849`, `stack_jobs` em `check_fd_fx03_ack.py:1962`. O terceiro não chama os dois primeiros. Eles ainda compartilham a DSL e `TYPE_WRONG`. Por isso a conta sozinha não fecha NEW-GOV-01.

O número 308 não é regra de mutação. É a quantidade de literais na referência semântica: tipo, const, `minLength`, `minItems`, `ref`, required, allowed, grupo e `same_length`.

## O que o autor observou

Python 3.10.22. `PYTHONDONTWRITEBYTECODE=1`. `python3 -B tools/check_fd_fx03_ack.py`. Exit 0. Stderr vazio. O transcript está em CMP-FD-12. Trecho:

```
COVERAGE_RULES declared=508 exercised=508 gap=0
COVERAGE_OCCURRENCES declared=2443 exercised=2443 gap=0
ID_MANIFEST rules=508 occurrences=2443 enumerated_outside_checker=true
SEMANTIC_BINDINGS count=308 digest=f642f0a1fa4b1a554dfa3ec96b32501e68154913d1a5192543efb24c864167ec ratification=PENDING_HUMAN_APPROVAL independence=NOT_RATIFIED new_gov_01=OPEN
FULL_PRODUCT_COVERAGE false
COVERAGE_TOTAL_PASS not_claimed
STATIC_ACK_V14_CHECK PASS_FIXTURE_ONLY
```

O banner final não é PASS do pacote. Se a política de um auditor impedir a execução, como ocorreu na v0.13, este transcript não substitui a reprodução. A lista de IDs fica no arquivo para leitura sem executar o gerador.
