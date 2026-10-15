# CMP-FD-10 v0.8 — Disposição

**Estado:** CANDIDATE FOR CODEX REVIEW, salvo o que outro parecer já fechou e salvo LOW-01. O autor não escreve PASS e não fecha FD07-05..FD07-09.

## FD07-05

- Causa: a v0.7 classificava `n < 0` no checker e na norma, mas o conjunto obrigatório não tinha `ack_of_sequence < 0`. Vários campos de efeito eram só declaração.
- Texto: CMP-FD-02:32 define `422 ACK_REGRESSION` no estágio `negative`, antes do peer. CMP-FD-02:47-64 exige os campos de efeito e nomeia `FX03-NEGATIVE-SEQUENCE`. A fixture:543 é `n=-1`. A fixture:558-560 mantém high-water 2 e o código. O checker:172 devolve o estágio `negative`. O checker:404 recusa mutação de campo declarado.
- Negativo: O84 e O85, CMP-FD-07:15 e CMP-FD-07:19. NOT RUN.
- Status: CANDIDATE.

## FD07-06

- Causa: a v0.7 não tinha `receiver_participant_id` e o checker olhava um inteiro só.
- Texto: CMP-FD-02:14 é a chave com sessão, stream e receiver, dentro do tenant. CMP-FD-02:28-30 são tenant errado, receiver ausente e stream não alocado, sem lock cruzado. O checker:160-166 aplica essa ordem depois do par null. O checker:442 percorre o mapa. O checker:468 falha se a mutação mexe em outra chave.
- Negativo: O86, O87 e O88, CMP-FD-07:23, CMP-FD-07:27 e CMP-FD-07:31. NOT RUN.
- Status: CANDIDATE. O mapa não é o lock.

## FD07-07

- Causa: as linhas chamadas race na v0.7 são replay sequencial.
- Texto: CMP-FD-13:20-21 é `INSERT ... ON CONFLICT DO NOTHING`. CMP-FD-13:26 pede `SELECT ... FOR UPDATE`. CMP-FD-13:38 guarda o `UPDATE` com `:n > peer_ack_high_water`. CMP-FD-13:45-55 é o teste futuro das duas ordens e dos trios distintos. CMP-FD-02:76 diz que o replay da fixture não é essa corrida.
- Negativo: O92 e O93, CMP-FD-07:47 e CMP-FD-07:51. NOT RUN. Nenhum PostgreSQL foi aberto.
- Status: CANDIDATE. Não executado.

## FD07-08

- Causa: a duplicata da v0.7 conferia o inteiro e não a identidade durável nem `zero_new_effect`.
- Texto: CMP-FD-02:33-35 separam replay, chave reusada e `event_id`. CMP-FD-02:68-72 usa `forge.command_commit` e `forge.event.v1`, sem ledger novo, e define o crash antes do commit. O checker:223 distingue replay de digest diferente. O checker:235 deduplica `event_id`. O checker:518-532 modela rollback e o retry que não é replay.
- Negativo: O89, O90, O91, O94 e O95, CMP-FD-07:35, CMP-FD-07:39, CMP-FD-07:43, CMP-FD-07:55 e CMP-FD-07:59. NOT RUN.
- Status: CANDIDATE. O modelo de rollback não é o oráculo.

## FD07-09

- Causa: a rastreabilidade anterior chamava v0.5 e v0.6 de auditadas. Não há parecer desses pacotes no clone.
- Texto: CMP-FD-14:5. CMP-FD-14:17-18 registram ausência. CMP-FD-14:13-16 e CMP-FD-14:19 copiam só pareceres existentes. O manifest lista 91 SHA-256 e a igualdade com o parent.
- Negativo: não se inventa veredito. O checker do manifest recusa parecer de v0.5 ou v0.6.
- Status: CANDIDATE.

## HIGH-03

- Status: PARTIAL. Os textos acima não bastam. O92 não foi executado. O71..O83 continuam NOT RUN.

## NEW-MEDIUM-06

- Status: CLOSED documentalmente pelo parecer da v0.7. Opção B, null ativo antes do índice, predicado sem `task.status`. Esta pasta não edita a v0.6. Migration NOT RUN. O79 e O80 NOT RUN.

## LOW-01

- Texto: CMP-FD-07:9-11. Pessoa PENDING. Effort UNSTATED. DoR NOT MET.
- Status: OPEN BLOCKING DoR. Não é CANDIDATE de fechamento.

## Não redispostos

FD07-01, FD07-02, FD07-03 e FD07-04 permanecem CLOSED documentalmente pelo parecer da v0.7. NEW-MEDIUM-01 permanece CLOSED pelo Codex. HIGH-01, HIGH-02, NEW-HIGH-01, NEW-HIGH-02, NEW-MEDIUM-02, NEW-MEDIUM-04 e MEDIUM-01..05 permanecem fechados pelo Codex. NEW-HIGH-04, NEW-HIGH-03, NEW-MEDIUM-05 e NEW-MEDIUM-03 continuam CANDIDATE. Esta página não os reabre e não os confirma de novo.
