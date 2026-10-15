# PARECER INDEPENDENTE CODEX — CONVERSATIONAL FULL-DUPLEX v0.7

**Data:** 15 de outubro de 2026  
**SHA auditado:** `1a71dfa44fc2c88174c113e5c68eddc18d6cfad3`  
**Modalidade:** revisão documental independente, clone isolado e somente leitura  
**Veredito:** **FAIL DOCUMENT-ONLY**  
**Conclusão operacional:** nenhuma. Este parecer não declara PASS operacional.

O SHA foi confirmado por leitura direta de `.git/HEAD`. Nenhum arquivo foi modificado. Não executei checker, teste, parser, migration, banco, provider, deploy, BUILD-00 ou qualquer oráculo. Todas as execuções permanecem **NOT RUN**.

## 1. Escopo

Foram lidos integralmente os 10 artefatos de `docs/planning/conversational-full-duplex-v0.7/`:

- os oito documentos Markdown;
- `fixtures/CMP-FD-FX-03-ack.json`;
- `tools/check_fd_fx03_ack.py`.

Também foram confrontados:

- normas, fixture e checker da v0.6;
- documentos relevantes da v0.5;
- parecer Codex v0.4 e histórico pertinente;
- FDP-16A v1.7;
- `cmp.speech.v0`;
- evolução proposta de `cmp.media.duplex.v1`;
- decisões e atas do Founder;
- gates FDP-14/FDP-15/baseline/BUILD-00.

Não existe no clone um arquivo `PARECER-CODEX-FULL-DUPLEX-v0.5-*` ou `PARECER-CODEX-FULL-DUPLEX-v0.6-*`. O último parecer Full-Duplex disponível é o v0.4, cujo SHA e veredito estão em `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.4-2026-10-14.md:4-6`. Assim, referências internas a uma v0.5/v0.6 “auditada” foram tratadas como alegações sem parecer independente incorporado ao repositório.

## 2. Conclusão executiva

A correção focal da v0.7 está documentalmente correta:

- ambos os campos ACK nulos resultam em `NO_ACK`;
- exatamente um campo nulo resulta em `422 ACK_SCOPE_MISMATCH`;
- essas decisões precedem `ACK_STREAM_UNALLOCATED`;
- o `stream_id` do evento não é herdado;
- o checker declara corretamente que cobre somente as linhas da fixture;
- `FX03-NO-ACK` é explícito;
- as duas direções do mismatch estão presentes;
- regressão não escreve e aceite só eleva o inteiro no modelo local.

Contudo, a v0.7 não é suficiente para PASS documental do pacote/protocolo:

1. falta caso de fixture para `n < 0`, embora a norma e o checker o classifiquem;
2. não há prova estática de isolamento por `ack_stream_id` e `receiver_participant_id`;
3. a fixture não possui `receiver_participant_id`;
4. os casos de “race” são replays sequenciais em memória, não concorrência, lock ou idempotência transacional;
5. o checker não valida ausência de dinheiro/microfone para todos os negativos;
6. diversos campos declarativos da fixture — inclusive `opaque`, `zero_effect` e `zero_new_effect` — não são conferidos;
7. HIGH-03 permanece apenas parcialmente demonstrado;
8. LOW-01 continua bloqueando DoR;
9. inexiste no clone o parecer independente v0.5/v0.6 invocado pela rastreabilidade.

## 3. Matriz de findings

