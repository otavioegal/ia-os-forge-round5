# CMP-FD-00 v0.3 — Índice

**Estado:** CANDIDATE FOR CODEX REVIEW. **Não é PASS.** O autor não fecha finding.
**Pasta:** `docs/planning/conversational-full-duplex-v0.3/`. Aditiva. Não edita v1.7, CMP v0.3, full-duplex v0.1, full-duplex v0.2, ata, ADR ou pareceres.
**Pai desta entrega:** `ea0fc356e2a500eef8f6de2199d726acff99e4c2`.
**SHA auditado da v0.2:** `18aa352e7bf987aa3a2550b2e2b3251ce71c1f7d`, veredito Codex FAIL DOCUMENT-ONLY.
**Baseline histórica:** v1.7 `0c42373d583dec420348efd7bc0b8c6228a66f47`. CMP v0.3 `f404abc1b4a90f01a12266e3e56a65df277258dd`.

Nenhum teste de software, build, provider, banco, staging ou API de produto foi executado. BUILD-00 não está autorizado. FDP-14, FDP-15 e a consolidação da baseline continuam PENDING.

## Mapa

| Arquivo | Função |
|---|---|
| CMP-FD-01-LEDGER-AND-BUDGET-AUTHORITY.md | Transação ordenada, teto pai, escopo de tenant, CAS |
| CMP-FD-02-MEDIA-EVENT-SCHEMAS.md | União discriminada `cmp.media.duplex.v1`, inclusive timestamps |
| CMP-FD-03-LIFECYCLE.md | Máquinas já aceitas pelo Codex; sem regressão |
| CMP-FD-04-POLICY-SECURITY-PRIVACY.md | Consentimento e trust; sem regressão |
| CMP-FD-05-UX.md | Proveniência; sem regressão |
| CMP-FD-06-OBSERVABILITY.md | Pontos de medida e correlação de relógio; sem SLA |
| CMP-FD-07-STORIES-ORACLES-FIXTURES.md | Fixtures alinhadas ao schema; oráculos NOT RUN |
| CMP-FD-08-TRACEABILITY.md | AQ, findings, oráculos |
| CMP-FD-09-CHANGE-REPORT.md | O que a v0.3 muda em relação à v0.2 |
| CMP-FD-10-FINDING-DISPOSITION.md | Índice de alegações. Não é evidência de fechamento |
| CMP-FD-11-OPEN-QUESTIONS.md | AQ-04/09/12 e gates humanos |
| CMP-FD-12-CONSISTENCY-REPORT.md | Checagem estática do autor |
| CMP-FD-13-MIGRATION-ROLLBACK.md | Passos, downgrade, ledger intocável |

## Decisões humanas — não reabertas

| AQ | Estado |
|---|---|
| AQ-01, AQ-02, AQ-03, AQ-05, AQ-06, AQ-07, AQ-08, AQ-10, AQ-11 | APPROVED na ata ou, no caso de AQ-07, no ADR |
| AQ-04, AQ-09, AQ-12 | DEFERRED / UNDECIDED |

Full-duplex natural continua obrigatório no MVP para Jarvis, todos os agentes conversacionais e o Conselho. Meio-duplex com barge-in não satisfaz.

## O que esta versão corrige no texto

A v0.2 continua no repositório, imutável, com FAIL. A v0.3 substitui a proposta normativa nos pontos em que o Codex mostrou contradição:

1. Headroom, `stop_latch` e reconciliação só são lidos depois de `SELECT build FOR UPDATE`.
2. `OpenConversationalAnchor` não recebe teto. Há um Build pai por projeto e a soma das sessões não pode passar desse teto.
3. Org, projeto, canal, sessão, Build, Task e Operation têm predicado de igualdade e resposta que não vaza recurso estrangeiro.
4. `expected_task_version` e `expected_build_version` são obrigatórios, com `409 VERSION_CONFLICT`.
5. Cada `event_type` tem payload tipado. Os seis timestamps da fixture estão nesse schema.
6. O oráculo de eco não recebe `echo=true` como premissa.
7. Histórias continuam sem dono nomeado. Há papel proposto e processo; DoR segue NOT MET.

## Pedido de auditoria

Solicita-se revisão Codex independente, somente leitura, sobre o SHA imutável desta entrega. O relatório de consistência deste pacote não substitui esse parecer.
