# CMP-FD-12 v0.10 — Consistência

**Estado:** relato do autor. Não é PASS. Separa o que está escrito do que foi conferido em arquivo.

## Alegação documental, não executada

| Afirmação | Onde está escrita | Execução |
|---|---|---|
| Replay devolve o 422 original em transporte 200 | CMP-FD-02 | O96 NOT RUN |
| Dois backends terminam em 2 | CMP-FD-13 | O92 NOT RUN |
| O veredito do v0.2 não é único | CMP-FD-14 | leitura de blob, não oráculo |
| Campo obrigatório ausente é FAIL_SCHEMA | CMP-FD-15 | checagem estática, não produto |
| HIGH-03 continua PARTIAL | CMP-FD-02 | não é fechamento |
| Flag desligada | CMP-FD-13 | migration NOT RUN |

O84..O99 não foram executados. A tabela acima não é evidência deles. O replay sequencial não é O92.

## Checagem estática da fixture

Isto não executa o protocolo, não roda oráculo, não abre PostgreSQL e não prova produto. `proves_product` é false.

Comando, a partir de `docs/planning/conversational-full-duplex-v0.10/`:

`python3 tools/check_fd_fx03_ack.py`

Ambiente: Python 3.10.22. Sem rede, sem banco, sem provider.

Saída observada, exit 0:

```text
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
SCHEMA required_fields=enforced missing=FAIL_SCHEMA
PROVES_PRODUCT false
STATIC_ACK_V10_CHECK PASS_FIXTURE_ONLY
```

`PASS_FIXTURE_ONLY` significa que o script, o schema e o JSON concordam. Não é PASS do pacote. Não promove O96 nem O92. Não fecha HIGH-03, NEW-MEDIUM-09 nem NEW-LOW-02.

Limite: um processo local e um mapa em memória. Não há duas sessões de banco, não há barreira e não há `pg_locks`.

## Checagem dos dois commits

Sem repositório o checker não abre blob nenhum:

`python3 tools/check_fd_historical_manifest.py`

Saída observada, exit 2:

```text
GIT_BLOB_COMPARE NOT_RUN
PARECER_CHAIN NOT_RUN
```

Com clone somente leitura:

`python3 tools/check_fd_historical_manifest.py --repo <clone>`

Ambiente: Python 3.10.22. O clone não foi modificado. O comando lê `git ls-tree` e `git cat-file` em `422277f82efbc001140b5857095c4840e668e270` e em `311e2cf76db6fb2294745b9415f1ae829c883fa7`.

Saída observada, exit 0:

```text
REHASHED 122 paths at both commits
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
PROMPT_SET MATCH
NEGATIVE sha=rejected verdict=rejected path=rejected omission=rejected invented_prompt=rejected invented_parecer=rejected nomenclature=rejected
PLANNING_BLOBS MATCH READ_ONLY
PARECER_CHAIN NOT_FULLY_VERIFIED
```

`READ_ONLY` e `NOT_FULLY_VERIFIED` não são PASS. Os 122 paths de planejamento conferem, inclusive o v0.1 e a v0.9. O veredito do parecer v0.2 permanece NOT_VERIFIED. Isso não cria parecer de v0.5 ou v0.6 e não audita o produto.
