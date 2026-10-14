# PARECER INDEPENDENTE CODEX — CONVERSATIONAL FULL-DUPLEX v0.2

**Data:** 13 de outubro de 2026  
**SHA declarado do checkout:** `18aa352e7bf987aa3a2550b2e2b3251ce71c1f7d`  
**Modalidade:** auditoria documental independente, somente leitura  
**Veredito:** **FAIL**

O SHA foi fornecido como escopo da revisão. A política do ambiente bloqueou acesso ao conteúdo de `.git` e a execução de `git rev-parse`; portanto, não foi possível atestá-lo independentemente. Nenhum teste, build, checker, provider, banco, staging ou API de produto foi executado.

O parecer não pôde ser persistido em `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.2-2026-10-13.md`, pois o checkout é read-only e o pedido proíbe alterações. O texto integral está registrado nesta saída.

## 1. Escopo efetivamente examinado

Foram examinados:

- os 13 arquivos de `docs/planning/conversational-full-duplex-v0.2/`;
- `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.1-2026-10-13.md`;
- `docs/reviews/PROMPT-GROK-FULL-DUPLEX-v0.2-CORRECTIVE.md`;
- a Ata Founder e o ADR AQ-07;
- o pacote `docs/planning/conversational-mvp-v0.3/`;
- o pacote full-duplex v0.1;
- FDP-16/FDP-16A v1.7;
- FDP-15 histórico;
- contratos de Build, Task, TaskAttempt, Operation, atores, autorização, ledger, proof, idempotência e adapters relevantes.

O `CMP-FD-10-FINDING-DISPOSITION.md` e o relatório de consistência do autor foram tratados somente como índices de alegações, nunca como evidência de fechamento.

## 2. Conclusão executiva

A v0.2 é uma correção documental substancial, mas ainda não é uma especificação integrável.

Resultados dos achados anteriores:

| Finding anterior | Resultado |
|---|---|
| HIGH-01 — ledger, ator e Task-âncora | **PARTIAL** |
| HIGH-02 — prova de full-duplex real | **PARTIAL** |
| HIGH-03 — `cmp.media.duplex.v1` implementável | **PARTIAL** |
| MEDIUM-01 — cancelamento/retry | **CLOSED** documentalmente |
| MEDIUM-02 — revogação concorrente | **CLOSED** documentalmente |
| MEDIUM-03 — trust boundary | **CLOSED** documentalmente |
| MEDIUM-04 — identidade/proveniência | **CLOSED** documentalmente |
| MEDIUM-05 — latência/qualidade | **CLOSED** documentalmente |
| LOW-01 — DoR e fixtures | **PARTIAL** |

Bloqueios determinantes do `FAIL`:

1. A autorização financeira lê `headroom` e outros estados antes de especificar o lock obrigatório do Build.
2. O limite financeiro do novo Build é fornecido pelo comando de abertura sem fonte autorizativa ou teto pai, permitindo multiplicação de orçamento por sessão.
3. Não há regras explícitas suficientes para impedir associação cross-tenant/cross-project entre comando, sessão, Build, Task e Operation.
4. O schema `cmp.media.duplex.v1` omite justamente os campos temporais usados para provar simultaneidade e não define payloads tipados por evento.
5. A fixture de full-duplex é conceitualmente forte, mas não é executável contra o schema publicado.

## 3. Reavaliação dos findings anteriores

### HIGH-01 — PARTIAL

#### O que foi corrigido

O pacote agora propõe explicitamente:

- `conversation_router` como novo ator, sem impersonar `coding_engine`: `CMP-FD-01-LEDGER-DELTA.md:27-43`;
- comando próprio `ReserveConversationalCapability`: `CMP-FD-01-LEDGER-DELTA.md:45-96`;
- Policy Service externo ao LLM: `CMP-FD-01-LEDGER-DELTA.md:75`;
- mesmo ledger, mesma reserva e mesma origem de proof: `CMP-FD-01-LEDGER-DELTA.md:77-96,217-225`;
- Build `CONVERSATIONAL_ANCHOR`: `CMP-FD-01-LEDGER-DELTA.md:104-131`;
- `Task.build_id` preservado como NOT NULL: `CMP-FD-01-LEDGER-DELTA.md:102,144`;
- isolamento do DAG e proibição de attempt/worktree: `CMP-FD-01-LEDGER-DELTA.md:146-157,182-188`;
- lifecycle e orphan cleanup: `CMP-FD-01-LEDGER-DELTA.md:159-180`;
- denylist de deploy/terminal/vault: `CMP-FD-01-LEDGER-DELTA.md:190-205`;
- ordem proposta de migração e condição de rollback: `CMP-FD-01-LEDGER-DELTA.md:227-254`.

Isso resolve a lacuna estrutural mais evidente da v0.1.

#### Contradição bloqueante: lock order

O documento afirma que o authorizer verifica, “na mesma transação e nesta ordem”, inclusive `headroom`, `stop_latch` e reconciliação em `CMP-FD-01-LEDGER-DELTA.md:75`. O lock do Build aparece somente depois, no efeito comprometido, em `CMP-FD-01-LEDGER-DELTA.md:77-84`.

O contrato v1.7 exige:

- Build `FOR UPDATE` como primeiro lock: `FDP-16A-v1.7-EXECUTION-CONTRACTS.md:360-361`;
- Operation depois: `FDP-16A-v1.7-EXECUTION-CONTRACTS.md:362`;
- Reservation depois: `FDP-16A-v1.7-EXECUTION-CONTRACTS.md:363`;
- ManualReconciliation por último: `FDP-16A-v1.7-EXECUTION-CONTRACTS.md:364`.

