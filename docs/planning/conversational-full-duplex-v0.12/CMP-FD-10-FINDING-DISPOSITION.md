# CMP-FD-10 v0.12 — Disposição

**Estado:** CANDIDATE FOR CODEX REVIEW, salvo o que outro parecer já fechou e salvo LOW-01 e FD07-07. O autor não escreve PASS e não fecha NEW-MEDIUM-09, NEW-LOW-03 nem FD11-NEW-01.

## FD11-NEW-01 e NEW-LOW-03

- Causa: a v0.11 dizia mutar cada campo, mas só usava a primeira ocorrência de cada `kind` e o primeiro elemento de cada lista. Opcionais ausentes nessa ocorrência não eram mutados. `replay`, `fresh`, `probe` e os demais `setup` não tinham remoção própria.
- Texto: o schema em `fixtures/CMP-FD-FX-03-ack.schema.json:2` continua a autoridade. `check_fd_fx03_ack.py:1256` gera a regra a partir de cada objeto. `check_fd_fx03_ack.py:1392` percorre todos os casos. `check_fd_fx03_ack.py:1403`, `check_fd_fx03_ack.py:1414` e `check_fd_fx03_ack.py:1419` percorrem todos os índices. `check_fd_fx03_ack.py:1134` usa `True` onde o tipo é inteiro. `check_fd_fx03_ack.py:1136` usa `0` onde o tipo é booleano. `check_fd_fx03_ack.py:1525` confere a contagem por fora do gerador. `check_fd_fx03_ack.py:1652` e `check_fd_fx03_ack.py:1661` falham se a regra ou a ocorrência não foi exercitada. `check_fd_fx03_ack.py:1679` declara que a entrada de produto não é exaustiva.
- Neste turno o autor observou 480/480 regras e 2239/2239 ocorrências, `gap=0`. Isso é `PASS_FIXTURE_ONLY`. Não fecha o finding.
- Status: CANDIDATE. NEW-LOW-03 permanece PARTIAL até o Codex. FD11-NEW-01 não é fechado aqui.

## NEW-MEDIUM-09

- Causa: o blob do parecer v0.2 contém `FAIL` no cabeçalho e `FAIL — DOCUMENT-ONLY` no fecho, com o corpo duplicado.
- Texto: CMP-FD-16 cita o blob `2d992a9cf0ab38d639b95f69df1571eb97f444b4` e o SHA-256 `575e149c3e29203c9c5b7c6532f15b06af6c562551372077502eaf50b246daef`. `chosen_verdict` fica null. `check_fd_historical_manifest.py:167` recusa aprovação inventada. `check_fd_historical_manifest.py:287` recusa `chosen_verdict` preenchido. `check_fd_historical_manifest.py:211` compara `bytes` com o tamanho do blob. `check_fd_historical_manifest.py:291` rejeita `bytes+1`. `check_fd_historical_manifest.py:328` mantém `PARECER_CHAIN NOT_FULLY_VERIFIED`. `check_fd_historical_manifest.py:49` extrai o texto do blob. `check_fd_historical_manifest.py:24` aceita o rótulo `Checkout examinado`, que é o rótulo real do parecer v0.11.
- v0.5 e v0.6: ausência legítima. Prompts v0.6 e v0.7: ausentes. O prompt v0.12 está no parent e entra na lista presente.
- Status: PARTIAL. NOT_VERIFIED até ato humano. Não é fechamento. O `BYTES MATCH` autoral não substitui auditoria.

## NEW-LOW-02

- O parecer da v0.11 fechou este item como CLOSED documental, não executado. Esta pasta não o reabre e não o transforma em prova de produto.

## FD07-07

- Texto: CMP-FD-13. Dois backends, barreira, as duas ordens, rollback e locks continuam especificados e não executados.
- Status: OPEN. O92 e O93 NOT RUN.

## HIGH-03

- Status: PARTIAL. Sem a evidência de O92.

## Preservados

FD07-01..06, FD07-08, NEW-MEDIUM-07, NEW-MEDIUM-08 e FD07-09 no escopo dos blobs de planejamento permanecem CLOSED documentalmente. A fixture `fixtures/CMP-FD-FX-03-ack.json:543` continua `n=-1`. O replay do 422, o 409 sem troca da linha e o 404 de tenant não foram afrouxados. NEW-MEDIUM-06 permanece CLOSED documentalmente. Migration NOT RUN.

## LOW-01

- Texto: CMP-FD-07. Pessoa PENDING. Effort UNSTATED. DoR NOT MET.
- Status: OPEN BLOCKING DoR.

## Não redispostos

HIGH-01, HIGH-02, NEW-HIGH-01, NEW-HIGH-02, NEW-MEDIUM-01, NEW-MEDIUM-02, NEW-MEDIUM-04 e MEDIUM-01..05 permanecem fechados pelo Codex. NEW-HIGH-04, NEW-HIGH-03, NEW-MEDIUM-05 e NEW-MEDIUM-03 continuam CANDIDATE.
