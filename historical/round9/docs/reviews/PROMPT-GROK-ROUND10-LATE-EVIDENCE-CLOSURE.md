# IA OS Forge — Prompt Grok Round 10: fechamento do último MEDIUM

Repositório: https://github.com/otavioegal/ia-os-forge-round5
Baseline auditada: v1.6, commit a223f1ef460037221f64302bac4005f27f90ae4c.
Parecer independente: docs/reviews/PARECER-CODEX-ROUND9-2026-10-13.md.
Resultado: PASS WITH CONDITIONS documental. C-01 fechada. C-02 parcialmente fechada por NEW-MEDIUM-12.
Builder Grok; revisor independente Codex; governança ChatGPT e Founder.
Saída proposta: v1.7 — ROUND 10 — CANDIDATE FOR CODEX REVIEW.

Leia INTEGRALMENTE o parecer Round 9, FDP-16A v1.6 linhas 350, 405, 461, 463, FDP-19A F-015 v1.6, a matriz v1.6 LEDGER-08/15/17 e os documentos históricos. Não altere pareceres históricos nem reabra os 4 HIGH e C-01 já fechados.

MISSÃO ÚNICA — NEW-MEDIUM-12: eliminar contradição normativa para late evidence e pending_provider_cost.

1. Substitua em FDP-16A v1.6 linhas 350 e 405 a condição restritiva de inserir pending_provider_cost apenas quando o movimento anterior foi RELEASE. Toda transição para CONFLICT com um ou mais receipts conclusivos deve persistir idempotentemente uma linha append-only por (operation_id, proof_id), reason CONFLICT. Não invente recibo se não houver receipt conclusivo.
2. Defina explicitamente as três trajetórias: RELEASE seguido de receipt conclusivo, SETTLEMENT 30 seguido de receipt conclusivo 40, e SETTLEMENT seguido de no-effect conclusivo. Preserve todos os proofs; para o caso 30+40, materialize ambos os pending rows e pending_actual_minor=max(30,40)=40, sem escolher pelo lock. Para no-effect após SETTLEMENT preserve ou materialize receipt já conhecido. Estados de conflito, projeções e a ausência de segundo money movement devem ser inequívocos.
3. Em todos os cenários, não altere spent/reserved depois do movement já confirmado; não gere nova cobrança, liberação, evento financeiro ou redispatch; mantenha restrições para novos money commands e trilha auditável budget.proof_conflict.
4. Atualize FDP-16A e F-015 na mesma versão normativa e amplie LEDGER-17 ou crie um oracle de late-evidence com fixtures, passos, PASS/FAIL e evidências para as três trajetórias. Mantenha uma única matriz normativa.
5. Faça checagem cruzada de schema, transitions, ledger invariants, log/audit, ordens de lock, oracles e links. Preserve 41 histórias, 17 P0, 11 Task states e todo histórico v1.6 em historical/round9. Checks documentais não significam testes executados: manter NOT RUN.
6. Produza índice ROUND10, change report, finding closure de NEW-MEDIUM-12, consistency report, open pendencies. Entregar commit no GitHub e SHA para auditoria independente Codex. Não declarar PASS, não presumir aprovação FDP-14/15 ou Founder e não autorizar BUILD-00.

A correção é estritamente dirigida; evitar outras mudanças de arquitetura ou rounds artificiais. Estado final CANDIDATE FOR CODEX REVIEW.
