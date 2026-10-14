# CMP-FD-02 v0.4 — Mídia, handshake e ACK

**Estado:** PROPOSTA. Não é PASS. Não substitui `cmp.speech.v0`.
**Achados alvo:** HIGH-03 parcial, NEW-MEDIUM-04, NEW-MEDIUM-05. NEW-MEDIUM-02 permanece fechado: os seis timestamps continuam no schema.
**Campo desconhecido:** `422 UNKNOWN_FIELD`. O evento inteiro é descartado. Zero efeito.

`HELLO_ACK` da v0.3, como um tipo só, não é mais a proposta vigente. A v0.3 não é editada. Aqui a união de preâmbulo tem três tipos.

## 1. Preâmbulo

Schema id: `cmp.media.duplex.v1.preamble`.

### HELLO

| Campo | Tipo | Null | Regra |
|---|---|---|---|
| schema_id | string | no | literal do preâmbulo |
| event_type | string | no | `HELLO` |
| event_id | uuid | no | |
| event_digest | sha256 | no | seção 6, calculado sem este campo |
| channel_id | uuid | no | canal autenticado |
| organization_id | uuid | no | igual ao canal, senão erro |
| project_id | uuid | no | igual ao canal |
| principal_ref | string | no | principal do canal, não do modelo |
| contract_versions_offered | string[] | no | precisa conter `cmp.media.duplex.v1` e `cmp.speech.v0` |
| media_plane_offered | enum[] | no | subconjunto de `LOCAL_PIPELINE`, `PROVIDER_DUPLEX` |
| encodings_offered | enum[] | no | subconjunto de `PCM_S16LE`, `OPUS`, `FLAC` |

Sem áudio, sem reserva, sem microfone, sem task.

### HELLO_ACK_SUCCESS

| Campo | Tipo | Null | Regra |
|---|---|---|---|
| schema_id | string | no | preâmbulo |
| event_type | string | no | `HELLO_ACK_SUCCESS` |
| event_id | uuid | no | |
| event_digest | sha256 | no | |
| in_reply_to | uuid | no | event_id do HELLO |
| selected_media_contract | string | no | exatamente `cmp.media.duplex.v1` |
| selected_speech_contract | string | no | exatamente `cmp.speech.v0` |
| selected_media_plane | enum | no | interseção de oferta, `describe` e registry |
| selected_encoding | enum | no | interseção |
| input_stream_id | uuid | no | distinto dos outros dois |
| output_stream_id | uuid | no | |
| control_stream_id | uuid | no | todo `CONTROL` usa este id |

Este é o único preâmbulo que aloca streams. Ainda não abre microfone e não reserva.

### HELLO_ACK_ERROR

| Campo | Tipo | Null | Regra |
|---|---|---|---|
| schema_id | string | no | preâmbulo |
| event_type | string | no | `HELLO_ACK_ERROR` |
| event_id | uuid | no | |
| event_digest | sha256 | no | |
| in_reply_to | uuid | no | |
| error_code | enum | no | tabela abaixo |
| retryable | bool | no | false em todas as linhas atuais |
| terminal | bool | no | true em todas as linhas atuais |
| message_redacted | string | no | sem áudio e sem segredo |

Campos proibidos neste tipo, e portanto `422 UNKNOWN_FIELD` se aparecerem: `selected_media_contract`, `selected_speech_contract`, `selected_media_plane`, `selected_encoding`, `input_stream_id`, `output_stream_id`, `control_stream_id`, `session_id`, `payload_bytes`.

Efeito de `HELLO_ACK_ERROR`: zero. Não cria sessão, stream, task, Build, reservation, operation nem abre microfone. Não incrementa contador.

| error_code | Quando |
|---|---|
| DUPLEX_UNSUPPORTED_VERSION | a oferta não contém `cmp.media.duplex.v1` |
| SPEECH_UNSUPPORTED_VERSION | a oferta ou o `describe` não contém `cmp.speech.v0` |
| CHANNEL_SCOPE | org ou projeto diverge do canal |
| PREAMBLE_VALIDATION | campo ausente, extra ou tipo errado |

`SPEECH_UNSUPPORTED_VERSION` está nesta taxonomia de preâmbulo e também na taxonomia `SPEECH_*` já existente de `cmp.speech.v0`. Não fica só mencionado em prosa.

Não há downgrade para half-duplex. Texto pode seguir com `voice_required=true`. Isso não marca o MVP de voz como pronto.

