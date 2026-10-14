# Fechamento documental proposto — DELTA CONVERSATIONAL-MVP v0.2

**Estado:** DELTA CONVERSATIONAL-MVP v0.2 — CANDIDATE FOR CODEX REVIEW. Não é PASS. Não é parecer. Não autoriza BUILD-00.
**Nenhum finding abaixo está FECHADO por este pacote.** A frase correta é: correção especificada, teste NOT RUN, auditoria Codex ainda não feita sobre a v0.2.

Fonte dos findings: `docs/reviews/PARECER-CODEX-CMP-v0.1-2026-10-13.md`. Esse arquivo não foi alterado.

## HIGH-01 — independência do reviewer

| | |
|---|---|
| Correção | CMP-03 §8.1 e §8.2; deny `review.execute` no registro; CMP-S11; CMP-O-28 |
| Regra | Review formal cria `review_run_id` novo, principal `codex_reviewer`, contexto só com entradas admitidas pelo review gate. Não reutiliza sessão, cache, score, verdict candidate, credencial, actor id ou tool state do Builder. Chat read-only não é o executor. Conselho e Jarvis não contornam isso. |
| Oracle | CMP-O-28. Fixture com BUILDER_SCRATCH_ONLY, BUILDER_VERDICT_CANDIDATE, BUILDER_SESSION_CACHE e BUILDER_ACTOR_9f3a. PASS só se nenhum chega ao review formal e o principal não é o Builder. FAIL se houver reutilização. |
| Não feito | Teste, emenda de F-017, emenda de parecer, PASS. |

Estado: CORREÇÃO DOCUMENTAL ENTREGUE — AGUARDA AUDITORIA. NÃO ESTÁ FECHADO POR ESTE PACOTE.

## MEDIUM-01 — schemas STT/TTS

| | |
|---|---|
| Correção | CMP-02 §7.2 |
| Regra | `cmp.speech.v0` com request, result e error; PARTIAL não commita; FINAL commita; encoding e mime; idioma; cancel_state CONFIRMED ou UNCONFIRMED; versão incompatível é SPEECH_UNSUPPORTED_VERSION e não há downgrade. |
| Oracle | CMP-O-36, mais a permanência de voz em CMP-O-15 e CMP-O-16. |
| Não feito | Escolha de fornecedor, teste, medição de latência. |

Estado: CORREÇÃO DOCUMENTAL ENTREGUE — AGUARDA AUDITORIA. NÃO ESTÁ FECHADO POR ESTE PACOTE.

## MEDIUM-02 — retry depois do dispatch

| | |
|---|---|
| Correção | CMP-01 jornada G; CMP-02 §9 |
| Regra | Antes do dispatch, a mesma operação pode seguir uma vez. Resultado incerto ou HELD: sem redispatch, reconciliação. NO_EFFECT conclusivo: nova tentativa só com novo turn e novo operation_ref. Efeito conclusivo: replay, sem nova chamada. |
| Oracle | Passo negativo em CMP-O-15, CMP-O-16 e CMP-O-29. Tabela inteira em CMP-O-35. |
| Não feito | Liberação de reserva sem prova NO_EFFECT. Recibo inventado. Segundo ledger. |

Estado: CORREÇÃO DOCUMENTAL ENTREGUE — AGUARDA AUDITORIA. NÃO ESTÁ FECHADO POR ESTE PACOTE.

## MEDIUM-03 — custo por sessão, modelo e provider

| | |
|---|---|
| Correção | CMP-04 §7; CMP-O-31 |
| Regra | Cada operação externa carrega session, turn, agent e provider ou model. Dois speakers usam P1/M1 e P2/M2. A soma da sessão é a soma das operações. Estimativa não é custo confirmado. Não há meeting fee. |
| Oracle | CMP-O-31. CMP-O-29 e CMP-O-30 permanecem para duplicidade e deny. |
| Não feito | Cifra medida, preço de vendor, teste. |

Estado: CORREÇÃO DOCUMENTAL ENTREGUE — AGUARDA AUDITORIA. NÃO ESTÁ FECHADO POR ESTE PACOTE.

## LOW-01 — consent_id na abertura só texto

| | |
|---|---|
| Correção | CMP-02 §4.1; CMP-03 §4; CMP-O-19 |
| Regra | `microphone_consent_id` nulo se e só se o estado é NOT_GRANTED. `retention_policy_id` é outro campo e continua obrigatório. Sem GRANTED, zero bytes e zero STT. A voz continua oferecida. |
| Não feito | Política de retenção aprovada pelo Founder (AQ-06 continua aberta). Teste. |

Estado: CORREÇÃO DOCUMENTAL ENTREGUE — AGUARDA AUDITORIA. NÃO ESTÁ FECHADO POR ESTE PACOTE.

## Condição 6 do parecer

AQ-01, AQ-02, AQ-03, AQ-05, AQ-06, AQ-07, AQ-08, AQ-10 e AQ-11 continuam sem decisão humana. AQ-04, AQ-09 e AQ-12 continuam diferíveis sob deny-by-default, sem acoplamento e com reserva HELD. O quadro está em CMP-OPEN-QUESTIONS. Esta condição não foi “cumprida” por recomendação do builder.
