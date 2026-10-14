# CMP-FD-02 v0.2 — Contrato `cmp.media.duplex.v1`

**Estado:** PROPOSTA. Não implementada. Não substitui `cmp.speech.v0` (CMP-02 v0.3 §7.2), que permanece o contrato de invoke STT/TTS.
**Schema id:** `cmp.media.duplex.v1`.
**Achado alvo:** HIGH-03. Fechamento não declarado.

Meio-duplex, mesmo com barge-in, não satisfaz AQ-07. Este contrato não escolhe fornecedor (AQ-04 não decidida).

## 1. Handshake de versão

Mensagem `HELLO`, direction `CONTROL`, antes de qualquer byte de áudio.

| Campo | Tipo | Null | Regra |
|---|---|---|---|
| contract_versions_offered | string[] | no | deve conter `cmp.media.duplex.v1` e `cmp.speech.v0` |
| media_plane_offered | enum[] | no | subconjunto de `LOCAL_PIPELINE`, `PROVIDER_DUPLEX` |
| encodings_offered | enum[] | no | subconjunto de `PCM_S16LE`, `OPUS`, `FLAC` |

Resposta `HELLO_ACK`:

| Campo | Tipo | Null | Regra |
|---|---|---|---|
| selected_media_contract | string | no | exatamente `cmp.media.duplex.v1` ou erro |
| selected_speech_contract | string | no | exatamente `cmp.speech.v0` ou erro |
| selected_media_plane | enum | no | um valor que `describe` e o registry ambos admitem |
| selected_encoding | enum | no | um valor da interseção |

Se `describe.contract_versions` não contém `cmp.speech.v0`, o roteador não chama `invoke` e não envia áudio. Erro `SPEECH_UNSUPPORTED_VERSION` (já na v0.3).

Se o par duplex não for selecionado, erro `DUPLEX_UNSUPPORTED_VERSION`, terminal, não retryable. **Não** há downgrade silencioso para turn-taking. A UI pode seguir em texto com `voice_required` ainda verdadeiro (CMP-02 v0.3 §9). Isso não marca o MVP de voz como satisfeito (oráculo CMP-FD-O11).

`HELLO` não reserva dinheiro e não abre o microfone.

## 2. Envelope de todo evento depois do handshake

Campo ausente que a tabela marca como não nulo, ou campo desconhecido: `422 VALIDATION`. O evento é descartado. Não há coerce.

| Campo | Tipo | Null | Regra |
|---|---|---|---|
| contract_version | string | no | literal `cmp.media.duplex.v1` |
| organization_id | uuid | no | |
| project_id | uuid | no | |
| session_id | uuid | no | |
| stream_id | uuid | no | um stream por direção por capture_generation |
| event_id | uuid | no | dedupe. Replay do mesmo id não reprocessa |
| sequence | int64 | no | `>= 1`, monotônico estrito no escopo abaixo |
| sequence_scope | string | no | literal `{session_id}/{stream_id}` |
| direction | enum | no | `INPUT`, `OUTPUT`, `CONTROL` |
| event_type | enum | no | lista §4 |
| timestamp_monotonic_ns | int64 | no | relógio `forge.media.monotonic_clock`. Não é wall clock |
| wall_time_utc | date-time | yes | observacional. Proibido usá-lo no predicado de overlap |
| participant_id | uuid | no | humano ou agente |
| turn_id | uuid | sim | null só em `HELLO`, `HELLO_ACK`, `START_SESSION`. Obrigatório nos demais |
| invocation_id | uuid | sim | obrigatório em eventos ligados a STT ou TTS |
| speaker_agent_id | uuid | sim | obrigatório sse `direction=OUTPUT` e o evento é fala de agente |
| origin | enum | no | `HUMAN`, `AGENT`, `SYSTEM`, `CODEX_READ_ONLY` |
| source_turn_ids | uuid[] | no | vazio no input humano; não vazio em síntese Jarvis |
| evidence_refs | uuid[] | no | vazio só quando o rótulo não é `FACT` |
| epistemic_label | enum | sim | `FACT`, `INFERENCE`, `SUGGESTION`, `ABSENCE`. Obrigatório em saída textual de agente |
| media_encoding | enum | sim | obrigatório em chunk de áudio: `PCM_S16LE`, `OPUS`, `FLAC` |
| audio_mime | string | sim | `audio/wav`, `audio/ogg` ou `audio/flac`, casado com o encoding como em `cmp.speech.v0`. Descasamento: `SPEECH_BAD_AUDIO` |
| sample_rate_hz | int | sim | obrigatório sse encoding é `PCM_S16LE`; inteiro `> 0` |
| channels | int | sim | obrigatório em áudio; valor `1` |
| duration_ns | int64 | sim | obrigatório em chunk de áudio; `> 0` |
| payload_mode | enum | no | `INLINE_BYTES` ou `CONTENT_REF` ou `NONE` |
| payload_bytes | bytes | sim | obrigatório sse mode é `INLINE_BYTES`. Proibido no audit log |
| content_ref | string | sim | obrigatório sse mode é `CONTENT_REF`. Efêmero. Não é arquivo durável de áudio |
| content_sha256 | sha256 | sim | obrigatório quando há payload de áudio. Hash dos bytes do chunk |
| content_size_bytes | int64 | sim | obrigatório quando há áudio; `> 0` e igual ao tamanho hasheado |
| is_final | bool | no | |
| stream_end | bool | no | true só no último chunk do stream. Implica fim de stream, não implica sozinho `is_final` de transcript |
| consent_ref | uuid | sim | obrigatório quando `capture_generation > 0` |
| consent_grant_epoch | int64 | no | |
| capture_generation | int64 | no | |
| data_classification | enum | no | quatro classes de AQ-05 |
| execution_location | enum | sim | obrigatório em evento que pode egressar: `LOCAL`, `SELF_HOSTED`, `EXTERNAL` |
| trust_boundary | enum | sim | obrigatório no mesmo caso: `DEVICE`, `GATEWAY`, `PROVIDER` |
| media_plane | enum | no | `LOCAL_PIPELINE` ou `PROVIDER_DUPLEX` |
| operation_ref | string | sim | obrigatório quando o evento está ligado a invocation com efeito monetário possível |
| ack_of_sequence | int64 | sim | ack cumulativo do peer nesse `sequence_scope` |
| gap_policy | enum | no | literal `REJECT_GAP` |

