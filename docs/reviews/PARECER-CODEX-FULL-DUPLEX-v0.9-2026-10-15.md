# Parecer independente — Full-Duplex v0.9

**Checkout auditado:** `422277f82efbc001140b5857095c4840e668e270`  
**Modalidade:** auditoria documental estática, somente leitura  
**Execução:** nenhum teste, checker, script, migration, banco PostgreSQL, provider ou build executado  
**Veredito:** **FAIL DOCUMENT-ONLY**

A v0.9 corrige documentalmente as duas falhas focais da v0.8 — preservação do outcome e comparação histórica base/parent — sem regressão material observada em ACK null-pair, monotonicidade, isolamento tenant/trio ou full-duplex. Contudo, FD07-07, HIGH-03 e LOW-01 continuam bloqueantes, e foi encontrado um novo defeito de rastreabilidade na validação da cadeia de pareceres.

## Findings

| Finding | Severidade | Estado v0.9 | Resultado da auditoria |
|---|---:|---|---|
| FD07-08 — identidade/replay durável | Alta | CANDIDATE | **CLOSED documental com limite estático** |
| NEW-MEDIUM-07 — outcome original ausente | Média | CANDIDATE | **CLOSED documental com limite estático** |
| FD07-09 — manifest base/parent | Média | CANDIDATE | **CLOSED documental no escopo dos blobs de planejamento** |
| NEW-MEDIUM-08 — manifest autorreferente/sem v0.1 | Média | CANDIDATE | **CLOSED documental** |
| FD07-07 — concorrência PostgreSQL | Alta | OPEN | **OPEN** |
| HIGH-03 | Alta | PARTIAL | **PARTIAL** |
| FD07-05 — negativos e efeitos | Alta | CLOSED | **CLOSED documental; preservado** |
| FD07-06 — isolamento tenant/trio | Alta | CLOSED | **CLOSED documental; preservado** |
| LOW-01 | Baixa processual | OPEN BLOCKING DoR | **OPEN BLOCKING DoR** |
| NEW-MEDIUM-09 — cadeia de pareceres não validada | Média | Novo | **OPEN** |
| NEW-LOW-02 — schema fechado não exige presença integral | Baixa | Novo | **OPEN** |

## 1. FD07-08 e NEW-MEDIUM-07

A deficiência central da v0.8 foi corrigida.

A norma agora exige que `forge.command_commit` preserve:

- `command_digest`;
- `original_outcome_code`;
- `original_outcome_body`;
- `outcome_digest`.

Evidência: [CMP-FD-02-ACK-REPLAY.md:35](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v09-codex-independent/docs/planning/conversational-full-duplex-v0.9/CMP-FD-02-ACK-REPLAY.md:35), especialmente linhas 37–47.

O modelo estático também armazena esses quatro elementos e devolve cópia do corpo original no replay: [check_fd_fx03_ack.py:253](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v09-codex-independent/docs/planning/conversational-full-duplex-v0.9/tools/check_fd_fx03_ack.py:253) e [check_fd_fx03_ack.py:308](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v09-codex-independent/docs/planning/conversational-full-duplex-v0.9/tools/check_fd_fx03_ack.py:308).

A separação crítica está expressa corretamente:

- transporte do replay: `200`;
- outcome persistido: pode continuar `422`;
- corpo original não é substituído por `IDEMPOTENT_REPLAY`;
- digest diferente produz `409` sem substituir a linha.

Evidência normativa: [CMP-FD-02-ACK-REPLAY.md:47](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v09-codex-independent/docs/planning/conversational-full-duplex-v0.9/CMP-FD-02-ACK-REPLAY.md:47).  
Evidência de validação estática: [check_fd_fx03_ack.py:415](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v09-codex-independent/docs/planning/conversational-full-duplex-v0.9/tools/check_fd_fx03_ack.py:415).

A ordem também foi definida de forma consistente:

1. validar par null;
2. bloquear tenant errado;
3. consultar `command_commit`;
4. somente então aplicar validações mutáveis de receiver, stream e sequência.

Evidência: [CMP-FD-02-ACK-REPLAY.md:12](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v09-codex-independent/docs/planning/conversational-full-duplex-v0.9/CMP-FD-02-ACK-REPLAY.md:12) e [check_fd_fx03_ack.py:245](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v09-codex-independent/docs/planning/conversational-full-duplex-v0.9/tools/check_fd_fx03_ack.py:245).

