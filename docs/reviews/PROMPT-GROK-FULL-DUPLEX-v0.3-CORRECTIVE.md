# PROMPT OFICIAL PARA GROK — FULL-DUPLEX v0.3 — Correção após auditoria Codex v0.2

**Repositório:** https://github.com/otavioegal/ia-os-forge-round5
**SHA auditado v0.2:** `18aa352e7bf987aa3a2550b2e2b3251ce71c1f7d`
**Parecer independente:** `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.2-2026-10-13.md`
**Veredito:** **FAIL DOCUMENT-ONLY**, sem teste de software. NÃO autoriza BUILD-00.

## Missão

Leia integralmente o parecer Codex v0.2, os 13 arquivos `docs/planning/conversational-full-duplex-v0.2/`, o parecer v0.1, a ata de decisões do Founder, ADR AQ-07, FDP-16A v1.7 e FDP-15 histórico. Corrija os findings na **nova pasta aditiva** `docs/planning/conversational-full-duplex-v0.3/`. Preserve integralmente v1.7, CMP v0.3, full-duplex v0.1/v0.2, decisões humanas e pareceres. Não altere arquivos auditados nem declare finding fechado por conta própria. A v0.3 será apenas CANDIDATE FOR CODEX REVIEW.

**Nove AQ aprovadas (não reabrir):** AQ-01, AQ-02, AQ-03, AQ-05, AQ-06, AQ-07, AQ-08, AQ-10, AQ-11. **AQ-04, AQ-09, AQ-12** continuam diferíveis e não decididas. Full-duplex natural é obrigatório desde o MVP para Jarvis, todos os agentes conversacionais e Conselho Técnico. FDP-14/FDP-15, baseline consolidation e BUILD-00 continuam PENDING.

## Findings anteriores ainda PARTIAL — todos devem ser resolvidos

### HIGH-01 — reserva financeira e Task-âncora
- **Lock order:** `CMP-FD-01-LEDGER-DELTA.md:75` permite ler headroom/stop_latch antes do lock descrito em `:77-84`. Escreva **uma transação normativa ordenada**: validação estática de identidade/escopo, resolução de Build e Task, lock **Build FOR UPDATE primeiro**, só então ler contadores, headroom, stop_latch, reconciliação, dedupe e decidir reserva, locks Operation → Reservation → ManualReconciliation na ordem v1.7, commit/outbox/audit. Nenhum estado financeiro lido antes do lock. Inclua dois comandos concorrentes distintos tentando gastar o último saldo e oráculo de serialização.
- **Teto único:** `OpenConversationalAnchor` recebe `budget_limit_minor` do cliente e copia ao Build sem teto pai; abrir N sessões pode multiplicar orçamento. Proíba teto autodeclarado. Derive sub-limite da política/autorização humana autenticada e faça a soma de todos os Builds-âncora obedecer **um único teto superior compartilhado** com locking e invariantes. Diferencie autorização do gasto, limite por sessão e limite total por projeto/org. Inclua fixtures A/B simultâneas que tentam superar limite agregado; não invente nova moeda ou segundo ledger.
- **Isolamento:** predicados transacionais de igualdade org/project/canal/session/Build/Task/Operation/Reservation e FK composta ou checks equivalentes. Negar IDs válidos de outra organização/projeto sem vazar existência, sem Operation/Reservation nem contadores.
- **Rollback/migração:** enum/check constraints, consumer downgrade, SESSION_CLOSED, FKs, audit/outbox, rollback parcial em passos 1–9, proof/reconciliation e impossibilidade de apagar ledger; condições verificáveis para rollback seguro. Nenhuma migration real.
- Preserve `conversation_router` com comando próprio, sem impersonar `coding_engine`, mesmo `forge.provider_ingest`, Task.build_id NOT NULL em Build CONVERSATIONAL_ANCHOR fora do DAG, sem deploy/terminal/vault.

