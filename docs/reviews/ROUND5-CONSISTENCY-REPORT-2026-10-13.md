# Relatório de consistência documental — Round 5
Estado: ROUND 5 — CANDIDATE FOR INDEPENDENT REVIEW.
Este relatório registra uma verificação automática de texto. Não é teste de software e não é parecer do Codex.

## Comando
`python3 tools/check_round5_consistency.py`

## Saída observada em 2026-10-13
```
v1.2 files: 9
stories: 41
unique positive acceptances: 41
unique negative acceptances: 41
P0 oracle rows: 17/17
errors: 0
NOTE historical files preserved under historical/round4 (20 files)
```
Código de saída: 0.

## O que o script confere
- Presença da frase de estado candidato e de “NOT READY FOR BUILD” em cada FDP v1.2.
- Ausência de ponteiro normativo para matriz v1.0 ou v1.1.
- Título que não continua “v1.0 —”.
- Identificadores F-001 até F-041, sem furo e sem aceitação positiva ou negativa repetida.
- Ausência da fórmula genérica “as applicable”.
- AUTHZ-01 dentro de F-001, AUTHZ-02 dentro de F-002, SEC-01 dentro de F-006, COST-01 dentro de F-015, e a recusa explícita de F-021 em fechar COST-01.
- Uma linha de oráculo para cada um dos 17 ids de FDP-13 §191.
- Ausência de “authorized or nominal”.
- Os 11 estados de Task, os parâmetros de retry e os ids de envelope no FDP-16A.
- Presença física do parecer histórico do Codex Round 4, não reescrito.

## O que o script não confere
Não julga se um oráculo é suficiente para o Codex. Não prova que o software existe. Não mede RPO, RTO, latência nem custo. Não valida FDP-14 ou FDP-15 junto ao Founder.

## Integridade do histórico
`cmp` entre a cópia histórica de FDP-16A v1.1 e o arquivo extraído do pacote Round 4 retornou igualdade. A conferência completa de byte dos 20 arquivos históricos é a própria cópia recursiva feita no início da rodada, sem passo de edição sobre esse diretório.
