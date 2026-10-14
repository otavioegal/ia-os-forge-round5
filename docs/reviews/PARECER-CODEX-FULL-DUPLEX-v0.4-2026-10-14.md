# PARECER INDEPENDENTE CODEX — CONVERSATIONAL FULL-DUPLEX v0.4

**Data:** 14 de outubro de 2026  
**SHA auditado:** `90fc21c90402805959bab2fc4ae6b43dc758c66d`  
**Modalidade:** auditoria documental independente, ambiente isolado, somente leitura  
**Veredito exclusivo:** **FAIL DOCUMENT-ONLY**

O SHA foi confirmado diretamente em `.git/HEAD`, que contém o hash destacado solicitado. O comando `git` foi bloqueado pela política do sandbox; a confirmação ocorreu por leitura direta da referência, sem modificar o checkout.

Nenhum arquivo foi criado ou alterado. Não foram executados testes, verifier, parser, build, migration, banco, provider, staging ou API. Não houve provider real, gasto, mudança de credencial ou integração de flag.

## 1. Escopo examinado

Foram lidos integralmente os 17 arquivos de [conversational-full-duplex-v0.4](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4), incluindo:

- os 14 documentos `CMP-FD-00` a `CMP-FD-13`;
- os oito eventos da fixture JSON, em 480 linhas;
- os oito vetores `canonical_utf8 → sha256`;
- o verificador Python, apenas por inspeção.

Também foram confrontados:

- [parecer Codex v0.3](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.3-2026-10-14.md);
- [prompt corretivo v0.4](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/reviews/PROMPT-GROK-FULL-DUPLEX-v0.4-CORRECTIVE.md);
- contratos full-duplex v0.3 pertinentes;
- `cmp.speech.v0` do CMP v0.3;
- [FDP-16A v1.7](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md);
- [FDP-15 histórico](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/historical/round4/docs/planning/FDP-15-v1.0-INTEGRATION-ADAPTER-SPECIFICATION.md);
- [ata Founder](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/governance/ATA-FOUNDER-AQS-CONVERSATIONAL-2026-10-13.md);
- [gate FDP-14/FDP-15/baseline v1.7](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/governance/FOUNDER-GATE-FDP14-FDP15-BASELINE-v1.7.md).

Os relatórios de consistência e disposição produzidos pelo próprio autor foram tratados como índices de alegações, não como evidência.

## 2. Conclusão executiva

A v0.4 melhora substancialmente o pacote:

- introduz a conta `S + H - E + A <= L`;
- preserva zero movimento quando a fatia falha no caminho comum de `RecordReceipt`;
- leva tenant scope até Operation e Reservation no texto normativo;
- coloca replay antes do CAS;
- separa `HELLO_ACK_SUCCESS` de `HELLO_ACK_ERROR`;
- remove os dois campos conflitantes de `observation`;
- publica fixture, vetores e verifier separados;
- torna a mistura AEC aditiva;
- explicita unicidade de sessão por tenant;
- mantém owners e effort honestamente pendentes.

Ainda assim, o pacote não pode receber PASS documental. Permanecem defeitos normativos materiais:

1. O limite da fatia é aplicado somente ao `RecordReceipt`; `ApplyAuthorizedReconciliation` continua podendo liquidar uma Operation conversacional sem a checagem de `session_slice_minor`.
2. A migration de tenant não fecha o tratamento de linhas existentes nem explicita as chaves únicas exigidas pelas FKs compostas.
3. O ACK não contém um identificador independente do stream reconhecido; amarrá-lo ao `stream_id` do próprio evento torna ambíguo ou impossível reconhecer outro fluxo.
4. A taxonomia de handshake não cobre autenticação/principal incompatível.
5. O verifier não detecta `event_id` duplicado no arquivo de eventos nem vetores não consumidos.
6. A fixture AEC afirma saturação em uma amostra que, conforme a própria fórmula, vale `28000`, não `32767`.
7. A migration da unicidade usa terminologia inconsistente entre `status` e `session_status`.

Não encontrei regressão dos findings anteriormente CLOSED. Há, porém, findings ainda PARTIAL e LOW-01 permanece OPEN BLOCKING.

