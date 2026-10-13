# Relatório de alterações — Round 9, baseline v1.6
Estado: ROUND 9 — CANDIDATE FOR CODEX REVIEW.
Entrada: `docs/reviews/PARECER-CODEX-ROUND8-2026-10-13.md` e o prompt `docs/reviews/PROMPT-GROK-ROUND9-MEDIUM-CLOSURE.md`.
Commit auditado pelo Codex na Rodada 8: `e70112905e60016600eb41566913f63025685a22`.
A v1.5 foi preservada em `historical/round8/docs/planning/` e não foi editada. O parecer Round 8 não foi editado.

## O que mudou
- FDP-16A v1.6 declara que o Apply de PROVEN_RECEIPT revalida `ledger.reconcile` de `requested_by` e de `confirmed_by` na hora do Apply. Grant ausente não consome a autorização e não move dinheiro.
- O mesmo arquivo define o replay de Confirm, o Confirm com `command_id` novo depois de AUTHORIZED, e a recusa sem evento de auditoria.
- `pending_provider_cost` passa a ser único em `(operation_id, proof_id)`. `pending_actual_minor` é só a projeção `max(amount_minor)`.
- A matriz v1.6 é a única tabela de oráculos. LEDGER-08 passa a exigir a linha de pending. LEDGER-15 explicita DISPATCHED e reserved 150. Entram LEDGER-16 e LEDGER-17. LEDGER-14 não foi reescrito.
- F-015 cita esses oráculos. As outras 40 histórias não tiveram requisito reaberto; só o ponteiro da matriz foi para v1.6.
- FDP-16 v1.6, FDP-17 v1.6 e FDP-19 v1.6 só atualizam ponteiro e a lista de ids. A regra do AIOX não mudou.

## O que foi revalidado e não reescrito
- FDP-18 v1.3, FDP-18A v1.3 e FDP-20 v1.3 continuam em `docs/planning/` com o mesmo texto. A cópia em `historical/round8/` é idêntica.
- Stack congelado, 11 estados de Task, tuple de DeploymentApproval, classes A/B/C, e os HIGH já fechados pelo Codex.

## Arquivos
- docs/planning/FDP-16-v1.6-AIOX-EXECUTION-ENGINES.md
- docs/planning/FDP-16A-v1.6-EXECUTION-CONTRACTS.md
- docs/planning/FDP-17-v1.6-TESTING-STRATEGY.md
- docs/planning/FDP-19-v1.6-PRODUCT-BACKLOG.md
- docs/planning/FDP-19A-v1.6-STORY-ACCEPTANCE-REGISTER.md
- docs/planning/FDP-TRACEABILITY-MATRIX-v1.6-CANONICAL.md
- docs/planning/FDP-ROUND9-STATUS-INDEX.md
- docs/reviews/ROUND9-FINDING-CLOSURE-2026-10-13.md
- docs/reviews/ROUND9-CHANGE-REPORT-2026-10-13.md
- docs/reviews/ROUND9-CONSISTENCY-REPORT-2026-10-13.md
- docs/reviews/ROUND9-OPEN-PENDENCIES-2026-10-13.md
- tools/check_round9_consistency.py