| Finding | Estado | Fundamentação |
|---|---|---|
| FD07-01 — par null → `NO_ACK` | **CLOSED documentalmente** | Norma, fixture e implementação estática concordam; não é fechamento operacional |
| FD07-02 — mismatch bidirecional | **CLOSED documentalmente** | As duas formas de um único null estão especificadas e presentes |
| FD07-03 — precedência e primeiro casamento | **CLOSED documentalmente** | Mismatch/null precedem unallocated/zero/demais decisões |
| FD07-04 — checker limitado à fixture | **CLOSED documentalmente** | O limite é declarado honestamente; não há alegação de execução do protocolo |
| FD07-05 — completude dos negativos | **PARTIAL** | Falta linha explícita para `ack_of_sequence < 0` e validação completa dos efeitos |
| FD07-06 — isolamento por stream/receiver | **OPEN** | Contrato define o trio, mas a fixture/checker não modelam receiver nem interferência cruzada |
| FD07-07 — race monotônica real | **OPEN** | Há apenas replay sequencial local; lock e transações continuam NOT RUN |
| FD07-08 — idempotência/duplicata com efeitos | **PARTIAL** | Código/inteiro são conferidos, mas `zero_new_effect`, dinheiro, microfone e replay transacional não |
| FD07-09 — integridade histórica e cadeia de pareceres | **PARTIAL** | v0.6/v0.7 coexistem sem edição aparente, mas o parecer v0.5/v0.6 citado não está no clone |
| HIGH-03 | **PARTIAL** | Texto normativo melhorou; negativos, isolamento e concorrência ainda não estão completos |
| NEW-MEDIUM-06 | **CLOSED documentalmente nesta revisão** | Opção B fecha null ativo antes do índice e mantém predicado correto; migration continua NOT RUN |
| LOW-01 | **OPEN BLOCKING DoR** | Pessoa PENDING, effort UNSTATED, DoR NOT MET |
| Findings anteriormente CLOSED | **CLOSED; sem regressão documental encontrada** | A v0.7 é focal e declara não alterar os contratos correspondentes |
| Finding previamente CLOSED em estado `REGRESSED` | **nenhum identificado** | Não foi encontrada evidência objetiva de regressão |

## 4. Findings detalhados

### 4.1 FD07-01 — CLOSED documentalmente — ambos null são `NO_ACK`

A norma v0.6 já estabelecia primeiro casamento:

- um único null: `ACK_SCOPE_MISMATCH`;
- ambos null: nenhum ack;
- só depois: stream não alocado.

Evidência: `docs/planning/conversational-full-duplex-v0.6/CMP-FD-02-ACK-MONOTONIC.md:37-50`.

O checker v0.6 divergia: o XOR cobria somente um null e, quando ambos eram `None`, a consulta de alocação classificava o valor como `ACK_STREAM_UNALLOCATED`: `docs/planning/conversational-full-duplex-v0.6/tools/check_fd_fx03_ack.py:32-37`.

A v0.7 corrige a ordem:

- XOR em `docs/planning/conversational-full-duplex-v0.7/tools/check_fd_fx03_ack.py:55-58`;
- ambos null → `NO_ACK` em `:59-60`;
- unallocated somente depois, em `:61-62`.

A fixture torna o caso explícito e exige high-water inalterado, nenhuma escrita, dinheiro zero, microfone fechado e classificação não-unallocated: `docs/planning/conversational-full-duplex-v0.7/fixtures/CMP-FD-FX-03-ack.json:157-170`.

A norma equivalente está em `docs/planning/conversational-full-duplex-v0.7/CMP-FD-02-ACK-NULL-PAIR.md:21-25` e os efeitos em `:34-36`.

**Correção falsificável satisfeita:** uma fixture com ambos null deve produzir exatamente `NO_ACK`, preservar o high-water e não alcançar a decisão de stream não alocado.

**Ressalva:** CLOSED apenas para consistência documental e lógica estática inspecionada. O81 permanece NOT RUN.

### 4.2 FD07-02 — CLOSED documentalmente — mismatch nas duas direções

A ordem retorna `ACK_SCOPE_MISMATCH` quando exatamente um campo está ausente: `docs/planning/conversational-full-duplex-v0.7/tools/check_fd_fx03_ack.py:55-58`.

As duas direções estão presentes:

- sequence preenchida/stream null: fixture `:173-185`;
- sequence null/stream alocado: fixture `:188-200`.

O checker exige os dois IDs em `docs/planning/conversational-full-duplex-v0.7/tools/check_fd_fx03_ack.py:37-45` e valida suas formas em `:103-117`.

O texto proíbe inferir `ack_stream_id` do `stream_id` do evento e proíbe reclassificar stream-only como zero ou unallocated: `docs/planning/conversational-full-duplex-v0.7/CMP-FD-02-ACK-NULL-PAIR.md:34-36`.

**Correção falsificável satisfeita:** remover qualquer uma das duas linhas deve causar `FAIL_CASE_SET`/`FAIL_NULL_CASES_MISSING`; inverter o código esperado deve causar `FAIL_CODE`.

O82 e O83 continuam NOT RUN.

### 4.3 FD07-03 — CLOSED documentalmente — ordem de avaliação e high-water local

A ordem proposta é:

1. um único null;
2. ambos null;
3. stream não alocado;
4. zero;
5. negativo;
6. lock/releitura no protocolo;
7. futuro;
8. regressão;
9. duplicata;
10. aceite crescente.

