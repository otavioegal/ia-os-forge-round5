# CMP-FD-08 v0.2 — Rastreabilidade

**Estado:** mapa documental. Não é evidência de execução.

## 1. Decisões do Founder

| ID | Estado | Onde este pacote obedece | O que não faz |
|---|---|---|---|
| AQ-01 | APPROVED | CMP-FD-01 §2 `ReserveConversationalCapability` | não edita o enum histórico; não declara o comando já vigente |
| AQ-02 | APPROVED | CMP-FD-01 §3 âncora com `build_id` NOT NULL, fora do DAG | não anula a FK; não autoriza deploy/terminal/vault |
| AQ-03 | APPROVED | TOOL `speech.*`, MODEL `conversation.respond`, três famílias | não cria quarta família; não aprova FDP-15 |
| AQ-05 | APPROVED | CMP-FD-04 §5 matriz | não escolhe fornecedor |
| AQ-06 | APPROVED | CMP-FD-04 §6 `DO_NOT_STORE` | não inventa prazo de retenção |
| AQ-07 | APPROVED | contrato duplex e predicado de overlap | não aprova SLA; não rebaixa a half-duplex |
| AQ-08 | APPROVED | epochs e mic só na sessão ativa | não autoriza escuta de fundo |
| AQ-10 | APPROVED | mesmo §8A, um movimento, sem segundo ledger | não inventa teto numérico de projeto |
| AQ-11 | APPROVED | CMP-FD-O09, sem biometria | não move hard gate para a voz |
| AQ-04 | UNDECIDED | deny-by-default, nenhum vendor | não seleciona SDK |
| AQ-09 | UNDECIDED | nenhum conector Founder OS | não compartilha memória |
| AQ-12 | UNDECIDED | HELD sem prova, §8C | não fabrica recibo |

## 2. Findings do parecer v0.1

| Finding | Material proposto | Oráculos | Fechado pelo autor? |
|---|---|---|---|
| HIGH-01 | CMP-FD-01 | O15 O16 O17 O18 O30 O31 | não |
| HIGH-02 | CMP-FD-02 §6, CMP-FD-07 §3–§4, O01 O13 O14 | esses | não |
| HIGH-03 | CMP-FD-02 inteiro, O32 | esses | não |
| MEDIUM-01 | CMP-FD-03, O03 O34 | esses | não |
| MEDIUM-02 | CMP-FD-04 §1–§3, O05 O06 O19 O20 O21 O22 | esses | não |
| MEDIUM-03 | CMP-FD-04 §4–§5, O07 O23 O24 O25 O26 | esses | não |
| MEDIUM-04 | CMP-FD-05, O04 O27 | esses | não |
| MEDIUM-05 | CMP-FD-06, O29 | esses | não |
| LOW-01 | CMP-FD-07 histórias com DoR NOT MET e fixtures materializadas | O01–O34 como especificação | não |

## 3. Contratos que não se movem

| Contrato | Uso |
|---|---|
| FDP-16A §3.2 `build_id` NOT NULL | satisfeito por Build âncora, não por null |
| FDP-16A §3.4 `task_id` NOT NULL | operation aponta para a âncora |
| FDP-16A §4.1 enum histórico | não editado; ator novo só no delta |
| FDP-16A §5 `InvokeCapability` | continua `coding_engine via gateway` |
| FDP-16A §8A–§8C | único protocolo de dinheiro |
| FDP-15 três famílias | preservadas |
| `cmp.speech.v0` | invoke STT/TTS; duplex não o sobrescreve |
| CMP-02 v0.3 §9 | retry; duplex não o substitui |
| CMP-O-28 | independência; O12 só referencia |

## 4. Contagem de oráculos

| Conjunto | Quantidade | Estado |
|---|---|---|
| v1.7 históricos | 91 | NOT RUN |
| CMP-O v0.3 | 36 | NOT RUN, evidence ABSENT |
| CMP-FD-O01..O12 | 12 | NOT RUN, evidence ABSENT, aceite reespecificado |
| CMP-FD-O13..O34 | 22 | NOT RUN, evidence ABSENT |

Não há renumeração dos 91, dos 36 nem dos 12.
