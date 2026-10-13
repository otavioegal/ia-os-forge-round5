# Relatório de alterações — Round 8, baseline v1.5
Estado: ROUND 8 — CANDIDATE FOR CODEX REVIEW.
Entrada: `docs/reviews/PARECER-CODEX-ROUND7-2026-10-13.md` e o prompt `docs/reviews/PROMPT-GROK-ROUND8-EVIDENCE-LEDGER-CLOSURE.md`.
Commit da v1.4 auditado pelo Codex: `decef2809b61d3f1fe84bef74a5162d782cc6231`.
O SHA desta candidata é o commit que introduz estes arquivos. Não é escrito aqui.
A v1.4 foi preservada em `historical/round7/docs/planning/` e não foi editada. O parecer Round 7 não foi editado.

## O que mudou
- FDP-16A v1.5 acrescenta a seção 8A.3 (ProviderEffectProof) e troca a corrida receipt contra release. O lock continua na mesma ordem e deixa de decidir a prova.
- O catálogo passa a exigir prova conclusiva, `command_id` na autorização, e os códigos PROOF_CONFLICT, PROOF_INCONCLUSIVE, RECEIPT_PRECEDES_RELEASE, PENDING_COST_HELD, EVIDENCE_SELF_AUTHORED, SESSION_STALE, AUTHORIZATION_CONFLICT, AUTHORIZATION_EXPIRED e CAPABILITY_REVOKED.
- A matriz v1.5 é a única tabela de oráculos. Reescreve LEDGER-08, LEDGER-11 e LEDGER-12. Acrescenta LEDGER-13, LEDGER-14 e LEDGER-15. As outras linhas, inclusive os 17 P0, foram copiadas.
- F-015 passa a citar esses oráculos e a dizer que digest do aprovador não é prova. As outras 40 histórias não tiveram requisito reaberto. O ponteiro da matriz foi para v1.5, para não existirem duas autoridades. A frase de DoD passou a dizer Round 8 porque a candidata é esta, não porque o requisito tenha mudado.
- FDP-16 v1.5, FDP-17 v1.5 e FDP-19 v1.5 só atualizam ponteiro, os dois eventos de auditoria da prova e a lista de ids. A regra do AIOX, o método de teste e o índice das outras histórias ficam como na v1.4.

## O que foi revalidado e não reescrito
- FDP-18 v1.3, FDP-18A v1.3 e FDP-20 v1.3 continuam em `docs/planning/` com o mesmo texto. A cópia em `historical/round7/` é idêntica.
- Stack congelado, 11 estados de Task, tuple de DeploymentApproval, classes A/B/C, AUTHZ-01 em F-001, SEC-01 em F-006, COST-01 em F-015.
- LEDGER-01 a LEDGER-07, LEDGER-09 e LEDGER-10 permanecem com o mesmo texto de oráculo. LEDGER-02 continua sendo o caso sequencial de custo acima do limite. LEDGER-15 acrescenta a linha imutável.

## Via escolhida
Não foi “quem pegar o lock escolhe o terminal”. Não foi “o operador escreve um texto, calcula o digest e isso vira prova”. A prova entra só pelo ingest. Contradição conclusiva bloqueia e conserva as provas. Receipt conclusivo prevalece sobre no-effect inconclusivo. Sem atestação e sem consulta, não há caminho positivo de liberação. Não há comando de write-off nesta baseline.

## Errata da rodada anterior
A correção de Q01 está acrescentada ao fim de `docs/reviews/ROUND7-CHANGE-REPORT-2026-10-13.md`. A frase original não foi removida.

## Arquivos
- docs/planning/FDP-16-v1.5-AIOX-EXECUTION-ENGINES.md
- docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md
- docs/planning/FDP-17-v1.5-TESTING-STRATEGY.md
- docs/planning/FDP-19-v1.5-PRODUCT-BACKLOG.md
- docs/planning/FDP-19A-v1.5-STORY-ACCEPTANCE-REGISTER.md
- docs/planning/FDP-TRACEABILITY-MATRIX-v1.5-CANONICAL.md
- docs/planning/FDP-ROUND8-STATUS-INDEX.md
- docs/reviews/ROUND8-FINDING-CLOSURE-2026-10-13.md
- docs/reviews/ROUND8-CHANGE-REPORT-2026-10-13.md
- docs/reviews/ROUND8-CONSISTENCY-REPORT-2026-10-13.md
- docs/reviews/ROUND8-OPEN-PENDENCIES-2026-10-13.md
- historical/round7/README.md
- tools/check_round8_consistency.py