Evidência: `docs/planning/conversational-full-duplex-v0.7/CMP-FD-02-ACK-NULL-PAIR.md:21-32`.

A implementação estática segue essa ordem em `docs/planning/conversational-full-duplex-v0.7/tools/check_fd_fx03_ack.py:53-81`.

O modelo impede diminuição:

- regressão conserva `current`: `:75-76`;
- duplicata conserva `current`: `:77-78`;
- aceite escreve `n` apenas quando `current < n <= emitted`: `:79-80`;
- o replay recusa escrita não crescente e qualquer diminuição: `:84-100`;
- a inspeção de cada linha também rejeita diminuição: `:191-199`.

As linhas de zero, futuro, regressão, duplicata, cross-stream e unallocated aparecem respectivamente na fixture em `:13-40`, `:103-113`, `:77-87`, `:90-100`, `:116-127` e `:130-141`.

**Limite:** isso fecha a tabela local, não o procedimento SQL ou a concorrência.

### 4.4 FD07-04 — CLOSED documentalmente — checker não afirma protocolo

O checker declara que cobre somente decisões existentes na fixture e que não executa protocolo, oráculo ou teste de produto: `docs/planning/conversational-full-duplex-v0.7/tools/check_fd_fx03_ack.py:11-18`.

A fixture repete o limite em `docs/planning/conversational-full-duplex-v0.7/fixtures/CMP-FD-FX-03-ack.json:2-5`.

O documento de oráculos diz que `PASS_FIXTURE_ONLY` não é PASS do pacote: `docs/planning/conversational-full-duplex-v0.7/CMP-FD-07-ORACLES.md:3-7`.

O relatório separa “alegação documental” de “checagem estática” e admite ausência de transações/PostgreSQL: `docs/planning/conversational-full-duplex-v0.7/CMP-FD-12-CONSISTENCY-REPORT.md:20-28` e `:50-52`.

Não adoto a saída registrada em `CMP-FD-12:30-48` como evidência independente; o checker não foi executado nesta auditoria.

### 4.5 FD07-05 — PARTIAL — negativos incompletos e efeitos parcialmente ignorados

A norma contém `n < 0 → ACK_REGRESSION`: `docs/planning/conversational-full-duplex-v0.7/CMP-FD-02-ACK-NULL-PAIR.md:26-30`. O checker também possui o branch: `docs/planning/conversational-full-duplex-v0.7/tools/check_fd_fx03_ack.py:65-68`.

Porém, o conjunto obrigatório da fixture não contém caso de sequence negativa: `docs/planning/conversational-full-duplex-v0.7/tools/check_fd_fx03_ack.py:26-40`. A fixture termina com 13 casos e nenhum possui `ack_of_sequence < 0`: `docs/planning/conversational-full-duplex-v0.7/fixtures/CMP-FD-FX-03-ack.json:11-202`.

Também há campos que são apenas declarações não verificadas:

- `zero_effect` de regressão, futuro, unallocated e pair-invalid;
- `zero_new_effect` da duplicata;
- `opaque` do unallocated;
- `zero_money` e `opens_mic` nos casos de zero.

O checker valida `opens_mic`, `zero_money`, ausência de escrita e high-water inalterado somente para `NULL_CASES`: `docs/planning/conversational-full-duplex-v0.7/tools/check_fd_fx03_ack.py:103-126` e `:169-172`. Para os demais casos, limita-se principalmente a código, inteiro e flag de escrita: `:173-208`.

**Correção falsificável:** adicionar pelo menos `FX03-NEGATIVE-SEQUENCE` a `REQUIRED`, com `n=-1`, stream alocado, código `ACK_REGRESSION`, nenhuma escrita, high-water inalterado, dinheiro zero e microfone fechado. Fazer o checker validar efeitos e opacidade para toda linha negativa; alterar qualquer campo deve provocar saída não zero específica.

### 4.6 FD07-06 — OPEN — isolamento por stream e receiver não é provado

A norma v0.6 define o scope lógico como `{session_id, ack_stream_id, receiver_participant_id}` e uma unique física tenant-composta: `docs/planning/conversational-full-duplex-v0.6/CMP-FD-02-ACK-MONOTONIC.md:58-65`.

Também afirma que ACKs do mesmo trio serializam na mesma linha e outro tenant não é travado: `docs/planning/conversational-full-duplex-v0.6/CMP-FD-02-ACK-MONOTONIC.md:95-104`.

