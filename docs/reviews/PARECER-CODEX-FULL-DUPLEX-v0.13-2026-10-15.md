# Parecer independente — Full Duplex v0.13

**Checkout examinado:** `c7b08dc2a0127557293346ebd53e4ff43722683e`  
**Parent:** `cfb1c98412d4c183b406d919fabbe753ac43076b`  
**Estado Git:** detached, árvore de trabalho sem alterações observadas  
**Modalidade:** auditoria documental e estática, independente, somente leitura  
**Veredito exclusivo:** **PASS WITH CONDITIONS DOCUMENT-ONLY**  
**Estado do pacote:** permanece **CANDIDATE**, sujeito a decisão humana; não é PASS de produto.

## 1. Escopo e método

Foram examinados integralmente os 19 arquivos de `docs/planning/conversational-full-duplex-v0.13/`:

- 13 documentos Markdown;
- fixture comportamental;
- fixture sintética;
- schema;
- manifesto histórico;
- os dois checkers Python.

Também foram confrontados:

- o parecer v0.12 verdadeiro, presente em [PARECER-CODEX-FULL-DUPLEX-v0.12-2026-10-15.md](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.12-2026-10-15.md:1);
- v0.11 e os contratos anteriores pertinentes;
- FDP-16A v1.7;
- CMP v0.3;
- ata Founder/AQs;
- protocolo de governança e não regressão;
- histórico e manifesto v0.2–v0.12.

A alegação Grok/autor foi tratada somente como alegação verificável.

### Operações realizadas

Foram executados apenas comandos de leitura:

- `git status --short --branch`;
- `git log -1/-2`;
- inventário e leitura com `rg`, `Get-Content` e `findstr`;
- `git diff --name-status` entre o SHA auditado da v0.12, parent e HEAD, limitado à pasta v0.12.

O diff da pasta v0.12 foi vazio tanto entre `346cd04…` e o parent quanto entre `346cd04…` e o HEAD. Assim, a preservação dos blobs de planejamento v0.12 foi confirmada por Git no clone, dentro desse path.

### Scripts não executados

Tentei as invocações permitidas:

```text
python -B docs/planning/conversational-full-duplex-v0.13/tools/check_fd_fx03_ack.py

python -B docs/planning/conversational-full-duplex-v0.13/tools/check_fd_historical_manifest.py --repo .
```

Também tentei prefixar `PYTHONDONTWRITEBYTECODE=1`. A política read-only do ambiente rejeitou as invocações antes de iniciar o Python. Portanto:

- nenhum checker foi executado;
- `508/508` e `2443/2443` não foram reproduzidos;
- nenhum arquivo ou bytecode foi criado;
- nenhum teste, oracle, migration, PostgreSQL, provider, deploy, gasto ou BUILD-00 foi executado.

## 2. Conclusão executiva

A v0.13 corrige, por inspeção estática, as três falhas concretas que causaram a recusa da v0.12:

1. objetos inline agora entram nas travessias;
2. elementos de arrays de objetos recebem mutações escalares e listas;
3. chaves JSON duplicadas são recusadas durante o parse.

Isso está materialmente implementado, não apenas descrito:

- recursão de objetos inline: [check_fd_fx03_ack.py:1322](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/planning/conversational-full-duplex-v0.13/tools/check_fd_fx03_ack.py:1322) e [check_fd_fx03_ack.py:1328](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/planning/conversational-full-duplex-v0.13/tools/check_fd_fx03_ack.py:1328);
- ocorrências recursivas: [check_fd_fx03_ack.py:1351](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/planning/conversational-full-duplex-v0.13/tools/check_fd_fx03_ack.py:1351);
- mutação por índice de array de objeto: [check_fd_fx03_ack.py:1386](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/planning/conversational-full-duplex-v0.13/tools/check_fd_fx03_ack.py:1386) e [check_fd_fx03_ack.py:1530](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/planning/conversational-full-duplex-v0.13/tools/check_fd_fx03_ack.py:1530);
- rejeição de chave duplicada: [check_fd_fx03_ack.py:760](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/planning/conversational-full-duplex-v0.13/tools/check_fd_fx03_ack.py:760) e [check_fd_fx03_ack.py:1735](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/planning/conversational-full-duplex-v0.13/tools/check_fd_fx03_ack.py:1735).

