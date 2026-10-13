# IA OS FORGE — PROMPT GROK ROUND 7
## Missão: fechar exclusivamente HIGH-01 e NEW-HIGH-07

**Fonte normativa de auditoria:** `docs/reviews/PARECER-CODEX-ROUND6-2026-10-13.md`.
**Commit auditado:** `4e5783974ca27595c9592e2e6ac55ab23fcbeb5a`.
**Repositório:** https://github.com/otavioegal/ia-os-forge-round5
**Builder documental:** Grok. **Reviewer independente:** Codex. **Governança:** fundador + ChatGPT.
**Versão de saída:** v1.4, **ROUND 7 — CANDIDATE FOR CODEX REVIEW**.

Leia primeiro, integralmente, o parecer Round 6, o FDP-16A v1.3 (§5 e §8A), F-015 no FDP-19A v1.3, e as linhas LEDGER-01 a LEDGER-06 da matriz v1.3. Consulte FDP-12/13 históricos e a política de revisão. Não confie apenas no resumo do parecer.

## A. HIGH-01: concorrência transacional no ledger

Formalize **um protocolo único e normativo de serialização** para Reserve, RecordReceipt (settlement) e ReleaseReservation (refund/liberação) usando transação PostgreSQL com ordem de locks explícita em Build, Operation e Reservation, ou isolamento/CAS equivalente demonstravelmente seguro. Defina versão esperada, estados válidos, constraints e unique keys, transição monetária atômica e política de retry após conflito. Preserve invariantes `spent + reserved <= limit`, soma de reservas HELD e `at most one monetary terminal movement per operation_ref`.

Especifique resultado determinístico de quatro disputas: (1) dois RecordReceipt simultâneos; (2) RecordReceipt versus ReleaseReservation; (3) dois ReleaseReservation simultâneos; (4) retry tardio após o vencedor commitado. O perdedor não pode mover dinheiro, editar estado terminal nem criar evento de settlement/release duplicado. Especifique erros e outbox/audit no mesmo commit, inclusive crash e replay, sem redispatch cego. Considere receipt com actual > estimate e orçamento insuficiente, mantendo coerência do estado bloqueado sem falsificar gasto.

Crie oráculos adicionais com fixture, passos de corrida simultânea/barrier, PASS/FAIL e evidências de contadores/linhas/eventos; mantenha os 17 P0 com IDs e semântica originais e a matriz canônica única.

## B. NEW-HIGH-07: reconciliação manual

Resolva o conflito entre catálogo (§5) que autoriza RecordReceipt/ReleaseReservation apenas para system e §8A que permite intervenção humana em BLOCKED_RECONCILIATION. Escolha e especifique uma via **única** de autoridade: por exemplo, comando humano `ApproveManualReconciliation` contendo `evidence_ref`, com autenticação forte, papel security_operator, escopo, dual-control quando aplicável, política externa ao LLM, trilha e idempotência; e a execução contábil subsequente pelo system. Alternativamente, uma via humana direta devidamente tipada e autorizada. Não abra privilégios de coding_engine nem permita escrever evidência fictícia. Harmonize comando, payload, matrizes, contrato API, F-015, oráculos e audit/outbox. Exija evidence_ref para prova de receipt ou no-effect e recuse reconciliação ambígua.

## C. Escopo e integridade

Não reabra os cinco HIGH e cinco MEDIUM já fechados pelo Codex. Preserve a baseline v1.3 em `historical/round6/`, sem reescrever pareceres, fontes ou histórico. Gere apenas v1.4 dos arquivos atingidos e atualize apontadores para a matriz única v1.4 sem introduzir conflito de versões. Quando documentos não mudarem substancialmente, explicite revalidação e versionamento consistente, sem refazê-los inutilmente.

Rode verificador textual não destrutivo e uma checagem semântica documentada. Não execute produto, banco de produção, provider, deploy, testes de software ou staging. Status de testes permanece NOT RUN. FDP-14/15 e Founder permanecem pendentes; BUILD-00 não autorizado.

## D. Entregáveis

1. Documentos v1.4 corrigidos, com FDP-16A, F-015/FDP-19A e matriz de oráculos.
2. `docs/reviews/ROUND7-FINDING-CLOSURE-2026-10-13.md`, separado por HIGH-01 e NEW-HIGH-07, com arquivo:linha e prova específica.
3. `docs/reviews/ROUND7-CHANGE-REPORT-2026-10-13.md` e relatório de consistência.
4. `docs/planning/FDP-ROUND7-STATUS-INDEX.md` e pendências restantes.
5. Commit no repositório oficial; informe SHA. Não alterar parecer Codex Round 6.
6. Entrega final como **CANDIDATE FOR CODEX REVIEW**, nunca PASS autodeclarado.

Feche o problema financeiro verificando propriedades, não só contando IDs. Se surgir contradição nova, registre-a sem inventar aprovação. O Codex emitirá o parecer independente sobre commit congelado.
