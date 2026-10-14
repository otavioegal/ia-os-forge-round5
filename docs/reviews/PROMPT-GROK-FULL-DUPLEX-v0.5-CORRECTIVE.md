# PROMPT GROK — CORRETIVO FULL-DUPLEX v0.5
Repo: https://github.com/otavioegal/ia-os-forge-round5
SHA auditado: 90fc21c90402805959bab2fc4ae6b43dc758c66d
Parecer: docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.4-2026-10-14.md
Status: FAIL DOCUMENT-ONLY; sem BUILD-00.

Leia integralmente parecer, pacote v0.4, contratos v1.7 FDP-16A/FDP-15, CMP v0.3, ata e ADR AQ-07. Crie APENAS pasta aditiva docs/planning/conversational-full-duplex-v0.5/, sem alterar artefatos auditados. Não declare PASS nem feche findings unilateralmente.

PRIORIDADE 1 — NEW-HIGH-04 PARTIAL: a fórmula S+H-E+A<=session_slice_minor está aplicada a RecordReceipt mas NÃO a ApplyAuthorizedReconciliation. Aplique o mesmo controle a TODO comando que produz SETTLEMENT, sob lock Build-first, incluindo reconciliação manual PROVEN_RECEIPT. Se não couber: zero movimento, Reservation HELD, Operation BLOCKED_RECONCILIATION, autorização não consumida, pending_provider_cost SESSION_SLICE append-only. Defina correlação do pending com settlement terminal posterior sem update/delete, sem refund inventado. Oráculos para E40 A70 L50 root folgado, reconciliação autorizada, race AmendSessionSlice vs ApplyAuthorizedReconciliation, replay/crash/40001, prova tardia e sessão CLOSING.

PRIORIDADE 2 — NEW-HIGH-03 PARTIAL: migration tenant completa para Operation/Reservation. Colunas nullable -> backfill determinístico por join, contar e abortar órfãos -> UNIQUE(organization_id,project_id,id) em Operation -> FK composta Reservation -> Operation NOT VALID -> VALIDATE -> SET NOT NULL; índices e predicados tenant-compostos em lookup/ingest/replay; flag off até validação; 404 opaco e zero efeitos estrangeiros. Oráculos com dados preexistentes e IDs estrangeiros.

PRIORIDADE 3 — HIGH-03 PARTIAL: no envelope, ACK deve conter ack_stream_id ou ack_sequence_scope separado do stream_id do evento CONTROL. Defina high-water por session/acknowledged_stream/receiver, limites, ACK futuro, duplicado, regressivo, cross-stream e stream não alocado. Adicione autenticação do preâmbulo principal_ref vs principal autenticado, PREAMBLE_AUTH (ou CHANNEL_SCOPE explícito), rejeição sem abrir sessão/mic. Fixtures JSON positivas e negativas; sem downgrade para half-duplex.

PRIORIDADE 4 — NEW-MEDIUM-05 PARTIAL: verificador de digests deve exigir event_ids únicos em eventos, vetores únicos, bijeção exata entre conjuntos, todos vetores consumidos, object_pairs_hook que rejeite chaves JSON duplicadas, tipos e formato de sha256, canonical_byte_length e event_digest. Fixtures negativas para duplicata, vetor órfão, chave repetida, hash inválido. Checagem estática apenas, nunca declarar teste de produto.

PRIORIDADE 5 — NEW-MEDIUM-03 PARTIAL: corrigir amostra matemática de saturação AEC. Em i=1199 eco=-4000 e human=32000 => mic=28000, não 32767. Escolha i=1159 com eco positivo, human=32000 e mic=32767; preserve caso eco negativo, casos recuperáveis e irrecuperáveis de saturação e negativos de fala suprimida/eco preservado.

PRIORIDADE 6 — NEW-MEDIUM-06 PARTIAL: SQL executável do unique parcial em forge.task por (organization_id,project_id,session_id) WHERE execution_domain='CONVERSATION' AND session_status IN ('OPEN','CLOSING','ORPHAN_HELD'). Não misturar task.status com session_status. Validar duplicatas históricas antes de criar índice; 404 opaco cross-tenant.

PRIORIDADE 7 — NEW-MEDIUM-01 CLOSED: preservar replay antes CAS, esclarecer transport_status=200/replay=true/original_outcome_code/original_outcome_body.

LOW-01 continua OPEN BLOCKING DoR: pessoas PENDING, effort UNSTATED, DoR NOT MET até ato humano. Não invente nomes.

PRESERVAR findings CLOSED HIGH-01/02, NEW-HIGH-01/02, NEW-MEDIUM-01/02/04, MEDIUM-01..05; 9 AQs APPROVED, AQ-04/09/12 DEFERRED. FDP-14, FDP-15, baseline consolidation, BUILD-00 PENDING. Oráculos v1.7 (91), CMP (36), FD (52) NOT RUN; CMP-O-28 independente de CMP-FD-O28. Sem migration real, provider, deploy, credenciais, gastos, testes operacionais.

Entregáveis: índice/status, contratos financeiros/tenant/migration, mídia/handshake, fixture e checker, oráculos adversariais, lifecycle, segurança, rastreabilidade, disposition com path:line, consistency report, questões abertas. Publicar SHA completo como CANDIDATE FOR CODEX REVIEW e pedir auditoria Codex independente read-only.
