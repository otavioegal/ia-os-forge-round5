# Relatório de alterações — Round 6, baseline v1.3
Estado: ROUND 6 — CANDIDATE FOR CODEX REVIEW.
Entrada: parecer `docs/reviews/PARECER-CODEX-ROUND5-2026-10-13.md` e a baseline v1.2.
A v1.2 foi copiada para `historical/round5/` e não foi editada.

## Mudanças de contrato
- FDP-16A v1.3 acrescenta o protocolo 8A (reserva, liquidação, liberação, custo real maior ou menor, concorrência, crash), o tuple 8B e o caminho 8C para provider sem consulta de comprovante.
- Matrizes completas de Attempt e Build, com `blocked_from` e proibição de expirar attempt CREATED ou QUEUED.
- `environment_id` deixa de ser enum e passa a ser a identidade da linha de ambiente.
- Regra de identidade: `id` é a chave; `task_id` e equivalentes são aliases; `operation_ref` não é.

## Mudanças de backlog e oráculos
- F-012 passa a exigir a superfície completa pendente do FDP-15, com dependência de F-006, sem declarar o FDP-15 aprovado.
- F-013 deixa de dizer que o AIOX é a única entrada e especifica `FORGE_DIRECT`.
- F-015 passa a ser dono de LEDGER-01..06, além de COST-01. Um recibo sem settlement não é gasto.
- F-016 passa a ser dono de HANDOFF-01, não de QUEUE-01.
- F-029 ganha um teste negativo por campo do tuple, inclusive `approver_actor_ref` (DEPLOY-12). O nome `approved_by` foi removido.
- F-011, F-017, F-023 e F-036 ganham oráculos próprios para requisitos que a v1.2 não cobria.
- Cada história ganha fonte, estado de aprovação e o que é proposta nova.
- FDP-20 enumera o conjunto obrigatório de READY_FOR_HUMAN_TEST.

## Aperto antes da entrega ao Codex
A primeira geração da v1.3 ainda deixava quatro furos que o próprio critério desta rodada não aceitava:

- O tuple citava `approver_actor_ref`, mas F-029 ainda falava em `approved_by` e não havia oráculo para esse campo.
- DEPLOY-02 usava `409 APPROVAL_DIGEST` enquanto a seção 8B exigia `409 APPROVAL_MISMATCH`.
- COST-01 aceitava um recibo sem dizer que o gasto só existe em SETTLED. A segunda liquidação e a reserva concorrente não tinham oráculo.
- O DoD das histórias ainda dizia "Round 5".

Isso foi corrigido no gerador e regenerado. Não é uma rodada nova. Continua sendo a candidata v1.3.

## O que não mudou
Stack congelado, nove spikes, 11 estados de Task, AUTHZ-01 em F-001, SEC-01 em F-006, COST-01 só em F-015, classes A/B/C dos runbooks, ausência de BUILD-00 e ausência de testes executados.

## Arquivos novos da v1.3
- docs/planning/FDP-16-v1.3-AIOX-EXECUTION-ENGINES.md
- docs/planning/FDP-16A-v1.3-EXECUTION-CONTRACTS.md
- docs/planning/FDP-17-v1.3-TESTING-STRATEGY.md
- docs/planning/FDP-18-v1.3-DEPLOYMENT-ROLLBACK.md
- docs/planning/FDP-18A-v1.3-RECOVERY-RUNBOOKS.md
- docs/planning/FDP-19-v1.3-PRODUCT-BACKLOG.md
- docs/planning/FDP-19A-v1.3-STORY-ACCEPTANCE-REGISTER.md
- docs/planning/FDP-20-v1.3-SPRINT-IMPLEMENTATION-PLAN.md
- docs/planning/FDP-TRACEABILITY-MATRIX-v1.3-CANONICAL.md
- docs/planning/FDP-ROUND6-STATUS-INDEX.md
- docs/reviews/ROUND6-FINDING-CLOSURE-2026-10-13.md
- docs/reviews/ROUND6-CHANGE-REPORT-2026-10-13.md
- docs/reviews/ROUND6-CONSISTENCY-REPORT-2026-10-13.md
- docs/reviews/ROUND6-OPEN-PENDENCIES-2026-10-13.md
