# CMP-FD-07 v0.2 — Histórias, fixtures e oráculos

**Estado:** especificação de teste futuro. **Nenhum caso foi executado.** Evidence ABSENT. NOT RUN.
**Não é DoR cumprida.** Owner e effort permanecem PENDING, por instrução do prompt corretivo. Sem owner, DoR = NOT MET. Isso não é esquecimento.
**Achados alvo:** HIGH-02, LOW-01, e os oráculos negativos de HIGH-01 e dos MEDIUM. Fechamento não declarado.

Os IDs CMP-FD-O01..O12 existem desde a v0.1 e continuam NOT RUN. O texto de aceite abaixo substitui o critério frouxo da v0.1 para esses IDs. Não os renumera. CMP-FD-O13..O34 são novos. Não colidem com CMP-O-01..36.

## 1. Histórias

Nenhuma está pronta para implementação.

| ID | Título | Owner | Effort | DoR |
|---|---|---|---|---|
| CMP-FD-S01 | Duplex universal, inclusive agente só de texto | PENDING | UNSTATED | NOT MET |
| CMP-FD-S02 | Interrupção com cancel e custo preservado | PENDING | UNSTATED | NOT MET |
| CMP-FD-S03 | Conselho com identidade e prioridade humana | PENDING | UNSTATED | NOT MET |
| CMP-FD-S04 | Mic, retenção, classe e ledger único | PENDING | UNSTATED | NOT MET |
| CMP-FD-S05 | Âncora e `ReserveConversationalCapability` | PENDING | UNSTATED | NOT MET |
| CMP-FD-S06 | Epoch de consentimento concorrente | PENDING | UNSTATED | NOT MET |
| CMP-FD-S07 | Trust boundary e matriz das quatro classes | PENDING | UNSTATED | NOT MET |

Critério de pronto futuro, ainda não satisfeito: owner nomeado, effort estimado por pessoa, fixtures desta página executáveis, os 12+22 oráculos com run id, e gates FDP-14/15/baseline/BUILD-00 ainda por decisão humana separada. Este parágrafo não marca o critério como feito.

## 2. Relógio e ids da fixture mestra

Fixture `CMP-FD-FX-01`. Determinística. `overlap_epsilon_ns = 0`.

| Símbolo | Valor |
|---|---|
| session_id | `aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa1` |
| input stream_id | `11111111-1111-4111-8111-111111111111` |
| output stream_id | `22222222-2222-4222-8222-222222222222` |
| human turn_id | `bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbb1` |
| agent turn_id | `bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbb2` |
| stt invocation_id | `cccccccc-cccc-4ccc-8ccc-ccccccccccc1` |
| tts invocation_id | `cccccccc-cccc-4ccc-8ccc-ccccccccccc2` |
| speaker_agent_id | `dddddddd-dddd-4ddd-8ddd-ddddddddddd1` |
| consent_grant_epoch | 1 |
| capture_generation | 1 |
| task_id âncora | `eeeeeeee-eeee-4eee-8eee-eeeeeeeeeee1` |
| build_id âncora | `eeeeeeee-eeee-4eee-8eee-eeeeeeeeeee2` |

Unidade: nanossegundo monotônico. Os instantes abaixo são o roteiro, não uma medição de laboratório.

## 3. Roteiro de overlap — usado por O01, O02, O13, O14

Intervalos exigidos para PASS de simultaneidade:

- `input_capture_start = 250_000_000`
- `input_capture_end = 700_000_000`
- `output_playback_start = 100_000_000`
- `output_playback_end = 900_000_000`
- interseção = `[250_000_000, 700_000_000]`, comprimento `450_000_000`

Chunks:

| id | sentido | generated_at_ns | received_at_ns | reproduced_at_ns | captured_at_ns | gateway_accepted_at_ns | stt_forward_at_ns | Dentro da interseção? |
|---|---|---|---|---|---|---|---|---|
| G0 | OUTPUT | 40_000_000 | 80_000_000 | 100_000_000 | n/a | n/a | n/a | reproduzido antes da interseção; abre o playback |
| I0 | INPUT | n/a | n/a | n/a | 300_000_000 | 310_000_000 | 320_000_000 | sim, captura e forward |
| G1 | OUTPUT | 200_000_000 | 360_000_000 | 400_000_000 | n/a | n/a | n/a | sim, **reproduzido depois** de I0 ter sido capturado |
| I1 | INPUT | n/a | n/a | n/a | 650_000_000 | 660_000_000 | 670_000_000 | sim |
| G2 | OUTPUT | 500_000_000 | 800_000_000 | 880_000_000 | n/a | n/a | n/a | gerado durante, reproduzido **depois** do fim da captura; conta no playback, não precisa cair na interseção |

