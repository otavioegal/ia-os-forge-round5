# Relatório de alterações — Round 10, baseline v1.7
Estado: ROUND 10 — CANDIDATE FOR CODEX REVIEW.
Entrada: `docs/reviews/PARECER-CODEX-ROUND9-2026-10-13.md` e o prompt `docs/reviews/PROMPT-GROK-ROUND10-LATE-EVIDENCE-CLOSURE.md`.
Commit auditado pelo Codex na Rodada 9: `a223f1ef460037221f64302bac4005f27f90ae4c`.
A v1.6 foi preservada em `historical/round9/docs/planning/` e não foi editada. O parecer Round 9 não foi editado.

## O que mudou
- FDP-16A v1.7 tira a restrição “só quando o movement foi RELEASE”. Late evidence grava uma linha de pending por receipt conclusivo, também depois de SETTLEMENT.
- As três trajetórias — release e receipt 30, settlement 30 e receipt 40, settlement e no-effect — estão no mesmo parágrafo. Nenhuma altera `spent` ou `reserved` de novo e nenhuma cria segundo movement.
- A matriz v1.7 é a única tabela de oráculos. Entra LEDGER-18. LEDGER-17 e os demais oráculos da v1.6 foram copiados.
- F-015 cita LEDGER-18. As outras 40 histórias não tiveram requisito reaberto; só o ponteiro da matriz foi para v1.7.
- FDP-16 v1.7, FDP-17 v1.7 e FDP-19 v1.7 só atualizam ponteiro e a lista de ids. A regra do AIOX não mudou.

## O que foi revalidado e não reescrito
- FDP-18 v1.3, FDP-18A v1.3 e FDP-20 v1.3 continuam em `docs/planning/` com o mesmo texto. A cópia em `historical/round9/` é idêntica.
- Stack congelado, 11 estados de Task, tuple de DeploymentApproval, C-01 e os HIGH já fechados pelo Codex.

## Arquivos
- docs/planning/FDP-16-v1.7-AIOX-EXECUTION-ENGINES.md
- docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md
- docs/planning/FDP-17-v1.7-TESTING-STRATEGY.md
- docs/planning/FDP-19-v1.7-PRODUCT-BACKLOG.md
- docs/planning/FDP-19A-v1.7-STORY-ACCEPTANCE-REGISTER.md
- docs/planning/FDP-TRACEABILITY-MATRIX-v1.7-CANONICAL.md
- docs/planning/FDP-ROUND10-STATUS-INDEX.md
- docs/reviews/ROUND10-FINDING-CLOSURE-2026-10-13.md
- docs/reviews/ROUND10-CHANGE-REPORT-2026-10-13.md
- docs/reviews/ROUND10-CONSISTENCY-REPORT-2026-10-13.md
- docs/reviews/ROUND10-OPEN-PENDENCIES-2026-10-13.md
- tools/check_round10_consistency.py
