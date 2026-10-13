# Parecer independente — IA OS Forge Round 6

**Commit auditado:** `4e5783974ca27595c9592e2e6ac55ab23fcbeb5a`  
**Veredito de prontidão documental:** **FAIL**  
**Prontidão operacional:** **NÃO ATINGIDA / NÃO AVALIADA**

A v1.3 corrige substancialmente a v1.2 e fecha de modo satisfatório cinco dos seis findings HIGH e os cinco MEDIUM do Round 5. Entretanto, o protocolo financeiro ainda possui uma lacuna impeditiva de concorrência e uma inconsistência no caminho de reconciliação manual. Por isso, HIGH-01 permanece parcialmente aberto.

O `FAIL` é exclusivamente documental. Não resulta da ausência de software, testes, spikes ou staging drills.

## Findings

| ID | Severidade | Situação | Evidência e conclusão |
|---|---|---|---|
| HIGH-01 | **HIGH** | **PARCIALMENTE ABERTO** | A seção 8A agora cobre reserva, settlement, liberação, custo divergente, crash, estados terminais e reserva concorrente. Porém, só a reserva determina explicitamente lock/controle concorrente ([FDP-16A:306](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-16A-v1.3-EXECUTION-CONTRACTS.md:306), [FDP-16A:313](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-16A-v1.3-EXECUTION-CONTRACTS.md:313)). Não há regra de lock, CAS ou isolamento para duas liquidações concorrentes nem para a corrida `RecordReceipt` × `ReleaseReservation`. A declaração “at most one settlement” não define como o segundo writer é impedido. LEDGER-01 testa segunda liquidação sequencial e LEDGER-06 somente reserva concorrente ([matriz:61](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.3-CANONICAL.md:61), [matriz:66](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.3-CANONICAL.md:66)). |
| NEW-HIGH-07 | **HIGH**, associado a HIGH-01 | **ABERTO** | O catálogo autoriza `RecordReceipt` e `ReleaseReservation` somente para `system`, sem `evidence_ref` no payload ([FDP-16A:202](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-16A-v1.3-EXECUTION-CONTRACTS.md:202), [FDP-16A:203](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-16A-v1.3-EXECUTION-CONTRACTS.md:203)). A máquina financeira, porém, prescreve esses comandos por humano e com evidence ref quando `BLOCKED_RECONCILIATION` ([FDP-16A:338](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-16A-v1.3-EXECUTION-CONTRACTS.md:338), [FDP-16A:339](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-16A-v1.3-EXECUTION-CONTRACTS.md:339)). As duas definições não podem ser implementadas simultaneamente sem interpretação adicional. |
| HIGH-02 | — | **FECHADO** | O tuple contém os dez campos, incluindo `approver_actor_ref`; `environment_id` é identidade UUID distinta de `environment_class` ([FDP-16A:140](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-16A-v1.3-EXECUTION-CONTRACTS.md:140), [FDP-16A:152](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-16A-v1.3-EXECUTION-CONTRACTS.md:152), [FDP-16A:347](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-16A-v1.3-EXECUTION-CONTRACTS.md:347)). DEPLOY-02 e DEPLOY-04…12 fornecem negativo por campo; DEPLOY-12 cobre identidade distinta do aprovador ([matriz:75](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.3-CANONICAL.md:75)). |
| HIGH-03 | — | **FECHADO documentalmente** | F-012 e ADAPT-01 incluem os nove métodos literais do FDP-06/FDP-15, além da interface comum, e proíbem emulação silenciosa ([F-012:517](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-19A-v1.3-STORY-ACCEPTANCE-REGISTER.md:517), [F-012:524](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-19A-v1.3-STORY-ACCEPTANCE-REGISTER.md:524), [matriz:57](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.3-CANONICAL.md:57)). Isso coincide com FDP-06 linhas 353–361 e FDP-15 linhas 230–238. **Não implica aprovação do FDP-15.** |
| HIGH-04 | — | **FECHADO** | AIOX está definido como preferencial, não exclusivo, com fallback `FORGE_DIRECT` limitado a `NONE/INTERNAL`; deploy e efeitos externos permanecem negados ([FDP-16:6](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-16-v1.3-AIOX-EXECUTION-ENGINES.md:6), [F-013:570](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-19A-v1.3-STORY-ACCEPTANCE-REGISTER.md:570), [matriz:59](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.3-CANONICAL.md:59)). Está alinhado literalmente com FDP-06 linhas 372 e 407–409. |
| HIGH-05 | — | **FECHADO, com ressalva do ledger** | As 79 linhas possuem fixture, Steps, positivo e negativo. HANDOFF-01 cobre corrupção, grants, terminalização, novo attempt e crash ([matriz:60](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.3-CANONICAL.md:60)). Foram acrescentados AIOX-01, REVIEW-01, CTX-01, BRIDGE-01 e ENGINE-ALLOW-01. A insuficiência restante é específica ao HIGH-01: falta corrida settlement/release. |
| HIGH-06 | — | **FECHADO** | As 41 histórias distinguem requisito herdado, fonte pendente e proposta nova. Exemplos: adapter/FDP-15 ([F-012:517](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-19A-v1.3-STORY-ACCEPTANCE-REGISTER.md:517)); ledger como proposta Round 6 ([F-015:656](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-19A-v1.3-STORY-ACCEPTANCE-REGISTER.md:656)); tuple ([F-029:1277](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-19A-v1.3-STORY-ACCEPTANCE-REGISTER.md:1277)). As citações amostradas foram confirmadas nos extratos literais disponíveis. |
| M01 | MEDIUM anterior | **FECHADO** | Há matrizes completas e separadas para Task, Attempt e Build; watchdog não expira CREATED/QUEUED e Build usa `blocked_from` ([FDP-16A:239](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-16A-v1.3-EXECUTION-CONTRACTS.md:239), [FDP-16A:260](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-16A-v1.3-EXECUTION-CONTRACTS.md:260)). |
| M02 | MEDIUM anterior | **FECHADO** | A regra de identidade declara `id` como PK e os identificadores específicos como colunas geradas iguais a `id`; `operation_ref` permanece chave de negócio ([FDP-16A:33](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-16A-v1.3-EXECUTION-CONTRACTS.md:33)). |
| M03 | MEDIUM anterior | **FECHADO** | `receipt_query` pode ser `SUPPORTED` ou `ABSENT`; ausência leva a `BLOCKED_RECONCILIATION`, mantém reserva e proíbe redispatch ([FDP-16A:352](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-16A-v1.3-EXECUTION-CONTRACTS.md:352)). Resta apenas a inconsistência de ator/payload registrada acima. |
| M04 | MEDIUM anterior | **FECHADO** | O conjunto de 33 histórias requerido para `READY_FOR_HUMAN_TEST` está enumerado, assim como as exclusões ([FDP-20:43](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-20-v1.3-SPRINT-IMPLEMENTATION-PLAN.md:43)). |
| M05 | MEDIUM anterior | **FECHADO no texto / pendência operacional** | Há 41 blocos de DoR operacional e todos dizem `Not met`, mantendo pessoa, horas e timebox pendentes ([F-001:38](C:/Users/User/AppData/Local/Temp/ia-os-forge-round6-codex-independent/docs/planning/FDP-19A-v1.3-STORY-ACCEPTANCE-REGISTER.md:38)). Não bloqueia a revisão técnica; bloqueia declarar histórias READY ou autorizar capacidade/BUILD. |

