# CMP-FD-01 v0.2 — Delta normativo proposto FDP-16A / FDP-15

**Estado:** PROPOSTA. Não edita `docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md` nem `historical/round4/docs/planning/FDP-15-v1.0-INTEGRATION-ADAPTER-SPECIFICATION.md`.
**Não é Change Decision aprovada.** Não move dinheiro. Não cria tabela em banco.
**Schema id desta proposta:** `forge.conversation.delta.v1`.
**Achado alvo:** HIGH-01. Fechamento não declarado.

## 1. O que a v1.7 já fecha, e que esta proposta não afrouxa

Citações normativas, arquivo histórico intacto:

- `actor_class` do `forge.command.v1` admite só `human`, `security_operator`, `release_agent`, `coding_engine`, `reviewer`, `system` (FDP-16A §4.1).
- `InvokeCapability` admite só `coding_engine via gateway` (FDP-16A §5).
- `Task.build_id` é NOT NULL e FK para Build (FDP-16A §3.2).
- `Operation.task_id` é NOT NULL (FDP-16A §3.4).
- Reserva, liquidação e release existem só em FDP-16A §8A–§8A.3. Lock order: Build `FOR UPDATE`, depois Operation, Reservation, ManualReconciliation.
- `RecordReceipt` e `ReleaseReservation` são `system` only. Prova só por `forge.provider_ingest` / `ledger.proof_ingest`. Capturer não pode ser coding engine, adapter, reviewer, approver ou confirmer.
- Invariante de linha comprometida: `budget_spent_minor + budget_reserved_minor <= budget_limit_minor`.
- Famílias de adapter FDP-15: exatamente `ENGINE | MODEL | TOOL`. Não existe quarta família.

A v0.3 já tinha recusado impersonar `coding_engine` (CMP-02 v0.3 §8). AQ-01 aprovou o papel `conversation_router` com o mesmo efeito transacional, sem fingir o ator. Este delta especifica esse comando. Não o dá como já presente na v1.7.

## 2. Atores e comando novo

### 2.1 Enum proposto, só neste delta

Valor aditivo: `conversation_router`.

Não substitui o enum histórico. Um writer da baseline, antes de uma Change Decision futura, continua rejeitando esse valor com `422 VALIDATION` / `403 ACTOR_FORBIDDEN`.

O ator é um principal de host, atestado fora do modelo, preso ao Media Gateway. O LLM, o texto do usuário, Jarvis, o Conselho e o Codex conversacional não emitem este `actor_class`. Colar `actor_class=coding_engine` dentro de um payload é dado não confiável e não altera o envelope.

Proibições do `conversation_router`, todas `403`:

| Chamada | Código |
|---|---|
| `InvokeCapability` | `403 CONVERSATION_COMMAND_REQUIRED` |
| `RecordReceipt`, `ReleaseReservation`, `ApplyAuthorizedReconciliation` | `403 ACTOR_FORBIDDEN` |
| `ApproveManualReconciliation`, `ConfirmManualReconciliation` | `403 ACTOR_FORBIDDEN` |
| `DeployRelease`, `MergeTask`, `StopBuild`, `SubmitForReview` | `403 ACTOR_FORBIDDEN` |
| Inserir `ProviderEffectProof` | `422 EVIDENCE_UNTRUSTED` se um proof atribuir capturer a este ator |

`coding_engine` que chame `ReserveConversationalCapability` recebe `403 ACTOR_FORBIDDEN`. Não há caminho inverso de impersonação.

### 2.2 `ReserveConversationalCapability`

Único comando pelo qual o roteador reserva gasto.