Outro tenant recebe `404` antes do lookup e não recebe o corpo original: [check_fd_fx03_ack.py:252](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v09-codex-independent/docs/planning/conversational-full-duplex-v0.9/tools/check_fd_fx03_ack.py:252) e [check_fd_fx03_ack.py:698](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v09-codex-independent/docs/planning/conversational-full-duplex-v0.9/tools/check_fd_fx03_ack.py:698).

**Conclusão:** FD07-08 e NEW-MEDIUM-07 podem ser fechados documentalmente. Isso não equivale a provar implementação, transação real, RLS ou replay em produto. O96–O99 permanecem **NOT RUN**.

## 2. FD07-09 e NEW-MEDIUM-08

Os elementos ausentes na v0.8 foram acrescentados:

- `base_sha`;
- `parent_sha`;
- blob Git de ambos os commits;
- SHA-256 por arquivo em ambos;
- inclusão explícita do diretório histórico v0.1;
- remoção de `same_at_base_and_parent`.

Evidência: [CMP-FD-FX-04-historical-manifest.json:2](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v09-codex-independent/docs/planning/conversational-full-duplex-v0.9/fixtures/CMP-FD-FX-04-historical-manifest.json:2) e [CMP-FD-14-HISTORICAL-CHAIN.md:7](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v09-codex-independent/docs/planning/conversational-full-duplex-v0.9/CMP-FD-14-HISTORICAL-CHAIN.md:7).

O checker proposto:

- lê os dois commits com `git ls-tree`, `rev-parse` e `cat-file`;
- compara conjuntos de paths;
- recalcula SHA-256 dos blobs;
- exige igualdade dos blobs entre base e parent;
- retorna `NOT_RUN` sem `--repo`.

Evidência: [check_fd_historical_manifest.py:28](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v09-codex-independent/docs/planning/conversational-full-duplex-v0.9/tools/check_fd_historical_manifest.py:28), [check_fd_historical_manifest.py:91](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v09-codex-independent/docs/planning/conversational-full-duplex-v0.9/tools/check_fd_historical_manifest.py:91) e [check_fd_historical_manifest.py:116](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v09-codex-independent/docs/planning/conversational-full-duplex-v0.9/tools/check_fd_historical_manifest.py:116).

Sem executar esse checker, fiz apenas comparação Git read-only entre:

- base: `9fd88bb03e4cca4a1ee5126d5b595e028e2602b2`;
- parent: `aca5101d3684109175269b36c3cace2051a71c91`;
- escopo v0.1 e v0.2–v0.8.

O `git diff --name-status` resultou vazio, confirmando que os arquivos de planejamento no escopo não mudaram entre esses commits. Isso não substitui a revalidação independente de todos os SHA-256 declarados.

**Conclusão:** a falha focal FD07-09/NEW-MEDIUM-08 está documentalmente corrigida. A saída `GIT_BLOB_COMPARE MATCH READ_ONLY` registrada pelo autor em [CMP-FD-12-CONSISTENCY-REPORT.md:86](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v09-codex-independent/docs/planning/conversational-full-duplex-v0.9/CMP-FD-12-CONSISTENCY-REPORT.md:86) não foi adotada como execução desta auditoria.

## 3. Novo finding: NEW-MEDIUM-09

O manifest contém uma cadeia detalhada de pareceres v0.1–v0.8, mas o checker não valida a maior parte dessa cadeia contra os blobs reais dos pareceres.

Ele confere especificamente:

- ausência de parecer para v0.5/v0.6;
- colocação e veredito declarado de v0.8;
- inexistência dos prompts v0.6/v0.7.

Evidência: [check_fd_historical_manifest.py:51](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v09-codex-independent/docs/planning/conversational-full-duplex-v0.9/tools/check_fd_historical_manifest.py:51) e [check_fd_historical_manifest.py:101](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v09-codex-independent/docs/planning/conversational-full-duplex-v0.9/tools/check_fd_historical_manifest.py:101).

Porém, não abre e valida os pareceres v0.1–v0.4 e v0.7 para confirmar:

- `audited_sha`;
- `verdict`;
- `path`;
- presença em base e parent.

Também não valida a lista `full_duplex_prompts_present_at_parent`.

Assim, a prova dos **blobs de planejamento** é robusta, mas a cadeia de pareceres continua parcialmente declarativa.

**Gate de correção:** validar cada entrada de `parecer_chain` contra o arquivo real no commit pertinente, incluindo SHA auditado e veredito, e validar tanto a lista de prompts presentes quanto a de ausentes.

