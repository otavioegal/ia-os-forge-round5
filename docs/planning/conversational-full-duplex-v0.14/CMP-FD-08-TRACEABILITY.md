# CMP-FD-08 v0.14 — Rastreabilidade

**Estado:** PROPOSTA. Não é PASS.

| Fonte | Uso |
|---|---|
| SHA `c7b08dc2a0127557293346ebd53e4ff43722683e` | v0.13 auditada. Não editada. Base do manifesto |
| SHA `51d8ff2b89215470bbd6c8f99269301394d91083` | parent desta pasta. Parecer v0.13 e prompt v0.14. Tree `93ced75de5f9bb4a5b11ff7a7fac536fa1e77ec7` |
| Parecer `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.13-2026-10-15.md` | PASS WITH CONDITIONS DOCUMENT-ONLY. Presente só no parent. Não é PASS deste pacote |
| `fixtures/CMP-FD-FX-03-ack.schema.json:2` | id `cmp.fd.fx03.schema.v0.14` |
| `fixtures/CMP-FD-FX-03-ack.schema.json:38` | const `cmp.fd.fx03.ack.v0.14` |
| `fixtures/CMP-FD-FX-03-ack.schema.json:317` | objeto inline negativo |
| `fixtures/CMP-FD-FX-03-ack.schema.json:529` | objeto inline positivo |
| `check_fd_fx03_ack.py:796` | o schema só carrega se o id for v0.14 |
| `check_fd_fx03_ack.py:955` | `dsl_problems` recusa a DSL antes da decisão |
| `check_fd_fx03_ack.py:968` | a fixture só segue se `schema` for `cmp.fd.fx03.ack.v0.14` |
| `check_fd_fx03_ack.py:1206` | `dsl_problems`. Keyword fora do conjunto é `FAIL_UNKNOWN_KEYWORD` |
| `check_fd_fx03_ack.py:1338` | `literal_bindings`. Passeio iterativo. Não é o rascunho e não é mutação |
| `check_fd_fx03_ack.py:1414` | `ratification` diferente de `PENDING_HUMAN_APPROVAL` devolve `FAIL_INVENTED_APPROVAL` |
| `check_fd_fx03_ack.py:1471` | contraprovas que não mudam 508 nem 2443 |
| `check_fd_fx03_ack.py:1582` | fixture `allOf` e keyword `nullable` têm de falhar |
| `check_fd_fx03_ack.py:1624` | compara a lista externa de IDs com a enumeração do checker |
| `check_fd_fx03_ack.py:1678` | inteiro mutado com `True`. Booleano, na linha 1680, com `0` |
| `check_fd_fx03_ack.py:1689` | 480 e 2239 continuam catálogo rejeitado da v0.12 |
| `check_fd_fx03_ack.py:1791` | `expected_schema_rules` |
| `check_fd_fx03_ack.py:1849` | `expected_occurrences` |
| `check_fd_fx03_ack.py:1962` | `stack_jobs` não chama os dois anteriores |
| `check_fd_fx03_ack.py:2233` | chave duplicada em schema, fixture, sintético, manifesto, referência, fixture negativa, IDs e um `case_id` aninhado |
| `check_fd_fx03_ack.py:2378` | quantidade diferente devolve `FAIL_COVERAGE_GAP` |
| `check_fd_fx03_ack.py:2430` | `product_input_exhaustive=false` |
| `check_fd_fx03_ack.py:2576` | o banner é `STATIC_ACK_V14_CHECK PASS_FIXTURE_ONLY` |
| `tools/draft_semantic_reference.py` | rascunho recursivo. Não importa o checker |
| `tools/enumerate_coverage_ids.py` | segunda listagem. Não importa o checker. Não ratifica |
| `check_fd_historical_manifest.py:20` | base `c7b08dc…` |
| `check_fd_historical_manifest.py:21` | parent `51d8ff2…` |
| `check_fd_historical_manifest.py:22` | pacotes v0.1 a v0.13 |
| `check_fd_historical_manifest.py:124` | id do manifesto `cmp.fd.historical-manifest.v0.14` |
| `check_fd_historical_manifest.py:175` | path da própria v0.14 devolve `FAIL_SELF_HASH` |
| `check_fd_historical_manifest.py:197` | v0.2 continua `PENDING_HUMAN_APPROVAL` e `chosen_verdict` null |
| `check_fd_historical_manifest.py:241` | `bytes` comparado a `len(data)` |
| `check_fd_historical_manifest.py:317` | `chosen_verdict` preenchido devolve `FAIL_NOMENCLATURE` |
| `check_fd_historical_manifest.py:320` | `bytes+1` devolve `FAIL_BYTES` |
| `check_fd_historical_manifest.py:368` | `PARECER_CHAIN NOT_FULLY_VERIFIED` |
| `fixtures/CMP-FD-FX-03-ack.json:2` | schema da fixture v0.14 |
| `fixtures/CMP-FD-FX-03-ack.json:543` | `ack_of_sequence` -1 |
| `fixtures/CMP-FD-FX-03-ack.synthetic.json:2` | id sintético v0.14. `proves_product` false. `oracle_status` NOT_RUN |
| `fixtures/CMP-FD-FX-05-semantic-reference.json` | `ratification` PENDING_HUMAN_APPROVAL. `independence` NOT_RATIFIED. `new_gov_01` OPEN |

Sem `--repo`, o histórico imprime `DUPLICATE_KEY manifest=rejected`, `GIT_BLOB_COMPARE NOT_RUN` e `PARECER_CHAIN NOT_RUN`, e sai 2. Isso não é sucesso mascarado.
