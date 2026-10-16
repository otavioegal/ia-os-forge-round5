# Parecer independente — Full Duplex v0.11

**Checkout examinado:** `9522d5b090d451cc61face6e23a3f0b5081bf62f`  
**Modalidade:** auditoria documental estática, independente e somente leitura  
**Execução:** nenhum teste, checker, script, migration, PostgreSQL, build, provider ou deploy executado  
**BUILD-00:** **NÃO AUTORIZADO**  
**Veredito exclusivo:** **FAIL DOCUMENT-ONLY**

## 1. Conclusão executiva

A v0.11 corrige, no código inspecionado, os bypasses de validação identificados na v0.10:

- tipos escalares, UUIDs e objetos aninhados passam pela validação genérica antes da lógica de ACK;
- `rollback_model`, `interleave`, `sequential_replay`, `replay_receiver_removed` e `replay_cross_tenant` possuem schemas fechados;
- listas relevantes têm cardinalidade mínima;
- `commit_order` e `expected_steps` têm tipos de elementos e igualdade de comprimento;
- o checker histórico agora compara `bytes` com o comprimento obtido por `git cat-file`.

Entretanto, o pacote não satisfaz integralmente a ordem corretiva:

1. A afirmação de mutação de “cada campo declarado, inclusive aninhado” é mais ampla que a implementação. `type_failures()` inspeciona somente a primeira ocorrência de cada `kind` e somente o primeiro elemento de cada lista. Campos opcionais ausentes nessa primeira ocorrência não recebem mutação.
2. As mutações de ausência cobrem um único `setup`, um único `step` e o `attempt` do rollback, mas não exercitam separadamente todos os obrigatórios de `replay`, `fresh`, `probe` e cada variante de `setup`.
3. A saída autoral `REHASHED 138` / `BYTES MATCH` não foi reproduzida nesta auditoria. A inspeção confirma que o código faria a comparação real, mas não autoriza adotar a execução registrada pelo autor como verificação independente.
4. NEW-MEDIUM-09 continua necessariamente **PARTIAL / NOT FULLY VERIFIED** até ato humano sobre o conflito real do parecer v0.2.
5. LOW-01 permanece bloqueador de DoR; portanto, PASS global continua vedado.

Não identifiquei regressão material no modelo documental de replay, isolamento, ACK negativo, high-water ou zero movimento financeiro.

## 2. Matriz de findings

| Finding | Resultado independente v0.11 | Estado |
|---|---|---|
| FD07-01..04 | Contratos documentais preservados | CLOSED documental |
| FD07-05 | ACK negativo e zero movimento preservados | CLOSED documental |
| FD07-06 | Isolamento tenant/trio preservado no modelo estático | CLOSED documental |
| FD07-07 | Nenhuma concorrência PostgreSQL executada | **OPEN** |
| FD07-08 | Replay do outcome original preservado | CLOSED documental, limite estático |
| FD07-09 | Comparação histórica foi endurecida, mas não executada nesta auditoria | CLOSED documental no escopo anterior; nova alegação não reproduzida |
| NEW-MEDIUM-07 | Transporte 200 separado do outcome original 422 | CLOSED documental |
| NEW-MEDIUM-08 | v0.1 incluída; manifest v0.11 não autorreferente | CLOSED documental |
| NEW-MEDIUM-09 | Governança correta; v0.2 continua ambíguo | **PARTIAL / NOT FULLY VERIFIED** |
| NEW-LOW-02 | Validação efetiva de presença, tipos, UUIDs e cardinalidades corrigida no código | **CLOSED documental, não executado** |
| NEW-LOW-03 | Schema corrigido; cobertura negativa declarada é incompleta | **PARTIAL / OPEN** |
| HIGH-03 | Sem evidência real de O92 | **PARTIAL** |
| LOW-01 | Pessoa PENDING, effort UNSTATED, DoR NOT MET | **OPEN BLOCKING DoR** |
| O92/O93 | PostgreSQL não executado | **NOT RUN** |
| O96–O99 | Não executados | **NOT RUN** |

## 3. NEW-MEDIUM-09 — governança do parecer v0.2

A proposta de governança está correta e não promove resolução inexistente:

- estado `PENDING HUMAN APPROVAL`;
- nenhuma edição do parecer original;
- cabeçalho `FAIL` e fecho `FAIL — DOCUMENT-ONLY` preservados;
- `chosen_verdict` permanece `null`;
- autoridade reservada ao Founder ou autor;
- cadeia mantida como `PARECER_CHAIN NOT_FULLY_VERIFIED`.

Evidência: [CMP-FD-16-V02-GOVERNANCE.md:3](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/CMP-FD-16-V02-GOVERNANCE.md:3), [linha 5](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/CMP-FD-16-V02-GOVERNANCE.md:5), [linha 7](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/CMP-FD-16-V02-GOVERNANCE.md:7) e [linha 15](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/CMP-FD-16-V02-GOVERNANCE.md:15).

