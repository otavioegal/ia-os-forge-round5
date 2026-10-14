# CMP-FD-00 v0.5 — Índice

**Estado do pacote:** CANDIDATE FOR CODEX REVIEW. Não é PASS. O autor não fecha finding.
**SHA auditado que esta pasta não altera:** `90fc21c90402805959bab2fc4ae6b43dc758c66d`
**Parecer:** `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.4-2026-10-14.md`
**Flag proposta:** `forge.conversation.delta.v4`, desligada. `forge.conversation.delta.v3` não é integrada.
**Migration, deploy, provider e BUILD-00:** não executados e não autorizados.

| Arquivo | Papel |
|---|---|
| CMP-FD-01-LEDGER-SETTLEMENT.md | Fatia em todo `SETTLEMENT`, inclusive apply manual |
| CMP-FD-02-MEDIA-ACK.md | `ack_stream_id`, high-water e `PREAMBLE_AUTH` |
| CMP-FD-03-LIFECYCLE.md | MEDIUM-01 preservado |
| CMP-FD-04-POLICY.md | MEDIUM-02 e MEDIUM-03 preservados; preâmbulo aponta para `PREAMBLE_AUTH` |
| CMP-FD-05-UX.md | MEDIUM-04 preservado |
| CMP-FD-06-OBSERVABILITY.md | MEDIUM-05 preservado; sem SLA |
| CMP-FD-07-ORACLES.md | O53..O70 e a conta AEC corrigida. Todos NOT RUN |
| CMP-FD-08-TRACEABILITY.md | Achado para texto |
| CMP-FD-09-CHANGE-REPORT.md | O que esta pasta acrescenta |
| CMP-FD-10-FINDING-DISPOSITION.md | Causa, texto, path:line, negativo, status CANDIDATE |
| CMP-FD-11-OPEN-QUESTIONS.md | O que continua pendente de ato humano |
| CMP-FD-12-CONSISTENCY-REPORT.md | Checagem cruzada e a suíte estática |
| CMP-FD-13-MIGRATION.md | Backfill, FK, unique e SQL do índice de sessão. Não executada |
| fixtures/CMP-FD-FX-01-events.json | Oito eventos, agora com `ack_stream_id` null |
| fixtures/CMP-FD-FX-01-digest-vectors.json | `canonical_utf8` para SHA-256 |
| fixtures/CMP-FD-FX-02-ack.json | ACK positivo e negativo, mais `PREAMBLE_AUTH` |
| fixtures/negative/ | Duplicata, vetor órfão, chave repetida, hash inválido, tipo inválido |
| tools/check_fd_fx01_digests.py | Verificador estático de digest |
| tools/check_fd_fx01_static_suite.py | Roda positivos e negativos. Não é teste de produto |
| tools/check_fd_fx02_ack.py | Forma da FX-02. Não executa o protocolo |
| tools/check_fd_aec_arithmetic.py | Conta da fixture AEC. Não é o componente AEC |

LOW-01 permanece OPEN BLOCKING DoR. Os findings que o Codex fechou na v0.4 não são reabertos por este índice.
