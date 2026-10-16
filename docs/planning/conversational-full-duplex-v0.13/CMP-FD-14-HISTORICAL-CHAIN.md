# CMP-FD-14 v0.13 — Cadeia lida dos blobs

**Estado:** CANDIDATE. Não é PASS. Não cria parecer. Não altera arquivo histórico. Não escolhe o veredito do v0.2.

| Papel | SHA |
|---|---|
| Base, v0.12 auditada | `346cd04ae90bf57f4594e1a4b4af0584961dd546` |
| Parent, parecer v0.12 e prompt v0.13 | `cfb1c98412d4c183b406d919fabbe753ac43076b` |
| Tree do parent | `81cc3fec733daf91729a659b8f47bb62a797ff5e` |

Escopo: o diretório v0.1 e as pastas v0.2 a v0.12. 174 paths. Os blobs e os SHA-256 coincidem nos dois commits. `bytes` é o tamanho lido por `git cat-file`, conferido em `check_fd_historical_manifest.py:241`. A pasta v0.13 é rejeitada se aparecer nesse manifesto: `check_fd_historical_manifest.py:175`. A v0.12 entra no escopo porque já está publicada. O manifesto não se inclui.

v0.5 e v0.6 continuam ABSENT_LEGITIMATE. O parecer v0.12 está no parent e não na base. O rótulo de SHA dele é `Checkout examinado`. Cabeçalho e fecho são FAIL DOCUMENT-ONLY. SHA e veredito saem VERIFIED nessa leitura autoral. A data no nome do arquivo não é a versão.

v0.2: SHA `18aa352e7bf987aa3a2550b2e2b3251ce71c1f7d` VERIFIED. Cabeçalho `FAIL`. Fecho `FAIL — DOCUMENT-ONLY`. `verdict_status` NOT_VERIFIED. `duplicate_header_count` 2. Blob `2d992a9cf0ab38d639b95f69df1571eb97f444b4`. SHA-256 `575e149c3e29203c9c5b7c6532f15b06af6c562551372077502eaf50b246daef`. `chosen_verdict` null.

Prompts ausentes: v0.6 e v0.7. Prompts presentes no parent: v0.2, v0.3, v0.4, v0.5, v0.8, v0.9, v0.10, v0.11, v0.12 e v0.13.

Chave JSON duplicada no manifesto é `FAIL_DUPLICATE_KEY` em `check_fd_historical_manifest.py:45`, antes de qualquer comparação de blob.

Sem `--repo` a comparação fica NOT_RUN e o processo sai 2, depois de rejeitar a chave duplicada injetada. Com `--repo` o autor viu `REHASHED 174`, `PLANNING_BLOBS MATCH READ_ONLY`, `BYTES MATCH` e `PARECER_CHAIN NOT_FULLY_VERIFIED`. Esse último não é defeito de execução: a cadeia fica incompleta enquanto o v0.2 não tiver ato humano. O relato não é auditoria independente. FD07-09 continua CLOSED só para blobs de planejamento já publicados. Os bytes novos desta pasta são READ_ONLY do autor, não auditoria independente.
