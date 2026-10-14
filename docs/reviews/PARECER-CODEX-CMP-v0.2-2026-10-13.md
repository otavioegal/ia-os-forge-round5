# PARECER INDEPENDENTE CODEX — DELTA CONVERSATIONAL-MVP v0.2

**Data:** 13 de outubro de 2026  
**SHA congelado auditado:** `99474da514419a26ac8471c50c33697ade2a1cde`  
**Escopo:** exclusivamente `docs/planning/conversational-mvp-v0.2/`, contextualizado pela v0.1, decisão do Founder, contratos v1.7 e parecer Round 10.  
**Modalidade:** auditoria documental independente, somente leitura.  
**Execução:** nenhum arquivo alterado; nenhum build, checker, teste de software, banco, provider, staging ou API paga executado.

## Veredito executivo

| Dimensão | Veredito |
|---|---|
| DELTA CONVERSATIONAL-MVP v0.2 | **PASS WITH CONDITIONS** |
| HIGH-01 | **PARCIALMENTE FECHADO — contrato corrigido, oráculo ainda não conclusivo para runtime/credencial** |
| MEDIUM-01 | **FECHADO DOCUMENTALMENTE** |
| MEDIUM-02 | **FECHADO DOCUMENTALMENTE** |
| MEDIUM-03 | **FECHADO DOCUMENTALMENTE** |
| LOW-01 | **FECHADO DOCUMENTALMENTE** |
| Nova regressão CRITICAL | **NENHUMA** |
| Nova regressão HIGH | **NENHUMA distinta de HIGH-01 residual** |
| Nova regressão MEDIUM | **NENHUMA** |
| Histórias CMP-S | **13, preservadas** |
| Oráculos originais CMP-O-01…34 | **preservados por ID; alguns emendados; todos NOT RUN** |
| Novos oráculos | **CMP-O-35 e CMP-O-36; válidos; NOT RUN** |
| Autoridade duplicada de oráculos | **NÃO identificada** |
| AQ-01…AQ-12 | **12 abertas; 9 exigem decisão humana antes da integração** |
| Baseline v1.7 | **INTACTA; PASS histórico limitado ao SHA `0c42373…`** |
| FDP-14 / FDP-15 | **NÃO APROVADOS por este parecer** |
| Integração à baseline | **NÃO AUTORIZADA** |
| BUILD-00 | **NÃO AUTORIZADO** |

O pacote corrige substancialmente os cinco findings da v0.1 e não depende das afirmações de fechamento do Builder/Grok. Contudo, não concedo `PASS` simples porque o oráculo CMP-O-28 ainda permite uma implementação reutilizar o mesmo processo/runtime ou uma credencial ambiente do Builder, desde que troque o principal nominal e não exponha os quatro marcadores atuais. Isso deixa incompleta a demonstração futura exigida para HIGH-01.

## 1. Integridade do SHA e preservação histórica

O HEAD local aponta diretamente para o SHA solicitado:

- `.git/HEAD` referencia `refs/heads/main`;
- `.git/refs/heads/main` contém `99474da514419a26ac8471c50c33697ade2a1cde`;
- `.git/logs/HEAD` registra o clone nesse mesmo commit.

A comparação entre a baseline `0c42373d583dec420348efd7bc0b8c6228a66f47` e o SHA auditado não mostra alterações nos documentos normativos v1.7. As mudanças posteriores são aditivas — documentos de governança, pacotes conversational-mvp, revisões e ferramentas. A comparação entre a v0.1 `cad1ac6d6bb8a970165ebd17ce1bff13d98af806` e o SHA atual também não mostra alteração em `docs/planning/conversational-mvp/`.

Isso confirma materialmente as declarações de baseline e v0.1 intactas em:

- `docs/planning/conversational-mvp-v0.2/CMP-00-PACKAGE-INDEX.md:3-7`;
- `docs/planning/conversational-mvp-v0.2/CMP-CHANGE-REPORT.md:5-14`;
- `docs/planning/conversational-mvp-v0.2/CMP-06-TRACEABILITY-AND-IMPACT.md:43-58`.

O PASS documental do Round 10 continua histórico e restrito ao SHA v1.7. Não foi reaberto nem estendido automaticamente ao delta.

## 2. Findings da v0.1

### HIGH-01 — Independência do reviewer

