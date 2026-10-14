# CMP-FD-01 — Arquitetura suplementar para voz full-duplex

**Estado:** CANDIDATE FOR CODEX REVIEW; não implementado, não testado, não integrado à baseline. Fonte: ata de deliberação do Founder `docs/governance/ATA-FOUNDER-AQS-CONVERSATIONAL-2026-10-13.md`. Baseline v1.7 e CMP v0.3 intactos.

## Experiência obrigatória

Jarvis, todos os agentes conversacionais expostos no Forge e a Sala de Conselho permitem fala do humano DURANTE reprodução de áudio do agente, com entrada e saída simultâneas, interrupção e retomada natural. Half-duplex (mesmo com botão de interrupção) NÃO satisfaz o MVP. Agentes text-backed participam via camada de mídia STT incremental → agent/model → TTS incremental, desde que o áudio permaneça bidirecional e o usuário possa falar a qualquer momento da reprodução.

## Camadas

Tauri/React Universal Voice UI → canal bidirecional autenticado e escopado por projeto → Media Gateway/Session Sequencer → Policy/Consent/Data Classification → STT/TTS TOOL adapters + MODEL conversation.respond → Conversational Agent Router/Council Arbiter → Context Builder → Evidence/Audit + **mesmo ledger FDP-16A v1.7**. Não se cria quarta família de adapter, banco monetário paralelo ou uma engine de construção para falar.

## Contrato de mídia PROPOSTO: cmp.media.duplex.v1

Complementa `cmp.speech.v0` da v0.3 sem sobrescrevê-lo. Não escolher provider/SDK nem mudar contratos históricos antes de revisão independente e gates. Versão explicitamente negociada; sem downgrade silencioso para turn-taking.

Envelope em cada evento: contract_version, organization_id, project_id, session_id, stream_id, event_id, sequence monotônica, timestamp, participant_id, speaker_agent_id quando saída, media_encoding, data_classification, consent_ref, operation_ref quando houver efeito monetário. Validar escopo e versionamento fora do LLM, descartar mensagens duplicadas e impedir replay intersession.

Eventos e invariantes:
- `START_SESSION`: exige autenticação, consentimento explícito para microfone, classificação permitida e sessão ativa; liga indicador de captura apenas dentro da sessão.
- `INPUT_AUDIO_CHUNK` recebido mesmo durante `OUTPUT_AUDIO_CHUNK`. Input/output simultâneos são requisito verificável; buffers limitados, controle de eco, jitter, rede instável, timeouts e retomada segura.
- `STT_PARTIAL` nunca dispara tool nem fecha turno; `STT_FINAL` origina novo turno humano, ainda sujeito à política.
- `USER_SPEECH_START` durante fala do agente solicita duck/cancel da saída, dá prioridade ao humano e marca INTERRUPT_REQUESTED; `CANCEL_ACK` distingue CONFIRMED/UNCONFIRMED. Interrupção local não equivale a efeito externo cancelado nem a custo zero.
- `OUTPUT_AUDIO_CHUNK` é atribuído a agente/turno; a Sala registra divergências por agente e ata com turn_ids e fontes. Mídia bidirecional não autoriza fanout descontrolado de modelos pagos.
- `PAUSE_SESSION`, `STOP_SESSION`, `CONSENT_REVOKED` interrompem captura e egress; áudio bruto não armazenado por padrão; transcrição segue política definida da organização. No background e fora de sessão: mic DESLIGADO.
- `ERROR`: UNSUPPORTED_VERSION, BAD_AUDIO, CONSENT_REQUIRED, POLICY_DENIED, BUFFER_OVERFLOW, NETWORK_LOSS, PROVIDER_UNAVAILABLE, CANCEL_UNCONFIRMED, BUDGET_BLOCKED. Retry nunca ignora estado UNKNOWN/HELD ou gera novo dispatch indevido.

AQ-01 aprovada: `conversation_router` tem credencial/principal próprio e só reserva via gateway autorizado/mesma transação financeira da v1.7; nada de impersonar coding_engine. AQ-02 aprovada: Task-âncora por sessão, fora do DAG de build, task_id NOT NULL, sem deploy/terminal/vault. AQ-03 TOOL speech.*; conversation.respond MODEL. AQ-05 classes PUBLIC/INTERNAL/CONFIDENTIAL/RESTRICTED; conteúdo de projeto não é PUBLIC; CONFIDENTIAL e RESTRICTED bloqueados para providers speech externos. AQ-06 DO_NOT_STORE áudio bruto por default; transcrição por política com prazo/eliminação antes de produção. AQ-08 mic ligado somente em sessão expressamente consentida; captação concorrente durante essa sessão permite full-duplex; não escuta sempre ativa fora dela. AQ-10 spent + reserved <= limit, sem ledger paralelo, provider receipts só por forge.provider_ingest; uncertainty HELD/reconciliação. AQ-11 sem biometria; hard gates autenticados fora do canal de fala.

Codex conversacional voz = read-only; Codex formal = novo review_run_id e host-attested principal/runtime/processo/instância/credencial distintos do Builder, conforme CMP-O-28; chat não inicia review formal. Modelo nunca concede capability nem assina gate. AQ-04/09/12 diferíveis: provider não escolhido/deny-by-default; não compartilhar código/memória/sessão com Founder OS por suposição; sem prova ingerível, HELD sem receipt fictício.

## Integrações futuras necessárias

CMP-01 interface de voz simultânea, ativação/interrupção; CMP-02 novos eventos/transport; CMP-03 consentimento e proteção de egress inclusive interrupção; CMP-04 métricas e rastreabilidade de chunks, session, turn, provider, custos estimados versus comprovados; CMP-05 e matriz oráculos suplementares; FDP-14/15 ainda dependem de gate humano; recuperar FDP-11 se existir fora da árvore, caso contrário tratar UX como proposta nova. Não alterar v1.7 nem v0.3 em revisão dirigida.

**NÃO há medição de latência, custo, fornecedor escolhido, teste ou certificação de full-duplex.**
