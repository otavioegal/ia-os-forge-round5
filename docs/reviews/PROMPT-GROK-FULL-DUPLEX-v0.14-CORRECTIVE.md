# PROMPT CORRETIVO GROK — FULL DUPLEX v0.14 (CONDICIONAL)

**Repositório:** otavioegal/ia-os-forge-round5
**SHA auditado:** c7b08dc2a0127557293346ebd53e4ff43722683e
**Parecer Codex obrigatório:** docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.13-2026-10-15.md
**Veredito:** PASS WITH CONDITIONS DOCUMENT-ONLY; estado CANDIDATE, NÃO PASS produto/operacional.

## Mandato
Leia integralmente o parecer independente, os 19 arquivos docs/planning/conversational-full-duplex-v0.13, v0.12, v0.11, os contratos v0.5–v0.10 pertinentes, FDP-16A v1.7, CMP v0.3, ata e gates Founder. Preserve *todos* os arquivos anteriores como imutáveis. Trabalhe SOMENTE em novo diretório aditivo docs/planning/conversational-full-duplex-v0.14/. Não execute migration, PostgreSQL, backend, provider, deploy, gastos ou BUILD-00; não ative forge.conversation.delta.v4. Não declare PASS de produto, não altere pareceres e não encerre findings sem auditoria Codex independente.

## C1 — NEW-GOV-01 OPEN/MEDIUM: golden semântico independente
O Codex confirmou melhoria estrutural dos três defects da v0.12, mas a enumeração expected_schema_rules, expected_occurrences, stack_jobs e o validador compartilham a DSL, TYPE_WRONG e sufixos. Um bug espelhado pode preservar gap=0. Crie catálogo/golden externo versionado e independente do algoritmo auditado, com path, tipo de constraint, valor normativo esperado, schema digest, fixture digests e proveniência da decisão. Uma fonte de verdade semântica humana/autorizada deve ser separada de simulação/fixtures. Se a DSL é normativamente autoral e não existe golden ratificado, NÃO invente aprovação humana: declare PENDING HUMAN APPROVAL. Não use "golden" gerado pelo próprio checker como prova independente. Deixe claro que o catálogo comprova apenas os contratos incluídos, não o produto inteiro.

## C2 — schema DSL fechado e negativo de unknown keyword
Adicionar validador do próprio schema DSL de objetos/fields, tipos, ref, required, allowed, nullable, const, minLength, minItems, sha256, groups, same_length, items, de forma que keywords desconhecidos sejam rejeitados com código específico; rejeitar chaves JSON duplicadas em todos arquivos JSON de entrada. Respeitar o domínio efetivo da DSL, não inventar allOf/oneOf/$ref padrão que o schema não declara. Negative fixture: injetar keyword desconhecido e garantir exit != 0. Verificar coercion bool vs int, objetos inline, nested arrays, ambos sinais de nullable, refs resolúveis e constraints que mudam sentido sem mudar número de regras.

## C3 — Contraprovas sem alteração de cardinalidade
Casos adversariais com oracle/golden EXTERNO para: (i) alterar const mantendo valor em fixture; (ii) mudar minItems dentro do intervalo permitido pela fixture; (iii) minLength; (iv) trocar ref por outro alvo compatível; (v) trocar campos required/optional em compensação; (vi) editar valor esperado e modelo local simultaneamente. Exigir que cada alteração normativa sem autorização seja identificada, embora 508 e 2443 permaneçam iguais. Critérios: fail explícito com caminho/regra/digest divergente. Provar que checker pode detectar alteração em um só lado e definir o que NÃO detectará se mesmo autor editar todos lados.

## C4 — reproducibilidade e evidência 508/2443
Anexar processo reproduzível em ambiente de leitura segura (sem escrita no checkout, PYTHONDONTWRITEBYTECODE=1 / python -B) para ambos os checkers. Registrar SHA, Python version, stdout completo, stderr, exit code e hashes de quatro JSONs e dois scripts; nunca reportar execução se a política bloquear como ocorreu no Codex. Publicar em docs/planning/conversational-full-duplex-v0.14/ um manifest machine-readable com os 508 IDs de regras e os 2443 IDs de ocorrência, seus paths/indexes, chaves de identidade e seus digests, gerado e comparado com enumeração independente. Não deixar totais sem lista auditável; qualquer número novo deve ser justificado por diff e nova contagem, não forçar 508/2443 artificialmente. FULL_PRODUCT_COVERAGE continua FALSE; manter PASS_FIXTURE_ONLY mesmo que checagem estática passe.

## C5 — Findings e governança
Preservar como CLOSED apenas documental/estático FD12-NEW-01/02/03 (os três defects focalizados); FD11-NEW-01 PARTIAL e NEW-LOW-03 PARTIAL até prova quantitativa e semântica; NEW-GOV-01 OPEN até golden independente e gate humano; NEW-MEDIUM-09 v0.2 NOT_VERIFIED/chosen_verdict null e errata pendente; FD07-07 HIGH OPEN pois O92/O93 PostgreSQL NOT RUN; HIGH-03 HIGH PARTIAL; LOW-01 OPEN BLOCKING DoR com pessoa PENDING/effort UNSTATED/DoR NOT MET. Outros previously CLOSED sem regressão. Preservar nove AQs APPROVED e AQ-04/09/12 DEFERRED. O01–O99, 91 FDP-16A, 36 CMP-O NOT RUN. FDP-14/FDP-15 e baseline pending. Nenhum build ou alteração de flag.

## Entregáveis e submissão
Novo CMP-FD-00-INDEX, contrato de cobertura/golden e fonte normativa, manifesto IDs e hashes, script(s) somente estático(s), fixtures negativas não destrutivas, oráculos planejados NOT RUN, relatório de mudança, finding disposition path:line, traceability, consistency, status/governança, cadeia histórica, questões abertas. Se não houver possibilidade de golden independente por falta de decisão humana, registrar blocker em vez de simular independência. Commit somente arquivos novos na v0.14; publicar SHA completo e pedir outra auditoria Codex em clone read-only fixado nesse SHA. Publicar como CANDIDATE FOR CODEX REVIEW, não PASS.
