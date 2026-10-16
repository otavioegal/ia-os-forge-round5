# CMP-FD-18 v0.15 — Referência semântica, não ratificada

**Estado:** CANDIDATE. Não é golden humano. Não é PASS. NEW-GOV-01 permanece OPEN.

`fixtures/CMP-FD-FX-05-semantic-reference.json` continua candidato desta sessão. `ratification` é `PENDING_HUMAN_APPROVAL`. `independence` é `NOT_RATIFIED`. `new_gov_01` é `OPEN`. Outro valor devolve `FAIL_INVENTED_APPROVAL`.

Os campos `schema_sha256`, `fixture_sha256` e `synthetic_sha256` são o digest textual de `tools/canonical_json_text.py`, não o id do blob Git. LF e CRLF do mesmo JSON produzem esse digest. Uma edição real produz outro. A comparação não foi retirada: `check_fd_fx03_ack.py:1472`.

`SAME_AUTHOR_BOTH_SIDES not_detected` continua impresso. Normalizar fim de linha não cria um golden ratificado.