O checker também recusa:

- `chosen_verdict` não nulo;
- `approval` diferente de `PENDING`;
- promoção de `verdict_status`;
- divergência entre as duas strings registradas e o parecer lido.

Evidência: [check_fd_historical_manifest.py:156](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/tools/check_fd_historical_manifest.py:156) e [linha 166](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/tools/check_fd_historical_manifest.py:166).

### Blobs, bytes e não modificação histórica

O código compara, para cada path:

- blob Git declarado;
- SHA-256 do conteúdo;
- comprimento real do blob contra `bytes`;
- igualdade base/parent dos blobs de planejamento.

Evidência: [check_fd_historical_manifest.py:200](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/tools/check_fd_historical_manifest.py:200), [linha 206](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/tools/check_fd_historical_manifest.py:206), [linha 210](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/tools/check_fd_historical_manifest.py:210) e [linha 212](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/tools/check_fd_historical_manifest.py:212).

Há também mutação específica de `bytes`, esperando `FAIL_BYTES`: [check_fd_historical_manifest.py:289](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/tools/check_fd_historical_manifest.py:289).

Isso corrige o defeito de implementação da v0.10. Contudo, como nenhuma operação Git/checker foi executada nesta revisão, os valores concretos de `bytes`, blob e SHA-256 permanecem **não reproduzidos independentemente**. A saída autoral em [CMP-FD-12-CONSISTENCY-REPORT.md:89](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/CMP-FD-12-CONSISTENCY-REPORT.md:89) é relato do autor, não execução desta auditoria.

Conclusão: NEW-MEDIUM-09 permanece **PARTIAL**, corretamente rotulado `NOT_FULLY_VERIFIED`.

## 4. NEW-LOW-02 e NEW-LOW-03

### Validação efetivamente corrigida

A rotina genérica distingue:

- UUID de tipo errado: `FAIL_TYPE`;
- string UUID malformada: `FAIL_UUID`;
- booleano usado como inteiro: `FAIL_TYPE`;
- constantes inválidas: `FAIL_SCHEMA`;
- arrays e objetos de tipo errado: `FAIL_SCHEMA`;
- `minItems` e `minLength`.

Evidência: [check_fd_fx03_ack.py:777](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/tools/check_fd_fx03_ack.py:777).

A validação recursiva percorre objetos referenciados, objetos inline e elementos de arrays: [check_fd_fx03_ack.py:846](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/tools/check_fd_fx03_ack.py:846) e [linha 881](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/tools/check_fd_fx03_ack.py:881).

Assim, os bypasses concretos da v0.10 foram fechados no fluxo inspecionado:

- `interleave.steps` exige lista não vazia e objetos `step`: [schema:592](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/fixtures/CMP-FD-FX-03-ack.schema.json:592).
- `sequential_replay.commit_order` exige inteiros, `expected_steps` exige strings não vazias e ambos têm mesmo comprimento: [schema:722](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/fixtures/CMP-FD-FX-03-ack.schema.json:722), [linha 795](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/fixtures/CMP-FD-FX-03-ack.schema.json:795) e [linha 826](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/fixtures/CMP-FD-FX-03-ack.schema.json:826).
- `rollback_model` valida todos os escalares e o `attempt` aninhado: [schema:833](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/fixtures/CMP-FD-FX-03-ack.schema.json:833).
- `replay_receiver_removed` exige `setup` não vazio, `replay` e `fresh`: [schema:1009](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/fixtures/CMP-FD-FX-03-ack.schema.json:1009).
- `replay_cross_tenant` exige `setup` não vazio e `probe`: [schema:1052](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/fixtures/CMP-FD-FX-03-ack.schema.json:1052).

A chamada a `fields_error()` ocorre antes das ramificações semânticas por `kind`: [check_fd_fx03_ack.py:1021](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/tools/check_fd_fx03_ack.py:1021) e [linha 1039](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/tools/check_fd_fx03_ack.py:1039). Não encontrei bypass direto desses tipos para a lógica de ACK.

### Novo defeito de cobertura: FD11-NEW-01 — mutações não exaustivas

A documentação afirma que “cada campo declarado, inclusive aninhado” é mutado: [CMP-FD-15-SCHEMA.md:20](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/CMP-FD-15-SCHEMA.md:20).

A implementação não comprova isso integralmente:

- `seen` faz `type_failures()` coletar apenas a primeira ocorrência de cada `kind`;
- `collect()` ignora campos que não estão presentes nessa ocorrência;
- arrays têm apenas o elemento `[0]` inspecionado;
- portanto, campos opcionais presentes somente em ocorrências posteriores de `negative`/`positive` não recebem mutação;
- múltiplos itens de `setup`/`steps` também não são exercitados.