## 2. Envelope pós-handshake

Inalterado no que o Codex fechou em NEW-MEDIUM-02, e repetido para o pacote não depender da v0.3:

- `event_type` fechado: `START_SESSION`, `INPUT_AUDIO_CHUNK`, `STT_PARTIAL`, `STT_FINAL`, `USER_SPEECH_START`, `OUTPUT_AUDIO_CHUNK`, `PLAYBACK_SPAN`, `CANCEL_ACK`, `PAUSE_SESSION`, `STOP_SESSION`, `CONSENT_REVOKED`, `CAPTURE_CLOSED`, `ERROR`, `STREAM_GAP`, `FALLBACK_TEXT`.
- `direction=INPUT` usa `input_stream_id`; `OUTPUT` usa `output_stream_id`; `CONTROL` usa `control_stream_id`.
- `sequence_scope = {session_id}/{stream_id}`.
- `OUTPUT_AUDIO_CHUNK` traz `generated_at_ns` e `received_at_ns`, e `reproduced_at_ns` null.
- `PLAYBACK_SPAN` traz `reproduced_at_ns`. A reprodução não reescreve o chunk.
- `INPUT` aceito e encaminhado traz `captured_at_ns`, `gateway_accepted_at_ns` e `stt_forward_at_ns`.
- Carimbo não nulo exige o observador irmão. O inverso também.
- Dois `clock_domain_id` diferentes não provam overlap.

`observation` tem exatamente estes campos: `clock_domain_id`, os seis carimbos e os seis observadores. Não tem `consent_stop_deadline_ns`. Não tem `observation_tolerance_ns`. Esses dois nomes são chaves de configuração, seção 5. Presença deles no evento é `422 UNKNOWN_FIELD`.

Payloads de chunk, STT, `PLAYBACK_SPAN`, `CANCEL_ACK` e `ERROR` continuam os da v0.3: `transcript_state`, `cancel_state`, `discontinuity`, `provider_id`, `model_id`, hash, encoding e `invocation_id` onde já eram obrigatórios. Esta versão não os torna opcionais.

## 3. ACK

`ack_of_sequence` é inteiro ou null. Null significa “este evento não carrega ack”.

Para um `sequence_scope`, `high_water` é o maior inteiro tal que todo sequence de 1 até ele foi aceito. Começa em 0.

| Caso | Resultado |
|---|---|
| null | nenhum ack; o resto do evento segue as próprias regras |
| inteiro `n` com `0 <= n <= high_water` do mesmo scope | ack cumulativo. Ack igual ao último ack aceito é replay: zero efeito novo |
| `n > high_water` | `422 ACK_FUTURE`. O evento inteiro é descartado. Sessão, reservation e high_water não mudam |
| scope diferente do `stream_id` do evento | `422 ACK_SCOPE_MISMATCH`. Zero efeito |
| `n` menor que um ack já aceito nesse scope | `422 ACK_REGRESSION`. Zero efeito |
| mesmo `event_id` e mesmo digest | replay do evento, inclusive do ack. Zero efeito novo |
| mesmo `event_id` e digest diferente | `409 EVENT_ID_REUSED`. Zero efeito |

Ack não é `ProviderEffectProof` e não liquida.

Lacuna de sequence que sobrevive à janela `forge.media.reorder_window` (planejamento 8, não SLO) produz `STREAM_GAP` e `REJECT_GAP`. Não inventa sample. O chunk seguinte pode ter `discontinuity=true`. `discontinuity=true` sem `STREAM_GAP` anterior no mesmo scope é `422`.

## 4. Digest

Algoritmo normativo, o mesmo do verificador `tools/check_fd_fx01_digests.py`:

1. Remover `event_digest`.
2. JSON UTF-8, chaves ordenadas em todos os níveis, separadores vírgula e dois-pontos sem espaço, `ensure_ascii` falso.
3. `null` é JSON null. Inteiro é decimal sem expoente. UUID já está em minúsculas no documento.
4. SHA-256 dos bytes UTF-8, hex minúsculo de 64 caracteres.

Os oito eventos da FX-01 estão em `fixtures/CMP-FD-FX-01-events.json`. Os pares `canonical_utf8 → sha256` estão em `fixtures/CMP-FD-FX-01-digest-vectors.json`. Um byte, um null ou um campo diferente muda o digest. O evento armazenado deixa de bater. Isso é o oráculo O39, ainda NOT RUN como teste de produto.