## 3. Matriz de findings

| Finding | Estado v0.4 | Resultado |
|---|---:|---|
| HIGH-01 | **CLOSED** documentalmente | Lock financeiro Build-first e proibição de ledger paralelo preservados |
| HIGH-02 | **CLOSED** documentalmente | Overlap físico, seis timestamps e `PLAYBACK_SPAN` preservados |
| HIGH-03 | **PARTIAL** | Handshake melhorou; ACK e autenticação ainda incompletos |
| NEW-HIGH-01 | **CLOSED** documentalmente | Root único por organização/projeto preservado |
| NEW-HIGH-02 | **CLOSED** documentalmente | Build pai continua sendo o primeiro lock |
| NEW-HIGH-03 | **PARTIAL** | Predicados foram escritos, mas migration não fecha constraints/backfill |
| NEW-HIGH-04 | **PARTIAL** | `RecordReceipt` foi corrigido; apply manual ainda pode contornar a fatia |
| NEW-MEDIUM-01 | **CLOSED** documentalmente, com clarificação editorial | Lookup durável precede CAS |
| NEW-MEDIUM-02 | **CLOSED** documentalmente | Seis timestamps permanecem no schema fechado |
| NEW-MEDIUM-03 | **PARTIAL** | Mistura é aditiva, mas o vetor de saturação é matematicamente falso |
| NEW-MEDIUM-04 | **CLOSED** documentalmente | Campos foram coerentemente removidos do envelope |
| NEW-MEDIUM-05 | **PARTIAL** | Artefatos existem; verifier não garante bijeção entre eventos e vetores |
| NEW-MEDIUM-06 | **PARTIAL** | Escopo tenant está correto no contrato, mas o DDL normativo é ambíguo |
| MEDIUM-01 | **CLOSED**, preservado | Duck/stop/cancel/HELD continuam separados |
| MEDIUM-02 | **CLOSED**, preservado | Corte atômico e generations preservados |
| MEDIUM-03 | **CLOSED**, preservado | Registry e deny-before-egress preservados |
| MEDIUM-04 | **CLOSED**, preservado | Proveniência e review formal separados |
| MEDIUM-05 | **CLOSED**, preservado | Sem SLA ou números medidos inventados |
| LOW-01 | **OPEN BLOCKING DoR** | Pessoa PENDING, effort UNSTATED, DoR NOT MET |

**REGRESSED:** nenhum finding previamente CLOSED foi objetivamente regredido.

## 4. Findings detalhados

### 4.1 NEW-HIGH-04 — PARTIAL — bypass por reconciliação manual

O caminho comum de `RecordReceipt` agora bloqueia corretamente o settlement quando `S + H - E + A > L`: [CMP-FD-01:33-36](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-01-LEDGER-SETTLEMENT-TENANT-CAS.md:33) e [CMP-FD-01:38-61](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-01-LEDGER-SETTLEMENT-TENANT-CAS.md:38).

O caso adversarial 40/70/50 também exige zero movimento em [CMP-FD-07:45-53](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-07-ORACLES.md:45).

O defeito remanescente é que o delta se define como “RecordReceipt conversacional”. Não há regra equivalente para `ApplyAuthorizedReconciliation`. Na baseline, esse comando pode realizar settlement saindo de `BLOCKED_RECONCILIATION`: [FDP-16A:344-350](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md:344). Portanto:

1. uma Operation entra em conflito;
2. operadores autorizam `PROVEN_RECEIPT`;
3. o apply confirma custo real que cabe no root;
4. sem delta expresso, a baseline verifica apenas o teto do Build;
5. a fatia pode ser rompida pelo caminho manual.

Isso preserva exatamente uma rota para o defeito que NEW-HIGH-04 pretendia fechar.

Também falta definir a transição do `pending_provider_cost` de razão `SESSION_SLICE` quando a fatia é ampliada e o settlement posterior passa. A regra de fecho fala genericamente em “movimento terminal compatível” em [CMP-FD-01:85-87](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-01-LEDGER-SETTLEMENT-TENANT-CAS.md:85), mas a baseline torna pending append-only.

**Correção precisa:**

