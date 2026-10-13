# IA OS Forge — Índice oficial Round 5
Estado da entrega: **ROUND 5 — CANDIDATE FOR INDEPENDENT REVIEW**.
Não é aprovação do Founder. Não é READY FOR BUILD. Não autoriza BUILD-00.
Nenhum teste de software foi executado. Nenhum drill de staging foi executado.

## O que é normativo nesta rodada (proposta)
Somente os arquivos v1.2 abaixo, e somente depois de revisão independente e aprovação humana. Até lá são rascunhos candidatos.

| Arquivo | Papel |
|---|---|
| [FDP-16-v1.2-AIOX-EXECUTION-ENGINES.md](FDP-16-v1.2-AIOX-EXECUTION-ENGINES.md) | Fronteiras dos motores e apontadores. Não repete os schemas. |
| [FDP-16A-v1.2-EXECUTION-CONTRACTS.md](FDP-16A-v1.2-EXECUTION-CONTRACTS.md) | Schemas, envelopes, matriz de transição, retry, API interna, recuperação. |
| [FDP-17-v1.2-TESTING-STRATEGY.md](FDP-17-v1.2-TESTING-STRATEGY.md) | Método de teste. Não é a tabela de oráculos. |
| [FDP-18-v1.2-DEPLOYMENT-ROLLBACK.md](FDP-18-v1.2-DEPLOYMENT-ROLLBACK.md) | Stack congelado, ambientes, ordem do pipeline. |
| [FDP-18A-v1.2-RECOVERY-RUNBOOKS.md](FDP-18A-v1.2-RECOVERY-RUNBOOKS.md) | Classe A especificada; classes B e C em aberto. |
| [FDP-19-v1.2-PRODUCT-BACKLOG.md](FDP-19-v1.2-PRODUCT-BACKLOG.md) | Índice das 41 histórias. |
| [FDP-19A-v1.2-STORY-ACCEPTANCE-REGISTER.md](FDP-19A-v1.2-STORY-ACCEPTANCE-REGISTER.md) | DoR/DoD individual. |
| [FDP-20-v1.2-SPRINT-IMPLEMENTATION-PLAN.md](FDP-20-v1.2-SPRINT-IMPLEMENTATION-PLAN.md) | Marcos e spikes. Spikes NOT RUN. |
| [FDP-TRACEABILITY-MATRIX-v1.2-CANONICAL.md](FDP-TRACEABILITY-MATRIX-v1.2-CANONICAL.md) | Única tabela normativa de oráculos. |

## O que não é normativo
- `historical/round4/` — cópia integral e inalterada do pacote Round 4, incluindo pareceres do Codex, fontes FDP-06/10/12/13/14 e FDPs v1.1.
- Qualquer menção a matriz v1.0 ou v1.1. Esses arquivos continuam disponíveis só como histórico.

## Precedência de fontes
1. Extratos aprovados ou de referência em `historical/round4/docs/source-material/` (não editados).
2. Se este conjunto v1.2 for aceito pelo revisor e pelo Founder, a matriz v1.2 é a única tabela de oráculos e o FDP-16A v1.2 é o único contrato de execução.
3. FDP-14 segue com confirmação do Founder pendente. FDP-15 segue com aprovação do Founder pendente. Este índice não inventa essas aprovações.

## Verificações desta rodada
O script [tools/check_round5_consistency.py](../../tools/check_round5_consistency.py) confere integridade documental (contagem, unicidade, ponteiros). Ele não executa o produto. Resultado registrado no relatório de consistência: 0 erros.
