# Fechamento dos findings — Codex Round 7 para baseline v1.5
Estado da entrega: ROUND 8 — CANDIDATE FOR CODEX REVIEW.
Este registro não é o parecer do Codex. Não declara PASS. Nenhum teste de produto foi executado. Nenhuma aprovação foi inferida.
A serialização mecânica e a separação humano/system que o Codex marcou como parcialmente fechadas no Round 7 foram mantidas. HIGH-02 a HIGH-06 e M01 a M05 continuam fora desta rodada.

| Campo | HIGH-01 / NEW-HIGH-08 |
|---|---|
| ID | Provas financeiras contraditórias. O lock não é a verdade. |
| Situação no parecer | HIGH-01 PARCIALMENTE FECHADO. NEW-HIGH-08 ABERTO. LEDGER-08 aceitava SETTLED ou RELEASED conforme quem pegasse o lock, inclusive um receipt verificado de 30 contra uma liberação. |
| Causa-raiz | A frase da v1.4 dizia que o vencedor era a transação que adquirisse o lock da operação primeiro, e a tabela tratava receipt contra release como uma corrida em que qualquer um dos dois terminais era aceitável. |
| Correção | FDP-16A v1.5. A ordem Build, Operation, Reservation, autorização por último continua, só como exclusão. Depois do lock, a seção 8A.3 decide. Receipt conclusivo e no-effect conclusivo, ou dois receipts com valores diferentes, não geram movement: as duas provas ficam, `reconciliation_state` vai a CONFLICT, a reserva continua HELD, `spent` não muda, `pending_actual_minor` guarda o valor do receipt, e os dois comandos recebem 409 PROOF_CONFLICT. Receipt conclusivo contra no-effect inconclusivo liquida se couber no limite; a liberação recebe 409 RECEIPT_PRECEDES_RELEASE. Só um no-effect conclusivo, sem receipt, libera uma vez. Prova tardia que contradiz um movement já gravado não apaga a prova, não cria segundo movement e não deixa um RELEASED definitivo enquanto o receipt conclusivo existir. Não há redespacho automático. |
| Arquivo | docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md |
| Evidência | A frase de que o lock não decide a prova está na linha 358. A ordem de lock está na linha 360. A releitura que aplica 8A.3 está nas linhas 368–375. A linha da corrida receipt contra no-effect está na linha 396. O custo pendente está nas linhas 98 e 401. A prova tardia está na linha 405. LEDGER-08 está na linha 69 da matriz v1.5 e falha se o resultado for RELEASED ou se depender de quem pegou o lock. LEDGER-13 está na linha 74. |
| Prova pedida | Com as duas provas VERIFIED antes da barreira, o estado fica BLOCKED_RECONCILIATION, spent 800, reserved 150, as duas provas permanecem, não há movement. Um receipt verificado de 30 dentro do limite não termina RELEASED. |
| Estado neste builder | CORRIGIDO NESTA CANDIDATA. Não é fechamento do Codex. |

| Campo | NEW-HIGH-07 / NEW-HIGH-09 |
|---|---|
| ID | Autenticidade, procedência e validação da evidência. Digest não é verdade. |
| Situação no parecer | NEW-HIGH-07 PARCIALMENTE FECHADO. NEW-HIGH-09 ABERTO. `evidence_ref` mais digest mais author class `security_operator` ainda deixava o operador escrever conteúdo, calcular o digest e usá-lo. |
| Causa-raiz | Não havia tipo de prova, serviço capturador, vínculo com operation/provider/valor/moeda, nem separação entre quem captura e quem aprova. |
| Correção | A única prova financeira é ProviderEffectProof, seção 8A.3. Quem captura é só `forge.provider_ingest`, capability `ledger.proof_ingest`, que não aprova, não confirma e não aplica. `ledger.reconcile` não insere prova. Approver, confirmer, coding_engine, adapter e reviewer não capturam. ATTESTED só com atestação realmente enviada e chave já registrada; sem chave a linha não é ATTESTED e o sistema não inventa assinatura. QUERY_CORROBORATED só com `receipt_query` SUPPORTED e leitura que casa operation, provider_ref, moeda e valor. Se a consulta é ABSENT, QUERY_CORROBORATED é proibido. O resto fica UNVERIFIED e não liquida, não libera e não autoriza. O aprovador não pode ser o capturador (422 EVIDENCE_SELF_AUTHORED). Sessão STRONG com frescor de planejamento `forge.ledger.session_max_age_ms` = 900000, que não é SLO. A política é do Policy Service, não do modelo. O humano só autoriza. O system só move dinheiro no Apply, depois da autorização válida. |
| Arquivo | docs/planning/FDP-16A-v1.5-EXECUTION-CONTRACTS.md; FDP-19A v1.5 F-015; matriz v1.5 |
| Evidência | Catálogo nas linhas 204–209. Seção 8A.2 nas linhas 409–423. Seção 8A.3 nas linhas 425–463. A proibição de inventar assinatura está na linha 453. LEDGER-11 linha 72. LEDGER-12 linha 73. F-015 linha 659. |
| Prova pedida | Texto com digest escrito pelo operador não autoriza. O capturador não é op_a. coding_engine recebe 403. Sem capability, evidence_ref trocado, sessão velha ou Apply humano não movem dinheiro. O único caminho positivo de no-effect usa prova ATTESTED capturada pelo ingest, e o gasto só muda no Apply do system. |
| Estado neste builder | CORRIGIDO NESTA CANDIDATA. Não é fechamento do Codex. |

