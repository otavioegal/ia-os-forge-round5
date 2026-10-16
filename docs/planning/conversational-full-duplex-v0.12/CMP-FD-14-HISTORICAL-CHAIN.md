# CMP-FD-14 v0.12 — Cadeia lida dos blobs

**Estado:** CANDIDATE. Não é PASS. Não cria parecer. Não altera arquivo histórico. Não escolhe o veredito do v0.2.

| Papel | SHA |
|---|---|
| Base, v0.11 auditada | `9522d5b090d451cc61face6e23a3f0b5081bf62f` |
| Parent, parecer v0.11 e prompt v0.12 | `3d4de1be8b6f683d66c2514b4847619bec9cdfe9` |

Escopo: o diretório v0.1 e as pastas v0.2 a v0.11. 155 paths. Os blobs e os SHA-256 coincidem nos dois commits. `bytes` é o tamanho lido por `git cat-file`, conferido em `check_fd_historical_manifest.py:211`. A pasta v0.12 é rejeitada se aparecer nesse manifesto: `check_fd_historical_manifest.py:145`.

v0.5 e v0.6 continuam ABSENT_LEGITIMATE. O parecer v0.11 está no parent e não na base. O rótulo de SHA dele é `Checkout examinado`. A data no nome do arquivo não é a versão.

v0.2: SHA `18aa352e7bf987aa3a2550b2e2b3251ce71c1f7d` VERIFIED. Cabeçalho `FAIL`. Fecho `FAIL — DOCUMENT-ONLY`. `verdict_status` NOT_VERIFIED. `duplicate_header_count` 2. Blob `2d992a9cf0ab38d639b95f69df1571eb97f444b4`. SHA-256 `575e149c3e29203c9c5b7c6532f15b06af6c562551372077502eaf50b246daef`.

Prompts ausentes: v0.6 e v0.7. Prompts presentes no parent: v0.2, v0.3, v0.4, v0.5, v0.8, v0.9, v0.10, v0.11 e v0.12.

Sem `--repo` a comparação fica NOT_RUN e o processo sai 2. Com `--repo` o autor viu `PLANNING_BLOBS MATCH READ_ONLY`, `BYTES MATCH` e `PARECER_CHAIN NOT_FULLY_VERIFIED`. Esse último não é defeito de execução: a cadeia fica incompleta enquanto o v0.2 não tiver ato humano. O relato não é auditoria independente.
