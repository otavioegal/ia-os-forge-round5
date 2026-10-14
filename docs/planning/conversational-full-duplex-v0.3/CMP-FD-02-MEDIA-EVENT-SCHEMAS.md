# CMP-FD-02 v0.3 — Schemas discriminados `cmp.media.duplex.v1`

**Estado:** PROPOSTA. Não implementada. Não substitui `cmp.speech.v0`.
**Achados alvo:** HIGH-02, HIGH-03, NEW-MEDIUM-02. Fechamento não declarado.
**Campo desconhecido:** `422 UNKNOWN_FIELD`. O evento é descartado. Não há coerce. Por isso os timestamps do overlap estão nesta especificação, não só em prosa.

Meio-duplex não satisfaz AQ-07. Nenhum fornecedor é escolhido.

## 1. Dois schemas, um contrato

| Schema id | Quando é legal |
|---|---|
| `cmp.media.duplex.v1.preamble` | só `HELLO` e `HELLO_ACK`, antes de existir sessão de mídia |
| `cmp.media.duplex.v1` | todo evento depois que `HELLO_ACK` comprometeu o trio de streams |

`HELLO` não usa o envelope da seção 3. A frase da v0.2 que aplicava esse envelope “depois do handshake” deixa de esconder o preâmbulo: o preâmbulo tem schema próprio.

## 2. Preâmbulo

### HELLO

| Campo | Tipo | Null | Regra |
|---|---|---|---|
| schema_id | string | no | `cmp.media.duplex.v1.preamble` |
| event_type | string | no | `HELLO` |
| event_id | uuid | no | |
| event_digest | sha256 | no | seção 8, calculado sem este campo |
| channel_id | uuid | no | canal já autenticado |
| organization_id | uuid | no | igual ao canal. Senão `422 CHANNEL_SCOPE` |
| project_id | uuid | no | igual ao canal |
| principal_ref | string | no | principal do canal, não do modelo |
| contract_versions_offered | string[] | no | contém `cmp.media.duplex.v1` e `cmp.speech.v0` |
| media_plane_offered | enum[] | no | subconjunto de `LOCAL_PIPELINE`, `PROVIDER_DUPLEX` |
| encodings_offered | enum[] | no | subconjunto de `PCM_S16LE`, `OPUS`, `FLAC` |

Sem áudio, sem `operation_ref`, sem reserva, sem microfone aberto. O mesmo algoritmo de digest da seção 8 vale para o objeto de preâmbulo, que não tem o campo no momento do cálculo. `event_digest` é obrigatório também em `HELLO` e `HELLO_ACK`. Mesmo `event_id` com digest diferente: `409 EVENT_ID_REUSED`, sem criar sessão.

### HELLO_ACK

| Campo | Tipo | Null | Regra |
|---|---|---|---|
| schema_id | string | no | `cmp.media.duplex.v1.preamble` |
| event_type | string | no | `HELLO_ACK` |
| event_id | uuid | no | |
| event_digest | sha256 | no | seção 8 |
| in_reply_to | uuid | no | `event_id` do HELLO |
| selected_media_contract | string | no | `cmp.media.duplex.v1` ou erro |
| selected_speech_contract | string | no | `cmp.speech.v0` ou erro |
| selected_media_plane | enum | no | interseção entre oferta, `describe` e registry |
| selected_encoding | enum | no | interseção |
| input_stream_id | uuid | no | distinto dos outros dois |
| output_stream_id | uuid | no | |
| control_stream_id | uuid | no | todo `direction=CONTROL` usa este id |

Falha de versão: `DUPLEX_UNSUPPORTED_VERSION` ou `SPEECH_UNSUPPORTED_VERSION`, terminal, não retryable. Sem downgrade para turn-taking. Texto pode continuar com `voice_required=true`. Isso não marca o MVP de voz como pronto.

## 3. Envelope comum depois do handshake

Aplicável a todo `event_type` da seção 5. A união é fechada: `event_type` fora da lista é `422 UNKNOWN_FIELD`.

