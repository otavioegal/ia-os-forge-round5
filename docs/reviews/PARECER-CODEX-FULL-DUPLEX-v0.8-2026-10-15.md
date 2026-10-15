# PARECER INDEPENDENTE CODEX — CONVERSATIONAL FULL-DUPLEX v0.8

**Data:** 15 de outubro de 2026  
**Checkout submetido:** `9fd88bb03e4cca4a1ee5126d5b595e028e2602b2`  
**Modalidade:** auditoria documental independente, somente leitura  
**Veredito:** **FAIL DOCUMENT-ONLY**

Nenhum arquivo foi criado ou modificado. Checker, fixtures, testes, parser, PostgreSQL, migrations, provider, deploy e oráculos não foram executados. A saída `PASS_FIXTURE_ONLY` registrada pelo autor não foi adotada como evidência independente.

## 1. Conclusão executiva

A v0.8 corrige documentalmente uma parte substancial das falhas da v0.7:

- FD07-05: existe `n=-1`, os efeitos negativos são efetivamente lidos e os campos são rejeitados quando divergentes.
- FD07-06: o modelo agora usa chave tenant-composta com sessão, stream ACK e receiver; há casos de tenant errado, receiver ausente, stream não alocado e interferência cruzada.
- FD07-07: a SQL explicita `ON CONFLICT DO NOTHING`, `SELECT FOR UPDATE`, guarda crescente e as duas ordens futuras.
- FD07-08: aparecem `command_id`, `event_id`, replay, dedupe e rollback modelado.
- FD07-09: a narrativa deixa de inventar pareceres v0.5/v0.6 e contém um manifest com 91 entradas.

O pacote ainda não alcança PASS documental por três razões materiais:

1. FD07-07 continua sem evidência concorrente: O92/O93 são apenas especificações `NOT RUN`.
2. FD07-08 não implementa no modelo o contrato de replay que diz herdar: `forge.command_commit` é reduzido a `command_id → digest`, sem `original_outcome_code`, `original_outcome_body` ou `outcome_digest`.
3. FD07-09 não prova a comparação “base versus parent”: o manifest contém booleans autorreferentes, não identifica/valida `parent_sha`, não abre os dois commits e omite o pacote histórico v0.1 da lista de arquivos.

LOW-01 continua bloqueando DoR. HIGH-03 permanece PARTIAL. Logo, BUILD-00 permanece não autorizado.

## 2. Findings

| Finding | Severidade | Estado | Resultado |
|---|---:|---|---|
| FD07-01 — ambos null → `NO_ACK` | Alta | **CLOSED documental** | Preservado; decisão ocorre antes de unallocated |
| FD07-02 — XOR null → mismatch | Alta | **CLOSED documental** | Preservadas as duas direções |
| FD07-03 — precedência/monotonicidade local | Alta | **CLOSED documental** | Sem regressão documental observada |
| FD07-04 — limite do checker | Média | **CLOSED documental** | O checker admite ser somente modelo de fixture |
| FD07-05 — negativos e efeitos | Alta | **CLOSED documental com limite estático** | Correção focal satisfeita |
| FD07-06 — isolamento tenant/trio | Alta | **CLOSED documental com limite estático** | Mapa e interferência cruzada presentes; lock real não demonstrado |
| FD07-07 — concorrência PostgreSQL | Alta | **OPEN** | SQL especificada, O92/O93 `NOT RUN` |
| FD07-08 — replay/identidade durável | Alta | **PARTIAL** | Identidades existem, mas outcome original não é persistido/modelado |
| FD07-09 — cadeia histórica | Média | **PARTIAL** | Cadeia textual corrigida; prova criptográfica base/parent incompleta |
| HIGH-03 | Alta | **PARTIAL** | O71–O95 relevantes continuam `NOT RUN` |
| NEW-MEDIUM-06 | Média | **CLOSED DOCUMENTAL** | Opção B preservada; migration `NOT RUN` |
| LOW-01 | Baixa processual | **OPEN BLOCKING DoR** | Pessoa PENDING; effort UNSTATED |
| NEW-MEDIUM-07 — replay sem outcome original | Média | **NEW / OPEN** | Modelo contradiz o contrato `forge.command_commit` referenciado |
| NEW-MEDIUM-08 — manifest não prova base/parent e omite v0.1 | Média | **NEW / OPEN** | Integridade histórica alegada é mais ampla que a verificação implementada |

## 3. FD07-05 — CLOSED documental

