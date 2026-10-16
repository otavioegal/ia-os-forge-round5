# 01 — Registro dos achados do parecer Round 5

**Estado:** CANDIDATE FOR CODEX REVIEW. Este registro não é o parecer do Codex. Não declara PASS. Não marca finding como fechado por este autor.

O parecer está em `docs/reviews/PARECER-CODEX-ROUND5-2026-10-13.md`. Ele julgou a v1.2. A correção documental posterior está na v1.7, sem apagar a v1.2. A v1.2 permanece em `historical/round5/`.

Quando a linha diz "correção presente", o teste correspondente continua NOT RUN. Presença do texto não é execução.

## HIGH-01 — ciclo da reserva e do gasto

**Pedido:** reservar, confirmar o custo real, liberar o que não foi gasto, e tratar falha, cancelamento, custo divergente e recuperação depois de interrupção, com efeito atômico e estados finais.

**Situação nesta candidata:** a correção está escrita. Este autor não fecha o achado. O Round 10 registrou o fechamento documental do conjunto HIGH da baseline. Os testes seguem NOT RUN.

**Evidência:**

- `docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md`, seção 8A, linhas 310–351: reserva, despacho, acerto quando o real é menor, acerto quando o real é maior e ainda cabe no teto, bloqueio quando não cabe, liberação só com prova de que não houve efeito, e cancelamento antes da chamada.
- Linha 330: estados finais da operação são SETTLED, RELEASED, DENIED e CANCELLED. Os outros não são finais.
- Seção 8A.1, linhas 355–388: uma transação só, com trava do orçamento, da operação e da reserva, e no máximo um movimento de dinheiro.
- Seção 10, linhas 521–533: o que fazer se a interrupção ocorre antes da reserva, depois da reserva, depois da chamada, no meio do dinheiro, ou na passagem de tarefa.
- História F-015, no registro v1.7, aponta LEDGER-01 a LEDGER-18. A linha 536 do contrato diz que nenhum desses testes foi executado.

**O que não foi feito:** não houve PostgreSQL, concorrência real, provider nem gasto.

## HIGH-02 — aprovação presa à versão exata

**Pedido:** a publicação só vale para aquela versão: código, artefatos, grafo, migrações, ambiente e política. Um caso negativo para cada parte que divergir.

**Situação nesta candidata:** a correção está escrita. Testes NOT RUN. Achado não fechado por este autor.

**Evidência:**

- FDP-16A v1.7, seção 3.8, linhas 142–158: `environment_id` é a identidade do ambiente, não o tipo. Dois ambientes de produção são dois ids. O tipo fica em `environment_class`.
- Seção 8B, linhas 476–481: a comparação é de todos os campos, na ordem escrita. A primeira diferença recusa e não consome a aprovação.
- Campos negativos nomeados nessa seção: release, ambiente, classe, código, artefato, grafo, migrações, política, escopo e autor da aprovação. Os testes são DEPLOY-02 a DEPLOY-12.
- História F-029, linhas 1277–1321 do registro v1.7, repete um negativo por campo.

**O que não foi feito:** nenhum deploy e nenhum ensaio de publicação.

## HIGH-03 — adaptador alinhado ao FDP-15

**Pedido:** a história F-012 deve exigir todas as funções de adaptador do FDP-15, corrigir a dependência e dizer o que acontece quando uma função não existe.

**Situação nesta candidata:** o texto da história foi alinhado. O FDP-15 continua sem aprovação humana. Citar a lista não a aprova. Teste ADAPT-01 está NOT RUN. Achado não fechado por este autor.

**Evidência:**

