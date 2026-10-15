# CMP-FD-14 v0.9 — Cadeia e blobs dos dois commits

**Estado:** correção de rastreabilidade. Não é PASS. Não cria parecer. Não altera arquivo histórico.

v0.5/v0.6 candidatos, sem parecer independente incorporado.

O escopo dos arquivos comparados é explícito. Inclui o pacote histórico v0.1 em `docs/planning/conversational-full-duplex/`, mais `conversational-full-duplex-v0.2` até `v0.8`. Não é “v0.2 até v0.7” com o v0.1 de fora. A v0.9 não entra nessa lista.

Os dois commits comparados são:

| Papel | SHA |
|---|---|
| base_sha, v0.8 auditada | `9fd88bb03e4cca4a1ee5126d5b595e028e2602b2` |
| parent_sha, HEAD com o parecer da v0.8 | `aca5101d3684109175269b36c3cace2051a71c91` |

Cada path do manifest tem `base_git_blob`, `parent_git_blob`, `base_sha256` e `parent_sha256`, lidos dos blobs. Não há boolean `same_at_base_and_parent`. O checker sem `--repo` imprime `GIT_BLOB_COMPARE NOT_RUN` e sai 2. Com repositório, relê os dois commits. Isso não é auditoria do Codex e não é PASS.

Pareceres que existem, com o veredito do próprio arquivo:

| Pacote | SHA auditado no arquivo | Veredito | No base_sha |
|---|---|---|---|
| v0.1 | `97ee817ca8262b3a0bae996c510b935435b2e575` | FAIL — DOCUMENT-ONLY | sim |
| v0.2 | `18aa352e7bf987aa3a2550b2e2b3251ce71c1f7d` | FAIL | sim |
| v0.3 | `2fe0b0b2b75f2fc1430f639839e2d29d563f6dcb` | FAIL DOCUMENT-ONLY | sim |
| v0.4 | `90fc21c90402805959bab2fc4ae6b43dc758c66d` | FAIL DOCUMENT-ONLY | sim |
| v0.5 | nenhum | nenhum | não há parecer |
| v0.6 | nenhum | nenhum | não há parecer |
| v0.7 | `1a71dfa44fc2c88174c113e5c68eddc18d6cfad3` | FAIL DOCUMENT-ONLY | sim |
| v0.8 | `9fd88bb03e4cca4a1ee5126d5b595e028e2602b2` | FAIL DOCUMENT-ONLY | não. O parecer entrou no parent_sha |

Não existem `PROMPT-GROK-FULL-DUPLEX-v0.6-CORRECTIVE.md` nem `PROMPT-GROK-FULL-DUPLEX-v0.7-CORRECTIVE.md`. Um prompt não é parecer. Esta página não inventa essa cadeia.
