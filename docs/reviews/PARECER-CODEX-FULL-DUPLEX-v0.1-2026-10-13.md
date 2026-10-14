# PARECER INDEPENDENTE CODEX — PACOTE CONVERSATIONAL FULL-DUPLEX

**Data:** 13 de outubro de 2026  
**SHA congelado auditado:** `97ee817ca8262b3a0bae996c510b935435b2e575`  
**Modalidade:** revisão exclusivamente documental, independente e somente leitura  
**Veredito:** **FAIL — DOCUMENT-ONLY**

A referência `.git/refs/heads/main` confirma exatamente o SHA solicitado. Não executei testes, builds, checkers, providers, banco, staging, APIs ou software do projeto. Nenhum arquivo foi alterado.

O memorando não pôde ser persistido como arquivo porque o workspace está montado com permissão exclusivamente de leitura. O texto integral segue abaixo como saída da revisão.

## 1. Conclusão executiva

As nove decisões humanas estão registradas de maneira materialmente fiel:

- Aprovadas: AQ-01, AQ-02, AQ-03, AQ-05, AQ-06, AQ-07, AQ-08, AQ-10 e AQ-11.
- Diferidas e não decididas: AQ-04, AQ-09 e AQ-12.
- FDP-14 e FDP-15 continuam sem aprovação.
- A integração à baseline v1.7 continua sem aprovação.
- BUILD-00 continua não autorizado.

Isso não torna o desenho técnico aprovado. A ata distingue corretamente decisão humana de aprovação técnica em [ATA-FOUNDER-AQS-CONVERSATIONAL-2026-10-13.md:27](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/governance/ATA-FOUNDER-AQS-CONVERSATIONAL-2026-10-13.md:27), e o próprio índice apresenta o pacote como candidato, não como PASS, em [CMP-FD-00-INDEX.md:3](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-full-duplex/CMP-FD-00-INDEX.md:3).

O `FAIL` decorre de duas insuficiências bloqueantes:

1. A integração financeira aprovada pelo Founder não é compatível com os contratos v1.7 existentes e o pacote não especifica o delta necessário.
2. O contrato e os oráculos não são exatos o bastante para provar full-duplex simultâneo real, distinguindo-o de half-duplex com barge-in local.

Há ainda deficiências substanciais em STT/TTS, cancelamento, consentimento concorrente, política local versus externa, atribuição de fontes e critérios de latência.

## 2. Achados

### HIGH-01 — Papel financeiro e Task-âncora são incompatíveis com FDP-16A v1.7

A proposta afirma que `conversation_router` terá principal próprio e reservará pelo gateway e pela mesma transação financeira, em [CMP-FD-01:28](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-full-duplex/CMP-FD-01-FULL-DUPLEX-ARCHITECTURE.md:28).

Entretanto, FDP-16A v1.7:

- não contém `conversation_router` no enum de `actor_class`; admite somente `human`, `security_operator`, `release_agent`, `coding_engine`, `reviewer` e `system`, em [FDP-16A:167](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md:167);
- autoriza `InvokeCapability` especificamente a `coding_engine via gateway`, em [FDP-16A:202](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md:202);
- exige `Task.build_id` não nulo e FK para Build, em [FDP-16A:58](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md:58);
- exige `Operation.task_id`, em [FDP-16A:90](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md:90).

A Task-âncora “fora do DAG de build” não pode ser criada sob esse schema sem explicar a qual Build pertence, como deixa de participar do DAG e quais transições lhe são legais. O pacote novo também não define:

- novo comando financeiro para `conversation_router`;
- enum e regras de autorização do novo ator;
- payload, erros e idempotência desse comando;
- criação, estado, encerramento e cardinalidade da Task-âncora;
- relacionamento obrigatório com Build;
- política de recuperação de sessões órfãs;
- constraints que proíbem deploy, terminal e vault.

A própria v0.3 havia reconhecido explicitamente esse bloqueio: não se poderia fingir que o roteador era `coding_engine` e seria necessário um comando com o mesmo efeito transacional, em [CMP-02 v0.3:334](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-mvp-v0.3/CMP-02-SYSTEM-ARCHITECTURE.md:334).

**Correção requerida:** produzir delta normativo de FDP-16A/FDP-15 contendo schema, enum, comando, caller/callee, grants, transação, erros, dedupe e oráculos; definir formalmente como a Task conversacional satisfaz `build_id NOT NULL` sem ingressar no DAG. Até isso existir, nenhuma operação paga conversacional pode ser tecnicamente aprovada.

### HIGH-02 — Os oráculos não provam full-duplex simultâneo real

