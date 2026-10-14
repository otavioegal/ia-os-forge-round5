# PROMPT OFICIAL GROK — Correções CMP Full-Duplex após FAIL documental Codex

**Repositório:** `https://github.com/otavioegal/ia-os-forge-round5`
**SHA auditado (imutável):** `97ee817ca8262b3a0bae996c510b935435b2e575`
**Parecer independente:** `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.1-2026-10-13.md` — FAIL DOCUMENT-ONLY.
**Missão:** corrigir o delta full-duplex com contrato e oráculos conclusivos. A ata das nove decisões AQ do Founder está aprovada e NÃO deve ser refeita, relativizada ou reaberta. Status de entrega CANDIDATE FOR CODEX REVIEW, não PASS.

## Regras obrigatórias

Leia integralmente parecer Codex, ata Founder, ADR AQ-07, especificação full-duplex e CMP v0.3, e normativos FDP-16A v1.7, FDP-15 histórica. Não altere os pacotes/pareceres auditados; coloque **versão corretiva aditiva** em `docs/planning/conversational-full-duplex-v0.2/`. Nenhum build, provedor real, gasto, staging, contratação ou mudança em produção. Preserve 91 oráculos v1.7, 36 CMP-O v0.3, 12 CMP-FD-O da versão candidata, todos NOT RUN; prefixe novos IDs sem colisão. Não autodeclare fechamento de finding.

## HIGH-01 — integração financeira real e Task-âncora
O v1.7 tem actor_class fechado e `InvokeCapability` apenas `coding_engine via gateway`; Task.build_id NOT NULL e Operation.task_id NOT NULL. Não basta declarar `conversation_router`. Proponha explicitamente DELTA normativo compatível (sem editar contratos v1.7 históricos): enum/actor, comando autorizável novo para conversation_router sem impersonação, request/response/errors, authorizer e capability guards fora do LLM, idempotency/op_ref, mesmo ledger e lock order, receipts só por forge.provider_ingest, HELD/CONFLICT/reconciliação. Defina a modelagem válida de Task-âncora por sessão que satisfaz build_id NOT NULL ou delta justificado da FK/constraint e separação efetiva do DAG, lifecycle, cardinalidade, orphan cleanup e invariantes proibindo deploy/terminal/vault. Trace condições de migration/backward compatibility/rollback. Oráculos negativos: bypass, ator indevido, missing build_id, segunda reserva, conflated Task.

## HIGH-02 — provar full-duplex real
Monte fixture determinística com relógio monotônico confiável, dois streams instrumentados (captura→gateway→STT e TTS→gateway→playback), intervalos sobrepostos [input_capture_start,input_capture_end] e [output_playback_start,output_playback_end], chunks em ambos os sentidos durante a interseção, e playback mantido depois do primeiro input chunk. Distinga áudio gerado, recebido e reproduzido. FAIL se STT só começar depois de pause/stop TTS, mesmo que o input ocorra antes de um final lógico. Adicione contadores, timestamps, tolerância e observabilidade do caminho completo. Não exigir SLA inventado: métricas/valores calibráveis separados de fatos medidos.

## HIGH-03 — contrato implementável e compatível
Schema tipado e versionado para `cmp.media.duplex.v1`: payload bytes/ref, hash/duração/size, turn_id, invocation_id, direction, MIME/codec/encoding/sample_rate/channels, stream end/final, idempotência, sequence scope/window/acks, session states/transitions, version handshake, backpressure, jitter/reorder/gaps, per-stream auth, transport binding, timeouts/error enums. Faça crosswalk completo de cada evento com `cmp.speech.v0`: PARTIAL/FINAL, TTS chunks, cancel, event IDs, ledger operation_ref. Defina local pipeline e provider duplex nativo com semântica igual no contrato.

## MEDIUMs
- Separar state machines LOCAL_PLAYBACK / TTS_PROVIDER / MODEL_PROVIDER / LEDGER, duck versus stop versus cancel, ACK confirmed/unconfirmed, retries sem redespacho incerto, custos de cancelamento e proofs.
- Consent epoch/generation para cada frame, transições atômicas revoke/background/crash/reconnect, descarte de buffers/chunks antigos, provider bytes in-flight e ACK da paralisação, timeout de corte.
- Trust boundary de providers validado por host/policy e não por autodeclaração de adapter, reautorizar em todo egress (STT/TTS/model/fallback), matriz PUBLIC/INTERNAL/CONFIDENTIAL/RESTRICTED e troca de projeto.
- Identidade/proveniência: turn_id, speaker_agent_id, source_turn_ids, evidence_refs, FACT/INFERENCE/SUGGESTION/ABSENCE, diálogo Codex read-only, ata e divergência; preserve CMP-O-28 integralmente e referencie-o, não o substitua.
- Métricas: voz → STT_PARTIAL/FINAL, STT_FINAL → token, token → primeiro áudio, user interruption → stop/duck, jitter/loss/underrun; percentis/cenários de rede, thresholds só PROPOSED/PENDING CALIBRATION sem SLAs fictícios.
- Completar histórias, owners PENDING, schemas fixtures e oráculos com eventos exatos, antes/depois, PASS/FAIL adversarial, future evidence ABSENT e NOT RUN. Não trate resumos de cenário como testes executados.

## Entregáveis e gates
Produza índice, contrato FDP-16A/FDP-15 proposto, lifecycle e schemas, policy/security/privacy, UX full-duplex, observability, story/oracle matrix, traceability, change report, finding closure, open questions, consistency report. Identifique decisões humanas AQs 01/02/03/05/06/07/08/10/11 como APPROVED pelo Founder; AQ-04/09/12 como DEFERRED/UNDECIDED. FDP-14, FDP-15, baseline consolidation e BUILD-00 continuam PENDING. Publique commit e SHA no GitHub e peça auditoria Codex independente read-only. NÃO chame PASS por conta própria.
