# Modelo de execução proposto e estimativa inicial

**Estado:** proposta candidata. Não aprovada. Não é PASS. Não declara prontidão operacional. Não autoriza BUILD-00.

## O que o Founder já decidiu

O registro está em `docs/planning/forge-planning-closure-v1.0/01-DECISOES-DO-FOUNDER.md`. Ele confirma FDP-14, aprova FDP-15 e aceita a base escrita v1.7. Não escolhe equipe, ferramenta, orçamento ou data. Não autoriza BUILD-00.

As frases de “pendente” para FDP-14 e FDP-15 que ainda aparecem dentro de `docs/planning/FDP-19A-v1.7-STORY-ACCEPTANCE-REGISTER.md` são texto histórico dessa versão. Não foram apagadas. Para essas duas confirmações e para a base escrita, o registro de encerramento é posterior e prevalece. Isso não atualiza pessoa nomeada, hora calibrada nem autorização de construção.

## Proposta de execução, ainda não aprovada

Claude Code como Builder e AIOX como caminho de execução são uma proposta. O Founder não aprovou esse desenho.

- **Builder proposto:** Claude Code, para implementar e coordenar. Proposta, não decisão.
- **Caminho preferido, já escrito na base e não reaberto aqui:** Forge vai ao adaptador AIOX e depois ao motor. Não é caminho único. Fonte: FDP-19A, história F-013, requisitos.
- **Caminho alternativo, já escrito na mesma história:** se a saúde do AIOX não estiver boa, o Attempt Manager marca `orchestrator_path` como `FORGE_DIRECT` e só chama o adaptador do motor quando o efeito é `NONE` ou `INTERNAL`. `deploy.release` e efeito `EXTERNAL` ficam de fora. Nos dois caminhos, as tabelas do Forge continuam sendo o registro. Deixar de preferir AIOX exige uma decisão de mudança. Usar `FORGE_DIRECT` não exige.
- **Função não é squad exclusivo.** Os papéis já definidos — Data, Security, Backend, Desktop, UX, Orchestration, Integration, QA, Product e Release — indicam o tipo de trabalho. Não são nome de pessoa e não transformam o AIOX no único executor.
- **Revisor proposto:** Codex, ao fim de cada sprint ou marco. Quem implementa não aprova o próprio trabalho. Isso também faz parte da proposta, não de uma aprovação nova.

## Divergência entre Claude Code e AIOX

**Pendente. Não há regra aprovada. Esta versão não a cria e não escolhe um vencedor.**

A regra de fallback da F-013 trata de saúde do AIOX. Não diz o que prevalece se o Builder proposto e o caminho AIOX discordarem sobre uma história. Enquanto essa regra não existir por decisão humana, o modelo não está resolvido e não autoriza execução, corte de escopo nem declaração de pronto.

## Função, pessoa e calibração

A função atribuída diz o tipo de trabalho. A pessoa nomeada pedida pelo FDP-19A é outra coisa. Um papel de IA não atende a essa exigência, porque não é uma pessoa nomeada. Os nomes continuam pendentes. Este texto não inventa equipe, nome ou prazo, e não pede ao Founder que preencha as 41 histórias.

A hora abaixo é estimativa inicial, obtida só pela classe relativa já existente. Não é esforço calibrado. O FDP-19A continua com horas e timebox em `PENDING CALIBRATION`. Esta versão não muda esse estado.

**Prontidão operacional: não atendida.** Nenhuma história fica pronta para execução enquanto pessoa nomeada, hora calibrada ou timebox continuarem pendentes no FDP-19A, e enquanto o FDP-20 mantiver papel e timebox dos spikes pendentes no texto histórico.

## Faixas usadas

| Classe já existente | Estimativa inicial de esforço ativo |
|---|---:|
| S | 4–8 horas |
| M | 8–16 horas |
| L | 16–32 horas |
| XL | 32–64 horas |

Não há história de classe S. A faixa S só entra no SPIKE-06, porque a faixa anterior de 3–6 horas não existia nesta tabela. São horas de trabalho estimado, não dias de calendário. A faixa não foi calibrada por uma execução deste produto. Não inclui espera, aprovação humana nem dependência externa. O limite superior é só um limite inicial de trabalho ativo: se for alcançado sem cumprir o aceite, para-se, registra-se o motivo e reestima-se. Esse limite não autoriza cortar segurança nem declarar a história concluída sem evidência.

## Distribuição das 41 histórias

A função é a coluna de papel já existente no FDP-19A. A classe também é a desse registro. A hora vem da tabela acima. Nenhuma classe foi alterada.

| Função existente | Histórias e classe |
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

São 19 histórias M, 19 L e 3 XL.

## Estimativas separadas por prioridade

Estas linhas não se somam a um prazo. Cada uma é esforço ativo estimado.

| Recorte | Histórias | Estimativa | O que entra |
|---|---:|---:|---|
| P0 | 15 | 224–448 h | F-001 L, F-002 L, F-005 M, F-006 L, F-007 L, F-015 XL, F-026 M, F-027 L, F-028 M, F-029 L, F-030 M, F-031 M, F-032 L, F-033 XL, F-034 M |
| P1 | 21 | 256–512 h | F-003 L, F-004 L, F-008 M, F-009 M, F-010 M, F-011 L, F-012 L, F-013 L, F-014 M, F-016 L, F-017 M, F-018 L, F-019 M, F-020 L, F-035 L, F-036 M, F-037 M, F-038 M, F-039 M, F-040 L, F-041 L |
| P2 | 4 | 40–80 h | F-021 M, F-022 M, F-023 M, F-024 L. F-023 e F-024 continuam opcionais no plano de sprint |
| P3 | 1 | 32–64 h | Só F-025 XL. Adiada. Fora do calendário. Não entra no escopo autorizado |

| Total | Estimativa | Leitura |
|---|---:|---|
| 41 histórias | 552–1.104 h | Soma de P0, P1, P2 e P3. Inclui a história adiada |
| 40 histórias, sem F-025 | 520–1.040 h | Tira só as 32–64 h de F-025 |
| 32 histórias do FDP-20 | 424–848 h | Conjunto exigido para o sinal de teste humano. Não inclui F-039 |

O conjunto de 32 histórias, na ordem do FDP-20, é: F-001, F-002, F-003, F-004, F-005, F-006, F-007, F-008, F-009, F-010, F-011, F-012, F-013, F-014, F-015, F-016, F-017, F-018, F-019, F-026, F-027, F-028, F-029, F-030, F-031, F-032, F-033, F-034, F-035, F-036, F-037 e F-038.

F-039 não entra nessa conta. Ela é a história que deriva o sinal; não é pré-requisito de si mesma. Ficam de fora também F-020, F-021, F-022, F-023, F-024, F-025, F-040 e F-041. Por isso 424–848 não é a soma de P0 com P1. P0 com P1 inclui F-020, F-039, F-040 e F-041, e dá outro número.

Nenhum desses totais é duração do projeto, data de entrega, teto aprovado ou custo. A duração dependeria de capacidade real e de uma calibração que ainda não existe.

## Limites

- Sem orçamento, preço, data ou teto total.
- Sem provider real, credencial, banco, migration, deploy ou chamada paga.
- As classes e os critérios da v1.7 não foram alterados.
- A autorização de BUILD-00 continua separada e não foi concedida.
