# Parecer independente — IA OS Forge Round 10

**Data:** 13 de outubro de 2026  
**Commit auditado:** `0c42373d583dec420348efd7bc0b8c6228a66f47`  
**Modalidade:** auditoria documental independente, estritamente read-only. Nenhum arquivo foi alterado e nenhum teste, build, checker, banco, provider, staging ou drill foi executado.

## Veredito executivo

| Dimensão | Veredito |
|---|---|
| Prontidão documental v1.7 | **PASS** |
| NEW-MEDIUM-12 | **FECHADO** |
| C-01 / NEW-MEDIUM-10 | **PERMANECE FECHADO** |
| HIGH-01, NEW-HIGH-07, NEW-HIGH-08 e NEW-HIGH-09 | **PERMANECEM FECHADOS** |
| Novo CRITICAL/HIGH/MEDIUM | **NÃO IDENTIFICADO** |
| Finding novo | **1 LOW editorial, não bloqueante** |
| Prontidão operacional | **NOT MET / NÃO DEMONSTRADA** |
| FDP-14 | **PENDENTE DE CONFIRMAÇÃO DO FOUNDER** |
| FDP-15 | **PENDENTE DE APROVAÇÃO DO FOUNDER** |
| Aprovação geral do Founder | **NÃO CONCEDIDA NEM PRESUMIDA** |
| BUILD-00 | **NÃO AUTORIZADO** |

O SHA solicitado foi confirmado diretamente em [.git/refs/heads/main](C:/Users/User/AppData/Local/Temp/ia-os-forge-round10-codex-independent/.git/refs/heads/main:1).

O **PASS é exclusivamente documental**. A última condição substantiva do parecer Round 9 — NEW-MEDIUM-12 — está integralmente fechada. Não há fundamento documental para `PASS WITH CONDITIONS`, `FAIL` ou para inventar outra rodada arquitetural.

## 1. Fechamento preciso de NEW-MEDIUM-12

O Round 9 havia identificado uma contradição: a regra geral exigia uma linha imutável por receipt conclusivo em todo `CONFLICT`, mas a regra específica de late evidence limitava a inserção ao caso posterior a `RELEASE` ([parecer Round 9](C:/Users/User/AppData/Local/Temp/ia-os-forge-round10-codex-independent/docs/reviews/PARECER-CODEX-ROUND9-2026-10-13.md:95)).

A v1.7 elimina essa restrição.

### Regra normativa uniforme

A transição tardia agora estabelece que, depois de `SETTLEMENT` ou `RELEASE`:

- a operação entra em `BLOCKED_RECONCILIATION / CONFLICT`;
- o movement original permanece;
- não há segundo movement;
- `spent` e `reserved` permanecem nos valores já comprometidos;
- é inserida idempotentemente uma linha de `pending_provider_cost` para **cada receipt conclusivo**;
- a regra vale após `RELEASE` e após `SETTLEMENT`;
- nenhum receipt é inventado para uma prova `NO_EFFECT`;
- o evento é `budget.proof_conflict`.

Evidência normativa: [FDP-16A v1.7:350](C:/Users/User/AppData/Local/Temp/ia-os-forge-round10-codex-independent/docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md:350).

A serialização também não encerra prematuramente o caso como `ALREADY_SETTLED` ou `ALREADY_RELEASED`: quando há prova conclusiva contraditória, deve executar a transição de late evidence, sem novo movimento e sem mudar os contadores ([FDP-16A v1.7:368](C:/Users/User/AppData/Local/Temp/ia-os-forge-round10-codex-independent/docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md:368)).

### Três trajetórias exigidas

As três situações foram explicitadas no contrato:

1. **RELEASE → receipt 30**

   Mantém um único movement `RELEASE`, `spent=800`, `reserved=100`; insere uma linha para o receipt 30, `reason=CONFLICT`, e projeta `pending_actual_minor=30`.

2. **SETTLEMENT 30 → receipt 40**

   Mantém um único movement `SETTLEMENT`, `spent=830`, `reserved=100`; insere/mantém duas linhas, 30 e 40, ambas `CONFLICT`; projeta `max(30,40)=40`, sem escolher uma prova como verdadeira.

3. **SETTLEMENT 30 → NO_EFFECT**

   Mantém o settlement e os contadores; insere a linha do receipt 30 já conhecido, se ainda ausente; não cria linha nem valor fictício para `NO_EFFECT`.

Evidência: [FDP-16A v1.7:405](C:/Users/User/AppData/Local/Temp/ia-os-forge-round10-codex-independent/docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md:405).

### Imutabilidade e idempotência

O schema determina:

- tabela append-only;
- chave única `(operation_id, proof_id)`;
- `operation_id` isolado não é único;
- nenhuma atualização ou exclusão;
- reinserção do mesmo par não altera o valor;
- uma linha por receipt conclusivo em toda transição `CONFLICT`, inclusive depois de movement;
- `pending_actual_minor` é somente projeção;
- repetição não produz segundo `budget.proof_conflict`.

