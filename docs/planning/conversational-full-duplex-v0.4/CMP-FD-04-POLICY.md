# CMP-FD-04 v0.4 — Política e privacidade

**Estado:** PROPOSTA. Não é PASS.
**MEDIUM-02 e MEDIUM-03** foram fechados pelo Codex na v0.3. As regras centrais abaixo são as mesmas. O autor não as reabre.
**NEW-MEDIUM-04:** `consent_stop_deadline_ns` não é campo de `observation`.

## Consentimento

`consent_grant_epoch` muda em grant e revogação. `capture_generation` muda em grant, revogação, pause, stop, background, crash e resume explícito. Os dois começam em 0. Microfone fechado.

Chunk só é aceito se os dois inteiros batem com os correntes. Senão `422 CONSENT_EPOCH_STALE`. A comparação no gateway é atômica: generation N não passa depois que o contador já é N+1.

Ordem do corte: incrementar o contador e pôr `mic_open=false` antes de aceitar chunk novo; descartar buffer local ainda não encaminhado; exigir `CAPTURE_CLOSED`; não “desenviar” byte que já tenha `stt_forward_at_ns`; selar a invoke; não redespachar; dinheiro incerto continua HELD.

Background e crash não reabrem a generation anterior. Reconnect não aceita chunk velho.

Os quatro pontos continuam distintos: DEVICE, TRANSPORT, STT, BUFFER.

`forge.conversation.consent_stop_deadline_ns` é chave de configuração. O aceite é null, `PENDING CALIBRATION`. Não é membro de `observation`. O oráculo de corte não usa milissegundo. Usa microfone fechado, zero chunk novo e buffer pós-corte vazio. Evento que traga esse nome falha O48.

## Trust

A fonte é o registry lido pela Policy Service. Divergência com o auto-relato do adapter: `403 TRUST_BOUNDARY_MISMATCH`, sem egress. Cada egress de STT, TTS, modelo e fallback é rechecado. Default de conteúdo de projeto: `INTERNAL`, não `PUBLIC`. CONFIDENTIAL e RESTRICTED não saem para speech externo. AQ-04 não escolhe fornecedor.

## O que a voz não faz

Fala não passa hard gate e não é biometria. Codex de sala é `CODEX_READ_ONLY`. Review formal continua CMP-O-28, NOT RUN. AQ-09 e AQ-12 continuam não decididas: sem Founder OS implícito e sem recibo fictício.
