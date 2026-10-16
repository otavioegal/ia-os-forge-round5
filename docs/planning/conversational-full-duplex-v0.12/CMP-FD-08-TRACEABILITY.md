# CMP-FD-08 v0.12 — Rastreabilidade

**Estado:** PROPOSTA. Não é PASS.

| Fonte | Uso |
|---|---|
| SHA `9522d5b090d451cc61face6e23a3f0b5081bf62f` | v0.11 auditada. Não editada |
| SHA `3d4de1be8b6f683d66c2514b4847619bec9cdfe9` | parent desta pasta. Parecer v0.11 e prompt v0.12 |
| Parecer `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.11-2026-10-15.md` | FAIL DOCUMENT-ONLY. Presente só no parent |
| `fixtures/CMP-FD-FX-03-ack.schema.json:2` | id `cmp.fd.fx03.schema.v0.12`. Regras de campo iguais às da v0.11 |
| `check_fd_fx03_ack.py:1238` | `schema_jobs` nasce do schema, não do primeiro caso |
| `check_fd_fx03_ack.py:1256` | percorre `spec["objects"]` |
| `check_fd_fx03_ack.py:1392` | uma ocorrência por caso do host, não por `kind` |
| `check_fd_fx03_ack.py:1403` | cada índice de `setup` |
| `check_fd_fx03_ack.py:1414` | cada índice de `steps` |
| `check_fd_fx03_ack.py:1419` | cada índice de `commit_order` e, na linha 1421, de `expected_steps` |
| `check_fd_fx03_ack.py:1442` | contagem estrutural independente da execução |
| `check_fd_fx03_ack.py:1574` | falha se a contagem declarada não fechar |
| `check_fd_fx03_ack.py:1652` | lacuna de regra devolve `FAIL_COVERAGE_GAP` |
| `check_fd_historical_manifest.py:49` | extração do parecer a partir do blob |
| `check_fd_historical_manifest.py:167` | v0.2 continua `PENDING_HUMAN_APPROVAL` e `chosen_verdict` null |
| `check_fd_historical_manifest.py:211` | `bytes` comparado a `len(data)` |
| `check_fd_historical_manifest.py:328` | `PARECER_CHAIN NOT_FULLY_VERIFIED` |
| `fixtures/CMP-FD-FX-03-ack.json:543` | `n=-1` |
| `fixtures/CMP-FD-FX-03-ack.synthetic.json:2` | hosts sintéticos, não linhas de decisão |

Sem `--repo`, o histórico sai `GIT_BLOB_COMPARE NOT_RUN` e `PARECER_CHAIN NOT_RUN`, exit 2. Isso não é sucesso mascarado.
