# CMP-FD-09 v0.13 — Change report

**Estado:** PROPOSTA. Não é PASS. Não edita v0.1 a v0.12, baseline, CMP, ata, ADR nem parecer.

O parecer da v0.12 recusou 480/480 e 2239/2239. Aquele catálogo percorria `spec["objects"]`, só descia quando havia `ref`, montava `attempt`/`setup`/`step`/`counter` à mão e não entrava em `expected_original_outcome_body`. Também pulava `ELEMENT_TYPE` quando o item era objeto. O `gap=0` era consistente só dentro desse catálogo. Esta pasta não reaproveita esses dois números como prova.

O que muda no gerador, sem mudar a regra de campo:

- `expected_schema_rules` em `check_fd_fx03_ack.py:1293` é um passeio só do schema. Entra em objeto inline, em `fields` aninhados e declara, para array de objeto, `ELEMENT_SCALAR` e `ELEMENT_LIST`.
- `expected_occurrences` em `check_fd_fx03_ack.py:1351` é um segundo passeio, sobre a fixture e os sintéticos. Não monta job.
- `stack_jobs` em `check_fd_fx03_ack.py:1464` é um terceiro passeio, iterativo. Não chama os dois anteriores. Cada índice de array de objeto recebe escalar `1` e lista `[]`, ambos `FAIL_SCHEMA`.
- `raw_slots` em `check_fd_fx03_ack.py:1410` só conta comprimentos JSON. Se discordar dos ids de ocorrência, a cobertura falha.
- Depois da execução, `check_fd_fx03_ack.py:1877` exige que a quantidade de jobs `rule:` e `occ:` seja igual ao tamanho dos dois conjuntos esperados. Job a mais não imprime `gap=0`.
- Chave JSON duplicada é rejeitada no schema, na fixture, no sintético, no manifesto e num `case_id` aninhado da fixture. O checker histórico usa o mesmo parser em `check_fd_historical_manifest.py:45`.

Os campos opcionais de `positive` não existem na linha comportamental. O host `SYN-POSITIVE-ALL-OPTIONAL` carrega o corpo inline, inclusive `error_code`. Sem esse host, a regra positiva fica sem caminho e a cobertura falha. `SYN-NEGATIVE-ALL-OPTIONAL`, `SYN-RECEIVER-REMOVED-SETUP-2` e `SYN-CROSS-TENANT-SETUP-2` continuam hosts de mutação, não linhas de decisão. `proves_product` é false. `oracle_status` é NOT_RUN.

O que não mudou: ordem de ACK, replay 422/200, 409 imutável, 404 opaco antes do lookup, par null, `n` negativo, high-water monotônico, isolamento e zero movimento. NEW-MEDIUM-09 continua sem veredito escolhido. O parecer v0.2 não foi editado. `BYTES MATCH` neste turno é relato do autor, leitura somente, não auditoria independente.

Não houve migration, PostgreSQL, provider, deploy, gasto nem BUILD-00. A flag permanece desligada. `product_input_exhaustive=false` não autoriza omitir regra que já está no schema.
