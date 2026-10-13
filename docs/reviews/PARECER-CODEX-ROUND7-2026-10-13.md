# Parecer independente — IA OS Forge Round 7

**Data da revisão:** 13 de outubro de 2026  
**Commit imutável auditado:** `decef2809b61d3f1fe84bef74a5162d782cc6231`  
**Modalidade:** verificação documental read-only; nenhum arquivo alterado, nenhum teste de produto, build, banco, provider ou staging executado.

## Veredito executivo

| Dimensão | Veredito |
|---|---|
| Prontidão documental | **FAIL** |
| Prontidão operacional | **NÃO ATINGIDA / NÃO AVALIADA** |
| HIGH-01 do Round 6 | **PARCIALMENTE FECHADO** |
| NEW-HIGH-07 do Round 6 | **PARCIALMENTE FECHADO** |
| Recomendação ao gate documental do Founder | **NÃO APROVAR ainda a baseline v1.4** |

A v1.4 resolve de forma substancial a deficiência mecânica apontada no Round 6: agora existe uma transação única, ordem explícita de locks, unicidade do movimento monetário, resultados de vencedor/perdedor, idempotência do `command_id`, atomicidade com audit/outbox e oráculos concorrentes.

Contudo, permanecem duas lacunas documentais de severidade HIGH:

1. A corrida `RecordReceipt` × `ReleaseReservation` aceita por contrato que uma liberação por “no effect” vença mesmo diante de um receipt válido com custo real, apenas por adquirir o lock primeiro. Isso garante unicidade, mas não garante correção contábil diante de provas contraditórias.
2. A reconciliação humana considera confiável uma “evidence row” essencialmente por escopo, digest e classe de autor. Não há contrato para captura, autenticação forte, origem verificável ou vinculação da evidência ao receipt/provider/operation. Um digest prova imutabilidade, não veracidade. Assim, o texto ainda não impede documentalmente evidência fictícia produzida por um operador.

O `FAIL` é exclusivamente documental. Não se baseia na ausência de implementação ou de testes executados.

## Escopo documental revisado

Foram examinados diretamente:

- [Parecer Codex Round 6](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/reviews/PARECER-CODEX-ROUND6-2026-10-13.md:1).
- [FDP-16A v1.4](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md:1).
- [FDP-19A v1.4, inclusive F-015](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-19A-v1.4-STORY-ACCEPTANCE-REGISTER.md:645).
- [Matriz canônica v1.4](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.4-CANONICAL.md:1).
- [Índice oficial Round 7](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-ROUND7-STATUS-INDEX.md:1).
- FDP-16 v1.4, FDP-17 v1.4 e FDP-19 v1.4.
- FDP-18 v1.3, FDP-18A v1.3 e FDP-20 v1.3.
- As versões v1.3 correspondentes em `historical/round6/docs/planning`.
- [FDP-12 histórico](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/historical/round4/docs/source-material/chat-extracts/FDP-12-v1.0__msg074.md:1) e [FDP-13 histórico](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/historical/round4/docs/source-material/chat-extracts/FDP-13-v1.0__msg077.md:1).
- ROUND7 Change Report, Finding Closure, Consistency Report e Open Pendencies.
- Prompt de fechamento Round 7 e protocolo de revisão.

O HEAD foi confirmado pela leitura direta de `.git/HEAD` e `.git/refs/heads/main` como o commit fixado acima.

## Findings

| ID | Severidade | Resultado | Evidência e conclusão |
|---|---:|---|---|
| HIGH-01 | HIGH | **PARCIALMENTE FECHADO** | O mecanismo de serialização está agora bem definido, mas a semântica da corrida receipt × release continua insegura diante de provas contraditórias. |
| NEW-HIGH-07 | HIGH | **PARCIALMENTE FECHADO** | A separação humano/sistema foi corrigida, mas a confiança e a origem da evidência continuam insuficientemente especificadas. |
| NEW-HIGH-08 | HIGH | **ABERTO** | Um receipt válido pode perder para uma liberação “no effect” apenas pela ordem do lock, resultando em gasto real não contabilizado. |
| NEW-HIGH-09 | HIGH | **ABERTO** | Não existe contrato normativo que impeça um `security_operator` de criar evidência arbitrária, atribuir-lhe digest e usá-la para reconciliação. |
| NEW-MEDIUM-10 | MEDIUM | **ABERTO** | Replay/idempotência e duplicação de autorizações manuais não estão completamente definidos nem cobertos por LEDGER-11/12. |
| NEW-MEDIUM-11 | MEDIUM | **ABERTO** | O armazenamento do receipt/custo pendente após bloqueio por `actual > estimate` não está normalizado suficientemente para sustentar decisões concorrentes posteriores. |
| Q01 | MINOR | **ABERTO** | O Change Report Round 7 contém o hash do Round 6 como “commit auditado pelo Codex”. |