| Campo | Tipo | Null | Regra |
|---|---|---|---|
| schema_id | string | no | `cmp.media.duplex.v1` |
| contract_version | string | no | `cmp.media.duplex.v1` |
| event_type | enum | no | seção 5 |
| event_id | uuid | no | |
| event_digest | sha256 | no | seção 8. O gateway recalcula. Divergência do valor enviado: `422 DIGEST_MISMATCH` |
| organization_id | uuid | no | igual ao canal e à sessão |
| project_id | uuid | no | igual ao canal e à sessão |
| session_id | uuid | no | |
| stream_id | uuid | no | seção 4 |
| sequence | int64 | no | `>= 1`, monotônico estrito em `sequence_scope` |
| sequence_scope | string | no | `{session_id}/{stream_id}` |
| direction | enum | no | `INPUT`, `OUTPUT`, `CONTROL` |
| ack_of_sequence | int64 | yes | ack cumulativo desse escopo. Não é recibo financeiro |
| gap_policy | enum | no | literal `REJECT_GAP` |
| participant_id | uuid | no | |
| turn_id | uuid | yes | null só em `START_SESSION`. Obrigatório nos demais |
| invocation_id | uuid | yes | obrigatório quando a seção 6 diz |
| speaker_agent_id | uuid | yes | obrigatório sse saída de fala de agente |
| origin | enum | no | `HUMAN`, `AGENT`, `SYSTEM`, `CODEX_READ_ONLY` |
| source_turn_ids | uuid[] | no | vazio no input humano; não vazio na síntese Jarvis |
| evidence_refs | uuid[] | no | vazio só se o rótulo não é `FACT` |
| epistemic_label | enum | yes | obrigatório em saída textual de agente |
| media_plane | enum | no | o valor selecionado no HELLO_ACK |
| consent_ref | uuid | yes | obrigatório quando `capture_generation > 0` |
| consent_grant_epoch | int64 | no | |
| capture_generation | int64 | no | |
| data_classification | enum | no | `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED` |
| execution_location | enum | yes | obrigatório se o evento pode egressar |
| trust_boundary | enum | yes | obrigatório no mesmo caso |
| operation_ref | string | yes | obrigatório se há invocation com efeito monetário possível |
| is_final | bool | no | |
| stream_end | bool | no | |
| discontinuity | bool | no | default de contrato `false`. `true` só no chunk seguinte a `STREAM_GAP` |
| payload | object | no | exatamente o objeto da seção 6 para aquele `event_type`. Campo a mais dentro dele é `422 UNKNOWN_FIELD` |
| observation | object | no | seção 7. Sempre presente. Não é campo opcional “em algum lugar da prosa” |

## 4. Três streams

`HELLO_ACK` fixa três UUID distintos.

| direction | stream_id obrigatório | sequence_scope |
|---|---|---|
| INPUT | `input_stream_id` | `{session_id}/{input_stream_id}` |
| OUTPUT | `output_stream_id` | `{session_id}/{output_stream_id}` |
| CONTROL | `control_stream_id` | `{session_id}/{control_stream_id}` |

`STREAM_DIRECTION_MISMATCH` se a direction não usa o stream correspondente. Sequências não se emprestam entre streams. Ack, replay e dedupe são por `event_id` na sessão e, para ordem, por `sequence_scope`. `CONTROL` tem os mesmos ack, janela e `REJECT_GAP` da seção 9.

## 5. União fechada de event_type

| event_type | direction |
|---|---|
| START_SESSION | CONTROL |
| INPUT_AUDIO_CHUNK | INPUT |
| STT_PARTIAL | CONTROL |
| STT_FINAL | CONTROL |
| USER_SPEECH_START | CONTROL |
| OUTPUT_AUDIO_CHUNK | OUTPUT |
| PLAYBACK_SPAN | OUTPUT |
| CANCEL_ACK | CONTROL |
| PAUSE_SESSION | CONTROL |
| STOP_SESSION | CONTROL |
| CONSENT_REVOKED | CONTROL |
| CAPTURE_CLOSED | CONTROL |
| ERROR | CONTROL |
| STREAM_GAP | CONTROL |
| FALLBACK_TEXT | CONTROL |

Estados de sessão, inalterados em relação à v0.2 e repetidos para o pacote ser autossuficiente: `CLOSED`, `HANDSHAKE`, `ACTIVE_DUPLEX`, `INTERRUPTING`, `PAUSED`, `STOPPING`, `REVOKED`, `FAILED`. Não existe estado `HALF_DUPLEX` nem `TURN_TAKING`. `ACTIVE_DUPLEX` é o único em que captura e playback podem estar abertos juntos. `USER_SPEECH_START` não espera o fim do TTS para o STT já estar aceitando.