Escopo da monotonicidade: `sequence` não é global da sessão. Dois streams têm contadores independentes. Um buraco no escopo não é preenchido por sequência do outro sentido.

## 3. Sessão de mídia — estados e transições

Estados: `CLOSED`, `HANDSHAKE`, `ACTIVE_DUPLEX`, `INTERRUPTING`, `PAUSED`, `STOPPING`, `REVOKED`, `FAILED`.

| De | Evento | Para | Efeito lateral obrigatório |
|---|---|---|---|
| CLOSED | HELLO aceito | HANDSHAKE | mic fechado |
| HANDSHAKE | START_SESSION com authn, grant e classificação permitida | ACTIVE_DUPLEX | mic pode abrir; generation incrementa |
| HANDSHAKE | HELLO rejeitado | FAILED | nenhum byte |
| ACTIVE_DUPLEX | USER_SPEECH_START durante saída | INTERRUPTING | ver CMP-FD-03; captura **não** espera o fim do TTS |
| INTERRUPTING | CANCEL_ACK ou stop local já cometido e input segue | ACTIVE_DUPLEX | não é modo exclusivo permanente |
| ACTIVE_DUPLEX | PAUSE_SESSION ou background | PAUSED | mic fecha; generation incrementa; grant pode permanecer |
| PAUSED | resume explícito | ACTIVE_DUPLEX | nova generation; não reabre sozinho |
| ACTIVE_DUPLEX ou PAUSED ou INTERRUPTING | STOP_SESSION | STOPPING | mic fecha |
| STOPPING | CAPTURE_CLOSED ack | CLOSED | |
| qualquer não CLOSED | CONSENT_REVOKED | REVOKED | epochs incrementam; buffers locais descartados |
| REVOKED | CAPTURE_CLOSED | CLOSED | novo START exige grant novo |
| qualquer | versão ou auth inválida | FAILED | sem downgrade |

`ACTIVE_DUPLEX` é o único estado em que input e output podem estar ambos abertos. Não existe estado normativo `HALF_DUPLEX` nem `TURN_TAKING`.

## 4. Catálogo de eventos