### HIGH-02 — full-duplex real
- Preserve a fixture de overlap físico (G1 reproduzido enquanto input é capturado/encaminhado ao STT; sem pause-before-STT) e negativos existentes.
- Os timestamps `generated_at_ns`, `received_at_ns`, `reproduced_at_ns`, `captured_at_ns`, `gateway_accepted_at_ns`, `stt_forward_at_ns` devem existir **no schema tipado** com origem do relógio, processo observador, correlação, nullability por event_type e consistência com as fixtures. `CMP-FD-02:36` rejeita campos desconhecidos; não basta defini-los em prosa `:153-173`.
- Refazer CMP-FD-O28 de eco/VAD: entrada composta de referência playback + fala humana simultânea + eco, critérios independentes de classificação, false positive/negative, teste negativo de descarte da fala humana. Não aceitar `echo=true` como premissa infalível.
- Definir oráculos que possam ser executados e que falhem se houver apenas half-duplex com barge-in.

### HIGH-03 — schema implementável
- Substituir descrição narrativa por **discriminated union** versionada por `event_type` de `cmp.media.duplex.v1`, com todos os payloads e campos necessários: `transcript_state`, `cancel_state`, `discontinuity`, `provider_id`, `model_id`, payload de ERROR e associação `invocation_id`, PLAYBACK_SPAN begin/end, timestamps e conteúdo/encoding/hash.
- `HELLO`/`HELLO_ACK` precisam de schema próprio pré-handshake e binding ao canal; `CONTROL` requer stream_id, sequence_scope, ack/replay e dedupe inequívocos.
- Definir digest canônico de evento e tratamento do mesmo `event_id` com payload divergente; idempotência e replay com outcome; compatibilidade `cmp.speech.v0` campo a campo (PARTIAL/FINAL/TTS/cancel/erros/custos).
- Sem downgrade silencioso, sem dados externos classificados, sem provider escolhido.

## NOVOS findings HIGH

1. **NEW-HIGH-01 — orçamento multiplicável:** impedir criação de sessão A e B com limites X independentes que somam 2X. Autoridade do teto superior, lock e oráculo agregado obrigatórios.
2. **NEW-HIGH-02 — headroom antes do lock:** não basta constraint; dois comandos distintos concorrentes precisam ser serializados por Build/autoridade do orçamento antes da decisão.
3. **NEW-HIGH-03 — cross-tenant:** testes adversariais org A / project A / Task ou Build org B, com zero side effect e sem vazamento de existência.

## Novos MEDIUM

- **NEW-MEDIUM-01:** `expected_version` hoje nullable embora obrigatório para Task existente (`CMP-FD-01:68`); tornar obrigatório, especificar agregado e CAS, `409 VERSION_CONFLICT`, dedupe/replay/efeito em mismatch.
- **NEW-MEDIUM-02:** campos da fixture rejeitados pelo schema fechado. Resolver em tabela tipada, não somente comentário.
- **NEW-MEDIUM-03:** teste de eco pressupõe `echo=true`; criar sinal composto e medir preservação de fala humana.

## Estado dos demais findings

- **MEDIUM-01/02/03/04/05:** Codex declarou CLOSED documentalmente na v0.2. Preserve invariantes; não reabra sem regressão objetiva.
- **LOW-01:** PARTIAL porque sete histórias permanecem com owner PENDING, effort UNSTATED, DoR NOT MET. Não finja owner ou prontidão. Proponha responsabilidade por papel e processo de atribuição antes de DoR; marque status PENDING honestamente. Fixture e critérios já melhoraram.
- Preserve CMP-O-28 e sua independência host-attested, não substitua por CMP-FD-O28. Todas as 91 v1.7, 36 CMP-O e 34 CMP-FD-O permanecem NOT RUN; novos oráculos também NOT RUN.

## Entregáveis

Crie v0.3 aditiva com índice/status, contratos normativos de ledger e autorização, budget authority agregado, tenant scope, media event schemas, version/crosswalk, lifecycle, security/privacy, UX, observability, fixtures adversariais, matriz stories/oracles, rastreabilidade, finding disposition, migration/rollback, consistency report e questões abertas. Faça verificações estáticas de consistência documental sem declarar testes de software. Diferencie findings anteriores e novos, evidência path:line, e riscos residuais. Preserve documentação histórica e deliberações humanas.

Publique commit no GitHub e informe SHA. **Não declare PASS, não execute software, não use provider pago, não faça deploy, não inicie BUILD-00.** Solicite Codex independente read-only sobre SHA imutável.
