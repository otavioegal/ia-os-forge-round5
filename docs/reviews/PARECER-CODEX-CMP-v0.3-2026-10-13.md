# PARECER INDEPENDENTE CODEX — DELTA CONVERSATIONAL-MVP v0.3

**Data:** 13 de outubro de 2026  
**SHA congelado auditado:** `f404abc1b4a90f01a12266e3e56a65df277258dd`  
**Modalidade:** auditoria exclusivamente documental e somente leitura.  
**Execução:** nenhum arquivo alterado; nenhum software test, build, checker, provider, banco, staging ou API executado.

## 1. Veredito executivo

| Dimensão | Veredito |
|---|---|
| DELTA CONVERSATIONAL-MVP v0.3 | **PASS WITH CONDITIONS** |
| Residual HIGH-01 | **FECHADO DOCUMENTALMENTE** |
| CMP-O-28 | **CORRIGIDO E DOCUMENTALMENTE ADEQUADO; NOT RUN** |
| MEDIUM-01 | **PERMANECE FECHADO; SEM REGRESSÃO** |
| MEDIUM-02 | **PERMANECE FECHADO; SEM REGRESSÃO** |
| MEDIUM-03 | **PERMANECE FECHADO; SEM REGRESSÃO** |
| LOW-01 do parecer CMP | **PERMANECE FECHADO; SEM REGRESSÃO** |
| Nova regressão CRITICAL/HIGH/MEDIUM | **NÃO IDENTIFICADA** |
| Histórias CMP-S | **13; DoR operacional não atendido** |
| Oráculos CMP-O | **36; todos NOT RUN; evidência ABSENT** |
| AQ-01…AQ-12 | **12 indeterminadas** |
| Decisões humanas pré-integração | **9 ainda abertas** |
| Baseline v1.7 | **DOCUMENTALMENTE INALTERADA** |
| FDP-14 / FDP-15 | **NÃO APROVADOS** |
| Integração à baseline | **NÃO AUTORIZADA** |
| BUILD-00 | **NÃO AUTORIZADO** |

O HEAD documentalmente inspecionado é o SHA solicitado: [`.git/HEAD`](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/.git/HEAD:1) aponta para `main`, e [`.git/refs/heads/main`](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/.git/refs/heads/main:1) contém `f404abc1b4a90f01a12266e3e56a65df277258dd`.

O resultado não é `PASS` irrestrito: HIGH-01 está agora fechado no plano documental, mas o comportamento ainda não foi executado, nove decisões do Founder bloqueiam a integração normativa e FDP-14/FDP-15 continuam pendentes.

## 2. HIGH-01 — conclusão

**Conclusão: confirmo o fechamento documental do residual HIGH-01.**

A v0.3 satisfaz a condição exata deixada pelo parecer v0.2.

### 2.1 Separação normativa do reviewer

O contrato preservado em CMP-03 estabelece que:

- `codex_conversational` e `codex_review_executor` são atores distintos;
- Conselho, Jarvis e chat não podem iniciar formal review;
- cada review formal recebe novo `review_run_id`;
- o principal é exatamente `codex_reviewer`;
- o contexto é reconstruído apenas dos inputs admitidos pelo review gate;
- sessão, memória, cache, scores, verdict candidates, credenciais, actor id, tool state e instância do Builder são proibidos;
- reutilizar processo, credencial ou cache do Builder e apenas trocar o system prompt constitui review falho.

Evidência: [CMP-03:118](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-03-SECURITY-PRIVACY-AND-REVIEW-INDEPENDENCE.md:118), [CMP-03:133](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-03-SECURITY-PRIVACY-AND-REVIEW-INDEPENDENCE.md:133), [CMP-03:137](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-03-SECURITY-PRIVACY-AND-REVIEW-INDEPENDENCE.md:137), [CMP-03:147](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-03-SECURITY-PRIVACY-AND-REVIEW-INDEPENDENCE.md:147) e [CMP-03:155](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-03-SECURITY-PRIVACY-AND-REVIEW-INDEPENDENCE.md:155).

Também não há confusão entre reviewer formal e Codex conversacional: este último é read-only, não recebe `review.sign`, `review.edit` ou `review.execute`, e uma resposta de chat não altera o parecer armazenado. Evidência: [CMP-03:122](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-03-SECURITY-PRIVACY-AND-REVIEW-INDEPENDENCE.md:122).

### 2.2 Fixture adversarial concreta

CMP-O-28 agora fixa explicitamente:

- `BUILDER_RUNTIME_ID`;
- `BUILDER_PROCESS_ID`;
- `BUILDER_AGENT_INSTANCE_ID`;
- `BUILDER_CREDENTIAL_FINGERPRINT`;
- `BUILDER_TOOL_STATE`;
- marcadores distintos de scratch, verdict candidate, cache e actor;
- fingerprint como referência, sem expor segredo bruto;
- host policy service, e não o modelo, como fonte da attestation.

