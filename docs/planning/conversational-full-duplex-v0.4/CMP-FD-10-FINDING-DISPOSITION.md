# CMP-FD-10 v0.4 — Disposição dos findings

**Estado de cada linha abaixo:** CANDIDATE FOR CODEX REVIEW, salvo LOW-01, que permanece OPEN BLOCKING DoR. O autor não escreve CLOSED e não escreve PASS.

Linhas citadas são as desta pasta no momento em que o texto foi escrito. O auditor relê o SHA publicado.

## NEW-HIGH-04

- Causa: na v0.3 a fatia limitava o estimate. FDP-16A v1.7 `:322-324` ainda permite actual maior se o Build tem headroom. Fatia 50, estimate 40, actual 70, root folgado, liquidaria 70.
- Texto: CMP-FD-01, seção 2, a partir da linha 18. Checagem `S + H - E + A <= L` e a checagem de root, ambas depois do `SELECT` do Build `FOR UPDATE` (linha 43). Passo 12, linha 53: se só a fatia falha, zero settlement, reservation `HELD`, operation `RECONCILING`, um `pending_provider_cost` razão `SESSION_SLICE`, retorno `409 SESSION_SLICE_EXCEEDED`. L não muda. Prova não é apagada. Não há segunda reservation nem refund.
- Resolução: `AmendSessionSlice`, linhas 76-83, humano, não liquida. Fecho com pending: linhas 85-87, status `ORPHAN_HELD` ou `CLOSING`, fatia permanece na soma.
- Exemplo: linhas 63-71. A = 70 não move. A = 45 move uma vez.
- Negativo: CMP-FD-O41 e CMP-FD-O42, CMP-FD-07 linhas 49 e 59. NOT RUN.
- Status: CANDIDATE.

## NEW-HIGH-03

- Causa: predicados de canal, sessão, Build e Task não chegavam à Operation e à Reservation. Não havia FK composta.
- Texto: CMP-FD-01, seção 3, linhas 89-110. Reservation referencia `(organization_id, project_id, operation_id)`. Lookup estrangeiro: `404` com corpo `{"error_code":"NOT_FOUND","retryable":false,"terminal":true}`. Sem lock na linha do outro tenant, sem contador, sem vazamento.
- Migração especificada e não executada: CMP-FD-13 linhas 9-10.
- Negativo: O37 subcasos S, B, T, O, R e X, CMP-FD-07 linhas 65-80. NOT RUN.
- Status: CANDIDATE.

## NEW-MEDIUM-01

- Causa: a v0.3 comparava version antes de olhar `command_id`. Replay já cometido com version velha virava `409`.
- Texto: CMP-FD-01 linha 48, passo 7 antes do passo 8. Registro em CMP-FD-01:114-139. Tabela `forge.command_commit`, digest canônico incluindo as versions esperadas, mesmo commit de audit e outbox. Replay não entra no CAS. Chave reusada com outro digest: `409 IDEMPOTENCY_KEY_REUSED`. Comando novo com version velha: `409 VERSION_CONFLICT`, sem linha de commit. Crash e `40001` não deixam linha e não duplicam movimento.
- Negativo: O43, O44, O45, CMP-FD-07 linhas 88, 98 e 106. NOT RUN.
- Status: CANDIDATE.

## HIGH-03

- Causa: o preâmbulo exigia contratos selecionados e não modelava rejeição. `SPEECH_UNSUPPORTED_VERSION` não tinha lugar na união. ACK não tinha futuro, escopo nem regressão.
- Texto: CMP-FD-02. `HELLO` linhas 13-29, zero efeito de sessão. `HELLO_ACK_SUCCESS` linhas 31-48, único preâmbulo que aloca streams, ainda sem microfone e sem reserva. `HELLO_ACK_ERROR` linhas 50-77, inclusive `SPEECH_UNSUPPORTED_VERSION` na linha 71, campos selecionados proibidos, zero efeito. ACK linhas 96-114: `ACK_FUTURE`, `ACK_SCOPE_MISMATCH`, `ACK_REGRESSION`, replay, `EVENT_ID_REUSED`, `STREAM_GAP`. Seis carimbos e `PLAYBACK_SPAN` nas linhas 86-87, sem regressão do que o Codex fechou em NEW-MEDIUM-02. Payloads de todos os `event_type` na seção 7, a partir da linha 153. Crosswalk mínimo nas linhas 138-149 e crosswalk completo na seção 7.6.
- Negativo: O46 e O47, CMP-FD-07 linhas 118 e 128. O39 para digest divergente, linha 41. NOT RUN.
- Status: CANDIDATE. O autor não declara o contrato de mídia aprovado.