Logo, o texto corretivo permite interpretar que o headroom é lido antes do lock que serializa o orçamento. Duas reservas podem autorizar sobre o mesmo saldo observado. A constraint final pode rejeitar uma intenção duplicada, mas não duas intenções distintas que juntas excedam o limite.

**Correção precisa:** tornar normativa uma única transação em que o Build correspondente à Task seja resolvido e bloqueado antes de qualquer leitura de headroom, `stop_latch`, bloqueio de reconciliação ou contador monetário. A autorização não monetária pode ocorrer antes; toda decisão dependente do estado financeiro deve ocorrer depois do lock.

#### Contradição bloqueante: origem do orçamento

`OpenConversationalAnchor` recebe `budget_limit_minor` diretamente no payload em `CMP-FD-01-LEDGER-DELTA.md:163-166`. O único requisito indicado é que o humano esteja autenticado no projeto. O valor é copiado para o Build em `CMP-FD-01-LEDGER-DELTA.md:119`.

O texto admite não haver teto agregado além do limite de cada âncora em `CMP-FD-01-LEDGER-DELTA.md:225`. Assim:

1. um membro abre sessão A com limite X;
2. abre sessão B com limite X;
3. cada Build satisfaz localmente `spent + reserved <= limit`;
4. o gasto agregado chega a 2X sem violação local.

Isso é incompatível com a noção aprovada de “teto monetário único no ledger v1.7” da Ata, `ATA-FOUNDER-AQS-CONVERSATIONAL-2026-10-13.md:23`, e com a formulação anterior de “ledger existente do projeto” em `conversational-mvp-v0.3/CMP-OPEN-QUESTIONS.md:75`.

**Correção precisa:** o comando de abertura não pode escolher seu próprio teto. Deve referenciar uma autorização de orçamento existente, derivar o limite de uma policy imutável ou reservar sob um agregado pai comum. Se houver sub-limite por sessão, a soma deve continuar bloqueada por um teto autorizado superior.

#### Cross-tenant/cross-project insuficiente

O request contém `organization_id`, `project_id`, `task_id` e `build_id` em `CMP-FD-01-LEDGER-DELTA.md:56-62`, mas não há predicado expresso exigindo:

- organização do comando = organização da sessão;
- organização/projeto da Task = organização/projeto do Build;
- organização/projeto da Operation = organização/projeto da Task;
- `build_id` fornecido = Build realmente referenciado pela Task;
- canal autenticado = mesma organização/projeto do comando.

FDP-16A exige header durável com organização/projeto e projeto pertencente à mesma organização em `FDP-16A-v1.7-EXECUTION-CONTRACTS.md:23-32`.

**Correção precisa:** inserir validação transacional explícita de toda a cadeia e oráculo negativo com UUIDs válidos, porém pertencentes a organizações/projetos diferentes. O resultado deve ser `403`/`422`, zero Operation, zero Reservation e zero alteração de contadores.

#### Migração/rollback ainda incompletos

O rollback diz apenas que os valores de enum e colunas “podem ser retirados” se não houver anchors/operations relevantes, em `CMP-FD-01-LEDGER-DELTA.md:250-254`. Não define:

- tratamento de linhas `SESSION_CLOSED`;
- downgrade de consumidores que já persistiram os novos enums;
- remoção segura de valores de enum/check constraints;
- validação de referências em audit/outbox;
- rollback parcial entre passos 1–9;
- prova de que não existem events ou foreign keys dependentes.

**Resultado:** HIGH-01 melhora materialmente, mas permanece bloqueante.

### HIGH-02 — PARTIAL

#### O que foi corrigido

A fixture agora exige:

- intervalos explícitos de captura e playback: `CMP-FD-07-STORIES-ORACLES-FIXTURES.md:50-54`;
- chunk de entrada aceito e encaminhado ao STT durante playback: `CMP-FD-07:58-63,84`;
- chunk efetivamente reproduzido durante captura: `CMP-FD-07:62,85`;
- playback posterior ao primeiro input: `CMP-FD-07:76,86`;
- STT aberto antes de `STOP_LOCAL`: `CMP-FD-07:74`;
- proibição de pausa/stop antes do primeiro forward: `CMP-FD-07:88`;
- distinção entre generated, received e reproduced: `CMP-FD-07:89`;
- anti-fixture pause-before-capture: `CMP-FD-07:177-184`;
- anti-fixture generated-but-not-reproduced: `CMP-FD-07:185-189`.

Esse predicado distingue corretamente full-duplex físico de barge-in half-duplex.

#### Por que não está fechado

Os timestamps usados pelo predicado — `generated_at_ns`, `received_at_ns`, `reproduced_at_ns`, `captured_at_ns`, `gateway_accepted_at_ns` e `stt_forward_at_ns` — não constam da tabela tipada do envelope em `CMP-FD-02-MEDIA-CONTRACT.md:38-81`. Eles aparecem apenas em prosa posterior, em `CMP-FD-02:153-173`.

Como campos desconhecidos devem ser rejeitados em `CMP-FD-02:36`, uma implementação literal do schema rejeitaria os próprios campos requeridos pela fixture.

Além disso, o controle de eco em CMP-FD-O28 parte de um frame já marcado `echo=true`, `CMP-FD-07:290-297`; ele testa a reação à classificação pronta, mas não torna falsificável como a classificação foi obtida nem protege contra falso positivo que descarte fala humana sobreposta.

