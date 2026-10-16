# Parecer independente — Full Duplex v0.12

**Checkout examinado:** `346cd04ae90bf57f4594e1a4b4af0584961dd546`  
**Modalidade:** auditoria documental estática, independente e somente leitura  
**Escopo lido:** todos os 19 arquivos da v0.12, parecer Codex v0.11, prompt corretivo v0.12, parecer histórico v0.2 e baselines/governança relevantes  
**Execução:** nenhum script, checker, teste, banco, migration, provider, build ou deploy executado  
**BUILD-00:** **NÃO AUTORIZADO**  
**Veredito exclusivo:** **FAIL DOCUMENT-ONLY**

## 1. Conclusão executiva

A v0.12 melhora substancialmente a cobertura da v0.11:

- `occurrence_jobs()` percorre cada caso e os índices presentes de `setup`, `steps`, `commit_order` e `expected_steps`;
- `attempt`, `replay`, `fresh`, `probe`, contadores e `initial_keys` recebem jobs próprios;
- hosts sintéticos cobrem opcionais ausentes nas linhas comportamentais e arrays com dois elementos;
- IDs duplicados de jobs declarados são recusados;
- ausência de host, exceção e código de erro divergente impedem o `PASS_FIXTURE_ONLY`;
- os limites `proves_product=false`, `oracle_status=NOT_RUN` e `product_input_exhaustive=false` estão expressos corretamente.

Contudo, o núcleo de FD11-NEW-01 permanece incompleto. A afirmação de que `schema_jobs` deriva cobertura de “cada campo do schema” e que `480/480` representa todas as regras declaradas é falsa por construção:

1. O schema contém objetos inline em `negative.expected_original_outcome_body` e `positive.expected_original_outcome_body`, com `required`, `allowed` e cinco subcampos.
2. O validador efetivamente percorre esses objetos inline.
3. O indexador de cobertura, porém, só recursa objetos que tenham `ref`.
4. `schema_jobs()` só itera os objetos top-level de `spec["objects"]`.
5. `occurrence_jobs()` só entra em objetos aninhados por chamadas manuais a `nest()` para os objetos nomeados; nunca entra em `expected_original_outcome_body`.
6. Arrays de objetos também não recebem mutação de tipo no elemento: o código exclui explicitamente `item_type == "object"`.

Consequentemente, `gap=0` significa somente “nenhuma lacuna dentro do catálogo produzido pelo próprio gerador”, não “todas as regras do schema cobertas”. Os números autorais `480/480` e `2239/2239` são internamente autoconsistentes, mas o universo declarado está subcontado.

Também não há detecção de chaves JSON duplicadas na origem: schema, fixture, sintéticos e manifesto são carregados com `json.loads()` comum. Os testes de IDs duplicados ocorrem somente depois do parse, quando uma chave JSON repetida já teria sido silenciosamente sobrescrita.

Portanto:

- **NEW-LOW-03:** **PARTIAL / OPEN**
- **FD11-NEW-01:** **OPEN**
- A v0.12 não satisfaz integralmente o prompt corretivo.
- O estado global continua **FAIL DOCUMENT-ONLY**.

## 2. Findings novos da auditoria v0.12

### FD12-NEW-01 — Objetos inline não entram no catálogo de cobertura

**Severidade:** MEDIUM  
**Estado:** OPEN  
**Impacto:** invalida a alegação de cobertura integral de campos/regras e os rótulos `schema_rules=all_declared`.

O schema declara o objeto inline de `negative.expected_original_outcome_body`, incluindo `error_code` obrigatório e os opcionais `opaque`, `retryable`, `terminal` e `peer_ack_high_water`: [schema:317](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/fixtures/CMP-FD-FX-03-ack.schema.json:317), [schema:320](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/fixtures/CMP-FD-FX-03-ack.schema.json:320) e [schema:330](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/fixtures/CMP-FD-FX-03-ack.schema.json:330). A mesma estrutura reaparece para `positive`: [schema:529](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/fixtures/CMP-FD-FX-03-ack.schema.json:529).

O validador reconhece objetos inline por `"fields" in rule`, verifica obrigatórios, extras e tipos recursivamente: [check_fd_fx03_ack.py:859](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/tools/check_fd_fx03_ack.py:859) e [check_fd_fx03_ack.py:863](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/tools/check_fd_fx03_ack.py:863).