| event_type | direction | Liga a speech.v0 | Liga a operation |
|---|---|---|---|
| HELLO / HELLO_ACK | CONTROL | escolhe `cmp.speech.v0` | não |
| START_SESSION | CONTROL | não invoca | não |
| INPUT_AUDIO_CHUNK | INPUT | bytes que poderão compor **uma** invoke `speech.transcribe` | não, por chunk |
| STT_PARTIAL | CONTROL | result `transcript_state=PARTIAL`, `is_final=false` | a mesma operation da invoke |
| STT_FINAL | CONTROL | result `FINAL`, `is_final=true` | a mesma operation; único FINAL |
| USER_SPEECH_START | CONTROL | dispara `cancel(invocation_id)` do TTS ativo, além do gesto local | não cria operation |
| OUTPUT_AUDIO_CHUNK | OUTPUT | result de `speech.synthesize` | uma operation por invoke, não por chunk |
| PLAYBACK_SPAN | OUTPUT | não é result de speech | não |
| CANCEL_ACK | CONTROL | `cancel_state` CONFIRMED ou UNCONFIRMED | não liquida |
| PAUSE_SESSION / STOP_SESSION / CONSENT_REVOKED | CONTROL | pode pedir cancel | não libera dinheiro |
| CAPTURE_CLOSED | CONTROL | não | não |
| ERROR | CONTROL | mapeia quando a falha é da invoke | não redespacha por si |
| STREAM_GAP | CONTROL | não | não |
| FALLBACK_TEXT | CONTROL | sem invoke de voz | sem egress de áudio |

`STT_PARTIAL` não chama tool, não chama `conversation.respond` e não fecha turno. Só `STT_FINAL` pode virar turno humano, ainda sujeito à política. Um segundo `STT_FINAL` no mesmo `invocation_id` é erro de contrato e não inicia outra execução (regra já existente na v0.3).

`conversation.respond` não é evento de mídia. Acontece depois de `STT_FINAL`, com `operation_ref = cmp:{turn_id}:conversation.respond`, capability MODEL, família não ampliada.

Forma dos `operation_ref`, 1..128 caracteres, herdada:

- `cmp:{turn_id}:speech.transcribe`
- `cmp:{turn_id}:speech.synthesize`
- `cmp:{turn_id}:conversation.respond`

## 5. Chunk, janela, ack, lacuna, backpressure

Parâmetros de planejamento, não SLO e não medição:

| Id | Valor | Papel |
|---|---|---|
| forge.media.window_unacked | 32 | chunks não ackados por stream |
| forge.media.reorder_window | 8 | quantos sequences futuros podem esperar um buraco |
| forge.media.chunk_max_bytes | 16384 | acima disso `SPEECH_BAD_AUDIO` |

Se a quantidade não ackada excede a janela, o sender para. Não descarta em silêncio. Estourar o buffer é `BUFFER_OVERFLOW`, evento de erro, sem inventar áudio.

Reorder: o receptor guarda até `reorder_window`. Se o buraco permanece, emite `STREAM_GAP` e aplica `REJECT_GAP`: não sintetiza o sample faltante, não finge continuidade, não abre turno humano a partir do buraco. O stream pode continuar do próximo sequence explícito marcado `discontinuity=true` no payload de controle, ou encerrar com `stream_end`.

Ack é `ack_of_sequence` cumulativo no escopo. Ack de mídia não é recibo financeiro e não é `ProviderEffectProof`.

Perda, jitter e reordenação são contadores do CMP-FD-06. Não têm limiar de aceite neste pacote.

## 6. Três relógios do áudio de saída

Todo chunk de saída que exista carrega três carimbos monotônicos, nulos quando o fato ainda não ocorreu:

| Campo | Fato | Conta para o intervalo de playback? |
|---|---|---|
| generated_at_ns | o TTS ou o plano local **produziu** o chunk | não |
| received_at_ns | o gateway **recebeu** o chunk do provider ou do plano local | não |
| reproduced_at_ns | o sink de playback **reproduziu** o chunk | sim |

`output_playback_start` é o menor `reproduced_at_ns` da sessão no span. `output_playback_end` é o maior `reproduced_at_ns` enquanto o sink permanece em `PLAYING` ou `DUCKED`, ou o instante do stop local, o que a máquina CMP-FD-03 definir para o span. Chunk só gerado ou só recebido não prolonga playback.

Entrada:

| Campo | Fato |
|---|---|
| captured_at_ns | o dispositivo aceitou o frame |
| gateway_accepted_at_ns | o gateway aceitou o chunk com epoch corrente |
| stt_forward_at_ns | o byte foi entregue à invoke de STT aberta |

`input_capture_start` / `input_capture_end` usam `captured_at_ns` dos chunks **aceitos**. Chunk rejeitado por epoch não entra no intervalo.

## 7. Transporte e auth por stream

