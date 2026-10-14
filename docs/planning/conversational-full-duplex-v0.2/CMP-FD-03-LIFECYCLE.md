# CMP-FD-03 v0.2 — Máquinas de estado separadas

**Estado:** PROPOSTA. Não executada.
**Achado alvo:** MEDIUM-01. Fechamento não declarado.
**Não cria status monetário novo.** A quarta máquina é a de FDP-16A §3.4 e §8A.

Duck, stop local e cancel de provider são comandos diferentes. Um não implica o outro.

## 1. LOCAL_PLAYBACK

Estados: `IDLE`, `PLAYING`, `DUCKED`, `STOPPED`.

| De | Comando | Para | ACK de provider exigido? | Efeito no TTS |
|---|---|---|---|---|
| IDLE | PLAY quando o primeiro chunk tem `reproduced_at_ns` | PLAYING | não | nenhum |
| PLAYING | DUCK | DUCKED | não | geração continua |
| DUCKED | UNDUCK | PLAYING | não | geração continua |
| PLAYING ou DUCKED | STOP_LOCAL | STOPPED | não | não liquida e não prova cancel |
| STOPPED | PLAY de uma invoke nova, outro `invocation_id` | PLAYING | não | a invoke antiga não ressuscita |
| qualquer | DRAIN_END sem stop | IDLE | não | só se a invoke já está COMPLETE |

`STOP_LOCAL` é best-effort no dispositivo. Entra em `STOPPED` sem `CANCEL_ACK`. Isso corta o que a pessoa ouve. Não encerra a invoke e não zera custo.

`DUCK` reduz ganho local. A saída continua `PLAYING` do ponto de vista do intervalo de reprodução: chunks com `reproduced_at_ns` ainda contam como playback. Duck **não** é o predicado de full-duplex e **não** substitui captura simultânea. Também não é cancelamento.

Interrupt_mode da sessão, escolhido por política de produto, não pelo modelo:

| Modo | Gesto em `USER_SPEECH_START` |
|---|---|
| `STOP_PLAYBACK` | `STOP_LOCAL` imediato e `cancel` da invoke TTS. Default desta proposta, porque AQ-07 pediu interrupção. |
| `DUCK` | `DUCK` e a invoke TTS segue até o fim ou até um cancel explícito posterior. |

Os dois modos são testáveis. O default não apaga o outro. Nenhum modo autoriza abrir STT só depois do stop. A captura já tem de estar aceitando frames em `ACTIVE_DUPLEX` antes do gesto (CMP-FD-02). Parar o TTS antes de encaminhar o primeiro frame ao STT falha CMP-FD-O13, qualquer que seja o modo.

## 2. TTS_PROVIDER

Estados: `IDLE`, `RESERVED`, `DISPATCHED`, `STREAMING`, `CANCEL_REQUESTED`, `CANCEL_CONFIRMED`, `CANCEL_UNCONFIRMED`, `COMPLETE`, `UNCERTAIN`.

| De | Evento | Para | Redispatch desta operation_ref |
|---|---|---|---|
| IDLE | `ReserveConversationalCapability` comprometido | RESERVED | ainda não houve dispatch; no máximo um |
| RESERVED | `DispatchOperation` system | DISPATCHED | proibido um segundo |
| DISPATCHED | primeiro chunk `generated_at_ns` | STREAMING | proibido |
| STREAMING | `is_final=true` da synthesize | COMPLETE | proibido |
| STREAMING ou DISPATCHED | `cancel` enviado | CANCEL_REQUESTED | proibido |
| CANCEL_REQUESTED | ACK `CONFIRMED` | CANCEL_CONFIRMED | proibido. Não cria operation nova |
| CANCEL_REQUESTED | ACK `UNCONFIRMED` ou timeout sem ACK | CANCEL_UNCONFIRMED | proibido |
| DISPATCHED ou STREAMING | timeout depois do dispatch, ou efeito desconhecido | UNCERTAIN | proibido |

`CANCEL_CONFIRMED` mapeia para `SPEECH_CANCELLED`. Não é `ProviderEffectProof`. Se não houve dispatch, não há reservation. Se houve dispatch, só uma prova conclusiva `NO_EFFECT` sem `RECEIPT` autoriza `ReleaseReservation`. Confirmação de cancel de áudio não é essa prova.