Já o indexador de cobertura só recursa quando existe `ref`: [check_fd_fx03_ack.py:1221](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/tools/check_fd_fx03_ack.py:1221). O gerador de regras itera apenas `spec["objects"]`: [check_fd_fx03_ack.py:1256](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/tools/check_fd_fx03_ack.py:1256). Esses objetos inline não são entradas de `spec["objects"]`.

Em `occurrence_jobs()`, `nest()` também exige o nome de um objeto registrado e só é chamado manualmente para `attempt`, `setup`, `step` e `counter`: [check_fd_fx03_ack.py:1384](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/tools/check_fd_fx03_ack.py:1384).

Assim, não são mutados individualmente:

- ausência de `expected_original_outcome_body.error_code`;
- chave extra dentro do body;
- tipo e `minLength` de `error_code`;
- tipos de `opaque`, `retryable`, `terminal`;
- tipo de `peer_ack_high_water`;
- todas as ocorrências concretas desses subcampos.

Isso contradiz diretamente:

- “uma mutação por campo do schema”: [CMP-FD-09:5](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/CMP-FD-09-CHANGE-REPORT.md:5);
- “para cada objeto e cada campo”: [CMP-FD-17:7](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/CMP-FD-17-COVERAGE.md:7);
- `schema_rules=all_declared`: [CMP-FD-17:20](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/CMP-FD-17-COVERAGE.md:20).

### FD12-NEW-02 — Tipo dos elementos de arrays de objetos não é exercitado

**Severidade:** LOW  
**Estado:** OPEN

O schema declara vários arrays com itens `{type: "object", ref: ...}`: `initial_keys`, `setup` e `steps`. O validador rejeita um elemento escalar ou lista no lugar do objeto.

Entretanto, `schema_jobs()` exclui explicitamente objetos da geração de `ELEMENT_TYPE`: [check_fd_fx03_ack.py:1290](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/tools/check_fd_fx03_ack.py:1290) e [check_fd_fx03_ack.py:1293](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/tools/check_fd_fx03_ack.py:1293).

`occurrence_jobs()` remove e altera campos dentro dos objetos, mas não substitui cada elemento por um valor não objeto. Logo, o caminho de `value_error(element, {"type":"object"})` não recebe mutação dedicada.

Isso contraria a exigência corretiva de mutar “objetos e arrays” e reduz ainda mais o universo real por trás das 480 regras.

### FD12-NEW-03 — Chaves JSON duplicadas são invisíveis após o parse

**Severidade:** LOW  
**Estado:** OPEN

Os quatro JSONs relevantes são carregados por `json.loads()` comum:

- schema: [check_fd_fx03_ack.py:763](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/tools/check_fd_fx03_ack.py:763);
- sintéticos: [check_fd_fx03_ack.py:1586](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/tools/check_fd_fx03_ack.py:1586);
- fixture comportamental: [check_fd_fx03_ack.py:1693](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/tools/check_fd_fx03_ack.py:1693);
- manifesto histórico: [check_fd_historical_manifest.py:300](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/tools/check_fd_historical_manifest.py:300).

Não há `object_pairs_hook` ou parser equivalente que rejeite chaves repetidas. As verificações de duplicação em [check_fd_fx03_ack.py:1616](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/tools/check_fd_fx03_ack.py:1616) e [check_fd_fx03_ack.py:1634](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/tools/check_fd_fx03_ack.py:1634) cobrem IDs de jobs já gerados, não chaves duplicadas no JSON-fonte.

Não identifiquei visualmente chaves repetidas nos arquivos atuais; o finding é sobre uma via não protegida e capaz de produzir cobertura vacuamente reduzida.

## 3. Avaliação de `480/480` e `2239/2239`

| Alegação | Resultado independente |
|---|---|
| 480 regras declaradas | **Não reproduzida**; relato autoral |
| 480 regras exercitadas | **Não reproduzida**; além disso, o catálogo omite regras inline e elementos objeto |
| 2.239 ocorrências declaradas | **Não reproduzida**; relato autoral |
| 2.239 ocorrências exercitadas | **Não reproduzida**; ocorrências de subcampos inline estão ausentes |
| IDs de regras únicos | Implementação rejeita duplicação após geração |
| IDs de ocorrências únicos | Implementação rejeita duplicação após geração |
| Cobertura de cada caso e índice listado | Melhoria real e amplamente implementada |
| Cobertura de todos os campos do schema | **Falsa** |
| `gap=0` | Verdade apenas em relação ao catálogo incompleto produzido pelo mesmo checker |
| Prova de produto/oráculo | Corretamente negada |