**Estado: parcialmente fechado; condição HIGH residual.**

A regra normativa foi corrigida de maneira forte. A v0.2 agora:

- separa `codex_conversational` de `codex_review_executor`;
- nega `review.sign`, `review.edit` e `review.execute` ao papel conversacional;
- exige novo `review_run_id`;
- fixa o principal formal como `codex_reviewer`;
- reconstrói contexto apenas das entradas admitidas pelo review gate;
- proíbe sessão, memória, cache, scores, verdict candidates, credenciais, actor id, tool state, instância e processo do Builder;
- declara expressamente que apenas trocar o system prompt no processo do Builder constitui falha de independência.

Evidência: `docs/planning/conversational-mvp-v0.2/CMP-03-SECURITY-PRIVACY-AND-REVIEW-INDEPENDENCE.md:116-160`.

Essa separação também aparece no registro conversacional e impede que Jarvis, Conselho ou handoff iniciem formal review: `docs/planning/conversational-mvp-v0.2/CMP-02-SYSTEM-ARCHITECTURE.md:99-108`.

O defeito residual está no oráculo. CMP-O-28 possui marcadores para scratch, verdict candidate, session cache e actor id, e sua regra negativa menciona tool state e credenciais. Entretanto:

1. não há um `BUILDER_RUNTIME_ID` ou identificador de instância/processo na fixture;
2. não há um `BUILDER_CREDENTIAL_ID`/fingerprint ou principal de credencial verificável na fixture;
3. a regra positiva verifica que o “runtime actor” não é `BUILDER_ACTOR_9f3a`, mas não exige que o runtime/process/instance id seja diferente;
4. “credenciais attached to the run” não captura necessariamente uma credencial herdada do processo ou ambiente, mas não materializada no registro do run.

Evidência: `docs/planning/conversational-mvp-v0.2/CMP-05-ADDITIVE-STORIES-AND-ORACLES.md:580`.

Assim, uma implementação poderia reutilizar o processo/runtime do Builder, trocar o principal registrado para `codex_reviewer`, limpar os quatro marcadores e obter PASS pelo texto atual do oráculo — embora isso viole diretamente CMP-03.

**Condição necessária:** emendar CMP-O-28 para incluir, na fixture, pelo menos `BUILDER_RUNTIME_ID`, `BUILDER_AGENT_INSTANCE_ID` e `BUILDER_CREDENTIAL_FINGERPRINT`; exigir no PASS runtime/instância novos e credencial de reviewer distinta; e declarar FAIL para reutilização do processo/runtime ou credencial, mesmo que o principal nominal seja `codex_reviewer` e nenhum marcador de conteúdo vaze.

Isso é uma correção documental de oracle. Não requer executar teste neste gate.

### MEDIUM-01 — Contratos STT/TTS versionados

**Estado: fechado documentalmente.**

CMP-02 §7.2 agora especifica:

- versão literal `cmp.speech.v0`;
- negociação via `describe.contract_versions`;
- rejeição sem envio de bytes e sem downgrade;
- schemas separados de request/result para STT e TTS;
- transcript `PARTIAL` versus `FINAL`;
- regra de que PARTIAL não é commit nem input do modelo;
- encoding, MIME, idioma, canal e sample rate aplicáveis;
- resultado TTS e semântica de chunks;
- taxonomia retryable/terminal;
- cancelamento `CONFIRMED`/`UNCONFIRMED`;
- proibição de transformar `retryable` em autorização de redispatch.

Evidência: `docs/planning/conversational-mvp-v0.2/CMP-02-SYSTEM-ARCHITECTURE.md:187-293`.

CMP-O-36 cobre versão incompatível, PARTIAL/FINAL, codec/MIME, cancelamento e ausência de downgrade: `docs/planning/conversational-mvp-v0.2/CMP-05-ADDITIVE-STORIES-AND-ORACLES.md:588`.

Não há escolha de fornecedor nem afirmação de compatibilidade executada.

### MEDIUM-02 — Retry, HELD e prevenção de dupla cobrança

**Estado: fechado documentalmente.**

CMP-02 §9 estabelece cinco situações mutuamente distinguíveis:

