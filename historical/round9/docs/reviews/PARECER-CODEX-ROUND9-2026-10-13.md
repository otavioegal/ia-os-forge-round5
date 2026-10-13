# Parecer independente — IA OS Forge Round 9

**Data:** 13 de outubro de 2026  
**Commit auditado:** `a223f1ef460037221f64302bac4005f27f90ae4c`  
**Modalidade:** auditoria documental independente e estritamente read-only. Nenhum arquivo foi alterado; nenhum build, teste de produto, banco, provider, staging ou drill foi executado.

## Veredito executivo

| Dimensão | Veredito |
|---|---|
| Prontidão documental v1.6 | **PASS WITH CONDITIONS** |
| C-01 / NEW-MEDIUM-10 | **FECHADO** |
| C-02 / NEW-MEDIUM-11 | **PARCIALMENTE FECHADO** |
| Novo CRITICAL | **NÃO IDENTIFICADO** |
| Novo HIGH | **NÃO IDENTIFICADO** |
| Novo MEDIUM | **1 — conflito normativo no tratamento de late evidence** |
| HIGH-01, NEW-HIGH-07, NEW-HIGH-08 e NEW-HIGH-09 | **PERMANECEM FECHADOS** |
| Prontidão operacional | **NOT MET / NÃO AVALIADA POR EXECUÇÃO** |
| FDP-14 | **PENDENTE DE CONFIRMAÇÃO DO FOUNDER** |
| FDP-15 | **PENDENTE DE APROVAÇÃO DO FOUNDER** |
| Aprovação geral do Founder | **NÃO CONCEDIDA NEM PRESUMIDA** |
| BUILD-00 | **NÃO AUTORIZADO** |

O SHA foi confirmado diretamente em `.git/refs/heads/main:1`. Os relatórios Round 9 e o checker de consistência foram tratados apenas como alegações auxiliares; nenhuma conclusão deste parecer depende de declaração de Grok ou do resultado autodeclarado do checker.

A v1.6 resolve corretamente C-01 e quase toda C-02. Permanece, porém, uma contradição normativa MEDIUM: a regra geral exige uma linha de `pending_provider_cost` para cada receipt conclusivo em toda transição `CONFLICT`, mas os dois textos específicos de late evidence restringem a inserção ao caso em que o movimento anterior foi `RELEASE`. Isso deixa sem materialização definida os conflitos tardios posteriores a `SETTLEMENT`.

Por ser uma inconsistência MEDIUM, localizada e sem reabertura das garantias de movimento único ou dos HIGH anteriores, o resultado apropriado é **PASS WITH CONDITIONS**, não `FAIL`. Também não há fundamento para exigir uma rodada arquitetural adicional: basta corrigir pontualmente o texto e o oracle correspondente e fazer nova verificação documental dirigida.

## C-01 / NEW-MEDIUM-10 — fechado

A condição do Round 8 foi atendida de forma suficiente e testável.

No Apply de `PROVEN_RECEIPT`, o Policy Service relê `ledger.reconcile` para os dois atores: `requested_by` e `confirmed_by`. Para `PROVEN_NO_EFFECT`, relê o grant de `requested_by`. A aprovação histórica não substitui essa leitura (`docs/planning/FDP-16A-v1.6-EXECUTION-CONTRACTS.md:209,420`).

Quando qualquer grant exigido está ausente, o contrato determina:

- `403 CAPABILITY_REVOKED`;
- autorização permanece `AUTHORIZED` e não consumida;
- reserva permanece `HELD`;
- `spent` não muda;
- nenhum movement é inserido;
- não há `budget.settled` nem `budget.released`;
- repetição do mesmo Apply recusado mantém o `403`, sem virar falsamente `200 IDEMPOTENT_REPLAY`.

Isso está expresso em `docs/planning/FDP-16A-v1.6-EXECUTION-CONTRACTS.md:420`.

A semântica de Confirm também está coberta:

- replay do Confirm bem-sucedido com o mesmo `command_id` retorna `200 IDEMPOTENT_REPLAY`;
- não há segunda autorização nem segundo `budget.manual_reconciliation`;
- Confirm com novo `command_id` após `AUTHORIZED` retorna `409 ALREADY_CONFIRMED`;
- esse segundo Confirm não altera colunas nem grava evento;
- novo Apply após movimento retorna `409 ALREADY_SETTLED` ou `409 ALREADY_RELEASED`, sem novo money audit.

Evidência: `docs/planning/FDP-16A-v1.6-EXECUTION-CONTRACTS.md:422`.

LEDGER-16 separa adequadamente quatro fixtures: replay de K1, segundo Confirm K2, revogação do solicitante e revogação do confirmador. Em ambas as revogações exige `403`, autorização não consumida, reserva 50 ainda `HELD`, `spent=800`, `reserved=150` e nenhum movement (`docs/planning/FDP-TRACEABILITY-MATRIX-v1.6-CANONICAL.md:77`).

A compatibilidade com os oráculos anteriores foi preservada:

