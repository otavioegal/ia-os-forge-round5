# PROMPT CORRETIVO GROK — FULL-DUPLEX v0.13
Repo: https://github.com/otavioegal/ia-os-forge-round5
SHA v0.12 auditado: 346cd04ae90bf57f4594e1a4b4af0584961dd546
Parecer Codex: docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.12-2026-10-15.md
Veredito: FAIL DOCUMENT-ONLY. Leia o parecer INTEGRALMENTE antes de começar.

Crie SOMENTE pasta aditiva docs/planning/conversational-full-duplex-v0.13/, mantendo intactos todos os arquivos históricos. Sem BUILD-00, migrations, PostgreSQL, providers, deploy ou gastos.

CORREÇÃO OBRIGATÓRIA NEW-LOW-03 e FD11-NEW-01: a cobertura 480/480 e 2239/2239 da v0.12 era autoconsistente sobre catálogo incompleto. Não reutilize esses números como cobertura total. Inspecione schema e checker v0.12 linha a linha, corrija o universo de regras e evidências:
1. Implementar travessia recursiva genérica de TODAS as regras do schema, incluindo objetos inline, objetos referenciados, campos aninhados e cada ocorrência em fixtures/sintéticos; não usar apenas $ref ou chamadas manuais nest() por kind.
2. Incluir mutações de presença, tipo, mínimo de comprimento, UUID, extra key e elemento de array, com cobertura explícita de expected_original_outcome_body.error_code, body com chave extra, cada subcampo inline e todos os elementos setup, steps e initial_keys (substituir cada elemento por escalar e lista inválidos).
3. Para arrays de objetos, criar jobs ELEMENT_TYPE para CADA índice, substituindo o elemento por não objeto; cobrir campos aninhados dentro de cada índice.
4. O universo esperado de campos/regras/ocorrências deve vir de SEGUNDA travessia estrutural INDEPENDENTE do catálogo de jobs; comparar esperados x exercitados, registrar gaps por caminho e falhar em qualquer lacuna. Não usar o mesmo gerador para calcular numerador e denominador.
5. Rejeitar chaves JSON duplicadas durante parse de schema, fixtures, hosts sintéticos e manifest, com erros determinísticos. Acrescentar casos negativos específicos para duplicatas em cada classe de arquivo.
6. Mutações negativas devem provar rejeição na etapa de schema, antes de processamento ACK; erros FAIL_SCHEMA, FAIL_TYPE, FAIL_UUID, FAIL_EXTRA_KEY ou erro de duplicata explícito, sem crash. Não alegar cobertura de produto: product_input_exhaustive=false.
7. Gerar relatório quantitativo com paths/regras declaradas, caminhos aninhados, ocorrências, jobs executados e lacunas. Se não for possível provar completude, declarar PARTIAL, não PASS_FIXTURE_ONLY de cobertura total.
8. Remover/retificar alegações falsas da v0.12: uma mutação por campo, para cada objeto/campo, schema_rules=all_declared e cobertura independente 480/480, 2239/2239. Preserve registros históricos imutáveis e explique que os números anteriores eram incompletos.

GOVERNANÇA E GATES: parecer v0.2 intocado, chosen_verdict null, errata PENDING_HUMAN_APPROVAL, v0.2 NOT_VERIFIED, PARECER_CHAIN NOT_FULLY_VERIFIED. FD07-07 OPEN, HIGH-03 PARTIAL, LOW-01 OPEN BLOCKING DoR, owner PENDING, effort UNSTATED, DoR NOT MET. O92/O93 e O96–O99 NOT RUN. Flag forge.conversation.delta.v4 OFF. FDP-14, FDP-15 e baseline pendentes. Preserve todos findings CLOSED documental, ACK, replay, tenant isolation, zero movimento e integridade de blobs.

Entregar índice, normativas, fixtures, schema, checkers, coverage report, change report, matriz findings, traceability, oráculos, consistência e questões abertas. Checkers estáticos não equivalem a PASS global. Publique commit aditivo, SHA completo e parent, estado CANDIDATE FOR CODEX REVIEW. Solicite nova auditoria Codex independente read-only no SHA fixo.
