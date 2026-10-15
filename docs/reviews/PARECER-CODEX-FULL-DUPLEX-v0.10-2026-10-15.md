# Parecer independente — Full-Duplex v0.10

**Checkout auditado:** `a5d7e8fc85cb5b5f0605937b43075ce1a0c19e08`  
**Modalidade:** auditoria documental estática, independente e somente leitura  
**Execução:** nenhum teste, script, checker, migration, build, banco, provider ou deploy executado  
**Veredito:** **FAIL DOCUMENT-ONLY**  
**BUILD-00:** **NÃO AUTORIZADO**

## 1. Conclusão executiva

A v0.10 melhora substancialmente a rastreabilidade histórica e corrige o defeito original de campos obrigatórios ausentes. Contudo:

- NEW-MEDIUM-09 não pode ser integralmente fechado porque o blob do parecer v0.2 contém dois vereditos materialmente distintos. A classificação `NOT_VERIFIED` é correta.
- NEW-LOW-02 está apenas parcialmente corrigido: campos obrigatórios ausentes produzem `FAIL_SCHEMA`, mas ainda existem tipos e estruturas que atravessam a validação de schema e só são avaliados durante o processamento.
- FD07-07 permanece **OPEN**.
- HIGH-03 permanece **PARTIAL**.
- LOW-01 permanece **OPEN BLOCKING DoR**.
- PostgreSQL O92/O93 permanece **NOT RUN**.
- O96–O99 permanece **NOT RUN**.

Não identifiquei regressão material em FD07-01..06, FD07-08, NEW-MEDIUM-07/08 ou FD07-09.

## 2. Matriz de findings

| Finding | Resultado independente v0.10 | Estado |
|---|---|---|
| FD07-01..04 | Preservados documentalmente | CLOSED documental |
| FD07-05 | Negativos, `n < 0` e zero movimento preservados | CLOSED documental |
| FD07-06 | Isolamento tenant/trio preservado no modelo estático | CLOSED documental |
| FD07-07 | Nenhuma concorrência PostgreSQL executada | **OPEN** |
| FD07-08 | Replay/outcome original preservado | CLOSED documental, limite estático |
| FD07-09 | Base/parent e conjunto histórico preservados | CLOSED no escopo dos blobs de planejamento |
| NEW-MEDIUM-07 | Outcome original 422 separado do transporte 200 | CLOSED documental |
| NEW-MEDIUM-08 | v0.1 incluída; manifest não é autorreferente | CLOSED documental |
| NEW-MEDIUM-09 | Cadeia efetivamente consulta blobs; v0.2 continua ambíguo | **PARTIAL / NOT FULLY VERIFIED** |
| NEW-LOW-02 | Required/deletion corrigidos; validação integral de tipos ainda incompleta | **PARTIAL / OPEN** |
| HIGH-03 | Falta evidência real de O92 | **PARTIAL** |
| LOW-01 | Pessoa PENDING, effort UNSTATED, DoR NOT MET | **OPEN BLOCKING DoR** |
| NEW-LOW-03 | Schema declara proteção mais ampla que a implementada para tipos/estruturas compostas | **NEW / OPEN** |

## 3. NEW-MEDIUM-09 — cadeia histórica

### 3.1 SHAs e escopo

O checkout local está diretamente destacado no SHA solicitado. A cadeia v0.10 usa:

- base auditada v0.9: `422277f82efbc001140b5857095c4840e668e270`;
- parent com parecer v0.9: `311e2cf76db6fb2294745b9415f1ae829c883fa7`.

Evidência: [CMP-FD-14-HISTORICAL-CHAIN.md:7](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v10-codex-independent/docs/planning/conversational-full-duplex-v0.10/CMP-FD-14-HISTORICAL-CHAIN.md:7).

A comparação independente dos commits mostra que o parent acrescentou somente:

- `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.9-2026-10-15.md`;
- `docs/reviews/PROMPT-GROK-FULL-DUPLEX-v0.10-CORRECTIVE.md`.

Portanto, não houve alteração nos paths de planejamento entre base e parent. O manifest enumera 122 paths e inclui v0.1, v0.2–v0.9. Como nenhum checker foi executado nesta auditoria, a saída autoral `REHASHED 122` não é adotada como execução independente.