## 6. Payloads

### START_SESSION

`granted` bool não nulo. Sem bytes. `turn_id` do envelope null. `invocation_id` null.

### INPUT_AUDIO_CHUNK e OUTPUT_AUDIO_CHUNK

| Campo | Tipo | Null | Regra |
|---|---|---|---|
| media_encoding | enum | no | `PCM_S16LE`, `OPUS`, `FLAC` |
| audio_mime | string | no | `audio/wav`, `audio/ogg` ou `audio/flac`, casado com o encoding. Senão `SPEECH_BAD_AUDIO` |
| sample_rate_hz | int | yes | obrigatório sse `PCM_S16LE`; `> 0` |
| channels | int | no | `1` |
| duration_ns | int64 | no | `> 0` |
| payload_mode | enum | no | `INLINE_BYTES` ou `CONTENT_REF` |
| payload_bytes | bytes | yes | obrigatório sse inline. Proibido no audit |
| content_ref | string | yes | obrigatório sse ref. Efêmero. Não é arquivo durável |
| content_sha256 | sha256 | no | hash dos bytes |
| content_size_bytes | int64 | no | `> 0` e igual ao tamanho hasheado |

`OUTPUT_AUDIO_CHUNK.invocation_id` obrigatório. `INPUT_AUDIO_CHUNK.invocation_id` obrigatório quando o chunk foi encaminhado ao STT; null se ainda só capturado e não encaminhado. A fixture de overlap usa chunks já encaminhados, então `invocation_id` vem preenchido.

### STT_PARTIAL e STT_FINAL

| Campo | Tipo | Null | Regra |
|---|---|---|---|
| transcript_state | enum | no | `PARTIAL` no primeiro, `FINAL` no segundo. Outro valor é `422` |
| transcript_text | string | no | não vai para o audit em claro se a política de retenção não permitir; a fixture de teste pode carregá-lo em memória |
| language_detected | string | yes | BCP-47 |
| provider_id | string | no | id do descriptor, não escolha de fornecedor |
| model_id | string | yes | null se o adapter não tem dimensão de modelo |

Envelope: `is_final=true` sse `transcript_state=FINAL`. `invocation_id` e `operation_ref` obrigatórios. Segundo `STT_FINAL` no mesmo `invocation_id`: erro de contrato, sem segunda execution. `STT_PARTIAL` não chama tool nem `conversation.respond`.

### USER_SPEECH_START

`target_invocation_id` uuid não nulo: a invoke de TTS a cancelar. `interrupt_mode` enum não nulo: `STOP_PLAYBACK` ou `DUCK`. Não carrega `cancel_state`; quem carrega é `CANCEL_ACK`.

### PLAYBACK_SPAN

| Campo | Tipo | Null | Regra |
|---|---|---|---|
| span_role | enum | no | `START`, `CHUNK` ou `END` |
| playback_state | enum | no | `PLAYING`, `DUCKED` ou `STOPPED` |
| content_sha256 | sha256 | yes | obrigatório sse `span_role=CHUNK`; igual ao chunk de saída correlato |
| source_sequence | int64 | yes | obrigatório sse `CHUNK`; sequence do `OUTPUT_AUDIO_CHUNK` |

`invocation_id` do envelope obrigatório. O predicado de overlap lê `observation.reproduced_at_ns` **deste** evento, não um campo reescrito no chunk já emitido. Chunk de saída é imutável.

### CANCEL_ACK

| Campo | Tipo | Null | Regra |
|---|---|---|---|
| cancel_state | enum | no | `CONFIRMED` ou `UNCONFIRMED` |
| speech_error_code | enum | no | `SPEECH_CANCELLED` sse `CONFIRMED`; `SPEECH_CANCEL_UNCONFIRMED` sse `UNCONFIRMED` |

`invocation_id` obrigatório. Não liquida e não inventa `NO_EFFECT`.

### PAUSE_SESSION, STOP_SESSION, CONSENT_REVOKED, CAPTURE_CLOSED

Payload `reason` string não nula, 1..200 caracteres, sem áudio. `CAPTURE_CLOSED` acrescenta `mic_open` bool não nulo, valor legal `false`.

### ERROR

