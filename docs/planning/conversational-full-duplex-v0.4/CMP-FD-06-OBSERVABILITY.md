# CMP-FD-06 v0.4 — Observabilidade

**Estado:** PROPOSTA. Nenhum número abaixo foi medido. Não é PASS. Não há SLA. AQ-07 não aprovou SLA.
**MEDIUM-05** permanece como o Codex fechou. **NEW-MEDIUM-04:** `observation_tolerance_ns` não é campo de evento.

## Relógio

`forge.media.monotonic_clock`, nanossegundos, monotônico por `clock_domain_id`. O overlap usa só esse relógio. `wall_time_utc` não entra no PASS.

`overlap_epsilon_ns = 0` na FX-01. É constante de fixture.

`forge.media.observation_tolerance_ns` é chave de configuração para uma corrida futura. Valor: null. Estado: `PENDING CALIBRATION`. Não é campo de `observation`. Preencher um inteiro aqui seria medição fictícia. Um evento que carregue o nome é `422 UNKNOWN_FIELD` (O48).

## Pontos, sem aceite numérico

| metric_id | Início | Fim | Aceite |
|---|---|---|---|
| cmp.fd.latency.speech_to_stt_partial | `captured_at_ns` do primeiro frame aceito | primeiro `STT_PARTIAL` | PENDING CALIBRATION |
| cmp.fd.latency.speech_to_stt_final | mesmo início | `STT_FINAL` | PENDING CALIBRATION |
| cmp.fd.latency.stt_final_to_first_token | `STT_FINAL` | primeiro token | PENDING CALIBRATION |
| cmp.fd.latency.first_token_to_first_audio | primeiro token | primeiro `generated_at_ns` | PENDING CALIBRATION |
| cmp.fd.latency.first_audio_received | primeiro `generated_at_ns` | primeiro `received_at_ns` | PENDING CALIBRATION |
| cmp.fd.latency.first_audio_reproduced | primeiro `received_at_ns` | primeiro `reproduced_at_ns` de `PLAYBACK_SPAN` | PENDING CALIBRATION |
| cmp.fd.latency.interrupt_to_playback_change | `USER_SPEECH_START` | playback `STOPPED` ou `DUCKED` | PENDING CALIBRATION |
| cmp.fd.counter.loss | — | `STREAM_GAP` | PENDING CALIBRATION |
| cmp.fd.counter.underrun | — | sink sem sample em `PLAYING` | PENDING CALIBRATION |
| cmp.fd.counter.overflow | — | `BUFFER_OVERFLOW` | PENDING CALIBRATION |

`p50`, `p95` e `p99` são null. Cenários `NOMINAL`, `LOSS`, `REORDER` e `HIGH_JITTER` não têm amostra.

Custo observável continua por `operation_ref`: estimate não é gasto; `settled_minor` só depois de prova. `pending_actual_minor` não é escrito por regra nova.