## HIGH-01 — análise independente

### Aspectos fechados satisfatoriamente

A ordem normativa é Build → Operation → Reservation → ManualReconciliation, sem inversão, em [FDP-16A:352–361](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md:352). Todos os comandos financeiros relevantes usam a mesma ordem, inclusive `DispatchOperation` e `BlockReconciliation` ([linha 363](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md:363)).

Depois dos locks, o contrato exige releitura da operação e da tabela de movimentos. Movimento existente prevalece sobre versão stale, produzindo `409 ALREADY_SETTLED` ou `409 ALREADY_RELEASED`; conflito sem movimento retorna `409 VERSION_CONFLICT` ([linhas 365–371](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md:365)).

A unicidade de `operation_id` e `command_id`, e o rollback conjunto do contador quando o insert do movimento falha, estão explícitos em [FDP-16A:375–380](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md:375).

O mesmo commit inclui movimento, contadores, audit e outbox. Crash anterior ao commit não deixa nenhum deles; replay do mesmo `command_id` retorna `200 IDEMPOTENT_REPLAY` ([linhas 382–382](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md:382)).

Os resultados mecânicos das corridas estão especificados:

- Dois receipts: um settlement, perdedor `409 ALREADY_SETTLED` ([linha 388](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md:388)).
- Receipt × release: um movimento terminal ([linha 389](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md:389)).
- Duas releases: uma única redução de reserva ([linha 390](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md:390)).
- Retry tardio: replay idempotente ou erro terminal, sem redispatch ([linha 391](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md:391)).

Para custo real maior que a estimativa, a fórmula correta é `spent + reserved - estimate + actual <= limit`. Se ela falha, não há movimento nem aumento falso de `spent`, e a reserva permanece HELD ([linhas 322–325](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md:322), [395](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md:395)).

### HIGH remanescente: receipt × release

LEDGER-08 cria deliberadamente um receipt com `actual=30` e uma liberação com alegada prova de no effect, aceitando tanto SETTLED quanto RELEASED conforme o vencedor do lock ([matriz:69](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.4-CANONICAL.md:69)).

Isso prova exclusão mútua, mas não correção financeira. Se o receipt é autêntico, a operação produziu efeito e o custo deve ser registrado. Deixar a liberação vencer pode produzir `RELEASED`, `spent=800`, seguido de rejeição do receipt, embora exista gasto real de 30. Se as duas provas são contraditórias, a resolução segura é preservar/bloquear para reconciliação de conflito ou estabelecer precedência verificável do receipt, não escolher por timing.

Portanto, HIGH-01 está fechado quanto a double-spend/double-release, mas não integralmente quanto à semântica contábil da corrida.

## NEW-HIGH-07 — análise independente

### Aspectos fechados satisfatoriamente

O conflito de ator da v1.3 foi removido:

- `RecordReceipt` e `ReleaseReservation` continuam exclusivos do sistema e são ilegais a partir de `BLOCKED_RECONCILIATION` ([FDP-16A:203–204](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md:203)).
- O humano usa exclusivamente `ApproveManualReconciliation`; ele não move dinheiro ([linha 206](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md:206)).
- `PROVEN_RECEIPT` exige confirmação por outro `security_operator`, com `403 SELF_CONFIRM` para o primeiro operador ([linha 207](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md:207)).
- Somente `ApplyAuthorizedReconciliation`, executado pelo sistema, consome a autorização e movimenta dinheiro ([linha 208](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md:208)).
- O Policy Service exige `ledger.reconcile` no mesmo organization/project; modelo, coding engine e adapter ficam fora da decisão ([linhas 404–410](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md:404)).
- Decisão ambígua é rejeitada; `evidence_ref` ausente, estrangeira, desconhecida ou sem digest não movimenta dinheiro ([linhas 406–407](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md:406)).
- A matriz distingue autorização, confirmação e apply, sem gasto humano antecipado ([matriz:72–73](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.4-CANONICAL.md:72)).