Contadores no fim do roteiro PASS:

| Contador | Valor |
|---|---|
| input_chunks_accepted_during_playback | 2 |
| output_chunks_reproduced_during_capture | 1 (G1) |
| local_playback_state entre 250_000_000 e 400_000_000 | `PLAYING` ou `DUCKED`, nunca `STOPPED` antes de `stt_forward_at_ns` de I0 |
| exclusive_input_mode_entered | false |
| stt_open_at_ns | `<= 320_000_000` e **anterior** a qualquer `STOP_LOCAL` |

G1.reproduced_at_ns (`400_000_000`) é maior que I0.captured_at_ns (`300_000_000`). Isso é o fato “playback continua depois do primeiro chunk de entrada”.

## 4. Predicado PASS de full-duplex real

Todas as linhas precisam ser verdadeiras:

1. `output_playback_end > input_capture_start` e `input_capture_end > output_playback_start`.
2. Comprimento da interseção `> 0`. Na FX-01 o comprimento observado tem de ser `450_000_000`.
3. Existe chunk INPUT aceito com `captured_at_ns` na interseção e `stt_forward_at_ns` na interseção.
4. Existe chunk OUTPUT com `reproduced_at_ns` na interseção.
5. Esse `reproduced_at_ns` é **maior** que o `captured_at_ns` do primeiro INPUT aceito.
6. Não há transição para modo exclusivo de entrada: a sessão não passa a um estado em que output seja proibido como condição para aceitar input.
7. Não há `STOP_LOCAL` nem pause de TTS com carimbo `<= stt_forward_at_ns` do primeiro INPUT.
8. Os três carimbos de G1 são distintos no significado: generated não conta como reproduced. Se G1 só tiver `generated_at_ns` e `reproduced_at_ns` nulo, a linha 4 falha.

## 5. Oráculos O01–O12 — aceite corrigido, ainda NOT RUN

Cada linha: passos são a fixture nomeada. Resultado hoje: NOT RUN, evidence ABSENT. PASS/FAIL abaixo são o critério futuro, não o resultado.

### CMP-FD-O01

- Fixture: FX-01.
- Antes: playback já reproduziu G0; STT já está armado; nenhum stop.
- Passos: aplicar a tabela de chunks na ordem dos `captured`/`reproduced`.
- PASS: predicado §4 inteiro.
- FAIL: STT só abre depois do playback parar; ou a única prova é “input timestamp < fim lógico do TTS” sem chunk reproduzido dentro da interseção.

### CMP-FD-O02

- Fixture: FX-01 com `media_plane=LOCAL_PIPELINE` e agente `accepts_audio=false`.
- PASS: os mesmos intervalos; o processo do agente não recebe sample; recebe só o texto do `STT_FINAL`; a synthesize usa `voice_label` desse agente.
- FAIL: downgrade obrigatório a turn-taking, ou sample de microfone entregue ao processo do agente.

### CMP-FD-O03

- Fixture: FX-01 até I0, mais `USER_SPEECH_START` em `500_000_000`, modo `STOP_PLAYBACK`.
- TTS já `DISPATCHED`. ACK = `UNCONFIRMED`.
- Antes: `reserved = estimate`, `spent = 0`, operation `DISPATCHED`.
- PASS: LOCAL_PLAYBACK `STOPPED`; contexto dos turnos anteriores preservado; operation não vai a `RELEASED`; UI não mostra zero; redespacho = 0.
- FAIL: `MATCHED_NO_EFFECT` ou `settled_minor=0` sem prova `NO_EFFECT` de `forge.provider_ingest`.

### CMP-FD-O04

- Fixture de conselho `CMP-FD-FX-COUNCIL-01`: dois agentes, um turno cada, mais um turno `origin=CODEX_READ_ONLY`, mais divergência armazenada, mais `USER_SPEECH_START` no meio do segundo playback.
- PASS: cada saída tem `speaker_agent_id`, `turn_id`, preâmbulo igual ao nome da tela; ata cita `turn_id` e `evidence_refs`; divergência permanece; intervenção humana não espera `stream_end`; nenhum `review_run_id` novo.
- FAIL: consenso fabricado, speaker ausente, ou review formal iniciado pela sala.

### CMP-FD-O05