Evidência: [FDP-16A v1.7:471](C:/Users/User/AppData/Local/Temp/ia-os-forge-round10-codex-independent/docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md:471).

Assim, NEW-MEDIUM-12 está **FECHADO**.

## 2. F-015 e LEDGER-18

F-015 incorporou explicitamente LEDGER-18 e a regra tardia:

- lista de testes inclui `LEDGER-01…18`;
- conflito posterior a movement não está limitado a `RELEASE`;
- settlement 30 seguido de receipt 40 conserva as duas linhas e projeta 40;
- settlement seguido de no-effect conserva o receipt conhecido;
- `spent` e `reserved` não mudam novamente.

Evidência: [FDP-19A v1.7:645](C:/Users/User/AppData/Local/Temp/ia-os-forge-round10-codex-independent/docs/planning/FDP-19A-v1.7-STORY-ACCEPTANCE-REGISTER.md:645) e [FDP-19A v1.7:661](C:/Users/User/AppData/Local/Temp/ia-os-forge-round10-codex-independent/docs/planning/FDP-19A-v1.7-STORY-ACCEPTANCE-REGISTER.md:661).

LEDGER-18 contém três fixtures independentes e critérios positivos e negativos conclusivos:

- valores exatos de `spent` e `reserved`;
- uma ou duas linhas pending conforme o cenário;
- projeções 30 ou 40;
- preservação de todas as provas;
- exatamente um movement;
- exatamente um `budget.proof_conflict`;
- replay sem segunda linha ou segundo evento;
- proibição de novo `budget.settled` ou `budget.released`.

Evidência: [matriz v1.7:79](C:/Users/User/AppData/Local/Temp/ia-os-forge-round10-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.7-CANONICAL.md:79).

A cobertura é suficiente para detectar precisamente a falha apontada no Round 9.

## 3. LEDGER-17 preservado

LEDGER-17 continua sendo o caso anterior a qualquer movement: corrida simultânea entre receipts 30 e 40, duas linhas pending, projeção 40, nenhum movement e contadores inalterados.

O texto da linha v1.7 é igual ao snapshot v1.6:

- [LEDGER-17 original v1.6](C:/Users/User/AppData/Local/Temp/ia-os-forge-round10-codex-independent/historical/round9/docs/planning/FDP-TRACEABILITY-MATRIX-v1.6-CANONICAL.md:78)
- [LEDGER-17 v1.7](C:/Users/User/AppData/Local/Temp/ia-os-forge-round10-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.7-CANONICAL.md:78)

LEDGER-18 acrescenta o cenário pós-movement sem redefinir LEDGER-17.

## 4. Regressões e findings

### Nenhuma regressão CRITICAL, HIGH ou MEDIUM

Não foi encontrada reabertura de:

- movimento financeiro único por operação;
- unicidade de movement;
- preservação de `spent + reserved <= limit`;
- correspondência de `reserved` às reservas `HELD`;
- precedência de prova;
- retenção das provas conflitantes;
- proibição de settlement/release por prova inconclusiva;
- separação entre ingest, operadores e Apply system;
- revalidação dos grants no Apply;
- C-01;
- HIGH-01, NEW-HIGH-07, NEW-HIGH-08 e NEW-HIGH-09.

O texto esclarece ainda que a reserva não retorna a `HELD` depois de movement e que não há redispatch ou write-off implícito ([FDP-16A v1.7:403](C:/Users/User/AppData/Local/Temp/ia-os-forge-round10-codex-independent/docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md:403)).

### LOW-01 — referência editorial residual à matriz v1.6

**Severidade:** LOW  
**Impacto:** não bloqueia o PASS e não torna ambíguo o oracle normativo.

[FDP-17 v1.7:3](C:/Users/User/AppData/Local/Temp/ia-os-forge-round10-codex-independent/docs/planning/FDP-17-v1.7-TESTING-STRATEGY.md:3) declara corretamente que a única matriz normativa é a v1.7 e que o documento não aponta para matrizes v1.0–v1.6. Porém, [FDP-17 v1.7:31](C:/Users/User/AppData/Local/Temp/ia-os-forge-round10-codex-independent/docs/planning/FDP-17-v1.7-TESTING-STRATEGY.md:31) diz que os identificadores suplementares são definidos “only in the v1.6 matrix”.

É uma referência de versão obsoleta, imediatamente desmentida pelo ponteiro normativo explícito da linha 3 e pelo índice Round 10 ([status index:9](C:/Users/User/AppData/Local/Temp/ia-os-forge-round10-codex-independent/docs/planning/FDP-ROUND10-STATUS-INDEX.md:9)). Não altera fixtures, pass/fail ou semântica financeira.

