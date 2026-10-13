# IA OS Forge — Índice oficial Round 8
Estado: **ROUND 8 — CANDIDATE FOR CODEX REVIEW**.
Não é PASS. Não é aprovação do Founder. Não é READY FOR BUILD. Não autoriza BUILD-00.
Nenhum teste de software foi executado. Nenhum drill de staging foi executado.

## Autoridade desta rodada
A única tabela de oráculos é `FDP-TRACEABILITY-MATRIX-v1.5-CANONICAL.md`.
O único protocolo de dinheiro é FDP-16A v1.5 seções 8A a 8A.3.
O restante abaixo continua candidato. Nada disso está aprovado.

| Arquivo | Papel nesta rodada |
|---|---|
| FDP-16-v1.5-AIOX-EXECUTION-ENGINES.md | Fronteiras revalidadas. AIOX preferencial não foi reaberto. Só entraram os nomes de auditoria `budget.proof_conflict` e `budget.proof_inconclusive`. |
| FDP-16A-v1.5-EXECUTION-CONTRACTS.md | Contratos. A mudança de regra é precedência de prova, confiança da evidência, idempotência da autorização e custo pendente. |
| FDP-17-v1.5-TESTING-STRATEGY.md | Método revalidado. Ponteiro da matriz e ids LEDGER-13..15. |
| FDP-18-v1.3-DEPLOYMENT-ROLLBACK.md | Revalidado, não reescrito. Não define oráculo. |
| FDP-18A-v1.3-RECOVERY-RUNBOOKS.md | Revalidado, não reescrito. Classes B e C continuam abertas. |
| FDP-19-v1.5-PRODUCT-BACKLOG.md | Índice. Só a linha de testes de F-015 e o ponteiro da matriz mudaram. |
| FDP-19A-v1.5-STORY-ACCEPTANCE-REGISTER.md | 41 histórias. Só F-015 foi reaberta. |
| FDP-20-v1.3-SPRINT-IMPLEMENTATION-PLAN.md | Revalidado, não reescrito. O conjunto de READY_FOR_HUMAN_TEST não mudou. |
| FDP-TRACEABILITY-MATRIX-v1.5-CANONICAL.md | Única tabela de oráculos. |

## O que esta rodada decide
- A ordem de lock é exclusão mútua. Não escolhe qual prova é verdadeira.
- Um receipt conclusivo não perde para uma liberação só porque a liberação pegou o lock.
- Provas conclusivas contraditórias bloqueiam, conservam as duas provas e não inventam gasto.
- Sem atestação e sem consulta verificável, a prova fica UNVERIFIED e não move dinheiro. O sistema não inventa assinatura.
- Quem captura é `forge.provider_ingest`. Quem aprova não é quem captura. Quem confirma é um segundo operador. Quem move dinheiro é o system, depois da autorização.
- `pending_actual_minor` registra custo conhecido que ainda não é `spent`.

## Histórico
- `historical/round7/docs/planning/` — v1.4 byte a byte, mais a cópia idêntica de FDP-18, FDP-18A e FDP-20.
- `historical/round6/` — v1.3, sem edição.
- `historical/round5/` — v1.2, sem edição.
- `historical/round4/` — pacote anterior, sem edição.
- Os pareceres do Codex Round 5, Round 6 e Round 7 permanecem em `docs/reviews/` e não foram reescritos.

## Fora desta autoridade
Matrizes v1.0, v1.1, v1.2, v1.3 e v1.4. Resultados de teste. Drills. Nomes de pessoas. Aprovação de FDP-14 e FDP-15. BUILD-00.

O SHA auditável é o commit que introduz esta v1.5. Ele é informado na entrega ao Codex. Este índice não o antecipa, para não exigir um segundo commit.
