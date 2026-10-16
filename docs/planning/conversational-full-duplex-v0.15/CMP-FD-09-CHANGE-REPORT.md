# CMP-FD-09 v0.15 — Change report

**Estado:** PROPOSTA. Não é PASS. Não edita v0.1 a v0.14, baseline, CMP, ata, ADR nem parecer. O commit `2b2adf382b17a22f1372aaf05b7d3bd1a6ba14ba` não foi reescrito.

Escopo: só reprodutibilidade do digest textual. As regras de ACK, a DSL, os 508 IDs e as 2443 ocorrências não mudam de significado. O id do schema passou a `cmp.fd.fx03.schema.v0.15` porque o pacote é outro. Isso não é regra nova de produto.

O que estava errado na v0.14: `check_fd_fx03_ack.py` daquele SHA, nas linhas 1196–1197, fazia `hashlib.sha256(path.read_bytes())`. Em `core.autocrlf=true` o checkout troca LF por CRLF. Os bytes mudam, o JSON não. A comparação em 1430–1437 daquele arquivo imprimia `SEMANTIC_DRIFT` e `FAIL_SEMANTIC_DRIFT` antes de `STATIC_ACK_V14_CHECK`. Com `core.autocrlf=false` o mesmo conteúdo passava. A auditoria não é reclassificada: aquele resultado continua o que foi observado.

O que esta pasta faz:

- `tools/canonical_json_text.py:11` normaliza CRLF e CR para LF. `canonical_json_sha256` está na linha 17. `canonical_json_file_sha256` está na linha 21.
- O checker importa essa função em `check_fd_fx03_ack.py:40` e a usa em `file_sha256`, linha 1198. A comparação continua em `check_fd_fx03_ack.py:1472`, `1474` e `1476`. Não foi removida.
- `tools/draft_semantic_reference.py:84` e `tools/enumerate_coverage_ids.py:40` chamam a mesma função. Não há uma segunda definição.
- `line_ending_regression` em `check_fd_fx03_ack.py:1203` prova que LF e CRLF do mesmo texto têm o mesmo digest, que os bytes crus diferem, e que inserir um byte muda o digest nas duas formas. Se a alteração de conteúdo não mudar o digest, o checker devolve `FAIL_CANONICAL_HASH` em `check_fd_fx03_ack.py:2428`.
- O manifesto histórico não usa esse digest. `check_fd_historical_manifest.py:250` compara `len(data)` do blob lido por `git cat-file`. Identidade de blob e digest textual ficam separados.

Não houve migration, PostgreSQL, provider, deploy, gasto nem BUILD-00. A flag permanece desligada. Nenhum finding mudou de estado.