Binding de planejamento: canal autenticado já escopado por organização e projeto, uma credencial de stream derivada de `session_id + stream_id + capture_generation + consent_grant_epoch`, verificada no gateway. Não é API pública de browser que fale com o provider pulando o gateway.

A credencial não é capability de deploy, terminal ou vault. Expiração de planejamento `forge.media.stream_credential_ttl_ms = 300000`, não é SLO. Credencial de generation antiga é `422 CONSENT_EPOCH_STALE`.

Timeouts de invoke continuam os da v0.3 §7.2 (`stt_timeout_ms` 15000, `tts_first_byte_target_ms` 800, `barge_in_stop_ms` 200). Continuam propostas de configuração, não medições. O duplex não os transforma em SLA (AQ-07 não aprovou SLA).

## 8. Erros de mídia

Além da taxonomia `SPEECH_*` da v0.3, que permanece normativa para a invoke:

| Código | retryable | terminal | Quando |
|---|---|---|---|
| DUPLEX_UNSUPPORTED_VERSION | no | yes | handshake sem o par de contratos |
| BUFFER_OVERFLOW | no | no | janela estourada; não redespacha operation incerta |
| STREAM_GAP | no | no | lacuna após a janela de reorder |
| CONSENT_EPOCH_STALE | no | yes | epoch ou generation velha |
| TRUST_BOUNDARY_MISMATCH | no | yes | registry discorda do adapter |
| SESSION_NOT_DUPLEX | no | yes | evento de áudio fora de `ACTIVE_DUPLEX` ou `INTERRUPTING` |
| DUPLICATE_EVENT | no | yes | mesmo `event_id` com payload diferente |
| PAYLOAD_MODE_INVALID | no | yes | bytes e ref ambos, ou nenhum quando havia áudio |

`retryable` continua sem ser permissão de redespacho. CMP-FD-03 e CMP-02 v0.3 §9 decidem.

## 9. Crosswalk normativo

| Evento duplex | Campo speech.v0 correspondente | Dinheiro |
|---|---|---|
| HELLO_ACK selected_speech_contract | `contract_version` futuro das invokes será `cmp.speech.v0` | nenhum |
| INPUT_AUDIO_CHUNK aceito | ainda não é request; os bytes acumulados viram `audio` de **uma** request `speech.transcribe` | reserva só quando a invoke é reservada, uma vez |
| STT_PARTIAL | `transcript_state=PARTIAL`, `is_final=false`, mesmo `invocation_id` | não incrementa `reserved` de novo |
| STT_FINAL | `transcript_state=FINAL`, `is_final=true` | mesma operation `cmp:{turn_id}:speech.transcribe` |
| segundo FINAL | erro de contrato v0.3 | proibido segunda execution |
| USER_SPEECH_START | `cancel(invocation_id)` do synthesize ativo | não cria operation |
| CANCEL_ACK CONFIRMED | `cancel_state=CONFIRMED`, código `SPEECH_CANCELLED` | não inventa `NO_EFFECT` |
| CANCEL_ACK UNCONFIRMED | `UNCONFIRMED`, `SPEECH_CANCEL_UNCONFIRMED` | se já houve dispatch, reservation fica HELD |
| OUTPUT_AUDIO_CHUNK | `audio` bytes, encoding, mime, `is_final` false até o fim | uma operation `speech.synthesize` |
| OUTPUT is_final e stream_end | `is_final=true` | não é segunda operation |
| PLAYBACK_SPAN | sem campo em speech.v0; existe só aqui | nenhum |
| ERROR de invoke | objeto de erro v0.3, flags iguais à tabela | sem redespacho se UNKNOWN/HELD |
| operation_ref do evento | o mesmo string da request speech | chave do ledger v1.7 |
| provider_id / model_id | os da result speech, id de descriptor | não são escolha de fornecedor |
| data_classification | o mesmo campo da request, rechecado no egress | Policy antes da reserva |
| Áudio no audit | proibido nos dois contratos | digest apenas |

Plano local e provider duplex nativo são o mesmo crosswalk. O que muda é `media_plane`, não o número de operations nem a família do adapter.

## 10. Correlação mínima exigida

Para cada invocation STT ou TTS observável no futuro, a evidência terá de mostrar uma linha com: `event_id` de mídia, `invocation_id`, `turn_id`, `operation_ref`, `task_id` da âncora, `build_id` NOT NULL. Ausência de qualquer um desses seis, quando houve reserva, é falha de contrato, não um campo opcional.

Não há, neste repositório, essa evidência. Estado: ABSENT.