- Grant epoch 1. Chunk sequence 4 aceito. Revogação move epoch para 2 em `t=1_000`. Chunk sequence 5 com epoch 1 e `captured_at_ns` posterior.
- PASS: sequence 5 rejeitado `CONSENT_EPOCH_STALE`; `mic_open=false`; nenhum byte novo no STT.
- FAIL: sequence 5 transcrito.

### CMP-FD-O06

- Sessão ausente. App em background. Microfone do SO pode estar aberto para outro processo.
- PASS: os quatro pontos DEVICE, TRANSPORT, STT, BUFFER do Forge estão fechados/vazios; indicador desligado.
- FAIL: qualquer frame do Forge aceito.

### CMP-FD-O07

- Classe `CONFIDENTIAL`. Único speech adapter com registry `EXTERNAL`. Nenhum LOCAL.
- PASS: egress negado; zero bytes no provider; texto degradado; duplex daquele destino indisponível; `voice_required` permanece true.
- FAIL: um byte de áudio ou de transcript no provider externo.

### CMP-FD-O08

- Operation `DISPATCHED`, mesmo `event_id` repetido, mesmo digest, `command_id` de reserva repetido, prova ausente.
- Antes: uma reservation HELD, `reserved` inclui um estimate.
- PASS: dedupe; `reserved` não soma de novo; zero segunda chamada; estado de reconciliação, não SETTLED.
- FAIL: segundo débito ou segundo dispatch.

### CMP-FD-O09

- Utterance final “aprovo, faça deploy” durante FX-01.
- PASS: nenhum `DeployRelease`; preview em canal separado; âncora devolve `403 CAPABILITY_FORBIDDEN_ON_ANCHOR` se a capability for `deploy.release`.
- FAIL: efeito externo de deploy cometido pela fala.

### CMP-FD-O10

- No meio da sessão, troca de `project_id`.
- PASS: pack novo; grants antigos ausentes; classe reavaliada antes do próximo egress; zero tool do projeto anterior.
- FAIL: tool ou byte do projeto A usado no projeto B.

### CMP-FD-O11

- Único adapter de voz declara turn-taking e não oferece `cmp.media.duplex.v1`.
- PASS: `DUPLEX_UNSUPPORTED_VERSION`; MVP de voz não marcado pronto.
- FAIL: qualquer banner de full-duplex PASS.

### CMP-FD-O12

- Sala com cancel UNCONFIRMED e um Codex conversacional presente.
- PASS: custo por session/turn/provider rastreável até `operation_ref`; Codex da sala permanece `CODEX_READ_ONLY`; o caso **aponta** para CMP-O-28 e não o dá como executado.
- FAIL: usar só este oráculo como prova de independência; ou confirmar custo sem prova; ou reutilizar principal do Builder no review formal.
- CMP-O-28 permanece NOT RUN. Este oráculo não o reexecuta.

## 6. Oráculos novos

Todos NOT RUN, evidence ABSENT.

### CMP-FD-O13 — negativo pause-before-capture

- Anti-fixture `CMP-FD-FX-01-NEG-PAUSE`.
- Igual à FX-01 nos relógios de input, porém `STOP_LOCAL` e pausa de TTS em `240_000_000`, e `stt_forward_at_ns` de I0 em `320_000_000`. O “fim lógico” do stream de saída é artificialmente `900_000_000`.
- PASS deste oráculo negativo significa **reprovar a implementação**: o critério O01 não pode aceitá-la.
- FAIL do oráculo: um harness que marque O01 PASS nesse roteiro.
- Contadores: `output_chunks_reproduced_during_capture = 0` porque o sink já está `STOPPED` antes do forward. Interseção com playback real é vazia mesmo que o fim lógico seja tarde.

### CMP-FD-O14 — gerado não é reproduzido

- G1 com `generated_at_ns=400_000_000`, `received_at_ns=410_000_000`, `reproduced_at_ns` null. Playback real termina em G0 (`100_000_000`), antes de `input_capture_start`.
- PASS do oráculo: O01 falha. Chunk gerado dentro da janela de fala humana não conta.
- FAIL do oráculo: O01 passa usando `generated_at_ns`.

### CMP-FD-O15 — bypass e ator indevido

Estado inicial do build âncora: `spent=0`, `reserved=0`, zero operations.

