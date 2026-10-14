# CMP-FD-04 v0.5 — Política e privacidade

**Estado:** PROPOSTA. Não é PASS.
**MEDIUM-02 e MEDIUM-03** foram fechados pelo Codex na v0.3. O autor não os reabre.
**NEW-MEDIUM-04** foi fechado na v0.4. `consent_stop_deadline_ns` não é campo de `observation`.

## Consentimento

`consent_grant_epoch` muda em grant e revogação. `capture_generation` muda em grant, revogação, pause, stop, background, crash e resume explícito. Os dois começam em 0. Microfone fechado.

Chunk só é aceito se os dois inteiros batem com os correntes. Senão `422 CONSENT_EPOCH_STALE`. A comparação no gateway é atômica.

Ordem do corte: incrementar o contador e pôr `mic_open=false` antes de aceitar chunk novo; descartar buffer local ainda não encaminhado; exigir `CAPTURE_CLOSED`; não “desenviar” byte que já tenha `stt_forward_at_ns`; selar a invoke; não redespachar; dinheiro incerto continua HELD.

`forge.conversation.consent_stop_deadline_ns` é chave de configuração. O aceite é null, `PENDING CALIBRATION`. Não é membro de `observation`. Evento que traga esse nome falha O48.

## Preâmbulo

O principal autenticado do canal é comparado com `HELLO.principal_ref` em CMP-FD-02 v0.5. Divergência: `PREAMBLE_AUTH`, zero efeito, sem half-duplex. Isso não substitui o corte de consentimento e não abre o microfone.

## Trust

A fonte é o registry lido pela Policy Service. Divergência com o auto-relato do adapter: `403 TRUST_BOUNDARY_MISMATCH`, sem egress. Default de conteúdo de projeto: `INTERNAL`. CONFIDENTIAL e RESTRICTED não saem para speech externo. AQ-04 não escolhe fornecedor.

## O que a voz não faz

Fala não passa hard gate e não é biometria. Codex de sala é `CODEX_READ_ONLY`. Review formal continua CMP-O-28, NOT RUN. AQ-09 e AQ-12 continuam não decididas.
