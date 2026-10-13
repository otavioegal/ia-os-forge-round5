# Pendências que dependem de decisão humana ou de implementação futura
Estado: ROUND 5 — CANDIDATE FOR INDEPENDENT REVIEW.
Nenhuma linha abaixo está resolvida por este pacote.

| ID | Pendência | Por que não foi fechada aqui | Bloqueia |
|---|---|---|---|
| P-01 | Revisão independente do Codex sobre o v1.2 | O builder não audita a própria entrega no lugar do revisor | Qualquer uso do v1.2 como baseline |
| P-02 | Aprovação do Founder sobre o conjunto v1.2 | Não existe assinatura e nenhuma foi simulada | Baseline de planejamento |
| P-03 | Confirmação do Founder sobre FDP-14 | Já estava pendente no Round 4 | Pré-condição de FDP-20 |
| P-04 | Aprovação do Founder sobre FDP-15 | Já estava pendente no Round 4 | Contratos de adapter na implementação |
| P-05 | Nome da pessoa responsável por cada história e cada spike | O plano só tem papel (Data, Security, Desktop, e os demais) | DoR completo de execução |
| P-06 | Esforço em horas e timebox | Há só classe relativa S/M/L/XL e o motivo. Número de horas seria chute | Planejamento de capacidade |
| P-07 | Autorização explícita de BUILD-00 | Este pacote diz o contrário | Início de spikes e código |
| P-08 | Execução dos testes da matriz | Todos os status permanecem NOT RUN | SECURITY FOUNDATION e qualquer gate posterior |
| P-09 | Classe B dos runbooks: limiar, query, janela, RPO, RTO, plantão | Medir isso exige staging. Inventar o número foi proibido | Produção, não a escrita do código de Classe A |
| P-10 | Classe C: drills RB-APP, RB-SCHEMA, RB-RUNNER, RB-DESKTOP, RB-SECRET | Não houve ensaio | Certificação operacional e produção |
| P-11 | Scripts versionados de operador | O texto exige que existam e registra que não existem | Runbook executável |
| P-12 | Metas numéricas de EVAL-HIR-01 e EVAL-TFV-01 | F-041 define a fórmula e proíbe meta inventada | Decisão de produto depois de amostra real |
| P-13 | F-025 e PERF-01 | P3, sem sprint, à espera de Change Decision | Nada do MVP |
| P-14 | Resultados dos SPIKE-01…09 | Hipóteses escritas; evidência ausente | Ajustes de ADR que só os spikes podem motivar |

## Separação de prontidão
Prontidão documental desta entrega: candidata a revisão, não aprovada.
Prontidão operacional: inexistente. Não há software construído, não há evidência de teste e não há drill.
