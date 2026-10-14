# CMP-FD-04 v0.2 — Política, consentimento e privacidade

**Estado:** PROPOSTA. Não executada.
**Achados alvo:** MEDIUM-02, MEDIUM-03. Fechamento não declarado.
**Decisões usadas, sem reopen:** AQ-05, AQ-06, AQ-08, AQ-11 APPROVED. AQ-04, AQ-09, AQ-12 UNDECIDED.

Policy Service decide. O modelo não concede capability, não escolhe classificação e não assina trust boundary.

## 1. Dois contadores de consentimento

| Contador | Incrementa quando | Não incrementa quando |
|---|---|---|
| consent_grant_epoch | grant explícito; revogação | pause, background, crash |
| capture_generation | grant; revogação; pause; stop; background; crash; resume explícito | chunk, ack, duck |

Os dois começam em 0. Microfone fechado. `START_SESSION` sem grant não incrementa e não abre dispositivo.

Todo chunk carrega os dois inteiros. O dispositivo e o gateway aplicam a mesma regra, de forma independente: aceitar só se `chunk.consent_grant_epoch == current.consent_grant_epoch` **e** `chunk.capture_generation == current.capture_generation`. Senão `422 CONSENT_EPOCH_STALE`, sem STT, sem egress.

A comparação é atômica no gateway em relação ao contador que ele guarda: um chunk lido com generation N não é aceito depois que o contador já é N+1, mesmo que tenha sido capturado antes no relógio de parede. Não há janela normativa de “chunk tardio ainda vale”.

## 2. Ordem normativa da revogação

1. O comando de revogação, pause, stop, background ou crash incrementa o que a tabela manda e põe `mic_open=false` **antes** de qualquer aceite novo.
2. Buffers locais ainda não encaminhados são descartados. Não são despejados no STT no caminho do fecho.
3. O dispositivo deve observar `mic_open=false` e emitir `CAPTURE_CLOSED`.
4. Bytes que **já** tinham `stt_forward_at_ns` não são “desenviados”. Fica registro `INGRESS_SEALED` com o `invocation_id`, a generation antiga e o último sequence aceito. O provider pode tê-los. Cancel é pedido. Dinheiro segue CMP-FD-03: incerteza permanece HELD.
5. Ack `CAPTURE_CLOSED` é obrigatório para sair de `STOPPING` ou `REVOKED`. Ausência do ack não mantém o microfone aberto; mantém a sessão em fecho e o indicador em desligado.
6. Não há prazo numérico de corte aceito. O campo `consent_stop_deadline_ns` existe na observação e o valor de aceite está `PENDING CALIBRATION`. O oráculo não usa milissegundo inventado. Usa os booleanos: dispositivo fechado, zero chunk novo aceito, zero invoke nova, buffer pós-comando vazio.

Background e crash **não** reaproveitam a generation anterior ao voltar. Retomar exige gesto explícito, que incrementa `capture_generation` de novo e revalida o grant. Grant revogado não volta por reconnect.

Reconnect no meio da revogação: o socket novo apresenta a generation corrente. Chunk do socket velho, com generation anterior, é rejeitado (CMP-FD-O22). Não há merge de buffers.

## 3. Quatro pontos de observação depois do corte

O oráculo CMP-FD-O20 olha os quatro, não um agregado “zero STT”:

| Ponto | Passa se |
|---|---|
| DEVICE | `mic_open=false` e nenhuma abertura nova até o próximo grant+gesto |
| TRANSPORT | zero chunk aceito pelo gateway com generation antiga ou posterior ao corte sem gesto |
| STT | zero `speech.transcribe` novo; invoke já despachada fica selada, sem segundo dispatch |
| BUFFER | zero byte pós-corte em buffer local encaminhável; descarte registrado |

CMP-FD-O06 continua sendo o caso “sessão nem começou”. O20 é o caso concorrente, com sessão que existia.

## 4. Trust boundary

