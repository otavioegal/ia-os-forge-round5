# CMP-FD-09 v0.3 — Relatório de mudança

**Estado:** CANDIDATE FOR CODEX REVIEW. Não é PASS.
**Não edita** v1.7, CMP v0.3, full-duplex v0.1, full-duplex v0.2, ata, ADR nem pareceres.

## Em relação à v0.2

A v0.2 permanece no SHA `18aa352e7bf987aa3a2550b2e2b3251ce71c1f7d`, com FAIL documental. A v0.3 é outra pasta.

| Tema | v0.2, rejeitada nesse ponto | v0.3 |
|---|---|---|
| Lock | a lista do authorizer incluía headroom antes do `FOR UPDATE` | fases A/B sem coluna monetária; C1 é o primeiro lock; headroom só na fase D |
| Teto | `OpenConversationalAnchor` recebia `budget_limit_minor` e criava um Build por sessão | um Build pai por projeto; teto só por comando humano; fatia não eleva o teto |
| Tenant | ids no payload sem predicado | igualdade de canal, org, projeto, sessão, task, build e operation; `404` opaco |
| CAS | `expected_version` anulável | dois campos obrigatórios e `409 VERSION_CONFLICT` |
| Rollback | “podem ser retirados” | pré-condição por passo, `SESSION_CLOSED` bloqueia, ledger não se apaga |
| Schema | timestamps fora da tabela fechada | `observation` tipado e nulabilidade por `event_type` |
| Fixture | tabela em prosa | eventos JSON com digest, mais spans de playback imutáveis |
| Eco | entrada `echo=true` | referência, microfone composto e fala humana; rótulo é saída |
| Histórias | owner PENDING, sem processo | papel proposto, pessoa ainda PENDING, DoR NOT MET |

MEDIUM-01, 02, 03, 04 e 05 não foram afrouxados. As máquinas, os epochs, a matriz de egress, a proveniência e os pontos de latência sem SLA continuam.

## Arquivos novos

Quatorze arquivos em `docs/planning/conversational-full-duplex-v0.3/`:

- CMP-FD-00-INDEX.md
- CMP-FD-01-LEDGER-AND-BUDGET-AUTHORITY.md
- CMP-FD-02-MEDIA-EVENT-SCHEMAS.md
- CMP-FD-03-LIFECYCLE.md
- CMP-FD-04-POLICY-SECURITY-PRIVACY.md
- CMP-FD-05-UX.md
- CMP-FD-06-OBSERVABILITY.md
- CMP-FD-07-STORIES-ORACLES-FIXTURES.md
- CMP-FD-08-TRACEABILITY.md
- CMP-FD-09-CHANGE-REPORT.md
- CMP-FD-10-FINDING-DISPOSITION.md
- CMP-FD-11-OPEN-QUESTIONS.md
- CMP-FD-12-CONSISTENCY-REPORT.md
- CMP-FD-13-MIGRATION-ROLLBACK.md

## O que não foi feito

Teste de software, build, provider, banco, staging, migration real, contratação, deploy, escolha de fornecedor, ligação de flag e BUILD-00.
