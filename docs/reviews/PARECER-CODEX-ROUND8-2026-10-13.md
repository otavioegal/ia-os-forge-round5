# Parecer independente — IA OS Forge Round 8

**Data:** 13 de outubro de 2026  
**Commit auditado:** `e70112905e60016600eb41566913f63025685a22`  
**Modalidade:** auditoria documental independente, estritamente read-only. Nenhum arquivo foi modificado; nenhum build, teste de produto, banco, provider ou staging foi executado.

## Veredito executivo

| Dimensão | Veredito |
|---|---|
| Prontidão documental v1.5 | **PASS WITH CONDITIONS** |
| HIGH-01 | **FECHADO** |
| NEW-HIGH-07 | **FECHADO** |
| NEW-HIGH-08 | **FECHADO** |
| NEW-HIGH-09 | **FECHADO** |
| NEW-MEDIUM-10 | **PARCIALMENTE FECHADO — condição não bloqueante** |
| NEW-MEDIUM-11 | **PARCIALMENTE FECHADO — condição não bloqueante** |
| Regressão Critical/High nova | **NÃO IDENTIFICADA** |
| Prontidão operacional | **NÃO AVALIADA / NÃO ATINGIDA** |
| Aprovação Founder | **NÃO CONCEDIDA NEM PRESUMIDA** |
| BUILD-00 | **NÃO AUTORIZADO** |

A baseline v1.5 fecha os quatro findings HIGH do parecer Round 7. A semântica agora é conservadora e independente da ordem do lock:

- receipt conclusivo contra no-effect conclusivo resulta em `CONFLICT`, nunca `RELEASED`;
- receipt conclusivo contra no-effect inconclusivo resulta em settlement, se o orçamento comportar;
- prova financeira é um `ProviderEffectProof` capturado exclusivamente por `forge.provider_ingest`;
- digest produzido pelo operador não constitui prova;
- prova `UNVERIFIED` não liquida, não libera e não autoriza;
- autor, capturador, confirmador e aplicador têm papéis separados;
- autenticação forte, frescor e capability são verificadas;
- replay e unicidade impedem segundo movimento monetário.

Restam duas imprecisões de cobertura/schema, ambas MEDIUM e corrigíveis sem reabrir a arquitetura. Elas justificam `PASS WITH CONDITIONS`, não `FAIL`.

## Escopo e autoridade documental

O HEAD foi confirmado pela leitura de [.git/refs/heads/main](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/.git/refs/heads/main:1).

Foram examinados:

- [Parecer Codex Round 7](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/reviews/PARECER-CODEX-ROUND7-2026-10-13.md:1);
- [FDP-16A v1.5](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:1), especialmente §§8A–8A.3;
- [F-015 v1.5](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-19A-v1.5-STORY-ACCEPTANCE-REGISTER.md:645);
- [matriz canônica v1.5](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.5-CANONICAL.md:1);
- FDP-16, FDP-17, FDP-19 e índice Round 8;
- os quatro relatórios Round 8;
- baseline histórica Round 7/v1.4;
- FDP-12 e FDP-13 originais;
- documentos preservados FDP-18, FDP-18A e FDP-20.

Há somente uma matriz no diretório normativo `docs/planning`: v1.5. As matrizes anteriores estão corretamente tratadas como históricas, conforme [matriz:3](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.5-CANONICAL.md:3).

## Fechamento individual dos findings

### HIGH-01 — FECHADO

A serialização financeira permanece definida por uma única transação, ordem fixa de locks e unicidade do movimento:

- ordem Build → Operation → Reservation → ManualReconciliation em [FDP-16A:358–364](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:358);
- releitura pós-lock e precedência da prova em [linhas 368–375](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:368);
- unicidade por `operation_id` e `command_id`, com rollback conjunto dos contadores, em [linhas 381–388](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:381).

A lacuna do Round 7 foi eliminada: o lock agora apenas serializa e não escolhe qual prova é verdadeira ([linha 390](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:390)).

### NEW-HIGH-08 — FECHADO

Receipt conclusivo e no-effect conclusivo produzem:

