# Questões abertas — DELTA CONVERSATIONAL-MVP v0.3

**Estado:** DELTA CONVERSATIONAL-MVP v0.3 — CANDIDATE FOR CODEX REVIEW. DRAFT / NOT APPROVED / NOT READY FOR BUILD / NO BUILD-00 AUTHORIZATION. Nenhuma questão abaixo está decidida por este pacote. Não autoriza BUILD-00. Nenhuma linha do quadro é ata do Founder.

A decisão funcional sobre voz, paridade de agentes e Conselho já está tomada e não é reaberta aqui. As questões abaixo são arquitetura de implementação. Enquanto estiverem abertas, a especificação proíbe contornar o ledger e proíbe escolher fornecedor.

O parecer CMP v0.2 separou quais AQ bloqueiam a integração normativa à baseline e quais podem esperar. Esta v0.3 não decide nenhuma delas. A tabela para deliberação humana está em [CMP-AQ-FOUNDER-DECISIONS.md](CMP-AQ-FOUNDER-DECISIONS.md). Ela repete a recomendação e não é ata.

## Quadro executivo — ainda aberto

| AQ | Antes da integração à baseline | Recomendação deste pacote, não decisão | Risco se a integração ignorar a questão |
|---|---|---|---|
| AQ-01 | Decisão humana exigida | Ator `conversation_router` e comando cujo efeito de reserva é o da transação já existente. O roteador não finge ser `coding_engine`. | Gasto fora do gateway, ou um segundo ledger |
| AQ-02 | Decisão humana exigida | Uma Task âncora por sessão, fora do DAG de build, sem deploy, terminal ou vault. Não anular `task_id`. | Operação sem task, ou conversa misturada ao build |
| AQ-03 | Decisão humana exigida, junto com FDP-15 | `speech.transcribe` e `speech.synthesize` como TOOL. Sem quarta família. | Contradição com as três famílias do rascunho |
| AQ-04 | Pode esperar | Deny-by-default. Nenhum vendor. Não entra na allowlist de engines de código. | Escolha implícita de modelo ou de OpenRouter |
| AQ-05 | Decisão humana exigida | Rótulos PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED. Projeto não é PUBLIC até decisão contrária. Egress externo negado para CONFIDENTIAL e RESTRICTED. | Áudio classificado sai para provider |
| AQ-06 | Decisão humana exigida | Áudio bruto `DO_NOT_STORE`, salvo opt-in futuro. Transcrição conforme política da org. Sem prazo eterno. | Áudio retido sem regra |
| AQ-07 | Decisão humana exigida | Meia-duplex com barge-in local satisfaz o pedido de baixa latência neste delta. Full-duplex não está escolhido. Os milissegundos são default de planejamento, não SLA. | Voz adiada, ou um SLA inventado |
| AQ-08 | Decisão humana exigida | Ativação explícita ou push-to-talk. Escuta contínua não é o default. | Microfone sempre ligado sem consentimento |
| AQ-09 | Pode esperar | Sem banco, sessão ou código compartilhado com Founder OS até baseline comum. | Acoplamento indevido |
| AQ-10 | Decisão humana exigida | O teto é o ledger existente. Sem envelope paralelo e sem preço de sessão. | Tarifa oculta de Conselho |
| AQ-11 | Decisão humana exigida | Biometria fora do MVP. Gravação não autentica. | Áudio tratado como identidade |
| AQ-12 | Pode esperar | Sem prova ingerível, a reserva permanece HELD e não há recibo inventado. O vendor pode ser escolhido depois. | Recibo fabricado para “fechar” custo de voz |

AQ-04, AQ-09 e AQ-12 ficam diferíveis só enquanto deny-by-default, a proibição de acoplamento e a regra HELD permanecerem vinculantes. Diferir não as aprova e não escolhe fornecedor.

## AQ-01 — Quem reserva gasto conversacional

O comando `InvokeCapability` da v1.7 é exclusivo de `coding_engine via gateway`. O roteador de conversa não é coding engine e não pode fingir que é.

Proposta: um ator futuro `conversation_router` e um comando cujo efeito de reserva é o mesmo da transação já especificada, sem copiar um segundo ledger. Settlement e release continuam sendo os comandos atuais, com prova só de `forge.provider_ingest`.

Sem essa decisão, implementação não pode chamar provider por fora do gateway.

## AQ-02 — Âncora de task_id

`operation.task_id` é NOT NULL na v1.7. Uma conversa não é uma task de build. Este delta não torna a coluna nula e rejeita uma segunda tabela de dinheiro.

Proposta: uma Task de sistema por sessão, com propósito futuro `CONVERSATION_ANCHOR`, fora do DAG de build e sem deploy, terminal ou vault.

## AQ-03 — Família do adapter de voz

O rascunho FDP-15, ainda não aprovado, lista três famílias: Engine, Model, Tool. Uma quarta família contradiria essa frase.

Proposta: `speech.transcribe` e `speech.synthesize` como capabilities TOOL. `conversation.respond` permanece MODEL.

## AQ-04 — Modelo que responde

Nenhum modelo conversacional foi escolhido. Grok e OpenRouter continuam fora da allowlist de engines de código do FDP-16 até um grant próprio. OpenRouter segue opcional. Esta questão não é um grant.

## AQ-05 — Rótulos de classificação

Os extratos nomeiam o campo `data_classification` e não fixam o conjunto de rótulos nesta árvore.

Proposta: PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED. Áudio CONFIDENTIAL e RESTRICTED não sai para provider externo. Conteúdo de projeto, até decisão contrária, não é tratado como PUBLIC.

## AQ-06 — Retenção padrão

Proposta: áudio bruto `DO_NOT_STORE`, salvo opt-in futuro. Transcrição retida conforme política da org, apagável, sem prazo eterno implícito. Nenhum número de dias foi medido ou congelado.

## AQ-07 — Áudio de baixa latência

A decisão pede contratos de STT/TTS e áudio de baixa latência. A fase do addendum que empurrava áudio em tempo real foi substituída no que adia voz.

Proposta deste pacote: meia-duplex com STT/TTS, stream se o adapter declarar, interrupção local imediata. Não há fornecedor full-duplex. Os milissegundos em CMP-02 são default de planejamento, não SLA medido.

Confirmar se isso satisfaz a decisão ou se full-duplex é obrigatório antes do primeiro teste.

## AQ-08 — Microfone sempre ligado

Proposta: ativação explícita ou push-to-talk. Escuta contínua não é o default do MVP.

## AQ-09 — Founder OS e Conselho Consultivo

Reuso visual é referência. Não há código compartilhado, banco compartilhado nem sessão compartilhada até existir baseline comum aprovada.

## AQ-10 — Orçamento

Proposta: o teto é o ledger já existente do projeto (`spent + reserved <= limit`). Não há envelope monetário paralelo nem preço de sessão neste delta.

## AQ-11 — Biometria de voz

Proposta: fora do MVP. Gravação não autentica e não renova assurance.

## AQ-12 — Prova de custo do fornecedor de voz

Adapter não captura prova. Se `receipt_query` for ABSENT e não houver atestação, a operação segue FDP-16A §8C: reserva permanece HELD, sem recibo inventado. Proposta: um provider de voz sem caminho de prova ingerível não recebe regra mais fraca.

Nenhum vendor foi eliminado por nome porque nenhum foi escolhido.
