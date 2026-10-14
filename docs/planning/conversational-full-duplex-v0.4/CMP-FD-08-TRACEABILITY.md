# CMP-FD-08 v0.4 — Rastreabilidade

**Estado:** PROPOSTA. Não é PASS. Linhas abaixo foram lidas nesta pasta antes do commit. Se o Codex reler e a linha divergir, vale o texto, não esta tabela.

Fontes que esta pasta não edita:

| Fonte | Uso |
|---|---|
| `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.3-2026-10-14.md` | FAIL DOCUMENT-ONLY do SHA `2fe0b0b2b75f2fc1430f639839e2d29d563f6dcb` |
| `docs/reviews/PROMPT-GROK-FULL-DUPLEX-v0.4-CORRECTIVE.md` | ordem de reparo |
| `docs/planning/conversational-full-duplex-v0.3/` | pacote auditado, intacto |
| FDP-16A v1.7 | protocolo financeiro; `:322-324` ainda permite actual > estimate no Build genérico |
| FDP-15 histórico | famílias ENGINE, MODEL, TOOL; sem família nova |
| CMP v0.3 `cmp.speech.v0` | crosswalk, não substituição |
| Ata Founder e ADR AQ-07 | decisões humanas preservadas |

## Achados para texto v0.4

| Achado | Causa no parecer | Texto proposto | Negativo |
|---|---|---|---|
| NEW-HIGH-04 | settlement só limitava o estimate | CMP-FD-01:18-87 | O41, O42 |
| NEW-HIGH-03 | Operation e Reservation por id global | CMP-FD-01:89-110; CMP-FD-13:9-10 | O37-S, O37-B, O37-T, O37-O, O37-R, O37-X |
| NEW-MEDIUM-01 | CAS antes do `command_id` | CMP-FD-01:48 e CMP-FD-01:114-139 | O43, O44, O45 |
| HIGH-03 | sem `HELLO_ACK_ERROR`, ACK incompleto | CMP-FD-02:50-77, CMP-FD-02:96-114, CMP-FD-02:153-311 | O46, O47, O39 |
| NEW-MEDIUM-04 | nome exigido e proibido | CMP-FD-02:129-136; CMP-FD-04:19; CMP-FD-06:12 | O48 |
| NEW-MEDIUM-05 | digest só no Markdown | fixtures e `tools/check_fd_fx01_digests.py`; CMP-FD-02:116-127 | O39 |
| NEW-MEDIUM-03 | `mic[i]=16000` apagava o eco | CMP-FD-07:144-187 | O28, O51, O52 |
| NEW-MEDIUM-06 | unique talvez global | CMP-FD-01:145-151; CMP-FD-13:11 | O49, O50 |
| LOW-01 | pessoa e effort inventáveis | CMP-FD-07:7-23 | história marcada Ready sem pessoa |

## Fechados pelo Codex e só repetidos

| Achado | Onde a v0.4 o repete, sem reabrir |
|---|---|
| HIGH-01 | CMP-FD-01:7-16, lock do Build antes da leitura monetária |
| HIGH-02 | CMP-FD-02:81-90; CMP-FD-07:25-39; CMP-FD-06:6-10 |
| NEW-HIGH-01 | CMP-FD-01:12-13, um root por org e projeto |
| NEW-HIGH-02 | CMP-FD-01:10 e CMP-FD-01:43 |
| NEW-MEDIUM-02 | CMP-FD-02:81-92, seis carimbos e `PLAYBACK_SPAN` |
| MEDIUM-01 | CMP-FD-03 inteiro |
| MEDIUM-02 | CMP-FD-04:9-19 |
| MEDIUM-03 | CMP-FD-04:21-23 |
| MEDIUM-04 | CMP-FD-05 inteiro |
| MEDIUM-05 | CMP-FD-06:14-31, aceite PENDING CALIBRATION |

## Oráculos

| ID | Onde | Execução |
|---|---|---|
| O01..O36, O38, O40 | critério da v0.3, subordinado à ordem desta v0.4 quando falam de CAS ou de fatia | NOT RUN |
| O37 e subcasos S, B, T, O, R, X | CMP-FD-07:65-80 | NOT RUN |
| O39 | CMP-FD-07:41 | NOT RUN |
| O41, O42 | CMP-FD-07:43-63 | NOT RUN |
| O43, O44, O45 | CMP-FD-07:82-110 | NOT RUN |
| O46, O47, O48 | CMP-FD-07:112-142 | NOT RUN |
| O28 reescrito, O51, O52 | CMP-FD-07:144-187 | NOT RUN |
| O49, O50 | CMP-FD-07:189-205 | NOT RUN |
| 91 v1.7 e 36 CMP-O | fora desta pasta | NOT RUN |
| CMP-O-28 | review formal, independente de CMP-FD-O28 | NOT RUN |

## Comandos novos, só no papel

`AmendSessionSlice` está em CMP-FD-01:76-83. Não liquida. `RecordReceipt` conversacional está em CMP-FD-01:38-61. `OpenConversationalAnchor` continua sem `budget_limit_minor`.
