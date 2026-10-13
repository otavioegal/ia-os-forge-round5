# Relatório de consistência — Round 10
Estado: ROUND 10 — CANDIDATE FOR CODEX REVIEW.
Verificação textual. Nenhum teste de produto, banco, provider ou drill foi executado.
O script `tools/check_round10_consistency.py` só lê arquivos. Isso não é um PASS de prontidão.

## Passagem 1 — integridade
- 91 oráculos, 11 colunas, sem id duplicado. A v1.6 tinha 90. Entrou LEDGER-18.
- Os 17 P0 continuam com uma linha cada e com o mesmo texto de intent da matriz v1.6.
- Fora a linha de índice de F-015, o texto dos oráculos da v1.6 foi copiado. LEDGER-17 inclusive.
- Todo id citado em `Tests:` das 41 histórias existe na matriz v1.7.
- 41 blocos `- Inherited:` e 41 DoR operacionais `Not met`.
- `New in v1.7` aparece só em F-015.
- Só existe uma matriz em `docs/planning/`: a v1.7.
- FDP-18, FDP-18A e FDP-20 são byte a byte iguais ao snapshot em `historical/round9/`.
- O parecer Round 9 continua no caminho original e a cópia histórica é igual.
- A frase restritiva “when the movement was RELEASE” não está na v1.7. Ela continua na v1.6 congelada.
- Os 11 estados de Task, `approver_actor_ref`, `FORGE_DIRECT`, os dois grants do Apply e a chave `(operation_id, proof_id)` continuam presentes.

## Passagem 2 — NEW-MEDIUM-12
- A linha 350 do FDP-16A v1.7 manda uma linha de pending por receipt conclusivo tanto depois de RELEASE quanto depois de SETTLEMENT, sem segundo movement.
- As linhas 405 a 411 nomeiam as três trajetórias e os contadores: release deixa spent 800 e reserved 100; settlement deixa spent 830 e reserved 100; o par 30 e 40 projeta 40; o no-effect não ganha um receipt inventado.
- A linha 469 impede devolver a reserva para HELD quando o movement já existe. A linha 471 repete a mesma inserção no schema.
- LEDGER-18, linha 79, exige as linhas, a projeção, a preservação das provas, um único movement e os contadores inalterados. A repetição do comando tardio não cria segunda linha nem segundo `budget.proof_conflict`.

## Limite
Estas passagens não provam que o Codex vá aceitar a redação. Não há PASS desta candidata. Não há teste executado. BUILD-00 não foi autorizado. O PASS WITH CONDITIONS do Round 9 continua sendo o parecer da v1.6, não desta v1.7.
