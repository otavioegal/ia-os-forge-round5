# CMP-FD-08 v0.15 — Rastreabilidade

**Estado:** PROPOSTA. Não é PASS.

| Fonte | Uso |
|---|---|
| SHA `2b2adf382b17a22f1372aaf05b7d3bd1a6ba14ba` | v0.14 auditada. Não editada. Base e parent do manifesto |
| `tools/canonical_json_text.py:11` | normaliza CR e CRLF para LF |
| `tools/canonical_json_text.py:17` | SHA-256 desse texto. Não é blob Git |
| `check_fd_fx03_ack.py:40` | o checker importa essa definição |
| `check_fd_fx03_ack.py:1198` | `file_sha256` delega. Não usa mais `read_bytes` cru |
| `check_fd_fx03_ack.py:1203` | regressão LF/CRLF e edição de conteúdo |
| `check_fd_fx03_ack.py:1472` | `schema_sha256` continua comparado |
| `check_fd_fx03_ack.py:1474` | `fixture_sha256` continua comparado |
| `check_fd_fx03_ack.py:1476` | `synthetic_sha256` continua comparado |
| `check_fd_fx03_ack.py:2428` | regressão com falha devolve `FAIL_CANONICAL_HASH` |
| `check_fd_fx03_ack.py:2620` | banner `STATIC_ACK_V15_CHECK PASS_FIXTURE_ONLY` |
| `draft_semantic_reference.py:84` | o mesmo digest |
| `enumerate_coverage_ids.py:40` | o mesmo digest |
| `fixtures/CMP-FD-FX-03-ack.schema.json:2` | id `cmp.fd.fx03.schema.v0.15` |
| `fixtures/CMP-FD-FX-03-ack.schema.json:38` | const `cmp.fd.fx03.ack.v0.15` |
| `check_fd_historical_manifest.py:20` | base `2b2adf…` |
| `check_fd_historical_manifest.py:21` | parent o mesmo SHA |
| `check_fd_historical_manifest.py:24` | v0.14 sem parecer: `NO_PARECER_YET` |
| `check_fd_historical_manifest.py:184` | path da própria v0.15 é `FAIL_SELF_HASH` |
| `check_fd_historical_manifest.py:206` | v0.2 continua `chosen_verdict` null |
| `check_fd_historical_manifest.py:250` | compara `len(data)` do blob Git |
| `check_fd_historical_manifest.py:331` | `chosen_verdict` preenchido é `FAIL_NOMENCLATURE` |
| `check_fd_historical_manifest.py:384` | `PARECER_CHAIN NOT_FULLY_VERIFIED` |

A v0.14 citada pela auditoria usava `path.read_bytes()` nas linhas 1196–1197 daquele arquivo. Essas linhas não existem mais neste arquivo. O SHA antigo não foi reescrito para fingir o contrário.