A v0.13 também evita repetir a falsa conclusão v0.12: rotula `480/2239` como catálogo rejeitado, declara `product_input_exhaustive=false`, não reivindica `COVERAGE_TOTAL_PASS` e usa o banner `PASS_FIXTURE_ONLY`; ver [check_fd_fx03_ack.py:1889](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/planning/conversational-full-duplex-v0.13/tools/check_fd_fx03_ack.py:1889) e [check_fd_fx03_ack.py:2040](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/planning/conversational-full-duplex-v0.13/tools/check_fd_fx03_ack.py:2040).

Contudo, os números `508/508` e `2443/2443` permanecem não reproduzidos nesta auditoria e não constituem uma prova independente do universo semântico. Eles são, no máximo, uma alegação sobre o schema e as fixtures correntes.

## 3. Auditoria estrutural da cobertura

### 3.1 Universo de regras

`expected_schema_rules()` percorre todos os objetos nomeados e desce recursivamente em:

- objetos inline;
- subcampos;
- arrays;
- `items` de objeto;
- `required`;
- `allowed` mediante mutação `EXTRA`;
- UUID;
- nullable;
- `const`;
- `minLength`;
- `minItems`;
- SHA-256;
- grupos e relações `same_length`.

Evidência principal: [check_fd_fx03_ack.py:1293](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/planning/conversational-full-duplex-v0.13/tools/check_fd_fx03_ack.py:1293).

O schema não utiliza JSON Schema padrão. É uma DSL própria baseada em `objects`, `fields`, `ref`, `allowed`, `required`, `groups` e `same_length`. Portanto, neste schema concreto:

- `$ref`, `definitions`, `allOf`, `oneOf`, `anyOf`, `enum`, `additionalProperties`, `minimum`, `maximum` e `format` padrão são **não aplicáveis porque não são declarados**;
- `ref`, `allowed`, `const`, `minLength`, `minItems`, `sha256` e nulabilidade são os equivalentes efetivamente usados;
- `integer` versus `number` é representado apenas por `int`; booleanos são explicitamente excluídos do tipo inteiro em [check_fd_fx03_ack.py:827](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/planning/conversational-full-duplex-v0.13/tools/check_fd_fx03_ack.py:827).

`TYPE_WRONG` usa `True` contra `int` e `0` contra `bool`, o que é uma boa contraprova para a peculiaridade Python `bool <: int`: [check_fd_fx03_ack.py:1177](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/planning/conversational-full-duplex-v0.13/tools/check_fd_fx03_ack.py:1177).

### 3.2 Objetos inline

O body inline aparece em negativo e positivo no schema:

- [schema:317](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/planning/conversational-full-duplex-v0.13/fixtures/CMP-FD-FX-03-ack.schema.json:317);
- [schema:529](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/planning/conversational-full-duplex-v0.13/fixtures/CMP-FD-FX-03-ack.schema.json:529).

Agora são geradas regras para:

- ausência de `error_code`;
- tipo e `minLength`;
- chave extra;
- tipos de `opaque`, `retryable`, `terminal`;
- tipo de `peer_ack_high_water`.

Os anchors explícitos em [check_fd_fx03_ack.py:1667](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/planning/conversational-full-duplex-v0.13/tools/check_fd_fx03_ack.py:1667) reduzem o risco de regressão silenciosa desse ponto específico.

### 3.3 Arrays e tipagem real dos itens

Para cada ocorrência concreta de item objeto são geradas duas substituições:

- escalar `1`;
- lista `[]`.

Isso cobre `initial_keys`, `setup` e `steps`, inclusive por índice, e não apenas o primeiro elemento. A travessia usa todos os índices em [check_fd_fx03_ack.py:1387](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/planning/conversational-full-duplex-v0.13/tools/check_fd_fx03_ack.py:1387).

A contagem RAW compara comprimentos das fixtures com IDs de ocorrência para:

- `setup`;
- `steps`;
- `initial_keys`;
- bodies inline;
- campo `opaque`.

Evidência: [check_fd_fx03_ack.py:1410](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/planning/conversational-full-duplex-v0.13/tools/check_fd_fx03_ack.py:1410) e [check_fd_fx03_ack.py:1435](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/planning/conversational-full-duplex-v0.13/tools/check_fd_fx03_ack.py:1435).

### 3.4 Dedupe e paths

Os IDs de ocorrência incorporam o caminho completo e índices: [check_fd_fx03_ack.py:1195](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/planning/conversational-full-duplex-v0.13/tools/check_fd_fx03_ack.py:1195).

São recusados:

- IDs esperados duplicados;
- IDs de jobs duplicados;
- discrepância de conjuntos;
- discrepância de cardinalidade;
- job sem host;
- mutação que produz código inesperado;
- exceção durante mutação.

