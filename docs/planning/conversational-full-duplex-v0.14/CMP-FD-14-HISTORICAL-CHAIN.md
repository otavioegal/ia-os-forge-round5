# CMP-FD-14 v0.14 — Cadeia lida dos blobs

**Estado:** CANDIDATE. Não é PASS. Não cria parecer. Não altera arquivo histórico. Não escolhe o veredito do v0.2. Não adota o cabeçalho da v0.13 como PASS deste pacote.

| Papel | SHA |
|---|---|
| Base, v0.13 auditada | `c7b08dc2a0127557293346ebd53e4ff43722683e` |
| Parent, parecer v0.13 e prompt v0.14 | `51d8ff2b89215470bbd6c8f99269301394d91083` |
| Tree do parent | `93ced75de5f9bb4a5b11ff7a7fac536fa1e77ec7` |

Escopo: o diretório v0.1 e as pastas v0.2 a v0.13. 193 paths. Os blobs e os SHA-256 coincidem nos dois commits. `bytes` é o tamanho lido por `git cat-file`, conferido em `check_fd_historical_manifest.py:241`. A pasta v0.14 é rejeitada se aparecer nesse manifesto: `check_fd_historical_manifest.py:175`. A v0.13 entra no escopo porque já está publicada. O manifesto não se inclui.

v0.5 e v0.6 continuam ABSENT_LEGITIMATE. O parecer v0.13 está no parent e não na base. O rótulo de SHA dele é `Checkout examinado`. O cabeçalho lido do blob é `PASS WITH CONDITIONS DOCUMENT-ONLY`. O extrator não achou a forma `Veredito final:` e gravou `final_verdict` null. `sha_status` e `verdict_status` saíram VERIFIED nessa leitura autoral do blob. Isso registra o que o arquivo diz. Não declara PASS de produto e não declara PASS desta v0.14.

v0.2: SHA `18aa352e7bf987aa3a2550b2e2b3251ce71c1f7d` VERIFIED. Cabeçalho `FAIL`. Fecho `FAIL — DOCUMENT-ONLY`. `verdict_status` NOT_VERIFIED. `duplicate_header_count` 2. Blob `2d992a9cf0ab38d639b95f69df1571eb97f444b4`. SHA-256 `575e149c3e29203c9c5b7c6532f15b06af6c562551372077502eaf50b246daef`. `chosen_verdict` null.

Prompts ausentes: v0.6 e v0.7. Prompts presentes no parent: v0.2, v0.3, v0.4, v0.5, v0.8, v0.9, v0.10, v0.11, v0.12, v0.13 e v0.14.

Chave JSON duplicada no manifesto é `FAIL_DUPLICATE_KEY` em `check_fd_historical_manifest.py:45`, antes de qualquer comparação de blob.

Sem `--repo` a comparação fica NOT_RUN e o processo sai 2. Com `--repo` o autor viu `REHASHED 193`, `PLANNING_BLOBS MATCH READ_ONLY`, `BYTES MATCH` e `PARECER_CHAIN NOT_FULLY_VERIFIED`. Esse último não é defeito de execução: a cadeia fica incompleta enquanto o v0.2 não tiver ato humano. O relato não é auditoria independente.