A checagem estática que confere esses dois arquivos entre si não é execução de O01 e não é PASS do pacote.

## 5. Campos que não entram no envelope

| Nome | Onde vive | Valor neste pacote | Se aparecer num evento |
|---|---|---|---|
| forge.conversation.consent_stop_deadline_ns | configuração de política, não `observation` | null, `PENDING CALIBRATION` | `422 UNKNOWN_FIELD` |
| forge.media.observation_tolerance_ns | configuração de observação, não `observation` | null, `PENDING CALIBRATION` | `422 UNKNOWN_FIELD` |

O corte de consentimento continua atômico, sem depender desse número. A tolerância de overlap da FX-01 continua `overlap_epsilon_ns = 0`, constante da fixture, não este campo.

## 6. Crosswalk mínimo com `cmp.speech.v0`

| Duplex | Speech |
|---|---|
| HELLO_ACK_SUCCESS.selected_speech_contract | `contract_version = cmp.speech.v0` nas invokes |
| HELLO_ACK_ERROR SPEECH_UNSUPPORTED_VERSION | o mesmo código da taxonomia speech, sem invoke |
| INPUT bytes, encoding, mime, rate, channels | request `speech.transcribe` |
| STT_PARTIAL / STT_FINAL | `transcript_state` e `is_final` |
| CANCEL_ACK.cancel_state | `CONFIRMED` ou `UNCONFIRMED` |
| OUTPUT_AUDIO_CHUNK | result de `speech.synthesize`, uma operation por invoke |
| PLAYBACK_SPAN | não existe em speech.v0 e não cria operation |
| operation_ref | `cmp:{turn_id}:speech.transcribe` ou `:speech.synthesize` |

`LOCAL_PIPELINE` e `PROVIDER_DUPLEX` usam a mesma união.

## 7. Envelope e payloads — o pacote não depende da v0.3

A v0.3 não é editada. As regras abaixo são a proposta vigente. Onde a v0.3 diz um único `HELLO_ACK`, leia-se `HELLO_ACK_SUCCESS`. `HELLO_ACK_ERROR` não é evento deste envelope.

### 7.1 Envelope

Todo `event_type` da seção 7.2. Tipo fora da lista: `422 UNKNOWN_FIELD`.

| Campo | Tipo | Null | Regra |
|---|---|---|---|
| schema_id | string | no | `cmp.media.duplex.v1` |
| contract_version | string | no | `cmp.media.duplex.v1` |
| event_type | enum | no | seção 7.2 |
| event_id | uuid | no | |
| event_digest | sha256 | no | seção 4. Divergência do valor enviado: `422 DIGEST_MISMATCH` |
| organization_id | uuid | no | igual ao canal e à sessão |
| project_id | uuid | no | igual ao canal e à sessão |
| session_id | uuid | no | |
| stream_id | uuid | no | o id da direction |
| sequence | int64 | no | `>= 1`, monotônico estrito no `sequence_scope` |
| sequence_scope | string | no | `{session_id}/{stream_id}` |
| direction | enum | no | `INPUT`, `OUTPUT` ou `CONTROL` |
| ack_of_sequence | int64 | yes | seção 3. Não é recibo financeiro |
| gap_policy | enum | no | literal `REJECT_GAP` |
| participant_id | uuid | no | |
| turn_id | uuid | yes | null só em `START_SESSION` |
| invocation_id | uuid | yes | obrigatório quando o payload diz |
| speaker_agent_id | uuid | yes | obrigatório sse saída de fala de agente |
| origin | enum | no | `HUMAN`, `AGENT`, `SYSTEM`, `CODEX_READ_ONLY` |
| source_turn_ids | uuid[] | no | vazio no input humano; não vazio na síntese Jarvis |
| evidence_refs | uuid[] | no | vazio só se o rótulo não é `FACT` |
| epistemic_label | enum | yes | obrigatório em saída textual de agente: `FACT`, `INFERENCE`, `SUGGESTION`, `ABSENCE` |
| media_plane | enum | no | o valor de `HELLO_ACK_SUCCESS`, não o de um erro |
| consent_ref | uuid | yes | obrigatório quando `capture_generation > 0` |
| consent_grant_epoch | int64 | no | |
| capture_generation | int64 | no | |
| data_classification | enum | no | `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED` |
| execution_location | enum | yes | obrigatório se o evento pode egressar |
| trust_boundary | enum | yes | obrigatório no mesmo caso |
| operation_ref | string | yes | obrigatório se há invocation com efeito monetário possível |
| is_final | bool | no | |
| stream_end | bool | no | |
| discontinuity | bool | no | `false` por contrato. `true` só no chunk seguinte a `STREAM_GAP` |
| payload | object | no | exatamente a seção 7.3 daquele `event_type` |
| observation | object | no | seção 2. Sem os dois nomes de configuração |