- Fonte pendente: `historical/round4/docs/planning/FDP-15-v1.0-INTEGRATION-ADAPTER-SPECIFICATION.md`, linhas 221–224 (descrever, saúde, invocar, cancelar) e linhas 230–238 (iniciar, retomar, pausar, cancelar tarefa, status, checkpoint, artefatos, diferença e testes).
- F-012, registro v1.7, linhas 509–527: dependências F-011 e F-006; cada método de motor é suportado ou não suportado; método ausente das duas listas quebra o contrato; método não suportado não é imitado; segredo fica em referência de cofre, regra que depende de F-006.
- A citação interna "linhas 227–232" aponta o começo da seção, não a última função. As funções em si estão nas linhas 221–224 e 230–238. Esta pasta registra o alcance certo e não edita o registro.
- Matriz v1.7, linha do ADAPT-01: os passos chamam as funções comuns e as nove funções de motor. Resultado aprovado e resultado reprovado estão na mesma linha. Estado NOT RUN.

## HIGH-04 — AIOX preferencial, não ponto único de falha

**Pedido:** manter o AIOX como opção preferencial da fonte aprovada, sem torná-lo a única porta.

**Situação nesta candidata:** a frase antiga "única entrada suportada" não está mais na v1.7. O teste AIOX-01 está NOT RUN. Achado não fechado por este autor.

**Evidência:**

- Fonte: `historical/round4/docs/source-material/chat-extracts/FDP-06-v1.0__msg058.md`, linha 372, framework preferencial; linha 407, não será ponto único de falha.
- `docs/planning/FDP-16-v1.7-AIOX-EXECUTION-ENGINES.md`, seção 1: preferencial, não é a única entrada; se a saúde não estiver boa, o caminho é FORGE_DIRECT só para efeito interno ou nenhum; publicar e efeito externo continuam negados; trocar a preferência exige decisão de mudança; usar o reserva não exige.
- F-013, linhas 555–574 do registro v1.7, diz o mesmo e rejeita a frase da v1.2.

## HIGH-05 — cada aceite com um teste, passos, aprovado e reprovado

**Pedido:** em especial checkpoint, passagem entre agentes e recuperação.

**Situação nesta candidata:** a matriz v1.7 tem coluna de passos, regra positiva e regra negativa. F-016 tem o teste HANDOFF-01, que a v1.2 não tinha como oráculo completo. A recuperação de interrupção está na seção 10 do contrato. A conferência desta pasta achou 41/41 histórias com aceite positivo e negativo e com teste presente na matriz. Isso não é suficiência semântica julgada de novo, nem execução. Achado não fechado por este autor.

**Evidência:**

- `docs/planning/FDP-17-v1.7-TESTING-STRATEGY.md`, seção 3, linhas 33–34: cada caso declara fixture, passos, regra de aprovação e regra de falha.
- Matriz v1.7, linha 8: colunas Steps, Positive rule e Negative rule. Linha 6: história só é coberta pelo teste nomeado, não por um resumo.
- HANDOFF-01: digest inválido é recusado; digest válido encerra a tentativa anterior, revoga o que ela podia fazer, cria a tentativa nova e não deixa duas tentativas abertas; queda no meio não pode deixar duas abertas.
- ENG-02: a passagem não aumenta o que a tentativa pode fazer.
- Seção 10 do FDP-16A: recuperação nos pontos de interrupção, testes citados RETRY-01 e IDEM-01, também NOT RUN.
- Exceção já escrita, não corrigida por edição: PROD-05 descreve o reprovado sem a palavra FAIL. PERF-01 não tem resultado aprovado porque a história F-025 não tem meta e está fora do MVP. Inventar um número seria o erro que o próprio teste proíbe.

## HIGH-06 — as 41 histórias ligadas à fonte certa

**Pedido:** separar decisão já citada, o que depende de FDP-14, o que depende de FDP-15 e o que é proposta nova, com seção ou linha.

**Situação nesta candidata:** o registro v1.7 faz essa separação nas 41 histórias. A tabela está em `02-MATRIZ-HISTORIA-TESTE.md`. Conferência estrutural: 41/41. Achado não fechado por este autor. FDP-14 e FDP-15 continuam sem aprovação humana, então "fonte citada" não significa "fonte aprovada por você agora".