**Correção precisa:** incorporar os seis timestamps ao schema tipado, definir nulabilidade por `event_type`, origem do relógio, processo observador e correlação entre relógios. Para eco/VAD, especificar input de referência, critério de classificação, caso misto eco+fala humana e oráculo negativo contra fechamento do microfone.

### HIGH-03 — PARTIAL

O envelope melhorou consideravelmente: identidade, turn/invocation, direção, codec, tamanho, hash, sequence, ack, epochs, classification, trust boundary e `operation_ref` estão em `CMP-FD-02-MEDIA-CONTRACT.md:38-81`. Há lifecycle em `:85-104`, eventos em `:106-127`, backpressure em `:135-151`, erros em `:183-198` e crosswalk em `:200-225`.

Ainda assim, não é schema completo:

- timestamps normativos usados pelos oráculos estão ausentes da tabela;
- `transcript_state` é usado em `:113-114,206-207`, mas não está no schema do evento;
- `cancel_state` é usado em `:118,210-211`, mas não possui payload tipado;
- `discontinuity=true` é usado em `:147`, mas não existe na tabela;
- `provider_id` e `model_id` aparecem no crosswalk em `:217`, não no envelope;
- o objeto `ERROR` não possui shape, campos obrigatórios ou vínculo com `invocation_id`;
- `PLAYBACK_SPAN` não define payload de início/fim;
- `HELLO`/`HELLO_ACK` são listados no catálogo, mas o envelope é descrito como aplicável somente “depois do handshake” em `:34`;
- `stream_id` é “um stream por direção” em `:44`, mas não há regra para qual stream contém eventos `CONTROL`;
- a deduplicação de `event_id` não define digest canônico persistido que diferencie replay idêntico de mesmo ID com payload diferente.

**Correção precisa:** publicar schemas discriminados por `event_type`, com payloads completos e uma união fechada; definir o stream/sequence scope de CONTROL; incluir digest do evento e algoritmo de canonicalização; alinhar cada campo com o request/result/cancel/error de `cmp.speech.v0`.

### MEDIUM-01 — CLOSED documentalmente

Duck, stop local e cancel são separados em `CMP-FD-03-LIFECYCLE.md:7-24`. TTS possui estados `CANCEL_CONFIRMED`, `CANCEL_UNCONFIRMED` e `UNCERTAIN` em `:37-52`. Redespacho após incerteza é proibido e HELD é preservado em `:52,65-67,80,96-101`.

Fechamento é documental; nenhuma máquina foi executada.

### MEDIUM-02 — CLOSED documentalmente

Foram definidos:

- `consent_grant_epoch` e `capture_generation`: `CMP-FD-04-POLICY-SECURITY-PRIVACY.md:13-18`;
- comparação atômica e rejeição de epoch antiga: `:18-20`;
- descarte de buffers, sealing de bytes já enviados e cancel: `:22-29`;
- background/crash/reconnect sem reabertura automática: `:31-34`;
- quatro pontos distintos de observação: `:36-45`;
- oráculos concorrentes O19–O22.

O deadline numérico permanece `PENDING CALIBRATION`, mas a regra de segurança não depende dele: o aceite posterior ao corte é proibido atomicamente.

### MEDIUM-03 — CLOSED documentalmente

A fonte de verdade é o registry validado pela Policy Service, não a autodeclaração do adapter, em `CMP-FD-04:47-53`. Cada egress é reautorizado em `:55-61`. A matriz PUBLIC/INTERNAL/CONFIDENTIAL/RESTRICTED está em `:64-73`, com troca de classe, fallback e projeto em `:75-86`.

### MEDIUM-04 — CLOSED documentalmente

Foram restaurados `turn_id`, `speaker_agent_id`, `origin`, `source_turn_ids`, `evidence_refs` e `epistemic_label` em `CMP-FD-05-UX.md:36-45`. Falsa atribuição ao Codex é recusada em `:47`; CMP-O-28 formal permanece separado em `:30,47`.

### MEDIUM-05 — CLOSED documentalmente

Os pontos de medida estão especificados em `CMP-FD-06-OBSERVABILITY.md:21-34`. Aceites continuam `PENDING CALIBRATION`, tolerância de campo é nula em `:15`, e percentis permanecem `null` em `:36`. Não há SLA ou medição fabricada.

### LOW-01 — PARTIAL

As fixtures estão muito mais específicas e falsificáveis. Porém, as sete histórias permanecem com owner `PENDING`, effort `UNSTATED` e DoR `NOT MET` em `CMP-FD-07:13-23`.

Isso é corretamente confessado, não mascarado, mas o finding original incluía prontidão das histórias. Logo, somente a metade relativa às fixtures foi corrigida.

## 4. Novos findings

### NEW-HIGH-01 — Autoridade de orçamento multiplicável por sessão

**Reprodução documental:**

1. `OpenConversationalAnchor` aceita `budget_limit_minor` do request: `CMP-FD-01:163-166`.
2. O valor é copiado ao novo Build: `CMP-FD-01:119`.
3. Uma nova sessão cria novo par Build+Task: `CMP-FD-01:146`.
4. Não existe teto agregado: `CMP-FD-01:225`.

Um membro de projeto pode, conforme o texto atual, criar sucessivos envelopes financeiros independentes. Não há capability específica para estabelecer o valor, teto derivado, aprovação ou CAS contra um agregado pai.