| Campo | Tipo | Null | Regra |
|---|---|---|---|
| command_id | uuid | no | idempotência do comando |
| command_type | string | no | literal `ReserveConversationalCapability` |
| actor_ref | string | no | principal host-attested do gateway |
| actor_class | enum | no | literal `conversation_router` |
| caused_by_human_ref | string | no | sessão humana que abriu a conversa; não autoriza sozinha |
| organization_id | uuid | no | |
| project_id | uuid | no | membership rechecada pela Policy Service |
| policy_version | string | no | |
| correlation_id | uuid | no | |
| issued_at | date-time | no | relógio de comando, não prova de overlap de mídia |
| task_id | uuid | no | âncora da sessão |
| build_id | uuid | no | deve ser o `build_id` dessa task |
| capability | string | no | um id da allowlist §4 |
| operation_ref | string | no | 1..128; forma da v0.3 §7.2 |
| input | object | no | sem segredo, sem bytes de áudio no audit |
| normalized_input_digest | sha256 | no | mesma regra de concatenação da FDP-16A §8 |
| estimated_cost_minor | int64 | no | `>= 0`; `0` só se o descriptor diz `side_effects NONE` |
| expected_version | int64 | yes | obrigatório se a task já existe, que é o caso |
| consent_epoch | int64 | no | igual ao epoch corrente se a capability lê áudio |
| capture_generation | int64 | no | igual à geração corrente |
| data_classification | enum | no | `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED` |
| execution_location | enum | no | valor já validado no registry, não o texto do adapter |
| invocation_id | uuid | no | alvo de cancelamento |

**Authorizer.** Policy Service, fora do LLM, antes do commit da reserva. Recheca, na mesma transação e nesta ordem: ator e atestação de host; grant da capability no projeto; capability fora da denylist §4; classificação versus `execution_location`; consent epoch e capture generation quando há áudio; headroom; `stop_latch` false; ausência de reconciliação bloqueante no build; safe mode desligado. O modelo não é callee nem authorizer.

**Efeito comprometido.** Idêntico ao efeito de reserva de `InvokeCapability`, sem ser esse comando:

1. Lock do Build `FOR UPDATE` (FDP-16A §8A.1 passo 1). O `build_id` vem da task.
2. Inserir Operation `RESERVED` com `task_id` NOT NULL.
3. Inserir reservation `HELD`.
4. `reserved_minor += estimated_cost_minor`.
5. Nenhuma chamada de provider dentro da transação.
6. Outbox e audit `budget.reserved` na mesma transação.

**Resposta 200:** `operation_id`, `operation_ref`, `status=RESERVED`, `reservation_id`, `estimated_minor`, `build_id`, `task_id`, `version`, `event_id`.

**Erros:** `402 BUDGET_EXCEEDED`, `403 CAPABILITY_NOT_GRANTED`, `403 CAPABILITY_FORBIDDEN_ON_ANCHOR`, `403 ACTOR_FORBIDDEN`, `403 ACTOR_IMPERSONATION`, `403 CONVERSATION_COMMAND_REQUIRED`, `403 TRUST_BOUNDARY_MISMATCH`, `409 STOP_LATCH`, `409 RECONCILIATION_REQUIRED`, `409 SAFE_MODE`, `409 NOT_SESSION_ANCHOR`, `409 SESSION_NOT_OPEN`, `409 BUILD_KIND_MISMATCH`, `409 OPERATION_REF_REUSED`, `409 DUPLICATE_RESERVATION`, `422 VALIDATION`, `422 CONSENT_EPOCH_STALE`.

Replay do mesmo `command_id` já comprometido: `200 IDEMPOTENT_REPLAY`, sem segunda reserva.

Digest de idempotência, UTF-8, campos separados por newline, igual à v1.7: `project_id`, `task_id`, `operation_ref`, `capability`, JSON canônico do input com chaves ordenadas. Índice único herdado: `(project_id, task_id, operation_ref, capability, normalized_input_digest)`.

Constraint **aditiva** proposta, só para capabilities conversacionais: único `(project_id, operation_ref, capability)`. O mesmo `operation_ref` não reserva em duas tasks. Não altera o índice histórico das capabilities de build. Impede débito duplo da mesma intenção (AQ-10) sem segundo ledger.

`DispatchOperation` continua `system`. O roteador não despacha. Liquidação e release continuam só por prova conclusiva em §8A.3. `receipt_query ABSENT` e ausência de atestação continuam em §8C: `BLOCKED_RECONCILIATION`, reservation `HELD`, sem recibo inventado (AQ-12 não decidido, guarda preservada).