A documentação trata os números como relato autoral em [CMP-FD-12:3](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/CMP-FD-12-CONSISTENCY-REPORT.md:3), o que é adequado. O problema são as qualificações mais fortes `schema_rules=all_declared` e “cada campo”.

## 4. Hosts sintéticos

Os quatro hosts estão corretamente segregados das 26 linhas comportamentais e declaram:

- `proves_product: false`;
- `oracle_status: NOT_RUN`;
- propósito apenas de mutation host.

Evidência: [synthetic:2](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/fixtures/CMP-FD-FX-03-ack.synthetic.json:2).

Os hosts de `positive` e `negative` incluem os opcionais de primeiro nível, e os dois hosts estruturais fornecem `setup` com dois elementos. Isso corrige a falha amostral principal da v0.11.

Porém, reunir todos os opcionais em um único caso não corrige a ausência de recursão nos objetos inline. O body existe, mas seus subcampos não se tornam regras ou ocorrências independentes.

## 5. Matriz de findings

| Finding | Resultado v0.12 | Estado independente |
|---|---|---|
| FD07-01..06 | Contratos preservados documentalmente | CLOSED documental |
| FD07-07 | Nenhuma concorrência PostgreSQL executada | **OPEN** |
| FD07-08 | Replay do outcome original preservado | CLOSED documental, limite estático |
| FD07-09 | Código de comparação histórica preservado; não executado | CLOSED documental no escopo anterior |
| NEW-MEDIUM-06 | Migration não executada | CLOSED documental / NOT RUN operacional |
| NEW-MEDIUM-07 | Transporte 200 separado do outcome original 422 | CLOSED documental |
| NEW-MEDIUM-08 | Cadeia inclui v0.1 e evita autorreferência v0.12 | CLOSED documental |
| NEW-MEDIUM-09 | Governança preservada; conflito v0.2 sem ato humano | **PARTIAL / NOT_FULLY_VERIFIED** |
| NEW-LOW-02 | Validação de tipos/schema preservada | CLOSED documental, não executada |
| NEW-LOW-03 | Melhorada, mas cobertura total continua falsa | **PARTIAL / OPEN** |
| FD11-NEW-01 | Primeira ocorrência/índice corrigidos; campos inline e elementos objeto omitidos | **OPEN** |
| FD12-NEW-01 | Objetos inline ausentes do catálogo | **OPEN** |
| FD12-NEW-02 | Elementos objeto de arrays sem mutação de tipo | **OPEN** |
| FD12-NEW-03 | Chaves JSON duplicadas não são recusadas | **OPEN** |
| HIGH-03 | Sem evidência real de O92 | **PARTIAL** |
| LOW-01 | Pessoa PENDING, effort UNSTATED, DoR NOT MET | **OPEN BLOCKING DoR** |
| O92/O93 | PostgreSQL não executado | **NOT RUN** |
| O96–O99 | Não executados | **NOT RUN** |

As preservações obrigatórias estão explícitas em [CMP-FD-07:5](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/CMP-FD-07-ORACLES.md:5), [CMP-FD-07:11](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/CMP-FD-07-ORACLES.md:11) e [CMP-FD-07:17](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/CMP-FD-07-ORACLES.md:17).

## 6. Histórico v0.2 e alegações de blobs

A governança histórica foi preservada corretamente:

- `status: PENDING_HUMAN_APPROVAL`;
- `approval: PENDING`;
- `chosen_verdict: null`;
- `verdict_status: NOT_VERIFIED`;
- `PARECER_CHAIN NOT_FULLY_VERIFIED`;
- cabeçalho `FAIL` e fecho `FAIL — DOCUMENT-ONLY` mantidos sem escolha artificial.

Evidência: [manifest:23](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/fixtures/CMP-FD-FX-04-historical-manifest.json:23), [manifest:26](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/fixtures/CMP-FD-FX-04-historical-manifest.json:26), [manifest:29](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/fixtures/CMP-FD-FX-04-historical-manifest.json:29) e [CMP-FD-16:7](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/CMP-FD-16-V02-GOVERNANCE.md:7).