### HIGH remanescente: origem e veracidade da evidência

O contrato define como “confiável” uma evidência pré-existente no mesmo escopo, com `content_digest`, desde que o autor não seja `coding_engine` ou adapter ([FDP-16A:407](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md:407)). LEDGER-11 materializa essa regra usando E1 cuja única qualificação expressa é “digest e author class security_operator” ([matriz:72](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.4-CANONICAL.md:72)).

Não estão definidos:

- schema e tipo da prova — receipt assinado, extrato do provider, consulta independente ou outro artefato;
- vínculo imutável da evidência com `operation_id`, provider, valor e moeda;
- serviço ou ator autorizado a ingerir a prova;
- autenticação forte/frescor da sessão do operador;
- validação criptográfica ou independente da origem;
- proibição de o operador que aprova criar a própria evidência;
- tratamento de evidência contraditória posterior.

Logo, um operador pode, documentalmente, criar conteúdo arbitrário, gerar seu digest e usá-lo para `PROVEN_NO_EFFECT`; um segundo operador pode confirmar conteúdo igualmente não autenticado em `PROVEN_RECEIPT`. O dual control reduz abuso unilateral, mas não converte afirmação humana em prova de provider.

Essa lacuna contraria a exigência específica do Round 7 de não permitir evidência fictícia. NEW-HIGH-07 permanece parcialmente aberto.

## Oráculos LEDGER-07…12

| Oracle | Avaliação |
|---|---|
| LEDGER-07 | **PASS documental.** Dois receipts, um movimento, um evento e contadores exatos. |
| LEDGER-08 | **FAIL semântico.** Prova exclusão mútua, mas aceita RELEASED apesar de receipt válido concorrente. |
| LEDGER-09 | **PASS documental.** Duas releases reduzem a reserva uma vez. |
| LEDGER-10 | **PASS documental.** Distingue mesmo `command_id` de novo `command_id` e proíbe redispatch. |
| LEDGER-11 | **PARCIAL.** Cobre ator, evidência ausente, evidência de engine, comando sistêmico indevido e apply de no-effect; não cobre origem autêntica da prova, evidência foreign/digest-null, replay de aprovação nem dupla autorização. |
| LEDGER-12 | **PARCIAL.** Cobre segundo operador, self-confirm, ausência de movimento antes do apply e decisão ambígua; não cobre confirmer sem capability, evidence_ref divergente, apply humano, duplo apply, replay de approve/confirm ou autorização duplicada. |

A cobertura 07–12 é suficiente para demonstrar a arquitetura escolhida, mas ainda não é completa para os riscos específicos acima.

## Idempotência e autorizações manuais

`ManualReconciliation.command_id` é único e uma operação pode ter no máximo uma autorização `AWAITING_CONFIRM` ou `AUTHORIZED` ([FDP-16A:411–413](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md:411)). Após apply, a operação terminal e o movimento único impedem novo efeito monetário.

Ainda assim, falta especificar expressamente:

- resultado do replay do mesmo `command_id` em Approve e Confirm;
- resultado de uma segunda autorização igual, não apenas de uma “different decision”;
- idempotência do Confirm;
- oracle para segundo Apply com o mesmo e com novo `command_id`;
- comportamento quando o confirmer repete evidence_ref diferente ou perde capability antes da confirmação.

É uma lacuna MEDIUM, pois os locks e o estado terminal evitam segundo movimento, mas deixam respostas e trilha de autorização abertas à interpretação.

## Contagens e preservação histórica

Verificação independente:

- **85 IDs de oráculo**, não 126. As 126 linhas reconhecidas pelo padrão consistem em **85 oráculos + 41 linhas do story index**. A própria matriz separa o índice como “not a second oracle” ([matriz:97](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.4-CANONICAL.md:97)).
- **41 histórias**, F-001…F-041.
- **17 P0 históricos**, exatamente AUTH-01 até STOP-01 nas linhas 10–26 da matriz. Seus IDs e intents coincidem literalmente com FDP-13 linhas 2272–2288 ([fonte FDP-13](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/historical/round4/docs/source-material/chat-extracts/FDP-13-v1.0__msg077.md:2272)).
- F-015 referencia COST-01, LEDGER-01…12 e IDEM-01 ([F-015:651](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-19A-v1.4-STORY-ACCEPTANCE-REGISTER.md:651)).
- A v1.3 permanece sob `historical/round6`; a alteração substantiva da v1.4 está concentrada no ledger e F-015.
- FDP-18, FDP-18A e FDP-20 permanecem como v1.3.
- As histórias continuam com DoR operacional não atendido; não estão READY para sprint/build.
- Todos os oráculos continuam `NOT RUN`, sem evidência de execução.

