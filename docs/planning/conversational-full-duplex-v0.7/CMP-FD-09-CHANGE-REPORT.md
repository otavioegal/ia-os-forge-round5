# CMP-FD-09 v0.7 — Change report

**Estado:** PROPOSTA. Não é PASS. Não edita v0.1, v0.2, v0.3, v0.4, v0.5, v0.6, FDP-16A v1.7, CMP v0.3, ata, ADR nem parecer.

A norma da v0.6 já dizia: exatamente um campo ACK null é `422 ACK_SCOPE_MISMATCH`; os dois null são nenhum ack, sem efeito; só depois vem stream não alocado. O checker da v0.6 só tinha o ou-exclusivo. Com os dois campos null, `ack_stream_id` caía em `not in allocated` e o resultado virava `ACK_STREAM_UNALLOCATED`. A fixture só trazia `FX03-PAIR-INVALID`, sequence preenchida e stream null.

Esta pasta não muda essa ordem. O checker agora devolve `NO_ACK` no par null, antes de stream não alocado, e devolve `ACK_SCOPE_MISMATCH` nas duas direções. `NO_ACK` não é 422. Nenhuma dessas três linhas altera o high-water, abre microfone ou move dinheiro.

O checker não cobre todos os eventos. Cobre as linhas da fixture. A linha `FX03-NO-ACK` é explícita.

Regressão continua sem escrita. Aceite continua só para cima. As duas ordens da corrida continuam terminando em 2. Isso é checagem de inteiros da fixture, não o lock da v0.6.

HIGH-03 e NEW-MEDIUM-06 permanecem CANDIDATE. LOW-01 permanece OPEN BLOCKING DoR. Nada disto foi migration, oráculo, provider, gasto ou BUILD-00. `forge.conversation.delta.v4` permanece desligada. A v3 não é integrada.
