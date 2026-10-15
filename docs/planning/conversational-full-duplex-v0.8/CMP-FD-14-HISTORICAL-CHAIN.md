# CMP-FD-14 v0.8 — Cadeia de pareceres

**Estado:** correção de rastreabilidade. Não é PASS. Não cria parecer. Não altera arquivo histórico.

v0.5/v0.6 candidatos, sem parecer independente incorporado.

Foram procurados os nomes `PARECER-CODEX-FULL-DUPLEX-v0.5*` e `PARECER-CODEX-FULL-DUPLEX-v0.6*` no clone. Não existem. Um prompt corretivo não é parecer. Esta página não inventa SHA auditado nem veredito para esses dois pacotes.

Pareceres independentes que estão no repositório, com o SHA e o veredito escritos no próprio arquivo:

| Pacote | Arquivo | SHA auditado no arquivo | Veredito no arquivo | No commit `1a71dfa44fc2c88174c113e5c68eddc18d6cfad3` |
|---|---|---|---|---|
| v0.1 | `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.1-2026-10-13.md` | `97ee817ca8262b3a0bae996c510b935435b2e575` | FAIL — DOCUMENT-ONLY | sim |
| v0.2 | `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.2-2026-10-13.md` | `18aa352e7bf987aa3a2550b2e2b3251ce71c1f7d` | FAIL | sim |
| v0.3 | `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.3-2026-10-14.md` | `2fe0b0b2b75f2fc1430f639839e2d29d563f6dcb` | FAIL DOCUMENT-ONLY | sim |
| v0.4 | `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.4-2026-10-14.md` | `90fc21c90402805959bab2fc4ae6b43dc758c66d` | FAIL DOCUMENT-ONLY | sim |
| v0.5 | ausente | nenhum | nenhum | não há parecer |
| v0.6 | ausente | nenhum | nenhum | não há parecer |
| v0.7 | `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.7-2026-10-15.md` | `1a71dfa44fc2c88174c113e5c68eddc18d6cfad3` | FAIL DOCUMENT-ONLY | não. Entrou depois, no commit do parecer |

O manifest `fixtures/CMP-FD-FX-04-historical-manifest.json` guarda o SHA-256 dos 91 arquivos de `docs/planning/conversational-full-duplex-v0.1` até `v0.7` no commit base. Os mesmos bytes foram relidos no parent `4caabeca6a183934f0f4c68bc182877dee4ffdf6`. A comparação é somente leitura. Não é auditoria e não é aprovação.

Chamar v0.5 ou v0.6 de auditadas, como fizeram índices anteriores, fica corrigido só nesta pasta. Os arquivos antigos não são editados.
