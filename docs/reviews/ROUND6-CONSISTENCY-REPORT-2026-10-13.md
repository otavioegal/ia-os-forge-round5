# Relatório de consistência — Round 6
Estado: ROUND 6 — CANDIDATE FOR CODEX REVIEW.
Duas passagens documentais. Nenhuma delas executa o produto.

## Passagem 1 — integridade do conjunto
Conferido no texto gerado da v1.3:

- 79 linhas de oráculo, sem id duplicado e sem linha com número errado de colunas.
- Os 17 ids de FDP-13 §191 continuam com uma linha cada. AUTHZ-01, SEC-01 e COST-01 permanecem com o dono da v1.2.
- Todo id citado no campo Tests das histórias existe na matriz.
- 41 blocos `- Inherited:`.
- `environment_id` não é mais enum.
- A frase "only supported orchestrator" não aparece.
- A frase "reconcile with the provider receipt API" não aparece.
- Coluna Steps presente.
- DoR operacional separado e marcado como não atendido.
- Conjunto de READY_FOR_HUMAN_TEST presente no FDP-20.
- A cópia histórica de FDP-16A v1.2 é idêntica ao arquivo da rodada anterior (`cmp`).

## Passagem 2 — amostragem semântica dos findings
Não foi uma contagem de strings únicas.

- HANDOFF-01 exige attempt terminal, revogação de grant, digest inválido e proibição de dois attempts não terminais. Resultado: verdadeiro.
- LEDGER-01 fala em SETTLED e LEDGER-04 recusa segunda reserva. Resultado: verdadeiro.
- ADAPT-01 chama start_task, get_diff e get_test_results. Resultado: verdadeiro.
- DEPLOY-05 distingue dois ambientes PRODUCTION pelo environment_id. Resultado: verdadeiro.
- LEDGER-05 usa BLOCKED_RECONCILIATION quando não há consulta de receipt. Resultado: verdadeiro.

## Passagem 3 — furos achados na releitura, antes de chamar a entrega pronta
- Os dez campos do tuple de deploy têm um `mismatch_field` na matriz, incluindo `approver_actor_ref` em DEPLOY-12. Resultado: verdadeiro.
- F-029 não declara coluna `approved_by`. As duas ocorrências restantes da palavra dizem que a coluna não existe. Resultado: verdadeiro.
- COST-01 só passa se o recibo de 50 terminar em SETTLED, spent 850 e reserved de volta a 100. LEDGER-01 recusa a segunda liquidação. LEDGER-02 permanece RECONCILING. LEDGER-06 não duplica reserva. Resultado: verdadeiro.
- Nenhum DoD da v1.3 diz "Round 5". A v1.2 histórica ainda diz, de propósito. Resultado: verdadeiro.

## Limite
Estas passagens não provam que um implementador não possa ainda divergir em um detalhe que o Codex venha a apontar. Não há PASS de prontidão. Não há teste executado.
