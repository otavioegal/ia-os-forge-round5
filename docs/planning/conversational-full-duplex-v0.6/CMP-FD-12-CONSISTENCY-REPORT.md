# CMP-FD-12 v0.6 — Consistência

**Estado:** relato do autor. Não é PASS. Separa o que está escrito do que foi conferido em arquivo.

## Alegação documental, não executada

| Afirmação | Onde está escrita | Execução |
|---|---|---|
| `n = 0` tem código e não cai no vazio | CMP-FD-02:44 | oráculo O71 NOT RUN |
| High-water não diminui | CMP-FD-02:88 e CMP-FD-02:99-102 | oráculo O72 NOT RUN |
| Ack regressivo não escreve | CMP-FD-02:100 | oráculo O73 NOT RUN |
| `session_id` null aborta a migration inteira | CMP-FD-13:28 | oráculo O79 NOT RUN |
| Task de produto com null não entra no predicado | CMP-FD-13:51 | oráculo O80 NOT RUN |
| `task.status` fora do índice | CMP-FD-13:16 | não é teste |
| Half-duplex proibido | CMP-FD-02:7 | não é teste |
| Flag desligada | CMP-FD-13:16 | migration NOT RUN |

Os oráculos O71..O80 não foram executados. A tabela acima não é evidência deles.

## Checagem estática de fixture

Isto não executa o protocolo, não roda oráculo e não é teste de produto.

Comando: `python3 tools/check_fd_fx03_ack.py`

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
STATIC_ACK_MONOTONIC_CHECK PASS_FIXTURE_ONLY
```

`PASS_FIXTURE_ONLY` significa que o script e o JSON concordam nos números. Não é PASS do pacote. Não promove O71 nem O72 a executados.

Limite: o script aplica a tabela em processo local sobre os inteiros da fixture. Não há duas transações, não há `SELECT FOR UPDATE` e não há PostgreSQL. A serialização real continua NOT RUN.
