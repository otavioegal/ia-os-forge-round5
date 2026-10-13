# Parecer final — IA OS Forge Round 5

**Veredito para PRONTIDÃO DOCUMENTAL: FAIL**

**Prontidão operacional: NÃO AVALIÁVEL / INEXISTENTE.** Não existe software, execução dos testes, BUILD-00, deploy ou drill de staging. Isso não foi usado como motivo para o `FAIL`; o veredito decorre de lacunas e contradições ainda presentes na própria especificação documental.

Não há finding `CRITICAL`. Há findings `HIGH` que permitem interpretações de implementação incompatíveis em áreas de custo, aprovação de deployment, adapters, continuidade e critérios de aceite.

A v1.2 é uma evolução substancial sobre o Round 4: corrige os 17 IDs P0, restaura `AUTHZ-01`, `SEC-01` e `COST-01`, consolida a matriz v1.2, individualiza muito melhor as 41 histórias e separa corretamente runbook especificado de runbook certificado. Ainda assim, o registro autorrelatado como “RESOLVIDO” é excessivamente otimista para C01, C02, C05 e C07.

## Findings prioritários

### HIGH-01 — Ledger de custo e ciclo de `Operation` ainda não têm protocolo transacional completo

A especificação define o limite `spent + reserved <= limit` e a reserva anterior ao provider, mas não define de forma inequívoca:

- transição da reserva para gasto confirmado;
- liberação de reserva em falha, cancelamento ou custo menor;
- tratamento de custo final maior que o estimado;
- atomicidade entre receipt, gasto confirmado e liberação da reserva;
- estados terminais de `Operation` para sucesso, falha ou cancelamento.

`Operation.status` termina em `RECEIPT`, `RECONCILING` ou `DENIED`; `RecordReceipt` apenas grava `RECEIPT/MATCHED`. Isso não basta para implementar contabilização financeira convergente após retries e crashes.

Evidências:

- [FDP-16A:43](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-16A-v1.2-EXECUTION-CONTRACTS.md:43)
- [FDP-16A:50](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-16A-v1.2-EXECUTION-CONTRACTS.md:50)
- [FDP-16A:83](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-16A-v1.2-EXECUTION-CONTRACTS.md:83)
- [FDP-16A:196](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-16A-v1.2-EXECUTION-CONTRACTS.md:196)
- [F-015:552](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-19A-v1.2-STORY-ACCEPTANCE-REGISTER.md:552)

Impacto: implementações diferentes podem todas alegar conformidade, mas produzir saldo preso, gasto não contabilizado ou reserva duplicada após recuperação.

Correção documental: adicionar máquina de estados do ledger, efeitos atômicos de settlement/release e oráculos para sucesso, falha, cancelamento, custo real divergente e crash em cada fronteira.

---

### HIGH-02 — `DeploymentApproval` declara vínculo integral, mas os oráculos não o provam

O schema lista `release_id`, hashes de fonte/artefato/grafo/migração, ambiente e versão de política. Contudo:

- `environment_id` é tipado como enum `DEV/STAGING/PROD`, embora o nome indique identidade e FDP-12 possua entidades de ambiente; isso não distingue dois ambientes PROD;
- os testes verificam principalmente digest incorreto, expiração e replay;
- não há casos negativos explícitos para `release_id`, `source_git_hash`, `graph_revision`, `migration_set_hash`, ambiente e `policy_version` divergentes.

Evidências:

- [FDP-16A:136](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-16A-v1.2-EXECUTION-CONTRACTS.md:136)
- [FDP-16A:145](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-16A-v1.2-EXECUTION-CONTRACTS.md:145)
- [F-029:1073](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-19A-v1.2-STORY-ACCEPTANCE-REGISTER.md:1073)
- [F-029:1088](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-19A-v1.2-STORY-ACCEPTANCE-REGISTER.md:1088)
- [Matriz DEPLOY-02:22](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.2-CANONICAL.md:22)
- [Matriz DEPLOY-03:35](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.2-CANONICAL.md:35)

Impacto: a documentação não impede que uma aprovação válida para outra release, migração, grafo, política ou ambiente seja aceita por uma implementação incompleta.

Correção documental: tornar `environment_id` UUID/FK ou renomeá-lo para `environment_type` e acrescentar a identidade real; definir comparação integral do tuple e um caso negativo por componente.

---

### HIGH-03 — Contrato de adapters não está estritamente alinhado ao FDP-15

