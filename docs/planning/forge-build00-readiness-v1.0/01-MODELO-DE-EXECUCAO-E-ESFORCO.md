# Modelo de execução e estimativa inicial

## Modelo aprovado para a construção

- **Builder principal:** Claude Code, responsável pela implementação e pela coordenação do trabalho.
- **Execução por função:** Synkra AIOX Squad, usando a mesma função Owner já definida para cada história no FDP-19A. A tabela abaixo preserva esses papéis; não cria uma contratação nem exige que o Founder escolha nomes.
- **Revisão independente:** Codex, ao fim de cada sprint ou marco. O agente que implementa não aprova o próprio trabalho.

## Faixas de esforço propostas

A v1.7 já classifica as histórias por tamanho relativo. Para tornar a proposta útil ao planejamento, aplico as seguintes faixas de esforço ativo do Builder e do papel especialista:

| Classe existente | Esforço inicial proposto |
|---|---:|
| S | 4–8 horas |
| M | 8–16 horas |
| L | 16–32 horas |
| XL | 32–64 horas |

São horas de trabalho estimadas, não dias de calendário. A faixa não é calibrada por uma execução anterior deste produto; o Builder deve recalibrá-la após os primeiros spikes. Não inclui espera, aprovação humana ou dependências externas. O limite superior da faixa é o timebox inicial de trabalho ativo por história. Se for alcançado sem cumprir os critérios de aceite, o Builder pausa, registra o motivo e reestima; o limite nunca autoriza cortar segurança ou declarar a história concluída sem evidência.

## Distribuição das 41 histórias

A função é a coluna `Owner role` já aprovada no FDP-19A. Cada história conserva a classe relativa daquele registro; o esforço em horas vem da tabela acima.

| Função AIOX (Owner role existente) | Histórias e classe |
|---|---|
| Data | F-001 L; F-031 M |
| Security | F-002 L; F-006 L; F-015 XL; F-026 M; F-033 XL |
| Backend | F-003 L; F-004 L; F-005 M; F-010 M; F-032 L; F-038 M |
| Desktop | F-007 L; F-023 M; F-028 M; F-040 L |
| UX | F-008 M; F-009 M |
| Orchestration | F-011 L; F-014 M; F-016 L; F-027 L; F-034 M; F-035 L; F-036 M |
| Integration | F-012 L; F-013 L; F-024 L |
| QA | F-017 M; F-019 M; F-022 M; F-037 M; F-041 L |
| Product | F-018 L; F-021 M; F-025 XL; F-039 M |
| Release | F-020 L; F-029 L; F-030 M |

O backlog contém 19 histórias M, 19 L e 3 XL. Aplicando as faixas acima, a estimativa bruta é **552–1.104 horas de esforço ativo** para as 41 histórias. Isso não é uma previsão de duração do projeto: a duração depende da capacidade real de paralelização e da recalibração dos spikes. F-025 continua fora do calendário (não agendado); a sua faixa não o coloca no escopo autorizado.

## Limites

- Sem orçamento, preço de fornecedor, data de entrega ou teto total proposto.
- Sem provider real, credencial, banco, migration, deploy ou chamada paga.
- As classes e os critérios existentes não foram alterados. Esta tabela é uma camada de alocação e estimativa sobre o backlog aprovado.