## NEW-MEDIUM-04

- Causa: a v0.3 dizia que `consent_stop_deadline_ns` e `observation_tolerance_ns` estavam em `observation`, e o schema fechado os rejeitava.
- Escolha desta pasta: retirá-los do envelope, não acrescentá-los ao schema. CMP-FD-02 linhas 92 e 129-136. CMP-FD-04 linha 19. CMP-FD-06 linha 12. Valor null, `PENDING CALIBRATION`. Presença no evento: `422 UNKNOWN_FIELD`. O corte de consentimento não depende do número. `overlap_epsilon_ns = 0` continua constante da fixture.
- Negativo: O48, CMP-FD-07 linhas 134-142. NOT RUN.
- Status: CANDIDATE. MEDIUM-02 e MEDIUM-05 não são reabertos.

## NEW-MEDIUM-05

- Causa: os oito eventos estavam no Markdown, com digest não reproduzível por artefato separado.
- Texto: `fixtures/CMP-FD-FX-01-events.json`, `fixtures/CMP-FD-FX-01-digest-vectors.json`, `tools/check_fd_fx01_digests.py`. Algoritmo em CMP-FD-02 linhas 116-127: remover `event_digest`, JSON UTF-8, chaves ordenadas, separadores sem espaço, SHA-256 hex.
- Checagem estática: registrada em CMP-FD-12. Saída `PASS_FIXTURE_ONLY`. Isso não executa O39 e não é PASS do pacote.
- Negativo: O39, CMP-FD-07 linha 41. Um byte, um campo, um null ou o digest armazenado divergente. NOT RUN como teste de produto.
- Status: CANDIDATE.

## NEW-MEDIUM-03

- Causa: no trecho humano a v0.3 escrevia `mic[i] = 16000` e apagava o eco.
- Texto: CMP-FD-07 linhas 144-187. `mic[i] = clamp(echo[i] + human[i])`, eco = `reference[i-480] // 2` a partir da amostra 480, humano 16000 em 1000..1198 e 32000 em 1199, saturação int16. `aec_decision` é saída. Microfone fechado não reabre. `capture_generation` não sobe por causa do AEC.
- Negativo: O28 reescrito (fala e eco juntos), O51 (eco puro), O52 (saída que dropa ou fecha o microfone é reprovada). NOT RUN.
- Status: CANDIDATE.

## NEW-MEDIUM-06

- Causa: “uma task por session_id” não dizia se o índice era global. Conflito global vazaria outro tenant.
- Texto: CMP-FD-01 linhas 145-151. CMP-FD-13 linha 11. Unique parcial `(organization_id, project_id, session_id)` para `OPEN`, `CLOSING`, `ORPHAN_HELD`. Sem unique só em `session_id`. `409 ANCHOR_EXISTS` só depois da linha deste tenant.
- Negativo: O49 e O50, CMP-FD-07 linhas 195 e 203. NOT RUN.
- Status: CANDIDATE.

## LOW-01

- Causa: sete histórias sem pessoa e sem effort. Inventar os dois seria máscara.
- Texto: CMP-FD-07 linhas 7-23. Papéis propostos continuam. Pessoa PENDING. Effort UNSTATED. DoR NOT MET. Checklist desmarcada. Sem ato humano do Founder o estado é OPEN BLOCKING DoR.
- Negativo: marcar Ready sem pessoa e effort. Não executado.
- Status: OPEN BLOCKING DoR. Não é CANDIDATE de fechamento.

## Já fechados pelo Codex, não redispostos

HIGH-01, HIGH-02, NEW-HIGH-01, NEW-HIGH-02, NEW-MEDIUM-02, MEDIUM-01, MEDIUM-02, MEDIUM-03, MEDIUM-04, MEDIUM-05. Esta página não os reabre e não pede para o autor os “confirmar”. A preservação está em CMP-FD-01 seções 1, CMP-FD-02 seção 2, CMP-FD-03, CMP-FD-04, CMP-FD-05 e CMP-FD-06.
