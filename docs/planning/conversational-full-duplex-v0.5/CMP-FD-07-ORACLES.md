# CMP-FD-07 v0.5 — Oráculos

**Nenhum oráculo foi executado.** Evidence ABSENT. NOT RUN. Não é PASS.
**IDs novos:** CMP-FD-O53..O70. Não colidem com O01..O52 nem com CMP-O-01..36.
**CMP-O-28** continua o oráculo de independência. **CMP-FD-O28** continua AEC. Um não substitui o outro.

## 1. LOW-01 — OPEN BLOCKING DoR

Sete histórias. Pessoa PENDING. Effort UNSTATED. DoR NOT MET. O autor não nomeia ninguém e não estima.

| ID | Papel proposto | Pessoa | Effort | DoR |
|---|---|---|---|---|
| CMP-FD-S01 | Conversational Product Spec Owner | PENDING | UNSTATED | NOT MET |
| CMP-FD-S02 | Conversational Product Spec Owner | PENDING | UNSTATED | NOT MET |
| CMP-FD-S03 | Conversational Product Spec Owner | PENDING | UNSTATED | NOT MET |
| CMP-FD-S04 | Privacy Spec Owner | PENDING | UNSTATED | NOT MET |
| CMP-FD-S05 | Ledger Spec Owner | PENDING | UNSTATED | NOT MET |
| CMP-FD-S06 | Privacy Spec Owner | PENDING | UNSTATED | NOT MET |
| CMP-FD-S07 | Policy Spec Owner | PENDING | UNSTATED | NOT MET |

Sem ato humano do Founder que nomeie a pessoa, e sem effort registrado por essa pessoa, o estado é **OPEN BLOCKING DoR**. Papel proposto não remove o bloqueio. Marcar Ready sem pessoa e effort é falha de governança. Isso também não foi executado.

## 2. Settlement — o apply entra na fatia

Estado comum, ainda não executado: L=50, E=40, S=0, H=40, spent=0, reserved=40, teto do root=100. Prova RECEIPT conclusiva.

### CMP-FD-O41 — RecordReceipt, actual não cabe

A=70. PASS do oráculo: zero movimento; spent=0; reserved=40; L=50; operation `RECONCILING`; um pending `SESSION_SLICE` de 70; `409 SESSION_SLICE_EXCEEDED`.

FAIL: spent=70, ou L elevado, ou prova apagada. NOT RUN.

### CMP-FD-O42 — RecordReceipt, actual cabe

A=45. PASS: um movimento; spent=45; reserved=0; L=50. NOT RUN.

### CMP-FD-O58 — ApplyAuthorizedReconciliation não cabe

Operation já `BLOCKED_RECONCILIATION`. Autorização `AUTHORIZED` não consumida. Decisão `PROVEN_RECEIPT`. A=70. O root comportaria 70.

PASS: zero movimento; spent=0; reserved=40; L=50; operation continua `BLOCKED_RECONCILIATION`; reservation `HELD`; autorização continua `AUTHORIZED` e não `APPLIED`; um pending `SESSION_SLICE` valor 70; `409 SESSION_SLICE_EXCEEDED`.

FAIL: spent=70, autorização consumida, L elevado para 70, ou pending apagado. NOT RUN.

### CMP-FD-O59 — Apply em que o actual cabe

Mesmo estado, A=45.

PASS: um `SETTLEMENT`; spent=45; reserved=0; L=50; autorização `APPLIED`; `settles_proof_id` igual ao proof. NOT RUN.

### CMP-FD-O60 — corrida Amend contra Apply

Os dois comandos pedem o mesmo Build `FOR UPDATE` antes de ler L. Estado inicial L=50, A=70.

PASS, só estes desfechos: o amend commita L=80 e o apply com version antiga toma `409 VERSION_CONFLICT` sem movimento; o retry do apply, com a version nova, liquida uma vez porque 70 cabe em 80. Ou o apply commita primeiro o caminho sem liquidação, autorização não consumida, e o amend não liquida.

FAIL: dois settlements; ou settlement de 70 com L ainda 50; ou leitura de headroom antes do lock. NOT RUN.

