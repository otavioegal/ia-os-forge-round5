# CMP-FD-17 v0.15 — Cobertura quantitativa

**Estado:** relato do autor. Não é PASS. `gap=0` não fecha FD11-NEW-01, NEW-LOW-03 nem NEW-GOV-01. `COVERAGE_TOTAL_PASS` não é reivindicado. `FULL_PRODUCT_COVERAGE false`. `PASS_FIXTURE_ONLY` não é oráculo e não é prova de produto.

480 e 2239 continuam rejeitados. A conta observada de novo, nos dois checkouts, foi 508 regras e 2443 ocorrências. A lista está em `fixtures/CMP-FD-FX-07-coverage-ids.json`. O fim de linha não entra nessa conta: a regressão em `check_fd_fx03_ack.py:1203` mostra que LF e CRLF não mudam o digest, e que um byte a mais muda.

O número 308 é a quantidade de literais da referência, não uma regra de mutação nova. A referência segue `PENDING_HUMAN_APPROVAL`.
