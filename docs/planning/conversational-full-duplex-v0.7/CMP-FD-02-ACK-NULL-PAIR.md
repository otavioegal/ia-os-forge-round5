# CMP-FD-02 v0.7 — Par nulo do ACK

**Estado:** PROPOSTA. CANDIDATE FOR CODEX REVIEW. Não é PASS. Não aprova `cmp.media.duplex.v1`.
**Achado alvo:** o checker da v0.6 não implementa a linha 42 de CMP-FD-02 v0.6, e a fixture só tem uma direção de `ACK_SCOPE_MISMATCH`. A norma da v0.6 não muda. A v0.6 não é editada.
**O que esta página faz:** fixa o resultado estático dos dois campos null e das duas direções de um único campo null, antes de stream não alocado.

Não há downgrade para half-duplex. O modelo não lê o `stream_id` do evento. Ack não liquida e não abre microfone. A monotonicidade da v0.6 permanece: ack regressivo não escreve; aceite só sobe.

## 1. Cobertura

`tools/check_fd_fx03_ack.py` não percorre todos os eventos de uma sessão e não classifica evento ausente da fixture. Ele só avalia as linhas de `fixtures/CMP-FD-FX-03-ack.json`.

Essas linhas são casos de ACK mais a linha explícita `FX03-NO-ACK`. Os dois campos null não são um evento omitido e não são `ACK_STREAM_UNALLOCATED`. O resultado normativo é `NO_ACK`: nenhum ack, sem efeito.

## 2. Ordem, primeiro casamento

A ordem é a da v0.6, CMP-FD-02 linhas 41 a 50. Esta página não troca stream não alocado com zero, nem regressão com aceite.

`n` é `ack_of_sequence`. `S` é `ack_stream_id`. Não há linha seguinte se uma linha casou. O `stream_id` do envelope não entra na decisão.

| # | Condição | Resultado | Escrita |
|---|---|---|---|
| 1 | exatamente um dos dois campos é null | `422 ACK_SCOPE_MISMATCH` | nenhuma |
| 2 | os dois são null | `NO_ACK`. Não é 422. Não é stream não alocado | nenhuma |
| 3 | `S` não é um dos três streams alocados nesta sessão e neste tenant | `422 ACK_STREAM_UNALLOCATED`, corpo opaco | nenhuma |
| 4 | `n = 0` | `422 ACK_SEQUENCE_ZERO` | nenhuma |
| 5 | `n < 0` | `422 ACK_REGRESSION` | nenhuma |
| 6 | daqui a v0.6 trava e relê. O checker não trava: usa os inteiros da fixture como retrato depois do lock |  |  |
| 7 | `n > emitted_high_water` de `S` | `422 ACK_FUTURE` | nenhuma |
| 8 | `n < peer_ack_high_water` do trio | `422 ACK_REGRESSION` | nenhuma |
| 9 | `n = peer_ack_high_water` | `ACK_DUPLICATE`, zero efeito novo | nenhuma |
| 10 | `peer < n <= emitted` | `ACK_ACCEPT` | uma, só para cima |

`NO_ACK` não cria linha de high-water, não altera linha existente, não abre microfone e não move dinheiro. `ACK_SCOPE_MISMATCH` tem o mesmo efeito zero nas duas direções.

Sequence preenchida e stream null não herda o `stream_id` do evento, mesmo se esse `stream_id` estiver alocado. Sequence null e stream preenchido não vira `ACK_SEQUENCE_ZERO` nem `ACK_STREAM_UNALLOCATED`, mesmo se `S` estiver alocado.

## 3. Monotonicidade que continua obrigatória

Herdada da v0.6, seção 4. Não é relaxada aqui.

- `ACK_REGRESSION` devolve o inteiro atual e não escreve.
- `ACK_ACCEPT` só com `atual < n <= emitted`. O inteiro seguinte é `n`, maior que o atual.
- As ordens `n=1` depois `n=2` e `n=2` depois `n=1` terminam em 2. Na segunda, o segundo passo é `ACK_REGRESSION` e o valor não volta a 1.
- Nenhuma linha da fixture diminui o high-water.

O checker não executa `SELECT FOR UPDATE` nem o `UPDATE` com predicado `n > peer_ack_high_water`. Essa corrida real continua NOT RUN. O modelo só recusa, nos números da fixture, escrita para baixo e aceite que não suba.

## 4. Casos exigidos pelo checker

| case_id | Campos | Código | High-water | Microfone | Dinheiro |
|---|---|---|---|---|---|
| `FX03-NO-ACK` | os dois null | `NO_ACK` | igual ao anterior | fechado | zero |
| `FX03-ACK-SCOPE-MISMATCH-SEQUENCE-ONLY` | `n` preenchido, `S` null | `ACK_SCOPE_MISMATCH` | igual ao anterior | fechado | zero |
| `FX03-ACK-SCOPE-MISMATCH-STREAM-ONLY` | `n` null, `S` alocado | `ACK_SCOPE_MISMATCH` | igual ao anterior | fechado | zero |

`FX03-PAIR-INVALID` da v0.6 permanece, na forma sequence preenchida e stream null. Não substitui os três ids. O checker exige o conjunto exato dos casos da v0.6 mais estes três. Falta de um deles é falha da checagem estática, não um skip.

HIGH-03 e NEW-MEDIUM-06 não são fechados por esta página. LOW-01 não é tocado. `forge.conversation.delta.v4` permanece desligada. A v3 não é integrada.
