# CMP-FD-12 v0.14 — Consistência

**Estado:** relato do autor. Não é auditoria independente. Não é PASS. `PASS_FIXTURE_ONLY` não é PASS do pacote. `PARECER_CHAIN NOT_FULLY_VERIFIED` não foi escondido.

## Ambiente

- Python 3.10.22 `(main, Oct  1 2026, 21:57:32) [GCC 12.2.0]`
- `PYTHONDONTWRITEBYTECODE=1`
- `python3 -B`
- O checker não escreve no checkout. Não houve `__pycache__` neste run.
- Stderr dos três comandos: vazio.

Comandos:

```
PYTHONDONTWRITEBYTECODE=1 python3 -B tools/check_fd_fx03_ack.py
PYTHONDONTWRITEBYTECODE=1 python3 -B tools/check_fd_historical_manifest.py
PYTHONDONTWRITEBYTECODE=1 python3 -B tools/check_fd_historical_manifest.py --repo <clone do parent 51d8ff2b89215470bbd6c8f99269301394d91083>
```

Exits observados pelo autor: 0, 2 e 0. Se a política read-only impedir o Python, como no parecer da v0.13, este texto não conta como reprodução. A lista de IDs e a referência ficam nos JSON para leitura.

## SHA-256 dos insumos, lidos do disco do autor

| Arquivo | SHA-256 |
|---|---|
| fixtures/CMP-FD-FX-03-ack.schema.json | `80a355d662190691e36ae54b0cf27925f39dceda264534992921644164d0a74a` |
| fixtures/CMP-FD-FX-03-ack.json | `215452c4afb14adcf9591fdd7bf45f886101a6a6878693007b2b4b6a02956838` |
| fixtures/CMP-FD-FX-03-ack.synthetic.json | `65364ea50025a2759ec50de4b9fd33337d7d3c3b1e7b61572ed2a4b63a242953` |
| fixtures/CMP-FD-FX-04-historical-manifest.json | `ff20f1df80f872b943e414930c8331be6c4e9a1d0f1f362ef99f600c8fe15ec0` |
| fixtures/CMP-FD-FX-05-semantic-reference.json | `0dc4bfae618bbbf8d08fad60cfcde494a76cf36670bf87005c8313afb87f6e14` |
| fixtures/CMP-FD-FX-06-unknown-keyword.json | `18b6f0eb2d663ff865387028c478895a0827614827b6f96a1b990357a7e14c19` |
| fixtures/CMP-FD-FX-07-coverage-ids.json | `7d01c7eb754ec20bac4a2c88fe92bc3d1341ba4e4f3b1a9f4edf0fb800da610f` |
| tools/check_fd_fx03_ack.py | `833708bfafbc0ea9e09d71f0ab216039eceb8eebafbcde3a432ec4ec4d795608` |
| tools/check_fd_historical_manifest.py | `afdeeeba3a8cbe0889f7a5609122893a442cca30e135c8c1f834c67afdc50f85` |
| tools/draft_semantic_reference.py | `887f4f98061352dcb5285f14a154d132de74da1a2987a5b9be42b26b18da2533` |
| tools/enumerate_coverage_ids.py | `0dcd1479cf2dd27e5b10115f0e80e1f50fdcffb62b8e65b04fd0e7eef1e99631` |

Estes hashes são do autor, anteriores ao commit. O Codex deve recalcular no SHA publicado. Se divergirem, o transcript abaixo não vale.

## Stdout do ACK, exit 0

