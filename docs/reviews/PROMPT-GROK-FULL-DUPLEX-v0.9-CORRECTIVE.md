# PROMPT GROK — FULL-DUPLEX v0.9 CORRETIVO (Codex v0.8 FAIL)
Repositório: https://github.com/otavioegal/ia-os-forge-round5
SHA v0.8 auditado: 9fd88bb03e4cca4a1ee5126d5b595e028e2602b2
Parecer: docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.8-2026-10-15.md

Leia integralmente o parecer independente Codex v0.8, o pacote v0.8, v0.7, v0.6, v0.5, FDP-16A v1.7, decisões AQ e contratos citados. Crie exclusivamente docs/planning/conversational-full-duplex-v0.9/ de forma ADITIVA, sem alterar pastas anteriores, código operacional, banco, provider ou flags. NÃO declarar PASS ou executar BUILD-00.

1. FD07-08 PARTIAL + NEW-MEDIUM-07 OPEN: modelar forge.command_commit com command_digest, original_outcome_code, original_outcome_body e outcome_digest; replay retorna transport_status=200, replay=true, outcome original exato sem confundir código HTTP com outcome persistido. Demonstrar replay de outcome original não-200/409 e digest distinto, sem duplicar event_id/ledger. Especificar ordem de lookup em relação a validações mutáveis de sessão/receiver, sem bypass de autorização tenant. Criar fixtures negativas, invariantes e checker estático coerentes.

2. FD07-09 PARTIAL + NEW-MEDIUM-08 OPEN: manifest histórico verificável com base_sha e parent_sha, comparação efetiva dos blobs Git em AMBOS os commits, não booleans autorreferentes nem somente filesystem atual. Comparar path sets, sha256 por arquivo, incluir docs/planning/conversational-full-duplex/ v0.1 OU restringir explicitamente escopo alegado; registrar v0.5/v0.6 sem parecer independente e v0.7 com parecer. Não inventar hashes ou PASS. Se checker só inspecionar sem execução, declarar NOT RUN.

3. FD07-07 OPEN: SQL concorrência ON CONFLICT DO NOTHING, SELECT FOR UPDATE, monotonicidade e two-backend O92/O93 permanecem NOT RUN. Não simular corrida sequencial como prova PostgreSQL. Entregar protocolo de teste futuro com barreira real, ambas ordens, trios distintos, evidências de locks e rollback, sem executar migration ou PostgreSQL sem autorização do Founder. HIGH-03 permanece PARTIAL até evidência exigida.

4. FD07-05 CLOSED: preservar negativos, efeitos completos, n=-1, e incluir no harness de mutação peer_ack_high_water_before e expected_stage para cobrir alegação ampla.

5. FD07-06 CLOSED: preservar chave tenant (organization_id, project_id, session_id, ack_stream_id, receiver_participant_id), cross-tenant 404 opaco, receiver ausente, stream não alocado, high-water sem regressão, no ACK null pair bypass. NEW-MEDIUM-06 CLOSED DOCUMENTAL, migration NOT RUN.

6. Fortalecer schema fixture: tipos, UUID, proibição de extra keys, coerência participants/allocated_by_session/initial_keys; deixar claro que checker estático não prova produto.

7. LOW-01 OPEN BLOCKING DoR: owner pessoa PENDING, effort UNSTATED, DoR NOT MET. Não inventar responsável. Manter 9 AQ aprovadas, AQ-04/09/12 deferred, FDP14/15 pendentes, O84..O95 e oráculos anteriores NOT RUN, flag forge.conversation.delta.v4 desligada.

Entregue índice, change report, finding disposition por path:line, documentação e fixtures/checkers estáticos, consistency report, traceability, open questions. Publique SHA completo e parent como CANDIDATE FOR CODEX REVIEW. Solicite nova auditoria Codex independente read-only.