**Evidência:** F-001, linhas 20–24 do registro, é o modelo. F-012, linhas 517–521. F-039, linhas 1731–1735. F-008 marca proposta de tela. F-024 diz que o FDP-15 pendente governaria a forma, se um dia for construído.

## MEDIUM-01 — matrizes de Build e Attempt

**Situação:** correção presente. Não fechado por este autor. Testes de transição não executados.

**Evidência:** FDP-16A v1.7, seção 7.1, linhas 255–269, e seção 7.2, linhas 271–286. O vigia só encerra por tempo o que já está executando. CREATED e QUEUED não. Saídas de espera de aprovação, pedido de mudança e desbloqueio estão na grade de Build.

## MEDIUM-02 — um id, não dois

**Situação:** correção presente. Não fechado por este autor.

**Evidência:** FDP-16A v1.7, linha 34: `id` é a chave. Nomes como `task_id` e `build_id` repetem esse id. Não são outra chave. `operation_ref` não é apelido do id da operação.

## MEDIUM-03 — provider sem consulta de recibo

**Situação:** correção presente. Não fechado por este autor. Nenhum provider foi chamado.

**Evidência:** FDP-16A v1.7, seção 8C, linhas 483–488, e seção 8A.3, linhas 471–473. Se não há consulta nem atestado, a prova fica não verificada, a reserva continua presa, ninguém redispara a chamada e ninguém libera o dinheiro por chute. Uma frase humana não é prova.

## MEDIUM-04 — conjunto para "pronto para uma pessoa testar"

**Situação:** correção presente. Não fechado por este autor. O flag não foi calculado em software.

**Evidência:** `docs/planning/FDP-20-v1.3-SPRINT-IMPLEMENTATION-PLAN.md`, seção "Required set for READY_FOR_HUMAN_TEST", linhas 40–47. A tabela de sprints não é essa lista. F-039, linhas 1737–1743, aponta essa seção. RHFT-01 está NOT RUN.

## MEDIUM-05 — pessoas, horas e prazo

**Situação:** permanece ABERTO. Não foi inventado nome, hora nem custo.

**Por que é decisão humana:** saber quem faz cada história e quanto tempo cabe é responsabilidade de quem organiza o trabalho. Um documento técnico não pode escolher pessoas nem fingir um calendário.

**Onde está honesto hoje:** registro v1.7, linhas 6–9, e em cada história: pessoa PENDING HUMAN ASSIGNMENT; esforço PENDING CALIBRATION. O DoR operacional não está atendido. Isso não apaga a qualidade do texto de aceite. Impede dizer que as histórias estão prontas para execução.

**Decisão necessária:** nomear a pessoa responsável e calibrar o esforço de cada uma das 41 histórias, antes de planejar capacidade ou autorizar construção. Não é preciso, para isso, escolher fornecedor, banco ou protocolo.

## LOW-01 do Round 10 — frase velha na estratégia de teste

**Situação:** permanece ABERTO. O arquivo auditado não foi editado.

**Evidência:** `docs/planning/FDP-17-v1.7-TESTING-STRATEGY.md`, linha 31, ainda diz que os identificadores suplementares estão "only in the v1.6 matrix". A frase certa já está na linha 3 do mesmo arquivo e na primeira linha da matriz v1.7: a única tabela normativa é a v1.7. Esta pasta não corrige o arquivo no lugar, porque isso reescreveria a baseline auditada.

## O que continua pendente além destes achados

FDP-14 sem confirmação do Founder. FDP-15 sem aprovação do Founder. BUILD-00 não autorizado. 91 oráculos da matriz NOT RUN. Oráculos de conversa NOT RUN. Parecer da conversa v0.2 com veredito não escolhido. `forge.conversation.delta.v4` desligada. Nenhum destes itens foi promovido aqui.