FDP-15 exige, para Engine Adapters, além da interface comum: `start_task`, `resume_task`, `pause_task`, `cancel_task`, `get_status`, `capture_checkpoint`, `get_artifacts`, `get_diff` e `get_test_results`.

F-012 exige apenas `describe`, `health`, `invoke`, `cancel` e reporta somente parte das operações adicionais. Seu teste `ADAPT-01` também cobre apenas health/invoke/unsupported/cancel desconhecido. Além disso, F-012 declara depender de F-011, embora seu próprio requisito de vault refs diga depender de F-006.

Evidências:

- [FDP-15:227](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/historical/round4/docs/planning/FDP-15-v1.0-INTEGRATION-ADAPTER-SPECIFICATION.md:227)
- [FDP-15:232](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/historical/round4/docs/planning/FDP-15-v1.0-INTEGRATION-ADAPTER-SPECIFICATION.md:232)
- [F-012:435](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-19A-v1.2-STORY-ACCEPTANCE-REGISTER.md:435)
- [F-012:440](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-19A-v1.2-STORY-ACCEPTANCE-REGISTER.md:440)
- [F-012:443](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-19A-v1.2-STORY-ACCEPTANCE-REGISTER.md:443)
- [Matriz ADAPT-01:56](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.2-CANONICAL.md:56)

Como FDP-15 ainda aguarda aprovação humana, a v1.2 não deve congelar seletivamente uma superfície menor e simultaneamente alegar compatibilidade com FDP-15.

---

### HIGH-04 — Papel do AIOX contradiz a arquitetura de fallback da fonte

A fonte FDP-06 estabelece AIOX como framework **preferencial** e determina que a arquitetura permita execução sem AIOX quando possível. F-013, porém, diz que o adapter AIOX é “the only supported orchestrator entry in the MVP” e que substituí-lo exige Change Decision.

Evidências:

- [FDP-06:372](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/historical/round4/docs/source-material/chat-extracts/FDP-06-v1.0__msg058.md:372)
- [FDP-06:407](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/historical/round4/docs/source-material/chat-extracts/FDP-06-v1.0__msg058.md:407)
- [F-013:478](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-19A-v1.2-STORY-ACCEPTANCE-REGISTER.md:478)

Impacto: “preferencial, não SPOF” e “única entrada suportada” são decisões arquiteturais diferentes.

Correção documental: caracterizar AIOX como adapter/orquestrador preferencial, mantendo um caminho Forge/engine direto ou fallback definido; reservar Change Decision para troca da preferência frozen, não para o funcionamento degradado já exigido pela fonte.

---

### HIGH-05 — A “única matriz de oráculos” não cobre integralmente critérios das histórias

FDP-17 afirma que cada caso da matriz contém fixture, **steps**, regra de aprovação e regra de falha. A matriz não possui coluna de passos. Mais importante: várias histórias apontam para testes cujo oracle não cobre toda a aceitação da história.

Exemplo verificável: F-016 exige validação dos digests do checkpoint, terminalização do attempt anterior, revogação de grants, criação do novo attempt e ausência de dois attempts não terminais. Seus IDs são `QUEUE-01` e `ENG-02`; a matriz cobre corrida de leases e preservação de escopo, mas não fornece um oracle completo para corrupção de checkpoint e recuperação de handoff.

Evidências:

- [FDP-17:34](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-17-v1.2-TESTING-STRATEGY.md:34)
- [F-016:590](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-19A-v1.2-STORY-ACCEPTANCE-REGISTER.md:590)
- [F-016:604](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-19A-v1.2-STORY-ACCEPTANCE-REGISTER.md:604)
- [Matriz ENG-02:19](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.2-CANONICAL.md:19)
- [Matriz QUEUE-01:29](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.2-CANONICAL.md:29)

Correção documental: criar IDs/oráculos próprios para checkpoint/handoff/recovery ou declarar a aceitação da história como autoridade complementar. A formulação atual — “oráculos somente na matriz” — deixa requisitos sem autoridade de teste.

---

### HIGH-06 — Rastreabilidade das 41 histórias continua circular ou genérica

As aceitações estão muito mais individualizadas do que no Round 4, mas a linha `Source` de praticamente todas as histórias aponta apenas para o índice v1.2 e para as linhas de teste da própria matriz v1.2. Não aponta para FDP-06/10/12/13/14/15, seção ou linha que originou cada requisito.

Exemplo:

- [F-001:18](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-19A-v1.2-STORY-ACCEPTANCE-REGISTER.md:18)
- [F-012:438](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-19A-v1.2-STORY-ACCEPTANCE-REGISTER.md:438)
- [F-039:1446](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-19A-v1.2-STORY-ACCEPTANCE-REGISTER.md:1446)

