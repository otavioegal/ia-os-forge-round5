# CMP-FD-02 — 4 histórias e 12 oráculos aditivos

**Status:** DRAFT / NOT RUN; evidence ABSENT; no software tests performed. Não renumera nem altera as 13 histórias e 36 oráculos CMP v0.3 (NOT RUN), nem a matriz v1.7 (91 oráculos).

Histórias: **CMP-FD-S01** interação duplex universal com agentes text-backed; **CMP-FD-S02** interrupção natural com cancelamento e preservação de custos; **CMP-FD-S03** Conselho conversacional com identidade e prioridade ao humano; **CMP-FD-S04** mic consentido, retenção mínima, classificação e ledger único. Todas requerem owner/effort e DoR operacional futuro.

| Oráculo | Fixture e passos futuros | PASS exigido | FAIL |
|---|---|---|---|
| CMP-FD-O01 | TTS de agente em andamento; usuário começa a falar no mesmo stream | STT recebe entrada ANTES da saída terminar, áudio duplex, turno identificado | STT bloqueado até acabar TTS |
| CMP-FD-O02 | Agente text-backed sem áudio nativo e speech gateway | entrada/saída concorrentes no universal composer | downgrade obrigatório a turn-taking |
| CMP-FD-O03 | USER_SPEECH_START durante provider response; CANCEL_ACK UNCONFIRMED | playback cessa, contexto preservado, custo ainda incerto | marcar provider NO_EFFECT/zero cost sem proof |
| CMP-FD-O04 | Conselho com Arquiteto/Codex conversacional + divergência + intervenção humana | speaker_id, turn ids, intervenção imediata e ata com divergência | falso consenso, speaker ausente ou review formal iniciado |
| CMP-FD-O05 | Consent GRANTED depois REVOKED no meio do stream | encerramento de captura/egress e chunk tardio descartado | gravação após revogação |
| CMP-FD-O06 | Sessão não iniciada, app background e microfone da máquina ativo | zero captura/STT pelo Forge; indicador desligado | escuta fora da sessão |
| CMP-FD-O07 | Entrada CONFIDENTIAL, speech provider externo e nenhum adapter local disponível | egress negado, texto degradado, capacidade duplex marcada indisponível | envio de dado sensível |
| CMP-FD-O08 | reconnect/duplicated stream event, dispatch provider incerto e HELD | dedupe event/operation, nenhuma segunda reserva/chamada, reconcile | segundo débito ou redispatch |
| CMP-FD-O09 | fala “aprovo” + pedido deploy durante stream | requer preview/hard gate autenticado sem efeito externo automático | ferramenta privilegiada executada por voz |
| CMP-FD-O10 | troca de interlocutor/projeto durante sessão | novo context pack escopado, sem tool grant herdado | vazamento cross-tenant |
| CMP-FD-O11 | somente adaptador half-duplex oferece voz | capability UNSUPPORTED, não marca MVP pronto | declarar full-duplex PASS com turn-taking |
| CMP-FD-O12 | sala com múltiplos providers/cancel não confirmado + auditor Codex participante | custo rastreável session/turn/provider, reviewer formal isolado host-attested CMP-O-28 | custo confirmado sem proof ou auditor formal reutiliza estado Builder |

Todos os casos exigem, na execução futura, fixture materializada, passos, PASS/FAIL, id de run, commit, host/policy version, owner, environment e artefato de evidência. **Hoje todos NOT RUN e evidence ABSENT.** Não confundir este protocolo de teste com aprovação do projeto nem autorização BUILD-00.