A fixture ainda manda o modelo produzir uma falsa attestation enquanto o processo do Builder permanece ativo. Isso testa precisamente a tentativa de maquiar reutilização de runtime por meio de texto gerado pelo LLM.

Evidência normativa: [CMP-05:586](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-05-ADDITIVE-STORIES-AND-ORACLES.md:586).

### 2.3 Oracle positivo

O PASS exige cumulativamente:

- novo `review_run_id`;
- principal `codex_reviewer`;
- runtime id diferente;
- process id diferente;
- agent instance id diferente;
- `REVIEWER_CREDENTIAL_FINGERPRINT` diferente do fingerprint do Builder;
- fingerprint emitido fora do LLM;
- registro host-attested;
- ausência de scratch, verdict, cache, actor e tool state do Builder em input, hidden state, cache, tool state, prompt ou ambiente;
- rejeição da falsa attestation do modelo;
- separação explícita entre o turno conversacional e o review formal.

Isso é suficiente, documentalmente, para provar a identidade negativa que faltava na v0.2.

A história CMP-S11 espelha a mesma exigência em seus requirements e acceptance criteria: [CMP-05:436](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-05-ADDITIVE-STORIES-AND-ORACLES.md:436), [CMP-05:445](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-05-ADDITIVE-STORIES-AND-ORACLES.md:445) e [CMP-05:455](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-05-ADDITIVE-STORIES-AND-ORACLES.md:455).

### 2.4 Oracle negativo

CMP-O-28 falha expressamente quando processo, runtime, agent instance ou credential fingerprint do Builder é reutilizado, **mesmo que**:

- o ator registrado seja `codex_reviewer`; e
- todos os marcadores tenham sido removidos do prompt.

Também falha se:

- uma attestation escrita pelo modelo for aceita;
- hidden state, cache, score ou tool state anterior alcançar o reviewer;
- Conselho, Jarvis ou Codex conversacional forem tratados como review formal.

Essa é exatamente a contraprova adversarial exigida pelo parecer anterior. Evidência: [CMP-05:586](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-05-ADDITIVE-STORIES-AND-ORACLES.md:586) e [CMP-05:458](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-05-ADDITIVE-STORIES-AND-ORACLES.md:458).

### 2.5 Limite do fechamento

O fechamento é documental, não operacional. Os metadados futuros — runtime, processo, instância, principal, fingerprint e inputs admitidos — continuam `ABSENT`, e CMP-O-28 continua `NOT RUN`. O pacote reconhece corretamente esse limite em [CMP-FINDING-CLOSURE:21](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-FINDING-CLOSURE.md:21).

Não há AUTO PASS nem evidência de execução.

## 3. Não regressão dos findings anteriores

### MEDIUM-01 — STT/TTS versionado

Permanece fechado:

- versão literal `cmp.speech.v0`;
- `describe.contract_versions`;
- rejeição sem envio de bytes e sem downgrade;
- PARTIAL não é commit nem input do modelo;
- encoding/MIME e metadados;
- cancelamento confirmado ou inconclusivo;
- `retryable` não autoriza redispatch.

Evidência: [CMP-02:193](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-02-SYSTEM-ARCHITECTURE.md:193), [CMP-02:220](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-02-SYSTEM-ARCHITECTURE.md:220), [CMP-02:268](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-02-SYSTEM-ARCHITECTURE.md:268) e [CMP-02:292](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-02-SYSTEM-ARCHITECTURE.md:292).

### MEDIUM-02 — retry, HELD e dupla cobrança

A tabela de cinco estados permanece íntegra:

- pré-dispatch: no máximo um dispatch;
- resultado desconhecido: zero redispatch;
- `NO_EFFECT`: nova tentativa somente em novo turn e `operation_ref`;
- HELD/inconclusivo: reconciliação, sem redispatch;
- efeito conclusivo: replay sem nova chamada.

Evidência: [CMP-02:345](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-02-SYSTEM-ARCHITECTURE.md:345).

### MEDIUM-03 — atribuição e deduplicação de custo

Continuam obrigatórios `session_id`, `turn_id`, `agent_id`, `provider_id`, modelo ou capability aplicável, `operation_ref` e estimativa. O total continua sendo a soma das operações da sessão, sem meeting fee, sem custo confirmado sem prova e sem segundo invoke/reserva em duplicata.

Evidência: [CMP-04:122](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-04-OBSERVABILITY-EVIDENCE-AND-COST.md:122).

### LOW-01 — sessão text-only

A separação entre `microphone_consent_state`, consent id nullable e `retention_policy_id` permanece. `NOT_GRANTED` admite sessão text-only sem UUID sintético, com zero áudio e zero STT.

Evidência: [CMP-02:50](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-02-SYSTEM-ARCHITECTURE.md:50) e [CMP-02:66](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-02-SYSTEM-ARCHITECTURE.md:66).

