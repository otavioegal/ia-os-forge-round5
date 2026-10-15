# CMP-FD-12 v0.7 — Consistência

**Estado:** relato do autor. Não é PASS. Separa o que está escrito do que foi conferido em arquivo.

## Alegação documental, não executada

| Afirmação | Onde está escrita | Execução |
|---|---|---|
| Os dois campos null são `NO_ACK`, não stream não alocado | CMP-FD-02:24 | oráculo O81 NOT RUN |
| Exatamente um campo null é `ACK_SCOPE_MISMATCH` nas duas direções | CMP-FD-02:23 e CMP-FD-02:36 | oráculos O82 e O83 NOT RUN |
| Essas três saídas não alteram high-water, não abrem microfone e não movem dinheiro | CMP-FD-02:34 e CMP-FD-02:53-55 | oráculos O81..O83 NOT RUN |
| O checker não percorre todos os eventos; `NO_ACK` é linha explícita | CMP-FD-02:11-13 | não é teste de produto |
| Ack regressivo não escreve e aceite só sobe | CMP-FD-02:42-44 | oráculos O72 e O73 NOT RUN |
| Sequence zero continua `ACK_SEQUENCE_ZERO` antes da comparação com o peer | CMP-FD-02:26 | oráculo O71 NOT RUN |
| HIGH-03 e NEW-MEDIUM-06 continuam CANDIDATE | CMP-FD-02:59 | não é fechamento |
| Flag desligada | CMP-FD-02:59 | migration NOT RUN |

O71..O83 não foram executados. A tabela acima não é evidência deles.

## Checagem estática de fixture

Isto não executa o protocolo, não roda oráculo e não é teste de produto.

Comando, a partir de `docs/planning/conversational-full-duplex-v0.7/`:

`python3 tools/check_fd_fx03_ack.py`

Ambiente: Python 3.10.22. Sem rede, sem banco, sem provider.

Saída observada, exit 0:

```text
OK FX03-ACK-ZERO ACK_SEQUENCE_ZERO after=0 write=False
OK FX03-ACK-ZERO-AFTER-PROGRESS ACK_SEQUENCE_ZERO after=2 write=False
OK FX03-RACE-1-THEN-2 final=2 steps=['ACK_ACCEPT', 'ACK_ACCEPT']
OK FX03-RACE-2-THEN-1 final=2 steps=['ACK_ACCEPT', 'ACK_REGRESSION']
OK FX03-REGRESSION ACK_REGRESSION after=2 write=False
OK FX03-DUPLICATE ACK_DUPLICATE after=2 write=False
OK FX03-FUTURE ACK_FUTURE after=0 write=False
OK FX03-CROSS-VALID ACK_ACCEPT after=2 write=True
OK FX03-UNALLOCATED ACK_STREAM_UNALLOCATED after=0 write=False
OK FX03-PAIR-INVALID ACK_SCOPE_MISMATCH after=0 write=False
OK FX03-NO-ACK NO_ACK after=2 write=False opens_mic=False zero_money=True high_water_unchanged=True
OK FX03-ACK-SCOPE-MISMATCH-SEQUENCE-ONLY ACK_SCOPE_MISMATCH after=2 write=False opens_mic=False zero_money=True high_water_unchanged=True
OK FX03-ACK-SCOPE-MISMATCH-STREAM-ONLY ACK_SCOPE_MISMATCH after=2 write=False opens_mic=False zero_money=True high_water_unchanged=True
COVERAGE fixture_rows_only explicit_NO_ACK=present both_SCOPE_MISMATCH_directions=present
STATIC_ACK_NULL_PAIR_CHECK PASS_FIXTURE_ONLY
```

`PASS_FIXTURE_ONLY` significa que o script e o JSON concordam nos códigos e nos inteiros. Não é PASS do pacote. Não promove O81, O82, O83, O71 nem O72 a executados. Não fecha HIGH-03.

Limite: o script aplica a tabela em processo local sobre as linhas da fixture. Não há duas transações, não há `SELECT FOR UPDATE` e não há PostgreSQL. A serialização real continua NOT RUN. Evento que não está na fixture não é classificado. A linha `FX03-NO-ACK` existe para o caso dos dois campos null não ficar implícito.
