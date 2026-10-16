# CMP-FD-12 v0.12 — Consistência

**Estado:** relato do autor. Não é PASS. Não é auditoria independente. `PASS_FIXTURE_ONLY` e `gap=0` não são PASS do pacote. `BYTES MATCH` não foi reproduzido pelo Codex; a corrida abaixo é do autor, somente leitura.

## Checker de ACK

Comando local: `python3 tools/check_fd_fx03_ack.py`. Exit 0. O fim é `STATIC_ACK_V12_CHECK PASS_FIXTURE_ONLY`. Isso não executa oráculo.

```
COVERAGE_RULES declared=480 exercised=480 gap=0
COVERAGE_RULE_CLASSES ABSENCE=144 CARDINALITY=9 CONST=29 ELEMENT_MIN_LENGTH=1 ELEMENT_TYPE=2 EMPTY=2 EXTRA=14 FORMAT=2 GROUP=3 MAP=10 MIN_LENGTH=29 SAME_LENGTH=1 TYPE=170 UUID=64
COVERAGE_OCCURRENCES declared=2239 exercised=2239 gap=0
COVERAGE_OCCURRENCE_CLASSES OCC_ABSENCE=1057 OCC_EMPTY=17 OCC_TYPE=1165
STRUCT removed_setup_absence=30 removed_replay_absence=18 removed_fresh_absence=18 cross_setup_absence=30 cross_probe_absence=18 rollback_attempt_absence=9 interleave_step_absence=75 interleave_counter_absence=30 sequential_element_type=8 sequential_empty=4 case_required_absence=548 case_present_field_type=648 initial_key_absence=49 max_setup=2 max_steps=5 max_commit=2
COVERAGE_HOSTS behavioral_cases=26 synthetic_cases=4 synthetic_proves_product=false
COVERAGE_SCOPE schema_rules=all_declared occurrences=all_hosts_not_first_kind product_input_exhaustive=false
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
STATIC_ACK_V12_CHECK PASS_FIXTURE_ONLY
```

## Checker histórico com repositório

Comando local: `python3 tools/check_fd_historical_manifest.py --repo <clone>`. Exit 0. A última linha é `PARECER_CHAIN NOT_FULLY_VERIFIED`. v0.2 permanece `verdict=NOT_VERIFIED`.

```
REHASHED 155 paths at both commits
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
PROMPT_SET MATCH
NEGATIVE sha=rejected verdict=rejected path=rejected omission=rejected invented_prompt=rejected invented_parecer=rejected nomenclature=rejected bytes=rejected
PLANNING_BLOBS MATCH READ_ONLY
BYTES MATCH
PARECER_CHAIN NOT_FULLY_VERIFIED
```

## Checker histórico sem repositório

Exit 2. Não é sucesso.

```
GIT_BLOB_COMPARE NOT_RUN
PARECER_CHAIN NOT_RUN
```

## Separação

| Afirmação | O que ela é |
|---|---|
| 480 regras e 2239 ocorrências | Saída deste turno do checker local |
| `product_input_exhaustive=false` | Limite explícito. Não é exaustão de produto |
| `BYTES MATCH` | Relato autoral READ_ONLY. Não é parecer |
| `PARECER_CHAIN NOT_FULLY_VERIFIED` | Estado correto enquanto o v0.2 não tiver ato humano |
| Oráculos, O92, O93, O96–O99 | NOT RUN |
| LOW-01 | OPEN BLOCKING DoR. Pessoa PENDING. Effort UNSTATED |
