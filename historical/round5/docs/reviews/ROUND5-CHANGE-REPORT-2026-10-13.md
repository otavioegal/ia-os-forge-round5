# Relatório de alterações — Round 5
Data: 2026-10-13.
Autor da correção documental: Grok, no papel de builder documental.
Estado: ROUND 5 — CANDIDATE FOR INDEPENDENT REVIEW.

## Método
Os arquivos do Round 4 foram copiados sem edição para `historical/round4/` (20 arquivos, incluindo pareceres e fontes). As correções existem só como arquivos novos v1.2. Nenhuma fonte FDP-06, FDP-10, FDP-12, FDP-13 ou FDP-14 foi modificada. Nenhum parecer de auditor foi modificado.

Não houve Change Decision. O stack congelado, os 11 estados de Task, a preferência pelo AIOX, a separação Release Agent / Coding Engine e o hard budget em F-015 foram preservados.

## Arquivos novos
| Arquivo | O que mudou em relação ao v1.1 |
|---|---|
| docs/planning/FDP-16-v1.2-AIOX-EXECUTION-ENGINES.md | Título v1.2. Remove o adiamento “ADR before code”. Aponta contratos, eventos de auditoria obrigatórios e a direção de privilégio. |
| docs/planning/FDP-16A-v1.2-EXECUTION-CONTRACTS.md | Saiu de lista de campos sem tipo para schemas com tipo, nulidade e constraint; envelopes versionados; matriz 11×comandos; retry com parâmetros; API interna; recuperação após crash. |
| docs/planning/FDP-17-v1.2-TESTING-STRATEGY.md | Deixa de ser uma segunda matriz. Lista os 17 intents literais e aponta a matriz v1.2 como único oráculo. Não cita matriz v1.0. |
| docs/planning/FDP-18-v1.2-DEPLOYMENT-ROLLBACK.md | Título v1.2. Stack congelado reescrito sem reabrir escolha. Pipeline descrito como ordem exigida, não como execução ocorrida. |
| docs/planning/FDP-18A-v1.2-RECOVERY-RUNBOOKS.md | Três classes de evidência. Classe A escrita. Classes B e C declaradas vazias / não executadas. |
| docs/planning/FDP-19-v1.2-PRODUCT-BACKLOG.md | Índice com sprint resolvido, inclusive F-025 sem sprint. Ponteiro exclusivo à matriz v1.2. |
| docs/planning/FDP-19A-v1.2-STORY-ACCEPTANCE-REGISTER.md | 41 histórias reescritas com requisitos, DoR, aceitação positiva, aceitação negativa, evidência e gate próprios. |
| docs/planning/FDP-20-v1.2-SPRINT-IMPLEMENTATION-PLAN.md | Marcos alinhados às histórias, incluindo a divisão S01/S06 de F-029 e F-030. Spikes continuam NOT RUN, com pass/fail de planejamento. |
| docs/planning/FDP-TRACEABILITY-MATRIX-v1.2-CANONICAL.md | Uma linha de oráculo por teste, com fixture e regras PASS/FAIL. Sem a segunda faixa genérica “scoped acceptance”. |
| docs/planning/FDP-ROUND5-STATUS-INDEX.md | Índice desta rodada. |
| docs/reviews/ROUND5-FINDING-CLOSURE-2026-10-13.md | Fechamento por finding. |
| docs/reviews/ROUND5-CONSISTENCY-REPORT-2026-10-13.md | Saída do verificador. |
| docs/reviews/ROUND5-OPEN-PENDENCIES-2026-10-13.md | Pendências humanas e de implementação. |
| tools/check_round5_consistency.py | Verificador documental. |
| tools/generate_round5.py | Gerador usado para manter as 41 histórias e a matriz alinhadas. Não é documento normativo. |

## Decisões de mapeamento que o revisor deve enxergar
- AUTHZ-01 ficou em F-001 (isolamento de organização). AUTHZ-02 ficou em F-002 (mesmo org, outro projeto). O backlog v1.1 colocava AUTHZ-02 em F-001; isso contradizia a própria matriz v1.1. A v1.2 segue a matriz e o texto literal de FDP-13.
- TERM-01 tem dono primário F-007 (sandbox). F-015 também nega capability de terminal no gateway, mas não é o dono do id.
- ENG-01 e ENG-02 têm dono primário F-027, como na matriz v1.1. F-011 e F-016 contribuem com o filtro e o handoff e estão na coluna “Also exercised by”.
- SEC-01 tem dono único F-006. F-036 cobre o pacote de contexto e não toma o id.
- COST-01 tem uma única linha, dono F-015. O dashboard é COST-DASH-01 em F-021.
- Parâmetros de retry e lease são defaults de especificação (`forge.retry.v1`), marcados como não medidos. Não são SLO de staging.

## O que não foi feito
Não houve implementação, migração, teste, drill, nomeação de pessoas, estimativa em horas, nem aprovação.