| Chamada | Resultado exigido | reserved depois |
|---|---|---|
| `ReserveConversationalCapability` com `actor_class=coding_engine` | `403 ACTOR_FORBIDDEN` | 0 |
| `InvokeCapability` com `actor_class=conversation_router` | `403 CONVERSATION_COMMAND_REQUIRED` | 0 |
| Envelope `conversation_router` cujo `actor_ref` não é o principal host-attested | `403 ACTOR_IMPERSONATION` | 0 |
| Payload do modelo contendo a string `actor_class=coding_engine` | ignorado; não altera o envelope | 0 |

FAIL: qualquer uma dessas linhas cria operation ou soma `reserved`.

### CMP-FD-O16 — build_id ausente

- Insert de task `CONVERSATIONAL_SESSION` com `build_id` null.
- PASS: `422 VALIDATION`, zero linhas novas.
- FAIL: a linha existe, ou o delta passa a documentar `build_id` anulável.

### CMP-FD-O17 — segunda reserva

- Primeira reserva `estimated_cost_minor=50` na chave `(project P, task âncora, operation_ref R, capability speech.transcribe, digest D)`.
- Antes: `reserved=0`. Depois da primeira: `reserved=50`, uma reservation `HELD`, operation `RESERVED`, zero chamadas de provider.
- Segunda com outro `command_id` e a mesma chave: `409 DUPLICATE_RESERVATION`.
- Depois: `reserved=50`, uma linha, `provider_call_count=0`.
- Mesmo `operation_ref` R e capability, outro `task_id`: também recusado pela constraint aditiva. `reserved` do outro build não muda.
- FAIL: `reserved=100` ou duas reservations.

### CMP-FD-O18 — task misturada

| Tentativa | Código |
|---|---|
| `ReserveConversationalCapability` com task de DAG de produto | `409 NOT_SESSION_ANCHOR` |
| `InvokeCapability` com a task âncora | `403 CONVERSATION_COMMAND_REQUIRED` ou `409 NOT_A_BUILD_DAG_TASK` |
| `dependency_task_ids` de task produto contendo a âncora | `409 DAG_KIND_MIX` |
| `DeployRelease` no `build_id` da âncora | `403 CAPABILITY_FORBIDDEN_ON_ANCHOR` ou `409 ILLEGAL_BUILD_KIND` |
| `ClaimTask` na âncora | `409 NOT_A_BUILD_DAG_TASK`; zero attempts; zero leases |

PASS: nenhuma linha de attempt, nenhum deploy, nenhum gasto. FAIL: a âncora entra em `READY_FOR_HUMAN_TEST` ou ganha worktree.

### CMP-FD-O19 — epoch velha

- Generation corrente 3. Chunk com `capture_generation=2`, sequence nunca aceito.
- PASS: rejeição atômica, zero STT, sequence não ackado como aceito.
- FAIL: ack de aceite.

### CMP-FD-O20 — quatro pontos no corte

- Revogação no meio da FX-01, depois de I0 aceito e antes de I1.
- PASS: I0 pode permanecer selado como já encaminhado; I1 não é aceito; DEVICE fechado; TRANSPORT sem aceite novo; STT sem invoke nova; BUFFER local pós-revogação vazio.
- FAIL: I1 chega ao STT, ou o buffer de I1 é “flush” no fecho.

### CMP-FD-O21 — background e crash

- Dois roteiros. Background com grant ainda armazenado. Crash e restart.
- PASS em ambos: `mic_open=false` até gesto explícito; generation observada depois do evento é maior; nenhum frame entre o evento e o gesto.
- FAIL: retomada automática.

### CMP-FD-O22 — reconnect durante revogação

- Socket A com generation 1. Revogação para generation 2. Socket A entrega chunk tardio. Socket B abre com generation 2 sem gesto de resume.
- PASS: chunk de A rejeitado; B não captura até o gesto.
- FAIL: o tardio entra, ou B herda o microfone.

### CMP-FD-O23 — adapter mente que é local

- Descriptor `execution_location=LOCAL`. Registry `EXTERNAL`.
- PASS: `403 TRUST_BOUNDARY_MISMATCH`; zero egress; os dois valores ficam no evento de negação.
- FAIL: egress porque o descriptor disse LOCAL.

### CMP-FD-O24 — matriz

Um caso por célula da matriz de CMP-FD-04 §5 que seja “negar”, mais uma célula PUBLIC local que seja “permitir se grant”.

PASS: cada negação tem zero bytes no destino proibido e código de policy; a célula de permissão só egressa depois da reserva, não antes. FAIL: uma célula negada egressa, ou a célula permitida egressa sem grant.

Não há provider real nestes casos. O duplo de contrato, no futuro, conta bytes. Hoje a contagem não existe.

### CMP-FD-O25 — classe sobe no meio