- aplicar a fórmula de fatia a todo comando capaz de inserir `SETTLEMENT`, inclusive `ApplyAuthorizedReconciliation`;
- no apply que não cabe, manter autorização `AUTHORIZED` e não consumida, reservation `HELD`, Operation `BLOCKED_RECONCILIATION`, zero movimento e pending `SESSION_SLICE`;
- declarar que pending é append-only e que um settlement terminal posterior o torna historicamente resolvido por correlação com o movement, sem update/delete;
- acrescentar oráculo específico para apply manual com `E=40`, `A=70`, `L=50`, root folgado;
- acrescentar race entre `AmendSessionSlice` e `ApplyAuthorizedReconciliation`, ambos serializados pelo mesmo Build lock.

### 4.2 NEW-HIGH-03 — PARTIAL — tenant correto no contrato, incompleto na migration

O contrato agora exige predicados tenant-compostos até Reservation em [CMP-FD-01:89-108](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-01-LEDGER-SETTLEMENT-TENANT-CAS.md:89), resposta 404 opaca e ausência de lock estrangeiro.

O37 também passou a cobrir session, Build, Task, Operation, Reservation e escopo cruzado: [CMP-FD-07:65-80](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-07-ORACLES.md:65).

A migration, contudo, diz que as novas colunas são NOT NULL apenas “nas linhas novas” e que linhas antigas não são reescritas: [CMP-FD-13:9-16](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-13-MIGRATION-ROLLBACK.md:9). Isso não produz uma constraint NOT NULL completa.

Além disso, uma FK para `(organization_id, project_id, operation_id)` exige que a combinação correspondente em Operation seja candidata única. A v0.4 não adiciona ou referencia explicitamente `UNIQUE (organization_id, project_id, id)` em Operation.

**Correção precisa:**

1. adicionar as colunas inicialmente anuláveis;
2. backfill determinístico por join com Operation, com contagem e abort em órfãos;
3. criar/confirmar `UNIQUE (organization_id, project_id, id)` em Operation;
4. criar FK composta `NOT VALID`;
5. validar a FK;
6. aplicar `SET NOT NULL`;
7. impedir ativação da flag enquanto houver linha não validada;
8. adicionar negativos de replay e ingest estrangeiros para Operation e Reservation já existentes, não só novas.

### 4.3 NEW-MEDIUM-01 — CLOSED documentalmente

A ordem normativa agora é inequívoca:

- lookup de `command_id` no passo 7;
- CAS apenas no passo 8;
- definição detalhada em [CMP-FD-01:112-141](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-01-LEDGER-SETTLEMENT-TENANT-CAS.md:112).

O43, O44 e O45 distinguem replay, comando novo com versões antigas e reuse com digest diferente: [CMP-FD-07:82-110](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-07-ORACLES.md:82).

Crash e `40001` não deixam commit parcial. A unicidade `(organization_id, project_id, command_id)` está prevista na migration.

Há uma ambiguidade editorial entre armazenar o `outcome_code` original, inclusive 409, e devolver `200 IDEMPOTENT_REPLAY` “com o outcome guardado”: [CMP-FD-01:121-133](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-01-LEDGER-SETTLEMENT-TENANT-CAS.md:121). Isso não reabre o finding porque a baseline também usa 200 para replay, mas deve ser esclarecido.

**Correção editorial precisa:** definir separadamente `transport_status=200`, `replay=true`, `original_outcome_code` e `original_outcome_body`, evitando a expressão ambígua “outcome anterior”.

### 4.4 HIGH-03 — PARTIAL — ACK e autenticação continuam insuficientes

A separação do preâmbulo é uma correção válida:

- `HELLO`: [CMP-FD-02:13-29](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-02-MEDIA-CONTRACT.md:13);
- `HELLO_ACK_SUCCESS`: [CMP-FD-02:31-48](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-02-MEDIA-CONTRACT.md:31);
- `HELLO_ACK_ERROR`: [CMP-FD-02:50-77](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-02-MEDIA-CONTRACT.md:50);
- payloads, timestamps e crosswalk completo: [CMP-FD-02:153-311](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-02-MEDIA-CONTRACT.md:153).