## 3. Task-âncora que satisfaz `build_id NOT NULL` e fica fora do DAG

### 3.1 Por que não anular a FK

Anular `Task.build_id` quebraria o lock order: o primeiro lock é a linha de Build da task. A proposta **não** torna a coluna anulável.

### 3.2 Build de kind próprio

Coluna aditiva `build.kind`, NOT NULL, default `PRODUCT`, valores `PRODUCT | CONVERSATIONAL_ANCHOR`.

Toda linha já existente permanece `PRODUCT` sem rewrite.

Um Build `CONVERSATIONAL_ANCHOR`:

| Campo | Valor normativo |
|---|---|
| build_id | uuid novo; FK alvo da task |
| kind | `CONVERSATIONAL_ANCHOR` |
| plan_revision | literal `conversational-anchor-plan-v1` |
| graph_revision | literal `conversational-anchor-graph-v1` |
| policy_version | a versão checada na abertura |
| budget_limit_minor | inteiro `>= 0` copiado do comando de abertura; não é medição |
| budget_spent_minor | 0 na abertura |
| budget_reserved_minor | 0 na abertura |
| currency | `USD` |
| status | `SESSION_ACTIVE` enquanto a sessão pode reservar; `SESSION_CLOSED` no fecho limpo |
| stop_latch | false na abertura; StopBuild de produto não é o comando |
| evidence_ref | null. Este build nunca fica `READY_FOR_HUMAN_TEST` |

`SESSION_ACTIVE` e `SESSION_CLOSED` são valores aditivos. Um Build `PRODUCT` que os receba: `409 ILLEGAL_BUILD_KIND`. Um Build `CONVERSATIONAL_ANCHOR` que receba `PLANNED`, `TESTING`, `REVIEWING`, `READY_FOR_HUMAN_TEST` ou qualquer outro status de produto: `409 ILLEGAL_BUILD_KIND`.

Consumidores que não conhecem `SESSION_ACTIVE` falham fechados. Não podem tratar o valor como `RUNNING` de produto.

O grafo `conversational-anchor-graph-v1` tem um nó e zero arestas. Não é membro de plano de sprint, não referencia task de produto e não pode ser referenciado por `dependency_task_ids` de task `BUILD_DAG`.

### 3.3 Task

Colunas aditivas:

| Campo | Tipo | Null | Regra |
|---|---|---|---|
| execution_domain | enum | no | default `BUILD_DAG`. Âncora: `CONVERSATIONAL_SESSION` |
| session_id | uuid | yes | NOT NULL sse domínio conversacional |
| session_status | enum | yes | `OPEN`, `CLOSING`, `CLOSED`, `ORPHAN_HELD`. NOT NULL sse domínio conversacional; NULL no DAG |
| anchor_build_kind | enum | yes | deve ser `CONVERSATIONAL_ANCHOR` quando a task é âncora |

`build_id` continua NOT NULL. `task_id` continua NOT NULL nas operations.

Cardinalidade: **uma** task âncora por `session_id` em `OPEN`, `CLOSING` ou `ORPHAN_HELD`. Índice único parcial. Uma sessão fechada não reabre a mesma task; nova sessão é outro par build+task.

`dependency_task_ids` da âncora é exatamente `{}`.

`goal` e `acceptance` são literais de sistema, não texto do modelo:

- goal: `Hold the conversational session ledger anchor`
- acceptance: `Session closes without product DAG effects and without unproven money release`

Status de produto da âncora: valor aditivo `SESSION_OPEN` | `SESSION_CLOSING` | `SESSION_CLOSED` | `SESSION_ORPHAN_HELD`, permitido só quando `execution_domain=CONVERSATIONAL_SESSION`. Task de DAG com esses status: `409 ILLEGAL_TRANSITION`.