## 4. ACK isolation e regressão

Não encontrei regressão documental material:

- o par XOR-null continua antes de qualquer lookup: [CMP-FD-02-ACK-REPLAY.md:16](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v09-codex-independent/docs/planning/conversational-full-duplex-v0.9/CMP-FD-02-ACK-REPLAY.md:16);
- ambos null continuam `NO_ACK`: linha 17;
- tenant errado continua `404` opaco: linha 18;
- receiver ausente e stream não alocado permanecem separados: linhas 21–22;
- `n < 0` permanece antes da regressão relativa ao peer: linhas 24–27;
- ACK não abre microfone, não move dinheiro e não cria ledger alternativo: linhas 8 e 49–52;
- a chave tenant-composta permanece `(organization, project, session, ACK stream, receiver)` em [CMP-FD-13-CONCURRENCY-SPEC.md:9](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v09-codex-independent/docs/planning/conversational-full-duplex-v0.9/CMP-FD-13-CONCURRENCY-SPEC.md:9).

FD07-05 e FD07-06 permanecem corretamente fechados apenas no nível documental/estático.

## 5. Novo finding menor: NEW-LOW-02

O “schema fechado” rejeita chaves extras e valida diversos tipos e UUIDs, mas várias funções validam apenas campos presentes, sem exigir explicitamente o conjunto completo de propriedades antes de o restante do programa acessá-las.

Exemplo: `command_error()` percorre campos com `if name in row`, em vez de exigir todos os campos mandatórios. A fixture atual pode ser coerente, mas uma propriedade obrigatória ausente tende a causar exceção posterior, não um erro determinístico `FAIL_SCHEMA`.

Evidência: [check_fd_fx03_ack.py:750](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v09-codex-independent/docs/planning/conversational-full-duplex-v0.9/tools/check_fd_fx03_ack.py:750).

Isso não reabre FD07-08, mas limita a alegação ampla de schema fechado.

## 6. Concorrência e oráculos

Conforme solicitado:

- PostgreSQL O92: **NOT RUN**
- PostgreSQL O93: **NOT RUN**
- O96–O99: **NOT RUN**
- O84–O95: **NOT RUN**
- O01–O83: **NOT RUN**
- 91 oráculos v1.7: **NOT RUN**
- 36 CMP-O: **NOT RUN**
- migrations: **NOT RUN**
- checkers v0.9: **NOT RUN**
- BUILD-00: **NOT RUN / NÃO AUTORIZADO**

A especificação futura de O92/O93 é adequada: exige dois backends, barreira, ambas as ordens, duplicata, rollback e observação de locks para trios distintos em [CMP-FD-13-CONCURRENCY-SPEC.md:15](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v09-codex-independent/docs/planning/conversational-full-duplex-v0.9/CMP-FD-13-CONCURRENCY-SPEC.md:15). Mas nenhuma dessas evidências existe. Portanto:

- FD07-07 permanece **OPEN**;
- HIGH-03 permanece **PARTIAL**.

## 7. LOW-01

Permanece exatamente como instruído:

- owner pessoa: `PENDING`;
- effort: `UNSTATED`;
- DoR: `NOT MET`;
- estado: **OPEN BLOCKING DoR**.

Evidência: [CMP-FD-07-ORACLES.md:5](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v09-codex-independent/docs/planning/conversational-full-duplex-v0.9/CMP-FD-07-ORACLES.md:5).

## Gates finais

**Não autorizar:**

- BUILD-00;
- migration;
- execução ou integração de `forge.conversation.delta.v4`;
- promoção de `cmp.media.duplex.v1`;
- deploy/staging;
- provider, credenciais ou gasto;
- fechamento de FD07-07 ou HIGH-03;
- promoção de O92, O93 ou O96–O99 para PASS;
- PASS global enquanto LOW-01 estiver aberto.

**Pode ser aceito documentalmente:**

- FD07-08;
- NEW-MEDIUM-07;
- FD07-09 no escopo dos blobs de planejamento;
- NEW-MEDIUM-08;
- preservação de FD07-05 e FD07-06.

**Veredito final: FAIL DOCUMENT-ONLY.**

A v0.9 resolve as duas correções focais da v0.8, mas não pode alcançar PASS enquanto concorrência continuar sem execução, LOW-01 bloquear DoR e a nova lacuna de validação da cadeia de pareceres permanecer aberta.