A arquitetura exige entrada recebida durante saída em [CMP-FD-01:21](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-full-duplex/CMP-FD-01-FULL-DUPLEX-ARCHITECTURE.md:21). Porém, CMP-FD-O01 só exige que “STT recebe entrada ANTES da saída terminar”, em [CMP-FD-02:9](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-full-duplex/CMP-FD-02-ADDITIVE-STORIES-AND-ORACLES.md:9).

Esse critério pode passar com implementação de barge-in local:

1. detecta fala;
2. para ou encurta TTS;
3. abre STT;
4. registra o input antes de algum término lógico tardio do stream de saída.

Não há fixture temporal com intervalos de captura e playback comprovadamente sobrepostos, nem contadores ou timestamps que mostrem chunks de entrada aceitos enquanto chunks de saída continuam sendo produzidos/reproduzidos.

Também faltam:

- definição do relógio e tolerância;
- pontos exatos de observação;
- duração mínima da sobreposição;
- fixture que mantenha saída ativa depois do primeiro chunk de entrada;
- contraprova contra pause-before-capture;
- verificação do caminho completo, não apenas captura local;
- critérios para eco, VAD, jitter, perda e reordenação;
- distinção entre saída gerada, recebida e efetivamente reproduzida.

**Correção requerida:** criar fixture determinística com timeline e dois fluxos instrumentados. O PASS deve exigir interseção positiva entre `[input_capture_start,input_capture_end]` e `[output_playback_start,output_playback_end]`, chunks de ambas as direções observados dentro dessa interseção e ausência de uma transição obrigatória para modo exclusivo de entrada. Adicionar um oracle negativo específico para implementação que pausa TTS antes de encaminhar qualquer áudio ao STT.

### HIGH-03 — `cmp.media.duplex.v1` não é uma interface implementável nem compatível de forma verificável com `cmp.speech.v0`

O “envelope” de [CMP-FD-01:17](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-full-duplex/CMP-FD-01-FULL-DUPLEX-ARCHITECTURE.md:17) é apenas uma lista de nomes. Faltam tipos, nulabilidade, enums, constraints e payloads.

Em especial, não há definição para:

- bytes ou referência do chunk;
- `turn_id`;
- `invocation_id`;
- direção do fluxo;
- sample rate, canais e duração;
- MIME compatível com `cmp.speech.v0`;
- fronteira e hash do chunk;
- `is_final` e finalização de stream;
- janela de sequência e regra para lacunas;
- escopo da monotonicidade de `sequence`;
- acknowledgements de chunk;
- estados e transições da sessão;
- handshake de versões;
- transport binding e backpressure;
- correlação inequívoca entre evento de mídia, chamada STT/TTS e `operation_ref`.

Isso conflita com a precisão já alcançada por `cmp.speech.v0`, que define versionamento e negociação em [CMP-02 v0.3:193](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-mvp-v0.3/CMP-02-SYSTEM-ARCHITECTURE.md:193), encoding/MIME em [CMP-02 v0.3:199](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-mvp-v0.3/CMP-02-SYSTEM-ARCHITECTURE.md:199) e PARTIAL/FINAL em [CMP-02 v0.3:220](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-mvp-v0.3/CMP-02-SYSTEM-ARCHITECTURE.md:220).

Declarar que um contrato “complementa” o outro, em [CMP-FD-01:15](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-full-duplex/CMP-FD-01-FULL-DUPLEX-ARCHITECTURE.md:15), não define a composição.

**Correção requerida:** publicar schemas completos e uma tabela de mapeamento evento por evento entre `cmp.media.duplex.v1` e `cmp.speech.v0`, inclusive lifecycle, negociação, erros, cancelamento e vínculo financeiro.

### MEDIUM-01 — Cancelamento, interrupção e retry permanecem ambíguos

A arquitetura diz que `USER_SPEECH_START` solicita “duck/cancel”, em [CMP-FD-01:23](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-full-duplex/CMP-FD-01-FULL-DUPLEX-ARCHITECTURE.md:23). Duck e cancelamento são resultados diferentes: um mantém saída em volume reduzido; o outro encerra geração ou playback.

CMP-FD-O03 exige que playback cesse quando `CANCEL_ACK` é `UNCONFIRMED`, em [CMP-FD-02:11](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-full-duplex/CMP-FD-02-ADDITIVE-STORIES-AND-ORACLES.md:11), mas não separa:

- cancelamento local de playback;
- cancelamento do stream de TTS;
- cancelamento de geração do modelo;
- efeito financeiro externo;
- timeout e reconciliação de cada operação.

A regra genérica “retry nunca ignora UNKNOWN/HELD” em [CMP-FD-01:26](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-full-duplex/CMP-FD-01-FULL-DUPLEX-ARCHITECTURE.md:26) não substitui a tabela precisa de recuperação que a v0.3 já possuía.

