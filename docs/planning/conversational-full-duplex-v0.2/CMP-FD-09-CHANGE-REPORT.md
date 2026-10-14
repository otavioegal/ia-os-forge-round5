# CMP-FD-09 v0.2 — Relatório de mudança

**Autor:** Grok, revisão corretiva documental.
**Estado do pacote:** CANDIDATE FOR CODEX REVIEW. Não é PASS.

## Acrescentado

Diretório novo `docs/planning/conversational-full-duplex-v0.2/`, treze arquivos:

- CMP-FD-00 índice
- CMP-FD-01 delta de ledger e adapter
- CMP-FD-02 contrato de mídia
- CMP-FD-03 máquinas de estado
- CMP-FD-04 política e consentimento
- CMP-FD-05 UX e proveniência
- CMP-FD-06 observabilidade
- CMP-FD-07 histórias, fixtures e oráculos
- CMP-FD-08 rastreabilidade
- CMP-FD-09 este relatório
- CMP-FD-10 disposição dos findings
- CMP-FD-11 questões abertas
- CMP-FD-12 consistência

Nenhum desses arquivos existia na árvore auditada.

## Não modificado

- `docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md` e o restante da baseline v1.7
- `historical/round4/docs/planning/FDP-15-v1.0-INTEGRATION-ADAPTER-SPECIFICATION.md`
- `docs/planning/conversational-mvp/`, `conversational-mvp-v0.2/`, `conversational-mvp-v0.3/`
- `docs/planning/conversational-full-duplex/` (v0.1)
- pareceres em `docs/reviews/`, inclusive o FAIL e o prompt corretivo
- ata, ADR AQ-07 e os demais atos em `docs/governance/`
- código, configuração de deploy, migração SQL executável, segredo, workflow

Não houve teste, build, checker, provider, banco, staging, API de produto, contratação nem BUILD-00.

## Por que a v0.1 permanece

O parecer marcou FAIL naquele SHA. Reescrever aqueles três arquivos apagaria o objeto auditado. A correção é este diretório. A v0.3 continua dizendo o que dizia quando recebeu PASS WITH CONDITIONS; a decisão full-duplex é posterior e vive no ADR e na ata, não num patch retroativo.

## Pedido

Auditoria Codex independente, somente leitura, sobre este diretório. O veredito não está escrito aqui.