- LEDGER-12 continua cobrindo dual control, confirmer sem capability, evidência divergente, sessão forte/fresca e Apply somente system (`...MATRIX-v1.6-CANONICAL.md:73`);
- LEDGER-14 continua cobrindo replay de Approve e Apply, autorização única e movimento único (`...MATRIX-v1.6-CANONICAL.md:75`);
- LEDGER-16 acrescenta os casos que faltavam, sem redefinir LEDGER-12/14 (`...MATRIX-v1.6-CANONICAL.md:77`).

A autenticação forte permanece obrigatória no Approve e no Confirm: sessão `STRONG`, `authenticated_at` dentro de `forge.ledger.session_max_age_ms`, com `401 SESSION_STALE` fora da janela (`docs/planning/FDP-16A-v1.6-EXECUTION-CONTRACTS.md:416`). O Apply é um comando system e corretamente não exige novamente frescor da sessão humana, mas exige os grants atuais.

Os eventos financeiros continuam determinados: Confirm autorizado grava `budget.manual_reconciliation`; Apply bem-sucedido grava exatamente `budget.settled` ou `budget.released` (`docs/planning/FDP-16A-v1.6-EXECUTION-CONTRACTS.md:346-348`). A recusa por revogação não pode gravar evento financeiro; o contrato admite no máximo um `authz.denied` por `command_id` (`docs/planning/FDP-16A-v1.6-EXECUTION-CONTRACTS.md:420`).

**Conclusão C-01: FECHADO.**

## C-02 / NEW-MEDIUM-11 — parcialmente fechado

A maior parte da condição foi corrigida corretamente.

O schema agora define `pending_provider_cost` como append-only, com chave única `(operation_id, proof_id)`; `operation_id` isolado deixou de ser único. Não há update nem delete, e reinserir o mesmo par não altera o valor (`docs/planning/FDP-16A-v1.6-EXECUTION-CONTRACTS.md:463`).

`operation.pending_actual_minor` passou a ser somente uma projeção:

- nulo quando não existem linhas;
- `max(amount_minor)` quando as linhas usam a moeda do build;
- nunca atribuído diretamente pelo comando;
- não representa escolha da prova verdadeira.

Evidência: `docs/planning/FDP-16A-v1.6-EXECUTION-CONTRACTS.md:98,463`.

Os casos centrais estão adequados:

- LEDGER-08 exige a linha do receipt de 30, reason `CONFLICT`, e falha se a projeção existir sem a linha (`...MATRIX-v1.6-CANONICAL.md:69`);
- LEDGER-15 começa com operação `DISPATCHED`, reserva `HELD=50` e total `reserved=150`, insere a linha imutável de 200 e impede release (`...MATRIX-v1.6-CANONICAL.md:76`);
- LEDGER-17 mantém duas provas e duas linhas, 30 e 40, projeta 40 e rejeita qualquer resultado dependente da ordem do lock (`...MATRIX-v1.6-CANONICAL.md:78`).

Entretanto, a cobertura não fecha toda a regra declarada.

### NEW-MEDIUM-12 — late evidence contradiz a regra de inserção universal

**Severidade:** MEDIUM  
**Impacto:** impede `PASS` documental incondicional, mas não reabre um HIGH financeiro.

A regra geral afirma inequivocamente:

> Toda transição `CONFLICT` que contenha receipts conclusivos insere uma linha por proof.

Isso aparece em `docs/planning/FDP-16A-v1.6-EXECUTION-CONTRACTS.md:461,463` e é repetido em F-015 (`docs/planning/FDP-19A-v1.6-STORY-ACCEPTANCE-REGISTER.md:673`).

Porém, os textos específicos de late evidence dizem que a linha é inserida apenas “when the movement was a RELEASE”:

- tabela de transições em `docs/planning/FDP-16A-v1.6-EXECUTION-CONTRACTS.md:350`;
- regra narrativa de late evidence em `docs/planning/FDP-16A-v1.6-EXECUTION-CONTRACTS.md:405`.

A própria linha 405 enumera três conflitos tardios:

1. movimento `RELEASE` seguido de receipt conclusivo;
2. `SETTLEMENT` seguido de no-effect conclusivo;
3. `SETTLEMENT` seguido de receipt conclusivo com valor diferente.

Mas só manda inserir pending no primeiro. Isso contradiz a regra universal das linhas 461/463. Em particular, um settlement anterior de 30 seguido de receipt conclusivo de 40 entra em `CONFLICT`, preserva as provas e não move dinheiro novamente, mas as linhas 350/405 não mandam materializar as linhas 30/40.

LEDGER-17 cobre somente a corrida entre dois receipts antes de qualquer movimento. Portanto, não detecta essa divergência tardia (`docs/planning/FDP-TRACEABILITY-MATRIX-v1.6-CANONICAL.md:78`).

**Correção precisa:**

1. Em `FDP-16A:350` e `FDP-16A:405`, substituir a condição “quando o movimento foi RELEASE” pela regra uniforme: qualquer entrada em `CONFLICT` insere, idempotentemente, uma linha `(operation_id, proof_id)` para cada receipt conclusivo relacionado, reason `CONFLICT`.
2. Explicitar que:
   - RELEASE seguido de receipt insere a linha daquele receipt;
   - SETTLEMENT de 30 seguido de receipt de 40 mantém/inclui linhas para ambos os receipts e projeta 40;
   - SETTLEMENT seguido de no-effect conclusivo mantém/inclui a linha do receipt já existente;
   - nenhum desses casos cria segundo movement ou altera novamente `spent`/`reserved`.
