# Relatório de consistência — Round 9
Estado: ROUND 9 — CANDIDATE FOR CODEX REVIEW.
Verificação textual. Nenhum teste de produto, banco, provider ou drill foi executado.
O script `tools/check_round9_consistency.py` só lê arquivos. Isso não é um PASS de prontidão.

## Passagem 1 — integridade
- 90 oráculos, 11 colunas, sem id duplicado. A v1.5 tinha 88. Entraram LEDGER-16 e LEDGER-17.
- Os 17 P0 continuam com uma linha cada e com o mesmo texto de intent da matriz v1.5.
- Fora LEDGER-08, LEDGER-15 e a linha de índice de F-015, o texto dos oráculos da v1.5 foi copiado.
- LEDGER-12 e LEDGER-14 permanecem byte a byte.
- Todo id citado em `Tests:` das 41 histórias existe na matriz v1.6.
- 41 blocos `- Inherited:` e 41 DoR operacionais `Not met`.
- `New in v1.6` aparece só em F-015.
- Só existe uma matriz em `docs/planning/`: a v1.6.
- FDP-18, FDP-18A e FDP-20 são byte a byte iguais ao snapshot em `historical/round8/`.
- O parecer Round 8 continua no caminho original e a cópia histórica é igual.
- A frase antiga do Apply, "the human capability used to authorize is still present", não está na v1.6. Ela continua na v1.5 congelada.
- Os 11 estados de Task, `approver_actor_ref`, `FORGE_DIRECT` e a ordem de lock continuam presentes.

## Passagem 2 — as duas condições
- C-01: a linha 420 do FDP-16A v1.6 exige os dois grants no PROVEN_RECEIPT e um grant no PROVEN_NO_EFFECT, lidos na hora do Apply. A linha 422 separa replay de Confirm e Confirm novo sem evento. LEDGER-16, linha 77, cobre os quatro casos e falha se a autorização for consumida ou se houver evento de dinheiro.
- C-02: a linha 463 define a chave `(operation_id, proof_id)` e a projeção `max`. A linha 98 diz que o comando não atribui `pending_actual_minor`. LEDGER-08 exige a linha do receipt de 30. LEDGER-15 começa em DISPATCHED com reserva HELD de 50 e reserved 150. LEDGER-17 exige duas linhas, 30 e 40, e projeção 40, e falha se o valor for o de quem pegou o lock.

## Limite
Estas passagens não provam que o Codex vá aceitar a redação. Não há PASS desta candidata. Não há teste executado. BUILD-00 não foi autorizado. O PASS WITH CONDITIONS do Round 8 continua sendo o parecer da v1.5, não desta v1.6.
