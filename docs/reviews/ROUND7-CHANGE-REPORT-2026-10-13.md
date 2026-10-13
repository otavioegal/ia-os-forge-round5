# Relatório de alterações — Round 7, baseline v1.4
Estado: ROUND 7 — CANDIDATE FOR CODEX REVIEW.
Entrada: `docs/reviews/PARECER-CODEX-ROUND6-2026-10-13.md` e o prompt `docs/reviews/PROMPT-GROK-ROUND7-LEDGER-CLOSURE.md`.
Commit auditado pelo Codex: `4e5783974ca27595c9592e2e6ac55ab23fcbeb5a`.
A v1.3 foi preservada em `historical/round6/docs/planning/` e não foi editada. O parecer Round 6 não foi editado.

## O que mudou
- FDP-16A v1.4 acrescenta a seção 8A.1 (lock, constraint, quatro corridas, retry, custo acima do limite) e a seção 8A.2 (uma via humana de autorização e apply posterior pelo system).
- O catálogo deixa de aceitar RecordReceipt e ReleaseReservation em BLOCKED_RECONCILIATION e deixa de tratá-los como comando humano.
- A matriz v1.4 é a única tabela de oráculos. Acrescenta LEDGER-07 a LEDGER-12. As linhas anteriores, inclusive os 17 P0, foram copiadas.
- F-015 passa a citar esses oráculos. As outras 40 histórias não tiveram requisito reaberto; só o ponteiro da matriz foi para v1.4, para não existirem duas autoridades.
- FDP-16 v1.4, FDP-17 v1.4 e FDP-19 v1.4 só atualizam ponteiro, eventos de auditoria do ledger e a lista de ids. A regra do AIOX, o método de teste e o índice das outras histórias ficam como na v1.3.

## O que foi revalidado e não reescrito
- FDP-18 v1.3, FDP-18A v1.3 e FDP-20 v1.3 continuam em `docs/planning/` com o mesmo texto. Eles não definem oráculo nem transição de dinheiro. A cópia em `historical/round6/` é idêntica.
- Stack congelado, 11 estados de Task, tuple de DeploymentApproval, classes A/B/C, AUTHZ-01 em F-001, SEC-01 em F-006, COST-01 em F-015.

## Via escolhida para NEW-HIGH-07
Não foi a via em que o humano chama RecordReceipt. Foi a via em que o humano só autoriza, com evidência prévia e dual control quando a decisão pode aumentar `spent`, e o system executa o movimento depois. Isso elimina a contradição entre o catálogo e a seção 8A da v1.3.

## Arquivos
- docs/planning/FDP-16-v1.4-AIOX-EXECUTION-ENGINES.md
- docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md
- docs/planning/FDP-17-v1.4-TESTING-STRATEGY.md
- docs/planning/FDP-19-v1.4-PRODUCT-BACKLOG.md
- docs/planning/FDP-19A-v1.4-STORY-ACCEPTANCE-REGISTER.md
- docs/planning/FDP-TRACEABILITY-MATRIX-v1.4-CANONICAL.md
- docs/planning/FDP-ROUND7-STATUS-INDEX.md
- docs/reviews/ROUND7-FINDING-CLOSURE-2026-10-13.md
- docs/reviews/ROUND7-CHANGE-REPORT-2026-10-13.md
- docs/reviews/ROUND7-CONSISTENCY-REPORT-2026-10-13.md
- docs/reviews/ROUND7-OPEN-PENDENCIES-2026-10-13.md
- tools/check_round7_consistency.py

## Errata — 2026-10-13
A frase da abertura, “Commit auditado pelo Codex: `4e5783974ca27595c9592e2e6ac55ab23fcbeb5a`”, permanece como foi publicada na Rodada 7. Ela não foi apagada. Está errada como identificação do commit auditado.

`4e5783974ca27595c9592e2e6ac55ab23fcbeb5a` é o commit da baseline Round 6. O commit da baseline v1.4 que o parecer `docs/reviews/PARECER-CODEX-ROUND7-2026-10-13.md` declara ter auditado é `decef2809b61d3f1fe84bef74a5162d782cc6231`.

Esta errata não reescreve o restante do relatório.