Entretanto:

- a fixture possui três IDs de stream, mas todas as decisões de ACK usam o mesmo input stream, salvo o UUID não alocado: `docs/planning/conversational-full-duplex-v0.7/fixtures/CMP-FD-FX-03-ack.json:6-10`, `:13-141`;
- não existe campo `receiver_participant_id`;
- `decide()` recebe apenas um inteiro `current`, não um mapa indexado pelo trio: `docs/planning/conversational-full-duplex-v0.7/tools/check_fd_fx03_ack.py:53-81`;
- `replay()` opera um único high-water: `:84-100`.

Logo, não há evidência de que ACK no input do receptor A não altere output, control ou o estado do receptor B.

**Correção falsificável:** criar fixture com dois streams alocados e dois receivers, high-waters distintos e operações intercaladas. Após cada ACK, exigir que somente a chave `{session, ack_stream, receiver}` correspondente possa mudar. O checker deve falhar se qualquer outra chave mudar.

### 4.7 FD07-07 — OPEN — race monotônica real

A especificação do lock é documentalmente robusta:

- inserção/unique e `SELECT FOR UPDATE`: `docs/planning/conversational-full-duplex-v0.6/CMP-FD-02-ACK-MONOTONIC.md:69-75`;
- `UPDATE` com chave completa e `:n > peer_ack_high_water`: `:76-89`;
- releitura e classificação do perdedor: `:91-102`.

A v0.7 reconhece corretamente que o checker não executa lock nem update real: `docs/planning/conversational-full-duplex-v0.7/CMP-FD-02-ACK-NULL-PAIR.md:47`.

As linhas rotuladas “race” são apenas listas de ordem de commit: `docs/planning/conversational-full-duplex-v0.7/fixtures/CMP-FD-FX-03-ack.json:43-74`. `replay()` itera sequencialmente sobre essas listas: `docs/planning/conversational-full-duplex-v0.7/tools/check_fd_fx03_ack.py:84-100`.

**Correção falsificável:** oráculo futuro com duas transações PostgreSQL reais sobre o mesmo trio, barreira antes do commit e ambas as ordens observadas; final obrigatório 2, nenhuma escrita 2→1, perdedor classificado como regressão/duplicata após releitura. Acrescentar casos paralelos para trios distintos, que não devem bloquear a mesma linha.

O72 permanece NOT RUN.

### 4.8 FD07-08 — PARTIAL — duplicata e idempotência

A decisão local de duplicata está correta: `n == current` retorna `ACK_DUPLICATE` sem escrita em `docs/planning/conversational-full-duplex-v0.7/tools/check_fd_fx03_ack.py:77-78`. A fixture exige high-water 2 antes/depois e `writes_high_water=false`: `docs/planning/conversational-full-duplex-v0.7/fixtures/CMP-FD-FX-03-ack.json:90-100`.

Mas `zero_new_effect` não é lido pelo checker. Também não há `event_id`, `command_id`, outbox ou audit na fixture; portanto ela não demonstra idempotência de transporte, deduplicação persistida ou ausência de segundo efeito fora do inteiro.

A baseline exige dedupe de eventos e replay sem segundo efeito em `docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md:176-191` e preserva replay por `command_id` sem segundo movimento em `:521-533`. Essas regras não são exercitadas pela FX03.

**Correção falsificável:** repetir o mesmo ACK com a mesma identidade durável e depois com nova identidade, exigindo high-water invariável, zero novo audit financeiro, zero abertura de microfone e no máximo um registro idempotente conforme o contrato escolhido. O checker estático, se mantido, deve pelo menos validar `zero_new_effect=true`.

### 4.9 FD07-09 — PARTIAL — integridade e cadeia histórica

A v0.7 declara explicitamente que não edita v0.1–v0.6, baseline, CMP, ata, ADR ou parecer: `docs/planning/conversational-full-duplex-v0.7/CMP-FD-09-CHANGE-REPORT.md:3`.

As pastas v0.6 e v0.7 coexistem e a divergência focal é documentada:

- causa no checker v0.6: `docs/planning/conversational-full-duplex-v0.7/CMP-FD-10-FINDING-DISPOSITION.md:5-10`;
- v0.6 histórica ainda contém a implementação defeituosa em `docs/planning/conversational-full-duplex-v0.6/tools/check_fd_fx03_ack.py:32-37`;
- a v0.7 contém implementação separada, sem sobrescrever o arquivo histórico.

