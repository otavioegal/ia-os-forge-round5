# IA OS Forge — Prompt oficial Grok — CMP v0.3, fechamento HIGH-01

**SHA auditado v0.2:** `99474da514419a26ac8471c50c33697ade2a1cde`.
**Parecer independente:** `docs/reviews/PARECER-CODEX-CMP-v0.2-2026-10-13.md`
**Estado:** PASS WITH CONDITIONS do delta, 4/5 findings fechados. Não equivale à aprovação Founder.
**Objetivo:** EMENDA DOCUMENTAL FOCAL CMP v0.3 — CANDIDATE FOR CODEX REVIEW.

Grok, leia INTEGRALMENTE o parecer independente Codex CMP v0.2, os contratos `CMP-03-SECURITY-PRIVACY-AND-REVIEW-INDEPENDENCE.md` e `CMP-02-SYSTEM-ARCHITECTURE.md`, a história correspondente e `CMP-O-28` da v0.2. Corrija exclusivamente o HIGH-01 residual do oráculo. Os MEDIUM-01/02/03 e LOW-01 estão FECHADOS: não os reabra.

**Falha específica:** o oráculo CMP-O-28 permite que o revisor formal reutilize PROCESSO/RUNTIME/INSTÂNCIA ou credenciais do Builder, desde que o principal nominal seja `codex_reviewer` e os marcadores textuais anteriores tenham sido filtrados. A regra normativa já é correta; falta teste conclusivo.

**Correção obrigatória da fixture, PASS e FAIL de CMP-O-28:**
- Inserir marcadores adversariais inequívocos: `BUILDER_RUNTIME_ID`, `BUILDER_PROCESS_ID`, `BUILDER_AGENT_INSTANCE_ID`, `BUILDER_CREDENTIAL_FINGERPRINT`, além dos marcadores já existentes de scratch, score/verdict, actor, sessão/cache e tool state.
- Definir um review formal com `review_run_id` NOVO, principal `codex_reviewer`, processo/runtime/instância independentes e credencial/referência de reviewer separada, com origem registrada por política fora do LLM. Não é suficiente apenas trocar system prompt, label ou actor textual.
- Evidência futura documentada deve incluir reviewer run metadata, runtime/process/instance IDs, principal de execução e fingerprint/referência da credencial — sem expor segredo bruto — e as entradas permitidas pelo gate, de modo a detectar herança por ambiente/processo mesmo que não esteja no prompt ou no registro da run.
- PASS apenas se os IDs e a identidade de credencial forem distintos dos do Builder e se nenhum hidden state/cache/score/tool state anterior alcançar o reviewer.
- FAIL se mesmo processo, runtime, agent instance ou credencial do Builder for reutilizado, **mesmo que** o actor registrado seja `codex_reviewer` e os marcadores do prompt tenham sido removidos.
- Cobrir origem/fonte do runtime id e a impossibilidade de o próprio LLM falsificar o attestation. Mantenha conversa com Codex apenas read-only e não confunda com uma auditoria formal.

**Entrega:** versão CMP v0.3 em documentos novos/aditivos ou alterações restritas na árvore v0.2, preservando integralmente v0.1, baseline v1.7, pareceres e todas as outras regras fechadas. Registre change report, finding closure, consistency check e índice. Mantenha 13 histórias e 36 oráculos, todos NOT RUN; não crie contagens fictícias, resultados de execução ou novo ledger. Preserve as 12 questões AQ sem decidir em nome do fundador.

**Também preparar para deliberação humana, sem presumir aprovação:** tabela executiva AQ-01/02/03/05/06/07/08/10/11 com proposta/default, riscos e consequências; AQ-04/09/12 deferíveis sob as guardas existentes. Não é obrigatório decidir agora o fornecedor de voz.

**Estado de saída:** DELTA CONVERSATIONAL-MVP v0.3 — CANDIDATE FOR CODEX REVIEW. Publique no GitHub e informe o commit SHA para auditoria Codex separada. Sem testes de software, sem gasto/API, sem build, sem alteração histórica, sem auto-PASS. FDP-14/FDP-15 e BUILD-00 continuam pendentes.