Não se reutiliza `RUNNING` para não herdar lease, attempt e worktree. `TaskAttempt` da âncora é proibido: zero linhas. `worktree_ref`, lease e checkpoint são proibidos. `ClaimTask`, `SubmitForReview`, `VerifyTask`, `BeginHandoff`, `MergeTask` na âncora: `409 NOT_A_BUILD_DAG_TASK`.

### 3.4 Comandos de ciclo da âncora

`OpenConversationalAnchor`

- Ator: `conversation_router` via gateway. Não é o modelo.
- Payload: `session_id`, `organization_id`, `project_id`, `policy_version`, `budget_limit_minor`, `currency=USD`, `command_id`.
- Pré-condição: humano autenticado no projeto; não existe âncora aberta para esse `session_id`. Consentimento de microfone **não** é esta abertura (AQ-08 é outro comando).
- Efeito, uma transação: insert do Build `SESSION_ACTIVE` e da Task `SESSION_OPEN` com o mesmo `build_id`. Nenhum provider. Nenhum gasto.
- Erros: `409 ANCHOR_EXISTS`, `403 NOT_PROJECT_MEMBER`, `422 VALIDATION`.

`CloseConversationalAnchor`

- Se existir operation `DISPATCHED`, `RECONCILING` ou `BLOCKED_RECONCILIATION`: `session_status=ORPHAN_HELD`, build permanece `SESSION_ACTIVE` para o lock poder continuar, grants de mídia revogados, **nenhum** `ReleaseReservation`.
- Se toda operation está ausente ou em status terminal monetário (`SETTLED`, `RELEASED`, `DENIED`, `CANCELLED`) e não há prova conclusiva contraditória pendente: task `SESSION_CLOSED`, build `SESSION_CLOSED`, grants revogados.
- `VerifyTask` não fecha a âncora.

`SweepOrphanConversationalAnchor`

- Ator: `system` (watchdog), nunca o modelo.
- Dispara quando o heartbeat de sessão excede `forge.conversation.anchor_orphan_ttl_ms`.
- Valor de planejamento: `120000`. Não é SLO, não é medição, não é RTO.
- Mesma regra de dinheiro do close: incerteza fica `HELD`. Não há release por timeout.

### 3.5 Separação do DAG — invariantes

1. Nenhuma task `BUILD_DAG` lista uma task `CONVERSATIONAL_SESSION` em `dependency_task_ids` (`409 DAG_KIND_MIX`).
2. A âncora não lista task alguma.
3. `DeriveRhft`, `MarkTesting`, `MarkReviewing`, `SubmitForApproval`, `ApprovePlan` no build âncora: `409 ILLEGAL_BUILD_KIND`.
4. A âncora não produz `EvidenceBundle` de produto e não satisfaz predicado de `READY_FOR_HUMAN_TEST`.
5. `graph_revision` de produto que cite `conversational-anchor-graph-v1`: `409 GRAPH_KIND_MIX` na abertura do build de produto.

## 4. Allowlist e denylist

Allowlist, famílias FDP-15 preservadas (AQ-03). Nenhuma quarta família.

| Capability | Família | side_effects | Reserva |
|---|---|---|---|
| `speech.transcribe` | TOOL | EXTERNAL | sim, uma por invocation, não por chunk |
| `speech.synthesize` | TOOL | EXTERNAL | sim, uma por invocation |
| `conversation.respond` | MODEL | EXTERNAL | sim, uma por turno de agente |
| `conversation.show_evidence` | TOOL | NONE | não reserva se `estimated_cost_minor` é 0 e descriptor confirma NONE |
| `conversation.invite` | comando interno do roteador | NONE | sem operation monetária |
| `conversation.issue_minutes` | efeito interno | INTERNAL | sem provider externo; sem prova fictícia |

Denylist da âncora, match por prefixo, `403 CAPABILITY_FORBIDDEN_ON_ANCHOR` antes de qualquer reserva:

`deploy.`, `release.`, `terminal.`, `shell.`, `vault.`, `secret.`, `credential.`, `ledger.reconcile`, `ledger.proof_ingest`, e os comandos `DeployRelease`, `MergeTask`, `StopBuild`, `InvokeCapability`.