Isso resolve a falha concreta de dedupe/posição observada na v0.11/v0.12.

## 4. Limite oculto: independência semântica ainda é parcial

Os três passeios são separados em termos de fluxo de controle:

- `expected_schema_rules`;
- `expected_occurrences`;
- `stack_jobs`.

O terceiro não chama os dois primeiros. Isso é melhor que v0.12.

Porém, eles não são completamente independentes em termos de semântica:

- todos interpretam a mesma DSL;
- todos dependem do mesmo `TYPE_WRONG`;
- todos codificam praticamente a mesma lista de sufixos;
- os jobs são avaliados pelo mesmo validador Python cuja cobertura está sendo medida.

Logo, bugs semânticos espelhados nos passeios podem fechar `gap=0`.

### Cenários adversariais read-only

1. **Alterar um valor de `const` no schema e o valor correspondente na fixture.**  
   O número de regras e ocorrências não muda; as mutações continuam obtendo `FAIL_SCHEMA`, embora o contrato semântico tenha sido falsificado.

2. **Alterar `minItems: 6` para outro limite ainda satisfeito pela fixture.**  
   O ID `CARDINALITY` continua único e a mutação continua sendo `[]`; `508/2443` não muda.

3. **Trocar um `ref` por outro objeto estruturalmente compatível.**  
   A contagem pode permanecer idêntica, apesar de mudar o significado do campo.

4. **Alterar o conteúdo esperado e o modelo local na mesma revisão.**  
   Fixture e simulador voltam a concordar. Não há golden externo assinado para a semântica ACK v0.13.

5. **Adicionar um keyword desconhecido à DSL do schema.**  
   A integridade interna do schema não recusa genericamente todas as propriedades desconhecidas de regras. Se o keyword não for interpretado por nenhum dos passeios, ele pode ser ignorado sem deslocar counts.

Isso não reabre a falha específica de objetos inline, mas impede interpretar `508/508` como enumeração semanticamente independente de todo contrato concebível.

## 5. Contagens

| Alegação | Resultado independente |
|---|---|
| 508 regras declaradas | **Não reproduzida**; plausível por inspeção, mas autoral |
| 508 regras exercitadas | **Não reproduzida** |
| 2.443 ocorrências declaradas | **Não reproduzida** |
| 2.443 ocorrências exercitadas | **Não reproduzida** |
| Objetos inline enumerados | **Verificado estaticamente** |
| Itens de arrays de objetos por índice | **Verificado estaticamente** |
| Dedupe de IDs e paths | **Verificado estaticamente** |
| Rejeição de chave JSON duplicada | **Verificada no código; não executada** |
| Independência completa de golden inputs | **Não demonstrada** |
| Prova de produto | **Não** |
| Oráculo executado | **Nenhum** |

## 6. Findings

| Finding | Severidade | Estado v0.13 | Parecer |
|---|---:|---|---|
| FD12-NEW-01 — objetos inline omitidos | MEDIUM | CANDIDATE | **CLOSED documental/estático** |
| FD12-NEW-02 — tipo de item objeto omitido | LOW | CANDIDATE | **CLOSED documental/estático** |
| FD12-NEW-03 — chave JSON duplicada | LOW | CANDIDATE | **CLOSED estático, NOT RUN** |
| FD11-NEW-01 — catálogo incompleto | MEDIUM | CANDIDATE | **PARTIAL**: falha concreta corrigida; independência semântica não provada |
| NEW-LOW-03 — cobertura quantitativa | LOW | PARTIAL | **PARTIAL**; 508/2443 não reproduzidos |
| NEW-MEDIUM-09 — parecer v0.2 | MEDIUM | PARTIAL | **OPEN/PARTIAL**, `NOT_VERIFIED` |
| FD07-07 — concorrência real | HIGH | OPEN | **OPEN**, sem PostgreSQL |
| HIGH-03 | HIGH | PARTIAL | **PARTIAL**, depende de O92 |
| LOW-01 | BLOCKING | OPEN | **OPEN BLOCKING DoR** |
| NEW-GOV-01 — mudança semântica sem golden externo | MEDIUM | novo | **NEW / OPEN** |

Os findings historicamente CLOSED não foram reabertos sem causa. FD07-01..06, FD07-08, NEW-MEDIUM-07, NEW-MEDIUM-08, NEW-LOW-02 e FD07-09 permanecem CLOSED apenas no limite documental declarado em [CMP-FD-10:50](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/planning/conversational-full-duplex-v0.13/CMP-FD-10-FINDING-DISPOSITION.md:50).

