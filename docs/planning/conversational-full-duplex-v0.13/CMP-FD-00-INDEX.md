# CMP-FD-00 v0.13 — Índice

**Estado do pacote:** CANDIDATE FOR CODEX REVIEW. Não é PASS. O autor não fecha finding.
**SHA auditado da v0.12:** `346cd04ae90bf57f4594e1a4b4af0584961dd546`
**Parent desta pasta:** `cfb1c98412d4c183b406d919fabbe753ac43076b`
**Migration, deploy, provider, gasto, PostgreSQL e BUILD-00:** não executados e não autorizados.
**`forge.conversation.delta.v4`:** desligada. A v3 não é integrada.

O parecer da v0.12 é FAIL DOCUMENT-ONLY. A falha que esta pasta trata é o catálogo incompleto: objetos inline e o tipo do elemento de array de objeto ficaram de fora, e chaves JSON duplicadas passavam. 480 regras e 2239 ocorrências eram a conta interna desse catálogo. Não são prova desta pasta. NEW-LOW-03, FD11-NEW-01, FD12-NEW-01, FD12-NEW-02 e FD12-NEW-03 ficam CANDIDATE. Não são fechamento.

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
| CMP-FD-15 | Schema. Regras de campo iguais. Id v0.13. Objetos inline entram no catálogo |
| CMP-FD-16 | Governança da v0.2. `chosen_verdict` null |
| CMP-FD-17 | Contagem de um passeio independente. Não é cobertura total |
| fixtures/CMP-FD-FX-03-ack.json | 26 linhas de decisão. Não é oráculo |
| fixtures/CMP-FD-FX-03-ack.schema.json | Autoridade de nomes, tipos e cardinalidade, inclusive objetos inline |
| fixtures/CMP-FD-FX-03-ack.synthetic.json | Hosts sintéticos. `proves_product` false. `oracle_status` NOT_RUN |
| fixtures/CMP-FD-FX-04-historical-manifest.json | 174 paths de v0.1 a v0.12. `bytes` comparado ao blob |
| tools/check_fd_fx03_ack.py | Checker estático. `PASS_FIXTURE_ONLY` não é PASS |
| tools/check_fd_historical_manifest.py | Sem `--repo`, exit 2 e NOT_RUN. Chave duplicada rejeitada |

Nada aqui edita v0.1–v0.12, baseline, CMP v0.3, ata, ADR ou parecer. `COVERAGE_TOTAL_PASS` não é reivindicado. `product_input_exhaustive=false`.