O descriptor FDP-15 continua com `describe`, `health`, `invoke`, `cancel`, `receipt_query` = `SUPPORTED|ABSENT`. Campo aditivo proposto no descriptor, não uma família nova:

| Campo | Valores | Quem valida |
|---|---|---|
| media_plane | `LOCAL_PIPELINE` ou `PROVIDER_DUPLEX` | Policy Service contra o registry de host |
| execution_location | `LOCAL`, `SELF_HOSTED`, `EXTERNAL` | o registry, nunca o auto-relato do adapter |
| trust_boundary | `DEVICE`, `GATEWAY`, `PROVIDER` | o registry |

`PROVIDER_DUPLEX` significa um socket interno do fornecedor. Não funde `speech.transcribe` com `speech.synthesize`, não funde `operation_ref`, não pula a rechecagem de egress. Os dois planos emitem os mesmos eventos de `cmp.media.duplex.v1`.

## 5. Teto único sem segundo ledger (AQ-10)

Não se cria `conversation_ledger`, não se atribui `pending_actual_minor` por regra nova, não se insere `pending_provider_cost` por caminho novo.

Os contadores do Build âncora são as colunas já definidas em FDP-16A §3.1. A reserva usa a mesma transação, o mesmo movimento único e a mesma prova. Isso é o mesmo ledger, não um livro paralelo.

Não se cobra a mesma intenção também num Build de produto: a constraint aditiva de `(project_id, operation_ref, capability)` e o oráculo de task misturada recusam o segundo débito.

Não há número de teto de projeto além do `budget_limit_minor` da âncora. AQ-10 aprovou a fórmula `spent + reserved <= limit` e a unicidade do protocolo. Não aprovou um inteiro compartilhado entre sessões. Inventar esse inteiro aqui seria decisão nova. Fica em questão aberta, sem reopen da AQ.

## 6. Migração, compatibilidade e rollback

**Não executada.** DDL abaixo é especificação.

Ordem aditiva:

1. `build.kind` default `PRODUCT`.
2. Ampliar o check de `build.status` com `SESSION_ACTIVE` e `SESSION_CLOSED`, válidos só com kind âncora.
3. `task.execution_domain` default `BUILD_DAG`; `session_id`; `session_status`; status aditivos só no domínio novo.
4. Índice único parcial de sessão aberta.
5. Checks de dependência vazia, kind coerente e proibição de aresta cruzada.
6. Valor `conversation_router` no check de `actor_class` **somente** para comandos deste delta. `InvokeCapability` continua recusando qualquer ator que não seja `coding_engine`.
7. Catálogo ganha `OpenConversationalAnchor`, `CloseConversationalAnchor`, `SweepOrphanConversationalAnchor`, `ReserveConversationalCapability`.
8. Lista de capturer proibido ganha `conversation_router`.
9. Constraint única aditiva das capabilities conversacionais.

Compatibilidade:

- Linha antiga sem as colunas novas, após default, continua válida.
- Comando histórico não aceita o ator novo.
- Leitor que não entende `SESSION_ACTIVE` nega. Não promove a build de produto.
- Nenhuma operation de produto muda de task.

Rollback:

- Recusado se existir Build `CONVERSATIONAL_ANCHOR` ou operation não terminal apontando para task conversacional.
- Se não existir, as colunas e os valores de enum podem ser retirados.
- Rollback nunca apaga movement, proof ou `pending_provider_cost`.

## 7. O que continua igual no dinheiro

Dispatch, timeout, HELD, CONFLICT, late evidence, dual control de `PROVEN_RECEIPT`, `40001` sem segundo efeito, e a frase “não redespachar em incerteza” permanecem FDP-16A §8A–§8C e CMP-02 v0.3 §9. Este delta não os reescreve. A máquina que liga cancelamento de voz a esses status está em CMP-FD-03.

Até uma Change Decision humana em separado, e até o Codex aceitar este texto, **nenhuma operação paga conversacional está tecnicamente aprovada.**
