# CMP-FD-06 v0.3 — Observabilidade e latência

**Estado:** PROPOSTA. Nenhum valor abaixo foi medido. Não é PASS.
**Achado:** MEDIUM-05 foi marcado CLOSED documentalmente pelo Codex na v0.2. Não há SLA novo.
**Relação com o schema:** os seis carimbos medidos aqui são os campos de `observation` em CMP-FD-02 v0.3. Dois carimbos só entram no mesmo predicado se tiverem o mesmo `clock_domain_id`. Senão o resultado é `NOT_EVALUABLE`, não PASS.
**ADR AQ-07:** a decisão de produto não aprovou SLA. Este arquivo não cria SLA.


## 1. Relógio

`forge.media.monotonic_clock`: inteiro de nanossegundos, monotônico por processo de observação, não ajustável para trás. O predicado de overlap usa só esse relógio.

`wall_time_utc` pode ser logado e não entra no PASS de simultaneidade.

Tolerância do predicado de fixture: `overlap_epsilon_ns = 0` na fixture determinística CMP-FD-FX-01. Não é folga de rede.

Campo `observation_tolerance_ns` existe para uma corrida futura de campo. Valor de aceite: `null`, estado `PENDING CALIBRATION`. Preencher um número aqui seria medição fictícia.

## 2. Catálogo de medidas

Cada medida é um registro. Não é um alvo.

| metric_id | Início | Fim | Unidade | Aceite |
|---|---|---|---|---|
| cmp.fd.latency.speech_to_stt_partial | `captured_at_ns` do primeiro frame aceito do utterance | primeiro `STT_PARTIAL` desse `invocation_id` | ns | PENDING CALIBRATION |
| cmp.fd.latency.speech_to_stt_final | mesmo início | `STT_FINAL` | ns | PENDING CALIBRATION |
| cmp.fd.latency.stt_final_to_first_token | `STT_FINAL` | primeiro token de `conversation.respond` | ns | PENDING CALIBRATION |
| cmp.fd.latency.first_token_to_first_audio | primeiro token | primeiro `generated_at_ns` do TTS | ns | PENDING CALIBRATION |
| cmp.fd.latency.first_audio_received | primeiro `generated_at_ns` | primeiro `received_at_ns` | ns | PENDING CALIBRATION |
| cmp.fd.latency.first_audio_reproduced | primeiro `received_at_ns` | primeiro `reproduced_at_ns` | ns | PENDING CALIBRATION |
| cmp.fd.latency.interrupt_to_playback_change | `USER_SPEECH_START` | LOCAL_PLAYBACK em `STOPPED` ou `DUCKED`, conforme o modo | ns | PENDING CALIBRATION |
| cmp.fd.counter.jitter_ns | n/a | profundidade observada do buffer | ns | PENDING CALIBRATION |
| cmp.fd.counter.loss | n/a | chunks com `STREAM_GAP` | count | PENDING CALIBRATION |
| cmp.fd.counter.underrun | n/a | sink sem sample enquanto `PLAYING` | count | PENDING CALIBRATION |
| cmp.fd.counter.overflow | n/a | `BUFFER_OVERFLOW` | count | PENDING CALIBRATION |
| cmp.fd.counter.reorder | n/a | sequences aplicados fora de ordem e depois aceitos dentro da janela | count | PENDING CALIBRATION |

Percentis `p50`, `p95`, `p99` são colunas anuláveis do registro de calibração futura. Neste pacote são `null`. Um documento que os preencha sem um registro de calibração referenciado é violação, não otimismo.

Cenários nomeados para essa calibração futura, sem resultado: `NOMINAL`, `LOSS`, `REORDER`, `HIGH_JITTER`. Não há amostra.

## 3. O que “baixa latência” significa aqui

Nada, como número. A frase de produto no ADR não virou limiar. O contrato só fixa os pontos de corte para que um oracle futuro possa ler os campos. CMP-FD-O29 passa, no futuro, se os campos existem e os aceites continuam nulos **ou** apontam para uma calibração humana posterior. Falha se um SLA numérico aparece sem essa calibração, ou se o campo nem existe.

Nenhuma dessas medidas libera gasto, escolhe fornecedor ou autoriza BUILD-00.

## 4. Custo observável

Por `session_id`, `turn_id`, `invocation_id`, `operation_ref`, `provider_id` de descriptor, `estimated_minor`, `settled_minor` nulo até prova. Estimado não é gasto. `pending_actual_minor` não é escrito por este pacote; continua projeção da v1.7 quando a linha existir.

Duplo débito é falha de AQ-10, não métrica de qualidade.
