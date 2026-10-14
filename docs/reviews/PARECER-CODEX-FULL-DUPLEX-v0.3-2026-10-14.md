# PARECER INDEPENDENTE CODEX — CONVERSATIONAL FULL-DUPLEX v0.3

**Data:** 14 de outubro de 2026  
**Repositório:** `otavioegal/ia-os-forge-round5`  
**SHA auditado:** `2fe0b0b2b75f2fc1430f639839e2d29d563f6dcb`  
**Modalidade:** auditoria documental independente, somente leitura  
**Veredito exclusivo:** **FAIL DOCUMENT-ONLY**

O SHA foi confirmado diretamente no checkout destacado. O repositório não foi alterado. Nenhum teste, checker, build, parser, migration, banco, provider, staging ou API foi executado. Este parecer não constitui PASS operacional e não autoriza BUILD-00.

Como o ambiente é somente leitura e o pedido proíbe alterações, o parecer não foi persistido no repositório; segue integralmente nesta resposta.

## 1. Escopo examinado

Foram lidos integralmente os 14 arquivos de `docs/planning/conversational-full-duplex-v0.3/`, de `CMP-FD-00` a `CMP-FD-13`, além de:

- [PARECER-CODEX-FULL-DUPLEX-v0.2-2026-10-13.md](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.2-2026-10-13.md)
- [PROMPT-GROK-FULL-DUPLEX-v0.3-CORRECTIVE.md](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/reviews/PROMPT-GROK-FULL-DUPLEX-v0.3-CORRECTIVE.md)
- [ATA-FOUNDER-AQS-CONVERSATIONAL-2026-10-13.md](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/governance/ATA-FOUNDER-AQS-CONVERSATIONAL-2026-10-13.md)
- [ADR-FDR-AQ07-FULL-DUPLEX-MVP-2026-10-13.md](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/governance/ADR-FDR-AQ07-FULL-DUPLEX-MVP-2026-10-13.md)
- FDP-16A v1.7, FDP-15 histórico, CMP v0.3 e full-duplex v0.2 nas seções relevantes a ledger, idempotência, schemas, privacidade, oráculos e governança.

Os relatórios de mudança, consistência e disposição de findings da v0.3 foram tratados como índices de alegações do autor, não como evidência de fechamento.

## 2. Conclusão executiva

A v0.3 corrige materialmente:

- a leitura de headroom antes do lock;
- a multiplicação de teto entre sessões;
- a ausência dos seis timestamps no schema;
- o preâmbulo `HELLO`;
- grande parte da união discriminada de mídia;
- o CAS de Task/Build em intenção;
- a fixture AEC que antes recebia `echo=true`;
- a especificação de migration/rollback.

Contudo, o pacote ainda não é integrável porque persistem bloqueios normativos:

1. A cadeia de tenant não cobre de forma completa Operation e Reservation, e O37 testa apenas `task_id` estrangeiro.
2. A ordem normativa de CAS contradiz a regra de replay idempotente.
3. O “cap” de sessão pode ser rompido por settlement cujo custo real excede a estimativa.
4. O contrato de mídia ainda é incompleto em ACK/erros/handshake de falha e não possui fixture JSON independente nem teste de reprodutibilidade dos digests.
5. A fixture AEC não contém, no trecho humano, mistura aditiva de eco e fala: a fala sobrescreve o eco.
6. Dois campos declarados como existentes em `observation` são proibidos pelo próprio schema fechado.
7. Owners, effort e DoR continuam pendentes.
8. Todos os oráculos permanecem NOT RUN e sem evidência.

## 3. Matriz de findings

