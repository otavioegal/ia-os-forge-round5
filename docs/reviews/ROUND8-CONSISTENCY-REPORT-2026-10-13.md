# Relatório de consistência — Round 8
Estado: ROUND 8 — CANDIDATE FOR CODEX REVIEW.
Verificação textual. Nenhum teste de produto, banco, provider ou drill foi executado.
O script `tools/check_round8_consistency.py` só lê arquivos. O resultado impresso por ele nesta execução não é um PASS de prontidão e não é o veredito do Codex.

## Passagem 1 — integridade
- 88 oráculos: os 85 da v1.4 mais LEDGER-13, LEDGER-14 e LEDGER-15. Onze colunas. Sem id duplicado.
- Os 17 P0 continuam com uma linha cada e com o mesmo texto de intent da matriz v1.4.
- LEDGER-01 a LEDGER-07, LEDGER-09, LEDGER-10, DEPLOY-02 e HANDOFF-01 conservam a linha da v1.4.
- Todo id citado em `Tests:` das 41 histórias existe na matriz v1.5.
- 41 blocos `- Inherited:` e 41 DoR operacionais `Not met`.
- `New in v1.5` aparece só em F-015. `New in v1.3` e `New in v1.4` continuam em F-015.
- Só existe uma matriz em `docs/planning/`: a v1.5.
- FDP-18, FDP-18A e FDP-20 são byte a byte iguais ao snapshot em `historical/round7/`.
- A v1.4 em `historical/round7/docs/planning/` é a árvore movida, sem edição de conteúdo.
- O parecer Round 7 continua no caminho original e ainda contém HIGH-01, NEW-HIGH-07, NEW-HIGH-08 e NEW-HIGH-09.
- A frase original do hash `4e57839…` continua no change report da Rodada 7. A errata aponta `decef2809…`.
- Os 11 estados de Task continuam no contrato.
- `approver_actor_ref`, `blocked_from`, `NOT_EXECUTING`, `FORGE_DIRECT` e `start_task` continuam presentes.
- A frase `only supported orchestrator` continua ausente.

## Passagem 2 — propriedades, não só ids
- LEDGER-08 não aceita RELEASED com spent 800 como alternativa positiva. O positivo é CONFLICT, spent 800, reserved 150, as duas provas vivas, `pending_actual_minor` 30, sem movement. O negativo falha se o resultado depender de quem pegou o lock.
- LEDGER-13 liquida o receipt verificado de 30 e recusa a liberação com 409 RECEIPT_PRECEDES_RELEASE. Falha se o estado for RELEASED.
- LEDGER-11 não trata digest de operador como prova. O caminho positivo é prova ATTESTED capturada pelo ingest, e o movimento só ocorre no Apply do system.
- LEDGER-12 exige outro operador, capability, o mesmo `evidence_ref`, sessão fresca e Apply do system. Self-confirm, confirmer sem capability, evidência trocada, sessão velha e Apply humano não movem dinheiro.
- LEDGER-14 cobre replay do mesmo `command_id`, autorização duplicada, conflito de decisão e segundo Apply.
- LEDGER-15 guarda a linha imutável de 200 e recusa a liberação posterior sem apagar essa linha e sem elevar `spent` a 1000 ou 1050.
- O contrato proíbe inventar assinatura quando o provider não enviou atestação.
- Não há estado de Task novo. CONFLICT é valor de `reconciliation_state`, não de Task.

## Limite
Estas passagens não provam que o Codex vá aceitar a via escolhida. Não há PASS. Não há teste executado. BUILD-00 não foi autorizado.
