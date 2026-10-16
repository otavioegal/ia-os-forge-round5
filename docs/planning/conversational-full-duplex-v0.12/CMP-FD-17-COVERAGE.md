# CMP-FD-17 v0.12 — Cobertura quantitativa

**Estado:** relato do autor sobre o checker local. Não é PASS. Não é oráculo. `gap=0` não fecha FD11-NEW-01 nem NEW-LOW-03.

## O que está declarado

1. Regra de schema: para cada objeto e cada campo, tipo; ausência se o campo é obrigatório; UUID se o tipo é UUID; const; `minLength`; cardinalidade de lista; tipo do elemento escalar; extra por objeto; grupo parcial; `same_length`; variantes de `uuid_map`.
2. Ocorrência: cada caso do host, cada campo presente, cada obrigatório removido, cada índice de `setup`, `steps`, `commit_order` e `expected_steps`, cada `attempt` de rollback, `replay`, `fresh` e `probe`, e cada `initial_key`.

O host é a fixture de 26 linhas mais quatro casos sintéticos. Os sintéticos não passam pelo ACK semântico.

## O que o autor observou

```
COVERAGE_RULES declared=480 exercised=480 gap=0
COVERAGE_RULE_CLASSES ABSENCE=144 CARDINALITY=9 CONST=29 ELEMENT_MIN_LENGTH=1 ELEMENT_TYPE=2 EMPTY=2 EXTRA=14 FORMAT=2 GROUP=3 MAP=10 MIN_LENGTH=29 SAME_LENGTH=1 TYPE=170 UUID=64
COVERAGE_OCCURRENCES declared=2239 exercised=2239 gap=0
COVERAGE_OCCURRENCE_CLASSES OCC_ABSENCE=1057 OCC_EMPTY=17 OCC_TYPE=1165
STRUCT removed_setup_absence=30 removed_replay_absence=18 removed_fresh_absence=18 cross_setup_absence=30 cross_probe_absence=18 rollback_attempt_absence=9 interleave_step_absence=75 interleave_counter_absence=30 sequential_element_type=8 sequential_empty=4 case_required_absence=548 case_present_field_type=648 initial_key_absence=49 max_setup=2 max_steps=5 max_commit=2
COVERAGE_SCOPE schema_rules=all_declared occurrences=all_hosts_not_first_kind product_input_exhaustive=false
```

`removed_setup_absence=30` é 3 itens de `setup` vezes 10 obrigatórios: o caso comportamental de tamanho 1 e o sintético de tamanho 2. `interleave_step_absence=75` é 5 steps vezes 15 obrigatórios. `sequential_element_type=8` é dois casos vezes quatro elementos. `max_setup=2`, `max_steps=5`, `max_commit=2`. Se o gerador voltasse a usar só o índice zero, essa conta independente falharia em `check_fd_fx03_ack.py:1442`.

## O que não está declarado e portanto não é PASS

Não é exaustivo sobre todo JSON. Não executa PostgreSQL. Não prova O92. Uma lacuna imprime `COVERAGE_GAP` e devolve `FAIL_COVERAGE_GAP` em `check_fd_fx03_ack.py:1652` ou `check_fd_fx03_ack.py:1661`. O processo não segue para um PASS global.