A norma contém a sequência negativa no estágio anterior ao peer em [CMP-FD-02-ACK-ISOLATION.md:32](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v08-codex-independent/docs/planning/conversational-full-duplex-v0.8/CMP-FD-02-ACK-ISOLATION.md:32). A fixture possui `ack_of_sequence: -1` em [CMP-FD-FX-03-ack.json:542](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v08-codex-independent/docs/planning/conversational-full-duplex-v0.8/fixtures/CMP-FD-FX-03-ack.json:542) e exige `ACK_REGRESSION`/estágio `negative` em `:560-561`.

O checker:

- exige o caso no conjunto `REQUIRED`: [check_fd_fx03_ack.py:43](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v08-codex-independent/docs/planning/conversational-full-duplex-v0.8/tools/check_fd_fx03_ack.py:43);
- contém todos os IDs negativos em `NEGATIVE_IDS`: `:67-84`;
- classifica `n < 0` antes da comparação com o peer: `:168-172`;
- exige campos e todos os contadores: `:329-340`;
- confere código, high-water, escrita, dinheiro, microfone, opacidade, efeitos, estágio e contadores: `:302-326`;
- aplica mutações aos principais campos declarados e contadores: `:404-438`.

Ressalva: o harness interno de mutação não inclui `peer_ack_high_water_before` nem `expected_stage` em seu dicionário, embora ambos sejam validados pelo caminho normal em `check_row`. Isso não constitui bypass da fixture atual, mas a alegação “mutação de qualquer campo” seria mais precisa se esses dois campos também fossem mutados automaticamente.

**Correção recomendada:** incluir no harness mutações explícitas de `peer_ack_high_water_before` → `FAIL_BEFORE` e `expected_stage` → `FAIL_STAGE`.

## 4. FD07-06 — CLOSED documental, não operacional

A chave é:

`(organization_id, project_id, session_id, ack_stream_id, receiver_participant_id)`

Evidência normativa: [CMP-FD-02-ACK-ISOLATION.md:12](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v08-codex-independent/docs/planning/conversational-full-duplex-v0.8/CMP-FD-02-ACK-ISOLATION.md:12).

Evidência estática:

- `key_of()` inclui tenant, sessão, stream ACK e receiver: [check_fd_fx03_ack.py:104](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v08-codex-independent/docs/planning/conversational-full-duplex-v0.8/tools/check_fd_fx03_ack.py:104);
- tenant errado retorna `NOT_FOUND`: `:155-160`;
- receiver fora da sessão retorna `NOT_FOUND`: `:161-163`;
- stream não alocado retorna `ACK_STREAM_UNALLOCATED`: `:164-166`;
- alteração/criação de chave estrangeira é detectada: `:138-146`;
- o caso intercalado verifica cada passo e injeta alteração estrangeira para confirmar a detecção: `:442-469`;
- a fixture contém tenant errado em [CMP-FD-FX-03-ack.json:692](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v08-codex-independent/docs/planning/conversational-full-duplex-v0.8/fixtures/CMP-FD-FX-03-ack.json:692), receiver errado em `:728` e stream não alocado em `:347`.

O par null continua antes dessas verificações, em [check_fd_fx03_ack.py:149](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v08-codex-independent/docs/planning/conversational-full-duplex-v0.8/tools/check_fd_fx03_ack.py:149).

Isso fecha a deficiência documental específica da v0.7. Não prova RLS, lock, índice físico ou comportamento PostgreSQL.

## 5. FD07-07 — OPEN

A especificação futura contém:

- unique tenant-composta: [CMP-FD-13-CONCURRENCY-SPEC.md:9](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v08-codex-independent/docs/planning/conversational-full-duplex-v0.8/CMP-FD-13-CONCURRENCY-SPEC.md:9);
- `INSERT ... ON CONFLICT (...) DO NOTHING`: `:13-21`;
- `SELECT ... FOR UPDATE`: `:26`;
- `UPDATE` com chave completa, CAS sobre `current` e guarda `:n > peer_ack_high_water`: `:28-38`;
- ordens 1→2, 2→1 e duplicata: `:47-53`;
- corrida de trios distintos: `:55`;
- declaração inequívoca de que os casos `FX03-RACE-*` são sequenciais: `:57`.

Entretanto, nenhuma barreira, dois backends ou `pg_locks` foram observados. O próprio documento marca tudo como `NOT RUN` em `:43-55`.

**Correção precisa:** em fase autorizada, executar O92 com dois backends e barreira real para ambas as ordens; persistir evidência externa ao pacote. Executar O93 com trios distintos e observação de locks/timeout. Até isso ocorrer, FD07-07 e HIGH-03 não podem ser fechados.

## 6. FD07-08 — PARTIAL e NEW-MEDIUM-07

A parte positiva:

