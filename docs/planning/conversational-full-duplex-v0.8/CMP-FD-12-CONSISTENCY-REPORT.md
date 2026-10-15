# CMP-FD-12 v0.8 — Consistência

**Estado:** relato do autor. Não é PASS. Separa o que está escrito do que foi conferido em arquivo.

## Alegação documental, não executada

| Afirmação | Onde está escrita | Execução |
|---|---|---|
| `n < 0` é `ACK_REGRESSION` antes do peer | CMP-FD-02:32 | O84 NOT RUN |
| Efeitos das linhas negativas são lidos | CMP-FD-02:47 | O85 NOT RUN |
| Só a chave alvo muda | CMP-FD-02:14-18 | O86 NOT RUN |
| Tenant errado é 404 sem lock | CMP-FD-02:28 | O87 NOT RUN |
| Replay não repete efeito | CMP-FD-02:33 e CMP-FD-02:72 | O89 NOT RUN |
| Crash desfaz a transação inteira | CMP-FD-02:70 | O91 NOT RUN |
| Duas transações reais terminam em 2 | CMP-FD-13:49-50 | O92 NOT RUN |
| v0.5/v0.6 não têm parecer incorporado | CMP-FD-14:5 | não é oráculo |
| HIGH-03 continua PARTIAL | CMP-FD-07:69 | não é fechamento |
| Flag desligada | CMP-FD-13:5 | migration NOT RUN |

O84..O95 não foram executados. A tabela acima não é evidência deles. O replay sequencial não é O92.

## Checagem estática da fixture

Isto não executa o protocolo, não roda oráculo, não abre PostgreSQL e não é teste de produto.

Comando, a partir de `docs/planning/conversational-full-duplex-v0.8/`:

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
COVERAGE fixture_rows_only explicit_NO_ACK=present both_SCOPE_MISMATCH_directions=present negative_sequence=present
ISOLATION static_map_only POSTGRESQL_RACE=NOT_RUN
MUTATION declared_fields=rejected foreign_key=rejected
STATIC_ACK_V08_CHECK PASS_FIXTURE_ONLY
```

`PASS_FIXTURE_ONLY` significa que o script e o JSON concordam. Não é PASS do pacote. Não promove O84 nem O92. Não fecha HIGH-03.

Limite: um processo local, um mapa em memória e mutação dos campos declarados. Não há duas sessões de banco, não há barreira e não há `pg_locks`.

## Checagem estática do manifest

Comando:

`python3 tools/check_fd_historical_manifest.py --root <clone somente leitura>`

Ambiente: Python 3.10.22. O clone não foi modificado.

Saída observada, exit 0:

```text
REHASHED 91 historical files
v0.5_parecer=ABSENT
v0.6_parecer=ABSENT
HISTORICAL_MANIFEST_MATCH READ_ONLY
```

`READ_ONLY` não é PASS. Confere SHA-256 dos arquivos históricos presentes no clone. Não audita o conteúdo normativo e não cria parecer de v0.5 ou v0.6.