```
CARDINALITY_STABLE const rules=508/508 occurrences=2443/2443 drift=document.schema.const
CARDINALITY_STABLE minItems rules=508/508 occurrences=2443/2443 drift=document.initial_keys.minItems
CARDINALITY_STABLE minLength rules=508/508 occurrences=2443/2443 drift=document.note.minLength
CARDINALITY_STABLE ref rules=508/508 occurrences=2443/2443 drift=step.counter_delta.ref host_validation=FAIL_SCHEMA
CARDINALITY_STABLE ref_compatible rules=521/521 occurrences=2443/2443 swap_delta_rules=0 swap_delta_occurrences=0 drift=step.counter_delta.ref host_validation=accepted alias_rules_above_508=13
CARDINALITY_STABLE required_optional rules=508/508 occurrences=2443/2443 drift=positive.expected_original_outcome_body.required
CARDINALITY_STABLE SAME_AUTHOR_BOTH_SIDES not_detected path=document.schema.const
SEMANTIC_BINDINGS count=308 digest=f642f0a1fa4b1a554dfa3ec96b32501e68154913d1a5192543efb24c864167ec ratification=PENDING_HUMAN_APPROVAL independence=NOT_RATIFIED new_gov_01=OPEN
ID_MANIFEST rules=508 occurrences=2443 enumerated_outside_checker=true
DSL_CLOSED unknown_keyword=rejected nullable_keyword=rejected json_schema_keywords=rejected
COERCION int_rejects_bool=true bool_rejects_int=true nullable_accepts_null=true
FULL_PRODUCT_COVERAGE false
COVERAGE_RULES declared=508 exercised=508 gap=0
COVERAGE_OCCURRENCES declared=2443 exercised=2443 gap=0
COVERAGE_CLASSES ABSENCE=146 CARDINALITY=9 CONST=29 ELEMENT_LIST=6 ELEMENT_MIN_LENGTH=1 ELEMENT_SCALAR=6 ELEMENT_TYPE=2 EMPTY=2 EXTRA=14 FORMAT=2 GROUP=3 INLINE_EXTRA=2 MAP=10 MIN_LENGTH=31 OCC_ABSENCE=1075 OCC_ELEMENT_LIST=28 OCC_ELEMENT_SCALAR=28 OCC_ELEMENT_TYPE=8 OCC_EMPTY=19 OCC_EXTRA=98 OCC_TYPE=1187 SAME_LENGTH=1 TYPE=180 UUID=64
RAW setup_scalar=16/16 setup_list=16/16 step_scalar=5/5 step_list=5/5 initial_scalar=7/7 initial_list=7/7 body_error_code_absence=4/4 body_opaque_type=3/3
COVERAGE_HOSTS behavioral_cases=26 synthetic_cases=4 synthetic_proves_product=false
COVERAGE_BASIS expected_walk=independent job_walk=iterative raw_slot_count=independent product_input_exhaustive=false
V12_CATALOG_REJECTED rules=480 occurrences=2239 reason=inline_objects_and_object_elements_omitted
COVERAGE_TOTAL_PASS not_claimed
DUPLICATE_KEY schema=rejected fixture=rejected synthetic=rejected manifest=rejected semantic=rejected unknown=rejected ids=rejected nested_fixture=rejected
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
STATIC_ACK_V14_CHECK PASS_FIXTURE_ONLY
```

## Stdout histórico sem `--repo`, exit 2

```
DUPLICATE_KEY manifest=rejected
GIT_BLOB_COMPARE NOT_RUN
PARECER_CHAIN NOT_RUN
```

## Stdout histórico com `--repo`, exit 0

```
REHASHED 193 paths at both commits
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
PARECER v0.13 sha=VERIFIED verdict=VERIFIED
PROMPT_SET MATCH
NEGATIVE sha=rejected verdict=rejected path=rejected omission=rejected invented_prompt=rejected invented_parecer=rejected nomenclature=rejected bytes=rejected
PLANNING_BLOBS MATCH READ_ONLY
BYTES MATCH
PARECER_CHAIN NOT_FULLY_VERIFIED
```

`PARECER v0.13 sha=VERIFIED verdict=VERIFIED` lê o blob. O cabeçalho daquele blob é PASS WITH CONDITIONS DOCUMENT-ONLY. Não é o veredito desta pasta. Esta pasta é CANDIDATE FOR CODEX REVIEW.

Nenhuma contradição foi fechada por este relato. v0.2 segue NOT_VERIFIED. Oráculos seguem NOT RUN. PostgreSQL segue NOT RUN. BUILD-00 segue bloqueado.