### CMP-FD-O61 — replay, crash e 40001 no apply

PASS: `command_id` já cometido no caminho de O58 volta `transport_status=200`, `replay=true`, `original_outcome_code=409`, sem segundo pending. Crash ou `40001` antes do commit não deixa linha. O retry não duplica movimento nem pending. NOT RUN.

### CMP-FD-O62 — prova tardia

Depois de um `SETTLEMENT` já cometido, uma prova contraditória não cria segundo movimento, não devolve `spent`, não reescreve L e não inventa refund. NOT RUN.

### CMP-FD-O63 — sessão CLOSING

`session_status=CLOSING`, operation `BLOCKED_RECONCILIATION`, pending `SESSION_SLICE` sem movimento correlato. PASS: a transição para `CLOSED` é negada; o status permanece `CLOSING`; L continua na soma; o fecho não liquida. A coluna lida é `session_status`, não `task.status`. NOT RUN.

### CMP-FD-O64 — correlação sem update

Depois de O58, um amend eleva L para 80 e um apply novo liquida. PASS: a linha pending `SESSION_SLICE` continua existindo, sem update e sem delete; existe um movimento com `settles_proof_id` igual; a projeção marca resolução histórica. FAIL: `UPDATE` ou `DELETE` no pending, ou refund. NOT RUN.

## 3. Tenant preexistente

### CMP-FD-O55

Reservation sem Operation correspondente. PASS da spec, não executada: a contagem de órfãos é maior que zero, a transação faz `ROLLBACK`, nenhuma org é inventada, a flag segue desligada. NOT RUN.

### CMP-FD-O56

Operation já existente na org B. Canal da org A apresenta esse id em ingest. PASS: `404` opaco, zero prova na linha B, zero lock em B, zero contador em B. NOT RUN.

### CMP-FD-O57

Reservation já existente na org B. Lookup da org A. PASS: o mesmo `404`, sem `SELECT FOR UPDATE` em B. NOT RUN.

### CMP-FD-O70

`command_id` já cometido na org B, apresentado no canal da org A. PASS: não retorna o outcome de B, não trava a linha de B, não revela que o commit existe. NOT RUN.

O37 e os subcasos S, B, T, O, R, X da v0.4 continuam NOT RUN.

## 4. ACK e preâmbulo

Fixture estática: `fixtures/CMP-FD-FX-02-ack.json`. A checagem de forma não executa estes oráculos.

### CMP-FD-O65

Evento `CONTROL` com `ack_stream_id` do input e `ack_of_sequence=2`, emitted high-water do input igual a 2, peer high-water 0. PASS: ack aceito; a sequence do control não é tratada como a sequence reconhecida; zero dinheiro; microfone não abre. NOT RUN.

### CMP-FD-O66

`ack_of_sequence=9` com emitted high-water 2. PASS: `422 ACK_FUTURE`, high-water intacto. Ack menor que o peer high-water: `422 ACK_REGRESSION`. Ack igual ao peer high-water: zero efeito novo. Stream fora dos três alocados: `422 ACK_STREAM_UNALLOCATED`, corpo opaco, mesmo se o UUID existir em outra sessão. NOT RUN.

### CMP-FD-O67

`HELLO` com `principal_ref` diferente do principal autenticado. PASS: `HELLO_ACK_ERROR` com `PREAMBLE_AUTH`. Zero sessão, zero stream, zero task, zero reservation, microfone fechado. FAIL: abrir sessão ou cair para half-duplex. NOT RUN.

## 5. AEC — conta corrigida

Entradas. `PCM_S16LE`, 48000 Hz, um canal. Sem campo `echo`. `reference` tem 960 amostras, índices 0..959: `8000` se `(i // 40) % 2 == 0`, senão `-8000`.

- `echo[i] = 0` se i < 480; senão `reference[i - 480] // 2`.
- `human[i] = 0` fora de 1000..1199.
- Em 1000..1199, `human[i] = 16000`, exceto `human[1159] = 32000` e `human[1199] = 32000`.
- `mic[i] = clamp(echo[i] + human[i])` no int16 fechado, de `-32768` a `32767`.