### 3.2 Pareceres reais

A leitura dos blobs confirma:

| Versão | Path | SHA auditado | Veredito |
|---|---|---|---|
| v0.1 | `PARECER-CODEX-FULL-DUPLEX-v0.1-2026-10-13.md` | `97ee817…` | `FAIL — DOCUMENT-ONLY`, VERIFIED |
| v0.2 | `PARECER-CODEX-FULL-DUPLEX-v0.2-2026-10-13.md` | `18aa352…` | **NOT_VERIFIED** |
| v0.3 | `PARECER-CODEX-FULL-DUPLEX-v0.3-2026-10-14.md` | `2fe0b0b…` | `FAIL DOCUMENT-ONLY`, VERIFIED |
| v0.4 | `PARECER-CODEX-FULL-DUPLEX-v0.4-2026-10-14.md` | `90fc21c…` | `FAIL DOCUMENT-ONLY`, VERIFIED |
| v0.5 | nenhum parecer | — | ABSENT_LEGITIMATE |
| v0.6 | nenhum parecer | — | ABSENT_LEGITIMATE |
| v0.7 | `PARECER-CODEX-FULL-DUPLEX-v0.7-2026-10-15.md` | `1a71dfa…` | `FAIL DOCUMENT-ONLY`, VERIFIED |
| v0.8 | `PARECER-CODEX-FULL-DUPLEX-v0.8-2026-10-15.md` | `9fd88bb…` | `FAIL DOCUMENT-ONLY`, VERIFIED |
| v0.9 | `PARECER-CODEX-FULL-DUPLEX-v0.9-2026-10-15.md` | `422277f…` | `FAIL DOCUMENT-ONLY`, VERIFIED |

Os valores declarados aparecem no manifest em [CMP-FD-FX-04-historical-manifest.json:984](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v10-codex-independent/docs/planning/conversational-full-duplex-v0.10/fixtures/CMP-FD-FX-04-historical-manifest.json:984).

### 3.3 Caso v0.2

O parecer v0.2 contém:

- cabeçalho: `FAIL`;
- fecho: `FAIL — DOCUMENT-ONLY`;
- cabeçalho/veredito duplicado no conteúdo.

Logo, não existe uma única string de veredito verificável. A decisão de não promover nenhum dos textos e registrar `NOT_VERIFIED` é correta: [CMP-FD-14-HISTORICAL-CHAIN.md:17](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v10-codex-independent/docs/planning/conversational-full-duplex-v0.10/CMP-FD-14-HISTORICAL-CHAIN.md:17).

Consequência: a cadeia pode ser considerada estruturalmente verificada, mas não integralmente verificada quanto ao veredito. NEW-MEDIUM-09 fica **PARTIAL**, com `PARECER_CHAIN NOT_FULLY_VERIFIED`.

### 3.4 Ausências legítimas e prompts

A ausência dos pareceres v0.5/v0.6 é legítima. O checker pesquisa por prefixo nos dois commits, em vez de depender apenas de dois nomes exatos: [check_fd_historical_manifest.py:178](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v10-codex-independent/docs/planning/conversational-full-duplex-v0.10/tools/check_fd_historical_manifest.py:178).

Prompts presentes no parent:

- v0.2, v0.3, v0.4, v0.5, v0.8, v0.9 e v0.10.

Prompts ausentes:

- v0.6;
- v0.7.

Evidência: [CMP-FD-FX-04-historical-manifest.json:1135](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v10-codex-independent/docs/planning/conversational-full-duplex-v0.10/fixtures/CMP-FD-FX-04-historical-manifest.json:1135).

O checker compara o conjunto completo de prompts do parent e verifica os ausentes nos dois commits: [check_fd_historical_manifest.py:161](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v10-codex-independent/docs/planning/conversational-full-duplex-v0.10/tools/check_fd_historical_manifest.py:161).

### 3.5 Validade do checker histórico

Foram corrigidos os defeitos principais da v0.9:

- path/version validado por expressão regular;
- presença por commit verificada com `cat-file`;
- SHA, rótulo e veredito extraídos do blob;
- comparação de base/parent quando o parecer existe em ambos;
- troca de SHA, veredito, path, omissão e invenção cobertas por mutações negativas.

