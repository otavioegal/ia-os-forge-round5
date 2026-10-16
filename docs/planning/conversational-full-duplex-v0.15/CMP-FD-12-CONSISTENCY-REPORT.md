# CMP-FD-12 v0.15 — Consistência

**Estado:** relato do autor. Não é auditoria independente. Não é PASS. Não é oráculo. `PASS_FIXTURE_ONLY` não é PASS do pacote. `PARECER_CHAIN NOT_FULLY_VERIFIED` não foi escondido. v0.2 não foi reclassificado.

## Ambiente

- Python 3.10.22 `(main, Oct  1 2026, 21:57:32) [GCC 12.2.0]`
- `PYTHONDONTWRITEBYTECODE=1`
- `python3 -B`
- Stderr vazio nos dois comandos do ACK e nos dois do histórico.
- Os dois clones de teste ficaram com `git status --short` vazio depois do checker.

O SHA publicado da v0.14, `2b2adf382b17a22f1372aaf05b7d3bd1a6ba14ba`, não contém esta correção e não foi reescrito. Os clones abaixo são checkouts desta pasta, não daquele commit. O SHA do GitHub desta pasta nasce na publicação e não é escrito neste relato. O checker não lê markdown. Os hashes LF da tabela identificam os arquivos que ele abre.

| Clone | core.autocrlf | Schema: CRLF | Schema: bytes | Exit | Banner |
|---|---|---:|---:|---:|---|
| `/tmp/v15-lf` | false | 0 | 25447 | 0 | `STATIC_ACK_V15_CHECK PASS_FIXTURE_ONLY` |
| `/tmp/v15-crlf` | true | 1128 | 26575 | 0 | o mesmo banner |

Os dois stdout têm 5484 bytes e são iguais. Os dois imprimem `COVERAGE_RULES declared=508 exercised=508 gap=0` e `COVERAGE_OCCURRENCES declared=2443 exercised=2443 gap=0`.

Comando, em cada clone, sem escrever no checkout:

```
PYTHONDONTWRITEBYTECODE=1 python3 -B tools/check_fd_fx03_ack.py
```

## Stdout idêntico dos dois clones, exit 0

```
CARDINALITY_STABLE const rules=508/508 occurrences=2443/2443 drift=document.schema.const
CARDINALITY_STABLE minItems rules=508/508 occurrences=2443/2443 drift=document.initial_keys.minItems
CARDINALITY_STABLE minLength rules=508/508 occurrences=2443/2443 drift=document.note.minLength
CARDINALITY_STABLE ref rules=508/508 occurrences=2443/2443 drift=step.counter_delta.ref host_validation=FAIL_SCHEMA
CARDINALITY_STABLE ref_compatible rules=521/521 occurrences=2443/2443 swap_delta_rules=0 swap_delta_occurrences=0 drift=step.counter_delta.ref host_validation=accepted alias_rules_above_508=13
CARDINALITY_STABLE required_optional rules=508/508 occurrences=2443/2443 drift=positive.expected_original_outcome_body.required
CARDINALITY_STABLE SAME_AUTHOR_BOTH_SIDES not_detected path=document.schema.const
SEMANTIC_BINDINGS count=308 digest=7bfa4c4624a8935e56d6de52894545fb82fe32c2749ca1d95573026ef1a59aa2 ratification=PENDING_HUMAN_APPROVAL independence=NOT_RATIFIED new_gov_01=OPEN
ID_MANIFEST rules=508 occurrences=2443 enumerated_outside_checker=true
DSL_CLOSED unknown_keyword=rejected nullable_keyword=rejected json_schema_keywords=rejected
COERCION int_rejects_bool=true bool_rejects_int=true nullable_accepts_null=true
CANONICAL_TEXT_SHA256 lf_crlf=equal raw_bytes_differ=true content_edit=detected git_blob_id=not_used
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
STATIC_ACK_V15_CHECK PASS_FIXTURE_ONLY
```

## Histórico

```
PYTHONDONTWRITEBYTECODE=1 python3 -B tools/check_fd_historical_manifest.py
```

Exit 2.

```
DUPLICATE_KEY manifest=rejected
GIT_BLOB_COMPARE NOT_RUN
PARECER_CHAIN NOT_RUN
```

```
PYTHONDONTWRITEBYTECODE=1 python3 -B tools/check_fd_historical_manifest.py --repo /tmp/repo
```

O `--repo` aponta um clone que contém `2b2adf382b17a22f1372aaf05b7d3bd1a6ba14ba`. Exit 0. `PARECER v0.2` permanece `verdict=NOT_VERIFIED`.

```
REHASHED 218 paths at both commits
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
PARECER v0.14 NOT_INCORPORATED
PROMPT_SET MATCH
NEGATIVE sha=rejected verdict=rejected path=rejected omission=rejected invented_prompt=rejected invented_parecer=rejected nomenclature=rejected bytes=rejected
PLANNING_BLOBS MATCH READ_ONLY
BYTES MATCH
PARECER_CHAIN NOT_FULLY_VERIFIED
```

## SHA-256 dos insumos textuais no disco LF do autor

Estes são hashes crus do arquivo LF, não o digest canônico e não o blob Git. O Codex deve recalcular no SHA publicado.

| Arquivo | SHA-256 |
|---|---|
| fixtures/CMP-FD-FX-03-ack.schema.json | `addbe8ccf59ee549646e69c1c79b76ac81f03273f497932ff75959847bb2706e` |
| fixtures/CMP-FD-FX-03-ack.json | `29decb258c3da98622e600f29a543279bcb2a12b2640123a2d2a26f17ce935b4` |
| fixtures/CMP-FD-FX-03-ack.synthetic.json | `e92aa0d083a596783b323208614ec832c8a47224280a943235f0a426222a18a5` |
| fixtures/CMP-FD-FX-04-historical-manifest.json | `0d121a99311800aa4d09a3228f2bc114d2fd33a469c5dd9f89a9bcbbd8479d5a` |
| fixtures/CMP-FD-FX-05-semantic-reference.json | `a10ed0e8f4a4d75da89b7653b9df5886db75838a46ac2fedd3e778a7446df2bf` |
| fixtures/CMP-FD-FX-06-unknown-keyword.json | `957eb62014a656772310036bda2f65b18702c0653843fcc61a0b2572ec9bc338` |
| fixtures/CMP-FD-FX-07-coverage-ids.json | `a860ccd8b1539716c70e1f1b5e83f3899bb9c2d0256b3567931dc1c14a4b62dc` |
| tools/canonical_json_text.py | `f931aca3aca0f491aba1f04a126aee8aaf2e95444db2d7e58096a20434bfecd3` |
| tools/check_fd_fx03_ack.py | `65de346c53c854f5f62e0f50ce129c3c9e35bc325c2db6e5d1f303d4cdf02a69` |
| tools/check_fd_historical_manifest.py | `306f878536728ff42386774349240b77424dffdac744611ced61bcad974c2ce2` |
| tools/draft_semantic_reference.py | `0bf6a52019bae32822417cea9f06b232d10f733f50a8db2220ee11be63938f5f` |
| tools/enumerate_coverage_ids.py | `a4488abc5bb9d6dc3fc56c5690c0d522a27b28dd8564ddb932c39cf81d2215b3` |

Nenhuma contradição foi fechada por este relato. Oráculos seguem NOT RUN. PostgreSQL segue NOT RUN. BUILD-00 segue bloqueado.
