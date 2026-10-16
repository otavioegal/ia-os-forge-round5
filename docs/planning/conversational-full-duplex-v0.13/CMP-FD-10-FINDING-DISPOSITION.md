# CMP-FD-10 v0.13 — Disposição

**Estado:** CANDIDATE FOR CODEX REVIEW, salvo o que outro parecer já fechou e salvo LOW-01 e FD07-07. O autor não escreve PASS e não fecha NEW-MEDIUM-09, NEW-LOW-03, FD11-NEW-01, FD12-NEW-01, FD12-NEW-02 nem FD12-NEW-03.

## FD12-NEW-01 — objeto inline fora do catálogo da v0.12

- Causa: `expected_original_outcome_body` é objeto inline, com `error_code` obrigatório e `opaque`, `retryable`, `terminal`, `peer_ack_high_water` opcionais. O catálogo da v0.12 não descia nele. O validador já descia, em `fields_error`.
- Texto: o objeto está em `fixtures/CMP-FD-FX-03-ack.schema.json:317` e de novo em `fixtures/CMP-FD-FX-03-ack.schema.json:529`. `check_fd_fx03_ack.py:895` continua a validar `fields` aninhados. `check_fd_fx03_ack.py:1328` declara extra e cada subcampo. A ausência de `error_code` e o tipo de `opaque` entram na conta RAW.
- Neste turno o autor observou, no checker local, `COVERAGE_RULES declared=508 exercised=508 gap=0` e `COVERAGE_OCCURRENCES declared=2443 exercised=2443 gap=0`. Isso é `PASS_FIXTURE_ONLY`. `COVERAGE_TOTAL_PASS not_claimed`. Não fecha o finding.
- Status: CANDIDATE.

## FD12-NEW-02 — tipo do elemento de array de objeto

- Causa: a v0.12 pulava mutação de tipo quando `item_type == "object"`.
- Texto: `check_fd_fx03_ack.py:1322` declara `ELEMENT_SCALAR` e `ELEMENT_LIST` para item objeto. `check_fd_fx03_ack.py:1530` aplica os dois em cada índice. Os valores são `1` e `[]`. O código esperado é `FAIL_SCHEMA`. A conta RAW deste turno foi `setup_scalar=16/16`, `setup_list=16/16`, `step_scalar=5/5`, `step_list=5/5`, `initial_scalar=7/7`, `initial_list=7/7`.
- Status: CANDIDATE. Não é fechamento.

## FD12-NEW-03 — chave JSON duplicada

- Causa: o parser padrão aceita chave repetida e fica com a última.
- Texto: `check_fd_fx03_ack.py:1735` sonda schema, fixture, sintético, manifesto e uma chave aninhada na fixture. `check_fd_historical_manifest.py:32` define `DuplicateKeyError`. `check_fd_historical_manifest.py:45` devolve `FAIL_DUPLICATE_KEY` antes de comparar blob. Sem `--repo` o processo ainda sai 2.
- Status: CANDIDATE. A rejeição estática não é auditoria independente.

## FD11-NEW-01 e NEW-LOW-03

- Causa residual depois da v0.12: a contagem fechava um catálogo que não era o schema inteiro. Dizer "uma mutação por campo" e "para cada objeto e cada campo" era falso enquanto o inline e o elemento objeto ficavam de fora.
- Texto: os dois passeios esperados são `check_fd_fx03_ack.py:1293` e `check_fd_fx03_ack.py:1351`. O gerador é `check_fd_fx03_ack.py:1464` e não os chama. `check_fd_fx03_ack.py:1877` falha se as quantidades divergirem. `check_fd_fx03_ack.py:1191` guarda 480 e 2239 só para imprimir `V12_CATALOG_REJECTED`. `check_fd_fx03_ack.py:1894` mantém `product_input_exhaustive=false`. `check_fd_fx03_ack.py:1180` usa `True` onde o tipo é inteiro. `check_fd_fx03_ack.py:1182` usa `0` onde o tipo é booleano.
- Status: CANDIDATE. NEW-LOW-03 permanece PARTIAL até o Codex. FD11-NEW-01 não é fechado aqui. 508 e 2443 são relato do autor sobre esta fixture. Não são PASS de produto e não reabilitam 480 e 2239.

## NEW-MEDIUM-09

- Causa: o blob do parecer v0.2 contém `FAIL` no cabeçalho e `FAIL — DOCUMENT-ONLY` no fecho, com o corpo duplicado.
- Texto: CMP-FD-16 cita o blob `2d992a9cf0ab38d639b95f69df1571eb97f444b4` e o SHA-256 `575e149c3e29203c9c5b7c6532f15b06af6c562551372077502eaf50b246daef`. `chosen_verdict` fica null. `check_fd_historical_manifest.py:197` recusa aprovação inventada. `check_fd_historical_manifest.py:317` recusa `chosen_verdict` preenchido. `check_fd_historical_manifest.py:241` compara `bytes` com o tamanho do blob. `check_fd_historical_manifest.py:320` rejeita `bytes+1`. `check_fd_historical_manifest.py:368` mantém `PARECER_CHAIN NOT_FULLY_VERIFIED`. `check_fd_historical_manifest.py:79` extrai o texto do blob. `check_fd_historical_manifest.py:25` aceita o rótulo `Checkout examinado`.
- v0.5 e v0.6: ausência legítima. Prompts v0.6 e v0.7: ausentes. O prompt v0.13 está no parent e entra na lista presente, junto com v0.2, v0.3, v0.4, v0.5, v0.8, v0.9, v0.10, v0.11 e v0.12.
- Status: PARTIAL. NOT_VERIFIED até ato humano. Não é fechamento. O `BYTES MATCH` autoral não substitui auditoria.

## NEW-LOW-02

- O parecer da v0.11 fechou este item como CLOSED documental, não executado. O parecer da v0.12 não o reabriu. Esta pasta não o reabre e não o transforma em prova de produto.

## FD07-07

- Texto: CMP-FD-13. Dois backends, barreira, as duas ordens, rollback e locks continuam especificados e não executados.
- Status: OPEN. O92 e O93 NOT RUN.

## HIGH-03

- Status: PARTIAL. Sem a evidência de O92.

## Preservados

FD07-01..06, FD07-08, NEW-MEDIUM-07, NEW-MEDIUM-08 e FD07-09 no escopo dos blobs de planejamento permanecem CLOSED documentalmente. A fixture `fixtures/CMP-FD-FX-03-ack.json:543` continua `ack_of_sequence` -1, estágio `negative`. O replay do 422, o 409 sem troca da linha e o 404 de tenant antes do lookup não foram afrouxados. NEW-MEDIUM-06 permanece CLOSED documentalmente. Migration NOT RUN.

## LOW-01

- Texto: CMP-FD-07. Pessoa PENDING. Effort UNSTATED. DoR NOT MET.
- Status: OPEN BLOCKING DoR. O autor não inventa dono nem esforço.

## Não redispostos

HIGH-01, HIGH-02, NEW-HIGH-01, NEW-HIGH-02, NEW-MEDIUM-01, NEW-MEDIUM-02, NEW-MEDIUM-04 e MEDIUM-01..05 permanecem fechados pelo Codex. NEW-HIGH-04, NEW-HIGH-03, NEW-MEDIUM-05 e NEW-MEDIUM-03 continuam CANDIDATE.
