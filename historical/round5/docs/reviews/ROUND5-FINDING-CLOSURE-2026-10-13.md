# Registro de fechamento dos findings — Round 4 para Round 5
Estado: ROUND 5 — CANDIDATE FOR INDEPENDENT REVIEW.
Este registro mostra onde cada finding foi tratado. Não substitui o parecer do Codex. Não declara o plano aprovado.

Classificação usada:
- RESOLVIDO — o defeito descrito no finding não permanece no texto v1.2, e a evidência está citada.
- PARCIAL — uma parte do defeito foi fechada no texto e outra foi explicitamente deixada aberta, sem número inventado e sem drill inventado.
- ABERTO — não fechado.

## Findings do Codex Round 4 e do Grok Round 4

| ID | Finding | Classe | Evidência no v1.2 | Estado |
|---|---|---|---|---|
| C01 | Contratos de execução não implementáveis: sem tipos, sem matriz completa, retry vago, sem API, normalização adiada para ADR | HIGH | [FDP-16A-v1.2-EXECUTION-CONTRACTS.md](../planning/FDP-16A-v1.2-EXECUTION-CONTRACTS.md) seções 1–3 (tipos, nulidade, constraints), seção 4 (envelopes `forge.command.v1` e `forge.event.v1`), seção 5 (catálogo de comandos), seção 6 (matriz dos 11 estados de Task), seção 8 (`max_attempts` 5, `base_delay_ms` 250, `cap_delay_ms` 30000, classes transient/permanent/ambiguous), seção 9 (API entre Controller, Task Service, Attempt Manager, Gateway, Adapter), seção 10 (recuperação). [FDP-16 v1.2](../planning/FDP-16-v1.2-AIOX-EXECUTION-ENGINES.md) seção 3 retira o adiamento de ADR. Os 11 estados continuam os de FDP-12: QUEUED, READY, RUNNING, WAITING, RETRYING, HANDOFF, REVIEWING, BLOCKED, COMPLETED, FAILED, CANCELLED. | RESOLVIDO |
| C02 | 41 registros DoR/DoD eram o mesmo template; aceitação positiva repetia o título; negativa era “as applicable” | HIGH | [FDP-19A v1.2](../planning/FDP-19A-v1.2-STORY-ACCEPTANCE-REGISTER.md) tem F-001…F-041. O verificador contou 41 aceitações positivas distintas e 41 negativas distintas. A frase “as applicable” não ocorre. Exemplo de especificidade, não de amostra genérica: F-015 usa limit 1000 / spent 800 / reserved 100 e exige contador de provider em 0 no caso de 200 minor units. | RESOLVIDO |
| C03 | AUTHZ-01 ausente de F-001 e SEC-01 ausente de F-006; COST-01 precisava permanecer hard stop | HIGH | F-001 lista os testes RLS-01 e AUTHZ-01 e descreve org_a contra org_b. F-006 lista SEC-01, SEC-02 e VAULT-01 e fixa o canário `CANARY_SECRET_FORGE_9f3a`. F-015 é o único dono de COST-01. F-021 diz que não pode satisfazer COST-01. Matriz v1.2: uma linha por id, primário conforme a coluna Primary story. Os outros 15 ids P0 de FDP-13 §191 também têm uma linha cada (17/17). | RESOLVIDO |
| C04 | Matriz v1.1 não era a única referência; FDP-17 e FDP-19 ainda citavam v1.0 | HIGH | Nenhum arquivo v1.2 contém `TRACEABILITY-MATRIX-v1.0` ou `v1.1`. FDP-17 v1.2 declara que a única tabela de oráculos é a matriz v1.2. O índice Round 5 repete essa regra. As matrizes antigas permanecem só em `historical/round4/`. | RESOLVIDO |
| C05 | Oráculos “authorized or nominal / prohibited or adversarial” | MEDIUM | A matriz v1.2 troca esse par por fixture, regra positiva e regra negativa. O verificador falha se a frase “authorized or nominal” voltar. Exemplo: AUTHZ-01 exige 403 `AUTHZ_FOREIGN_ORG` e falha se houver 200 ou campo de org_b. | RESOLVIDO |
| C06 | Runbooks dependentes de calibração de staging e ainda assim tratados como procedimento | HIGH | [FDP-18A v1.2](../planning/FDP-18A-v1.2-RECOVERY-RUNBOOKS.md) separa Classe A (gatilho, papel, ação, verificação, ramo de falha — escrito), Classe B (limiar, janela, query, RPO, RTO, nomes de plantão — em branco de propósito) e Classe C (drills — NOT EXECUTED). Nenhum número medido foi inventado. | PARCIAL |
| C07 | Integridade: privilégio, handoff, concorrência, interrupção parcial, ciclos de autoridade | HIGH (pedido de revisão; não era um defeito de código, porque não há código) | FDP-16A seções 8, 9 e 10 e FDP-16 v1.2 seção 8. Direção permitida: política humana → Policy → Gateway → Adapter. O motor não escreve policy, orçamento nem DeploymentApproval. Dois leases válidos no mesmo task são falha de QUEUE-01. Sequências de crash antes do commit, depois da reserva e depois do dispatch estão na seção 10. | RESOLVIDO no texto. Sem evidência de implementação — isso é esperado e não é um teste executado. |
| C08 | Títulos v1.0 em arquivos v1.1 | MEDIUM | A primeira linha de cada FDP v1.2 diz v1.2. O verificador recusa título “v1.0 —”. O estado comum é “ROUND 5 — CANDIDATE FOR INDEPENDENT REVIEW” e “NOT READY FOR BUILD”. | RESOLVIDO |

## Itens que permanecem abertos de propósito
Estão listados em [ROUND5-OPEN-PENDENCIES-2026-10-13.md](ROUND5-OPEN-PENDENCIES-2026-10-13.md). Resumo: donos nomeados, calibração de esforço, aprovação de FDP-14 e FDP-15, autorização de BUILD-00, execução de testes, preenchimento da Classe B, drills da Classe C, metas numéricas de avaliação e qualquer trabalho de F-025.

## O que este registro não faz
Não altera os pareceres em `historical/round4/docs/reviews/`. Não marca nenhum teste como PASS. Não pede que o Codex trate este arquivo como autoauditoria conclusiva.
