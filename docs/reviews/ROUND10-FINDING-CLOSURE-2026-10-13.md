# Fechamento da condição — Codex Round 9 para baseline v1.7
Estado da entrega: ROUND 10 — CANDIDATE FOR CODEX REVIEW.
Este registro não é o parecer do Codex. Não declara PASS. Nenhum teste de produto foi executado. Nenhuma aprovação foi inferida.
C-01 e os quatro HIGH fechados no parecer Round 9 não foram reabertos. A v1.6 permanece em `historical/round9/`.

| Campo | NEW-MEDIUM-12 |
|---|---|
| ID | NEW-MEDIUM-12 — late evidence e `pending_provider_cost` |
| Situação no parecer | A regra geral das linhas 461 e 463 da v1.6 exigia uma linha por receipt conclusivo em todo CONFLICT. As linhas 350 e 405 só mandavam inserir quando o movement anterior era RELEASE. Um SETTLEMENT de 30 seguido de um receipt de 40 ficava sem materialização. |
| Causa-raiz | O texto específico de late evidence era mais estreito que o schema. |
| Correção | FDP-16A v1.7. Qualquer entrada em CONFLICT com receipt conclusivo insere, de forma idempotente, uma linha `(operation_id, proof_id)`, reason CONFLICT, tenha o movement sido RELEASE ou SETTLEMENT. Não se inventa receipt para NO_EFFECT. As três trajetórias ficam explícitas: release e depois receipt 30; settlement 30 e depois receipt 40, com as duas linhas e projeção 40; settlement e depois no-effect, com a linha do receipt já conhecido. `spent` e `reserved` não mudam depois do movement. Não há segundo movement, nem `budget.settled`, nem `budget.released`, nem redispatch. A auditoria é um `budget.proof_conflict`. |
| Arquivo | docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md; matriz v1.7; F-015 |
| Evidência | Transição na linha 350. Regra e as três trajetórias nas linhas 405 a 411. A distinção entre conflito sem movement e conflito tardio está na linha 469. O schema, na linha 471, repete a mesma inserção depois do movement. LEDGER-18 está na linha 79 da matriz. LEDGER-17, linha 78, não foi reescrito: continua sendo a corrida antes de qualquer movement. |
| Estado neste builder | CORRIGIDO NESTA CANDIDATA. Não é fechamento do Codex. |

## O que permanece como o Codex deixou
C-01 permanece fechada. HIGH-01, NEW-HIGH-07, NEW-HIGH-08 e NEW-HIGH-09 permanecem fechados. A revalidação dos dois grants no Apply, a chave `(operation_id, proof_id)` e a projeção `max` não foram redesenhadas. FDP-18, FDP-18A e FDP-20 permanecem v1.3.
