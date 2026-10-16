# Achados do parecer sobre a v1.0 e tratamento na v1.1

**Parecer de origem:** leitura independente do commit `a6196b6c5a5036f23707781b06fe9db028974ead`, pacote `docs/planning/forge-build00-readiness-v1.0/`.
**Esta versão:** candidata. Nenhum finding foi fechado. Nenhum resultado abaixo é PASS nem pronto para construir.

A conta foi refeita a partir das classes do FDP-19A v1.7, sem teste de produto, sem banco e sem spike. P0 224–448, P1 256–512, P2 40–80, P3 32–64, total 552–1.104, sem F-025 520–1.040, conjunto de 32 histórias 424–848. Nove spikes na faixa S dão 36–72.

| Achado | Tratamento nesta versão | Continua pendente? |
|---|---|---|
| 1. O título dizia “Modelo aprovado para a construção”, embora Claude Code e AIOX não tivessem sido aprovados | `01`, seção “Proposta de execução, ainda não aprovada”. O título antigo foi abandonado | Sim. O modelo segue não aprovado. O finding não foi fechado |
| 2. O único total, 552–1.104, misturava P0, P1, P2 e a história adiada | `01`, seção “Estimativas separadas por prioridade”, com 224–448, 256–512, 40–80, 32–64, além de 520–1.040 sem F-025 e de 424–848 para as 32 histórias, sem F-039 | Não como erro de conta. As horas continuam estimativa, não prazo nem orçamento |
| 3. SPIKE-06 usava 3–6 horas, faixa que a tabela não definia | `02`. Passa a usar a faixa S já definida, 4–8 horas. O total dos spikes passa de 35–70 para 36–72 | Não como faixa órfã. 36–72 não é compromisso |
| 4. SPIKE-06 estava em Data e SPIKE-09 em Security, diferentes dos papéis de F-003 e F-007 | `02`. SPIKE-06 fica Backend, como F-003. SPIKE-09 fica Desktop, como F-007 | Não nesse alinhamento. A função ainda não é pessoa nomeada |
| 5. A proposta tratava AIOX como executor único e não registrava o caminho alternativo | `01`. Caminho preferido e `FORGE_DIRECT` citados da F-013, com os limites já escritos nessa história | Não quanto ao caminho alternativo, que já estava na base. A base não foi reaberta |
| 6. Não havia regra se Claude Code e AIOX discordassem | `01`, seção “Divergência entre Claude Code e AIOX”, e `03`, item 2 | Sim, de propósito. Não existe regra aprovada. Nenhum vencedor foi escolhido. O documento não trata isso como resolvido |
| 7. Função atribuída, pessoa nomeada, estimativa e esforço calibrado pareciam a mesma coisa, e a prontidão operacional podia ser lida como cumprida | `01`, seção “Função, pessoa e calibração”, e `03`, seções “Proposto” e “Ainda pendente” | Sim. Papel de IA não cumpre pessoa nomeada. A estimativa não é calibração. A prontidão operacional não foi declarada e continua não atendida |
| 8. As aprovações do Founder estavam só no registro de encerramento, enquanto o FDP-19A antigo ainda diz pendente | `01` e `03` citam `forge-planning-closure-v1.0/01-DECISOES-DO-FOUNDER.md` e dizem que as frases antigas são históricas | Não quanto à localização do registro. Os arquivos antigos não foram reescritos. BUILD-00 continua sem autorização |

Nada nesta tabela autoriza construção, fecha um finding antigo ou converte uma proposta em decisão.