Não há silent downgrade: erro de negociação tem zero efeito, não cria sessão e não abre microfone.

O ACK, porém, continua estruturalmente incompleto. O envelope possui `ack_of_sequence`, mas não contém `ack_stream_id` ou `ack_sequence_scope`. A regra exige que o scope seja o mesmo do `stream_id` do evento: [CMP-FD-02:96-110](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-02-MEDIA-CONTRACT.md:96).

Consequências:

- um evento CONTROL usa o control stream e não consegue indicar que reconhece INPUT ou OUTPUT;
- um peer não consegue reconhecer o fluxo oposto sem fabricar um evento no próprio stream reconhecido;
- `high_water` não identifica inequivocamente se é o recebido localmente ou o aceito pelo peer;
- O47 cobre ACK futuro e scope errado em prosa, mas não resolve a falta do campo discriminante.

O prompt também exigia autenticação no handshake. `principal_ref` existe, mas não há regra de comparação com o principal autenticado nem código específico para mismatch. `CHANNEL_SCOPE` só descreve org/projeto.

**Correção precisa:**

- acrescentar `ack_stream_id` ou `ack_sequence_scope`, obrigatório quando `ack_of_sequence != null`;
- definir high-water por `{session_id, acknowledged_stream_id, receiver}`;
- permitir ACK no CONTROL stream para INPUT/OUTPUT sem confundi-lo com a sequence do próprio CONTROL;
- definir janela inferior e superior, duplicado, regressão e ACK de stream não alocado;
- acrescentar `PREAMBLE_AUTH` ou incluir explicitamente principal mismatch em `CHANNEL_SCOPE`;
- acrescentar fixture JSON de ACK válido, futuro, regressivo e cross-stream.

### 4.5 NEW-MEDIUM-04 — CLOSED documentalmente

Os dois nomes foram coerentemente retirados do schema de eventos:

- enumeração exata de `observation`: [CMP-FD-02:81-94](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-02-MEDIA-CONTRACT.md:81);
- chaves externas ao envelope: [CMP-FD-02:129-136](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-02-MEDIA-CONTRACT.md:129);
- política: [CMP-FD-04:7-19](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-04-POLICY.md:7);
- observabilidade: [CMP-FD-06:6-12](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-06-OBSERVABILITY.md:6).

Valores permanecem null e `PENDING CALIBRATION`; nenhum número fictício foi introduzido. Presença em evento resulta em `422 UNKNOWN_FIELD`. O48 cobre o negativo.

### 4.6 NEW-MEDIUM-05 — PARTIAL — verifier não garante correspondência bijetiva

A entrega agora contém os três artefatos requeridos:

- [eventos JSON](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/fixtures/CMP-FD-FX-01-events.json);
- [vetores de digest](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/fixtures/CMP-FD-FX-01-digest-vectors.json);
- [verifier](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/tools/check_fd_fx01_digests.py).

O algoritmo do verifier corresponde à descrição de ordenação, separadores, UTF-8 e remoção de `event_digest`: [check_fd_fx01_digests.py:18-49](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/tools/check_fd_fx01_digests.py:18).

Porém, ele só verifica duplicidade de `event_id` nos vetores. Não verifica duplicidade no array de eventos nem que todo vetor foi consumido. Com oito entradas em cada lado, um evento duplicado e um evento ausente podem reutilizar o mesmo vetor enquanto outro vetor permanece ignorado.

Também usa `json.loads` padrão, que aceita chaves JSON duplicadas escolhendo a última; isso reduz a força do artefato como fixture canônica.

**Correção precisa:**

- construir `event_ids` e exigir oito IDs distintos;
- exigir igualdade exata entre os conjuntos de IDs dos eventos e vetores;
- marcar cada vetor consumido exatamente uma vez;
- rejeitar chaves JSON duplicadas via `object_pairs_hook`;
- validar formato e tipo de `event_digest`, `sha256` e `canonical_byte_length`;
- criar negativo estático para evento duplicado, vetor órfão e chave JSON duplicada.

O verifier não foi executado nesta auditoria. A alegação `PASS_FIXTURE_ONLY` do autor não é adotada como evidência independente.

