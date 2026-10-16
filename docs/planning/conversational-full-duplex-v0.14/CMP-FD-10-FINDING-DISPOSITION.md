# CMP-FD-10 v0.14 — Disposição

**Estado:** CANDIDATE FOR CODEX REVIEW. O autor não escreve PASS e não fecha NEW-GOV-01, FD11-NEW-01, NEW-LOW-03, NEW-MEDIUM-09, FD07-07, HIGH-03 nem LOW-01.

## FD12-NEW-01, FD12-NEW-02, FD12-NEW-03

O parecer da v0.13 fechou estes três só no limite documental/estático. FD12-NEW-03 ficou CLOSED estático, NOT RUN, porque o Codex não executou o checker. Esta pasta não reabre esse fechamento e não o promove a prova de produto. Objeto inline, elemento de array e chave duplicada continuam no checker: `check_fd_fx03_ack.py:1791`, `check_fd_fx03_ack.py:1849` e `check_fd_fx03_ack.py:2233`.

## FD11-NEW-01 — PARTIAL

A falha concreta da v0.12, catálogo incompleto, foi tratada na v0.13 e o parecer não a reabriu como omissão de inline ou de elemento. A independência semântica não foi provada. Esta pasta acrescenta referência externa e lista de IDs. A referência não está ratificada. Status: **PARTIAL**.

## NEW-LOW-03 — PARTIAL

O autor executou o checker e viu 508/508 e 2443/2443. O parecer da v0.13 não reproduziu esses números. A lista está em `fixtures/CMP-FD-FX-07-coverage-ids.json`. Isso é evidência autoral, `PASS_FIXTURE_ONLY`, não reprodução Codex e não cobertura de produto. Status: **PARTIAL**.

## NEW-GOV-01 — OPEN

Não existe golden ratificado por ato humano. O arquivo `fixtures/CMP-FD-FX-05-semantic-reference.json` é candidato, da mesma sessão de autoria, separado do gerador de mutação. `check_fd_fx03_ack.py:1414` recusa `ratification` diferente de `PENDING_HUMAN_APPROVAL`. A linha `SAME_AUTHOR_BOTH_SIDES not_detected` em `check_fd_fx03_ack.py:1471` declara o que o comparador não vê se todos os lados forem editados juntos. Status: **OPEN**. Não é fechamento.

## NEW-MEDIUM-09

O blob do parecer v0.2 continua `2d992a9cf0ab38d639b95f69df1571eb97f444b4`. SHA-256 `575e149c3e29203c9c5b7c6532f15b06af6c562551372077502eaf50b246daef`. Cabeçalho `FAIL`. Fecho `FAIL — DOCUMENT-ONLY`. `chosen_verdict` null. `check_fd_historical_manifest.py:197` recusa aprovação inventada. `check_fd_historical_manifest.py:317` recusa `chosen_verdict` preenchido. Status: **PARTIAL**. NOT_VERIFIED. A errata continua pendente.

## FD07-07

CMP-FD-13. Dois backends, barreira, as duas ordens, rollback e locks continuam especificados e não executados. Status: **OPEN**. O92 e O93 NOT RUN.

## HIGH-03

Status: **PARTIAL**. Sem a evidência de O92.

## LOW-01

Pessoa PENDING. Effort UNSTATED. DoR NOT MET. Status: **OPEN BLOCKING DoR**. O autor não inventa dono nem esforço.

## Preservados

FD07-01..06, FD07-08, NEW-MEDIUM-07, NEW-MEDIUM-08, NEW-LOW-02 e FD07-09 permanecem CLOSED no limite documental já dado. NEW-MEDIUM-06 permanece CLOSED documentalmente, migration NOT RUN. HIGH-01, HIGH-02, NEW-HIGH-01, NEW-HIGH-02, NEW-MEDIUM-01, NEW-MEDIUM-02, NEW-MEDIUM-04 e MEDIUM-01..05 permanecem fechados pelo Codex. NEW-HIGH-04, NEW-HIGH-03, NEW-MEDIUM-05 e NEW-MEDIUM-03 continuam CANDIDATE. A fixture `fixtures/CMP-FD-FX-03-ack.json:543` continua `ack_of_sequence` -1.

Nove AQs permanecem APPROVED: AQ-01, AQ-02, AQ-03, AQ-05, AQ-06, AQ-07, AQ-08, AQ-10, AQ-11. AQ-04, AQ-09 e AQ-12 permanecem DEFERRED. FDP-14, FDP-15, baseline e BUILD-00 permanecem PENDING.