**Correção específica recomendada:** substituir apenas “v1.6 matrix” por “v1.7 matrix” em FDP-17:31. Trata-se de higiene editorial; não exige nova rodada nem condiciona este parecer.

## 5. Contagens e integridade estrutural

A inspeção documental encontrou:

- **91 oráculos**: 132 linhas de IDs na matriz menos as 41 linhas do story index;
- todos os 91 permanecem **NOT RUN**;
- **41 histórias** em FDP-19A;
- **41 entradas** no story index;
- **41 blocos `Inherited`**;
- **41 DoR operacionais `Not met`**;
- **17 identificadores P0 históricos**, com os intents literais preservados;
- **11 estados de Task** preservados.

Os 17 P0 estão enumerados em [FDP-17 v1.7:9](C:/Users/User/AppData/Local/Temp/ia-os-forge-round10-codex-independent/docs/planning/FDP-17-v1.7-TESTING-STRATEGY.md:9). Os 11 estados são `QUEUED`, `READY`, `RUNNING`, `WAITING`, `RETRYING`, `HANDOFF`, `REVIEWING`, `BLOCKED`, `COMPLETED`, `FAILED` e `CANCELLED` ([FDP-16A v1.7:8](C:/Users/User/AppData/Local/Temp/ia-os-forge-round10-codex-independent/docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md:8)).

A matriz mantém um único story index e F-015 aponta para COST-01, LEDGER-01…18 e IDEM-01 ([matriz v1.7:103](C:/Users/User/AppData/Local/Temp/ia-os-forge-round10-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.7-CANONICAL.md:103), [matriz v1.7:120](C:/Users/User/AppData/Local/Temp/ia-os-forge-round10-codex-independent/docs/planning/FDP-TRACEABILITY-MATRIX-v1.7-CANONICAL.md:120)).

## 6. História e aprovações preservadas

O parecer Round 9 permanece no caminho corrente e no snapshot [historical/round9](C:/Users/User/AppData/Local/Temp/ia-os-forge-round10-codex-independent/historical/round9/docs/reviews/PARECER-CODEX-ROUND9-2026-10-13.md:1). A v1.6 continua separada em `historical/round9/docs/planning/`, e LEDGER-17 foi preservado literalmente.

Os documentos Round 10 declaram corretamente que:

- a candidata não se autoaprova;
- FDP-14 continua aguardando confirmação do Founder;
- FDP-15 continua aguardando aprovação do Founder;
- nenhuma aprovação geral foi presumida;
- BUILD-00 não foi autorizado;
- testes, providers e drills continuam não executados.

Evidência: [pendências Round 10:6](C:/Users/User/AppData/Local/Temp/ia-os-forge-round10-codex-independent/docs/reviews/ROUND10-OPEN-PENDENCIES-2026-10-13.md:6) e [status index:3](C:/Users/User/AppData/Local/Temp/ia-os-forge-round10-codex-independent/docs/planning/FDP-ROUND10-STATUS-INDEX.md:3).

## 7. Gate documental versus prontidão operacional

O **PASS documental** significa que os contratos, critérios e oráculos da v1.7 são suficientes e internamente coerentes para fechar NEW-MEDIUM-12.

Ele não demonstra:

- implementação do comportamento;
- migrations ou constraints reais;
- execução dos 91 oráculos;
- atomicidade efetiva no banco;
- comportamento de providers;
- segurança operacional;
- staging, restore, RPO/RTO ou drills;
- capacidade, owner pessoal, horas ou timebox;
- autorização para iniciar BUILD-00.

Os 41 DoR operacionais continuam `Not met`; F-015, por exemplo, ainda tem pessoa, horas e calibração pendentes ([FDP-19A v1.7:685](C:/Users/User/AppData/Local/Temp/ia-os-forge-round10-codex-independent/docs/planning/FDP-19A-v1.7-STORY-ACCEPTANCE-REGISTER.md:685)).

## Conclusão

A baseline v1.7 recebe **PASS DOCUMENTAL**.

NEW-MEDIUM-12 está completamente fechado: todo `CONFLICT` com receipt conclusivo materializa uma linha imutável por `(operation_id, proof_id)`, inclusive depois de `RELEASE` ou `SETTLEMENT`; os três cenários tardios estão definidos; não há segundo movement nem segunda alteração de `spent`/`reserved`; `budget.proof_conflict` e sua idempotência estão especificados; LEDGER-18 possui fixtures e critérios pass/fail adequados; LEDGER-17 permanece inalterado.

O único finding novo é LOW e editorial. Não reabre C-01 ou qualquer HIGH, não condiciona o PASS e não justifica outra rodada. FDP-14, FDP-15, aprovação do Founder, prontidão operacional e BUILD-00 permanecem pendentes e separados deste resultado.