### 4.7 NEW-MEDIUM-03 — PARTIAL — mistura corrigida, saturação incorreta

A fórmula principal foi reparada: [CMP-FD-07:144-155](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-07-ORACLES.md:144) define:

`mic[i] = clamp(echo[i] + human[i])`.

Isso fecha o defeito de sobrescrever o eco com a fala humana.

A amostra de saturação, entretanto, é falsa:

- em `i=1199`, `echo[1199] = reference[719] // 2`;
- `719 // 40 = 17`, ímpar;
- portanto `reference[719] = -8000`;
- `echo[1199] = -4000`;
- `human[1199] = 32000`;
- `mic[1199] = 28000`, sem saturação.

Isso contradiz diretamente [CMP-FD-07:153](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-07-ORACLES.md:153) e torna o critério da linha 163 inadequado.

**Correção precisa:**

- mover a amostra de saturação para um índice de eco positivo, por exemplo `i=1159`, pois `reference[679]` está no bloco positivo;
- definir `human[1159]=32000`;
- esperar `mic[1159]=32767`;
- manter uma amostra distinta de eco negativo para provar cancelamento nos dois sinais;
- no PASS, comparar `forwarded_pcm` com o sinal humano ideal antes do clamp quando recuperável e declarar separadamente o caso irrecuperável por saturação;
- acrescentar falso negativo real: saída que preserva eco durante fala deve reprovar.

### 4.8 NEW-MEDIUM-06 — PARTIAL — contrato correto, predicate de migration ambíguo

A regra principal está correta em [CMP-FD-01:143-151](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-01-LEDGER-SETTLEMENT-TENANT-CAS.md:143):

`(organization_id, project_id, session_id)` para sessões ainda abertas.

O49 e O50 distinguem cross-tenant e duplicata dentro do tenant.

A migration, contudo, diz “onde o status da task está em OPEN, CLOSING, ORPHAN_HELD”: [CMP-FD-13:11](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-13-MIGRATION-ROLLBACK.md:11). Na v0.3:

- `session_status` usa `OPEN`, `CLOSING`, `CLOSED`, `ORPHAN_HELD`;
- `task.status` usa `SESSION_OPEN`, `SESSION_CLOSING`, `SESSION_CLOSED`, `SESSION_ORPHAN_HELD`.

O texto mistura as duas colunas e não restringe explicitamente `execution_domain`.

**Correção precisa:**

```sql
CREATE UNIQUE INDEX ... ON forge.task
  (organization_id, project_id, session_id)
WHERE execution_domain = 'CONVERSATION'
  AND session_status IN ('OPEN', 'CLOSING', 'ORPHAN_HELD');
```

O pacote deve escolher explicitamente `session_status`, ou usar os valores prefixados se a intenção for `task.status`, sem misturá-los.

### 4.9 LOW-01 — OPEN BLOCKING DoR

A v0.4 age corretamente ao não inventar pessoas ou effort: [CMP-FD-07:7-23](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-07-ORACLES.md:7).

As sete histórias permanecem:

- pessoa `PENDING`;
- effort `UNSTATED`;
- DoR `NOT MET`.

**Correção precisa:** ato humano do Founder nomeando responsáveis, registro de effort pelas pessoas responsáveis e reavaliação expressa do checklist DoR. Papel abstrato não satisfaz owner.

## 5. Cenários adversariais e invariantes

### Race e movimento único

A ordem Build → Task → Operation → Reservation preserva o Build como primeiro lock. O pacote proíbe segundo movimento, segunda reservation e provider dentro da transação.

Entretanto, deve ser acrescentada a race `AmendSessionSlice` versus `ApplyAuthorizedReconciliation`. Sem isso, o caminho de reconciliação manual permanece fora da prova de serialização da fatia.

### Prova tardia

A regra de não criar segundo movimento está preservada em [CMP-FD-01:85-87](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/conversational-full-duplex-v0.4/CMP-FD-01-LEDGER-SETTLEMENT-TENANT-CAS.md:85) e na baseline [FDP-16A:405-413](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v04-codex-independent/docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md:405).

A fatia não é reescrita por prova tardia. Spent/reserved e o movement existente permanecem intactos. Não identifiquei autorização de refund inventado.

