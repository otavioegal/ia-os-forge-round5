# CMP-FD-14 v0.10 — Cadeia lida dos blobs

**Estado:** CANDIDATE. Não é PASS. Não cria parecer. Não altera arquivo histórico.

v0.5/v0.6 candidatos, sem parecer independente incorporado. Essa ausência é legítima: nenhum blob `PARECER-CODEX-FULL-DUPLEX-v0.5` ou `v0.6` existe em qualquer dos dois commits.

Os commits comparados são:

| Papel | SHA |
|---|---|
| base_sha, v0.9 auditada | `422277f82efbc001140b5857095c4840e668e270` |
| parent_sha, HEAD com o parecer da v0.9 | `311e2cf76db6fb2294745b9415f1ae829c883fa7` |

O escopo dos blobs de planejamento inclui `docs/planning/conversational-full-duplex/` e `conversational-full-duplex-v0.2` até `v0.9`. A v0.10 não entra. Não há boolean `same_at_base_and_parent`.

Cada parecer incorporado é aberto com `git cat-file`. O checker compara o SHA e o veredito extraídos do arquivo com o manifest. Metadata declarada sozinha não basta. A data no nome do arquivo não é a versão.

Os rótulos não são uniformes: `SHA congelado auditado`, `SHA declarado do checkout`, `SHA auditado`, `Checkout submetido` e `Checkout auditado`. Onde o cabeçalho e o veredito final são a mesma string, o status é VERIFIED. O v0.2 não é: o cabeçalho diz `FAIL` e o veredito final diz `FAIL — DOCUMENT-ONLY`, e o corpo está duplicado. O SHA do v0.2 confere. O veredito fica **NOT_VERIFIED**. Nenhum dos dois textos é promovido. Por isso a cadeia inteira fica `PARECER_CHAIN NOT_FULLY_VERIFIED`.

O parecer da v0.9 está no parent_sha e não no commit auditado. Os prompts corretivos v0.6 e v0.7 continuam ausentes. Um prompt não é parecer. Sem `--repo` a comparação sai `NOT_RUN`.