| Finding | Estado | Síntese |
|---|---:|---|
| HIGH-01 | **CLOSED** documentalmente | Lock financeiro e rollback foram reescritos adequadamente; riscos novos são tratados separadamente abaixo. |
| HIGH-02 | **CLOSED** documentalmente | Há predicado físico de overlap, timestamps tipados e negativos contra pause-before-STT. |
| HIGH-03 | **PARTIAL** | União melhorou, mas handshake de erro, ACK e fixture/digest reproduzível permanecem incompletos. |
| NEW-HIGH-01 | **CLOSED** documentalmente | Um root por org/projeto, autoridade humana e soma de fatias sob o mesmo lock. |
| NEW-HIGH-02 | **CLOSED** documentalmente | Build pai é bloqueado antes de leitura financeira; O35 cobre chaves distintas. |
| NEW-HIGH-03 | **PARTIAL** | Channel/session/project/Build/Task estão cobertos, mas Operation/Reservation e os negativos completos não. |
| NEW-MEDIUM-01 | **PARTIAL** | Campos CAS e 409 existem, mas a ordem de avaliação contradiz replay de `command_id`. |
| NEW-MEDIUM-02 | **CLOSED** documentalmente | Os seis timestamps agora pertencem ao schema fechado, com nulabilidade e observador. |
| NEW-MEDIUM-03 | **PARTIAL** | `echo=true` deixou de ser premissa, mas a fixture não produz efetivamente fala+eco no mesmo trecho. |
| MEDIUM-01 | **CLOSED**, preservado | Duck, stop, cancel, incerteza, HELD e proibição de redispatch permanecem separados. |
| MEDIUM-02 | **CLOSED**, preservado | Epoch/generation e corte atômico foram preservados. |
| MEDIUM-03 | **CLOSED**, preservado | Registry/Policy Service e deny em divergência permanecem normativos. |
| MEDIUM-04 | **CLOSED**, preservado | Identidade, proveniência e separação do review formal permanecem. |
| MEDIUM-05 | **CLOSED**, preservado | Pontos de medição sem SLA inventado permanecem. |
| LOW-01 | **PARTIAL** | Fixtures avançaram, mas pessoa, effort e DoR permanecem pendentes. |
| NEW-HIGH-04 | **OPEN** | Settlement real pode romper `session_slice_minor`. |
| NEW-MEDIUM-04 | **OPEN** | Campos declarados em `observation` não existem no schema fechado. |
| NEW-MEDIUM-05 | **OPEN** | Digests da FX-01 não têm artefato/reprodutor documental executável. |
| NEW-MEDIUM-06 | **OPEN** | Unicidade de sessão não é explicitamente tenant-composta. |

## 4. Findings detalhados

### HIGH-01 — CLOSED documentalmente

**Evidência.** O pacote proíbe leitura de dinheiro, stop e reconciliação antes de C1 em [CMP-FD-01:101-114](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-01-LEDGER-AND-BUDGET-AUTHORITY.md:101). O primeiro lock é o Build pai, seguido por Task, Operation, Reservation e ManualReconciliation em [CMP-FD-01:135-155](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-01-LEDGER-AND-BUDGET-AUTHORITY.md:135).

Isso é compatível com o protocolo financeiro v1.7, que exige Build primeiro e Operation → Reservation → ManualReconciliation depois, em [FDP-16A:355-375](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md:355).

O rollback agora possui pré-condições por passo, bloqueia remoção diante de `SESSION_CLOSED`, outbox, audit, proof ou ledger e prevê consumidor rebaixado fail-closed: [CMP-FD-13:23-65](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-13-MIGRATION-ROLLBACK.md:23).

**Risco residual:** nenhum fechamento operacional; o desenho não foi implementado nem exercitado.

**Reparo:** não reabrir o texto; implementar futuramente exatamente essa ordem e executar O35 mais os oráculos v1.7.

**Oráculo negativo:** tentativa de ler `budget_*`, `stop_latch` ou reconciliação antes do lock deve falhar a revisão/contract test; execução continua **NOT RUN**.

### HIGH-02 — CLOSED documentalmente

Os seis timestamps integram `observation`, com clock monotônico, provenance de observador e nulabilidade por evento: [CMP-FD-02:217-249](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-02-MEDIA-EVENT-SCHEMAS.md:217).

A FX-01 contém oito eventos e mede reprodução real via `PLAYBACK_SPAN`, não apenas geração/recepção. O predicado exige captura e forward ao STT durante playback e rejeita pause-before-STT: [CMP-FD-07:563-607](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-07-STORIES-ORACLES-FIXTURES.md:563).

**Risco:** fechamento apenas normativo; O01/O13/O14 não foram executados.

**Reparo:** manter os predicados e produzir evidência futura com `clock_domain_id` único verificável.