`INPUT` usa `input_stream_id`. `OUTPUT` usa `output_stream_id`. `CONTROL` usa `control_stream_id`. Direction no stream errado: `422 STREAM_DIRECTION_MISMATCH`. Sequências não se emprestam. `CONTROL` tem o mesmo ACK e o mesmo `REJECT_GAP`.

Estados de sessão, sem estado novo: `CLOSED`, `HANDSHAKE`, `ACTIVE_DUPLEX`, `INTERRUPTING`, `PAUSED`, `STOPPING`, `REVOKED`, `FAILED`. Não existe `HALF_DUPLEX` nem `TURN_TAKING`. Só `ACTIVE_DUPLEX` admite captura e playback abertos juntos.

### 7.2 União

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

### 7.3 Payloads

Campo a mais no payload: `422 UNKNOWN_FIELD`. O evento inteiro é descartado.

`START_SESSION`: `granted` bool não nulo. Sem bytes. `turn_id` e `invocation_id` null.

`INPUT_AUDIO_CHUNK` e `OUTPUT_AUDIO_CHUNK`: `media_encoding` em `PCM_S16LE`, `OPUS`, `FLAC`; `audio_mime` casado (`audio/wav`, `audio/ogg`, `audio/flac`), senão `SPEECH_BAD_AUDIO`; `sample_rate_hz` obrigatório sse PCM e `> 0`; `channels = 1`; `duration_ns > 0`; `payload_mode` `INLINE_BYTES` ou `CONTENT_REF`; `payload_bytes` obrigatório sse inline e proibido no audit; `content_ref` obrigatório sse ref, efêmero; `content_sha256` obrigatório; `content_size_bytes > 0` e igual ao tamanho hasheado. `OUTPUT` exige `invocation_id`. `INPUT` exige `invocation_id` quando já encaminhado ao STT; null se só capturado.

`STT_PARTIAL` e `STT_FINAL`: `transcript_state` `PARTIAL` ou `FINAL`, respectivamente; `transcript_text` não nulo; `language_detected` BCP-47 ou null; `provider_id` não nulo, id de descriptor, não escolha de fornecedor; `model_id` ou null. Envelope `is_final=true` sse `FINAL`. `invocation_id` e `operation_ref` obrigatórios. Segundo `STT_FINAL` no mesmo `invocation_id` é erro de contrato, sem segunda execution. `STT_PARTIAL` não chama tool nem `conversation.respond`.

`USER_SPEECH_START`: `target_invocation_id` uuid não nulo; `interrupt_mode` `STOP_PLAYBACK` ou `DUCK`. Não carrega `cancel_state`.

`PLAYBACK_SPAN`: `span_role` `START`, `CHUNK` ou `END`; `playback_state` `PLAYING`, `DUCKED` ou `STOPPED`; `content_sha256` e `source_sequence` obrigatórios sse `CHUNK`. `invocation_id` obrigatório. O overlap lê `reproduced_at_ns` deste evento. O chunk de saída não é reescrito.

`CANCEL_ACK`: `cancel_state` `CONFIRMED` ou `UNCONFIRMED`; `speech_error_code` `SPEECH_CANCELLED` sse confirmado, `SPEECH_CANCEL_UNCONFIRMED` sse não. `invocation_id` obrigatório. Não liquida e não inventa `NO_EFFECT`.

`PAUSE_SESSION`, `STOP_SESSION`, `CONSENT_REVOKED`, `CAPTURE_CLOSED`: `reason` string 1..200, sem áudio. `CAPTURE_CLOSED` acrescenta `mic_open=false`.

`ERROR`: `error_code`, `retryable`, `terminal` e `message_redacted` não nulos; `provider_code` ou null; `speech_error_code` obrigatório quando o erro é de invoke. `invocation_id` obrigatório sse `speech_error_code` não é null. Flags que discordem da taxonomia não redespacham.

`STREAM_GAP`: `missing_sequence`, `from_sequence`, `to_sequence`, os três int64 não nulos. Sem bytes inventados.