**Correção:** separar `OpenConversationalAnchor` de concessão de orçamento. O comando deve receber `budget_authorization_ref`, derivar o limite de uma policy assinada e bloquear o agregado financeiro pai antes de criar o sub-limite.

### NEW-HIGH-02 — Ordem autorizativa diverge do protocolo único de concorrência

`CMP-FD-01:75` lê headroom antes do lock descrito em `:79`. FDP-16A exige Build lock primeiro em `FDP-16A:360-364`.

**Correção:** reescrever o algoritmo como passos transacionais únicos, incluindo resolução e validação tenant/project, lock, leitura de contadores, dedupe, insert de Operation/Reservation, incremento, audit/outbox e commit.

### NEW-HIGH-03 — Relações cross-tenant não têm predicado nem oráculo adversarial

O pacote possui os identificadores, mas não exige documentalmente igualdade de escopo em toda a cadeia. CMP-FD-O10 cobre troca de projeto na experiência, não tentativa de usar Task/Build de outro tenant numa reserva.

**Correção:** constraint/FK composta ou checks equivalentes e novo oracle com:

- channel/org A;
- project A;
- task/build pertencente a org B ou project B;
- zero linha/zero reserva/zero evento de sucesso;
- evento de negação sem vazar existência do recurso estrangeiro.

### NEW-MEDIUM-01 — `expected_version` contraditório e sem erro correspondente

`expected_version` é nullable mas “obrigatório se a task já existe, que é o caso” em `CMP-FD-01:68`. A lista de erros em `:88` não contém `409 VERSION_CONFLICT`. Isso enfraquece o CAS e não define replay quando a versão diverge.

**Correção:** tornar o campo não nulo para a reserva, indicar qual aggregate/version ele referencia e adicionar semântica exata de `VERSION_CONFLICT`.

### NEW-MEDIUM-02 — Schema fechado rejeita campos necessários à própria fixture

`CMP-FD-02:36` rejeita campos desconhecidos. Os timestamps de simultaneidade aparecem somente em `:153-173`, fora da tabela `:38-81`.

**Correção:** integrar os campos ao schema discriminado antes de considerar a fixture implementável.

### NEW-MEDIUM-03 — Oráculo de eco confia na classificação que deveria testar

CMP-FD-O28 recebe `echo=true` como fato de entrada em `CMP-FD-07:290-297`. Isso não testa AEC/VAD nem o caso em que fala humana e eco coexistem.

**Correção:** fixture com sinal de referência de playback, captura composta e expectativa de preservar a fala humana enquanto remove apenas o componente de eco.

## 5. Governança e preservação

A preservação das decisões humanas está correta:

- APPROVED: AQ-01, 02, 03, 05, 06, 07, 08, 10 e 11;
- DEFERRED/UNDECIDED: AQ-04, 09 e 12.

Evidência: `CMP-FD-00-INDEX.md:42-49`, `CMP-FD-08-TRACEABILITY.md:7-20` e Ata Founder.

Também permanecem corretamente pendentes:

- FDP-14;
- FDP-15;
- incorporação do delta à baseline;
- consolidação da baseline;
- BUILD-00.

Evidência: `CMP-FD-11-OPEN-QUESTIONS.md:13-22`.

Não identifiquei escolha implícita de fornecedor, compartilhamento implícito com Founder OS ou autorização de BUILD-00.

## 6. Independência CMP-O-28

A independência formal foi preservada documentalmente:

- Codex conversacional continua `CODEX_READ_ONLY`;
- CMP-FD-O12 apenas referencia CMP-O-28;
- CMP-O-28 continua NOT RUN;
- CMP-FD-O27 e CMP-FD-O28 não o substituem.

Evidência: `CMP-FD-04:94`, `CMP-FD-05:30,47`, `CMP-FD-07:169-171,288-292`.

Não há regressão documental neste ponto.

## 7. Estado de execução

- Testes: **NOT RUN**
- Builds: **NOT RUN**
- Providers: **NOT RUN**
- Banco/staging/APIs: **NOT RUN**
- CMP-FD-O01..O12: **NOT RUN; evidence ABSENT**
- CMP-FD-O13..O34: **NOT RUN; evidence ABSENT**
- CMP-O-01..O36: **NOT RUN; evidence ABSENT**
- 91 oráculos v1.7: **não executados nesta revisão**
- Aprovação operacional: **nenhuma**
- BUILD-00: **NÃO AUTORIZADO**

## 8. Gate recommendation

**FAIL. Não integrar `forge.conversation.delta.v1`, não aprovar o contrato full-duplex e não autorizar BUILD-00.**

Condições mínimas para nova auditoria:

1. Corrigir a ordem transacional do ledger.
2. Definir autoridade e teto agregado para `budget_limit_minor`.
3. Fechar invariantes cross-tenant/cross-project e seus oráculos negativos.
4. Tornar `expected_version` e CAS inequívocos.
5. Publicar schemas discriminados completos de todos os eventos.
6. Incorporar os timestamps usados pela fixture ao schema.
7. Completar o oracle de eco/VAD.
8. Manter todos os oráculos como NOT RUN até execução real.
9. Preservar FDP-14, FDP-15, baseline e BUILD-00 como gates humanos separados.
10. Submeter a nova versão a revisão Codex independente read-only.

**Veredito final: FAIL — DOCUMENT-ONLY.** A v0.2 corrige grande parte da intenção, mas ainda contém falhas normativas de concorrência financeira, autoridade de orçamento, isolamento de tenant e completude do contrato de mídia.
tokens used
154.383
# PARECER INDEPENDENTE CODEX — CONVERSATIONAL FULL-DUPLEX v0.2

