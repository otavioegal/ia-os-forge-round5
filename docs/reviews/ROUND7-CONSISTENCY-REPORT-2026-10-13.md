# Relatório de consistência — Round 7
Estado: ROUND 7 — CANDIDATE FOR CODEX REVIEW.
Verificação textual. Nenhum teste de produto, banco, provider ou drill foi executado.
O script `tools/check_round7_consistency.py` só lê arquivos. Nesta execução ele terminou com as contagens abaixo. Isso não é um PASS de prontidão.

## Passagem 1 — integridade
- 85 oráculos, 11 colunas, sem id duplicado.
- Os 17 P0 continuam com uma linha cada e com o mesmo texto de intent da matriz v1.3.
- Todo id citado em `Tests:` das 41 histórias existe na matriz v1.4.
- 41 blocos `- Inherited:` e 41 DoR operacionais `Not met`.
- `New in v1.4` aparece só em F-015.
- Só existe uma matriz em `docs/planning/`: a v1.4.
- FDP-18, FDP-18A e FDP-20 são byte a byte iguais ao snapshot em `historical/round6/`.
- O parecer Round 6 continua no caminho original.
- Os 11 estados de Task continuam no contrato.
- A frase antiga `human RecordReceipt with evidence ref` não está na v1.4.
- `approver_actor_ref`, `blocked_from`, `NOT_EXECUTING`, `FORGE_DIRECT` e `start_task` continuam presentes.

## Passagem 2 — propriedades, não só ids
- Dois RecordReceipt: a seção 8A.1, linha 388, exige um movement SETTLEMENT, um `budget.settled` e o perdedor em 409 ALREADY_SETTLED. LEDGER-07 repete os contadores: spent 830, reserved 100, não 860.
- RecordReceipt contra ReleaseReservation: a linha 389 exige exatamente um dos dois estados terminais e proíbe os dois eventos de dinheiro no mesmo operation. LEDGER-08 falha se `reserved` cair duas vezes.
- Duas ReleaseReservation: a linha 390 exige uma queda de `reserved` e um `budget.released`. LEDGER-09 falha se a queda for o dobro.
- Retry depois do commit: a linha 391 separa 200 IDEMPOTENT_REPLAY do mesmo `command_id` e 409 do `command_id` novo, sem redispatch. LEDGER-10 exige que a contagem de chamadas ao provider fique em 1.
- O perdedor só é decidido depois do `FOR UPDATE`, relendo a linha. `VERSION_CONFLICT` não é o resultado dessas quatro corridas quando o movement já existe.
- Custo acima do limite: a linha 395 não insere movement e não aumenta `spent`.
- Autoridade manual: o catálogo, linhas 203–208, não deixa humano chamar RecordReceipt. BLOCKED_RECONCILIATION só muda dinheiro em ApplyAuthorizedReconciliation. LEDGER-11 cobre coding engine, evidência ausente, evidência do coding engine e receipt do system. LEDGER-12 cobre o segundo operador e o fato de Confirm, sozinho, não gastar.

## Limite
Estas passagens não provam que o Codex vá aceitar a via escolhida. Não há PASS. Não há teste executado. BUILD-00 não foi autorizado.
