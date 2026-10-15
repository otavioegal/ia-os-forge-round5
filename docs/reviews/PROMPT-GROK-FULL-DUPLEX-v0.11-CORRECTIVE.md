# PROMPT CORRETIVO GROK — FULL-DUPLEX v0.11
Repositório: https://github.com/otavioegal/ia-os-forge-round5
SHA auditado v0.10: a5d7e8fc85cb5b5f0605937b43075ce1a0c19e08
Parecer: docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.10-2026-10-15.md
Veredito: FAIL DOCUMENT-ONLY.

Leia integralmente parecer v0.10, prompt presente e documentação v0.10. Trabalhe SOMENTE na pasta aditiva docs/planning/conversational-full-duplex-v0.11/; preserve v0.10 e históricos imutáveis. Não execute migrations, PostgreSQL, provider, build, deploy ou gastos.

A) NEW-MEDIUM-09 PARTIAL: parecer v0.2 contém vereditos distintos FAIL (cabeçalho) e FAIL — DOCUMENT-ONLY (fecho), inclusive duplicações. Não edite o parecer original, não escolha arbitrariamente uma string e não declare VERIFIED. Produza proposta documental de resolução por governança (errata aditiva com referências a blob/SHA, autoridade e aprovação humana pendente). Até aprovação, manter v0.2 NOT_VERIFIED e PARECER_CHAIN NOT_FULLY_VERIFIED. Verifique cada parecer por blob, SHA, path, veredito e existência nos commits pertinentes; preservar ausências legítimas v0.5/v0.6, listas completas de prompts presentes/ausentes. Campo bytes no manifest: comparar rigorosamente com comprimento real de cada blob Git ou remover o campo da nova versão; não deixar metadado não verificado.

B) NEW-LOW-02 PARTIAL e NEW-LOW-03 NEW OPEN: endurecer schema externo e check_fd_fx03_ack.py para exigir, ANTES da lógica de processamento, campos obrigatórios, chaves extras proibidas, UUIDs, tipos escalares e estruturas compostas. Cobrir explicitamente rollback_model, interleave, sequential_replay, replay_receiver_removed e replay_cross_tenant. Exigir cardinalidade mínima e tipos de elementos para setup, steps, commit_order e expected_steps. Para cada kind, criar mutações negativas de ausência E TIPO de TODOS os campos, inclusive aninhados; retornar deterministicamente FAIL_SCHEMA, FAIL_TYPE, FAIL_UUID ou FAIL_EXTRA_KEY sem exceções ou bypass para processamento semântico. Distinguir erros de schema de falhas de negócio e reportar casos limítrofes. Não confiar somente no checker autoral.

C) PRESERVAR FECHAMENTOS DOCUMENTAIS: FD07-01..06, FD07-08, FD07-09 no escopo blobs de planejamento, NEW-MEDIUM-07/08 e NEW-MEDIUM-06. Replay deve manter original_outcome_code/body/digest, transporte 200 vs outcome 422, 409 digest mismatch sem mutação, tenant 404 antes lookup, null-pair, ACK negativo, high-water monotônico e zero movimento em erro.

D) FD07-07 OPEN, HIGH-03 PARTIAL: PostgreSQL O92/O93 com dois backends/barreira/ambas ordens/trios distintos continuam NOT RUN; O96-O99 NOT RUN. LOW-01 OPEN BLOCKING DoR: owner pessoa PENDING, effort UNSTATED, DoR NOT MET. Não inventar pessoa nem promover PASS. forge.conversation.delta.v4 desligada; BUILD-00, migrations, provider e deploy não autorizados.

E) ENTREGÁVEIS: índice, normas/fixtures/checkers estáticos, relatório de mudanças, matriz findings, rastreabilidade, consistência, governança do v0.2 e lista explícita de oráculos NOT RUN. Checkers estáticos só podem declarar PASS_FIXTURE_ONLY ou resultado equivalente, nunca PASS global. Publique commit aditivo, informe SHA completo e parent, estado CANDIDATE FOR CODEX REVIEW, para nova auditoria independente somente leitura. Não reescreva nem force-push histórico.