O adapter declara `execution_location`. Essa declaração **não** é evidência. O registry de host, lido pela Policy Service, é a fonte. Se os dois divergem, o resultado é `403 TRUST_BOUNDARY_MISMATCH` e o egress não ocorre. Empate não existe: divergência nega. Não se “escolhe o mais restritivo e segue”. Seguir seria confiar num dos dois textos sem registrar o conflito. O evento de negação guarda os dois valores.

Cada egress recheca. Uma classificação aceita em `START_SESSION` não cobre o chunk seguinte. A rechecagem vale para:

- `speech.transcribe`
- `speech.synthesize`
- `conversation.respond`
- fallback de um plano local para um plano externo
- troca de projeto ou de interlocutor

`START_SESSION` guarda a classe inicial só como fato de abertura, não como capability durável.

## 5. Matriz de egress

Default de conteúdo derivado de projeto: `INTERNAL`, nunca `PUBLIC` (AQ-05). Sem linha de allowlist, externo é negado para `INTERNAL`.

| Classe | LOCAL | SELF_HOSTED no registry | EXTERNAL speech | EXTERNAL model | Fallback local → externo |
|---|---|---|---|---|---|
| PUBLIC | permitir se grant | permitir se o id está na allowlist | permitir se grant e id allowlisted | idem | nova decisão; não herda a anterior |
| INTERNAL | permitir se grant | permitir se allowlist | negar sem linha explícita de allowlist para aquele `provider_id` | igual | se o destino não está permitido, negar e degradar a texto |
| CONFIDENTIAL | permitir se grant | permitir só se registry diz SELF_HOSTED e a policy nomeia o id | negar | negar | negar; não enviar o buffer |
| RESTRICTED | permitir se grant e a policy local nomeia o destino | negar salvo linha futura que este pacote **não** cria | negar | negar | negar |

AQ-05 falou de speech externo para CONFIDENTIAL e RESTRICTED. A coluna de modelo externo nessas duas classes também nasce negada, para o egress não ser um desvio. Isso não escolhe fornecedor (AQ-04). Uma allowlist vazia é o default. Preencher a allowlist é configuração futura, não esta ata.

Mudança de classe no meio da sessão, por exemplo o turno passa a citar material CONFIDENTIAL:

1. Antes do próximo egress, rechecar.
2. Buffer ainda não enviado não sai.
3. Plano externo é recusado.
4. Se não há plano local permitido, `NO_PERMITTED_SPEECH_ADAPTER`, texto degradado, duplex marcado indisponível naquele destino. `voice_required` do MVP não vira false.

Troca de projeto reconstrói o context pack (jornada D da v0.3). Grants não herdam. Classe é reavaliada. Tool do agente anterior não segue.

## 6. Retenção (AQ-06)

Áudio bruto: `DO_NOT_STORE`. `CONTENT_REF` é efêmero e não é artefato de evidência. O audit guarda `content_sha256` e tamanho, não os bytes.

Transcrição: só se a política da organização, já configurada antes de produção, disser o período e a exclusão. Este pacote não inventa o número de dias. Sem essa configuração, a transcrição de produção não é retida. O contrato de teste pode usar fixture em memória, descartada ao fim do caso, e isso não é retenção de produto.

## 7. O que a voz não autoriza (AQ-11)

Fala, inclusive “aprovo”, não autentica e não confirma hard gate. Não há biometria no MVP. Preview e confirmação ficam em canal próprio (CMP-FD-O09, já existente, texto preservado e detalhado na fixture).

Codex conversacional é `origin=CODEX_READ_ONLY`. Não inicia review formal. Independência formal continua CMP-O-28, NOT RUN, não substituído por CMP-FD-O12.

## 8. Founder OS e prova de fornecedor

AQ-09 não decidida: nenhum compartilhamento de banco, código, memória ou sessão com Founder OS é implícito. Este delta não cria esse conector.

AQ-12 não decidida: sem prova ingerível, HELD, sem recibo fictício. Já é o §8C da v1.7. Repetido para não parecer que duplex ganhou exceção.