- nenhum movimento;
- ambas as provas preservadas;
- `BLOCKED_RECONCILIATION`;
- `reconciliation_state=CONFLICT`;
- reserva `HELD`;
- `spent` inalterado;
- `pending_actual_minor` derivado do receipt.

Isso está expresso em [FDP-16A:395–397](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:395) e [459](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:459).

LEDGER-08 agora falha expressamente se o resultado for `SETTLED`, `RELEASED` ou depender de quem obteve o lock primeiro ([matriz:69](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.5-CANONICAL.md:69)).

Prova tardia contraditória também não é descartada: o movimento anterior permanece, não há segundo movimento, mas a operação deixa de ser terminal incontestada e passa a conflito ([FDP-16A:405](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:405)).

### Receipt conclusivo × no-effect inconclusivo — PASS

A ordem normativa primeiro detecta receipt conclusivo e retorna `409 RECEIPT_PRECEDES_RELEASE`; uma alegação inconclusiva não pode liberar ([FDP-16A:373–375](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:373)).

LEDGER-13 exige settlement em 830/100, um único movimento e rejeita qualquer resultado `RELEASED` ([matriz:74](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.5-CANONICAL.md:74)).

### NEW-HIGH-07 — FECHADO

A separação de autoridade está suficientemente definida:

- `RecordReceipt` e `ReleaseReservation`: somente system;
- `ApproveManualReconciliation`: `security_operator`;
- `ConfirmManualReconciliation`: outro operador;
- `ApplyAuthorizedReconciliation`: somente system.

O catálogo e suas negativas estão em [FDP-16A:204–209](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:204).

O aprovador não pode ser o capturador; coding engine, adapter e reviewer não podem capturar; `ledger.reconcile` não permite inserir prova ([linhas 415 e 450](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:415)).

Sessões de operador devem ser `STRONG` e recentes, com `authenticated_at` dentro do limite configurado; sessão antiga retorna `401 SESSION_STALE` ([linha 416](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:416)).

### NEW-HIGH-09 — FECHADO

`ProviderEffectProof` passa a ser a única prova financeira durável; prosa humana acompanhada de digest é expressamente insuficiente ([FDP-16A:425–426](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:425)).

O schema vincula a prova a:

- `operation_id`;
- provider e referência externa;
- kind;
- moeda e valor;
- timestamps de provider/captura;
- serviço e ator capturador;
- origem e classe de confiança;
- digest;
- presença de attestation;
- estado de verificação;
- evento de proveniência.

Evidência: [FDP-16A:428–446](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:428).

`ATTESTED` exige uma attestation realmente recebida e validação contra chave previamente registrada; o sistema não pode inventá-la. `QUERY_CORROBORATED` exige consulta suportada e correspondência de operação, referência, moeda e valor ([linhas 452–455](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:452)).

`UNVERIFIED` é imóvel financeiramente: não liquida, não libera e não autoriza ([linha 455](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:455)). Na ausência de attestation e consulta, a reserva permanece `HELD` e nenhum write-off ocorre ([linha 463](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:463)).

LEDGER-11 cobre explicitamente digest de operador, autor capturador, prova estrangeira, digest nulo e coding engine ([matriz:72](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.5-CANONICAL.md:72)).

## Condições documentais remanescentes

### C-01 / NEW-MEDIUM-10 — cobertura incompleta de Confirm e revogação

**Severidade:** MEDIUM  
**Estado:** parcialmente fechado; não bloqueia o PASS documental condicionado.

O contrato normativo define:

- replay do mesmo `command_id` em Approve, Confirm e Apply;
- autorização duplicada;
- decisão/evidência conflitante;
- segundo Apply;
- capability revogada;
- expiração.

Evidência: [FDP-16A:417–423](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:417).

Entretanto, LEDGER-14 exercita apenas replay/duplicação de **Approve** e **Apply**. Não há passo de Confirm, replay do mesmo Confirm, novo `command_id` depois de confirmado ou revogação entre Confirm e Apply ([matriz:75](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.5-CANONICAL.md:75)).

