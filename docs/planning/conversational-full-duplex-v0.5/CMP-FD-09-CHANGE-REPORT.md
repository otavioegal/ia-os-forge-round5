# CMP-FD-09 v0.5 — Change report

**Estado:** PROPOSTA. Não é PASS. Não edita v1.7, CMP v0.3, full-duplex v0.1, v0.2, v0.3 ou v0.4, ata, ADR ou parecer.

A v0.4 corrigiu `RecordReceipt` e deixou `ApplyAuthorizedReconciliation` fora da fatia. Esta pasta aplica `S + H - E + A <= L` a todo comando que insere `SETTLEMENT`, sob Build `FOR UPDATE` primeiro. Se o apply de `PROVEN_RECEIPT` não cabe, não há movimento, a reservation fica `HELD`, a operation fica `BLOCKED_RECONCILIATION`, a autorização não é consumida e o pending `SESSION_SLICE` é append-only. A correlação com um settlement posterior é projeção sobre `settles_proof_id`, sem update e sem delete do pending.

A migration deixa de dizer que a coluna nova nasce NOT NULL só nas linhas novas. O desenho é: coluna anulável, backfill por join, abortar órfão, unique `(organization_id, project_id, id)` em Operation, FK `NOT VALID`, `VALIDATE`, `SET NOT NULL`. A flag permanece desligada.

O ACK ganha `ack_stream_id`, separado do `stream_id` do evento. High-water de emissão e high-water de peer são chaves diferentes. `PREAMBLE_AUTH` cobre principal divergente, com zero efeito.

O verificador passa a exigir bijeção, chave JSON única e formato de hash. A amostra `i=1199` fica em 28000. A saturação vai para `i=1159`, mic 32767. O índice único de sessão é SQL com `session_status`, não com `task.status`.

O replay continua antes do CAS. A resposta separa `transport_status=200` de `original_outcome_code`.

Nada disso foi executado como migration, oracle ou BUILD-00. LOW-01 não mudou: pessoa PENDING, effort UNSTATED, DoR NOT MET.
