# IA OS Forge — Índice oficial Round 9
Estado: **ROUND 9 — CANDIDATE FOR CODEX REVIEW**.
Não é PASS. Não é aprovação do Founder. Não é READY FOR BUILD. Não autoriza BUILD-00.
Nenhum teste de software foi executado. Nenhum drill de staging foi executado.

O parecer Round 8 deu PASS WITH CONDITIONS à v1.5 e fechou os quatro HIGH. Esta rodada só responde às condições C-01 e C-02. Isso não converte a v1.6 em PASS.

## Autoridade desta rodada
A única tabela de oráculos é `FDP-TRACEABILITY-MATRIX-v1.6-CANONICAL.md`.
O único protocolo de dinheiro é FDP-16A v1.6 seções 8A a 8A.3.
O restante abaixo continua candidato. Nada disso está aprovado.

| Arquivo | Papel nesta rodada |
|---|---|
| FDP-16-v1.6-AIOX-EXECUTION-ENGINES.md | Fronteiras revalidadas. AIOX não foi reaberto. Nenhum nome de auditoria novo. |
| FDP-16A-v1.6-EXECUTION-CONTRACTS.md | Contratos. A mudança de regra é a revalidação de capability no Apply e a cardinalidade de `pending_provider_cost`. |
| FDP-17-v1.6-TESTING-STRATEGY.md | Método revalidado. Ponteiro da matriz e ids LEDGER-16 e LEDGER-17. |
| FDP-18-v1.3-DEPLOYMENT-ROLLBACK.md | Revalidado, não reescrito. Não define oráculo. |
| FDP-18A-v1.3-RECOVERY-RUNBOOKS.md | Revalidado, não reescrito. Classes B e C continuam abertas. |
| FDP-19-v1.6-PRODUCT-BACKLOG.md | Índice. Só a linha de testes de F-015 e o ponteiro da matriz mudaram. |
| FDP-19A-v1.6-STORY-ACCEPTANCE-REGISTER.md | 41 histórias. Só F-015 foi reaberta. |
| FDP-20-v1.3-SPRINT-IMPLEMENTATION-PLAN.md | Revalidado, não reescrito. O conjunto de READY_FOR_HUMAN_TEST não mudou. |
| FDP-TRACEABILITY-MATRIX-v1.6-CANONICAL.md | Única tabela de oráculos. |

## O que esta rodada decide
- No Apply de `PROVEN_RECEIPT`, `ledger.reconcile` é revalidado para `requested_by` e para `confirmed_by`. A aprovação anterior não basta.
- Se qualquer um desses grants faltou: `403 CAPABILITY_REVOKED`, autorização não consumida, reserva HELD, nenhum movimento.
- Confirm com o mesmo `command_id` é replay. Confirm com `command_id` novo depois de AUTHORIZED não grava linha nem evento.
- `pending_provider_cost` tem uma linha imutável por `(operation_id, proof_id)`. `pending_actual_minor` só projeta `max(amount_minor)`. Não é atribuído pelo comando e não escolhe a prova verdadeira.

## Histórico
- `historical/round8/docs/planning/` — v1.5 byte a byte, mais a cópia idêntica de FDP-18, FDP-18A e FDP-20.
- `historical/round7/` — v1.4, sem edição.
- `historical/round6/` — v1.3, sem edição.
- `historical/round5/` — v1.2, sem edição.
- `historical/round4/` — pacote anterior, sem edição.
- O parecer do Codex Round 8 permanece em `docs/reviews/` e a cópia em `historical/round8/docs/reviews/` é o mesmo texto.

## Fora desta autoridade
Matrizes v1.0 a v1.5. Resultados de teste. Drills. Nomes de pessoas. Aprovação de FDP-14 e FDP-15. BUILD-00.

O SHA auditável é o commit que introduz esta v1.6. Ele é informado na entrega ao Codex. Este índice não o antecipa, para não exigir um segundo commit.
