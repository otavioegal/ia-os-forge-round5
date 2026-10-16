# CMP-FD-12 v0.13 — Consistência

**Estado:** relato do autor. Não é PASS. Não é auditoria independente. `PASS_FIXTURE_ONLY` e `gap=0` não são PASS do pacote. `COVERAGE_TOTAL_PASS` não é reivindicado. `BYTES MATCH` não foi reproduzido pelo Codex; a corrida abaixo é do autor, somente leitura, Python 3.10.22.

480 regras e 2239 ocorrências são o catálogo incompleto da v0.12. O parecer as recusou porque objetos inline e elementos de array de objeto ficaram de fora. Esta página não as usa como prova. O checker as imprime só na linha `V12_CATALOG_REJECTED`.

## Checker de ACK

Comando local: `python3 tools/check_fd_fx03_ack.py`. Exit 0. O fim é `STATIC_ACK_V13_CHECK PASS_FIXTURE_ONLY`. Isso não executa oráculo.

```
COVERAGE_RULES declared=508 exercised=508 gap=0
COVERAGE_OCCURRENCES declared=2443 exercised=2443 gap=0
COVERAGE_CLASSES ABSENCE=146 CARDINALITY=9 CONST=29 ELEMENT_LIST=6 ELEMENT_MIN_LENGTH=1 ELEMENT_SCALAR=6 ELEMENT_TYPE=2 EMPTY=2 EXTRA=14 FORMAT=2 GROUP=3 INLINE_EXTRA=2 MAP=10 MIN_LENGTH=31 OCC_ABSENCE=1075 OCC_ELEMENT_LIST=28 OCC_ELEMENT_SCALAR=28 OCC_ELEMENT_TYPE=8 OCC_EMPTY=19 OCC_EXTRA=98 OCC_TYPE=1187 SAME_LENGTH=1 TYPE=180 UUID=64
RAW setup_scalar=16/16 setup_list=16/16 step_scalar=5/5 step_list=5/5 initial_scalar=7/7 initial_list=7/7 body_error_code_absence=4/4 body_opaque_type=3/3
COVERAGE_HOSTS behavioral_cases=26 synthetic_cases=4 synthetic_proves_product=false
COVERAGE_BASIS expected_walk=independent job_walk=iterative raw_slot_count=independent product_input_exhaustive=false
V12_CATALOG_REJECTED rules=480 occurrences=2239 reason=inline_objects_and_object_elements_omitted
COVERAGE_TOTAL_PASS not_claimed
DUPLICATE_KEY schema=rejected fixture=rejected synthetic=rejected manifest=rejected nested_fixture=rejected
COVERAGE_SYNTHETIC oracle_status=NOT_RUN
ORACLE_EXECUTION NOT_RUN
POSTGRESQL NOT_RUN
COVERAGE_GAP count=0
OK FX03-ACK-ZERO ACK_SEQUENCE_ZERO stage=zero after=0 write=False opens_mic=False zero_money=True
OK FX03-ACK-ZERO-AFTER-PROGRESS ACK_SEQUENCE_ZERO stage=zero after=2 write=False opens_mic=False zero_money=True
OK FX03-RACE-1-THEN-2 sequential_not_concurrency final=2
OK FX03-RACE-2-THEN-1 sequential_not_concurrency final=2
OK FX03-REGRESSION ACK_REGRESSION stage=regression after=2 write=False opens_mic=False zero_money=True
OK FX03-DUPLICATE ACK_DUPLICATE stage=duplicate after=2 write=False opens_mic=False zero_money=True
OK FX03-FUTURE ACK_FUTURE stage=future after=0 write=False opens_mic=False zero_money=True
OK FX03-CROSS-VALID ACK_ACCEPT stage=accept after=2 write=True opens_mic=False zero_money=True
OK FX03-UNALLOCATED ACK_STREAM_UNALLOCATED stage=unallocated after=0 write=False opens_mic=False zero_money=True
OK FX03-PAIR-INVALID ACK_SCOPE_MISMATCH stage=pair after=0 write=False opens_mic=False zero_money=True
OK FX03-NO-ACK NO_ACK stage=pair after=0 write=False opens_mic=False zero_money=True
OK FX03-ACK-SCOPE-MISMATCH-SEQUENCE-ONLY ACK_SCOPE_MISMATCH stage=pair after=0 write=False opens_mic=False zero_money=True
OK FX03-ACK-SCOPE-MISMATCH-STREAM-ONLY ACK_SCOPE_MISMATCH stage=pair after=0 write=False opens_mic=False zero_money=True
OK FX03-NEGATIVE-SEQUENCE ACK_REGRESSION stage=negative after=2 write=False opens_mic=False zero_money=True
OK FX03-ISOLATION-INTERLEAVE keys_isolated=true foreign_mutation=detected
OK FX03-WRONG-TENANT NOT_FOUND stage=tenant after=0 write=False opens_mic=False zero_money=True
OK FX03-WRONG-RECEIVER NOT_FOUND stage=receiver after=0 write=False opens_mic=False zero_money=True
OK FX03-REPLAY-SAME-COMMAND IDEMPOTENT_REPLAY stage=replay after=2 write=False opens_mic=False zero_money=True
OK FX03-REPLAY-DISTINCT-COMMAND ACK_DUPLICATE stage=duplicate after=2 write=False opens_mic=False zero_money=True
OK FX03-REPLAY-KEY-REUSED IDEMPOTENCY_KEY_REUSED stage=reused after=2 write=False opens_mic=False zero_money=True
OK FX03-EVENT-DEDUPE EVENT_DEDUPE stage=event after=1 write=False opens_mic=False zero_money=True
OK FX03-ROLLBACK-BEFORE-COMMIT rollback_model oracle=NOT_RUN
OK FX03-REPLAY-ORIGINAL-422 IDEMPOTENT_REPLAY stage=replay after=0 write=False opens_mic=False zero_money=True
OK FX03-REPLAY-DIGEST-DISTINCT IDEMPOTENCY_KEY_REUSED stage=reused after=0 write=False opens_mic=False zero_money=True
OK FX03-REPLAY-RECEIVER-REMOVED replay_keeps_422 transport=200 fresh_receiver=NOT_FOUND
OK FX03-REPLAY-CROSS-TENANT tenant_lookup_blocked
COVERAGE fixture_rows_only explicit_NO_ACK=present both_SCOPE_MISMATCH_directions=present negative_sequence=present
ISOLATION static_map_only POSTGRESQL_RACE=NOT_RUN
MUTATION declared_fields=rejected before=rejected stage=rejected foreign_key=rejected extra_key=rejected
REPLAY original_outcome_separated_from_transport
SCHEMA required_and_types=enforced missing=FAIL_SCHEMA
PROVES_PRODUCT false
STATIC_ACK_V13_CHECK PASS_FIXTURE_ONLY
```

