# CMP-FD-00 v0.15 — Índice

**Estado do pacote:** CANDIDATE FOR CODEX REVIEW. Não é PASS. O autor não fecha finding.
**SHA auditado da v0.14, preservado:** `2b2adf382b17a22f1372aaf05b7d3bd1a6ba14ba`
**Parent desta pasta:** o mesmo SHA. Não houve commit de parecer depois dele. Este pacote não reescreve esse commit.
**Migration, deploy, provider, gasto, PostgreSQL e BUILD-00:** não executados e não autorizados.
**`forge.conversation.delta.v4`:** desligada.

A v0.14 permanece o objeto histórico auditado. Num checkout com `core.autocrlf=true` o checker dela não alcançou `STATIC_ACK_V14_CHECK`: `file_sha256` lia `path.read_bytes()` e a comparação de `schema_sha256`, `fixture_sha256` e `synthetic_sha256` devolvia `FAIL_SEMANTIC_DRIFT`. Com `core.autocrlf=false` o mesmo checker terminava em `PASS_FIXTURE_ONLY`. Esta pasta não altera aqueles arquivos. Corrige a definição do digest textual na v0.15.

O digest textual normaliza CR e CRLF para LF antes do SHA-256. Não é identidade de blob Git. O manifesto histórico continua a usar `git cat-file`.

| Peça | Papel |
|---|---|
| CMP-FD-02 | Replay preservado |
| CMP-FD-07 | Oráculos NOT RUN. LOW-01 OPEN BLOCKING DoR |
| CMP-FD-08 | Rastreabilidade |
| CMP-FD-09 | O que mudou: só o digest textual |
| CMP-FD-10 | Disposição. Nenhum finding foi fechado |
| CMP-FD-11 | Questões abertas |
| CMP-FD-12 | Transcripts LF e CRLF, e o histórico |
| CMP-FD-13 | Concorrência não executada |
| CMP-FD-14 | Cadeia. v0.2 NOT_VERIFIED. v0.14 sem parecer inventado |
| CMP-FD-15 | Schema. Regras de campo iguais. Id v0.15 |
| CMP-FD-16 | Governança da v0.2. `chosen_verdict` null |
| CMP-FD-17 | 508 e 2443. `PASS_FIXTURE_ONLY`. Não é cobertura total |
| CMP-FD-18 | Referência semântica não ratificada. NEW-GOV-01 OPEN |
| fixtures/CMP-FD-FX-03-ack.json | 26 linhas. Não é oráculo |
| fixtures/CMP-FD-FX-03-ack.schema.json | Autoridade de nomes e tipos |
| fixtures/CMP-FD-FX-03-ack.synthetic.json | Hosts. `proves_product` false. `oracle_status` NOT_RUN |
| fixtures/CMP-FD-FX-04-historical-manifest.json | 218 paths, v0.1 a v0.14. Blob Git, não digest textual |
| fixtures/CMP-FD-FX-05-semantic-reference.json | 308 literais. `PENDING_HUMAN_APPROVAL` |
| fixtures/CMP-FD-FX-06-unknown-keyword.json | `allOf` tem de falhar |
| fixtures/CMP-FD-FX-07-coverage-ids.json | 508 e 2443 IDs |
| tools/canonical_json_text.py | A única definição do digest textual |
| tools/check_fd_fx03_ack.py | Checker. `PASS_FIXTURE_ONLY` não é PASS |
| tools/check_fd_historical_manifest.py | Sem `--repo`, exit 2 |
| tools/draft_semantic_reference.py | Usa a mesma função de digest |
| tools/enumerate_coverage_ids.py | Usa a mesma função de digest |

`FULL_PRODUCT_COVERAGE false`. `COVERAGE_TOTAL_PASS not_claimed`. `product_input_exhaustive=false`.
