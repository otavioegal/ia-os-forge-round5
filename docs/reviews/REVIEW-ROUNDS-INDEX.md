# Registro central de revisões — IA OS Forge

**Repositório:** https://github.com/otavioegal/ia-os-forge-round5  
**Função:** histórico versionado e auditável de baselines, correções e pareceres; não é banco de produção.

| Rodada | Baseline | Parecer independente | Status documental | Encaminhamento |
|---|---|---|---|---|
| 5 | v1.2 | [Codex Round 5](PARECER-CODEX-ROUND5-2026-10-13.md) | FAIL; 6 HIGH, 5 MEDIUM | Grok Round 6 |
| 6 | v1.3; commit `4e57839` | [Codex Round 6](PARECER-CODEX-ROUND6-2026-10-13.md) | FAIL; HIGH-01 parcial + NEW-HIGH-07 aberto | [Prompt Grok Round 7](PROMPT-GROK-ROUND7-LEDGER-CLOSURE.md) |
| 7 | v1.4 candidata nesta árvore | NÃO EMITIDO | ROUND 7 — CANDIDATE FOR CODEX REVIEW | Codex revisa o commit. Não é PASS. |

## Regra operacional

Preservar a baseline anterior em `historical/roundN/`; registrar commit exato auditado, parecer integral, findings, changelog, verificações documentais, pendências e índice. Não substituir pareceres nem declarar testes executados sem evidência. Cada revisão só fecha após parecer independente e gate humano quando cabível. Nada neste registro autoriza BUILD-00.

## Pendências que não são findings de prontidão documental

FDP-14 pendente de confirmação, FDP-15 pendente de aprovação, pessoas/horas/timeboxes, execução dos 17 P0 e demais testes, spikes, métricas de staging, drills e gates de produção. Não converter prematuramente em PASS operacional.