**Correção requerida:** definir state machines separadas para playback, TTS invocation, model invocation e ledger operation; estabelecer qual cancelamento é best-effort, qual exige ACK e qual jamais permite redispatch.

### MEDIUM-02 — Revogação de consentimento não tem semântica concorrente completa

O pacote acerta ao exigir mic desligado fora da sessão e cessação após pause, stop ou revogação, em [CMP-FD-01:25](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-full-duplex/CMP-FD-01-FULL-DUPLEX-ARCHITECTURE.md:25). CMP-FD-O05 também rejeita chunk tardio, em [CMP-FD-02:13](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-full-duplex/CMP-FD-02-ADDITIVE-STORIES-AND-ORACLES.md:13).

Faltam, porém:

- ordem normativa entre revogação e chunks concorrentes;
- geração/epoch de consentimento em cada chunk;
- corte no dispositivo versus gateway;
- limpeza de buffers já capturados;
- tratamento de bytes já enviados ao provider;
- ACK de encerramento;
- deadline de cessação;
- teste de revogação durante reconnect;
- teste de background após suspensão ou crash do app.

CMP-FD-O06 verifica apenas “zero captura/STT”, em [CMP-FD-02:14](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-full-duplex/CMP-FD-02-ADDITIVE-STORIES-AND-ORACLES.md:14), sem observar abertura de dispositivo, transmissão, buffers ou egress.

**Correção requerida:** adicionar `consent_epoch` ou equivalente, regra de rejeição atômica para epochs antigas e oráculos distintos para dispositivo, transporte, STT e buffers.

### MEDIUM-03 — Política local versus externa não é operacionalmente verificável

A decisão AQ-05 está corretamente reproduzida. Entretanto, o novo contrato não define um atributo autenticado que distinga adapter local, self-hosted e provider externo. “Classificação permitida” em `START_SESSION` não prova que cada egress posterior foi reavaliado.

CMP-FD-O07 cobre apenas CONFIDENTIAL com provider speech externo, em [CMP-FD-02:15](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-full-duplex/CMP-FD-02-ADDITIVE-STORIES-AND-ORACLES.md:15). Não cobre:

- RESTRICTED;
- INTERNAL com allowlist;
- mudança de classificação no meio da sessão;
- fallback local → externo;
- provider que declara falsamente ser local;
- egress por `conversation.respond`;
- reclassificação após troca de projeto ou interlocutor.

**Correção requerida:** tornar `execution_location`/`trust_boundary` parte do descriptor validado pela Policy Service e criar matriz de oráculos para as quatro classes, STT, TTS, modelo e fallback.

### MEDIUM-04 — Atribuição de interlocutor e de fontes regrediu em precisão

O envelope torna `speaker_agent_id` obrigatório somente “quando saída”, mas não contém `turn_id`, em [CMP-FD-01:17](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-full-duplex/CMP-FD-01-FULL-DUPLEX-ARCHITECTURE.md:17).

A v0.3 já exigia:

- agente atual identificado na interface, [CMP-01 v0.3:43](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-mvp-v0.3/CMP-01-PRD-UX-JOURNEYS.md:43);
- um speaker por turno, identidade textual e preâmbulo de áudio, [CMP-01 v0.3:100](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-mvp-v0.3/CMP-01-PRD-UX-JOURNEYS.md:100);
- minutos com `turn_id` e evidence refs, [CMP-01 v0.3:103](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-mvp-v0.3/CMP-01-PRD-UX-JOURNEYS.md:103);
- síntese de Jarvis com `source_turn_ids`, [CMP-01 v0.3:120](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-mvp-v0.3/CMP-01-PRD-UX-JOURNEYS.md:120).

CMP-FD-O04 verifica speaker e divergência, mas não verifica evidence refs, `source_turn_ids`, classificação FACT/INFERENCE/SUGGESTION ou não atribuição indevida ao Codex.

**Correção requerida:** tornar `turn_id`, `speaker_agent_id`, `origin`, `source_turn_ids` e `evidence_refs` parte explícita do contrato de saída ou de sua correlação normativa, preservando os oráculos de proveniência da v0.3.

### MEDIUM-05 — Não há critério verificável de baixa latência ou qualidade

É correto não fabricar métricas. [CMP-FD-01:36](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-full-duplex/CMP-FD-01-FULL-DUPLEX-ARCHITECTURE.md:36) declara que não existe medição de latência, e o ADR diz que a decisão não aprovou SLA, em [ADR AQ07:17](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/governance/ADR-FDR-AQ07-FULL-DUPLEX-MVP-2026-10-13.md:17).