Isso é evidência de preservação no snapshot atual, mas não substitui uma comparação criptográfica com o SHA-base.

Além disso, `docs/planning/conversational-full-duplex-v0.6/CMP-FD-00-INDEX.md:5` afirma que a v0.5 foi auditada em 14/10/2026, e `docs/planning/conversational-full-duplex-v0.7/CMP-FD-08-TRACEABILITY.md:7-8` chama v0.6/v0.5 de auditadas. O parecer correspondente não está presente no clone.

**Correção falsificável:** incorporar o parecer independente v0.5/v0.6 imutável, com SHA auditado e estados dos findings, ou corrigir a rastreabilidade para dizer que esses pacotes eram apenas candidatos. Adicionar manifest de hashes das versões históricas para provar ausência de edição.

## 5. Findings herdados

### HIGH-03 — PARTIAL

O último parecer independente disponível classificou HIGH-03 como PARTIAL: `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.4-2026-10-14.md:67` e detalhou a insuficiência em `:152`.

A v0.5 acrescentou `ack_stream_id`, scope por receptor e autenticação do preâmbulo: `docs/planning/conversational-full-duplex-v0.5/CMP-FD-02-MEDIA-ACK.md:18-64` e `:66-81`.

A v0.6 acrescentou zero explícito e escrita monotônica: `docs/planning/conversational-full-duplex-v0.6/CMP-FD-02-ACK-MONOTONIC.md:23-33` e `:54-102`.

A v0.7 corrige o par null no checker. Ainda assim, os findings FD07-05, FD07-06 e FD07-07 impedem fechamento integral: negativos incompletos, ausência de isolamento receiver/stream na evidência e race real NOT RUN.

**Correção falsificável para CLOSED:** completar negativos, isolamento por trio, efeitos zero e executar os oráculos transacionais O71–O83 em ambiente autorizado. Até lá, `cmp.media.duplex.v1` não deve ser promovido.

### NEW-MEDIUM-06 — CLOSED documentalmente nesta revisão

O parecer v0.4 classificou o item como PARTIAL por ambiguidade entre `task.status` e `session_status`: `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.4-2026-10-14.md:77` e `:247`.

A v0.5 passou a usar o predicado correto, mas ainda permitia `session_id` null no unique: `docs/planning/conversational-full-duplex-v0.5/CMP-FD-13-MIGRATION.md:87-113`.

A v0.6 fecha essa folga documentalmente:

- conta uma única task ativa null antes do índice: `docs/planning/conversational-full-duplex-v0.6/CMP-FD-13-MIGRATION-SESSION-ID.md:18-30`;
- cria e valida check condicional: `:32-51`;
- cria o índice somente depois: `:53-68`;
- preserva 409 local e 404 opaco cross-tenant: `:70-76`;
- mantém flag desligada e rollback conservador: `:16`, `:78-80`.

Isso satisfaz o defeito documental original. O79/O80 e a migration continuam NOT RUN; portanto não há aprovação operacional.

### LOW-01 — OPEN BLOCKING DoR

A v0.7 preserva sete histórias sem pessoa e sem effort: `docs/planning/conversational-full-duplex-v0.7/CMP-FD-07-ORACLES.md:9-11`.

O estado também consta em `docs/planning/conversational-full-duplex-v0.7/CMP-FD-10-FINDING-DISPOSITION.md:22-25`.

**Correção falsificável:** ato humano nomeando pessoas responsáveis; effort registrado por essas pessoas; checklist DoR reavaliado e aprovado. Papel abstrato ou nome inventado não fecha o finding.

## 6. Ausência de regressões previamente fechadas

Não encontrei regressão documental objetiva de:

- HIGH-01, HIGH-02;
- NEW-HIGH-01, NEW-HIGH-02;
- NEW-MEDIUM-01, NEW-MEDIUM-02, NEW-MEDIUM-04;
- MEDIUM-01 a MEDIUM-05.

A própria v0.7 limita o escopo e conserva esses estados em `docs/planning/conversational-full-duplex-v0.7/CMP-FD-00-INDEX.md:23` e `CMP-FD-10-FINDING-DISPOSITION.md:27-29`.

Isso não revalida operacionalmente esses findings; apenas registra que nenhum texto da v0.7 os contradiz.