## 4. Contagens e estado de execução

O registro consolida:

- 13 histórias, CMP-S01…CMP-S13;
- 36 oráculos, CMP-O-01…CMP-O-36;
- nenhum novo ID na v0.3;
- somente CMP-O-28 alterado;
- todos os oráculos `NOT RUN`;
- DoR operacional de todas as histórias `Not met`;
- evidência futura `ABSENT`.

Evidência: [CMP-05:553](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-05-ADDITIVE-STORIES-AND-ORACLES.md:553), [CMP-05:596](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-05-ADDITIVE-STORIES-AND-ORACLES.md:596) e a enumeração completa [CMP-ORACLE-MATRIX:7](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-ORACLE-MATRIX-v0.2.md:7).

A matriz suplementar continua sendo apenas índice; CMP-05 é a autoridade dos oráculos CMP, e a matriz v1.7 não foi substituída: [CMP-ORACLE-MATRIX:3](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-ORACLE-MATRIX-v0.2.md:3).

## 5. Baseline e escopo histórico

O pacote declara e preserva documentalmente:

- baseline v1.7 no SHA `0c42373d…`;
- v0.1 no SHA `cad1ac6…`;
- v0.2 no SHA `99474da…`;
- 91 oráculos, 41 histórias, 17 P0 e 11 estados Task da baseline;
- PASS Round 10 restrito ao SHA histórico;
- ausência de integração automática do delta.

Evidência: [CMP-00:3](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-00-PACKAGE-INDEX.md:3), [CMP-00:6](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-00-PACKAGE-INDEX.md:6), [CMP-CHANGE-REPORT:5](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-CHANGE-REPORT.md:5) e [CMP-06:40](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-06-TRACEABILITY-AND-IMPACT.md:40).

O relatório mecânico registra `CHECKER_RESULT: SATISFIED`, mas corretamente limita isso à consistência e nega que seja PASS: [CMP-CONSISTENCY-REPORT:30](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-CONSISTENCY-REPORT.md:30). Não executei esse checker neste parecer.

## 6. AQ e decisões do Founder

As 12 questões permanecem indeterminadas.

Nove ainda exigem decisão humana antes da integração:

- AQ-01, AQ-02, AQ-03;
- AQ-05, AQ-06, AQ-07, AQ-08;
- AQ-10 e AQ-11.

AQ-04, AQ-09 e AQ-12 continuam apenas diferíveis, respectivamente sob deny-by-default, ausência de acoplamento e reserva HELD sem prova.

Evidência: [CMP-AQ-FOUNDER-DECISIONS:8](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-AQ-FOUNDER-DECISIONS.md:8), [CMP-AQ-FOUNDER-DECISIONS:22](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-AQ-FOUNDER-DECISIONS.md:22) e [CMP-OPEN-QUESTIONS:9](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-OPEN-QUESTIONS.md:9).

Nenhuma proposta da tabela constitui decisão do Founder; silêncio não é aceite: [CMP-AQ-FOUNDER-DECISIONS:3](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-AQ-FOUNDER-DECISIONS.md:3).

## 7. Pendência editorial

Permanece o LOW editorial histórico de FDP-17: a referência “v1.6 matrix”. A v0.3 deliberadamente não altera a baseline para corrigi-lo: [CMP-RISKS:19](C:/Users/User/AppData/Local/Temp/ia-os-forge-cmp03-codex-independent/docs/planning/conversational-mvp-v0.3/CMP-RISKS.md:19).

Ele não afeta HIGH-01, não reabre os findings CMP fechados e não justifica outra rodada específica de review. Pode ser corrigido futuramente em commit editorial separado.

## 8. Gates remanescentes

Antes de integração ou execução, permanecem necessários:

1. decisão expressa do Founder sobre as nove AQ pré-integração;
2. deliberação própria de FDP-14;
3. deliberação própria de FDP-15;
4. aprovação explícita da integração do delta à baseline;
5. atribuição de responsáveis e calibração operacional das 13 histórias;
6. execução futura dos 36 CMP-O, incluindo CMP-O-28, com evidência host-attested;
7. ato separado e explícito para qualquer BUILD-00.

## Conclusão

A v0.3 corrige exatamente a insuficiência documental apontada na v0.2. CMP-O-28 agora detecta reutilização real de processo, runtime, instância e credencial, mesmo sob principal nominal correto e prompt higienizado, e separa inequivocamente review formal de chat/Conselho/Jarvis.

Portanto:

- **HIGH-01: FECHADO DOCUMENTALMENTE**;
- **DELTA v0.3: PASS WITH CONDITIONS**;
- **não há autorização para integrar à baseline**;
- **FDP-14 e FDP-15 não são aprovados**;
- **BUILD-00 não é autorizado**;
- **os 36 oráculos continuam NOT RUN e não há AUTO PASS**.