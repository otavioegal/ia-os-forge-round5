# PROMPT CORRETIVO GROK — FULL-DUPLEX v0.10
Repo: https://github.com/otavioegal/ia-os-forge-round5
SHA auditado v0.9: 422277f82efbc001140b5857095c4840e668e270
Parecer: docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.9-2026-10-15.md
VEREDITO: FAIL DOCUMENT-ONLY.

Leia integralmente parecer v0.9, pacote v0.9, baselines e governança. Produza SOMENTE pasta aditiva docs/planning/conversational-full-duplex-v0.10/; não altere v0.9 ou anteriores. Não execute migration, banco, provider, deploy, build, testes de produto ou gastos.

1) NEW-MEDIUM-09 OPEN: a cadeia parecer_chain v0.1..v0.8 do manifest precisa ser verificável contra arquivos reais nos commits corretos. Para cada parecer, verificar path, audited_sha, verdict e presença em base/parent com leitura de blobs Git, nunca aceitar apenas metadata declarada. Validar full_duplex_prompts_present_at_parent e ausentes, incluindo verificação de path sets e invariantes. Reportar precisamente ausências legítimas, não inventar pareceres v0.5/v0.6. Testes estáticos negativos para troca de SHA, verdict, path, omissão e prompts inventados. Se houver limitação por nomenclatura ou data, declarar explicitamente e tratar como NOT VERIFIED.

2) NEW-LOW-02 OPEN: schema fechado deve exigir TODOS os campos obrigatórios e proibir extras, tipos errados e UUID inválidos antes de processamento. Ausência de campo obrigatório retorna FAIL_SCHEMA determinístico, não KeyError/exception. Incluir mutações de remoção de cada campo obrigatório, além de mutações de valores; checar integridade de fixtures e evitar o checker virar única autoridade.

3) FD07-07 OPEN e HIGH-03 PARTIAL: preservar SQL de concorrência, lock/monotonicidade e especificação O92/O93 de dois backends/barreira real/ambas ordens/trios distintos. Estes continuam NOT RUN até autorização expressa. Não simular concorrência sequencial como PASS. Não tentar fechar HIGH-03 sem evidência real.

4) PRESERVAR CLOSED documental FD07-08, NEW-MEDIUM-07, FD07-09 (somente blobs planejamento), NEW-MEDIUM-08, FD07-05, FD07-06, FD07-01..04, NEW-MEDIUM-06. Preservar replay original outcome 422 com transport 200, tenant 404 antes lookup, ACK null-pair, n<0, high-water monotônico, ausência de ledger alternativo e zero movimentos nos erros.

5) LOW-01 OPEN BLOCKING DoR: owner pessoa PENDING, effort UNSTATED, DoR NOT MET. Não inventar responsáveis. Manter nove AQ APPROVED, AQ04/09/12 DEFERRED, FDP14/15 pendentes, forge.conversation.delta.v4 desligada, BUILD00 não autorizado.

Entregar índice, change report, matriz findings, normativas/fixtures/checkers de escopo estático, traceability, oráculos NOT RUN, consistency report e open questions. SHA completo, parent, candidato para nova auditoria Codex independente somente leitura. Não declarar PASS por execução de checker.