- antes do dispatch: mesma operação, no máximo um dispatch;
- resultado desconhecido após dispatch: reconciliação, sem redispatch;
- `NO_EFFECT` conclusivo: nova tentativa somente em novo turn e novo `operation_ref`;
- HELD/inconclusivo: reconciliação, sem redispatch, recibo ou write-off;
- efeito conclusivo: replay do resultado armazenado, sem nova chamada.

Evidência: `docs/planning/conversational-mvp-v0.2/CMP-02-SYSTEM-ARCHITECTURE.md:337-364`.

A UX apresenta controles distintos em `docs/planning/conversational-mvp-v0.2/CMP-01-PRD-UX-JOURNEYS.md:131-148`.

A cobertura negativa existe em CMP-O-15, CMP-O-16 e CMP-O-29, enquanto CMP-O-35 percorre explicitamente os cinco estados: `docs/planning/conversational-mvp-v0.2/CMP-05-ADDITIVE-STORIES-AND-ORACLES.md:564-565`, `:578`, `:587`.

O protocolo monetário permanece FDP-16A; não foi criado segundo ledger nem novo capturador de prova.

### MEDIUM-03 — Atribuição e deduplicação de custo

**Estado: fechado documentalmente.**

CMP-04 exige que cada operação externa carregue:

- `session_id`;
- `turn_id`;
- `agent_id`;
- `provider_id`;
- `model_id`, quando houver dimensão de modelo;
- capability substituta apenas quando a dimensão de modelo não existe;
- `operation_ref`;
- `estimated_minor`;
- proof id posterior, se houver ingestão.

Também fixa:

- total da sessão como soma das operações daquela sessão;
- ausência de meeting fee;
- estimativa distinta de custo confirmado;
- custo confirmado somente por prova conclusiva;
- deduplicação sem segundo `forge.adapter.invoke` ou `budget.reserved`;
- HELD quando a prova for inconclusiva.

Evidência: `docs/planning/conversational-mvp-v0.2/CMP-04-OBSERVABILITY-EVIDENCE-AND-COST.md:121-138`.

CMP-O-31 usa dois agentes, dois modelos e dois providers e exige quatro operações individualizadas, soma por sessão, ausência de meeting fee e ausência de custo confirmado sem prova: `docs/planning/conversational-mvp-v0.2/CMP-05-ADDITIVE-STORIES-AND-ORACLES.md:580`.

A expressão “provider_id ou capability” para TTS na regra positiva é imprecisa, porque a própria regra negativa e CMP-04 exigem `provider_id` em toda chamada externa. Considero isso **editorial**, pois a norma e o FAIL são inequívocos. Recomenda-se substituir por “provider_id e, quando não houver model_id, capability”.

### LOW-01 — Consentimento em sessão somente texto

**Estado: fechado documentalmente.**

A nova modelagem separa:

- `microphone_consent_state`;
- `microphone_consent_id`, nullable;
- `retention_policy_id`, sempre obrigatório.

`NOT_GRANTED` exige consent id nulo, permite abertura somente texto e proíbe captura e STT. `DENIED` e `REVOKED` referenciam a respectiva decisão, mas igualmente impedem captura. Somente `GRANTED` permite tentativa de STT.

Evidência:

- `docs/planning/conversational-mvp-v0.2/CMP-02-SYSTEM-ARCHITECTURE.md:52-80`;
- `docs/planning/conversational-mvp-v0.2/CMP-03-SECURITY-PRIVACY-AND-REVIEW-INDEPENDENCE.md:42-55`;
- `docs/planning/conversational-mvp-v0.2/CMP-05-ADDITIVE-STORIES-AND-ORACLES.md:568`.

Não há mais necessidade de UUID sintético para abrir uma sessão text-only.

## 3. Histórias e oráculos

Confirmei:

- exatamente 13 histórias, CMP-S01…CMP-S13;
- DoR operacional não atendido em todas;
- pessoa responsável e calibração continuam pendentes;
- CMP-O-01…CMP-O-34 preservam os identificadores da v0.1;
- CMP-O-35 e CMP-O-36 são os únicos oráculos novos;
- todos os 36 estão `NOT RUN`;
- evidência futura está `ABSENT`;
- cada oráculo contém fixture, passos, regra positiva, regra negativa, evidência futura e status;
- não há duplicidade de IDs;
- nenhuma linha foi inserida na matriz normativa v1.7.

Evidência consolidada:

