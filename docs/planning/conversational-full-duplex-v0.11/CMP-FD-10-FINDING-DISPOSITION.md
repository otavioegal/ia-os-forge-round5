# CMP-FD-10 v0.11 — Disposição

**Estado:** CANDIDATE FOR CODEX REVIEW, salvo o que outro parecer já fechou e salvo LOW-01 e FD07-07. O autor não escreve PASS e não fecha NEW-MEDIUM-09, NEW-LOW-02 nem NEW-LOW-03.

## NEW-MEDIUM-09

- Causa: o blob do parecer v0.2 contém `FAIL` no cabeçalho e `FAIL — DOCUMENT-ONLY` no fecho, com o corpo duplicado.
- Texto: CMP-FD-16 cita o blob `2d992a9cf0ab38d639b95f69df1571eb97f444b4` e o SHA-256 `575e149c3e29203c9c5b7c6532f15b06af6c562551372077502eaf50b246daef`. `chosen_verdict` fica null. O checker histórico:166 recusa aprovação inventada. O checker histórico:211 compara `bytes` com o tamanho do blob. O checker histórico:327 mantém `PARECER_CHAIN NOT_FULLY_VERIFIED`. O checker histórico:48 continua extraindo o texto do blob.
- v0.5 e v0.6: ausência legítima.
- Status: CANDIDATE. NOT_VERIFIED até ato humano. Não é fechamento.

## NEW-LOW-02 e NEW-LOW-03

- Causa: presença obrigatória já falhava em `FAIL_SCHEMA`, mas tipos e listas compostas ainda podiam seguir para o processamento.
- Texto: CMP-FD-15. O schema externo, linha 2, é a lista. O checker ACK:777 classifica UUID, inteiro, booleano, string, lista e mapa. O checker ACK:846 percorre o aninhado. O checker ACK:1124 troca o tipo de cada campo declarado. O checker ACK:1238 continua removendo os obrigatórios. Lista vazia, tamanhos desiguais e `executed_database=true` devolvem `FAIL_SCHEMA` antes da decisão de ACK.
- Status: CANDIDATE. Não é prova de produto.

## FD07-07

- Texto: CMP-FD-13. Dois backends, barreira, as duas ordens, rollback e locks continuam especificados e não executados.
- Status: OPEN. O92 e O93 NOT RUN.

## HIGH-03

- Status: PARTIAL. Sem a evidência de O92.

## Preservados

FD07-01..06, FD07-08, NEW-MEDIUM-07, NEW-MEDIUM-08 e FD07-09 no escopo dos blobs de planejamento permanecem CLOSED documentalmente. A fixture:543 continua `n=-1`. O replay do 422, o 409 sem troca da linha e o 404 de tenant não foram afrouxados. NEW-MEDIUM-06 permanece CLOSED documentalmente. Migration NOT RUN.

## LOW-01

- Texto: CMP-FD-07. Pessoa PENDING. Effort UNSTATED. DoR NOT MET.
- Status: OPEN BLOCKING DoR.

## Não redispostos

HIGH-01, HIGH-02, NEW-HIGH-01, NEW-HIGH-02, NEW-MEDIUM-01, NEW-MEDIUM-02, NEW-MEDIUM-04 e MEDIUM-01..05 permanecem fechados pelo Codex. NEW-HIGH-04, NEW-HIGH-03, NEW-MEDIUM-05 e NEW-MEDIUM-03 continuam CANDIDATE.
