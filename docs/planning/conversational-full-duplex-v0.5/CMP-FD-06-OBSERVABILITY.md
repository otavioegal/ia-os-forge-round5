# CMP-FD-06 v0.5 — Observabilidade

**Estado:** PROPOSTA. Nenhum número abaixo foi medido. Não é PASS. Não há SLA. AQ-07 não aprovou SLA.
**MEDIUM-05** permanece como o Codex fechou. **NEW-MEDIUM-04** permanece fechado: `observation_tolerance_ns` não é campo de evento.

## Relógio

`forge.media.monotonic_clock`, nanossegundos, monotônico por `clock_domain_id`. O overlap usa só esse relógio. `wall_time_utc` não entra no PASS.

`overlap_epsilon_ns = 0` na FX-01. É constante de fixture.

`forge.media.observation_tolerance_ns` é chave de configuração. Valor: null. Estado: `PENDING CALIBRATION`. Não é campo de `observation`. Um evento que carregue o nome é `422 UNKNOWN_FIELD` (O48).

## Pontos, sem aceite numérico

| metric_id | Início | Fim | Aceite |
|---|---|---|---|
| cmp.fd.latency.speech_to_stt_partial | `captured_at_ns` | primeiro `STT_PARTIAL` | PENDING CALIBRATION |
| cmp.fd.latency.speech_to_stt_final | mesmo início | `STT_FINAL` | PENDING CALIBRATION |
| cmp.fd.latency.interrupt_to_playback_change | `USER_SPEECH_START` | playback `STOPPED` ou `DUCKED` | PENDING CALIBRATION |

`p50`, `p95` e `p99` são null. Custo observável continua por `operation_ref`: estimate não é gasto; `settled_minor` só depois de prova. Pending não é escrito por regra nova além do insert append-only já especificado. A projeção de resolução histórica não altera a linha.
