# CMP-FD-07 v0.4 — Oráculos e fixtures

**Nenhum oráculo foi executado.** Evidence ABSENT. NOT RUN. Não é PASS.
**IDs novos:** CMP-FD-O41..O52. Não colidem com O01..O40 nem com CMP-O-01..36.
**CMP-O-28** continua o oráculo de independência. **CMP-FD-O28** continua AEC/VAD. Um não substitui o outro.

## 1. LOW-01 — OPEN BLOCKING DoR

Sete histórias. Pessoa PENDING. Effort UNSTATED. DoR NOT MET. O autor não nomeia ninguém e não estima.

| ID | Papel proposto | Pessoa | Effort | DoR |
|---|---|---|---|---|
| CMP-FD-S01 | Conversational Product Spec Owner | PENDING | UNSTATED | NOT MET |
| CMP-FD-S02 | Conversational Product Spec Owner | PENDING | UNSTATED | NOT MET |
| CMP-FD-S03 | Conversational Product Spec Owner | PENDING | UNSTATED | NOT MET |
| CMP-FD-S04 | Privacy Spec Owner | PENDING | UNSTATED | NOT MET |
| CMP-FD-S05 | Ledger Spec Owner | PENDING | UNSTATED | NOT MET |
| CMP-FD-S06 | Privacy Spec Owner | PENDING | UNSTATED | NOT MET |
| CMP-FD-S07 | Policy Spec Owner | PENDING | UNSTATED | NOT MET |

Processo ainda não ocorrido: um ato humano do Founder nomeia a pessoa; essa pessoa registra effort; só então o DoR poderia ser reavaliado. Checklist desmarcada: pessoa, effort, schema v0.4 citado, fixtures identificadas. Sem o ato, o estado é **OPEN BLOCKING DoR**. Papel proposto não remove o bloqueio.

Negativo: marcar qualquer história como Ready ou DoR MET sem pessoa e effort é falha de governança. Isso também não foi executado.

## 2. FX-01 — predicado preservado

Artefato normativo: `fixtures/CMP-FD-FX-01-events.json`, oito eventos. Vetores: `fixtures/CMP-FD-FX-01-digest-vectors.json`.

Intervalos lidos desses eventos, não de uma tabela paralela:

- playback começa no span G0, `reproduced_at_ns = 100000000`;
- I0 tem `captured_at_ns = 300000000`, `gateway_accepted_at_ns = 310000000`, `stt_forward_at_ns = 320000000`;
- span G1 reproduz em `400000000`, depois da captura de I0 e dentro da interseção;
- fim da captura = `650000000 + 20000000 = 670000000` (I1);
- fim do playback reproduzido = span G2 em `880000000`;
- interseção = `[300000000, 670000000]`;
- `OUTPUT` de G1 tem `reproduced_at_ns` null. Quem prova reprodução é o `PLAYBACK_SPAN`.

O01 passa no futuro só se esse predicado for verdadeiro. O13 continua o negativo de `STOPPED` antes do forward. O14 continua o negativo de usar só `generated_at_ns`. Os três estão NOT RUN.

O39: o mesmo `event_id` de I0 com um byte ou um campo diferente produz outro digest e `409 EVENT_ID_REUSED`, sem efeito. NOT RUN.

## 3. NEW-HIGH-04

### CMP-FD-O41 — actual não cabe na fatia

Antes: L = 50, E = 40, S = 0, H = 40, spent = 0, reserved = 40, teto do root = 100. Prova RECEIPT conclusiva com A = 70. O root comportaria 70.

PASS do oráculo: zero movimento; spent = 0; reserved = 40; L = 50; operation `RECONCILING`; um pending razão `SESSION_SLICE` valor 70; retorno `409 SESSION_SLICE_EXCEEDED`.

FAIL: spent = 70, ou L elevado para 70, ou prova apagada, ou segunda reservation.

NOT RUN.

### CMP-FD-O42 — actual cabe

Mesmo estado, A = 45.

PASS: um movimento; spent = 45; reserved = 0; L = 50; sem pending de fatia.

FAIL: bloquear um actual que satisfaz `S + H - E + A <= L` e o teto do root.

NOT RUN.

## 4. Tenant — O37 expandido

Canal da org A e do projeto A. Cada subcaso usa um UUID que existe só na org B. Corpo sempre `{"error_code":"NOT_FOUND","retryable":false,"terminal":true}`. Zero lock na linha B. Zero contador alterado em B. Zero Operation nova. Zero Reservation nova.

| Subcaso | Elo estrangeiro |
|---|---|
| O37-S | session_id |
| O37-B | build_id do root |
| O37-T | task_id |
| O37-O | operation_id |
| O37-R | reservation_id |
| O37-X | task da org A com operation_id da org B no mesmo comando |

FAIL: qualquer subcaso com código diferente, corpo que cite a org B, ou débito em B.

NOT RUN. Os subcasos não criam IDs novos; continuam sendo O37.

## 5. Replay e CAS

### CMP-FD-O43

`command_id` já cometido, digest igual, `expected_build_version` ainda a versão antiga, banco já em version maior.

