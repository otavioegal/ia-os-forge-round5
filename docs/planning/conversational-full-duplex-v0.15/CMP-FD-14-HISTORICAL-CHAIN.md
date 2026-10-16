# CMP-FD-14 v0.15 — Cadeia lida dos blobs

**Estado:** CANDIDATE. Não é PASS. Não cria parecer. Não altera arquivo histórico. Não escolhe o veredito do v0.2. Não reescreve `2b2adf382b17a22f1372aaf05b7d3bd1a6ba14ba`.

| Papel | SHA |
|---|---|
| Base e parent | `2b2adf382b17a22f1372aaf05b7d3bd1a6ba14ba` |
| Por que são iguais | Não há commit de parecer posterior à v0.14. Os dois lados são o objeto auditado |

Escopo: o diretório v0.1 e as pastas v0.2 a v0.14. 218 paths. O id de blob, o SHA-256 dos bytes do blob e `bytes` vêm de `git cat-file`. Isso não é o digest textual LF/CRLF. `check_fd_historical_manifest.py:250` compara o tamanho do blob. Divergência devolve `FAIL_BYTES` na linha 251. A pasta v0.15 é `FAIL_SELF_HASH` em `check_fd_historical_manifest.py:184`.

v0.5 e v0.6 continuam ABSENT_LEGITIMATE. v0.14 não tem parecer nesse commit. O manifesto grava `NOT_INCORPORATED` e `check_fd_historical_manifest.py:24` recusa inventar o arquivo. Isso não é o mesmo que a ausência legítima de v0.5 e v0.6, e não é VERIFIED.

v0.2: cabeçalho `FAIL`, fecho `FAIL — DOCUMENT-ONLY`, `verdict_status` NOT_VERIFIED, `chosen_verdict` null. Blob `2d992a9cf0ab38d639b95f69df1571eb97f444b4`. SHA-256 `575e149c3e29203c9c5b7c6532f15b06af6c562551372077502eaf50b246daef`. O transcript autoral imprime `PARECER v0.2 sha=VERIFIED verdict=NOT_VERIFIED` e `PARECER_CHAIN NOT_FULLY_VERIFIED`.

Prompts ausentes: v0.6 e v0.7. O conjunto presente no parent foi conferido com `PROMPT_SET MATCH`.

Sem `--repo` a comparação fica NOT_RUN e o processo sai 2.
