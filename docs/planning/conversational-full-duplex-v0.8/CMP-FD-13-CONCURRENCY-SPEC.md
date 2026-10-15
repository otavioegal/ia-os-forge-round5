# CMP-FD-13 v0.8 — Especificação futura de concorrência

**Nenhuma migration foi executada.** Nenhum PostgreSQL foi aberto. Não é PASS. Não é o replay sequencial da fixture.

A norma SQL continua a da v0.6, `CMP-FD-02-ACK-MONOTONIC.md` v0.6:65-102. Esta página não cria `forge.media_peer_ack_high_water`. A flag `forge.conversation.delta.v4` permanece desligada.

## 1. Escrita que a v0.6 já exigia

Unique física: `(organization_id, project_id, session_id, ack_stream_id, receiver_participant_id)`.

O passo 2 da v0.6 insere a linha com zero se ela não existe e a unique serializa dois criadores. A grafia desta pasta, não executada, é:

```sql
INSERT INTO forge.media_peer_ack_high_water (
  organization_id, project_id, session_id, ack_stream_id,
  receiver_participant_id, peer_ack_high_water, version
) VALUES (
  :org, :project, :session, :ack_stream, :receiver, 0, 0
)
ON CONFLICT (organization_id, project_id, session_id, ack_stream_id, receiver_participant_id)
DO NOTHING;
```

O perdedor relê. `n = 0` e `n < 0` não chegam aqui e não criam linha.

Em seguida, na mesma transação: `SELECT ... FOR UPDATE` da linha de peer, ler `current` e o `emitted` já travado, e o único `UPDATE` continua guardado por `:n > peer_ack_high_water`:

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

Zero linhas atualizadas: reler sob o mesmo lock. `n` menor vira `ACK_REGRESSION` sem escrita. `n` igual vira `ACK_DUPLICATE` sem escrita. Final 1 depois de um 2 já cometido é ilegal. `40001` aborta o perdedor sem escrita parcial, sem `command_commit` e sem outbox.

## 2. Teste futuro, NOT RUN

Dois backends PostgreSQL, a mesma chave, barreira real antes do commit. Não é lista em memória.

| Ordem que commita | Primeiro | Perdedor depois de reler | Final |
|---|---|---|---|
| `n=1` depois `n=2` | `ACK_ACCEPT`, valor 1 | `ACK_ACCEPT`, valor 2 | 2 |
| `n=2` depois `n=1` | `ACK_ACCEPT`, valor 2 | `ACK_REGRESSION`, valor 2 | 2 |
| o mesmo `n` já cometido | `ACK_ACCEPT` | `ACK_DUPLICATE`, valor intacto | o maior já cometido |

Proibido observar 2 e depois 1. O teste só pode ser marcado executado quando as duas ordens tiverem corrido com a barreira e o resultado tiver sido gravado fora desta pasta. Até lá: NOT RUN.

Segunda corrida, também NOT RUN: duas transações em trios distintos, por exemplo input do receiver A e output do receiver B. Não podem esperar a mesma linha. A observação prevista é `pg_locks` ou timeout que falharia se houvesse lock compartilhado. Não foi feita.

`FX03-RACE-1-THEN-2` e `FX03-RACE-2-THEN-1` permanecem replay sequencial. `concurrency=false`. Não substituem esta seção.

## 3. O que não entra

Não há `CREATE TABLE` nesta pasta. Não há `ALTER`. A opção B de `session_id`, fechada documentalmente pelo Codex na revisão da v0.7, continua em CMP-FD-13 da v0.6 e não é reescrita aqui. A migration dela continua NOT RUN.