Não identifiquei regressão CRITICAL nas áreas preservadas de Task/Attempt/Build, AIOX, deploy tuple, isolamento, handoff ou estados.

## Qualificações menores e não bloqueantes

O [Round 7 Change Report:4](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/reviews/ROUND7-CHANGE-REPORT-2026-10-13.md:4) declara como “commit auditado pelo Codex” o hash `4e578...`, que é a baseline Round 6, e não o commit Round 7 efetivamente auditado aqui. É erro de metadado e deve ser corrigido, mas não é a causa do `FAIL`.

A frase “winner is whichever transaction acquires the operation lock first” ([FDP-16A:384](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md:384)) é imprecisa, pois o Build é bloqueado antes da Operation. O resultado ainda é serializado, mas a redação deveria dizer “a primeira transação que avança pela ordem normativa de locks”.

O modelo possui `external_receipt`, mas não normaliza um `pending_actual_minor` ou estrutura equivalente para o receipt bloqueado por excesso de orçamento ([FDP-16A:93–97](C:/Users/User/AppData/Local/Temp/ia-os-forge-round7-codex-independent/docs/planning/FDP-16A-v1.4-EXECUTION-CONTRACTS.md:93)). Isso torna menos verificável a afirmação posterior de que uma release concorrente “vê” custo positivo.

## O que pode legitimamente ficar para BUILD/staging

Não é necessário executar software para aprovar completude documental. Podem permanecer posteriores ao gate documental:

- implementação PostgreSQL e validação real de `FOR UPDATE`, constraints e `40001`;
- testes LEDGER-01…12 e demais 85 oráculos;
- testes de crash entre movimento, audit e outbox;
- medição de contention/deadlocks;
- integração com providers e assinatura real de receipts;
- classes B/C, RPO/RTO, restore e drills;
- calibração de horas, pessoas e timeboxes;
- métricas HIR/TFV e PERF-01;
- evidências reais e resultados de staging.

O que não pode ser deferido é decidir a semântica normativa para provas contraditórias e definir o contrato de confiança da evidência humana. São escolhas de segurança e contabilidade, não detalhes de implementação.

## Ações documentais necessárias

Para habilitar nova decisão de gate:

1. Alterar a corrida receipt × release para que uma prova de receipt válida não possa ser anulada por timing. Provas contraditórias devem ir para estado de conflito/reconciliação, ou deve existir precedência normativa baseada em verificação de origem.
2. Definir o schema da evidência de reconciliação: `operation_id`, provider, receipt/provider reference, valor, moeda, origem, digest, assinatura/attestation quando disponível e ator/serviço de captura.
3. Impedir que “conteúdo com digest escrito pelo mesmo operador” seja suficiente como prova. Estabelecer origem independente ou separação entre captor e aprovador.
4. Especificar autenticação forte e frescor para `ledger.reconcile`.
5. Completar idempotência de Approve/Confirm/Apply e duplicação de autorizações.
6. Ampliar LEDGER-11/12 para os negativos descritos acima.
7. Corrigir o hash no Round 7 Change Report.

## Recomendação ao Founder

**Não conceder PASS documental à baseline v1.4 neste commit.** Recomendo uma correção documental estreita, limitada aos dois findings HIGH e à cobertura associada; não há justificativa para reabrir os demais contratos ou criar uma rodada ampla por razões meramente procedurais.

Este parecer:

- **não aprova FDP-14 ou FDP-15**;
- **não registra nem presume aprovação do Founder**;
- **não autoriza BUILD-00, sprint, capacidade, implementação ou deploy**;
- **não exige testes de software para fechar a completude documental**;
- reconhece que a v1.4 fecha a maior parte técnica de HIGH-01 e elimina a contradição central de ator de NEW-HIGH-07, mas ainda não torna segura a semântica de conflito nem a confiança da evidência humana.