Contas desta fixture, não medidas de produto:

| i | echo | human | soma | mic | classe |
|---|---|---|---|---|---|
| 480 | 4000 | 0 | 4000 | 4000 | eco puro |
| 1000 | -4000 | 16000 | 12000 | 12000 | recuperável, eco negativo |
| 1040 | 4000 | 16000 | 20000 | 20000 | recuperável, eco positivo |
| 1159 | 4000 | 32000 | 36000 | 32767 | saturação irrecuperável |
| 1199 | -4000 | 32000 | 28000 | 28000 | recuperável, sem saturação |

`i=1199` não satura. A v0.4 errou ao dizer 32767 nesse índice. `i=1159` satura. `|32767 - 32000| = 767`, então a distância até o humano não separa “eco removido” de “mic saturado passou direto”. Esse índice não entra no critério de distância.

`aec_decision` e `forwarded_pcm` são saída.

### CMP-FD-O28

PASS futuro, todas as linhas:

1. `mic_open` não muda. O AEC não abre microfone fechado e não incrementa `capture_generation`.
2. Amostras recuperáveis com humano diferente de zero, inclusive 1000, 1040 e 1199: `forwarded_pcm` difere do humano ideal de no máximo `1000` e difere de `mic` em mais de `1000`.
3. Em 480..999, `forwarded_pcm` difere de 0 em no máximo `400`.
4. A amostra 1159 é `UNRECOVERABLE_SATURATION`. Não conta como fala preservada. `mic` é 32767. A soma pré-clamp 36000 não é exigida como amostra int16. Saída que marque essa amostra como limpa falha este item.
5. O STT recebe `forwarded_pcm` nas amostras recuperáveis, não o `mic` bruto.

Os limites `1000` e `400` são `FIXTURE_CONSTANT`. Não são SLA. NOT RUN.

### CMP-FD-O51 — eco puro

`human[i]=0`. PASS: `forwarded` difere de 0 em no máximo `400`; `mic_open` não muda; nenhum turno humano abre. NOT RUN.

### CMP-FD-O52 — falso positivo

Saída vazia, `aec_decision=DROPPED`, ou `mic_open` false. PASS do oráculo: a saída é reprovada. O microfone consentido não fecha por causa do eco. NOT RUN.

### CMP-FD-O53 — eco preservado

`forwarded_pcm` igual a `mic` nas amostras recuperáveis 1000, 1040 e 1199. O índice 1159 não entra, porque o mic saturado não separa eco de fala. PASS do oráculo: a saída é reprovada. NOT RUN.

### CMP-FD-O54 — fala suprimida

`forwarded_pcm` a mais de `1000` do humano nas amostras recuperáveis, inclusive zerado onde o humano é 16000. PASS do oráculo: a saída é reprovada. NOT RUN.

## 6. Sessão

### CMP-FD-O68

Antes do índice, duas tasks `CONVERSATION` com o mesmo `(organization_id, project_id, session_id)` e `session_status=OPEN`. PASS da spec: a contagem histórica aborta, o índice não é criado, nenhuma task é apagada. NOT RUN.

O mesmo `session_id` em outra org, sem duplicata local: as duas aberturas sucedem. Não há `409` cruzado. NOT RUN.

### CMP-FD-O50

Segunda abertura no mesmo org, projeto e `session_id`, status ainda aberto. PASS: `409 ANCHOR_EXISTS`. Uma task. NOT RUN.

## 7. Replay de transporte

### CMP-FD-O69

Comando já cometido com `original_outcome_code=409`. PASS: HTTP `transport_status=200`, `replay=true`, o corpo traz o 409 original, o CAS não corre. FAIL: HTTP 409 nesse replay, ou um segundo efeito. NOT RUN.

## 8. O que continua NOT RUN

O01..O52 que esta página não reescreve continuam com o critério da v0.4, subordinados a esta v0.5 quando falam de fatia, apply, ACK ou sessão. Não foram executados. Os 91 oráculos v1.7 e os 36 CMP-O também não. O28 da v0.4 fica substituído pelo texto desta seção 5 para a amostra de saturação; o id não muda; a execução continua NOT RUN.