| Campo | Tipo | Null | Regra |
|---|---|---|---|
| error_code | string | no | taxonomia da seção 10 |
| retryable | bool | no | tem de bater com a linha da taxonomia |
| terminal | bool | no | idem |
| provider_code | string | yes | opaco, redigido se parecer segredo |
| message_redacted | string | no | sem áudio, sem transcript, sem segredo |
| speech_error_code | string | yes | obrigatório quando o erro é de invoke; um código da tabela `cmp.speech.v0` |

`invocation_id` do envelope: obrigatório quando `speech_error_code` não é null; null só em erro de sessão sem invoke (`DUPLEX_UNSUPPORTED_VERSION` no preâmbulo não usa este envelope). Flags que discordem da taxonomia: violação de contrato, tratar como não redespachável.

### STREAM_GAP

`missing_sequence` int64 não nulo. `from_sequence` e `to_sequence` int64 não nulos. Sem bytes inventados.

### FALLBACK_TEXT

`reason_code` não nulo. `voice_required` bool não nulo, valor legal `true`. Sem egress de áudio.

## 7. Objeto observation

Presente em todo evento da seção 3. Relógio `forge.media.monotonic_clock`: int64 de nanossegundos, monotônico, não é wall clock. `wall_time_utc` é proibido dentro de `observation` e proibido no predicado de overlap.

| Campo | Tipo | Null no objeto | Significado |
|---|---|---|---|
| clock_domain_id | string | no | domínio único do processo observador. Dois carimbos com domínios diferentes não provam overlap: o predicado fica `NOT_EVALUABLE` e não passa |
| generated_at_ns | int64 | yes | TTS ou plano local produziu o chunk. Observador `TTS_ADAPTER` |
| generated_observer | enum | yes | obrigatório sse o carimbo irmão não é null. Valor `TTS_ADAPTER` |
| received_at_ns | int64 | yes | gateway recebeu o chunk. Observador `GATEWAY` |
| received_observer | enum | yes | `GATEWAY` quando o carimbo existe |
| reproduced_at_ns | int64 | yes | sink reproduziu. Observador `PLAYBACK_SINK`. Só isto entra no intervalo de playback |
| reproduced_observer | enum | yes | `PLAYBACK_SINK` |
| captured_at_ns | int64 | yes | dispositivo aceitou o frame. Observador `DEVICE` |
| captured_observer | enum | yes | `DEVICE` |
| gateway_accepted_at_ns | int64 | yes | gateway aceitou com epoch corrente. Observador `GATEWAY` |
| gateway_accepted_observer | enum | yes | `GATEWAY` |
| stt_forward_at_ns | int64 | yes | byte entregue à invoke STT aberta. Observador `STT_ADAPTER` |
| stt_forward_observer | enum | yes | `STT_ADAPTER` |

Carimbo não nulo com observador null, ou o inverso: `422 VALIDATION`.

Nulabilidade normativa por `event_type`. “req” = não nulo. “null” = tem de ser null; valor presente é `422`.

| event_type | generated | received | reproduced | captured | gateway_accepted | stt_forward |
|---|---|---|---|---|---|---|
| INPUT_AUDIO_CHUNK aceito e encaminhado | null | null | null | req | req | req |
| OUTPUT_AUDIO_CHUNK | req | req | null | null | null | null |
| PLAYBACK_SPAN CHUNK, START ou END com sink ativo | null | null | req | null | null | null |
| STT_PARTIAL, STT_FINAL | null | null | null | null | null | req |
| demais event_types da seção 5 | null | null | null | null | null | null |

`OUTPUT_AUDIO_CHUNK` nasce com `reproduced_at_ns` null. A reprodução é outro evento, `PLAYBACK_SPAN`, correlacionado por `content_sha256` e `source_sequence`. A fixture FX-01 usa essa forma. Um harness que só preencha `generated_at_ns` não satisfaz o intervalo de playback.

## 8. Digest, replay e payload divergente

Corpo canônico: o evento sem o campo `event_digest`, JSON UTF-8, chaves ordenadas em todos os níveis, separadores vírgula e dois-pontos sem espaço, UUID em minúsculas, inteiros decimais sem expoente. `payload_bytes`, quando existem, entram como hex minúsculo. SHA-256 desse UTF-8, hex minúsculo de 64 caracteres.