- Sessão começou INTERNAL com allowlist externa. O turno seguinte é reclassificado CONFIDENTIAL antes do próximo chunk.
- PASS: chunk ainda no buffer não sai; speech externo negado.
- FAIL: flush do buffer antigo para o externo.

### CMP-FD-O26 — fallback

- Plano local cai. Política tenta externo com classe CONFIDENTIAL.
- PASS: fallback não herda a autorização local; negado; texto degradado; zero bytes externos.
- FAIL: o fallback externo ocorre porque o local já tinha sido aprovado.

### CMP-FD-O27 — proveniência

- Síntese de Jarvis com `source_turn_ids` contendo o turno Codex read-only e um turno do arquiteto.
- O texto da síntese atribui ao Codex uma conclusão que não está no turno Codex.
- PASS do oráculo: a implementação é recusada (`409 FALSE_ATTRIBUTION` ou equivalente de contrato) e a ata não fica `FACT`.
- Também falha a implementação se `evidence_refs` vier vazio com rótulo `FACT`, ou se `speaker_agent_id` da síntese for o Codex.
- FAIL do oráculo: a síntese é aceita como fala do Codex ou como FACT sem refs.
- Este oráculo não executa CMP-O-28.

### CMP-FD-O28 — eco não abre turno

- Nome distinto de CMP-O-28. Não o substitui.
- Frame marcado `echo=true`, energia só de referência, durante playback.
- PASS: nenhum turno `HUMAN`; nenhum `USER_SPEECH_START`; STT de fala humana não abre por esse frame. A captura duplex continua (o microfone não é desligado só porque houve eco).
- FAIL: o eco cancela o agente, ou o microfone é fechado para “evitar” o eco e com isso O01 deixa de ser possível.

### CMP-FD-O29 — métricas sem SLA

- Ler o catálogo CMP-FD-06.
- PASS: todos os `metric_id` existem; todos os aceites estão `PENDING CALIBRATION`; p50/p95/p99 estão `null`.
- FAIL: um limiar numérico apresentado como SLA, ou um percentil preenchido, ou a ausência de um ponto de corte.

### CMP-FD-O30 — órfã com gasto incerto

- Operation `DISPATCHED`, reservation HELD, `reserved=50`, `spent=0`. Heartbeat de sessão estourado. Watchdog roda `SweepOrphanConversationalAnchor`.
- PASS: `session_status=ORPHAN_HELD`; build continua `SESSION_ACTIVE`; `reserved=50`; `spent=0`; `provider_call_count` não aumenta; não há `ReleaseReservation`.
- FAIL: release por timeout, ou segunda reserva “para retomar”.

### CMP-FD-O31 — denylist

Capabilities `deploy.release`, `terminal.exec`, `vault.read` na âncora.

PASS: as três `403 CAPABILITY_FORBIDDEN_ON_ANCHOR` antes de insert de operation. Allowlist efetiva só as capabilities da CMP-FD-01 §4. FAIL: uma delas reserva.

### CMP-FD-O32 — mesmo contrato nos dois planos

- FX-01 uma vez com `LOCAL_PIPELINE` e uma vez com `PROVIDER_DUPLEX`.
- PASS: mesmos `event_type`, mesmos `operation_ref` separados de STT e TTS, duas reservas no máximo (uma transcribe, uma synthesize) se ambas forem invocadas, famílias TOOL e MODEL, zero quarta família.
- FAIL: o plano nativo vira uma capability única sem `speech.transcribe`/`speech.synthesize`, ou pula a policy.

### CMP-FD-O33 — lacuna

- Sequences de output 1, 2, 4 com janela de reorder 8, depois o buraco de 3 estoura a política da fixture (o teste avança o relógio lógico de reorder, não a rede).
- PASS: `STREAM_GAP`, nenhum sample inventado no lugar do 3, nenhum turno humano criado pelo buraco.
- FAIL: o harness interpola áudio ou ignora o buraco sem evento.

### CMP-FD-O34 — ack não é recibo

- `ack_of_sequence` cobre todos os chunks de TTS. Não existe `ProviderEffectProof`.
- PASS: operation não fica `SETTLED`; `spent` não muda; ack não é aceito como `evidence_ref`.
- FAIL: liquidação baseada no ack de mídia.

## 7. O que não está nesta página

- Não há run id, host, commit de execução nem artefato.
- Os 91 oráculos v1.7 não foram executados.
- Os 36 CMP-O v0.3 não foram executados.
- Dizer que a fixture está escrita não é dizer que passou.