Evidência: [check_fd_historical_manifest.py:48](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v10-codex-independent/docs/planning/conversational-full-duplex-v0.10/tools/check_fd_historical_manifest.py:48), [check_fd_historical_manifest.py:210](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v10-codex-independent/docs/planning/conversational-full-duplex-v0.10/tools/check_fd_historical_manifest.py:210) e [check_fd_historical_manifest.py:244](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v10-codex-independent/docs/planning/conversational-full-duplex-v0.10/tools/check_fd_historical_manifest.py:244).

Limite menor: o campo `bytes` de cada entrada do manifest não é comparado ao tamanho real do blob. Isso não invalida os IDs/hashes, mas o campo permanece metadata não verificada.

## 4. NEW-LOW-02 e NEW-LOW-03 — schema

### 4.1 Correção confirmada

A v0.10 agora possui lista externa de `required` e `allowed`: [CMP-FD-FX-03-ack.schema.json:2](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v10-codex-independent/docs/planning/conversational-full-duplex-v0.10/fixtures/CMP-FD-FX-03-ack.schema.json:2).

O fluxo rejeita campos obrigatórios ausentes antes da indexação:

- documento e canal: [check_fd_fx03_ack.py:782](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v10-codex-independent/docs/planning/conversational-full-duplex-v0.10/tools/check_fd_fx03_ack.py:782);
- initial keys: [check_fd_fx03_ack.py:824](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v10-codex-independent/docs/planning/conversational-full-duplex-v0.10/tools/check_fd_fx03_ack.py:824);
- comandos/casos: [check_fd_fx03_ack.py:860](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v10-codex-independent/docs/planning/conversational-full-duplex-v0.10/tools/check_fd_fx03_ack.py:860).

A rotina de mutação remove os campos obrigatórios do documento, canal, initial key, cada kind, step, setup e attempt, exigindo `FAIL_SCHEMA`; exceções viram `FAIL_SCHEMA_EXCEPTION`: [check_fd_fx03_ack.py:972](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v10-codex-independent/docs/planning/conversational-full-duplex-v0.10/tools/check_fd_fx03_ack.py:972).

Assim, o defeito específico “missing obrigatório causa KeyError” foi corrigido.

### 4.2 Schema bypass restante

A alegação mais ampla — “tipos errados são rejeitados antes do processamento” — ainda não é integralmente verdadeira.

Exemplos:

- `rollback_model`: o schema declara obrigatórios `executed_database`, `oracle_status`, `opens_mic`, `zero_money`, `zero_new_effect_after_rollback` e `command_stored_after_rollback`, mas `case_schema_error()` valida apenas o objeto `attempt`; não valida os tipos dos demais campos: [check_fd_fx03_ack.py:921](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v10-codex-independent/docs/planning/conversational-full-duplex-v0.10/tools/check_fd_fx03_ack.py:921).
- `interleave`: os tipos de `concurrency` e `not_a_postgresql_test` não são validados no estágio de schema.
- `sequential_replay`: `commit_order` e `expected_steps` são exigidos como listas, mas os tipos de seus elementos e cardinalidade correlata não são validados: [check_fd_fx03_ack.py:908](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v10-codex-independent/docs/planning/conversational-full-duplex-v0.10/tools/check_fd_fx03_ack.py:908).
- `replay_receiver_removed` e `replay_cross_tenant`: não há invariantes de cardinalidade explícitos para `setup`; uma lista vazia atravessa o loop de validação estrutural.

Isso constitui **NEW-LOW-03** e mantém NEW-LOW-02 apenas parcialmente resolvido. A correção de presença é válida; a garantia de schema fechado completo ainda não.

## 5. Preservação dos findings anteriores

Não encontrei regressão documental material:

- replay do outcome original `422` com transporte `200`;
- digest distinto resulta em conflito sem substituir a linha;
- tenant errado recebe `404` antes do lookup;
- par ACK null continua validado antes de consultas;
- ambos null continuam `NO_ACK`;
- `n < 0` continua no estágio `negative`;
- high-water não diminui no modelo;
- ACK não abre microfone;
- erros não produzem movimento financeiro;
- não existe ledger alternativo.