Além disso, a frase do Apply — “the human capability used to authorize is still present” — não diz inequivocamente se, para `PROVEN_RECEIPT`, devem continuar válidas as capabilities do aprovador e do confirmador ([FDP-16A:419](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:419)).

**Correção precisa:**

1. Declarar que Apply de `PROVEN_RECEIPT` revalida `ledger.reconcile` tanto para `requested_by` quanto para `confirmed_by`.
2. Declarar o resultado quando qualquer um perde o grant: `403 CAPABILITY_REVOKED`, autorização não consumida, reserva `HELD`, nenhum movimento.
3. Ampliar LEDGER-14 ou criar novo oracle para:
   - replay do mesmo Confirm;
   - Confirm com novo `command_id` depois de `AUTHORIZED`;
   - revogação do aprovador antes do Apply;
   - revogação do confirmador antes do Apply.

### C-02 / NEW-MEDIUM-11 — cardinalidade e materialização do pending cost

**Severidade:** MEDIUM  
**Estado:** parcialmente fechado; não bloqueia o PASS documental condicionado.

O caso simples de over-estimate está correto: inserção imutável, reserva mantida, `spent` inalterado e release posterior rejeitada ([FDP-16A:401](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:401)).

Há, porém, uma ambiguidade interna:

- `pending_actual_minor` é declarado como gerado a partir de `pending_provider_cost` ([linha 98](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:98));
- transições de conflito dizem “set pending_actual_minor”, mas nem sempre ordenam explicitamente inserir a linha correspondente ([linhas 372, 396 e 405](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:372));
- `pending_provider_cost.operation_id` é único, embora dois receipts conclusivos com valores diferentes devam ser preservados ([linhas 395 e 461](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:395)). Não está definido qual valor singular deve ser espelhado sem introduzir uma escolha por timing.

LEDGER-15 também começa com `reserved=100`, menciona “this estimate 50”, mas chama diretamente `RecordReceipt`; falta tornar explícito que a operação já está `DISPATCHED` e que o reserve anterior elevou o total a 150 ([matriz:76](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.5-CANONICAL.md:76)).

**Correção precisa:**

1. Tornar obrigatório o insert de `pending_provider_cost` em toda transição `CONFLICT` que contenha receipt.
2. Para receipts conflitantes com valores diferentes, escolher explicitamente:
   - uma linha por `proof_id`, removendo unicidade exclusiva de `operation_id`; ou
   - uma linha agregada com política conservadora definida, por exemplo `max(amount_minor)`, sem depender da ordem de chegada.
3. Fazer `pending_actual_minor` exclusivamente derivado dessa regra; não atribuí-lo independentemente.
4. Ajustar LEDGER-08 para verificar a(s) linha(s) `pending_provider_cost`.
5. Ajustar o fixture de LEDGER-15 para dizer `DISPATCHED`, reservation `HELD=50` e total `reserved=150`, ou incluir Reserve e Dispatch nos passos.

## Avaliação dos oráculos LEDGER-08/11/12/13/14/15

| Oracle | Avaliação documental |
|---|---|
| LEDGER-08 | **PASS.** Conflito conclusivo nunca aceita RELEASED/SETTLED e independe do lock. |
| LEDGER-11 | **PASS.** Impede prova por digest do operador, self-authorship, engine evidence, foreign evidence e UNVERIFIED. |
| LEDGER-12 | **PASS.** Cobre segundo operador, capability, mesma evidência, sessão fresca e Apply somente system. |
| LEDGER-13 | **PASS.** Receipt conclusivo vence no-effect inconclusivo. |
| LEDGER-14 | **PASS PARCIAL.** Approve e Apply estão cobertos; Confirm e revogação pré-Apply não estão. |
| LEDGER-15 | **PASS PARCIAL.** A imobilidade financeira está correta; fixture e cardinalidade do pending cost precisam precisão. |

Os demais replays financeiros permanecem protegidos:

- dois receipts iguais: um settlement ([matriz:68](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.5-CANONICAL.md:68));
- duas releases: uma redução ([matriz:70](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.5-CANONICAL.md:70));
- retry tardio: sem redispatch ou segundo movimento ([matriz:71](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.5-CANONICAL.md:71)).