## Resultado C01–C08

| Controle | Resultado |
|---|---|
| C01 — contratos | **PARCIAL / FAIL**. Schemas e máquinas melhoraram, mas o ledger ainda não define serialização de settlement/release e contradiz o ator da reconciliação manual. |
| C02 — 41 histórias | **PASS documental técnico**. 41/41 presentes, individualizadas e com DoR técnico/operacional separado. **Não estão operacionalmente READY.** |
| C03 — semântica e 17 P0 | **PASS documental**. Os 17 IDs e sentidos literais de FDP-13 linhas 2272–2288 foram preservados, uma linha cada. Nenhum está executado. |
| C04 — links/versionamento | **PASS**. v1.3 é a única matriz candidata; v1.2 e v1.1 estão históricas. |
| C05 — oráculos reais | **PARCIAL / FAIL** apenas pelo caso concorrente financeiro ausente. Nos demais pontos, há fixture, Steps e regras positivas/negativas. |
| C06 — runbooks A/B/C | **PASS documental**. Classe A está especificada; B e C continuam corretamente abertas para staging/produção. |
| C07 — least privilege/crash/TOCTOU | **PARCIAL / FAIL** pelo ledger. Aprovação de deploy, fencing, fallback AIOX, handoff e providers sem receipt estão adequadamente restringidos. |
| C08 — metadados | **PASS**. Todos os normativos declaram DRAFT, NOT APPROVED, NOT READY FOR BUILD, testes/drills não executados e nenhuma aprovação inferida. |

