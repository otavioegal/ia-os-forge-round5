# CMP-FD-14 v0.11 — Cadeia lida dos blobs

**Estado:** CANDIDATE. Não é PASS. Não cria parecer. Não altera arquivo histórico. Não escolhe o veredito do v0.2.

v0.5/v0.6 candidatos, sem parecer independente incorporado. Essa ausência é legítima nos dois commits.

| Papel | SHA |
|---|---|
| base_sha, v0.10 auditada | `a5d7e8fc85cb5b5f0605937b43075ce1a0c19e08` |
| parent_sha, HEAD com o parecer da v0.10 | `2e947d0222f184a3735ead6422b2fc054ea231df` |

O escopo dos blobs de planejamento inclui `docs/planning/conversational-full-duplex/` e `conversational-full-duplex-v0.2` até `v0.10`. A v0.11 não entra. Cada entrada tem `base_sha256`, `parent_sha256`, os dois blobs Git e `bytes`. O checker compara `bytes` com o comprimento real do blob. Não há boolean `same_at_base_and_parent`.

Cada parecer incorporado é aberto com `git cat-file`. A data no nome não é a versão. O parecer da v0.10 está no parent e não no commit auditado. Os prompts v0.6 e v0.7 continuam ausentes. Os prompts presentes são exatamente os do parent, inclusive o da v0.11. Um prompt não é parecer.

O v0.2 continua **NOT_VERIFIED**. A proposta de errata está em CMP-FD-16 e aguarda aprovação humana. A cadeia continua `PARECER_CHAIN NOT_FULLY_VERIFIED`. Sem `--repo` a comparação sai `NOT_RUN`.
