# CMP-FD-10 v0.5 — Disposição dos findings

**Estado de cada linha abaixo:** CANDIDATE FOR CODEX REVIEW, salvo onde está escrito OPEN BLOCKING ou CLOSED pelo Codex. O autor não escreve PASS e não fecha finding.

## NEW-HIGH-04

- Causa: a v0.4 aplicava a fatia só em `RecordReceipt`. `ApplyAuthorizedReconciliation` ainda podia liquidar pelo teto do Build, FDP-16A v1.7 `:344-350`.
- Texto: CMP-FD-01:32, fórmula `S + H - E + A <= L`, com H incluindo E na linha 35. Conjunto de comandos na linha 44. Apply na linha 97: se a fatia não comporta, zero settlement, reservation `HELD`, operation `BLOCKED_RECONCILIATION`, autorização não consumida, pending `SESSION_SLICE` append-only. Correlação sem update na linha 145. Corrida na linha 159. Fecho na linha 172, coluna `session_status` na linha 174.
- Negativo: O58, O59, O60, O61, O62 e O64, CMP-FD-07 linhas 37, 45, 51, 59, 63 e 71. NOT RUN.
- Status: CANDIDATE.

## NEW-HIGH-03

- Causa: a migration v0.4 não fazia backfill, não criava o unique que a FK composta exige e não levava as colunas a NOT NULL.
- Texto: CMP-FD-13 linhas 17, 60, 67, 70 e 73. Órfão aborta. Flag desligada até a validação. Predicado opaco em CMP-FD-01:180.
- Negativo: O55, O56, O57 e O70, CMP-FD-07 linhas 77 e seguintes da seção 3. NOT RUN.
- Status: CANDIDATE.

## HIGH-03

- Causa: o ack usava o `stream_id` do próprio evento, e o preâmbulo não comparava `principal_ref` com o principal autenticado.
- Texto: CMP-FD-02 linhas 27-31, `ack_stream_id`. High-water na linha 42. `ACK_STREAM_UNALLOCATED` na linha 55. `PREAMBLE_AUTH` na linha 73. `PLAYBACK_SPAN` e os seis carimbos continuam na linha 15. Sem half-duplex.
- Negativo: O65, O66, O67, CMP-FD-07 linhas 99 e 107. Fixture `fixtures/CMP-FD-FX-02-ack.json`. NOT RUN como protocolo.
- Status: CANDIDATE. O contrato de mídia não está aprovado.

## NEW-MEDIUM-05

- Causa: o verificador da v0.4 não via `event_id` duplicado nos eventos nem vetor não consumido, e `json.loads` aceitava chave repetida.
- Texto: `tools/check_fd_fx01_digests.py` linhas 17, 24, 35, 76 e 102. Bijeção, formato de `sha256`, tipo de `canonical_byte_length`, formato de `event_digest`.
- Negativo estático, não é teste de produto: `fixtures/negative/duplicate-event-id.json`, `orphan-vector.json`, `duplicate-key.json`, `bad-sha256.json`, `bad-length-type.json`.
- Status: CANDIDATE. `PASS_FIXTURE_ONLY` não é PASS do pacote.

## NEW-MEDIUM-03

- Causa: em `i=1199` o eco é -4000 e o humano é 32000, então o mic é 28000. A v0.4 dizia 32767.
- Texto: CMP-FD-07 linhas 127-130. Saturação em `i=1159`, soma 36000, mic 32767. `i=1199` permanece recuperável.
- Negativo: O53 e O54, linhas 154 e 158. O28 reescrito na linha 134. NOT RUN.
- Status: CANDIDATE.

## NEW-MEDIUM-06

- Causa: a migration dizia “status da task” e misturava `task.status` com `session_status`.
- Texto: CMP-FD-13 linhas 105-111. O predicado é `execution_domain = 'CONVERSATION'` e `session_status IN ('OPEN','CLOSING','ORPHAN_HELD')`. Duplicata histórica aborta na linha 100, sem apagar task.
- Negativo: O68, CMP-FD-07 linha 164, e O50. NOT RUN.
- Status: CANDIDATE.

## NEW-MEDIUM-01

- O Codex fechou este finding na v0.4. Esta pasta não o reabre.
- Clarificação pedida: CMP-FD-01 linhas 125-130. `transport_status=200`, `replay=true`, `original_outcome_code` e `original_outcome_body` são campos distintos. O lookup continua antes do CAS, linha 60.
- Negativo: O69, CMP-FD-07 linha 176. NOT RUN.
- Status: CLOSED pelo Codex, com texto editorial CANDIDATE. O autor não reemite o CLOSED.

## LOW-01

- Texto: CMP-FD-07 linhas 7-21. Pessoa PENDING. Effort UNSTATED. DoR NOT MET.
- Status: OPEN BLOCKING DoR. Não é CANDIDATE de fechamento.

## Já fechados pelo Codex, não redispostos

HIGH-01, HIGH-02, NEW-HIGH-01, NEW-HIGH-02, NEW-MEDIUM-02, NEW-MEDIUM-04, MEDIUM-01, MEDIUM-02, MEDIUM-03, MEDIUM-04, MEDIUM-05. A preservação está em CMP-FD-01 seção 1, CMP-FD-02 seção 1, CMP-FD-03, CMP-FD-04, CMP-FD-05 e CMP-FD-06.
