# Fechamento das condições — Codex Round 8 para baseline v1.6
Estado da entrega: ROUND 9 — CANDIDATE FOR CODEX REVIEW.
Este registro não é o parecer do Codex. Não declara PASS. Nenhum teste de produto foi executado. Nenhuma aprovação foi inferida.
Os quatro HIGH que o Codex fechou no Round 8 não foram reabertos. A v1.5 permanece em `historical/round8/`.

| Campo | C-01 / NEW-MEDIUM-10 |
|---|---|
| ID | C-01 — confirmação, replay e revogação |
| Situação no parecer | PARCIALMENTE FECHADO. LEDGER-14 cobria Approve e Apply. Não havia Confirm, nem revogação do aprovador ou do confirmador antes do Apply. A frase do Apply não dizia se os dois grants continuavam obrigatórios. |
| Causa-raiz | "the human capability used to authorize is still present" podia ser lida como um único grant histórico. |
| Correção | FDP-16A v1.6. No Apply de PROVEN_RECEIPT, o Policy Service relê `ledger.reconcile` de `requested_by` e de `confirmed_by`. No PROVEN_NO_EFFECT, relê só `requested_by`. A aprovação anterior não substitui essa leitura. Apply é comando de system: não reconfere frescor de sessão, porque isso já ocorreu no Approve e no Confirm. Se o grant exigido falta, o resultado é 403 CAPABILITY_REVOKED, a autorização fica AUTHORIZED e não consumida, a reserva fica HELD, `spent` não muda e não há movement nem `budget.settled` nem `budget.released`. O mesmo `command_id` nessa recusa não é 200 IDEMPOTENT_REPLAY. Confirm repetido no mesmo `command_id` é 200 IDEMPOTENT_REPLAY e não acrescenta outro `budget.manual_reconciliation`. Confirm com `command_id` novo depois de AUTHORIZED é 409 ALREADY_CONFIRMED, não altera coluna e não grava evento. |
| Arquivo | docs/planning/FDP-16A-v1.6-EXECUTION-CONTRACTS.md; matriz v1.6; F-015 |
| Evidência | Catálogo do Apply na linha 209. Regra dos dois grants na linha 420. Replay e duplicata de Confirm na linha 422. LEDGER-16 na linha 77 da matriz. LEDGER-12 e LEDGER-14 não foram reescritos: evidência divergente, confirmer sem capability e o segundo Apply continuam nessas linhas. |
| Estado neste builder | CORRIGIDO NESTA CANDIDATA. Não é fechamento do Codex. |

| Campo | C-02 / NEW-MEDIUM-11 |
|---|---|
| ID | C-02 — cardinalidade e materialização de `pending_provider_cost` |
| Situação no parecer | PARCIALMENTE FECHADO. O over-estimate simples estava certo, mas CONFLICT nem sempre mandava inserir a linha, `operation_id` era único, e LEDGER-15 não dizia que a operação já estava DISPATCHED com reserved 150. |
| Causa-raiz | `pending_actual_minor` era descrito como espelho e também como valor atribuído. Dois receipts não cabiam numa linha única sem escolher um valor pelo lock. |
| Correção | Uma linha imutável por `(operation_id, proof_id)`. `operation_id` sozinho não é único. Toda transição CONFLICT com receipt insere uma linha por RECEIPT conclusivo, reason CONFLICT. Over-estimate insere uma linha, reason OVER_ESTIMATE. `pending_actual_minor` não é atribuído: é nulo sem linha e, com linhas na moeda do build, é `max(amount_minor)`. Dois receipts de 30 e 40 geram duas linhas e a projeção 40. Esse máximo não escolhe a prova verdadeira e não depende de quem pegou o lock. |
| Arquivo | docs/planning/FDP-16A-v1.6-EXECUTION-CONTRACTS.md; matriz v1.6; F-015 |
| Evidência | Coluna na linha 98. Schema na linha 463. Dois valores na linha 395. LEDGER-08 na linha 69 exige a linha de pending do proof R. LEDGER-15 na linha 76 começa DISPATCHED, reserva HELD 50, reserved 150. LEDGER-17 na linha 78 exige as duas linhas e a projeção 40. |
| Estado neste builder | CORRIGIDO NESTA CANDIDATA. Não é fechamento do Codex. |

## O que permanece como o Codex deixou
HIGH-01, NEW-HIGH-07, NEW-HIGH-08 e NEW-HIGH-09 continuam fechados no parecer Round 8. Prova, lock, ator e digest não foram redesenhados. LEDGER-01 a LEDGER-07, LEDGER-09 a LEDGER-14, LEDGER-11, LEDGER-12 e LEDGER-13 mantêm o texto da v1.5. FDP-18, FDP-18A e FDP-20 permanecem v1.3.