## Verificações documentais

Somente verificações read-only foram realizadas:

- HEAD confirmado diretamente em `.git/refs/heads/main`: commit solicitado.
- Nove normativos v1.3 identificados.
- 41 histórias `F-001…F-041`.
- 41 blocos de DoR operacional e 41 declarações `Not met`.
- Matriz com 79 oráculos mais 41 linhas do índice, totalizando 120 linhas identificadas.
- 17 P0 conferidos contra FDP-13 literal.
- 11 estados de Task conferidos: `QUEUED`, `READY`, `RUNNING`, `WAITING`, `RETRYING`, `HANDOFF`, `REVIEWING`, `BLOCKED`, `COMPLETED`, `FAILED`, `CANCELLED`.
- FDP-06 e FDP-15 históricos conferidos para interface de adapter e AIOX preferencial/fallback.
- Nenhum teste de software, gerador, spike, provider ou drill foi executado.
- O repositório não contém checker específico de Round 6; o checker existente é fixado à v1.2 e não foi tratado como evidência da v1.3.

## Gates e ações necessárias

Para sair de `FAIL` documental:

1. Definir uma única transação serializável para `RecordReceipt` e `ReleaseReservation`, incluindo lock/CAS sobre Operation, Reservation e Build, ou mecanismo equivalente inequivocamente normativo.
2. Definir o resultado da corrida:
   - dois receipts simultâneos;
   - receipt versus release/refund;
   - dois releases;
   - retry após o vencedor ter cometido.
3. Acrescentar oracle concorrente que prove exatamente um movimento monetário e um estado terminal.
4. Harmonizar o catálogo com a reconciliação manual: ator autorizado, payload com `evidence_ref`, política de autenticação e evento de auditoria.
5. Repetir a checagem de cobertura sem declarar testes executados.

Após essas correções, a baseline poderá ser reavaliada para `PASS WITH CONDITIONS` ou `PASS` documental.

## Ressalvas

- Este parecer **não aprova FDP-14 nem FDP-15**.
- Não registra ou presume aprovação do Founder.
- Não autoriza BUILD-00, sprint, capacidade, implementação ou deploy.
- Não exige staging drills, RPO/RTO medidos, nomes de on-call ou testes executados para corrigir o planejamento documental.
- Classes B/C, testes P0, spikes, restore e rollout continuam gates operacionais posteriores.
- O tuple de `DeploymentApproval`, inclusive `approver_actor_ref`, foi considerado documentalmente completo; isso não significa que qualquer aprovação humana exista.
- A baseline Round 6 é significativamente melhor que a Round 5. O `FAIL` remanescente é estreito, mas proporcional à criticidade de dupla contabilização ou liberação incorreta sob concorrência.