3. Ampliar LEDGER-17 ou criar um oracle complementar para os conflitos tardios acima. O oracle deve verificar linhas, projeção, preservação das provas, ausência de segundo movimento e counters inalterados.

**Conclusão C-02: PARCIALMENTE FECHADO.**

## Invariantes e regressões

Não foi identificada regressão Critical/High.

Permanecem preservados:

- ordem de locks Build → Operation → Reservation → ManualReconciliation;
- unicidade de `operation_money_movement.operation_id` e `command_id`;
- atualização de counters e movement na mesma transação;
- receipt conclusivo contra no-effect conclusivo nunca resulta em release ou settlement;
- receipt conclusivo prevalece sobre alegação inconclusiva;
- prova `UNVERIFIED` não liquida, não libera nem autoriza;
- prova financeira só pode ser capturada por `forge.provider_ingest`;
- separação entre capturador, solicitante, confirmador e system Apply;
- impossibilidade de segundo movimento;
- `spent + reserved <= limit`;
- `reserved` igual à soma das reservas `HELD`.

O finding MEDIUM acima afeta a completude da materialização de pending cost depois de um movimento já existente. Não permite segundo movimento, não apaga prova e não converte conflito em sucesso; por isso não reabre HIGH-01, NEW-HIGH-07, NEW-HIGH-08 ou NEW-HIGH-09.

## Contagens, fontes e integridade

A inspeção independente encontrou:

- **90 oráculos**, todos `NOT RUN`;
- **41 linhas** no story index;
- **41 histórias** em FDP-19A;
- **41 blocos `Inherited`**;
- **41 DoR operacionais `Not met`**;
- **17 P0 históricos**, uma linha por ID e com os intents originais;
- **11 estados de Task** preservados.

Os 17 P0 e seus intents coincidem com FDP-13 original em `historical/round4/docs/source-material/chat-extracts/FDP-13-v1.0__msg077.md:2272-2288`.

Os 11 estados são `QUEUED`, `READY`, `RUNNING`, `WAITING`, `RETRYING`, `HANDOFF`, `REVIEWING`, `BLOCKED`, `COMPLETED`, `FAILED` e `CANCELLED`, conforme FDP-12 original em `historical/round4/docs/source-material/chat-extracts/FDP-12-v1.0__msg074.md:1134-1147` e FDP-16A v1.6 em `docs/planning/FDP-16A-v1.6-EXECUTION-CONTRACTS.md:8,63`.

F-015 referencia COST-01, LEDGER-01…17 e IDEM-01, e distingue requisitos herdados das adições v1.3–v1.6 (`docs/planning/FDP-19A-v1.6-STORY-ACCEPTANCE-REGISTER.md:645-673`).

Não encontrei corrupção da história v1.5 nem reescrita indevida dos documentos preservados. O parecer Round 8 permanece tanto no caminho original quanto em `historical/round8/`. Os ponteiros normativos relativos da v1.6 resolvem para arquivos existentes (`docs/planning/FDP-16A-v1.6-EXECUTION-CONTRACTS.md:3` e `docs/planning/FDP-17-v1.6-TESTING-STRATEGY.md:3`). Os links absolutos do parecer histórico conservam o workspace original da auditoria Round 8; são proveniência histórica, não autoridade normativa da v1.6, e não devem ser “corrigidos” mediante edição do snapshot.

## Gate documental versus gate operacional

Este `PASS WITH CONDITIONS` é exclusivamente documental. Não demonstra implementação, comportamento real de banco, provider, attestations, segurança operacional, staging, restore, RPO/RTO, capacidade ou execução dos 90 oráculos.

O DoR operacional continua **NOT MET** nas 41 histórias porque pessoa responsável, horas e timebox permanecem pendentes. Isso não deve ser confundido com a suficiência técnica do texto de aceitação.

Também permanecem separados e pendentes:

- confirmação humana de FDP-14;
- aprovação humana de FDP-15;
- aprovação geral do Founder;
- autorização de BUILD-00;
- testes, spikes, providers e staging;
- classes B e C e drills;
- metas HIR/TFV dependentes de amostra real.

Nenhuma dessas aprovações pode ser inferida dos relatórios Round 9, do checker ou deste parecer.

## Recomendação final

Aceitar a baseline v1.6 como **documentalmente PASS WITH CONDITIONS**, com C-01 fechado e C-02 condicionado apenas à correção de `FDP-16A:350,405` e à cobertura oracle do late evidence.

Após essa correção dirigida e sua verificação documental, não restará fundamento para manter a condição MEDIUM ou exigir nova rodada arquitetural. Até lá, FDP-14 e FDP-15 continuam pendentes, o Founder não aprovou a baseline, o DoR operacional permanece `NOT MET` e **BUILD-00 não está autorizado**.