`CANCEL_UNCONFIRMED` e `UNCERTAIN` mapeiam para operation `RECONCILING` ou `BLOCKED_RECONCILIATION` conforme `receipt_query` (FDP-16A §8C). Reservation permanece `HELD`. A UI não mostra custo zero.

`COMPLETE` não liquida sozinho. Liquidação continua `RecordReceipt` com prova de `forge.provider_ingest`.

## 3. MODEL_PROVIDER

Mesmos estados, sem chunk de áudio. `conversation.respond` é outra operation, outro `invocation_id`, outra linha.

`USER_SPEECH_START` pode pedir cancel da geração do modelo **em curso**. Esse cancel é independente do cancel de TTS:

| Invoke | Cancel é | Se o ACK não chega |
|---|---|---|
| playback local | best-effort, sem ACK | playback já está `STOPPED`; nada a redespachar |
| TTS já despachada | exige ACK | `CANCEL_UNCONFIRMED`, sem redespacho, dinheiro incerto |
| modelo já despachado | exige ACK | idem |
| modelo ainda só `RESERVED`, sem dispatch | cancel antes de dispatch | `ReleaseReservation` **não** é automático; v1.7 só libera com `NO_EFFECT` conclusivo. Sem chamada observada, o caminho permitido é o da v0.3 §9 linha “antes do dispatch”: `RETRY_SAME_OPERATION` ou cancel interno da reservation **somente** se o comando system puder provar que não houve chamada. Este pacote não inventa essa prova. Se a prova não existe, a reservation fica `HELD` e o estado é `UNCERTAIN`. |

Fan-out paralelo de vários modelos pagos continua proibido (CMP-02 v0.3 §6). Interrupção não autoriza disparar o conselho inteiro.

## 4. LEDGER

Status legais, sem acréscimo: `RESERVED`, `DISPATCHED`, `SETTLED`, `RELEASED`, `DENIED`, `CANCELLED`, `RECONCILING`, `BLOCKED_RECONCILIATION`.

| Estado de TTS ou modelo | Estado de operation que pode coexistir | Movimento de dinheiro neste passo |
|---|---|---|
| RESERVED | RESERVED, reservation HELD | `reserved += estimate` já cometido; `spent` igual |
| DISPATCHED ou STREAMING | DISPATCHED | nenhum |
| CANCEL_CONFIRMED sem dispatch | RESERVED ainda, ou RELEASED só com prova | sem prova, nenhum |
| CANCEL_UNCONFIRMED ou UNCERTAIN | RECONCILING ou BLOCKED_RECONCILIATION | nenhum; HELD |
| COMPLETE com RECEIPT conclusivo | SETTLED via RecordReceipt system | um movimento |
| NO_EFFECT conclusivo e nenhum RECEIPT | RELEASED via ReleaseReservation system | um release |
| qualquer | DENIED antes da reserva | nenhum |

Célula não listada não é permissão. `conversation_router` não escreve estas transições.

## 5. Retry

A tabela da CMP-02 v0.3 §9 permanece. Resumo que este pacote não afrouxa:

| Situação | Ação | Chamada nova |
|---|---|---|
| Antes do dispatch | no máximo um dispatch da mesma operation | uma |
| DISPATCHED sem prova | `RECONCILIATION_REQUIRED` | zero |
| NO_EFFECT conclusivo | nova tentativa só com novo turno e novo `operation_ref`, se a pessoa pedir | uma, na chave nova |
| HELD / BLOCKED / prova inconclusiva | sem release, sem recibo fictício | zero |
| SETTLED | replay do resultado | zero |
| CANCEL_UNCONFIRMED | tratar como resultado desconhecido | zero |
| DUCK ou STOP_LOCAL | não são retry e não são release | zero |

Timeout de cancel de planejamento: `forge.conversation.cancel_ack_timeout_ms = 2000`. Não é SLO. Ao estourar, o estado vai a `CANCEL_UNCONFIRMED`, não a `CANCEL_CONFIRMED` e não a custo zero.
