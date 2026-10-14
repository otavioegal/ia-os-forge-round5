# Relatório de mudança — DELTA CONVERSATIONAL-MVP v0.2

**Estado:** DELTA CONVERSATIONAL-MVP v0.2 — CANDIDATE FOR CODEX REVIEW. Não é PASS. Não autoriza BUILD-00. Nenhum teste de software foi executado.

## O que não mudou

- Arquivos em `docs/planning/conversational-mvp/` (v0.1), em relação ao commit `cad1ac6d6bb8a970165ebd17ce1bff13d98af806`.
- Baseline v1.7 e o SHA `0c42373d583dec420348efd7bc0b8c6228a66f47`.
- Pareceres, inclusive `docs/reviews/PARECER-CODEX-CMP-v0.1-2026-10-13.md` e o prompt `docs/reviews/PROMPT-GROK-CMP-v0.2-CORRECTIVE.md`.
- 13 histórias CMP-S01..CMP-S13, sem renumerar F-001..F-041.
- Identificadores CMP-O-01..CMP-O-34. O texto de alguns foi emendado; os ids não.
- Voz obrigatória no MVP. Nenhum fallback passou a ser corte de escopo.
- Um único protocolo de dinheiro: FDP-16A v1.7. Nenhum recibo novo foi fabricado.

## O que a v0.2 acrescenta ou emenda

| Finding | Mudança |
|---|---|
| HIGH-01 | CMP-03 separa `codex_conversational` de `codex_review_executor`. Review formal exige `review_run_id` novo e principal `codex_reviewer`. Proíbe sessão, cache, score, verdict candidate, credencial, actor id e tool state do Builder. Conselho e Jarvis não iniciam o review. CMP-O-28 passa a exigir ausência dos quatro marcadores e principal distinto. F-017 não foi editado. |
| MEDIUM-01 | CMP-02 §7.2 fixa request, result e error de `speech.transcribe` e `speech.synthesize`, PARTIAL versus FINAL, encoding, mime, idioma, versão `cmp.speech.v0`, cancel CONFIRMED ou UNCONFIRMED, e a taxonomia retryable/terminal. CMP-O-36 cobre validade, falha de versão, cancelamento e permanência da voz. |
| MEDIUM-02 | CMP-01 e CMP-02 §9 substituem o retry único por RETRY_SAME_OPERATION, RECONCILIATION_REQUIRED, NEW_ATTEMPT e REPLAY_RESULT. CMP-O-15, CMP-O-16 e CMP-O-29 ganham o passo negativo de resultado incerto. CMP-O-35 percorre as cinco situações. Sem segundo ledger e sem recibo inventado. |
| MEDIUM-03 | CMP-O-31 exige `session_id`, `turn_id`, `agent_id`, `provider_id` e `model_id` em dois providers, soma só das operações, e estimativa distinta de custo confirmado. Sem tarifa de reunião. |
| LOW-01 do parecer CMP | `microphone_consent_id` é nulo quando o estado é NOT_GRANTED. `retention_policy_id` continua obrigatório. CMP-O-19 cobre a abertura só texto. Captura e STT seguem zerados sem GRANTED. |

## Fora do diff normativo

O verificador da v0.1 ganha apenas permissão de worktree para esta pasta nova, para continuar executável. O texto da v0.1 não entra nesse diff.

AQ-01 a AQ-12 continuam abertas. O quadro em CMP-OPEN-QUESTIONS recomenda quais precisam de decisão antes da integração e quais podem esperar. Nenhuma foi marcada como tomada.