| Campo | NEW-MEDIUM-10 |
|---|---|
| ID | Idempotência e duplicação de autorizações. |
| Situação no parecer | ABERTO. Faltavam replay de Approve/Confirm, segunda autorização igual, Confirm com evidence_ref diferente, perda de capability, segundo Apply e expiração. |
| Correção | O mesmo `command_id` em Approve, Confirm ou Apply devolve 200 IDEMPOTENT_REPLAY, uma linha de autorização e, no Apply, um movement e um audit de dinheiro. `command_id` novo com a mesma decisão e a mesma evidência devolve 409 AUTHORIZATION_EXISTS. Decisão ou `evidence_ref` diferentes devolvem 409 AUTHORIZATION_CONFLICT e não alteram a linha existente. Confirm sem capability devolve 403 CAPABILITY_NOT_GRANTED ou 403 CAPABILITY_REVOKED. evidence_ref diferente devolve 409 EVIDENCE_MISMATCH. Segundo Apply com `command_id` novo, depois do movement, devolve 409 ALREADY_SETTLED ou 409 ALREADY_RELEASED e não grava outro audit de dinheiro. `expires_at` é obrigatório. O default de planejamento é `forge.ledger.authorization_ttl_ms` = 86400000 e não é SLO. Expirada, a autorização fica EXPIRED, a operação continua BLOCKED_RECONCILIATION, a reserva continua HELD, e o Apply devolve 409 AUTHORIZATION_EXPIRED. |
| Arquivo | FDP-16A v1.5 seções 8A.1 e 8A.2; matriz LEDGER-14 |
| Evidência | Regras de replay na linha 420. TTL na linha 421. LEDGER-14 na linha 75 da matriz. |
| Estado neste builder | CORRIGIDO NESTA CANDIDATA. Não é fechamento do Codex. |

| Campo | NEW-MEDIUM-11 |
|---|---|
| ID | Custo real pendente quando actual supera a estimativa e o limite. |
| Situação no parecer | ABERTO. Não havia `pending_actual_minor` nem linha imutável para o receipt bloqueado. |
| Correção | `forge.pending_provider_cost` é append-only, uma linha por operação, com `proof_id`, valor, moeda e razão OVER_ESTIMATE ou CONFLICT. Não há update nem delete. `operation.pending_actual_minor` só espelha essa linha e não é gasto. Se a desigualdade falha, não há movement, `spent` fica 800, a reserva fica HELD, o status fica RECONCILING, e a linha guarda 200 no fixture de LEDGER-15. Uma liberação posterior devolve 409 PENDING_COST_HELD e não apaga a linha. |
| Arquivo | FDP-16A v1.5 seções 3.4, 8A e 8A.3; matriz LEDGER-15 |
| Evidência | Campo na linha 98. Inserção na linha 401. Tabela da prova na linha 461. LEDGER-15 na linha 76 da matriz. |
| Estado neste builder | CORRIGIDO NESTA CANDIDATA. Não é fechamento do Codex. |

| Campo | Q01 |
|---|---|
| ID | Hash ambíguo no change report da Rodada 7. |
| Situação no parecer | MINOR ABERTO. A linha 4 citava `4e57839…`, que é a baseline da Rodada 6. |
| Correção | Errata datada de 2026-10-13 acrescentada ao fim de `docs/reviews/ROUND7-CHANGE-REPORT-2026-10-13.md`. A frase original não foi apagada. O commit auditado no parecer Round 7 é `decef2809b61d3f1fe84bef74a5162d782cc6231`. |
| Estado neste builder | CORRIGIDO NESTA CANDIDATA. Não é fechamento do Codex. |

## O que permanece e não foi reescrito
Tuple de deploy, superfície de adapter, AIOX preferencial, HANDOFF-01, identidade, matrizes de Task, Attempt e Build, conjunto de READY_FOR_HUMAN_TEST e DoR operacional. FDP-18, FDP-18A e FDP-20 permanecem v1.3. Os 17 intents P0 não foram reescritos. Os 11 estados de Task continuam. FDP-14 e FDP-15 não foram aprovados.