Ainda assim, não há contrato para medir:

- fala → primeiro STT partial;
- fala final → STT final;
- final → primeiro token;
- primeiro token → primeiro áudio;
- `USER_SPEECH_START` → duck/stop local;
- jitter, perda, underrun e overflow;
- percentis, janela amostral e condições de rede.

Sem isso, “natural” e “baixa latência” não têm oracle futuro.

**Correção requerida:** especificar campos e pontos de medição agora; deixar valores de aceitação explicitamente pendentes de calibração/FDP-14, sem convertê-los em medições ou SLAs fictícios.

### LOW-01 — Histórias não estão em DoR e os oráculos não são fixtures exatas

O documento reconhece que as quatro histórias ainda requerem owner, effort e DoR em [CMP-FD-02:5](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-codex-review/docs/planning/conversational-full-duplex/CMP-FD-02-ADDITIVE-STORIES-AND-ORACLES.md:5).

As linhas chamadas de “Fixture e passos futuros” são cenários resumidos, não fixtures materializadas. Não contêm IDs, eventos completos, contadores iniciais, timestamps, payloads, expectativas campo a campo ou artefatos esperados.

**Correção requerida:** materializar fixtures e passos determinísticos antes de qualquer gate de implementação.

## 3. Decisões do Founder

A ata é consistente com o pacote de deliberação:

| AQ | Resultado da auditoria |
|---|---|
| AQ-01 | Aprovação humana fiel; implementação financeira ainda ausente |
| AQ-02 | Aprovação humana fiel; incompatibilidade de schema ainda aberta |
| AQ-03 | Aprovação humana fiel; continua dependente do gate FDP-15 |
| AQ-05 | Aprovação humana fiel; enforcement local/externo incompleto |
| AQ-06 | Aprovação humana fiel; lifecycle de buffers e transcrição incompleto |
| AQ-07 | Aprovação humana fiel; especificação não prova full-duplex real |
| AQ-08 | Aprovação humana fiel; revogação concorrente incompleta |
| AQ-10 | Aprovação humana fiel; ledger único preservado conceitualmente |
| AQ-11 | Aprovação humana fiel; hard gates fora da voz preservados |
| AQ-04 | Continua diferida e não decidida |
| AQ-09 | Continua diferida e não decidida |
| AQ-12 | Continua diferida e não decidida |

Não identifiquei seleção implícita de fornecedor. Não identifiquei autorização de compartilhamento com Founder OS. A regra HELD sem prova conclusiva é preservada conceitualmente.

## 4. Independência do revisor

Não identifiquei regressão documental direta no princípio de independência:

- Codex conversacional continua read-only.
- Chat, Jarvis e Conselho não iniciam review formal.
- O review formal continua dependente de principal, runtime, processo, instância e credencial host-attested distintos.
- CMP-O-28 da v0.3 continua NOT RUN.

Contudo, CMP-FD-O12 não substitui nem reexecuta a fixture adversarial completa de CMP-O-28. Ele deve referenciá-la normativamente, e não ser usado sozinho como prova de independência.

## 5. Gates remanescentes

Antes de integração ou BUILD-00, continuam obrigatórios:

1. Correção dos HIGH-01, HIGH-02 e HIGH-03 deste parecer.
2. Delta contratual formal para FDP-16A e FDP-15.
3. Deliberação humana separada de FDP-14.
4. Deliberação humana separada de FDP-15.
5. Aprovação explícita da baseline consolidada.
6. Owner, effort e DoR das quatro histórias CMP-FD.
7. Materialização e execução futura dos 12 CMP-FD-O.
8. Execução futura dos 36 CMP-O v0.3, inclusive CMP-O-28.
9. Preservação dos 91 oráculos históricos v1.7.
10. Ato separado e explícito autorizando BUILD-00.

## 6. Registro de execução

- Testes: **NOT RUN**
- Builds: **NOT RUN**
- Checkers: **NOT RUN**
- Providers: **NOT RUN**
- Banco/staging/APIs: **NOT RUN**
- Oráculos CMP-FD: **12 NOT RUN; evidence ABSENT**
- Oráculos CMP v0.3: **36 NOT RUN; evidence ABSENT**
- Oráculos v1.7: **não executados nesta revisão**
- Arquivos alterados: **nenhum**
- Aprovação técnica inferida das decisões do Founder: **nenhuma**
- BUILD-00: **NÃO AUTORIZADO**

**Veredito final: FAIL — DOCUMENT-ONLY.** As decisões humanas foram registradas corretamente, mas o pacote parcial ainda não possui contratos e oráculos suficientes para aprovação técnica de full-duplex simultâneo real nem para integração segura com o ledger v1.7.