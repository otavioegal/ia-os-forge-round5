# CMP-FD-00 v0.12 — Índice

**Estado do pacote:** CANDIDATE FOR CODEX REVIEW. Não é PASS. O autor não fecha finding.
**SHA auditado da v0.11:** `9522d5b090d451cc61face6e23a3f0b5081bf62f`
**Parent desta pasta:** `3d4de1be8b6f683d66c2514b4847619bec9cdfe9`
**Migration, deploy, provider, gasto, PostgreSQL e BUILD-00:** não executados e não autorizados.
**`forge.conversation.delta.v4`:** desligada. A v3 não é integrada.

O parecer da v0.11 é FAIL DOCUMENT-ONLY. O schema da v0.11 foi aceito. A falha que esta pasta trata é a cobertura: `type_failures()` só via a primeira ocorrência de cada `kind` e o índice zero. Isso é NEW-LOW-03 PARTIAL e FD11-NEW-01. A correção é candidata. Não é fechamento.

| Peça | Papel |
|---|---|
| CMP-FD-02 | Replay, 409, 404, null-pair, `n<0` e zero movimento preservados |
| CMP-FD-07 | Oráculos NOT RUN. LOW-01 OPEN BLOCKING DoR |
| CMP-FD-08 | Rastreabilidade |
| CMP-FD-09 | Change report |
| CMP-FD-10 | Disposição. O autor não promove PASS |
| CMP-FD-11 | Questões abertas |
| CMP-FD-12 | Consistência. Relato do autor, não auditoria independente |
| CMP-FD-13 | Concorrência especificada e não executada |
| CMP-FD-14 | Cadeia lida dos blobs. v0.2 NOT_VERIFIED |
| CMP-FD-15 | Schema inalterado nas regras. Id v0.12 |
| CMP-FD-16 | Governança da v0.2. `chosen_verdict` null |
| CMP-FD-17 | Contagem declarada versus exercitada |
| fixtures/CMP-FD-FX-03-ack.json | 26 linhas de decisão. Não é oráculo |
| fixtures/CMP-FD-FX-03-ack.schema.json | Autoridade de nomes, tipos e cardinalidade |
| fixtures/CMP-FD-FX-03-ack.synthetic.json | Hosts sintéticos. `proves_product` false. `oracle_status` NOT_RUN |
| fixtures/CMP-FD-FX-04-historical-manifest.json | 155 paths. `bytes` comparado ao blob |
| tools/check_fd_fx03_ack.py | Checker estático. `PASS_FIXTURE_ONLY` não é PASS |
| tools/check_fd_historical_manifest.py | Sem `--repo`, exit 2 e NOT_RUN |

Nada aqui edita v0.1–v0.11, baseline, CMP v0.3, ata, ADR ou parecer.