## Contagens, fontes e regressões

Verificação independente por leitura e contagem:

- **88 linhas de oracle** com status `NOT RUN`;
- **41 linhas do story index**, expressamente “not a second oracle” em [matriz:100](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.5-CANONICAL.md:100);
- **41 histórias**;
- **41 blocos `Inherited`**;
- **41 DoR operacionais `Not met`**;
- **17 P0 históricos**, preservados literalmente.

Os 17 P0 correspondem às linhas AUTH-01…STOP-01 do FDP-13 original ([FDP-13:2272–2288](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/historical/round4/docs/source-material/chat-extracts/FDP-13-v1.0__msg077.md:2272)).

Os 11 estados de Task correspondem ao FDP-12 original — `QUEUED`, `READY`, `RUNNING`, `WAITING`, `RETRYING`, `HANDOFF`, `REVIEWING`, `BLOCKED`, `COMPLETED`, `FAILED`, `CANCELLED` — em [FDP-12:1134–1147](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/historical/round4/docs/source-material/chat-extracts/FDP-12-v1.0__msg074.md:1134), e são preservados em [FDP-16A:8](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md:8).

F-015 referencia corretamente COST-01, LEDGER-01…15 e IDEM-01 ([F-015:651](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-19A-v1.5-STORY-ACCEPTANCE-REGISTER.md:651)). Sua proveniência distingue adequadamente requisitos herdados de propostas introduzidas nas versões v1.3, v1.4 e v1.5 ([linhas 653–659](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/planning/FDP-19A-v1.5-STORY-ACCEPTANCE-REGISTER.md:653)).

Não identifiquei aprovação injustificada:

- FDP-14 continua pendente;
- FDP-15 continua pendente;
- extratos FDP-06/10/12/13 não são apresentados como novas aprovações;
- todas as histórias continuam operacionalmente `Not met`;
- todos os oráculos continuam `NOT RUN`.

A errata Q01 foi corretamente acrescentada: o hash original Round 7 é preservado e explicitamente corrigido para `decef2809…` em [ROUND7 Change Report:36–38](C:/Users/User/AppData/Local/Temp/ia-os-forge-round8-codex-independent/docs/reviews/ROUND7-CHANGE-REPORT-2026-10-13.md:36).

Não foi encontrada regressão Critical/High nas matrizes Task/Attempt/Build, isolamento, deployment tuple, AIOX, handoff, audit, reserva, release ou idempotência de provider call.

## Checker documental

O arquivo `tools/check_round8_consistency.py` foi integralmente inspecionado e é read-only. A política do ambiente bloqueou a inicialização do Python antes da execução; portanto, ele ficou **não executado**.

As contagens principais foram refeitas por comandos nativos de leitura:

- 88 oráculos;
- 41 linhas de story index;
- 41 histórias;
- 41 fontes herdadas;
- 41 DoR operacionais não atendidos.

Isso não é teste de produto e não influencia artificialmente o veredito.

## Distinção entre gate documental e operação

O presente `PASS WITH CONDITIONS` significa apenas que a arquitetura documental v1.5 está suficientemente fechada e não contém finding Critical/High aberto.

Ele não prova:

- implementação das transações ou constraints;
- comportamento real de PostgreSQL;
- integração com provider, chaves ou attestations;
- execução de LEDGER-01…15;
- segurança operacional;
- readiness de sprint;
- staging, restore, RPO/RTO ou drills;
- capacidade, pessoas ou timeboxes.

Não é necessário executar software ou staging para este gate documental.

## Recomendação ao Founder

**Aprovar a prontidão documental v1.5 com as condições C-01 e C-02 registradas para correção antes de BUILD-00.**

Este parecer:

- **não aprova FDP-14**;
- **não aprova FDP-15**;
- **não registra aprovação do Founder**;
- **não autoriza BUILD-00, sprint, implementação ou deploy**;
- **não declara prontidão operacional**;
- **não converte oráculos `NOT RUN` em resultados**;
- aprova exclusivamente a suficiência documental da baseline v1.5 no SHA auditado, condicionada às correções MEDIUM acima.