Exemplo mínimo, só para o algoritmo: o objeto `{"event_id":"00000000-0000-4000-8000-000000000001","sequence":1}` canoniza para essa mesma string e digere para `0abace1a92024c77579c84079786d1ec986e061ab00d3914a19b70206e23c218`.

| Caso | Resultado |
|---|---|
| mesmo `event_id`, mesmo digest, mesmo efeito já cometido | replay do resultado anterior. Zero efeito novo |
| mesmo `event_id`, digest diferente | `409 EVENT_ID_REUSED`. Zero mudança de sessão, zero reserva |
| `event_id` novo | processar |

Dedupe de mídia não é dedupe de `command_id` financeiro. Os dois existem.

## 9. Janela e transporte

Planejamento, não SLO: `forge.media.window_unacked=32`, `forge.media.reorder_window=8`, `forge.media.chunk_max_bytes=16384`. Estouro: `BUFFER_OVERFLOW`, sem descarte silencioso e sem áudio inventado. Lacuna que sobrevive à janela: `STREAM_GAP` e `REJECT_GAP`. O chunk seguinte pode trazer `discontinuity=true`.

Credencial de stream: `session_id + stream_id + capture_generation + consent_grant_epoch`, verificada no gateway. TTL de planejamento `300000` ms. Não é capability de deploy, terminal ou vault. Generation antiga: `422 CONSENT_EPOCH_STALE`.

## 10. Erros

A taxonomia `SPEECH_*` de `cmp.speech.v0` continua válida na invoke. Códigos adicionais:

| Código | retryable | terminal |
|---|---|---|
| DUPLEX_UNSUPPORTED_VERSION | no | yes |
| BUFFER_OVERFLOW | no | no |
| STREAM_GAP | no | no |
| CONSENT_EPOCH_STALE | no | yes |
| TRUST_BOUNDARY_MISMATCH | no | yes |
| SESSION_NOT_DUPLEX | no | yes |
| EVENT_ID_REUSED | no | yes |
| DIGEST_MISMATCH | no | yes |
| STREAM_DIRECTION_MISMATCH | no | yes |
| PAYLOAD_MODE_INVALID | no | yes |
| UNKNOWN_FIELD | no | yes |

`retryable` não autoriza redespacho. CMP-FD-03 decide.

## 11. Crosswalk com `cmp.speech.v0`

| Duplex | Speech v0 |
|---|---|
| HELLO_ACK.selected_speech_contract | `contract_version` das invokes = `cmp.speech.v0` |
| INPUT_AUDIO_CHUNK bytes / hash / encoding / mime / sample_rate / channels | request `speech.transcribe`: `audio`, `audio_encoding`, `audio_mime`, `sample_rate_hz`, `channels` |
| STT_PARTIAL.transcript_state PARTIAL, is_final false | result `transcript_state=PARTIAL`, `is_final=false`, mesmo `invocation_id` |
| STT_FINAL.transcript_state FINAL, is_final true | result `FINAL`, `is_final=true`. Uma operation |
| provider_id, model_id nesses results | os mesmos campos da result v0 |
| USER_SPEECH_START.target_invocation_id | `cancel(invocation_id)` da synthesize |
| CANCEL_ACK.cancel_state | `cancel_state` CONFIRMED ou UNCONFIRMED, códigos `SPEECH_CANCELLED` / `SPEECH_CANCEL_UNCONFIRMED` |
| OUTPUT_AUDIO_CHUNK | result `speech.synthesize`: bytes, encoding, mime, `is_final` false até o fim. Uma operation por invoke |
| PLAYBACK_SPAN | não existe em speech.v0. Não cria operation |
| ERROR.speech_error_code e flags | o objeto de erro v0, flags iguais à tabela v0 |
| operation_ref | `cmp:{turn_id}:speech.transcribe` ou `:speech.synthesize` ou, fora da mídia, `:conversation.respond` |
| data_classification | o mesmo campo, rechecado no egress antes da reserva |

`LOCAL_PIPELINE` e `PROVIDER_DUPLEX` usam este mesmo crosswalk. Muda `media_plane`, não o número de operations nem a família.

Correlação mínima quando houve reserva: `event_id`, `invocation_id`, `turn_id`, `operation_ref`, `task_id`, `build_id` NOT NULL. Evidência real: ABSENT.