**Oráculo negativo:** `generated_at_ns` sem `PLAYBACK_SPAN`, ou `STOPPED` antes do primeiro forward STT, deve reprovar O01. **NOT RUN.**

### HIGH-03 — PARTIAL

A v0.3 corrige vários pontos: preâmbulo próprio em [CMP-FD-02:9-55](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-02-MEDIA-EVENT-SCHEMAS.md:9), união fechada em [CMP-FD-02:57-131](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-02-MEDIA-EVENT-SCHEMAS.md:57), payloads em `:133-215`, digest em `:251-263` e crosswalk em `:291-310`.

Persistem lacunas:

- `HELLO_ACK.selected_media_contract` e `selected_speech_contract` são obrigatórios e descritos como “valor ou erro”, mas não existe uma variante discriminada de rejeição nem shape de erro pré-handshake; ver `:38-55`.
- O texto menciona `SPEECH_UNSUPPORTED_VERSION` em `:55`, mas a taxonomia adicional de `:275-287` não o inclui.
- `ack_of_sequence` é apenas campo anulável; faltam limites (`<= último sequence recebido`), rejeição de ACK futuro, replay de ACK e outcome normativo. Ver `:72-76,109`.
- Não existe artefato JSON separado nem schema machine-readable; os oito objetos estão embutidos no Markdown.
- Não existe teste/reprodutor do digest canônico. A própria checagem do autor admite que nenhum parser foi executado em [CMP-FD-12:30](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-12-CONSISTENCY-REPORT.md:30).

**Risco:** dois implementadores podem produzir handshakes/ACKs incompatíveis ou aceitar um digest incorreto como fixture normativa.

**Reparo:** publicar schemas fechados para `HELLO`, `HELLO_ACK_SUCCESS`, `HELLO_ACK_ERROR` e eventos pós-handshake; normatizar ACK futuro/duplicado/out-of-scope; fornecer FX-01 como JSON de oito eventos e um vetor canônico `canonical_bytes → sha256`.

**Oráculo negativo:** ACK maior que o último sequence, erro de versão sem variante válida, campo extra e digest divergente devem ser rejeitados sem criar sessão ou efeito. **NOT RUN.**

### NEW-HIGH-01 — CLOSED documentalmente

A autoridade do teto é exclusivamente humana; o root é único por `(organization_id, project_id)` e `OpenConversationalAnchor` não aceita teto: [CMP-FD-01:23-38](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-01-LEDGER-AND-BUDGET-AUTHORITY.md:23), `:44-76`, `:164-180`.

O36 serializa duas sessões no mesmo Build e recusa soma 160 sob teto 100: [CMP-FD-07:647-654](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-07-STORIES-ORACLES-FIXTURES.md:647). O40 recusa teto autodeclarado em `:656-661`.

**Risco:** O36/O40 continuam NOT RUN. A relação entre orçamento conversacional e Builds `PRODUCT` continua explicitamente não decidida em [CMP-FD-11:18](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-11-OPEN-QUESTIONS.md:18), mas isso não recria multiplicação entre sessões.

**Oráculo negativo:** duas sessões concorrentes de organizações distintas devem tocar roots distintos; duas sessões da mesma org/projeto devem serializar no mesmo root. **NOT RUN.**

### NEW-HIGH-02 — CLOSED documentalmente

O Build compartilhado é o primeiro lock, e O35 usa duas chaves/estimates distintos, não somente duplicação da mesma idempotency key: [CMP-FD-01:137-158](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-01-LEDGER-AND-BUDGET-AUTHORITY.md:137), [CMP-FD-07:637-645](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-07-STORIES-ORACLES-FIXTURES.md:637).

**Oráculo negativo:** dois estimates 60 sob teto 100 não podem comprometer 120. **NOT RUN.**

### NEW-HIGH-03 — PARTIAL

A fase B fecha canal → sessão → Task → Build e usa `404 NOT_FOUND` opaco: [CMP-FD-01:116-133](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-01-LEDGER-AND-BUDGET-AUTHORITY.md:116). A migration adiciona FKs compostas Task→Build e Operation→Task em [CMP-FD-13:13-15](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-13-MIGRATION-ROLLBACK.md:13).

