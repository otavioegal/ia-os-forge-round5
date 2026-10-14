# CMP-FD-03 v0.5 — Lifecycle

**Estado:** PROPOSTA. Não executada. Não é PASS.
**MEDIUM-01** foi fechado pelo Codex. Esta página não mistura duck, stop e cancel, e não cria status monetário novo.

`LOCAL_PLAYBACK`: `IDLE`, `PLAYING`, `DUCKED`, `STOPPED`. `STOP_LOCAL` não espera ACK e não prova cancel. `DUCK` não é cancel e não é o predicado de full-duplex. O default de interrupção é `STOP_PLAYBACK`. A captura já está aberta antes desse gesto. Parar o TTS antes do primeiro `stt_forward_at_ns` continua falhando O13.

`TTS_PROVIDER` e `MODEL_PROVIDER`: `RESERVED`, `DISPATCHED`, `STREAMING`, `CANCEL_REQUESTED`, `CANCEL_CONFIRMED`, `CANCEL_UNCONFIRMED`, `COMPLETE`, `UNCERTAIN`. `UNCONFIRMED` e `UNCERTAIN` não redespacham. Reservation fica HELD sem prova. Cancel confirmado não é `ProviderEffectProof`.

Ledger: só os status da v1.7. O settlement conversacional, inclusive `ApplyAuthorizedReconciliation`, está em CMP-FD-01 v0.5. `SESSION_SLICE_EXCEEDED` não é custo zero. Fechar a sessão não liquida. `session_status` `CLOSING` ou `ORPHAN_HELD` não é `task.status`.

Retry de comando já cometido obedece a ordem replay-antes-do-CAS e a separação `transport_status` / `original_outcome_code` de CMP-FD-01 v0.5.