Isso deixa a auditoria de fidelidade dependente de reconstrução manual e permite que requisitos novos pareçam herdados das fontes.

Correção documental: por história, distinguir `Fonte aprovada`, `FDP-14 pendente`, `FDP-15 pendente` e `proposta nova v1.2`, com seção/linha.

## Findings MEDIUM

### MEDIUM-01 — `Build` e `Attempt` não têm matrizes exaustivas equivalentes à de `Task`

Há uma matriz completa para os 11 estados de `Task`, mas Build e Attempt são descritos em prosa. A descrição de Build não esclarece todas as saídas de `AWAITING_APPROVAL`, retorno de `CHANGES_REQUESTED`, desbloqueio ou comportamento terminal. Para Attempt, “watchdog pode marcar qualquer não terminal como TIMED_OUT ou LOST” conflita semanticamente com estados ainda não executantes, como `CREATED`.

Evidência: [FDP-16A:239](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-16A-v1.2-EXECUTION-CONTRACTS.md:239).

### MEDIUM-02 — Schema comum produz ambiguidade de identidade

“Every durable aggregate includes `id`”, mas os schemas específicos introduzem `build_id`, `task_id`, `attempt_id` etc. Somente `build_id` declara explicitamente ser igual a `id`; os demais não dizem se são aliases, colunas duplicadas ou substitutos.

Evidência: [FDP-16A:19](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-16A-v1.2-EXECUTION-CONTRACTS.md:19).

### MEDIUM-03 — Recovery de efeito externo ambíguo presume API de receipt

Após crash pós-dispatch, a ação prescrita é “reconcile with the provider receipt API”. FDP-15 admite providers heterogêneos; não está definido o procedimento quando o provider não oferece consulta idempotente/receipt.

Evidência: [FDP-16A:295](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-16A-v1.2-EXECUTION-CONTRACTS.md:295).

É necessário definir um estado/manual gate terminal ou uma capability declarada de reconciliação, mantendo a proibição de redispatch cego.

### MEDIUM-04 — Conjunto requerido para `READY_FOR_HUMAN_TEST` não está realmente enumerado

F-039 afirma que o conjunto requerido está “listed explicitly in FDP-20”. FDP-20 lista histórias por sprint, mas não fornece uma lista normativa inequívoca de quais são “required MVP tasks”, especialmente com P2 e itens opcionais.

Evidências:

- [F-039:1454](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-19A-v1.2-STORY-ACCEPTANCE-REGISTER.md:1454)
- [FDP-20:10](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-20-v1.2-SPRINT-IMPLEMENTATION-PLAN.md:10)

### MEDIUM-05 — As 41 histórias ainda não estão `Ready` para execução

Todas possuem papel, classe relativa e razão, mas pessoa, horas e timebox continuam pendentes. Isso é honesto e não invalida a qualidade dos critérios técnicos; impede, porém, alegar DoR operacional completo ou planejamento de capacidade concluído.

Evidências:

- [FDP-19A:6](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-19A-v1.2-STORY-ACCEPTANCE-REGISTER.md:6)
- [FDP-20:35](C:/Users/User/AppData/Local/Temp/ia-os-forge-round5-codex-independent/docs/planning/FDP-20-v1.2-SPRINT-IMPLEMENTATION-PLAN.md:35)

## Resultado C01–C08

| Controle | Resultado independente | Conclusão |
|---|---|---|
| C01 — contratos | **PARCIAL / FAIL** | Tipos, nullability, envelopes, 11 estados de Task, retry, lease e fencing melhoraram; ledger, approval tuple, recovery ambígua e matrizes Build/Attempt continuam incompletos. |
| C02 — 41 DoR/DoD | **PARCIAL** | 41/41 presentes e critérios positivos/negativos são majoritariamente específicos. Falham a rastreabilidade literal, algumas dependências e a correspondência integral com a matriz única. Pessoas/timeboxes seguem abertos. |
| C03 — semântica e 17 P0 | **PASS documental** | Os 17 IDs estão preservados. `AUTHZ-01`, `SEC-01` e `COST-01` recuperaram seu significado. Nenhum teste foi executado. |
| C04 — links/versionamento | **PASS** | A matriz v1.2 está estabelecida como única matriz candidata; versões antigas estão isoladas em `historical/round4`. |
| C05 — oráculos reais | **PARCIAL / FAIL** | Os oráculos deixaram de ser genéricos e são úteis, mas não há steps explícitos e há requisitos de histórias sem oracle correspondente. |
| C06 — runbooks A/B/C | **PASS documental** | A separação é correta e proporcional. Classe B/C pode e deve ser gateada para pós-BUILD/staging sem bloquear a escrita da Classe A. |
| C07 — least privilege/crash/TOCTOU/ciclos | **PARCIAL / FAIL** | Direção de autoridade, fencing e crash points estão descritos. Persistem lacunas em aprovação integral, settlement, reconciliação sem receipt e contradição do papel AIOX. |
| C08 — metadados | **PASS** | Títulos, estado candidato, ausência de aprovação e `NOT RUN` estão claros. |