NEW-HIGH-04, NEW-HIGH-03, NEW-MEDIUM-05 e NEW-MEDIUM-03 permanecem CANDIDATE conforme `docs/planning/conversational-full-duplex-v0.7/CMP-FD-08-TRACEABILITY.md:25-29`. Não os marco CLOSED sem o parecer independente ausente.

## 7. Governança e gates

As decisões humanas estão preservadas:

- AQ-01, AQ-02, AQ-03, AQ-05, AQ-06, AQ-07, AQ-08, AQ-10 e AQ-11: APPROVED, conforme `docs/governance/ATA-FOUNDER-AQS-CONVERSATIONAL-2026-10-13.md:10-23`;
- AQ-04, AQ-09 e AQ-12: DEFERRED/UNDECIDED, `:25`;
- full-duplex natural obrigatório, sem half-duplex como substituto: `docs/governance/ADR-FDR-AQ07-FULL-DUPLEX-MVP-2026-10-13.md:11-17`;
- FDP-14, FDP-15, baseline e BUILD-00 seguem em gates separados: `docs/governance/FOUNDER-GATE-FDP14-FDP15-BASELINE-v1.7.md:22-39`;
- a decisão funcional não autoriza BUILD-00, provider, deploy ou testes: `docs/governance/FOUNDER-DECISION-JARVIS-VOICE-ALL-AGENTS-MVP-2026-10-13.md:29-44`.

A v0.7 preserva corretamente:

- `forge.conversation.delta.v4` desligada;
- v3 não integrada;
- migration/deploy/provider/gasto/BUILD-00 não autorizados.

Evidência: `docs/planning/conversational-full-duplex-v0.7/CMP-FD-00-INDEX.md:6-7`, `:23`, e `CMP-FD-11-OPEN-QUESTIONS.md:7-17`.

## 8. Estado dos oráculos

Nesta auditoria:

- checker v0.7: **NOT RUN**;
- checker v0.6: **NOT RUN**;
- O71–O83: **NOT RUN**;
- O01–O70: **NOT RUN**;
- 91 oráculos v1.7: **NOT RUN**;
- 36 CMP-O: **NOT RUN**;
- CMP-O-28 e CMP-FD-O28: **NOT RUN**;
- testes de produto: **NOT RUN**;
- migration: **NOT RUN**;
- banco/PostgreSQL: **NOT RUN**;
- provider/API: **NOT RUN**;
- deploy/staging: **NOT RUN**;
- BUILD-00: **NOT RUN / NÃO AUTORIZADO**.

A saída alegada pelo autor em `docs/planning/conversational-full-duplex-v0.7/CMP-FD-12-CONSISTENCY-REPORT.md:30-48` não foi reproduzida e não foi adotada como evidência independente.

## 9. Recomendação de gate

1. **Não integrar** `forge.conversation.delta.v4`; manter a flag desligada.
2. **Não promover** `cmp.media.duplex.v1` a contrato aprovado.
3. **Não autorizar** BUILD-00, migration, deploy, provider ou gasto.
4. **Não marcar HIGH-03 CLOSED**.
5. Aceitar como correção documental focal apenas:
   - ambos null → `NO_ACK`;
   - um null → `ACK_SCOPE_MISMATCH`;
   - precedência anterior a unallocated;
   - cobertura explicitamente limitada à fixture.
6. Exigir uma v0.8 aditiva ou correção equivalente contendo:
   - negativo explícito `n < 0`;
   - validação dos efeitos para todos os negativos;
   - isolamento por stream e receiver;
   - teste futuro de concorrência PostgreSQL;
   - caso de idempotência/replay com efeitos observáveis;
   - parecer independente v0.5/v0.6 ou correção formal da cadeia de rastreabilidade.
7. Resolver LOW-01 por ato humano antes de DoR.

## 10. Veredito final

**FAIL DOCUMENT-ONLY.**

A v0.7 fecha documentalmente a divergência específica do par nulo e completa as duas direções de `ACK_SCOPE_MISMATCH`. Não há base, porém, para PASS do pacote: a evidência continua restrita a uma fixture incompleta, não cobre isolamento por receiver/stream, não prova race ou idempotência transacional, deixa efeitos declarativos sem validação e depende de uma cadeia de pareceres v0.5/v0.6 ausente no clone.

Este veredito não é reprovação operacional — nenhuma operação foi executada — e tampouco autoriza integração, BUILD-00 ou promoção de contrato.