Porém:

- não há FK composta ou predicado equivalente para Reservation→Operation;
- a consulta/lock de Operation e Reservation existentes em `CMP-FD-01:139-140` não especifica predicate tenant-composto;
- O37 cobre somente `task_id` de outra organização, não session, Build, Operation e Reservation estrangeiros: [CMP-FD-07:663-671](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-07-STORIES-ORACLES-FIXTURES.md:663);
- isso fica aquém do prompt corretivo, que exigiu a cadeia completa em [PROMPT v0.3:19](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/reviews/PROMPT-GROK-FULL-DUPLEX-v0.3-CORRECTIVE.md:19).

**Risco:** replay ou lookup de Operation/Reservation pode ser implementado por identificador sem prova estrutural de pertencimento ao mesmo tenant.

**Reparo:** FK composta Reservation `(organization_id, project_id, operation_id)` → Operation; todas as consultas e índices financeiros tenant-compostos; expandir O37 para cada elo isoladamente e para combinações cruzadas.

**Oráculo negativo:** canal A com session/Build/Task/Operation/Reservation de B deve sempre produzir o mesmo 404 opaco, zero lock/débito no tenant B e zero detalhe de existência. **NOT RUN.**

### NEW-MEDIUM-01 — PARTIAL

Os campos `expected_task_version` e `expected_build_version` são obrigatórios em [CMP-FD-01:107-114](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-01-LEDGER-AND-BUDGET-AUTHORITY.md:107), e mismatch produz rollback/409 em `:147-155`.

Há, entretanto, contradição de ordem:

- passo D3 verifica versão e retorna `409`;
- apenas D7 reconhece `command_id` já comprometido e diz que deve retornar `200 IDEMPOTENT_REPLAY` “mesmo que a version corrente já tenha andado”.

Uma execução literal nunca chega a D7 quando o replay carrega as versões originais.

**Risco:** o mesmo comando comprometido pode alternar entre 200 e 409 conforme a implementação, quebrando idempotência e recuperação.

**Reparo:** após obter locks, consultar primeiro o registro durável de `command_id`. Se já comprometido e digest igual, replay do outcome vence CAS; se não comprometido, aplicar CAS; mesmo `command_id` com digest divergente deve ser 409 específico.

**Oráculo negativo:** replay comprometido com versões antigas deve retornar o outcome anterior; comando novo com versões antigas deve retornar `409 VERSION_CONFLICT`. **NOT RUN.**

### NEW-MEDIUM-02 — CLOSED documentalmente

Os seis timestamps foram incorporados ao objeto fechado e à matriz de nulabilidade, satisfazendo o defeito original. Veja [CMP-FD-02:217-249](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-02-MEDIA-EVENT-SCHEMAS.md:217).

**Oráculo negativo:** timestamp proibido para o `event_type`, ou timestamp sem provenance irmã, deve produzir 422. **NOT RUN.**

### NEW-MEDIUM-03 — PARTIAL

A fixture já não recebe `echo=true`; reference e mic são entradas, e `aec_decision` é saída: [CMP-FD-07:609-631](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-07-STORIES-ORACLES-FIXTURES.md:609).

Mas a construção de `mic_pcm` primeiro copia eco e depois faz `mic[i] = 16000` no trecho humano (`:615-616`). Essa segunda atribuição **substitui**, não soma, o eco. Logo, entre 1000 e 1199 não há sinal misto de fala humana + eco.

**Risco:** um componente que apenas segmenta pela amplitude pode passar sem demonstrar preservação de fala sobreposta ao cancelamento de eco.

**Reparo:** definir `mic[i] = clamp(reference[i-480] // 2 + human[i])` no trecho misto; medir erro contra `human[i]` após cancelamento; incluir negativos de falso positivo e falso negativo.

**Oráculo negativo:** saída que elimina a fala, preserva o eco, ou só funciona quando os sinais não coexistem deve falhar. **NOT RUN.**

### LOW-01 — PARTIAL

As fixtures e o processo de atribuição foram melhorados, mas todas as sete histórias continuam com pessoa `PENDING`, effort `UNSTATED` e DoR `NOT MET`: [CMP-FD-07:7-27](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-07-STORIES-ORACLES-FIXTURES.md:7).

