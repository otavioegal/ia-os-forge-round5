# CMP-FD-00 v0.14 — Índice

**Estado do pacote:** CANDIDATE FOR CODEX REVIEW. Não é PASS. O autor não fecha finding.
**SHA auditado da v0.13:** `c7b08dc2a0127557293346ebd53e4ff43722683e`
**Parent desta pasta:** `51d8ff2b89215470bbd6c8f99269301394d91083`
**Migration, deploy, provider, gasto, PostgreSQL e BUILD-00:** não executados e não autorizados.
**`forge.conversation.delta.v4`:** desligada. A v3 não é integrada.

O parecer da v0.13 é PASS WITH CONDITIONS DOCUMENT-ONLY. Isso não promove produto nem operação. O pacote v0.13 permanece CANDIDATE até decisão humana. Esta pasta não adota aquele cabeçalho como PASS próprio.

O limite que esta pasta trata é NEW-GOV-01: os passeios da v0.13 compartilham a DSL, `TYPE_WRONG` e os sufixos. Um bug espelhado pode conservar `gap=0`. A referência semântica daqui é um arquivo externo, não ratificado. `PENDING_HUMAN_APPROVAL` não é aprovação inventada. NEW-GOV-01 fica OPEN.

| Peça | Papel |
|---|---|
| CMP-FD-02 | Replay, 409, 404, null-pair, `n<0` e zero movimento preservados |
| CMP-FD-07 | Oráculos NOT RUN. LOW-01 OPEN BLOCKING DoR |
| CMP-FD-08 | Rastreabilidade |
| CMP-FD-09 | Change report |
| CMP-FD-10 | Disposição. O autor não promove PASS |
| CMP-FD-11 | Questões abertas |
| CMP-FD-12 | Consistência. Relato do autor, não auditoria independente |
| CMP-FD-13 | Concorrência especificada e não executada |
| CMP-FD-14 | Cadeia lida dos blobs. v0.2 NOT_VERIFIED |
| CMP-FD-15 | Schema fechado. Keyword desconhecido é `FAIL_UNKNOWN_KEYWORD` |
| CMP-FD-16 | Governança da v0.2. `chosen_verdict` null |
| CMP-FD-17 | 508 regras e 2443 ocorrências, com a lista auditável. Não é cobertura total |
| CMP-FD-18 | Referência semântica. Não ratificada. NEW-GOV-01 OPEN |
| fixtures/CMP-FD-FX-03-ack.json | 26 linhas de decisão. Não é oráculo |
| fixtures/CMP-FD-FX-03-ack.schema.json | Autoridade de nomes, tipos e cardinalidade |
| fixtures/CMP-FD-FX-03-ack.synthetic.json | Hosts sintéticos. `proves_product` false. `oracle_status` NOT_RUN |
| fixtures/CMP-FD-FX-04-historical-manifest.json | 193 paths de v0.1 a v0.13. A v0.14 não entra |
| fixtures/CMP-FD-FX-05-semantic-reference.json | 308 literais. Ratificação pendente. Não é golden humano |
| fixtures/CMP-FD-FX-06-unknown-keyword.json | Fixture negativa. `allOf` tem de ser recusado |
| fixtures/CMP-FD-FX-07-coverage-ids.json | 508 IDs de regra e 2443 IDs de ocorrência, com digest |
| tools/check_fd_fx03_ack.py | Checker estático. `PASS_FIXTURE_ONLY` não é PASS |
| tools/check_fd_historical_manifest.py | Sem `--repo`, exit 2 e NOT_RUN |
| tools/draft_semantic_reference.py | Rascunho recursivo dos literais. Não importa o checker |
| tools/enumerate_coverage_ids.py | Segunda listagem dos IDs. Não importa o checker. Não ratifica |

Nada aqui edita v0.1–v0.13, baseline, CMP v0.3, ata, ADR ou parecer. `COVERAGE_TOTAL_PASS` não é reivindicado. `FULL_PRODUCT_COVERAGE false`. `product_input_exhaustive=false`.