PASS: `200 IDEMPOTENT_REPLAY`. Nenhum CAS é aplicado. Zero movimento novo.

FAIL: `409 VERSION_CONFLICT` nesse replay.

NOT RUN.

### CMP-FD-O44

Outro `command_id`, sem linha em `command_commit`, versions esperadas velhas.

PASS: `409 VERSION_CONFLICT`. Sem `command_commit`. Sem reservation nova.

NOT RUN.

### CMP-FD-O45

Mesmo `command_id` já cometido, um campo do payload diferente, digest diferente.

PASS: `409 IDEMPOTENCY_KEY_REUSED`. Outcome antigo intacto.

NOT RUN.

Crash antes do commit e `40001` não deixam linha. O retry não duplica movimento. Isso é critério de O43/O44, não um ensaio executado.

## 6. Handshake, ACK e campo ilegal

### CMP-FD-O46

HELLO sem `cmp.speech.v0` na oferta.

PASS: `HELLO_ACK_ERROR` com `SPEECH_UNSUPPORTED_VERSION`. Zero sessão, zero stream, zero task, zero reservation, microfone fechado.

FAIL: `HELLO_ACK_SUCCESS` parcial, ou alocação de `session_id`.

NOT RUN.

### CMP-FD-O47

`high_water = 2`. Evento com `ack_of_sequence = 9`.

PASS: `422 ACK_FUTURE`. high_water continua 2. Reservation inalterada.

Ack repetido igual a 2: zero efeito novo. Ack de outro stream: `422 ACK_SCOPE_MISMATCH`.

NOT RUN.

### CMP-FD-O48

Evento pós-handshake com `consent_stop_deadline_ns` ou `observation_tolerance_ns`.

PASS: `422 UNKNOWN_FIELD`. Zero efeito.

FAIL: aceitar o campo ou exigí-lo para o corte de consentimento.

NOT RUN.

## 7. AEC — O28 refeito, mais O51 e O52

Entradas. `PCM_S16LE`, 48000 Hz, um canal. Sem campo `echo`.

- `reference[i]` para i em 0..959: `8000` se `(i // 40) % 2 == 0`, senão `-8000`.
- `human[i] = 0` fora de 1000..1199. Nesse intervalo, `human[i] = 16000`, exceto `human[1199] = 32000`.
- `echo[i] = 0` se i < 480; senão `reference[i-480] // 2`.
- `mic[i] = clamp(echo[i] + human[i])`, com `clamp` no intervalo fechado de int16, de `-32768` a `32767`.

No intervalo 1000..1198 os dois sinais coexistem. Exemplo: eco `4000` e humano `16000` produzem mic `20000`, não `16000`. Em 1199, `32000 + echo` satura em `32767`. A fala não apaga o eco na construção do microfone.

`aec_decision` e `forwarded_pcm` são saída do componente.

### CMP-FD-O28

PASS futuro, todas as linhas:

1. `mic_open` permanece como estava. O AEC não abre microfone fechado e não incrementa `capture_generation`.
2. Em 1000..1198, cada amostra de `forwarded_pcm` difere de `human[i]` em no máximo `1000`, e difere de `mic[i]` em mais de `1000`. A fala permanece; o eco sai.
3. A amostra 1199 de `forwarded_pcm` é `32767` ou difere de `human` saturado em no máximo `1000`, e não é o mic pré-clamp.
4. Em 480..999, onde o humano é 0, cada amostra difere de 0 em no máximo `400`.
5. O STT recebe `forwarded_pcm`, não o `mic` bruto e não silêncio.

FAIL: `forwarded` igual a `mic`; ou fala zerada; ou entrada com `echo=true`.

Os limites `1000` e `400` são `FIXTURE_CONSTANT`. Não são SLA. NOT RUN.

### CMP-FD-O51 — eco puro

`human[i] = 0` em todo o vetor. `mic` é só o eco atrasado.

PASS: `forwarded` difere de 0 em no máximo `400`; `mic_open` não muda; nenhum turno humano é aberto.

FAIL: abrir turno ou fechar o microfone.

NOT RUN.

### CMP-FD-O52 — falso positivo

Mesma mistura de O28, porém a saída vem vazia ou com `aec_decision=DROPPED`, ou `mic_open` passa a false.

PASS do oráculo: essa saída é reprovada. O microfone consentido não fecha por causa do eco.

NOT RUN.

## 8. Sessão composta

### CMP-FD-O49

O mesmo `session_id` na org A e na org B, projetos distintos, os dois sem task aberta.

PASS: as duas aberturas sucedem. Duas tasks. Nenhum erro. A resposta de A não cita B.

NOT RUN.

### CMP-FD-O50

Segunda abertura no mesmo org, projeto e `session_id`, com a primeira ainda `OPEN`.

PASS: `409 ANCHOR_EXISTS`. Uma task só.

NOT RUN.

## 9. O que permanece NOT RUN sem texto novo

O01..O36, O38, O40 e os demais O01..O40 que esta página não reescreve continuam com o critério da v0.3, subordinados às correções de ordem do CMP-FD-01 v0.4 quando falam de CAS ou de fatia. Não foram executados. Os 91 oráculos v1.7 e os 36 CMP-O também não.