**Reparo:** ato humano com pessoa nomeada, effort registrado e checklist DoR atendido. Papel proposto não basta.

**Oráculo negativo:** qualquer história marcada Ready/DoR MET sem esses campos deve falhar.

## 5. Novos findings

### NEW-HIGH-04 — OPEN — `session_slice_minor` não limita settlement real

A v0.3 declara como invariante que HELD + SETTLED por Task não excede `session_slice_minor`: [CMP-FD-01:29-36](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-01-LEDGER-AND-BUDGET-AUTHORITY.md:29).

Na reserva, porém, só o estimate é comparado à fatia (`:151-155`). O protocolo v1.7 permite settlement com `actual > estimate` quando ainda cabe no teto do Build: [FDP-16A:322-324](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md:322). A v0.3 não acrescenta ao `RecordReceipt` a checagem de `session_slice_minor`.

**Reprodução documental:** fatia 50, estimate 40, actual 70, root com headroom suficiente. A reserva passa; o settlement v1.7 também pode passar; o total SETTLED da Task vira 70 e viola a invariante 4.

**Risco:** o sub-limite de sessão é apenas declaratório e pode ser ultrapassado por custo confirmado.

**Reparo:** sob o mesmo Build lock, settlement conversacional deve verificar `settled_da_task + held_restante_da_task - estimate + actual <= session_slice_minor`; caso contrário manter HELD/RECONCILING com `pending_provider_cost`, sem movimento.

**Oráculo negativo:** estimate cabe na fatia, actual não cabe, mas cabe no root; settlement deve ser bloqueado sem romper nenhum contador. Não há oráculo atual para isso.

### NEW-MEDIUM-04 — OPEN — campos inexistentes em `observation`

A política afirma que `consent_stop_deadline_ns` existe em `observation`: [CMP-FD-04:24-31](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-04-POLICY-SECURITY-PRIVACY.md:24).

A observabilidade afirma que `observation_tolerance_ns` existe: [CMP-FD-06:9-17](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-06-OBSERVABILITY.md:9).

Nenhum deles consta do objeto fechado `observation` em `CMP-FD-02:221-247`; campos desconhecidos são rejeitados em `CMP-FD-02:5,96`.

**Risco:** requisitos normativos inexprimíveis no contrato publicado.

**Reparo:** inserir ambos no schema com tipo, nulabilidade, event types legais, provenance e semântica; ou remover as afirmações de existência.

**Oráculo negativo:** evento que usa os campos hoje seria simultaneamente obrigatório pela prosa e inválido pelo schema.

### NEW-MEDIUM-05 — OPEN — digest sem vetor reproduzível

O algoritmo canônico é descrito em [CMP-FD-02:251-263](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-02-MEDIA-EVENT-SCHEMAS.md:251), e a FX-01 inclui oito strings `event_digest`. Não existe arquivo de fixture independente, canonical bytes esperados por evento ou teste de reprodutibilidade. Nenhum parser foi executado, conforme `CMP-FD-12:30`.

**Risco:** erro de digest no Markdown torna toda FX-01 inválida, e a divergência somente apareceria durante implementação.

**Reparo:** publicar JSON válido com os oito eventos, vetor canonical UTF-8 e digest esperado, além de teste determinístico que recalcule todos.

**Oráculo negativo:** alterar uma chave, null, inteiro ou byte deve mudar o digest e resultar em `DIGEST_MISMATCH`/`EVENT_ID_REUSED`.

### NEW-MEDIUM-06 — OPEN — unicidade de sessão sem escopo tenant explícito

A regra é “uma task aberta por `session_id`” em [CMP-FD-01:84-97](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-01-LEDGER-AND-BUDGET-AUTHORITY.md:84), repetida pela migration em [CMP-FD-13:13](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-13-MIGRATION-ROLLBACK.md:13).

Não está dito se o índice é `(session_id)` global ou `(organization_id, project_id, session_id)`.

**Risco:** colisão cross-tenant pode negar abertura ou revelar, por diferença de erro, que o UUID já existe.

**Reparo:** tornar a chave explicitamente tenant-composta e manter a resposta opaca.