## Pontos confirmados como adequados

- Os 11 estados de Task correspondem a FDP-12.
- `CLAIMED_DONE` não é status persistido.
- `attempt_id` foi corretamente excluído da chave de idempotência.
- Retry tem defaults versionados, taxonomia e exaustão explícita.
- Lease acquire, epoch e stale-writer denial estão suficientemente especificados para iniciar implementação após as correções.
- `AUTHZ-01` é isolamento de organização; `AUTHZ-02`, de projeto.
- `SEC-01` usa canário e sinks definidos.
- `COST-01` pertence a F-015; F-021 é somente dashboard.
- Frozen/P1/deferred reproduz FDP-10, inclusive os nove spikes.
- FDP-14 e FDP-15 permanecem corretamente sem aprovação presumida.
- Classe B e C dos runbooks não devem bloquear prontidão documental nem BUILD de hooks Classe A; bloqueiam certificação operacional e produção.
- Não há versões concorrentes da matriz na baseline candidata.
- Não identifiquei evidência de aprovação humana simulada.

## Condições para um Founder gate documental

Antes de considerar `PASS WITH CONDITIONS` ou `PASS` para a baseline:

1. Fechar HIGH-01 com protocolo transacional completo de reserva, settlement, liberação e recovery.
2. Fechar HIGH-02 com tuple de deployment integral e oráculos negativos por componente.
3. Reconciliar F-012 com toda a interface de Engine Adapter do FDP-15 e corrigir suas dependências.
4. Reconciliar o papel do AIOX com a regra “preferencial, não ponto único de falha”.
5. Cobrir na matriz todos os critérios normativos das histórias ou alterar formalmente a regra de autoridade dos oráculos.
6. Inserir rastreabilidade literal por história, distinguindo fonte aprovada, documento pendente e proposta nova.
7. Enumerar o conjunto normativo de tarefas requerido por F-039.
8. Manter FDP-14 como “confirmação pendente” e FDP-15 como “aprovação pendente”; nenhuma aprovação pode ser inferida deste parecer.
9. Nomear responsáveis e calibrar timeboxes antes de declarar as histórias `READY` para execução. Isso pode ocorrer depois da correção técnica da baseline, mas antes da autorização de capacidade/BUILD.

## O que pertence a implementação ou staging — não à correção documental atual

Não são condições para aprovar a qualidade documental:

- executar SPIKE-01…09;
- implementar serviços, migrations, adapters ou UI;
- obter PASS nos 17 P0;
- demonstrar lease/fencing em concorrência real;
- executar providers reais;
- medir latência, HIR ou TFV;
- preencher thresholds, queries, RPO/RTO e on-call da Classe B;
- criar scripts operacionais finais;
- executar drills Classe C;
- realizar restore, rollback ou deploy;
- certificar `READY_FOR_HUMAN_TEST` ou produção.

Esses itens devem permanecer `NOT RUN` até autorização explícita de BUILD-00 e, quando aplicável, staging.

## Nota sobre a checagem automática

Não tratei `check_round5_consistency.py` como teste do produto nem como prova de fechamento. A tentativa de executá-lo foi recusada pela política read-only do ambiente; o relatório existente informa zero erros textuais, mas o próprio relatório admite que o script não avalia suficiência semântica de oráculos, implementação, RPO/RTO ou aprovações. Os findings acima são independentes dessas contagens.

**Conclusão:** a v1.2 está significativamente mais madura e pode ser corrigida sem reabrir o stack ou exigir ensaios prematuros. Contudo, os `HIGH` restantes afetam contratos que implementadores e revisores usariam como autoridade. Portanto, o parecer proporcional para **PRONTIDÃO DOCUMENTAL** é **FAIL**, sem qualquer inferência sobre aprovação do Founder e sem julgamento de prontidão operacional.