Evidência: [check_fd_fx03_ack.py:1140](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/tools/check_fd_fx03_ack.py:1140), especialmente [linha 1145](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/tools/check_fd_fx03_ack.py:1145), [linha 1152](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/tools/check_fd_fx03_ack.py:1152) e [linha 1173](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/tools/check_fd_fx03_ack.py:1173).

A cobertura de remoção também é amostral:

- um `step`;
- o primeiro caso que contenha `setup`;
- apenas o `attempt` do rollback.

Ela não remove independentemente cada obrigatório de `replay`, `fresh`, `probe` e dos demais objetos `setup`: [check_fd_fx03_ack.py:1265](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/tools/check_fd_fx03_ack.py:1265).

Exceções são capturadas como `FAIL_SCHEMA_EXCEPTION`, o que evita sucesso silencioso, mas não transforma a cobertura incompleta em exaustiva: [check_fd_fx03_ack.py:1186](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/tools/check_fd_fx03_ack.py:1186) e [linha 1286](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/tools/check_fd_fx03_ack.py:1286).

Resultado:

- NEW-LOW-02: corrigido documentalmente quanto aos bypasses de validação;
- NEW-LOW-03: **PARTIAL**, porque a implementação do schema está adequada, mas a alegação de cobertura negativa total é falsa.

## 5. Preservações obrigatórias

O pacote mantém explicitamente:

- FD07-07 **OPEN**;
- HIGH-03 **PARTIAL**;
- LOW-01 **OPEN BLOCKING DoR**;
- pessoa `PENDING`;
- effort `UNSTATED`;
- DoR `NOT MET`;
- O92/O93 **NOT RUN**;
- O96–O99 **NOT RUN**.

Evidência: [CMP-FD-07-ORACLES.md:3](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/CMP-FD-07-ORACLES.md:3), [linha 5](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/CMP-FD-07-ORACLES.md:5) e [linha 11](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/CMP-FD-07-ORACLES.md:11).

A concorrência PostgreSQL continua apenas especificada: [CMP-FD-13-CONCURRENCY-SPEC.md:3](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/CMP-FD-13-CONCURRENCY-SPEC.md:3) e [linha 9](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/CMP-FD-13-CONCURRENCY-SPEC.md:9).

Replay 422/200, 409 sem substituição, tenant 404, null-pair, ACK negativo e zero movimento permanecem documentados: [CMP-FD-02-ACK-REPLAY.md:8](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v11-codex-independent/docs/planning/conversational-full-duplex-v0.11/CMP-FD-02-ACK-REPLAY.md:8).

## 6. Próximas correções precisas

1. Alterar `type_failures()` para gerar mutações a partir do schema, não apenas dos campos presentes na primeira ocorrência de cada `kind`.
2. Criar uma fixture mínima sintética para cada campo opcional declarado, garantindo que todos sejam efetivamente exercitados.
3. Percorrer todos os elementos de `setup`, `steps`, `commit_order` e `expected_steps`, ou documentar explicitamente que a mutação é por regra representativa, não por ocorrência.
4. Remover separadamente cada obrigatório de:
   - `rollback_model.attempt`;
   - `replay_receiver_removed.setup[*]`;
   - `replay_receiver_removed.replay`;
   - `replay_receiver_removed.fresh`;
   - `replay_cross_tenant.setup[*]`;
   - `replay_cross_tenant.probe`;
   - `interleave.steps[*]`.
5. Fazer o relatório informar contagens esperadas e observadas de regras, campos e mutações. Falhar se alguma regra declarada não tiver mutação.
6. Manter v0.2 com `chosen_verdict: null`, `PENDING_HUMAN_APPROVAL`, `NOT_VERIFIED` e `PARECER_CHAIN NOT_FULLY_VERIFIED`.
7. Não modificar o parecer v0.2; eventual resolução deve ser errata aditiva aprovada por humano.
8. Reproduzir a comparação de bytes/blobs em futura auditoria autorizada e somente leitura; até lá, tratar `BYTES MATCH` como relato autoral.
9. Não fechar FD07-07 ou HIGH-03 sem PostgreSQL real autorizado e evidência de O92/O93.
10. Resolver LOW-01 apenas por ato humano: responsável nominal, esforço e DoR satisfeitos.
11. Manter BUILD-00, migrations, PostgreSQL, providers, deploy e ativação de flags **não autorizados**.

**Veredito final: FAIL DOCUMENT-ONLY.**

A v0.11 corrige o mecanismo de schema, mas ainda exagera a abrangência das mutações negativas, não permite reproduzir nesta auditoria a alegação concreta de bytes/blobs e, por desenho correto, mantém a cadeia v0.2 incompleta. LOW-01 continua bloqueando qualquer PASS global.