- o documento adota `forge.command_commit` e `event_id` de `forge.event.v1`: [CMP-FD-02-ACK-ISOLATION.md:68](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v08-codex-independent/docs/planning/conversational-full-duplex-v0.8/CMP-FD-02-ACK-ISOLATION.md:68);
- não cria ledger novo;
- especifica transação única e crash pré-commit: `:70`;
- distingue replay, command reutilizado, command distinto e dedupe de evento: `:72`;
- o checker diferencia digest igual/diferente: [check_fd_fx03_ack.py:218](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v08-codex-independent/docs/planning/conversational-full-duplex-v0.8/tools/check_fd_fx03_ack.py:218);
- deduplica `event_id`: `:233-244`;
- o rollback é honestamente marcado como modelo e `NOT_RUN`: `:518-548` e [CMP-FD-FX-03-ack.json:944](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v08-codex-independent/docs/planning/conversational-full-duplex-v0.8/fixtures/CMP-FD-FX-03-ack.json:944).

A lacuna material é que o modelo guarda apenas:

```text
commits[(organization_id, project_id, command_id)] = digest
```

Evidência: [check_fd_fx03_ack.py:218](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v08-codex-independent/docs/planning/conversational-full-duplex-v0.8/tools/check_fd_fx03_ack.py:218) e `:254-256`.

Mas a v0.5, que a v0.8 afirma reutilizar, exige que `forge.command_commit` guarde:

- `original_outcome_code`;
- `original_outcome_body`;
- `outcome_digest`.

Evidência: [CMP-FD-01-LEDGER-SETTLEMENT.md:107](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v08-codex-independent/docs/planning/conversational-full-duplex-v0.5/CMP-FD-01-LEDGER-SETTLEMENT.md:107), especialmente `:111-130`.

Consequentemente, o checker não pode provar a afirmação “outcome original”: ele só fabrica `IDEMPOTENT_REPLAY`. Também não demonstra replay de outcome original não-200/409 previamente cometido.

**Correção precisa:** modelar o valor de `commits` com `command_digest`, `original_outcome_code`, `original_outcome_body` e `outcome_digest`; fazer o replay devolver e conferir esses campos. Adicionar fixture em que o outcome original não seja confundido com o status HTTP 200 do replay. Definir explicitamente em que ponto o lookup ocorre relativamente a validações mutáveis de sessão/receiver.

## 7. FD07-09 — PARTIAL e NEW-MEDIUM-08

A correção textual sobre pareceres é válida:

- v0.5/v0.6 são declarados candidatos sem parecer independente: [CMP-FD-14-HISTORICAL-CHAIN.md:5](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v08-codex-independent/docs/planning/conversational-full-duplex-v0.8/CMP-FD-14-HISTORICAL-CHAIN.md:5);
- a ausência é registrada em `:17-18`;
- o parecer v0.7 e seu SHA são registrados em `:19`;
- a busca no clone realmente não localiza pareceres v0.5/v0.6.

O manifest possui 91 linhas de arquivo e cada uma declara hash SHA-256 de 64 caracteres e `same_at_base_and_parent=true`. Porém:

1. O checker apenas compara esses hashes ao filesystem apontado por `--root`: [check_fd_historical_manifest.py:83](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v08-codex-independent/docs/planning/conversational-full-duplex-v0.8/tools/check_fd_historical_manifest.py:83).
2. Ele não abre o commit base e o parent.
3. Não existe campo `parent_sha` validado.
4. `same_at_base_and_parent` é somente exigido como boolean `true`: `:60-61`.
5. O texto identifica o parent `4caabeca6a183934f0f4c68bc182877dee4ffdf6`, mas o checker nunca o usa: [CMP-FD-14-HISTORICAL-CHAIN.md:21](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v08-codex-independent/docs/planning/conversational-full-duplex-v0.8/CMP-FD-14-HISTORICAL-CHAIN.md:21).
6. As 91 entradas começam em `conversational-full-duplex-v0.2`; o pacote histórico v0.1, armazenado sob `docs/planning/conversational-full-duplex/`, não é incluído. Portanto, a frase “v0.1 até v0.7” é inexata.

Além disso, por ordem expressa desta auditoria, os SHA-256 não foram recalculados. A saída alegada `REHASHED 91` em [CMP-FD-12-CONSISTENCY-REPORT.md:75](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v08-codex-independent/docs/planning/conversational-full-duplex-v0.8/CMP-FD-12-CONSISTENCY-REPORT.md:75) não é evidência independente.

**Correção precisa:**

