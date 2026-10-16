# CMP-FD-08 v0.13 — Rastreabilidade

**Estado:** PROPOSTA. Não é PASS.

| Fonte | Uso |
|---|---|
| SHA `346cd04ae90bf57f4594e1a4b4af0584961dd546` | v0.12 auditada. Não editada. Base do manifesto |
| SHA `cfb1c98412d4c183b406d919fabbe753ac43076b` | parent desta pasta. Parecer v0.12 e prompt v0.13. Tree `81cc3fec733daf91729a659b8f47bb62a797ff5e` |
| Parecer `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.12-2026-10-15.md` | FAIL DOCUMENT-ONLY. Presente só no parent |
| `fixtures/CMP-FD-FX-03-ack.schema.json:2` | id `cmp.fd.fx03.schema.v0.13` |
| `fixtures/CMP-FD-FX-03-ack.schema.json:38` | const `cmp.fd.fx03.ack.v0.13` |
| `fixtures/CMP-FD-FX-03-ack.schema.json:317` | objeto inline negativo `expected_original_outcome_body` |
| `fixtures/CMP-FD-FX-03-ack.schema.json:529` | o mesmo objeto no positivo |
| `check_fd_fx03_ack.py:796` | o schema só carrega se o id for v0.13 |
| `check_fd_fx03_ack.py:895` | `fields_error` entra em objeto inline com `fields` |
| `check_fd_fx03_ack.py:965` | a fixture só segue se `schema` for `cmp.fd.fx03.ack.v0.13` |
| `check_fd_fx03_ack.py:1180` | inteiro mutado com `True`; booleano, na linha 1182, com `0` |
| `check_fd_fx03_ack.py:1191` | 480 e 2239 ficam rotulados como catálogo rejeitado, não como esta cobertura |
| `check_fd_fx03_ack.py:1293` | `expected_schema_rules`: passeio só do schema, sem ver jobs nem fixture |
| `check_fd_fx03_ack.py:1322` | array de objeto declara `ELEMENT_SCALAR` e `ELEMENT_LIST` |
| `check_fd_fx03_ack.py:1328` | objeto inline declara extra e desce em cada subcampo |
| `check_fd_fx03_ack.py:1351` | `expected_occurrences`: segundo passeio, recursivo, não monta job |
| `check_fd_fx03_ack.py:1410` | `raw_slots` conta comprimentos JSON, sem schema e sem job |
| `check_fd_fx03_ack.py:1435` | `raw_disagrees` compara esses comprimentos com os ids de ocorrência |
| `check_fd_fx03_ack.py:1464` | `stack_jobs` é iterativo e não chama os dois passeios esperados |
| `check_fd_fx03_ack.py:1530` | cada índice de array de objeto recebe escalar e lista inválida |
| `check_fd_fx03_ack.py:1735` | sondas de chave duplicada: schema, fixture, sintético, manifesto e um aninhado |
| `check_fd_fx03_ack.py:1769` | `coverage_failures` compara esperado com exercido |
| `check_fd_fx03_ack.py:1877` | contagem de jobs diferente do conjunto esperado devolve `FAIL_COVERAGE_GAP` |
| `check_fd_fx03_ack.py:1894` | `product_input_exhaustive=false` |
| `check_fd_fx03_ack.py:1901` | `COVERAGE_TOTAL_PASS not_claimed` |
| `check_fd_fx03_ack.py:2040` | o banner é `STATIC_ACK_V13_CHECK PASS_FIXTURE_ONLY` |
| `check_fd_historical_manifest.py:20` | base `346cd04…` |
| `check_fd_historical_manifest.py:21` | parent `cfb1c98…` |
| `check_fd_historical_manifest.py:22` | pacotes v0.1 a v0.12 |
| `check_fd_historical_manifest.py:25` | o rótulo `Checkout examinado` entra na extração |
| `check_fd_historical_manifest.py:32` | `DuplicateKeyError` |
| `check_fd_historical_manifest.py:45` | `load_strict_text` rejeita chave duplicada antes da comparação |
| `check_fd_historical_manifest.py:79` | extração do parecer a partir do blob |
| `check_fd_historical_manifest.py:124` | id do manifesto `cmp.fd.historical-manifest.v0.13` |
| `check_fd_historical_manifest.py:175` | path da própria v0.13 devolve `FAIL_SELF_HASH` |
| `check_fd_historical_manifest.py:197` | v0.2 continua `PENDING_HUMAN_APPROVAL` e `chosen_verdict` null |
| `check_fd_historical_manifest.py:241` | `bytes` comparado a `len(data)` |
| `check_fd_historical_manifest.py:317` | `chosen_verdict` preenchido devolve `FAIL_NOMENCLATURE` |
| `check_fd_historical_manifest.py:320` | `bytes+1` devolve `FAIL_BYTES` |
| `check_fd_historical_manifest.py:368` | `PARECER_CHAIN NOT_FULLY_VERIFIED` |
| `fixtures/CMP-FD-FX-03-ack.json:2` | schema da fixture `cmp.fd.fx03.ack.v0.13` |
| `fixtures/CMP-FD-FX-03-ack.json:543` | `ack_of_sequence` -1 |
| `fixtures/CMP-FD-FX-03-ack.synthetic.json:2` | id sintético v0.13. `proves_product` false na linha 3. `oracle_status` NOT_RUN na linha 4 |
| `fixtures/CMP-FD-FX-04-historical-manifest.json:2` | schema do manifesto v0.13. Base na linha 3. Parent na linha 4 |

Sem `--repo`, o histórico imprime `DUPLICATE_KEY manifest=rejected`, `GIT_BLOB_COMPARE NOT_RUN` e `PARECER_CHAIN NOT_RUN`, e sai 2. Isso não é sucesso mascarado.