**Oráculo negativo:** duas organizações usando o mesmo UUID de sessão não devem colidir, compartilhar Task ou produzir resposta distinguível.

## 6. Preservação dos MEDIUM-01..05

Não encontrei regressão objetiva que justifique reabri-los:

- **MEDIUM-01:** lifecycle conserva STOP_LOCAL, cancel do provider, prova e HELD separados em [CMP-FD-03:10-102](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/planning/conversational-full-duplex-v0.3/CMP-FD-03-LIFECYCLE.md:10).
- **MEDIUM-02:** epoch/generation, corte atômico, buffer discard e reconnect permanecem em `CMP-FD-04:11-48`.
- **MEDIUM-03:** registry vence auto-relato e cada egress é rechecado em `CMP-FD-04:50-84`.
- **MEDIUM-04:** speaker, origin, source turns, evidence e separação do review formal permanecem em `CMP-FD-05:17-51`.
- **MEDIUM-05:** pontos de medida existem e os aceites permanecem sem SLA em `CMP-FD-06:19-46`.

Os novos findings de schema acima não convertem automaticamente esses cinco em REGRESSED, pois suas invariantes centrais continuam normativas.

## 7. Governança, AQs e gates

A v0.3 preserva corretamente as decisões humanas:

- **APPROVED:** AQ-01, AQ-02, AQ-03, AQ-05, AQ-06, AQ-07, AQ-08, AQ-10 e AQ-11.
- **DEFERRED/UNDECIDED:** AQ-04, AQ-09 e AQ-12.

A fonte normativa é a Ata, especialmente [linhas 10-31](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/governance/ATA-FOUNDER-AQS-CONVERSATIONAL-2026-10-13.md:10), e o ADR AQ-07 mantém full-duplex natural obrigatório, sem half-duplex como substituto, em [linhas 11-30](C:/Users/User/AppData/Local/Temp/ia-os-forge-full-duplex-v03-codex-independent/docs/governance/ADR-FDR-AQ07-FULL-DUPLEX-MVP-2026-10-13.md:11).

Também permanecem corretamente pendentes:

- FDP-14;
- FDP-15;
- incorporação/consolidação da baseline;
- owners e effort;
- BUILD-00.

Não identifiquei fornecedor escolhido, compartilhamento implícito com Founder OS, recibo fictício ou autorização de BUILD-00.

## 8. Estado dos oráculos

- 91 oráculos v1.7: **NOT RUN nesta revisão**.
- CMP-O-01..36, inclusive CMP-O-28: **NOT RUN; evidence ABSENT**.
- CMP-FD-O01..O40: **NOT RUN; evidence ABSENT**.
- O35, O36, O37 e O40: especificados, mas **NOT RUN**.
- CMP-FD-O28: especificado, mas **NOT RUN**.
- Nenhum run id, host, artifact hash, exit code ou evidência de execução foi apresentado.

A distinção entre CMP-O-28, de independência formal, e CMP-FD-O28, de AEC/VAD, foi preservada.

## 9. Recomendação de gate

**FAIL DOCUMENT-ONLY.**

Recomendo:

1. Não integrar `forge.conversation.delta.v2`.
2. Não promover `cmp.media.duplex.v1` a contrato aprovado.
3. Não incorporar esta pasta à baseline.
4. Não aprovar FDP-14/FDP-15 por inferência.
5. Não autorizar BUILD-00.
6. Produzir v0.4 aditiva corrigindo:
   - cadeia tenant completa, inclusive Reservation;
   - precedência idempotência-versus-CAS;
   - enforcement de `session_slice_minor` no settlement real;
   - handshake/ACK/error schemas;
   - campos ausentes de `observation`;
   - FX-01 JSON e vetores de digest reproduzíveis;
   - fixture AEC com mistura aditiva real;
   - unicidade tenant-composta de sessão;
   - owners, effort e DoR.
7. Submeter o novo SHA imutável a outra auditoria Codex independente e somente leitura.

**Veredito final: FAIL DOCUMENT-ONLY.** A v0.3 fecha documentalmente parte substancial dos bloqueios financeiros e de simultaneidade, mas ainda contém contradições normativas suficientes para impedir integração segura.