- `docs/planning/conversational-mvp-v0.2/CMP-05-ADDITIVE-STORIES-AND-ORACLES.md:548-594`;
- `docs/planning/conversational-mvp-v0.2/CMP-ORACLE-MATRIX-v0.2.md:3-46`.

A autoridade não está duplicada: CMP-05 contém o texto normativo dos oráculos suplementares; a matriz v0.2 é explicitamente um índice e determina que CMP-05 prevalece. A matriz v1.7 continua sendo a única autoridade para os 91 oráculos da baseline.

Não exijo execução de oráculos neste gate documental.

## 4. Questões abertas e gates

As 12 questões AQ-01…AQ-12 permanecem abertas, sem decisão atribuída ao Founder.

Nove são pré-requisito para integração normativa:

- AQ-01 — ator e comando para reserva conversacional;
- AQ-02 — âncora obrigatória de `task_id`;
- AQ-03 — família dos adapters de voz, junto com FDP-15;
- AQ-05 — enum e política de classificação;
- AQ-06 — política padrão de retenção;
- AQ-07 — confirmação de half-duplex com barge-in;
- AQ-08 — ativação explícita versus always-on;
- AQ-10 — teto financeiro pelo ledger existente;
- AQ-11 — biometria fora ou dentro do MVP.

AQ-04, AQ-09 e AQ-12 podem permanecer diferidas somente enquanto vigorem, respectivamente, deny-by-default, ausência de acoplamento e reserva HELD sem prova.

Evidência: `docs/planning/conversational-mvp-v0.2/CMP-OPEN-QUESTIONS.md:8-32`.

Outros gates pendentes:

- confirmação humana de FDP-14;
- aprovação humana de FDP-15;
- aprovação expressa da integração do delta à baseline;
- responsáveis e calibração operacional das histórias;
- correção conclusiva de CMP-O-28;
- ato futuro e separado para qualquer BUILD-00.

## 5. Relatórios de fechamento e autocertificação

`CMP-FINDING-CLOSURE.md` não foi aceito como prova por si só. Sua linguagem é corretamente cautelosa: declara que os findings não estão fechados pelo pacote, que os testes estão NOT RUN e que a auditoria Codex ainda era necessária.

Evidência: `docs/planning/conversational-mvp-v0.2/CMP-FINDING-CLOSURE.md:1-5`.

O relatório de consistência também limita `CHECKER_RESULT: SATISFIED` à coerência mecânica e nega que isso constitua PASS: `docs/planning/conversational-mvp-v0.2/CMP-CONSISTENCY-REPORT.md:25-37`.

Portanto, não identifiquei autocertificação material ou tentativa de converter afirmações Grok/Builder em autoridade de review.

## 6. Pontos editoriais não bloqueantes

Não classifico os seguintes pontos como regressões MEDIUM:

- CMP-02 apresenta §7.2 antes de §7.1 — problema de ordenação editorial;
- CMP-O-31 diz “provider_id ou capability” para TTS, embora CMP-04 e a própria regra negativa exijam provider_id em chamadas externas;
- alguns relatórios dizem genericamente que HIGH-01 recebeu “correção documental”, mas preservam corretamente “aguarda auditoria” e “não está fechado”.

Eles podem ser corrigidos junto com CMP-O-28 sem reabrir arquitetura.

## 7. Recomendação ao Founder

**Não autorizar BUILD-00 e não integrar ainda o delta à baseline.**

Recomendo:

1. aceitar que MEDIUM-01, MEDIUM-02, MEDIUM-03 e LOW-01 estão documentalmente sanados;
2. devolver somente HIGH-01 para uma emenda focal de CMP-O-28, adicionando identidade negativa verificável de runtime/processo/instância e credencial do Builder;
3. deliberar expressamente as nove AQ pré-integração;
4. tratar FDP-14 e FDP-15 em atos próprios, sem inferir aprovação deste parecer;
5. após essas ações, solicitar uma revisão documental final do delta consolidado;
6. somente depois considerar um pre-flight separado de BUILD-00.

**Conclusão:** a v0.2 é materialmente mais robusta e quase fecha o parecer anterior, mas o oráculo central de independência ainda não prova toda a regra que o próprio contrato corretamente estabelece. Por isso, o resultado responsável é **PASS WITH CONDITIONS**, restrito ao gate documental e ao SHA `99474da514419a26ac8471c50c33697ade2a1cde`.