## 7. Governança e gates

A documentação v0.13 preserva corretamente:

- nove AQs aprovadas;
- AQ-04, AQ-09 e AQ-12 deferred/undecided;
- FDP-14, FDP-15, baseline e BUILD-00 pendentes;
- `forge.conversation.delta.v4` desligada;
- parecer v0.2 `NOT_VERIFIED`;
- `chosen_verdict: null`;
- HIGH-03 `PARTIAL`;
- FD07-07 `OPEN`;
- LOW-01 `OPEN BLOCKING DoR`.

Evidência consolidada: [CMP-FD-11:7](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/planning/conversational-full-duplex-v0.13/CMP-FD-11-OPEN-QUESTIONS.md:7).

LOW-01 continua:

- **owner:** PENDING;
- **effort:** UNSTATED;
- **DoR:** NOT MET.

A própria v0.13 o declara em [CMP-FD-07:5](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/planning/conversational-full-duplex-v0.13/CMP-FD-07-ORACLES.md:5).

## 8. Oráculos e prova operacional

Todos permanecem **NOT RUN**:

- O01–O99;
- os 91 oráculos FDP-16A v1.7;
- os 36 CMP-O;
- especificamente O92 e O93 para concorrência;
- O96–O99 históricos.

A fixture de interleave é um modelo sequencial/mapa estático. Não prova:

- dois backends concorrentes;
- bloqueio real;
- ordem real de aquisição;
- rollback transacional;
- isolamento PostgreSQL;
- ausência de race sob contenção.

A v0.13 reconhece isso corretamente em [CMP-FD-13-CONCURRENCY-SPEC.md:3](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v013-codex-independent/docs/planning/conversational-full-duplex-v0.13/CMP-FD-13-CONCURRENCY-SPEC.md:3).

Nenhum `PASS_FIXTURE_ONLY`, `gap=0`, oracle spec ou fixture pode ser promovido a prova operacional.

## 9. Corrigendas precisas

Antes de qualquer promoção além de candidato documental:

1. Executar os dois checkers em ambiente read-only reproduzível e anexar stdout, exit code, versão Python e hashes dos quatro JSONs e dois scripts.
2. Publicar uma enumeração machine-readable dos 508 IDs e 2.443 occurrence IDs, não apenas totais.
3. Adicionar validação fechada da própria DSL do schema, recusando keywords desconhecidos.
4. Introduzir um catálogo/golden independente que fixe:
   - path;
   - categoria da regra;
   - constraint;
   - valor esperado;
   - digest do schema e fixtures.
5. Adicionar contraprovas que alterem valores sem mudar cardinalidade:
   - `const`;
   - `minItems`;
   - `minLength`;
   - destino de `ref`;
   - required/optional compensados;
   - conteúdo esperado e simulador simultaneamente.
6. Manter o rótulo `PASS_FIXTURE_ONLY`; não publicar `508/508` como cobertura total do produto.
7. Executar O92/O93 apenas após autorização expressa e ambiente apropriado.
8. Resolver LOW-01 com owner nominal, effort e ato Founder que torne o DoR atendido.
9. Manter BUILD-00 bloqueado até FDP-14/FDP-15, baseline e gates humanos.

## 10. Risco residual

O risco documental da regressão v0.12 caiu materialmente: os caminhos antes omitidos agora estão presentes.

O risco residual principal é confundir:

```text
fixture + schema + checker autoconsistentes
```

com:

```text
contrato semanticamente completo + implementação real correta
```

A primeira proposição é plausível, mas não foi executada nesta auditoria. A segunda permanece totalmente não demonstrada.

# Veredito final

**PASS WITH CONDITIONS DOCUMENT-ONLY.**

A v0.13 corrige estaticamente as causas específicas da recusa v0.12 — objetos inline, itens de arrays de objetos e chaves JSON duplicadas — e documenta honestamente os limites.

Este veredito:

- não confirma numericamente `508/508` ou `2443/2443`;
- não é PASS de produto;
- não é PASS operacional;
- não fecha FD07-07, HIGH-03, LOW-01, NEW-MEDIUM-09 nem o novo limite de independência semântica;
- não autoriza migrations, PostgreSQL, provider, deploy, gastos ou BUILD-00;
- não autoriza ligar `forge.conversation.delta.v4`.

**Gate:** v0.13 permanece **CANDIDATE até decisão humana**, reprodução independente dos checkers e satisfação dos gates de governança e concorrência.