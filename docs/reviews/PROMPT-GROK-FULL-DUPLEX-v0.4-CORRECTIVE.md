# PROMPT OFICIAL — GROK BUILDER — FULL-DUPLEX v0.4 CORRECTIVE

**Repositório:** https://github.com/otavioegal/ia-os-forge-round5
**SHA documental auditado:** `2fe0b0b2b75f2fc1430f639839e2d29d563f6dcb`
**Parecer Codex independente:** `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.3-2026-10-14.md`
**Veredito:** **FAIL DOCUMENT-ONLY**. Não é autorização de implementação.

## Mandato e fontes

Leia integralmente o parecer acima, o prompt corretivo v0.3, os 14 arquivos de `docs/planning/conversational-full-duplex-v0.3/`, a Ata Founder, ADR AQ-07, FDP-16A v1.7, FDP-15 histórico, CMP v0.3 e as versões full-duplex anteriores pertinentes. Não aceite o relatório do próprio Grok como prova. Corrija **somente em pacote aditivo v0.4** em `docs/planning/conversational-full-duplex-v0.4/`, sem modificar baseline v1.7, CMP v0.3, v0.1/v0.2/v0.3, ata, ADR e pareceres.

O Codex fechou documentalmente HIGH-01, HIGH-02, NEW-HIGH-01, NEW-HIGH-02, NEW-MEDIUM-02 e MEDIUM-01..05. Preserve integralmente esses invariantes. Ainda **PARTIAL**: HIGH-03, NEW-HIGH-03, NEW-MEDIUM-01, NEW-MEDIUM-03 e LOW-01. Novos **OPEN**: NEW-HIGH-04 e NEW-MEDIUM-04/05/06. Não declare nenhum fechamento unilateral.

## Reparos obrigatórios, em ordem de risco

### 1. NEW-HIGH-04 — settlement pode ultrapassar a fatia da sessão
Em `CMP-FD-01 v0.3:29-36,151-155`, só o estimate é limitado por `session_slice_minor`. FDP-16A v1.7 `:322-324` permite actual > estimate se houver headroom no Build pai. Portanto uma sessão com fatia 50, estimate 40 e actual 70 pode violar a invariante de sessão mesmo quando o root ainda tem saldo.

Especifique delta normativo explícito no mesmo protocolo financeiro FDP-16A, sem editar a fonte histórica: no settlement de Operation conversacional, sob **Build FOR UPDATE primeiro**, recalcule `settled_task + held_task_restante - estimate_operacao + actual <= session_slice_minor` e também o teto do root. Trate reconciliação, prova tardia, receipt contraditório, actual > estimate, retries, crash e 40001 sem segundo movimento. Se não couber na fatia, preserve reserva HELD / reconciliação e pending_provider_cost conforme v1.7; **não** ajuste silenciosamente a fatia, não descarte prova, não duplique reserva, não invente refund. Declare como `session_slice_minor` evolui quando a sessão fecha e ainda há provider proof pendente. Crie oráculo adversarial com estimate 40, actual 70, slice 50, root com headroom: **zero settlement** até resolução autorizada; e um caso em que actual cabe na fatia.

### 2. NEW-HIGH-03 — tenant scope completo até Reservation
`CMP-FD-01 v0.3:116-140` valida canal/sessão/Build/Task, mas Operation/Reservation ainda podem ser consultadas só por id; `CMP-FD-13:13-15` não tem FK composta Reservation→Operation. Defina todas as constraints e predicados de consulta/lock: `(organization_id, project_id, operation_id)` em Reservation referenciando Operation, e cadeia channel→session→root Build→Task→Operation→Reservation. Não confie em IDs globais ou somente RLS. Negue replay, ingest e lookup de foreign tenant com resposta 404 opaca, zero escrita, zero contador, sem vazamento de existência e sem tocar lock de outro tenant. Expanda O37 com subcasos adversariais de **cada elo** (session, Build, Task, Operation, Reservation), mesmo UUID em org distinta e escopo cruzado.

### 3. NEW-MEDIUM-01 — replay idempotente deve preceder CAS
Na transação `CMP-FD-01 v0.3:147-155`, D3 compara versões antes de D7 verificar `command_id`; replay comprometido com versão antiga retorna 409, contradizendo `200 IDEMPOTENT_REPLAY`. Depois do Build lock e validação de escopo, faça **lookup durável de command_id/digest antes do CAS**. Mesmo digest comprometido → retornar outcome anterior mesmo com versões antigas, sem novo efeito; mesmo ID/digest diferente → `409 IDEMPOTENCY_KEY_REUSED`; comando novo com versão antiga → `409 VERSION_CONFLICT`. Especifique qual registro fica durável, retenção, canonical digest e atomicidade com audit/outbox. Oráculos de replay após commit, crash, versões avançadas e concorrência de IDs distintos.

