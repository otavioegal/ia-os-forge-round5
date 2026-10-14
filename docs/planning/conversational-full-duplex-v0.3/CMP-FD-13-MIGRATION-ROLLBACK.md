# CMP-FD-13 v0.3 — Migração e rollback

**Estado:** ESPECIFICAÇÃO. Nenhuma migration foi executada. Nenhum banco foi contactado.
**Achado alvo:** a parte de rollback que deixou HIGH-01 parcial. Fechamento não declarado.

Rollback não apaga ledger. “Podem ser retirados” não é mais a regra. Cada passo tem pré-condição verificável. Se ela falha, o passo responde `ROLLBACK_BLOCKED` e para. Não há compensação criativa.

## 1. Ordem de ida

1. `build.kind` NOT NULL default `PRODUCT`.
2. Checks de status `SESSION_ACTIVE` e `SESSION_CLOSED` só com kind de root conversacional.
3. Colunas de task: `execution_domain` default `BUILD_DAG`, `session_id`, `session_status`, `session_slice_minor`. Status `SESSION_OPEN`, `SESSION_CLOSING`, `SESSION_CLOSED`, `SESSION_ORPHAN_HELD` só nesse domínio.
4. Unicidade de um root por `(organization_id, project_id)` e de uma task aberta por `session_id`.
5. FKs compostas: task `(organization_id, project_id, build_id)` → build `(organization_id, project_id, id)`; operation `(organization_id, project_id, task_id)` → task `(organization_id, project_id, id)`.
6. Valor de ator `conversation_router` só nos comandos deste delta. `InvokeCapability` continua recusando quem não é `coding_engine`.
7. Comandos novos no catálogo: `AuthorizeConversationalBudget`, `OpenConversationalAnchor`, `CloseConversationalAnchor`, `SweepOrphanConversationalAnchor`, `ReserveConversationalCapability`.
8. Tabela `forge.conversational_budget_authorization` sem colunas de dinheiro.
9. Flag `forge.conversation.delta.v2` nasce desligada. A proposta rejeitada da v0.2 não deve ser ligada sob o nome `forge.conversation.delta.v1`. Este documento não liga flag alguma. Ligar a flag não é BUILD-00 e não está autorizado.
10. Nada neste passo escreve movement, prova ou `pending_provider_cost`.

Linhas históricas nascem `PRODUCT` / `BUILD_DAG` sem rewrite.

## 2. Volta de cada passo

A volta é o reverso, e só se a pré-condição vale. Consultas abaixo são especificação, não foram rodadas.

| Passo | Pré-condição para desfazer | Ação | Bloqueio |
|---|---|---|---|
| 10 | sempre, porque nada foi escrito | nenhuma | |
| 9 | flag ainda desligada, ou um humano a desliga antes sem apagar dado | desligar a flag | flag ligada com reserva não terminal: não desfazer o resto |
| 8 | zero build com `authorization_id` preenchido | drop da tabela | qualquer referência: `ROLLBACK_BLOCKED` |
| 7 | zero linhas de outbox ou audit cujo `command_type` seja um comando novo | remover do catálogo **executável** | se existe outbox, o tipo continua reconhecido como histórico e recusado para execução nova. Não se apaga a linha |
| 6 | zero envelope, audit ou outbox com `actor_class=conversation_router` | retirar o valor do check | senão `ROLLBACK_BLOCKED` |
| 5 | nenhum writer do delta ativo | drop das FKs compostas | se ainda há task conversacional, `ROLLBACK_BLOCKED`. Drop de FK não é desculpa para apagar operation |
| 4 | zero task de sessão e zero root | drop dos índices | senão bloqueado |
| 3 | zero task com `execution_domain<>BUILD_DAG`, inclusive `SESSION_CLOSED` e `SESSION_ORPHAN_HELD` | drop das colunas e dos status | uma linha `SESSION_CLOSED` bloqueia. Não mapear esse status para `CANCELLED`: seria mentira de produto |
| 2 | zero build em `SESSION_ACTIVE` ou `SESSION_CLOSED` | retirar os valores do check | o mesmo bloqueio |
| 1 | zero build com `kind<>PRODUCT` | drop de `kind` | senão bloqueado |

Presença de `SESSION_CLOSED` bloqueia a retirada do enum. Consumidor rebaixado não converte esse valor em status de produto. Falha fechado ao ler a linha.

## 3. Rollback parcial

Se os passos 1..K estão aplicados e K+1 não:

- Desfazer de K para 1, cada um com a sua pré-condição.
- Parar no primeiro `ROLLBACK_BLOCKED`.
- Não pular um passo do meio.
- Passo cuja pré-condição falha por existência de ledger não é “forçado”.

Exemplo: passos 1–8 aplicados, existe Operation `DISPATCHED` numa task de sessão. Os passos 8, 7, 6, 5, 4 e 3 bloqueiam. Audit e outbox ficam. O teto e as reservations ficam. Não há meio-rollback que deixe Operation sem task.

## 4. O que nunca se apaga

`operation`, `reservation`, `operation_money_movement`, `ProviderEffectProof`, `pending_provider_cost`, outbox e audit. Qualquer compensação que exigisse `DELETE` nessas tabelas é `ROLLBACK_BLOCKED_LEDGER`.

Prova não muda de `verification_state` por causa de rollback de schema. Reconciliação HELD continua HELD. Não se inventa `NO_EFFECT` para “limpar” e poder dropar coluna.

## 5. Downgrade de consumidor

1. Parar writers dos comandos novos. A flag fica desligada.
2. Esperar não haver transação de reserva aberta. Especificação de espera, não um drill executado.
3. Se existe operation `DISPATCHED`, `RECONCILING` ou `BLOCKED_RECONCILIATION` no root: rollback total bloqueado.
4. Consumidor que não entende `SESSION_ACTIVE`, `SESSION_CLOSED` ou `conversation_router` rejeita a linha ou o evento. Não coage para `RUNNING` nem para `coding_engine`.
5. Evento desconhecido vai para dead-letter **sem** ser marcado como efeito de negócio aplicado. A linha de outbox permanece para um leitor que conheça o delta.
6. Rebaixar não é autorização para gastar, nem para soltar reservation.

## 6. Relação com a v0.2

A migração da v0.2, que criaria um Build `CONVERSATIONAL_ANCHOR` por sessão, não deve ser aplicada. Se alguma linha dessa forma existir fora deste repositório, esta especificação não a adota e não a apaga: um operador humano teria de tratá-la em gate separado. Neste repositório essa forma nunca foi migrada, porque nenhuma migration rodou.
