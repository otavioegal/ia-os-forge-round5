# CMP-FD-10 v0.10 — Disposição

**Estado:** CANDIDATE FOR CODEX REVIEW, salvo o que outro parecer já fechou e salvo LOW-01 e FD07-07. O autor não escreve PASS e não fecha NEW-MEDIUM-09 nem NEW-LOW-02.

## NEW-MEDIUM-09

- Causa: o checker da v0.9 não abria os pareceres v0.1–v0.4 e v0.7, nem a lista de prompts presentes.
- Texto: CMP-FD-14 fixa os dois SHAs e diz que a data do arquivo não é a versão. O checker histórico:48 extrai SHA e veredito do texto do blob. O checker histórico:212 recusa promover um veredito conflitante. O checker histórico:293 deixa a cadeia `NOT_FULLY_VERIFIED`.
- v0.5 e v0.6: ausência legítima, sem parecer inventado.
- v0.2: SHA verificado. Veredito NOT_VERIFIED. O cabeçalho é `FAIL` e o veredito final é `FAIL — DOCUMENT-ONLY`. O corpo está duplicado.
- Negativo estático, só com `--repo`: troca de SHA, veredito, path, omissão, prompt inventado, parecer v0.5 inventado e promoção do v0.2. Sem repositório, `PARECER_CHAIN NOT_RUN`.
- Status: CANDIDATE. Não é fechamento.

## NEW-LOW-02

- Causa: o checker da v0.9 validava o campo só quando ele já estava presente.
- Texto: CMP-FD-15. O arquivo `fixtures/CMP-FD-FX-03-ack.schema.json:2` é a lista. O checker ACK:782-783 devolve `FAIL_SCHEMA` se um nome obrigatório do documento falta, antes de indexar o resto. O checker ACK:860 faz o mesmo para o comando. O checker ACK:985 remove cada campo obrigatório. O checker ACK:1035 transforma exceção em `FAIL_SCHEMA_EXCEPTION`.
- Status: CANDIDATE. O checker não é prova de produto.

## FD07-07

- Texto: CMP-FD-13 conserva a SQL e a exigência de dois backends, barreira, as duas ordens, rollback e locks.
- Status: OPEN. O92 e O93 NOT RUN. Nenhum PostgreSQL foi aberto.

## HIGH-03

- Status: PARTIAL. Sem a evidência de O92.

## Preservados como o parecer da v0.9 os fechou

FD07-08, NEW-MEDIUM-07, FD07-09 no escopo dos blobs de planejamento, NEW-MEDIUM-08, FD07-05, FD07-06 e FD07-01..04 permanecem CLOSED documentalmente. A fixture:543 continua `n=-1`. O replay do 422 e o 404 de tenant não foram afrouxados. NEW-MEDIUM-06 permanece CLOSED documentalmente. Migration NOT RUN.

## LOW-01

- Texto: CMP-FD-07. Pessoa PENDING. Effort UNSTATED. DoR NOT MET.
- Status: OPEN BLOCKING DoR.

## Não redispostos

HIGH-01, HIGH-02, NEW-HIGH-01, NEW-HIGH-02, NEW-MEDIUM-01, NEW-MEDIUM-02, NEW-MEDIUM-04 e MEDIUM-01..05 permanecem fechados pelo Codex. NEW-HIGH-04, NEW-HIGH-03, NEW-MEDIUM-05 e NEW-MEDIUM-03 continuam CANDIDATE.