### 4. HIGH-03 — schema de mídia e handshake ainda incompletos
`CMP-FD-02 v0.3:38-55` exige `selected_media_contract` e `selected_speech_contract` mas não modela `HELLO_ACK` de rejeição; `SPEECH_UNSUPPORTED_VERSION` aparece sem taxonomia correspondente. Especifique união fechada de `HELLO`, `HELLO_ACK_SUCCESS`, `HELLO_ACK_ERROR`, com error code, version negotiation, auth, session allocation e **zero side effects em erro**. Defina ACK `ack_of_sequence` não futuro, dentro do stream e window, replay idêntico, duplicado, fora de escopo, gaps e erro. Defina payload tipado e invariantes para todos os event_types e complete crosswalk `cmp.speech.v0`, sem regressão no `PLAYBACK_SPAN` ou seis timestamps.

### 5. NEW-MEDIUM-04 — campos obrigatórios ausentes de observation
`CMP-FD-04 v0.3:24-31` afirma `consent_stop_deadline_ns` em `observation`, e `CMP-FD-06:9-17` afirma `observation_tolerance_ns`; `CMP-FD-02:221-247` rejeita esses campos por ser schema fechado. Corrija de forma normativa: inclua-os no schema com tipo, nulabilidade, provenance, event_type permitido e invariantes, **ou** retire as afirmações e vincule-os a configuração/policy fora do envelope com crosswalk explícito. Não deixe campo exigido e proibido simultaneamente. Oráculo negativo para campo ilegal/ausente.

### 6. NEW-MEDIUM-05 — digest e fixture reproduzíveis
Os oito eventos FX-01 estão embutidos em Markdown e contêm digests não verificados. Publique **arquivo JSON separado** com os oito eventos; especifique canonicalização UTF-8 determinística (ordenação de chaves, null, inteiros, strings, exclusão de event_digest, bytes/ref). Forneça vetor de teste `canonical_bytes → sha256` por evento e um verificador offline pequeno, sem dependências externas nem acesso a dados reais. Execute, se permitido, **apenas a checagem estática de fixture/documentação**, identificando claramente comando, versão, hash e saída; não confunda com testes de produto. Se não executar, registre NOT RUN sem afirmar reprodutibilidade. Negativos: alteração de um byte/campo/null/digest; `EVENT_ID_REUSED` com digest divergente.

### 7. NEW-MEDIUM-03 — AEC/VAD deve receber eco + fala humana somados
`CMP-FD-07 v0.3:609-631` usa `mic[i]=16000` no trecho humano, **substituindo** o eco. Mude para mistura aditiva real, por exemplo `mic[i]=clamp(reference[i-480]//2 + human[i])`, com sinal de referência, componente humano, sobreposição, saturação, tolerâncias de erro e expectativa de preservar a fala enquanto elimina eco. A saída `aec_decision` é resultado do sistema, não fato de entrada. Oráculos falsificáveis para fala humana + eco simultâneos, eco puro, falso positivo e falso negativo; nenhuma reabertura de microfone sem consentimento.

### 8. NEW-MEDIUM-06 — unicidade de sessão tenant-composta
`CMP-FD-01 v0.3:84-97` e `CMP-FD-13:13` dizem uma Task aberta por `session_id` sem definir se índice é global. Faça unique parcial explícito por `(organization_id, project_id, session_id)` com predicado de sessão aberta e sem vazamento por erro de conflito. Oráculo: mesmo session UUID em orgs diferentes não colide nem compartilha Task; dentro da mesma org/projeto não abre duplicata.

### 9. LOW-01 — owner/effort/DoR
As sete histórias continuam com pessoa PENDING, effort UNSTATED, DoR NOT MET. **Não invente responsável ou estimativa**. Mantenha papéis propostos, checklist de atribuição humana e gate separado. Se for impossível fechar sem ato humano, registre como OPEN BLOCKING DoR e deixe pendente; não mascare o problema.

## Invariantes de governança

APPROVED pelo Founder: AQ-01, AQ-02, AQ-03, AQ-05, AQ-06, AQ-07, AQ-08, AQ-10, AQ-11. DEFERRED/UNDECIDED: AQ-04, AQ-09, AQ-12. AQ-07 exige full-duplex natural desde o MVP, não half-duplex como equivalente. Não escolha provider, não crie ledger paralelo, não confunda Codex do Conselho (read-only) com auditor Codex CLI independente. CMP-O-28 permanece independente de CMP-FD-O28. FDP-14, FDP-15, incorporação/consolidação da baseline e BUILD-00 seguem PENDING. Os 91 oráculos v1.7, 36 CMP-O e 40 CMP-FD-O permanecem NOT RUN; novos também NOT RUN.

## Entrega e gate

Criar pasta aditiva `docs/planning/conversational-full-duplex-v0.4/` com índice/status, contratos delta de ledger/settlement/tenant/CAS, schema de mídia, lifecycle, security, UX, observability, fixture JSON + vetores de digest, oráculos adversariais novos (IDs sem colisão), matriz de rastreabilidade, migration/rollback, change report, finding disposition e consistency report. Checar todos os cross-references e não truncar arquivos. Identificar em cada finding: causa, texto corrigido, path:line, fixture negativa, status CANDIDATE (nunca self-PASS).

**Proibido:** editar v1.7 ou fontes auditadas, migration real, deploy, provider real/pago, mudanças de credenciais, testes operacionais, gastos, integração na baseline, BUILD-00. Commit/push no GitHub e informar SHA completo. Pedir nova auditoria Codex independente **somente leitura** no SHA fixo. Não reabrir as nove decisões humanas nem fingir fechamento de finding.