O numerador e o denominador não saem do mesmo gerador. O esperado vem de `expected_schema_rules` e `expected_occurrences`. O exercido vem de `stack_jobs`. `raw_slots` é uma terceira conta. Se qualquer um divergir, o código é `FAIL_COVERAGE_GAP`. 508 e 2443 são o que este turno imprimiu sobre esta fixture. Não são exaustão de JSON de produto.

## Checker histórico com repositório

Comando local: `python3 tools/check_fd_historical_manifest.py --repo <clone somente leitura>`. Exit 0. A última linha é `PARECER_CHAIN NOT_FULLY_VERIFIED`. v0.2 permanece `verdict=NOT_VERIFIED`. v0.12 está `sha=VERIFIED` e `verdict=VERIFIED` porque o parecer está no parent e não na base.

```
REHASHED 174 paths at both commits
v0.1_included=YES
PARECER v0.1 sha=VERIFIED verdict=VERIFIED
PARECER v0.2 sha=VERIFIED verdict=NOT_VERIFIED
PARECER v0.3 sha=VERIFIED verdict=VERIFIED
PARECER v0.4 sha=VERIFIED verdict=VERIFIED
PARECER v0.5 ABSENT_LEGITIMATE
PARECER v0.6 ABSENT_LEGITIMATE
PARECER v0.7 sha=VERIFIED verdict=VERIFIED
PARECER v0.8 sha=VERIFIED verdict=VERIFIED
PARECER v0.9 sha=VERIFIED verdict=VERIFIED
PARECER v0.10 sha=VERIFIED verdict=VERIFIED
PARECER v0.11 sha=VERIFIED verdict=VERIFIED
PARECER v0.12 sha=VERIFIED verdict=VERIFIED
PROMPT_SET MATCH
NEGATIVE sha=rejected verdict=rejected path=rejected omission=rejected invented_prompt=rejected invented_parecer=rejected nomenclature=rejected bytes=rejected
PLANNING_BLOBS MATCH READ_ONLY
BYTES MATCH
PARECER_CHAIN NOT_FULLY_VERIFIED
```

174 é 155 paths anteriores mais os 19 arquivos da v0.12. O commit de review não altera a árvore de planejamento, então base e parent coincidem nesses paths. Isso é leitura do autor. Não é auditoria independente.

## Checker histórico sem repositório

Exit 2. Não é sucesso. A chave duplicada é rejeitada mesmo sem o clone.

```
DUPLICATE_KEY manifest=rejected
GIT_BLOB_COMPARE NOT_RUN
PARECER_CHAIN NOT_RUN
```

## Separação

| Afirmação | O que ela é |
|---|---|
| 508 regras e 2443 ocorrências | Saída deste turno do checker local. `PASS_FIXTURE_ONLY` |
| 480 e 2239 | Catálogo incompleto da v0.12. Rejeitado. Não é esta cobertura |
| `product_input_exhaustive=false` | Limite explícito. Não autoriza pular regra que está no schema |
| `COVERAGE_TOTAL_PASS not_claimed` | O autor não alega cobertura total |
| `BYTES MATCH` | Relato autoral READ_ONLY. Não é parecer |
| `PARECER_CHAIN NOT_FULLY_VERIFIED` | Estado correto enquanto o v0.2 não tiver ato humano |
| Oráculos, O92, O93, O96–O99 | NOT RUN |
| LOW-01 | OPEN BLOCKING DoR. Pessoa PENDING. Effort UNSTATED |
| FD12-NEW-01, FD12-NEW-02, FD12-NEW-03 | CANDIDATE. Esta página não os fecha |