Por inspeção, o checker compara:

- path set;
- blob Git;
- SHA-256;
- `len(data)` contra `bytes`;
- igualdade base/parent;
- conteúdo dos pareceres;
- conjunto de prompts.

Evidência: [check_fd_historical_manifest.py:200](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/tools/check_fd_historical_manifest.py:200) e [check_fd_historical_manifest.py:211](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/tools/check_fd_historical_manifest.py:211).

A mutação `bytes+1` existe: [check_fd_historical_manifest.py:289](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/tools/check_fd_historical_manifest.py:289).

Entretanto, os valores concretos de blob, SHA-256, bytes, “155 paths” e `BYTES MATCH` não foram executados nem reproduzidos nesta auditoria. Permanecem exclusivamente **alegações verificáveis por código**, não evidência independente. A própria documentação rotula isso corretamente em [CMP-FD-14:18](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v12-codex-independent/docs/planning/conversational-full-duplex-v0.12/CMP-FD-14-HISTORICAL-CHAIN.md:18).

## 7. Correções acionáveis

1. Criar uma travessia recursiva única do schema que trate igualmente:

   - objetos `ref`;
   - objetos inline com `fields`;
   - itens de arrays;
   - objetos inline dentro de arrays, se futuros.

2. Fazer `schema_jobs()` usar essa travessia para produzir IDs canônicos pelo caminho completo, por exemplo:

   - `negative.expected_original_outcome_body.error_code.ABSENCE`;
   - `.TYPE`;
   - `.MIN_LENGTH`;
   - `.EXTRA`.

3. Fazer `occurrence_jobs()` recursar genericamente cada campo presente, em vez de depender de chamadas manuais a `nest()` por `kind`.

4. Gerar `ELEMENT_TYPE` para arrays de objetos, substituindo separadamente cada índice por valor não objeto.

5. Calcular o universo esperado por uma segunda travessia estrutural independente da lista de jobs. O atual `structural_problems()` é independente apenas para algumas estruturas selecionadas.

6. Rejeitar chaves JSON duplicadas em schema, fixtures, sintéticos e manifesto durante o parse.

7. Adicionar testes negativos estáticos específicos para:

   - remover `expected_original_outcome_body.error_code`;
   - inserir chave extra no body;
   - alterar cada subcampo inline;
   - substituir cada elemento de `setup`, `steps` e `initial_keys` por escalar/lista;
   - inserir chave JSON duplicada em cada tipo de arquivo.

8. Remover ou corrigir até nova revisão as afirmações:

   - “uma mutação por campo do schema”;
   - “para cada objeto e cada campo”;
   - `schema_rules=all_declared`;
   - cobertura independente `480/480` e `2239/2239`.

9. Manter `product_input_exhaustive=false`, mas não usar esse limite para justificar omissões de regras que estão efetivamente declaradas no schema.

## 8. Gates

Permanecem obrigatórios:

- FD07-07 **OPEN**;
- HIGH-03 **PARTIAL**;
- LOW-01 **OPEN BLOCKING DoR**;
- owner **PENDING**;
- effort **UNSTATED**;
- DoR **NOT MET**;
- O92/O93 **NOT RUN**;
- O96–O99 **NOT RUN**;
- v0.2 `chosen_verdict: null`;
- errata **PENDING HUMAN APPROVAL**;
- cadeia **PARECER_CHAIN NOT_FULLY_VERIFIED**;
- flag `forge.conversation.delta.v4` desligada;
- FDP-14, FDP-15 e baseline pendentes;
- migrations, PostgreSQL, providers, deploy e gastos não autorizados.

**BUILD-00 permanece expressamente NÃO AUTORIZADO.**

## Veredito final

**FAIL DOCUMENT-ONLY.**

A v0.12 corrige a amostragem por primeiro `kind` e índice zero, mas não fecha NEW-LOW-03 nem FD11-NEW-01. A cobertura quantitativa é autoconsistente apenas dentro de um catálogo incompleto: omite objetos inline, seus campos e ocorrências, além do tipo dos elementos de arrays de objetos. Os números `480/480` e `2239/2239` não podem ser apresentados como cobertura de todas as regras/campos do schema.