**Data:** 13 de outubro de 2026  
**SHA declarado do checkout:** `18aa352e7bf987aa3a2550b2e2b3251ce71c1f7d`  
**Modalidade:** auditoria documental independente, somente leitura  
**Veredito:** **FAIL**

O SHA foi fornecido como escopo da revisão. A política do ambiente bloqueou acesso ao conteúdo de `.git` e a execução de `git rev-parse`; portanto, não foi possível atestá-lo independentemente. Nenhum teste, build, checker, provider, banco, staging ou API de produto foi executado.

O parecer não pôde ser persistido em `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.2-2026-10-13.md`, pois o checkout é read-only e o pedido proíbe alterações. O texto integral está registrado nesta saída.

## 1. Escopo efetivamente examinado

Foram examinados:

- os 13 arquivos de `docs/planning/conversational-full-duplex-v0.2/`;
- `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.1-2026-10-13.md`;
- `docs/reviews/PROMPT-GROK-FULL-DUPLEX-v0.2-CORRECTIVE.md`;
- a Ata Founder e o ADR AQ-07;
- o pacote `docs/planning/conversational-mvp-v0.3/`;
- o pacote full-duplex v0.1;
- FDP-16/FDP-16A v1.7;
- FDP-15 histórico;
- contratos de Build, Task, TaskAttempt, Operation, atores, autorização, ledger, proof, idempotência e adapters relevantes.

O `CMP-FD-10-FINDING-DISPOSITION.md` e o relatório de consistência do autor foram tratados somente como índices de alegações, nunca como evidência de fechamento.

## 2. Conclusão executiva

A v0.2 é uma correção documental substancial, mas ainda não é uma especificação integrável.

Resultados dos achados anteriores:

| Finding anterior | Resultado |
|---|---|
| HIGH-01 — ledger, ator e Task-âncora | **PARTIAL** |
| HIGH-02 — prova de full-duplex real | **PARTIAL** |
| HIGH-03 — `cmp.media.duplex.v1` implementável | **PARTIAL** |
| MEDIUM-01 — cancelamento/retry | **CLOSED** documentalmente |
| MEDIUM-02 — revogação concorrente | **CLOSED** documentalmente |
| MEDIUM-03 — trust boundary | **CLOSED** documentalmente |
| MEDIUM-04 — identidade/proveniência | **CLOSED** documentalmente |
| MEDIUM-05 — latência/qualidade | **CLOSED** documentalmente |
| LOW-01 — DoR e fixtures | **PARTIAL** |

Bloqueios determinantes do `FAIL`:

1. A autorização financeira lê `headroom` e outros estados antes de especificar o lock obrigatório do Build.
2. O limite financeiro do novo Build é fornecido pelo comando de abertura sem fonte autorizativa ou teto pai, permitindo multiplicação de orçamento por sessão.
3. Não há regras explícitas suficientes para impedir associação cross-tenant/cross-project entre comando, sessão, Build, Task e Operation.
4. O schema `cmp.media.duplex.v1` omite justamente os campos temporais usados para provar simultaneidade e não define payloads tipados por evento.
5. A fixture de full-duplex é conceitualmente forte, mas não é executável contra o schema publicado.

## 3. Reavaliação dos findings anteriores

### HIGH-01 — PARTIAL

#### O que foi corrigido

O pacote agora propõe explicitamente:

- `conversation_router` como novo ator, sem impersonar `coding_engine`: `CMP-FD-01-LEDGER-DELTA.md:27-43`;
- comando próprio `ReserveConversationalCapability`: `CMP-FD-01-LEDGER-DELTA.md:45-96`;
- Policy Service externo ao LLM: `CMP-FD-01-LEDGER-DELTA.md:75`;
- mesmo ledger, mesma reserva e mesma origem de proof: `CMP-FD-01-LEDGER-DELTA.md:77-96,217-225`;
- Build `CONVERSATIONAL_ANCHOR`: `CMP-FD-01-LEDGER-DELTA.md:104-131`;
- `Task.build_id` preservado como NOT NULL: `CMP-FD-01-LEDGER-DELTA.md:102,144`;
- isolamento do DAG e proibição de attempt/worktree: `CMP-FD-01-LEDGER-DELTA.md:146-157,182-188`;
- lifecycle e orphan cleanup: `CMP-FD-01-LEDGER-DELTA.md:159-180`;
- denylist de deploy/terminal/vault: `CMP-FD-01-LEDGER-DELTA.md:190-205`;
- ordem proposta de migração e condição de rollback: `CMP-FD-01-LEDGER-DELTA.md:227-254`.

Isso resolve a lacuna estrutural mais evidente da v0.1.

#### Contradição bloqueante: lock order

O documento afirma que o authorizer verifica, “na mesma transação e nesta ordem”, inclusive `headroom`, `stop_latch` e reconciliação em `CMP-FD-01-LEDGER-DELTA.md:75`. O lock do Build aparece somente depois, no efeito comprometido, em `CMP-FD-01-LEDGER-DELTA.md:77-84`.

O contrato v1.7 exige:

- Build `FOR UPDATE` como primeiro lock: `FDP-16A-v1.7-EXECUTION-CONTRACTS.md:360-361`;
- Operation depois: `FDP-16A-v1.7-EXECUTION-CONTRACTS.md:362`;
- Reservation depois: `FDP-16A-v1.7-EXECUTION-CONTRACTS.md:363`;
- ManualReconciliation por último: `FDP-16A-v1.7-EXECUTION-CONTRACTS.md:364`.