Evidência resumida: [CMP-FD-02-ACK-REPLAY.md:6](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v10-codex-independent/docs/planning/conversational-full-duplex-v0.10/CMP-FD-02-ACK-REPLAY.md:6).

Portanto, permanecem suportados:

- FD07-01..06;
- FD07-08;
- NEW-MEDIUM-07;
- NEW-MEDIUM-08;
- FD07-09, limitado aos blobs de planejamento.

## 6. Concorrência, oráculos e DoR

A especificação futura preserva:

- chave composta por organization, project, session, ACK stream e receiver;
- `INSERT ... ON CONFLICT DO NOTHING`;
- `SELECT ... FOR UPDATE`;
- update somente quando `n > peer_ack_high_water`;
- dois backends;
- barreira real;
- ambas as ordens;
- duplicata;
- rollback `40001`;
- observação de locks para trios distintos.

Evidência: [CMP-FD-13-CONCURRENCY-SPEC.md:5](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v10-codex-independent/docs/planning/conversational-full-duplex-v0.10/CMP-FD-13-CONCURRENCY-SPEC.md:5).

Mas nada disso foi executado:

- O92: **NOT RUN**
- O93: **NOT RUN**
- O96–O99: **NOT RUN**
- O01–O91 e O94–O95: **NOT RUN**
- 91 oráculos v1.7: **NOT RUN**
- 36 CMP-O: **NOT RUN**

Logo:

- FD07-07: **OPEN**;
- HIGH-03: **PARTIAL**.

LOW-01 permanece:

- owner pessoa: `PENDING`;
- effort: `UNSTATED`;
- DoR: `NOT MET`;
- estado: **OPEN BLOCKING DoR**.

Evidência: [CMP-FD-07-ORACLES.md:5](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v10-codex-independent/docs/planning/conversational-full-duplex-v0.10/CMP-FD-07-ORACLES.md:5).

## 7. Ações corretivas precisas

1. Manter v0.2 como `NOT_VERIFIED`; não escolher arbitrariamente entre `FAIL` e `FAIL — DOCUMENT-ONLY`.
2. Se for necessário fechar NEW-MEDIUM-09 integralmente, corrigir o parecer histórico v0.2 somente por procedimento de governança que preserve o original e acrescente uma resolução explícita, nunca por edição silenciosa.
3. Validar o campo `bytes` do manifest contra o comprimento do blob ou removê-lo.
4. Expandir `case_schema_error()` para validar todos os tipos declarados em `rollback_model`, `interleave`, `sequential_replay`, `replay_receiver_removed` e `replay_cross_tenant`.
5. Exigir cardinalidade mínima e tipos de elementos para `setup`, `steps`, `commit_order` e `expected_steps`.
6. Acrescentar mutações de tipo para cada campo de cada kind, além das mutações de remoção.
7. Manter falhas de schema determinísticas como `FAIL_SCHEMA`, `FAIL_TYPE`, `FAIL_UUID` ou `FAIL_EXTRA_KEY`, sem depender de validações semânticas posteriores.
8. Não fechar FD07-07/HIGH-03 antes de PostgreSQL real autorizado com O92/O93.
9. Resolver LOW-01 por ato humano: pessoa responsável, effort e DoR satisfeito.

## 8. Gates finais

Não autorizar:

- BUILD-00;
- migration;
- PostgreSQL;
- integração ou ativação de `forge.conversation.delta.v4`;
- promoção de `cmp.media.duplex.v1`;
- provider, credenciais ou gasto;
- deploy ou staging;
- fechamento de FD07-07;
- fechamento de HIGH-03;
- promoção de O92, O93 ou O96–O99 para PASS;
- PASS global enquanto LOW-01 estiver aberto;
- fechamento integral de NEW-MEDIUM-09 enquanto v0.2 estiver `NOT_VERIFIED`;
- fechamento integral de NEW-LOW-02 enquanto restarem bypasses de tipo/estrutura.

**Veredito final: FAIL DOCUMENT-ONLY.**

A v0.10 corrige a leitura da cadeia histórica e a falha determinística de campos ausentes, mas a cadeia continua necessariamente incompleta pelo conflito real do parecer v0.2, e o schema ainda não rejeita todos os tipos/estruturas inválidos antes do processamento. BUILD-00 permanece expressamente não autorizado.