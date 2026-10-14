# CMP-FD-03 v0.4 — Lifecycle

**Estado:** PROPOSTA. Não executada. Não é PASS.
**MEDIUM-01** foi fechado pelo Codex. Esta página não mistura duck, stop e cancel, e não cria status monetário novo.

`LOCAL_PLAYBACK`: `IDLE`, `PLAYING`, `DUCKED`, `STOPPED`. `STOP_LOCAL` não espera ACK e não prova cancel. `DUCK` não é cancel e não é o predicado de full-duplex. O default de interrupção é `STOP_PLAYBACK`: stop local e `cancel` da invoke TTS. A captura já está aberta antes desse gesto. Parar o TTS antes do primeiro `stt_forward_at_ns` continua falhando O13.

`TTS_PROVIDER` e `MODEL_PROVIDER`: `RESERVED`, `DISPATCHED`, `STREAMING`, `CANCEL_REQUESTED`, `CANCEL_CONFIRMED`, `CANCEL_UNCONFIRMED`, `COMPLETE`, `UNCERTAIN`. `UNCONFIRMED` e `UNCERTAIN` não redespacham. Reservation fica HELD sem prova. Cancel confirmado não é `ProviderEffectProof`.

Ledger: só os status da v1.7. Settlement conversacional adicional está em CMP-FD-01 v0.4. Ele não autoriza release sem `NO_EFFECT`, não autoriza segundo movimento e não trata `SESSION_SLICE_EXCEEDED` como custo zero.

Retry segue a tabela da CMP-02 do conversational-mvp-v0.3, seção 9. Comando já cometido obedece a ordem replay-antes-do-CAS desta v0.4.