Logo, o texto corretivo permite interpretar que o headroom é lido antes do lock que serializa o orçamento. Duas reservas podem autorizar sobre o mesmo saldo observado. A constraint final pode rejeitar uma intenção duplicada, mas não duas intenções distintas que juntas excedam o limite.

**Correção precisa:** tornar normativa uma única transação em que o Build correspondente à Task seja resolvido e bloqueado antes de qualquer leitura de headroom, `stop_latch`, bloqueio de reconciliação ou contador monetário. A autorização não monetária pode ocorrer antes; toda decisão dependente do estado financeiro deve ocorrer depois do lock.

#### Contradição bloqueante: origem do orçamento

`OpenConversationalAnchor` recebe `budget_limit_minor` diretamente no payload em `CMP-FD-01-LEDGER-DELTA.md:163-166`. O único requisito indicado é que o humano esteja autenticado no projeto. O valor é copiado para o Build em `CMP-FD-01-LEDGER-DELTA.md:119`.

O texto admite não haver teto agregado além do limite de cada âncora em `CMP-FD-01-LEDGER-DELTA.md:225`. Assim:

1. um membro abre sessão A com limite X;
2. abre sessão B com limite X;
3. cada Build satisfaz localmente `spent + reserved <= limit`;
4. o gasto agregado chega a 2X sem violação local.

Isso é incompatível com a noção aprovada de “teto monetário único no ledger v1.7” da Ata, `ATA-FOUNDER-AQS-CONVERSATIONAL-2026-10-13.md:23`, e com a formulação anterior de “ledger existente do projeto” em `conversational-mvp-v0.3/CMP-OPEN-QUESTIONS.md:75`.

**Correção precisa:** o comando de abertura não pode escolher seu próprio teto. Deve referenciar uma autorização de orçamento existente, derivar o limite de uma policy imutável ou reservar sob um agregado pai comum. Se houver sub-limite por sessão, a soma deve continuar bloqueada por um teto autorizado superior.

#### Cross-tenant/cross-project insuficiente

O request contém `organization_id`, `project_id`, `task_id` e `build_id` em `CMP-FD-01-LEDGER-DELTA.md:56-62`, mas não há predicado expresso exigindo:

- organização do comando = organização da sessão;
- organização/projeto da Task = organização/projeto do Build;
- organização/projeto da Operation = organização/projeto da Task;
- `build_id` fornecido = Build realmente referenciado pela Task;
- canal autenticado = mesma organização/projeto do comando.

FDP-16A exige header durável com organização/projeto e projeto pertencente à mesma organização em `FDP-16A-v1.7-EXECUTION-CONTRACTS.md:23-32`.

**Correção precisa:** inserir validação transacional explícita de toda a cadeia e oráculo negativo com UUIDs válidos, porém pertencentes a organizações/projetos diferentes. O resultado deve ser `403`/`422`, zero Operation, zero Reservation e zero alteração de contadores.

#### Migração/rollback ainda incompletos

O rollback diz apenas que os valores de enum e colunas “podem ser retirados” se não houver anchors/operations relevantes, em `CMP-FD-01-LEDGER-DELTA.md:250-254`. Não define:

- tratamento de linhas `SESSION_CLOSED`;
- downgrade de consumidores que já persistiram os novos enums;
- remoção segura de valores de enum/check constraints;
- validação de referências em audit/outbox;
- rollback parcial entre passos 1–9;
- prova de que não existem events ou foreign keys dependentes.

**Resultado:** HIGH-01 melhora materialmente, mas permanece bloqueante.

### HIGH-02 — PARTIAL

#### O que foi corrigido

A fixture agora exige:

- intervalos explícitos de captura e playback: `CMP-FD-07-STORIES-ORACLES-FIXTURES.md:50-54`;
- chunk de entrada aceito e encaminhado ao STT durante playback: `CMP-FD-07:58-63,84`;
- chunk efetivamente reproduzido durante captura: `CMP-FD-07:62,85`;
- playback posterior ao primeiro input: `CMP-FD-07:76,86`;
- STT aberto antes de `STOP_LOCAL`: `CMP-FD-07:74`;
- proibição de pausa/stop antes do primeiro forward: `CMP-FD-07:88`;
- distinção entre generated, received e reproduced: `CMP-FD-07:89`;
- anti-fixture pause-before-capture: `CMP-FD-07:177-184`;
- anti-fixture generated-but-not-reproduced: `CMP-FD-07:185-189`.

Esse predicado distingue corretamente full-duplex físico de barge-in half-duplex.

#### Por que não está fechado

Os timestamps usados pelo predicado — `generated_at_ns`, `received_at_ns`, `reproduced_at_ns`, `captured_at_ns`, `gateway_accepted_at_ns` e `stt_forward_at_ns` — não constam da tabela tipada do envelope em `CMP-FD-02-MEDIA-CONTRACT.md:38-81`. Eles aparecem apenas em prosa posterior, em `CMP-FD-02:153-173`.

Como campos desconhecidos devem ser rejeitados em `CMP-FD-02:36`, uma implementação literal do schema rejeitaria os próprios campos requeridos pela fixture.

Além disso, o controle de eco em CMP-FD-O28 parte de um frame já marcado `echo=true`, `CMP-FD-07:290-297`; ele testa a reação à classificação pronta, mas não torna falsificável como a classificação foi obtida nem protege contra falso positivo que descarte fala humana sobreposta.

