# CMP-FD-10 v0.9 — Disposição

**Estado:** CANDIDATE FOR CODEX REVIEW, salvo o que outro parecer já fechou e salvo LOW-01 e FD07-07. O autor não escreve PASS e não fecha FD07-08 nem FD07-09.

## FD07-08 e NEW-MEDIUM-07

- Causa: o modelo da v0.8 guardava só o digest e fabricava `IDEMPOTENT_REPLAY`, sem `original_outcome_code`, `original_outcome_body` nem `outcome_digest`.
- Texto: CMP-FD-02:43-45 nomeia os quatro campos. CMP-FD-02:47 separa transporte 200 do outcome guardado. CMP-FD-02:19 é o replay. CMP-FD-02:31 põe esse lookup depois do tenant e antes do receiver mutável. O checker:263 lê a linha. O checker:268 devolve o replay. O checker:308-309 grava o outcome. A fixture:1018 é transporte 200. A fixture:1019 é original 422. A fixture:1021 é o corpo `ACK_FUTURE`.
- Negativo: O96, O97, O98 e O99, CMP-FD-07:15, CMP-FD-07:19, CMP-FD-07:23 e CMP-FD-07:27. NOT RUN. O checker:659 mostra o receiver removido só no modelo. O checker:698 bloqueia o outro tenant só no modelo.
- Status: CANDIDATE. Não é fechamento.

## FD07-09 e NEW-MEDIUM-08

- Causa: o manifest da v0.8 não abria os dois commits, aceitava um boolean e omitia o diretório v0.1.
- Texto: CMP-FD-14:7 inclui `docs/planning/conversational-full-duplex/`. CMP-FD-14:13-14 fixam `base_sha` e `parent_sha`. CMP-FD-14:16 exige os dois hashes e recusa boolean. CMP-FD-14:26-27 registram v0.5 e v0.6 sem parecer. CMP-FD-14:29 coloca o parecer da v0.8 no parent, não no commit auditado. CMP-FD-14:31 registra a ausência dos prompts v0.6 e v0.7.
- Negativo: sem `--repo` a comparação é NOT_RUN. Com repositório, a saída é `GIT_BLOB_COMPARE MATCH READ_ONLY`, não PASS.
- Status: CANDIDATE.

## FD07-07

- Texto: CMP-FD-13:11 conserva `ON CONFLICT DO NOTHING`, `SELECT ... FOR UPDATE` e `:n > peer_ack_high_water`. CMP-FD-13:19-25 pede dois backends, barreira, as duas ordens, rollback e locks. CMP-FD-13:27 diz que a fixture sequencial não substitui isso.
- Status: OPEN. O92 e O93 NOT RUN. Nenhum PostgreSQL foi aberto.

## FD07-05

- Preservado como CLOSED documental pelo parecer da v0.8.
- Acréscimo pedido por aquele parecer: o checker:514 muta `expected_stage` e o checker:518 muta `peer_ack_high_water_before`. A fixture:543 continua `n=-1`. A fixture:561 continua estágio `negative`. O pré-lock não grava `command_commit`.
- Status: CLOSED documental. O autor não reabre e não promove a execução.

## FD07-06

- Preservado como CLOSED documental pelo parecer da v0.8.
- A chave continua `(organization_id, project_id, session_id, ack_stream_id, receiver_participant_id)`. CMP-FD-02:18 é o 404 de outro tenant, antes do lookup. O par null continua nos passos 1 e 2, CMP-FD-02:16-17.
- Status: CLOSED documental, com o mesmo limite estático. Lock real não demonstrado.

## HIGH-03

- Status: PARTIAL. O92 não foi executado. CMP-FD-02:5.

## NEW-MEDIUM-06

- Status: CLOSED documentalmente. Opção B permanece na v0.6. Esta pasta não a edita. Migration NOT RUN.

## LOW-01

- Texto: CMP-FD-07:5-7. Pessoa PENDING. Effort UNSTATED. DoR NOT MET.
- Status: OPEN BLOCKING DoR.

## Não redispostos

FD07-01 a FD07-04 permanecem CLOSED documentalmente. NEW-MEDIUM-01 permanece CLOSED pelo Codex. HIGH-01, HIGH-02, NEW-HIGH-01, NEW-HIGH-02, NEW-MEDIUM-02, NEW-MEDIUM-04 e MEDIUM-01..05 permanecem fechados pelo Codex. NEW-HIGH-04, NEW-HIGH-03, NEW-MEDIUM-05 e NEW-MEDIUM-03 continuam CANDIDATE.
