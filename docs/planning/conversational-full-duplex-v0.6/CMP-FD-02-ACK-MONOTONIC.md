# CMP-FD-02 v0.6 — ACK de sequence zero e high-water monotônico

**Estado:** PROPOSTA. CANDIDATE FOR CODEX REVIEW. Não é PASS. Não aprova `cmp.media.duplex.v1`.
**Achado alvo:** HIGH-03 ainda PARTIAL na v0.5. A v0.5 não é editada.
**O que esta página substitui:** só a decisão de ACK da v0.5 que deixava `ack_of_sequence = 0` sem resultado quando `peer_ack_high_water` também era 0, e a frase que aceitava o ack sem serializar a escrita.

Não há downgrade para half-duplex. O stream reconhecido não é inferido do `stream_id` do evento. O ack não liquida e não abre microfone.

## 1. O que não muda

Continuam vigentes, na v0.5, e não são reabertos aqui:

- `ack_stream_id` obrigatório se `ack_of_sequence` não é null, e null se o outro é null;
- scope lógico `{session_id, ack_stream_id, receiver_participant_id}`;
- `emitted_high_water` separado do peer high-water;
- `ACK_FUTURE`, `ACK_REGRESSION`, `ACK_DUPLICATE`, `ACK_STREAM_UNALLOCATED`, cross-stream válido;
- `PREAMBLE_AUTH` com zero efeito;
- seis carimbos e `PLAYBACK_SPAN`;
- `observation` sem `consent_stop_deadline_ns` e sem `observation_tolerance_ns`.

Sequences de evento continuam `>= 1`. O zero abaixo é só `ack_of_sequence`.

## 2. Sequence zero é inválido

`ack_of_sequence = 0` não é aceite, não é no-op e não é duplicata.

O peer high-water começa em 0 porque nenhum ack foi aceito. Zero não é uma sequence recebida. A tabela da v0.5 não cobria o par `(n = 0, peer = 0)`: a duplicata exigia `n > 0` e o aceite exigia `n > peer`. Esta página fecha esse buraco.

Código: `422 ACK_SEQUENCE_ZERO`. `retryable=false`. `terminal=true`.

Efeito: zero. Não cria linha de high-water. Não altera linha existente. Não abre sessão, stream, task nem microfone. Não move dinheiro. O mesmo código vale se o peer high-water já é maior que 0. Não se reclassifica como `ACK_REGRESSION`.

`n < 0` continua `422 ACK_REGRESSION`, também sem escrita.

## 3. Ordem fechada, primeiro casamento

`n` é `ack_of_sequence`. `S` é `ack_stream_id`. `R` é o `participant_id` autenticado. Não há linha seguinte se uma linha casou.

| # | Condição | Resultado | Escrita |
|---|---|---|---|
| 1 | exatamente um dos dois campos é null | `422 ACK_SCOPE_MISMATCH` | nenhuma |
| 2 | os dois são null | nenhum ack | nenhuma |
| 3 | `S` não é um dos três streams alocados nesta sessão e neste tenant | `422 ACK_STREAM_UNALLOCATED`, corpo opaco | nenhuma |
| 4 | `n = 0` | `422 ACK_SEQUENCE_ZERO` | nenhuma |
| 5 | `n < 0` | `422 ACK_REGRESSION` | nenhuma |
| 6 | daqui em diante a seção 4 trava as linhas e relê os inteiros |  |  |
| 7 | `n > emitted_high_water` de `S` | `422 ACK_FUTURE` | nenhuma |
| 8 | `n < peer_ack_high_water` do trio | `422 ACK_REGRESSION` | nenhuma |
| 9 | `n = peer_ack_high_water` | `ACK_DUPLICATE`, zero efeito novo | nenhuma |
| 10 | `peer < n <= emitted` | `ACK_ACCEPT` | uma, só para cima |

A janela `forge.media.window_unacked=32` não autoriza ack futuro. `CONTROL` pode reconhecer `INPUT` ou `OUTPUT`. A sequence do próprio evento não entra nessa conta.

## 4. Escrita atômica e monotônica

Linha proposta, não criada por esta pasta: `forge.media_peer_ack_high_water`.

| Coluna | Regra |
|---|---|
| organization_id, project_id | os do canal. Fazem parte da chave física. Não substituem o scope lógico |
| session_id, ack_stream_id, receiver_participant_id | o scope |
| peer_ack_high_water | int64 `>= 0`. Nasce 0 na inserção da linha. Não é sequence aceita |
| version | int64, sobe só quando o inteiro sobe |

Unique: `(organization_id, project_id, session_id, ack_stream_id, receiver_participant_id)`.

Invariante de toda escrita cometida: o inteiro novo é maior que o inteiro antigo. Nenhuma sentença faz `SET` para um valor menor.

Procedimento, na mesma transação, só se as linhas 1 a 5 da seção 3 não casaram:

1. Travar a linha de `emitted_high_water` de `(tenant, session_id, S)`.
2. Inserir a linha de peer com valor 0 se ela não existe. A unique serializa dois criadores. O perdedor relê. `n = 0` não chega aqui e não cria linha.
3. `SELECT ... FOR UPDATE` da linha de peer.
4. Ler `current` dessa linha e o `emitted` já travado. Não usar valor lido antes do lock.
5. Aplicar as linhas 7 a 10 com esses inteiros.
6. O único `UPDATE` é:

```sql
UPDATE forge.media_peer_ack_high_water
SET peer_ack_high_water = :n,
    version = version + 1
WHERE organization_id = :org
  AND project_id = :project
  AND session_id = :session
  AND ack_stream_id = :ack_stream
  AND receiver_participant_id = :receiver
  AND peer_ack_high_water = :current
  AND :n > peer_ack_high_water;
```

Se o `UPDATE` não afeta uma linha, a transação não escreve outro valor. Relê sob o mesmo lock. Se `n` agora é menor, `ACK_REGRESSION` sem escrita. Se igual, `ACK_DUPLICATE` sem escrita.

Ack regressivo não entra na fórmula `max`. `max(valor_atual, ack_aceito)` só descreve um aceite da linha 10, em que `ack_aceito` já é maior que o atual. Um `n` rejeitado não é `ack_aceito` e não é argumento desse max.

Dois ACKs do mesmo trio bloqueiam na mesma linha. O segundo lê o commit do primeiro. Com emitted `>= 2` e current inicial 0:

| Ordem que commita | Primeiro | Segundo | Valor final |
|---|---|---|---|
| `n=1` depois `n=2` | aceite, valor 1 | aceite, valor 2 | 2 |
| `n=2` depois `n=1` | aceite, valor 2 | `ACK_REGRESSION`, valor permanece 2 | 2 |

O final 1 depois de um 2 já cometido é resultado ilegal. `40001` aborta a transação do perdedor sem escrita parcial.

Outro tenant não é travado. A busca leva org e projeto do canal. UUID estrangeiro não seleciona a linha de lá.

## 5. Fixture

`fixtures/CMP-FD-FX-03-ack.json` traz sequence zero, zero depois de progresso, as duas ordens da corrida, regressão, duplicata, futuro, cross-stream, stream não alocado e par inválido.

`tools/check_fd_fx03_ack.py` confere esses números com a ordem da seção 3. Não executa o protocolo. Não é oráculo. Não é teste de produto.