**Correção precisa:** incorporar os seis timestamps ao schema tipado, definir nulabilidade por `event_type`, origem do relógio, processo observador e correlação entre relógios. Para eco/VAD, especificar input de referência, critério de classificação, caso misto eco+fala humana e oráculo negativo contra fechamento do microfone.

### HIGH-03 — PARTIAL

O envelope melhorou consideravelmente: identidade, turn/invocation, direção, codec, tamanho, hash, sequence, ack, epochs, classification, trust boundary e `operation_ref` estão em `CMP-FD-02-MEDIA-CONTRACT.md:38-81`. Há lifecycle em `:85-104`, eventos em `:106-127`, backpressure em `:135-151`, erros em `:183-198` e crosswalk em `:200-225`.

Ainda assim, não é schema completo:

- timestamps normativos usados pelos oráculos estão ausentes da tabela;
- `transcript_state` é usado em `:113-114,206-207`, mas não está no schema do evento;
- `cancel_state` é usado em `:118,210-211`, mas não possui payload tipado;
- `discontinuity=true` é usado em `:147`, mas não existe na tabela;
- `provider_id` e `model_id` aparecem no crosswalk em `:217`, não no envelope;
- o objeto `ERROR` não possui shape, campos obrigatórios ou vínculo com `invocation_id`;
- `PLAYBACK_SPAN` não define payload de início/fim;
- `HELLO`/`HELLO_ACK` são listados no catálogo, mas o envelope é descrito como aplicável somente “depois do handshake” em `:34`;
- `stream_id` é “um stream por direção” em `:44`, mas não há regra para qual stream contém eventos `CONTROL`;
- a deduplicação de `event_id` não define digest canônico persistido que diferencie replay idêntico de mesmo ID com payload diferente.

**Correção precisa:** publicar schemas discriminados por `event_type`, com payloads completos e uma união fechada; definir o stream/sequence scope de CONTROL; incluir digest do evento e algoritmo de canonicalização; alinhar cada campo com o request/result/cancel/error de `cmp.speech.v0`.

### MEDIUM-01 — CLOSED documentalmente

Duck, stop local e cancel são separados em `CMP-FD-03-LIFECYCLE.md:7-24`. TTS possui estados `CANCEL_CONFIRMED`, `CANCEL_UNCONFIRMED` e `UNCERTAIN` em `:37-52`. Redespacho após incerteza é proibido e HELD é preservado em `:52,65-67,80,96-101`.

Fechamento é documental; nenhuma máquina foi executada.

### MEDIUM-02 — CLOSED documentalmente

Foram definidos:

- `consent_grant_epoch` e `capture_generation`: `CMP-FD-04-POLICY-SECURITY-PRIVACY.md:13-18`;
- comparação atômica e rejeição de epoch antiga: `:18-20`;
- descarte de buffers, sealing de bytes já enviados e cancel: `:22-29`;
- background/crash/reconnect sem reabertura automática: `:31-34`;
- quatro pontos distintos de observação: `:36-45`;
- oráculos concorrentes O19–O22.

O deadline numérico permanece `PENDING CALIBRATION`, mas a regra de segurança não depende dele: o aceite posterior ao corte é proibido atomicamente.

### MEDIUM-03 — CLOSED documentalmente

A fonte de verdade é o registry validado pela Policy Service, não a autodeclaração do adapter, em `CMP-FD-04:47-53`. Cada egress é reautorizado em `:55-61`. A matriz PUBLIC/INTERNAL/CONFIDENTIAL/RESTRICTED está em `:64-73`, com troca de classe, fallback e projeto em `:75-86`.

### MEDIUM-04 — CLOSED documentalmente

Foram restaurados `turn_id`, `speaker_agent_id`, `origin`, `source_turn_ids`, `evidence_refs` e `epistemic_label` em `CMP-FD-05-UX.md:36-45`. Falsa atribuição ao Codex é recusada em `:47`; CMP-O-28 formal permanece separado em `:30,47`.

### MEDIUM-05 — CLOSED documentalmente

Os pontos de medida estão especificados em `CMP-FD-06-OBSERVABILITY.md:21-34`. Aceites continuam `PENDING CALIBRATION`, tolerância de campo é nula em `:15`, e percentis permanecem `null` em `:36`. Não há SLA ou medição fabricada.

### LOW-01 — PARTIAL

As fixtures estão muito mais específicas e falsificáveis. Porém, as sete histórias permanecem com owner `PENDING`, effort `UNSTATED` e DoR `NOT MET` em `CMP-FD-07:13-23`.

Isso é corretamente confessado, não mascarado, mas o finding original incluía prontidão das histórias. Logo, somente a metade relativa às fixtures foi corrigida.

## 4. Novos findings

### NEW-HIGH-01 — Autoridade de orçamento multiplicável por sessão

**Reprodução documental:**

1. `OpenConversationalAnchor` aceita `budget_limit_minor` do request: `CMP-FD-01:163-166`.
2. O valor é copiado ao novo Build: `CMP-FD-01:119`.
3. Uma nova sessão cria novo par Build+Task: `CMP-FD-01:146`.
4. Não existe teto agregado: `CMP-FD-01:225`.

Um membro de projeto pode, conforme o texto atual, criar sucessivos envelopes financeiros independentes. Não há capability específica para estabelecer o valor, teto derivado, aprovação ou CAS contra um agregado pai.

