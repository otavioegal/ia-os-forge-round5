# CMP-FD-02 v0.5 — ACK com stream próprio e autenticação do preâmbulo

**Estado:** PROPOSTA. Não é PASS. Não aprova `cmp.media.duplex.v1`.
**Achado alvo:** HIGH-03 ainda PARTIAL. NEW-MEDIUM-02 e NEW-MEDIUM-04 permanecem CLOSED.
**Substituição normativa:** a regra da v0.4 que exige o ack no mesmo `stream_id` do evento deixa de ser a proposta vigente. O arquivo v0.4 não é editado.

Campo desconhecido no evento: `422 UNKNOWN_FIELD`. O evento inteiro é descartado. Zero efeito.

## 1. O que não regride

- União de preâmbulo: `HELLO`, `HELLO_ACK_SUCCESS`, `HELLO_ACK_ERROR`.
- `HELLO_ACK_ERROR` não carrega contrato selecionado nem id de stream. Zero sessão, zero stream, zero task, zero reservation, microfone fechado, zero contador.
- `SPEECH_UNSUPPORTED_VERSION` continua na taxonomia. Não há downgrade para half-duplex. `voice_required` não vira false.
- `observation` tem só `clock_domain_id`, os seis carimbos e os seis observadores. Não tem `consent_stop_deadline_ns` nem `observation_tolerance_ns`.
- `OUTPUT_AUDIO_CHUNK` traz `reproduced_at_ns` null. Quem prova reprodução é `PLAYBACK_SPAN`.
- Payloads da v0.4, seção 7.3, continuam a proposta vigente para o miolo de cada `event_type`. Esta página não os torna opcionais.

## 2. Campos de ACK no envelope

O envelope pós-handshake ganha um discriminante que não é o `stream_id` do próprio evento.

| Campo | Tipo | Null | Regra |
|---|---|---|---|
| stream_id | uuid | no | stream **deste** evento. `CONTROL` usa `control_stream_id` |
| sequence | int64 | no | sequence **deste** evento, no scope `{session_id}/{stream_id}` |
| ack_of_sequence | int64 | yes | null se este evento não carrega ack |
| ack_stream_id | uuid | yes | obrigatório sse `ack_of_sequence` não é null; null sse `ack_of_sequence` é null |

Um dos dois preenchido e o outro null: `422 ACK_SCOPE_MISMATCH`. Zero efeito.

`ack_sequence_scope` derivado, não é campo armazenado: `{session_id}/{ack_stream_id}`. Não se infere de `stream_id`.

Um evento `CONTROL` pode reconhecer `INPUT` ou `OUTPUT`. A sequence do `CONTROL` não é a sequence reconhecida.

A FX-01 desta v0.5 traz `ack_stream_id` null em todos os oito eventos, junto com `ack_of_sequence` null. O overlap não depende de ack.

## 3. Dois high-waters

| Nome | Chave | Significado |
|---|---|---|
| emitted_high_water | `{session_id, stream_id}` | maior inteiro tal que toda sequence de 1 até ele foi aceita neste stream. Começa em 0 |
| peer_ack_high_water | `{session_id, ack_stream_id, receiver_participant_id}` | maior ack já aceito daquele receptor para aquele stream. Começa em 0 |

`receiver_participant_id` é o `participant_id` autenticado do evento que carrega o ack. Não é um terceiro identificador solto.

O ack não altera `emitted_high_water`. O ack não é `ProviderEffectProof` e não liquida.

## 4. Decisão do ack

`n` = `ack_of_sequence`. `S` = `ack_stream_id`. `R` = receptor.

| Caso | Resultado |
|---|---|
| os dois campos null | nenhum ack |
| `S` não é um dos três streams alocados nesta sessão | `422 ACK_STREAM_UNALLOCATED`. O mesmo código se o UUID é aleatório ou se pertence a outra sessão. Corpo sem id estrangeiro. Zero efeito |
| `n < 0` | `422 ACK_REGRESSION`. Zero efeito |
| `n > emitted_high_water` daquele stream | `422 ACK_FUTURE`. Zero efeito. Lacuna no meio impede o high-water de passar. Janela `forge.media.window_unacked=32` não autoriza ack futuro |
| `n < peer_ack_high_water` de `(sessão, S, R)` | `422 ACK_REGRESSION`. Zero efeito |
| `n` igual a esse peer high-water e `n > 0`, ou igual ao último ack já aceito | duplicata. Zero efeito novo. Código de fixture `ACK_DUPLICATE` |
| `0 <= n <= emitted_high_water` e `n > peer_ack_high_water` | aceita. O peer high-water daquele trio passa a `n`. A sequence do evento em si segue as regras do próprio stream |

Ack de stream não alocado não abre sessão e não cria o stream.

Limites: piso `0`; teto `emitted_high_water` do stream reconhecido; regressão contra o peer high-water daquele receptor. Os três são independentes da sequence do evento `CONTROL`.

## 5. Autenticação do preâmbulo

`HELLO.principal_ref` tem de ser igual ao principal autenticado do binding do canal.

| Divergência | Código | Efeito |
|---|---|---|
| org ou projeto diferente do canal | `CHANNEL_SCOPE` | zero |
| `principal_ref` diferente do principal autenticado | `PREAMBLE_AUTH` | zero |
| `principal_ref` ausente | `PREAMBLE_VALIDATION` | zero |
| oferta sem `cmp.speech.v0` | `SPEECH_UNSUPPORTED_VERSION` | zero |

`CHANNEL_SCOPE` não absorve o principal. `PREAMBLE_AUTH` é código próprio, `retryable=false`, `terminal=true`.

Efeito de `PREAMBLE_AUTH`: nenhum. Não cria sessão, stream, task, Build, reservation nem operation. Não abre microfone. Não incrementa contador. Não escolhe half-duplex.

`HELLO_ACK_SUCCESS` só existe quando principal, org, projeto e as duas versões fecham. Ainda assim não abre microfone e não reserva.

## 6. Fixture

`fixtures/CMP-FD-FX-02-ack.json` traz os casos estáticos: cross-stream válido, mesmo stream válido, futuro, regressivo, duplicado, stream não alocado e `PREAMBLE_AUTH`.

`tools/check_fd_fx02_ack.py` só confere a forma desses números. Não executa o protocolo. Não é oráculo. Não é teste de produto.

## 7. Digest

O algoritmo não muda: remover `event_digest`; JSON UTF-8; chaves ordenadas; separadores sem espaço; `ensure_ascii` falso; SHA-256 hex minúsculo de 64 caracteres.

A inclusão de `ack_stream_id: null` muda o digest dos oito eventos em relação à v0.4. Os vetores vigentes são os desta pasta. Os da v0.4 permanecem históricos.

O verificador está em `tools/check_fd_fx01_digests.py`. Rejeita `event_id` duplicado nos eventos, vetor órfão, chave JSON duplicada, `sha256` fora de `[0-9a-f]{64}`, `canonical_byte_length` que não seja int e `event_digest` fora do mesmo formato. Bijeção exata entre os dois conjuntos. Cada vetor é consumido uma vez.