`FALLBACK_TEXT`: `reason_code` não nulo; `voice_required=true`. Sem egress de áudio. Não marca o MVP de voz como dispensado.

### 7.4 Nulabilidade dos seis carimbos

“req” = não nulo. “null” = tem de ser null.

| event_type | generated | received | reproduced | captured | gateway_accepted | stt_forward |
|---|---|---|---|---|---|---|
| INPUT_AUDIO_CHUNK aceito e encaminhado | null | null | null | req | req | req |
| OUTPUT_AUDIO_CHUNK | req | req | null | null | null | null |
| PLAYBACK_SPAN | null | null | req | null | null | null |
| STT_PARTIAL, STT_FINAL | null | null | null | null | null | req |
| demais da seção 7.2 | null | null | null | null | null | null |

Carimbo e observador irmão andam juntos. `wall_time_utc` é proibido em `observation` e no predicado de overlap. Dois `clock_domain_id` diferentes não provam overlap.

### 7.5 Códigos desta união

A taxonomia `SPEECH_*` de `cmp.speech.v0` continua na invoke. Códigos do duplex, todos com o par retryable/terminal abaixo. `retryable` não autoriza redespacho.

| Código | retryable | terminal |
|---|---|---|
| DUPLEX_UNSUPPORTED_VERSION | no | yes |
| SPEECH_UNSUPPORTED_VERSION | no | yes |
| CHANNEL_SCOPE | no | yes |
| PREAMBLE_VALIDATION | no | yes |
| BUFFER_OVERFLOW | no | no |
| STREAM_GAP | no | no |
| CONSENT_EPOCH_STALE | no | yes |
| TRUST_BOUNDARY_MISMATCH | no | yes |
| SESSION_NOT_DUPLEX | no | yes |
| EVENT_ID_REUSED | no | yes |
| DIGEST_MISMATCH | no | yes |
| STREAM_DIRECTION_MISMATCH | no | yes |
| PAYLOAD_MODE_INVALID | no | yes |
| ACK_FUTURE | no | yes |
| ACK_SCOPE_MISMATCH | no | yes |
| ACK_REGRESSION | no | yes |
| UNKNOWN_FIELD | no | yes |

`SPEECH_UNSUPPORTED_VERSION` está nesta tabela e na taxonomia speech. Não é só menção.

Janela, planejamento e não SLO: `forge.media.window_unacked=32`, `forge.media.reorder_window=8`, `forge.media.chunk_max_bytes=16384`. Estouro: `BUFFER_OVERFLOW`, sem descarte silencioso e sem áudio inventado.

### 7.6 Crosswalk completo

Acrescenta a seção 6. Não a contradiz.

| Duplex | Speech v0 |
|---|---|
| HELLO_ACK_SUCCESS.selected_speech_contract | `contract_version = cmp.speech.v0` |
| HELLO_ACK_ERROR / SPEECH_UNSUPPORTED_VERSION | o mesmo código, sem invoke e sem operation |
| INPUT_AUDIO_CHUNK bytes, hash, encoding, mime, rate, channels | request `speech.transcribe` |
| STT_PARTIAL, `is_final=false` | result `PARTIAL`, mesmo `invocation_id` |
| STT_FINAL, `is_final=true` | result `FINAL`. Uma operation |
| provider_id, model_id | os mesmos campos da result, sem eleger fornecedor |
| USER_SPEECH_START.target_invocation_id | `cancel(invocation_id)` da synthesize |
| CANCEL_ACK.cancel_state | `CONFIRMED` / `UNCONFIRMED` e os dois códigos `SPEECH_CANCEL*` |
| OUTPUT_AUDIO_CHUNK | result `speech.synthesize`. Uma operation por invoke |
| PLAYBACK_SPAN | não existe em speech.v0 e não cria operation |
| ERROR.speech_error_code e flags | o objeto de erro v0, flags iguais |
| operation_ref | `cmp:{turn_id}:speech.transcribe` ou `:speech.synthesize` ou, fora da mídia, `:conversation.respond` |
| data_classification | o mesmo campo, rechecado no egress antes da reserva |

Os dois planos usam este crosswalk. Muda `media_plane`, não o número de operations nem a família do adapter.

Correlação mínima quando houve reserva: `event_id`, `invocation_id`, `turn_id`, `operation_ref`, `task_id`, `build_id` NOT NULL. Evidência real: ABSENT.

