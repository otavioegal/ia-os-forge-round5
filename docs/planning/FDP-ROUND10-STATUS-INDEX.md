# IA OS Forge — Índice oficial Round 10
Estado: **ROUND 10 — CANDIDATE FOR CODEX REVIEW**.
Não é PASS. Não é aprovação do Founder. Não é READY FOR BUILD. Não autoriza BUILD-00.
Nenhum teste de software foi executado. Nenhum drill de staging foi executado.

O parecer Round 9 deu PASS WITH CONDITIONS à v1.6, fechou C-01 e deixou NEW-MEDIUM-12. Esta rodada só responde a essa condição. Isso não converte a v1.7 em PASS.

## Autoridade desta rodada
A única tabela de oráculos é `FDP-TRACEABILITY-MATRIX-v1.7-CANONICAL.md`.
O único protocolo de dinheiro é FDP-16A v1.7 seções 8A a 8A.3.
O restante abaixo continua candidato. Nada disso está aprovado.

| Arquivo | Papel nesta rodada |
|---|---|
| FDP-16-v1.7-AIOX-EXECUTION-ENGINES.md | Fronteiras revalidadas. AIOX não foi reaberto. |
| FDP-16A-v1.7-EXECUTION-CONTRACTS.md | Contratos. A única mudança de regra é late evidence depois de um movement já gravado. |
| FDP-17-v1.7-TESTING-STRATEGY.md | Método revalidado. Ponteiro da matriz e o id LEDGER-18. |
| FDP-18-v1.3-DEPLOYMENT-ROLLBACK.md | Revalidado, não reescrito. Não define oráculo. |
| FDP-18A-v1.3-RECOVERY-RUNBOOKS.md | Revalidado, não reescrito. Classes B e C continuam abertas. |
| FDP-19-v1.7-PRODUCT-BACKLOG.md | Índice. Só a linha de testes de F-015 e o ponteiro da matriz mudaram. |
| FDP-19A-v1.7-STORY-ACCEPTANCE-REGISTER.md | 41 histórias. Só F-015 foi reaberta. |
| FDP-20-v1.3-SPRINT-IMPLEMENTATION-PLAN.md | Revalidado, não reescrito. O conjunto de READY_FOR_HUMAN_TEST não mudou. |
| FDP-TRACEABILITY-MATRIX-v1.7-CANONICAL.md | Única tabela de oráculos. |

## O que esta rodada decide
- Toda entrada em CONFLICT com um ou mais receipts conclusivos grava uma linha `pending_provider_cost` por `(operation_id, proof_id)`, reason CONFLICT. Isso vale depois de RELEASE e depois de SETTLEMENT.
- Não se inventa receipt para um NO_EFFECT.
- `spent` e `reserved` ficam nos valores do movement já confirmado. Não há segundo movement, nem `budget.settled`, nem `budget.released`, nem redispatch.
- RELEASE seguido de receipt 30 grava essa linha. SETTLEMENT 30 seguido de receipt 40 grava as duas e projeta 40. SETTLEMENT seguido de no-effect grava o receipt já conhecido.

## Histórico
- `historical/round9/docs/planning/` — v1.6 byte a byte, mais a cópia idêntica de FDP-18, FDP-18A e FDP-20.
- `historical/round8/` — v1.5, sem edição.
- `historical/round7/` — v1.4, sem edição.
- `historical/round6/` — v1.3, sem edição.
- `historical/round5/` — v1.2, sem edição.
- `historical/round4/` — pacote anterior, sem edição.
- O parecer do Codex Round 9 permanece em `docs/reviews/` e a cópia em `historical/round9/docs/reviews/` é o mesmo texto.

## Fora desta autoridade
Matrizes v1.0 a v1.6. Resultados de teste. Drills. Nomes de pessoas. Aprovação de FDP-14 e FDP-15. BUILD-00.

O SHA auditável é o commit que introduz esta v1.7. Ele é informado na entrega ao Codex. Este índice não o antecipa, para não exigir um segundo commit.