### Session close

Sessões com Operation `DISPATCHED`, `RECONCILING`, `BLOCKED_RECONCILIATION` ou pending incompatível não fecham. Permanecem `CLOSING` ou `ORPHAN_HELD`, e a fatia continua na soma.

A regra é adequada, salvo pela terminologia inconsistente na migration e pela ausência de tratamento explícito do pending histórico após settlement autorizado.

### Zero ledger duplicado

A v0.4 preserva:

- um movimento no sucesso;
- zero movimento nos caminhos `OVER_ESTIMATE` e `SESSION_SLICE`;
- pending único por `(operation_id, proof_id)`;
- `40001` abortando toda a transação;
- replay sem segundo movimento.

Nenhum segundo ledger ou moeda nova foi introduzido.

### No silent downgrade

`HELLO_ACK_ERROR` tem zero efeito e não cria modo half-duplex. `FALLBACK_TEXT` conserva `voice_required=true`. O requisito Founder AQ-07 permanece normativo.

### No provider real

A pasta declara que nenhum provider foi chamado, e nenhum elemento observado constitui binding de fornecedor. `LOCAL_PIPELINE` e `PROVIDER_DUPLEX` usam o mesmo contrato e não elegem provider. Isso é compatível com FDP-15 e com AQ-04 ainda DEFERRED.

## 6. Governança

As decisões humanas foram preservadas corretamente:

- **APPROVED:** AQ-01, AQ-02, AQ-03, AQ-05, AQ-06, AQ-07, AQ-08, AQ-10 e AQ-11.
- **DEFERRED/UNDECIDED:** AQ-04, AQ-09 e AQ-12.

Não identifiquei:

- escolha implícita de provider;
- Founder OS implícito;
- recibo fictício;
- quarta família de adapter;
- transformação de Codex read-only em aprovador;
- integração automática na baseline;
- autorização de BUILD-00.

FDP-15 continua histórico e pendente de ato expresso do Founder. As capabilities speech permanecem na família TOOL, sem quarta família.

## 7. Estado dos oráculos

Nesta auditoria:

- 91 oráculos v1.7: **NOT RUN**;
- 36 CMP-O: **NOT RUN**;
- CMP-O-28: **NOT RUN**;
- CMP-FD-O01..O40: **NOT RUN**;
- CMP-FD-O41..O52: **NOT RUN**;
- subcasos O37-S/B/T/O/R/X: **NOT RUN**;
- verifier de digest: **NOT RUN**;
- testes de produto: **NOT RUN**;
- BUILD-00: **não iniciado**.

Nenhuma saída declarada pelo autor foi promovida a evidência independente.

## 8. Gates obrigatórios

Enquanto os defects acima não forem corrigidos:

1. não integrar `forge.conversation.delta.v3`;
2. manter a flag desligada;
3. não promover `cmp.media.duplex.v1` a contrato aprovado;
4. não incorporar v0.4 à baseline;
5. não aprovar FDP-14 ou FDP-15 por inferência;
6. não autorizar BUILD-00;
7. não executar migration;
8. não chamar provider real;
9. não marcar histórias como Ready;
10. produzir v0.5 aditiva ou correção equivalente e submetê-la a novo SHA imutável e auditoria read-only.

Para sair de FAIL documental, no mínimo:

- estender a checagem da fatia a `ApplyAuthorizedReconciliation`;
- fechar backfill/constraints da cadeia tenant;
- tornar ACK cross-stream inequivocamente representável;
- corrigir autenticação do preâmbulo;
- fortalecer o verifier para bijeção e duplicatas;
- corrigir a amostra AEC de saturação;
- tornar o índice parcial de sessão executável e coerente;
- resolver LOW-01 por ato humano.

**Veredito final: FAIL DOCUMENT-ONLY.** A v0.4 corrige boa parte dos defects da v0.3 e preserva os findings anteriormente CLOSED, mas ainda deixa um bypass financeiro de alta severidade no settlement manual, além de lacunas normativas em tenant migration, ACK, fixture AEC, verifier e unicidade de sessão. Não há base para PASS, integração ou BUILD-00.