# CMP-FD-13 v0.4 — Migração e rollback

**Especificação. Nenhuma migration foi executada.** Não é PASS.

A v0.3 já exigia pré-condição por passo e proibia apagar ledger, prova, outbox e audit. Isso continua. Os passos abaixo são adicionais do delta v3. Não aplicar o delta v2 como se esta página o autorizasse.

## Ida

1. Colunas `reservation.organization_id` e `reservation.project_id`, NOT NULL nas linhas novas, copiadas da Operation na mesma transação.
2. FK `(organization_id, project_id, operation_id)` da Reservation para a Operation.
3. Índice único parcial `(organization_id, project_id, session_id)` onde o status da task está em `OPEN`, `CLOSING`, `ORPHAN_HELD`. Não criar índice único só em `session_id`.
4. Tabela `forge.command_commit` com unicidade `(organization_id, project_id, command_id)`.
5. Valor `SESSION_SLICE` na razão de `pending_provider_cost`, só para task conversacional. `OVER_ESTIMATE` e `CONFLICT` continuam.
6. Flag `forge.conversation.delta.v3` nasce desligada. Esta página não a liga.

Linha antiga de Reservation, se um dia existir sem as colunas, não é reescrita por este texto: a migration real está proibida aqui. O desenho exige que nenhuma Reservation conversacional seja inserida sem o par org/projeto.

## Volta

| Passo | Pode desfazer se | Bloqueio |
|---|---|---|
| 6 | a flag segue desligada | flag ligada com operation não terminal |
| 5 | zero linhas com razão `SESSION_SLICE` | qualquer linha dessa razão: `ROLLBACK_BLOCKED` |
| 4 | zero linhas em `command_commit` | senão as linhas ficam; a tabela não é dropada |
| 3 | zero task conversacional aberta | senão `ROLLBACK_BLOCKED` |
| 2 | nenhum writer do delta ativo e zero reservation conversacional | FK não sai se ainda aponta para operation com movimento |
| 1 | zero reservation com as colunas preenchidas por este delta | não apagar a reservation |

`SESSION_CLOSED`, movement, prova, pending, outbox, audit e `command_commit` cometido não são apagados. Consumidor que não entende `SESSION_SLICE` falha fechado. Não coage para `OVER_ESTIMATE` e não liquida.

Rollback parcial para no primeiro bloqueio. Não há compensação que delete ledger para “limpar” o passo.