- incluir `base_sha` e `parent_sha`;
- gerar/validar dois hashes por path, derivados dos blobs de cada commit, não de booleans declarativos;
- falhar se os conjuntos de paths dos commits diferirem;
- incluir explicitamente o pacote v0.1 ou corrigir a alegação de cobertura para v0.2–v0.7;
- manter pareceres fora do conjunto de “pacotes de planejamento” ou documentar separadamente seu momento de incorporação.

## 8. Schema, bypasses e invariantes

A fixture não possui JSON Schema independente. O checker verifica apenas o valor da propriedade `schema` em [check_fd_fx03_ack.py:556](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v08-codex-independent/docs/planning/conversational-full-duplex-v0.8/tools/check_fd_fx03_ack.py:556) e depois acessa campos diretamente.

Isso significa:

- vários tipos/formato UUID não são validados;
- chaves extras não são recusadas;
- relações estruturais entre `participants`, `allocated_by_session`, `initial_keys` e casos são verificadas apenas parcialmente;
- fixture e checker continuam sendo uma única autoridade acoplada, não um oráculo independente.

Não encontrei bypass que permita diminuir o high-water no modelo atual: aceite exige `current < n <= emitted` em `:176-185`, e alteração estrangeira é detectada. O principal risco não é diminuição silenciosa, mas superestimar a força probatória do modelo.

## 9. Estados preservados

- **FD07-01..FD07-04:** CLOSED documental.
- **HIGH-03:** PARTIAL.
- **NEW-MEDIUM-06:** CLOSED DOCUMENTAL; migration `NOT RUN`.
- **LOW-01:** OPEN BLOCKING DoR — pessoa PENDING e effort UNSTATED em [CMP-FD-07-ORACLES.md:9](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v08-codex-independent/docs/planning/conversational-full-duplex-v0.8/CMP-FD-07-ORACLES.md:9).
- Nenhuma regressão documental objetiva de HIGH-01/02, NEW-HIGH-01/02, NEW-MEDIUM-01/02/04 ou MEDIUM-01..05 foi identificada.
- NEW-HIGH-03/04 e NEW-MEDIUM-03/05 permanecem candidatos, não revalidados nesta revisão focal.

Os arquivos de prompt corretivo v0.6 e v0.7 não existem no checkout. Existem os prompts v0.5 e v0.8; os pacotes v0.6/v0.7 e o parecer v0.7 foram tratados como fontes. A ausência não altera por si só o protocolo, mas deve ser registrada para não alegar uma cadeia de prompts inexistente.

## 10. Oráculos e gates

Estado nesta auditoria:

- O84–O95: **NOT RUN**
- O71–O83: **NOT RUN**
- O01–O70: **NOT RUN**
- 91 oráculos v1.7: **NOT RUN**
- 36 CMP-O: **NOT RUN**
- checker ACK v0.8: **NOT RUN**
- checker do manifest: **NOT RUN**
- PostgreSQL/O92/O93: **NOT RUN**
- migration: **NOT RUN**
- provider/API: **NOT RUN**
- deploy/staging: **NOT RUN**
- BUILD-00: **NOT RUN / NÃO AUTORIZADO**

As decisões de Founder continuam coerentes:

- full-duplex natural é obrigatório e half-duplex não o substitui: [ADR-FDR-AQ07:13](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v08-codex-independent/docs/governance/ADR-FDR-AQ07-FULL-DUPLEX-MVP-2026-10-13.md:13);
- nove AQs estão aprovadas e AQ-04/09/12 diferidas: [ATA-FOUNDER:10](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v08-codex-independent/docs/governance/ATA-FOUNDER-AQS-CONVERSATIONAL-2026-10-13.md:10);
- a ata não autoriza BUILD-00, contratação, deploy, testes ou gastos: `:29`;
- FDP-14/FDP-15 seguem pendentes e BUILD-00 não autorizado: [FOUNDER-GATE:26](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v08-codex-independent/docs/governance/FOUNDER-GATE-FDP14-FDP15-BASELINE-v1.7.md:26).

## 11. Gate final

**Não autorizar:**

- BUILD-00;
- migration;
- promoção de `cmp.media.duplex.v1`;
- integração de `forge.conversation.delta.v4`;
- deploy ou staging;
- provider, credenciais ou gasto;
- fechamento de HIGH-03;
- promoção de O84–O95 para PASS.

**Veredito final: FAIL DOCUMENT-ONLY.**

A v0.8 é uma correção documental relevante e fecha focalmente FD07-05 e FD07-06. Ainda não há base para PASS ou PASS WITH CONDITIONS enquanto concorrência permanecer `NOT RUN`, o replay não preservar o outcome original do contrato citado, a prova histórica não comparar efetivamente base/parent e LOW-01 continuar bloqueando DoR.