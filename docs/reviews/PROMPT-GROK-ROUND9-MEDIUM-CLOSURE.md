# IA OS Forge — Round 9: fechamento de condições MEDIUM

**Repositório:** https://github.com/otavioegal/ia-os-forge-round5
**Baseline auditada:** v1.5, commit `e70112905e60016600eb41566913f63025685a22`
**Parecer obrigatório:** `docs/reviews/PARECER-CODEX-ROUND8-2026-10-13.md`
**Veredito anterior:** PASS WITH CONDITIONS documental; 0 Critical/High. **Não é autorização BUILD-00.**
**Builder:** Grok. **Reviewer independente:** Codex. **Entrega:** v1.6, ROUND 9 — CANDIDATE FOR CODEX REVIEW.

Leia integralmente o parecer Round 8 e os FDP-16A/F-015/matriz v1.5. Corrija SOMENTE as condições C-01 e C-02, preservando 4 HIGH fechados e todos os demais contratos aceitos. Não reabra a arquitetura nem crie exigências operacionais prematuras.

## C-01 — confirmação, replay e revogação (NEW-MEDIUM-10)

No FDP-16A, tornar inequívoco que `ApplyAuthorizedReconciliation` para PROVEN_RECEIPT revalida `ledger.reconcile` tanto para `requested_by` como `confirmed_by`. Se qualquer permissão estiver revogada: `403 CAPABILITY_REVOKED`, autorização não consumida, reserva HELD e nenhum movimento, audit/outbox coerentes. Definir as condições de sessão/capability verificadas no momento do Apply, sem assumir permissão por causa da aprovação histórica.

Completar contrato e oráculos para:
- Confirm repetido com mesmo command_id (idempotent replay);
- Confirm com command_id novo após estado AUTHORIZED (duplicata rejeitada sem evento contraditório);
- revoke do solicitante ANTES de Apply;
- revoke do confirmador ANTES de Apply;
- confirmar sem capability, evidence_ref divergente e Apply duplicado (mesmo e novo command_id), sem segunda mutação financeira.
Atualize LEDGER-14 ou acrescente oracle(s) específicos com fixture, passos, PASS/FAIL, audit, contadores e garantia NOT RUN.

## C-02 — pending_provider_cost (NEW-MEDIUM-11)

Tornar obrigatória a persistência da linha `pending_provider_cost` em todas as transições de CONFLICT com receipt. `pending_actual_minor` será SOMENTE derivado das linhas persistidas, nunca atribuído independentemente.

Resolver explicitamente dois receipts conclusivos divergentes para a mesma operação:
- preferencialmente uma linha imutável por proof_id com unique(operation_id, proof_id) e regra de projeção documentada, ou uma agregação conservadora rigorosamente definida;
- preservar todas as provas, moedas, valores, escopos e auditoria, sem escolher pelo timing/lock;
- preservar invariantes de budget, reserva HELD e nenhuma contabilização indevida.

Corrigir LEDGER-08 para conferir a persistência de pending cost em CONFLICT. Corrigir a fixture LEDGER-15: operação DISPATCHED, reserva individual HELD=50, contadores anteriores spent=800/reserved=100 e após Reserve total reserved=150; ou incluir Reserve/Dispatch nos passos. Oráculos com valores, PASS/FAIL e critérios de prova explícitos.

## Entrega e escopo

1. Versionar apenas documentos normativos afetados em v1.6 com matriz única, história F-015, FDP-16A e apontadores coerentes. Preservar v1.5 intacta em historical/round8, incluindo parecer Codex original.
2. Produzir índice Round 9, change report, finding-closure C-01/C-02, consistency report e open pendencies.
3. Validar documentos e links, 41 histórias, 17 P0, 11 Task states; nenhum teste de produto. Todos os oráculos permanecem NOT RUN.
4. Não modificar regras aceitas de AIOX, segurança, deploy, runbooks ou outros Highs.
5. FDP-14 e FDP-15 continuam pendentes de confirmação/aprovação; fundador não aprovou e BUILD-00 não está autorizado.
6. Criar commit não destrutivo no mesmo GitHub e informar SHA para auditoria Codex.
7. Nomear entrega **ROUND 9 — CANDIDATE FOR CODEX REVIEW**, nunca PASS autodeclarado.

O objetivo é encerrar essas duas MEDIUM sem reabrir planejamento já aceito documentalmente.