**Correção:** separar `OpenConversationalAnchor` de concessão de orçamento. O comando deve receber `budget_authorization_ref`, derivar o limite de uma policy assinada e bloquear o agregado financeiro pai antes de criar o sub-limite.

### NEW-HIGH-02 — Ordem autorizativa diverge do protocolo único de concorrência

`CMP-FD-01:75` lê headroom antes do lock descrito em `:79`. FDP-16A exige Build lock primeiro em `FDP-16A:360-364`.

**Correção:** reescrever o algoritmo como passos transacionais únicos, incluindo resolução e validação tenant/project, lock, leitura de contadores, dedupe, insert de Operation/Reservation, incremento, audit/outbox e commit.

### NEW-HIGH-03 — Relações cross-tenant não têm predicado nem oráculo adversarial

O pacote possui os identificadores, mas não exige documentalmente igualdade de escopo em toda a cadeia. CMP-FD-O10 cobre troca de projeto na experiência, não tentativa de usar Task/Build de outro tenant numa reserva.

**Correção:** constraint/FK composta ou checks equivalentes e novo oracle com:

- channel/org A;
- project A;
- task/build pertencente a org B ou project B;
- zero linha/zero reserva/zero evento de sucesso;
- evento de negação sem vazar existência do recurso estrangeiro.

### NEW-MEDIUM-01 — `expected_version` contraditório e sem erro correspondente

`expected_version` é nullable mas “obrigatório se a task já existe, que é o caso” em `CMP-FD-01:68`. A lista de erros em `:88` não contém `409 VERSION_CONFLICT`. Isso enfraquece o CAS e não define replay quando a versão diverge.

**Correção:** tornar o campo não nulo para a reserva, indicar qual aggregate/version ele referencia e adicionar semântica exata de `VERSION_CONFLICT`.

### NEW-MEDIUM-02 — Schema fechado rejeita campos necessários à própria fixture

`CMP-FD-02:36` rejeita campos desconhecidos. Os timestamps de simultaneidade aparecem somente em `:153-173`, fora da tabela `:38-81`.

**Correção:** integrar os campos ao schema discriminado antes de considerar a fixture implementável.

### NEW-MEDIUM-03 — Oráculo de eco confia na classificação que deveria testar

CMP-FD-O28 recebe `echo=true` como fato de entrada em `CMP-FD-07:290-297`. Isso não testa AEC/VAD nem o caso em que fala humana e eco coexistem.

**Correção:** fixture com sinal de referência de playback, captura composta e expectativa de preservar a fala humana enquanto remove apenas o componente de eco.

## 5. Governança e preservação

A preservação das decisões humanas está correta:

- APPROVED: AQ-01, 02, 03, 05, 06, 07, 08, 10 e 11;
- DEFERRED/UNDECIDED: AQ-04, 09 e 12.

Evidência: `CMP-FD-00-INDEX.md:42-49`, `CMP-FD-08-TRACEABILITY.md:7-20` e Ata Founder.

Também permanecem corretamente pendentes:

- FDP-14;
- FDP-15;
- incorporação do delta à baseline;
- consolidação da baseline;
- BUILD-00.

Evidência: `CMP-FD-11-OPEN-QUESTIONS.md:13-22`.

Não identifiquei escolha implícita de fornecedor, compartilhamento implícito com Founder OS ou autorização de BUILD-00.

## 6. Independência CMP-O-28

A independência formal foi preservada documentalmente:

- Codex conversacional continua `CODEX_READ_ONLY`;
- CMP-FD-O12 apenas referencia CMP-O-28;
- CMP-O-28 continua NOT RUN;
- CMP-FD-O27 e CMP-FD-O28 não o substituem.

Evidência: `CMP-FD-04:94`, `CMP-FD-05:30,47`, `CMP-FD-07:169-171,288-292`.

Não há regressão documental neste ponto.

## 7. Estado de execução

- Testes: **NOT RUN**
- Builds: **NOT RUN**
- Providers: **NOT RUN**
- Banco/staging/APIs: **NOT RUN**
- CMP-FD-O01..O12: **NOT RUN; evidence ABSENT**
- CMP-FD-O13..O34: **NOT RUN; evidence ABSENT**
- CMP-O-01..O36: **NOT RUN; evidence ABSENT**
- 91 oráculos v1.7: **não executados nesta revisão**
- Aprovação operacional: **nenhuma**
- BUILD-00: **NÃO AUTORIZADO**

## 8. Gate recommendation

**FAIL. Não integrar `forge.conversation.delta.v1`, não aprovar o contrato full-duplex e não autorizar BUILD-00.**

Condições mínimas para nova auditoria:

1. Corrigir a ordem transacional do ledger.
2. Definir autoridade e teto agregado para `budget_limit_minor`.
3. Fechar invariantes cross-tenant/cross-project e seus oráculos negativos.
4. Tornar `expected_version` e CAS inequívocos.
5. Publicar schemas discriminados completos de todos os eventos.
6. Incorporar os timestamps usados pela fixture ao schema.
7. Completar o oracle de eco/VAD.
8. Manter todos os oráculos como NOT RUN até execução real.
9. Preservar FDP-14, FDP-15, baseline e BUILD-00 como gates humanos separados.
10. Submeter a nova versão a revisão Codex independente read-only.

**Veredito final: FAIL — DOCUMENT-ONLY.** A v0.2 corrige grande parte da intenção, mas ainda contém falhas normativas de concorrência financeira, autoridade de orçamento, isolamento de tenant e completude do contrato de mídia.
